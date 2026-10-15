"""A real TreeArtifact to exercise package assembly across Bazel actions."""

def _fixture_impl(ctx):
    output = ctx.actions.declare_directory(ctx.label.name)
    ctx.actions.run_shell(
        outputs = [output],
        arguments = [output.path],
        command = """set -eu
mkdir -p "$1/root/usr/bin"
printf 'fixture payload\n' > "$1/root/usr/bin/probe"
chmod 755 "$1/root/usr/bin/probe"
ln -s probe "$1/root/usr/bin/probe-alias"
printf '{"release_ready":false}\n' > "$1/build.json"
""",
    )
    return [DefaultInfo(files = depset([output]))]

fixture_stage = rule(implementation = _fixture_impl)
