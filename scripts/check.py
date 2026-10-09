#!/usr/bin/env python3
"""Check token contrast, asset references and offline font packaging."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote
import json
import re

ROOT=Path(__file__).resolve().parents[1]
tokens=json.loads((ROOT/'tokens/design-tokens.json').read_text())
failures=[]
checked=0
def luminance(color):
    values=[int(color[i:i+2],16)/255 for i in (1,3,5)]
    values=[v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in values]
    return sum(v*w for v,w in zip(values,(.2126,.7152,.0722)))
def check_pair(name,foreground,background,minimum=4.5):
    global checked
    a,b=sorted((luminance(foreground),luminance(background)))
    ratio=(b+.05)/(a+.05);checked+=1
    if ratio<minimum:failures.append(f'{name}: {ratio:.3f}:1 below {minimum}:1')

core=tokens['core']
for surface,background in [('dark',core['ink']),('dark',core['surface-dark']),('light',core['white']),('light',core['paper'])]:
    for role in ['','-secondary','-muted']:
        check_pair(surface+role,core['text-'+surface+role],background)
    for state in ['success','warning','danger','info']:
        check_pair(state+' '+surface,core[state+'-'+surface],background)
    check_pair('control '+surface,core['control-'+surface],background,3)
palettes=dict(tokens['products'])
for product,components in tokens['components'].items():
    palettes.update({product+'/'+name:values for name,values in components.items()})
for name,t in palettes.items():
    for state in ['accent','hover','pressed']:
        check_pair(name+' '+state,t['on-accent'],t[state])
    check_pair(name+' light accent',t['accent-ink'],core['white'])
    check_pair(name+' dark accent',t['accent'],core['ink'])
    check_pair(name+' tint',core['ink'],t['tint'])
for background in ['#2570CC','#1D5BA7','#174A89']:
    check_pair('Unfazed light button','#FFFFFF',background)
for state in ['gold','gold-hover','gold-pressed']:
    check_pair('Parent '+state,core['ink'],core[state])
check_pair('Gold ink on cream',core['gold-ink'],core['cream'])

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids=[]; self.anchors=[]; self.products=[]; self.nav=[]; self.portfolio=[]
        self.sections=[]; self.component_parents={}; self.headings=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        classes=a.get('class','').split()
        if 'id' in a:self.ids.append(a['id'])
        if tag=='section':
            self.sections.append(a.get('id'))
            if 'product-section' in classes:self.products.append(a.get('id'))
        if 'core-spec' in classes:self.component_parents[a.get('id')]=self.sections[-1] if self.sections else None
        if 'nav-link' in classes:self.nav.append(a.get('href'))
        if 'portfolio-row' in classes:self.portfolio.append(a.get('href'))
        if tag in ('h1','h2','h3','h4','h5','h6'):self.headings.append(int(tag[1]))
        for key,value in attrs:
            if key not in ('href','src') or not value:continue
            parsed=urlparse(value)
            if value.startswith('#'):self.anchors.append(unquote(value[1:]))
            if parsed.scheme or parsed.netloc or not parsed.path:continue
            path=(ROOT/unquote(parsed.path)).resolve()
            if not path.is_file():failures.append('Missing local reference: '+value)
    def handle_endtag(self,tag):
        if tag=='section' and self.sections:self.sections.pop()
document=(ROOT/'index.html').read_text()
structure=Links();structure.feed(document)
expected=['fireflow','unfazed','lanni','privateinference','galactica']
products=json.loads((ROOT/'src/products.json').read_text())
if [p['id'] for p in products]!=expected or structure.products!=expected:
    failures.append('Expected the five owner-defined product identities in order')
if list(tokens['products'])!=expected:failures.append('Product tokens do not match the portfolio')
if structure.portfolio!=['#'+p for p in expected]:failures.append('Portfolio links do not match the five products')
for p in expected:
    if structure.nav.count('#'+p)!=1:failures.append('Expected one product navigation link: '+p)
for component in ('orchestration-engine','memorytree','flamechorus'):
    if structure.component_parents.get(component)!='fireflow':failures.append('Core part must remain inside FireFlow: '+component)
    if '#'+component in structure.nav or '#'+component in structure.portfolio:
        failures.append('Core part must not appear as a peer product: '+component)
if len(structure.ids)!=len(set(structure.ids)):failures.append('Duplicate HTML IDs')
for anchor in structure.anchors:
    if anchor not in structure.ids:failures.append('Broken local anchor: #'+anchor)
if structure.headings.count(1)!=1:failures.append('Expected one h1')
if any(b>a+1 for a,b in zip(structure.headings,structure.headings[1:])):failures.append('Skipped heading level')
for path in re.findall(r'url\([\'"]?(assets/fonts/[^)\'\"]+)',document):
    if not (ROOT/path).is_file():failures.append('Missing font: '+path)
font_files=list((ROOT/'assets/fonts').glob('*.woff2'))
if len(font_files)!=11:failures.append('Expected three Red Hat files and eight Poppins weights')
for path in font_files:
    if path.read_bytes()[:4]!=b'wOF2':failures.append('Invalid WOFF2 magic: '+path.name)
if len(list((ROOT/'assets/fonts').glob('OFL*.txt')))!=4:failures.append('Expected four font licenses')
if not re.search(r'@font-face',document):failures.append('No local font declarations')
# Source colors stay exact; functional UI pairs use accessible source combinations.
pi=tokens['identities']['privateinference']
assert pi['palettes']['light']==['#FBD78E','#1E1E1E','#FFFFFF','#BFBFBF']
assert pi['palettes']['dark']==['#E5B14A','#F5F5F5','#1A1A1A','#7F7F7F']
check_pair('Pi light action','#1E1E1E','#FBD78E')
check_pair('Pi dark action','#1A1A1A','#E5B14A')
check_pair('Pi dark reading','#F5F5F5','#1A1A1A')
check_pair('Pi light reading','#1E1E1E','#FFFFFF')
for surface, values in pi['surfaces'].items():
    for role in ('text','text-secondary','text-muted'):check_pair('Pi '+surface+' '+role,values[role],values['surface'])
    for state in ('action','action-hover','action-pressed'):check_pair('Pi '+surface+' '+state,values['on-action'],values[state])
    check_pair('Pi '+surface+' control',values['control-border'],values['surface'],3)
    check_pair('Pi '+surface+' focus',values['focus'],values['surface'],3)
if (ROOT/'assets/privateinference.svg').read_bytes()!=(ROOT/'assets/pi/mark.svg').read_bytes():failures.append('Pi compatibility asset differs from source-extracted mark')
if failures:raise SystemExit('\n'.join(failures))
print(f'Passed: {checked} color pairs, five-product hierarchy, nested FireFlow core parts, anchors, headings, local references, Red Hat and Poppins offline fonts and licenses.')
