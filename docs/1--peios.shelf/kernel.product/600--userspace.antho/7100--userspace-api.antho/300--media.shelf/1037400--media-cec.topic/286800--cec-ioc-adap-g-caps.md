---
title: "ioctl CEC_ADAP_G_CAPS"
type: reference
description: "CEC_ADAP_G_CAPS - Query device capabilities"
---

<a id="rst-ioctl-cec-adap-g-caps"></a>
<a id="rst-cec-adap-g-caps"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: CEC -->

<a id="rst-name"></a>

## Name

CEC_ADAP_G_CAPS - Query device capabilities

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-CEC_ADAP_G_CAPS"></a>

```c
CEC_ADAP_G_CAPS
```

`int ioctl(int fd, CEC_ADAP_G_CAPS, struct cec_caps *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

`argp`

<a id="rst-description"></a>

## Description

All cec devices must support [ioctl CEC_ADAP_G_CAPS](<#rst-cec-adap-g-caps>). To query device information, applications call the ioctl with a pointer to a struct `cec_caps`. The driver fills the structure and returns the information to the application. The ioctl never fails.

<!-- tabularcolumns: |p{1.2cm}|p{2.5cm}|p{13.6cm}| -->





<a id="c-cec_caps"></a>

```c
cec_caps
```


<table>
<caption>struct cec_caps</caption>
<tbody>
<tr>
<td>


char

</td>
<td>


`driver[32]`

</td>
<td>


The name of the cec adapter driver.

</td>
</tr>
<tr>
<td>


char

</td>
<td>


`name[32]`

</td>
<td>


The name of this CEC adapter. The combination `driver` and `name` must be unique.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`available_log_addrs`

</td>
<td>


The maximum number of logical addresses that can be configured.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`capabilities`

</td>
<td>


The capabilities of the CEC adapter, see [cec-capabilities](<#rst-cec-capabilities>).

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`version`

</td>
<td>


CEC Framework API version, formatted with the `KERNEL_VERSION()` macro.

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{4.4cm}|p{2.5cm}|p{10.4cm}| -->

<a id="rst-cec-capabilities"></a>


<table>
<caption>CEC Capabilities Flags</caption>
<tbody>
<tr>
<td>


`CEC_CAP_PHYS_ADDR`

</td>
<td>


0x00000001

</td>
<td>


<a id="rst-cec-cap-phys-addr"></a>

Userspace has to configure the physical address by calling [ioctl CEC_ADAP_S_PHYS_ADDR](<~kernel/userspace/userspace-api/media-cec/cec-ioc-adap-g-phys-addr#rst-cec-adap-s-phys-addr>). If this capability isn't set, then setting the physical address is handled by the kernel whenever the EDID is set (for an HDMI receiver) or read (for an HDMI transmitter).

</td>
</tr>
<tr>
<td>


`CEC_CAP_LOG_ADDRS`

</td>
<td>


0x00000002

</td>
<td>


<a id="rst-cec-cap-log-addrs"></a>

Userspace has to configure the logical addresses by calling [ioctl CEC_ADAP_S_LOG_ADDRS](<~kernel/userspace/userspace-api/media-cec/cec-ioc-adap-g-log-addrs#rst-cec-adap-s-log-addrs>). If this capability isn't set, then the kernel will have configured this.

</td>
</tr>
<tr>
<td>


`CEC_CAP_TRANSMIT`

</td>
<td>


0x00000004

</td>
<td>


<a id="rst-cec-cap-transmit"></a>

Userspace can transmit CEC messages by calling [ioctl CEC_TRANSMIT](<~kernel/userspace/userspace-api/media-cec/cec-ioc-receive#rst-cec-transmit>). This implies that userspace can be a follower as well, since being able to transmit messages is a prerequisite of becoming a follower. If this capability isn't set, then the kernel will handle all CEC transmits and process all CEC messages it receives.

</td>
</tr>
<tr>
<td>


`CEC_CAP_PASSTHROUGH`

</td>
<td>


0x00000008

</td>
<td>


<a id="rst-cec-cap-passthrough"></a>

Userspace can use the passthrough mode by calling [ioctl CEC_S_MODE](<~kernel/userspace/userspace-api/media-cec/cec-ioc-g-mode#rst-cec-s-mode>).

</td>
</tr>
<tr>
<td>


`CEC_CAP_RC`

</td>
<td>


0x00000010

</td>
<td>


<a id="rst-cec-cap-rc"></a>

This adapter supports the remote control protocol.

</td>
</tr>
<tr>
<td>


`CEC_CAP_MONITOR_ALL`

</td>
<td>


0x00000020

</td>
<td>


<a id="rst-cec-cap-monitor-all"></a>

The CEC hardware can monitor all messages, not just directed and broadcast messages.

</td>
</tr>
<tr>
<td>


`CEC_CAP_NEEDS_HPD`

</td>
<td>


0x00000040

</td>
<td>


<a id="rst-cec-cap-needs-hpd"></a>

The CEC hardware is only active if the HDMI Hotplug Detect pin is high. This makes it impossible to use CEC to wake up displays that set the HPD pin low when in standby mode, but keep the CEC bus alive.

</td>
</tr>
<tr>
<td>


`CEC_CAP_MONITOR_PIN`

</td>
<td>


0x00000080

</td>
<td>


<a id="rst-cec-cap-monitor-pin"></a>

The CEC hardware can monitor CEC pin changes from low to high voltage and vice versa. When in pin monitoring mode the application will receive `CEC_EVENT_PIN_CEC_LOW` and `CEC_EVENT_PIN_CEC_HIGH` events.

</td>
</tr>
<tr>
<td>


`CEC_CAP_CONNECTOR_INFO`

</td>
<td>


0x00000100

</td>
<td>


<a id="rst-cec-cap-connector-info"></a>

If this capability is set, then [ioctl CEC_ADAP_G_CONNECTOR_INFO](<~kernel/userspace/userspace-api/media-cec/cec-ioc-adap-g-conn-info#rst-cec-adap-g-connector-info>) can be used.

</td>
</tr>
<tr>
<td>


`CEC_CAP_REPLY_VENDOR_ID`

</td>
<td>


0x00000200

</td>
<td>


<a id="rst-cec-cap-reply-vendor-id"></a>

If this capability is set, then [CEC_MSG_FL_REPLY_VENDOR_ID](<~kernel/userspace/userspace-api/media-cec/cec-ioc-receive#rst-cec-msg-flags>) can be used.

</td>
</tr>
</tbody>
</table>

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
