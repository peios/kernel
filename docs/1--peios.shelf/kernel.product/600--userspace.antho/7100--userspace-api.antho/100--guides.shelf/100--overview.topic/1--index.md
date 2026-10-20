---
title: "Kernel interfaces for userspace"
type: guide
description: "Find system-call, device and protocol interface reference."
---

<a id="rst-the-linux-kernel-user-space-api-guide"></a>
<a id="rst-man-pages"></a>
<a id="rst-system-calls"></a>
<a id="rst-security-related-interfaces"></a>
<a id="rst-devices-and-i-o"></a>
<a id="rst-everything-else"></a>

This collection documents interfaces between userspace and the kernel.
General guides cover execution, synchronisation, memory and security controls;
device and protocol topics contain the detailed ABI references.

- **Execution and synchronisation:** [ELF](<~kernel/userspace/userspace-api/execution/elf>),
  [Futexes](<~kernel/userspace/userspace-api/execution/futex2>) and
  [Restartable sequences](<~kernel/userspace/userspace-api/execution/rseq>).
- **Device access:** [ioctl conventions](<~kernel/userspace/userspace-api/ioctl/index>),
  [GPIO](<~kernel/userspace/userspace-api/gpio/index>) and
  [Netlink](<~kernel/userspace/userspace-api/netlink/index>).
- **Media:** [Video4Linux](<~kernel/userspace/userspace-api/media-v4l/v4l2>),
  [Digital television](<~kernel/userspace/userspace-api/media-dvb/dvbapi>) and
  [Media controllers](<~kernel/userspace/userspace-api/media-mediactl/media-controller>).

The media shelf separates video, television, HDMI CEC, media controllers and
remote-control interfaces. The [Kernel ABI catalogue](<~kernel/administration/admin-guide/abi/abi>)
also documents exported attributes and their stability categories.

An interface described here may depend on configuration or a loaded driver;
its presence in the reference does not guarantee availability on every system.
