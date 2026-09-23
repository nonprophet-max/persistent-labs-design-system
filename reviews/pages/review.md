# Separate-page edition review

Reviewed 23 September 2026 by the implementing/publishing agent before publication and push. This was a code, browser and visual review, not an independent multi-agent review round.

## Requested behavior

The top navigation opens dedicated Foundations, Products, Tokens and Guidelines pages. Each of the five product identity links opens its own page. A home page links to the sections and products. FireFlow's orchestration engine, MemoryTree and FlameChorus remain subordinate sections within FireFlow.

The ten-page build uses the canonical section content, assets and tokens. Every one of the original 18 chapters appears exactly once across the section and product pages. The original single-page build, source archive and six portable brand plugins are unchanged.

## Review findings and corrections

1. The Lanni home-page identity link was narrower than the intended 44px tap target. Added a 44px minimum width.
2. Turning a chapter heading into a page heading initially skipped heading levels. Promoted the complete chapter heading hierarchy and retained each heading's existing visual styling.
3. The first production check read the page theme before deferred initialization had completed. The browser test now waits for navigation to finish, and the page restores the saved theme before loading styles to avoid a light-theme flash.

All findings are closed in the final local browser report. Code review also checked route allocation, cross-page fragments, absolute asset paths, public-file exclusions, optional page controls, current-page navigation and separate publishing configuration.

## Verification

- Ten pages across five widths (320, 390, 768, 1024, 1440px) and both themes: 100 successful render combinations.
- No page overflow, solid-background contrast findings, undersized tested controls, duplicate IDs, heading-order errors, browser runtime errors or failed requests.
- All 40 opening-page screenshots were visually reviewed at desktop and mobile widths in both themes; no material layout findings remain.
- Main navigation and five product links open separate documents and survive direct reload.
- Mobile menu focus and Escape, active navigation, browser Back/Forward and theme persistence across pages pass.
- Token CSS/JSON downloads, clipboard fallback, form validation, all five product demos, reduced motion and the nested MemoryTree link pass.
- The build validates all internal page links, assets and fragments and excludes private source directories.
- Existing static checks still pass for 87 token color pairs and the five-product architecture.

The exact local page hashes, browser version, render matrix and results are in [local browser evidence](evidence/browser-qa.json). The [production browser report](production-evidence/browser-qa.json) also passes all 100 render combinations and interaction checks, with no runtime errors or failed requests in the final run. Five private source paths return 404. Two production screenshots were reviewed at full size after deployment. Netlify's own hosting badge may cancel its asynchronous request during deliberate navigation; the harness records this separately as a hosting warning when observed.

The [separate-page site](https://persistent-labs-design-pages.netlify.app/) is published on Netlify project `04e05890-2a17-4aae-a575-b8cb4b263cb0`, deployment `6ab43b31df8d4bdf02ae6cae`. The original single-page site's deployment was verified unchanged. See [release verification](release-verification.json).

## Limits

Chromium only; no Safari, Firefox, screen-reader or full WCAG audit. Automated contrast checking covers solid composited backgrounds. The public site requests no indexing; this is not access control.
