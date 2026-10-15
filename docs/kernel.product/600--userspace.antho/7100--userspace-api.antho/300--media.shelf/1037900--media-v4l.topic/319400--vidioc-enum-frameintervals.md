---
title: "ioctl VIDIOC_ENUM_FRAMEINTERVALS"
type: reference
description: "VIDIOC_ENUM_FRAMEINTERVALS - Enumerate frame intervals"
---

<a id="rst-ioctl-vidioc-enum-frameintervals"></a>
<a id="rst-vidioc-enum-frameintervals"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

VIDIOC_ENUM_FRAMEINTERVALS - Enumerate frame intervals

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-VIDIOC_ENUM_FRAMEINTERVALS"></a>

```c
VIDIOC_ENUM_FRAMEINTERVALS
```

`int ioctl(int fd, VIDIOC_ENUM_FRAMEINTERVALS, struct v4l2_frmivalenum *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to struct `v4l2_frmivalenum` that contains a pixel format and size and receives a frame interval.

<a id="rst-description"></a>

## Description

This ioctl allows applications to enumerate all frame intervals that the device supports for the given pixel format and frame size.

The supported pixel formats and frame sizes can be obtained by using the [ioctl VIDIOC_ENUM_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-enum-fmt#rst-vidioc-enum-fmt>) and [ioctl VIDIOC_ENUM_FRAMESIZES](<~kernel/userspace/userspace-api/media-v4l/vidioc-enum-framesizes#rst-vidioc-enum-framesizes>) functions.

The return value and the content of the `v4l2_frmivalenum.type` field depend on the type of frame intervals the device supports. Here are the semantics of the function for the different cases:

- **Discrete:** The function returns success if the given index value (zero-based) is valid. The application should increase the index by one for each call until `EINVAL` is returned. The `v4l2_frmivalenum.type` field is set to `V4L2_FRMIVAL_TYPE_DISCRETE` by the driver. Of the union only the `discrete` member is valid.

- **Step-wise:** The function returns success if the given index value is zero and `EINVAL` for any other index value. The `v4l2_frmivalenum.type` field is set to `V4L2_FRMIVAL_TYPE_STEPWISE` by the driver. Of the union only the `stepwise` member is valid.

- **Continuous:** This is a special case of the step-wise type above. The function returns success if the given index value is zero and `EINVAL` for any other index value. The `v4l2_frmivalenum.type` field is set to `V4L2_FRMIVAL_TYPE_CONTINUOUS` by the driver. Of the union only the `stepwise` member is valid and the `step` value is set to 1.

When the application calls the function with index zero, it must check the `type` field to determine the type of frame interval enumeration the device supports. Only for the `V4L2_FRMIVAL_TYPE_DISCRETE` type does it make sense to increase the index value to receive more frame intervals.

> [!NOTE]
>
> The order in which the frame intervals are returned has no special meaning. In particular does it not say anything about potential default frame intervals.

Applications can assume that the enumeration data does not change without any interaction from the application itself. This means that the enumeration data is consistent if the application does not perform any other ioctl calls while it runs the frame interval enumeration.

> [!NOTE]
>
> **Frame intervals and frame rates:** The V4L2 API uses frame intervals instead of frame rates. Given the frame interval the frame rate can be computed as follows:
>
>
>
> ```text
> frame_rate = 1 / frame_interval
> ```

<a id="rst-structs"></a>

## Structs

In the structs below, *IN* denotes a value that has to be filled in by the application, *OUT* denotes values that the driver fills in. The application should zero out all members except for the *IN* fields.





<a id="c-v4l2_frmival_stepwise"></a>

```c
v4l2_frmival_stepwise
```


<table>
<caption>struct v4l2_frmival_stepwise</caption>
<tbody>
<tr>
<td>


struct `v4l2_fract`

</td>
<td>


`min`

</td>
<td>


Minimum frame interval \[s\].

</td>
</tr>
<tr>
<td>


struct `v4l2_fract`

</td>
<td>


`max`

</td>
<td>


Maximum frame interval \[s\].

</td>
</tr>
<tr>
<td>


struct `v4l2_fract`

</td>
<td>


`step`

</td>
<td>


Frame interval step size \[s\].

</td>
</tr>
</tbody>
</table>





<a id="c-v4l2_frmivalenum"></a>

```c
v4l2_frmivalenum
```

<!-- tabularcolumns: |p{4.9cm}|p{3.3cm}|p{9.1cm}| -->


<table>
<caption>struct v4l2_frmivalenum</caption>
<tbody>
<tr>
<td>


\__u32

</td>
<td>


`index`

</td>
<td>


IN: Index of the given frame interval in the enumeration.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`pixel_format`

</td>
<td>


IN: Pixel format for which the frame intervals are enumerated.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`width`

</td>
<td>


IN: Frame width for which the frame intervals are enumerated.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`height`

</td>
<td>


IN: Frame height for which the frame intervals are enumerated.

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


OUT: Frame interval type the device supports.

</td>
</tr>
<tr>
<td>


union \{

</td>
<td>


(anonymous)

</td>
<td>


OUT: Frame interval with the given index.

</td>
</tr>
<tr>
<td>


struct `v4l2_fract`

</td>
<td>


`discrete`

</td>
<td>


Frame interval \[s\].

</td>
</tr>
<tr>
<td>


struct `v4l2_frmival_stepwise`

</td>
<td>


`stepwise`

</td>
<td>




</td>
</tr>
<tr>
<td>


\}

</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`reserved[2]`

</td>
<td>


Reserved space for future use. Must be zeroed by drivers and applications.

</td>
</tr>
</tbody>
</table>

<a id="rst-enums"></a>

## Enums





<a id="c-v4l2_frmivaltypes"></a>

```c
v4l2_frmivaltypes
```

<!-- tabularcolumns: |p{6.6cm}|p{2.2cm}|p{8.5cm}| -->


<table>
<caption>enum v4l2_frmivaltypes</caption>
<tbody>
<tr>
<td>


`V4L2_FRMIVAL_TYPE_DISCRETE`

</td>
<td>


1

</td>
<td>


Discrete frame interval.

</td>
</tr>
<tr>
<td>


`V4L2_FRMIVAL_TYPE_CONTINUOUS`

</td>
<td>


2

</td>
<td>


Continuous frame interval.

</td>
</tr>
<tr>
<td>


`V4L2_FRMIVAL_TYPE_STEPWISE`

</td>
<td>


3

</td>
<td>


Step-wise defined frame interval.

</td>
</tr>
</tbody>
</table>

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
