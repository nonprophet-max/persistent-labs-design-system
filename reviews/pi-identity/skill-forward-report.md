# Private Inference: independent forward specification

**Historical first-pass result.** The package was rebuilt after this report. Read `closure.md` for the current assessment: the blocking CSS mapping issue, missing theme-aware interaction guidance, and Pi naming inconsistency are fixed. The manual palette overrides below are superseded by the rebuilt package's exported surface mappings.

This specification uses only the portable Private Inference brand skill and its bundled references and assets. Layout, component behavior and copy below are implementation proposals, not additional specifications from the identity PDF. No network access, publication or tracked-file edits were performed.

## Result

The package supports a faithful visual concept. It does not support a factual product marketing proposition or operational settings implementation: the supplied identity establishes neither capabilities nor settings behavior. A developer can implement the following explicitly illustrative hero and panel. Pi-specific color and font assignments must be made explicitly because the generic CSS surface mappings retain the parent brand defaults.

## Assets

All paths below are relative to `plugins/privateinference-brand/skills/privateinference-brand/`. Use the supplied files directly, with `height: auto`; preserve their viewBoxes, fixed fills and path geometry. Do not retype outlined lettering, redraw the asymmetric flare or substitute a π glyph.

| Use | Exact asset | ViewBox | Verified fixed fills |
| --- | --- | --- | --- |
| Light desktop header | `assets/pi/horizontal.svg` | `0 0 667.9436 114.0001` | Disc `#FBD78E`; flare and lettering `#1A1A1A` |
| Light narrow-screen lockup when horizontal space is insufficient | `assets/pi/vertical.svg` | `0 0 388.0002 475.7285` | Disc `#FBD78E`; flare and lettering `#1A1A1A` |
| Dark panel or dark page lockup | `assets/pi/horizontal-dark.svg` | `0 0 506.7164 86.4828` | Disc `#FBD78E`; flare `#1A1A1A`; lettering `#FFFFFF` |
| Standalone emblem | `assets/pi/mark.svg` | `0 0 197.9996 198.0001` | Disc `#FBD78E`; flare `#1A1A1A` |
| Standalone outlined name | `assets/pi/logotype.svg` | `0 0 308.6296 34.0000` | `#1A1A1A` |
| Source white-on-gold treatment | `assets/pi/horizontal-reversed.svg` | `0 0 506.7162 86.4766` | White artwork `#FFFFFF`; background must be supplied separately |

`assets/privateinference.svg` is byte-identical to `assets/pi/mark.svg`. `assets/pi/brand-identity.pdf` and the two provenance JSON files are present. The PDF, all six Pi SVG variants and all eight Poppins files match the recorded SHA-256 values.

Use `alt="Private Inference"` on a meaningful full lockup. Use empty alt text for a repeated decorative mark. The maker endorsement is live text, “by Persistent Labs,” on its own quiet line with at least one line of clear space. Do not merge the two brand marks.

The brand reference recommends a 240px-wide horizontal lockup, a 32px standalone mark, and half a disc diameter of clear space. These are practical recommendations, not source-defined minimum sizes. At 240px wide, the horizontal lockup is about 41px high; reserve approximately 21px clear space around it. On a tight screen use the vertical asset at a proposed 144px width, preserving its approximately 177px height and providing clear space based on its actual rendered disc.

## Typeface and hierarchy

Load `assets/fonts.css` with its adjacent `assets/fonts/` directory intact. Apply `font-family: "Poppins", sans-serif` to the Pi surface and inherit it in buttons and fields. Merely loading the stylesheet or defining `--product-font-family` does not apply the font.

All supplied Poppins fonts are upright Latin WOFF2 files: `assets/fonts/poppins-latin-100.woff2` through `poppins-latin-800.woff2`, in 100 increments. Names are Thin 100, Extralight 200, Light 300, Regular 400, Medium 500, Semibold 600, Bold 700 and Extrabold 800. Retain `assets/fonts/OFL-Poppins.txt`. No italic or non-Latin masters are supplied.

Proposed application of the shared scale:

