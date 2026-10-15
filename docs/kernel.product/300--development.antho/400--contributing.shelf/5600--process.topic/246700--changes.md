---
title: "Minimal requirements to compile the Kernel"
type: reference
description: "This document is designed to provide a list of the minimum levels of software necessary to run the current kernel version."
---

<a id="rst-minimal-requirements-to-compile-the-kernel"></a>
<a id="rst-changes"></a>

<a id="rst-intro"></a>

## Intro

This document is designed to provide a list of the minimum levels of software necessary to run the current kernel version.

This document is originally based on my "Changes" file for 2.0.x kernels and therefore owes credit to the same people as that file (Jared Mauch, Axel Boldt, Alessandro Sigala, and countless other users all over the 'net).

<a id="rst-current-minimal-requirements"></a>

### Current Minimal Requirements

Upgrade to at **least** these software revisions before thinking you've encountered a bug\!  If you're unsure what version you're currently running, the suggested command should tell you.

Again, keep in mind that this list assumes you are already functionally running a Linux kernel.  Also, not all tools are necessary on all systems; obviously, if you don't have any PC Card hardware, for example, you probably needn't concern yourself with pcmciautils.


<table>
<thead>
<tr>
<th>


Program

</th>
<th>


Minimal version

</th>
<th>


Command to check the version

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


GNU C

</td>
<td>


8.1

</td>
<td>


gcc --version

</td>
</tr>
<tr>
<td>


Clang/LLVM (optional)

</td>
<td>


15.0.0

</td>
<td>


clang --version

</td>
</tr>
<tr>
<td>


Rust (optional)

</td>
<td>


1.78.0

</td>
<td>


rustc --version

</td>
</tr>
<tr>
<td>


bindgen (optional)

</td>
<td>


0.65.1

</td>
<td>


bindgen --version

</td>
</tr>
<tr>
<td>


GNU make

</td>
<td>


4.0

</td>
<td>


make --version

</td>
</tr>
<tr>
<td>


bash

</td>
<td>


4.2

</td>
<td>


bash --version

</td>
</tr>
<tr>
<td>


binutils

</td>
<td>


2.30

</td>
<td>


ld -v

</td>
</tr>
<tr>
<td>


flex

</td>
<td>


2.5.35

</td>
<td>


flex --version

</td>
</tr>
<tr>
<td>


bison

</td>
<td>


2.0

</td>
<td>


bison --version

</td>
</tr>
<tr>
<td>


pahole

</td>
<td>


1.22

</td>
<td>


pahole --version

</td>
</tr>
<tr>
<td>


util-linux

</td>
<td>


2.10o

</td>
<td>


mount --version

</td>
</tr>
<tr>
<td>


kmod

</td>
<td>


13

</td>
<td>


depmod -V

</td>
</tr>
<tr>
<td>


e2fsprogs

</td>
<td>


1.41.4

</td>
<td>


e2fsck -V

</td>
</tr>
<tr>
<td>


jfsutils

</td>
<td>


1.1.3

</td>
<td>


fsck.jfs -V

</td>
</tr>
<tr>
<td>


xfsprogs

</td>
<td>


2.6.0

</td>
<td>


xfs_db -V

</td>
</tr>
<tr>
<td>


squashfs-tools

</td>
<td>


4.0

</td>
<td>


mksquashfs -version

</td>
</tr>
<tr>
<td>


btrfs-progs

</td>
<td>


0.18

</td>
<td>


btrfs --version

</td>
</tr>
<tr>
<td>


pcmciautils

</td>
<td>


004

</td>
<td>


pccardctl -V

</td>
</tr>
<tr>
<td>


quota-tools

</td>
<td>


3.09

</td>
<td>


quota -V

</td>
</tr>
<tr>
<td>


PPP

</td>
<td>


2.4.0

</td>
<td>


pppd --version

</td>
</tr>
<tr>
<td>


nfs-utils

</td>
<td>


1.0.5

</td>
<td>


showmount --version

</td>
</tr>
<tr>
<td>


procps

</td>
<td>


3.2.0

</td>
<td>


ps --version

</td>
</tr>
<tr>
<td>


udev

</td>
<td>


081

</td>
<td>


udevd --version

</td>
</tr>
<tr>
<td>


grub

</td>
<td>


0.93

</td>
<td>


grub --version \|\| grub-install --version

</td>
</tr>
<tr>
<td>


mcelog

</td>
<td>


0.6

</td>
<td>


mcelog --version

</td>
</tr>
<tr>
<td>


iptables

</td>
<td>


1.4.2

</td>
<td>


iptables -V

</td>
</tr>
<tr>
<td>


openssl &amp; libcrypto

</td>
<td>


1.0.0

</td>
<td>


openssl version

</td>
</tr>
<tr>
<td>


bc

</td>
<td>


1.06.95

</td>
<td>


bc --version

</td>
</tr>
<tr>
<td>


Sphinx<a id="rst-footnote-reference-1"></a>[1](#rst-f1)

</td>
<td>


3.4.3

</td>
<td>


sphinx-build --version

</td>
</tr>
<tr>
<td>


GNU tar

</td>
<td>


1.28

</td>
<td>


tar --version

</td>
</tr>
<tr>
<td>


gtags (optional)

</td>
<td>


6.6.5

</td>
<td>


gtags --version

</td>
</tr>
<tr>
<td>


mkimage (optional)

</td>
<td>


2017.01

</td>
<td>


mkimage --version

</td>
</tr>
<tr>
<td>


Python

</td>
<td>


3.9.x

</td>
<td>


python3 --version

</td>
</tr>
<tr>
<td>


GNU AWK (optional)

</td>
<td>


5.1.0

</td>
<td>


gawk --version

</td>
</tr>
</tbody>
</table>

<a id="rst-f1"></a>



**[1]** Sphinx is needed only to build the Kernel documentation

<a id="rst-kernel-compilation"></a>

### Kernel compilation

<a id="rst-gcc"></a>

#### GCC

The gcc version requirements may vary depending on the type of CPU in your computer.

<a id="rst-clang-llvm-optional"></a>

#### Clang/LLVM (optional)

The latest formal release of clang and LLVM utils (according to [releases.llvm.org](<https://releases.llvm.org>)<a id="rst-releases-llvm-org"></a>) are supported for building kernels. Older releases aren't guaranteed to work, and we may drop workarounds from the kernel that were used to support older versions. Please see additional docs on [Building Linux with Clang/LLVM](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/kbuild/llvm.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>).

<a id="rst-rust-optional"></a>

#### Rust (optional)

A recent version of the Rust compiler is required.

Please see [Documentation/rust/quick-start.rst](~kernel/development/rust/quick-start) for instructions on how to satisfy the build requirements of Rust support. In particular, the `Makefile` target `rustavailable` is useful to check why the Rust toolchain may not be detected.

<a id="rst-bindgen-optional"></a>

#### bindgen (optional)

`bindgen` is used to generate the Rust bindings to the C side of the kernel. It depends on `libclang`.

<a id="rst-make"></a>

#### Make

You will need GNU make 4.0 or later to build the kernel.

<a id="rst-bash"></a>

#### Bash

Some bash scripts are used for the kernel build. Bash 4.2 or newer is needed.

<a id="rst-binutils"></a>

#### Binutils

Binutils 2.30 or newer is needed to build the kernel.

<a id="rst-pkg-config"></a>

#### pkg-config

The build system, as of 4.18, requires pkg-config to check for installed kconfig tools and to determine flags settings for use in 'make \{g,x\}config'.  Previously pkg-config was being used but not verified or documented.

<a id="rst-flex"></a>

#### Flex

Since Linux 4.16, the build system generates lexical analyzers during build.  This requires flex 2.5.35 or later.

<a id="rst-bison"></a>

#### Bison

Since Linux 4.16, the build system generates parsers during build.  This requires bison 2.0 or later.

<a id="rst-pahole"></a>

#### pahole

Since Linux 5.2, if CONFIG_DEBUG_INFO_BTF is selected, the build system generates BTF (BPF Type Format) from DWARF in vmlinux, a bit later from kernel modules as well.  This requires pahole v1.22 or later.

It is found in the 'dwarves' or 'pahole' distro packages or from [https://fedorapeople.org/\~acme/dwarves/](<https://fedorapeople.org/~acme/dwarves/>).

<a id="rst-perl"></a>

#### Perl

You will need perl 5 and the following modules: `Getopt::Long`, `Getopt::Std`, `File::Basename`, and `File::Find` to build the kernel.

<a id="rst-python"></a>

#### Python

Several config options require it: it is required for arm/arm64 default configs, CONFIG_LTO_CLANG, some DRM optional configs, the kernel-doc tool, and docs build (Sphinx), among others.

<a id="rst-bc"></a>

#### BC

You will need bc to build kernels 3.10 and higher

<a id="rst-openssl"></a>

#### OpenSSL

Module signing and external certificate handling use the OpenSSL program and crypto library to do key creation and signature generation.

You will need openssl to build kernels 3.7 and higher if module signing is enabled.  You will also need openssl development packages to build kernels 4.3 and higher.

<a id="rst-tar"></a>

#### Tar

GNU tar is needed if you want to enable access to the kernel headers via sysfs (CONFIG_IKHEADERS).

<a id="rst-gtags-gnu-global-optional"></a>

#### gtags / GNU GLOBAL (optional)

The kernel build requires GNU GLOBAL version 6.6.5 or later to generate tag files through `make gtags`.  This is due to its use of the gtags `-C (--directory)` flag.

<a id="rst-mkimage"></a>

#### mkimage

This tool is used when building a Flat Image Tree (FIT), commonly used on ARM platforms. The tool is available via the `u-boot-tools` package or can be built from the U-Boot source code. See the instructions at [https://docs.u-boot.org/en/latest/build/tools.html\#building-tools-for-linux](<https://docs.u-boot.org/en/latest/build/tools.html#building-tools-for-linux>)

<a id="rst-gnu-awk"></a>

#### GNU AWK

GNU AWK is needed if you want kernel builds to generate address range data for builtin modules (CONFIG_BUILTIN_MODULE_RANGES).

<a id="rst-system-utilities"></a>

### System utilities

<a id="rst-architectural-changes"></a>

#### Architectural changes

DevFS has been obsoleted in favour of udev ([https://www.kernel.org/pub/linux/utils/kernel/hotplug/](<https://www.kernel.org/pub/linux/utils/kernel/hotplug/>))

32-bit UID support is now in place.  Have fun\!

Linux documentation for functions is transitioning to inline documentation via specially-formatted comments near their definitions in the source.  These comments can be combined with ReST files in the Documentation/ directory to make enriched documentation, which can then be converted to PostScript, HTML, LaTex, ePUB and PDF files. In order to convert from ReST format to a format of your choice, you'll need Sphinx.

<a id="rst-util-linux"></a>

#### Util-linux

New versions of util-linux provide `fdisk` support for larger disks, support new options to mount, recognize more supported partition types, and similar goodies. You'll probably want to upgrade.

<a id="rst-ksymoops"></a>

#### Ksymoops

If the unthinkable happens and your kernel oopses, you may need the ksymoops tool to decode it, but in most cases you don't. It is generally preferred to build the kernel with `CONFIG_KALLSYMS` so that it produces readable dumps that can be used as-is (this also produces better output than ksymoops).  If for some reason your kernel is not build with `CONFIG_KALLSYMS` and you have no way to rebuild and reproduce the Oops with that option, then you can still decode that Oops with ksymoops.

<a id="rst-mkinitrd"></a>

#### Mkinitrd

These changes to the `/lib/modules` file tree layout also require that mkinitrd be upgraded.

<a id="rst-e2fsprogs"></a>

#### E2fsprogs

The latest version of `e2fsprogs` fixes several bugs in fsck and debugfs.  Obviously, it's a good idea to upgrade.

<a id="rst-jfsutils"></a>

#### JFSutils

The `jfsutils` package contains the utilities for the file system. The following utilities are available:

- `fsck.jfs` - initiate replay of the transaction log, and check and repair a JFS formatted partition.

- `mkfs.jfs` - create a JFS formatted partition.

- other file system utilities are also available in this package.

<a id="rst-xfsprogs"></a>

#### Xfsprogs

The latest version of `xfsprogs` contains `mkfs.xfs`, `xfs_db`, and the `xfs_repair` utilities, among others, for the XFS filesystem.  It is architecture independent and any version from 2.0.0 onward should work correctly with this version of the XFS kernel code (2.6.0 or later is recommended, due to some significant improvements).

<a id="rst-pcmciautils"></a>

#### PCMCIAutils

PCMCIAutils replaces `pcmcia-cs`. It properly sets up PCMCIA sockets at system startup and loads the appropriate modules for 16-bit PCMCIA devices if the kernel is modularized and the hotplug subsystem is used.

<a id="rst-quota-tools"></a>

#### Quota-tools

Support for 32 bit uid's and gid's is required if you want to use the newer version 2 quota format.  Quota-tools version 3.07 and newer has this support.  Use the recommended version or newer from the table above.

<a id="rst-intel-ia32-microcode"></a>

#### Intel IA32 microcode

A driver has been added to allow updating of Intel IA32 microcode, accessible as a normal (misc) character device.  If you are not using udev you may need to:



```text
mkdir /dev/cpu
mknod /dev/cpu/microcode c 10 184
chmod 0644 /dev/cpu/microcode
```

as root before you can use this.  You'll probably also want to get the user-space microcode_ctl utility to use with this.

<a id="rst-udev"></a>

#### udev

`udev` is a userspace application for populating `/dev` dynamically with only entries for devices actually present. `udev` replaces the basic functionality of devfs, while allowing persistent device naming for devices.

<a id="rst-fuse"></a>

#### FUSE

Needs libfuse 2.4.0 or later.  Absolute minimum is 2.3.0 but mount options `direct_io` and `kernel_cache` won't work.

<a id="rst-networking"></a>

### Networking

<a id="rst-general-changes"></a>

#### General changes

If you have advanced network configuration needs, you should probably consider using the network tools from ip-route2.

<a id="rst-packet-filter-nat"></a>

#### Packet Filter / NAT

The packet filtering and NAT code uses the same tools like the previous 2.4.x kernel series (iptables).  It still includes backwards-compatibility modules for 2.2.x-style ipchains and 2.0.x-style ipfwadm.

<a id="rst-ppp"></a>

#### PPP

The PPP driver has been restructured to support multilink and to enable it to operate over diverse media layers.  If you use PPP, upgrade pppd to at least 2.4.0.

If you are not using udev, you must have the device file /dev/ppp which can be made by:



```text
mknod /dev/ppp c 108 0
```

as root.

<a id="rst-nfs-utils"></a>

#### NFS-utils

In ancient (2.4 and earlier) kernels, the nfs server needed to know about any client that expected to be able to access files via NFS.  This information would be given to the kernel by `mountd` when the client mounted the filesystem, or by `exportfs` at system startup.  exportfs would take information about active clients from `/var/lib/nfs/rmtab`.

This approach is quite fragile as it depends on rmtab being correct which is not always easy, particularly when trying to implement fail-over.  Even when the system is working well, `rmtab` suffers from getting lots of old entries that never get removed.

With modern kernels we have the option of having the kernel tell mountd when it gets a request from an unknown host, and mountd can give appropriate export information to the kernel.  This removes the dependency on `rmtab` and means that the kernel only needs to know about currently active clients.

To enable this new functionality, you need to:



```text
mount -t nfsd nfsd /proc/fs/nfsd
```

before running exportfs or mountd.  It is recommended that all NFS services be protected from the internet-at-large by a firewall where that is possible.

<a id="rst-mcelog"></a>

#### mcelog

On x86 kernels the mcelog utility is needed to process and log machine check events when `CONFIG_X86_MCE` is enabled. Machine check events are errors reported by the CPU. Processing them is strongly encouraged.

<a id="rst-kernel-documentation"></a>

### Kernel documentation

<a id="rst-sphinx"></a>

#### Sphinx

Please see [sphinx_install](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/doc-guide/sphinx.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>) in [Documentation/doc-guide/sphinx.rst](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/doc-guide/sphinx.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>) for details about Sphinx requirements.

<a id="rst-rustdoc"></a>

#### rustdoc

`rustdoc` is used to generate the documentation for Rust code. Please see [Documentation/rust/general-information.rst](~kernel/development/rust/general-information) for more information.

<a id="rst-getting-updated-software"></a>

## Getting updated software

<a id="rst-kernel-compilation-1"></a>

### Kernel compilation

<a id="rst-gcc-1"></a>

#### gcc

- &lt;[ftp://ftp.gnu.org/gnu/gcc/](<ftp://ftp.gnu.org/gnu/gcc/>)&gt;

<a id="rst-clang-llvm"></a>

#### Clang/LLVM

- [Getting LLVM](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/kbuild/llvm.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>).

<a id="rst-rust"></a>

#### Rust

- [Documentation/rust/quick-start.rst](~kernel/development/rust/quick-start).

<a id="rst-bindgen"></a>

#### bindgen

- [Documentation/rust/quick-start.rst](~kernel/development/rust/quick-start).

<a id="rst-make-1"></a>

#### Make

- &lt;[ftp://ftp.gnu.org/gnu/make/](<ftp://ftp.gnu.org/gnu/make/>)&gt;

<a id="rst-bash-1"></a>

#### Bash

- &lt;[ftp://ftp.gnu.org/gnu/bash/](<ftp://ftp.gnu.org/gnu/bash/>)&gt;

<a id="rst-binutils-1"></a>

#### Binutils

- &lt;[https://www.kernel.org/pub/linux/devel/binutils/](<https://www.kernel.org/pub/linux/devel/binutils/>)&gt;

<a id="rst-flex-1"></a>

#### Flex

- &lt;[https://github.com/westes/flex/releases](<https://github.com/westes/flex/releases>)&gt;

<a id="rst-bison-1"></a>

#### Bison

- &lt;[ftp://ftp.gnu.org/gnu/bison/](<ftp://ftp.gnu.org/gnu/bison/>)&gt;

<a id="rst-openssl-1"></a>

#### OpenSSL

- &lt;[https://www.openssl.org/](<https://www.openssl.org/>)&gt;

<a id="rst-system-utilities-1"></a>

### System utilities

<a id="rst-util-linux-1"></a>

#### Util-linux

- &lt;[https://www.kernel.org/pub/linux/utils/util-linux/](<https://www.kernel.org/pub/linux/utils/util-linux/>)&gt;

<a id="rst-kmod"></a>

#### Kmod

- &lt;[https://www.kernel.org/pub/linux/utils/kernel/kmod/](<https://www.kernel.org/pub/linux/utils/kernel/kmod/>)&gt;

- &lt;[https://git.kernel.org/pub/scm/utils/kernel/kmod/kmod.git](<https://git.kernel.org/pub/scm/utils/kernel/kmod/kmod.git>)&gt;

<a id="rst-ksymoops-1"></a>

#### Ksymoops

- &lt;[https://www.kernel.org/pub/linux/utils/kernel/ksymoops/v2.4/](<https://www.kernel.org/pub/linux/utils/kernel/ksymoops/v2.4/>)&gt;

<a id="rst-mkinitrd-1"></a>

#### Mkinitrd

- &lt;[https://code.launchpad.net/initrd-tools/main](<https://code.launchpad.net/initrd-tools/main>)&gt;

<a id="rst-e2fsprogs-1"></a>

#### E2fsprogs

- &lt;[https://www.kernel.org/pub/linux/kernel/people/tytso/e2fsprogs/](<https://www.kernel.org/pub/linux/kernel/people/tytso/e2fsprogs/>)&gt;

- &lt;[https://git.kernel.org/pub/scm/fs/ext2/e2fsprogs.git/](<https://git.kernel.org/pub/scm/fs/ext2/e2fsprogs.git/>)&gt;

<a id="rst-jfsutils-1"></a>

#### JFSutils

- &lt;[https://jfs.sourceforge.net/](<https://jfs.sourceforge.net/>)&gt;

<a id="rst-xfsprogs-1"></a>

#### Xfsprogs

- &lt;[https://git.kernel.org/pub/scm/fs/xfs/xfsprogs-dev.git](<https://git.kernel.org/pub/scm/fs/xfs/xfsprogs-dev.git>)&gt;

- &lt;[https://www.kernel.org/pub/linux/utils/fs/xfs/xfsprogs/](<https://www.kernel.org/pub/linux/utils/fs/xfs/xfsprogs/>)&gt;

<a id="rst-pcmciautils-1"></a>

#### Pcmciautils

- &lt;[https://www.kernel.org/pub/linux/utils/kernel/pcmcia/](<https://www.kernel.org/pub/linux/utils/kernel/pcmcia/>)&gt;

<a id="rst-quota-tools-1"></a>

#### Quota-tools

- &lt;[https://sourceforge.net/projects/linuxquota/](<https://sourceforge.net/projects/linuxquota/>)&gt;

<a id="rst-intel-p6-microcode"></a>

#### Intel P6 microcode

- &lt;[https://downloadcenter.intel.com/](<https://downloadcenter.intel.com/>)&gt;

<a id="rst-udev-1"></a>

#### udev

- &lt;[https://www.freedesktop.org/software/systemd/man/udev.html](<https://www.freedesktop.org/software/systemd/man/udev.html>)&gt;

<a id="rst-fuse-1"></a>

#### FUSE

- &lt;[https://github.com/libfuse/libfuse/releases](<https://github.com/libfuse/libfuse/releases>)&gt;

<a id="rst-mcelog-1"></a>

#### mcelog

- &lt;[https://www.mcelog.org/](<https://www.mcelog.org/>)&gt;

<a id="rst-networking-1"></a>

### Networking

<a id="rst-ppp-1"></a>

#### PPP

- &lt;[https://download.samba.org/pub/ppp/](<https://download.samba.org/pub/ppp/>)&gt;

- &lt;[https://git.ozlabs.org/?p=ppp.git](<https://git.ozlabs.org/?p=ppp.git>)&gt;

- &lt;[https://github.com/paulusmack/ppp/](<https://github.com/paulusmack/ppp/>)&gt;

<a id="rst-nfs-utils-1"></a>

#### NFS-utils

- &lt;[https://sourceforge.net/project/showfiles.php?group_id=14](<https://sourceforge.net/project/showfiles.php?group_id=14>)&gt;

- &lt;[https://nfs.sourceforge.net/](<https://nfs.sourceforge.net/>)&gt;

<a id="rst-iptables"></a>

#### Iptables

- &lt;[https://netfilter.org/projects/iptables/index.html](<https://netfilter.org/projects/iptables/index.html>)&gt;

<a id="rst-ip-route2"></a>

#### Ip-route2

- &lt;[https://www.kernel.org/pub/linux/utils/net/iproute2/](<https://www.kernel.org/pub/linux/utils/net/iproute2/>)&gt;

<a id="rst-oprofile"></a>

#### OProfile

- &lt;[https://oprofile.sf.net/download/](<https://oprofile.sf.net/download/>)&gt;

<a id="rst-kernel-documentation-1"></a>

### Kernel documentation

<a id="rst-sphinx-1"></a>

#### Sphinx

- &lt;[https://www.sphinx-doc.org/](<https://www.sphinx-doc.org/>)&gt;
