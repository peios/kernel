---
title: "Device Frequency Scaling"
type: reference
description: "This framework provides a standard kernel interface for Dynamic Voltage and Frequency Switching on arbitrary devices."
---

<a id="rst-device-frequency-scaling"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

<a id="rst-introduction"></a>

## Introduction

This framework provides a standard kernel interface for Dynamic Voltage and Frequency Switching on arbitrary devices.

It exposes controls for adjusting frequency through sysfs files which are similar to the cpufreq subsystem.

Devices for which current usage can be measured can have their frequency automatically adjusted by governors.

<a id="rst-api"></a>

## API

Device drivers need to initialize a `devfreq_profile` and call the `devfreq_add_device()` function to create a `devfreq` instance.

```{kernel-doc} include/linux/devfreq.h

```

```{kernel-doc} include/linux/devfreq-event.h

```

```{kernel-doc} drivers/devfreq/devfreq.c
:export:
```

```{kernel-doc} drivers/devfreq/devfreq-event.c
:export:
```
