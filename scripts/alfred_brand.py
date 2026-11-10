"""Alfred's scoped chapter and portable guide, from one guidance/token source.

Importing this module and rendering are read-only. Only build_assets writes files.
"""
from pathlib import Path
import html
import json

ROOT = Path(__file__).resolve().parents[1]
E = html.escape
AGENT_SKILL_URL = 'https://raw.githubusercontent.com/nonprophet-max/persistent-labs-design-system/codex/design-bible/plugins/alfred-brand/skills/alfred-brand/SKILL.md'


def sources():
    return (json.loads((ROOT / 'src/alfred-brand.json').read_text()),
            json.loads((ROOT / 'tokens/design-tokens.json').read_text())['identities']['alfred'])


def token_css(identity):
    lines = ['/* Generated from identities.alfred. Do not edit. */', '[data-product="alfred"] {']
    for key, value in identity['color'].items():
        lines.append(f'  --alfred-{key}: {value};')
    for role, font in identity['font'].items():
        stack = ', '.join('"'+x+'"' if ' ' in x else x for x in font['stack'])
        lines.append(f'  --alfred-font-{role}: {stack};')
    for key, value in identity['shape'].items():
        if key.endswith('Px'): lines.append(f'  --alfred-{key[:-2]}: {value}px;')
    for key, value in identity['spacing']['roles'].items():
        value = f'clamp({value["min"]}px, {value["fluid"]}, {value["max"]}px)' if isinstance(value, dict) else f'{value}px'
        lines.append(f'  --alfred-{key}: {value};')
    lines += [f'  --alfred-container: {identity["layout"]["containerMaxPx"]}px;', f'  --alfred-target: {identity["web"]["controlMinPx"]}px;', '}']
    for role, values in identity['typography'].items():
        size = f'clamp({values["sizePx"]}px, {values["fluid"]}, {values["maxSizePx"]}px)' if 'fluid' in values else f'{values["sizePx"]}px'
        lines.append(f'[data-product="alfred"] .alfred-type-{role} {{ font-family: var(--alfred-font-{values["font"]}); font-size: {size}; font-weight: {values["weight"]}; line-height: {values["lineHeight"]}; letter-spacing: {values["trackingEm"]}em;'+(' font-variant-numeric: tabular-nums;' if values.get('tabular') else '')+' }')
    return '\n'.join(lines)+'\n'


def font_css(identity):
    lines = ['/* Generated from identities.alfred; Cormorant Garamond supplies Cyrillic heading glyphs. */']
    for font in identity['font'].values():
        for file in font['files']:
            lines.append('@font-face{font-family:"'+font['bundledFamily']+'";font-style:normal;font-weight:'+font['declaredWeight']+';font-display:swap;src:url("'+file['file']+'") format("woff2");unicode-range:'+file['unicodeRange']+'}')
    return '\n'.join(lines)+'\n'


def brand_markdown():
    guidance, identity = sources()
    lines = ['# Alfred brand guide', f'\nCurrent v{guidance["version"]} · {guidance["editionDate"]}', '\n'+guidance['authority']]
    for section in guidance['sections']:
        lines += ['\n## '+section['title'], '\n'+section['headline']]
        lines += ['\n'+text for text in section['paragraphs']]
        if section['id'] == 'voice':
            for example in guidance['voiceExamples']:
                lines += [f'\n**{example["context"]}:** {example["use"]} Avoid: {example["avoid"]} {example["reason"]}']
    lines += ['\n## Exact colours', '\n| Token | Value |', '| --- | --- |']
    lines += [f'| {name} | `{value}` |' for name, value in identity['color'].items()]
    lines += ['\n## Exact type roles', '\n| Role | Family | Size | Weight | Line height |', '| --- | --- | --- | --- | --- |']
    for role, values in identity['typography'].items():
        size = f'clamp({values["sizePx"]}px, {values["fluid"]}, {values["maxSizePx"]}px)' if 'fluid' in values else f'{values["sizePx"]}px'
        lines += [f'| {role} | {identity["font"][values["font"]]["bundledFamily"]} | {size} | {values["weight"]} | {values["lineHeight"]} |']
    lines += ['\n## Files', '\nUse `tokens.json`, `tokens.css` and `fonts.css` beside this guide. Preserve the `fonts/`, `logos/` and `illustrations/` folders. See `ASSETS-LICENCES.md` and `provenance.json` for rights and origin.']
    return '\n'.join(lines)+'\n'


