"""Validate explicitly authored Peios replacements for automodule wrappers.

These are selected integration references, not lossless Sphinx API exports.
Keep every source module's disposition and dependency baseline reviewable.
"""
import hashlib
import re
from collections import Counter

from markdown_it import MarkdownIt


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_page(root, page, markdown):
    from verify import Visible

    record = page['adaptation']
    if record['kind'] != 'peios-python-integration-reference':
        raise ValueError('unknown adaptation kind')
    source = root / page['source']
    if sha(source) != page['source_sha256']:
        raise ValueError(f'{source}: adapted source changed; review its disposition')
    modules = re.findall(r'^\.\. automodule::\s+(\S+)\s*$', source.read_text(), re.M)
    dispositions = record['modules']
    if len(modules) != len(dispositions) or set(modules) != {m['module'] for m in dispositions}:
        raise ValueError(f'{source}: automodule coverage differs from recorded dispositions')
    dependencies = {d['path']: d for d in page['source_dependencies']}
    for module in dispositions:
        if module['disposition'] not in ('adapted-active-interface', 'adapted-optional-interface', 'context-only') or not module['reason']:
            raise ValueError(f'{source}: incomplete module disposition')
        path = 'tools/' + module['module'].replace('.', '/') + '.py'
        if path not in dependencies:
            raise ValueError(f'{source}: module dependency missing: {path}')
    for path, dependency in dependencies.items():
        if sha(root / path) != dependency['sha256']:
            raise ValueError(f'{path}: adaptation dependency changed; review maintained prose')
    if hashlib.sha256(markdown.encode()).hexdigest() != page['current_output_sha256']:
        raise ValueError(f"{page['destination']}: changed article needs a refreshed review baseline")
    if '<!-- SPDX-License-Identifier: GPL-2.0 -->' not in markdown:
        raise ValueError(f'{source}: source licence missing')
    visible = Visible()
    visible.feed(MarkdownIt('commonmark', {'html': True}).render(markdown.split('---\n', 2)[2]))
    for anchor in page['labels'].values():
        if anchor.removeprefix('#') not in visible.ids:
            raise ValueError(f'{source}: missing retained anchor {anchor}')
    return {'articles': 1, 'adapted_articles': 1, 'automodules_accounted': len(modules),
            'adaptation_dependencies': len(dependencies)}


def check_rendered(markdown, html):
    """Compare authored block text and exact code with the article body only."""
    from verify import Visible, normal

    body = html.split('<article class="article-body"', 1)[1].split('>', 1)[1].split('</article>', 1)[0]
    visible = Visible()
    visible.feed(body)
    text = normal(''.join(visible.text))
    md = MarkdownIt('commonmark', {'html': True}).enable('table')
    tokens = md.parse(markdown.split('---\n', 2)[2])
    counts = Counter()
    for token in tokens:
        if token.type == 'inline':
            expected = Visible()
            expected.feed(md.renderInline(token.content))
            if normal(''.join(expected.text)) not in text:
                raise ValueError('missing adapted prose: ' + token.content[:120])
            counts['authored_text_blocks'] += 1
    # Reuse the HTML code collector without interpreting the source RST.
    from check_rendered_preservation import Rendered
    rendered = Rendered()
    rendered.feed(body)
    expected_code = [t.content for t in tokens if t.type in ('fence', 'code_block')]
    if expected_code != rendered.code_blocks:
        raise ValueError('adapted article literal blocks changed in rendered HTML')
    counts['literal_blocks'] = len(expected_code)
    counts['articles'] = 1
    return dict(counts)
