---
title: "Firewire (IEEE 1394) driver Interface Guide"
type: reference
description: "use/maintain+any resource on IEEE 1394 bus."
---

<a id="rst-firewire-ieee-1394-driver-interface-guide"></a>

<a id="rst-introduction-and-overview"></a>

## Introduction and Overview

- **The Linux FireWire subsystem adds some interfaces into the Linux system to**

  use/maintain+any resource on IEEE 1394 bus.

The main purpose of these interfaces is to access address space on each node on IEEE 1394 bus by ISO/IEC 13213 (IEEE 1212) procedure, and to control isochronous resources on the bus by IEEE 1394 procedure.

Two types of interfaces are added, according to consumers of the interface. A set of userspace interfaces is available via `firewire character devices`. A set of kernel interfaces is available via exported symbols in `firewire-core` module.

<a id="rst-firewire-char-device-data-structures"></a>

## Firewire char device data structures



```{kernel-include} Documentation/ABI/stable/firewire-cdev
:tab-width: 8
```

```{kernel-doc} include/uapi/linux/firewire-cdev.h
:internal:
```

<a id="rst-firewire-device-probing-and-sysfs-interfaces"></a>

## Firewire device probing and sysfs interfaces



```{kernel-include} Documentation/ABI/stable/sysfs-bus-firewire
:tab-width: 8
```

```{kernel-doc} drivers/firewire/core-device.c
:export:
```

<a id="rst-firewire-core-transaction-interfaces"></a>

## Firewire core transaction interfaces

```{kernel-doc} drivers/firewire/core-transaction.c
:export:
```

<a id="rst-firewire-isochronous-i-o-interfaces"></a>

## Firewire Isochronous I/O interfaces

```{kernel-doc} include/linux/firewire.h
:functions: fw_iso_context_schedule_flush_completions
```

```{kernel-doc} drivers/firewire/core-iso.c
:export:
```
