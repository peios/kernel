---
title: "GPU RFC Section"
type: reference
description: "For complex work, especially new uapi, it is often good to nail the high level design issues before getting lost in the code details. This section is meant to host such documentation:"
---

<a id="rst-gpu-rfc-section"></a>

For complex work, especially new uapi, it is often good to nail the high level design issues before getting lost in the code details. This section is meant to host such documentation:

- Each RFC should be a section in this file, explaining the goal and main design considerations. Especially for uapi make sure you Cc: all relevant project mailing lists and involved people outside of dri-devel.

- For uapi structures add a file to this directory with and then pull the kerneldoc in like with real uapi headers.

- Once the code has landed move all the documentation to the right places in the main core, helper or driver sections.

- [GPU SVM Section](<~kernel/hardware/gpu/rfc/gpusvm>)

- [I915 DG1/LMEM RFC Section](<~kernel/hardware/gpu/rfc/i915-gem-lmem>)

- [i915_scheduler](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/gpu/rfc/i915_scheduler.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>)

- [I915 Small BAR RFC Section](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/gpu/rfc/i915_small_bar.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>)

- [I915 VM_BIND feature design and use cases](<~kernel/hardware/gpu/rfc/i915-vm-bind>)

- [Linux Color Pipeline API](<~kernel/hardware/gpu/rfc/color-pipeline>)
