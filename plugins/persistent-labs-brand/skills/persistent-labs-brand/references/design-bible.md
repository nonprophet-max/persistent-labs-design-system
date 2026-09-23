# Persistent Labs full design bible

Edition 2.3 · 23 September 2026.

Foundations / 01

## A system with staying power.

One parent. Distinct products. A shared standard of care. This edition turns the original visual inventory into a practical system for making decisions.

01

**Working edition 2.3 · 23 September 2026.** Core rules are reconciled recommendations. Existing identities, proposed extensions and unconfirmed product decisions are labelled separately. The original bible is preserved in the reference archive.

01

### Keep the recognizable parts.

Graphite, warm gold, Red Hat and the infinity ribbon remain the Persistent Labs signature. Give established products room to keep their own identity.

02

### Show how it works.

Execution diagrams, readable commands and useful interface states do the explaining. Every product needs a visual grammar beyond a new accent color.

03

### Make reading effortless.

Use stable foreground colors, generous leading and a bounded reading width. Specimens must remain readable in either document theme.

04

### Make the next action clear.

One primary action per decision. Give feedback, preserve context and state what has changed. Rounded geometry supports this clarity.

05

### Keep evidence beside claims.

Separate a product promise from a verified capability. Date proof points and name their scope. Draft interfaces never masquerade as a live product.

Foundations / 02

## Built by Persistent Labs.

Use an endorsed portfolio: the product leads with its own promise; “by Persistent Labs” provides a consistent maker’s signature.

02

FireFlowEstablished product · extended identityOrchestration, persistent memory & chat UX↗
Unfazed.devLive identity · preserved & documentedDeployment for agents↗
LanniExisting brand · extended identityAn agent for getting things done↗
PrivateInferenceUpcoming · proposed identity & positioningPI · upcoming brand↗05GalacticaLive product · proposed family adaptationPrivacy technology across AI & blockchain↗

**FireFlow is one product.** Its three core parts are the FireFlow orchestration engine, MemoryTree for persistent memory and FlameChorus, the chat UX engine. They sit within the FireFlow chapter and share its product identity.

### Five products. A clear hierarchy.

Persistent Labs creates FireFlow, Unfazed.dev, Lanni, PrivateInference and Galactica. Lanni is built on FireFlow. Galactica is a live privacy technology firm across AI and blockchain; PrivateInference is an upcoming brand. Their listing together does not imply a shared technical architecture.

### Core parts, one FireFlow identity.

MemoryTree and FlameChorus identify parts of FireFlow. Their names and accent colors help explain the system inside the product; they do not get separate portfolio cards, product chapters or maker endorsements.

### The endorsement has one job.

Use “by Persistent Labs” in a quiet footer or beneath a product lockup, with at least one line of clear space. It should be secondary to the product name. Do not combine multiple marks inside one crowded capsule.

Foundations / 03

## A signature, not a watermark.

The original four-stroke infinity ribbon stays intact. Raise its contrast for identification and reserve fading for decorative uses.

03

Persistent LabsPrimary / white on graphite

Persistent LabsReversed / graphite on white

| Specification | Rule |
| --- | --- |
| Lockup | Horizontal infinity ribbon + Persistent Labs, two words. Red Hat Display 500. Preserve the supplied ribbon paths. |
| Clear space | One ribbon height on each side. Gap between ribbon and wordmark: half the ribbon height. |
| Minimum size | Ribbon: 40px wide in the parent lockup; complete lockup: 180px wide. Use 24px minimum for separate product symbols. |
| Color | Solid white on ink, solid ink on white. Full opacity for identification. Faded marks are decorative only and have no independent meaning. |
| Narrow screens | Keep a readable horizontal lockup. Move the product endorsement to its own line; do not squeeze a co-brand row. |
| Avoid | Distortion, gradient fills, clipped ribbons, reconstructed official product marks and substituting a guessed font glyph for the PI logo. |

Downloadable vector masters are in assets/persistent-labs.svg and the individual product chapters. New product symbols are labelled concepts.

Foundations / 04

## Warmth, with discipline.

Graphite does the grounding. Gold directs attention. Product accents carry identity; semantic colors carry meaning.

04

**Graphite**#1C1E21Parent ground and primary light-surface text.

**Warm gold**#FBD78EParent actions and text on dark.

**Paper**#F6F6F6Reading surfaces and light collateral.

**Gold ink**#76580DAccessible accent text on white and cream.

### Foregrounds belong to surfaces.

### Light surfaces

Primary #1C1E21 · secondary #50545B · muted #62666D. Use the deep product accent for links. Gold fills carry dark labels. A light specimen keeps these colors even when the surrounding document is dark.

### Dark surfaces

Primary #FFFFFF · secondary #CBCDD0 · muted #A8ADB4. Use the light product accent for emphasis. A dark specimen owns its text colors; it never inherits dark ink from the surrounding page.

| Pair | Foreground | Background | Ratio |
| --- | --- | --- | --- |
| Primary text | #FFFFFF | #1C1E21 | 16.71:1 |
| Dark secondary | #CBCDD0 | #25272A | 9.40:1 |
| Dark muted | #A8ADB4 | #25272A | 6.63:1 |
| Light muted | #62666D | #F6F6F6 | 5.34:1 |
| Gold button | #1C1E21 | #FBD78E | 12.10:1 |
| Gold text on cream | #76580D | #FFF5E6 | 6.13:1 |
| Success on dark | #83D995 | #1C1E21 | 9.80:1 |
| FireFlow light text | #8C4900 | #FFFFFF | 6.84:1 |
| FireFlow dark accent | #F7931A | #1C1E21 | 7.27:1 |
| Unfazed.dev light text | #2570CC | #FFFFFF | 4.92:1 |
| Unfazed.dev dark accent | #8AB8F6 | #1C1E21 | 8.17:1 |
| Lanni light text | #A6381C | #FFFFFF | 6.55:1 |
| Lanni dark accent | #FF6741 | #1C1E21 | 5.78:1 |
| PrivateInference light text | #6544A2 | #FFFFFF | 7.24:1 |
| PrivateInference dark accent | #C4B5FD | #1C1E21 | 9.05:1 |
| Galactica light text | #97502A | #FFFFFF | 6.01:1 |
| Galactica dark accent | #F4A77A | #1C1E21 | 8.48:1 |

