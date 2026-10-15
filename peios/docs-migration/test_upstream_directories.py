import unittest
from pathlib import Path
from unittest.mock import patch
from upstream_changes import changes

class DirectoryDependencies(unittest.TestCase):
    def test_relocated_runtime_input_keeps_original_upstream_identity(self):
        mapping={'pages':[{'source':'Documentation/page.rst','destination':'docs/page.md','kernel_doc':[],
                 'include_plugin_dependencies':[{'path':'docs/sources/data.csv','upstream_path':'Documentation/data.csv'}]}]}
        with patch('upstream_changes.subprocess.check_output',side_effect=['old\n','new\n',b'M\0Documentation/data.csv\0']):
            report=changes(Path('/tmp'),mapping,'old','new')['changes']
        self.assertEqual(report[0]['destinations'],['docs/page.md'])

    def test_added_file_and_rename_under_directory_map_to_page(self):
        mapping={'pages':[{'source':'Documentation/admin-guide/abi.rst','destination':'docs/abi.md','kernel_doc':[],'generator_dependencies':[{'path':'Documentation/ABI','kind':'directory'}]}]}
        diff=b'A\0Documentation/ABI/testing/new-interface\0R100\0Documentation/ABI/stable/old\0Documentation/elsewhere\0A\0Documentation/ABI/.swap\0'
        with patch('upstream_changes.subprocess.check_output',side_effect=['old\n','new\n',diff]):
            report=changes(Path('/tmp'),mapping,'old','new')['changes']
        self.assertEqual(report[0]['destinations'],['docs/abi.md'])
        self.assertEqual(report[1]['destinations'],['docs/abi.md'])
        self.assertEqual(report[2]['destinations'],[])

    def test_shared_registry_group_covers_additions_renames_and_generator(self):
        pages=[{'source':'Documentation/'+n+'.yaml','destination':'docs/'+n+'.md','kernel_doc':[]} for n in ('a','b')]
        mapping={'pages':pages,'dependency_groups':{'bindings':{'destinations':['docs/a.md','docs/b.md'],'dependencies':[
            {'path':'Documentation/devicetree/bindings','kind':'directory'},
            {'path':'tools/binding.py','kind':'file'}]}}}
        diff=b'A\0Documentation/devicetree/bindings/new.yaml\0R100\0Documentation/devicetree/bindings/old.yaml\0Documentation/other.yaml\0M\0tools/binding.py\0'
        with patch('upstream_changes.subprocess.check_output',side_effect=['old\n','new\n',diff]):
            report=changes(Path('/tmp'),mapping,'old','new')['changes']
        self.assertEqual(len(report),3)
        self.assertTrue(all(r['destinations']==['docs/a.md','docs/b.md'] for r in report))

    def test_unknown_group_destination_rejected(self):
        mapping={'pages':[],'dependency_groups':{'bad':{'destinations':['missing'],'dependencies':[]}}}
        with patch('upstream_changes.subprocess.check_output',side_effect=['old\n','new\n',b'']):
            with self.assertRaisesRegex(ValueError,'unknown destination'):changes(Path('/tmp'),mapping,'old','new')

    def test_membership_group_does_not_expand_an_ordinary_source_edit(self):
        pages=[{'source':'Documentation/bindings/'+n+'.yaml','destination':'docs/'+n+'.md','kernel_doc':[]} for n in ('a','b')]
        mapping={'pages':pages,'dependency_groups':{'bindings':{'destinations':['docs/a.md','docs/b.md'],'dependencies':[
            {'path':'Documentation/bindings','kind':'directory','membership_only':True}]}}}
        diff=b'M\0Documentation/bindings/a.yaml\0A\0Documentation/bindings/new.yaml\0'
        with patch('upstream_changes.subprocess.check_output',side_effect=['old\n','new\n',diff]):
            report=changes(Path('/tmp'),mapping,'old','new')['changes']
        self.assertEqual(report[0]['destinations'],['docs/a.md'])
        self.assertEqual(report[1]['destinations'],['docs/a.md','docs/b.md'])

if __name__=='__main__':unittest.main()
