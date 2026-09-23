#!/usr/bin/env python3
"""Build a separate, public multipage edition from the canonical bible content."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote
import html
import json
import re
import runpy
import shutil

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'dist-pages'
source = runpy.run_path(str(ROOT / 'scripts/build.py'))
sections = source['SECTIONS']
products = source['PRODUCTS']
E = html.escape
TOP = [('foundations', 'Foundations'), ('products', 'Products'), ('tokens', 'Tokens'), ('guidelines', 'Guidelines')]
PRODUCT_IDS = [p['id'] for p in products]
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
    content = content.replace('reference/original-design-bible.html', 'the private source archive')
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


if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir()
for folder in ('assets', 'tokens'):
    shutil.copytree(ROOT / folder, OUT / folder)
styles = source['styles'].replace("url('assets/", "url('/assets/")
# Preserve the canonical visual hierarchy when a chapter becomes a page.
styles = re.sub(r'(?<![\w-])h([2-6])\b', lambda match: f':is(h{match[1]},[data-heading-level="{match[1]}"])', styles)
styles += '\n' + (ROOT / 'src/pages.css').read_text()
(OUT / 'assets/site.css').write_text(styles)
shutil.copy2(ROOT / 'src/pages.js', OUT / 'assets/site.js')
cover = re.search(r'<header class="cover">.*?</header>', source['document'], re.S).group(0)
for product in products:
    name = product['name']
    cover = re.sub(r'<span>(<i [^>]+></i>)' + re.escape(name) + r'</span>',
                   rf'<a href="/products/{product["id"]}/">\1{E(name)}</a>', cover)
cards = [('foundations', '01', 'Foundations', 'The shared rules for identity, color, type, layout and interaction.'),
         ('products', '02', 'Products', 'Five distinct identities, with their marks, palettes and interface specimens.'),
         ('tokens', '03', 'Tokens', 'Copy or download the shared design tokens in CSS and JSON.'),
         ('guidelines', '04', 'Guidelines', 'Decisions, source boundaries and the release checklist.')]
home_cards = '<section class="section"><div class="section-head"><div><div class="eyebrow">Explore the bible</div><h2>Find your starting point.</h2></div></div><div class="page-cards">' + ''.join(
    f'<a class="page-card" href="/{slug}/"><span class="eyebrow">{num}</span><h3>{title} <span aria-hidden="true">↗</span></h3><p>{copy}</p></a>' for slug, num, title, copy in cards) + '</div></section>'
by_id = {s[0]: s[4] for s in sections}
for route, page in routes.items():
    top = ''.join(f'<a href="/{slug}/"{active("/products/" if route.startswith("/products/") else route, "/"+slug+"/")}>{label}</a>' for slug, label in TOP)
    if route == '/':
        body = public_content(cover, route) + '<div class="content">' + home_cards
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
        body = '<div class="content"><nav class="breadcrumbs" aria-label="Breadcrumb">' + crumbs + '</nav>' + public_content(content, route)
    footer = '<footer class="footer"><span>Persistent Labs / Design system 2.3<br>One foundation. Five product identities.</span><a href="/">Back to overview ↗</a></footer></div>'
    document = f'''<!doctype html>
<html lang="en" data-theme="light"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex, nofollow"><meta name="description" content="{E(page['title'])} — Persistent Labs design bible."><title>{E(page['title'])} — Persistent Labs</title><script>try{{document.documentElement.dataset.theme=localStorage.getItem('persistent-bible-theme')==='dark'?'dark':'light'}}catch{{}}</script><link rel="icon" href="/assets/persistent-labs.svg" type="image/svg+xml"><link rel="stylesheet" href="/assets/site.css"><script defer src="/assets/site.js"></script></head><body>
<a class="skip" href="#main">Skip to content</a><header class="site-bar"><a class="home-link" href="/" aria-label="Persistent Labs design bible home">{source['logo']()}</a><nav class="quick-nav" aria-label="Main navigation">{top}</nav><button id="menu-toggle" type="button" aria-expanded="false" aria-controls="contents">Contents</button></header>
<aside class="rail" id="contents"><div class="edition">Design bible / edition 02.3<br>23 September 2026</div><nav class="rail-nav" aria-label="Design bible contents">{navigation(route)}</nav><div class="rail-footer"><button class="theme-button" type="button" id="theme-toggle" aria-pressed="false">Switch to dark view</button></div></aside>
<main class="page" id="main" tabindex="-1">{body}{footer}</main><div class="sr-only" id="live-status" role="status" aria-live="polite"></div><script type="application/json" id="token-json">{source['token_json']}</script></body></html>'''
    target = OUT / route.strip('/') / 'index.html'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(document)

(OUT / '404.html').write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found — Persistent Labs</title></head><body style="font:18px/1.6 system-ui;max-width:40rem;margin:10vh auto;padding:24px"><h1>Page not found.</h1><p><a href="/">Return to the design bible.</a></p></body></html>')
(OUT / 'robots.txt').write_text('User-agent: *\nDisallow: /\n')
(OUT / '_headers').write_text('/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  X-Robots-Tag: noindex, nofollow\n')
(OUT / '_redirects').write_text('/products/memorytree/ /products/fireflow/#memorytree 301\n/products/flamechorus/ /products/fireflow/#flamechorus 301\n')


class Page(HTMLParser):
    def __init__(self, content):
        super().__init__(); self.ids = []; self.refs = []; self.h1 = 0
        self.feed(content)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs: self.ids.append(attrs['id'])
        if tag == 'h1': self.h1 += 1
        for key in ('href', 'src'):
            if attrs.get(key): self.refs.append(attrs[key])


parsed = {route: Page((OUT / route.strip('/') / 'index.html').read_text()) for route in routes}
for route, page in parsed.items():
    assert page.h1 == 1 and len(page.ids) == len(set(page.ids)), route
    for ref in page.refs:
        url = urlparse(ref)
        if url.scheme or url.netloc: continue
        target_route = url.path or route
        if target_route in parsed:
            assert not url.fragment or unquote(url.fragment) in parsed[target_route].ids, (route, ref)
        else:
            assert not url.fragment and (OUT / unquote(target_route).lstrip('/')).is_file(), (route, ref)
assert sorted(id for page in routes.values() for id in page['ids']) == sorted(s[0] for s in sections)
assert not any((OUT / name).exists() for name in ('.git', 'plugins', 'reviews', 'reference', 'src'))
manifest = [{'path': path, **page} for path, page in routes.items()]
(ROOT / 'build').mkdir(exist_ok=True)
(ROOT / 'build/pages-manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
print(f'Built {len(routes)} separate pages; all 18 chapters, local links, fragments and private-file exclusions verified.')
