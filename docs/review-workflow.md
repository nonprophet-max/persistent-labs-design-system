# Repeatable design review

The review loop runs three independent reviewers concurrently: creative strategy,
visual design, and accessibility/implementation. An integrator makes the fixes
between rounds. Each continuation asks the reviewers to verify the prior findings
against the changed artifact. The default audit budget is three rounds.

The live review recorded elsewhere in this project was performed by the desktop
agent team. The reusable CLI runner is a separate deliverable; its offline tests
use fake reviewer processes and do not establish the quality of the design bible.

## Run it

Requirements: Python 3.9 or later, a signed-in Codex CLI, and current rendered
evidence. The runner uses the CLI's default model unless `--model` is provided.
It does not load the user configuration or execution rules. CLI 0.153.4 was used
to verify the available command flags on 23 September 2026. The runner checks for
required flags before launching a review.

From the project directory, first inspect the plan without model calls or writes:

```sh
python3 scripts/review-loop.py --target index.html --dry-run
```

Prepare desktop/mobile screenshots plus dated source notes and browser check
results. Include all CSS, scripts, fonts, or other local files the target needs
as repeated `--context` inputs. Inputs must be ordinary, non-hidden files under
the project root. The runner deliberately copies only the files you provide.

Example using evidence already included in this repository:

```sh
python3 scripts/review-loop.py \
  --target index.html \
  --context reviews/round-1-strategy.md \
  --context reviews/evidence/browser-qa.json \
  --image reviews/evidence/cover-light-1440.png \
  --image reviews/evidence/cover-light-390.png \
  --session review-workflow/runs/design-audit \
  --max-rounds 3
```

For a full product audit, also pass each product’s desktop/mobile interface PNGs in `reviews/evidence/` as repeated `--image` inputs. Include `src/products.json`, `tokens/design-tokens.json` and font assets with `--context` when those details are in scope. The example above is a cover-focused review.

This command runs one round, saves reports, and exits. Read its `summary.md`, make
the corrections, regenerate any affected screenshots/checks, then write a short
change note that maps each finding ID to its correction and evidence. Continue
with the same command and these additional options:

```sh
--resume --changes reviews/round-01-fixes.md
```

Keep `--target`, `--max-rounds`, `--fail-on`, and `--model` unchanged when resuming.
The runner refuses an unchanged set of review inputs, except after an execution
error. Notes alone do not count as a design correction. If only evidence was
missing, adding that evidence is a valid change. An incomplete audit does not
become a pass just because the maximum round count has been reached.

## Evidence and stop conditions

Each round stores a manifest, three validated JSON reports when successful,
integrator notes, and machine-readable and readable summaries. The session
records SHA-256 hashes of inputs, prompts, schema, runner, and saved artifacts.
The runner checks input integrity during the round and report integrity before a
continuation. Retain the reviewed source version alongside a curated summary;
hashes establish identity but do not contain the source themselves.

The default release gate blocks `blocker`, `high`, and `medium` findings. Use
`--fail-on low` for a gate that also blocks minor polish. A reviewer must report
complete coverage for a pass. Missing screenshots or runtime evidence cannot be
silently treated as a successful visual/accessibility review. Source inspection
is valuable but does not replace looking at the rendered design.

| Exit | Meaning |
| --- | --- |
| `0` | Every review is complete and the configured gate passes, or a dry-run succeeds. |
| `2` | Findings or coverage gaps require integration before the next round. |
| `3` | Input, history, schema, reviewer process, timeout, CLI, or orchestration error. |

The runner launches separate `codex exec` processes in separate temporary input
snapshots. Reviewers have a read-only sandbox and may not start other agents.
They receive their own prior findings, not other reviewers' current reports.
No reviewer can fix the artifact through this workflow. Integrator corrections
remain explicit and reviewable, and prior findings require an evidence-backed
resolved/unresolved disposition. The runner never commits, pushes, publishes,
or creates a repository.

All subprocess arguments are passed directly, without shell interpolation.
Prompts go through standard input. Raw process output, tool transcripts,
environment values and authentication files are not logged; only validated
review reports are saved. Reviewer shell commands inherit only the core
environment, apply secret-name exclusions, and do not load the shell profile;
the web search tool is disabled. The CLI reuses its existing authentication. Model
calls still consume the signed-in account's usage, and supplied review inputs
are sent to that service. Do not add unrelated secrets to the input set.

Review sessions are ignored by the nested `.gitignore`; deliberately curate
reports for a private commit rather than checking in raw session data. The
read-only sandbox and focused snapshots reduce accidental edits and irrelevant
context; they are not a separate operating-system account or a guarantee that a
model can never access unrelated readable files on the host.

## Recovery and local validation

Each reviewer has a 600-second limit by default; `--timeout` accepts 30–1800
seconds. A failed reviewer yields an error result and can be retried in the next
round; valid prior reports are retained for continuity. The maximum audit budget
is six rounds, configurable down to one, with three the default.

If the runner is forcibly terminated, an incomplete round folder or `.running`
lock can remain. Confirm that its child processes have stopped, preserve the
incomplete evidence, and start a new session directory. Never delete an active
run's lock to start a competing process. A finished or exhausted audit also
requires a new, deliberately named session to begin another audit.

Run the offline suite without Codex access or network:

```sh
python3 -m unittest discover -s review-workflow -p 'test_*.py' -v
```

These tests exercise separate fake reviewer processes, a finding/fix/verification
cycle, unchanged-input refusal, round limits, tampered history, invalid reports,
missing visual evidence, subprocess timeout and paths containing shell syntax.

The implementation follows [OpenAI's non-interactive Codex documentation](https://learn.chatgpt.com/docs/non-interactive-mode)
for read-only execution, ephemeral sessions, input through standard input and
schema-constrained output. Checked-in prompts and schema are versioned together
with the runner so that later review changes remain inspectable.
Environment restrictions follow the [official configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference).
