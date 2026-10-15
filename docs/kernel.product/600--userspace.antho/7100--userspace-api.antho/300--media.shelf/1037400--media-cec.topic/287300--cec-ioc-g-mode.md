---
title: "ioctls CEC_G_MODE and CEC_S_MODE"
type: reference
description: "CEC_G_MODE, CEC_S_MODE - Get or set exclusive use of the CEC adapter"
---

<a id="rst-ioctls-cec-g-mode-and-cec-s-mode"></a>
<a id="rst-cec-s-mode"></a>
<a id="rst-cec-g-mode"></a>
<a id="rst-cec-mode"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: CEC -->

CEC_G_MODE, CEC_S_MODE - Get or set exclusive use of the CEC adapter

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-CEC_G_MODE"></a>

```c
CEC_G_MODE
```

`int ioctl(int fd, CEC_G_MODE, __u32 *argp)`





<a id="c-CEC_S_MODE"></a>

```c
CEC_S_MODE
```

`int ioctl(int fd, CEC_S_MODE, __u32 *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to CEC mode.

<a id="rst-description"></a>

## Description

By default any filehandle can use [ioctls CEC_RECEIVE and CEC_TRANSMIT](<~kernel/userspace/userspace-api/media-cec/cec-ioc-receive#rst-cec-transmit>), but in order to prevent applications from stepping on each others toes it must be possible to obtain exclusive access to the CEC adapter. This ioctl sets the filehandle to initiator and/or follower mode which can be exclusive depending on the chosen mode. The initiator is the filehandle that is used to initiate messages, i.e. it commands other CEC devices. The follower is the filehandle that receives messages sent to the CEC adapter and processes them. The same filehandle can be both initiator and follower, or this role can be taken by two different filehandles.

When a CEC message is received, then the CEC framework will decide how it will be processed. If the message is a reply to an earlier transmitted message, then the reply is sent back to the filehandle that is waiting for it. In addition the CEC framework will process it.

If the message is not a reply, then the CEC framework will process it first. If there is no follower, then the message is just discarded and a feature abort is sent back to the initiator if the framework couldn't process it. If there is a follower, then the message is passed on to the follower who will use [ioctl CEC_RECEIVE](<~kernel/userspace/userspace-api/media-cec/cec-ioc-receive#rst-cec-receive>) to dequeue the new message. The framework expects the follower to make the right decisions.

The CEC framework will process core messages unless requested otherwise by the follower. The follower can enable the passthrough mode. In that case, the CEC framework will pass on most core messages without processing them and the follower will have to implement those messages. There are some messages that the core will always process, regardless of the passthrough mode. See [cec-core-processing](<#rst-cec-core-processing>) for details.

If there is no initiator, then any CEC filehandle can use [ioctl CEC_TRANSMIT](<~kernel/userspace/userspace-api/media-cec/cec-ioc-receive#rst-cec-transmit>). If there is an exclusive initiator then only that initiator can call [ioctls CEC_RECEIVE and CEC_TRANSMIT](<~kernel/userspace/userspace-api/media-cec/cec-ioc-receive#rst-cec-transmit>). The follower can of course always call [ioctl CEC_TRANSMIT](<~kernel/userspace/userspace-api/media-cec/cec-ioc-receive#rst-cec-transmit>).

Available initiator modes are:

<!-- tabularcolumns: |p{5.6cm}|p{0.9cm}|p{10.8cm}| -->

<a id="rst-cec-mode-initiator-e"></a>


<table>
<caption>Initiator Modes</caption>
<tbody>
<tr>
<td>


`CEC_MODE_NO_INITIATOR`

</td>
<td>


0x0

</td>
<td>


<a id="rst-cec-mode-no-initiator"></a>

This is not an initiator, i.e. it cannot transmit CEC messages or make any other changes to the CEC adapter.

</td>
</tr>
<tr>
<td>


`CEC_MODE_INITIATOR`

</td>
<td>


0x1

</td>
<td>


<a id="rst-cec-mode-initiator"></a>

This is an initiator (the default when the device is opened) and it can transmit CEC messages and make changes to the CEC adapter, unless there is an exclusive initiator.

</td>
</tr>
<tr>
<td>


`CEC_MODE_EXCL_INITIATOR`

</td>
<td>


0x2

</td>
<td>


<a id="rst-cec-mode-excl-initiator"></a>

This is an exclusive initiator and this file descriptor is the only one that can transmit CEC messages and make changes to the CEC adapter. If someone else is already the exclusive initiator then an attempt to become one will return the `EBUSY` error code error.

</td>
</tr>
</tbody>
</table>

Available follower modes are:

<!-- tabularcolumns: |p{6.6cm}|p{0.9cm}|p{9.8cm}| -->

<a id="rst-cec-mode-follower-e"></a>


<table>
<caption>Follower Modes</caption>
<tbody>
<tr>
<td>


`CEC_MODE_NO_FOLLOWER`

</td>
<td>


0x00

</td>
<td>


<a id="rst-cec-mode-no-follower"></a>

This is not a follower (the default when the device is opened).

</td>
</tr>
<tr>
<td>


`CEC_MODE_FOLLOWER`

</td>
<td>


0x10

</td>
<td>


<a id="rst-cec-mode-follower"></a>

This is a follower and it will receive CEC messages unless there is an exclusive follower. You cannot become a follower if [CEC_CAP_TRANSMIT](<~kernel/userspace/userspace-api/media-cec/cec-ioc-adap-g-caps#rst-cec-cap-transmit>) is not set or if [CEC_MODE_NO_INITIATOR](<#rst-cec-mode-no-initiator>) was specified, the `EINVAL` error code is returned in that case.

</td>
</tr>
<tr>
<td>


`CEC_MODE_EXCL_FOLLOWER`

</td>
<td>


0x20

</td>
<td>


<a id="rst-cec-mode-excl-follower"></a>

This is an exclusive follower and only this file descriptor will receive CEC messages for processing. If someone else is already the exclusive follower then an attempt to become one will return the `EBUSY` error code. You cannot become a follower if [CEC_CAP_TRANSMIT](<~kernel/userspace/userspace-api/media-cec/cec-ioc-adap-g-caps#rst-cec-cap-transmit>) is not set or if [CEC_MODE_NO_INITIATOR](<#rst-cec-mode-no-initiator>) was specified, the `EINVAL` error code is returned in that case.

</td>
</tr>
<tr>
<td>


`CEC_MODE_EXCL_FOLLOWER_PASSTHRU`

</td>
<td>


0x30

</td>
<td>


<a id="rst-cec-mode-excl-follower-passthru"></a>

This is an exclusive follower and only this file descriptor will receive CEC messages for processing. In addition it will put the CEC device into passthrough mode, allowing the exclusive follower to handle most core messages instead of relying on the CEC framework for that. If someone else is already the exclusive follower then an attempt to become one will return the `EBUSY` error code. You cannot become a follower if [CEC_CAP_TRANSMIT](<~kernel/userspace/userspace-api/media-cec/cec-ioc-adap-g-caps#rst-cec-cap-transmit>) is not set or if [CEC_MODE_NO_INITIATOR](<#rst-cec-mode-no-initiator>) was specified, the `EINVAL` error code is returned in that case.

</td>
</tr>
<tr>
<td>


`CEC_MODE_MONITOR_PIN`

</td>
<td>


0xd0

</td>
<td>


<a id="rst-cec-mode-monitor-pin"></a>

Put the file descriptor into pin monitoring mode. Can only be used in combination with [CEC_MODE_NO_INITIATOR](<#rst-cec-mode-no-initiator>), otherwise the `EINVAL` error code will be returned. This mode requires that the [CEC_CAP_MONITOR_PIN](<~kernel/userspace/userspace-api/media-cec/cec-ioc-adap-g-caps#rst-cec-cap-monitor-pin>) capability is set, otherwise the `EINVAL` error code is returned. While in pin monitoring mode this file descriptor can receive the `CEC_EVENT_PIN_CEC_LOW` and `CEC_EVENT_PIN_CEC_HIGH` events to see the low-level CEC pin transitions. This is very useful for debugging. This mode is only allowed if the process has the `CAP_NET_ADMIN` capability. If that is not set, then the `EPERM` error code is returned.

</td>
</tr>
<tr>
<td>


`CEC_MODE_MONITOR`

</td>
<td>


0xe0

</td>
<td>


<a id="rst-cec-mode-monitor"></a>

Put the file descriptor into monitor mode. Can only be used in combination with [CEC_MODE_NO_INITIATOR](<#rst-cec-mode-no-initiator>), otherwise the `EINVAL` error code will be returned. In monitor mode all messages this CEC device transmits and all messages it receives (both broadcast messages and directed messages for one its logical addresses) will be reported. This is very useful for debugging. This is only allowed if the process has the `CAP_NET_ADMIN` capability. If that is not set, then the `EPERM` error code is returned.

</td>
</tr>
<tr>
<td>


`CEC_MODE_MONITOR_ALL`

</td>
<td>


0xf0

</td>
<td>


<a id="rst-cec-mode-monitor-all"></a>

Put the file descriptor into 'monitor all' mode. Can only be used in combination with [CEC_MODE_NO_INITIATOR](<#rst-cec-mode-no-initiator>), otherwise the `EINVAL` error code will be returned. In 'monitor all' mode all messages this CEC device transmits and all messages it receives, including directed messages for other CEC devices, will be reported. This is very useful for debugging, but not all devices support this. This mode requires that the [CEC_CAP_MONITOR_ALL](<~kernel/userspace/userspace-api/media-cec/cec-ioc-adap-g-caps#rst-cec-cap-monitor-all>) capability is set, otherwise the `EINVAL` error code is returned. This is only allowed if the process has the `CAP_NET_ADMIN` capability. If that is not set, then the `EPERM` error code is returned.

</td>
</tr>
</tbody>
</table>

Core message processing details:

<!-- tabularcolumns: |p{6.6cm}|p{10.9cm}| -->

<a id="rst-cec-core-processing"></a>


<table>
<caption>Core Message Processing</caption>
<tbody>
<tr>
<td>


`CEC_MSG_GET_CEC_VERSION`

</td>
<td>


<a id="rst-cec-msg-get-cec-version"></a>

The core will return the CEC version that was set with [ioctl CEC_ADAP_S_LOG_ADDRS](<~kernel/userspace/userspace-api/media-cec/cec-ioc-adap-g-log-addrs#rst-cec-adap-s-log-addrs>), except when in passthrough mode. In passthrough mode the core does nothing and this message has to be handled by a follower instead.

</td>
</tr>
<tr>
<td>


`CEC_MSG_GIVE_DEVICE_VENDOR_ID`

</td>
<td>


<a id="rst-cec-msg-give-device-vendor-id"></a>

The core will return the vendor ID that was set with [ioctl CEC_ADAP_S_LOG_ADDRS](<~kernel/userspace/userspace-api/media-cec/cec-ioc-adap-g-log-addrs#rst-cec-adap-s-log-addrs>), except when in passthrough mode. In passthrough mode the core does nothing and this message has to be handled by a follower instead.

</td>
</tr>
<tr>
<td>


`CEC_MSG_ABORT`

</td>
<td>


<a id="rst-cec-msg-abort"></a>

The core will return a Feature Abort message with reason 'Feature Refused' as per the specification, except when in passthrough mode. In passthrough mode the core does nothing and this message has to be handled by a follower instead.

</td>
</tr>
<tr>
<td>


`CEC_MSG_GIVE_PHYSICAL_ADDR`

</td>
<td>


<a id="rst-cec-msg-give-physical-addr"></a>

The core will report the current physical address, except when in passthrough mode. In passthrough mode the core does nothing and this message has to be handled by a follower instead.

</td>
</tr>
<tr>
<td>


`CEC_MSG_GIVE_OSD_NAME`

</td>
<td>


<a id="rst-cec-msg-give-osd-name"></a>

The core will report the current OSD name that was set with [ioctl CEC_ADAP_S_LOG_ADDRS](<~kernel/userspace/userspace-api/media-cec/cec-ioc-adap-g-log-addrs#rst-cec-adap-s-log-addrs>), except when in passthrough mode. In passthrough mode the core does nothing and this message has to be handled by a follower instead.

</td>
</tr>
<tr>
<td>


`CEC_MSG_GIVE_FEATURES`

</td>
<td>


<a id="rst-cec-msg-give-features"></a>

The core will do nothing if the CEC version is older than 2.0, otherwise it will report the current features that were set with [ioctl CEC_ADAP_S_LOG_ADDRS](<~kernel/userspace/userspace-api/media-cec/cec-ioc-adap-g-log-addrs#rst-cec-adap-s-log-addrs>), except when in passthrough mode. In passthrough mode the core does nothing (for any CEC version) and this message has to be handled by a follower instead.

</td>
</tr>
<tr>
<td>


`CEC_MSG_USER_CONTROL_PRESSED`

</td>
<td>


<a id="rst-cec-msg-user-control-pressed"></a>

If [CEC_CAP_RC](<~kernel/userspace/userspace-api/media-cec/cec-ioc-adap-g-caps#rst-cec-cap-rc>) is set and if [CEC_LOG_ADDRS_FL_ALLOW_RC_PASSTHRU](<~kernel/userspace/userspace-api/media-cec/cec-ioc-adap-g-log-addrs#rst-cec-log-addrs-fl-allow-rc-passthru>) is set, then generate a remote control key press. This message is always passed on to the follower(s).

</td>
</tr>
<tr>
<td>


`CEC_MSG_USER_CONTROL_RELEASED`

</td>
<td>


<a id="rst-cec-msg-user-control-released"></a>

If [CEC_CAP_RC](<~kernel/userspace/userspace-api/media-cec/cec-ioc-adap-g-caps#rst-cec-cap-rc>) is set and if [CEC_LOG_ADDRS_FL_ALLOW_RC_PASSTHRU](<~kernel/userspace/userspace-api/media-cec/cec-ioc-adap-g-log-addrs#rst-cec-log-addrs-fl-allow-rc-passthru>) is set, then generate a remote control key release. This message is always passed on to the follower(s).

</td>
</tr>
<tr>
<td>


`CEC_MSG_REPORT_PHYSICAL_ADDR`

</td>
<td>


<a id="rst-cec-msg-report-physical-addr"></a>

The CEC framework will make note of the reported physical address and then just pass the message on to the follower(s).

</td>
</tr>
</tbody>
</table>

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

The [ioctl CEC_S_MODE](<#rst-cec-s-mode>) can return the following error codes:

- **EINVAL**

  The requested mode is invalid.

- **EPERM**

  Monitor mode is requested, but the process does have the `CAP_NET_ADMIN` capability.

- **EBUSY**

  Someone else is already an exclusive follower or initiator.
