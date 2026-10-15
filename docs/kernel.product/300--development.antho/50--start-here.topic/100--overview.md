---
title: "Developing the kernel"
type: guide
description: "Find build, programming, testing and maintenance guidance."
---

Use this section when changing the kernel or investigating its behaviour.

1. **Build and program:** start with [Building Peios](<~kernel/development/start-here/building-peios>), then the [Build system](<~kernel/development/kbuild/index>),
   [Kernel programming](<~kernel/development/kernel-hacking/index>) and
   [Rust](<~kernel/development/rust/index>) guidance.
2. **Test the change:** the [Development tools](<~kernel/development/dev-tools/index>)
   collection includes KUnit, selftests, sanitizers and static analysis.
   [Fault injection](<~kernel/development/fault-injection/index>) exercises error paths.
3. **Observe the result:** use [Tracing](<~kernel/development/trace/index>) for runtime
   behaviour and [Livepatch](<~kernel/development/livepatch/index>) for live code changes.
4. **Prepare and maintain the work:** consult the [Development process](<~kernel/development/process/index>),
   [Maintainer guidance](<~kernel/development/maintainer/index>) and
   [Documentation workflow](<~kernel/development/doc-guide/maintaining-peios-documentation>).

The inherited process material describes Linux upstream contribution practices.
For work in the Peios repositories, also follow the workspace's `_styleguide`
and the instructions in the repository you are changing.
