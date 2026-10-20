---
title: "Client Driver API Documentation"
type: reference
description: "Serial Hub Communication"
---

<a id="rst-client-driver-api-documentation"></a>

<!-- SPDX-License-Identifier: GPL-2.0+ -->

<a id="rst-contents"></a>



<a id="rst-serial-hub-communication"></a>

## Serial Hub Communication

```{kernel-doc} include/linux/surface_aggregator/serial_hub.h

```

```{kernel-doc} drivers/platform/surface/aggregator/ssh_packet_layer.c
:export:
```

<a id="rst-controller-and-core-interface"></a>

## Controller and Core Interface

```{kernel-doc} include/linux/surface_aggregator/controller.h

```

```{kernel-doc} drivers/platform/surface/aggregator/controller.c
:export:
```

```{kernel-doc} drivers/platform/surface/aggregator/core.c
:export:
```

<a id="rst-client-bus-and-client-device-api"></a>

## Client Bus and Client Device API

```{kernel-doc} include/linux/surface_aggregator/device.h

```

```{kernel-doc} drivers/platform/surface/aggregator/bus.c
:export:
```
