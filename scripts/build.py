#!/usr/bin/env python3
"""Build a portable HTML bible and CSS tokens using only Python's standard library."""
from pathlib import Path
import json
import re
import html

ROOT = Path(__file__).resolve().parents[1]
T = json.loads((ROOT / 'tokens/design-tokens.json').read_text())
PRODUCTS = json.loads((ROOT / 'src/products.json').read_text())
E = html.escape

def token_css():
    lines = ['/* Persistent Labs v2.3 — generated from design-tokens.json. */', ':root {']
    for group, prefix in [('core',''),('type',''),('space','s'),('layout',''),('radius','r-'),('motion','t-')]:
        lines.append('  /* '+group+' */')
        lines += [f'  --pl-{prefix}{key}: {value};' for key,value in T[group].items()]
    lines.append('}')
    for product, values in T['products'].items():
        lines.append(f'[data-product="{product}"] {{')
        lines += [f'  --product-{key}: {value};' for key,value in values.items()]
        lines.append('}')
    for product, components in T['components'].items():
        for component, values in components.items():
            lines.append(f'[data-product="{product}"] [data-component="{component}"] {{')
            lines += [f'  --component-{key}: {value};' for key,value in values.items()]
            lines.append('}')
    lines += ['/* Semantic context must be scoped on fixed specimen surfaces too. */',
        '[data-surface="dark"] { --surface: var(--pl-ink); --text: var(--pl-text-dark); --text-secondary: var(--pl-text-dark-secondary); --text-muted: var(--pl-text-dark-muted); --action: var(--pl-gold); --on-action: var(--pl-ink); --action-hover: var(--pl-gold-hover); --action-pressed: var(--pl-gold-pressed); --control-border: var(--pl-control-dark); --focus: var(--pl-gold); }',
        '[data-surface="light"] { --surface: var(--pl-white); --text: var(--pl-text-light); --text-secondary: var(--pl-text-light-secondary); --text-muted: var(--pl-text-light-muted); --action: var(--pl-gold); --on-action: var(--pl-ink); --action-hover: var(--pl-gold-hover); --action-pressed: var(--pl-gold-pressed); --control-border: var(--pl-control-light); --focus: var(--pl-gold-ink); }',
        '/* Pair product accent with ink on dark surfaces; accent-ink is text on light. */',
        '[data-product] { --action: var(--product-accent); --on-action: var(--product-on-accent); --action-hover: var(--product-hover); --action-pressed: var(--product-pressed); }',
        '[data-product][data-surface="dark"] { --focus: var(--product-accent); }',
        '[data-product][data-surface="light"] { --focus: var(--product-accent-ink); }',
        '[data-product="unfazed"][data-surface="light"] { --action: #2570CC; --on-action: #FFFFFF; --action-hover: #1D5BA7; --action-pressed: #174A89; }',
        '@media (prefers-reduced-motion: reduce) { :root { --pl-t-fast: 0ms; --pl-t-ui: 0ms; --pl-t-panel: 0ms; } }', '']
    return '\n'.join(lines)

CSS = token_css()
(ROOT/'tokens/persistent-labs.tokens.css').write_text(CSS)

def svg_file(name, inner, view='0 0 96 96'):
    s=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{view}" fill="currentColor" role="img" aria-label="{E(name)}">{inner}</svg>'
    (ROOT/'assets'/f'{name}.svg').write_text(s+'\n')
    return s

svg_file('fireflow', '<path d="M18 14h60v16H34v18h32v16H34v18H18z"/><path d="M70 44h12v24H70z"/>')
svg_file('lanni', '<path d="M16 14h18v50h38v18H16z"/><circle cx="67" cy="29" r="13"/>')
svg_file('privateinference', '<path d="M10 22h76v16H73v26q0 8 8 8v14h-8q-16 0-16-20V38H39l-6 48H17l6-48H10z"/>')
svg_file('memorytree', '<path d="M43 30h10v14h22v24H65V54H53v14H43V54H31v14H21V44h22z"/><rect x="36" y="10" width="24" height="24" rx="5"/><rect x="14" y="66" width="24" height="20" rx="5"/><rect x="58" y="66" width="24" height="20" rx="5"/>')

def mark(name):
    s=(ROOT/'assets'/f'{name}.svg').read_text()
    s=re.sub(r'<style>.*?</style>','',s,flags=re.S)
    s=s.replace('class="mark"','fill="currentColor"')
    s=re.sub(r' role="img"| aria-label="[^"]*"','',s)
    return s.replace('<svg ', '<svg aria-hidden="true" ',1)

def logo(): return '<span class="wordmark">'+mark('persistent-labs')+'<span>Persistent Labs</span></span>'
def table(headers, rows, label):
    return f'<div class="table-wrap" role="region" tabindex="0" aria-label="{E(label)}"><table><thead><tr>'+''.join('<th scope="col">'+h+'</th>' for h in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+str(c)+'</td>' for c in row)+'</tr>' for row in rows)+'</tbody></table></div>'
def swatch(name,color,note=''):
    return f'<div class="swatch"><div class="swatch-color" style="--color:{color}" aria-hidden="true"></div><b>{E(name)}</b><code>{color}</code><small>{E(note)}</small></div>'
def card(title,copy): return f'<div class="card"><h3>{title}</h3><p>{copy}</p></div>'
SECTIONS=[]
def section(id,title,intro,body,group='Foundations',classes='',attrs=''):
    num=f'{len(SECTIONS)+1:02}'
    SECTIONS.append((id,title,num,group, f'<section class="section {classes}" id="{id}" {attrs}><div class="section-head"><div><div class="eyebrow">{group} / {num}</div><h2>{title}</h2><p class="intro">{intro}</p></div><span class="section-no" aria-hidden="true">{num}</span></div>{body}</section>'))

