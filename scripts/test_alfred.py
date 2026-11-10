"""Consumer checks: links must resolve and portable exports must preserve canonical data."""
import importlib
import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids = []; self.links = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a: self.ids.append(a['id'])
        for key in ('href', 'src'):
            if key in a: self.links.append(a[key])

class AlfredTests(unittest.TestCase):
    def module(self):
        self.assertTrue((ROOT / 'scripts/alfred_brand.py').exists(), 'Alfred renderer is absent')
        return importlib.import_module('alfred_brand')

    def test_renderer_links_reach_sections_and_real_downloads(self):
        module = self.module(); module.build_assets()
        parser = Links(); parser.feed(module.render_alfred())
        self.assertEqual(len(parser.ids), len(set(parser.ids)), 'Duplicate ids break direct sharing')
        self.assertGreaterEqual(len([x for x in parser.links if x.startswith('#alfred-')]), 8)
        self.assertIn('assets/alfred/logos/alfred-logo-ink.svg', parser.links)
        self.assertIn('assets/alfred/tokens.json', parser.links)
        self.assertIn('assets/downloads/alfred-brand.zip', parser.links)
        self.assertIn('https://raw.githubusercontent.com/nonprophet-max/persistent-labs-design-system/codex/design-bible/plugins/alfred-brand/skills/alfred-brand/SKILL.md', parser.links)
        for link in parser.links:
            if link.startswith('#'): self.assertIn(link[1:], parser.ids)
            elif not link.startswith(('https:', 'http:')):
                self.assertTrue((ROOT / link).is_file(), f'Broken resource: {link}')

    def test_portable_tokens_and_fonts_round_trip_from_canonical_identity(self):
        module = self.module(); module.build_assets()
        identity = json.loads((ROOT / 'tokens/design-tokens.json').read_text())['identities']['alfred']
        exported = json.loads((ROOT / 'assets/alfred/tokens.json').read_text())
        self.assertEqual(exported, identity, 'Portable token data drifted')
        css = (ROOT / 'assets/alfred/tokens.css').read_text()
        for name, value in identity['color'].items():
            self.assertIn(f'--alfred-{name}: {value};', css)
        fonts = (ROOT / 'assets/alfred/fonts.css').read_text()
        for file in re.findall(r'url\("([^\"]+)"\)', fonts):
            self.assertTrue((ROOT / 'assets/alfred' / file).is_file())
        self.assertIn('outfit-variable-latin-ext.woff2', fonts)
        self.assertNotIn('outfit-variable-cyrillic', fonts)
        markdown = module.brand_markdown()
        for value in identity['color'].values(): self.assertIn(value, markdown)
        self.assertIn('system-ui', markdown)

if __name__ == '__main__': unittest.main()
