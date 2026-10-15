---
title: "Cards List"
type: reference
description: "The media subsystem provide support for lots of PCI and USB drivers, plus platform-specific drivers. It also contains several ancillary I²C drivers."
---

<a id="rst-cards-list"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

The media subsystem provide support for lots of PCI and USB drivers, plus platform-specific drivers. It also contains several ancillary I²C drivers.

The platform-specific drivers are usually present on embedded systems, or are supported by the main board. Usually, setting them is done via OpenFirmware or ACPI.

The PCI and USB drivers, however, are independent of the system's board, and may be added/removed by the user.

You may also take a look at [https://linuxtv.org/wiki/index.php/Hardware_Device_Information](<https://linuxtv.org/wiki/index.php/Hardware_Device_Information>) for more details about supported cards.

- [USB drivers](<~kernel/administration/admin-guide/media/usb-cardlist>)
- [pci-cardlist](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/admin-guide/media/pci-cardlist.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>)
- [Platform drivers](<~kernel/administration/admin-guide/media/platform-cardlist>)
- [Radio drivers](<~kernel/administration/admin-guide/media/radio-cardlist>)
- [I²C drivers](<~kernel/administration/admin-guide/media/i2c-cardlist>)
- [Firewire driver](<~kernel/administration/admin-guide/media/misc-cardlist>)
