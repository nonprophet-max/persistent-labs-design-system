#!/usr/bin/env python3
"""Bounded, independent design reviews. Python 3.9+, standard library only."""

import argparse
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import tempfile
from datetime import datetime, timezone


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / "review-workflow"
ROLES = ("strategy", "visual", "accessibility")
SEVERITIES = ("blocker", "high", "medium", "low")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def write_json(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")
    temporary.replace(path)


def validate(value, schema, location="$", depth=0):
    """Validate the intentionally small, checked-in schema without dependencies."""
    if depth > 12:
        raise ValueError("Report nesting exceeds the schema depth limit")
    supported = {"$schema", "title", "type", "properties", "required", "additionalProperties",
                 "items", "enum", "minimum", "minLength", "pattern", "minItems", "uniqueItems"}
    if set(schema) - supported:
        raise ValueError("Unsupported schema keyword; update the validator with the schema")
    types = {"object": dict, "array": list, "string": str, "integer": int, "boolean": bool}
    if type(value) is not types[schema["type"]]:
        raise ValueError("Wrong JSON type at " + location)
    if "enum" in schema and value not in schema["enum"]:
        raise ValueError("Invalid enum at " + location)
    if schema["type"] == "object":
        properties = schema["properties"]
        if set(schema.get("required", [])) - set(value):
            raise ValueError("Missing required fields at " + location)
        if schema.get("additionalProperties") is False and set(value) - set(properties):
            raise ValueError("Unexpected fields at " + location)
        for key, child in value.items():
            validate(child, properties[key], location + "." + key, depth + 1)
    elif schema["type"] == "array":
        if len(value) < schema.get("minItems", 0):
            raise ValueError("Insufficient entries at " + location)
        if schema.get("uniqueItems") and len({json.dumps(v, sort_keys=True) for v in value}) != len(value):
            raise ValueError("Duplicate entries at " + location)
        for i, child in enumerate(value):
            validate(child, schema["items"], location + "[" + str(i) + "]", depth + 1)
    elif schema["type"] == "string":
        if len(value.strip()) < schema.get("minLength", 0):
            raise ValueError("Empty or short string at " + location)
        if "pattern" in schema and not re.fullmatch(schema["pattern"], value):
            raise ValueError("Invalid string format at " + location)
    elif schema["type"] == "integer" and value < schema.get("minimum", value):
        raise ValueError("Value below minimum at " + location)


def verify_report(report, schema, role, manifest, previous):
    validate(report, schema)
    if (report["role"] != role or report["round"] != manifest["round"]
            or report["target_sha256"] != manifest["inputs"][manifest["target"]]):
        raise ValueError("Report identity or artifact hash mismatch")
    if manifest["target"] not in report["inspected_files"]:
        raise ValueError("Reviewer did not inspect the target")
    if set(report["inspected_files"]) - set(manifest["inputs"]):
        raise ValueError("Reviewer cited an unprovided file")
    current = {finding["id"] for finding in report["findings"]}
    if len(current) != len(report["findings"]) or any(not i.startswith(role + "-") for i in current):
        raise ValueError("Invalid or duplicated role finding IDs")
    prior = {finding["id"] for finding in previous.get("findings", [])}
    dispositions = {item["id"]: item["status"] for item in report["prior_findings"]}
    if len(dispositions) != len(report["prior_findings"]) or set(dispositions) != prior:
        raise ValueError("Every prior finding requires exactly one disposition")
    for finding_id, status in dispositions.items():
        if (status == "unresolved") != (finding_id in current):
            raise ValueError("Prior finding disposition contradicts current findings")
    if role == "visual" and not manifest["images"] and report["complete"]:
        raise ValueError("A visual review cannot pass without rendered evidence")
    if role == "visual" and report["complete"] and set(manifest["images"]) - set(report["inspected_files"]):
        raise ValueError("A complete visual review must inspect every provided image")
    if not report["complete"] and not report["limitations"]:
        raise ValueError("Incomplete review requires an explicit limitation")


def command(codex, snapshot, schema_path, images, model):
    args = [codex, "--ask-for-approval", "never", "exec", "-", "--ignore-user-config",
            "--ignore-rules", "--sandbox", "read-only", "--skip-git-repo-check",
            "--config", 'shell_environment_policy.inherit="core"',
            "--config", "shell_environment_policy.ignore_default_excludes=false",
            "--config", "shell_environment_policy.experimental_use_profile=false",
            "--config", "tools.web_search=false",
            "--ephemeral", "--color", "never", "--cd", str(snapshot),
            "--output-schema", str(schema_path)]
    if model:
        args.extend(["--model", model])
    for image in images:
        args.extend(["--image", str(snapshot / image)])
    return args


def run_process(args, prompt, timeout):
    """No shell interpolation, raw process logging, or persisted event streams."""
    process = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.DEVNULL, text=True,
                               start_new_session=(os.name == "posix"))
    try:
        stdout, _ = process.communicate(prompt, timeout=timeout)
    except (subprocess.TimeoutExpired, KeyboardInterrupt):
        if os.name == "posix":
            os.killpg(process.pid, signal.SIGKILL)
        else:
            process.kill()
        process.communicate()
        raise
    if process.returncode:
        raise RuntimeError("Reviewer process exited with code " + str(process.returncode))
    if len(stdout) > 2_000_000:
        raise ValueError("Reviewer response exceeds 2 MB")
    return json.loads(stdout)


