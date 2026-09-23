# Round 1 — brand strategy and evidence review

Reviewer: independent brand strategist. Evidence checked: **23 September 2026**. Scope: original local design bible, public Persistent pages, public Unfazed homepage and SVG. This is a design and editorial review, not a technical certification of product claims. Implementation was not edited. The only supplied implementation asset is the existing public Unfazed mark, by explicit request of the coordinating agent.

## Executive judgment

The original bible captures useful visual DNA but largely turns whatever happened to exist in production into permanent brand law. A stronger system distinguishes **observed legacy implementation**, **adopted family standards**, **product exceptions**, and **proposed additions**. The portfolio should feel related through quality, typography where appropriate, spacing discipline, accessible interaction, and a discreet Persistent Labs endorsement. It should not make every product look like the same dark gold landing page.

Keep Persistent Labs' ribbon, charcoal, warm gold, and Red Hat family. Preserve FireFlow's orange and flame/pixel heritage, Lanni's coral, MemoryTree's sky, and Unfazed's already coherent light, lowercase, utilitarian identity. Treat PrivateInference's bold pi symbol as an explicit user requirement. Its other identity details are proposed. The fifth requested product remains unnamed by the user: MemoryTree may be developed as a clearly provisional fifth chapter because it is already in the original source; it cannot silently become a confirmed scope decision.

## Source register and observed facts

