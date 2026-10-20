---
title: "Contents"
type: reference
description: "1 Clang implementation notes"
---

<a id="rst-contents"></a>



<a id="rst-clang-implementation-notes"></a>

## 1   Clang implementation notes

This document provides more details specific to the Clang/LLVM implementation of the eBPF instruction set.

<a id="rst-versions"></a>

### 1.1   Versions

Clang defined "CPU" versions, where a CPU version of 3 corresponds to the current eBPF ISA.

Clang can select the eBPF ISA version using `-mcpu=v3` for example to select version 3.

<a id="rst-arithmetic-instructions"></a>

### 1.2   Arithmetic instructions

For CPU versions prior to 3, Clang v7.0 and later can enable `BPF_ALU` support with `-Xclang -target-feature -Xclang +alu32`.  In CPU version 3, support is automatically included.

<a id="rst-jump-instructions"></a>

### 1.3   Jump instructions

If `-O0` is used, Clang will generate the `BPF_CALL | BPF_X | BPF_JMP` (0x8d) instruction, which is not supported by the Linux kernel verifier.

<a id="rst-atomic-operations"></a>

### 1.4   Atomic operations

Clang can generate atomic instructions by default when `-mcpu=v3` is enabled. If a lower version for `-mcpu` is set, the only atomic instruction Clang can generate is `BPF_ADD` <em>without</em> `BPF_FETCH`. If you need to enable the atomics features, while keeping a lower `-mcpu` version, you can use `-Xclang -target-feature -Xclang +alu32`.
