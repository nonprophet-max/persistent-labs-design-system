#!/usr/bin/env python3
"""Validate standalone brand packages and source consistency without dependencies."""
from pathlib import Path
import json,re,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
catalog=json.loads((ROOT/'brand-skills.json').read_text())['plugins']
source=json.loads((ROOT/'tokens/design-tokens.json').read_text())
expected=['persistent-labs-brand','fireflow-brand','unfazed-brand','lanni-brand','privateinference-brand','galactica-brand','alfred-brand']
assert [p['name'] for p in catalog]==expected
checks=0
for item in catalog:
    plugin=ROOT/item['plugin'];skill=(ROOT/item['skill']).parent
    manifest=json.loads((plugin/'.codex-plugin/plugin.json').read_text())
    assert manifest['name']==plugin.name and manifest['version']=='2.4.0'
    entry=(skill/'SKILL.md').read_text()
    assert entry.startswith('---\nname: '+plugin.name+'\n')
    frontmatter=entry.split('\n---\n',1)[0].removeprefix('---\n').splitlines()
    assert len(frontmatter)==2 and frontmatter[1].startswith('description: ')
    description=json.loads(frontmatter[1].removeprefix('description: '))
    assert isinstance(description,str) and 0<len(description)<=1024
    assert '<' not in description and '>' not in description and '[TODO:' not in description
    assert json.loads((plugin/'.claude-plugin/plugin.json').read_text())['name']==plugin.name
    tokens=json.loads((skill/'references/design-tokens.json').read_text())
    assert tokens['core']==source['core'] and tokens['type']==source['type']
    ids=list(source['products']) if plugin.name=='persistent-labs-brand' else [plugin.name.removesuffix('-brand')]
    assert list(tokens['products'])==ids
    for id in ids:assert tokens['products'][id]==source['products'][id]
    for p in skill.rglob('*.md'):
        for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
            if link.startswith(('https://','http://','#')):continue
            target=(p.parent/link.split('#')[0]).resolve()
            assert target.is_relative_to(plugin.resolve()),(p,link,'outside standalone plugin')
            assert target.exists(),(p,link,'missing')
    for p in skill.rglob('*.svg'):ET.parse(p)
    for link in re.findall(r'url\([\'"]?([^\)\'\"]+)',(skill/'assets/fonts.css').read_text()):
        assert (skill/'assets'/link).is_file()
    if plugin.name!='alfred-brand':
        assert all((skill/'assets/fonts'/f'OFL-Red-Hat-{f}.txt').exists() for f in ('Display','Text','Mono'))
    if plugin.name in ('alfred-brand','persistent-labs-brand'):
        assert tokens['identities']['alfred']==source['identities']['alfred']
        for path in (ROOT/'assets/alfred').rglob('*'):
            if path.is_file():assert (skill/'assets/alfred'/path.relative_to(ROOT/'assets/alfred')).read_bytes()==path.read_bytes()
    else:
        assert not (skill/'assets/alfred').exists(),plugin.name
    assert len((plugin/'chatbot.md').read_text())>5000
    checks+=1
for name in ('persistent-labs-brand','galactica-brand'):
    svg=ROOT/f'plugins/{name}/skills/{name}/assets/galactica.svg'
    tree=ET.parse(svg);dot=tree.find('.//{http://www.w3.org/2000/svg}circle')
    assert tree.getroot().get('aria-label')=='Galactica.com' and dot.get('fill')=='#F7931A'
for name in ('persistent-labs-brand','privateinference-brand'):
    skill=ROOT/f'plugins/{name}/skills/{name}'
    assert (skill/'assets/pi/brand-identity.pdf').read_bytes()==(ROOT/'assets/pi/brand-identity.pdf').read_bytes()
    assert (skill/'assets/privateinference.svg').read_bytes()==(ROOT/'assets/pi/mark.svg').read_bytes()
    for weight in range(100,900,100):assert (skill/f'assets/fonts/poppins-latin-{weight}.woff2').is_file()
    assert (skill/'assets/fonts/OFL-Poppins.txt').is_file()
    for asset in ('horizontal','vertical','logotype','horizontal-dark','horizontal-reversed'):
        assert (skill/f'assets/pi/{asset}.svg').read_bytes()==(ROOT/f'assets/pi/{asset}.svg').read_bytes()
print(f'Passed: {checks} self-contained plugins, scoped tokens, references, SVGs, font assets and chatbot documents.')
