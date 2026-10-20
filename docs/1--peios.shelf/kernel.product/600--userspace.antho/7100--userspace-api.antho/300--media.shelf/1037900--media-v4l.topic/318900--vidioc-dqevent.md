---
title: "ioctl VIDIOC_DQEVENT"
type: reference
description: "VIDIOC_DQEVENT - Dequeue event"
---

<a id="rst-ioctl-vidioc-dqevent"></a>
<a id="rst-vidioc-dqevent"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

VIDIOC_DQEVENT - Dequeue event

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-VIDIOC_DQEVENT"></a>

```c
VIDIOC_DQEVENT
```

`int ioctl(int fd, VIDIOC_DQEVENT, struct v4l2_event *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to struct `v4l2_event`.

<a id="rst-description"></a>

## Description

Dequeue an event from a video device. No input is required for this ioctl. All the fields of the struct `v4l2_event` structure are filled by the driver. The file handle will also receive exceptions which the application may get by e.g. using the select system call.





<a id="c-v4l2_event"></a>

```c
v4l2_event
```

<!-- tabularcolumns: |p{3.0cm}|p{3.4cm}|p{10.9cm}| -->


<table>
<caption>struct v4l2_event</caption>
<tbody>
<tr>
<td>


\__u32

</td>
<td>


`type`

</td>
<td>


Type of the event, see [event-type](<#rst-event-type>).

</td>
</tr>
<tr>
<td>


union \{

</td>
<td colspan="2">


`u`

</td>
</tr>
<tr>
<td>


struct `v4l2_event_vsync`

</td>
<td>


`vsync`

</td>
<td>


Event data for event `V4L2_EVENT_VSYNC`.

</td>
</tr>
<tr>
<td>


struct `v4l2_event_ctrl`

</td>
<td>


`ctrl`

</td>
<td>


Event data for event `V4L2_EVENT_CTRL`.

</td>
</tr>
<tr>
<td>


struct `v4l2_event_frame_sync`

</td>
<td>


`frame_sync`

</td>
<td>


Event data for event `V4L2_EVENT_FRAME_SYNC`.

</td>
</tr>
<tr>
<td>


struct `v4l2_event_motion_det`

</td>
<td>


`motion_det`

</td>
<td>


Event data for event V4L2_EVENT_MOTION_DET.

</td>
</tr>
<tr>
<td>


struct `v4l2_event_src_change`

</td>
<td>


`src_change`

</td>
<td>


Event data for event V4L2_EVENT_SOURCE_CHANGE.

</td>
</tr>
<tr>
<td>


\__u8

</td>
<td>


`data`\[64\]

</td>
<td>


Event data. Defined by the event type. The union should be used to define easily accessible type for events.

</td>
</tr>
<tr>
<td>


\}

</td>
<td colspan="2">




</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`pending`

</td>
<td>


Number of pending events excluding this one.

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


Event sequence number. The sequence number is incremented for every subscribed event that takes place. If sequence numbers are not contiguous it means that events have been lost.

</td>
</tr>
<tr>
<td>


struct timespec

</td>
<td>


`timestamp`

</td>
<td>


Event timestamp. The timestamp has been taken from the `CLOCK_MONOTONIC` clock. To access the same clock outside V4L2, use `clock_gettime()`.

</td>
</tr>
<tr>
<td>


u32

</td>
<td>


`id`

</td>
<td>


The ID associated with the event source. If the event does not have an associated ID (this depends on the event type), then this is 0.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`reserved`\[8\]

</td>
<td>


Reserved for future extensions. Drivers must set the array to zero.

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{6.2cm}|p{2.6cm}|p{8.5cm}| -->

<a id="rst-event-type"></a>


<table>
<caption>Event Types</caption>
<tbody>
<tr>
<td>


`V4L2_EVENT_ALL`

</td>
<td>


0

</td>
<td>


All events. V4L2_EVENT_ALL is valid only for VIDIOC_UNSUBSCRIBE_EVENT for unsubscribing all events at once.

</td>
</tr>
<tr>
<td>


`V4L2_EVENT_VSYNC`

</td>
<td>


1

</td>
<td>


This event is triggered on the vertical sync. This event has a struct `v4l2_event_vsync` associated with it.

</td>
</tr>
<tr>
<td>


`V4L2_EVENT_EOS`

</td>
<td>


2

</td>
<td>


This event is triggered when the end of a stream is reached. This is typically used with MPEG decoders to report to the application when the last of the MPEG stream has been decoded.

</td>
</tr>
<tr>
<td>


`V4L2_EVENT_CTRL`

</td>
<td>


3

</td>
<td>


This event requires that the `id` matches the control ID from which you want to receive events. This event is triggered if the control's value changes, if a button control is pressed or if the control's flags change. This event has a struct `v4l2_event_ctrl` associated with it. This struct contains much of the same information as struct [v4l2_queryctrl](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/vidioc-queryctrl.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>) and struct `v4l2_control`.

If the event is generated due to a call to [VIDIOC_S_CTRL](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-ctrl#rst-vidioc-g-ctrl>) or [VIDIOC_S_EXT_CTRLS](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/vidioc-g-ext-ctrls.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>), then the event will *not* be sent to the file handle that called the ioctl function. This prevents nasty feedback loops. If you *do* want to get the event, then set the `V4L2_EVENT_SUB_FL_ALLOW_FEEDBACK` flag.

This event type will ensure that no information is lost when more events are raised than there is room internally. In that case the struct `v4l2_event_ctrl` of the second-oldest event is kept, but the `changes` field of the second-oldest event is ORed with the `changes` field of the oldest event.

</td>
</tr>
<tr>
<td>


`V4L2_EVENT_FRAME_SYNC`

</td>
<td>


4

</td>
<td>


Triggered immediately when the reception of a frame has begun. This event has a struct `v4l2_event_frame_sync` associated with it.

If the hardware needs to be stopped in the case of a buffer underrun it might not be able to generate this event. In such cases the `frame_sequence` field in struct `v4l2_event_frame_sync` will not be incremented. This causes two consecutive frame sequence numbers to have n times frame interval in between them.

</td>
</tr>
<tr>
<td>


`V4L2_EVENT_SOURCE_CHANGE`

</td>
<td>


5

</td>
<td>


This event is triggered when a source parameter change is detected during runtime by the video device. It can be a runtime resolution change triggered by a video decoder or the format change happening on an input connector. This event requires that the `id` matches the input index (when used with a video device node) or the pad index (when used with a subdevice node) from which you want to receive events.

This event has a struct `v4l2_event_src_change` associated with it. The `changes` bitfield denotes what has changed for the subscribed pad. If multiple events occurred before application could dequeue them, then the changes will have the ORed value of all the events generated.

</td>
</tr>
<tr>
<td>


`V4L2_EVENT_MOTION_DET`

</td>
<td>


6

</td>
<td>


Triggered whenever the motion detection state for one or more of the regions changes. This event has a struct `v4l2_event_motion_det` associated with it.

</td>
</tr>
<tr>
<td>


`V4L2_EVENT_PRIVATE_START`

</td>
<td>


0x08000000

</td>
<td>


Base event number for driver-private events.

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{4.4cm}|p{4.4cm}|p{8.5cm}| -->





<a id="c-v4l2_event_vsync"></a>

```c
v4l2_event_vsync
```


<table>
<caption>struct v4l2_event_vsync</caption>
<tbody>
<tr>
<td>


\__u8

</td>
<td>


`field`

</td>
<td>


The upcoming field. See enum `v4l2_field`.

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{3.5cm}|p{3.0cm}|p{10.8cm}| -->





<a id="c-v4l2_event_ctrl"></a>

```c
v4l2_event_ctrl
```


<table>
<caption>struct v4l2_event_ctrl</caption>
<tbody>
<tr>
<td>


\__u32

</td>
<td>


`changes`

</td>
<td>


A bitmask that tells what has changed. See [ctrl-changes-flags](<#rst-ctrl-changes-flags>).

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`type`

</td>
<td>


The type of the control. See enum `v4l2_ctrl_type`.

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


\__s32

</td>
<td>


`value`

</td>
<td>


The 32-bit value of the control for 32-bit control types. This is 0 for string controls since the value of a string cannot be passed using [ioctl VIDIOC_DQEVENT](<#rst-vidioc-dqevent>).

</td>
</tr>
<tr>
<td>


\__s64

</td>
<td>


`value64`

</td>
<td>


The 64-bit value of the control for 64-bit control types.

</td>
</tr>
<tr>
<td>


\}

</td>
<td colspan="2">




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


The control flags. See [control-flags](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/vidioc-queryctrl.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>).

</td>
</tr>
<tr>
<td>


\__s32

</td>
<td>


`minimum`

</td>
<td>


The minimum value of the control. See struct [v4l2_queryctrl](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/vidioc-queryctrl.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>).

</td>
</tr>
<tr>
<td>


\__s32

</td>
<td>


`maximum`

</td>
<td>


The maximum value of the control. See struct [v4l2_queryctrl](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/vidioc-queryctrl.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>).

</td>
</tr>
<tr>
<td>


\__s32

</td>
<td>


`step`

</td>
<td>


The step value of the control. See struct [v4l2_queryctrl](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/vidioc-queryctrl.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>).

</td>
</tr>
<tr>
<td>


\__s32

</td>
<td>


`default_value`

</td>
<td>


The default value of the control. See struct [v4l2_queryctrl](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/vidioc-queryctrl.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>).

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{4.4cm}|p{4.4cm}|p{8.5cm}| -->





<a id="c-v4l2_event_frame_sync"></a>

```c
v4l2_event_frame_sync
```


<table>
<caption>struct v4l2_event_frame_sync</caption>
<tbody>
<tr>
<td>


\__u32

</td>
<td>


`frame_sequence`

</td>
<td>


The sequence number of the frame being received.

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{4.4cm}|p{4.4cm}|p{8.5cm}| -->





<a id="c-v4l2_event_src_change"></a>

```c
v4l2_event_src_change
```


<table>
<caption>struct v4l2_event_src_change</caption>
<tbody>
<tr>
<td>


\__u32

</td>
<td>


`changes`

</td>
<td>


A bitmask that tells what has changed. See [src-changes-flags](<#rst-src-changes-flags>).

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{4.4cm}|p{4.4cm}|p{8.5cm}| -->





<a id="c-v4l2_event_motion_det"></a>

```c
v4l2_event_motion_det
```


<table>
<caption>struct v4l2_event_motion_det</caption>
<tbody>
<tr>
<td>


\__u32

</td>
<td>


`flags`

</td>
<td>


Currently only one flag is available: if `V4L2_EVENT_MD_FL_HAVE_FRAME_SEQ` is set, then the `frame_sequence` field is valid, otherwise that field should be ignored.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`frame_sequence`

</td>
<td>


The sequence number of the frame being received. Only valid if the `V4L2_EVENT_MD_FL_HAVE_FRAME_SEQ` flag was set.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`region_mask`

</td>
<td>


The bitmask of the regions that reported motion. There is at least one region. If this field is 0, then no motion was detected at all. If there is no `V4L2_CID_DETECT_MD_REGION_GRID` control (see [Detect Control Reference](<~kernel/userspace/userspace-api/media-v4l/ext-ctrls-detect#rst-detect-controls>)) to assign a different region to each cell in the motion detection grid, then that all cells are automatically assigned to the default region 0.

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{6.6cm}|p{2.2cm}|p{8.5cm}| -->

<a id="rst-ctrl-changes-flags"></a>


<table>
<caption>Control Changes</caption>
<tbody>
<tr>
<td>


`V4L2_EVENT_CTRL_CH_VALUE`

</td>
<td>


0x0001

</td>
<td>


This control event was triggered because the value of the control changed. Special cases: Volatile controls do no generate this event; If a control has the `V4L2_CTRL_FLAG_EXECUTE_ON_WRITE` flag set, then this event is sent as well, regardless its value.

</td>
</tr>
<tr>
<td>


`V4L2_EVENT_CTRL_CH_FLAGS`

</td>
<td>


0x0002

</td>
<td>


This control event was triggered because the control flags changed.

</td>
</tr>
<tr>
<td>


`V4L2_EVENT_CTRL_CH_RANGE`

</td>
<td>


0x0004

</td>
<td>


This control event was triggered because the minimum, maximum, step or the default value of the control changed.

</td>
</tr>
<tr>
<td>


`V4L2_EVENT_CTRL_CH_DIMENSIONS`

</td>
<td>


0x0008

</td>
<td>


This control event was triggered because the dimensions of the control changed. Note that the number of dimensions remains the same.

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{6.6cm}|p{2.2cm}|p{8.5cm}| -->

<a id="rst-src-changes-flags"></a>


<table>
<caption>Source Changes</caption>
<tbody>
<tr>
<td>


`V4L2_EVENT_SRC_CH_RESOLUTION`

</td>
<td>


0x0001

</td>
<td>


This event gets triggered when a resolution change is detected at an input. This can come from an input connector or from a video decoder. Applications will have to query the new resolution (if any, the signal may also have been lost).

For stateful decoders follow the guidelines in [Memory-to-Memory Stateful Video Decoder Interface](<~kernel/userspace/userspace-api/media-v4l/dev-decoder#rst-decoder>). Video Capture devices have to query the new timings using [ioctl VIDIOC_QUERY_DV_TIMINGS](<~kernel/userspace/userspace-api/media-v4l/vidioc-query-dv-timings#rst-vidioc-query-dv-timings>) or [VIDIOC_QUERYSTD](<~kernel/userspace/userspace-api/media-v4l/vidioc-querystd#rst-vidioc-querystd>).

*Important*: even if the new video timings appear identical to the old ones, receiving this event indicates that there was an issue with the video signal and you must stop and restart streaming ([VIDIOC_STREAMOFF](<~kernel/userspace/userspace-api/media-v4l/vidioc-streamon#rst-vidioc-streamon>) followed by [VIDIOC_STREAMON](<~kernel/userspace/userspace-api/media-v4l/vidioc-streamon#rst-vidioc-streamon>)). The reason is that many Video Capture devices are not able to recover from a temporary loss of signal and so restarting streaming I/O is required in order for the hardware to synchronize to the video signal.

</td>
</tr>
</tbody>
</table>

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
