#!/usr/bin/env python3
"""Build only the shareable design bible, assets and tokens for static hosting."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse,unquote
import shutil,re,json
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'dist'
if OUT.exists():shutil.rmtree(OUT)
OUT.mkdir()
for folder in ('assets','tokens'):shutil.copytree(ROOT/folder,OUT/folder)
html=(ROOT/'index.html').read_text()
# The current bible is public. Source archives and internal review files stay in
# the private repository; remove links to files outside the publish directory.
html=re.sub(r'<a\b[^>]*href="(?:reviews|reference|docs)/[^"]*"[^>]*>(.*?)</a>',r'\1',html,flags=re.S)
html=html.replace('reference/original-design-bible.html','the private source archive')
html=html.replace('<meta name="description"','<meta name="robots" content="noindex, nofollow"><meta name="description"',1)
html=html.replace('</head>','<link rel="icon" href="assets/persistent-labs.svg" type="image/svg+xml"></head>',1)
(OUT/'index.html').write_text(html)
(OUT/'404.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Page not found · Persistent Labs</title><body style="font:18px/1.6 system-ui;max-width:40rem;margin:10vh auto;padding:24px"><h1>Page not found.</h1><p><a href="/">Return to the Persistent Labs design bible.</a></p></body></html>')
(OUT/'robots.txt').write_text('User-agent: *\nDisallow: /\n')
(OUT/'_headers').write_text('/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  X-Robots-Tag: noindex, nofollow\n')
class Refs(HTMLParser):
    def handle_starttag(self,tag,attrs):
        for k,v in attrs:
            if k not in ('href','src') or not v:continue
            p=urlparse(v)
            if p.scheme or p.netloc or not p.path:continue
            assert (OUT/unquote(p.path)).is_file(),v
Refs().feed(html)
assert not any((OUT/name).exists() for name in ('.git','plugins','reviews','reference','src'))
print(f'Built shareable site: {len(list(OUT.rglob("*")))} paths; local links verified. Private repository files excluded.')
