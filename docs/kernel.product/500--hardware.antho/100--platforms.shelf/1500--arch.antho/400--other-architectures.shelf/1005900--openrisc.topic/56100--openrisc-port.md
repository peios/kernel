---
title: "OpenRISC Linux"
type: reference
description: "This is a port of Linux to the OpenRISC class of microprocessors; the initial target architecture, specifically, is the 32-bit OpenRISC 1000 family (or1k)."
---

<a id="rst-openrisc-linux"></a>

This is a port of Linux to the OpenRISC class of microprocessors; the initial target architecture, specifically, is the 32-bit OpenRISC 1000 family (or1k).

For information about OpenRISC processors and ongoing development:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> website
>
> </td>
> <td>
>
>
> [https://openrisc.io](<https://openrisc.io>)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> email
>
> </td>
> <td>
>
>
> [linux-openrisc@vger.kernel.org](<mailto:linux-openrisc@vger.kernel.org>)
>
> </td>
> </tr>
> </tbody>
> </table>

---

<a id="rst-build-instructions-for-openrisc-toolchain-and-linux"></a>

## Build instructions for OpenRISC toolchain and Linux

In order to build and run Linux for OpenRISC, you'll need at least a basic toolchain and, perhaps, the architectural simulator.  Steps to get these bits in place are outlined here.

1. Toolchain

Toolchain binaries can be obtained from openrisc.io or our github releases page. Instructions for building the different toolchains can be found on openrisc.io or Stafford's toolchain build and release scripts.

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> binaries
>
> </td>
> <td>
>
>
> [https://github.com/stffrdhrn/or1k-toolchain-build/releases](<https://github.com/stffrdhrn/or1k-toolchain-build/releases>)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> toolchains
>
> </td>
> <td>
>
>
> [https://openrisc.io/software](<https://openrisc.io/software>)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> building
>
> </td>
> <td>
>
>
> [https://github.com/stffrdhrn/or1k-toolchain-build](<https://github.com/stffrdhrn/or1k-toolchain-build>)
>
> </td>
> </tr>
> </tbody>
> </table>

2. Building

Build the Linux kernel as usual:



```text
make ARCH=openrisc CROSS_COMPILE="or1k-linux-" defconfig
make ARCH=openrisc CROSS_COMPILE="or1k-linux-"
```

If you want to embed initramfs in the kernel, also pass `CONFIG_INITRAMFS_SOURCE`. For example:



```text
make ARCH=openrisc CROSS_COMPILE="or1k-linux-" CONFIG_INITRAMFS_SOURCE="path/to/rootfs path/to/devnodes"
```

For more information on this, please check [Documentation/filesystems/ramfs-rootfs-initramfs.rst](~kernel/internals/filesystems/ramfs-rootfs-initramfs).

3. Running on FPGA (optional)

The OpenRISC community typically uses FuseSoC to manage building and programming an SoC into an FPGA.  The below is an example of programming a De0 Nano development board with the OpenRISC SoC.  During the build FPGA RTL is code downloaded from the FuseSoC IP cores repository and built using the FPGA vendor tools.  Binaries are loaded onto the board with openocd.



```text
git clone https://github.com/olofk/fusesoc
cd fusesoc
sudo pip install -e .

fusesoc init
fusesoc build de0_nano
fusesoc pgm de0_nano

openocd -f interface/altera-usb-blaster.cfg \
        -f board/or1k_generic.cfg

telnet localhost 4444
> init
> halt; load_image vmlinux ; reset
```

4. Running on a Simulator (optional)

QEMU is a processor emulator which we recommend for simulating the OpenRISC platform.  Please follow the OpenRISC instructions on the QEMU website to get Linux running on QEMU.  You can build QEMU yourself, but your Linux distribution likely provides binary packages to support OpenRISC.

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> qemu openrisc
>
> </td>
> <td>
>
>
> [https://wiki.qemu.org/Documentation/Platforms/OpenRISC](<https://wiki.qemu.org/Documentation/Platforms/OpenRISC>)
>
> </td>
> </tr>
> </tbody>
> </table>

---

<a id="rst-terminology"></a>

## Terminology

In the code, the following particles are used on symbols to limit the scope to more or less specific processor implementations:


<table>
<tbody>
<tr>
<td>


openrisc:

</td>
<td>


the OpenRISC class of processors

</td>
</tr>
<tr>
<td>


or1k:

</td>
<td>


the OpenRISC 1000 family of processors

</td>
</tr>
<tr>
<td>


or1200:

</td>
<td>


the OpenRISC 1200 processor

</td>
</tr>
</tbody>
</table>

---

<a id="rst-history"></a>

## History

- **18-11-2003      Matjaz Breskvar ([phoenix@bsemi.com](<mailto:phoenix@bsemi.com>))**

  initial port of linux to OpenRISC/or32 architecture. all the core stuff is implemented and seams usable.

- **08-12-2003      Matjaz Breskvar ([phoenix@bsemi.com](<mailto:phoenix@bsemi.com>))**

  complete change of TLB miss handling. rewrite of exceptions handling. fully functional sash-3.6 in default initrd. a much improved version with changes all around.

- **10-04-2004      Matjaz Breskvar ([phoenix@bsemi.com](<mailto:phoenix@bsemi.com>))**

  a lot of bugfixes all over. ethernet support, functional http and telnet servers. running many standard linux apps.

- **26-06-2004      Matjaz Breskvar ([phoenix@bsemi.com](<mailto:phoenix@bsemi.com>))**

  port to 2.6.x

- **30-11-2004      Matjaz Breskvar ([phoenix@bsemi.com](<mailto:phoenix@bsemi.com>))**

  lots of bugfixes and enhancements. added opencores framebuffer driver.

- **09-10-2010    Jonas Bonn ([jonas@southpole.se](<mailto:jonas@southpole.se>))**

  major rewrite to bring up to par with upstream Linux 2.6.36
