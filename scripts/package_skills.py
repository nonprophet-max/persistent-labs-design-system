#!/usr/bin/env python3
"""Generate six self-contained, provider-neutral brand skill plugins."""
from pathlib import Path
from html.parser import HTMLParser
import json
import re
import shutil
import runpy
import zipfile

ROOT=Path(__file__).resolve().parents[1]
bible=runpy.run_path(str(ROOT/'scripts/build.py'))
T=bible['T']; PRODUCTS=bible['PRODUCTS']; SECTIONS=bible['SECTIONS']

class Markdown(HTMLParser):
    def __init__(self):
        super().__init__();self.parts=[];self.skip=0;self.link=None;self.row=[];self.cell=None;self.header=False
    def emit(self,s):
        if self.cell is not None:self.cell.append(s)
        else:self.parts.append(s)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag in ('svg','script','style'):self.skip+=1
        if self.skip:return
        if tag in ('h1','h2','h3','h4'):self.emit('\n\n'+'#'*int(tag[1])+' ')
        elif tag in ('p','div','section','article','details','summary','dl'):self.emit('\n\n')
        elif tag in ('b','strong'):self.emit('**')
        elif tag=='br':self.emit('\n')
        elif tag=='li':self.emit('\n- ')
        elif tag=='dt':self.emit('\n- **')
        elif tag=='dd':self.emit(': ')
        elif tag=='a':
            self.link=a.get('href','')
            if self.link.startswith('http'):self.emit('[')
        elif tag=='tr':self.row=[];self.header=False
        elif tag in ('td','th'):self.cell=[];self.header=self.header or tag=='th'
        elif tag=='pre':self.emit('\n\n```css\n')
    def handle_startendtag(self,tag,attrs):
        if tag=='br' and not self.skip:self.emit('\n')
    def handle_endtag(self,tag):
        if tag in ('svg','script','style'):
            self.skip=max(0,self.skip-1);return
        if self.skip:return
        if tag in ('b','strong'):self.emit('**')
        elif tag=='dt':self.emit('**')
        elif tag=='a':
            if self.link and self.link.startswith('http'):self.emit(']('+self.link+')')
            self.link=None
        elif tag in ('td','th'):
            self.row.append(re.sub(r'\s+',' ',''.join(self.cell or [])).replace('|','\\|').strip());self.cell=None
        elif tag=='tr':
            self.emit('\n| '+' | '.join(self.row)+' |')
            if self.header:self.emit('\n| '+' | '.join('---' for _ in self.row)+' |')
        elif tag=='pre':self.emit('\n```\n')
        elif tag in ('p','section','article','h1','h2','h3','h4','table'):self.emit('\n\n')
    def handle_data(self,data):
        if not self.skip:self.emit(data)
    def output(self):return re.sub(r'\n[ \t]*\n(?:[ \t]*\n)+','\n\n',''.join(self.parts)).strip()+'\n'

def md(fragment):
    p=Markdown();p.feed(fragment);return p.output()

def write(path,text):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text)
def dump(path,value):write(path,json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def copy(src,dst):dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)

