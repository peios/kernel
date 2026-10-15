---
title: "ioctl FE_SET_VOLTAGE"
type: reference
description: "FE_SET_VOLTAGE - Allow setting the DC level sent to the antenna subsystem."
---

<a id="rst-ioctl-fe-set-voltage"></a>
<a id="rst-fe-set-voltage"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: DTV.fe -->

<a id="rst-name"></a>

## Name

FE_SET_VOLTAGE - Allow setting the DC level sent to the antenna subsystem.

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-FE_SET_VOLTAGE"></a>

```c
FE_SET_VOLTAGE
```

`int ioctl(int fd, FE_SET_VOLTAGE, enum fe_sec_voltage voltage)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`voltage`**

  An integer enumerated value described at `fe_sec_voltage`

<a id="rst-description"></a>

## Description

This ioctl allows to set the DC voltage level sent through the antenna cable to 13V, 18V or off.

Usually, a satellite antenna subsystems require that the digital TV device to send a DC voltage to feed power to the LNBf. Depending on the LNBf type, the polarization or the intermediate frequency (IF) of the LNBf can controlled by the voltage level. Other devices (for example, the ones that implement DISEqC and multipoint LNBf's don't need to control the voltage level, provided that either 13V or 18V is sent to power up the LNBf.

> [!NOTE]
>
> if more than one device is connected to the same antenna, setting a voltage level may interfere on other devices, as they may lose the capability of setting polarization or IF. So, on those cases, setting the voltage to SEC_VOLTAGE_OFF while the device is not is used is recommended.

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned.

On error -1 is returned, and the `errno` variable is set appropriately.

Generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
