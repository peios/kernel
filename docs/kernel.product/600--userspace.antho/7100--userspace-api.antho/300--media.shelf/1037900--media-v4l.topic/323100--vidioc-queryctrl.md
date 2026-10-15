---
title: "ioctls VIDIOC_QUERYCTRL, VIDIOC_QUERY_EXT_CTRL and VIDIOC_QUERYMENU"
type: reference
description: "VIDIOC_QUERYCTRL - VIDIOC_QUERY_EXT_CTRL - VIDIOC_QUERYMENU - Enumerate controls and menu control items"
---

<a id="rst-ioctls-vidioc-queryctrl-vidioc-query-ext-ctrl-and-vidioc-querymenu"></a>
<a id="rst-vidioc-queryctrl"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

VIDIOC\_QUERYCTRL - VIDIOC\_QUERY\_EXT\_CTRL - VIDIOC\_QUERYMENU - Enumerate controls and menu control items

<a id="rst-synopsis"></a>

## Synopsis

<a id="c-VIDIOC_QUERY_CTRL"></a>



```c
VIDIOC_QUERY_CTRL
```

`int ioctl(int fd, int VIDIOC_QUERYCTRL, struct v4l2_queryctrl *argp)`

<a id="c-VIDIOC_QUERY_EXT_CTRL"></a>



```c
VIDIOC_QUERY_EXT_CTRL
```

`int ioctl(int fd, VIDIOC_QUERY_EXT_CTRL, struct v4l2_query_ext_ctrl *argp)`

<a id="c-VIDIOC_QUERYMENU"></a>



```c
VIDIOC_QUERYMENU
```

