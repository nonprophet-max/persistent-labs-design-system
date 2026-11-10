# Persistent Labs brand library

A shareable design bible with a shared parent system and six distinct product identities: FireFlow, Unfazed.dev, Lanni, Private Inference, Galactica and Alfred.

The complete central walkthrough is hosted on [GitHub Pages](https://nonprophet-max.github.io/persistent-labs-design-system/). Alfred's chapter is at `/products/alfred/`. See [GitHub Pages build and publishing](docs/github-pages.md) and [the Alfred review/release record](reviews/alfred-brand/review.md) for actual verification and publication status. Historical Netlify deployment records remain in `reviews/`; they are not a dependency of the Pages build.

## Contents

- Nineteen chapters covering the parent foundations, six product identities, governance and exact tokens.
- Eleven navigable walkthrough pages, reading-theme controls, accessible fixed specimens and per-brand AI resources.
- Alfred's interactive logo/background comparison, copyable palette, editable typography, geometry, voice, application examples and complete skill download.
- Seven independent portable brand packages: the parent plus six products. See [BRAND-SKILLS.md](BRAND-SKILLS.md).
- Bundled fonts, source/provenance records and the supplied brand assets. Existing source archives remain unchanged.

FireFlow is one product with three core parts: the FireFlow orchestration engine, MemoryTree for persistent memory and FlameChorus for chat UX. Those components stay within FireFlow. Pi follows the supplied identity PDF and Poppins. Alfred retains its supplied v0.3 Instrument Serif/Outfit identity. Product examples do not establish capabilities, availability or partnerships.

## Maintained sources

- `tokens/design-tokens.json`: parent/product tokens and detailed identity primitives.
- `src/products.json`: product registration and chapter summaries.
- `src/alfred-brand.json`: current Alfred rules, distinct from historical handoff reviews.
- `scripts/alfred_brand.py`: Alfred rendering, Markdown export and portable token/font generation from the shared sources.
- `src/style.css`, `src/pages.css`, `src/pi.css`, `src/alfred.css`: scoped presentation.
- `src/app.js`, `src/pages.js`, `src/alfred.js`: reading, navigation and product interactions.
- `scripts/package_skills.py`: standalone skills, chatbot guides, registries and the complete Alfred ZIP.

Edit maintained sources and regenerate. Do not patch generated HTML, CSS or plugin instructions as a competing source of truth. `reference/` is read-only history.

## Build

Python 3.9+ is sufficient for the static site and packages; no Python dependencies or remote services are required.

```sh
python3 scripts/package_skills.py
SITE_BASE_PATH=/persistent-labs-design-system python3 scripts/build_pages.py
```

Publish only `dist-pages/`. That directory contains the whole public walkthrough and its intended downloads, excludes source/plugins/reviews, and is ready for the repository's GitHub Pages URL. An empty `SITE_BASE_PATH` builds a root-mounted local site. The single-file reading edition remains generated at `index.html` by `python3 scripts/build.py`.

## Verify

```sh
python3 -m unittest discover -s scripts -p 'test_*.py' -v
python3 scripts/check.py
python3 scripts/check_skills.py
python3 -m unittest discover -s review-workflow -p 'test_*.py' -v
```

Browser checks require Node.js 20+ and the existing Playwright development dependency. Run `npm ci` and install Playwright's Chromium, or set `NODE_PATH`/`BROWSER_EXECUTABLE` to an existing compatible installation.

```sh
SITE_BASE_PATH=/persistent-labs-design-system npm run check:pages
node scripts/qa.mjs
SITE_URL=http://localhost:8000/persistent-labs-design-system/ node scripts/qa-alfred.mjs
```

The focused Alfred command expects a separately running preview server mounted at that path. Set `SITE_URL` to the deployed library root for live checks; `QA_OUTPUT` selects an evidence directory. Browser checks cover actual font loading, keyboard/focus, copy failure, downloads, enlarged/long text, theme isolation, navigation, contrast and overflow. Chromium evidence does not certify Safari/Firefox, screen-reader support or full WCAG compliance.

## AI use

Use [the Alfred skill](plugins/alfred-brand/skills/alfred-brand/SKILL.md), [plain chatbot guide](plugins/alfred-brand/chatbot.md), or the complete `assets/downloads/alfred-brand.zip`. Skill-aware tools can invoke `$alfred-brand`; ordinary chatbots can use the attached guide. Rendering, file access and execution depend on the host tool. No package silently installs itself or authorises publication, purchases or account changes.

## Identity source and rights

The parent ribbon and established product assets are preserved. Pi's unchanged source PDF, vector extraction and font provenance remain under `assets/pi/`; see [its source review](reviews/pi-identity/review.md). Alfred's supplied logos and illustrations, corrected font metadata and exact asset hashes are under `assets/alfred/`.

Brand marks/artwork are included for the requested brand work; no general trademark, ownership or redistribution rights are granted. Open fonts retain their SIL OFL notices. Alfred's recorded mascot decision is a brand-use decision, not legal clearance. Instrument Serif/Cormorant cover the documented heading scripts; Cyrillic body text uses the explicitly documented system fallback because the supplied Outfit files do not cover Cyrillic.