section('principles','A system with staying power.', 'One parent. Distinct products. A shared standard of care. This edition turns the original visual inventory into a practical system for making decisions.', '''
<div class="callout"><strong>Working edition 2.3 · 23 September 2026.</strong> Core rules are reconciled recommendations. Existing identities, proposed extensions and unconfirmed product decisions are labelled separately. The original bible is preserved in the reference archive.</div>
<div class="rule-list">
<div class="rule"><span class="rule-number">01</span><h3>Keep the recognizable parts.</h3><p>Graphite, warm gold, Red Hat and the infinity ribbon remain the Persistent Labs signature. Give established products room to keep their own identity.</p></div>
<div class="rule"><span class="rule-number">02</span><h3>Show how it works.</h3><p>Execution diagrams, readable commands and useful interface states do the explaining. Every product needs a visual grammar beyond a new accent color.</p></div>
<div class="rule"><span class="rule-number">03</span><h3>Make reading effortless.</h3><p>Use stable foreground colors, generous leading and a bounded reading width. Specimens must remain readable in either document theme.</p></div>
<div class="rule"><span class="rule-number">04</span><h3>Make the next action clear.</h3><p>One primary action per decision. Give feedback, preserve context and state what has changed. Rounded geometry supports this clarity.</p></div>
<div class="rule"><span class="rule-number">05</span><h3>Keep evidence beside claims.</h3><p>Separate a product promise from a verified capability. Date proof points and name their scope. Draft interfaces never masquerade as a live product.</p></div>
</div>''')

rows=[]
for p in PRODUCTS:
    t=T['products'][p['id']]
    portfolio_icon='<span class="portfolio-index" aria-hidden="true">05</span>' if p["id"]=="galactica" else mark(p["id"])
    rows.append(f'<a class="portfolio-row" href="#{p["id"]}" style="--brand-ink:{t["accent-ink"]};--tint:{t["tint"]}"><span class="product-icon">{portfolio_icon}</span><span class="product-name">{p["name"]}<span class="product-status">{p["status"]}</span></span><span class="product-role">{p["role"]}</span><span class="arrow" aria-hidden="true">↗</span></a>')
section('brand','Built by Persistent Labs.', 'Use an endorsed portfolio: the product leads with its own promise; “by Persistent Labs” provides a consistent maker’s signature.', '<div class="portfolio">'+''.join(rows)+'''</div>
<div class="callout"><strong>FireFlow is one product.</strong> Its three core parts are the FireFlow orchestration engine, MemoryTree for persistent memory and FlameChorus, the chat UX engine. They sit within the FireFlow chapter and share its product identity.</div>
<h3 class="subheading">Five products. A clear hierarchy.</h3><p class="small">Persistent Labs creates FireFlow, Unfazed.dev, Lanni, PrivateInference and Galactica. Lanni is built on FireFlow. Galactica is a live privacy technology firm across AI and blockchain; PrivateInference is an upcoming brand. Their listing together does not imply a shared technical architecture.</p>
<div class="grid2" style="margin-top:24px">'''+card('Core parts, one FireFlow identity.', 'MemoryTree and FlameChorus identify parts of FireFlow. Their names and accent colors help explain the system inside the product; they do not get separate portfolio cards, product chapters or maker endorsements.')+card('The endorsement has one job.', 'Use “by Persistent Labs” in a quiet footer or beneath a product lockup, with at least one line of clear space. It should be secondary to the product name. Do not combine multiple marks inside one crowded capsule.')+'</div>')

section('logo','A signature, not a watermark.', 'The original four-stroke infinity ribbon stays intact. Raise its contrast for identification and reserve fading for decorative uses.',
    '<div class="grid2"><div class="brand-stage">'+logo()+'<span class="caption">Primary / white on graphite</span></div><div class="brand-stage light">'+logo()+'<span class="caption">Reversed / graphite on white</span></div></div>'+table(['Specification','Rule'],[
    ['Lockup','Horizontal infinity ribbon + Persistent Labs, two words. Red Hat Display 500. Preserve the supplied ribbon paths.'],
    ['Clear space','One ribbon height on each side. Gap between ribbon and wordmark: half the ribbon height.'],
    ['Minimum size','Ribbon: 40px wide in the parent lockup; complete lockup: 180px wide. Use 24px minimum for separate product symbols.'],
    ['Color','Solid white on ink, solid ink on white. Full opacity for identification. Faded marks are decorative only and have no independent meaning.'],
    ['Narrow screens','Keep a readable horizontal lockup. Move the product endorsement to its own line; do not squeeze a co-brand row.'],
    ['Avoid','Distortion, gradient fills, clipped ribbons, reconstructed official product marks and substituting a guessed font glyph for the PI logo.']],'Parent logo specifications')+'<p class="note">Downloadable vector masters are in <a href="assets/persistent-labs.svg">assets/persistent-labs.svg</a> and the individual product chapters. New product symbols are labelled concepts.</p>')

def lum(color):
    rgb=[int(color[i:i+2],16)/255 for i in (1,3,5)]
    rgb=[c/12.92 if c<=.04045 else ((c+.055)/1.055)**2.4 for c in rgb]
    return sum(v*w for v,w in zip(rgb,(.2126,.7152,.0722)))
def contrast(a,b):
    x,y=sorted((lum(a),lum(b)));return (y+.05)/(x+.05)
pairs=[('Primary text','#FFFFFF','#1C1E21'),('Dark secondary','#CBCDD0','#25272A'),('Dark muted','#A8ADB4','#25272A'),('Light muted','#62666D','#F6F6F6'),('Gold button','#1C1E21','#FBD78E'),('Gold text on cream','#76580D','#FFF5E6'),('Success on dark','#83D995','#1C1E21')]
for p in PRODUCTS:
    t=T['products'][p['id']];pairs.append((p['name']+' light text',t['accent-ink'],'#FFFFFF'));pairs.append((p['name']+' dark accent',t['accent'],'#1C1E21'))
