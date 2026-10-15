#!/usr/bin/python3
"""Build kernel-family staging trees using the pinned development image."""

import argparse
import importlib.util
import json
import signal
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location(
    "kernel_runner", Path(__file__).resolve().parents[1] / "runner.py"
)
assert spec is not None and spec.loader is not None
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


def tools(args: argparse.Namespace) -> None:
    output = Path(args.output).absolute()
    output.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".kernel-tools-", dir=output.parent) as temporary:
        state = Path(temporary)
        digest = runner.stage(Path(args.manifest), state)
        settings = json.loads((state / "src/peios/build-settings.json").read_text())
        (state / "temp").mkdir()
        command = runner.docker_args(settings)
        command += [
            "--mount",
            f"type=bind,src={state},dst=/work",
            "--mount",
            f"type=bind,src={output},dst=/output",
            "-e",
            "TMPDIR=/work/temp",
            "-e",
            "PEIOS_TOOLS_WORK=/work/tool-source",
            "-e",
            f"PEIOS_JOBS={settings['jobs']}",
            "-e",
            f"SOURCE_DATE_EPOCH={settings['source_date_epoch']}",
            "-e",
            f"KBUILD_BUILD_TIMESTAMP=@{settings['source_date_epoch']}",
            "-e",
            "CFLAGS=-O2 -g -pipe -fexceptions -Wall -Werror=format-security -Wp,-D_FORTIFY_SOURCE=3 -fstack-clash-protection -fcf-protection -gno-record-gcc-switches -fdebug-prefix-map=/work/tool-source=/usr/src/debug/kernel-tools -ffile-prefix-map=/work/tool-source=/usr/src/debug/kernel-tools",
            "-e",
            "CXXFLAGS=-O2 -g -pipe -fexceptions -fstack-clash-protection -fcf-protection -ffile-prefix-map=/work/tool-source=/usr/src/debug/kernel-tools",
            "-e",
            "LDFLAGS=-Wl,-z,relro -Wl,-z,now -Wl,--as-needed -Wl,-z,pack-relative-relocs -Wl,--build-id=sha1",
            settings["image"],
            "bash",
            "/work/src/peios/packages/build-tools.sh",
            "/work/src",
            "/output/root",
        ]
        runner.run_container(command)
        (output / "build.json").write_text(
            json.dumps(
                {
                    "image": settings["image"],
                    "input_digest": digest,
                    "userspace_abi": "debian-development",
                    "release_ready": False,
                },
                indent=2,
            )
            + "\n"
        )


def kernel(args: argparse.Namespace) -> None:
    output = Path(args.output).absolute()
    output.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".kernel-package-", dir=output.parent) as temporary:
        state = Path(temporary)
        runner.stage(Path(args.manifest), state)
        settings = json.loads((state / "src/peios/build-settings.json").read_text())
        command = runner.docker_args(settings)
        command += [
            "--mount",
            f"type=bind,src={state},dst=/work",
            "--mount",
            f"type=bind,src={output},dst=/output",
            "--mount",
            f"type=bind,src={Path(args.kernel).absolute()},dst=/built,readonly",
            "--mount",
            f"type=bind,src={state}/src/peios/packages,dst=/recipe,readonly",
            "-e",
            f"SOURCE_DATE_EPOCH={settings['source_date_epoch']}",
            settings["image"],
            "python3",
            "/recipe/stage-kernel.py",
        ]
        runner.run_container(command)


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(143))
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=["tools", "kernel"])
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--kernel")
    args = parser.parse_args()
    if args.stage == "kernel" and not args.kernel:
        parser.error("--kernel is required for the kernel stage")
    {"tools": tools, "kernel": kernel}[args.stage](args)
