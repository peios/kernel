"""Verify newly generated ML-DSA fixtures with OpenSSL 3.5 or later."""

import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PEIOS = Path(__file__).absolute().parent


class MldsaVectors(unittest.TestCase):
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

    def test_mldsa_vectors_verify_independently_with_openssl(self) -> None:
        output = self.root / "vectors.h"
        result = self.invoke("generate-kacs-kunit-mldsa-vectors.py", "--out", str(output))
        self.assertEqual(result.returncode, 0, result.stderr)
        arrays = {
            name: bytes(int(value, 16) for value in re.findall(r"0x([0-9a-f]{2})", body))
            for name, body in re.findall(
                r"static const u8 (\w+)\[\d+\] __maybe_unused = \{(.*?)\};",
                output.read_text(),
                re.S,
            )
        }
        public = arrays["pkm_kunit_mldsa65_pubkey"]
        self.assertEqual(len(public), 1952)
        # SubjectPublicKeyInfo: id-ml-dsa-65 (2.16.840.1.101.3.4.3.18), raw BIT STRING.
        key = self.root / "public.der"
        key.write_bytes(bytes.fromhex("308207b2300b0609608648016503040312038207a100") + public)
        for label in ("tcb", "alt"):
            message = self.root / "message"
            signature = self.root / "signature"
            message.write_bytes(arrays[f"pkm_kunit_mldsa65_{label}_hash"])
            signature.write_bytes(arrays[f"pkm_kunit_mldsa65_{label}_sig"])
            command = [
                "openssl",
                "pkeyutl",
                "-verify",
                "-pubin",
                "-inkey",
                str(key),
                "-keyform",
                "DER",
                "-rawin",
                "-in",
                str(message),
                "-sigfile",
                str(signature),
            ]
            verified = subprocess.run(command, capture_output=True, text=True, timeout=10)
            self.assertEqual(verified.returncode, 0, verified.stderr)
            message.write_bytes(b"\x55" * 32)
            rejected = subprocess.run(command, capture_output=True, text=True, timeout=10)
            self.assertNotEqual(rejected.returncode, 0)


if __name__ == "__main__":
    unittest.main()
