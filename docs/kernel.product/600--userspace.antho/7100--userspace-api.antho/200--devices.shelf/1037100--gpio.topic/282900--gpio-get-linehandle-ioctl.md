---
title: "GPIO_GET_LINEHANDLE_IOCTL"
type: reference
description: "Duplicate implicit target name: \"gpio_get_linehandle_ioctl\"."
---

<a id="rst-gpio-get-linehandle-ioctl-1"></a>
<a id="rst-gpio-get-linehandle-ioctl"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

> [!WARNING]
>
> This ioctl is part of [chardev_v1.rst](~kernel/userspace/userspace-api/gpio/chardev-v1) and is obsoleted by [gpio-v2-get-line-ioctl.rst](~kernel/userspace/userspace-api/gpio/gpio-v2-get-line-ioctl).

<a id="rst-name"></a>

## Name

GPIO_GET_LINEHANDLE_IOCTL - Request a line or lines from the kernel.

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-GPIO_GET_LINEHANDLE_IOCTL"></a>

```c
GPIO_GET_LINEHANDLE_IOCTL
```

`int ioctl(int chip_fd, GPIO_GET_LINEHANDLE_IOCTL, struct gpiohandle_request *request)`

<a id="rst-arguments"></a>

## Arguments

- **`chip_fd`**

  The file descriptor of the GPIO character device returned by `open()`.

- **`request`**

  The `handle_request<gpiohandle_request>` specifying the lines to request and their configuration.

<a id="rst-description"></a>

## Description

Request a line or lines from the kernel.

While multiple lines may be requested, the same configuration applies to all lines in the request.

On success, the requesting process is granted exclusive access to the line value and write access to the line configuration.

The state of a line, including the value of output lines, is guaranteed to remain as requested until the returned file descriptor is closed. Once the file descriptor is closed, the state of the line becomes uncontrolled from the userspace perspective, and may revert to its default state.

Requesting a line already in use is an error (**EBUSY**).

Closing the `chip_fd` has no effect on existing line handles.

<a id="rst-configuration-rules"></a>
<a id="rst-gpio-get-linehandle-config-rules"></a>

### Configuration Rules

The following configuration rules apply:

The direction flags, `GPIOHANDLE_REQUEST_INPUT` and `GPIOHANDLE_REQUEST_OUTPUT`, cannot be combined. If neither are set then the only other flag that may be set is `GPIOHANDLE_REQUEST_ACTIVE_LOW` and the line is requested "as-is" to allow reading of the line value without altering the electrical configuration.

The drive flags, `GPIOHANDLE_REQUEST_OPEN_xxx`, require the `GPIOHANDLE_REQUEST_OUTPUT` to be set. Only one drive flag may be set. If none are set then the line is assumed push-pull.

Only one bias flag, `GPIOHANDLE_REQUEST_BIAS_xxx`, may be set, and it requires a direction flag to also be set. If no bias flags are set then the bias configuration is not changed.

Requesting an invalid configuration is an error (**EINVAL**).

<a id="rst-configuration-support"></a>
<a id="rst-gpio-get-linehandle-config-support"></a>

### Configuration Support

Where the requested configuration is not directly supported by the underlying hardware and driver, the kernel applies one of these approaches:

> - reject the request
>
> - emulate the feature in software
>
> - treat the feature as best effort

The approach applied depends on whether the feature can reasonably be emulated in software, and the impact on the hardware and userspace if the feature is not supported. The approach applied for each feature is as follows:


<table>
<thead>
<tr>
<th>


Feature

</th>
<th>


Approach

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


Bias

</td>
<td>


best effort

</td>
</tr>
<tr>
<td>


Direction

</td>
<td>


reject

</td>
</tr>
<tr>
<td>


Drive

</td>
<td>


emulate

</td>
</tr>
</tbody>
</table>

Bias is treated as best effort to allow userspace to apply the same configuration for platforms that support internal bias as those that require external bias. Worst case the line floats rather than being biased as expected.

Drive is emulated by switching the line to an input when the line should not be driven.

In all cases, the configuration reported by [gpio-get-lineinfo-ioctl.rst](~kernel/userspace/userspace-api/gpio/gpio-get-lineinfo-ioctl) is the requested configuration, not the resulting hardware configuration. Userspace cannot determine if a feature is supported in hardware, is emulated, or is best effort.

<a id="rst-return-value"></a>

## Return Value

On success 0 and the `request.fd<gpiohandle_request>` contains the file descriptor for the request.

On error -1 and the `errno` variable is set appropriately. Common error codes are described in [error-codes.rst](~kernel/userspace/userspace-api/gpio/error-codes).
