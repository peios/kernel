---
title: "Device drivers infrastructure"
type: reference
description: "Reference for Device drivers infrastructure."
---

<a id="rst-device-drivers-infrastructure"></a>

<a id="rst-the-basic-device-driver-model-structures"></a>

## The Basic Device Driver-Model Structures

```{kernel-doc} include/linux/device.h
:internal:
:no-identifiers: device_link_state
```

```{kernel-doc} include/linux/device/bus.h
:identifiers: bus_type bus_notifier_event
```

```{kernel-doc} include/linux/device/class.h
:identifiers: class
```

```{kernel-doc} include/linux/device/driver.h
:identifiers: probe_type device_driver
```

<a id="rst-device-drivers-base"></a>

## Device Drivers Base

```{kernel-doc} drivers/base/init.c
:internal:
```

```{kernel-doc} include/linux/device/driver.h
:no-identifiers: probe_type device_driver
```

```{kernel-doc} drivers/base/driver.c
:export:
```

```{kernel-doc} drivers/base/core.c
:export:
```

```{kernel-doc} drivers/base/syscore.c
:export:
```

```{kernel-doc} include/linux/device/class.h
:no-identifiers: class
```

```{kernel-doc} drivers/base/class.c
:export:
```

```{kernel-doc} include/linux/device/faux.h
:internal:
```

```{kernel-doc} drivers/base/faux.c
:export:
```

```{kernel-doc} drivers/base/node.c
:internal:
```

```{kernel-doc} drivers/base/transport_class.c
:export:
```

```{kernel-doc} drivers/base/dd.c
:export:
```

```{kernel-doc} include/linux/platform_device.h
:internal:
```

```{kernel-doc} drivers/base/platform.c
:export:
```

```{kernel-doc} include/linux/device/bus.h
:no-identifiers: bus_type bus_notifier_event
```

```{kernel-doc} drivers/base/bus.c
:export:
```

<a id="rst-device-drivers-dma-management"></a>

## Device Drivers DMA Management

```{kernel-doc} kernel/dma/mapping.c
:export:
```

<a id="rst-device-drivers-pnp-support"></a>

## Device drivers PnP support

```{kernel-doc} drivers/pnp/core.c
:internal:
```

```{kernel-doc} drivers/pnp/card.c
:export:
```

```{kernel-doc} drivers/pnp/driver.c
:internal:
```

```{kernel-doc} drivers/pnp/manager.c
:export:
```

```{kernel-doc} drivers/pnp/support.c
:export:
```

<a id="rst-userspace-io-devices"></a>

## Userspace IO devices

```{kernel-doc} drivers/uio/uio.c
:export:
```

```{kernel-doc} include/linux/uio_driver.h
:internal:
```
