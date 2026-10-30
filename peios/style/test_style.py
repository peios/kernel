"""Exercise ownership boundaries, read-only failure and explicit formatting."""

import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).absolute().parents[2]
spec = importlib.util.spec_from_file_location("kernel_style", ROOT / "peios/style.py")
assert spec is not None and spec.loader is not None
style = importlib.util.module_from_spec(spec)
spec.loader.exec_module(style)


class StyleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        shutil.copytree(ROOT / "peios/style", self.root / "peios/style")
        # The checkout may be read-only, as a build sandbox's is; the copy
        # is the test's to change.
        for path in [self.root, *self.root.rglob("*")]:
            path.chmod(path.stat().st_mode | 0o200)
        (self.root / "peios/style/test_style.py").unlink()
        shutil.copyfile(ROOT / "peios/style.py", self.root / "peios/style.py")
        for name in (".clang-format", ".rustfmt.toml"):
            shutil.copyfile(ROOT / name, self.root / name)
        scope = {
            "roots": ["peios/"],
            "files": [],
            "exclusions": {
                "peios/vendor/": "Test vendor boundary",
                "peios/generated.py": "Test generated-file boundary",
            },
        }
        (self.root / "peios/style/scope.json").write_text(json.dumps(scope))
        self.probe = self.root / "peios/probe.py"
        self.probe.write_text('def greet() -> str:\n    return "hello"\n')
        self.vendor = self.root / "peios/vendor/invalid.py"
        self.vendor.parent.mkdir()
        self.vendor.write_text("deliberately invalid Python\n")
        self.generated = self.root / "peios/generated.py"
        self.generated.write_text("also deliberately invalid\n")

    def invoke(self, command: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(self.root / "peios/style.py"), command],
            env={**os.environ, "PEIOS_STYLE_CACHE": str(style.CACHE)},
            capture_output=True,
            text=True,
            timeout=60,
        )

    def test_inventory_discovers_new_owned_files_and_excludes_other_sources(self) -> None:
        (self.root / "upstream.py").write_text("unformatted upstream\n")
        result = self.invoke("inventory")
        self.assertEqual(result.returncode, 0, result.stderr)
        files = json.loads(result.stdout)["python"]
        self.assertIn("peios/probe.py", files)
        self.assertNotIn("peios/generated.py", files)
        self.assertNotIn("peios/vendor/invalid.py", files)
        self.assertNotIn("upstream.py", files)

    def test_clean_check_accepts_generated_and_vendor_exclusions(self) -> None:
        result = self.invoke("check")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_formatting_failure_is_read_only_then_explicit_format_is_stable(self) -> None:
        original = "def greet()->str: return 'hello'\n"
        self.probe.write_text(original)
        result = self.invoke("check")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.probe.read_text(), original)
        result = self.invoke("format")
        self.assertEqual(result.returncode, 0, result.stderr)
        first = self.probe.read_bytes()
        result = self.invoke("format")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.probe.read_bytes(), first)
        self.assertEqual(self.vendor.read_text(), "deliberately invalid Python\n")
        self.assertEqual(self.generated.read_text(), "also deliberately invalid\n")
        result = self.invoke("check")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_type_failure_blocks_the_check(self) -> None:
        self.probe.write_text('def value() -> int:\n    return "wrong"\n')
        result = self.invoke("check")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("return-value", result.stdout)

    def test_missing_tools_fail_without_downloading(self) -> None:
        result = subprocess.run(
            [sys.executable, str(self.root / "peios/style.py"), "check"],
            env={**os.environ, "PEIOS_STYLE_CACHE": str(self.root / "missing-tools")},
            capture_output=True,
            text=True,
            timeout=10,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("setup", result.stderr)
        self.assertFalse((self.root / "missing-tools").exists())


if __name__ == "__main__":
    unittest.main()
