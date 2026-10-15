import hashlib
from pathlib import Path
import tempfile
import unittest

import adapted


class AdaptedReferenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        source = self.root/'Documentation/tools/example.rst'
        source.parent.mkdir(parents=True)
        source.write_text('.. automodule:: lib.python.example\n   :members:\n')
        dependency = self.root/'tools/lib/python/example.py'
        dependency.parent.mkdir(parents=True)
        dependency.write_text('class Example: pass\n')
        self.markdown = '---\ntitle: Example\n---\n<!-- SPDX-License-Identifier: GPL-2.0 -->\n<a id="rst-example"></a>\n\nUseful reference.\n\n```python\nExample()\n```\n'
        self.page = {
            'source': str(source.relative_to(self.root)), 'source_sha256': adapted.sha(source),
            'destination': 'docs/example.md',
            'current_output_sha256': hashlib.sha256(self.markdown.encode()).hexdigest(),
            'labels': {'example': '#rst-example'},
            'source_dependencies': [{'path': str(dependency.relative_to(self.root)), 'sha256': adapted.sha(dependency)}],
            'adaptation': {'kind': 'peios-python-integration-reference', 'modules': [
                {'module': 'lib.python.example', 'disposition': 'adapted-active-interface', 'reason': 'Active consumer'}]},
        }

    def test_complete_reference(self):
        self.assertEqual(adapted.verify_page(self.root, self.page, self.markdown)['automodules_accounted'], 1)

    def test_optional_interface_is_explicit(self):
        self.page['adaptation']['modules'][0]['disposition'] = 'adapted-optional-interface'
        self.assertEqual(adapted.verify_page(self.root, self.page, self.markdown)['automodules_accounted'], 1)
        self.page['adaptation']['modules'][0]['disposition'] = 'silently-skipped'
        with self.assertRaisesRegex(ValueError, 'incomplete module disposition'):
            adapted.verify_page(self.root, self.page, self.markdown)

    def test_unaccounted_module_fails(self):
        self.page['adaptation']['modules'] = []
        with self.assertRaisesRegex(ValueError, 'coverage'):
            adapted.verify_page(self.root, self.page, self.markdown)

    def test_source_or_dependency_change_requires_review(self):
        for path in [self.page['source'], self.page['source_dependencies'][0]['path']]:
            with self.subTest(path=path):
                p = self.root/path
                original = p.read_text()
                p.write_text(original+'\n# changed\n')
                with self.assertRaisesRegex(ValueError, 'changed'):
                    adapted.verify_page(self.root, self.page, self.markdown)
                p.write_text(original)

    def test_rendered_body_and_code_are_checked(self):
        html = '<article class="article-body"><p>Useful reference.</p><pre><code>Example()\n</code></pre></article>'
        self.assertEqual(adapted.check_rendered(self.markdown, html)['literal_blocks'], 1)
        with self.assertRaisesRegex(ValueError, 'missing adapted prose'):
            adapted.check_rendered(self.markdown, html.replace('<p>Useful reference.</p>', ''))
        with self.assertRaisesRegex(ValueError, 'literal blocks'):
            adapted.check_rendered(self.markdown, html.replace('Example()', 'Wrong()'))


if __name__ == '__main__':
    unittest.main()
