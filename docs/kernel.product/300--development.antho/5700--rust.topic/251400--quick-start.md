---
title: "Quick Start"
type: reference
description: "This document describes how to get started with kernel development in Rust."
---

<a id="rst-quick-start"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

This document describes how to get started with kernel development in Rust.

There are a few ways to install a Rust toolchain needed for kernel development. A simple way is to use the packages from your Linux distribution if they are suitable -- the first section below explains this approach. An advantage of this approach is that, typically, the distribution will match the LLVM used by Rust and Clang.

Another way is using the prebuilt stable versions of LLVM+Rust provided on [kernel.org](<https://kernel.org/pub/tools/llvm/rust/>)<a id="rst-kernel-org"></a>. These are the same slim and fast LLVM toolchains from [Getting LLVM](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/kbuild/llvm.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>) with versions of Rust added to them that Rust for Linux supports. Two sets are provided: the "latest LLVM" and "matching LLVM" (please see the link for more information).

Alternatively, the next two "Requirements" sections explain each component and how to install them through `rustup`, the standalone installers from Rust and/or building them.

The rest of the document explains other aspects on how to get started.

<a id="rst-distributions"></a>

## Distributions

<a id="rst-arch-linux"></a>

### Arch Linux

Arch Linux provides recent Rust releases and thus it should generally work out of the box, e.g.:



```text
pacman -S rust rust-src rust-bindgen
```

<a id="rst-debian"></a>

### Debian

Debian 13 (Trixie), as well as Testing and Debian Unstable (Sid) provide recent Rust releases and thus they should generally work out of the box, e.g.:



```text
apt install rustc rust-src bindgen rustfmt rust-clippy
```

<a id="rst-fedora-linux"></a>

### Fedora Linux

Fedora Linux provides recent Rust releases and thus it should generally work out of the box, e.g.:



```text
dnf install rust rust-src bindgen-cli rustfmt clippy
```

<a id="rst-gentoo-linux"></a>

### Gentoo Linux

Gentoo Linux (and especially the testing branch) provides recent Rust releases and thus it should generally work out of the box, e.g.:



```text
USE='rust-src rustfmt clippy' emerge dev-lang/rust dev-util/bindgen
```

`LIBCLANG_PATH` may need to be set.

<a id="rst-nix"></a>

### Nix

Nix (unstable channel) provides recent Rust releases and thus it should generally work out of the box, e.g.:



```text
{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
  nativeBuildInputs = with pkgs; [ rustc rust-bindgen rustfmt clippy ];
  RUST_LIB_SRC = "${pkgs.rust.packages.stable.rustPlatform.rustLibSrc}";
}
```

<a id="rst-opensuse"></a>

### openSUSE

openSUSE Slowroll and openSUSE Tumbleweed provide recent Rust releases and thus they should generally work out of the box, e.g.:



```text
zypper install rust rust1.79-src rust-bindgen clang
```

<a id="rst-ubuntu"></a>

### Ubuntu

<a id="rst-section-1"></a>

#### 25.04

The latest Ubuntu releases provide recent Rust releases and thus they should generally work out of the box, e.g.:



```text
apt install rustc rust-src bindgen rustfmt rust-clippy
```

In addition, `RUST_LIB_SRC` needs to be set, e.g.:



```text
RUST_LIB_SRC=/usr/src/rustc-$(rustc --version | cut -d' ' -f2)/library
```

For convenience, `RUST_LIB_SRC` can be exported to the global environment.

<a id="rst-lts-and-older"></a>

#### 24.04 LTS and older

Though Ubuntu 24.04 LTS and older versions still provide recent Rust releases, they require some additional configuration to be set, using the versioned packages, e.g.:



```text
apt install rustc-1.80 rust-1.80-src bindgen-0.65 rustfmt-1.80 \
        rust-1.80-clippy
ln -s /usr/lib/rust-1.80/bin/rustfmt /usr/bin/rustfmt-1.80
ln -s /usr/lib/rust-1.80/bin/clippy-driver /usr/bin/clippy-driver-1.80
```

None of these packages set their tools as defaults; therefore they should be specified explicitly, e.g.:



```text
make LLVM=1 RUSTC=rustc-1.80 RUSTDOC=rustdoc-1.80 RUSTFMT=rustfmt-1.80 \
        CLIPPY_DRIVER=clippy-driver-1.80 BINDGEN=bindgen-0.65
```

Alternatively, modify the `PATH` variable to place the Rust 1.80 binaries first and set `bindgen` as the default, e.g.:



```text
PATH=/usr/lib/rust-1.80/bin:$PATH
update-alternatives --install /usr/bin/bindgen bindgen \
        /usr/bin/bindgen-0.65 100
update-alternatives --set bindgen /usr/bin/bindgen-0.65
```

`RUST_LIB_SRC` needs to be set when using the versioned packages, e.g.:



```text
RUST_LIB_SRC=/usr/src/rustc-$(rustc-1.80 --version | cut -d' ' -f2)/library
```

For convenience, `RUST_LIB_SRC` can be exported to the global environment.

In addition, `bindgen-0.65` is available in newer releases (24.04 LTS and 24.10), but it may not be available in older ones (20.04 LTS and 22.04 LTS), thus `bindgen` may need to be built manually (please see below).

<a id="rst-requirements-building"></a>

## Requirements: Building

This section explains how to fetch the tools needed for building.

To easily check whether the requirements are met, the following target can be used:



```text
make LLVM=1 rustavailable
```

This triggers the same logic used by Kconfig to determine whether `RUST_IS_AVAILABLE` should be enabled; but it also explains why not if that is the case.

<a id="rst-rustc"></a>

### rustc

A recent version of the Rust compiler is required.

If `rustup` is being used, enter the kernel build directory (or use `--path=<build-dir>` argument to the `set` sub-command) and run, for instance:



```text
rustup override set stable
```

This will configure your working directory to use the given version of `rustc` without affecting your default toolchain.

Note that the override applies to the current working directory (and its sub-directories).

If you are not using `rustup`, fetch a standalone installer from:

> [https://forge.rust-lang.org/infra/other-installation-methods.html\#standalone](<https://forge.rust-lang.org/infra/other-installation-methods.html#standalone>)

<a id="rst-rust-standard-library-source"></a>

### Rust standard library source

The Rust standard library source is required because the build system will cross-compile `core`.

If `rustup` is being used, run:



```text
rustup component add rust-src
```

The components are installed per toolchain, thus upgrading the Rust compiler version later on requires re-adding the component.

Otherwise, if a standalone installer is used, the Rust source tree may be downloaded into the toolchain's installation folder:



```text
curl -L "https://static.rust-lang.org/dist/rust-src-$(rustc --version | cut -d' ' -f2).tar.gz" |
        tar -xzf - -C "$(rustc --print sysroot)/lib" \
        "rust-src-$(rustc --version | cut -d' ' -f2)/rust-src/lib/" \
        --strip-components=3
```

In this case, upgrading the Rust compiler version later on requires manually updating the source tree (this can be done by removing `$(rustc --print sysroot)/lib/rustlib/src/rust` then rerunning the above command).

<a id="rst-libclang"></a>

### libclang

`libclang` (part of LLVM) is used by `bindgen` to understand the C code in the kernel, which means LLVM needs to be installed; like when the kernel is compiled with `LLVM=1`.

Linux distributions are likely to have a suitable one available, so it is best to check that first.

There are also some binaries for several systems and architectures uploaded at:

> [https://releases.llvm.org/download.html](<https://releases.llvm.org/download.html>)

Otherwise, building LLVM takes quite a while, but it is not a complex process:

> [https://llvm.org/docs/GettingStarted.html\#getting-the-source-code-and-building-llvm](<https://llvm.org/docs/GettingStarted.html#getting-the-source-code-and-building-llvm>)

Please see [Documentation/kbuild/llvm.rst](https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/kbuild/llvm.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92) for more information and further ways to fetch pre-built releases and distribution packages.

<a id="rst-bindgen"></a>

### bindgen

The bindings to the C side of the kernel are generated at build time using the `bindgen` tool.

Install it, for instance, via (note that this will download and build the tool from source):



```text
cargo install --locked bindgen-cli
```

`bindgen` uses the `clang-sys` crate to find a suitable `libclang` (which may be linked statically, dynamically or loaded at runtime). By default, the `cargo` command above will produce a `bindgen` binary that will load `libclang` at runtime. If it is not found (or a different `libclang` than the one found should be used), the process can be tweaked, e.g. by using the `LIBCLANG_PATH` environment variable. For details, please see `clang-sys`'s documentation at:

> [https://github.com/KyleMayes/clang-sys\#linking](<https://github.com/KyleMayes/clang-sys#linking>)
>
> [https://github.com/KyleMayes/clang-sys\#environment-variables](<https://github.com/KyleMayes/clang-sys#environment-variables>)

<a id="rst-requirements-developing"></a>

## Requirements: Developing

This section explains how to fetch the tools needed for developing. That is, they are not needed when just building the kernel.

<a id="rst-rustfmt"></a>

### rustfmt

The `rustfmt` tool is used to automatically format all the Rust kernel code, including the generated C bindings (for details, please see [coding-guidelines.rst](~kernel/development/rust/coding-guidelines)).

If `rustup` is being used, its `default` profile already installs the tool, thus nothing needs to be done. If another profile is being used, the component can be installed manually:



```text
rustup component add rustfmt
```

The standalone installers also come with `rustfmt`.

<a id="rst-clippy"></a>

### clippy

`clippy` is a Rust linter. Running it provides extra warnings for Rust code. It can be run by passing `CLIPPY=1` to `make` (for details, please see [general-information.rst](~kernel/development/rust/general-information)).

If `rustup` is being used, its `default` profile already installs the tool, thus nothing needs to be done. If another profile is being used, the component can be installed manually:



```text
rustup component add clippy
```

The standalone installers also come with `clippy`.

<a id="rst-rustdoc"></a>

### rustdoc

`rustdoc` is the documentation tool for Rust. It generates pretty HTML documentation for Rust code (for details, please see [general-information.rst](~kernel/development/rust/general-information)).

`rustdoc` is also used to test the examples provided in documented Rust code (called doctests or documentation tests). The `rusttest` Make target uses this feature.

If `rustup` is being used, all the profiles already install the tool, thus nothing needs to be done.

The standalone installers also come with `rustdoc`.

<a id="rst-rust-analyzer"></a>

### rust-analyzer

The [rust-analyzer](<https://rust-analyzer.github.io/>)<a id="rst-rust-analyzer-1"></a> language server can be used with many editors to enable syntax highlighting, completion, go to definition, and other features.

`rust-analyzer` needs a configuration file, `rust-project.json`, which can be generated by the `rust-analyzer` Make target:



```text
make LLVM=1 rust-analyzer
```

<a id="rst-configuration"></a>

## Configuration

`Rust support` (`CONFIG_RUST`) needs to be enabled in the `General setup` menu. The option is only shown if a suitable Rust toolchain is found (see above), as long as the other requirements are met. In turn, this will make visible the rest of options that depend on Rust.

Afterwards, go to:



```text
Kernel hacking
    -> Sample kernel code
        -> Rust samples
```

And enable some sample modules either as built-in or as loadable.

<a id="rst-building"></a>

## Building

Building a kernel with a complete LLVM toolchain is the best supported setup at the moment. That is:



```text
make LLVM=1
```

Using GCC also works for some configurations, but it is very experimental at the moment.

<a id="rst-hacking"></a>

## Hacking

To dive deeper, take a look at the source code of the samples at `samples/rust/`, the Rust support code under `rust/` and the `Rust hacking` menu under `Kernel hacking`.

If GDB/Binutils is used and Rust symbols are not getting demangled, the reason is the toolchain does not support Rust's new v0 mangling scheme yet. There are a few ways out:

- Install a newer release (GDB &gt;= 10.2, Binutils &gt;= 2.36).

- Some versions of GDB (e.g. vanilla GDB 10.1) are able to use the pre-demangled names embedded in the debug info (`CONFIG_DEBUG_INFO`).
