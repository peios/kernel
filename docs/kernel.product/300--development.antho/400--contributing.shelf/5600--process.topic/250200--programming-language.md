---
title: "Programming Language"
type: reference
description: "The Linux kernel is written in the C programming language c-language. More precisely, it is typically compiled with gcc gcc under -std=gnu11 gcc-c-dialect-options: the GNU dialect of ISO C11. clang clang is also supported; see…"
---

> **Peios:** This is inherited Linux development and upstream contribution guidance. For Peios repository changes, follow the workspace `_styleguide` and use [Building Peios](<~kernel/development/start-here/building-peios>). Upstream mailing lists, maintainer roles and release processes below apply when contributing to Linux upstream.


<a id="rst-programming-language-1"></a>
<a id="rst-programming-language"></a>

The Linux kernel is written in the C programming language <a id="rst-citation-reference-1"></a>[c-language](#rst-c-language). More precisely, it is typically compiled with `gcc` <a id="rst-citation-reference-2"></a>[gcc](#rst-gcc) under `-std=gnu11` <a id="rst-citation-reference-3"></a>[gcc-c-dialect-options](#rst-gcc-c-dialect-options): the GNU dialect of ISO C11. `clang` <a id="rst-citation-reference-4"></a>[clang](#rst-clang) is also supported; see documentation on [Building Linux with Clang/LLVM](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/kbuild/llvm.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>).

This dialect contains many extensions to the language <a id="rst-citation-reference-5"></a>[gnu-extensions](#rst-gnu-extensions), and many of them are used within the kernel as a matter of course.

<a id="rst-attributes"></a>

## Attributes

One of the common extensions used throughout the kernel are attributes <a id="rst-citation-reference-6"></a>[gcc-attribute-syntax](#rst-gcc-attribute-syntax). Attributes allow to introduce implementation-defined semantics to language entities (like variables, functions or types) without having to make significant syntactic changes to the language (e.g. adding a new keyword) <a id="rst-citation-reference-7"></a>[n2049](#rst-n2049).

In some cases, attributes are optional (i.e. a compiler not supporting them should still produce proper code, even if it is slower or does not perform as many compile-time checks/diagnostics).

The kernel defines pseudo-keywords (e.g. `__pure`) instead of using directly the GNU attribute syntax (e.g. `__attribute__((__pure__))`) in order to feature detect which ones can be used and/or to shorten the code.

Please refer to `include/linux/compiler_attributes.h` for more information.

<a id="rst-rust"></a>

## Rust

The kernel has support for the Rust programming language <a id="rst-citation-reference-8"></a>[rust-language](#rst-rust-language) under `CONFIG_RUST`. It is compiled with `rustc` <a id="rst-citation-reference-9"></a>[rustc](#rst-rustc) under `--edition=2021` <a id="rst-citation-reference-10"></a>[rust-editions](#rst-rust-editions). Editions are a way to introduce small changes to the language that are not backwards compatible.

On top of that, some unstable features <a id="rst-citation-reference-11"></a>[rust-unstable-features](#rst-rust-unstable-features) are used in the kernel. Unstable features may change in the future, thus it is an important goal to reach a point where only stable features are used.

Please refer to [Documentation/rust/index.rst](https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/rust/index.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92) for more information.

<a id="rst-c-language"></a>



**[c-language]** [http://www.open-std.org/jtc1/sc22/wg14/www/standards](<http://www.open-std.org/jtc1/sc22/wg14/www/standards>)

<a id="rst-gcc"></a>



**[gcc]** [https://gcc.gnu.org](<https://gcc.gnu.org>)

<a id="rst-clang"></a>



**[clang]** [https://clang.llvm.org](<https://clang.llvm.org>)

<a id="rst-gcc-c-dialect-options"></a>



**[gcc-c-dialect-options]** [https://gcc.gnu.org/onlinedocs/gcc/C-Dialect-Options.html](<https://gcc.gnu.org/onlinedocs/gcc/C-Dialect-Options.html>)

<a id="rst-gnu-extensions"></a>



**[gnu-extensions]** [https://gcc.gnu.org/onlinedocs/gcc/C-Extensions.html](<https://gcc.gnu.org/onlinedocs/gcc/C-Extensions.html>)

<a id="rst-gcc-attribute-syntax"></a>



**[gcc-attribute-syntax]** [https://gcc.gnu.org/onlinedocs/gcc/Attribute-Syntax.html](<https://gcc.gnu.org/onlinedocs/gcc/Attribute-Syntax.html>)

<a id="rst-n2049"></a>



**[n2049]** [http://www.open-std.org/jtc1/sc22/wg14/www/docs/n2049.pdf](<http://www.open-std.org/jtc1/sc22/wg14/www/docs/n2049.pdf>)

<a id="rst-rust-language"></a>



**[rust-language]** [https://www.rust-lang.org](<https://www.rust-lang.org>)

<a id="rst-rustc"></a>



**[rustc]** [https://doc.rust-lang.org/rustc/](<https://doc.rust-lang.org/rustc/>)

<a id="rst-rust-editions"></a>



**[rust-editions]** [https://doc.rust-lang.org/edition-guide/editions/](<https://doc.rust-lang.org/edition-guide/editions/>)

<a id="rst-rust-unstable-features"></a>



**[rust-unstable-features]** [https://github.com/Rust-for-Linux/linux/issues/2](<https://github.com/Rust-for-Linux/linux/issues/2>)
