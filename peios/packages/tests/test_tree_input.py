import hashlib
import tomllib
import unittest
from pathlib import Path


class TreeInputTests(unittest.TestCase):
    def test_files_are_blobs_and_payload_symlinks_are_preserved(self) -> None:
        store = Path(__file__).with_name("fixture.ppk")
        manifest = next(store.glob("manifests/*/*/*/manifest.toml"))
        files = tomllib.loads(manifest.read_text())["files"]
        expected = hashlib.sha256(b"fixture payload\n").hexdigest()
        self.assertEqual(files["usr/bin/probe"], {"blob": "sha256:" + expected, "exec": True})
        self.assertTrue((store / "blobs/sha256" / (expected + ".zst")).is_file())
        self.assertEqual(files["usr/bin/probe-alias"], {"symlink": "probe"})
        self.assertIn("blob", files["usr/share/licenses/dev.peios.test-fixture/COPYING"])
        self.assertEqual(len(files), 3)


if __name__ == "__main__":
    unittest.main()