section('color','Warmth, with discipline.', 'Graphite does the grounding. Gold directs attention. Product accents carry identity; semantic colors carry meaning.',
    '<div class="swatches">'+''.join(swatch(*x) for x in [('Graphite','#1C1E21','Parent ground and primary light-surface text.'),('Warm gold','#FBD78E','Parent actions and text on dark.'),('Paper','#F6F6F6','Reading surfaces and light collateral.'),('Gold ink','#76580D','Accessible accent text on white and cream.')])+'</div>'+'''
<h3 class="subheading">Foregrounds belong to surfaces.</h3><div class="grid2">'''+card('Light surfaces', 'Primary #1C1E21 · secondary #50545B · muted #62666D. Use the deep product accent for links. Gold fills carry dark labels. A light specimen keeps these colors even when the surrounding document is dark.')+card('Dark surfaces', 'Primary #FFFFFF · secondary #CBCDD0 · muted #A8ADB4. Use the light product accent for emphasis. A dark specimen owns its text colors; it never inherits dark ink from the surrounding page.')+'</div>'+table(['Pair','Foreground','Background','Ratio'],[[n,f'<code>{a}</code>',f'<code>{b}</code>',f'<span class="pass">{contrast(a,b):.2f}:1</span>'] for n,a,b in pairs],'Calculated text contrast')+'''
<p class="note">Ratios are calculated from the source token values with the WCAG sRGB luminance formula. All listed text pairs meet 4.5:1. This is a check of these pairs, not certification of every future interface. Borders that identify controls must meet 3:1; decorative rules may be quieter.</p>
<h3 class="subheading">Semantic colors stay semantic.</h3>'''+table(['State','On light','On dark','Required label'],[['Success','#246938','#83D995','Complete / saved'],['Warning','#785300','#F1C14E','Needs review'],['Error','#AE3024','#FF9A8F','Failed / action required'],['Information','#215F8B','#8ECFFB','Information / source']],'Semantic status palette')+'''
<div class="callout"><strong>Reconciled from v1.1:</strong> deepen light gold from #8B6914 to #76580D; replace opacity-based muted copy with solid tokens; keep #FFCB63 as parent hover and #EABD64 as pressed. Historical gradients remain references, never backgrounds behind untested small text.</div>''')

type_rows=[['Display XL','display-xl','700 / 1.04','Campaign headline'],['Display','display','700 / 1.04','Product hero'],['Heading 1','h1','700 / 1.15','Major section'],['Heading 2','h2','700 / 1.15','Feature section'],['Heading 3','h3','700 / 1.15','Subsection'],['Heading 4','h4','600 / 1.15','Card title'],['Heading 5','h5','600 / 1.15','Small heading'],['Lead','lead','400 / 1.55','Opening context'],['Body large','body-l','400 / 1.6','Short introduction'],['Body','body','400 / 1.6','Reading / chat'],['Body small','body-s','400 / 1.6','Supporting copy'],['UI','ui','500 / 1.4','Controls'],['Tag','tag','500 / 1.4','Compact labels'],['Eyebrow','eyebrow','500 / 1.5','Short labels only']]
section('type','Three cuts. One clear hierarchy.', 'Red Hat Display makes the statement. Red Hat Text handles reading and controls. Red Hat Mono makes technical detail legible. Unfazed retains its established system-font identity.', '''
<div class="type-stage"><div class="type-row"><span class="type-label">Red Hat Display<br>700 / −3%</span><div class="type-display">Built to<br><span style="color:#FBD78E">keep going.</span></div></div><div class="type-row"><span class="type-label">Red Hat Text<br>400 / 1.6</span><p class="type-body">A good system helps people understand what is happening, what matters and what comes next.</p></div><div class="type-row"><span class="type-label">Red Hat Mono<br>400 / tabular</span><div class="type-mono">workflow / review-required<br>run_example_001 · illustrative data</div></div></div>
'''+table(['Role','CSS size','Weight / leading','Use'],[[name,f'<code>{E(T["type"][key])}</code>',weight,use] for name,key,weight,use in type_rows],'Type scale generated from tokens')+'''
<p class="note">Sizes use rem floors and bounded fluid growth. Body tracking is 0; headings use −.03em. Keep prose within 55–70 characters and left aligned. Main body starts at 16px; supporting copy at 14px; short metadata may use 11–12px with strong contrast. Size token names do not determine HTML heading levels.</p><p class="note">The font files and open license are bundled for offline use. Arial and system mono remain intentional fallbacks if fonts cannot load. Unfazed uses system sans and mono by design.</p>''')

section('layout','Let the content set the limits.', 'Build from a readable column, then add space. Replace artboard ratios and mobile multipliers with bounded containers and explicit layout changes.',
table(['Surface','Wide layout','Narrow layout'],[['Marketing','Maximum 1520px container; 64px outer gutter; two-column hero when both columns remain useful.','20px gutters; single column; headline before illustration.'],['Documentation','220–244px navigation; readable content up to 66ch; specimens can use the full content column.','Collapsible contents below 900px; keep visible menu control and keyboard exit.'],['Product UI','Navigation + main workspace + optional detail panel. Let the task determine column widths.','One primary task panel. Move details into explicit disclosure; preserve labels.'],['Unfazed','680px reading shell, sparse rows, system typography.','20px gutters; commands wrap or scroll locally.'],['Collateral','A4 / Letter for documents; 16:9 for presentations. Design for the actual output size.','Do not shrink a dense desktop table until labels become illegible.']],'Responsive layout rules')+'''
<div class="grid2" style="margin-top:32px">'''+card('Three working thresholds', 'Below 600px: stack paired cards and product diagrams. Below 900px: collapse the navigation rail. Below 1180px: simplify dense multi-column compositions. Also test 320, 390, 768, 1024 and 1440px; breakpoints are responses to content, not device brands.')+card('Overflow must be intentional', 'Allow a labelled data table or code sample to scroll within its own region. Text, headings, logos and the page itself must fit. Never hide a layout error with overflow:hidden on the body.')+'</div>')

