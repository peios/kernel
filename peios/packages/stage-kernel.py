#!/usr/bin/python3
"""Prepare kernel package file trees inside the pinned build image."""

import json
import os
import re
import shutil
import subprocess
import tarfile
from pathlib import Path

SOURCE = Path("/work/src")
BUILT = Path("/built")
OUTPUT = Path("/output")
RECIPE = Path("/recipe")


def run(*args: str | Path) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run([str(a) for a in args], check=True)


def copy(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    if source.is_dir():
        shutil.copytree(source, target, dirs_exist_ok=True, symlinks=True)
        # A frozen input's copies are as writable as a file's copy is.
        for path in [target, *target.rglob("*")]:
            if not path.is_symlink():
                path.chmod(path.stat().st_mode | 0o200)
    else:
        shutil.copy2(source, target, follow_symlinks=False)
        if not target.is_symlink():
            # Bazel freezes build outputs. Copies used for stripping/debugedit
            # must be writable without ever modifying the immutable input.
            target.chmod(0o755 if target.stat().st_mode & 0o111 else 0o644)


def host_compiler() -> list[str]:
    """Kbuild's host compiler, if the build names one, as `build.sh` takes it."""
    if not os.environ.get("PEIOS_HOSTCC"):
        return []
    return [f"HOSTCC={os.environ['PEIOS_HOSTCC']}", f"HOSTCXX={os.environ['PEIOS_HOSTCXX']}"]


def extract(source: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    with tarfile.open(source) as archive:
        archive.extractall(destination, filter="data")


def main() -> None:
    release = (BUILT / "kernel.release").read_text().strip()
    if not re.fullmatch(r"[A-Za-z0-9._+-]+", release):
        raise ValueError("invalid kernel release")
    settings = json.loads((SOURCE / "peios/build-settings.json").read_text())
    kernel = OUTPUT / "kernel"
    kernel.mkdir(parents=True, exist_ok=True)
    for name in ("Makefile", "scripts", "include", "arch/x86/Makefile", "arch/x86/include"):
        copy(SOURCE / name, kernel / name)
    extract(BUILT / "kbuild-support.tar", kernel)
    for source, target in [
        ("bzImage", "arch/x86/boot/bzImage"),
        ("System.map", "System.map"),
        ("config", ".config"),
        ("Module.symvers", "Module.symvers"),
    ]:
        copy(BUILT / source, kernel / target)

    # UAPI header export is independent of module-development headers.
    run(
        "make",
        "-C",
        SOURCE,
        "O=/work/headers-build",
        "ARCH=x86",
        f"LLVM={settings['llvm']}",
        *host_compiler(),
        "headers_install",
        f"INSTALL_HDR_PATH={OUTPUT}/headers/usr",
    )

    raw = Path("/work/raw-modules")
    extract(BUILT / "modules.tar", raw)
    modroot = kernel / "modules-root"
    moddir = modroot / "lib/modules" / release
    moddir.mkdir(parents=True)
    debug = OUTPUT / "debuginfo/usr/lib/debug"
    for path in sorted(raw.rglob("*.ko")):
        relative = path.relative_to(raw)
        final = moddir / "kernel" / relative
        copy(path, final)
        symbols = debug / "lib/modules" / release / "kernel" / (str(relative) + ".debug")
        symbols.parent.mkdir(parents=True, exist_ok=True)
        run("objcopy", "--only-keep-debug", path, symbols)
        run("strip", "--strip-debug", final)
        run("zstd", "-q", "-T1", "-19", "--rm", final)
    order = (raw / "modules.order").read_text().splitlines()
    (moddir / "modules.order").write_text(
        "".join(
            "kernel/" + (name[:-2] + ".ko" if name.endswith(".o") else name) + "\n"
            for name in order
        )
    )
    for name in ("modules.builtin", "modules.builtin.modinfo"):
        copy(raw / name, moddir / name)
    run("depmod", "-b", modroot, release)
    for name in (
        "modules.dep",
        "modules.dep.bin",
        "modules.alias",
        "modules.alias.bin",
        "modules.symbols",
        "modules.symbols.bin",
    ):
        if not (moddir / name).stat().st_size:
            raise ValueError(f"module index is empty: {name}")

    # Reuse PKM's existing initramfs membership and dependency-closure checks.
    policy = Path("/work/policy/build/config")
    policy.mkdir(parents=True)
    copy(RECIPE / "irf-modules.list", policy / "irf-modules.list")
    run(
        "bash",
        RECIPE / "install-modules-irf.sh",
        "/work/policy",
        modroot,
        kernel / "modules-irf-root",
        kernel / "System.map",
    )

    vmlinux = debug / "lib/modules" / release / "vmlinux"
    copy(BUILT / "vmlinux", vmlinux)
    sections = subprocess.check_output(["readelf", "-SW", str(vmlinux)], text=True)
    if ".debug_names" in sections:
        run("objcopy", "--remove-section=.debug_names", vmlinux)
    baseversion = subprocess.check_output(
        ["make", "-s", "-C", str(SOURCE), "kernelversion"], text=True
    ).strip()
    debugroot = "/usr/src/debug/kernel-" + baseversion
    srclist = Path("/work/debug-sources")
    run("debugedit", "-b", debugroot, "-d", debugroot, "-l", srclist, vmlinux)
    notes = subprocess.check_output(["readelf", "-n", str(vmlinux)], text=True)
    match = re.search(r"Build ID: ([0-9a-f]+)", notes)
    if not match:
        raise ValueError("vmlinux has no build ID")
    buildid = match[1]
    link = debug / ".build-id" / buildid[:2] / (buildid[2:] + ".debug")
    link.parent.mkdir(parents=True, exist_ok=True)
    link.symlink_to("../../lib/modules/" + release + "/vmlinux")
    copied = 0
    for entry in set(srclist.read_bytes().split(b"\0")):
        name = entry.decode()
        if not name or name.endswith("/"):
            continue
        if name.startswith(debugroot + "/"):
            name = name[len(debugroot) + 1 :]
        relative = Path(name)
        if relative.is_absolute() or ".." in relative.parts:
            continue
        candidate = kernel / relative
        if not candidate.is_file():
            candidate = SOURCE / relative
        if candidate.is_file():
            copy(candidate, OUTPUT / "debuginfo" / debugroot.lstrip("/") / relative)
            copied += 1
    if not copied:
        raise ValueError("debug-source extraction produced no files")
    run("bash", RECIPE / "split-host-debug.sh", kernel, kernel / "host-debug")
    run("bash", RECIPE / "runtime-shebangs.sh", kernel / "scripts")
    for path in (kernel / "scripts").rglob("*"):
        if path.is_file() and not path.is_symlink():
            with path.open("rb") as stream:
                if stream.read(2) == b"#!":
                    path.chmod(path.stat().st_mode | 0o111)
    (OUTPUT / "build.json").write_text(
        json.dumps(
            {
                "kernel_release": release,
                "kernel_build": json.loads((BUILT / "build.json").read_text()),
                "modules": "unsigned",
                "userspace_abi": "debian-development",
                "release_ready": False,
                "debug_source_files": copied,
            },
            indent=2,
        )
        + "\n"
    )


if __name__ == "__main__":
    main()