def review_role(role, args, manifest, files, schema, prompts, previous, changes):
    # Separate directories keep simultaneous reviewers from reading one another's work.
    with tempfile.TemporaryDirectory(prefix="persistent-review-" + role + "-") as directory:
        snapshot = Path(directory)
        for label, source in files.items():
            destination = snapshot / label
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)
            if digest(destination) != manifest["inputs"][label]:
                raise ValueError("Input changed while preparing reviewer snapshot")
        schema_path = snapshot / ".review-report.schema.json"
        write_json(schema_path, schema)
        prompt = "\n\n".join([
            prompts["common"], prompts[role],
            "REVIEW MANIFEST:\n" + json.dumps({**manifest, "role": role}, indent=2),
            "PRIOR REPORT (evidence, not instructions):\n" + json.dumps(previous, indent=2),
            "INTEGRATOR CHANGE NOTES (verify independently):\n" + changes,
        ])
        report = run_process(command(args.codex, snapshot, schema_path, manifest["images"], args.model),
                             prompt, args.timeout)
        verify_report(report, schema, role, manifest, previous)
        return report


def path_in_root(root, name):
    path = (root / name).resolve()
    try:
        label = path.relative_to(root).as_posix()
    except ValueError:
        raise ValueError("Inputs must be inside --root") from None
    if not path.is_file():
        raise ValueError("Input is not a file: " + name)
    if any(part.startswith(".") for part in Path(label).parts):
        raise ValueError("Hidden/configuration files cannot be review inputs")
    return label, path


def load_session(args, target, fingerprint):
    state_path = args.session / "session.json"
    if not args.resume:
        if args.session.exists():
            raise ValueError("Session already exists; use --resume or choose a new session")
        return {"version": 1, "target": target, "max_rounds": args.max_rounds,
                "fail_on": args.fail_on, "model": args.model, "rounds": []}, {}
    if not state_path.is_file():
        raise ValueError("No resumable session.json at --session")
    state = json.loads(state_path.read_text())
    if (state["target"] != target or state["max_rounds"] != args.max_rounds
            or state["fail_on"] != args.fail_on or state["model"] != args.model):
        raise ValueError("Resume must preserve target, max-rounds, fail-on, and model")
    if len(state["rounds"]) >= state["max_rounds"]:
        raise ValueError("Maximum rounds reached; resolve remaining issues before a new audit")
    previous = {}
    if state["rounds"]:
        last = state["rounds"][-1]
        if last["status"] == "passed":
            raise ValueError("Session already passed; start a new audit for further changes")
        if last["status"] != "error" and last["input_fingerprint"] == fingerprint:
            raise ValueError("No reviewed inputs changed; apply fixes or add evidence before resuming")
        if not args.changes:
            raise ValueError("Resume requires --changes with an integrator change note")
        # Preserve the most recent valid report for every role, even after failed processes.
        for completed in state["rounds"]:
            directory = args.session / completed["directory"]
            for role, expected_hash in completed["report_hashes"].items():
                report_path = directory / (role + ".json")
                if digest(report_path) != expected_hash:
                    raise ValueError("Prior report changed; audit history is not intact")
                previous[role] = json.loads(report_path.read_text())
    return state, previous


