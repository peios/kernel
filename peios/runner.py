#!/usr/bin/env python3
"""Host orchestration only; all compilation and VM tooling live in the image."""

import argparse
import fcntl
import hashlib
import json
import os
import platform
import re
import shutil
import signal
import subprocess
import sys
import tarfile
import tempfile
from collections.abc import Sequence
from pathlib import Path
from typing import TypedDict


class BuildSettings(TypedDict):
    """Fields consumed from the build image configuration."""

    image: str
    source_date_epoch: int
    jobs: int
    localversion: str
    rust: str
    bindgen: str
    llvm: str


def run(args: Sequence[str | Path]) -> None:
    subprocess.run([str(a) for a in args], check=True)


def run_container(command: list[str]) -> None:
    # Killing the client alone can leave Docker compiling in the background.
    with tempfile.TemporaryDirectory(prefix="peios-container-") as temp:
        cid = Path(temp) / "id"
        split = command.index("run") + 1
        command = command[:split] + ["--cidfile", str(cid)] + command[split:]
        try:
            run(command)
        finally:
            if cid.exists():
                subprocess.run(
                    command[: split - 1] + ["rm", "-f", cid.read_text().strip()],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )


def docker_args(settings: BuildSettings) -> list[str]:
    image = settings["image"]
    if not re.fullmatch(r"sha256:[0-9a-f]{64}", image):
        raise ValueError("build-settings.json must pin a Docker image ID")
    docker = ["/usr/bin/docker", "--host", "unix:///var/run/docker.sock"]
    actual = subprocess.check_output(
        docker + ["image", "inspect", "--format", "{{.Id}}", image], text=True
    ).strip()
    if actual != image:
        raise ValueError("Docker image identity does not match the toolchain pin")
    return docker + [
        "run",
        "--rm",
        "--pull=never",
        "--network=none",
        "--read-only",
        "--cap-drop=ALL",
        "--security-opt=no-new-privileges",
        "--user",
        f"{os.getuid()}:{os.getgid()}",
        "--tmpfs",
        "/tmp:rw,exec,nosuid,size=2g",
        "-e",
        "HOME=/tmp",
        "-e",
        "LC_ALL=C",
        "-e",
        "TZ=UTC",
    ]


def stage(manifest: Path, state: Path, workspace: Path | None = None) -> str:
    """Copy declared files, tracking content so timestamp-only edits do not rebuild."""
    src = state / "src"
    src.mkdir(exist_ok=True)
    index = state / "inputs.json"
    old = json.loads(index.read_text()) if index.exists() else {}
    current = {}
    for entry in json.loads(manifest.read_text()):
        name = entry["relative"]
        if Path(name).is_absolute() or ".." in Path(name).parts:
            raise ValueError(f"input outside kernel workspace: {name}")
        original = (workspace / name) if workspace else Path(entry["path"])
        content = original.read_bytes()
        mode = 0o755 if original.stat().st_mode & 0o111 else 0o644
        fingerprint = hashlib.sha256(content).hexdigest() + ":" + oct(mode)
        current[name] = fingerprint
        target = src / name
        if old.get(name) != fingerprint or not target.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
            target.chmod(mode)
    for name in old.keys() - current.keys():
        (src / name).unlink(missing_ok=True)
    pending = index.with_suffix(".tmp")
    pending.write_text(json.dumps(current, sort_keys=True))
    pending.replace(index)
    return hashlib.sha256(index.read_bytes()).hexdigest()


def tree_digest(root: Path) -> str:
    """A digest of the tree at `root`: each file's content and mode, each link's target."""
    current = {}
    for parent, directories, names in os.walk(root):
        directories.sort()
        for name in [*names, *(d for d in directories if (Path(parent) / d).is_symlink())]:
            path = Path(parent) / name
            relative = str(path.relative_to(root))
            if path.is_symlink():
                current[relative] = "link:" + os.readlink(path)
            else:
                mode = 0o755 if path.stat().st_mode & 0o111 else 0o644
                current[relative] = hashlib.sha256(path.read_bytes()).hexdigest() + ":" + oct(mode)
    return hashlib.sha256(json.dumps(current, sort_keys=True).encode()).hexdigest()


