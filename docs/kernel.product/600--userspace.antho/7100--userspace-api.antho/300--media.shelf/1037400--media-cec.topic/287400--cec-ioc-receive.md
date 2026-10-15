---
title: "ioctls CEC_RECEIVE and CEC_TRANSMIT"
type: reference
description: "CEC_RECEIVE, CEC_TRANSMIT - Receive or transmit a CEC message"
---

<a id="rst-ioctls-cec-receive-and-cec-transmit"></a>
<a id="rst-cec-receive"></a>
<a id="rst-cec-transmit"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: CEC -->

<a id="rst-name"></a>

## Name

CEC_RECEIVE, CEC_TRANSMIT - Receive or transmit a CEC message

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-CEC_RECEIVE"></a>

```c
CEC_RECEIVE
```

`int ioctl(int fd, CEC_RECEIVE, struct cec_msg *argp)`





<a id="c-CEC_TRANSMIT"></a>

```c
CEC_TRANSMIT
```

`int ioctl(int fd, CEC_TRANSMIT, struct cec_msg *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to struct cec_msg.

<a id="rst-description"></a>

## Description

To receive a CEC message the application has to fill in the `timeout` field of struct `cec_msg` and pass it to [ioctl CEC_RECEIVE](<#rst-cec-receive>). If the file descriptor is in non-blocking mode and there are no received messages pending, then it will return -1 and set errno to the `EAGAIN` error code. If the file descriptor is in blocking mode and `timeout` is non-zero and no message arrived within `timeout` milliseconds, then it will return -1 and set errno to the `ETIMEDOUT` error code.

A received message can be:

1. a message received from another CEC device (the `sequence` field will be 0, `tx_status` will be 0 and `rx_status` will be non-zero).

2. the transmit result of an earlier non-blocking transmit (the `sequence` field will be non-zero, `tx_status` will be non-zero and `rx_status` will be 0).

3. the reply to an earlier non-blocking transmit (the `sequence` field will be non-zero, `tx_status` will be 0 and `rx_status` will be non-zero).

To send a CEC message the application has to fill in the struct `cec_msg` and pass it to [ioctl CEC_TRANSMIT](<#rst-cec-transmit>). The [ioctl CEC_TRANSMIT](<#rst-cec-transmit>) is only available if `CEC_CAP_TRANSMIT` is set. If there is no more room in the transmit queue, then it will return -1 and set errno to the `EBUSY` error code. The transmit queue has enough room for 18 messages (about 1 second worth of 2-byte messages). Note that the CEC kernel framework will also reply to core messages (see [cec-core-processing](<~kernel/userspace/userspace-api/media-cec/cec-ioc-g-mode#rst-cec-core-processing>)), so it is not a good idea to fully fill up the transmit queue.

If the file descriptor is in non-blocking mode then the transmit will return 0 and the result of the transmit will be available via [ioctl CEC_RECEIVE](<#rst-cec-receive>) once the transmit has finished. If a non-blocking transmit also specified waiting for a reply, then the reply will arrive in a later message. The `sequence` field can be used to associate both transmit results and replies with the original transmit.

Normally calling [ioctl CEC_TRANSMIT](<#rst-cec-transmit>) when the physical address is invalid (due to e.g. a disconnect) will return `ENONET`.

However, the CEC specification allows sending messages from 'Unregistered' to 'TV' when the physical address is invalid since some TVs pull the hotplug detect pin of the HDMI connector low when they go into standby, or when switching to another input.

When the hotplug detect pin goes low the EDID disappears, and thus the physical address, but the cable is still connected and CEC still works. In order to detect/wake up the device it is allowed to send poll and 'Image/Text View On' messages from initiator 0xf ('Unregistered') to destination 0 ('TV').

<!-- tabularcolumns: |p{1.0cm}|p{3.5cm}|p{12.8cm}| -->





<a id="c-cec_msg"></a>

```c
cec_msg
```


<table>
<caption>struct cec_msg</caption>
<tbody>
<tr>
<td>


\__u64

</td>
<td>


`tx_ts`

</td>
<td>


Timestamp in ns of when the last byte of the message was transmitted. The timestamp has been taken from the `CLOCK_MONOTONIC` clock. To access the same clock from userspace use `clock_gettime()`.

</td>
</tr>
<tr>
<td>


\__u64

</td>
<td>


`rx_ts`

</td>
<td>


Timestamp in ns of when the last byte of the message was received. The timestamp has been taken from the `CLOCK_MONOTONIC` clock. To access the same clock from userspace use `clock_gettime()`.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`len`

</td>
<td>


The length of the message. For [ioctl CEC_TRANSMIT](<#rst-cec-transmit>) this is filled in by the application. The driver will fill this in for [ioctl CEC_RECEIVE](<#rst-cec-receive>). For [ioctl CEC_TRANSMIT](<#rst-cec-transmit>) it will be filled in by the driver with the length of the reply message if `reply` was set.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`timeout`

</td>
<td>


The timeout in milliseconds. This is the time the device will wait for a message to be received before timing out. If it is set to 0, then it will wait indefinitely when it is called by [ioctl CEC_RECEIVE](<#rst-cec-receive>). If it is 0 and it is called by [ioctl CEC_TRANSMIT](<#rst-cec-transmit>), then it will be replaced by 1000 if the `reply` is non-zero or ignored if `reply` is 0.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`sequence`

</td>
<td>


A non-zero sequence number is automatically assigned by the CEC framework for all transmitted messages. It is used by the CEC framework when it queues the transmit result for a non-blocking transmit. This allows the application to associate the received message with the original transmit.

In addition, if a non-blocking transmit will wait for a reply (ii.e. `timeout` was not 0), then the `sequence` field of the reply will be set to the sequence value of the original transmit. This allows the application to associate the received message with the original transmit.

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


Flags. See [cec-msg-flags](<#rst-cec-msg-flags>) for a list of available flags.

</td>
</tr>
<tr>
<td>


\__u8

</td>
<td>


`msg[16]`

</td>
<td>


The message payload. For [ioctl CEC_TRANSMIT](<#rst-cec-transmit>) this is filled in by the application. The driver will fill this in for [ioctl CEC_RECEIVE](<#rst-cec-receive>). For [ioctl CEC_TRANSMIT](<#rst-cec-transmit>) it will be filled in by the driver with the payload of the reply message if `timeout` was set.

</td>
</tr>
<tr>
<td>


\__u8

</td>
<td>


`reply`

</td>
<td>


Wait until this message is replied. If `reply` is 0 and the `timeout` is 0, then don't wait for a reply but return after transmitting the message. Ignored by [ioctl CEC_RECEIVE](<#rst-cec-receive>). The case where `reply` is 0 (this is the opcode for the Feature Abort message) and `timeout` is non-zero is specifically allowed to make it possible to send a message and wait up to `timeout` milliseconds for a Feature Abort reply. In this case `rx_status` will either be set to [CEC_RX_STATUS_TIMEOUT](<#rst-cec-rx-status-timeout>) or [CEC_RX_STATUS_FEATURE_ABORT](<#rst-cec-rx-status-feature-abort>).

If the transmitter message is `CEC_MSG_INITIATE_ARC` then the `reply` values `CEC_MSG_REPORT_ARC_INITIATED` and `CEC_MSG_REPORT_ARC_TERMINATED` are processed differently: either value will match both possible replies. The reason is that the `CEC_MSG_INITIATE_ARC` message is the only CEC message that has two possible replies other than Feature Abort. The `reply` field will be updated with the actual reply so that it is synchronized with the contents of the received message.

</td>
</tr>
<tr>
<td>


\__u8

</td>
<td>


`rx_status`

</td>
<td>


The status bits of the received message. See [cec-rx-status](<#rst-cec-rx-status>) for the possible status values.

</td>
</tr>
<tr>
<td>


\__u8

</td>
<td>


`tx_status`

</td>
<td>


The status bits of the transmitted message. See [cec-tx-status](<#rst-cec-tx-status>) for the possible status values. When calling [ioctl CEC_TRANSMIT](<#rst-cec-transmit>) in non-blocking mode, this field will be 0 if the transmit started, or non-0 if the transmit result is known immediately. The latter would be the case when attempting to transmit a Poll message to yourself. That results in a [CEC_TX_STATUS_NACK](<#rst-cec-tx-status-nack>) without ever actually transmitting the Poll message.

</td>
</tr>
<tr>
<td>


\__u8

</td>
<td>


`tx_arb_lost_cnt`

</td>
<td>


A counter of the number of transmit attempts that resulted in the Arbitration Lost error. This is only set if the hardware supports this, otherwise it is always 0. This counter is only valid if the [CEC_TX_STATUS_ARB_LOST](<#rst-cec-tx-status-arb-lost>) status bit is set.

</td>
</tr>
<tr>
<td>


\__u8

</td>
<td>


`tx_nack_cnt`

</td>
<td>


A counter of the number of transmit attempts that resulted in the Not Acknowledged error. This is only set if the hardware supports this, otherwise it is always 0. This counter is only valid if the [CEC_TX_STATUS_NACK](<#rst-cec-tx-status-nack>) status bit is set.

</td>
</tr>
<tr>
<td>


\__u8

</td>
<td>


`tx_low_drive_cnt`

</td>
<td>


A counter of the number of transmit attempts that resulted in the Arbitration Lost error. This is only set if the hardware supports this, otherwise it is always 0. This counter is only valid if the [CEC_TX_STATUS_LOW_DRIVE](<#rst-cec-tx-status-low-drive>) status bit is set.

</td>
</tr>
<tr>
<td>


\__u8

</td>
<td>


`tx_error_cnt`

</td>
<td>


A counter of the number of transmit errors other than Arbitration Lost or Not Acknowledged. This is only set if the hardware supports this, otherwise it is always 0. This counter is only valid if the [CEC_TX_STATUS_ERROR](<#rst-cec-tx-status-error>) status bit is set.

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{6.2cm}|p{1.0cm}|p{10.1cm}| -->

<a id="rst-cec-msg-flags"></a>


<table>
<caption>Flags for struct cec_msg</caption>
<tbody>
<tr>
<td>


`CEC_MSG_FL_REPLY_TO_FOLLOWERS`

</td>
<td>


1

</td>
<td>


<a id="rst-cec-msg-fl-reply-to-followers"></a>

If a CEC transmit expects a reply, then by default that reply is only sent to the filehandle that called [ioctl CEC_TRANSMIT](<#rst-cec-transmit>). If this flag is set, then the reply is also sent to all followers, if any. If the filehandle that called [ioctl CEC_TRANSMIT](<#rst-cec-transmit>) is also a follower, then that filehandle will receive the reply twice: once as the result of the [ioctl CEC_TRANSMIT](<#rst-cec-transmit>), and once via [ioctl CEC_RECEIVE](<#rst-cec-receive>).

</td>
</tr>
<tr>
<td>


`CEC_MSG_FL_RAW`

</td>
<td>


2

</td>
<td>


<a id="rst-cec-msg-fl-raw"></a>

Normally CEC messages are validated before transmitting them. If this flag is set when [ioctl CEC_TRANSMIT](<#rst-cec-transmit>) is called, then no validation takes place and the message is transmitted as-is. This is useful when debugging CEC issues. This flag is only allowed if the process has the `CAP_SYS_RAWIO` capability. If that is not set, then the `EPERM` error code is returned.

</td>
</tr>
<tr>
<td>


`CEC_MSG_FL_REPLY_VENDOR_ID`

</td>
<td>


4

</td>
<td>


<a id="rst-cec-msg-fl-reply-vendor-id"></a>

This flag is only available if the `CEC_CAP_REPLY_VENDOR_ID` capability is set. If this flag is set, then the reply is expected to consist of the `CEC_MSG_VENDOR_COMMAND_WITH_ID` opcode followed by the Vendor ID (in bytes 1-4 of the message), followed by the `struct cec_msg` `reply` field.

Note that this assumes that the byte after the Vendor ID is a vendor-specific opcode.

This flag makes it easier to wait for replies to vendor commands.

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{5.6cm}|p{0.9cm}|p{10.8cm}| -->

<a id="rst-cec-tx-status"></a>


<table>
<caption>CEC Transmit Status</caption>
<tbody>
<tr>
<td>


`CEC_TX_STATUS_OK`

</td>
<td>


0x01

</td>
<td>


<a id="rst-cec-tx-status-ok"></a>

The message was transmitted successfully. This is mutually exclusive with [CEC_TX_STATUS_MAX_RETRIES](<#rst-cec-tx-status-max-retries>). Other bits can still be set if earlier attempts met with failure before the transmit was eventually successful.

</td>
</tr>
<tr>
<td>


`CEC_TX_STATUS_ARB_LOST`

</td>
<td>


0x02

</td>
<td>


<a id="rst-cec-tx-status-arb-lost"></a>

CEC line arbitration was lost, i.e. another transmit started at the same time with a higher priority. Optional status, not all hardware can detect this error condition.

</td>
</tr>
<tr>
<td>


`CEC_TX_STATUS_NACK`

</td>
<td>


0x04

</td>
<td>


<a id="rst-cec-tx-status-nack"></a>

Message was not acknowledged. Note that some hardware cannot tell apart a 'Not Acknowledged' status from other error conditions, i.e. the result of a transmit is just OK or FAIL. In that case this status will be returned when the transmit failed.

</td>
</tr>
<tr>
<td>


`CEC_TX_STATUS_LOW_DRIVE`

</td>
<td>


0x08

</td>
<td>


<a id="rst-cec-tx-status-low-drive"></a>

Low drive was detected on the CEC bus. This indicates that a follower detected an error on the bus and requests a retransmission. Optional status, not all hardware can detect this error condition.

</td>
</tr>
<tr>
<td>


`CEC_TX_STATUS_ERROR`

</td>
<td>


0x10

</td>
<td>


<a id="rst-cec-tx-status-error"></a>

Some error occurred. This is used for any errors that do not fit `CEC_TX_STATUS_ARB_LOST` or `CEC_TX_STATUS_LOW_DRIVE`, either because the hardware could not tell which error occurred, or because the hardware tested for other conditions besides those two. Optional status.

</td>
</tr>
<tr>
<td>


`CEC_TX_STATUS_MAX_RETRIES`

</td>
<td>


0x20

</td>
<td>


<a id="rst-cec-tx-status-max-retries"></a>

The transmit failed after one or more retries. This status bit is mutually exclusive with [CEC_TX_STATUS_OK](<#rst-cec-tx-status-ok>). Other bits can still be set to explain which failures were seen.

</td>
</tr>
<tr>
<td>


`CEC_TX_STATUS_ABORTED`

</td>
<td>


0x40

</td>
<td>


<a id="rst-cec-tx-status-aborted"></a>

The transmit was aborted due to an HDMI disconnect, or the adapter was unconfigured, or a transmit was interrupted, or the driver returned an error when attempting to start a transmit.

</td>
</tr>
<tr>
<td>


`CEC_TX_STATUS_TIMEOUT`

</td>
<td>


0x80

</td>
<td>


<a id="rst-cec-tx-status-timeout"></a>

The transmit timed out. This should not normally happen and this indicates a driver problem.

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{5.6cm}|p{0.9cm}|p{10.8cm}| -->

<a id="rst-cec-rx-status"></a>


<table>
<caption>CEC Receive Status</caption>
<tbody>
<tr>
<td>


`CEC_RX_STATUS_OK`

</td>
<td>


0x01

</td>
<td>


<a id="rst-cec-rx-status-ok"></a>

The message was received successfully.

</td>
</tr>
<tr>
<td>


`CEC_RX_STATUS_TIMEOUT`

</td>
<td>


0x02

</td>
<td>


<a id="rst-cec-rx-status-timeout"></a>

The reply to an earlier transmitted message timed out.

</td>
</tr>
<tr>
<td>


`CEC_RX_STATUS_FEATURE_ABORT`

</td>
<td>


0x04

</td>
<td>


<a id="rst-cec-rx-status-feature-abort"></a>

The message was received successfully but the reply was `CEC_MSG_FEATURE_ABORT`. This status is only set if this message was the reply to an earlier transmitted message.

</td>
</tr>
<tr>
<td>


`CEC_RX_STATUS_ABORTED`

</td>
<td>


0x08

</td>
<td>


<a id="rst-cec-rx-status-aborted"></a>

The wait for a reply to an earlier transmitted message was aborted because the HDMI cable was disconnected, the adapter was unconfigured or the [CEC_TRANSMIT](<#rst-cec-receive>) that waited for a reply was interrupted.

</td>
</tr>
</tbody>
</table>

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

The [ioctl CEC_RECEIVE](<#rst-cec-receive>) can return the following error codes:

- **EAGAIN**

  No messages are in the receive queue, and the filehandle is in non-blocking mode.

- **ETIMEDOUT**

  The `timeout` was reached while waiting for a message.

- **ERESTARTSYS**

  The wait for a message was interrupted (e.g. by Ctrl-C).

The [ioctl CEC_TRANSMIT](<#rst-cec-transmit>) can return the following error codes:

- **ENOTTY**

  The `CEC_CAP_TRANSMIT` capability wasn't set, so this ioctl is not supported.

- **EPERM**

  The CEC adapter is not configured, i.e. [ioctl CEC_ADAP_S_LOG_ADDRS](<~kernel/userspace/userspace-api/media-cec/cec-ioc-adap-g-log-addrs#rst-cec-adap-s-log-addrs>) has never been called, or `CEC_MSG_FL_RAW` was used from a process that did not have the `CAP_SYS_RAWIO` capability.

- **ENONET**

  The CEC adapter is not configured, i.e. [ioctl CEC_ADAP_S_LOG_ADDRS](<~kernel/userspace/userspace-api/media-cec/cec-ioc-adap-g-log-addrs#rst-cec-adap-s-log-addrs>) was called, but the physical address is invalid so no logical address was claimed. An exception is made in this case for transmits from initiator 0xf ('Unregistered') to destination 0 ('TV'). In that case the transmit will proceed as usual.

- **EBUSY**

  Another filehandle is in exclusive follower or initiator mode, or the filehandle is in mode `CEC_MODE_NO_INITIATOR`. This is also returned if the transmit queue is full.

- **EINVAL**

  The contents of struct `cec_msg` is invalid.

- **ERESTARTSYS**

  The wait for a successful transmit was interrupted (e.g. by Ctrl-C).
