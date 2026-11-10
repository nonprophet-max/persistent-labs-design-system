"""Exercise the Pages builder with a tiny real, dependency-free source tree."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


BUILDER = Path(__file__).with_name('build_pages.py')
BASE = '/persistent-labs-design-system'


class PagesBaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.temp.name)
        for name in ('scripts', 'src', 'assets/fonts', 'tokens', 'resources'):
            (cls.root / name).mkdir(parents=True)
        shutil.copy2(BUILDER, cls.root / 'scripts/build_pages.py')
        (cls.root / 'assets/persistent-labs.svg').write_text('<svg/>')
        (cls.root / 'assets/fonts/font.woff2').write_bytes(b'font')
        (cls.root / 'tokens/design-tokens.json').write_text('{}')
        (cls.root / 'src/pages.css').write_text('.extra{background:url(/assets/persistent-labs.svg)}')
        (cls.root / 'src/pages.js').write_text('/* navigation */')
        (cls.root / 'src/alfred.js').write_text('/* scoped Alfred interactions */')
        (cls.root / 'resources/SKILL.md').write_text('Fixture resource')
        (cls.root / 'brand-skills.json').write_text(json.dumps({'plugins': [
            {'name': name, 'product': name, 'skill': 'resources/SKILL.md',
             'plugin': 'resources', 'chatbot': 'resources/SKILL.md'}
            for name in ('persistent-labs-brand', 'fireflow-brand', 'alfred-brand')
        ]}))
        (cls.root / 'scripts/build.py').write_text('''
PRODUCTS = [{'id': 'fireflow', 'name': 'FireFlow'}, {'id': 'alfred', 'name': 'Alfred'}]
SECTIONS = [
    ('type', 'Typography', '01', 'Foundations', '<section id="type"><h2>Typography</h2><a href="#memorytree">Memory</a></section>'),
    ('brand', 'Products', '02', 'Products', '<section id="brand"><h2>Products</h2><a href="#alfred">Alfred</a></section>'),
    ('fireflow', 'FireFlow', '03', 'Products', '<section id="fireflow"><h2>FireFlow</h2><div id="memorytree">Memory</div><div id="flamechorus">Chat</div><a href="#memorytree">Same-page memory</a></section>'),
    ('alfred', 'Alfred', '04', 'Products', '<section id="alfred"><h2>Alfred</h2><img src="assets/persistent-labs.svg" alt="Mark"><a href="https://example.com/path?q=1#external">External</a><a href="//example.com/other">Protocol-relative</a><a href="tokens/design-tokens.json" download>Tokens</a><a href="reviews/private.md">Review</a></section>'),
    ('tokens', 'Tokens', '05', 'Reference', '<section id="tokens"><h2>Tokens</h2></section>'),
    ('decisions', 'Guidelines', '06', 'Reference', '<section id="decisions"><h2>Guidelines</h2></section>')
]
T = {'products': {p['id']: {'accent-ink': '#000'} for p in PRODUCTS}}
styles = "@font-face{font-family:Fixture;src:url('assets/fonts/font.woff2')} .mark{background:url(/assets/persistent-labs.svg)}"
document = '<header class="cover"><h1>Library</h1><span><i class="dot"></i>FireFlow</span><span><i class="dot"></i>Alfred</span></header>'
token_json = '{}'
def logo(): return '<svg aria-hidden="true"></svg>'
''')
        cls.prefixed = cls.build(BASE)
        cls.output = cls.root / 'dist-pages'

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    @classmethod
    def build(cls, base):
        return subprocess.run([sys.executable, 'scripts/build_pages.py'], cwd=cls.root,
                              env={**os.environ, 'SITE_BASE_PATH': base},
                              capture_output=True, text=True)

    def test_navigation_assets_downloads_and_cross_page_fragments_use_base(self):
        self.assertEqual(self.prefixed.returncode, 0, self.prefixed.stderr)
        alfred = (self.output / 'products/alfred/index.html').read_text()
        foundations = (self.output / 'foundations/index.html').read_text()
        for url in (BASE + '/', BASE + '/products/', BASE + '/assets/site.css',
                    BASE + '/assets/persistent-labs.svg', BASE + '/tokens/design-tokens.json'):
            self.assertIn('"' + url + '"', alfred)
        self.assertIn('href="' + BASE + '/products/fireflow/#memorytree"', foundations)
        fireflow = (self.output / 'products/fireflow/index.html').read_text()
        self.assertIn('href="#memorytree"', fireflow)
        self.assertIn('href="#main"', fireflow)
        self.assertNotIn('<base', alfred)
        self.assertNotIn('reviews/private.md', alfred)

    def test_css_font_and_background_urls_use_base(self):
        css = (self.output / 'assets/site.css').read_text()
        self.assertIn(BASE + '/assets/fonts/font.woff2', css)
        self.assertIn(BASE + '/assets/persistent-labs.svg', css)

    def test_external_and_raw_repository_urls_stay_intact(self):
        page = (self.output / 'products/alfred/index.html').read_text()
        self.assertIn('href="https://example.com/path?q=1#external"', page)
        self.assertIn('href="//example.com/other"', page)
        self.assertIn('href="https://raw.githubusercontent.com/nonprophet-max/persistent-labs-design-system/codex/design-bible/resources/SKILL.md"', page)

    def test_static_redirects_alfred_script_and_manifest(self):
        self.assertTrue((self.output / '.nojekyll').is_file())
        self.assertFalse((self.output / '_redirects').exists())
        self.assertFalse((self.output / 'persistent-labs-design-system').exists())
        for name, anchor in (('memorytree', 'memorytree'), ('flamechorus', 'flamechorus')):
            redirect = (self.output / f'products/{name}/index.html').read_text()
            self.assertIn(BASE + '/products/fireflow/#' + anchor, redirect)
        self.assertEqual((self.output / 'assets/alfred.js').read_text(), '/* scoped Alfred interactions */')
        self.assertIn('defer src="' + BASE + '/assets/alfred.js"',
                      (self.output / 'products/alfred/index.html').read_text())
        manifest = json.loads((self.root / 'build/pages-manifest.json').read_text())
        # Keep the route list consumed by the existing browser suite.
        self.assertIsInstance(manifest, list)
        self.assertEqual(next(row for row in manifest if row['path'] == '/products/alfred/')['url'],
                         BASE + '/products/alfred/')

    def test_library_identity_count_follows_product_catalogue(self):
        home = (self.output / 'index.html').read_text()
        self.assertIn('2 distinct identities,', home)
        self.assertIn('2 product identities.', home)


    def test_invalid_base_paths_fail_before_replacing_output(self):
        marker = self.output / 'keep.txt'
        marker.write_text('keep existing build')
        for value in ('relative', '//host/path', '/a/../b', '/a?query', '/a#fragment', '/a\\b', '/a b', '/a%2Fb'):
            with self.subTest(base=value):
                result = self.build(value)
                self.assertNotEqual(result.returncode, 0, value)
                self.assertIn('SITE_BASE_PATH', result.stderr)
                self.assertTrue(marker.exists())

    def test_validation_rejects_missing_css_assets(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / 'site'
            shutil.copytree(self.root, root, ignore=shutil.ignore_patterns('dist-pages', 'build'))
            (root / 'src/pages.css').write_text('.broken{background:url(/assets/missing.svg)}')
            result = subprocess.run([sys.executable, 'scripts/build_pages.py'], cwd=root,
                                    env={**os.environ, 'SITE_BASE_PATH': BASE},
                                    capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('missing.svg', result.stderr)

    def test_z_root_default_and_trailing_slash_are_compatible(self):
        self.assertEqual(self.build('/').returncode, 0)
        page = (self.output / 'products/alfred/index.html').read_text()
        self.assertIn('href="/assets/site.css"', page)
        self.assertNotIn('href="' + BASE + '/', page)
        self.assertEqual(self.build(BASE + '/').returncode, 0)
        self.assertIn('href="' + BASE + '/assets/site.css"',
                      (self.output / 'products/alfred/index.html').read_text())


if __name__ == '__main__':
    unittest.main()
