---
title: "Arch Support"
type: reference
description: "Currently, the Rust compiler (rustc) uses LLVM for code generation, which limits the supported architectures that can be targeted. In addition, support for building the kernel with LLVM/Clang varies (please see…"
---

<a id="rst-arch-support"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

Currently, the Rust compiler (`rustc`) uses LLVM for code generation, which limits the supported architectures that can be targeted. In addition, support for building the kernel with LLVM/Clang varies (please see [Documentation/kbuild/llvm.rst](https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/kbuild/llvm.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92)). This support is needed for `bindgen` which uses `libclang`.

Below is a general summary of architectures that currently work. Level of support corresponds to `S` values in the `MAINTAINERS` file.


<table>
<thead>
<tr>
<th>


Architecture

</th>
<th>


Level of support

</th>
<th>


Constraints

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


`arm`

</td>
<td>


Maintained

</td>
<td>


ARMv7 Little Endian only.

</td>
</tr>
<tr>
<td>


`arm64`

</td>
<td>


Maintained

</td>
<td>


Little Endian only.

</td>
</tr>
<tr>
<td>


`loongarch`

</td>
<td>


Maintained

</td>
<td>


\-

</td>
</tr>
<tr>
<td>


`riscv`

</td>
<td>


Maintained

</td>
<td>


`riscv64` and LLVM/Clang only.

</td>
</tr>
<tr>
<td>


`um`

</td>
<td>


Maintained

</td>
<td>


\-

</td>
</tr>
<tr>
<td>


`x86`

</td>
<td>


Maintained

</td>
<td>


`x86_64` only.

</td>
</tr>
</tbody>
</table>
