---
title: "ioctl VIDIOC_G_EXT_CTRLS, VIDIOC_S_EXT_CTRLS, VIDIOC_TRY_EXT_CTRLS"
type: reference
description: "VIDIOC_G_EXT_CTRLS - VIDIOC_S_EXT_CTRLS - VIDIOC_TRY_EXT_CTRLS - Get or set the value of several controls, try control values"
---

<a id="rst-ioctl-vidioc-g-ext-ctrls-vidioc-s-ext-ctrls-vidioc-try-ext-ctrls"></a>
<a id="rst-vidioc-g-ext-ctrls"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

VIDIOC\_G\_EXT\_CTRLS - VIDIOC\_S\_EXT\_CTRLS - VIDIOC\_TRY\_EXT\_CTRLS - Get or set the value of several controls, try control values

<a id="rst-synopsis"></a>

## Synopsis

<a id="c-VIDIOC_G_EXT_CTRLS"></a>



```c
VIDIOC_G_EXT_CTRLS
```

`int ioctl(int fd, VIDIOC_G_EXT_CTRLS, struct v4l2_ext_controls *argp)`

<a id="c-VIDIOC_S_EXT_CTRLS"></a>



```c
VIDIOC_S_EXT_CTRLS
```

`int ioctl(int fd, VIDIOC_S_EXT_CTRLS, struct v4l2_ext_controls *argp)`

<a id="c-VIDIOC_TRY_EXT_CTRLS"></a>



```c
VIDIOC_TRY_EXT_CTRLS
```

