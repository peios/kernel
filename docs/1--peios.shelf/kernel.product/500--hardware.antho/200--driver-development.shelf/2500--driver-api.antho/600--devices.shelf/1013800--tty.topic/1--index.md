---
title: "TTY"
type: reference
description: "Teletypewriter (TTY) layer takes care of all those serial devices. Including the virtual ones like pseudoterminal (PTY)."
---

<a id="rst-tty"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

Teletypewriter (TTY) layer takes care of all those serial devices. Including the virtual ones like pseudoterminal (PTY).

<a id="rst-tty-structures"></a>

## TTY structures

There are several major TTY structures. Every TTY device in a system has a corresponding struct tty_port. These devices are maintained by a TTY driver which is struct tty_driver. This structure describes the driver but also contains a reference to operations which could be performed on the TTYs. It is struct tty_operations. Then, upon open, a struct tty_struct is allocated and lives until the final close. During this time, several callbacks from struct tty_operations are invoked by the TTY layer.

Every character received by the kernel (both from devices and users) is passed through a preselected [TTY Line Discipline](<~kernel/hardware/driver-api/tty/tty-ldisc>) (in short ldisc; in C, struct tty_ldisc_ops). Its task is to transform characters as defined by a particular ldisc or by user too. The default one is n_tty, implementing echoes, signal handling, jobs control, special characters processing, and more. The transformed characters are passed further to user/device, depending on the source.

In-detail description of the named TTY structures is in separate documents:

- [TTY Driver and TTY Operations](<~kernel/hardware/driver-api/tty/tty-driver>)
- [TTY Port](<~kernel/hardware/driver-api/tty/tty-port>)
- [TTY Struct](<~kernel/hardware/driver-api/tty/tty-struct>)
- [TTY Line Discipline](<~kernel/hardware/driver-api/tty/tty-ldisc>)
- [TTY Buffer](<~kernel/hardware/driver-api/tty/tty-buffer>)
- [TTY IOCTL Helpers](<~kernel/hardware/driver-api/tty/tty-ioctl>)
- [TTY Internals](<~kernel/hardware/driver-api/tty/tty-internals>)
- [Console](<~kernel/hardware/driver-api/tty/console>)

<a id="rst-writing-tty-driver"></a>

## Writing TTY Driver

Before one starts writing a TTY driver, they must consider [Serial](<~kernel/hardware/driver-api/serial/driver>) and [USB Serial](<~kernel/hardware/usb/usb-serial>) layers first. Drivers for serial devices can often use one of these specific layers to implement a serial driver. Only special devices should be handled directly by the TTY Layer. If you are about to write such a driver, read on.

A *typical* sequence a TTY driver performs is as follows:

1. Allocate and register a TTY driver (module init)

2. Create and register TTY devices as they are probed (probe function)

3. Handle TTY operations and events like interrupts (TTY core invokes the former, the device the latter)

4. Remove devices as they are going away (remove function)

5. Unregister and free the TTY driver (module exit)

Steps regarding driver, i.e. 1., 3., and 5. are described in detail in [TTY Driver and TTY Operations](<~kernel/hardware/driver-api/tty/tty-driver>). For the other two (devices handling), look into [TTY Port](<~kernel/hardware/driver-api/tty/tty-port>).

<a id="rst-other-documentation"></a>

## Other Documentation

Miscellaneous documentation can be further found in these documents:

- [MOXA Smartio/Industio Family Device Driver Installation Guide](<~kernel/hardware/driver-api/tty/moxa-smartio>)
- [GSM 0710 tty multiplexor HOWTO](<~kernel/hardware/driver-api/tty/n-gsm>)
- [N_TTY](<~kernel/hardware/driver-api/tty/n-tty>)
