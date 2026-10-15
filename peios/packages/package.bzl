"""Independent ppk commits and a deduplicated, verified family store."""

load(":versions.bzl", "DEFAULT_VERSION", "PACKAGE_VERSIONS")

def _package_impl(ctx):
    output = ctx.actions.declare_directory(ctx.label.name + ".ppk")
    inputs = ctx.files.data + ctx.files.srcs
    args = [
        ctx.file._driver.path,
        "commit",
        "--output",
        output.path,
        "--writer",
        ctx.executable._writer.path,
        "--version",
        ctx.attr.version,
        "--data",
        ctx.file._base.dirname + "/../data",
        "--base",
        ctx.file._base.path,
    ]
    inputs += [ctx.file._base, ctx.file._driver, ctx.file._assembly]
    if ctx.attr.source:
        manifest = ctx.actions.declare_file(ctx.label.name + ".inputs.json")
        ctx.actions.write(manifest, json.encode([
            {"path": f.path, "relative": f.short_path}
            for f in ctx.files.srcs
        ]))
        inputs.append(manifest)
        args += ["--source-manifest", manifest.path]
    else:
        inputs.append(ctx.file.definition)
        args += ["--definition", ctx.file.definition.path]
    if ctx.attr.kernel:
        inputs += ctx.files.kernel
        args += ["--kernel", ctx.files.kernel[0].path]
    if ctx.attr.tools:
        inputs += ctx.files.tools
        args += ["--tools", ctx.files.tools[0].path]
    ctx.actions.run(
        executable = "/usr/bin/python3",
        arguments = args,
        inputs = depset(inputs),
        tools = [ctx.executable._writer],
        outputs = [output],
        env = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8"},
        # TreeArtifact sandbox leaves are transport symlinks. Assembly must
        # see the actual declared tree to preserve its real payload symlinks.
        execution_requirements = {"no-sandbox": "1", "no-remote-exec": "1"},
        mnemonic = "PpkCommit",
        progress_message = "Committing %s blobs and manifest" % ctx.label.name,
    )
    return [DefaultInfo(files = depset([output]))]

kernel_package = rule(implementation = _package_impl, attrs = {
    "definition": attr.label(allow_single_file = True),
    "version": attr.string(default = DEFAULT_VERSION),
    "kernel": attr.label(),
    "tools": attr.label(),
    "source": attr.bool(),
    "srcs": attr.label_list(allow_files = True),
    "data": attr.label_list(allow_files = True),
    "_base": attr.label(default = "//peios/packages:legacy/package.pekit.toml", allow_single_file = True),
    "_driver": attr.label(default = "//peios/packages:package.py", allow_single_file = True),
    "_assembly": attr.label(default = "//peios/packages:assembly.py", allow_single_file = True),
    "_writer": attr.label(default = "//peios/vendor/ppk:ppk", executable = True, cfg = "exec"),
})

def _store_impl(ctx):
    output = ctx.actions.declare_directory(ctx.label.name)
    args = [
        ctx.file._driver.path,
        "merge",
        "--output",
        output.path,
        "--checker",
        ctx.executable._checker.path,
    ]
    for f in ctx.files.packages:
        args += ["--store", f.path]
    ctx.actions.run(
        executable = "/usr/bin/python3",
        arguments = args,
        inputs = depset(ctx.files.packages + [ctx.file._driver, ctx.file._assembly]),
        tools = [ctx.executable._checker],
        outputs = [output],
        env = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8"},
        execution_requirements = {"no-remote-exec": "1"},
        mnemonic = "PpkStore",
        progress_message = "Assembling and verifying the kernel package store",
    )
    return [DefaultInfo(files = depset([output]))]

package_store = rule(implementation = _store_impl, attrs = {
    "packages": attr.label_list(mandatory = True),
    "_driver": attr.label(default = "//peios/packages:package.py", allow_single_file = True),
    "_assembly": attr.label(default = "//peios/packages:assembly.py", allow_single_file = True),
    "_checker": attr.label(default = "//peios/packages:check-blobs", executable = True, cfg = "exec"),
})

def _store_test_impl(ctx):
    executable = ctx.actions.declare_file(ctx.label.name + ".sh")
    ctx.actions.write(executable, """#!/bin/bash
set -euo pipefail
root="${RUNFILES_DIR:-$0.runfiles}/%s"
export PPK_WRITER="$root/%s"
export PPK_CHECKER="$root/%s"
exec /usr/bin/python3 "$root/%s"
""" % (
        ctx.workspace_name,
        ctx.executable._writer.short_path,
        ctx.executable._checker.short_path,
        ctx.file.main.short_path,
    ), is_executable = True)
    return [DefaultInfo(executable = executable, runfiles = ctx.runfiles(
        files = ctx.files.srcs + [ctx.file.main, ctx.executable._writer, ctx.executable._checker],
    ))]

package_store_test = rule(implementation = _store_test_impl, test = True, attrs = {
    "main": attr.label(allow_single_file = True, mandatory = True),
    "srcs": attr.label_list(allow_files = True),
    "_writer": attr.label(default = "//peios/vendor/ppk:ppk", executable = True, cfg = "exec"),
    "_checker": attr.label(default = "//peios/packages:check-blobs", executable = True, cfg = "exec"),
})

def kernel_package_family():
    """Declare every kernel package using the shared version catalogue."""
    targets = []
    names = []
    for definition in native.glob(["legacy/*.package.pekit.toml"]):
        name = definition[len("legacy/"):-len(".package.pekit.toml")]
        names.append(name)
        kernel = name == "kernel" or name.startswith("kernel-")
        tools = not kernel or name == "kernel-tools-debuginfo"
        kernel_package(
            name = name,
            definition = definition,
            version = PACKAGE_VERSIONS.get(name, DEFAULT_VERSION),
            kernel = "//:kernel-package-content" if kernel else None,
            tools = "//:kernel-tools" if tools else None,
            data = native.glob(["data/**"]),
        )
        targets.append(":" + name)
    for name in PACKAGE_VERSIONS:
        if name not in names + ["kernel-source"]:
            fail("Unknown package version override: " + name)
    kernel_package(
        name = "kernel-source",
        source = True,
        version = PACKAGE_VERSIONS.get("kernel-source", DEFAULT_VERSION),
        srcs = ["//:package-sources"],
    )
    native.filegroup(name = "all", srcs = targets + [":kernel-source"])
