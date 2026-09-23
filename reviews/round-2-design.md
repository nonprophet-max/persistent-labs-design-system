# Round 2 — revised bible design review

Reviewer: design-audit agent. Date: 23 September 2026.

Reviewed: generated `index.html`, `scripts/build.py`, `src/style.css`, `src/app.js`, `src/products.json`, generated/source tokens, and supplied screenshot evidence. Initial browser-evidence HTML SHA-256: `41b7fb0a7c1111cbd275b8dfa44c4cd665d9c3847e7f3dc4d2dbed33e4c76405`. Implementation was actively being revised during this round; findings below are checkpoints for the final rebuild, not a claim that the initial evidence describes the final artifact.

## Creative direction verdict

The revision retains the recognizable graphite/gold/ribbon identity and establishes a much clearer distinction between parent and product. The editorial navigation, generous cover hierarchy and repeatable product chapters make the bible easier to use. The product cover marks read at mobile size. PI is visibly a bold mathematical pi, as requested. The Unfazed white stage and original face give it a meaningfully different visual voice; the three additional concepts remain clearly labelled proposals.

The structure now separates source observation, recommendation and proposed identity. MemoryTree is explicitly the provisional fifth product, while Flame Chorus remains visible in the architecture. This resolves the main efficacy problem from round 1.

## Independently inspected images

Opened with the image-view tool, not inferred from filenames:

- `cover-light-1440.png`: strong hierarchy and generous desktop composition; parent mark, navigation and product index fit.
- `cover-dark-390.png`: clean single-column cover; complete headline, clear contents control and legible product labels.
- `fireflow-light-1440.png`: orange mark/headline consistent; balanced content and symbol.
- `privateinference-light-390.png`: bold pi survives small format; no clipped symbol or copy; deliberate separation of mark, positioning and endorsement.
- `unfazed-light-1440.png` and `unfazed-dark-390.png`: original face on white, flat geometry and restrained system typography visibly distinguish the brand.
- `lanni-light-1440.png`: coral mark/headline and short human-facing proposition read clearly.
- `memorytree-dark-390.png`: branch symbol, sky accent and provisional label remain readable.
- `shape-light-1440.png`: radius examples are aligned and their captions fit.

These initial screenshots use fallback typography. Font assets and a second screenshot pass are already in progress; final visual acceptance must use the bundled Red Hat families. The images named for each product currently show its cover, not the lower interactive specimen.

## Round-1 disposition

| Earlier finding | Disposition in revision |
|---|---|
| D01–D03 fixed-surface inheritance and low-contrast specimen text | Resolved in current code: dark stages own explicit foregrounds; muted text is solid; unsafe green/grey/gold examples were removed or corrected. Initial browser matrix reports no failing text pairs. |
| D04–D06 navigation, implicit columns and clipped co-brand | Resolved by rebuilt responsive layouts. Initial matrix reports no page/content overflow across 320, 390, 768, 1024 and 1440px in both themes. |
| D07 comparison matrix dark text rule | Resolved: separate light/dark semantic foreground rules replace the contradictory legacy matrix. |
| D08 disputed proof numbers | Resolved: disputed counts live only in the decision register, with inherited PDF findings clearly archived. |
| D09 dead buttons / incomplete state contract | Resolved: action specimens give local feedback, native disabled state is present, field error/recovery is demonstrated, and loading/pressed/focus rules are documented. |
| D10 nested radii | Resolved: visible specimen and prose agree on40px outer /8px inset /32px inner. |
| D11 type/token mismatch | Substantially resolved: a complete type scale is generated from tokens. New product-specific sample mismatches are listed below. |
| D12 universal vw/mobile multiplier | Resolved: bounded fluid values, explicit thresholds and gutters replace the universal multiplier. |
| D13 misleading size floors/chips | Resolved: realistic metadata exception is documented; pill wrapping issues from original are removed. |
| D14 navigation/heading/copy accessibility | Substantially resolved: skip link, active contents, theme control, heading order and announced copy fallback added. Initial copy-feedback check is still failing in browser evidence; root is investigating async test timing. |
| D15 gold on cream | Resolved: deeper `#76580D` is used and calculated. |
| D16 naming/casing | Resolved: specimens consistently use sentence case; product-specific lowercase exception is explicit. |
| D17 resilient fonts | In progress: requires bundled-font loading evidence and refreshed screenshots. |
| D18 provenance/authority | Resolved: working edition, original archive, source inventory, decisions and proposed status are explicit. |

## Findings for round 3

| ID | Priority | Evidence | Required correction / verification |
|---|---|---|---|
| R2-D01 | P1 verification | Initial `browser-qa.json` has `structure.fonts: []`; initial screenshots show fallback families. | Finish font bundling, verify all three Red Hat families actually load, and refresh desktop/mobile cover and product evidence. A fallback-only visual pass cannot certify the chosen typography. Root has already assigned this. |
| R2-D02 | P2 | `src/products.json` Lanni specifies16px chat /1.6,24px conversation panels and16px between speakers; `src/style.css` `.chat-bubble` is14px, `margin-top:12px`, and `.product-ui` defaults to16px radius. | Make the live Lanni specimen demonstrate its own contract:16px chat,16px between messages and24px outer conversation panel, or explicitly revise the stated rules. Increasing type should be rechecked at320/390px. |
| R2-D03 | P2 | PI mark spec calls clear space “one stem width (12/96 of the mark viewBox)”; SVG right stem spans x57…73, i.e.16 units. | Correct the clearspace measure to16/96 or deliberately change the vector geometry and document the resulting stem. |
| R2-D04 | P2 | Parent logo table minimum ribbon40px; mobile header `.wordmark svg` is34px. | Make the mobile specimen comply with40px minimum or explicitly document34px as the compact-header exception. Verify320px header fit with loaded Red Hat. |
| R2-D05 | P3 | MemoryTree mark spec says “three-branch tree”; SVG has three nodes with two child branches. | Rename it a “three-node tree” or “root with two branches” for a measurable, accurate construction description. |
| R2-D06 | P2 verification | Product screenshot loop selects `.product-cover`; no actual lower `.product-ui` screenshots were available in the first set. | Add desktop/mobile captures of at least Lanni, Unfazed and PI interface specimens and independently inspect them. The original task includes spacing/design errors, so product-cover evidence alone is insufficient. |

No menu-focus bug is reported: the rail wordmark is a non-link span, so its first anchor is a visible navigation entry. Using `.nav-link` explicitly is a sensible clarification, but the original selector is not itself a demonstrated defect.

## Round-3 release gate

Accept the design revision once the six findings above are resolved or explicitly dispositioned, browser copy success/fallback checks pass, all selected fonts load, and refreshed visual evidence shows actual product specimens as well as covers. Existing caveats about no assistive-technology or cross-browser certification remain appropriate. The provisional fifth-product choice and proposed brand concepts are owner decisions, not implementation failures.
