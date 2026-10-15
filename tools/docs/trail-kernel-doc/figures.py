# SPDX-License-Identifier: GPL-2.0
"""Reviewed Mermaid replacements for figures embedded in kernel-doc comments.

The registry pins upstream bytes: a changed DOT source is a build error until
its maintained Mermaid replacement has been reconciled and revalidated.
"""
import hashlib
import json
from pathlib import Path


class Figures:
    def __init__(self, srctree, directory=None):
        self.root=Path(srctree).resolve()
        self.directory=Path(directory) if directory else self.root/'docs/sources/figures'
        self.dependencies={str(Path(__file__).resolve())}

    def render(self, argument, options, body):
        registry=self.directory/'registry.json'
        entries=json.loads(registry.read_text())
        if argument not in entries:raise ValueError('kernel-figure needs a reviewed Mermaid replacement: '+argument)
        entry=entries[argument]
        source=(self.root/entry['source']).resolve()
        target=(self.directory/entry['mermaid']).resolve()
        if not source.is_relative_to(self.root) or not target.is_relative_to(self.directory.resolve()):
            raise ValueError('figure registry path escapes its root')
        if hashlib.sha256(source.read_bytes()).hexdigest()!=entry['source_sha256']:
            raise ValueError('upstream diagram changed; reconcile Mermaid replacement: '+entry['source'])
        mermaid=target.read_text().strip()
        if '```' in mermaid:raise ValueError('Mermaid replacement contains a fence')
        self.dependencies.update(map(str,(registry.resolve(),source,target)))
        # kernel-figure body is the caption. Convert it through the ordinary
        # prose renderer at the call site; options such as width are layout only.
        caption='\n'.join(body).strip() or options.get('alt','')
        return '```mermaid\n'+mermaid+'\n```',caption
