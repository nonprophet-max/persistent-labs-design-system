# Persistent Labs design bible

A revised design system and a reusable multi-agent review workflow. Open **[index.html](index.html)** in a browser; the finished artifact works locally with no build service or account.

The original user-supplied bible is preserved unchanged in `reference/original-design-bible.html`. The Desktop original and synced project sources were not edited.

## Contents

- 18 chapters covering foundations, five product identities, governance and exportable tokens.
- FireFlow, Unfazed.dev, Lanni, PrivateInference (PI) and Galactica. **FireFlow is one product with three core parts:** the FireFlow orchestration engine, MemoryTree for persistent memory and FlameChorus, the chat UX engine.
- Bold vector π for PI; original Persistent Labs and Unfazed marks; clearly labelled concept product symbols for FireFlow and Lanni, plus a subordinate MemoryTree component icon.
- A sticky menu bar, chapter navigation, light/dark reading views, accessible local specimens, copy/download controls, and bundled Red Hat fonts.
- Independent review records, versioned browser evidence and a bounded reusable review loop.
- Galactica’s privacy/identity direction adapted into the family with proposed copper/monochrome tokens, separate AI and blockchain guidance and a disclosure-review specimen. The owner-directed Galactica.com lockup includes .com and a bold orange dot; its SVG lettering is outlined.

New product design directions are proposals for review. Product features, availability, technical guarantees and the meaning of “private” are not inferred from visual design. Unfazed’s existing identity is preserved as an explicit family exception.

## Edit and rebuild

Requires Python 3.9 or later. No Python dependencies.

```sh
python3 scripts/build.py
```

Edit `tokens/design-tokens.json` for tokens, `src/products.json` for product specifications and FireFlow’s nested core parts, `src/style.css` for presentation, `src/app.js` for interactions, and `scripts/build.py` for the foundation content and page assembly. Generated outputs are `index.html`, `tokens/persistent-labs.tokens.css`, and the four concept SVGs. The separate `scripts/build_galactica_mark.py` regenerates Galactica.com’s outlined wordmark using the optional `fonttools[woff]` dependency; its generated SVG is checked in so ordinary builds remain dependency-free. Do not edit the generated HTML or token CSS directly.

Local fonts and licenses are in `assets/fonts/`. The font-face declarations in `src/fonts.css` use local relative paths. No analytics, remote scripts, API keys or product connections are required.

## Current verification status

Edition 2.3 adds the Galactica.com lockup, a website menu bar, a static Netlify build and six standalone brand skill plugins. Static and standalone plugin checks pass. Current Chromium checks pass at five widths (320–1440px) in both themes, with no runtime errors, request warnings, contrast findings, overflow or undersized controls. All 52 local screenshots were visually reviewed, with no material layout findings. See [current verification](reviews/release-verification.json) and [live deployment checks](reviews/deployment-verification.json). Historical browser evidence remains archived separately.

## Verify

The browser checks use Node.js 20+ and Playwright. Install the optional test dependency and its browser once:

```sh
npm ci
npx playwright install chromium
npm run check
```

To use an existing Chromium-based browser, set `BROWSER_EXECUTABLE` to its executable path before running `npm run check`. `NODE_PATH` can identify an existing Playwright installation. The code contains no machine-specific runtime paths.

Checks cover five viewport widths in light and dark themes, text contrast against composited solid backgrounds, page overflow, heading structure, local anchors, minimum control sizes, font loading, theme persistence, mobile navigation, Escape/focus behavior, validation, specimen feedback, clipboard fallback and reduced motion. Screenshots are retained for independent visual review. These checks are targeted evidence, not a claim of full WCAG certification or cross-browser support.

The reusable review orchestrator has separate offline tests:

```sh
python3 -m unittest discover -s review-workflow -p 'test_*.py' -v
```

See [the review record](reviews/README.md) for actual session results and limitations. See [the workflow guide](docs/review-workflow.md) for repeating the independent strategy, visual and accessibility reviews. The loop runs reviewers read-only and stops for an integrator’s fixes between rounds; it does not commit, publish or approve its own changes.

## Website and brand skills

Build the shareable site with `npm run build:site`. Netlify publishes only `dist/`; plugin packages, source archives and internal review files stay in the private repository. The site is shareable by URL and requests no search indexing; this is not access control.

See [BRAND-SKILLS.md](BRAND-SKILLS.md) for the complete brand skill and five independent product plugins, invocation names and chatbot-compatible documents. Rebuild them with `npm run build:skills` and check with `npm run check:skills`.

Published on 23 September 2026:

- [Live reading site](https://persistent-labs-design-bible.netlify.app/), verified on desktop and mobile.
- [Private GitHub repository](https://github.com/nonprophet-max/persistent-labs-design-system), branch `codex/design-bible`; private visibility was verified through GitHub.

The public deployment passes 45 navigation checks, 19 file checks and six checks that private source paths return 404. Netlify adds its hosting comment and public badge script to the HTML; after removing those exact additions and a trailing newline for comparison, the served page content matches the site build. Other assets match byte for byte. Only the isolated public site directory was uploaded.

## Separate-page website

The separate-page edition has a home page, dedicated Foundations, Products, Tokens and Guidelines pages, and individual FireFlow, Unfazed.dev, Lanni, PrivateInference and Galactica pages. FireFlow's three core parts remain within its product page.

[Open the separate-page site](https://persistent-labs-design-pages.netlify.app/). This is a separate Netlify project; the original reading link remains available. All ten live pages pass the browser checks across five widths and both themes. See [the release record](reviews/pages/release-verification.json).

Run `npm run build:pages` to generate `dist-pages/` and `npm run check:pages` to run its browser review. The same `NODE_PATH` and `BROWSER_EXECUTABLE` options described above apply. `SITE_URL` can point the review at a deployed site; `QA_OUTPUT` selects a separate evidence directory. Use `netlify.pages.toml` for this site's build configuration. The original single-page site continues to use `netlify.toml` and `dist/`.

See [the prepublication review](reviews/pages/review.md) for the findings, corrections and browser/visual evidence. The original design content and brand plugins remain unchanged.

## Rights and provenance

Persistent Labs/product assets are included for the user’s requested design work; no general license is granted for those marks. Red Hat fonts retain their bundled SIL Open Font License. Unfazed’s existing mark is sourced from its public site and attributed in the source review. The supplied original design bible is retained as reference material.