def build_assets():
    _, identity = sources()
    target = ROOT / 'assets/alfred'; target.mkdir(parents=True, exist_ok=True)
    (target / 'tokens.json').write_text(json.dumps(identity, indent=2, ensure_ascii=False)+'\n')
    (target / 'tokens.css').write_text(token_css(identity))
    (target / 'fonts.css').write_text(font_css(identity))
    (target / 'brand-guide.md').write_text(brand_markdown())


def render_alfred():
    guidance, identity = sources()
    color = identity['color']
    def image(file, alt, cls='', extra=''):
        return f'<img class="{cls}" src="assets/alfred/{file}" alt="{E(alt)}" {extra}>'
    def download(file, label):
        return f'<a class="alfred-download" href="assets/alfred/{file}" download>{E(label)}<span aria-hidden="true">↓</span></a>'
    def copy(value, label, cls=''):
        return f'<button class="alfred-copy {cls}" type="button" data-alfred-copy="{E(value, quote=True)}" hidden>{E(label)}</button>'
    def paragraphs(section):
        return ''.join(f'<p>{E(p)}</p>' for p in section['paragraphs'])
    def section(key, demo):
        item = next(x for x in guidance['sections'] if x['id'] == key)
        return f'<section class="alfred-section" id="alfred-{key}"><div class="alfred-rail"><h3>{E(item["title"])}</h3></div><div class="alfred-section-body"><h4 class="alfred-section-title">{E(item["headline"])}</h4>{demo}<div class="alfred-guidance">{paragraphs(item)}</div></div></section>'
    nav = '<nav class="alfred-nav" aria-label="Alfred chapter sections">'+''.join(f'<a href="#alfred-{x["id"]}">{E(x["title"])}</a>' for x in guidance['sections'])+'</nav>'
    meet = guidance['sections'][0]
    hero = f'''<header class="alfred-intro" id="alfred-meet"><div class="alfred-masthead">{image('logos/alfred-logo-ink.svg', 'Alfred', 'alfred-header-logo')}<span>Brand guide · v0.3</span><a href="{E(AGENT_SKILL_URL)}" data-alfred-agent-skill>Agent skill</a><a href="#alfred-resources">Use the brand <span aria-hidden="true">↓</span></a></div>
<h2 class="alfred-type-h1">{E(guidance['promise'])}</h2><div class="alfred-hero-body">{image('illustrations/hero-mascot-light-bg.png', 'Alfred’s supplied multi-armed butler, facing toward the introduction.', 'alfred-mascot', 'width="340" height="340"')}<div><p class="alfred-type-lead">{E(meet['paragraphs'][0])}</p><p class="alfred-functional">{E(guidance['functionalPromise'])}</p><p>{E(meet['paragraphs'][1])}</p><div class="alfred-signature-palette" aria-label="Signature palette"><span>Paper</span><span>Sand</span><span>Ink</span><span>Accent</span></div></div></div><p class="alfred-caption">{E(meet['paragraphs'][2])}</p></header>'''
    logos = '''<div class="alfred-controls" data-alfred-logo-controls hidden><span>Compare artwork</span><button type="button" data-alfred-view="both" aria-pressed="true">Both grounds</button><button type="button" data-alfred-view="light" aria-pressed="false">Light ground</button><button type="button" data-alfred-view="dark" aria-pressed="false">Dark ground</button></div><div class="alfred-logo-comparison">'''
    for surface, variant, caption in [('light','ink','Ink on paper'),('dark','paper','Paper on ink')]:
        logos += f'<figure class="alfred-logo-board alfred-{surface}" data-alfred-logo="{surface}"><div class="alfred-clearspace">{image("logos/alfred-logo-"+variant+".svg", "Alfred wordmark: "+caption)}</div><div class="alfred-mark-row">{image("logos/alfred-icon-"+variant+".svg", "Standalone Alfred star mark")}<figcaption>{caption}<br>½ wordmark height clear space</figcaption></div></figure>'
    logos += '</div><div class="alfred-downloads">'+download('logos/alfred-logo-ink.svg','Ink logo · SVG')+download('logos/alfred-logo-paper.svg','Paper logo · SVG')+download('logos/alfred-icon-ink.svg','Ink mark · SVG')+download('logos/alfred-icon-paper.svg','Paper mark · SVG')+'</div>'
    logos += f'<div class="alfred-do-dont"><figure>{image("logos/alfred-logo-ink.svg","Correct logo proportions")}<figcaption><strong>Keep it intact.</strong> Original proportions and generous clear space.</figcaption></figure><figure>{image("logos/alfred-logo-ink.svg","Incorrect example: stretched logo","alfred-stretched")}<figcaption><strong>Avoid stretching.</strong> Distortion changes the mark’s character.</figcaption></figure></div>'
    colour = '<div class="alfred-colour-proportion" aria-label="Recommended visual balance: predominantly paper and sand, some ink, a small yellow accent"><span>Paper</span><span>Sand</span><span>Ink</span><span aria-label="Small yellow accent"></span></div><div class="alfred-colour-list">'
    names={'ink':'Ink · text and outlines','ink2':'Secondary ink · supporting text','paper':'Paper · main canvas','sand':'Sand · grouped surfaces','accent':'Yellow · purposeful accent','line':'Helper line · ink at 18%'}
    for key, name in names.items():
        colour += f'<div class="alfred-colour-row"><span class="alfred-swatch" style="--alfred-chip:{color[key]}" aria-hidden="true"></span><span>{name}</span><span class="alfred-value">{color[key]}</span>{copy(color[key], "Copy "+key)}</div>'
    colour += '</div><div class="alfred-pairings"><p>Ink on paper <strong>10.5:1</strong></p><p>Secondary ink on sand <strong>4.6:1</strong></p><p>Ink on yellow <strong>6.2:1</strong></p></div><div class="alfred-yellow-comparison"><div><div class="alfred-mini-layout"><span></span><span></span><b></b></div><strong>Give yellow a job.</strong><p>A small action against a neutral canvas.</p></div><div><div class="alfred-mini-layout alfred-excessive"><span></span><span></span><b></b></div><strong>Avoid a yellow takeover.</strong><p>Whole yellow sections bury the hierarchy.</p></div></div>'
    type_demo = '''<div class="alfred-type-lab"><label for="alfred-sample">Try your own words</label><textarea id="alfred-sample" rows="2" maxlength="240" aria-describedby="alfred-type-help">A little less to think about.</textarea><p id="alfred-type-help" class="alfred-caption">Latin headings: Instrument Serif. Cyrillic headings: Cormorant Garamond. Cyrillic body: your system font.</p><div class="alfred-live-type"><p class="alfred-type-caption">Instrument Serif · heading</p><p class="alfred-type-h2" data-alfred-sample-heading>A little less to think about.</p><p class="alfred-type-caption">Outfit · body and controls</p><p class="alfred-type-body" data-alfred-sample-body>A little less to think about.</p></div></div><div class="alfred-type-scale"><div><span class="alfred-type-h1">Aa</span><span>40–76px<br>Display · 1.08</span></div><div><span class="alfred-type-h2">Aa</span><span>36–44px<br>Section · 1.08</span></div><div><span class="alfred-type-body">Aa</span><span>16px<br>Body · 1.6</span></div><div><span class="alfred-type-caption">Aa</span><span>15px<br>Caption · 1.4</span></div></div>'''
    shape_tokens = identity['shape']
    spacing = identity['spacing']['roles']
    section_bottom = spacing['sectionBottom']
    spec = (f"{shape_tokens['borderPx']}px solid {color['ink']}; "
            f"cards {shape_tokens['cardRadiusPx']}px; capsules {shape_tokens['capsuleRadiusPx']}px; "
            f"pills {shape_tokens['pillRadiusPx']}px; "
            f"card padding {spacing['cardPaddingMin']}–{spacing['cardPaddingMax']}px; "
            f"related-card gap {spacing['cardGroupGap']}px; lot gap {spacing['lotGap']}px; "
            f"rail/content gap {spacing['railContentGap']}px; section top padding {spacing['sectionTop']}px; "
            f"section bottom padding clamp({section_bottom['min']}px, {section_bottom['fluid']}, {section_bottom['max']}px).")
    shape = '''<div class="alfred-geometry"><div class="alfred-capsule-demo">Capsule <span>36px corners</span></div><div class="alfred-spacing-demo"><div class="alfred-shape-card"><h5>A generous interior.</h5><p>24–32px padding keeps the content distinct from its outline.</p><span>28px corners · 1.5px outline</span></div><div class="alfred-space-measure"><span>14px related gap</span><span>56px between groups</span></div></div><div class="alfred-component-line">'''+copy(spec,'Copy geometry','alfred-primary')+'''<a href="#alfred-resources">Get exact tokens</a><span class="alfred-tag">A quiet label</span></div></div>'''
    voice = '<div class="alfred-voice-list">'
    for example in guidance['voiceExamples']:
        voice += f'<article class="alfred-voice-example"><h5>{E(example["context"])}</h5><blockquote>{E(example["use"])}</blockquote><p><strong>Instead of:</strong> {E(example["avoid"])}</p><p class="alfred-caption">{E(example["reason"])}</p></article>'
    voice += '</div>'
    applications = f'''<p class="alfred-caption">Illustrative applications · editorial recommendations</p><div class="alfred-application-report"><div class="alfred-report-bar">{image('logos/alfred-logo-ink.svg','Alfred report cover logo')}<span>Personal report</span></div><h5>A considered<br>point of view.</h5><p>What matters. What to compare.<br>What to do next.</p><div class="alfred-report-footer"><span>Prepared for your next decision</span><span>Illustrative cover</span></div></div><div class="alfred-applications-pair"><div class="alfred-presentation">{image('logos/alfred-icon-paper.svg','Alfred star on an ink presentation panel')}<h5>Find it.<br>Book it.<br>Buy it.</h5><p>A presentation panel.<br>One thought, given room.</p></div><div class="alfred-note"><h5>A note from Alfred.</h5><p>Your next move starts with a message.</p><p>Keep the invitation short. Let a clear next step do the work.</p><span>Communication example</span></div></div>'''
    resources = f'<div class="alfred-resource-list"><div><a class="alfred-download" href="assets/downloads/alfred-brand.zip" download>Complete Alfred skill · ZIP<span aria-hidden="true">↓</span></a><p>Includes instructions, exact tokens, logos, both illustrations, fonts and licences.</p></div><div><a class="alfred-download" href="{E(AGENT_SKILL_URL)}">Open the agent skill</a><p>Use $alfred-brand in a supporting agent, or ask it to read this entrypoint.</p></div><div><a class="alfred-download" href="https://raw.githubusercontent.com/nonprophet-max/persistent-labs-design-system/codex/design-bible/plugins/alfred-brand/chatbot.md">Open the plain chatbot guide</a><p>Attach or paste the guide into a chat. Text guidance works without installation.</p></div>'
    for file, title, detail in [('brand-guide.md','Current brand guide','Readable Markdown for people and AI tools.'),('tokens.json','Exact tokens · JSON','Canonical palette, type, shape and spacing.'),('tokens.css','Scoped tokens · CSS','Use inside data-product="alfred".'),('fonts.css','Local font declarations','Keep the fonts folder beside this file.'),('illustrations/hero-mascot-light-bg.png','Butler · light ground','Supplied PNG; use on paper.'),('illustrations/hero-mascot-dark-bg.png','Butler · dark ground','Supplied PNG with opaque paper details.'),('ASSETS-LICENCES.md','Asset rights and font licences','Read before reusing or distributing assets.'),('provenance.json','Asset provenance','Original source paths and byte hashes.')]:
        resources += f'<div>{download(file,title)}<p>{E(detail)}</p></div>'
    resources += '</div><div class="alfred-ai-handoff"><h5>A useful starting prompt</h5><p id="alfred-prompt">Read the Alfred brand guide and use the supplied assets. Apply the current colours, Instrument Serif headings, Outfit body text and restrained yellow. Keep Alfred styles scoped to its material. Label illustrative applications and do not invent product claims.</p>'+copy('Read the Alfred brand guide and use the supplied assets. Apply the current colours, Instrument Serif headings, Outfit body text and restrained yellow. Keep Alfred styles scoped to its material. Label illustrative applications and do not invent product claims.','Copy starting prompt')+'</div>'
    body = hero + nav + section('logos',logos) + section('colour',colour) + section('type',type_demo) + section('shape',shape) + section('voice',voice) + section('applications',applications) + section('resources',resources)
    return '<section class="section product-section alfred-chapter" id="alfred" data-product="alfred">'+body+'<div class="alfred-feedback" role="status" aria-live="polite" data-alfred-status></div><div class="alfred-copy-fallback" hidden><label for="alfred-copy-text">Copy manually: select the text below.</label><textarea id="alfred-copy-text" readonly rows="3"></textarea><button type="button" data-alfred-close-copy>Close copy text</button></div></section>'
