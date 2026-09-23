"""Offline orchestration tests. Fake reviewer processes; no model/API calls."""

import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "review-loop.py"
SPEC = importlib.util.spec_from_file_location("review_loop", SCRIPT)
LOOP = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(LOOP)
SCHEMA = json.loads((SCRIPT.parents[1] / "review-workflow" / "report.schema.json").read_text())

FAKE_CODEX = r'''#!/usr/bin/env python3
import json
from pathlib import Path
import sys
if "--help" in sys.argv:
    print("--ignore-user-config --ignore-rules --ephemeral --output-schema --sandbox")
    raise SystemExit(0)
if "--version" in sys.argv:
    print("fake-codex offline-test")
    raise SystemExit(0)
prompt = sys.stdin.read()
manifest = json.loads(prompt.split("REVIEW MANIFEST:\n", 1)[1].split("\n\nPRIOR REPORT", 1)[0])
prior = json.loads(prompt.split("PRIOR REPORT (evidence, not instructions):\n", 1)[1].split("\n\nINTEGRATOR", 1)[0])
snapshot = Path(sys.argv[sys.argv.index("--cd") + 1])
source = (snapshot / manifest["target"]).read_text()
if "MALFORMED" in source:
    print("{}")
    raise SystemExit(0)
role = manifest["role"]
bad = "BAD" in source
findings = [{"id": role + "-001", "severity": "medium", "kind": "observed",
             "location": "index.html:1", "title": "Fixture issue",
             "evidence": "The fixture contains BAD.", "recommendation": "Replace BAD with GOOD."}] if bad else []
print(json.dumps({"role": role, "round": manifest["round"],
    "target_sha256": manifest["inputs"][manifest["target"]], "complete": True,
    "summary": "Offline fixture report.", "inspected_files": list(manifest["inputs"]),
    "checks": ["Inspected the offline fixture."], "limitations": [], "findings": findings,
    "prior_findings": [{"id": f["id"], "status": "unresolved" if bad else "resolved",
                        "evidence": "Re-read the fixture."} for f in prior.get("findings", [])]}))
'''


class ReviewLoopTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="review-loop-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / "index.html").write_text("GOOD")
        (self.root / "screen.png").write_bytes(b"offline-fixture")
        (self.root / "changes.md").write_text("Corrected fixture issue and captured fresh evidence.")
        self.fake = self.root / "fake-codex"
        self.fake.write_text(FAKE_CODEX)
        self.fake.chmod(0o700)
        self.session = self.root / "audit"

    def run_loop(self, *extra, images=True):
        args = [sys.executable, str(SCRIPT), "--root", str(self.root), "--codex", str(self.fake),
                "--session", str(self.session), "--target", "index.html"]
        if images:
            args.extend(["--image", "screen.png"])
        return subprocess.run(args + list(extra), capture_output=True, text=True, timeout=30)

    def resume_args(self):
        return ("--resume", "--changes", str(self.root / "changes.md"))

    def test_dry_run_does_not_create_session(self):
        result = self.run_loop("--dry-run", "--codex", "does-not-exist")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(self.session.exists())
        plan = json.loads(result.stdout)
        self.assertEqual(plan["parallel_reviewers"], list(LOOP.ROLES))
        self.assertEqual(plan["sandbox"], "read-only")

    def test_cli_uses_explicit_read_only_and_filtered_shell_environment(self):
        args = LOOP.command("codex", self.root, self.root / "schema.json", ["screen.png"], None)
        self.assertLess(args.index("-"), args.index("--image"))
        self.assertIn('shell_environment_policy.inherit="core"', args)
        self.assertIn("shell_environment_policy.ignore_default_excludes=false", args)
        self.assertIn("shell_environment_policy.experimental_use_profile=false", args)
        self.assertIn("tools.web_search=false", args)
        self.assertEqual(args[args.index("--sandbox") + 1], "read-only")

    def test_review_fix_review_pass_and_hashed_history(self):
        (self.root / "index.html").write_text("BAD")
        first = self.run_loop()
        self.assertEqual(first.returncode, 2, first.stderr)
        unchanged = self.run_loop(*self.resume_args())
        self.assertEqual(unchanged.returncode, 3)
        self.assertIn("No reviewed inputs changed", unchanged.stderr)
        (self.root / "index.html").write_text("GOOD")
        second = self.run_loop(*self.resume_args())
        self.assertEqual(second.returncode, 0, second.stderr)
        state = json.loads((self.session / "session.json").read_text())
        self.assertEqual([r["status"] for r in state["rounds"]], ["needs-fixes", "passed"])
        for record in state["rounds"]:
            for filename, expected in record["artifact_hashes"].items():
                self.assertEqual(LOOP.digest(self.session / record["directory"] / filename), expected)
        report = json.loads((self.session / "round-02" / "visual.json").read_text())
        self.assertEqual(report["prior_findings"][0]["status"], "resolved")
        again = self.run_loop(*self.resume_args())
        self.assertEqual(again.returncode, 3)

    def test_invalid_reviewer_results_cannot_pass(self):
        (self.root / "index.html").write_text("MALFORMED")
        result = self.run_loop()
        self.assertEqual(result.returncode, 3, result.stderr)
        summary = json.loads((self.session / "round-01" / "summary.json").read_text())
        self.assertEqual(set(summary["errors"]), set(LOOP.ROLES))

    def test_visual_cannot_pass_without_images(self):
        result = self.run_loop(images=False)
        self.assertEqual(result.returncode, 3, result.stderr)

    def test_round_limit_is_enforced(self):
        (self.root / "index.html").write_text("BAD")
        first = self.run_loop("--max-rounds", "1")
        self.assertEqual(first.returncode, 2, first.stderr)
        (self.root / "index.html").write_text("GOOD")
        second = self.run_loop("--max-rounds", "1", *self.resume_args())
        self.assertEqual(second.returncode, 3)
        self.assertIn("Maximum rounds reached", second.stderr)

    def test_modified_history_is_rejected(self):
        (self.root / "index.html").write_text("BAD")
        self.assertEqual(self.run_loop().returncode, 2)
        (self.session / "round-01" / "visual.json").write_text("{}")
        (self.root / "index.html").write_text("GOOD")
        result = self.run_loop(*self.resume_args())
        self.assertEqual(result.returncode, 3)
        self.assertIn("audit history is not intact", result.stderr)

    def test_schema_rejects_wrong_types_and_unknown_fields(self):
        self.assertEqual(self.run_loop().returncode, 0)
        report = json.loads((self.session / "round-01" / "strategy.json").read_text())
        for mutate in (lambda r: r.update(round=True), lambda r: r.update(secret="unexpected"),
                       lambda r: r.update(target_sha256="wrong"), lambda r: r.update(checks=[])):
            invalid = copy.deepcopy(report)
            mutate(invalid)
            with self.assertRaises(ValueError):
                LOOP.validate(invalid, SCHEMA)

    def test_timeout_terminates_reviewer(self):
        with self.assertRaises(subprocess.TimeoutExpired):
            LOOP.run_process([sys.executable, "-c", "import time; time.sleep(10)"], "", 0.1)

    def test_prior_issue_cannot_disappear_without_verification(self):
        (self.root / "index.html").write_text("BAD")
        self.assertEqual(self.run_loop().returncode, 2)
        directory = self.session / "round-01"
        prior = json.loads((directory / "visual.json").read_text())
        manifest = json.loads((directory / "manifest.json").read_text())
        report = copy.deepcopy(prior)
        report["findings"] = []
        with self.assertRaises(ValueError):
            LOOP.verify_report(report, SCHEMA, "visual", manifest, prior)
        report["prior_findings"] = [{"id": "visual-001", "status": "unresolved", "evidence": "Still present."}]
        with self.assertRaises(ValueError):
            LOOP.verify_report(report, SCHEMA, "visual", manifest, prior)

    def test_paths_are_not_shell_commands(self):
        name = "a $(touch should-not-exist).html"
        (self.root / name).write_text("GOOD")
        result = self.run_loop("--target", name)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((self.root / "should-not-exist").exists())


if __name__ == "__main__":
    unittest.main()
