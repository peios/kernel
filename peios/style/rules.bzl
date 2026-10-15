"""Local style and Cargo commands shared by developer workflows and CI."""

def _command_impl(ctx):
    launcher = ctx.actions.declare_file(ctx.label.name + ".sh")
    if ctx.attr.workspace:
        directory = '"${BUILD_WORKSPACE_DIRECTORY:?Run this target with bazel run}"'
    else:
        directory = '"${RUNFILES_DIR:-$0.runfiles}/%s"' % ctx.workspace_name
    ctx.actions.write(
        launcher,
        "#!/bin/bash\nset -euo pipefail\ncd %s\n%s\n" % (directory, ctx.attr.command),
        is_executable = True,
    )
    return [RunEnvironmentInfo(
        inherited_environment = ["PATH", "HOME", "RUSTUP_HOME", "CARGO_HOME", "PEIOS_STYLE_CACHE"],
    ), DefaultInfo(
        executable = launcher,
        runfiles = ctx.runfiles(files = ctx.files.srcs),
    )]

_attrs = {
    "command": attr.string(mandatory = True),
    "srcs": attr.label_list(allow_files = True),
    "workspace": attr.bool(default = False),
}

local_command = rule(implementation = _command_impl, attrs = _attrs, executable = True)
local_test = rule(implementation = _command_impl, attrs = _attrs, test = True)
