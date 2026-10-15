"""Exercise source generators without replacing checked-in security fixtures."""

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PEIOS = Path(__file__).absolute().parent


class DataGenerators(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)

    def invoke(self, name: str, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(PEIOS / name), *args],
            capture_output=True,
            text=True,
            timeout=30,
        )

    def test_port_seed_check_is_read_only_and_generation_repairs_drift(self) -> None:
        seed = self.root / "ports.reg"
        shutil.copyfile(PEIOS / "packages/data/regim/port-reservations.reg", seed)
        expected = seed.read_bytes()
        doc = json.loads(expected)
        doc["keys"][-1]["values"][1]["data"] = "bad"
        seed.write_text(json.dumps(doc))
        changed = seed.read_bytes()
        result = self.invoke("gen-port-reservations-seed.py", "--output", str(seed), "--check")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(seed.read_bytes(), changed)
        result = self.invoke("gen-port-reservations-seed.py", "--output", str(seed))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(seed.read_bytes(), expected)
        result = self.invoke("gen-port-reservations-seed.py", "--output", str(seed), "--check")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_casefold_filters_full_and_turkic_mappings_and_preserves_simple_pairs(self) -> None:
        source = self.root / "CaseFolding.txt"
        source.write_text(
            "0043; C; 0063; # C\n0041; C; 0061; # A\n0042; C; 0062; # B\n"
            "1E9E; S; 00DF;\n00DF; F; 0073 0073;\n0049; T; 0131;\n"
        )
        rust = self.root / "fold.rs"
        go = self.root / "fold.go"
        result = self.invoke(
            "generate-casefold-table.py",
            "--input",
            str(source),
            "--out",
            str(rust),
            "--go-out",
            str(go),
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("start: 0x0041, end: 0x0043, mapped_start: 0x0061", rust.read_text())
        self.assertIn("(0x1E9E, 0x00DF)", rust.read_text())
        self.assertIn("{0x0041, 0x0043, 0x0061}", go.read_text())
        self.assertIn("{0x1E9E, 0x00DF}", go.read_text())
        self.assertIn("caseFoldMappings = 4", go.read_text())
        self.assertNotIn("0x0131", rust.read_text())

    def test_casefold_rejects_duplicate_or_non_simple_rows(self) -> None:
        source = self.root / "CaseFolding.txt"
        output = self.root / "fold.rs"
        for data in ("0041; C; 0061;\n0041; S; 0062;\n", "0041; C; 0061 0062;\n"):
            with self.subTest(data=data):
                source.write_text(data)
                result = self.invoke(
                    "generate-casefold-table.py", "--input", str(source), "--out", str(output)
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
