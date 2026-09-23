# Round 1 — independent creative direction and design QA

Reviewer: design-audit agent. Date: 23 September 2026.

Source: `/Users/max.rabinovitch/Desktop/persistent-labs-design-bible.html` (read-only, 892 lines).

Method: full HTML/CSS/content inspection and independent sRGB contrast calculations using alpha compositing. This round does not claim screenshot or screen-reader testing. UI/UX skill used as an audit checklist, without replacing the supplied identity with a generated palette.

## Creative assessment

Preserve the actual identity: Red Hat typography, graphite `#1C1E21`, gold `#FBD78E`, the four-stroke infinity mark, soft large containers, warm light collateral and restrained aurora. The original has strong visual specificity and useful production details. Its main weakness is that observations from several sources are promoted into universal rules even when they contradict each other or the specimens. A usable bible must distinguish observed legacy values, current approved rules and proposed product directions.

The expanded edition needs a clear family architecture before five separate product chapters. Master brand endorsement should remain stable, while each product gets its own audience, promise, accent, mark treatment, geometry, imagery, voice and component example. Accent color alone is not sufficient differentiation. Avoid repeating five near-identical master-brand cards.

## Prioritized findings

| ID | Priority | Evidence in original | Problem and recommended fix |
|---|---|---|---|
| D01 | P1 | Lines 127–128; fixed dark type stage at 463–470 | `.spec .lab` reads global `--muted` and `--ink`. In light page mode these are dark ink, making labels disappear on the fixed ink stage (bold labels reach **1.00:1**). Scope semantic foreground/border variables on each fixed dark/light stage. Test specimens in both document themes. |
| D02 | P1 | Lines 15, 61, 70, 73, 84, 96, 103, 116, 127, 194, 211 | Light-page muted ink at 58% gives **4.15:1 on white** and **4.05:1 on paper**, used repeatedly at 11–14.5px. Raise muted contrast, preferably a solid semantic text color, and test every surface rather than judging one swatch. |
| D03 | P1 | Lines 170, 187–188, 350–355, 379, 650, 661 | Actual specimen contrast fails: stat-card body ink60 on paper **4.31:1**; white on success green **2.995:1** at 11.5px; white on `#A07D19` **3.86:1**; white on `#7C7C7C` **4.17:1**; white on `#818181` **3.90:1**. Use ink text for bright chips/action fills and stronger body text. |
| D04 | P1 | Lines 155–157 and 597–601 | Navigation combines fixed 64px height, wrapping flex and wide navigation. The viewport breakpoint is 760px, but its stage can be substantially narrower than the viewport. Use container-responsive specimen behavior or min-height with a deliberate stacked/mobile navigation variant. Do not simply hide overflow. |
| D05 | P1 | Lines 90, 136, 649–652 | `grid-column:span 2` on the aurora panel creates an implicit extra column when the auto-fit grid reaches one column. Parent stage then clips overflow. Reset to `1 / -1` or use a scoped responsive grid. Verify 320, 375, 768, 1024 and 1440px. |
| D06 | P1 | Lines 279–294 | Horizontal co-brand lockup contains master mark, long name, divider and FireFlow wordmark inside a narrow three-column grid. `overflow:hidden` conceals the problem. Give the co-brand a full-width stage, reduce at a clear breakpoint or introduce an approved narrow lockup composition. Do not distort the mark. |
| D07 | P1 | Lines 401–408, 672 | Comparison matrix defines dark fills but prescribes ink text for every theme. Ink text on dark tinted fills will fail severely. Define separate light and dark foregrounds and ensure strength/partial/gap are explicit words or symbols as well as colors. |
| D08 | P1 | Lines 770, 806 versus 644; lead at 467 and PDF review 735–791 | The bible warns that node counts are disputed, yet publishes `320+ typed building blocks` as specimen copy. It also repeats unverified performance, regulatory and PDF-derived claims as facts. Remove disputed numbers from canonical specimens or visibly label them examples/source observations; retain provenance and approval status. Current PDF audit should be identified as inherited if the actual PDF was not inspected in this session. |
| D09 | P2 | Lines 144–151, 218, 599, 608–614 | Several displayed buttons are dead interactions; ghost buttons are 38px high; the outline button has no defined hover or active state. Label specimens as examples and provide meaningful local demo feedback, or render them as noninteractive specimens. Document default/hover/focus/pressed/disabled/loading states and adopt a consistent 44px target policy. |
| D10 | P2 | Lines 178–179 versus 564 and 371 | Aurora border is 6px wide with outer radius40/inner36, while its radius difference should be6; prose says 8px and ring80→72. Pick one canonical relationship and make the specimen and token sheet demonstrate it. Rule: inner radius=max(0,outer radius−border thickness). |
| D11 | P2 | Lines 441–459 versus 849–866 | Token sheet and typography table disagree: `display` mobile55 versus token44; h3 mobile32 versus token26; h4 mobile26 versus token24. h2/h5/body-l/tag tokens are missing. Mobile container is mentioned only in a comment, never implemented. Generate both table and copyable CSS from one explicit token model, or revise all values together. |
| D12 | P2 | Lines 495–507, 525, 865–866 | Proportional vw is described as a universal rule, leaving text and spacing scaling from an artboard rather than content needs. The stated mobile multiplier (~2.9) is also inconsistent with the section-padding example (11.9vw/9.375vw≈1.27). Replace the multiplier with bounded fluid values, explicit gutters and documented layout thresholds. Keep historical dimensions as observations. |
| D13 | P2 | Lines 95, 112, 140, 487 | `white-space:nowrap` tags can exceed narrow cards; small swatch tags use white on translucent black over bright swatches (e.g. gold yields **3.25:1**). Caption ink55 on paper is **3.70:1**. The declared “never below14px on screen” rule conflicts with dozens of 11–13px labels. Set realistic text-role floors, allow long tag wrapping and make chip contrast independent of the underlying swatch. |
| D14 | P2 | Lines 242–263; 269–274; 642–651; 878–885 | No skip link, current-section indication or explicit theme selector; headings skip levels in some cards; clipboard feedback has no live region and assumes ⌘C for fallback. Add skip navigation, active TOC with `aria-current`, theme control, consistent heading semantics and announced copy feedback with platform-neutral fallback wording. |
| D15 | P2 | Lines 358, 403–407 | Gold-ink `#8B6914` is described as suitable for white or cream. It is **5.09:1 on white**, **4.71:1 on paper**, but only **4.05:1 on dawn `#FAE3B6`**. Supply a deeper light-surface gold for cream, or restrict its allowed pairings explicitly. |
| D16 | P2 | Lines 480, 608, 613, 714, 805 | Sentence-case rules conflict with title-case buttons and voice guidance allowing Title Case. Normalize all live examples and publish one rule. Also replace “institution teams” with “institutional teams” (651). |
| D17 | P2 | Lines 9, 485, 710–715 | Google Fonts is the only typography source; offline rendering silently substitutes Arial even though prose bans system fonts. Keep a truthful fallback policy and preferably ship licensed font assets for a portable handoff. Distinguish nominal brand family from resilient implementation. |
| D18 | P2 | Lines 259, 734–808, 876 | A long forensic PDF review and unresolved choices are given the same authority as current rules. Add a release status, source inventory and decision log; label archived observations as such. Keep new product proposals clearly separated from established product facts. |

