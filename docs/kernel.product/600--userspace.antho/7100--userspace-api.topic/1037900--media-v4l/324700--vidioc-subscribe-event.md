---
title: "ioctl VIDIOC_SUBSCRIBE_EVENT, VIDIOC_UNSUBSCRIBE_EVENT"
type: reference
description: "VIDIOC_SUBSCRIBE_EVENT - VIDIOC_UNSUBSCRIBE_EVENT - Subscribe or unsubscribe event"
---

<a id="rst-ioctl-vidioc-subscribe-event-vidioc-unsubscribe-event"></a>
<a id="rst-vidioc-unsubscribe-event"></a>
<a id="rst-vidioc-subscribe-event"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

VIDIOC_SUBSCRIBE_EVENT - VIDIOC_UNSUBSCRIBE_EVENT - Subscribe or unsubscribe event

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-VIDIOC_SUBSCRIBE_EVENT"></a>

```c
VIDIOC_SUBSCRIBE_EVENT
```

`int ioctl(int fd, VIDIOC_SUBSCRIBE_EVENT, struct v4l2_event_subscription *argp)`





<a id="c-VIDIOC_UNSUBSCRIBE_EVENT"></a>

```c
VIDIOC_UNSUBSCRIBE_EVENT
```

`int ioctl(int fd, VIDIOC_UNSUBSCRIBE_EVENT, struct v4l2_event_subscription *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to struct `v4l2_event_subscription`.

<a id="rst-description"></a>

## Description

Subscribe or unsubscribe V4L2 event. Subscribed events are dequeued by using the [ioctl VIDIOC_DQEVENT](<~kernel/userspace/userspace-api/media-v4l/vidioc-dqevent#rst-vidioc-dqevent>) ioctl.

<!-- tabularcolumns: |p{2.6cm}|p{4.4cm}|p{10.3cm}| -->





<a id="c-v4l2_event_subscription"></a>

```c
v4l2_event_subscription
```


<table>
<caption>struct v4l2_event_subscription</caption>
<tbody>
<tr>
<td>


\__u32

</td>
<td>


`type`

</td>
<td>


Type of the event, see [event-type](<~kernel/userspace/userspace-api/media-v4l/vidioc-dqevent#rst-event-type>).

> [!NOTE]
>
> `V4L2_EVENT_ALL` can be used with [VIDIOC_UNSUBSCRIBE_EVENT](<#rst-vidioc-subscribe-event>) for unsubscribing all events at once.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`id`

</td>
<td>


ID of the event source. If there is no ID associated with the event source, then set this to 0. Whether or not an event needs an ID depends on the event type.

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


Event flags, see [event-flags](<#rst-event-flags>).

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`reserved`\[5\]

</td>
<td>


Reserved for future extensions. Drivers and applications must set the array to zero.

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{7.5cm}|p{2.0cm}|p{7.8cm}| -->

<a id="rst-event-flags"></a>


<table>
<caption>Event Flags</caption>
<tbody>
<tr>
<td>


`V4L2_EVENT_SUB_FL_SEND_INITIAL`

</td>
<td>


0x0001

</td>
<td>


When this event is subscribed an initial event will be sent containing the current status. This only makes sense for events that are triggered by a status change such as `V4L2_EVENT_CTRL`. Other events will ignore this flag.

</td>
</tr>
<tr>
<td>


`V4L2_EVENT_SUB_FL_ALLOW_FEEDBACK`

</td>
<td>


0x0002

</td>
<td>


If set, then events directly caused by an ioctl will also be sent to the filehandle that called that ioctl. For example, changing a control using [VIDIOC_S_CTRL](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-ctrl#rst-vidioc-g-ctrl>) will cause a V4L2_EVENT_CTRL to be sent back to that same filehandle. Normally such events are suppressed to prevent feedback loops where an application changes a control to a one value and then another, and then receives an event telling it that that control has changed to the first value.

Since it can't tell whether that event was caused by another application or by the [VIDIOC_S_CTRL](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-ctrl#rst-vidioc-g-ctrl>) call it is hard to decide whether to set the control to the value in the event, or ignore it.

Think carefully when you set this flag so you won't get into situations like that.

</td>
</tr>
</tbody>
</table>

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
