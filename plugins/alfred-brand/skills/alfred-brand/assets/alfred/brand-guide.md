# Alfred brand guide

Current v0.3 · 2026-11-10

This guide and its exact tokens define the current Alfred identity. Apply these rules within Alfred material and preserve the host brand around it.

## Meet the identity

Life, handled.

Alfred brings a calm, contemporary interface together with the character of 1930s rubber-hose animation. Warm paper, expressive serif headlines and a capable butler give the identity its personality. Thin outlines and generous space keep it modern.

Use “Life, handled.” as the brand promise and “Find it. Book it. Buy it.” as the functional language. Keep the voice capable, warm and direct.

Persistent Labs remains the host identity. Scope Alfred’s fonts, colours and components to Alfred material; keep the surrounding navigation and other product identities distinct.

## Logo and mark

A signature with a little flourish.

Use the supplied outlined star-and-wordmark logo. Preserve its proportions, trail and lettering; never retype it. The standalone star is for small spaces such as avatars and footers.

Use ink artwork on paper or sand, and paper artwork on an ink field. Header logo height: 24px (approximately 132px wide). Footer mark height: 22px. Keep roughly half the visible wordmark height clear on every side.

Do not stretch, outline, recolour yellow or place the artwork on an unprepared photograph. The white fill inside SVG clip paths is a technical mask. The lowercase Archivo Black wordmark and earlier character-head logo are retired.

## Colour

Warm neutrals. A purposeful yellow.

Paper is the main canvas; sand groups supporting material; ink carries text and outlines. Secondary ink creates hierarchy on paper and sand. Pure black, pure white and the retired pink/blue palette are not current Alfred colours.

Use yellow for a primary action, one warning/callout per screen, small meaningful markers or the hero circle decoration. Never flood a section, colour its heading, or use yellow for resting link underlines.

Use ink text on yellow. Secondary ink belongs on paper or sand, not yellow. The proportion study below is an application recommendation, not a fixed mathematical brand ratio.

## Typography

A characterful headline. A clear next step.

Instrument Serif 400 is the approved heading face. Outfit handles body copy, controls, captions, numbers and prices. Headings use −0.005em tracking; body copy stays at 16–17px with generous leading. Nothing is smaller than 14px.

Instrument Serif includes Latin and Latin-ext. Cyrillic headings deliberately use bundled Cormorant Garamond 400 under the Instrument Serif CSS alias. Outfit has no supplied Cyrillic coverage: Cyrillic body text uses system-ui fallback and varies across devices.

Load the bundled font files with their SIL OFL notices. Keep the fonts folder alongside the supplied font stylesheet, and preserve the declared script ranges. Other unsupported scripts use the documented fallback.

## Shape and spacing

Room to breathe. One clear outline.

Use one 1.5px solid ink outline, with no shadows or doubled borders. Cards and photos have 28px corners, header/footer capsules 36px, and buttons and pills 999px.

Use a maximum container width of 1240px and clamp(20px, 5vw, 56px) side gutters. Sections have a top rule, 36px top padding and clamp(56px, 7vw, 96px) bottom padding. The title rail is 220px, the content basis 560px, and the gap 56px; wrap the rail above content when needed.

Cards use 24–32px internal space, 14px between related cards and 56px between lots. A permitted pair of stat tiles overlaps by 24px; overlap is controlled, never essential text over text. Listing photos keep a fixed 7:6 ratio. No barcodes.

Primary buttons use ink text on yellow and reverse to yellow text on ink on hover. Links are ink and underlined; hover makes the underline yellow and 2px thick. Keep controls at least 44px high and editable text at least 16px.

## Voice

Useful first. Warm throughout.

Write like a capable, friendly concierge: direct, warm, calm and lightly playful. Lead with the useful outcome. Choose familiar verbs and concrete actions.

Be precise about what happened and what still needs a decision. Humour stays away from money, consent, failures and sensitive choices. Avoid inflated AI language, invented savings and promises that Alfred can do everything.

Product messages in this bible are illustrative future copy. “Completed” requires evidence in a real product; confidence alone is not a confirmation.

**Invitation:** Your next move starts with a message. Avoid: Unlock limitless AI-powered possibilities. Offer a familiar starting point.

**Approval:** Review the details before you approve. Avoid: Relax. We’ll take care of everything. Keep the decision visible and specific.

**Recovery:** The booking wasn’t confirmed. Here’s the next option. Avoid: Oops! Something went wrong. Name the problem and give a next step.

## Brand in use

The same character, wherever it appears.

These report, presentation and communication examples are illustrative brand applications, not product screenshots or evidence of a deployed service. They demonstrate typography, proportion, hierarchy and tone.

Use the supplied butler once in the introduction, facing into the content. The light-ground file has semi-transparent face/gloves; the dark-ground file has paper-coloured opaque details. Choose the matching file, never fake it with a CSS filter. Preserve the supplied raster bytes; their linework is not pixel-exact to the ink token.

The owner elected to use the mascot as supplied despite the recorded resemblance concern; that is a brand decision, not legal clearance. A future Alfred card remains a verbal concept only. No new card visual, issuer/network branding, credentials or benefits claim is approved here.

## Use the brand

Everything starts from the same source.

Use the outlined SVGs, supplied illustrations and bundled fonts. Download the exact tokens and current guide below. Preserve relative asset paths when moving a complete package.

For an AI task, supply the current guide and assets, state what you want to make, and ask the agent to apply the Alfred identity locally. A text-only chatbot can help with writing and specifications; rendering and font loading require suitable tools.

The source guide and portable tokens are generated from the same maintained rules as this chapter. Brand assets are owner-supplied; this package grants no general ownership, trademark or redistribution rights. Fonts retain their individual OFL licences.

## Exact colours

| Token | Value |
| --- | --- |
| ink | `#3E3D3D` |
| ink2 | `#6A665F` |
| paper | `#FFFBF7` |
| sand | `#ECE7DC` |
| accent | `#F2BD3C` |
| line | `#3E3D3D2E` |

## Exact type roles

| Role | Family | Size | Weight | Line height |
| --- | --- | --- | --- | --- |
| h1 | Instrument Serif | clamp(40px, 6.4vw, 76px) | 400 | 1.08 |
| h2 | Instrument Serif | clamp(36px, 3.6vw, 44px) | 400 | 1.08 |
| h3 | Instrument Serif | clamp(30px, 3vw, 36px) | 400 | 1.14 |
| lead | Outfit | clamp(18px, 1.9vw, 21px) | 400 | 1.55 |
| body | Outfit | 16px | 400 | 1.6 |
| caption | Outfit | 15px | 500 | 1.4 |
| control | Outfit | 15px | 600 | 1.3 |
| pill | Outfit | 14px | 500 | 1.3 |
| stat | Outfit | 48px | 400 | 1 |
| price | Outfit | clamp(34px, 3.4vw, 40px) | 400 | 1.05 |

## Files

Use `tokens.json`, `tokens.css` and `fonts.css` beside this guide. Preserve the `fonts/`, `logos/` and `illustrations/` folders. See `ASSETS-LICENCES.md` and `provenance.json` for rights and origin.
