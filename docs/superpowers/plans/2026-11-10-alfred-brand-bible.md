# Alfred Brand Bible Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task. Steps use checkbox syntax for tracking.

**Goal:** Add a polished interactive Alfred brand bible to the Persistent library, with a matching independent brand skill, chatbot guide and full download.

**Architecture:** Extend the existing static Python/HTML/CSS/JS pipeline. Canonical Alfred guidance and tokens feed the web chapter and package; generated files are not alternate editable sources. Preserve the parent shell and other product identities.

**Tech Stack:** Python standard-library generators, existing vanilla CSS/JS, existing Playwright browser checks. No new framework or runtime service.

**Spec:** `docs/superpowers/specs/2026-11-10-alfred-brand-bible-design.md` (approved).

## Global Constraints

- Preserve the supplied v0.3 logo, star mark and both mascot PNGs; do not redraw or recolour them.
- Ink `#3E3D3D`, secondary ink `#6A665F`, paper `#FFFBF7`, sand `#ECE7DC`, accent `#F2BD3C`; yellow remains restrained.
- Instrument Serif 400 headings, Outfit body/controls, documented Cormorant Cyrillic heading companion; Cyrillic body uses an explicit system fallback.
- Outline 1.5px; 28px cards, 36px capsules, pill buttons. No hard shadows, retired pink/blue identity or invented capability claims.
- All Alfred styling and interaction are scoped. Other product records, source archives and parent token primitives remain intact.
- Controls at least 44px, input text at least 16px, readable focus and copy feedback, no essential JS-only content.
- Brand rules and exact tokens have one maintained source; downloadable skills are standalone.
- Max authorised implementation and publication on completion. His approval covers the agreed brief; do not add another routine planning approval gate.
- Read-only independent reviews; batch material corrections; no unchanged re-read, test or audit loops. Codex adaptation only, no Pi hooks.

## Review Focus

- Hosted directory/base paths: links, fonts and ZIPs must resolve from both reading and multipage output.
- Cyrillic samples: declared fonts must match actual glyph coverage; unsupported coverage must be explicit.
- Shared host themes and narrow screens: Alfred remains isolated and usable at 320px and with larger text.
- Clipboard unavailable: users can still select/copy exact values with visible feedback.
- Portable skill without parent checkout: all referenced assets, tokens and instructions remain usable.

## Hosting change — authorised by Max

During implementation Max asked to move hosting for the whole site to GitHub Pages. Use `https://nonprophet-max.github.io/persistent-labs-design-system/` as the primary library URL. The complete multipage build needs a configurable repository base path and a reproducible Pages workflow; verify all chapters, assets, skill links and downloads at that subpath. Preserve the source repository and default branch. Existing Netlify hosting is no longer a dependency. A disjoint hosting subtask may run alongside Task 1, owning `scripts/build_pages.py` and Pages workflow/tests; the chapter implementer is explicitly excluded from those files.

## Execution record

Use a single isolated Desktop checkout because the app's native worktree tool rejected the source repository as outside this chat's workspace folders. Source checkout remains unchanged. Branch: `codex/alfred-brand-bible`. Run the SDD workspace helper and keep task status/rulings in its ledger. Delegate implementation tasks sequentially; root can do independent environment/release preparation while a task runs.

### Task 1: Canonical identity and interactive Alfred chapter

**Files:**
- Create `src/alfred-brand.json`, `src/alfred.css`, `src/alfred.js`, `scripts/alfred_brand.py` and a focused generator check under `scripts/test_alfred.py`.
- Add supplied assets under `assets/alfred/`; supply `assets/alfred.svg` for the existing portfolio mark interface.
- Modify `src/products.json`, `tokens/design-tokens.json`, `scripts/build.py`, and reading/multipage script composition only as needed to load the scoped module.

**Interfaces:**
- Consumes: original handoff at `/Users/max.rabinovitch/Desktop/Alfred Design Bible Review/alfred-brand-v0.3-handoff/skills/alfred-brand/` and the approved spec.
- Produces: `products.alfred` registration; `identities.alfred` canonical detailed token object; `src/alfred-brand.json` canonical current brand guidance.
- Expose side-effect-free helpers `render_alfred() -> str` and `brand_markdown() -> str` from `scripts/alfred_brand.py`; both consume the same canonical guidance/tokens. Expose `build_assets() -> None` to emit portable token/font CSS plus JSON into `assets/alfred/` from that token object.
- Alfred output is under `[data-product="alfred"]` with unique `alfred-*` ids and classes. `src/alfred.js` is loaded by both output modes, with safe absence handling on other pages.
- Task 2 will use these helpers and canonical assets for packaging; do not patch the package generator in Task 1.

