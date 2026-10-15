import unittest
from diagrams import convert


class DiagramTests(unittest.TestCase):
    def test_scoped_edge_defaults_and_reverse_directions(self):
        text='digraph {a -> b; edge [style=dashed;dir=back]; a -> b; subgraph cluster_x {label="Group"; c -> d}}'
        output,data=convert(text)
        self.assertEqual(len(data['nodes']),4);self.assertEqual(len(data['edges']),3)
        self.assertNotIn('dir',data['edges'][0]['attributes'])
        self.assertEqual(data['edges'][1]['attributes']['dir'],'back')
        self.assertIn('n1 --> n0',output);self.assertIn('subgraph g0["Group"]',output)
        self.assertIn('linkStyle 1 stroke-dasharray',output)

    def test_record_ports_are_preserved_on_connections(self):
        output,data=convert('digraph {a [shape=Mrecord,label="{<p0> 0|Device|<p1> 1}"]; b [label="Output"]; a:p1 -> b}')
        self.assertIn('from pad 1',output);self.assertEqual(data['edges'][0]['source_port'],'p1')

    def test_grouped_endpoints_expand_and_layout_only_nodes_are_recorded(self):
        _,data=convert('digraph {a -> {b,c}; pad [style=invis]; a -> pad [style=invis]}')
        self.assertEqual(len(data['edges']),2);self.assertEqual(len(data['nodes']),3)
        self.assertEqual(len(data['layout_only_omissions']),2)

    def test_unknown_semantics_fail_closed(self):
        with self.assertRaisesRegex(ValueError,'special arrow'):convert('digraph {a -> b [arrowhead=diamond]}')
        with self.assertRaisesRegex(ValueError,'unknown port'):convert('digraph {a:missing -> b}')
