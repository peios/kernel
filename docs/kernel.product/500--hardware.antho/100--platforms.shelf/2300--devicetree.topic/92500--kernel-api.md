---
title: "DeviceTree Kernel API"
type: reference
description: "Reference for DeviceTree Kernel API."
---

<a id="rst-devicetree-kernel-api"></a>
<a id="rst-devicetree"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

<a id="rst-core-functions"></a>

## Core functions

```{kernel-doc} drivers/of/base.c
:export:
```

```{kernel-doc} include/linux/of.h
:internal:
```

```{kernel-doc} drivers/of/property.c
:export:
```

```{kernel-doc} include/linux/of_graph.h
:internal:
```

```{kernel-doc} drivers/of/address.c
:export:
```

```{kernel-doc} drivers/of/irq.c
:export:
```

```{kernel-doc} drivers/of/fdt.c
:export:
```

<a id="rst-driver-model-functions"></a>

## Driver model functions

```{kernel-doc} include/linux/of_device.h
:internal:
```

```{kernel-doc} drivers/of/device.c
:export:
```

```{kernel-doc} include/linux/of_platform.h
:internal:
```

```{kernel-doc} drivers/of/platform.c
:export:
```

<a id="rst-overlay-and-dynamic-dt-functions"></a>

## Overlay and Dynamic DT functions

```{kernel-doc} drivers/of/resolver.c
:export:
```

```{kernel-doc} drivers/of/dynamic.c
:export:
```

```{kernel-doc} drivers/of/overlay.c
:export:
```
