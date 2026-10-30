#!/usr/bin/env python3
"""Install, check or format the explicitly owned kernel sources."""

import argparse
import concurrent.futures
import hashlib
import io
import json
import os
import platform
import subprocess
import sys
import tarfile
import urllib.request
from pathlib import Path

ROOT = Path(__file__).absolute().parents[1]
CONFIG = ROOT / "peios/style"
LOCKS = ["requirements.lock", "binary-tools.lock.json", "runtimes.json"]
IDENTITY = hashlib.sha256(b"".join((CONFIG / name).read_bytes() for name in LOCKS)).hexdigest()[:20]
CACHE = Path(os.environ.get("PEIOS_STYLE_CACHE", Path.home() / ".cache/peios/kernel-style"))
TOOLS = CACHE / IDENTITY
RUNTIMES = json.loads((CONFIG / "runtimes.json").read_text())


def run(command: list[str], **kwargs: object) -> subprocess.CompletedProcess:
    """Run a tool; subprocess keywords are supplied only by this module."""
    # subprocess has different overloads for captured text and binary streams.
    return subprocess.run(command, cwd=ROOT, check=True, **kwargs)  # type: ignore[call-overload]


def binary(name: str) -> str:
    directory = ".venv/bin" if name in {"python", "ruff", "mypy", "clang-format"} else "bin"
    return str(TOOLS / directory / name)


def verify() -> None:
    """Reject missing or drifted tools before inspecting source."""
    if sys.platform != "linux" or platform.machine() != "x86_64":
        raise ValueError("The qualified style tools require x86_64 Linux")
    pins = {
        line.split()[0].split("==")[0]: line.split()[0].split("==")[1]
        for line in (CONFIG / "requirements.lock").read_text().splitlines()
        if line and not line.startswith("#")
    }
    code = "import importlib.metadata,json,platform,sys; print(json.dumps([platform.python_version(),{n:importlib.metadata.version(n) for n in sys.argv[1:]}]))"
    actual = json.loads(
        run([binary("python"), "-c", code, *pins], capture_output=True, text=True).stdout
    )
    if actual != [RUNTIMES["python"], pins]:
        raise ValueError("Style Python environment differs from its locks; rerun setup")
    for name, entry in json.loads((CONFIG / "binary-tools.lock.json").read_text()).items():
        if hashlib.sha256(Path(binary(name)).read_bytes()).hexdigest() != entry["binary_sha256"]:
            raise ValueError(f"Style binary hash mismatch: {name}")
    for key in ("rust_toolchain", "kernel_rust_toolchain"):
        run(["rustfmt", "+" + RUNTIMES[key], "--version"], capture_output=True)


def setup() -> None:
    """Install hash-locked tools in a cache outside source and Bazel inputs."""
    if platform.python_version() != RUNTIMES["python"]:
        raise ValueError(f"Run setup with Python {RUNTIMES['python']}")
    TOOLS.mkdir(parents=True, exist_ok=True)
    run([sys.executable, "-m", "venv", str(TOOLS / ".venv")])
    run(
        [
            binary("python"),
            "-m",
            "pip",
            "install",
            "--disable-pip-version-check",
            "--require-hashes",
            "--only-binary=:all:",
            "-r",
            str(CONFIG / "requirements.lock"),
        ]
    )
    (TOOLS / "bin").mkdir(exist_ok=True)
    for name, entry in json.loads((CONFIG / "binary-tools.lock.json").read_text()).items():
        target = Path(binary(name))
        if (
            target.exists()
            and hashlib.sha256(target.read_bytes()).hexdigest() == entry["binary_sha256"]
        ):
            continue
        request = urllib.request.Request(entry["url"], headers={"User-Agent": "Peios-style"})
        with urllib.request.urlopen(request, timeout=60) as response:
            artifact = response.read()
        if hashlib.sha256(artifact).hexdigest() != entry["sha256"]:
            raise ValueError(f"Download hash mismatch: {name}")
        if entry["member"]:
            with tarfile.open(fileobj=io.BytesIO(artifact), mode="r:gz") as archive:
                member = archive.extractfile(entry["member"])
                if member is None:
                    raise ValueError(f"Missing executable: {name}")
                artifact = member.read()
        if hashlib.sha256(artifact).hexdigest() != entry["binary_sha256"]:
            raise ValueError(f"Executable hash mismatch: {name}")
        pending = target.with_suffix(".download")
        pending.write_bytes(artifact)
        pending.chmod(0o755)
        pending.replace(target)
    verify()
    print(f"Style tools ready: {TOOLS}")