space_use={'1':'Icon adjustment','2':'Label → control','3':'Compact inline gap','4':'Related content','5':'Mobile gutter','6':'Card padding / group gap','8':'Independent groups','10':'Large card padding','12':'Section heading → body','16':'Mobile sections','20':'Desktop sections','24':'Large section pause','30':'Maximum section pause'}
section('spacing','Space communicates structure.', 'Use a 4px base with an 8px rhythm. A few deliberate increments are more useful than dozens of extracted one-off values.', '<div class="metric-list">'+''.join(f'<div class="metric-row"><span class="value">{v}</span><div class="bar" style="--size:{v}" aria-hidden="true"></div><span class="small">{space_use[k]}</span></div>' for k,v in T['space'].items())+'</div>'+table(['Relationship','Small screens','Wide screens'],[['Headline → supporting copy','16px','20–24px'],['Supporting copy → action','24px','32px'],['Card inset','24px','28–40px'],['Card grid gap','16–24px','24–32px'],['Independent sections','64px','80–120px'],['Control hit area','At least 44 × 44px','At least 44 × 44px']],'Spacing application')+'<p class="note">Use shared spacing tokens for layout. Optical exceptions are limited to mark alignment and documented product identities, such as Unfazed’s existing 6px corners. Do not multiply mobile dimensions by a universal factor.</p>')

section('shape','Soft edges. Precise relationships.', 'The parent is generous and rounded. Product interfaces tune that softness to their job. Shape follows hierarchy and is never a substitute for spacing.', '<div class="radii">'+''.join(f'<div class="radius-item"><div class="radius-box" style="--r:{v}" aria-hidden="true"></div><span>{k} / {v}</span></div>' for k,v in T['radius'].items())+'</div>'+'''
<div class="nest"><div class="nest-inner"><h3>One rule for nested corners.</h3><p>Outer radius 40px. Ring 8px. Inner radius 32px. The inner and outer curves share a center. Use max(0, outer radius − inset) and render the value you specify.</p></div></div>
'''+table(['Material','Specification','Use'],[['Control outline','1px; #70757D on light or #828891 on dark','Inputs, secondary actions and essential boundaries.'],['Decorative divider','1px quiet neutral; not relied on to identify a control','Reading rhythm and non-interactive grouping.'],['Gold bloom','Optional, one per hero; never behind body copy','Parent campaign artwork only. Disabled in dense product UI.'],['Glass','White at 90%; 20px blur; opaque fallback','Optional parent marketing header. Ensure contrast over the worst background.'],['Aurora','Retain warm gold, copper, teal and sage as a static artwork palette','Feature imagery or a decorative frame. No continuous background animation by default.']],'Shape and material specifications'))

section('components','Every state is part of the design.', 'Default, hover, focus, pressed, disabled, loading and error states belong in the same specification. These examples are local demonstrations.', '''
<div class="specimen"><span class="caption">Button family / interactive local specimen</span><div class="buttons"><button type="button" class="btn" data-demo="Primary action selected. This is a local design specimen.">Primary action</button><button type="button" class="btn secondary" data-demo="Secondary action selected. This is a local design specimen.">Secondary action</button><button type="button" class="btn" disabled>Unavailable</button></div><div class="state-line"><span class="status-label success">✓ Complete</span><span class="status-label warning">! Needs review</span><span class="status-label danger">× Failed</span></div><div class="demo-feedback" aria-live="polite">Choose an action to see its feedback.</div></div>
'''+table(['State','Specification'],[['Default','48px control height; minimum hit area 44px; text label that names the action.'],['Hover','Parent fill #FFCB63; product hover token; same label and geometry.'],['Focus','3px visible ring, 4px offset, contrast checked against the local surface. Never suppress keyboard focus.'],['Pressed','Parent fill #EABD64; product pressed token. Do not move surrounding layout.'],['Disabled','Use the native disabled attribute; dim the fill but preserve a readable label. Explain prerequisites nearby.'],['Loading','Keep the control width stable, set aria-busy=true and show a textual progress label. Prevent duplicate submission.'],['Error','Explain the problem and recovery step beside the affected field. Announce the result; do not rely on red alone.']],'Component state contract')+'''
<h3 class="subheading">Fields explain what they need.</h3><div class="specimen"><div class="sample-field"><label for="run-name">Run name</label><input id="run-name" type="text" autocomplete="off" aria-describedby="run-hint" aria-invalid="false" placeholder="e.g. Invoice review"><p id="run-hint">A descriptive name helps people recognize this workflow.</p></div><div class="buttons"><button class="btn" id="validate-field" type="button">Validate example</button></div></div>
<p class="note">One primary action per decision. Tooltips supplement labels; they never carry essential instructions. Keep controls keyboard reachable and return focus to the initiating control when dismissing overlays.</p>''')

