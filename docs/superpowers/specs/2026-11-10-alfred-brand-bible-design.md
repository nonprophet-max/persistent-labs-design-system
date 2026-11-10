# Alfred brand bible — design brief

Date: 10 November 2026  
Status: Approved by Max; implementation authorised with “approved please continue”.  
Owner: Max Rabinovitch

## Purpose

Create a clear, useful Alfred brand bible that people can explore and share, and that AI tools can use to produce consistent Alfred material. Alfred becomes a product-level module in Persistent Labs' central brand library, alongside FireFlow, Private Inference and the other existing identities.

This work defines the brand's expression and application. It does not define Alfred's product capabilities. Any illustrative application exists to demonstrate the brand rules.

The two deliverables are one system:

1. A hosted, interactive Alfred brand walkthrough within the existing central library.
2. A matching, self-contained `alfred-brand` skill and chatbot-readable package in the same Git repository.

## Target library

- Repository: [nonprophet-max/persistent-labs-design-system](https://github.com/nonprophet-max/persistent-labs-design-system).
- Existing branch: `codex/design-bible`; use an isolated feature checkout for implementation and verify the current remote before integration.
- Primary hosted destination, changed by Max during implementation: [GitHub Pages](https://nonprophet-max.github.io/persistent-labs-design-system/), built from `dist-pages/`. Migrate the whole central library, not only Alfred.
- Intended Alfred URL: `https://nonprophet-max.github.io/persistent-labs-design-system/products/alfred/`.
- Preserve the single-page reading edition as a generated/downloadable artifact; GitHub Pages becomes the primary hosted library. Historical Netlify URLs are source history.
- Relevant current local source checkout: `/Users/max.rabinovitch/.codex/.chatgpt-projects/g-p-6ab3b7765b2881919a97d1559cbda6a6/persistent-labs-design-system`.

## Agreed foundation

Preserve the supplied v0.3 identity while refining its documentation and implementation:

- Ink `#3E3D3D`, secondary ink `#6A665F`, paper `#FFFBF7`, sand `#ECE7DC`, and restrained yellow `#F2BD3C`.
- Instrument Serif 400 for headings; Outfit for body copy and controls. The existing Cormorant Garamond Cyrillic heading companion is declared explicitly.
- Supplied outlined star-and-wordmark logos, standalone star marks, and both supplied butler illustrations.
- A 1.5px outline, 28px card corners, 36px capsules, pill-shaped buttons, generous spacing and controlled overlaps.
- “Life, handled.” and “Find it. Book it. Buy it.” as the existing brand language.
- Capable, warm, direct and lightly playful writing.

The original handoff remains intact. Its older Apple/ITC Garamond targets, pink/blue identity and superseded review decisions become history rather than conflicting live instructions.

New application recommendations must be identified as recommendations. They must not masquerade as instructions found in the original reference.

## Readers and success

The bible serves people making Alfred material and AI tools helping them do that work. A person should be able to understand the identity, find an exact rule, compare an example, and obtain the right asset without searching through historical reviews. An agent should be able to load the Alfred skill without the parent repository and apply the same rules.

Success means the human and AI editions agree, the page is usable on a phone, downloads contain their dependencies, and the Alfred chapter joins the central library without altering the other product identities.

## Approaches considered

### A. Extend the existing central library — recommended

Add an Alfred product module and dedicated walkthrough at `/products/alfred/`. Retain the library's navigation and generate the Alfred web chapter and portable package from shared Alfred sources.

This follows the existing product-plugin architecture, gives Alfred a clear home, and reduces duplicated maintenance. It requires a focused extension to the existing generators and resource registry.

### B. Keep a separate Alfred microsite and link to it

This would preserve the handoff's existing site structure, but leave two navigation systems and two release locations to maintain. It is a weaker fit for the requested central brand library.

### C. Publish the supplied HTML and ZIP unchanged

This is quick, but retains broken links, conflicting sources, font defects and a static reading experience. It does not meet the refinement brief.

The proposed build follows A. Max has approved beginning work on the central-library/skill outcome; this document is the first concrete design checkpoint for that work.

## Walkthrough structure

Keep the central library's established shell and product navigation. Alfred's chapter uses a scoped product identity, with no global replacement of Persistent or other product styles.

The chapter contains these navigable sections:

1. **Meet the identity:** concise brand introduction, supplied logo and one butler illustration, signature palette and an explanation of its character.
2. **Logo and mark:** supplied light/dark variants, clear space, sizing and background examples, downloadable SVGs, and illustrated misuse.
3. **Colour:** named palette, practical accent rules, readable pairings and examples of balanced versus excessive yellow.
4. **Typography:** real bundled fonts, heading/body roles, readable hierarchy and a live type specimen with editable sample text.
5. **Shape and spacing:** outlines, corners, layout relationships, cards, capsules, buttons and links; examples show the actual rules.
6. **Voice:** concise tone principles and paired examples demonstrating warm, direct, capable copy without inventing product claims.
7. **Brand in use:** a small set of illustrative applications, such as a report cover, presentation panel and compact communication example. Each demonstrates identity and is labelled as an illustration where needed.
8. **Use the brand:** logo/asset downloads, exact tokens, complete skill ZIP, skill entrypoint and plain chatbot instructions.

The precise arrangement within each section is left to the builder. Preserve the supplied identity and favour useful examples over decorative novelty.

## Interaction and accessibility

- Chapter links and section anchors support direct sharing and browser history.
- Copyable colour values and specifications provide visible and announced feedback; copy failure offers selectable text.
- Logo and asset previews allow comparison on suitable light/dark backgrounds. These previews do not claim to define a new complete Alfred dark theme.
- A type specimen accepts user text and demonstrates heading/body roles. Unsupported scripts are identified honestly.
- Paired correct/incorrect examples explain the relevant rule in text as well as visually.
- Resource links remain usable without JavaScript. Essential brand guidance is readable without interaction.
- Controls work with keyboard input, have visible focus, and meet the supplied 44px minimum target rule. Input text is at least 16px.
- Layout supports narrow phones, long labels and larger text without horizontal page overflow or hidden essential copy.
- Motion stays restrained and respects reduced-motion preferences.
- Keep code examples readable without importing an unrelated monospace identity into Alfred's branded prose. Technical text can wrap.

## Authority and source organisation

Use one maintained Alfred source for live brand rules and one canonical Alfred token file. The existing library's `src/products.json` and `tokens/design-tokens.json` remain the entrypoints for product registration and parent integration. A focused Alfred-specific source may hold the detailed rules and examples if that keeps the generic generators small; document its role and prevent a second editable version of those rules in generated outputs.

The web chapter, skill references, chatbot guide and downloadable package derive from these maintained sources. Generators may copy supplied binary assets, but must not redraw or recolour the supplied logos and illustrations during routine builds.

Historical reviews and the original handoff can remain a clearly separated source archive. Public guidance should present current rules directly rather than making a reader reconstruct approval chronology.

The `Report v5` reference is described by the handoff but absent from the ZIP. On 10 November 2026, Max explicitly instructed us to develop from the existing assets while it is missing. The supplied v0.3 assets and latest explicit token/font decisions therefore provide the visual basis. Report v5 is not a build or release dependency; do not claim to have compared the result against it.

## Font defect and multilingual honesty

The supplied `outfit-variable-cyrillic.woff2` has no Cyrillic glyphs. Do not redistribute it under that misleading description or claim that Outfit covers Cyrillic based on the filename.

Official Google Fonts metadata lists Outfit's `latin`, `latin-ext` and `menu` subsets; it does not list Cyrillic. The original Outfit repository's Cyrillic request remains unresolved. Sources checked for this review: [Google Fonts metadata](https://raw.githubusercontent.com/google/fonts/main/ofl/outfit/METADATA.pb) and [the official Cyrillic request](https://github.com/Outfitio/Outfit-Fonts/issues/6).

Proposed release default: preserve Outfit for its supported text. Correct the mislabeled subset to Latin-ext and explicitly document the existing `system-ui` fallback for Cyrillic body text; do not claim cross-device typeface consistency for that fallback. Keep the bundled Cormorant Garamond Cyrillic heading companion. For this release, that documented body fallback is an acceptable stated limitation and does not block publication. A new bundled body companion that materially changes the identity would be a separate decision for Max, rather than a silent font substitution.

The heading companion must remain identified as Cormorant Garamond, even when CSS uses a shared family alias. Retain the bundled SIL Open Font License notices.

## Portable AI package

Add the standalone plugin using the existing `plugins/<name>/skills/<name>/` convention and register it in the central brand registry and supported plugin catalogs.

The Alfred package includes:

- A concise `SKILL.md` with accurate discovery metadata and task-based links to deeper references.
- Exact current brand guidance, typography/spacing instructions, token JSON/CSS and the supplied approved-use assets.
- Fonts and their licences; asset source/status records that distinguish brand ownership from open font licences.
- A plain `chatbot.md` for attachment or pasting into ordinary chat tools.
- A complete downloadable ZIP preserving relative file paths.
- Existing host-specific metadata/manifests as supported by the central library.

`$alfred-brand` works in tools that support that invocation. A text-only chatbot can use the writing/specification guidance; rendering, font loading and script execution require appropriate tools. No universal automatic installation or tool execution is promised.

The skill cannot grant publishing, account, deployment or purchasing authority. It applies the user's brief and the Alfred brand rules within the actual task.

## Assets and rights records

Use the supplied logo/mark and both supplied mascot assets. Record their origin as owner-supplied handoff assets; do not invent creator attribution or a general redistribution licence.

The handoff records a prior decision to use the mascot despite a resemblance concern. Preserve that record without presenting it as legal clearance. The portable package grants no general ownership or trademark rights to third parties.

The supplied raster linework does not exactly equal the stated ink token. Keep the images intact and describe their actual status rather than claiming pixel-perfect palette conformity.

Move or clearly label retired pink/blue examples as historical. The optional card remains a documented future application; a new card identity is outside this release.

## Validation and bounded review

Use targeted checks based on the known defects and actual deliverables:

1. Generated rules/tokens and package assets agree; regeneration is deterministic.
2. Local and hosted-path HTML/CSS links resolve, including downloads and font URLs.
3. Font files contain the glyphs claimed by their CSS declarations.
4. The independent Alfred package has no hidden parent-repository or local-machine dependency.
5. Browser checks cover Alfred at 320, 390, 768 and 1440px, library light/dark reading modes, keyboard access, copy fallback, long labels, larger text and actual font loading.
6. Existing library checks continue to pass for the other identities; focus additional visual review on changed shared surfaces.
7. Independent strategy, visual and accessibility review uses actual rendered screenshots. A fresh agent also exercises the skill with a realistic brand-design task.

Collect material findings once, fix them in a batch, then verify those fixes. Reuse evidence for unchanged material. Stop when the acceptance checks are met; do not add repeated open-ended audit rounds.

## Publication and review checkpoints

Max requested hosting and Git publication on completion. Prepare and verify the complete Alfred addition before that final stage. Publish only intended public site output and the intentional portable brand package; do not accidentally expose unrelated local files or review material through a deployment.

Max subsequently instructed migration of the whole site from Netlify to GitHub Pages. Before release, verify the current GitHub branch and Pages state. Add repository-base-path support, a reproducible Pages build/deploy workflow and verify all existing product pages, Alfred, AI resources and downloads at the new URL. No Netlify authentication or credit change is a dependency.

Review checkpoints:

1. This design brief: confirm the intended brand-bible structure and implementation boundary.
2. A working visual preview: review identity fidelity and usability before final packaging.
3. Final verified release: review the walkthrough, portable skill and hosted/Git links together.

Questions should concern a decision that changes the brand or the deliverable. Routine implementation fixes remain the builder's responsibility.

## Acceptance

- Alfred appears as a peer product identity within the existing central brand library.
- The walkthrough is interactive, shareable, responsive and faithful to the supplied v0.3 direction.
- Brand rules, examples and resources are easy to find and agree with the skill.
- The standalone skill, plain chatbot guide and full asset package work without the parent installation.
- Known font, link, authority and obsolete-example defects are resolved or explicitly documented where a brand decision is still required.
- Existing product identities and source archives remain intact.
- Review evidence supports the completion claims; remaining limitations are disclosed plainly.

## First-checkpoint review

A fresh builder reviewed this brief for questions that would materially affect planning. The target repository/site has now been added, and the proposed first-release handling of Cyrillic body text has been made explicit. No unresolved implementation question remains that requires reopening Alfred's capabilities or the established v0.3 identity.
