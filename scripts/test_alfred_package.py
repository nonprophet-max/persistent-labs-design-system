"""Check the real portable archive outside the checkout (no install/network needed)."""
from pathlib import Path
import json
import re
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / 'assets/downloads/alfred-brand.zip'


def local_dependencies(directory):
    """Resolve portable Markdown links and CSS resources within the extracted skill."""
    missing = []
    for path in directory.rglob('*'):
        if not path.is_file() or path.suffix not in ('.md', '.css'):
            continue
        text = path.read_text()
        links = re.findall(r'\]\(([^)]+)\)', text) if path.suffix == '.md' else re.findall(r'url\([\'\"]?([^\)\'\"]+)', text)
        for link in links:
            if link.startswith(('https:', 'http:', 'data:', '#')):
                continue
            target = (path.parent / link.split('#')[0]).resolve()
            if not target.is_relative_to(directory.resolve()) or not target.exists():
                missing.append((path.relative_to(directory).as_posix(), link))
    return missing


class AlfredPackageTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(ARCHIVE.is_file(), 'Alfred complete download has not been generated')
        self.temp = tempfile.TemporaryDirectory(prefix='alfred-skill-')
        self.addCleanup(self.temp.cleanup)
        with zipfile.ZipFile(ARCHIVE) as archive:
            self.assertTrue(all(name.startswith('alfred-brand/') and '..' not in Path(name).parts for name in archive.namelist()))
            archive.extractall(self.temp.name)
        self.skill = Path(self.temp.name) / 'alfred-brand'

    def test_extracted_skill_resolves_dependencies_without_checkout(self):
        self.assertTrue((self.skill / 'SKILL.md').is_file())
        self.assertEqual(local_dependencies(self.skill), [])
        for host in ('.codex-plugin', '.claude-plugin'):
            manifest = json.loads((self.skill / host / 'plugin.json').read_text())
            self.assertEqual(manifest['skills'], './')
        self.assertTrue((self.skill / 'chatbot.md').is_file())

    def test_missing_font_is_reported_locally(self):
        font = self.skill / 'assets/alfred/fonts/instrumentserif-400-latin.woff2'
        self.assertTrue(font.is_file())
        font.unlink()
        self.assertTrue(any('instrumentserif-400-latin.woff2' in link for _, link in local_dependencies(self.skill)))

    def test_exact_identity_assets_and_font_provenance_are_bundled(self):
        identity = json.loads((ROOT / 'tokens/design-tokens.json').read_text())['identities']['alfred']
        self.assertEqual(json.loads((self.skill / 'assets/alfred/tokens.json').read_text()), identity)
        self.assertEqual((self.skill / 'assets/tokens.css').read_bytes(), (ROOT / 'assets/alfred/tokens.css').read_bytes())
        for file in (ROOT / 'assets/alfred').rglob('*'):
            if file.is_file():
                bundled = self.skill / 'assets/alfred' / file.relative_to(ROOT / 'assets/alfred')
                self.assertEqual(bundled.read_bytes(), file.read_bytes(), str(bundled))
        for name in ('fireflow', 'unfazed', 'lanni', 'privateinference', 'galactica'):
            package = ROOT / f'plugins/{name}-brand/skills/{name}-brand'
            self.assertFalse((package / 'assets/alfred').exists(), name)
            self.assertFalse(any('instrumentserif' in p.name or 'outfit-' in p.name for p in package.rglob('*.woff2')), name)

    def test_archive_matches_generated_skill_and_has_stable_metadata(self):
        source = ROOT / 'plugins/alfred-brand/skills/alfred-brand'
        for path in source.rglob('*'):
            if path.is_file():
                self.assertEqual((self.skill / path.relative_to(source)).read_bytes(), path.read_bytes())
        with zipfile.ZipFile(ARCHIVE) as archive:
            self.assertEqual(archive.namelist(), sorted(archive.namelist()))
            self.assertTrue(all(item.date_time == (1980, 1, 1, 0, 0, 0) for item in archive.infolist()))


if __name__ == '__main__':
    unittest.main()