foundations='# Persistent Labs shared foundations\n\nEdition '+T['version']+'. Product-specific exceptions take precedence inside their own product surfaces.\n\n'+ '\n'.join(md(s[4]) for s in SECTIONS if s[3]=='Foundations')
complete='# Persistent Labs full design bible\n\nEdition '+T['version']+' · 23 September 2026.\n\n'+'\n'.join(md(s[4]) for s in SECTIONS)
# Local archive links in the reading page are provenance, not portable skill dependencies.
complete+='\n## Portable-package provenance\n\nReferences above to original archives, review rounds and workflow guides describe records in the private source repository. They are historical context, not bundled dependencies or instructions to locate missing files. Applying this skill requires only the included references, tokens and assets. Current browser rendering remains unverified; do not inherit historical passes as proof for a new deliverable.\n'
foundations+='\n## Portable-package provenance\n\nMentions of the source archive are provenance only. The original archive remains in the private source repository and is not required to apply these shared foundations.\n'
common='''## Apply the identity

Use this guidance for the requested brand and deliverable. Follow explicit owner directions when they override a proposed treatment, and record the change instead of silently mixing rules. Preserve the brief’s format and audience.

Read the brand reference and shared foundations, then choose the surface (marketing, product UI, documents or presentation). Use the supplied tokens and assets; do not improvise replacements for established marks. Keep each product’s color, typography, geometry and voice distinct. For a narrow copy task, load only the relevant voice and positioning guidance.

Use the maker endorsement “by Persistent Labs” quietly and separately. State illustrative data as illustrative. Design does not establish technical capabilities, availability, privacy, security or compliance guarantees. Keep observations, owner directions and proposals distinct.

For visual work, check the actual output at its intended dimensions, including narrow screens when applicable. Check the real foreground/background pairs and interaction states; bright product actions use their specified on-accent text. Keep controls at least 44px and honor reduced motion. If rendering is unavailable, say which checks were not performed.

Deliver the requested artifact and briefly explain any meaningful deviations, unresolved brand decisions or verification limits. This skill does not authorize publication, deployment, purchase or account changes.
'''
products_by_id={p['id']:p for p in PRODUCTS}
entries=[('persistent-labs-brand','Persistent Labs',None)]+[(p['id']+'-brand',p['name'],p) for p in PRODUCTS]
catalog=[]
for plugin_name,label,p in entries:
    plugin=ROOT/'plugins'/plugin_name
    skill=plugin/'skills'/plugin_name
    skill.mkdir(parents=True,exist_ok=True)
    is_parent=p is None
    desc=('Create and review work using the full Persistent Labs design bible and its five product identities. Use for parent-brand or multi-product work; use the individual product skill for work confined to one product.' if is_parent else f'Create and review {label} branded interfaces, pages, copy and collateral using its identity specifications. Use for {label} work, not unrelated brands.')
    if p and p['id']=='fireflow':desc+=' Includes the FireFlow orchestration engine, MemoryTree and FlameChorus as parts of one product.'
    manifest={
      'name':plugin_name,'version':'2.3.0','description':desc,'author':{'name':'Persistent Labs'},'skills':'./skills/',
      'interface':{'displayName':label+' Brand','shortDescription':('Full design bible and five product identities' if is_parent else label+' identity, assets and design guidance'),'longDescription':desc,'developerName':'Persistent Labs','category':'Productivity','capabilities':[],'defaultPrompt':'Use $'+plugin_name+' for this design brief.','brandColor':T['core']['gold'] if is_parent else T['products'][p['id']]['accent']}
    }
    dump(plugin/'.codex-plugin/plugin.json',manifest)
    # Claude-compatible packaging is supplemental; the skill itself is plain Markdown.
    dump(plugin/'.claude-plugin/plugin.json',{k:manifest[k] for k in ('name','version','description','author','skills')})
    write(skill/'agents/openai.yaml', 'interface:\n  display_name: '+json.dumps(label+' Brand')+'\n  short_description: '+json.dumps(manifest['interface']['shortDescription'])+'\n  default_prompt: '+json.dumps('Use $'+plugin_name+' to apply the '+label+' brand to this task.')+'\n')
    refs='''## References and assets

- [Shared foundations](references/foundations.md): parent identity, contrast, typography, spacing, shape, components and motion.
- [Token values](references/design-tokens.json) and [CSS variables](assets/tokens.css): exact values and scoped usage.
- [Asset inventory](references/assets.md): available vector files and font provenance.
'''
    if is_parent:
        route='''## Choose the scope

For parent-brand and portfolio work, read [the full design bible](references/design-bible.md). For a single product, read its own reference below plus the relevant shared foundations; do not merge identities into a generic gold brand.

'''+ '\n'.join(f'- [{q["name"]}](references/{q["id"]}.md): {q["role"]}.' for q in PRODUCTS)+'''

The portfolio is FireFlow, Unfazed.dev, Lanni, PrivateInference and Galactica. FireFlow contains its orchestration engine, MemoryTree (persistent memory) and FlameChorus (chat UX engine). Never promote those components into peer product brands. Lanni is built on FireFlow. Galactica is live; PrivateInference is upcoming. Their shared portfolio does not imply shared technical architecture.
'''
        write(skill/'references/design-bible.md',complete)
        for q in PRODUCTS:write(skill/f'references/{q["id"]}.md',md(next(s[4] for s in SECTIONS if s[0]==q['id'])))
        selected=T
        asset_names=['persistent-labs','fireflow','memorytree','unfazed','lanni','privateinference','galactica']
        body=route+'\n'+common+'\n'+refs
    else:
        chapter=md(next(s[4] for s in SECTIONS if s[0]==p['id']))
        write(skill/'references/brand.md',chapter)
        selected={k:v for k,v in T.items() if k not in ('products','components')}
        selected['products']={p['id']:T['products'][p['id']]}
        selected['components']={'fireflow':T['components']['fireflow']} if p['id']=='fireflow' else {}
        asset_names=['persistent-labs',p['id']]+(['memorytree'] if p['id']=='fireflow' else [])
        invariant={
          'fireflow':'FireFlow is one product with three core parts: its orchestration engine, MemoryTree for persistent memory and FlameChorus for chat UX. Component accents are subordinate; primary actions stay FireFlow orange. Do not create separate MemoryTree or FlameChorus product brands.',
          'unfazed':'Preserve the unimpressed face, lowercase unfazed wordmark, white ground, system typography, blue accent and 6px corners. Use Unfazed.dev in the portfolio. Do not impose parent gold, pill controls or Red Hat inside Unfazed’s interface.',
          'lanni':'Lanni is built on FireFlow. Preserve coral and the human, clear voice. The L-shaped mark is a proposed extension, and current availability is unverified. Keep proposed actions, review, execution and completion distinguishable.',
          'privateinference':'PrivateInference is upcoming. Its abbreviation is PI and its symbol is the supplied bold vector π, not a font glyph or improvised P/I monogram. Lavender and positioning remain proposals. Do not invent deployment, retention, encryption or locality guarantees.',
          'galactica':'Galactica is live and operates as a privacy technology firm across AI and blockchain. Use the full Galactica.com lockup with the bold orange dot #F7931A. The outlined supplied lockup follows owner direction; copper UI colors are proposed family adaptations. Keep Galactica distinct from upcoming PI and do not infer specific AI or privacy capabilities.'
        }[p['id']]
        body='## Brand essentials\n\n'+invariant+'\n\nRead [the product identity](references/brand.md) for positioning, logo, palette, typography, geometry, motion, voice and component behavior.\n\n'+common+'\n'+refs
    skill_text='---\nname: '+plugin_name+'\ndescription: '+json.dumps(desc,ensure_ascii=False)+'\n---\n\n# '+label+' brand\n\n'+body
    write(skill/'SKILL.md',skill_text)
    write(skill/'references/foundations.md',foundations)
    dump(skill/'references/design-tokens.json',selected)
    # Scope product variables to the selected product; keep shared semantic rules.
    css=(ROOT/'tokens/persistent-labs.tokens.css').read_text()
    if not is_parent:
        for other in T['products']:
            if other!=p['id']:css=re.sub(r'\[data-product="'+other+r'"\][^{]*\{[^}]*\}\n?','',css)
    write(skill/'assets/tokens.css',css)
    for name in asset_names:copy(ROOT/f'assets/{name}.svg',skill/f'assets/{name}.svg')
    for font in (ROOT/'assets/fonts').iterdir():
        if font.is_file():copy(font,skill/'assets/fonts'/font.name)
    write(skill/'assets/fonts.css',re.sub(r'/\*.*?\*/', '/* Link this stylesheet from your page. Keep the adjacent fonts/ directory; rebase URLs if inlining. */', (ROOT/'src/fonts.css').read_text(), count=1, flags=re.S).replace('assets/fonts/','fonts/'))
    font_sources=(ROOT/'assets/fonts/SOURCES.md').read_text()
    start=font_sources.index('The weight ranges')
    end=font_sources.index('| File |')
    font_sources=font_sources[:start]+'Load the bundled families by linking assets/fonts.css. Its URLs resolve relative to that stylesheet and its adjacent fonts/ directory. If you inline the CSS into a document, rebase the font URLs to that document. No project build script is required.\n\n'+font_sources[end:]
    write(skill/'assets/fonts/SOURCES.md',font_sources)
    inventory='# Assets and provenance\n\n'+ '\n'.join(f'- [{name}.svg](../assets/{name}.svg)' for name in asset_names)+'''

Use SVG assets directly, preserving their viewBox and proportions. Assets with currentColor inherit the chosen approved foreground when inlined; external SVG images use their own foreground. The Galactica.com dot is a fixed orange circle and remains orange in full-color lockups. Do not replace PI’s vector π with a font character.

The Persistent Labs ribbon and Unfazed face are retained source marks. FireFlow and Lanni marks and the MemoryTree component icon are proposed. The Galactica.com wordmark is an owner-directed family adaptation, outlined from Red Hat Display 700; it is not an extracted website master.

Red Hat Display, Text and Mono are bundled with their SIL Open Font Licenses in assets/fonts. Include assets/fonts.css when using these webfonts. Unfazed uses system typography as its product exception. The brand marks and design bible are proprietary; the font licenses do not grant rights to the brand identities.
'''
    write(skill/'references/assets.md',inventory)
    # This portable document can be attached/pasted without a plugin runtime.
    chatbot=skill_text+'\n\n---\n\n'+(complete if is_parent else (skill/'references/brand.md').read_text()+'\n'+foundations)+'\n\n## Machine-readable tokens\n\n```json\n'+json.dumps(selected,indent=2)+'\n```\n'
    write(plugin/'chatbot.md',chatbot)
    catalog.append({'name':plugin_name,'product':label,'skill':f'plugins/{plugin_name}/skills/{plugin_name}/SKILL.md','chatbot':f'plugins/{plugin_name}/chatbot.md','plugin':f'plugins/{plugin_name}'})

