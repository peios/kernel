import hashlib
import tempfile
from pathlib import Path
import unittest
from check_inventory import check,files

class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
        (self.root/'Documentation').mkdir();self.path=self.root/'Documentation/no-extension';self.path.write_text('source')
        self.mapping={'pages':[]};self.inventory={'sources':[dict(files(self.root)['Documentation/no-extension'],disposition='retained metadata',reason='Test metadata.',owners=[])]}
    def test_unknown_extension_and_hidden_additions_fail(self):
        self.assertFalse(check(self.root,self.mapping,self.inventory)['errors'])
        for name in ['new.odd','.hidden']:(self.root/'Documentation'/name).write_text('new')
        self.assertEqual(len(check(self.root,self.mapping,self.inventory)['errors']),2)
    def test_changes_and_removals_fail(self):
        self.path.write_text('changed');self.assertIn('changed source',check(self.root,self.mapping,self.inventory)['errors'][0])
        self.path.unlink();self.assertIn('removed source',check(self.root,self.mapping,self.inventory)['errors'][0])
    def test_false_article_disposition_and_unknown_category_fail(self):
        self.inventory['sources'][0]['disposition']='translated article';self.assertTrue(check(self.root,self.mapping,self.inventory)['errors'])
        self.inventory['sources'][0]['disposition']='ignored';self.assertTrue(check(self.root,self.mapping,self.inventory)['errors'])
    def test_symlink_retargeting_detected_even_when_contents_match(self):
        alias=self.root/'Documentation/alias';alias.symlink_to('no-extension')
        record=dict(files(self.root)['Documentation/alias'],disposition='redirect',reason='Alias.',owners=[]);self.inventory['sources'].append(record)
        other=self.root/'outside';other.write_text('source');alias.unlink();alias.symlink_to('../outside')
        self.assertIn('symlink_target',check(self.root,self.mapping,self.inventory)['errors'][0])

    def test_pruned_source_must_stay_absent_and_new_sources_fail(self):
        self.inventory['layout']='tooling-and-trail'
        self.inventory['sources'][0]['storage']={'action':'remove','reason':'Migrated.'}
        self.path.unlink()
        self.assertFalse(check(self.root,self.mapping,self.inventory)['errors'])
        self.path.write_text('source')
        self.assertTrue(check(self.root,self.mapping,self.inventory)['errors'])
        (self.root/'Documentation/new.odd').write_text('new')
        self.assertTrue(any('unclassified' in e for e in check(self.root,self.mapping,self.inventory)['errors']))

    def test_moved_input_must_exist_once_and_match_reviewed_bytes(self):
        self.inventory['layout']='tooling-and-trail'
        target='docs/sources/example';path=self.root/target;path.parent.mkdir(parents=True)
        self.inventory['sources'][0]['storage']={'action':'move','path':target,'reason':'Trail input.'}
        self.path.rename(path)
        self.assertFalse(check(self.root,self.mapping,self.inventory)['errors'])
        path.write_text('drift')
        self.assertTrue(check(self.root,self.mapping,self.inventory)['errors'])
        path.unlink()
        self.assertTrue(check(self.root,self.mapping,self.inventory)['errors'])

if __name__=='__main__':unittest.main()
