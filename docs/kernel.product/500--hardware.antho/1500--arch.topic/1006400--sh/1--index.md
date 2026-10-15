---
title: "SuperH Interfaces Guide"
type: reference
description: "Reference for SuperH Interfaces Guide."
---

<a id="rst-superh-interfaces-guide"></a>

**Author:** Paul Mundt

- [DeviceTree Booting](<~kernel/hardware/arch/sh/booting>)
- [Adding a new board to LinuxSH](<~kernel/hardware/arch/sh/new-machine>)
- [Notes on register bank usage in the kernel](<~kernel/hardware/arch/sh/register-banks>)
- [features](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/arch/sh/features.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>)

<a id="rst-memory-management"></a>

## Memory Management

<a id="rst-sh-4"></a>

### SH-4

<a id="rst-store-queue-api"></a>

#### Store Queue API

```{kernel-doc} arch/sh/kernel/cpu/sh4/sq.c
:export:
```

<a id="rst-machine-specific-interfaces"></a>

## Machine Specific Interfaces

<a id="rst-mach-dreamcast"></a>

### mach-dreamcast

```{kernel-doc} arch/sh/boards/mach-dreamcast/rtc.c
:internal:
```

<a id="rst-mach-x3proto"></a>

### mach-x3proto

```{kernel-doc} arch/sh/boards/mach-x3proto/ilsel.c
:export:
```

<a id="rst-busses"></a>

## Busses

<a id="rst-maple"></a>

### Maple

```{kernel-doc} drivers/sh/maple/maple.c
:export:
```
