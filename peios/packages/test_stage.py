import importlib.util
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location("stage", Path(__file__).with_name("stage-kernel.py"))
assert spec is not None and spec.loader is not None
stage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(stage)


class StageTests(unittest.TestCase):
    def test_frozen_bazel_artifact_gets_a_writable_private_copy(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for mode in (0o444, 0o555):
                source = root / ("input-" + str(mode))
                target = root / ("output-" + str(mode))
                source.write_bytes(b"immutable build artifact")
                source.chmod(mode)
                stage.copy(source, target)
                self.assertTrue(target.stat().st_mode & 0o200)
                self.assertEqual(bool(target.stat().st_mode & 0o111), bool(mode & 0o111))
                target.write_bytes(b"transformed debug artifact")
                self.assertEqual(source.read_bytes(), b"immutable build artifact")
                self.assertEqual(source.stat().st_mode & 0o777, mode)


if __name__ == "__main__":
    unittest.main()
