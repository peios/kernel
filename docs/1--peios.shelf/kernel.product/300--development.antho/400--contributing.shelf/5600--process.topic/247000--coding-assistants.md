---
title: "AI Coding Assistants"
type: reference
description: "This document provides guidance for AI tools and developers using AI assistance when contributing to the Linux kernel."
---

> **Peios:** This is inherited Linux development and upstream contribution guidance. For Peios repository changes, follow [Peios Standards and Conventions](https://learn.peios.org/psc/) and use [Building Peios](<~kernel/development/start-here/building-peios>). Upstream mailing lists, maintainer roles and release processes below apply when contributing to Linux upstream.


<a id="rst-ai-coding-assistants"></a>
<a id="rst-coding-assistants"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

This document provides guidance for AI tools and developers using AI assistance when contributing to the Linux kernel.

AI tools helping with Linux kernel development should follow the standard kernel development process:

- [Documentation/process/development-process.rst](~kernel/development/process/development-process)

- [Documentation/process/coding-style.rst](https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/process/coding-style.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92)

- [Documentation/process/submitting-patches.rst](~kernel/development/process/submitting-patches)

<a id="rst-licensing-and-legal-requirements"></a>

## Licensing and Legal Requirements

All contributions must comply with the kernel's licensing requirements:

- All code must be compatible with GPL-2.0-only

- Use appropriate SPDX license identifiers

- See [Documentation/process/license-rules.rst](https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/process/license-rules.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92) for details

<a id="rst-signed-off-by-and-developer-certificate-of-origin"></a>

## Signed-off-by and Developer Certificate of Origin

AI agents MUST NOT add Signed-off-by tags. Only humans can legally certify the Developer Certificate of Origin (DCO). The human submitter is responsible for:

- Reviewing all AI-generated code

- Ensuring compliance with licensing requirements

- Adding their own Signed-off-by tag to certify the DCO

- Taking full responsibility for the contribution

<a id="rst-attribution"></a>

## Attribution

When AI tools contribute to kernel development, proper attribution helps track the evolving role of AI in the development process. Contributions should include an Assisted-by tag in the following format:



```text
Assisted-by: AGENT_NAME:MODEL_VERSION [TOOL1] [TOOL2]
```

Where:

- `AGENT_NAME` is the name of the AI tool or framework

- `MODEL_VERSION` is the specific model version used

- `[TOOL1] [TOOL2]` are optional specialized analysis tools used (e.g., coccinelle, sparse, smatch, clang-tidy)

Basic development tools (git, gcc, make, editors) should not be listed.

Example:



```text
Assisted-by: Claude:claude-3-opus coccinelle sparse
```
