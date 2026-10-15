#!/usr/bin/env python3
"""Regenerate the shipped port-reservation security descriptors.

The descriptors grant PORT_BIND | READ_CONTROL. Capability SIDs use eight
little-endian sub-authorities from SHA-256 of the UTF-8 capability name.
"""

import argparse
import hashlib
import json
import struct
from pathlib import Path

PORT_BIND = 0x1
READ_CONTROL = 0x20000


def sid(authority: int, subauthorities: list[int]) -> bytes:
    return (
        bytes([1, len(subauthorities)])
        + authority.to_bytes(6, "big")
        + b"".join(struct.pack("<I", value) for value in subauthorities)
    )


SYSTEM = sid(5, [18])
EVERYONE = sid(1, [0])


def capability(name: str) -> tuple[bytes, str]:
    digest = hashlib.sha256(name.encode("utf-8")).digest()
    subauthorities = list(struct.unpack("<8I", digest))
    return sid(15, [3, *subauthorities]), "S-1-15-3-" + "-".join(map(str, subauthorities))


def ace(principal: bytes, mask: int) -> bytes:
    return bytes([0, 0]) + struct.pack("<HI", 8 + len(principal), mask) + principal


def sd(aces: list[bytes]) -> bytes:
    body = b"".join(aces)
    acl = bytes([2, 0]) + struct.pack("<HHH", 8 + len(body), len(aces), 0) + body
    owner = 20
    group = owner + len(SYSTEM)
    header = bytes([1, 0]) + struct.pack("<HIIII", 0x8004, owner, group, 0, group + len(SYSTEM))
    return header + SYSTEM + SYSTEM + acl


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="report drift without writing")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).absolute().parent / "packages/data/regim/port-reservations.reg",
    )
    args = parser.parse_args()
    original = args.output.read_text()
    doc = json.loads(original)
    principal, principal_name = capability("bindLowPorts")
    values = doc["keys"][-1]["values"]
    values[0]["data"] = sd([ace(EVERYONE, PORT_BIND | READ_CONTROL)]).hex()
    values[1]["data"] = sd(
        [ace(SYSTEM, PORT_BIND | READ_CONTROL), ace(principal, PORT_BIND | READ_CONTROL)]
    ).hex()
    doc["_comment"] = [
        "                   " + principal_name + " is the derived capability SID for the name"
        if "S-1-15-3-" in line
        else line
        for line in doc["_comment"]
    ]
    generated = json.dumps(doc, indent=2) + "\n"
    if args.check:
        if generated != original:
            print(f"stale port reservation seed: {args.output}")
            return 1
    else:
        args.output.write_text(generated)
    print(principal_name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
