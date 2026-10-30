"""Integration checks for generator ownership and fail-closed split coverage."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
KERNEL = Path(os.environ.get('PEIOS_TEST_KERNEL_ROOT', HERE.parents[2]))
SOURCE = Path(os.environ.get('PEIOS_TEST_OUTPUT_ROOT', KERNEL))


class NativeReferenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='native-reference-test-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.mapping_path = self.root / 'peios/docs-migration/trm-source-map.json'
        self.mapping_path.parent.mkdir(parents=True)
        # Copies without the source's modes: a checkout may be read-only, as a
        # build sandbox's is, and the copies are the test's to change.
        shutil.copyfile(SOURCE / self.mapping_path.relative_to(self.root), self.mapping_path)
        self.mapping = json.loads(self.mapping_path.read_text())
        for page in self.mapping['generated_pages']:
            dst = self.root / page['path']
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(SOURCE / page['path'], dst)

    def run_generator(self, *args):
        return subprocess.run(['python3', str(HERE / 'generate.py'), '--kernel-root', str(KERNEL),
                               '--output-root', str(self.root), *args], capture_output=True, text=True)

    def test_check_detects_drift_without_writing(self):
        page = self.root / self.mapping['generated_pages'][0]['path']
        page.write_text(page.read_text() + '\nUnreviewed hand edit.\n')
        before = page.read_bytes()
        result = self.run_generator('--check')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('out of date', result.stderr)
        self.assertEqual(page.read_bytes(), before)

    def test_regenerate_preserves_authored_files(self):
        page = self.root / self.mapping['generated_pages'][0]['path']
        original = page.read_bytes()
        page.write_text('drift\n')
        authored = page.parent / '9999--authored-notes.md'
        authored.write_text('Handwritten notes must survive regeneration.\n')
        before = authored.read_bytes()
        result = self.run_generator()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(page.read_bytes(), original)
        self.assertEqual(authored.read_bytes(), before)
        updated = json.loads(self.mapping_path.read_text())
        self.assertEqual(updated['current_outputs'][page.relative_to(self.root).as_posix()], hashlib.sha256(original).hexdigest())

    def test_missing_section_assignment_is_rejected(self):
        page = self.mapping['generated_pages'][0]
        page['sections'].pop()
        self.mapping_path.write_text(json.dumps(self.mapping))
        before = {p: (self.root / p).read_bytes() for p in self.mapping['current_outputs'] if (self.root / p).is_file()}
        result = self.run_generator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('cover each generated section', result.stderr)
        self.assertTrue(all((self.root / p).read_bytes() == data for p, data in before.items()))


if __name__ == '__main__':
    unittest.main()