def export(
    state: Path, output: Path, settings: BuildSettings, profile: str, digest: str, mode: str
) -> None:
    output.mkdir(parents=True, exist_ok=True)
    out = state / "out"
    for source, dest in [
        ("arch/x86/boot/bzImage", "bzImage"),
        ("vmlinux", "vmlinux"),
        ("System.map", "System.map"),
        (".config", "config"),
        ("Module.symvers", "Module.symvers"),
        ("include/config/kernel.release", "kernel.release"),
    ]:
        shutil.copyfile(out / source, output / dest)
    # Raw unsigned .ko files, plus Kbuild's module lists. Packaging/signing are
    # deliberately later stages; no modules_install and no private-key input.
    order = out / "modules.order"
    modules = []
    for name in order.read_text().splitlines() if order.exists() else []:
        # Current Kbuild records the module's .o in modules.order; older
        # versions recorded .ko. Export the final module, never its object.
        if name.endswith(".o"):
            name = name[:-2] + ".ko"
        elif not name.endswith(".ko"):
            raise ValueError(f"unrecognised modules.order entry: {name}")
        modules.append(out / name)
    modules += [
        out / n
        for n in ("modules.order", "modules.builtin", "modules.builtin.modinfo")
        if (out / n).exists()
    ]
    with tarfile.open(output / "modules.tar", "w") as archive:
        for path in modules:
            info = archive.gettarinfo(str(path), arcname=str(path.relative_to(out)))
            info.uid = info.gid = 0
            info.uname = info.gname = ""
            info.mtime = settings["source_date_epoch"]
            with path.open("rb") as stream:
                archive.addfile(info, stream)
    # Preserve generated headers and host programs needed by kernel-devel.
    # Packaging consumes these exact build outputs instead of regenerating a
    # potentially different configuration or depending on the private O= tree.
    support = []
    for name in ("include", "arch/x86/include", "scripts", "tools/objtool/objtool", "rust"):
        path = out / name
        candidates = path.rglob("*") if path.is_dir() else [path]
        for item in candidates:
            if not item.is_file() or item.is_symlink():
                continue
            if item.name.startswith(".") or item.suffix in (
                ".o",
                ".a",
                ".cmd",
                ".d",
                ".rmeta",
                ".rlib",
            ):
                continue
            if name == "rust" and item.suffix not in (".rs", ".h", ".c"):
                continue
            support.append((str(item.relative_to(out)), item))
    for name in ("security/pkm/kacs/builtin_signing_keys.h", "certs/peios-modsig.pem"):
        support.append((name, state / "src" / name))
    with tarfile.open(output / "kbuild-support.tar", "w") as archive:
        for name, path in sorted(support):
            info = archive.gettarinfo(str(path), arcname=name)
            info.uid = info.gid = 0
            info.uname = info.gname = ""
            info.mtime = settings["source_date_epoch"]
            with path.open("rb") as stream:
                archive.addfile(info, stream)
    (output / "build.json").write_text(
        json.dumps(
            dict(
                settings,
                profile=profile,
                input_digest=digest,
                mode=mode,
                trust="development",
                modules="unsigned",
            ),
            indent=2,
        )
        + "\n"
    )
    print(f"Kernel outputs: {output}", flush=True)


def compile_kernel(args: argparse.Namespace, state: Path, workspace: Path | None = None) -> None:
    digest = stage(Path(args.manifest), state, workspace)
    settings = json.loads((state / "src/peios/build-settings.json").read_text())
    # An image change invalidates all Kbuild compiler probes and host tools.
    identity = state / "toolchain"
    if identity.exists() and identity.read_text() != settings["image"]:
        if (state / "out").exists():
            shutil.rmtree(state / "out")
    identity.write_text(settings["image"])
    command = docker_args(settings)
    command += [
        "--mount",
        f"type=bind,src={state},dst=/work",
        "-e",
        f"SOURCE_DATE_EPOCH={settings['source_date_epoch']}",
        "-e",
        f"PEIOS_LOCALVERSION={settings['localversion']}",
        "-e",
        f"PEIOS_RUST_VERSION={settings['rust']}",
        "-e",
        f"PEIOS_BINDGEN_VERSION={settings['bindgen']}",
        "-e",
        f"PEIOS_LLVM={settings['llvm']}",
        settings["image"],
        "bash",
        "/work/src/peios/build.sh",
        args.profile,
        str(settings["jobs"]),
    ]
    run_container(command)
    output = Path(args.output).absolute() if args.command == "build" else state / "artifacts"
    export(state, output, settings, args.profile, digest, args.command)


def test_kernel(args: argparse.Namespace) -> None:
    settings = json.loads(Path("peios/build-settings.json").read_text())
    image = (Path(args.kernel) / "bzImage").resolve()
    logs = Path(os.environ.get("TEST_UNDECLARED_OUTPUTS_DIR", "/tmp/peios-kunit-logs")).resolve()
    logs.mkdir(parents=True, exist_ok=True)
    command = docker_args(settings)
    if Path("/dev/kvm").exists():
        command += ["--device", "/dev/kvm", "--group-add", str(Path("/dev/kvm").stat().st_gid)]
    command += [
        "--mount",
        f"type=bind,src={image},dst=/kernel/bzImage,readonly",
        "--mount",
        f"type=bind,src={Path('peios/test-kunit.sh').resolve()},dst=/test-kunit.sh,readonly",
        "--mount",
        f"type=bind,src={logs},dst=/logs",
        "-e",
        "PKM_KUNIT_LOG=/logs/kunit-qemu.log",
        settings["image"],
        "bash",
        "/test-kunit.sh",
        "/kernel/bzImage",
    ]
    run_container(command)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("build", "dev"):
        p = commands.add_parser(name)
        p.add_argument("--manifest", required=True)
        p.add_argument("--profile", choices=("production", "kunit"), default="production")
        if name == "build":
            p.add_argument("--output", required=True)
    commands.add_parser("test").add_argument("--kernel", required=True)
    args = parser.parse_args()
    if platform.system() != "Linux" or platform.machine() != "x86_64":
        parser.error("initial kernel build requires an x86_64 Linux host")
    if args.command == "test":
        test_kernel(args)
    elif args.command == "build":
        parent = Path(args.output).absolute().parent
        parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix=".kbuild-", dir=parent) as temp:
            compile_kernel(args, Path(temp))
    else:
        workspace = Path(os.environ["BUILD_WORKSPACE_DIRECTORY"]).resolve()
        state = workspace / ".peios-dev" / args.profile
        state.mkdir(parents=True, exist_ok=True)
        with (state / "lock").open("a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            compile_kernel(args, state, workspace)


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(128 + signal.SIGTERM))
    try:
        main()
    except (subprocess.CalledProcessError, ValueError, OSError) as error:
        sys.exit(f"peios-kbuild: {error}")
