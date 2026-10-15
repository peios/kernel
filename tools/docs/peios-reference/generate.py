#!/usr/bin/env python3
"""Regenerate only the kernel-owned native ABI and constants reference pages.

The migration layout is deliberately explicit. A new section or citation stops
generation until its destination is reviewed, rather than silently losing it.
Handwritten articles and the retained learn/TRM tree are never written here.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


def clean(text):
    return re.sub(r'\s*\[\*[^\]]+\]', '', text).strip().replace('`', '')


def chunks(text, number, depth):
    body = text.split('---', 2)[2].strip() + '\n'
    tagged = []
    h2 = h3 = 0
    for line in body.splitlines(keepends=True):
        heading = re.match(r'^(#{2,3}) (.*)', line)
        if heading:
            if heading[1] == '##':
                h2 += 1
                h3 = 0
            else:
                h3 += 1
            n = number + '.' + str(h2) + ('.' + str(h3) if heading[1] == '###' else '')
            tagged.append(f'<!--TRMSECTION:{n}:{clean(heading[2])}-->\n')
        tagged.append(line)
    parts = re.split(r'(?=<!--TRMSECTION:[^\n]+-->\n#{2,' + str(depth) + r'} )', ''.join(tagged))
    result = {}
    for i, part in enumerate(parts):
        if not part.strip():
            continue
        if not result:
            part = '<a id="trm-' + number.lower().replace('.', '-') + '"></a>\n\n' + part
        result[i] = part
    return result


def transform(text, mapping):
    text = re.sub(r'<!--TRMSECTION:([^:]+):.*?-->', lambda m: '<a id="trm-' + m[1].lower().replace('.', '-') + '"></a>\n', text)
    text = re.sub(r'\[\*([^\]]+)\]', lambda m: '<a id="cite-' + m[1] + '"></a>', text)

    def section(match):
        n = match[1].rstrip('.')
        target = mapping['sections'][n]
        return '[' + target['title'].replace('[', '').replace(']', '') + '](<~' + target['reference'] + '#' + target['fragment'] + '>)' + match[1][len(n):]

    text = re.sub(r'§([0-9A-Z]+(?:\.[0-9A-Z]+)*\.?)(?![\w])', section, text)
    for old, new in mapping['path_replacements']:
        text = re.sub(r'(?<![\w/])' + re.escape(old), lambda m: new, text)
    return text


def render_all(kernel_root, output_root):
    mapping_path = output_root / 'peios/docs-migration/trm-source-map.json'
    mapping = json.loads(mapping_path.read_text())
    articles = {a['source']: a for a in mapping['articles']}
    generated = mapping['generated_pages']
    rendered = {}
    with tempfile.TemporaryDirectory(prefix='peios-reference-') as temp:
        env = dict(os.environ, PEIOS_KERNEL_ROOT=str(kernel_root),
                   PEIOS_REFERENCE_RAW_OUTPUT=temp, PYTHONDONTWRITEBYTECODE='1')
        for generator in dict.fromkeys(p['generator'] for p in generated):
            script = Path(__file__).parent / 'generators' / ('gen-' + generator + '.py')
            subprocess.run(['python3', str(script)], env=env, check=True, stdout=subprocess.DEVNULL)
        for source in dict.fromkeys(p['source'] for p in generated):
            destinations = [p for p in generated if p['source'] == source]
            article = articles[source]
            raw = (Path(temp) / (destinations[0]['generator'] + '.md')).read_text()
            depth = 3 if destinations[0]['generator'] in ('kacs-abi', 'lcs-abi') else 2
            parts = chunks(raw, article['number'], depth)
            expected = {b['index']: b['heading'] for b in article['blocks']}
            actual = {}
            for index, part in parts.items():
                heading = re.search(r'^#{2,3} (.*)$', part, re.M)
                actual[index] = clean(heading[1]) if heading else ''
            if expected != actual:
                raise SystemExit(f'{source}: generated sections changed; review trm-source-map.json before regenerating')
            names = re.findall(r'\[\*([^\]]+)\]', raw)
            expected_names = {n for n, c in mapping['claims'].items() if c['source'] == source}
            if set(names) != expected_names or len(names) != len(set(names)):
                raise SystemExit(f'{source}: named claims changed; review their destinations before regenerating')
            assigned = [index for p in destinations for index in p['sections']]
            if sorted(assigned) != sorted(parts) or len(assigned) != len(set(assigned)):
                raise SystemExit(f'{source}: split layout does not cover each generated section exactly once')
            for i, page in enumerate(destinations):
                text = ('---\ntitle: ' + json.dumps(page['title'], ensure_ascii=False)
                        + '\ndescription: ' + json.dumps(page['description'], ensure_ascii=False)
                        + '\ntype: reference\n---\n\n')
                for index in page['sections']:
                    body = transform(parts[index], mapping)
                    if depth == 3:
                        body = re.sub(r'^### ', '## ', body, flags=re.M)
                    text += body.strip() + '\n\n'
                text = text.rstrip() + '\n'
                if i == 0 and len(destinations) > 1:
                    text += '\n## Related explanations\n\n' + ''.join(
                        '- [' + p['title'] + '](<~' + p['reference'] + '>)\n'
                        for p in destinations[1:])
                rendered[page['path']] = text
    return rendered


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--kernel-root', type=Path, default=Path(__file__).resolve().parents[3])
    parser.add_argument('--output-root', type=Path, help='Optional staged kernel tree; defaults to --kernel-root')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    kernel_root = args.kernel_root.resolve()
    output_root = (args.output_root or kernel_root).resolve()
    rendered = render_all(kernel_root, output_root)
    changed = [p for p, text in rendered.items() if not (output_root / p).is_file() or (output_root / p).read_text() != text]
    if args.check:
        if changed:
            raise SystemExit('Generated reference is out of date:\n' + '\n'.join(changed))
        print(f'{len(rendered)} native reference pages are current')
        return
    for path in changed:
        target = output_root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        temporary = target.with_suffix('.md.new')
        temporary.write_text(rendered[path])
        temporary.replace(target)
    if changed:
        mapping_path = output_root / 'peios/docs-migration/trm-source-map.json'
        mapping = json.loads(mapping_path.read_text())
        for path in changed:
            mapping.setdefault('current_outputs', {})[path] = hashlib.sha256(rendered[path].encode()).hexdigest()
        mapping_path.write_text(json.dumps(mapping, indent=2, ensure_ascii=False) + '\n')
    print(f'Updated {len(changed)} of {len(rendered)} native reference pages')


if __name__ == '__main__':
    main()
