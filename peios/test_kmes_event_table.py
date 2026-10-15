"""Check catalogue validation, generated policy data and read-only drift detection."""

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

GENERATOR = Path(__file__).absolute().with_name("gen-kmes-event-table.py")


class EventTableTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.generator = self.root / "peios/gen-kmes-event-table.py"
        self.generator.parent.mkdir()
        shutil.copyfile(GENERATOR, self.generator)
        self.catalogue = self.root / "peios/packages/data/evman/test.evman"
        self.catalogue.parent.mkdir(parents=True)
        output = self.root / "security/pkm/kmes"
        output.mkdir(parents=True)
        self.outputs = [output / "event_types.h", output / "event_types.rs"]

    def invoke(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(self.generator), *arguments],
            cwd=self.root,
            capture_output=True,
            text=True,
            timeout=15,
        )

    def test_matching_ids_tiers_defaults_and_parent_paths(self) -> None:
        self.catalogue.write_text(
            "--- event example.standard\ntier: standard\n\n"
            "--- event example.debug\ntier: debug\n\n"
            "--- event example.essential\ntier: essential\n\n"
            "--- event example.verbose\ntier: verbose\n\n"
        )
        result = self.invoke()
        self.assertEqual(result.returncode, 0, result.stderr)
        header, rust = [path.read_text() for path in self.outputs]
        self.assertIn("PKM_KMES_EV_DEFAULT_MASK 0x0000000000000006ULL", header)
        self.assertIn('"example", 7, -1', header)
        self.assertIn('"essential", 9, 0', header)
        for index, tier in enumerate(("debug", "essential", "standard", "verbose")):
            self.assertRegex(header, rf"PKM_KMES_EV_EXAMPLE_{tier.upper()}\s*= {index},")
            self.assertIn(
                f'id: {index},\n    name: b"example.{tier}",\n    tier: Tier::{tier.capitalize()}',
                rust,
            )
        self.assertIn("if event.tier == Tier::Essential", rust)
        self.assertEqual(self.invoke("--check").returncode, 0)

    def test_drift_check_does_not_rewrite_and_regeneration_is_stable(self) -> None:
        self.catalogue.write_text("--- event example.event\ntier: standard\n\n")
        self.assertEqual(self.invoke().returncode, 0)
        original = [path.read_bytes() for path in self.outputs]
        self.catalogue.write_text("--- event example.event\ntier: debug\n\n")
        result = self.invoke("--check")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(result.stderr.count("out of date:"), 2)
        self.assertEqual([path.read_bytes() for path in self.outputs], original)
        self.assertEqual(self.invoke().returncode, 0)
        updated = [path.read_bytes() for path in self.outputs]
        self.assertNotEqual(updated, original)
        self.assertEqual(self.invoke().returncode, 0)
        self.assertEqual([path.read_bytes() for path in self.outputs], updated)
        self.assertEqual(self.invoke("--check").returncode, 0)

    def test_missing_output_is_reported_without_creating_it(self) -> None:
        self.catalogue.write_text("--- event example.event\ntier: standard\n\n")
        self.assertEqual(self.invoke("--check").returncode, 1)
        self.assertFalse(any(path.exists() for path in self.outputs))

    def test_invalid_catalogues_fail_before_writing_outputs(self) -> None:
        cases = {
            "empty": "",
            "missing tier": "--- event example.event\n\n",
            "invalid tier": "--- event example.event\ntier: loud\n\n",
            "invalid name": "--- event Example.event\ntier: standard\n\n",
            "duplicate": "--- event example.event\ntier: standard\n\n" * 2,
            "identifier collision": (
                "--- event example.a-b\ntier: standard\n\n--- event example.a.b\ntier: standard\n\n"
            ),
            "mask overflow": "".join(
                f"--- event example.event{i}\ntier: standard\n\n" for i in range(65)
            ),
        }
        for name, catalogue in cases.items():
            with self.subTest(name=name):
                self.catalogue.write_text(catalogue)
                for output in self.outputs:
                    output.write_text("preserve existing output\n")
                for arguments in ((), ("--check",)):
                    result = self.invoke(*arguments)
                    self.assertEqual(result.returncode, 2, result.stderr)
                    self.assertTrue(
                        all(
                            path.read_text() == "preserve existing output\n"
                            for path in self.outputs
                        )
                    )


if __name__ == "__main__":
    unittest.main()