| Role | Size | Weight | Line height / tracking |
| --- | --- | --- | --- |
| Hero heading | `clamp(2.5rem, 1.5rem + 3vw, 5.5rem)` | 700 | 1.04 / `-.03em` |
| Hero lead | `clamp(1.125rem, 1rem + .5vw, 1.5rem)` | 400 | 1.55 / 0 |
| Panel title | 1.25rem | 600 | 1.15 / `-.03em` |
| Body and values | 1rem | 400 | 1.6 / 0 |
| Controls and labels | 1rem | 500 | 1.4 / 0 |
| Supporting copy and endorsement | .875rem | 400 | 1.6 / 0 |
| Short status label | .75rem | 500 | 1.5 / 0 |

The numerical scale is shared implementation guidance. The PDF establishes the family and available weights, not type sizes.

## Palette mappings

Every source palette value is retained. Proposed UI roles are explicit:

| Role | Light hero | Dark panel |
| --- | --- | --- |
| Surface | `#FFFFFF` | `#1A1A1A` |
| Primary and secondary readable text | `#1E1E1E` | `#F5F5F5` |
| Action fill | `#FBD78E` | `#E5B14A` |
| Text on action | `#1E1E1E` | `#1A1A1A` |
| Decorative divider | `#BFBFBF` | `#7F7F7F` |
| Essential control outline | `#1E1E1E` | `#7F7F7F` |
| Focus ring | `#1E1E1E` | `#E5B14A` |

Use hierarchy, spacing and size to distinguish secondary copy; do not lower its opacity. White-on-gold is a supplied logo treatment, not a reading-text treatment. The dark logo correctly retains its source pale-gold disc even though the dark UI action gold is `#E5B14A`.

Calculated contrast: light text 16.67:1; light action label 12.08:1; dark text 15.96:1; dark action label 8.88:1. `#7F7F7F` on `#1A1A1A` is 4.35:1: adequate for an essential outline, below the 4.5:1 normal-text target. `#BFBFBF` on white is 1.84:1: decorative only, not essential control identification. Pale gold on white is 1.38:1, so a pale-gold button on white needs its proposed ink outline to make the boundary discernible.

After the bundled CSS, use explicit product/surface overrides, then consume these variables in component CSS:

```css
[data-product="privateinference"] {
  font-family: "Poppins", sans-serif;
}
[data-product="privateinference"] :is(button, input, select, textarea) {
  font: inherit;
}
[data-product="privateinference"][data-surface="light"] {
  --surface: #FFFFFF;
  --text: #1E1E1E;
  --text-secondary: #1E1E1E;
  --text-muted: #1E1E1E;
  --action: #FBD78E;
  --on-action: #1E1E1E;
  --action-hover: #E5B14A;
  --action-pressed: #E5B14A;
  --control-border: #1E1E1E;
  --focus: #1E1E1E;
}
[data-product="privateinference"][data-surface="dark"] {
  --surface: #1A1A1A;
  --text: #F5F5F5;
  --text-secondary: #F5F5F5;
  --text-muted: #F5F5F5;
  --action: #E5B14A;
  --on-action: #1A1A1A;
  --action-hover: #E5B14A;
  --action-pressed: #E5B14A;
  --control-border: #7F7F7F;
  --focus: #E5B14A;
}
```

Put both attributes on each fixed surface, including the nested dark panel. These overrides are a proposed resolution of the package's generic mappings, not new source brand rules.

## Desktop and narrow-screen hero

At 1440px, use a centered container, maximum 1520px, with 64px outer gutters. The header carries the 240px horizontal lockup; place the maker endorsement separately. The hero has two columns, `minmax(0, 7fr) minmax(0, 5fr)`, with a 64px gap. The left column holds headline, lead and one action. The right column holds the dark illustrative settings panel, maximum 520px wide. Use 80–120px vertical section space. Keep prose within 66ch and left aligned; do not fix the hero height.

Below 1180px, stack the hero with the heading and action before the panel. Below 600px, use 20px page gutters, 64px section spacing, 16px heading-to-copy spacing, and 24px copy-to-action spacing. Use the vertical lockup where the horizontal version and clear space would crowd the screen. At 320px, the panel is 280px wide, with 24px insets and 232px content width. Values stack below their labels. Keep headings and labels wrapping naturally; do not hide overflow at page level.

