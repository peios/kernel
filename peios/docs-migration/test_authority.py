import hashlib
from pathlib import Path
import tempfile
import unittest
from check_authority import check

class AuthorityTests(unittest.TestCase):
    def test_original_prose_is_provenance_but_live_inputs_are_required(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'docs').mkdir();article=root/'docs/page.md';article.write_text('Maintained prose')
            source=root/'data';source.write_text('input')
            page={'source':'Documentation/removed.rst','destination':'docs/page.md',
                  'current_output_sha256':hashlib.sha256(article.read_bytes()).hexdigest(),
                  'plugin_dependencies':[{'path':'data','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest()}]}
            mapping={'pages':[page]}
            self.assertEqual(check(root,root/'docs',mapping)['errors'],0)
            source.unlink()
            with self.assertRaisesRegex(ValueError,'missing runtime'):check(root,root/'docs',mapping)
            source.write_text('input');article.write_text('Unreviewed edit')
            with self.assertRaisesRegex(ValueError,'maintained article changed'):check(root,root/'docs',mapping)
