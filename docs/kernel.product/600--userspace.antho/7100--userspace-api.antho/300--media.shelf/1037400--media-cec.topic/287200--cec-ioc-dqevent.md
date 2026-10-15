---
title: "ioctl CEC_DQEVENT"
type: reference
description: "CEC_DQEVENT - Dequeue a CEC event"
---

<a id="rst-ioctl-cec-dqevent"></a>
<a id="rst-cec-dqevent"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: CEC -->

<a id="rst-name"></a>

## Name

CEC_DQEVENT - Dequeue a CEC event

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-CEC_DQEVENT"></a>

```c
CEC_DQEVENT
```

`int ioctl(int fd, CEC_DQEVENT, struct cec_event *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

`argp`

<a id="rst-description"></a>

## Description

CEC devices can send asynchronous events. These can be retrieved by calling `CEC_DQEVENT()`. If the file descriptor is in non-blocking mode and no event is pending, then it will return -1 and set errno to the `EAGAIN` error code.

The internal event queues are per-filehandle and per-event type. If there is no more room in a queue then the last event is overwritten with the new one. This means that intermediate results can be thrown away but that the latest event is always available. This also means that is it possible to read two successive events that have the same value (e.g. two [CEC_EVENT_STATE_CHANGE](<#rst-cec-event-state-change>) events with the same state). In that case the intermediate state changes were lost but it is guaranteed that the state did change in between the two events.

<!-- tabularcolumns: |p{1.2cm}|p{2.9cm}|p{13.2cm}| -->





<a id="c-cec_event_state_change"></a>

```c
cec_event_state_change
```


<table>
<caption>struct cec_event_state_change</caption>
<tbody>
<tr>
<td>


\__u16

</td>
<td>


`phys_addr`

</td>
<td>


The current physical address. This is `CEC_PHYS_ADDR_INVALID` if no valid physical address is set.

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


The current set of claimed logical addresses. This is 0 if no logical addresses are claimed or if `phys_addr` is `CEC_PHYS_ADDR_INVALID`. If bit 15 is set (`1 << CEC_LOG_ADDR_UNREGISTERED`) then this device has the unregistered logical address. In that case all other bits are 0.

</td>
</tr>
<tr>
<td>


\__u16

</td>
<td>


`have_conn_info`

</td>
<td>


If non-zero, then HDMI connector information is available. This field is only valid if `CEC_CAP_CONNECTOR_INFO` is set. If that capability is set and `have_conn_info` is zero, then that indicates that the HDMI connector device is not instantiated, either because the HDMI driver is still configuring the device or because the HDMI device was unbound.

</td>
</tr>
</tbody>
</table>





<a id="c-cec_event_lost_msgs"></a>

```c
cec_event_lost_msgs
```

<!-- tabularcolumns: |p{1.0cm}|p{2.0cm}|p{14.3cm}| -->


<table>
<caption>struct cec_event_lost_msgs</caption>
<tbody>
<tr>
<td>


\__u32

</td>
<td>


`lost_msgs`

</td>
<td>


Set to the number of lost messages since the filehandle was opened or since the last time this event was dequeued for this filehandle. The messages lost are the oldest messages. So when a new message arrives and there is no more room, then the oldest message is discarded to make room for the new one. The internal size of the message queue guarantees that all messages received in the last two seconds will be stored. Since messages should be replied to within a second according to the CEC specification, this is more than enough.

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{1.0cm}|p{4.4cm}|p{2.5cm}|p{9.2cm}| -->





<a id="c-cec_event"></a>

```c
cec_event
```


<table>
<caption>struct cec_event</caption>
<tbody>
<tr>
<td>


\__u64

</td>
<td>


`ts`

</td>
<td>


Timestamp of the event in ns.

The timestamp has been taken from the `CLOCK_MONOTONIC` clock.

To access the same clock from userspace use `clock_gettime()`.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`event`

</td>
<td>


The CEC event type, see [cec-events](<#rst-cec-events>).

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


Event flags, see [cec-event-flags](<#rst-cec-event-flags>).

</td>
</tr>
<tr>
<td>


union \{

</td>
<td colspan="2">


(anonymous)

</td>
</tr>
<tr>
<td>


struct cec_event_state_change

</td>
<td>


`state_change`

</td>
<td>


The new adapter state as sent by the [CEC_EVENT_STATE_CHANGE](<#rst-cec-event-state-change>) event.

</td>
</tr>
<tr>
<td>


struct cec_event_lost_msgs

</td>
<td>


`lost_msgs`

</td>
<td>


The number of lost messages as sent by the [CEC_EVENT_LOST_MSGS](<#rst-cec-event-lost-msgs>) event.

</td>
</tr>
<tr>
<td>


\}

</td>
<td colspan="2">




</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{5.6cm}|p{0.9cm}|p{10.8cm}| -->

<a id="rst-cec-events"></a>


<table>
<caption>CEC Events Types</caption>
<tbody>
<tr>
<td>


`CEC_EVENT_STATE_CHANGE`

</td>
<td>


1

</td>
<td>


<a id="rst-cec-event-state-change"></a>

Generated when the CEC Adapter's state changes. When open() is called an initial event will be generated for that filehandle with the CEC Adapter's state at that time.

</td>
</tr>
<tr>
<td>


`CEC_EVENT_LOST_MSGS`

</td>
<td>


2

</td>
<td>


<a id="rst-cec-event-lost-msgs"></a>

Generated if one or more CEC messages were lost because the application didn't dequeue CEC messages fast enough.

</td>
</tr>
<tr>
<td>


`CEC_EVENT_PIN_CEC_LOW`

</td>
<td>


3

</td>
<td>


<a id="rst-cec-event-pin-cec-low"></a>

Generated if the CEC pin goes from a high voltage to a low voltage. Only applies to adapters that have the `CEC_CAP_MONITOR_PIN` capability set.

</td>
</tr>
<tr>
<td>


`CEC_EVENT_PIN_CEC_HIGH`

</td>
<td>


4

</td>
<td>


<a id="rst-cec-event-pin-cec-high"></a>

Generated if the CEC pin goes from a low voltage to a high voltage. Only applies to adapters that have the `CEC_CAP_MONITOR_PIN` capability set.

</td>
</tr>
<tr>
<td>


`CEC_EVENT_PIN_HPD_LOW`

</td>
<td>


5

</td>
<td>


<a id="rst-cec-event-pin-hpd-low"></a>

Generated if the HPD pin goes from a high voltage to a low voltage. Only applies to adapters that have the `CEC_CAP_MONITOR_PIN` capability set. When open() is called, the HPD pin can be read and if the HPD is low, then an initial event will be generated for that filehandle.

</td>
</tr>
<tr>
<td>


`CEC_EVENT_PIN_HPD_HIGH`

</td>
<td>


6

</td>
<td>


<a id="rst-cec-event-pin-hpd-high"></a>

Generated if the HPD pin goes from a low voltage to a high voltage. Only applies to adapters that have the `CEC_CAP_MONITOR_PIN` capability set. When open() is called, the HPD pin can be read and if the HPD is high, then an initial event will be generated for that filehandle.

</td>
</tr>
<tr>
<td>


`CEC_EVENT_PIN_5V_LOW`

</td>
<td>


6

</td>
<td>


<a id="rst-cec-event-pin-5v-low"></a>

Generated if the 5V pin goes from a high voltage to a low voltage. Only applies to adapters that have the `CEC_CAP_MONITOR_PIN` capability set. When open() is called, the 5V pin can be read and if the 5V is low, then an initial event will be generated for that filehandle.

</td>
</tr>
<tr>
<td>


`CEC_EVENT_PIN_5V_HIGH`

</td>
<td>


7

</td>
<td>


<a id="rst-cec-event-pin-5v-high"></a>

Generated if the 5V pin goes from a low voltage to a high voltage. Only applies to adapters that have the `CEC_CAP_MONITOR_PIN` capability set. When open() is called, the 5V pin can be read and if the 5V is high, then an initial event will be generated for that filehandle.

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{6.0cm}|p{0.6cm}|p{10.7cm}| -->

<a id="rst-cec-event-flags"></a>


<table>
<caption>CEC Event Flags</caption>
<tbody>
<tr>
<td>


`CEC_EVENT_FL_INITIAL_STATE`

</td>
<td>


1

</td>
<td>


<a id="rst-cec-event-fl-initial-state"></a>

Set for the initial events that are generated when the device is opened. See the table above for which events do this. This allows applications to learn the initial state of the CEC adapter at open() time.

</td>
</tr>
<tr>
<td>


`CEC_EVENT_FL_DROPPED_EVENTS`

</td>
<td>


2

</td>
<td>


<a id="rst-cec-event-fl-dropped-events"></a>

Set if one or more events of the given event type have been dropped. This is an indication that the application cannot keep up.

</td>
</tr>
</tbody>
</table>

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

The [ioctl CEC_DQEVENT](<#rst-cec-dqevent>) can return the following error codes:

- **EAGAIN**

  This is returned when the filehandle is in non-blocking mode and there are no pending events.

- **ERESTARTSYS**

  An interrupt (e.g. Ctrl-C) arrived while in blocking mode waiting for events to arrive.
