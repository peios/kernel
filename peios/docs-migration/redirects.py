#!/usr/bin/env python3
"""Redirect former RST and Trail addresses without replacing maintained pages."""
import argparse
import html
import json
import os
from pathlib import Path

def write(root, out):
    mapping = json.loads((root / "peios/docs-migration/source-map.json").read_text())
    count = 0
    for page in mapping["pages"]:
        source = Path(page["source"])
        destinations = [out / old / "index.html" for old in page.get("previous_references", [])]
        if source.suffix == ".rst" and source.parts[0] == "Documentation":
            destinations.append(out / source.relative_to("Documentation").with_suffix(".html"))
        if not destinations:
            continue
        target = out / page["reference"] / "index.html"
        if not target.is_file():
            raise ValueError("build Trail before generating redirects: " + str(target))
        for destination in destinations:
            if destination == out / "index.html":
                continue
            link = html.escape(os.path.relpath(target, destination.parent), quote=True)
            content = (
                '<!doctype html><meta charset="utf-8">'
                f'<meta http-equiv="refresh" content="0; url={link}">'
                f'<a href="{link}">Read the maintained Peios documentation</a>\n'
            )
            if destination.exists() and destination.read_text() != content:
                raise ValueError("refusing to replace existing output: " + str(destination))
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(content)
            count += 1
    return count

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kernel-root", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps({"redirects": write(args.kernel_root, args.out)}))
