---
title: "ioctl VIDIOC_G_PRIORITY, VIDIOC_S_PRIORITY"
type: reference
description: "VIDIOC_G_PRIORITY - VIDIOC_S_PRIORITY - Query or request the access priority associated with a file descriptor"
---

<a id="rst-ioctl-vidioc-g-priority-vidioc-s-priority"></a>
<a id="rst-vidioc-g-priority"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

VIDIOC_G_PRIORITY - VIDIOC_S_PRIORITY - Query or request the access priority associated with a file descriptor

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-VIDIOC_G_PRIORITY"></a>

```c
VIDIOC_G_PRIORITY
```

`int ioctl(int fd, VIDIOC_G_PRIORITY, enum v4l2_priority *argp)`





<a id="c-VIDIOC_S_PRIORITY"></a>

```c
VIDIOC_S_PRIORITY
```

`int ioctl(int fd, VIDIOC_S_PRIORITY, const enum v4l2_priority *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to an enum `v4l2_priority` type.

<a id="rst-description"></a>

## Description

To query the current access priority applications call the [VIDIOC_G_PRIORITY](<#rst-vidioc-g-priority>) ioctl with a pointer to an enum v4l2_priority variable where the driver stores the current priority.

To request an access priority applications store the desired priority in an enum v4l2_priority variable and call [VIDIOC_S_PRIORITY](<#rst-vidioc-g-priority>) ioctl with a pointer to this variable.





<a id="c-v4l2_priority"></a>

```c
v4l2_priority
```

<!-- tabularcolumns: |p{6.6cm}|p{2.2cm}|p{8.5cm}| -->


<table>
<caption>enum v4l2_priority</caption>
<tbody>
<tr>
<td>


`V4L2_PRIORITY_UNSET`

</td>
<td>


0

</td>
<td>




</td>
</tr>
<tr>
<td>


`V4L2_PRIORITY_BACKGROUND`

</td>
<td>


1

</td>
<td>


Lowest priority, usually applications running in background, for example monitoring VBI transmissions. A proxy application running in user space will be necessary if multiple applications want to read from a device at this priority.

</td>
</tr>
<tr>
<td>


`V4L2_PRIORITY_INTERACTIVE`

</td>
<td>


2

</td>
<td>




</td>
</tr>
<tr>
<td>


`V4L2_PRIORITY_DEFAULT`

</td>
<td>


2

</td>
<td>


Medium priority, usually applications started and interactively controlled by the user. For example TV viewers, Teletext browsers, or just "panel" applications to change the channel or video controls. This is the default priority unless an application requests another.

</td>
</tr>
<tr>
<td>


`V4L2_PRIORITY_RECORD`

</td>
<td>


3

</td>
<td>


Highest priority. Only one file descriptor can have this priority, it blocks any other fd from changing device properties. Usually applications which must not be interrupted, like video recording.

</td>
</tr>
</tbody>
</table>

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

- **EINVAL**

  The requested priority value is invalid.

- **EBUSY**

  Another application already requested higher priority.