1. **Original local bible** — `/Users/max.rabinovitch/Desktop/persistent-labs-design-bible.html`, v1.1 draft dated 23 September 2026. Supplies the ribbon SVG, Red Hat typography, named product palette, FireFlow/flame wordmark history, and detailed observations of earlier sources. Its account of `FF_intro.pdf` and private stage tokens has not been independently repeated in this review. Preserve that provenance; do not restate inherited observations as new audit findings.
2. **[Persistent homepage](https://persistentai.org/)** — accessible non-www address; reviewed 23 September 2026. Primarily markets FireFlow to institutional finance, emphasizing durable, governed execution, visual building, and deployment within an institution's environment. Legacy company naming persists. Its audience and sales journey should inform FireFlow, not dictate every sibling product's personality. Broad assurances and comparative business estimates on the page are marketing claims requiring separate substantiation before reuse.
3. **[Lanni product page](https://persistentai.org/lanni)** — reviewed 23 September 2026. Describes an agent application built on FireFlow, Flame Chorus, and MemoryTree; mixes everyday and professional use cases with institutional infrastructure language. A coming-soon label coexists with launch language. It lists 146+ nodes, describes Flame Chorus as moving toward production, and presents memory capability broadly. These are source observations, not independently verified availability statements.
4. **[Persistent docs](https://docs.persistentai.org/)** — reviewed 23 September 2026. Identifies FireFlow as the builder/execution engine, Flame Chorus as the conversation layer, and Memory Tree as built-in memory. Lists 320+ building blocks, unlike the Lanni page. Describes graph/retrieval capabilities as shipping soon. Explicitly labels the software source-available under BUSL-1.1. Preserve that wording rather than treating it as interchangeable with open source. All runtime guarantees should retain scope and source.
5. **[Unfazed](https://unfazed.dev/)** — direct public HTTPS source fetched 23 September 2026; the www hostname failed DNS. Its promise is agent-led deployment: static sites, services, and persistent Linux workspaces accessible through SSH. The entry flow offers an MCP endpoint and a deployment prompt. Public copy also claims stable URLs, encrypted secrets, service recovery, and persistent workspaces; these claims were read, not operationally tested. Existing voice is lowercase, terse, and composed. The family name/ownership comes from the user's brief, not independent legal verification.
6. **[Unfazed logo SVG](https://unfazed.dev/icon.svg)** — fetched 23 September 2026 and retained at `assets/unfazed.svg`. Existing unimpressed face, full 1024-square viewBox; foreground `#231F20` and OS-dark white variant. No new logo should replace it without an explicit redesign decision.
7. **PrivateInference / PI** — user brief only. Upcoming brand, full name PrivateInference, short name PI, logo is a bold mathematical pi. Audience, architecture, available functionality, launch date, and privacy guarantees remain unspecified.

## Priority findings and required corrections

| ID | Priority | Finding | Recommended correction / review condition |
|---|---|---|---|
| STR-01 | High | Observation and standard are blended. The opening asserts one reconciled rule set despite unresolved decisions. | Label inherited facts, adopted decisions, and proposals. Publish an evidence/date ledger. |
| STR-02 | High | Portfolio coverage is incomplete: Unfazed and PI are absent; the request says five but supplies four names. | Four named chapters plus clearly provisional MemoryTree. Keep Flame Chorus visible as a stack component. |
| STR-03 | High | Generic gold-only / dark-only / Red Hat-only rules would erase Unfazed's existing brand. | Document product exceptions explicitly, including Unfazed white canvas, lowercase, system type and blue interaction accent. |
| STR-04 | High | Original prose encourages naming a failure mode followed by a guarantee; specimens repeat absolute security/execution claims. | Lead with a specific mechanism and its documented scope. Do not generalize sandboxing, privacy, or deterministic orchestration into universal safety or correctness. |
| STR-05 | High | Current node counts disagree (146+ / approximately 300 inherited from PDF / 320+ docs). | Remove numeric proof from reusable specimens until an owner verifies scope/version/date. Keep conflict in the decision ledger. |
| STR-06 | High | Original memory description flattens delivery stages. | Separate current documented layers from graph/retrieval described as forthcoming. Never show all features as shipped by default. |
| STR-07 | High | “Open-source” and broad legal assurances risk unsupported claims. | Use the precise source-available wording; do not infer certification, compliance, or licensing rights from design context. |
| STR-08 | Medium | Product accents are prohibited page-wide while individual products now need their own identities. | Keep neutral grounds; permit product accent in CTA, selection, small surfaces, diagrams. Avoid saturating every large panel. |
| STR-09 | Medium | Pure vw layout is promoted as canonical despite severe scale changes and arbitrary responsive advice. | Promote bounded responsive containers and type/space tokens; keep the 1920 reference as legacy measurement context only. |
| STR-10 | Medium | Body at negative tracking and 1.3 leading is treated as universal; many visible labels fall below the bible's stated minimum. | Use readable body 16–18px / 1.5–1.65 with neutral tracking; keep display tracking local to large headings. Define UI metadata exception and contrast. |
| STR-11 | Medium | Parent and product naming repeatedly disagree: FlameChorus/Flame Chorus; Memory Tree/MemoryTree; FireFlow Engine/FireFlow. | Canonical editorial names: FireFlow, Flame Chorus, MemoryTree, Lanni, Unfazed.dev, PrivateInference. Preserve lowercase unfazed as its display wordmark and lowercase fireflow in existing logo artwork. |
| STR-12 | Medium | Original title-case button exception contradicts sentence-case recommendation. | Adopt sentence case for family copy; preserve Unfazed's deliberate lowercase product voice. |
| STR-13 | Medium | Original fixed foreground/opacity values are promoted without enough context for dark and light surfaces. | State tested foreground/background pairs, not standalone “accessible color.” Keep neutral text on tinted status surfaces. |
| STR-14 | Medium | “Marketing web dark only” unnecessarily freezes implementation rather than purpose. | Dark parent/FireFlow expression, expressive Lanni alternative, and light Unfazed are sanctioned product choices. Let docs and dense work surfaces follow task needs. |
| STR-15 | Low | The parent ribbon opacity is described as an immutable rule rather than tested small-size behavior. | Preserve ribbon form; use a solid mark when reduced opacity loses detail at favicon scale. Record legacy 55% specimen separately. |

## Proposed portfolio architecture

Use **an endorsed family**: Persistent Labs is the maker and trust signature; product names lead their own experiences. At the entry or footer, use “By Persistent Labs” in secondary type. On the corporate portfolio, use equal card structures and consistent category labels. Inside products, preserve appropriate typography, density and voice.

- **FireFlow — orchestration.** Infrastructure / builder experience; serious and precise.
- **Unfazed.dev — deployment.** Agent-led shipping and persistent execution environments; clear and unceremonious.
- **Lanni — agent experience.** The human-facing application; task progress, outcomes and control.
- **PrivateInference — proposed private inference category.** Upcoming, scope unconfirmed; visual identity can be completed independently of product claims.
- **MemoryTree — memory, provisional fifth chapter.** Existing source product / layer; confirmation of requested fifth slot pending.
- **Flame Chorus — conversation layer.** Continue to name it in stack relationships and components. Do not remove or reclassify it just to make the count fit.

Do not draw runtime dependency arrows between Unfazed, PI, and the FireFlow stack without product evidence. An endorsed family is an ownership/design relationship, not an assertion of implementation architecture.

## Product identity direction

### FireFlow

**Preserve:** flame/pixel heritage, lowercase italic original logo when original artwork is available, canonical FireFlow in prose, orange `#F7931A`, ink `#1C1E21`, parent Red Hat typography. An invented simplified icon must be labeled as a proposed symbol, not the recovered production logo.

**Propose:** use orange for primary execution actions and selected path emphasis; keep normal text off bright orange unless the exact pair is tested. Add a deep burnt-orange light-mode text token and a pale warm surface. Use Red Hat Display 700 for marketing, Red Hat Text 400/500 for dense UI, Mono for runs and identifiers. Dense cards 12px radius, panels 20px, controls 8px; 16/24/32px spacing; flow connectors orthogonal or gently routed, with labels and arrow direction.

**Voice and interaction:** evidence first, architectural scope second, outcome third. Suggested copy: “Build the flow. Inspect the run.” Use explicit states: queued, running, awaiting approval, resumed, completed, failed. Show actor, timestamp, input/output and replay entry point. Separate orange brand emphasis from warning semantics. Avoid simulated money movement or invented performance metrics in specimens.

### Unfazed.dev

**Observed design specifications:** white `#FFFFFF`, foreground `#141414`, secondary `#666666`, hero copy `#3F3F3F`, divider `#ECECEC`, strong border `#D8D8D8`. Existing blue interaction accent `oklch(0.55 0.16 256)`, converted to sRGB approximately `#2570CC`. Logo ink `#231F20`. System sans stack (`-apple-system`, BlinkMacSystemFont, Helvetica Neue, Helvetica, Arial) and system mono. Existing landing shell max 680px with 24px side padding. Hero 22px, regular, 1.35; body16px / 1.6; section gap48px; row gap12px. Inputs/buttons6px radius. Wordmark18px, mark23px, gap9px.

**Preserve:** face mark, lowercase wordmark “unfazed”, lowercase product voice, light canvas, direct prompt/MCP handoff. Use Unfazed.dev in the portfolio's editorial naming, while preserving unfazed in its own wordmark. There is no need for lime or emerald rebranding.

**Propose:** calm deployment receipt cards with resource type, endpoint, status, last activity and next action. Increase tiny controls' hit areas without making typography oversized. Keep blue for links/actions, green only for successful status, red only for errors. A narrow landing layout may expand into a practical two-column workspace for logs/settings. Failed operations should retain context and offer a specific recovery action. Suggested product-native copy: “your project is live.” / “deployment failed. view the log.” These are proposed microcopy, not actual verified state.

**Asset note:** the original external SVG responds to OS dark mode; it can disappear on a light specimen in a dark OS. For explicit theme specimens, inline the retained geometry with the prescribed current foreground color. Do not alter the face geometry.

### Lanni

**Preserve:** coral `#FF6741`, dark app lineage, human-facing role, and task/result emphasis. Do not transplant the entire bank-sales pitch into every consumer interaction.

**Propose:** Red Hat Display 700 for approachable headlines; Text400 for conversation; 16px minimum reading copy / 1.6. Rounded conversation surfaces24px, outcome cards16px, controls12px. Coral fills require dark foreground; on pale surfaces use a separately tested deeper coral for links. Keep large surfaces neutral. A simple bespoke L-shaped gesture can be proposed as a mark, but its status must be clear.

**Voice and interaction:** warm, concise, competent, never presumptuous. Organize a specimen as request → plan → progress → result. Explicitly separate “Ready to confirm” from “Confirmed”; show the user's next step and reversible edits. Put supporting evidence or activity under disclosure rather than spilling runtime details into every chat turn. Suggested copy: “Here’s the plan. Review it before I book.” Do not claim a transaction completed merely because a card looks successful.

### PrivateInference / PI

**Required by user:** bold mathematical pi symbol **π**. **Proposed identity:** a custom vector silhouette with heavy crossbar, clearly separated legs and broad optical footprint; no dependence on an OS font's pi glyph. Keep π as the mark, PI as shorthand in prose after first introduction, and PrivateInference as the full wordmark. Supply mono dark/light and a compact icon. The logo needs clear space of at least one stem width and small-size inspection at24px; no lock/shield substitution.

**Propose:** mineral violet `#C4B5FD` on ink, deep violet `#6D28D9` on pale lavender `#F3EFFF`, with neutral operational surfaces. Preserve Red Hat family; use balanced, measured headings and very clear numerals. Radius8px for controls,16px for panels; grid geometry and quiet contained regions rather than smoke, glass, or neon security theater.

**Voice and interaction:** precise, composed, explicit about scope. Header can say “PrivateInference” with an “Upcoming” badge and “A Persistent Labs product in development.” Any substantive tagline should be labeled proposed positioning. A conceptual UI may show configuration labels such as endpoint, model, and deployment, but should not imply a real deployed privacy guarantee. Do not assert no logging, no training, encryption model, on-prem availability, data residency, zero retention, certification, or performance without evidence.

### MemoryTree — provisional fifth chapter

**Observed anchor:** name and role are already in the bible; sky `#8ECFFB`. **Proposed complete extension:** layered branch/record symbol, deep blue companion for light-mode links, Red Hat family with Mono for revision IDs. Cards12px, controls8px; fixed record rows with comfortable 12–16px vertical rhythm. Use a timeline/tree motif with labeled records, human-readable dates, and content previews. Never rely on blue alone to indicate current selection.

**Voice and interaction:** calm continuity: “Keep context. Trace changes.” Separate history, files, structured records, and upcoming graph/retrieval. A status column must reveal availability rather than blending planned capabilities with shipped ones. The visual spec may be fully developed while the fifth-product assignment remains explicitly provisional.

## Second-round acceptance checklist

1. Every product chapter has role, verified/proposed status, logo handling, palette with contrast-safe usage, type, shape, spacing, voice, UI specimen, endorsement and source.
2. Unfazed's face geometry and blue/light/lowercase identity survive family integration.
3. PI has the requested bold pi, upcoming label, and no unsupported privacy claims.
4. MemoryTree's chapter cannot be mistaken for user confirmation of the fifth brand.
5. Existing Flame Chorus stays represented in architecture and source naming.
6. Statements inherited from the PDF review remain marked inherited rather than newly verified.
7. Reusable examples contain no unapproved metrics, licensing overstatements, availability claims, or universal guarantees.
8. Brand exceptions are deliberate and legible; product sections are recognizably distinct without losing shared craft standards.
