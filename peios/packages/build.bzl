"""Kernel-family build stages; package assembly is separate from compilation."""

def _tools_impl(ctx):
    files = depset(ctx.files.srcs + ctx.files._recipe).to_list()
    manifest = ctx.actions.declare_file(ctx.label.name + ".inputs.json")
    ctx.actions.write(manifest, json.encode([
        {"path": f.path, "relative": f.short_path}
        for f in files
    ]))
    output = ctx.actions.declare_directory(ctx.label.name)
    arguments = [
        ctx.file._driver.path,
        ctx.attr.stage,
        "--manifest",
        manifest.path,
        "--output",
        output.path,
    ]
    extra = []
    if ctx.attr.stage == "kernel":
        extra = ctx.files.kernel
        arguments += ["--kernel", extra[0].path]
    ctx.actions.run(
        executable = "/usr/bin/python3",
        arguments = arguments,
        inputs = depset(files + extra + [manifest, ctx.file._driver]),
        outputs = [output],
        env = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8"},
        execution_requirements = {"no-sandbox": "1", "no-remote-exec": "1"},
        mnemonic = "KernelPackagesStage",
        progress_message = "Preparing %s package contents in the development image" % ctx.attr.stage,
    )
    return [DefaultInfo(files = depset([output]))]

kernel_tools = rule(implementation = _tools_impl, attrs = {
    "srcs": attr.label_list(allow_files = True),
    "_recipe": attr.label(default = "//peios/packages:tools_recipe"),
    "_driver": attr.label(default = "//peios/packages:stages.py", allow_single_file = True),
    "stage": attr.string(default = "tools", values = ["tools"]),
})

kernel_content = rule(implementation = _tools_impl, attrs = {
    "srcs": attr.label_list(allow_files = True),
    "kernel": attr.label(mandatory = True),
    "_recipe": attr.label(default = "//peios/packages:kernel_recipe"),
    "_driver": attr.label(default = "//peios/packages:stages.py", allow_single_file = True),
    "stage": attr.string(default = "kernel", values = ["kernel"]),
})

def _assembly_test_impl(ctx):
    executable = ctx.actions.declare_file(ctx.label.name + ".sh")
    ctx.actions.write(executable, """#!/bin/bash
set -euo pipefail
exec /usr/bin/python3 "${RUNFILES_DIR:-$0.runfiles}/%s/%s"
""" % (ctx.workspace_name, ctx.file.main.short_path), is_executable = True)
    return [DefaultInfo(
        executable = executable,
        runfiles = ctx.runfiles(files = ctx.files.srcs + [ctx.file.main]),
    )]

package_assembly_test = rule(implementation = _assembly_test_impl, test = True, attrs = {
    "main": attr.label(allow_single_file = True, mandatory = True),
    "srcs": attr.label_list(allow_files = True),
})