section('motion','Make movement explain change.', 'The default is calm. Motion earns its place by showing a transition, a relationship or progress that is really occurring.',
table(['Token','Duration','Purpose'],[['Fast','150ms','Color feedback and compact toggles'],['UI','200ms','Card state changes and action feedback'],['Panel','300ms','Disclosure and panel entrance'],['Reduced motion','0ms; preserve textual feedback','Honor prefers-reduced-motion in CSS and scripted transitions']],'Motion rules')+'''
<div id="imagery"><h3 class="subheading">Build an image language from the product.</h3></div><div class="grid2">'''+card('Primary imagery', 'Use real product views, clear diagrams and meaningful interface details. Label illustrative data. Keep screenshots legible at their rendered size and remove secrets from captured content.')+card('Secondary material', 'The original prismatic glass can remain a parent campaign motif. Keep it away from small text and operational interfaces. FireFlow uses execution diagrams, memory provenance and conversation states; Unfazed uses commands; Lanni uses actions; PI uses explicit boundaries.')+'</div><p class="note">Icons use a consistent 24px grid and 2px strokes unless they are a supplied filled brand mark. Avoid emoji as interface icons. Do not animate the Unfazed face or the PI symbol as decorative loading states.</p>')

section('voice','Confidence comes from clarity.', 'Name the action, explain the mechanism and give the reader a useful next step. Each product has its own cadence inside that standard.',
table(['Context','Use','Avoid'],[['Claims','A dated, scoped capability linked to a source','Regulatory-grade, unbreakable, zero risk, or unsupported performance numbers'],['Actions','Sentence case: “Inspect the workflow”','Title Case Everywhere or a label that changes on hover'],['Technical copy','Name the mechanism when it explains the benefit','Acronyms without context or unqualified “exactly-once” promises'],['Status','“Awaiting review”, “Complete”, “Failed”','Color dots that force people to infer meaning'],['Product name','Persistent Labs; FireFlow; Unfazed.dev; Lanni; PrivateInference (PI); Galactica','PersistentAI as the new company name or Fireflow in body text'],['FireFlow core parts','FireFlow orchestration engine; MemoryTree (persistent memory); FlameChorus (chat UX engine)','Listing MemoryTree or FlameChorus as standalone products; Flame Chorus as two words']],'Voice and naming rules')+'''
<div id="surfaces"><h3 class="subheading">Apply the system by surface.</h3></div><div class="grid2">'''+card('Marketing & product UI', 'Parent marketing leads with graphite and gold. Product marketing leads with that product’s identity. Product UI prioritizes task clarity and accessible states. Preserve Unfazed’s white, square-edged simplicity.')+card('Docs & collateral', 'Use a light reading surface by default, optional dark view and product accents for orientation. Print uses real paper sizes and static graphics. Archive earlier measurements so history cannot be mistaken for a current rule.')+'</div>')

def product_ui(p):
    id=p['id']
    if id=='fireflow':
        body='<p class="core-ui-label">FireFlow orchestration engine</p><div class="flow-nodes"><div class="flow-node"><b>01 / Receive</b><span class="node-state">Input recorded</span></div><span class="flow-arrow" aria-hidden="true">→</span><div class="flow-node"><b>02 / Review</b><span class="node-state">Awaiting a decision</span></div><span class="flow-arrow" aria-hidden="true">→</span><div class="flow-node"><b>03 / Execute</b><span class="node-state">Not started</span></div></div><div class="core-ui-parts"><div><p class="core-ui-label">MemoryTree / persistent memory</p><div class="context-row"><b>Project preferences</b><span>Source: example project brief</span></div><div class="context-row"><b>Example workspace</b><span>Updated 23 Sep 2026 · illustrative</span></div></div><div><p class="core-ui-label">FlameChorus / chat UX engine</p><div class="chat-bubble">Review the proposed action before execution.</div><p class="ui-result">Conversation state: awaiting a decision</p></div></div>'
        button='Inspect the workflow';result='Example workflow: step 02 is awaiting a decision; step 03 has not started.'
    elif id=='unfazed':
        body='<div class="terminal-line"><span class="prompt">$</span> deploy &lt;your-project&gt;</div><p class="small" style="margin-top:16px">Choose a destination. Read the guide. Let the agent do the work.</p><p class="ui-result" style="margin-top:12px">Pseudocode specimen. Use the live documentation for actual commands.</p>'
        button='Inspect the example';result='Illustrative deployment panel. Visit unfazed.dev for the current command and deployment options.'
    elif id=='lanni':
        body='<div class="chat-bubble user">Prepare a summary of this week’s decisions.</div><div class="chat-bubble">I can prepare a draft. Review the sources and the summary before sharing it.</div><div class="context-row"><b>Weekly summary</b><span>Draft · ready for review</span></div>'
        button='Review the action';result='Example action: prepare a draft summary. Sharing is a separate action requiring review.'
    elif id=='privateinference':
        body='<div class="context-row"><b>Deployment location</b><span>Not specified</span></div><div class="context-row"><b>Access scope</b><span>Not specified</span></div><div class="context-row"><b>Retention policy</b><span>Not specified</span></div>'
        button='Explore the concept';result='PI is an upcoming identity concept. Architecture and privacy properties have not been specified.'
    elif id=='galactica':
        body='''<div class="disclosure-heading"><h4>Review a disclosure</h4><span class="disclosure-status">Awaiting review · example</span></div><div class="disclosure-grid"><div class="disclosure-panel"><p class="disclosure-label">01 / The request</p><dl><dt>Requester</dt><dd>Example service</dd><dt>Purpose</dt><dd>Access to an age-restricted experience</dd><dt>Requested statement</dt><dd>Age is 18 or above</dd></dl></div><div class="disclosure-panel"><p class="disclosure-label">02 / Proposed disclosure</p><dl><dt>Statement result</dt><dd>Not generated</dd><dt>Personal fields</dt><dd>No name or birth date in this example</dd><dt>Consent</dt><dd>No authorization given</dd></dl></div></div><p class="disclosure-footnote">Illustrates the distinction between a statement and its underlying data. Actual disclosures, processing and retention depend on the implementation.</p>'''
        button='Review the disclosure';result='Example only: the requested statement is age 18 or above. No proof was generated. No data was shared.'
    else:
        raise ValueError('Unknown product: '+id)
    icon='' if id=='galactica' else mark(id)
    name_html='<span class="galactica-ui-wordmark" role="img" aria-label="Galactica.com">'+mark(id)+'</span>' if id=='galactica' else '<span>'+('unfazed' if id=='unfazed' else E(p['name']))+'</span>'
    return f'<div class="product-ui"><div class="ui-header">{icon}{name_html}<span class="ui-caption">Illustrative interface / not live data</span></div><div class="ui-body">{body}</div><div class="ui-action"><button class="btn" type="button" data-demo="{E(result)}">{button}</button></div><p class="ui-result" aria-live="polite">Local specimen. No product action will run.</p></div>'