Ratios are calculated from the source token values with the WCAG sRGB luminance formula. All listed text pairs meet 4.5:1. This is a check of these pairs, not certification of every future interface. Borders that identify controls must meet 3:1; decorative rules may be quieter.

### Semantic colors stay semantic.

| State | On light | On dark | Required label |
| --- | --- | --- | --- |
| Success | #246938 | #83D995 | Complete / saved |
| Warning | #785300 | #F1C14E | Needs review |
| Error | #AE3024 | #FF9A8F | Failed / action required |
| Information | #215F8B | #8ECFFB | Information / source |

**Reconciled from v1.1:** deepen light gold from #8B6914 to #76580D; replace opacity-based muted copy with solid tokens; keep #FFCB63 as parent hover and #EABD64 as pressed. Historical gradients remain references, never backgrounds behind untested small text.

Foundations / 05

## Three cuts. One clear hierarchy.

Red Hat Display makes the statement. Red Hat Text handles reading and controls. Red Hat Mono makes technical detail legible. Unfazed retains its established system-font identity.

05

Red Hat Display
700 / −3%

Built to
keep going.

Red Hat Text
400 / 1.6

A good system helps people understand what is happening, what matters and what comes next.

Red Hat Mono
400 / tabular

workflow / review-required
run_example_001 · illustrative data

| Role | CSS size | Weight / leading | Use |
| --- | --- | --- | --- |
| Display XL | clamp(2.75rem, 1.5rem + 4vw, 8rem) | 700 / 1.04 | Campaign headline |
| Display | clamp(2.5rem, 1.5rem + 3vw, 5.5rem) | 700 / 1.04 | Product hero |
| Heading 1 | clamp(2rem, 1.5rem + 2vw, 4rem) | 700 / 1.15 | Major section |
| Heading 2 | clamp(1.75rem, 1.25rem + 1.5vw, 3rem) | 700 / 1.15 | Feature section |
| Heading 3 | clamp(1.5rem, 1.25rem + 1vw, 2rem) | 700 / 1.15 | Subsection |
| Heading 4 | 1.25rem | 600 / 1.15 | Card title |
| Heading 5 | 1.125rem | 600 / 1.15 | Small heading |
| Lead | clamp(1.125rem, 1rem + .5vw, 1.5rem) | 400 / 1.55 | Opening context |
| Body large | 1.125rem | 400 / 1.6 | Short introduction |
| Body | 1rem | 400 / 1.6 | Reading / chat |
| Body small | .875rem | 400 / 1.6 | Supporting copy |
| UI | 1rem | 500 / 1.4 | Controls |
| Tag | .875rem | 500 / 1.4 | Compact labels |
| Eyebrow | .75rem | 500 / 1.5 | Short labels only |

Sizes use rem floors and bounded fluid growth. Body tracking is 0; headings use −.03em. Keep prose within 55–70 characters and left aligned. Main body starts at 16px; supporting copy at 14px; short metadata may use 11–12px with strong contrast. Size token names do not determine HTML heading levels.

The font files and open license are bundled for offline use. Arial and system mono remain intentional fallbacks if fonts cannot load. Unfazed uses system sans and mono by design.

Foundations / 06

## Let the content set the limits.

Build from a readable column, then add space. Replace artboard ratios and mobile multipliers with bounded containers and explicit layout changes.

06

| Surface | Wide layout | Narrow layout |
| --- | --- | --- |
| Marketing | Maximum 1520px container; 64px outer gutter; two-column hero when both columns remain useful. | 20px gutters; single column; headline before illustration. |
| Documentation | 220–244px navigation; readable content up to 66ch; specimens can use the full content column. | Collapsible contents below 900px; keep visible menu control and keyboard exit. |
| Product UI | Navigation + main workspace + optional detail panel. Let the task determine column widths. | One primary task panel. Move details into explicit disclosure; preserve labels. |
| Unfazed | 680px reading shell, sparse rows, system typography. | 20px gutters; commands wrap or scroll locally. |
| Collateral | A4 / Letter for documents; 16:9 for presentations. Design for the actual output size. | Do not shrink a dense desktop table until labels become illegible. |

### Three working thresholds

Below 600px: stack paired cards and product diagrams. Below 900px: collapse the navigation rail. Below 1180px: simplify dense multi-column compositions. Also test 320, 390, 768, 1024 and 1440px; breakpoints are responses to content, not device brands.

### Overflow must be intentional

Allow a labelled data table or code sample to scroll within its own region. Text, headings, logos and the page itself must fit. Never hide a layout error with overflow:hidden on the body.

Foundations / 07

## Space communicates structure.

Use a 4px base with an 8px rhythm. A few deliberate increments are more useful than dozens of extracted one-off values.

07

4px

Icon adjustment

8px

Label → control

12px

Compact inline gap

16px

Related content

20px

Mobile gutter

24px

Card padding / group gap

32px

Independent groups

40px

Large card padding

48px

Section heading → body

64px

Mobile sections

80px

Desktop sections

96px

Large section pause

120px

Maximum section pause

| Relationship | Small screens | Wide screens |
| --- | --- | --- |
| Headline → supporting copy | 16px | 20–24px |
| Supporting copy → action | 24px | 32px |
| Card inset | 24px | 28–40px |
| Card grid gap | 16–24px | 24–32px |
| Independent sections | 64px | 80–120px |
| Control hit area | At least 44 × 44px | At least 44 × 44px |

Use shared spacing tokens for layout. Optical exceptions are limited to mark alignment and documented product identities, such as Unfazed’s existing 6px corners. Do not multiply mobile dimensions by a universal factor.

Foundations / 08

## Soft edges. Precise relationships.

The parent is generous and rounded. Product interfaces tune that softness to their job. Shape follows hierarchy and is never a substitute for spacing.

08

input / 8px

tile / 12px

card / 24px

feature / 40px

hero / 64px

pill / 999px

### One rule for nested corners.

Outer radius 40px. Ring 8px. Inner radius 32px. The inner and outer curves share a center. Use max(0, outer radius − inset) and render the value you specify.