Proposed safe copy:

- Status: **Upcoming product**
- Heading: **Meet Private Inference.**
- Lead: **An upcoming product from Persistent Labs.**
- Primary action: **Explore the concept**
- Note: **Illustrative interface. Product details are not yet specified.**
- Endorsement: **by Persistent Labs**

The action links to the visible `#settings-preview` section. It does not imply account creation, API access, a waitlist, pricing or availability. Do not ship “Pi Lorem Ipsum.” No benefit-led tagline can be substantiated by these materials.

## Dark settings panel

Use a semantic section labelled by **Settings preview**, preceded by the dark lockup or a decorative 32px mark. Background `#1A1A1A`, text `#F5F5F5`, border `1px solid #7F7F7F`, proposed 24px corner radius, 24px internal padding and 24px group gaps. Corners are inherited implementation guidance, not a Pi source specification.

Panel copy:

- Title: **Settings preview**
- Introduction: **Illustrative interface. These product details are not specified.**
- **Deployment location** — **Not specified**
- **Access scope** — **Not specified**
- **Retention policy** — **Not specified**
- Footnote: **This preview does not change product settings.**

Render these as labelled read-only information rows, not invented dropdown options or a privacy toggle. No Save action is justified until settings schemas, permissions and persistence behavior are confirmed. This is a concept panel; it is not an operational settings specification.

Controls elsewhere use a 48px height and at least 44×44px target, clear text labels and a 3px focus ring with 4px offset. Light primary hover/pressed uses the supplied `#E5B14A` reuse. For a dark primary action, the base, hover and pressed color coincide; proposed extra feedback is an underline on hover and inset ink outline on press, with stable geometry. Keep the preview static and honor reduced motion. If operational controls are later added, specify loading, disabled, error, success, keyboard and announcement behavior against the real operation.

## Contradictions and missing facts

1. **CSS surface mismatch:** `assets/tokens.css:99–104` assigns generic dark surfaces `#1C1E21`, white/parent secondary text and pale gold; light surfaces use parent ink `#1C1E21`. It does not map the exact Pi palettes. An implementer following the stylesheet alone will not reproduce the Pi dark palette. Explicit overrides above resolve this for the proposed concept.
2. **Incomplete theme-aware action states:** Pi has one action token set, with `#E5B14A` serving both hover and pressed. There are no independent dark-theme states or component tokens (`components` is empty). The brand reference describes dark action pairing, but the CSS does not implement it.
3. **Residual abbreviation inconsistency:** the product skill and brand reference use **Pi**; shared foundations still say **Private Inference (PI)** and “PI symbol.” Product-specific precedence resolves this in favor of **Pi**, but the shared text is inconsistent.
4. **Contextual shared color table:** shared foundations lists the Pi dark accent on the parent's `#1C1E21` ground. That pair is accessible, but it should not be read as the Pi dark-palette mapping. The product reference takes precedence.
5. **No missing core files found:** the source PDF, provenance, six logo variants, mark alias, eight font weights, CSS and license are present. The font inventory heading focuses on Red Hat but Poppins is documented separately in `assets/pi/font-provenance.json` and declared in `assets/fonts.css`.
6. **Unspecified product facts:** approved audience, positioning, tagline, release timing, call-to-action destination beyond a local concept, availability, deployment, model/providers, retention, encryption, locality, access permissions, compliance and any operational settings are absent. These prevent truthful full marketing or live-settings implementation, not the illustrative visual concept above.
7. **Unspecified source design details:** the PDF supplies no type-size scale, numeric logo clear space/minimum sizes, radius system, motion system or component contract. The package clearly labels its additions as recommendations. This specification does the same.

## Verification limits

Verified bundle presence, SVG metadata/fills, recorded hashes and the specified color-pair calculations. The PDF hash is verified; direct PDF content/render inspection was not performed because neither PDF extraction command nor PDF library was available in the default runtime. No page was built or rendered, so actual line wraps, SVG appearance at intended size, keyboard behavior and screenshots at 320, 390, 768, 1024 and 1440px remain unverified. A production implementation must perform those visual and interaction checks.
