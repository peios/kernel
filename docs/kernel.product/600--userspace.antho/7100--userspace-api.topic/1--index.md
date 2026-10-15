---
title: "The Linux kernel user-space API guide"
type: reference
description: "While much of the kernel's user-space API is documented elsewhere (particularly in the man-pages project), some user-space information can also be found in the kernel tree itself. This manual is intended to be the place where this…"
---

<a id="rst-the-linux-kernel-user-space-api-guide"></a>

<a id="rst-man-pages"></a>



While much of the kernel's user-space API is documented elsewhere (particularly in the [man-pages](<https://www.kernel.org/doc/man-pages/>) project), some user-space information can also be found in the kernel tree itself.  This manual is intended to be the place where this information is gathered.

<a id="rst-system-calls"></a>

## System calls

- [unshare system call](<~kernel/userspace/userspace-api/unshare>)
- [futex2](<~kernel/userspace/userspace-api/futex2>)
- [eBPF Userspace API](<~kernel/userspace/userspace-api/ebpf/index>)
- [IOCTLs](<~kernel/userspace/userspace-api/ioctl/index>)
- [Introduction of mseal](<~kernel/userspace/userspace-api/mseal>)
- [Restartable Sequences](<~kernel/userspace/userspace-api/rseq>)

<a id="rst-security-related-interfaces"></a>

## Security-related interfaces

- [No New Privileges Flag](<~kernel/userspace/userspace-api/no-new-privs>)
- [Seccomp BPF (SECure COMPuting with filters)](<~kernel/userspace/userspace-api/seccomp-filter>)
- [Landlock: unprivileged access control](<~kernel/userspace/userspace-api/landlock>)
- [Linux Security Modules](<~kernel/userspace/userspace-api/lsm>)
- [Introduction of non-executable mfd](<~kernel/userspace/userspace-api/mfd-noexec>)
- [Speculation Control](<~kernel/userspace/userspace-api/spec-ctrl>)
- [TEE (Trusted Execution Environment) Userspace API](<~kernel/userspace/userspace-api/tee>)
- [Executability check](<~kernel/userspace/userspace-api/check-exec>)

<a id="rst-devices-and-i-o"></a>

## Devices and I/O

- [OpenCAPI (Open Coherent Accelerator Processor Interface)](<~kernel/userspace/userspace-api/accelerators/ocxl>)
- [Allocating dma-buf using heaps](<~kernel/userspace/userspace-api/dma-buf-heaps>)
- [dma-buf-alloc-exchange](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/dma-buf-alloc-exchange.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>)
- [Firmware Control (FWCTL) Userspace API](<~kernel/userspace/userspace-api/fwctl/index>)
- [GPIO](<~kernel/userspace/userspace-api/gpio/index>)
- [IOMMUFD](<~kernel/userspace/userspace-api/iommufd>)
- [Linux Media Infrastructure userspace API](<~kernel/userspace/userspace-api/media/index>)
- [Dell Systems Management Base Driver](<~kernel/userspace/userspace-api/dcdbas>)
- [VDUSE - "vDPA Device in Userspace"](<~kernel/userspace/userspace-api/vduse>)
- [ISA Plug &amp; Play support](<~kernel/userspace/userspace-api/isapnp>)

<a id="rst-everything-else"></a>

## Everything else

- [Linux-specific ELF idiosyncrasies](<~kernel/userspace/userspace-api/elf>)
- [Live Update uAPI](<~kernel/userspace/userspace-api/liveupdate>)
- [Netlink Handbook](<~kernel/userspace/userspace-api/netlink/index>)
- [Platform Profile Selection (e.g. /sys/firmware/acpi/platform_profile)](<~kernel/userspace/userspace-api/sysfs-platform-profile>)
- [VDUSE - "vDPA Device in Userspace"](<~kernel/userspace/userspace-api/vduse>)
- [futex2](<~kernel/userspace/userspace-api/futex2>)
- [Perf ring buffer](<~kernel/userspace/userspace-api/perf-ring-buffer>)
- [NT synchronization primitive driver](<~kernel/userspace/userspace-api/ntsync>)