def fireflow_architecture(product):
    parts=[]
    for i,c in enumerate(product['components'],1):
        icon=mark(c['mark']) if c['mark'] else '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M4 4h16v12H9l-5 4V4z"/><path d="M8 8h8M8 12h5"/></svg>'
        parts.append(f'<a class="core-part" data-component="{c["id"]}" href="#{c["id"]}"><span class="core-part-icon">{icon}</span><span class="core-part-number">Core part 0{i}</span><h4>{E(c["name"])}</h4><p>{E(c["role"])}</p><span class="core-part-link">View specifications ↓</span></a>')
    return '<div class="fireflow-core" id="fireflow-core"><h3>Three core parts. One product.</h3><p class="small">The orchestration engine, persistent memory and chat UX engine together make up FireFlow.</p><div class="fireflow-core-grid">'+''.join(parts)+'</div><p class="note">One FireFlow product identity and one “by Persistent Labs” endorsement. Component names clarify each part of the system.</p></div>'

def fireflow_component_specs(product):
    parts=[]
    for i,c in enumerate(product['components'],1):
        specs=''.join(f'<div class="spec-detail"><h4>{E(k)}</h4><p>{E(v)}</p></div>' for k,v in c['specs'])
        download='<p class="note"><a href="assets/memorytree.svg" download>Download proposed MemoryTree component icon ↓</a></p>' if c['id']=='memorytree' else ''
        parts.append(f'<article class="core-spec" id="{c["id"]}" data-component="{c["id"]}"><p class="eyebrow">FireFlow / Core part 0{i}</p><h3>{E(c["name"])}</h3><p class="small">{E(c["description"])}</p><div class="spec-grid">{specs}</div>{download}</article>')
    return ''.join(parts)

for p in PRODUCTS:
    id=p['id'];t=T['products'][id]
    cover=f'<div class="product-cover"><div><div class="product-label">{E(p["status"])}</div><h3>{E(p["headline"])}</h3><p>{E(p["description"])}</p><div class="endorsement">by Persistent Labs</div></div><div class="giant-mark">{mark(id)}</div></div>'
    if id=='galactica':
        cover=f'''<div class="product-cover galactica-cover"><div class="galactica-masthead"><span class="galactica-title" role="img" aria-label="Galactica.com">{mark(id)}</span><span class="product-label">Live product / proposed family treatment</span></div><div class="galactica-cover-body"><div><h3>{E(p['headline'])}</h3><p>{E(p['description'])}</p><div class="galactica-domains"><span>AI</span><span>Blockchain</span></div></div><div class="proof-motif" aria-hidden="true"><svg viewBox="0 0 240 200" fill="none"><rect x="15" y="20" width="126" height="160" rx="12" stroke="#828891"/><path d="M37 53h68M37 70h48M37 103h68M37 120h48M37 153h34" stroke="#CBCDD0" stroke-width="2"/><path d="M125 100h75" stroke="currentColor" stroke-width="2"/><circle cx="200" cy="100" r="24" fill="#1C1E21" stroke="currentColor" stroke-width="2"/><circle cx="200" cy="100" r="7" fill="currentColor"/></svg><span>A statement, selectively disclosed.</span></div></div><div class="galactica-cover-footer"><span>Privacy technology / AI &amp; blockchain</span><span>by Persistent Labs</span></div></div>'''
    body=cover+f'<p class="product-caption">{E(p["evidence"])} '+(f'<a href="{p["source"]}" target="_blank" rel="noopener">{E(p["sourceLabel"])} ↗</a>' if p['source'] else E(p['sourceLabel']))+'</p>'
    if id=='fireflow': body+=fireflow_architecture(p)
    if id=='galactica':
        body+='<div class="grid2 galactica-direction">'+card('Carry the core forward.', 'Keep the name, the privacy and identity themes, and the public preview’s monochrome/orange direction. Keep the owner-directed Galactica.com lockup with its bold orange dot. The site’s selective-disclosure narrative gives the identity a useful explanatory focus.')+card('Make the family connection.', 'Use the shared reading grid, Red Hat typography, accessible color pairs and quiet maker endorsement. Give AI and blockchain separate editorial lanes. Galactica is live; PI remains an upcoming brand with its own π identity.')+'</div><p class="note">Source boundary: public text and an indexed <a href="https://galactica.com/preview.jpg" target="_blank" rel="noopener">homepage preview</a> informed this direction. Exact site CSS and direct image inspection were unavailable. Copper values and visual specifications are proposed family adaptations. The Galactica.com lockup, including its bold orange dot, follows the owner’s subsequent direction; the diagram is explanatory artwork.</p>'
    body+='<div class="swatches product-palette">'+''.join([swatch('Signature on dark',t['accent'],'Foreground on graphite; ink label on fill.'),swatch('Signature on light',t['accent-ink'],'Text on white.'),swatch('Product tint',t['tint'],'Decorative light surface; ink text.'),swatch('Shared graphite','#1C1E21','Neutral foundation.')])+'</div>'
    body+='<div class="spec-grid">'+''.join(f'<div class="spec-detail"><h3>{E(k)}</h3><p>{E(v)}</p></div>' for k,v in p['specs'])+'</div>'
    body+='<h3 class="subheading">The system in use.</h3>'+product_ui(p)
    body+='<div class="grid2" style="margin-top:24px">'+card('Do',E(p['do']))+card('Avoid',E(p['avoid']))+'</div>'
    if id=='galactica':
        body+='<div class="download-row"><a class="utility" href="assets/galactica.svg" download>Download Galactica.com lockup ↓</a><a class="utility" href="https://galactica.com/" target="_blank" rel="noopener">Visit Galactica ↗</a><a class="utility" href="tokens/design-tokens.json" download>Download family tokens ↓</a></div><p class="note">Owner-directed family lockup: Galactica.com, with a bold orange dot. The downloadable SVG contains outlined lettering and needs no installed font. This is an adapted lockup, not an extracted website master.</p>'
    else:
        body+=f'<div class="download-row"><a class="utility" href="assets/{id}.svg" download>Download {"source mark" if id=="unfazed" else "π vector" if id=="privateinference" else "concept mark"} ↓</a></div>'
    if id=='fireflow': body+=fireflow_component_specs(p)
    if id=='privateinference':
        body+='<div class="grid2"><div class="brand-stage"><div style="width:80px">'+mark(id)+'</div><span class="caption">Solid white / primary</span></div><div class="brand-stage light"><div style="width:80px">'+mark(id)+'</div><span class="caption">Solid ink / reversed</span></div></div>'
    if id=='unfazed':
        body+='<p class="note">Source blue #2570CC is the sRGB approximation of oklch(0.55 0.16 256); #8AB8F6 is a proposed dark-surface companion. Product text uses #141414 on white; parent endorsement uses the shared family language.</p>'
    section(id,p['name'],p['role'],body,'Product identities','product-section',f'data-product="{id}" style="--brand:{t["accent"]};--brand-ink:{t["accent-ink"]};--product-hover:{t["hover"]};--product-pressed:{t["pressed"]}"')

