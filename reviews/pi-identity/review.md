# Pi identity update — edition 2.4

The owner supplied **Pi Brand Identity(upd).pdf** as the new Pi source of truth on 9 October 2026, replacing the earlier Figma reference and proposed mathematical π/lavender identity. The owner also explicitly confirmed that the GitHub repository should remain public.

## Source fidelity

The one-page PDF is retained unchanged at `assets/pi/brand-identity.pdf`. SHA-256: `f7ad60d71d1fecf9433996562ede36d6e02b64ffa73b434f41e92028e58623bf`.

- **Private Inference**, two words; short name **Pi**.
- Original gold-disc/asymmetric four-point-flare artwork, with horizontal, vertical, mark and logotype formats. Six supplied color/layout variants are extracted as outlined vector paths; no retyping or redrawing. Extraction bounds, drawing indexes and hashes are recorded in `assets/pi/provenance.json`.
- Poppins upright weights 100–800. The Latin webfonts are bundled with their SIL OFL license; `assets/pi/font-provenance.json` records official font URLs and hashes.
- Light Palette: `#FBD78E`, `#1E1E1E`, `#FFFFFF`, `#BFBFBF`.
- Dark Palette: `#E5B14A`, `#F5F5F5`, `#1A1A1A`, `#7F7F7F`.
- The PDF's “Pi Lorem Ipsum” is placeholder text and is excluded from production assets.

The PDF defines visual identity. It does not establish product capabilities, technical privacy guarantees, launch availability, positioning, a voice system, spacing dimensions or UI states. The existing owner-provided upcoming status is retained. Accessible UI mappings, spacing, minimum sizes and focus/pressed treatments are explicitly identified as implementation guidance, separate from source facts.

## Review and corrections

A read-only source reviewer checked the PDF, extracted vectors, identity data and desktop/mobile evidence, and reported PASS with no substantive source-fidelity issues. A separate reviewer tested whether the portable skill could support a practical hero/settings brief without the source repository. That review found inherited parent colors in the exported Pi surface tokens. The mappings now support both same-element and nested surface usage, and the reviewer verified closure. See [initial skill review](skill-forward-report.md) and [closure](skill-forward-closure.md).

The integrator also aligned the generic pressed token with the Pi semantic mapping and clarified the portfolio contrast-table label; these final small corrections were checked by static validation. Browser testing found incorrectly rebased unquoted Poppins font URLs in the multipage build. The URL handling was corrected, and all eight font faces now load in both local and production checks.

## Verification

- Static checks pass for **107 color pairs**, document structure, anchors, five-product hierarchy, exact PDF palettes, source asset copies and font/license completeness.
- All **six standalone brand plugins** and their skill frontmatter pass validation. Pi and the parent plugin carry the source PDF, six logo variants, font files and provenance. Other product plugins preserve their own typography.
- Local reading-site browser suite: five widths × two themes = **10 combinations**, plus interaction checks; pass.
- Local multipage suite: ten pages × five widths × two themes = **100 combinations**; pass.
- Live multipage suite: the same **100 combinations**, including navigation, controls and actual Poppins loading; pass.
- Live reading-site Pi checks at 390px and 1440px verify the identity heading, all eight palette values, all eight loaded Poppins weights and absence of page overflow; pass.
- **59 published asset responses** across both sites match local SVG, PDF, font, token, provenance and CSS bytes exactly.

The integrator visually reviewed Pi hero, logo variants, typography and UI specimens in light/dark and desktop/mobile layouts, plus final live desktop/mobile captures. Component-only screenshots hide the fixed navigation in test-only capture styles; production layout is unchanged. Historical review records and screenshots remain unchanged and describe their original artifact hashes.

These checks use Chromium 154. They are not Safari/Firefox, screen-reader or complete WCAG certification. Automated contrast evidence covers solid composited backgrounds. The independent skill exercise is source-based and is not presented as a browser test.

## Published release

- [Pi walkthrough](https://persistent-labs-design-pages.netlify.app/products/privateinference/): deploy `6ac8ea37db28a6ca70bf4eb6`, generated `dist-pages/` only (50 files).
- [Pi reading chapter](https://persistent-labs-design-bible.netlify.app/#privateinference): deploy `6ac8ea31db28a6ca10bf4ed5`, generated `dist/` only (38 files).
- [Public GitHub repository](https://github.com/nonprophet-max/persistent-labs-design-system), branch `codex/design-bible`; portable skill invocation remains `$privateinference-brand`.

Both Netlify deploys were confirmed ready and published before live testing. The release record includes deployment identifiers, archive hashes, source/build hashes and evidence links. Source code, plugins, review records and the original bible archive are not part of either web deployment. The owner-supplied Pi PDF is intentionally included as the chapter's identity reference.
