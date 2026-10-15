---
title: "ioctl MEDIA_IOC_DEVICE_INFO"
type: reference
description: "MEDIA_IOC_DEVICE_INFO - Query device information"
---

<a id="rst-ioctl-media-ioc-device-info"></a>
<a id="rst-media-ioc-device-info"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: MC -->

<a id="rst-name"></a>

## Name

MEDIA_IOC_DEVICE_INFO - Query device information

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-MEDIA_IOC_DEVICE_INFO"></a>

```c
MEDIA_IOC_DEVICE_INFO
```

`int ioctl(int fd, MEDIA_IOC_DEVICE_INFO, struct media_device_info *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to struct `media_device_info`.

<a id="rst-description"></a>

## Description

All media devices must support the `MEDIA_IOC_DEVICE_INFO` ioctl. To query device information, applications call the ioctl with a pointer to a struct `media_device_info`. The driver fills the structure and returns the information to the application. The ioctl never fails.





<a id="c-media_device_info"></a>

```c
media_device_info
```

<!-- tabularcolumns: |p{4.4cm}|p{4.4cm}|p{8.5cm}| -->


<table>
<caption>struct media_device_info</caption>
<tbody>
<tr>
<td>


char

</td>
<td>


`driver`\[16\]

</td>
<td>


Name of the driver implementing the media API as a NUL-terminated ASCII string. The driver version is stored in the `driver_version` field.

Driver specific applications can use this information to verify the driver identity. It is also useful to work around known bugs, or to identify drivers in error reports.

</td>
</tr>
<tr>
<td>


char

</td>
<td>


`model`\[32\]

</td>
<td>


Device model name as a NUL-terminated UTF-8 string. The device version is stored in the `device_version` field and is not be appended to the model name.

</td>
</tr>
<tr>
<td>


char

</td>
<td>


`serial`\[40\]

</td>
<td>


Serial number as a NUL-terminated ASCII string.

</td>
</tr>
<tr>
<td>


char

</td>
<td>


`bus_info`\[32\]

</td>
<td>


Location of the device in the system as a NUL-terminated ASCII string. This includes the bus type name (PCI, USB, ...) and a bus-specific identifier.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`media_version`

</td>
<td>


Media API version, formatted with the `KERNEL_VERSION()` macro.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`hw_revision`

</td>
<td>


Hardware device revision in a driver-specific format.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`driver_version`

</td>
<td>


Media device driver version, formatted with the `KERNEL_VERSION()` macro. Together with the `driver` field this identifies a particular driver.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`reserved`\[31\]

</td>
<td>


Reserved for future extensions. Drivers and applications must set this array to zero.

</td>
</tr>
</tbody>
</table>

The `serial` and `bus_info` fields can be used to distinguish between multiple instances of otherwise identical hardware. The serial number takes precedence when provided and can be assumed to be unique. If the serial number is an empty string, the `bus_info` field can be used instead. The `bus_info` field is guaranteed to be unique, but can vary across reboots or device unplug/replug.

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