section('decisions','A living system needs a record.', 'Use the bible to make decisions, and the review record to understand why they changed. A clean visual treatment must never turn an assumption into a fact.', '''
<div class="review-round"><span class="round">Round 01</span><div><h3>Diagnose the original.</h3><p>Independent strategy and visual reviews separated established identity from unsupported claims. The visual audit recorded 18 issues, including low contrast, clipped specimens and contradictory tokens. <a href="reviews/round-1-design.md">Read the design review</a> · <a href="reviews/round-1-strategy.md">Read the strategy review</a>.</p></div></div>
<div class="review-round"><span class="round">Round 02</span><div><h3>Review the revised system.</h3><p>Check distinct product roles, accessible color pairs, token consistency and rendered layouts. Record findings against the revision and fix them before the next review. Evidence and results are in the <a href="reviews/README.md">review record</a>.</p></div></div>
<div class="review-round"><span class="round">Round 03</span><div><h3>Verify the corrections.</h3><p>Recheck prior findings and test navigation, theme selection, copy feedback, responsive layouts and reduced motion. The reusable workflow stores reviewer outputs and artifact hashes; it stops for fixes instead of granting its own approval.</p></div></div>
<p class="note">The three review rounds above cover edition 2.0. The owner-confirmed FireFlow architecture is recorded in <a href="reviews/fireflow-architecture-update.md">the edition 2.1 review</a>. Galactica’s addition and the current verification limits are recorded in <a href="reviews/galactica-identity-update.md">the edition 2.2 review</a>.</p><h3 class="subheading">Decisions carried forward.</h3>
'''+table(['Decision','Current treatment','Status'],[['Company name','Persistent Labs, two words.','Resolved by brief'],['FireFlow architecture','One product: FireFlow orchestration engine + MemoryTree (persistent memory) + FlameChorus (chat UX engine). Five products in the portfolio.','Confirmed by owner'],['Unfazed identity','Preserve source face, system type, white ground, blue and 6px corners.','Source-grounded'],['Galactica identity','Fifth product; live privacy technology across AI and blockchain. Proposed copper/monochrome family treatment; Galactica.com lockup with the owner-requested bold orange dot.','Owner brief + public sources'],['PI mark','Bold vector π; full name PrivateInference; abbreviation PI.','Required by brief'],['PI positioning','Proposed audience, promise and lavender; no claimed privacy architecture.','Concept for review'],['Other new marks','FireFlow node-F and Lanni action-L are proposed product marks. MemoryTree branches are a proposed component icon within FireFlow.','Concepts for review'],['Proof numbers','Do not publish the conflicting 146+ / ~300 / 320+ counts as canonical copy.','Needs authoritative facts'],['Licensing language','Avoid blanket “open source” claims; current docs describe source-available licensing. Verify per component and version.','Documentation-led']],'Decision register')+'''
<h3 class="subheading">Release checklist.</h3><ul class="checklist"><li>Every new product chapter has a role, mark, palette, type, geometry, motion, voice and component contract.</li><li>Foreground/background pairs pass their intended contrast threshold on the actual surface.</li><li>No clipped wordmarks, page overflow or inaccessible controls across the supported widths.</li><li>Each factual claim has a dated source; conceptual screens and proposed product decisions remain labelled.</li><li>Update JSON tokens first, rebuild the HTML, then run browser checks and independent reviews.</li></ul>
<div id="pdf"><h3 class="subheading">Source inventory & original archive.</h3></div>
<details><summary>Supplied design bible and inherited PDF notes</summary><p>The original v1.1 HTML is preserved unchanged at <a href="reference/original-design-bible.html">reference/original-design-bible.html</a>. It includes a review of FF_intro.pdf, CSS measurements and historical source links. The underlying PDF was not supplied for this revision; its measurements and claims are inherited observations, not revalidated findings.</p></details>
<details><summary>Current public sources · checked 23 September 2026</summary><p><a href="https://persistentai.org/">Persistent AI site</a>, <a href="https://persistentai.org/lanni">Lanni page</a>, <a href="https://docs.persistentai.org/">product documentation</a>, <a href="https://unfazed.dev/">Unfazed</a>, and <a href="https://galactica.com/">Galactica</a> informed the product descriptions. The non-www Unfazed URL is the working source. The company name and FireFlow’s three-part product architecture follow the owner’s instructions, superseding legacy naming and portfolio descriptions in earlier sources. Galactica’s live status and AI/blockchain positioning follow the owner’s brief; public privacy and identity themes inform its proposed family adaptation. Source access and visual-verification limits are recorded in the Galactica revision review.</p></details>
<details><summary>How to repeat the multi-agent review</summary><p>Run the versioned workflow with the current HTML, source evidence and desktop/mobile screenshots. Independent strategy, visual and accessibility reviewers return structured findings. An integrator applies fixes between rounds. See <a href="docs/review-workflow.md">the workflow guide</a>. The current session’s reviews are recorded separately from the reusable harness tests.</p></details>
''','Reference')

