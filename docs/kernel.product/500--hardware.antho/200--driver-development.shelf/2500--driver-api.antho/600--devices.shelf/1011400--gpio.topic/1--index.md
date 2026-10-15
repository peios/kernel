---
title: "General Purpose Input/Output (GPIO)"
type: reference
description: "Contents:"
---

<a id="rst-general-purpose-input-output-gpio"></a>

Contents:

- [Introduction](<~kernel/hardware/driver-api/gpio/intro>)
- [Using GPIO Lines in Linux](<~kernel/hardware/driver-api/gpio/using-gpio>)
- [GPIO Driver Interface](<~kernel/hardware/driver-api/gpio/driver>)
- [GPIO Descriptor Consumer Interface](<~kernel/hardware/driver-api/gpio/consumer>)
- [GPIO Mappings](<~kernel/hardware/driver-api/gpio/board>)
- [Supporting Legacy Boards](<~kernel/hardware/driver-api/gpio/legacy-boards>)
- [Subsystem drivers using GPIO](<~kernel/hardware/driver-api/gpio/drivers-on-gpio>)
- [A driver for a selfmade cheap BT8xx based PCI GPIO-card (bt8xxgpio)](<~kernel/hardware/driver-api/gpio/bt8xxgpio>)
- [PCA953x I²C GPIO expander compatibility list](<~kernel/hardware/driver-api/gpio/pca953x>)

<a id="rst-core"></a>

## Core

```{kernel-doc} include/linux/gpio/driver.h
:internal:
```

```{kernel-doc} drivers/gpio/gpiolib.c
:export:
```

<a id="rst-acpi-support"></a>

## ACPI support

```{kernel-doc} drivers/gpio/gpiolib-acpi-core.c
:export:
```

<a id="rst-device-tree-support"></a>

## Device tree support

```{kernel-doc} drivers/gpio/gpiolib-of.c
:export:
```

<a id="rst-device-managed-api"></a>

## Device-managed API

```{kernel-doc} drivers/gpio/gpiolib-devres.c
:export:
```

<a id="rst-sysfs-helpers"></a>

## sysfs helpers

```{kernel-doc} drivers/gpio/gpiolib-sysfs.c
:export:
```
