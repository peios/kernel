---
title: "Resource API"
type: reference
description: "This file documents the KUnit resource API."
---

<a id="rst-resource-api"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

This file documents the KUnit resource API.

Most users won't need to use this API directly, power users can use it to store state on a per-test basis, register custom cleanup actions, and more.

```{kernel-doc} include/kunit/resource.h
:internal:
```

<a id="rst-managed-devices"></a>

## Managed Devices

Functions for using KUnit-managed struct device and struct device_driver. Include `kunit/device.h` to use these.

```{kernel-doc} include/kunit/device.h
:internal:
```
