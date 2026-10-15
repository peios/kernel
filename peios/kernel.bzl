"""Linux-local Kbuild actions and an explicitly incremental developer command."""

def _manifest(ctx):
    files = depset(ctx.files.srcs + ctx.files._recipe).to_list()
    manifest = ctx.actions.declare_file(ctx.label.name + ".inputs.json")
    ctx.actions.write(manifest, json.encode([
        {"path": f.path, "relative": f.short_path}
        for f in files
    ]))
    return files, manifest

def _build_impl(ctx):
    files, manifest = _manifest(ctx)
    out = ctx.actions.declare_directory(ctx.label.name)
    ctx.actions.run(
        executable = "/usr/bin/python3",
        arguments = [
            ctx.file._runner.path,
            "build",
            "--manifest",
            manifest.path,
            "--profile",
            ctx.attr.profile,
            "--output",
            out.path,
        ],
        inputs = depset(files + [manifest, ctx.file._runner]),
        outputs = [out],
        env = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8"},
        execution_requirements = {"no-sandbox": "1", "no-remote-exec": "1"},
        mnemonic = "Kbuild",
        progress_message = "Building %s kernel with pinned Kbuild toolchain" % ctx.attr.profile,
    )
    return [DefaultInfo(files = depset([out]))]

def _launcher(ctx, arguments, files):
    executable = ctx.actions.declare_file(ctx.label.name + ".sh")
    ctx.actions.write(executable, """#!/bin/bash
set -euo pipefail
cd "${RUNFILES_DIR:-$0.runfiles}/%s"
exec /usr/bin/python3 %s %s "$@"
""" % (ctx.workspace_name, ctx.file._runner.short_path, arguments), is_executable = True)
    return [DefaultInfo(
        executable = executable,
        runfiles = ctx.runfiles(files = files + [ctx.file._runner]),
    )]

def _dev_impl(ctx):
    _, manifest = _manifest(ctx)
    return _launcher(ctx, "dev --manifest " + manifest.short_path, [manifest])

def _test_impl(ctx):
    kernel = ctx.files.kernel[0]
    return _launcher(
        ctx,
        "test --kernel " + kernel.short_path,
        [kernel] + ctx.files._recipe,
    )

_common = {
    "_runner": attr.label(default = "//peios:runner.py", allow_single_file = True),
    "_recipe": attr.label(default = "//peios:recipe"),
}
_sources = dict(_common, srcs = attr.label_list(allow_files = True))
kernel_build = rule(implementation = _build_impl, attrs = dict(
    _sources,
    profile = attr.string(values = ["production", "kunit"], mandatory = True),
))
kernel_dev = rule(implementation = _dev_impl, attrs = _sources, executable = True)
kernel_test = rule(implementation = _test_impl, attrs = dict(
    _common,
    kernel = attr.label(mandatory = True),
), test = True)