dump(ROOT/'brand-skills.json',{'version':'2.3.0','plugins':catalog})
# A repository-local Claude catalog; no local app configuration is changed.
dump(ROOT/'.claude-plugin/marketplace.json',{'name':'persistent-labs-brands','owner':{'name':'Persistent Labs'},'plugins':[{'name':c['name'],'source':'./'+c['plugin'],'description':'Brand guidance for '+c['product']} for c in catalog]})
write(ROOT/'BRAND-SKILLS.md','''# Portable brand skills

One full-system skill and five independent product plugins. Each product package contains its own references, tokens, vector assets and fonts; it does not depend on installing the parent package.

| Brand | Invoke | Skill entrypoint | Chatbot document |
| --- | --- | --- | --- |
'''+ '\n'.join(f'| {c["product"]} | `${c["name"]}` | [SKILL.md]({c["skill"]}) | [chatbot.md]({c["chatbot"]}) |' for c in catalog)+'''

## Use with an agent

Copy the desired `plugins/<name>/skills/<name>/` directory into the agent’s supported skill directory, or point it directly to that SKILL.md. Hosts with skill discovery can select by the frontmatter description; explicit invocation uses the names above. Host setup varies, so no universal automatic installation is implied. In Claude Code, installed plugin skills use the host’s slash-command namespace (for example `/fireflow-brand:fireflow-brand`); the `$` notation above is for agents that support it.

Each plugin also includes `.codex-plugin/plugin.json` and `.claude-plugin/plugin.json`. Use the host’s supported local/private-repository plugin installation flow. The repository-level Claude marketplace catalog lists all six plugins. None has been silently installed into an account or local app. Packaging follows [Claude Code’s plugin reference](https://code.claude.com/docs/en/plugins-reference) and the bundled Codex plugin manifest schema.

## Use with a chatbot

Attach or paste the desired `chatbot.md` and give the actual task. It combines instructions, detailed brand rules and tokens in plain Markdown/JSON. If the chatbot can use files, also attach the plugin ZIP or the SVG/font files required by the deliverable. A text-only chatbot can follow the writing and specification guidance but cannot render or validate files without suitable tools.

## Rebuild and validate

Run `python3 scripts/package_skills.py` after changing the bible sources, then `python3 scripts/check_skills.py`. The packaging process derives references and tokens from the same sources as the web bible. Preserve owner decisions and product exceptions when extending the system.

The GitHub repository is intended to remain private. Publishing the reading website does not publish this repository or its plugin catalog.
''')
print('Packaged six independent brand skill plugins and chatbot documents.')
