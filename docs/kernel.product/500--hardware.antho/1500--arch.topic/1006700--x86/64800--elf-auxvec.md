---
title: "x86-specific ELF Auxiliary Vectors"
type: reference
description: "This document describes the semantics of the x86 auxiliary vectors."
---

<a id="rst-x86-specific-elf-auxiliary-vectors"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

This document describes the semantics of the x86 auxiliary vectors.

<a id="rst-introduction"></a>

## Introduction

ELF Auxiliary vectors enable the kernel to efficiently provide configuration-specific parameters to userspace. In this example, a program allocates an alternate stack based on the kernel-provided size:



```text
#include <sys/auxv.h>
#include <elf.h>
#include <signal.h>
#include <stdlib.h>
#include <assert.h>
#include <err.h>

#ifndef AT_MINSIGSTKSZ
#define AT_MINSIGSTKSZ       51
#endif

....
stack_t ss;

ss.ss_sp = malloc(ss.ss_size);
assert(ss.ss_sp);

ss.ss_size = getauxval(AT_MINSIGSTKSZ) + SIGSTKSZ;
ss.ss_flags = 0;

if (sigaltstack(&ss, NULL))
     err(1, "sigaltstack");
```

<a id="rst-the-exposed-auxiliary-vectors"></a>

## The exposed auxiliary vectors

AT_SYSINFO is used for locating the vsyscall entry point.  It is not exported on 64-bit mode.

AT_SYSINFO_EHDR is the start address of the page containing the vDSO.

AT_MINSIGSTKSZ denotes the minimum stack size required by the kernel to deliver a signal to user-space.  AT_MINSIGSTKSZ comprehends the space consumed by the kernel to accommodate the user context for the current hardware configuration.  It does not comprehend subsequent user-space stack consumption, which must be added by the user.  (e.g. Above, user-space adds SIGSTKSZ to AT_MINSIGSTKSZ.)
