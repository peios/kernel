import tempfile
from pathlib import Path
import unittest
from supplementary import sha,verify,comment_notes

class SourceExcerptTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
        (self.root/'test').write_text('\tline\n\n')
        self.markdown='---\ntitle: Test\n---\n\n```{kernel-include} test\n:language: text\n```\n'
        self.page={'source':'test','source_title':'Test','source_sha256':sha((self.root/'test').read_bytes()),'current_output_sha256':sha(self.markdown.encode()),'supplementary_source':{'kind':'live-source','language':'text'}}
    def test_exact_example_whitespace_required(self):
        html='<h1>Test</h1><pre><code>\tline\n\n\n</code></pre>'
        verify(self.root,self.page,self.markdown,html)
        with self.assertRaisesRegex(ValueError,'whitespace'):verify(self.root,self.page,self.markdown,html.replace('\t','    '))
    def test_slicing_cannot_be_hidden_by_updating_wrapper_hash(self):
        markdown=self.markdown.replace(':language: text',':language: text\n:start-line: 2');self.page['current_output_sha256']=sha(markdown.encode())
        with self.assertRaisesRegex(ValueError,'complete original'):verify(self.root,self.page,markdown)
    def test_commented_readme_stops_before_archive_and_keeps_indentation(self):
        source='#! /bin/sh\n#  Title\n#\n#      indented example\n#!/bin/sh\necho archive\n'
        self.assertEqual(comment_notes(source),'Title\n\n    indented example\n')
        with self.assertRaisesRegex(ValueError,'unexpected code'):comment_notes(source.replace('#\n','echo unexpected\n'))

if __name__=='__main__':unittest.main()