section('tokens','One source of truth.', 'The tables, product palettes and downloadable CSS are generated from the same token data. Change a decision once, then regenerate the bible.', '''
<div class="download-row"><button type="button" class="utility" id="copy-tokens">Copy CSS tokens</button><a class="utility" href="tokens/persistent-labs.tokens.css" data-download="css">Download CSS ↓</a><a class="utility" href="tokens/design-tokens.json" data-download="json">Download JSON ↓</a></div><pre class="codeblock" id="tokens-src" tabindex="0" aria-label="Generated CSS tokens">'''+E(CSS)+'''</pre><p class="note">Core, type, space, layout, radius and motion tokens live in :root. Product tokens are scoped with data-product; core-part accents are scoped with data-component inside FireFlow. Core-part accents do not replace FireFlow action colors. Light/dark foregrounds are explicitly scoped with data-surface. The reading interface has its own layout styles. Product UI exceptions, including Unfazed, are documented in their chapters.</p>''','Reference')

nav=[];last_group=None
for id,title,num,group,_ in SECTIONS:
    if group!=last_group:nav.append(f'<div class="nav-group">{group}</div>');last_group=group
    short={'principles':'Principles','brand':'Portfolio architecture','logo':'Parent identity','color':'Color & contrast','type':'Typography','layout':'Layout & grid','spacing':'Spacing','shape':'Shape & effects','components':'Components','motion':'Motion & imagery','voice':'Voice & surfaces','decisions':'Review & decisions','tokens':'Token library'}.get(id,title)
    dot=f'<span class="dot" style="--dot:{T["products"][id]["accent-ink"]}" aria-hidden="true"></span>' if id in T['products'] else f'<span class="num">{num}</span>'
    nav.append(f'<a class="nav-link" href="#{id}">{dot}{short}</a>')
font_css=(ROOT/'src/fonts.css').read_text() if (ROOT/'src/fonts.css').exists() else ''
styles=CSS+'\n'+font_css+'\n'+(ROOT/'src/style.css').read_text()
js=(ROOT/'src/app.js').read_text()
cover_products=''.join(f'<span><i style="--dot:{T["products"][p["id"]]["accent"]}"></i>{p["name"]}</span>' for p in PRODUCTS)
token_json=json.dumps(T).replace('<', chr(92)+'u003c')
document=f'''<!doctype html>
<html lang="en" data-theme="light"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="Persistent Labs design bible. A shared foundation and distinct product identities for FireFlow, Unfazed.dev, Lanni, PrivateInference and Galactica. FireFlow contains the orchestration engine, MemoryTree and FlameChorus."><title>Persistent Labs — Design Bible 2.3</title><style>{styles}</style></head><body>
<a class="skip" href="#main">Skip to design bible</a><header class="site-bar"><a class="home-link" href="#main" aria-label="Persistent Labs design bible home">{logo()}</a><nav class="quick-nav" aria-label="Main navigation"><a href="#principles">Foundations</a><a href="#brand">Products</a><a href="#tokens">Tokens</a><a href="#decisions">Guidelines</a></nav><button id="menu-toggle" type="button" aria-expanded="false" aria-controls="contents">Contents</button></header>
<aside class="rail" id="contents">{logo()}<div class="edition">Design bible / edition 02.3<br>23 September 2026</div><nav class="rail-nav" aria-label="Design bible contents">{''.join(nav)}</nav><div class="rail-footer"><button class="theme-button" type="button" id="theme-toggle" aria-pressed="false">Switch to dark view</button></div></aside>
<main class="page" id="main" tabindex="-1"><header class="cover"><div class="cover-top"><span class="label">Persistent Labs / Design bible</span><span>Edition 02.3<br>A working standard</span></div><div class="cover-art" aria-hidden="true">{mark('persistent-labs')}</div><div class="cover-main"><h1>Distinct.<br>By design.<em>Persistent.<br>By nature.</em></h1><p>A shared foundation. A family of products with something of their own to say.</p></div><div class="cover-bottom"><div class="cover-products">{cover_products}</div><a href="#brand">Explore the system ↗</a></div></header>
<div class="content">{''.join(s[4] for s in SECTIONS)}<footer class="footer"><span>Persistent Labs / Design system 2.3<br>FireFlow / orchestration engine + MemoryTree + FlameChorus.</span><a href="#main">Back to the beginning ↑</a></footer></div></main><div class="sr-only" id="live-status" role="status" aria-live="polite"></div><script type="application/json" id="token-json">{token_json}</script><script>{js}</script></body></html>'''
(ROOT/'index.html').write_text(document)
print(f'Built index.html ({len(document):,} characters), {len(SECTIONS)} chapters and generated CSS tokens.')
