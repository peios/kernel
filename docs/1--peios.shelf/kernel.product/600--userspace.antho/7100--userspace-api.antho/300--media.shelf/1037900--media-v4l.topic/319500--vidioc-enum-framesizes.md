---
title: "ioctl VIDIOC_ENUM_FRAMESIZES"
type: reference
description: "VIDIOC_ENUM_FRAMESIZES - Enumerate frame sizes"
---

<a id="rst-ioctl-vidioc-enum-framesizes"></a>
<a id="rst-vidioc-enum-framesizes"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

VIDIOC_ENUM_FRAMESIZES - Enumerate frame sizes

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-VIDIOC_ENUM_FRAMESIZES"></a>

```c
VIDIOC_ENUM_FRAMESIZES
```

`int ioctl(int fd, VIDIOC_ENUM_FRAMESIZES, struct v4l2_frmsizeenum *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to struct `v4l2_frmsizeenum` that contains an index and pixel format and receives a frame width and height.

<a id="rst-description"></a>

## Description

This ioctl allows applications to enumerate all frame sizes (i. e. width and height in pixels) that the device supports for the given pixel format.

The supported pixel formats can be obtained by using the [ioctl VIDIOC_ENUM_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-enum-fmt#rst-vidioc-enum-fmt>) function.

The return value and the content of the `v4l2_frmsizeenum.type` field depend on the type of frame sizes the device supports. Here are the semantics of the function for the different cases:

- **Discrete:** The function returns success if the given index value (zero-based) is valid. The application should increase the index by one for each call until `EINVAL` is returned. The `v4l2_frmsizeenum.type` field is set to `V4L2_FRMSIZE_TYPE_DISCRETE` by the driver. Of the union only the `discrete` member is valid.

- **Step-wise:** The function returns success if the given index value is zero and `EINVAL` for any other index value. The `v4l2_frmsizeenum.type` field is set to `V4L2_FRMSIZE_TYPE_STEPWISE` by the driver. Of the union only the `stepwise` member is valid.

- **Continuous:** This is a special case of the step-wise type above. The function returns success if the given index value is zero and `EINVAL` for any other index value. The `v4l2_frmsizeenum.type` field is set to `V4L2_FRMSIZE_TYPE_CONTINUOUS` by the driver. Of the union only the `stepwise` member is valid and the `step_width` and `step_height` values are set to 1.

When the application calls the function with index zero, it must check the `type` field to determine the type of frame size enumeration the device supports. Only for the `V4L2_FRMSIZE_TYPE_DISCRETE` type does it make sense to increase the index value to receive more frame sizes.

> [!NOTE]
>
> The order in which the frame sizes are returned has no special meaning. In particular does it not say anything about potential default format sizes.

Applications can assume that the enumeration data does not change without any interaction from the application itself. This means that the enumeration data is consistent if the application does not perform any other ioctl calls while it runs the frame size enumeration.

<a id="rst-structs"></a>

## Structs

In the structs below, *IN* denotes a value that has to be filled in by the application, *OUT* denotes values that the driver fills in. The application should zero out all members except for the *IN* fields.





<a id="c-v4l2_frmsize_discrete"></a>

```c
v4l2_frmsize_discrete
```


<table>
<caption>struct v4l2_frmsize_discrete</caption>
<tbody>
<tr>
<td>


\__u32

</td>
<td>


`width`

</td>
<td>


Width of the frame \[pixel\].

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


Height of the frame \[pixel\].

</td>
</tr>
</tbody>
</table>





<a id="c-v4l2_frmsize_stepwise"></a>

```c
v4l2_frmsize_stepwise
```


<table>
<caption>struct v4l2_frmsize_stepwise</caption>
<tbody>
<tr>
<td>


\__u32

</td>
<td>


`min_width`

</td>
<td>


Minimum frame width \[pixel\].

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`max_width`

</td>
<td>


Maximum frame width \[pixel\].

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`step_width`

</td>
<td>


Frame width step size \[pixel\].

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`min_height`

</td>
<td>


Minimum frame height \[pixel\].

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`max_height`

</td>
<td>


Maximum frame height \[pixel\].

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`step_height`

</td>
<td>


Frame height step size \[pixel\].

</td>
</tr>
</tbody>
</table>





<a id="c-v4l2_frmsizeenum"></a>

```c
v4l2_frmsizeenum
```

<!-- tabularcolumns: |p{6.4cm}|p{2.8cm}|p{8.1cm}| -->


<table>
<caption>struct v4l2_frmsizeenum</caption>
<tbody>
<tr>
<td>


\__u32

</td>
<td>


`index`

</td>
<td>


IN: Index of the given frame size in the enumeration.

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


IN: Pixel format for which the frame sizes are enumerated.

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


OUT: Frame size type the device supports.

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


OUT: Frame size with the given index.

</td>
</tr>
<tr>
<td>


struct `v4l2_frmsize_discrete`

</td>
<td>


`discrete`

</td>
<td>




</td>
</tr>
<tr>
<td>


struct `v4l2_frmsize_stepwise`

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





<a id="c-v4l2_frmsizetypes"></a>

```c
v4l2_frmsizetypes
```

<!-- tabularcolumns: |p{6.6cm}|p{2.2cm}|p{8.5cm}| -->


<table>
<caption>enum v4l2_frmsizetypes</caption>
<tbody>
<tr>
<td>


`V4L2_FRMSIZE_TYPE_DISCRETE`

</td>
<td>


1

</td>
<td>


Discrete frame size.

</td>
</tr>
<tr>
<td>


`V4L2_FRMSIZE_TYPE_CONTINUOUS`

</td>
<td>


2

</td>
<td>


Continuous frame size.

</td>
</tr>
<tr>
<td>


`V4L2_FRMSIZE_TYPE_STEPWISE`

</td>
<td>


3

</td>
<td>


Step-wise defined frame size.

</td>
</tr>
</tbody>
</table>

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