`int ioctl(int fd, VIDIOC_QUERYMENU, struct v4l2_querymenu *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to struct `v4l2_queryctrl`, `v4l2_query_ext_ctrl` or `v4l2_querymenu` (depending on the ioctl).

<a id="rst-description"></a>

## Description

To query the attributes of a control applications set the `id` field of a struct [v4l2\_queryctrl](<#rst-v4l2-queryctrl>) and call the `VIDIOC_QUERYCTRL` ioctl with a pointer to this structure. The driver fills the rest of the structure or returns an `EINVAL` error code when the `id` is invalid.

It is possible to enumerate controls by calling `VIDIOC_QUERYCTRL` with successive `id` values starting from `V4L2_CID_BASE` up to and exclusive `V4L2_CID_LASTP1`. Drivers may return `EINVAL` if a control in this range is not supported. Further applications can enumerate private controls, which are not defined in this specification, by starting at `V4L2_CID_PRIVATE_BASE` and incrementing `id` until the driver returns `EINVAL`.

In both cases, when the driver sets the `V4L2_CTRL_FLAG_DISABLED` flag in the `flags` field this control is permanently disabled and should be ignored by the application. <a id="rst-footnote-reference-1"></a>[1](#rst-f1)

When the application ORs `id` with `V4L2_CTRL_FLAG_NEXT_CTRL` the driver returns the next supported non-compound control, or `EINVAL` if there is none. In addition, the `V4L2_CTRL_FLAG_NEXT_COMPOUND` flag can be specified to enumerate all compound controls (i.e. controls with type ≥ `V4L2_CTRL_COMPOUND_TYPES` and/or array control, in other words controls that contain more than one value). Specify both `V4L2_CTRL_FLAG_NEXT_CTRL` and `V4L2_CTRL_FLAG_NEXT_COMPOUND` in order to enumerate all controls, compound or not. Drivers which do not support these flags yet always return `EINVAL`.

The `VIDIOC_QUERY_EXT_CTRL` ioctl was introduced in order to better support controls that can use compound types, and to expose additional control information that cannot be returned in struct [v4l2\_queryctrl](<#rst-v4l2-queryctrl>) since that structure is full.

`VIDIOC_QUERY_EXT_CTRL` is used in the same way as `VIDIOC_QUERYCTRL`, except that the `reserved` array must be zeroed as well.

Additional information is required for menu controls: the names of the menu items. To query them applications set the `id` and `index` fields of struct [v4l2\_querymenu](<#rst-v4l2-querymenu>) and call the `VIDIOC_QUERYMENU` ioctl with a pointer to this structure. The driver fills the rest of the structure or returns an `EINVAL` error code when the `id` or `index` is invalid. Menu items are enumerated by calling `VIDIOC_QUERYMENU` with successive `index` values from struct [v4l2\_queryctrl](<#rst-v4l2-queryctrl>) `minimum` to `maximum`, inclusive.

> [!NOTE]
>
> It is possible for `VIDIOC_QUERYMENU` to return an `EINVAL` error code for some indices between `minimum` and `maximum`. In that case that particular menu item is not supported by this driver. Also note that the `minimum` value is not necessarily 0.

See also the examples in [control](<~kernel/userspace/userspace-api/media-v4l/control#rst-control>).

<!-- tabularcolumns: |p{1.2cm}|p{3.6cm}|p{12.5cm}| -->

<a id="rst-v4l2-queryctrl"></a>

<a id="c-struct-v4l2_queryctrl"></a>



```c
v4l2_queryctrl
```


<table>
<caption>

struct v4l2\_queryctrl

</caption>
<tbody>
<tr>
<td>



\_\_u32

</td>
<td>



`id`

</td>
<td>



Identifies the control, set by the application. See [control-id](<~kernel/userspace/userspace-api/media-v4l/control#rst-control-id>) for predefined IDs. When the ID is ORed with V4L2\_CTRL\_FLAG\_NEXT\_CTRL the driver clears the flag and returns the first control with a higher ID. Drivers which do not support this flag yet always return an `EINVAL` error code.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`type`

</td>
<td>



Type of control, see `v4l2_ctrl_type`.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`name`\[32\]

</td>
<td>



Name of the control, a NUL-terminated ASCII string. This information is intended for the user.

</td>
</tr>
<tr>
<td>



\_\_s32

</td>
<td>



`minimum`

</td>
<td>



Minimum value, inclusive. This field gives a lower bound for the control. See enum `v4l2_ctrl_type` how the minimum value is to be used for each possible control type. Note that this a signed 32-bit value.

</td>
</tr>
<tr>
<td>



\_\_s32

</td>
<td>



`maximum`

</td>
<td>



Maximum value, inclusive. This field gives an upper bound for the control. See enum `v4l2_ctrl_type` how the maximum value is to be used for each possible control type. Note that this a signed 32-bit value.

</td>
</tr>
<tr>
<td>



\_\_s32

</td>
<td>



`step`

</td>
<td>



This field gives a step size for the control. See enum `v4l2_ctrl_type` how the step value is to be used for each possible control type. Note that this an unsigned 32-bit value.

Generally drivers should not scale hardware control values. It may be necessary for example when the `name` or `id` imply a particular unit and the hardware actually accepts only multiples of said unit. If so, drivers must take care values are properly rounded when scaling, such that errors will not accumulate on repeated read-write cycles.

This field gives the smallest change of an integer control actually affecting hardware. Often the information is needed when the user can change controls by keyboard or GUI buttons, rather than a slider. When for example a hardware register accepts values 0-511 and the driver reports 0-65535, step should be 128.

Note that although signed, the step value is supposed to be always positive.

</td>
</tr>
<tr>
<td>



\_\_s32

</td>
<td>



`default_value`

</td>
<td>



The default value of a `V4L2_CTRL_TYPE_INTEGER`, `_BOOLEAN`, `_BITMASK`, `_MENU` or `_INTEGER_MENU` control. Not valid for other types of controls.

> [!NOTE]
>
> Drivers reset controls to their default value only when the driver is first loaded, never afterwards.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`flags`

</td>
<td>



Control flags, see [control-flags](<#rst-control-flags>).

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`reserved`\[2\]

</td>
<td>



Reserved for future extensions. Drivers must set the array to zero.

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{1.2cm}|p{5.5cm}|p{10.6cm}| -->

<a id="rst-v4l2-query-ext-ctrl"></a>

<a id="c-struct-v4l2_query_ext_ctrl"></a>



```c
v4l2_query_ext_ctrl
```


<table>
<caption>

struct v4l2\_query\_ext\_ctrl

</caption>
<tbody>
<tr>
<td>



\_\_u32

</td>
<td>



`id`

</td>
<td>



Identifies the control, set by the application. See [control-id](<~kernel/userspace/userspace-api/media-v4l/control#rst-control-id>) for predefined IDs. When the ID is ORed with `V4L2_CTRL_FLAG_NEXT_CTRL` the driver clears the flag and returns the first non-compound control with a higher ID. When the ID is ORed with `V4L2_CTRL_FLAG_NEXT_COMPOUND` the driver clears the flag and returns the first compound control with a higher ID. Set both to get the first control (compound or not) with a higher ID.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`type`

</td>
<td>



Type of control, see `v4l2_ctrl_type`.

</td>
</tr>
<tr>
<td>



char

</td>
<td>



`name`\[32\]

</td>
<td>



Name of the control, a NUL-terminated ASCII string. This information is intended for the user.

</td>
</tr>
<tr>
<td>



\_\_s64

</td>
<td>



`minimum`

</td>
<td>



Minimum value, inclusive. This field gives a lower bound for the control. See enum `v4l2_ctrl_type` how the minimum value is to be used for each possible control type. Note that this a signed 64-bit value.

</td>
</tr>
<tr>
<td>



\_\_s64

</td>
<td>



`maximum`

</td>
<td>



Maximum value, inclusive. This field gives an upper bound for the control. See enum `v4l2_ctrl_type` how the maximum value is to be used for each possible control type. Note that this a signed 64-bit value.

</td>
</tr>
<tr>
<td>



\_\_u64

</td>
<td>



`step`

</td>
<td>



This field gives a step size for the control. See enum `v4l2_ctrl_type` how the step value is to be used for each possible control type. Note that this an unsigned 64-bit value.

Generally drivers should not scale hardware control values. It may be necessary for example when the `name` or `id` imply a particular unit and the hardware actually accepts only multiples of said unit. If so, drivers must take care values are properly rounded when scaling, such that errors will not accumulate on repeated read-write cycles.

This field gives the smallest change of an integer control actually affecting hardware. Often the information is needed when the user can change controls by keyboard or GUI buttons, rather than a slider. When for example a hardware register accepts values 0-511 and the driver reports 0-65535, step should be 128.

</td>
</tr>
<tr>
<td>



\_\_s64

</td>
<td>



`default_value`

</td>
<td>



The default value of a `V4L2_CTRL_TYPE_INTEGER`, `_INTEGER64`, `_BOOLEAN`, `_BITMASK`, `_MENU`, `_INTEGER_MENU`, `_U8` or `_U16` control. Not valid for other types of controls.

> [!NOTE]
>
> Drivers reset controls to their default value only when the driver is first loaded, never afterwards.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`flags`

</td>
<td>



Control flags, see [control-flags](<#rst-control-flags>).

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`elem_size`

</td>
<td>



The size in bytes of a single element of the array. Given a char pointer `p` to a 3-dimensional array you can find the position of cell `(z, y, x)` as follows: `p + ((z * dims[1] + y) * dims[0] + x) * elem_size`. `elem_size` is always valid, also when the control isn't an array. For string controls `elem_size` is equal to `maximum + 1`.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`elems`

</td>
<td>



The number of elements in the N-dimensional array. If this control is not an array, then `elems` is 1. The `elems` field can never be 0.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`nr_of_dims`

</td>
<td>



The number of dimension in the N-dimensional array. If this control is not an array, then this field is 0.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`dims[V4L2_CTRL_MAX_DIMS]`

</td>
<td>



The size of each dimension. The first `nr_of_dims` elements of this array must be non-zero, all remaining elements must be zero.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`reserved`\[32\]

</td>
<td>



Reserved for future extensions. Applications and drivers must set the array to zero.

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{1.2cm}|p{3.0cm}|p{13.1cm}| -->

<a id="rst-v4l2-querymenu"></a>

<a id="c-struct-v4l2_querymenu"></a>



```c
v4l2_querymenu
```


<table>
<caption>

struct v4l2\_querymenu

</caption>
<tbody>
<tr>
<td>



\_\_u32

</td>
<td>



`id`

</td>
<td>



Identifies the control, set by the application from the respective struct [v4l2\_queryctrl](<#rst-v4l2-queryctrl>) `id`.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`index`

</td>
<td>



Index of the menu item, starting at zero, set by the application.

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



\_\_u8

</td>
<td>



`name`\[32\]

</td>
<td>



Name of the menu item, a NUL-terminated ASCII string. This information is intended for the user. This field is valid for `V4L2_CTRL_TYPE_MENU` type controls.

</td>
</tr>
<tr>
<td>



\_\_s64

</td>
<td>



`value`

</td>
<td>



Value of the integer menu item. This field is valid for `V4L2_CTRL_TYPE_INTEGER_MENU` type controls.

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



\_\_u32

</td>
<td>



`reserved`

</td>
<td>



Reserved for future extensions. Drivers must set the array to zero.

</td>
</tr>
</tbody>
</table>

<a id="c-v4l2_ctrl_type"></a>



```c
v4l2_ctrl_type
```

<!-- Source LaTeX layout: \footnotesize -->

<!-- tabularcolumns: |p{6.5cm}|p{1.5cm}|p{1.1cm}|p{1.5cm}|p{6.8cm}| -->


<table>
<caption>

enum v4l2\_ctrl\_type

</caption>
<thead>
<tr>
<th>



Type

</th>
<th>



`minimum`

</th>
<th>



`step`

</th>
<th>



`maximum`

</th>
<th>



Description

</th>
</tr>
</thead>
<tbody>
<tr>
<td>



`V4L2_CTRL_TYPE_INTEGER`

</td>
<td>



any

</td>
<td>



any

</td>
<td>



any

</td>
<td>



An integer-valued control ranging from minimum to maximum inclusive. The step value indicates the increment between values.

</td>
</tr>
<tr>
<td>



`V4L2_CTRL_TYPE_BOOLEAN`

</td>
<td>



0

</td>
<td>



1

</td>
<td>



1

</td>
<td>



A boolean-valued control. Zero corresponds to "disabled", and one means "enabled".

</td>
</tr>
<tr>
<td>



`V4L2_CTRL_TYPE_MENU`

</td>
<td>



≥ 0

</td>
<td>



1

</td>
<td>



N-1

</td>
<td>



The control has a menu of N choices. The names of the menu items can be enumerated with the `VIDIOC_QUERYMENU` ioctl.

</td>
</tr>
<tr>
<td>



`V4L2_CTRL_TYPE_INTEGER_MENU`

</td>
<td>



≥ 0

</td>
<td>



1

</td>
<td>



N-1

</td>
<td>



The control has a menu of N choices. The values of the menu items can be enumerated with the `VIDIOC_QUERYMENU` ioctl. This is similar to `V4L2_CTRL_TYPE_MENU` except that instead of strings, the menu items are signed 64-bit integers.

</td>
</tr>
<tr>
<td>



`V4L2_CTRL_TYPE_BITMASK`

</td>
<td>



0

</td>
<td>



n/a

</td>
<td>



any

</td>
<td>



A bitmask field. The maximum value is the set of bits that can be used, all other bits are to be 0. The maximum value is interpreted as a \_\_u32, allowing the use of bit 31 in the bitmask.

</td>
</tr>
<tr>
<td>



`V4L2_CTRL_TYPE_BUTTON`

</td>
<td>



0

</td>
<td>



0

</td>
<td>



0

</td>
<td>



A control which performs an action when set. Drivers must ignore the value passed with `VIDIOC_S_CTRL` and return an `EACCES` error code on a `VIDIOC_G_CTRL` attempt.

</td>
</tr>
<tr>
<td>



`V4L2_CTRL_TYPE_INTEGER64`

</td>
<td>



any

</td>
<td>



any

</td>
<td>



any

</td>
<td>



A 64-bit integer valued control. Minimum, maximum and step size cannot be queried using `VIDIOC_QUERYCTRL`. Only `VIDIOC_QUERY_EXT_CTRL` can retrieve the 64-bit min/max/step values, they should be interpreted as n/a when using `VIDIOC_QUERYCTRL`.

</td>
</tr>
<tr>
<td>



`V4L2_CTRL_TYPE_STRING`

</td>
<td>



≥ 0

</td>
<td>



≥ 1

</td>
<td>



≥ 0

</td>
<td>



The minimum and maximum string lengths. The step size means that the string must be (minimum + N \* step) characters long for N ≥ 0. These lengths do not include the terminating zero, so in order to pass a string of length 8 to [VIDIOC\_S\_EXT\_CTRLS](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-ext-ctrls#rst-vidioc-g-ext-ctrls>) you need to set the `size` field of struct `v4l2_ext_control` to 9. For [VIDIOC\_G\_EXT\_CTRLS](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-ext-ctrls#rst-vidioc-g-ext-ctrls>) you can set the `size` field to `maximum` + 1. Which character encoding is used will depend on the string control itself and should be part of the control documentation.

</td>
</tr>
<tr>
<td>



`V4L2_CTRL_TYPE_CTRL_CLASS`

</td>
<td>



n/a

</td>
<td>



n/a

</td>
<td>



n/a

</td>
<td>



This is not a control. When `VIDIOC_QUERYCTRL` is called with a control ID equal to a control class code (see [ctrl-class](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-ext-ctrls#rst-ctrl-class>)) + 1, the ioctl returns the name of the control class and this control type. Older drivers which do not support this feature return an `EINVAL` error code.

</td>
</tr>
<tr>
<td>



`V4L2_CTRL_TYPE_U8`

</td>
<td>



any

</td>
<td>



any

</td>
<td>



any

</td>
<td>



An unsigned 8-bit valued control ranging from minimum to maximum inclusive. The step value indicates the increment between values.

</td>
</tr>
<tr>
<td>



`V4L2_CTRL_TYPE_U16`

</td>
<td>



any

</td>
<td>



any

</td>
<td>



any

</td>
<td>



An unsigned 16-bit valued control ranging from minimum to maximum inclusive. The step value indicates the increment between values.

</td>
</tr>
<tr>
<td>



`V4L2_CTRL_TYPE_U32`

</td>
<td>



any

</td>
<td>



any

</td>
<td>



any

</td>
<td>



An unsigned 32-bit valued control ranging from minimum to maximum inclusive. The step value indicates the increment between values.

</td>
</tr>
<tr>
<td>



`V4L2_CTRL_TYPE_MPEG2_QUANTISATION`

</td>
<td>



n/a

</td>
<td>



n/a

</td>
<td>



n/a

</td>
<td>



A struct `v4l2_ctrl_mpeg2_quantisation`, containing MPEG-2 quantisation matrices for stateless video decoders.

</td>
</tr>
<tr>
<td>



`V4L2_CTRL_TYPE_MPEG2_SEQUENCE`

</td>
<td>



n/a

</td>
<td>



n/a

</td>
<td>



n/a

</td>
<td>



A struct `v4l2_ctrl_mpeg2_sequence`, containing MPEG-2 sequence parameters for stateless video decoders.

</td>
</tr>
<tr>
<td>



`V4L2_CTRL_TYPE_MPEG2_PICTURE`

</td>
<td>



n/a

</td>
<td>



n/a

</td>
<td>



n/a

</td>
<td>



A struct `v4l2_ctrl_mpeg2_picture`, containing MPEG-2 picture parameters for stateless video decoders.

</td>
</tr>
<tr>
<td>



`V4L2_CTRL_TYPE_AREA`

</td>
<td>



n/a

</td>
<td>



n/a

</td>
<td>



n/a

</td>
<td>



A struct `v4l2_area`, containing the width and the height of a rectangular area. Units depend on the use case.

</td>
</tr>
<tr>
<td>



`V4L2_CTRL_TYPE_RECT`

</td>
<td>



n/a

</td>
<td>



n/a

</td>
<td>



n/a

</td>
<td>



A struct `v4l2_rect`, containing a rectangle described by the position of its top-left corner, the width and the height. Units depend on the use case. Support for `V4L2_CTRL_WHICH_MIN_VAL` and `V4L2_CTRL_WHICH_MAX_VAL` is optional and depends on the `V4L2_CTRL_FLAG_HAS_WHICH_MIN_MAX` flag. See the documentation of the specific control on how to interpret the minimum and maximum values.

</td>
</tr>
<tr>
<td>



`V4L2_CTRL_TYPE_H264_SPS`

</td>
<td>



n/a

</td>
<td>



n/a

</td>
<td>



n/a

</td>
<td>



A struct `v4l2_ctrl_h264_sps`, containing H264 sequence parameters for stateless video decoders.

</td>
</tr>
<tr>
<td>



`V4L2_CTRL_TYPE_H264_PPS`

</td>
<td>



n/a

</td>
<td>



n/a

</td>
<td>



n/a

</td>
<td>



A struct `v4l2_ctrl_h264_pps`, containing H264 picture parameters for stateless video decoders.

</td>
</tr>
<tr>
<td>



`V4L2_CTRL_TYPE_H264_SCALING_MATRIX`

</td>
<td>



n/a

</td>
<td>



n/a

</td>
<td>



n/a

</td>
<td>



A struct `v4l2_ctrl_h264_scaling_matrix`, containing H264 scaling matrices for stateless video decoders.

</td>
</tr>
<tr>
<td>



`V4L2_CTRL_TYPE_H264_SLICE_PARAMS`

</td>
<td>



n/a

</td>
<td>



n/a

</td>
<td>



n/a

</td>
<td>



A struct `v4l2_ctrl_h264_slice_params`, containing H264 slice parameters for stateless video decoders.

</td>
</tr>
<tr>
<td>



`V4L2_CTRL_TYPE_H264_DECODE_PARAMS`

</td>
<td>



n/a

</td>
<td>



n/a

</td>
<td>



n/a

</td>
<td>



A struct `v4l2_ctrl_h264_decode_params`, containing H264 decode parameters for stateless video decoders.

</td>
</tr>
<tr>
<td>



`V4L2_CTRL_TYPE_FWHT_PARAMS`

</td>
<td>



n/a

</td>
<td>



n/a

</td>
<td>



n/a

</td>
<td>



A struct `v4l2_ctrl_fwht_params`, containing FWHT parameters for stateless video decoders.

</td>
</tr>
<tr>
<td>



`V4L2_CTRL_TYPE_HEVC_SPS`

</td>
<td>



n/a

</td>
<td>



n/a

</td>
<td>



n/a

</td>
<td>



A struct `v4l2_ctrl_hevc_sps`, containing HEVC Sequence Parameter Set for stateless video decoders.

</td>
</tr>
<tr>
<td>



`V4L2_CTRL_TYPE_HEVC_PPS`

</td>
<td>



n/a

</td>
<td>



n/a

</td>
<td>



n/a

</td>
<td>



A struct `v4l2_ctrl_hevc_pps`, containing HEVC Picture Parameter Set for stateless video decoders.

</td>
</tr>
<tr>
<td>



`V4L2_CTRL_TYPE_HEVC_SLICE_PARAMS`

</td>
<td>



n/a

</td>
<td>



n/a

</td>
<td>



n/a

</td>
<td>



A struct `v4l2_ctrl_hevc_slice_params`, containing HEVC slice parameters for stateless video decoders.

</td>
</tr>
<tr>
<td>



`V4L2_CTRL_TYPE_HEVC_SCALING_MATRIX`

</td>
<td>



n/a

</td>
<td>



n/a

</td>
<td>



n/a

</td>
<td>



A struct `v4l2_ctrl_hevc_scaling_matrix`, containing HEVC scaling matrix for stateless video decoders.

</td>
</tr>
<tr>
<td>



`V4L2_CTRL_TYPE_VP8_FRAME`

</td>
<td>



n/a

</td>
<td>



n/a

</td>
<td>



n/a

</td>
<td>



A struct `v4l2_ctrl_vp8_frame`, containing VP8 frame parameters for stateless video decoders.

</td>
</tr>
<tr>
<td>



`V4L2_CTRL_TYPE_HEVC_DECODE_PARAMS`

</td>
<td>



n/a

</td>
<td>



n/a

</td>
<td>



n/a

</td>
<td>



A struct `v4l2_ctrl_hevc_decode_params`, containing HEVC decoding parameters for stateless video decoders.

</td>
</tr>
<tr>
<td>



`V4L2_CTRL_TYPE_HEVC_EXT_SPS_LT_RPS`

</td>
<td>



n/a

</td>
<td>



n/a

</td>
<td>



n/a

</td>
<td>



A struct `v4l2_ctrl_hevc_ext_sps_lt_rps`, containing HEVC extended Long-Term RPS for stateless video decoders.

</td>
</tr>
<tr>
<td>



`V4L2_CTRL_TYPE_HEVC_EXT_SPS_ST_RPS`

</td>
<td>



n/a

</td>
<td>



n/a

</td>
<td>



n/a

</td>
<td>



A struct `v4l2_ctrl_hevc_ext_sps_st_rps`, containing HEVC extended Short-Term RPS for stateless video decoders.

</td>
</tr>
<tr>
<td>



`V4L2_CTRL_TYPE_VP9_COMPRESSED_HDR`

</td>
<td>



n/a

</td>
<td>



n/a

</td>
<td>



n/a

</td>
<td>



A struct `v4l2_ctrl_vp9_compressed_hdr`, containing VP9 probabilities updates for stateless video decoders.

</td>
</tr>
<tr>
<td>



`V4L2_CTRL_TYPE_VP9_FRAME`

</td>
<td>



n/a

</td>
<td>



n/a

</td>
<td>



n/a

</td>
<td>



A struct `v4l2_ctrl_vp9_frame`, containing VP9 frame decode parameters for stateless video decoders.

</td>
</tr>
<tr>
<td>



`V4L2_CTRL_TYPE_AV1_SEQUENCE`

</td>
<td>



n/a

</td>
<td>



n/a

</td>
<td>



n/a

</td>
<td>



A struct `v4l2_ctrl_av1_sequence`, containing AV1 Sequence OBU decoding parameters for stateless video decoders.

</td>
</tr>
<tr>
<td>



`V4L2_CTRL_TYPE_AV1_TILE_GROUP_ENTRY`

</td>
<td>



n/a

</td>
<td>



n/a

</td>
<td>



n/a

</td>
<td>



A struct `v4l2_ctrl_av1_tile_group_entry`, containing AV1 Tile Group OBU decoding parameters for stateless video decoders.

</td>
</tr>
<tr>
<td>



`V4L2_CTRL_TYPE_AV1_FRAME`

</td>
<td>



n/a

</td>
<td>



n/a

</td>
<td>



n/a

</td>
<td>



A struct `v4l2_ctrl_av1_frame`, containing AV1 Frame/Frame Header OBU decoding parameters for stateless video decoders.

</td>
</tr>
<tr>
<td>



`V4L2_CTRL_TYPE_AV1_FILM_GRAIN`

</td>
<td>



n/a

</td>
<td>



n/a

</td>
<td>



n/a

</td>
<td>



A struct `v4l2_ctrl_av1_film_grain`, containing AV1 Film Grain parameters for stateless video decoders.

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

<!-- tabularcolumns: |p{7.3cm}|p{1.8cm}|p{8.2cm}| -->

<a id="rst-control-flags"></a>


<table>
<caption>

Control Flags

</caption>
<tbody>
<tr>
<td>



`V4L2_CTRL_FLAG_DISABLED`

</td>
<td>



0x0001

</td>
<td>



This control is permanently disabled and should be ignored by the application. Any attempt to change the control will result in an `EINVAL` error code.

</td>
</tr>
<tr>
<td>



`V4L2_CTRL_FLAG_GRABBED`

</td>
<td>



0x0002

</td>
<td>



This control is temporarily unchangeable, for example because another application took over control of the respective resource. Such controls may be displayed specially in a user interface. Attempts to change the control may result in an `EBUSY` error code.

</td>
</tr>
<tr>
<td>



`V4L2_CTRL_FLAG_READ_ONLY`

</td>
<td>



0x0004

</td>
<td>



This control is permanently readable only. Any attempt to change the control will result in an `EINVAL` error code.

</td>
</tr>
<tr>
<td>



`V4L2_CTRL_FLAG_UPDATE`

</td>
<td>



0x0008

</td>
<td>



A hint that changing this control may affect the value of other controls within the same control class. Applications should update their user interface accordingly.

</td>
</tr>
<tr>
<td>



`V4L2_CTRL_FLAG_INACTIVE`

</td>
<td>



0x0010

</td>
<td>



This control is not applicable to the current configuration and should be displayed accordingly in a user interface. For example the flag may be set on a MPEG audio level 2 bitrate control when MPEG audio encoding level 1 was selected with another control.

</td>
</tr>
<tr>
<td>



`V4L2_CTRL_FLAG_SLIDER`

</td>
<td>



0x0020

</td>
<td>



A hint that this control is best represented as a slider-like element in a user interface.

</td>
</tr>
<tr>
<td>



`V4L2_CTRL_FLAG_WRITE_ONLY`

</td>
<td>



0x0040

</td>
<td>



This control is permanently writable only. Any attempt to read the control will result in an `EACCES` error code error code. This flag is typically present for relative controls or action controls where writing a value will cause the device to carry out a given action (e. g. motor control) but no meaningful value can be returned.

</td>
</tr>
<tr>
<td>



`V4L2_CTRL_FLAG_VOLATILE`

</td>
<td>



0x0080

</td>
<td>



This control is volatile, which means that the value of the control changes continuously. A typical example would be the current gain value if the device is in auto-gain mode. In such a case the hardware calculates the gain value based on the lighting conditions which can change over time.

> [!NOTE]
>
> Setting a new value for a volatile control will be ignored unless [V4L2\_CTRL\_FLAG\_EXECUTE\_ON\_WRITE](<#rst-flag-execute-on-write>) is also set. Setting a new value for a volatile control will <em>never</em> trigger a [V4L2\_EVENT\_CTRL\_CH\_VALUE](<~kernel/userspace/userspace-api/media-v4l/vidioc-dqevent#rst-ctrl-changes-flags>) event.

</td>
</tr>
<tr>
<td>



`V4L2_CTRL_FLAG_HAS_PAYLOAD`

</td>
<td>



0x0100

</td>
<td>



This control has a pointer type, so its value has to be accessed using one of the pointer fields of struct `v4l2_ext_control`. This flag is set for controls that are an array, string, or have a compound type. In all cases you have to set a pointer to memory containing the payload of the control.

</td>
</tr>
<tr>
<td>



`V4L2_CTRL_FLAG_EXECUTE_ON_WRITE`

</td>
<td>



0x0200

</td>
<td>



<a id="rst-flag-execute-on-write"></a>

The value provided to the control will be propagated to the driver even if it remains constant. This is required when the control represents an action on the hardware. For example: clearing an error flag or triggering the flash. All the controls of the type `V4L2_CTRL_TYPE_BUTTON` have this flag set.

</td>
</tr>
<tr>
<td>



`V4L2_CTRL_FLAG_MODIFY_LAYOUT`

</td>
<td>



0x0400

</td>
<td>



<a id="rst-flag-modify-layout"></a>

Changing this control value may modify the layout of the buffer (for video devices) or the media bus format (for sub-devices).

A typical example would be the `V4L2_CID_ROTATE` control.

Note that typically controls with this flag will also set the `V4L2_CTRL_FLAG_GRABBED` flag when buffers are allocated or streaming is in progress since most drivers do not support changing the format in that case.

</td>
</tr>
<tr>
<td>



`V4L2_CTRL_FLAG_DYNAMIC_ARRAY`

</td>
<td>



0x0800

</td>
<td>



This control is a dynamically sized 1-dimensional array. It behaves the same as a regular array, except that the number of elements as reported by the `elems` field is between 1 and `dims[0]`. So setting the control with a differently sized array will change the `elems` field when the control is queried afterwards.

</td>
</tr>
<tr>
<td>



`V4L2_CTRL_FLAG_HAS_WHICH_MIN_MAX`

</td>
<td>



0x1000

</td>
<td>



This control supports getting minimum and maximum values using vidioc\_g\_ext\_ctrls with V4L2\_CTRL\_WHICH\_MIN/MAX\_VAL.

</td>
</tr>
</tbody>
</table>

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

- **EINVAL**

  The struct [v4l2\_queryctrl](<#rst-v4l2-queryctrl>) `id` is invalid. The struct [v4l2\_querymenu](<#rst-v4l2-querymenu>) `id` is invalid or `index` is out of range (less than `minimum` or greater than `maximum`) or this particular menu item is not supported by the driver.

- **EACCES**

  An attempt was made to read a write-only control.

<a id="rst-f1"></a>



**[1]** `V4L2_CTRL_FLAG_DISABLED` was intended for two purposes: Drivers can skip predefined controls not supported by the hardware (although returning `EINVAL` would do as well), or disable predefined and private controls after hardware detection without the trouble of reordering control arrays and indices (`EINVAL` cannot be used to skip private controls because it would prematurely end the enumeration).
