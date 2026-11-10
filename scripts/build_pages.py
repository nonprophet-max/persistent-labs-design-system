#!/usr/bin/env python3
"""Build a separate, public multipage edition from the canonical bible content."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote, urljoin, urlunparse
import html
import json
import os
import re
import runpy
import shutil

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'dist-pages'


def normalized_base_path(value):
    """Accept an empty/root path or plain absolute path without ambiguous URL syntax."""
    if value in ('', '/'):
        return ''
    if not re.fullmatch(r'/(?:[A-Za-z0-9_-]+/)*[A-Za-z0-9_-]+/?', value):
        raise ValueError('SITE_BASE_PATH must be empty, /, or an absolute path such as /persistent-labs-design-system')
    return value.rstrip('/')


def site_url(ref, base_path, current='/'):
    """Make a local URL deployment-absolute; preserve fragments and external URLs."""
    url = urlparse(ref)
    if not ref or ref.startswith('#') or url.scheme or url.netloc:
        return ref
    path = urljoin(current, url.path) if url.path else current
    if base_path and (path == base_path or path.startswith(base_path + '/')):
        deployed = path
    else:
        deployed = base_path + path
    return urlunparse(('', '', deployed, url.params, url.query, url.fragment))


def rebase_css(content, base_path):
    def replace(match):
        ref = match.group(2)
        return 'url(' + match.group(1) + site_url(ref, base_path) + match.group(1) + ')'
    return re.sub(r"url\(\s*(['\"]?)([^)\"'\s]+)\1\s*\)", replace, content)


def rebase_html(content, base_path, current):
    def replace(match):
        ref = html.unescape(match.group(3))
        return match.group(1) + match.group(2) + html.escape(site_url(ref, base_path, current), quote=True) + match.group(2)
    content = re.sub(r"(?<![\w:-])((?:href|src|poster|action|xlink:href)=)(['\"])(.*?)\2", replace, content, flags=re.S)
    # Inline specimen backgrounds follow the same asset rules as the shared stylesheet.
    return rebase_css(content, base_path)


def undeployed_path(path, base_path):
    if not base_path:
        return path
    if path == base_path:
        return '/'
    assert path.startswith(base_path + '/'), ('URL escapes SITE_BASE_PATH', path)
    return path[len(base_path):]


def build():
    # Validate before running the canonical builder or removing an existing output.
    base_path = normalized_base_path(os.environ.get('SITE_BASE_PATH', ''))
    source = runpy.run_path(str(ROOT / 'scripts/build.py'))
    sections = source['SECTIONS']
    products = source['PRODUCTS']
    E = html.escape
    TOP = [('foundations', 'Foundations'), ('products', 'Products'), ('tokens', 'Tokens'), ('guidelines', 'Guidelines')]
    PRODUCT_IDS = [p['id'] for p in products]
    BRAND_SKILLS = json.loads((ROOT / 'brand-skills.json').read_text())['plugins']
    REPOSITORY = 'https://github.com/nonprophet-max/persistent-labs-design-system'
    RAW_REPOSITORY = 'https://raw.githubusercontent.com/nonprophet-max/persistent-labs-design-system/codex/design-bible'
    foundation_ids = [s[0] for s in sections if s[3] == 'Foundations' and s[0] != 'brand']
    routes = {'/': {'title': 'Design bible', 'ids': []},
              '/foundations/': {'title': 'Foundations', 'ids': foundation_ids},
              '/products/': {'title': 'Products', 'ids': ['brand']},
              '/tokens/': {'title': 'Tokens', 'ids': ['tokens']},
              '/guidelines/': {'title': 'Guidelines', 'ids': ['decisions']}}
    for product in products:
        routes[f'/products/{product["id"]}/'] = {'title': product['name'], 'ids': [product['id']]}
    section_routes = {id: route for route, page in routes.items() for id in page['ids']}
    id_routes = {}
    for id, _, _, _, content in sections:
        for anchor in re.findall(r'\bid="([^"]+)"', content):
            id_routes[anchor] = section_routes[id]


    def public_content(content, current):
        content = re.sub(r'<a\b[^>]*href="(?:reviews|reference|docs)/[^"]*"[^>]*>(.*?)</a>', r'\1', content, flags=re.S)
        content = content.replace('reference/original-design-bible.html', 'the source archive')
        content = re.sub(r'((?:href|src)=")((?:assets|tokens)/[^\"]+)', r'\1/\2', content)

        def link(match):
            anchor = match.group(1)
            if anchor == 'main':
                return match.group(0)
            target = id_routes[anchor]
            # Chapter entry links lead to the actual page; nested specifications keep anchors.
            if anchor in PRODUCT_IDS or anchor in ('brand', 'tokens', 'decisions'):
                return f'href="{target}"'
            return f'href="{("" if target == current else target)}#{anchor}"'

        return re.sub(r'href="#([^"]+)"', link, content)


    def navigation(current):
        nav = [f'<a class="nav-link" href="/"{active(current, "/")}>Overview</a>']
        last_group = None
        for id, title, num, group, _ in sections:
            if group != last_group:
                nav.append(f'<div class="nav-group">{group}</div>')
                last_group = group
            short = {'principles':'Principles', 'brand':'Portfolio architecture', 'logo':'Parent identity',
                     'color':'Color & contrast', 'type':'Typography', 'layout':'Layout & grid',
                     'spacing':'Spacing', 'shape':'Shape & effects', 'components':'Components',
                     'motion':'Motion & imagery', 'voice':'Voice & surfaces',
                     'decisions':'Review & decisions', 'tokens':'Token library'}.get(id, title)
            route = section_routes[id]
            href = route + ('#' + id if id in foundation_ids else '')
            dot = f'<span class="dot" style="--dot:{source["T"]["products"][id]["accent-ink"]}" aria-hidden="true"></span>' if id in PRODUCT_IDS else f'<span class="num">{num}</span>'
            nav.append(f'<a class="nav-link" href="{href}"{active(current, route) if id not in foundation_ids else ""}>{dot}{E(short)}</a>')
        return ''.join(nav)


    def active(current, target):
        return ' aria-current="page"' if current == target else ''


    def skill_access(route):
        product_id = route.strip('/').split('/')[-1]
        name = f'{product_id}-brand' if product_id in PRODUCT_IDS else 'persistent-labs-brand'
        skill = next(item for item in BRAND_SKILLS if item['name'] == name)
        for key in ('skill', 'plugin', 'chatbot'):
            assert (ROOT / skill[key]).exists(), skill[key]

        def resource(key, label, description, url):
            id = f'brand-resource-{key}'
            return f'''<div class="skill-resource" data-resource="{key}">
    <div class="skill-resource-label"><strong>{label}</strong><span>{description}</span></div>
    <a class="skill-url" id="{id}" href="{E(url)}" target="_blank" rel="noopener">{E(url)}</a>
    <button class="utility" type="button" data-copy-link="{id}" aria-label="Copy {label} link">Copy link</button></div>'''

        agent = resource('skill', 'Agent skill', 'Give this link to your AI coding agent.', f'{RAW_REPOSITORY}/{skill["skill"]}')
        plugin = resource('plugin', 'Full plugin', 'Includes instructions, references, logos and fonts.', f'{REPOSITORY}/tree/codex/design-bible/{skill["plugin"]}')
        chatbot = resource('chatbot', 'Chatbot guide', 'Open, then paste or attach the Markdown to your chat.', f'{RAW_REPOSITORY}/{skill["chatbot"]}')
        return f'''<aside class="skill-access" aria-label="{E(skill['product'])} AI brand resources" data-brand-skill="{name}">
    <div class="skill-access-title"><span class="skill-access-kicker">Build with AI</span><strong>{E(skill['product'])}</strong></div>
    {agent}<details class="skill-more"><summary>Plugin &amp; chatbot links</summary>{plugin}{chatbot}
    <p>Use the full plugin for work that needs brand assets. Installation depends on your AI tool.</p></details></aside>'''


    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    for folder in ('assets', 'tokens'):
        shutil.copytree(ROOT / folder, OUT / folder)
    styles = source['styles']
    # Preserve the canonical visual hierarchy when a chapter becomes a page.
    styles = re.sub(r'(?<![\w-])h([2-6])\b', lambda match: f':is(h{match[1]},[data-heading-level="{match[1]}"])', styles)
    styles += '\n' + (ROOT / 'src/pages.css').read_text()
    (OUT / 'assets/site.css').write_text(rebase_css(styles, base_path))
    shutil.copy2(ROOT / 'src/pages.js', OUT / 'assets/site.js')
    alfred_script = ROOT / 'src/alfred.js'
    if alfred_script.is_file():
        shutil.copy2(alfred_script, OUT / 'assets/alfred.js')
    cover = re.search(r'<header class="cover">.*?</header>', source['document'], re.S).group(0)
    for product in products:
        name = product['name']
        cover = re.sub(r'<span>(<i [^>]+></i>)' + re.escape(name) + r'</span>',
                       rf'<a href="/products/{product["id"]}/">\1{E(name)}</a>', cover)
    cards = [('foundations', '01', 'Foundations', 'The shared rules for identity, color, type, layout and interaction.'),
             ('products', '02', 'Products', f'{len(products)} distinct identities, with their marks, palettes and interface specimens.'),
             ('tokens', '03', 'Tokens', 'Copy or download the shared design tokens in CSS and JSON.'),
             ('guidelines', '04', 'Guidelines', 'Decisions, source boundaries and the release checklist.')]
    home_cards = '<section class="section"><div class="section-head"><div><div class="eyebrow">Explore the bible</div><h2>Find your starting point.</h2></div></div><div class="page-cards">' + ''.join(
        f'<a class="page-card" href="/{slug}/"><span class="eyebrow">{num}</span><h3>{title} <span aria-hidden="true">↗</span></h3><p>{copy}</p></a>' for slug, num, title, copy in cards) + '</div></section>'
    by_id = {s[0]: s[4] for s in sections}
    for route, page in routes.items():
        top = ''.join(f'<a href="/{slug}/"{active("/products/" if route.startswith("/products/") else route, "/"+slug+"/")}>{label}</a>' for slug, label in TOP)
        if route == '/':
            body = public_content(cover, route) + '<div class="content">' + skill_access(route) + home_cards
        else:
            crumbs = '<a href="/">Home</a><span aria-hidden="true">/</span>'
            if route.startswith('/products/') and route != '/products/':
                crumbs += '<a href="/products/">Products</a><span aria-hidden="true">/</span>'
            crumbs += f'<span aria-current="page">{E(page["title"])}</span>'
            content = ''.join(by_id[id] for id in page['ids'])
            if route == '/foundations/':
                content = '<header class="page-intro"><div class="eyebrow">The shared system</div><h1>Foundations.</h1><p>Identity, color, typography and interaction. The rules that hold the family together.</p></header>' + content
            else:
                def promote(match):
                    closing, level, attrs = match.groups()
                    return f'</h{int(level)-1}>' if closing else f'<h{int(level)-1} data-heading-level="{level}"{attrs}>'
                content = re.sub(r'<(/?)h([2-6])(\b[^>]*)>', promote, content)
            body = '<div class="content"><nav class="breadcrumbs" aria-label="Breadcrumb">' + crumbs + '</nav>' + skill_access(route) + public_content(content, route)
        footer = f'<footer class="footer"><span>Persistent Labs / Design system 2.4<br>One foundation. {len(products)} product identities.</span><a href="/">Back to overview ↗</a></footer></div>'
        document = f'''<!doctype html>
    <html lang="en" data-theme="light"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex, nofollow"><meta name="description" content="{E(page['title'])} — Persistent Labs design bible."><title>{E(page['title'])} — Persistent Labs</title><script>try{{document.documentElement.dataset.theme=localStorage.getItem('persistent-bible-theme')==='dark'?'dark':'light'}}catch{{}}</script><link rel="icon" href="/assets/persistent-labs.svg" type="image/svg+xml"><link rel="stylesheet" href="/assets/site.css"><script defer src="/assets/site.js"></script></head><body>
    <a class="skip" href="#main">Skip to content</a><header class="site-bar"><a class="home-link" href="/" aria-label="Persistent Labs design bible home">{source['logo']()}</a><nav class="quick-nav" aria-label="Main navigation">{top}</nav><button id="menu-toggle" type="button" aria-expanded="false" aria-controls="contents">Contents</button></header>
    <aside class="rail" id="contents"><div class="edition">Design bible / edition 02.4<br>9 October 2026</div><nav class="rail-nav" aria-label="Design bible contents">{navigation(route)}</nav><div class="rail-footer"><button class="theme-button" type="button" id="theme-toggle" aria-pressed="false">Switch to dark view</button></div></aside>
    <main class="page" id="main" tabindex="-1">{body}{footer}</main><div class="sr-only" id="live-status" role="status" aria-live="polite"></div><script type="application/json" id="token-json">{source['token_json']}</script></body></html>'''
        if route == '/products/alfred/' and alfred_script.is_file():
            document = document.replace('</head>', '<script defer src="/assets/alfred.js"></script></head>')
        document = rebase_html(document, base_path, route)
        target = OUT / route.strip('/') / 'index.html'
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(document)

    (OUT / '404.html').write_text(rebase_html('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found — Persistent Labs</title></head><body style="font:18px/1.6 system-ui;max-width:40rem;margin:10vh auto;padding:24px"><h1>Page not found.</h1><p><a href="/">Return to the design bible.</a></p></body></html>', base_path, '/404.html'))
    (OUT / 'robots.txt').write_text('User-agent: *\nDisallow: /\n')
    (OUT / '.nojekyll').write_text('')
    redirects = {}
    for component in ('memorytree', 'flamechorus'):
        route = f'/products/{component}/'
        destination = site_url(f'/products/fireflow/#{component}', base_path)
        redirects[route] = destination
        target = OUT / route.strip('/') / 'index.html'
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex, nofollow"><meta http-equiv="refresh" content="0;url={E(destination)}"><link rel="canonical" href="{E(destination)}"><title>Moved — FireFlow</title></head><body><h1>Part of FireFlow</h1><p><a href="{E(destination)}">Continue to FireFlow.</a></p></body></html>')


    class Page(HTMLParser):
        def __init__(self, content):
            super().__init__(); self.ids = []; self.refs = []; self.h1 = 0
            self.feed(content)

        def handle_starttag(self, tag, attrs):
            attrs = dict(attrs)
            if 'id' in attrs: self.ids.append(attrs['id'])
            if tag == 'h1': self.h1 += 1
            for key in ('href', 'src', 'poster', 'action', 'xlink:href'):
                if attrs.get(key): self.refs.append(attrs[key])


    parsed = {}
    for path in OUT.rglob('*.html'):
        relative = path.relative_to(OUT)
        route = '/' + relative.as_posix()
        if path.name == 'index.html':
            route = '/' if relative.parent == Path('.') else '/' + relative.parent.as_posix() + '/'
        parsed[route] = Page(path.read_text())

    def validate_ref(ref, current):
        url = urlparse(ref)
        if url.scheme or url.netloc:
            return
        # Resolve at the deployed URL, then strip exactly one deployment prefix.
        resolved = urlparse(urljoin(base_path + current, ref))
        target_route = unquote(undeployed_path(resolved.path, base_path))
        assert '..' not in Path(target_route).parts, (current, ref)
        if target_route in parsed:
            assert not resolved.fragment or unquote(resolved.fragment) in parsed[target_route].ids, (current, ref)
        else:
            target = (OUT / target_route.lstrip('/')).resolve()
            assert OUT.resolve() in target.parents and target.is_file(), (current, ref)
            assert not resolved.fragment or target.suffix == '.svg', (current, ref)

    for route, page in parsed.items():
        assert page.h1 == 1 and len(page.ids) == len(set(page.ids)), route
        for ref in page.refs:
            validate_ref(ref, route)
    for stylesheet in OUT.rglob('*.css'):
        for match in re.finditer(r"url\(\s*(['\"]?)([^)\"'\s]+)\1\s*\)", stylesheet.read_text()):
            validate_ref(match.group(2), '/' + str(stylesheet.relative_to(OUT)))
    assert sorted(id for page in routes.values() for id in page['ids']) == sorted(s[0] for s in sections)
    assert not any((OUT / name).exists() for name in ('.git', 'plugins', 'reviews', 'reference', 'src'))
    manifest = [{'path': path, 'url': site_url(path, base_path), **page} for path, page in routes.items()]
    (ROOT / 'build').mkdir(exist_ok=True)
    (ROOT / 'build/pages-manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    (ROOT / 'build/pages-validation.json').write_text(json.dumps({
        'base_path': base_path, 'pages': len(routes), 'chapters': len(sections),
        'redirects': redirects, 'html_files_validated': len(parsed),
        'files': sorted(str(path.relative_to(OUT)) for path in OUT.rglob('*') if path.is_file()),
        'local_links_fragments_css_and_exclusions': 'passed'
    }, indent=2)+'\n')
    print(f'Built {len(routes)} separate pages at {base_path or "/"}; all {len(sections)} chapters, local links, fragments, CSS assets and private-file exclusions verified.')


if __name__ == '__main__':
    build()