## Measured contrast values

Calculations use WCAG sRGB relative luminance, with source alpha composited over the declared background. They are deterministic checks of the CSS pairs; they are not a blanket accessibility certification.

| Pair | Ratio |
|---|---:|
| Ink at 58% / white | 4.152 |
| Ink at 58% / paper | 4.051 |
| Ink at 60% / paper | 4.308 |
| Ink at 55% / paper | 3.701 |
| White / success `#24AC2B` | 2.995 |
| White / gold step `#A07D19` | 3.859 |
| White / `#7C7C7C` | 4.174 |
| White / `#818181` | 3.896 |
| Gold-ink / paper | 4.707 |
| Gold-ink / dawn `#FAE3B6` | 4.052 |
| White / black35 over gold | 3.254 |

## Product design direction

- **FireFlow:** execution clarity. Keep existing orange as identification; use flow nodes, ports and step/state relationships as the visual grammar. The user's supplied FireFlow identity takes precedence over an invented replacement. Use orange accessibly, with a dark orange foreground on light surfaces.
- **Unfazed.dev:** its live visual identity and product promise must be researched before assigning colors or language. A consumer calm brand and developer observability brand would need different systems; the name alone is insufficient evidence.
- **Lanni:** action-oriented assistance with a more human rhythm. Preserve coral as a differentiator and use chat/action-card examples, not another generic orchestration graph. Default/selected/confirmed states should remain unambiguous.
- **PrivateInference / PI:** upcoming concept; the requested logo is a **bold π**. Use an outlined/custom vector mathematical pi with controlled weight rather than a font-dependent Unicode glyph. Define monochrome versions, clearspace, minimum size and endorsed lockup. Do not invent privacy/security guarantees from the name alone.
- **Fifth sub-product:** user named four; fifth needs an explicit documented assumption or clarification. Existing MemoryTree and Flame Chorus are candidates, but choosing one should not silently erase the other from the architecture.

## Next-round acceptance gates

1. Both page themes and all fixed specimen surfaces remain readable; no text pair below4.5:1 unless a precisely documented large-text exception applies.
2. No horizontal page overflow or clipped lockups at320/375/768/1024/1440; dense tables may scroll in labelled containers.
3. Five separately specified products with visible provenance and no invented technical or launch claims; retain related stack components.
4. Typography, spacing/radius values and component-state rules agree between prose, specimens and copyable tokens.
5. Keyboard traversal, focus visibility, skip link, theme control, copy feedback and reduced motion work.
6. Reviewer findings have explicit resolved/deferred status, with reproducible checks and honest limits on visual/accessibility verification.