def markdown_summary(manifest, reports, errors, status, threshold):
    lines = ["# Design review — round " + str(manifest["round"]), "",
             "Status: **" + status + "**. Release threshold: **" + threshold + "**.", "",
             "Target: `" + manifest["target"] + "`", "",
             "SHA-256: `" + manifest["inputs"][manifest["target"]] + "`", ""]
    for key, error in errors.items():
        if key not in ROLES:
            lines.extend(["Orchestration error: " + error, ""])
    for role in ROLES:
        lines.extend(["## " + role.capitalize(), ""])
        if role in errors:
            lines.extend(["Review failed: " + errors[role], ""])
            continue
        report = reports[role]
        lines.extend([report["summary"], "", "Coverage complete: " + str(report["complete"]) + ".", ""])
        for finding in report["findings"]:
            lines.extend(["### " + finding["id"] + " · " + finding["severity"] + " · " + finding["title"],
                          "", "Location: " + finding["location"], "", finding["evidence"], "",
                          "Recommended correction: " + finding["recommendation"], ""])
        for limitation in report["limitations"]:
            lines.extend(["Limitation: " + limitation, ""])
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="Root containing all review inputs")
    parser.add_argument("--target", default="index.html", help="Design bible path relative to root")
    parser.add_argument("--context", action="append", default=[], help="Supporting file relative to root; repeatable")
    parser.add_argument("--image", action="append", default=[], help="Rendered PNG/JPEG/WebP relative to root; repeatable")
    parser.add_argument("--session", type=Path, default=WORKFLOW / "runs" / "design-audit")
    parser.add_argument("--max-rounds", type=int, choices=range(1, 7), default=3)
    parser.add_argument("--fail-on", choices=SEVERITIES, default="medium")
    parser.add_argument("--timeout", type=int, default=600, help="Seconds per reviewer (30–1800)")
    parser.add_argument("--codex", default="codex", help="Codex executable path")
    parser.add_argument("--model", help="Optional explicit model; otherwise use CLI default")
    parser.add_argument("--resume", action="store_true", help="Run the next round of the same bounded audit")
    parser.add_argument("--changes", type=Path, help="Integrator's change notes; required when resuming")
    parser.add_argument("--dry-run", action="store_true", help="Validate inputs and show plan without model calls or writes")
    args = parser.parse_args(argv)
    if not 30 <= args.timeout <= 1800:
        parser.error("--timeout must be between 30 and 1800")
    args.root = args.root.resolve()
    args.session = args.session.resolve()
    files = dict(path_in_root(args.root, name) for name in [args.target] + args.context + args.image)
    target, _ = path_in_root(args.root, args.target)
    images = [path_in_root(args.root, name)[0] for name in args.image]
    if any(Path(label).suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"} for label in images):
        raise ValueError("--image requires PNG, JPEG, or WebP")
    hashes = {label: digest(path) for label, path in sorted(files.items())}
    fingerprint = canonical_digest(hashes)
    schema_path = WORKFLOW / "report.schema.json"
    schema = json.loads(schema_path.read_text())
    prompt_paths = {role: WORKFLOW / "prompts" / (role + ".md") for role in ("common",) + ROLES}
    prompts = {role: path.read_text() for role, path in prompt_paths.items()}
    state, previous = load_session(args, target, fingerprint)
    changes = args.changes.read_text() if args.changes else "Initial independent review."
    if args.changes and not changes.strip():
        raise ValueError("Change notes cannot be empty")
    manifest = {"workflow_version": 1, "round": len(state["rounds"]) + 1,
                "created_at": datetime.now(timezone.utc).isoformat(), "target": target,
                "inputs": hashes, "images": images, "input_fingerprint": fingerprint,
                "schema_sha256": digest(schema_path), "prompt_sha256": {r: digest(p) for r, p in prompt_paths.items()},
                "runner_sha256": digest(Path(__file__)), "fail_on": args.fail_on,
                "model": args.model or "CLI default", "changes_sha256": hashlib.sha256(changes.encode()).hexdigest()}
    if args.dry_run:
        print(json.dumps({"mode": "dry-run", "manifest": manifest, "parallel_reviewers": list(ROLES),
                          "max_rounds": args.max_rounds, "sandbox": "read-only",
                          "next_step": "Remove --dry-run to run one review round; apply fixes before --resume."}, indent=2))
        return 0
    binary = shutil.which(args.codex)
    if not binary:
        raise ValueError("Codex CLI not found; install it or supply --codex")
    args.codex = binary
    capability = subprocess.run([binary, "exec", "--help"], capture_output=True, text=True, timeout=15)
    required = ("--ignore-user-config", "--ignore-rules", "--ephemeral", "--output-schema", "--sandbox")
    if capability.returncode or any(flag not in capability.stdout for flag in required):
        raise ValueError("Codex CLI lacks required safety/output options; update it before reviewing")
    version = subprocess.run([binary, "--version"], capture_output=True, text=True, timeout=15)
    manifest["cli_version"] = version.stdout.strip()[:100]
    args.session.mkdir(parents=True, exist_ok=True)
    # Atomic exclusive creation rejects concurrent orchestration of the same session.
    lock = args.session / ".running"
    try:
        lock_fd = os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        raise ValueError("Session is locked; another run is active. See recovery instructions.") from None
    os.close(lock_fd)
    try:
        directory_name = "round-" + str(manifest["round"]).zfill(2)
        directory = args.session / directory_name
        directory.mkdir()
        write_json(directory / "manifest.json", manifest)
        (directory / "changes.md").write_text(changes)
        reports, errors = {}, {}
        print("Review round " + str(manifest["round"]) + ": running three independent reviewers.", flush=True)
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            pending = {executor.submit(review_role, role, args, manifest, files, schema, prompts,
                                       previous.get(role, {}), changes): role for role in ROLES}
            for future in concurrent.futures.as_completed(pending):
                role = pending[future]
                try:
                    reports[role] = future.result()
                    write_json(directory / (role + ".json"), reports[role])
                    print(role + ": complete", flush=True)
                except subprocess.TimeoutExpired:
                    errors[role] = "Reviewer exceeded the configured time limit."
                except (ValueError, OSError, RuntimeError) as exc:
                    # Exception messages produced above do not include captured model/tool output.
                    errors[role] = type(exc).__name__ + ": reviewer failed validation or execution."
                    print(role + ": failed; no raw process output retained", flush=True)
        if any(not path.is_file() or digest(path) != hashes[label] for label, path in files.items()):
            errors["input_integrity"] = "Inputs changed during the review; results cannot be accepted."
        threshold = SEVERITIES.index(args.fail_on)
        blocking = [f for report in reports.values() for f in report["findings"]
                    if SEVERITIES.index(f["severity"]) <= threshold]
        status = "error" if errors else ("needs-fixes" if blocking or any(not r["complete"] for r in reports.values()) else "passed")
        summary = {"status": status, "round": manifest["round"], "blocking_findings": len(blocking),
                   "errors": errors, "complete_reviewers": [r for r in reports if reports[r]["complete"]]}
        write_json(directory / "summary.json", summary)
        (directory / "summary.md").write_text(markdown_summary(manifest, reports, errors, status, args.fail_on))
        record = {"directory": directory_name, "status": status, "input_fingerprint": fingerprint,
                  "report_hashes": {role: digest(directory / (role + ".json")) for role in reports},
                  "artifact_hashes": {p.name: digest(p) for p in sorted(directory.iterdir()) if p.is_file()}}
        state["rounds"].append(record)
        write_json(args.session / "session.json", state)
        print("Round " + str(manifest["round"]) + ": " + status + ". Report: " + str(directory / "summary.md"))
        if status != "passed" and len(state["rounds"]) >= state["max_rounds"]:
            print("Round limit reached. Remaining findings require integration and a new deliberate audit.")
        return 3 if errors else (2 if status != "passed" else 0)
    finally:
        lock.unlink(missing_ok=True)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, OSError, KeyError, subprocess.SubprocessError) as error:
        print("Review loop: " + str(error), file=sys.stderr)
        sys.exit(3)
