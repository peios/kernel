import json
from pathlib import Path
import tempfile
import unittest

from redirects import write


class RedirectTests(unittest.TestCase):
    def test_moved_trail_and_upstream_addresses_share_a_relative_target(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            mapping = root / "peios/docs-migration/source-map.json"
            mapping.parent.mkdir(parents=True)
            mapping.write_text(json.dumps({"pages": [{
                "source": "Documentation/example.rst",
                "reference": "kernel/new/example",
                "previous_references": ["kernel/old/example"],
            }]}))
            out = root / "output"
            target = out / "kernel/new/example/index.html"
            target.parent.mkdir(parents=True)
            target.write_text("Maintained article")
            self.assertEqual(write(root, out), 2)
            self.assertEqual(write(root, out), 2)
            old = out / "kernel/old/example/index.html"
            self.assertIn('href="../../new/example/index.html"', old.read_text())
            self.assertTrue((out / "example.html").is_file())
            self.assertEqual(target.read_text(), "Maintained article")
            old.write_text("A real page now occupies this address")
            with self.assertRaisesRegex(ValueError, "refusing to replace"):
                write(root, out)

    def test_missing_target_fails_before_writing_redirect(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            mapping = root / "peios/docs-migration/source-map.json"
            mapping.parent.mkdir(parents=True)
            mapping.write_text(json.dumps({"pages": [{
                "source": "Documentation/example.txt",
                "reference": "kernel/new/example",
                "previous_references": ["kernel/old/example"],
            }]}))
            with self.assertRaisesRegex(ValueError, "build Trail before"):
                write(root, root / "output")
            self.assertFalse((root / "output").exists())
