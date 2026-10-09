# Rebuilt Pi package: forward-test closure

The blocking CSS mismatch is closed. The generated portable package now exports the Pi light/dark surface mappings from `identities.privateinference.surfaces`; all 20 semantic values exactly match the JSON. Both same-element and descendant fixed surfaces are scoped, and each gets the Poppins font assignment.

| Role | Light surface | Dark surface |
| --- | --- | --- |
| Surface | `#FFFFFF` | `#1A1A1A` |
| All readable text roles | `#1E1E1E` | `#F5F5F5` |
| Action | `#FBD78E` | `#E5B14A` |
| On action | `#1E1E1E` | `#1A1A1A` |
| Hover | `#E5B14A` | `#FBD78E` |
| Pressed | `#FBD78E` | `#E5B14A` |
| Control border | `#7F7F7F` | `#BFBFBF` |
| Focus | `#1E1E1E` | `#FBD78E` |

The JSON implementation note specifies a 2px inset on-action-colored edge on press, and a 3px focus outline with 4px offset. The brand reference describes these choices as implementation guidance. Hover now visibly swaps the two supplied golds. Component CSS must implement the inset edge and consume the exported variables; the token stylesheet is not a full component library.

Computed contrast checks pass for normal text and action labels in default, hover and pressed states, and for control borders and focus rings against their surfaces. Light control outline: 4.00:1. Dark outline: 9.47:1. Dark focus: 12.61:1. Font choices, control targets and reduced-motion guidance remain consistent.

The shared foundations naming table and imagery/motion paragraphs now say **Pi**, closing the prior uppercase-PI inconsistency.

No remaining substantive contradiction prevents implementing the illustrative hero and panel. Two minor documentation considerations remain:

- The shared foundations contrast table still labels pale gold on parent graphite as “Private Inference dark accent.” This remains a valid accessible pair, but it is not the canonical Pi dark-surface mapping. The product-specific mapping is explicit and takes precedence; clearer table labelling would reduce ambiguity.
- The generic `products.privateinference.pressed` value remains `#E5B14A`, whereas the canonical light semantic `action-pressed` is `#FBD78E`. Generated CSS resolves this correctly through the more-specific surface rules. Developers should consume `--action-pressed`, not bypass the semantic mapping by directly consuming `--product-pressed`. A legacy/fallback note would make that distinction clearer.

Unspecified product facts remain deliberate boundaries: audience, positioning, tagline, capabilities, availability and operational settings cannot be inferred from a visual identity. These do not block the labelled concept described in the original report.

Only the allowed forward-test artifacts were edited. Verification was static file inspection plus token equality and contrast calculations; no browser or PDF rendering was performed during this recheck.
