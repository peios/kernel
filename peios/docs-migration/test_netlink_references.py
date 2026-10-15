import hashlib
from pathlib import Path
import tempfile
import unittest
from netlink_references import verify_wrapper


class NetlinkWrapperTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);source=self.root/'Documentation/netlink/specs/test.yaml'
        source.parent.mkdir(parents=True);source.write_text('name: test\n')
        self.source=source
        self.markdown='---\ntitle: Test\n---\n\n```{kernel-netlink} Documentation/netlink/specs/test.yaml\n```\n'
        self.page={'source':str(source.relative_to(self.root)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
                   'destination':'docs/test.md','current_output_sha256':hashlib.sha256(self.markdown.encode()).hexdigest(),
                   'generated_reference':{'kind':'netlink-yaml','argument':str(source.relative_to(self.root))}}

    def test_matching_wrapper(self):
        self.assertEqual(verify_wrapper(self.root,self.page,self.markdown)['netlink_yaml_wrappers'],1)

    def test_changed_input_requires_review(self):
        self.source.write_text('name: changed\n')
        with self.assertRaisesRegex(ValueError,'baseline changed'):verify_wrapper(self.root,self.page,self.markdown)

    def test_wrong_fence_rejected_even_with_refreshed_output_hash(self):
        for markdown in [self.markdown.replace('test.yaml','other.yaml'),self.markdown.replace('\n```\n','\n:unknown:\n```\n')]:
            self.page['current_output_sha256']=hashlib.sha256(markdown.encode()).hexdigest()
            with self.assertRaisesRegex(ValueError,'source fence'):verify_wrapper(self.root,self.page,markdown)


if __name__=='__main__':unittest.main()