| Material | Specification | Use |
| --- | --- | --- |
| Control outline | 1px; #70757D on light or #828891 on dark | Inputs, secondary actions and essential boundaries. |
| Decorative divider | 1px quiet neutral; not relied on to identify a control | Reading rhythm and non-interactive grouping. |
| Gold bloom | Optional, one per hero; never behind body copy | Parent campaign artwork only. Disabled in dense product UI. |
| Glass | White at 90%; 20px blur; opaque fallback | Optional parent marketing header. Ensure contrast over the worst background. |
| Aurora | Retain warm gold, copper, teal and sage as a static artwork palette | Feature imagery or a decorative frame. No continuous background animation by default. |

Foundations / 09

## Every state is part of the design.

Default, hover, focus, pressed, disabled, loading and error states belong in the same specification. These examples are local demonstrations.

09

Button family / interactive local specimen

Primary actionSecondary actionUnavailable

✓ Complete! Needs review× Failed

Choose an action to see its feedback.

| State | Specification |
| --- | --- |
| Default | 48px control height; minimum hit area 44px; text label that names the action. |
| Hover | Parent fill #FFCB63; product hover token; same label and geometry. |
| Focus | 3px visible ring, 4px offset, contrast checked against the local surface. Never suppress keyboard focus. |
| Pressed | Parent fill #EABD64; product pressed token. Do not move surrounding layout. |
| Disabled | Use the native disabled attribute; dim the fill but preserve a readable label. Explain prerequisites nearby. |
| Loading | Keep the control width stable, set aria-busy=true and show a textual progress label. Prevent duplicate submission. |
| Error | Explain the problem and recovery step beside the affected field. Announce the result; do not rely on red alone. |

### Fields explain what they need.

Run name

A descriptive name helps people recognize this workflow.

Validate example

One primary action per decision. Tooltips supplement labels; they never carry essential instructions. Keep controls keyboard reachable and return focus to the initiating control when dismissing overlays.

Foundations / 10

## Make movement explain change.

The default is calm. Motion earns its place by showing a transition, a relationship or progress that is really occurring.

10

| Token | Duration | Purpose |
| --- | --- | --- |
| Fast | 150ms | Color feedback and compact toggles |
| UI | 200ms | Card state changes and action feedback |
| Panel | 300ms | Disclosure and panel entrance |
| Reduced motion | 0ms; preserve textual feedback | Honor prefers-reduced-motion in CSS and scripted transitions |

### Build an image language from the product.

### Primary imagery

Use real product views, clear diagrams and meaningful interface details. Label illustrative data. Keep screenshots legible at their rendered size and remove secrets from captured content.

### Secondary material

The original prismatic glass can remain a parent campaign motif. Keep it away from small text and operational interfaces. FireFlow uses execution diagrams, memory provenance and conversation states; Unfazed uses commands; Lanni uses actions; PI uses explicit boundaries.

Icons use a consistent 24px grid and 2px strokes unless they are a supplied filled brand mark. Avoid emoji as interface icons. Do not animate the Unfazed face or the PI symbol as decorative loading states.

Foundations / 11

## Confidence comes from clarity.

Name the action, explain the mechanism and give the reader a useful next step. Each product has its own cadence inside that standard.

11

| Context | Use | Avoid |
| --- | --- | --- |
| Claims | A dated, scoped capability linked to a source | Regulatory-grade, unbreakable, zero risk, or unsupported performance numbers |
| Actions | Sentence case: “Inspect the workflow” | Title Case Everywhere or a label that changes on hover |
| Technical copy | Name the mechanism when it explains the benefit | Acronyms without context or unqualified “exactly-once” promises |
| Status | “Awaiting review”, “Complete”, “Failed” | Color dots that force people to infer meaning |
| Product name | Persistent Labs; FireFlow; Unfazed.dev; Lanni; PrivateInference (PI); Galactica | PersistentAI as the new company name or Fireflow in body text |
| FireFlow core parts | FireFlow orchestration engine; MemoryTree (persistent memory); FlameChorus (chat UX engine) | Listing MemoryTree or FlameChorus as standalone products; Flame Chorus as two words |

### Apply the system by surface.

### Marketing & product UI

Parent marketing leads with graphite and gold. Product marketing leads with that product’s identity. Product UI prioritizes task clarity and accessible states. Preserve Unfazed’s white, square-edged simplicity.

### Docs & collateral

Use a light reading surface by default, optional dark view and product accents for orientation. Print uses real paper sizes and static graphics. Archive earlier measurements so history cannot be mistaken for a current rule.

Product identities / 12

## FireFlow

Orchestration, persistent memory & chat UX

12

Established product · extended identity

### Make every step count.

One product with three core parts: the FireFlow orchestration engine, MemoryTree for persistent memory and FlameChorus for chat UX.

by Persistent Labs