- [x] Write focused failing tests for the renderer's real link targets and the canonical/portable token round-trip. The tests must show the current absent Alfred module fails before implementation.
- [x] Copy supplied SVGs/PNGs/fonts with provenance and OFL notices. Rename the mislabelled Outfit subset to Latin-ext and correct its declared range; preserve original file bytes.
- [x] Implement canonical guidance and helpers. Current guidance includes all eight approved sections; superseded fonts/colours are historical, and missing Report v5 is no dependency.
- [x] Build the chapter with authored, varied demonstrations: real logos, colour proportions, type hierarchy, spacing/geometry, voice examples, correct/incorrect use, applications and usable resources. Use the mascot once in the chapter introduction. Do not turn the page into repeated equal cards.
- [x] Add working copy controls/fallback, editable type specimen, light/dark asset comparison, section navigation and direct downloads where available. Full ZIP becomes available through Task 2. Defaults must remain readable without JS.
- [x] Run focused tests, `python3 scripts/build.py`, inspect generated chapter/resource references, and self-review. Browser evidence may follow after Task 2 enables the generated registry/routes.
- [x] Commit source, assets and generated reading output; report exact checks and remaining integration dependencies.

### Task 2: Standalone skill and central-library integration

**Files:**
- Modify `scripts/package_skills.py`, `scripts/build_pages.py`, `scripts/build_site.py` as needed, `scripts/check.py`, `scripts/check_skills.py`, registry/catalog outputs and relevant generated plugin files.
- Create `scripts/test_alfred_package.py`, `assets/downloads/alfred-brand.zip` (generated) and Alfred plugin output under `plugins/alfred-brand/`.
- Update public-facing product counts/names in source and generated documentation where Alfred changes them.

**Interfaces:**
- Consumes Task 1's helpers, canonical rules/tokens and `assets/alfred/`.
- Produces `plugins/alfred-brand/skills/alfred-brand/SKILL.md`, linked references, exact tokens/CSS/fonts/assets, existing supported host manifests, `plugins/alfred-brand/chatbot.md`, deterministic complete ZIP, registry/catalog membership and `/products/alfred/`.
- The standalone Alfred skill uses Alfred identity before inherited parent rules. Existing five product packages must not gain Alfred fonts or styling. Parent package may include Alfred as a sixth identity.

- [x] Write failing integration checks for an independent extracted skill, missing local dependencies and ZIP link resolution. Validate portability by extracting into a temporary directory outside the checkout.
- [x] Extend the packager using the shared Alfred source helpers, concise progressive-disclosure skill guidance and plain chatbot instructions. Preserve all brand invariants and asset/OFL provenance. Keep technical history outside the live instruction route.
- [x] Generate a stable ZIP containing a complete installable `alfred-brand/` skill folder; include plugin metadata/chatbot guide where clearly organised. Support downloading from the public output.
- [x] Extend the public build's asset handling and anchor rewrites where needed; all Alfred nested anchors and resources resolve in both output modes. Fix current explicit expected product/plugin lists to six/seven while retaining FireFlow hierarchy checks.
- [x] Run focused package tests, `python3 scripts/package_skills.py`, `python3 scripts/build_pages.py`, `python3 scripts/check.py`, `python3 scripts/check_skills.py` and skill frontmatter validation. Check deterministic regeneration of generated Alfred material.
- [x] Commit, self-review and report. Do not publish or change unrelated host settings.

### Task 3: Browser verification, documentation and release

**Files:**
- Modify `scripts/qa.mjs`, `scripts/qa-pages.mjs` for the new counts and meaningful Alfred interaction/loaded-font assertions.
- Create a focused `scripts/qa-alfred.mjs` if that avoids growing the existing suites with product-specific checks.
- Update `README.md`, `PRODUCT.md`/scoped design documentation as needed, and `reviews/alfred-brand/` evidence/release records.

**Interfaces:**
- Consumes final generated reading/site output and standalone package.
- Produces measured browser results, inspected screenshots, independent review/skill exercise, verified hosted link and Git commit/reference.

- [ ] Run the full applicable static/skill checks once on integrated code. Run reading and multipage browser suites, including Alfred at 320/390/768/1440px and both host reading themes. Explicitly exercise keyboard access, copy success/failure, type editing, asset previews, downloads, long labels, enlarged text and actual loaded fonts.
- [ ] Capture desktop/mobile Alfred sections and inspect the images. Run Impeccable detector once over changed UI targets and adjudicate findings against the fixed Alfred brief. Independent reviewers inspect actual screenshot evidence for strategy, visual fidelity and accessibility; another fresh agent exercises the skill in an isolated output directory.
- [ ] Batch material fixes and verify their closure without reopening unchanged code. Preserve original assets and parent identities; disclose browser/platform limits.
- [ ] Offer Max a concrete working visual preview during this stage while continuing independent packaging/checks. Ask only if a decision changes the agreed identity or deliverable.
- [ ] Verify current remote branch/hosting state. Commit and upload the complete reviewed addition to the intended public repository. Publish the complete intended generated public output with GitHub Pages; do not expose unrelated files. If external publication is blocked, preserve the complete tested release and report the concrete external requirement.
- [ ] Verify actual published URLs/assets/ZIP and record the commit, deployment identifiers and evidence. Return walkthrough and skill links with a concise verification summary.

## Plan self-review

The three tasks cover the spec's identity, source authority, interactive examples, portability, review and release requirements. Task 2 consumes named Task 1 helpers; Task 3 consumes their generated outputs. Publication was already requested by Max and remains the final stage after verification. The documented Cyrillic system fallback is the approved-brief default; no new typeface selection is required.
