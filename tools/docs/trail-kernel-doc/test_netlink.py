# SPDX-License-Identifier: GPL-2.0
import importlib.machinery
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE/'.deps'))
import netlink_markdown as md

ROOT = Path(os.environ['KERNEL_SRCTREE'])


class NetlinkTests(unittest.TestCase):
    def test_reference_labels_and_nested_fields(self):
        rst = '''Title
=====

.. _netlink-example:

Operations
----------

.. _example-operation-get:

get
~~~

:do:
.. LINENO 12

    **request**
        :attributes: [``id``]

See :ref:`example-operation-get`.
'''
        result = md.render(rst, 'example.yaml')
        self.assertIn('id="rst-example-operation-get"', result)
        self.assertIn('[get](#rst-example-operation-get)', result)
        self.assertIn('**attributes**', result)
        self.assertNotIn('LINENO', result)

    def test_literal_and_escaped_syntax(self):
        result = md.render('Title\n=====\n\nA literal::\n\n    <tag> `value`\n\nAn ``a`b`` token.\n', 'example')
        self.assertIn('```text\n<tag> `value`\n```', result)
        self.assertIn('``a`b``', result)

    def test_missing_reference_fails(self):
        with self.assertRaisesRegex(ValueError, 'unresolved Netlink reference'):
            md.render('See :ref:`missing`.', 'bad')

    def test_disabled_and_unsupported_directives_fail(self):
        for text in ['.. include:: /etc/passwd', '.. raw:: html\n\n   <script>x</script>', '.. image:: picture.png']:
            with self.subTest(text=text), self.assertRaises(ValueError):
                md.render(text, 'bad')

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.specs = self.root/'Documentation/netlink/specs'
        self.specs.mkdir(parents=True)
        generator = self.root/'tools/net/ynl/pyynl/lib/doc_generator.py'
        generator.parent.mkdir(parents=True)
        shutil.copy2(ROOT/'tools/net/ynl/pyynl/lib/doc_generator.py', generator)
        self.source = self.specs/'example.yaml'
        self.source.write_text('name: example\ndoc: First description.\n')

    def call(self, arguments, options=None, body=''):
        blocks = [dict(id=str(i), file='page.md', line=1, reference='kernel/example',
                       argument=argument, options=options or {}, body=body) for i, argument in enumerate(arguments)]
        result = subprocess.run([sys.executable, str(HERE/'trail-kernel-netlink'), '--srctree', str(self.root)],
                                input=json.dumps({'protocol':1,'blocks':blocks}), text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_protocol_dependencies_and_live_source(self):
        argument = str(self.source.relative_to(self.root))
        first = self.call([argument])
        self.assertIn('First description.', first['blocks'][0]['markdown'])
        for p in [self.source, self.specs, self.root/'tools/net/ynl/pyynl/lib/doc_generator.py']:
            self.assertIn(str(p), first['depends_on'])
        self.source.write_text('name: example\ndoc: Updated description.\n')
        second = self.call([argument])
        self.assertIn('Updated description.', second['blocks'][0]['markdown'])
        self.assertNotEqual(first['blocks'], second['blocks'])

    def test_paths_cannot_escape_specifications(self):
        outside = self.root/'outside.yaml'
        outside.write_text('name: outside\n')
        (self.specs/'escape.yaml').symlink_to(outside)
        for path in [str(self.source), 'Documentation/netlink/specs/../../../outside.yaml',
                     'Documentation/netlink/specs/escape.yaml', 'Documentation/netlink/specs/missing.yaml']:
            with self.subTest(path=path):
                self.assertIn('error', self.call([path])['blocks'][0])

    def test_options_body_and_bad_yaml_are_block_errors(self):
        path = str(self.source.relative_to(self.root))
        self.assertIn('error', self.call([path], options={'unknown':''})['blocks'][0])
        self.assertIn('error', self.call([path], body='unexpected')['blocks'][0])
        self.source.write_text('name: [broken\n')
        self.assertIn('error', self.call([path])['blocks'][0])

    def test_one_bad_block_does_not_omit_good_block(self):
        result = self.call(['Documentation/netlink/specs/missing.yaml', str(self.source.relative_to(self.root))])
        self.assertIn('error', result['blocks'][0])
        self.assertIn('markdown', result['blocks'][1])


if __name__ == '__main__':
    unittest.main()