The owner defines FireFlow as one product comprising the FireFlow orchestration engine, MemoryTree and FlameChorus. This hierarchy supersedes earlier stack and portfolio descriptions. The proposed node mark and visual extensions remain concepts. [FireFlow documentation ↗](https://docs.persistentai.org/)

### Three core parts. One product.

The orchestration engine, persistent memory and chat UX engine together make up FireFlow.

Core part 01

#### FireFlow orchestration engine

Orchestration & execution

View specifications ↓
Core part 02

#### MemoryTree

Persistent memory

View specifications ↓Core part 03

#### FlameChorus

Chat UX engine

View specifications ↓

One FireFlow product identity and one “by Persistent Labs” endorsement. Component names clarify each part of the system.

**Signature on dark**#F7931AForeground on graphite; ink label on fill.

**Signature on light**#8C4900Text on white.

**Product tint**#FFF0DEDecorative light surface; ink text.

**Shared graphite**#1C1E21Neutral foundation.

### Audience & position

For technical teams building agent experiences. Present FireFlow as one product: its orchestration engine handles workflows and execution, MemoryTree provides persistent memory, and FlameChorus provides the chat UX engine. Let documented behavior carry the proof.

### Mark & lockup

Set FireFlow in Red Hat Display 700. Preserve the italic fireflow spelling only inside an approved original logotype. The proposed three-step F mark is a schematic motif. Minimum mark: 24px; clear space: one node width on all sides.

### Color & hierarchy

Flame orange identifies FireFlow and its primary actions. Sky blue may identify MemoryTree and warm gold may identify FlameChorus within FireFlow diagrams and component labels. These are subordinate component accents, not separate product identities. Keep semantic state colors separate.

### Typography

Red Hat Display 700 for headlines; Red Hat Text 400/500 for UI; Red Hat Mono 400/500 for run identifiers and event details. Keep log text at 14px with 1.6 leading and tabular figures.

### Geometry & layout

24px marketing cards, 8px workflow nodes, 2px connectors and 12px ports. Align flows left to right on wide screens; stack with explicit arrows on mobile. Keep 24px between independent steps.

### Motion & imagery

Illustrate actual state transitions with a 200ms opacity change. Keep completed steps visible. Use real execution traces and diagrams; label sample runs as illustrative. No perpetual ‘running’ animation in static marketing.

### Voice & example

Direct, specific, operational. Proposed headline: ‘Make every step count.’ CTA: ‘Inspect the workflow’. Avoid ‘exactly once’ without stating the transaction boundary and applicable guarantees.

### Component contract

Use one FireFlow product shell and one primary action for each task. Within it, distinguish orchestration state, memory provenance and conversation state through labels and structure. Every core part inherits the shared accessibility and interaction rules.

### The system in use.

FireFlowIllustrative interface / not live data

FireFlow orchestration engine

**01 / Receive**Input recorded→

**02 / Review**Awaiting a decision→

**03 / Execute**Not started

MemoryTree / persistent memory

**Project preferences**Source: example project brief

**Example workspace**Updated 23 Sep 2026 · illustrative

FlameChorus / chat UX engine

Review the proposed action before execution.

Conversation state: awaiting a decision

Inspect the workflow

Local specimen. No product action will run.

### Do

Show inputs, transitions and outcomes together.

### Avoid

Flame decoration, unexplained performance claims and orange success indicators.

Download concept mark ↓

FireFlow / Core part 01

### FireFlow orchestration engine

The workflow and execution part of FireFlow.

#### Role & hierarchy

Name the engine explicitly when describing workflow behavior. FireFlow on its own names the complete product, including memory and chat UX.

#### Visual specification

Inherit FireFlow orange and Red Hat typography. Use 8px workflow nodes, 2px connectors and 12px ports. Keep node labels at 14px with 1.6 leading and a 24px step gap.

#### Interaction contract

Show named steps, textual execution states, timestamps and details. Errors identify the affected step and available recovery. Never use orange alone to indicate success.

FireFlow / Core part 02

### MemoryTree

The persistent-memory part of FireFlow.

#### Role & hierarchy

MemoryTree is a core part of FireFlow. Refer to it as “MemoryTree, FireFlow’s persistent memory” when context is needed. It does not receive a peer-level product listing or an independent Persistent Labs endorsement.

#### Mark & color

Retain the proposed three-node symbol as an optional component icon. Minimum icon: 24px; clear space: one node diameter. Sky #8ECFFB on dark and deep blue #215F8B on white identify memory inside FireFlow; primary product actions remain FireFlow orange.

#### Typography & geometry

Inherit Red Hat Display, Text and Mono from FireFlow. Use 16px body / 1.6, 16px collection cards, 8px source rows and 2px tree connectors. Tree indentation is 24px on desktop and 16px on mobile.

#### Motion & voice

Use 200ms disclosure that preserves the parent position. Be organized, contextual and traceable. Use provenance and source references; avoid limitless-memory or sentience claims.

#### Interaction contract

A memory entry shows title, source, scope and update time. Make missing-source and empty states explicit. Do not infer retention, deletion behavior or availability of graph/retrieval features beyond documented capabilities.

Download proposed MemoryTree component icon ↓

FireFlow / Core part 03

### FlameChorus

The chat user-experience part of FireFlow.

#### Role & hierarchy

Use FlameChorus as one word. Describe it as “FlameChorus, FireFlow’s chat UX engine.” It is a core part of the FireFlow product, not a separate product identity.

#### Color & typography

Warm gold #FBD78E on graphite and gold ink #76580D on white may label conversation diagrams. Inherit Red Hat Display and Text; dialogue uses 16px / 1.6. Primary actions inherit FireFlow orange.

#### Geometry & motion

Use 16px conversation bubbles and 24px enclosing panels, with a 16px gap between speakers. Introduce new content with a restrained 200ms transition; honor reduced motion.

#### Interaction contract

Distinguish user messages, agent responses and action states with labels and structure. Separate a proposed action from execution and completion. Preserve conversation context and explain the next step without claiming unsupported capabilities.

Product identities / 13

## Unfazed.dev

Deployment for agents

13

Live identity · preserved & documented

### Let your agents ship.

Spare, dry and useful. The existing lowercase wordmark and unimpressed face carry the personality.

by Persistent Labs

The live site uses a compact white layout, system typography, a blue accent and the unimpressed face mark. Its deployment offering includes static sites, services and persistent Linux environments. These are source observations; the endorsed family treatment is new. [Unfazed live site ↗](https://unfazed.dev/)

**Signature on dark**#8AB8F6Foreground on graphite; ink label on fill.

**Signature on light**#2570CCText on white.

**Product tint**#EBF2FCDecorative light surface; ink text.

**Shared graphite**#1C1E21Neutral foundation.

### Audience & position

For developers and the agents they use to deploy software. Keep the path to deployment obvious: show the command, explain the destination, then present the next action.

### Mark & lockup

Preserve the source unimpressed face and lowercase unfazed wordmark. Use ‘Unfazed.dev’ for the portfolio listing and ‘unfazed’ for the wordmark. Minimum face: 24px; clear space: half its height. Endorse separately in the footer.

### Color & hierarchy

White #FFFFFF and ink #141414 are the primary grounds. Preserve the source blue, oklch(0.55 0.16 256), for links and actions. Use a lighter blue on dark surfaces; do not force the parent gold into the product interface.

### Typography

Retain the existing system sans and system mono stacks inside the product. This is an explicit exception to Red Hat. Use 16px body / 1.6 and 14px code / 1.6 as the normalized accessible baseline.

### Geometry & layout

Preserve the narrow 680px reading shell and 6px input/button corners. Use a 20px mobile gutter and allow commands to wrap or scroll in a labelled region. Keep the interface flat with fine, visible rules.

### Motion & imagery

Show commands, outputs and deployment destinations. Use immediate textual feedback with a 150ms color transition. The face is a signature, not a bouncing mascot. Avoid cinematic gradients and prismatic imagery.

### Voice & example

Dry, concise, quietly confident. Existing headline: ‘let your agents ship’. Proposed CTA: ‘Read the deployment guide’. Keep instructions literal and use the source’s restrained lowercase treatment for campaign headlines.

### Component contract

A command panel names the destination and distinguishes example output from live status. Copy controls announce success or failure. Errors include the next useful step; agent actions remain inspectable.

### The system in use.

unfazedIllustrative interface / not live data

$ deploy <your-project>

Choose a destination. Read the guide. Let the agent do the work.

Pseudocode specimen. Use the live documentation for actual commands.

Inspect the example

Local specimen. No product action will run.

### Do

Keep the face, the whitespace and the useful instruction.

### Avoid

Gold pills, glossy cards and a fabricated infrastructure guarantee.

Download source mark ↓

Source blue #2570CC is the sRGB approximation of oklch(0.55 0.16 256); #8AB8F6 is a proposed dark-surface companion. Product text uses #141414 on white; parent endorsement uses the shared family language.

Product identities / 14

## Lanni

An agent for getting things done

14

Existing brand · extended identity

### From intent to action.

A warmer, conversational expression of the same engineered foundation.

by Persistent Labs

The original bible and the Lanni site position Lanni as an agent built on FireFlow. Coral is an observed accent. The action-card patterns and proposed headline below are design recommendations, not a statement that these exact screens are deployed. The source mixes coming-soon and launch language; current availability is not verified. [Lanni product page ↗](https://persistentai.org/lanni)

**Signature on dark**#FF6741Foreground on graphite; ink label on fill.

**Signature on light**#A6381CText on white.

**Product tint**#FFF0EBDecorative light surface; ink text.

**Shared graphite**#1C1E21Neutral foundation.

### Audience & position

For people delegating work to an agent. Explain what Lanni will do, what it needs from the person and what has actually happened. Favor understandable actions over orchestration terminology.

### Mark & lockup

Use Lanni in Red Hat Display 600, title case. Proposed symbol: an L-shaped conversation corner with a separate action dot. Minimum mark: 24px; clear space: one dot diameter. This is a proposed mark, not an extracted official asset.

### Color & hierarchy

Keep coral #FF6741 as the product signature with ink labels on filled actions. Use deep coral for text on white. Reserve gold for Persistent Labs endorsement; do not change a button label or product color on hover.

### Typography

Red Hat Display 600/700 for short headlines; Red Hat Text 400/500 for dialogue and actions. Use 16px chat copy / 1.6. Mono is limited to machine identifiers and technical disclosure.

### Geometry & layout

24px conversation panels, 16px message bubbles, pill action buttons. Keep 16px between speakers and 8px between a label and its supporting copy. A conversation should work in a single mobile column.

### Motion & imagery

An action card enters in 200ms and holds its position as status changes. Favor a simple result preview over abstract glass art. Display progress only when real work is occurring, with a reduced-motion alternative.

### Voice & example

Human, capable, plainspoken. Proposed headline: ‘From intent to action.’ CTA: ‘Review the action’. Prefer ‘Here’s the draft’ over anthropomorphic confidence or claims that completion is guaranteed.

### Component contract

Action cards state the proposed action, affected resource and review step. Distinguish draft, awaiting review, running, complete and failed in text. Make it possible to inspect or cancel before consequential actions.

### The system in use.

LanniIllustrative interface / not live data

Prepare a summary of this week’s decisions.

I can prepare a draft. Review the sources and the summary before sharing it.

**Weekly summary**Draft · ready for review

Review the action

Local specimen. No product action will run.

### Do

Make the next action and its current state unmistakable.

### Avoid

Human-like promises, simulated completion and unexplained tool jargon.

Download concept mark ↓

Product identities / 15

## PrivateInference

PI · upcoming brand

15

Upcoming · proposed identity & positioning

### A clear boundary for AI.

A bold mathematical π. Quiet lavender. A disciplined identity built around clarity and control.

by Persistent Labs

The user supplied the name PrivateInference, abbreviation PI and a bold π logo requirement. All positioning, palette and interface direction in this chapter is proposed. Product architecture, availability and privacy claims have not been provided or verified. User brief · 23 Sep 2026

**Signature on dark**#C4B5FDForeground on graphite; ink label on fill.

**Signature on light**#6544A2Text on white.

**Product tint**#F2EDFFDecorative light surface; ink text.

**Shared graphite**#1C1E21Neutral foundation.

### Audience & position

Proposed audience: teams evaluating control over inference and data handling. Confirm the target buyer and actual deployment model before writing launch copy. ‘A clear boundary for AI’ is a creative direction, not a privacy guarantee.

### Mark & lockup

Use the supplied bold vector π as the primary symbol, never the letters ‘PI’ drawn to imitate it. Full lockup: π + PrivateInference. PI is the verbal abbreviation. Minimum symbol: 24px; clear space: one stem width (16/96 of the mark viewBox).

### Color & hierarchy

Ink, white and proposed lavender #C4B5FD. Use deep violet #6544A2 for light-surface text. Keep the π monochrome in ink, white or the single accent. No gradient fill, shield, padlock or security-seal treatment.

### Typography

Red Hat Display 700 for the full name and headlines; Red Hat Text 400/500 for policy descriptions; Red Hat Mono 400 for endpoint and environment identifiers. The logo is a vector path and never depends on font glyph availability.

### Geometry & layout

12px configuration panels, 8px fields and pill primary actions. Define boundaries with a 1px visible rule. Keep 24px between policy groups. Use simple diagrams that distinguish a verified boundary from a proposed architecture.

### Motion & imagery

Static by default. Use 150ms state changes for explicit selections. Prefer named environments and readable data-flow diagrams. Do not suggest encryption, isolation or locality through decorative shields.

### Voice & example

Measured, exact, transparent about limits. Proposed CTA: ‘Explore the concept’. Avoid ‘zero retention’, ‘air-gapped’, ‘private by default’, ‘never leaves your device’ or compliance claims until architecture and policy substantiate them.

### Component contract

A proposed environment panel separates deployment location, access scope and retention policy. Every unknown reads ‘Not specified’. Show supporting evidence alongside future verified claims. Do not display a green security badge for an unverified property.

### The system in use.

PrivateInferenceIllustrative interface / not live data

**Deployment location**Not specified

**Access scope**Not specified

**Retention policy**Not specified

Explore the concept

Local specimen. No product action will run.

### Do

Use the bold π and name the boundaries that can be verified.

### Avoid

Implied privacy guarantees and security claims without evidence.

Download π vector ↓

Solid white / primary

Solid ink / reversed

Product identities / 16

## Galactica

Privacy technology across AI & blockchain

16

Live product / proposed family treatment

### Privacy. With purpose.

Privacy technology for AI and blockchain. A clear identity built around people, proof and control over disclosure.

AIBlockchain

A statement, selectively disclosed.

Privacy technology / AI & blockchainby Persistent Labs

Galactica is live; its positioning across AI and blockchain follows the owner’s brief. The public site emphasizes identity, zkCertificates and selective disclosure. Its indexed homepage preview suggests monochrome imagery, schematic lines and an orange accent. The palette, typography, layouts and headline below are proposed family adaptations, not measured website specifications. [Galactica live site ↗](https://galactica.com/)

### Carry the core forward.

Keep the name, the privacy and identity themes, and the public preview’s monochrome/orange direction. Keep the owner-directed Galactica.com lockup with its bold orange dot. The site’s selective-disclosure narrative gives the identity a useful explanatory focus.

### Make the family connection.

Use the shared reading grid, Red Hat typography, accessible color pairs and quiet maker endorsement. Give AI and blockchain separate editorial lanes. Galactica is live; PI remains an upcoming brand with its own π identity.

Source boundary: public text and an indexed [homepage preview](https://galactica.com/preview.jpg) informed this direction. Exact site CSS and direct image inspection were unavailable. Copper values and visual specifications are proposed family adaptations. The Galactica.com lockup, including its bold orange dot, follows the owner’s subsequent direction; the diagram is explanatory artwork.

**Signature on dark**#F4A77AForeground on graphite; ink label on fill.

**Signature on light**#97502AText on white.

**Product tint**#FFF1E8Decorative light surface; ink text.

**Shared graphite**#1C1E21Neutral foundation.

### Audience & position

For teams building and evaluating privacy technology across AI and blockchain. Lead with the application and explain the mechanism. Identity and selective disclosure are established public themes; AI positioning follows the owner’s brief. Verify the particular AI offering before describing its capabilities.

### Mark & lockup

Use Galactica.com as the full wordmark, including .com and the bold orange dot. The supplied outlined lockup follows the owner’s direction using Red Hat Display 700; it is a family adaptation, not an extracted website master. Keep the dot #F7931A in full-color lockups on light or dark backgrounds. Minimum width: 160px; clear space: one capital-height. Use the full lockup, never the dot as a standalone logo.

### Color & hierarchy

Carry the public preview’s orange-and-monochrome direction into a restrained proposed palette: copper #F4A77A on graphite, copper ink #97502A on white, and porcelain #FFF1E8. Keep most surfaces neutral. Copper marks a selected path or disclosure boundary; it never means verified, secure or successful. Exact source color values were not retrieved. The wordmark’s bold dot uses orange #F7931A, distinct from the copper interface accent.

### Typography

Use Red Hat Display 600/700 for the proposed family treatment, Red Hat Text 400/500 for reading, and Red Hat Mono for certificate identifiers only. Body: 16px / 1.6; supporting labels: 14px / 1.5. This is a typography adaptation, not a claim about the live site’s fonts. Preserve the supplied owner-directed Galactica.com lockup independently.

### Geometry & layout

Use 24px enclosing panels, 12px disclosure groups, 8px controls and 1px visible boundaries. Keep 24px between information groups and a 20px mobile gutter. Read paired panels left to right on desktop, then top to bottom on mobile: what a service requests, followed by what would be disclosed.

### Motion & imagery

Use restrained monochrome human imagery and precise schematic lines, with copper reserved for the relevant connection. The proof diagram here is a proposed explanatory motif, never a logo. Use 150–200ms changes for selection; avoid rotating orbits, decorative scanning and simulated verification. Honor reduced motion.

### Voice & example

Assured, lucid, evidence-led. Proposed headline: “Privacy. With purpose.” Descriptor: “Privacy technology across AI & blockchain.” CTA: “Review the disclosure”. Explain what is disclosed, to whom and for what purpose. Keep token-market content separate from the core firm narrative.

### Component contract

A disclosure review names the requester, purpose, requested statement, disclosed fields and relevant limits before consent. Separate pending, approved and completed in text. The illustrative screen in this chapter neither creates a proof nor asserts a deployed capability. Explain real processing, retention and revocation behavior from current documentation.

### The system in use.

Illustrative interface / not live data

#### Review a disclosure

Awaiting review · example

01 / The request

- **Requester**: Example service
- **Purpose**: Access to an age-restricted experience
- **Requested statement**: Age is 18 or above

02 / Proposed disclosure

- **Statement result**: Not generated
- **Personal fields**: No name or birth date in this example
- **Consent**: No authorization given

Illustrates the distinction between a statement and its underlying data. Actual disclosures, processing and retention depend on the implementation.

Review the disclosure

Local specimen. No product action will run.

### Do

Keep the complete Galactica.com wordmark and its bold orange dot; make disclosure scope readable before an action.

### Avoid

Turning a copper accent into a security badge, speculative AI claims, or conflating Galactica with the upcoming PI brand.

Download Galactica.com lockup ↓[Visit Galactica ↗](https://galactica.com/)Download family tokens ↓

Owner-directed family lockup: Galactica.com, with a bold orange dot. The downloadable SVG contains outlined lettering and needs no installed font. This is an adapted lockup, not an extracted website master.

Reference / 17

## A living system needs a record.

Use the bible to make decisions, and the review record to understand why they changed. A clean visual treatment must never turn an assumption into a fact.

17

Round 01

### Diagnose the original.

Independent strategy and visual reviews separated established identity from unsupported claims. The visual audit recorded 18 issues, including low contrast, clipped specimens and contradictory tokens. Read the design review · Read the strategy review.

Round 02

### Review the revised system.

Check distinct product roles, accessible color pairs, token consistency and rendered layouts. Record findings against the revision and fix them before the next review. Evidence and results are in the review record.

Round 03

### Verify the corrections.

Recheck prior findings and test navigation, theme selection, copy feedback, responsive layouts and reduced motion. The reusable workflow stores reviewer outputs and artifact hashes; it stops for fixes instead of granting its own approval.

The three review rounds above cover edition 2.0. The owner-confirmed FireFlow architecture is recorded in the edition 2.1 review. Galactica’s addition and the current verification limits are recorded in the edition 2.2 review.

### Decisions carried forward.

| Decision | Current treatment | Status |
| --- | --- | --- |
| Company name | Persistent Labs, two words. | Resolved by brief |
| FireFlow architecture | One product: FireFlow orchestration engine + MemoryTree (persistent memory) + FlameChorus (chat UX engine). Five products in the portfolio. | Confirmed by owner |
| Unfazed identity | Preserve source face, system type, white ground, blue and 6px corners. | Source-grounded |
| Galactica identity | Fifth product; live privacy technology across AI and blockchain. Proposed copper/monochrome family treatment; Galactica.com lockup with the owner-requested bold orange dot. | Owner brief + public sources |
| PI mark | Bold vector π; full name PrivateInference; abbreviation PI. | Required by brief |
| PI positioning | Proposed audience, promise and lavender; no claimed privacy architecture. | Concept for review |
| Other new marks | FireFlow node-F and Lanni action-L are proposed product marks. MemoryTree branches are a proposed component icon within FireFlow. | Concepts for review |
| Proof numbers | Do not publish the conflicting 146+ / ~300 / 320+ counts as canonical copy. | Needs authoritative facts |
| Licensing language | Avoid blanket “open source” claims; current docs describe source-available licensing. Verify per component and version. | Documentation-led |

### Release checklist.

- Every new product chapter has a role, mark, palette, type, geometry, motion, voice and component contract.
- Foreground/background pairs pass their intended contrast threshold on the actual surface.
- No clipped wordmarks, page overflow or inaccessible controls across the supported widths.
- Each factual claim has a dated source; conceptual screens and proposed product decisions remain labelled.
- Update JSON tokens first, rebuild the HTML, then run browser checks and independent reviews.

### Source inventory & original archive.

Supplied design bible and inherited PDF notes

The original v1.1 HTML is preserved unchanged at reference/original-design-bible.html. It includes a review of FF_intro.pdf, CSS measurements and historical source links. The underlying PDF was not supplied for this revision; its measurements and claims are inherited observations, not revalidated findings.

Current public sources · checked 23 September 2026

[Persistent AI site](https://persistentai.org/), [Lanni page](https://persistentai.org/lanni), [product documentation](https://docs.persistentai.org/), [Unfazed](https://unfazed.dev/), and [Galactica](https://galactica.com/) informed the product descriptions. The non-www Unfazed URL is the working source. The company name and FireFlow’s three-part product architecture follow the owner’s instructions, superseding legacy naming and portfolio descriptions in earlier sources. Galactica’s live status and AI/blockchain positioning follow the owner’s brief; public privacy and identity themes inform its proposed family adaptation. Source access and visual-verification limits are recorded in the Galactica revision review.

How to repeat the multi-agent review

Run the versioned workflow with the current HTML, source evidence and desktop/mobile screenshots. Independent strategy, visual and accessibility reviewers return structured findings. An integrator applies fixes between rounds. See the workflow guide. The current session’s reviews are recorded separately from the reusable harness tests.

Reference / 18

## One source of truth.

The tables, product palettes and downloadable CSS are generated from the same token data. Change a decision once, then regenerate the bible.

18

Copy CSS tokensDownload CSS ↓Download JSON ↓

```css
/* Persistent Labs v2.3 — generated from design-tokens.json. */
:root {
  /* core */
  --pl-ink: #1C1E21;
  --pl-void: #121212;
  --pl-gold: #FBD78E;
  --pl-gold-hover: #FFCB63;
  --pl-gold-pressed: #EABD64;
  --pl-gold-ink: #76580D;
  --pl-white: #FFFFFF;
  --pl-paper: #F6F6F6;
  --pl-cream: #FFF5E6;
  --pl-text-dark: #FFFFFF;
  --pl-text-dark-secondary: #CBCDD0;
  --pl-text-dark-muted: #A8ADB4;
  --pl-text-light: #1C1E21;
  --pl-text-light-secondary: #50545B;
  --pl-text-light-muted: #62666D;
  --pl-surface-dark: #25272A;
  --pl-surface-light: #FFFFFF;
  --pl-control-dark: #828891;
  --pl-control-light: #70757D;
  --pl-success-dark: #83D995;
  --pl-success-light: #246938;
  --pl-warning-dark: #F1C14E;
  --pl-warning-light: #785300;
  --pl-danger-dark: #FF9A8F;
  --pl-danger-light: #AE3024;
  --pl-info-dark: #8ECFFB;
  --pl-info-light: #215F8B;
  /* type */
  --pl-font-display: "Red Hat Display", "Helvetica Neue", Arial, sans-serif;
  --pl-font-text: "Red Hat Text", "Helvetica Neue", Arial, sans-serif;
  --pl-font-mono: "Red Hat Mono", ui-monospace, monospace;
  --pl-display-xl: clamp(2.75rem, 1.5rem + 4vw, 8rem);
  --pl-display: clamp(2.5rem, 1.5rem + 3vw, 5.5rem);
  --pl-h1: clamp(2rem, 1.5rem + 2vw, 4rem);
  --pl-h2: clamp(1.75rem, 1.25rem + 1.5vw, 3rem);
  --pl-h3: clamp(1.5rem, 1.25rem + 1vw, 2rem);
  --pl-h4: 1.25rem;
  --pl-h5: 1.125rem;
  --pl-lead: clamp(1.125rem, 1rem + .5vw, 1.5rem);
  --pl-body: 1rem;
  --pl-body-l: 1.125rem;
  --pl-body-s: .875rem;
  --pl-ui: 1rem;
  --pl-tag: .875rem;
  --pl-eyebrow: .75rem;
  --pl-track-head: -.03em;
  --pl-track-body: 0;
  --pl-lh-display: 1.04;
  --pl-lh-head: 1.15;
  --pl-lh-body: 1.6;
  --pl-lh-ui: 1.4;
  /* space */
  --pl-s1: 4px;
  --pl-s2: 8px;
  --pl-s3: 12px;
  --pl-s4: 16px;
  --pl-s5: 20px;
  --pl-s6: 24px;
  --pl-s8: 32px;
  --pl-s10: 40px;
  --pl-s12: 48px;
  --pl-s16: 64px;
  --pl-s20: 80px;
  --pl-s24: 96px;
  --pl-s30: 120px;
  /* layout */
  --pl-gutter: clamp(20px, 4vw, 64px);
  --pl-container: 1520px;
  --pl-reading: 66ch;
  --pl-section: clamp(64px, 7vw, 120px);
  --pl-grid-gap: clamp(16px, 2vw, 32px);
  --pl-target: 44px;
  /* radius */
  --pl-r-input: 8px;
  --pl-r-tile: 12px;
  --pl-r-card: 24px;
  --pl-r-feature: 40px;
  --pl-r-hero: 64px;
  --pl-r-pill: 999px;
  /* motion */
  --pl-t-fast: 150ms;
  --pl-t-ui: 200ms;
  --pl-t-panel: 300ms;
  --pl-t-ease: cubic-bezier(.2, 0, .2, 1);
}
[data-product="fireflow"] {
  --product-accent: #F7931A;
  --product-accent-ink: #8C4900;
  --product-on-accent: #1C1E21;
  --product-hover: #FFA638;
  --product-pressed: #E88712;
  --product-tint: #FFF0DE;
}
[data-product="unfazed"] {
  --product-accent: #8AB8F6;
  --product-accent-ink: #2570CC;
  --product-on-accent: #1C1E21;
  --product-hover: #A4C9FA;
  --product-pressed: #78A8E8;
  --product-tint: #EBF2FC;
}
[data-product="lanni"] {
  --product-accent: #FF6741;
  --product-accent-ink: #A6381C;
  --product-on-accent: #1C1E21;
  --product-hover: #FF8566;
  --product-pressed: #F06440;
  --product-tint: #FFF0EB;
}
[data-product="privateinference"] {
  --product-accent: #C4B5FD;
  --product-accent-ink: #6544A2;
  --product-on-accent: #1C1E21;
  --product-hover: #D5CAFF;
  --product-pressed: #AE9BEA;
  --product-tint: #F2EDFF;
}
[data-product="galactica"] {
  --product-accent: #F4A77A;
  --product-accent-ink: #97502A;
  --product-on-accent: #1C1E21;
  --product-hover: #FFC29D;
  --product-pressed: #E3986D;
  --product-tint: #FFF1E8;
  --product-logo-dot: #F7931A;
}
[data-product="fireflow"] [data-component="orchestration-engine"] {
  --component-accent: #F7931A;
  --component-accent-ink: #8C4900;
  --component-on-accent: #1C1E21;
  --component-hover: #FFA638;
  --component-pressed: #E88712;
  --component-tint: #FFF0DE;
}
[data-product="fireflow"] [data-component="memorytree"] {
  --component-accent: #8ECFFB;
  --component-accent-ink: #215F8B;
  --component-on-accent: #1C1E21;
  --component-hover: #A8DCFF;
  --component-pressed: #70BCEB;
  --component-tint: #E9F5FE;
}
[data-product="fireflow"] [data-component="flamechorus"] {
  --component-accent: #FBD78E;
  --component-accent-ink: #76580D;
  --component-on-accent: #1C1E21;
  --component-hover: #FFCB63;
  --component-pressed: #EABD64;
  --component-tint: #FFF5E6;
}
/* Semantic context must be scoped on fixed specimen surfaces too. */
[data-surface="dark"] { --surface: var(--pl-ink); --text: var(--pl-text-dark); --text-secondary: var(--pl-text-dark-secondary); --text-muted: var(--pl-text-dark-muted); --action: var(--pl-gold); --on-action: var(--pl-ink); --action-hover: var(--pl-gold-hover); --action-pressed: var(--pl-gold-pressed); --control-border: var(--pl-control-dark); --focus: var(--pl-gold); }
[data-surface="light"] { --surface: var(--pl-white); --text: var(--pl-text-light); --text-secondary: var(--pl-text-light-secondary); --text-muted: var(--pl-text-light-muted); --action: var(--pl-gold); --on-action: var(--pl-ink); --action-hover: var(--pl-gold-hover); --action-pressed: var(--pl-gold-pressed); --control-border: var(--pl-control-light); --focus: var(--pl-gold-ink); }
/* Pair product accent with ink on dark surfaces; accent-ink is text on light. */
[data-product] { --action: var(--product-accent); --on-action: var(--product-on-accent); --action-hover: var(--product-hover); --action-pressed: var(--product-pressed); }
[data-product][data-surface="dark"] { --focus: var(--product-accent); }
[data-product][data-surface="light"] { --focus: var(--product-accent-ink); }
[data-product="unfazed"][data-surface="light"] { --action: #2570CC; --on-action: #FFFFFF; --action-hover: #1D5BA7; --action-pressed: #174A89; }
@media (prefers-reduced-motion: reduce) { :root { --pl-t-fast: 0ms; --pl-t-ui: 0ms; --pl-t-panel: 0ms; } }

```

Core, type, space, layout, radius and motion tokens live in :root. Product tokens are scoped with data-product; core-part accents are scoped with data-component inside FireFlow. Core-part accents do not replace FireFlow action colors. Light/dark foregrounds are explicitly scoped with data-surface. The reading interface has its own layout styles. Product UI exceptions, including Unfazed, are documented in their chapters.

## Portable-package provenance

References above to original archives, review rounds and workflow guides describe records in the private source repository. They are historical context, not bundled dependencies or instructions to locate missing files. Applying this skill requires only the included references, tokens and assets. Current browser rendering remains unverified; do not inherit historical passes as proof for a new deliverable.
