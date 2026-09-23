# Website and brand skills — edition 2.3

Owner direction: include .com and a bold orange dot in Galactica’s logo; make the bible a navigable website, publish a share link on Netlify, and commit the full design system and individually callable product brand skills to a private repository under nonprophet-max.

## Changes

The Galactica.com wordmark uses outlined Red Hat Display 700 lettering and an orange #F7931A dot. This is an owner-directed adaptation, not a recovered website master. The large chapter lockup, local interface specimen, specifications and downloadable SVG all use the full name. The copper interface palette remains separate from the orange logo dot.

A sticky navigation bar links foundations, products, tokens and guidelines. Chapter navigation remains available, with a Contents control on small screens. The site-only build includes the current bible, assets and tokens; private source archives, review files and plugins are excluded from the public upload. References to those archives are unlinked in the public page.

Six standalone packages contain SKILL.md, Codex and Claude plugin manifests, brand and foundation references, scoped JSON/CSS tokens, relevant vector assets, font licenses and a consolidated chatbot.md. The parent skill contains the full bible. Product packages operate without the parent package. FireFlow’s components remain subordinate.

## Validation

- 87 token contrast pairs; hierarchy, heading, anchor, local asset and font checks.
- Six plugin manifest and skill-frontmatter validations. The bundled validators ran unchanged with a bridge to an installed Node YAML parser because PyYAML was unavailable.
- Standalone reference paths, token parity, SVG parsing, font references and chatbot documents checked by the repository’s dependency-free package check.
- Public build local links and exclusion of private directories checked.
- Independent forward-test reviewed a portfolio handoff and standalone FireFlow/Galactica use. Its findings are recorded separately.
- Chromium verification completed on 23 September 2026 after approved browser access: all five widths and both themes pass, with no runtime errors or request warnings. All 52 local screenshots and two production screenshots were visually reviewed with no material layout findings.

The original design bible is preserved unchanged. The [reading site](https://persistent-labs-design-bible.netlify.app/) is published on the existing Netlify project. The [GitHub repository](https://github.com/nonprophet-max/persistent-labs-design-system) is published on `codex/design-bible` with private visibility verified. Live checks pass for 19 files, 45 navigation actions and six private paths returning 404. Netlify’s hosting comment, public badge script and final newline are the only differences between the uploaded and served HTML. See [release verification](release-verification.json) and [deployment verification](deployment-verification.json).