def inventory() -> dict[str, list[str]]:
    """Discover supported files only inside declared ownership boundaries."""
    scope = json.loads((CONFIG / "scope.json").read_text())
    names = set(scope["files"])
    for prefix in scope["roots"]:
        names.update(str(p.relative_to(ROOT)) for p in (ROOT / prefix).rglob("*") if p.is_file())
    groups: dict[str, list[str]] = {
        name: [] for name in ("c", "rust", "host-rust", "python", "shell")
    }
    for name in sorted(names):
        if any(name == p or (p.endswith("/") and name.startswith(p)) for p in scope["exclusions"]):
            continue
        path = Path(name)
        kind = {
            ".c": "c",
            ".h": "c",
            ".rs": "rust",
            ".py": "python",
            ".sh": "shell",
        }.get(path.suffix)
        if kind == "rust" and name.startswith("peios/"):
            kind = "host-rust"
        if kind:
            if not (ROOT / name).is_file():
                raise ValueError(f"Missing explicitly owned file: {name}")
            groups[kind].append(name)
    return groups


def formatted(kind: str, name: str) -> tuple[str, bytes]:
    """Format one file through stdin, avoiding Rust child-module traversal."""
    commands = {
        "c": [binary("clang-format"), "--style=file", "--assume-filename=" + str(ROOT / name)],
        "rust": [
            "rustfmt",
            "+" + RUNTIMES["kernel_rust_toolchain"],
            "--config-path",
            str(ROOT / ".rustfmt.toml"),
            "--config",
            "reorder_modules=false,reorder_imports=false",
            "--emit",
            "stdout",
        ],
        "host-rust": [
            "rustfmt",
            "+" + RUNTIMES["rust_toolchain"],
            "--config-path",
            str(CONFIG / "rustfmt.toml"),
            "--emit",
            "stdout",
        ],
        "python": [
            binary("ruff"),
            "format",
            "--config",
            str(CONFIG / "ruff.toml"),
            "--stdin-filename",
            name,
            "-",
        ],
        "shell": [binary("shfmt"), "-i", "4", "-filename", name],
    }
    if kind == "host-rust" and any(
        name.startswith("peios/rust/" + crate + "/")
        for crate in ("kacs-core", "lcs-core", "pnp-core", "stratafs-core")
    ):
        commands[kind] += ["--edition", "2021"]
    result = run(commands[kind], input=(ROOT / name).read_bytes(), capture_output=True)
    return name, result.stdout


def check_or_format(apply: bool) -> int:
    """Check all owned files; formatting writes only files that differ."""
    verify()
    groups = inventory()
    changed = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        futures = [
            pool.submit(formatted, kind, name) for kind, names in groups.items() for name in names
        ]
        for future in futures:
            name, content = future.result()
            path = ROOT / name
            if path.read_bytes() != content:
                changed.append(name)
                if apply:
                    path.write_bytes(content)
                print(("Formatted: " if apply else "Needs formatting: ") + name)
    if apply:
        print(f"Formatted {len(changed)} files. Run check to inspect lint and types.")
        return 0
    failed = bool(changed)
    python = groups["python"]
    commands = [
        [binary("ruff"), "check", "--no-cache", "--config", str(CONFIG / "ruff.toml"), *python],
        [
            binary("mypy"),
            "--config-file",
            str(CONFIG / "mypy.ini"),
            "--cache-dir",
            "/dev/null",
            "--no-incremental",
            *python,
        ],
        [binary("shellcheck"), *groups["shell"]],
    ]
    for command in commands:
        if command[0] == binary("shellcheck") and not groups["shell"]:
            continue
        if command[0] in (binary("ruff"), binary("mypy")) and not python:
            continue
        try:
            run(command)
        except subprocess.CalledProcessError:
            failed = True
    print(
        f"Checked {sum(map(len, groups.values()))} owned files; "
        + ("FAILED" if failed else "passed")
    )
    return int(failed)


def main() -> int:
    """Expose identical style operations for local development and CI."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("setup", "check", "format", "inventory"))
    args = parser.parse_args()
    if args.command == "setup":
        setup()
        return 0
    if args.command == "inventory":
        print(json.dumps(inventory(), indent=2))
        return 0
    return check_or_format(args.command == "format")


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        sys.exit(
            f"peios-style: {error}\nInstall prerequisites and run: python3 peios/style.py setup"
        )
