---
title: "ioctls CEC_ADAP_G_LOG_ADDRS and CEC_ADAP_S_LOG_ADDRS"
type: reference
description: "CEC_ADAP_G_LOG_ADDRS, CEC_ADAP_S_LOG_ADDRS - Get or set the logical addresses"
---

<a id="rst-ioctls-cec-adap-g-log-addrs-and-cec-adap-s-log-addrs"></a>
<a id="rst-cec-adap-s-log-addrs"></a>
<a id="rst-cec-adap-g-log-addrs"></a>
<a id="rst-cec-adap-log-addrs"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: CEC -->

<a id="rst-name"></a>

## Name

CEC_ADAP_G_LOG_ADDRS, CEC_ADAP_S_LOG_ADDRS - Get or set the logical addresses

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-CEC_ADAP_G_LOG_ADDRS"></a>

```c
CEC_ADAP_G_LOG_ADDRS
```

`int ioctl(int fd, CEC_ADAP_G_LOG_ADDRS, struct cec_log_addrs *argp)`





<a id="c-CEC_ADAP_S_LOG_ADDRS"></a>

```c
CEC_ADAP_S_LOG_ADDRS
```

`int ioctl(int fd, CEC_ADAP_S_LOG_ADDRS, struct cec_log_addrs *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to struct `cec_log_addrs`.

<a id="rst-description"></a>

## Description

To query the current CEC logical addresses, applications call [ioctl CEC_ADAP_G_LOG_ADDRS](<#rst-cec-adap-g-log-addrs>) with a pointer to a struct `cec_log_addrs` where the driver stores the logical addresses.

To set new logical addresses, applications fill in struct `cec_log_addrs` and call [ioctl CEC_ADAP_S_LOG_ADDRS](<#rst-cec-adap-s-log-addrs>) with a pointer to this struct. The [ioctl CEC_ADAP_S_LOG_ADDRS](<#rst-cec-adap-s-log-addrs>) is only available if `CEC_CAP_LOG_ADDRS` is set (the `ENOTTY` error code is returned otherwise). The [ioctl CEC_ADAP_S_LOG_ADDRS](<#rst-cec-adap-s-log-addrs>) can only be called by a file descriptor in initiator mode (see [ioctls CEC_G_MODE and CEC_S_MODE](<~kernel/userspace/userspace-api/media-cec/cec-ioc-g-mode#rst-cec-s-mode>)), if not the `EBUSY` error code will be returned.

To clear existing logical addresses set `num_log_addrs` to 0. All other fields will be ignored in that case. The adapter will go to the unconfigured state and the `cec_version`, `vendor_id` and `osd_name` fields are all reset to their default values (CEC version 2.0, no vendor ID and an empty OSD name).

If the physical address is valid (see [ioctl CEC_ADAP_S_PHYS_ADDR](<~kernel/userspace/userspace-api/media-cec/cec-ioc-adap-g-phys-addr#rst-cec-adap-s-phys-addr>)), then this ioctl will block until all requested logical addresses have been claimed. If the file descriptor is in non-blocking mode then it will not wait for the logical addresses to be claimed, instead it just returns 0.

A [CEC_EVENT_STATE_CHANGE](<~kernel/userspace/userspace-api/media-cec/cec-ioc-dqevent#rst-cec-event-state-change>) event is sent when the logical addresses are claimed or cleared.

Attempting to call [ioctl CEC_ADAP_S_LOG_ADDRS](<#rst-cec-adap-s-log-addrs>) when logical address types are already defined will return with error `EBUSY`.





<a id="c-cec_log_addrs"></a>

```c
cec_log_addrs
```

<!-- tabularcolumns: |p{1.0cm}|p{8.0cm}|p{8.0cm}| -->


<table>
<caption>struct cec_log_addrs</caption>
<tbody>
<tr>
<td>


\__u8

</td>
<td>


`log_addr[CEC_MAX_LOG_ADDRS]`

</td>
<td>


The actual logical addresses that were claimed. This is set by the driver. If no logical address could be claimed, then it is set to `CEC_LOG_ADDR_INVALID`. If this adapter is Unregistered, then `log_addr[0]` is set to 0xf and all others to `CEC_LOG_ADDR_INVALID`.

</td>
</tr>
<tr>
<td>


\__u16

</td>
<td>


`log_addr_mask`

</td>
<td>


The bitmask of all logical addresses this adapter has claimed. If this adapter is Unregistered then `log_addr_mask` sets bit 15 and clears all other bits. If this adapter is not configured at all, then `log_addr_mask` is set to 0. Set by the driver.

</td>
</tr>
<tr>
<td>


\__u8

</td>
<td>


`cec_version`

</td>
<td>


The CEC version that this adapter shall use. See [cec-versions](<#rst-cec-versions>). Used to implement the `CEC_MSG_CEC_VERSION` and `CEC_MSG_REPORT_FEATURES` messages. Note that [CEC_OP_CEC_VERSION_1_3A](<#rst-cec-op-cec-version-1-3a>) is not allowed by the CEC framework.

</td>
</tr>
<tr>
<td>


\__u8

</td>
<td>


`num_log_addrs`

</td>
<td>


Number of logical addresses to set up. Must be ≤ `available_log_addrs` as returned by [ioctl CEC_ADAP_G_CAPS](<~kernel/userspace/userspace-api/media-cec/cec-ioc-adap-g-caps#rst-cec-adap-g-caps>). All arrays in this structure are only filled up to index `available_log_addrs`-1. The remaining array elements will be ignored. Note that the CEC 2.0 standard allows for a maximum of 2 logical addresses, although some hardware has support for more. `CEC_MAX_LOG_ADDRS` is 4. The driver will return the actual number of logical addresses it could claim, which may be less than what was requested. If this field is set to 0, then the CEC adapter shall clear all claimed logical addresses and all other fields will be ignored.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`vendor_id`

</td>
<td>


The vendor ID is a 24-bit number that identifies the specific vendor or entity. Based on this ID vendor specific commands may be defined. If you do not want a vendor ID then set it to `CEC_VENDOR_ID_NONE`.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`flags`

</td>
<td>


Flags. See [cec-log-addrs-flags](<#rst-cec-log-addrs-flags>) for a list of available flags.

</td>
</tr>
<tr>
<td>


char

</td>
<td>


`osd_name[15]`

</td>
<td>


The On-Screen Display name as is returned by the `CEC_MSG_SET_OSD_NAME` message.

</td>
</tr>
<tr>
<td>


\__u8

</td>
<td>


`primary_device_type[CEC_MAX_LOG_ADDRS]`

</td>
<td>


Primary device type for each logical address. See [cec-prim-dev-types](<#rst-cec-prim-dev-types>) for possible types.

</td>
</tr>
<tr>
<td>


\__u8

</td>
<td>


`log_addr_type[CEC_MAX_LOG_ADDRS]`

</td>
<td>


Logical address types. See [cec-log-addr-types](<#rst-cec-log-addr-types>) for possible types. The driver will update this with the actual logical address type that it claimed (e.g. it may have to fallback to [CEC_LOG_ADDR_TYPE_UNREGISTERED](<#rst-cec-log-addr-type-unregistered>)).

</td>
</tr>
<tr>
<td>


\__u8

</td>
<td>


`all_device_types[CEC_MAX_LOG_ADDRS]`

</td>
<td>


CEC 2.0 specific: the bit mask of all device types. See [cec-all-dev-types-flags](<#rst-cec-all-dev-types-flags>). It is used in the CEC 2.0 `CEC_MSG_REPORT_FEATURES` message. For CEC 1.4 you can either leave this field to 0, or fill it in according to the CEC 2.0 guidelines to give the CEC framework more information about the device type, even though the framework won't use it directly in the CEC message.

</td>
</tr>
<tr>
<td>


\__u8

</td>
<td>


`features[CEC_MAX_LOG_ADDRS][12]`

</td>
<td>


Features for each logical address. It is used in the CEC 2.0 `CEC_MSG_REPORT_FEATURES` message. The 12 bytes include both the RC Profile and the Device Features. For CEC 1.4 you can either leave this field to all 0, or fill it in according to the CEC 2.0 guidelines to give the CEC framework more information about the device type, even though the framework won't use it directly in the CEC message.

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{7.8cm}|p{1.0cm}|p{8.5cm}| -->

<a id="rst-cec-log-addrs-flags"></a>


<table>
<caption>Flags for struct cec_log_addrs</caption>
<tbody>
<tr>
<td>


`CEC_LOG_ADDRS_FL_ALLOW_UNREG_FALLBACK`

</td>
<td>


1

</td>
<td>


<a id="rst-cec-log-addrs-fl-allow-unreg-fallback"></a>

By default if no logical address of the requested type can be claimed, then it will go back to the unconfigured state. If this flag is set, then it will fallback to the Unregistered logical address. Note that if the Unregistered logical address was explicitly requested, then this flag has no effect.

</td>
</tr>
<tr>
<td>


`CEC_LOG_ADDRS_FL_ALLOW_RC_PASSTHRU`

</td>
<td>


2

</td>
<td>


<a id="rst-cec-log-addrs-fl-allow-rc-passthru"></a>

By default the `CEC_MSG_USER_CONTROL_PRESSED` and `CEC_MSG_USER_CONTROL_RELEASED` messages are only passed on to the follower(s), if any. If this flag is set, then these messages are also passed on to the remote control input subsystem and will appear as keystrokes. This features needs to be enabled explicitly. If CEC is used to enter e.g. passwords, then you may not want to enable this to avoid trivial snooping of the keystrokes.

</td>
</tr>
<tr>
<td>


`CEC_LOG_ADDRS_FL_CDC_ONLY`

</td>
<td>


4

</td>
<td>


<a id="rst-cec-log-addrs-fl-cdc-only"></a>

If this flag is set, then the device is CDC-Only. CDC-Only CEC devices are CEC devices that can only handle CDC messages.

All other messages are ignored.

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{7.8cm}|p{1.0cm}|p{8.5cm}| -->

<a id="rst-cec-versions"></a>


<table>
<caption>CEC Versions</caption>
<tbody>
<tr>
<td>


`CEC_OP_CEC_VERSION_1_3A`

</td>
<td>


4

</td>
<td>


<a id="rst-cec-op-cec-version-1-3a"></a>

CEC version according to the HDMI 1.3a standard.

</td>
</tr>
<tr>
<td>


`CEC_OP_CEC_VERSION_1_4B`

</td>
<td>


5

</td>
<td>


<a id="rst-cec-op-cec-version-1-4b"></a>

CEC version according to the HDMI 1.4b standard.

</td>
</tr>
<tr>
<td>


`CEC_OP_CEC_VERSION_2_0`

</td>
<td>


6

</td>
<td>


<a id="rst-cec-op-cec-version-2-0"></a>

CEC version according to the HDMI 2.0 standard.

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{6.6cm}|p{2.2cm}|p{8.5cm}| -->

<a id="rst-cec-prim-dev-types"></a>


<table>
<caption>CEC Primary Device Types</caption>
<tbody>
<tr>
<td>


`CEC_OP_PRIM_DEVTYPE_TV`

</td>
<td>


0

</td>
<td>


<a id="rst-cec-op-prim-devtype-tv"></a>

Use for a TV.

</td>
</tr>
<tr>
<td>


`CEC_OP_PRIM_DEVTYPE_RECORD`

</td>
<td>


1

</td>
<td>


<a id="rst-cec-op-prim-devtype-record"></a>

Use for a recording device.

</td>
</tr>
<tr>
<td>


`CEC_OP_PRIM_DEVTYPE_TUNER`

</td>
<td>


3

</td>
<td>


<a id="rst-cec-op-prim-devtype-tuner"></a>

Use for a device with a tuner.

</td>
</tr>
<tr>
<td>


`CEC_OP_PRIM_DEVTYPE_PLAYBACK`

</td>
<td>


4

</td>
<td>


<a id="rst-cec-op-prim-devtype-playback"></a>

Use for a playback device.

</td>
</tr>
<tr>
<td>


`CEC_OP_PRIM_DEVTYPE_AUDIOSYSTEM`

</td>
<td>


5

</td>
<td>


<a id="rst-cec-op-prim-devtype-audiosystem"></a>

Use for an audio system (e.g. an audio/video receiver).

</td>
</tr>
<tr>
<td>


`CEC_OP_PRIM_DEVTYPE_SWITCH`

</td>
<td>


6

</td>
<td>


<a id="rst-cec-op-prim-devtype-switch"></a>

Use for a CEC switch.

</td>
</tr>
<tr>
<td>


`CEC_OP_PRIM_DEVTYPE_VIDEOPROC`

</td>
<td>


7

</td>
<td>


<a id="rst-cec-op-prim-devtype-videoproc"></a>

Use for a video processor device.

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{6.6cm}|p{2.2cm}|p{8.5cm}| -->

<a id="rst-cec-log-addr-types"></a>


<table>
<caption>CEC Logical Address Types</caption>
<tbody>
<tr>
<td>


`CEC_LOG_ADDR_TYPE_TV`

</td>
<td>


0

</td>
<td>


<a id="rst-cec-log-addr-type-tv"></a>

Use for a TV.

</td>
</tr>
<tr>
<td>


`CEC_LOG_ADDR_TYPE_RECORD`

</td>
<td>


1

</td>
<td>


<a id="rst-cec-log-addr-type-record"></a>

Use for a recording device.

</td>
</tr>
<tr>
<td>


`CEC_LOG_ADDR_TYPE_TUNER`

</td>
<td>


2

</td>
<td>


<a id="rst-cec-log-addr-type-tuner"></a>

Use for a tuner device.

</td>
</tr>
<tr>
<td>


`CEC_LOG_ADDR_TYPE_PLAYBACK`

</td>
<td>


3

</td>
<td>


<a id="rst-cec-log-addr-type-playback"></a>

Use for a playback device.

</td>
</tr>
<tr>
<td>


`CEC_LOG_ADDR_TYPE_AUDIOSYSTEM`

</td>
<td>


4

</td>
<td>


<a id="rst-cec-log-addr-type-audiosystem"></a>

Use for an audio system device.

</td>
</tr>
<tr>
<td>


`CEC_LOG_ADDR_TYPE_SPECIFIC`

</td>
<td>


5

</td>
<td>


<a id="rst-cec-log-addr-type-specific"></a>

Use for a second TV or for a video processor device.

</td>
</tr>
<tr>
<td>


`CEC_LOG_ADDR_TYPE_UNREGISTERED`

</td>
<td>


6

</td>
<td>


<a id="rst-cec-log-addr-type-unregistered"></a>

Use this if you just want to remain unregistered. Used for pure CEC switches or CDC-only devices (CDC: Capability Discovery and Control).

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{6.6cm}|p{2.2cm}|p{8.5cm}| -->

<a id="rst-cec-all-dev-types-flags"></a>


<table>
<caption>CEC All Device Types Flags</caption>
<tbody>
<tr>
<td>


`CEC_OP_ALL_DEVTYPE_TV`

</td>
<td>


0x80

</td>
<td>


<a id="rst-cec-op-all-devtype-tv"></a>

This supports the TV type.

</td>
</tr>
<tr>
<td>


`CEC_OP_ALL_DEVTYPE_RECORD`

</td>
<td>


0x40

</td>
<td>


<a id="rst-cec-op-all-devtype-record"></a>

This supports the Recording type.

</td>
</tr>
<tr>
<td>


`CEC_OP_ALL_DEVTYPE_TUNER`

</td>
<td>


0x20

</td>
<td>


<a id="rst-cec-op-all-devtype-tuner"></a>

This supports the Tuner type.

</td>
</tr>
<tr>
<td>


`CEC_OP_ALL_DEVTYPE_PLAYBACK`

</td>
<td>


0x10

</td>
<td>


<a id="rst-cec-op-all-devtype-playback"></a>

This supports the Playback type.

</td>
</tr>
<tr>
<td>


`CEC_OP_ALL_DEVTYPE_AUDIOSYSTEM`

</td>
<td>


0x08

</td>
<td>


<a id="rst-cec-op-all-devtype-audiosystem"></a>

This supports the Audio System type.

</td>
</tr>
<tr>
<td>


`CEC_OP_ALL_DEVTYPE_SWITCH`

</td>
<td>


0x04

</td>
<td>


<a id="rst-cec-op-all-devtype-switch"></a>

This supports the CEC Switch or Video Processing type.

</td>
</tr>
</tbody>
</table>

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

The [ioctl CEC_ADAP_S_LOG_ADDRS](<#rst-cec-adap-s-log-addrs>) can return the following error codes:

- **ENOTTY**

  The `CEC_CAP_LOG_ADDRS` capability wasn't set, so this ioctl is not supported.

- **EBUSY**

  The CEC adapter is currently configuring itself, or it is already configured and `num_log_addrs` is non-zero, or another filehandle is in exclusive follower or initiator mode, or the filehandle is in mode `CEC_MODE_NO_INITIATOR`.

- **EINVAL**

  The contents of struct `cec_log_addrs` is invalid.
