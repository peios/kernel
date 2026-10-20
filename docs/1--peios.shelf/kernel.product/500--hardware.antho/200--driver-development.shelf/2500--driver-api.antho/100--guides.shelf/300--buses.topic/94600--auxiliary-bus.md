---
title: "Auxiliary Bus"
type: reference
description: "Reference for Auxiliary Bus."
---

<a id="rst-auxiliary-bus-1"></a>
<a id="rst-auxiliary-bus"></a>

<!-- SPDX-License-Identifier: GPL-2.0-only -->

```{kernel-doc} drivers/base/auxiliary.c
:doc: PURPOSE
```

<a id="rst-when-should-the-auxiliary-bus-be-used"></a>

## When Should the Auxiliary Bus Be Used

```{kernel-doc} drivers/base/auxiliary.c
:doc: USAGE
```

<a id="rst-auxiliary-device-creation"></a>

## Auxiliary Device Creation

```{kernel-doc} include/linux/auxiliary_bus.h
:identifiers: auxiliary_device
```

```{kernel-doc} drivers/base/auxiliary.c
:identifiers: auxiliary_device_init __auxiliary_device_add
```

<a id="rst-auxiliary-device-memory-model-and-lifespan"></a>

### Auxiliary Device Memory Model and Lifespan

```{kernel-doc} include/linux/auxiliary_bus.h
:doc: DEVICE_LIFESPAN
```

<a id="rst-auxiliary-drivers"></a>

## Auxiliary Drivers

```{kernel-doc} include/linux/auxiliary_bus.h
:identifiers: auxiliary_driver module_auxiliary_driver
```

```{kernel-doc} drivers/base/auxiliary.c
:identifiers: __auxiliary_driver_register auxiliary_driver_unregister
```

<a id="rst-example-usage"></a>

## Example Usage

```{kernel-doc} drivers/base/auxiliary.c
:doc: EXAMPLE
```