`int ioctl(int fd, VIDIOC_TRY_EXT_CTRLS, struct v4l2_ext_controls *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to struct `v4l2_ext_controls`.

<a id="rst-description"></a>

## Description

These ioctls allow the caller to get or set multiple controls atomically. Control IDs are grouped into control classes (see [ctrl-class](<#rst-ctrl-class>)) and all controls in the control array must belong to the same control class.

Applications must always fill in the `count`, `which`, `controls` and `reserved` fields of struct `v4l2_ext_controls`, and initialize the struct `v4l2_ext_control` array pointed to by the `controls` fields.

To get the current value of a set of controls applications initialize the `id`, `size` and `reserved2` fields of each struct `v4l2_ext_control` and call the [VIDIOC\_G\_EXT\_CTRLS](<#rst-vidioc-g-ext-ctrls>) ioctl. String controls must also set the `string` field. Controls of compound types (`V4L2_CTRL_FLAG_HAS_PAYLOAD` is set) must set the `ptr` field.

If the `size` is too small to receive the control result (only relevant for pointer-type controls like strings), then the driver will set `size` to a valid value and return an `ENOSPC` error code. You should re-allocate the memory to this new size and try again. For the string type it is possible that the same issue occurs again if the string has grown in the meantime. It is recommended to call [ioctls VIDIOC\_QUERYCTRL, VIDIOC\_QUERY\_EXT\_CTRL and VIDIOC\_QUERYMENU](<~kernel/userspace/userspace-api/media-v4l/vidioc-queryctrl#rst-vidioc-queryctrl>) first and use `maximum`+1 as the new `size` value. It is guaranteed that that is sufficient memory.

N-dimensional arrays are set and retrieved row-by-row. You cannot set a partial array, all elements have to be set or retrieved. The total size is calculated as `elems` \* `elem_size`. These values can be obtained by calling [VIDIOC\_QUERY\_EXT\_CTRL](<~kernel/userspace/userspace-api/media-v4l/vidioc-queryctrl#rst-vidioc-queryctrl>).

To change the value of a set of controls applications initialize the `id`, `size`, `reserved2` and `value/value64/string/ptr` fields of each struct `v4l2_ext_control` and call the [VIDIOC\_S\_EXT\_CTRLS](<#rst-vidioc-g-ext-ctrls>) ioctl. The controls will only be set if <em>all</em> control values are valid.

To check if a set of controls have correct values applications initialize the `id`, `size`, `reserved2` and `value/value64/string/ptr` fields of each struct `v4l2_ext_control` and call the [VIDIOC\_TRY\_EXT\_CTRLS](<#rst-vidioc-g-ext-ctrls>) ioctl. It is up to the driver whether wrong values are automatically adjusted to a valid value or if an error is returned.

When the `id` or `which` is invalid drivers return an `EINVAL` error code. When the value is out of bounds drivers can choose to take the closest valid value or return an `ERANGE` error code, whatever seems more appropriate. In the first case the new value is set in struct `v4l2_ext_control`. If the new control value is inappropriate (e.g. the given menu index is not supported by the menu control), then this will also result in an `EINVAL` error code error.

If `request_fd` is set to a not-yet-queued [request](<~kernel/userspace/userspace-api/media-mediactl/request-api#rst-media-request-api>) file descriptor and `which` is set to `V4L2_CTRL_WHICH_REQUEST_VAL`, then the controls are not applied immediately when calling [VIDIOC\_S\_EXT\_CTRLS](<#rst-vidioc-g-ext-ctrls>), but instead are applied by the driver for the buffer associated with the same request. If the device does not support requests, then `EACCES` will be returned. If requests are supported but an invalid request file descriptor is given, then `EINVAL` will be returned.

An attempt to call [VIDIOC\_S\_EXT\_CTRLS](<#rst-vidioc-g-ext-ctrls>) for a request that has already been queued will result in an `EBUSY` error.

If `request_fd` is specified and `which` is set to `V4L2_CTRL_WHICH_REQUEST_VAL` during a call to [VIDIOC\_G\_EXT\_CTRLS](<#rst-vidioc-g-ext-ctrls>), then it will return the values of the controls at the time of request completion. If the request is not yet completed, then this will result in an `EACCES` error.

The driver will only set/get these controls if all control values are correct. This prevents the situation where only some of the controls were set/get. Only low-level errors (e. g. a failed i2c command) can still cause this situation.

<!-- tabularcolumns: |p{6.8cm}|p{4.0cm}|p{6.5cm}| -->

<a id="c-v4l2_ext_control"></a>



```c
v4l2_ext_control
```

<!-- Source LaTeX layout: \footnotesize -->


<table>
<caption>

struct v4l2\_ext\_control

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



Identifies the control, set by the application.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`size`

</td>
<td>



The total size in bytes of the payload of this control.

</td>
</tr>
<tr>
<td colspan="3">



 The `size` field is normally 0, but for pointer controls this should be set to the size of the memory that contains the payload or that will receive the payload. If [VIDIOC\_G\_EXT\_CTRLS](<#rst-vidioc-g-ext-ctrls>) finds that this value is less than is required to store the payload result, then it is set to a value large enough to store the payload result and `ENOSPC` is returned.

> [!NOTE]
>
> For string controls, this `size` field should not be confused with the length of the string. This field refers to the size of the memory that contains the string. The actual <em>length</em> of the string may well be much smaller.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`reserved2`\[1\]

</td>
<td>



Reserved for future extensions. Drivers and applications must set the array to zero.

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



\_\_s32

</td>
<td>



`value`

</td>
<td>



New value or current value. Valid if this control is not of type `V4L2_CTRL_TYPE_INTEGER64` and `V4L2_CTRL_FLAG_HAS_PAYLOAD` is not set.

</td>
</tr>
<tr>
<td>



\_\_s64

</td>
<td>



`value64`

</td>
<td>



New value or current value. Valid if this control is of type `V4L2_CTRL_TYPE_INTEGER64` and `V4L2_CTRL_FLAG_HAS_PAYLOAD` is not set.

</td>
</tr>
<tr>
<td>



char \*

</td>
<td>



`string`

</td>
<td>



A pointer to a string. Valid if this control is of type `V4L2_CTRL_TYPE_STRING`.

</td>
</tr>
<tr>
<td>



\_\_u8 \*

</td>
<td>



`p_u8`

</td>
<td>



A pointer to a matrix control of unsigned 8-bit values. Valid if this control is of type `V4L2_CTRL_TYPE_U8`.

</td>
</tr>
<tr>
<td>



\_\_u16 \*

</td>
<td>



`p_u16`

</td>
<td>



A pointer to a matrix control of unsigned 16-bit values. Valid if this control is of type `V4L2_CTRL_TYPE_U16`.

</td>
</tr>
<tr>
<td>



\_\_u32 \*

</td>
<td>



`p_u32`

</td>
<td>



A pointer to a matrix control of unsigned 32-bit values. Valid if this control is of type `V4L2_CTRL_TYPE_U32`.

</td>
</tr>
<tr>
<td>



\_\_s32 \*

</td>
<td>



`p_s32`

</td>
<td>



A pointer to a matrix control of signed 32-bit values. Valid if this control is of type `V4L2_CTRL_TYPE_INTEGER` and `V4L2_CTRL_FLAG_HAS_PAYLOAD` is set.

</td>
</tr>
<tr>
<td>



\_\_s64 \*

</td>
<td>



`p_s64`

</td>
<td>



A pointer to a matrix control of signed 64-bit values. Valid if this control is of type `V4L2_CTRL_TYPE_INTEGER64` and `V4L2_CTRL_FLAG_HAS_PAYLOAD` is set.

</td>
</tr>
<tr>
<td>



struct `v4l2_area` \*

</td>
<td>



`p_area`

</td>
<td>



A pointer to a struct `v4l2_area`. Valid if this control is of type `V4L2_CTRL_TYPE_AREA`.

</td>
</tr>
<tr>
<td>



struct `v4l2_rect` \*

</td>
<td>



`p_rect`

</td>
<td>



A pointer to a struct `v4l2_rect`. Valid if this control is of type `V4L2_CTRL_TYPE_RECT`.

</td>
</tr>
<tr>
<td>



struct `v4l2_ctrl_h264_sps` \*

</td>
<td>



`p_h264_sps`

</td>
<td>



A pointer to a struct `v4l2_ctrl_h264_sps`. Valid if this control is of type `V4L2_CTRL_TYPE_H264_SPS`.

</td>
</tr>
<tr>
<td>



struct `v4l2_ctrl_h264_pps` \*

</td>
<td>



`p_h264_pps`

</td>
<td>



A pointer to a struct `v4l2_ctrl_h264_pps`. Valid if this control is of type `V4L2_CTRL_TYPE_H264_PPS`.

</td>
</tr>
<tr>
<td>



struct `v4l2_ctrl_h264_scaling_matrix` \*

</td>
<td>



`p_h264_scaling_matrix`

</td>
<td>



A pointer to a struct `v4l2_ctrl_h264_scaling_matrix`. Valid if this control is of type `V4L2_CTRL_TYPE_H264_SCALING_MATRIX`.

</td>
</tr>
<tr>
<td>



struct `v4l2_ctrl_h264_pred_weights` \*

</td>
<td>



`p_h264_pred_weights`

</td>
<td>



A pointer to a struct `v4l2_ctrl_h264_pred_weights`. Valid if this control is of type `V4L2_CTRL_TYPE_H264_PRED_WEIGHTS`.

</td>
</tr>
<tr>
<td>



struct `v4l2_ctrl_h264_slice_params` \*

</td>
<td>



`p_h264_slice_params`

</td>
<td>



A pointer to a struct `v4l2_ctrl_h264_slice_params`. Valid if this control is of type `V4L2_CTRL_TYPE_H264_SLICE_PARAMS`.

</td>
</tr>
<tr>
<td>



struct `v4l2_ctrl_h264_decode_params` \*

</td>
<td>



`p_h264_decode_params`

</td>
<td>



A pointer to a struct `v4l2_ctrl_h264_decode_params`. Valid if this control is of type `V4L2_CTRL_TYPE_H264_DECODE_PARAMS`.

</td>
</tr>
<tr>
<td>



struct `v4l2_ctrl_fwht_params` \*

</td>
<td>



`p_fwht_params`

</td>
<td>



A pointer to a struct `v4l2_ctrl_fwht_params`. Valid if this control is of type `V4L2_CTRL_TYPE_FWHT_PARAMS`.

</td>
</tr>
<tr>
<td>



struct `v4l2_ctrl_vp8_frame` \*

</td>
<td>



`p_vp8_frame`

</td>
<td>



A pointer to a struct `v4l2_ctrl_vp8_frame`. Valid if this control is of type `V4L2_CTRL_TYPE_VP8_FRAME`.

</td>
</tr>
<tr>
<td>



struct `v4l2_ctrl_mpeg2_sequence` \*

</td>
<td>



`p_mpeg2_sequence`

</td>
<td>



A pointer to a struct `v4l2_ctrl_mpeg2_sequence`. Valid if this control is of type `V4L2_CTRL_TYPE_MPEG2_SEQUENCE`.

</td>
</tr>
<tr>
<td>



struct `v4l2_ctrl_mpeg2_picture` \*

</td>
<td>



`p_mpeg2_picture`

</td>
<td>



A pointer to a struct `v4l2_ctrl_mpeg2_picture`. Valid if this control is of type `V4L2_CTRL_TYPE_MPEG2_PICTURE`.

</td>
</tr>
<tr>
<td>



struct `v4l2_ctrl_mpeg2_quantisation` \*

</td>
<td>



`p_mpeg2_quantisation`

</td>
<td>



A pointer to a struct `v4l2_ctrl_mpeg2_quantisation`. Valid if this control is of type `V4L2_CTRL_TYPE_MPEG2_QUANTISATION`.

</td>
</tr>
<tr>
<td>



struct `v4l2_ctrl_vp9_compressed_hdr` \*

</td>
<td>



`p_vp9_compressed_hdr_probs`

</td>
<td>



A pointer to a struct `v4l2_ctrl_vp9_compressed_hdr`. Valid if this control is of type `V4L2_CTRL_TYPE_VP9_COMPRESSED_HDR`.

</td>
</tr>
<tr>
<td>



struct `v4l2_ctrl_vp9_frame` \*

</td>
<td>



`p_vp9_frame`

</td>
<td>



A pointer to a struct `v4l2_ctrl_vp9_frame`. Valid if this control is of type `V4L2_CTRL_TYPE_VP9_FRAME`.

</td>
</tr>
<tr>
<td>



struct `v4l2_ctrl_hdr10_cll_info` \*

</td>
<td>



`p_hdr10_cll`

</td>
<td>



A pointer to a struct `v4l2_ctrl_hdr10_cll_info`. Valid if this control is of type `V4L2_CTRL_TYPE_HDR10_CLL_INFO`.

</td>
</tr>
<tr>
<td>



struct `v4l2_ctrl_hdr10_mastering_display` \*

</td>
<td>



`p_hdr10_mastering`

</td>
<td>



A pointer to a struct `v4l2_ctrl_hdr10_mastering_display`. Valid if this control is of type `V4L2_CTRL_TYPE_HDR10_MASTERING_DISPLAY`.

</td>
</tr>
<tr>
<td>



struct `v4l2_ctrl_hevc_sps` \*

</td>
<td>



`p_hevc_sps`

</td>
<td>



A pointer to a struct `v4l2_ctrl_hevc_sps`. Valid if this control is of type `V4L2_CTRL_TYPE_HEVC_SPS`.

</td>
</tr>
<tr>
<td>



struct `v4l2_ctrl_hevc_pps` \*

</td>
<td>



`p_hevc_pps`

</td>
<td>



A pointer to a struct `v4l2_ctrl_hevc_pps`. Valid if this control is of type `V4L2_CTRL_TYPE_HEVC_PPS`.

</td>
</tr>
<tr>
<td>



struct `v4l2_ctrl_hevc_slice_params` \*

</td>
<td>



`p_hevc_slice_params`

</td>
<td>



A pointer to a struct `v4l2_ctrl_hevc_slice_params`. Valid if this control is of type `V4L2_CTRL_TYPE_HEVC_SLICE_PARAMS`.

</td>
</tr>
<tr>
<td>



struct `v4l2_ctrl_hevc_scaling_matrix` \*

</td>
<td>



`p_hevc_scaling_matrix`

</td>
<td>



A pointer to a struct `v4l2_ctrl_hevc_scaling_matrix`. Valid if this control is of type `V4L2_CTRL_TYPE_HEVC_SCALING_MATRIX`.

</td>
</tr>
<tr>
<td>



struct `v4l2_ctrl_hevc_decode_params` \*

</td>
<td>



`p_hevc_decode_params`

</td>
<td>



A pointer to a struct `v4l2_ctrl_hevc_decode_params`. Valid if this control is of type `V4L2_CTRL_TYPE_HEVC_DECODE_PARAMS`.

</td>
</tr>
<tr>
<td>



struct `v4l2_ctrl_av1_sequence` \*

</td>
<td>



`p_av1_sequence`

</td>
<td>



A pointer to a struct `v4l2_ctrl_av1_sequence`. Valid if this control is of type `V4L2_CTRL_TYPE_AV1_SEQUENCE`.

</td>
</tr>
<tr>
<td>



struct `v4l2_ctrl_av1_tile_group_entry` \*

</td>
<td>



`p_av1_tile_group_entry`

</td>
<td>



A pointer to a struct `v4l2_ctrl_av1_tile_group_entry`. Valid if this control is of type `V4L2_CTRL_TYPE_AV1_TILE_GROUP_ENTRY`.

</td>
</tr>
<tr>
<td>



struct `v4l2_ctrl_av1_frame` \*

</td>
<td>



`p_av1_frame`

</td>
<td>



A pointer to a struct `v4l2_ctrl_av1_frame`. Valid if this control is of type `V4L2_CTRL_TYPE_AV1_FRAME`.

</td>
</tr>
<tr>
<td>



struct `v4l2_ctrl_av1_film_grain` \*

</td>
<td>



`p_av1_film_grain`

</td>
<td>



A pointer to a struct `v4l2_ctrl_av1_film_grain`. Valid if this control is of type `V4L2_CTRL_TYPE_AV1_FILM_GRAIN`.

</td>
</tr>
<tr>
<td>



struct `v4l2_ctrl_hdr10_cll_info` \*

</td>
<td>



`p_hdr10_cll_info`

</td>
<td>



A pointer to a struct `v4l2_ctrl_hdr10_cll_info`. Valid if this control is of type `V4L2_CTRL_TYPE_HDR10_CLL_INFO`.

</td>
</tr>
<tr>
<td>



struct `v4l2_ctrl_hdr10_mastering_display` \*

</td>
<td>



`p_hdr10_mastering_display`

</td>
<td>



A pointer to a struct `v4l2_ctrl_hdr10_mastering_display`. Valid if this control is of type `V4L2_CTRL_TYPE_HDR10_MASTERING_DISPLAY`.

</td>
</tr>
<tr>
<td>



void \*

</td>
<td>



`ptr`

</td>
<td>



A pointer to a compound type which can be an N-dimensional array and/or a compound type (the control's type is &gt;= `V4L2_CTRL_COMPOUND_TYPES`). Valid if `V4L2_CTRL_FLAG_HAS_PAYLOAD` is set for this control.

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

<!-- Source LaTeX layout: \normalsize -->

<!-- tabularcolumns: |p{4.0cm}|p{2.5cm}|p{10.8cm}| -->

<a id="c-v4l2_ext_controls"></a>



```c
v4l2_ext_controls
```


<table>
<caption>

struct v4l2\_ext\_controls

</caption>
<tbody>
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



\_\_u32

</td>
<td>



`which`

</td>
<td>



Which value of the control to get/set/try.

</td>
</tr>
<tr>
<td colspan="3">



 `V4L2_CTRL_WHICH_CUR_VAL` will return the current value of the control, `V4L2_CTRL_WHICH_DEF_VAL` will return the default value of the control, `V4L2_CTRL_WHICH_MIN_VAL` will return the minimum value of the control, and `V4L2_CTRL_WHICH_MAX_VAL` will return the maximum value of the control. `V4L2_CTRL_WHICH_REQUEST_VAL` indicates that the control value has to be retrieved from a request or tried/set for a request. In that case the `request_fd` field contains the file descriptor of the request that should be used. If the device does not support requests, then `EACCES` will be returned.

When using `V4L2_CTRL_WHICH_DEF_VAL`, `V4L2_CTRL_WHICH_MIN_VAL` or `V4L2_CTRL_WHICH_MAX_VAL` be aware that you can only get the default/minimum/maximum value of the control, you cannot set or try it.

Whether a control supports querying the minimum and maximum values using `V4L2_CTRL_WHICH_MIN_VAL` and `V4L2_CTRL_WHICH_MAX_VAL` is indicated by the `V4L2_CTRL_FLAG_HAS_WHICH_MIN_MAX` flag. Most non-compound control types support this. For controls with compound types, the definition of minimum/maximum values are provided by the control documentation. If a compound control does not document the meaning of minimum/maximum value, then querying the minimum or maximum value will result in the error code -EINVAL.

For backwards compatibility you can also use a control class here (see [ctrl-class](<#rst-ctrl-class>)). In that case all controls have to belong to that control class. This usage is deprecated, instead just use `V4L2_CTRL_WHICH_CUR_VAL`. There are some very old drivers that do not yet support `V4L2_CTRL_WHICH_CUR_VAL` and that require a control class here. You can test for such drivers by setting `which` to `V4L2_CTRL_WHICH_CUR_VAL` and calling [VIDIOC\_TRY\_EXT\_CTRLS](<#rst-vidioc-g-ext-ctrls>) with a count of 0. If that fails, then the driver does not support `V4L2_CTRL_WHICH_CUR_VAL`.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`ctrl_class`

</td>
<td>



Deprecated name kept for backwards compatibility. Use `which` instead.

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



`count`

</td>
<td>



The number of controls in the controls array. May also be zero.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`error_idx`

</td>
<td>



Index of the failing control. Set by the driver in case of an error.

</td>
</tr>
<tr>
<td colspan="3">



 If the error is associated with a particular control, then `error_idx` is set to the index of that control. If the error is not related to a specific control, or the validation step failed (see below), then `error_idx` is set to `count`. The value is undefined if the ioctl returned 0 (success).

Before controls are read from/written to hardware a validation step takes place: this checks if all controls in the list are valid controls, if no attempt is made to write to a read-only control or read from a write-only control, and any other up-front checks that can be done without accessing the hardware. The exact validations done during this step are driver dependent since some checks might require hardware access for some devices, thus making it impossible to do those checks up-front. However, drivers should make a best-effort to do as many up-front checks as possible.

This check is done to avoid leaving the hardware in an inconsistent state due to easy-to-avoid problems. But it leads to another problem: the application needs to know whether an error came from the validation step (meaning that the hardware was not touched) or from an error during the actual reading from/writing to hardware.

The, in hindsight quite poor, solution for that is to set `error_idx` to `count` if the validation failed. This has the unfortunate side-effect that it is not possible to see which control failed the validation. If the validation was successful and the error happened while accessing the hardware, then `error_idx` is less than `count` and only the controls up to `error_idx-1` were read or written correctly, and the state of the remaining controls is undefined.

Since [VIDIOC\_TRY\_EXT\_CTRLS](<#rst-vidioc-g-ext-ctrls>) does not access hardware there is also no need to handle the validation step in this special way, so `error_idx` will just be set to the control that failed the validation step instead of to `count`. This means that if [VIDIOC\_S\_EXT\_CTRLS](<#rst-vidioc-g-ext-ctrls>) fails with `error_idx` set to `count`, then you can call [VIDIOC\_TRY\_EXT\_CTRLS](<#rst-vidioc-g-ext-ctrls>) to try to discover the actual control that failed the validation step. Unfortunately, there is no `TRY` equivalent for [VIDIOC\_G\_EXT\_CTRLS](<#rst-vidioc-g-ext-ctrls>).

</td>
</tr>
<tr>
<td>



\_\_s32

</td>
<td>



`request_fd`

</td>
<td>



File descriptor of the request to be used by this operation. Only valid if `which` is set to `V4L2_CTRL_WHICH_REQUEST_VAL`. If the device does not support requests, then `EACCES` will be returned. If requests are supported but an invalid request file descriptor is given, then `EINVAL` will be returned.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`reserved`\[1\]

</td>
<td>



Reserved for future extensions.

Drivers and applications must set the array to zero.

</td>
</tr>
<tr>
<td>



struct `v4l2_ext_control` \*

</td>
<td>



`controls`

</td>
<td>



Pointer to an array of `count` v4l2\_ext\_control structures.

Ignored if `count` equals zero.

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{7.3cm}|p{2.0cm}|p{8.0cm}| -->

<a id="rst-ctrl-class"></a>


<table>
<caption>

Control classes

</caption>
<tbody>
<tr>
<td>



`V4L2_CTRL_CLASS_USER`

</td>
<td>



0x980000

</td>
<td>



The class containing user controls. These controls are described in [control](<~kernel/userspace/userspace-api/media-v4l/control#rst-control>). All controls that can be set using the [VIDIOC\_S\_CTRL](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-ctrl#rst-vidioc-g-ctrl>) and [VIDIOC\_G\_CTRL](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-ctrl#rst-vidioc-g-ctrl>) ioctl belong to this class.

</td>
</tr>
<tr>
<td>



`V4L2_CTRL_CLASS_CODEC`

</td>
<td>



0x990000

</td>
<td>



The class containing stateful codec controls. These controls are described in [Codec Control Reference](<~kernel/userspace/userspace-api/media-v4l/ext-ctrls-codec#rst-codec-controls>).

</td>
</tr>
<tr>
<td>



`V4L2_CTRL_CLASS_CAMERA`

</td>
<td>



0x9a0000

</td>
<td>



The class containing camera controls. These controls are described in [Camera Control Reference](<~kernel/userspace/userspace-api/media-v4l/ext-ctrls-camera#rst-camera-controls>).

</td>
</tr>
<tr>
<td>



`V4L2_CTRL_CLASS_FM_TX`

</td>
<td>



0x9b0000

</td>
<td>



The class containing FM Transmitter (FM TX) controls. These controls are described in [fm-tx-controls](<~kernel/userspace/userspace-api/media-v4l/ext-ctrls-fm-tx#rst-fm-tx-controls>).

</td>
</tr>
<tr>
<td>



`V4L2_CTRL_CLASS_FLASH`

</td>
<td>



0x9c0000

</td>
<td>



The class containing flash device controls. These controls are described in [flash-controls](<~kernel/userspace/userspace-api/media-v4l/ext-ctrls-flash#rst-flash-controls>).

</td>
</tr>
<tr>
<td>



`V4L2_CTRL_CLASS_JPEG`

</td>
<td>



0x9d0000

</td>
<td>



The class containing JPEG compression controls. These controls are described in [jpeg-controls](<~kernel/userspace/userspace-api/media-v4l/ext-ctrls-jpeg#rst-jpeg-controls>).

</td>
</tr>
<tr>
<td>



`V4L2_CTRL_CLASS_IMAGE_SOURCE`

</td>
<td>



0x9e0000

</td>
<td>



The class containing image source controls. These controls are described in [image-source-controls](<~kernel/userspace/userspace-api/media-v4l/ext-ctrls-image-source#rst-image-source-controls>).

</td>
</tr>
<tr>
<td>



`V4L2_CTRL_CLASS_IMAGE_PROC`

</td>
<td>



0x9f0000

</td>
<td>



The class containing image processing controls. These controls are described in [image-process-controls](<~kernel/userspace/userspace-api/media-v4l/ext-ctrls-image-process#rst-image-process-controls>).

</td>
</tr>
<tr>
<td>



`V4L2_CTRL_CLASS_FM_RX`

</td>
<td>



0xa10000

</td>
<td>



The class containing FM Receiver (FM RX) controls. These controls are described in [fm-rx-controls](<~kernel/userspace/userspace-api/media-v4l/ext-ctrls-fm-rx#rst-fm-rx-controls>).

</td>
</tr>
<tr>
<td>



`V4L2_CTRL_CLASS_RF_TUNER`

</td>
<td>



0xa20000

</td>
<td>



The class containing RF tuner controls. These controls are described in [rf-tuner-controls](<~kernel/userspace/userspace-api/media-v4l/ext-ctrls-rf-tuner#rst-rf-tuner-controls>).

</td>
</tr>
<tr>
<td>



`V4L2_CTRL_CLASS_DETECT`

</td>
<td>



0xa30000

</td>
<td>



The class containing motion or object detection controls. These controls are described in [detect-controls](<~kernel/userspace/userspace-api/media-v4l/ext-ctrls-detect#rst-detect-controls>).

</td>
</tr>
<tr>
<td>



`V4L2_CTRL_CLASS_CODEC_STATELESS`

</td>
<td>



0xa40000

</td>
<td>



The class containing stateless codec controls. These controls are described in [Stateless Codec Control Reference](<~kernel/userspace/userspace-api/media-v4l/ext-ctrls-codec-stateless#rst-codec-stateless-controls>).

</td>
</tr>
<tr>
<td>



`V4L2_CTRL_CLASS_COLORIMETRY`

</td>
<td>



0xa50000

</td>
<td>



The class containing colorimetry controls. These controls are described in [colorimetry-controls](<~kernel/userspace/userspace-api/media-v4l/ext-ctrls-colorimetry#rst-colorimetry-controls>).

</td>
</tr>
</tbody>
</table>

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

- **EINVAL**

  The struct `v4l2_ext_control` `id` is invalid, or the struct `v4l2_ext_controls` `which` is invalid, or the struct `v4l2_ext_control` `value` was inappropriate (e.g. the given menu index is not supported by the driver), or the `which` field was set to `V4L2_CTRL_WHICH_REQUEST_VAL` but the given `request_fd` was invalid or `V4L2_CTRL_WHICH_REQUEST_VAL` is not supported by the kernel. This error code is also returned by the [VIDIOC\_S\_EXT\_CTRLS](<#rst-vidioc-g-ext-ctrls>) and [VIDIOC\_TRY\_EXT\_CTRLS](<#rst-vidioc-g-ext-ctrls>) ioctls if two or more control values are in conflict.

- **ERANGE**

  The struct `v4l2_ext_control` `value` is out of bounds.

- **EBUSY**

  The control is temporarily not changeable, possibly because another applications took over control of the device function this control belongs to, or (if the `which` field was set to `V4L2_CTRL_WHICH_REQUEST_VAL`) the request was queued but not yet completed.

- **ENOSPC**

  The space reserved for the control's payload is insufficient. The field `size` is set to a value that is enough to store the payload and this error code is returned.

- **EACCES**

  Attempt to try or set a read-only control, or to get a write-only control, or to get a control from a request that has not yet been completed.

  Or the `which` field was set to `V4L2_CTRL_WHICH_REQUEST_VAL` but the device does not support requests.

  Or if there is an attempt to set an inactive control and the driver is not capable of caching the new value until the control is active again.
