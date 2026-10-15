---
title: "Stateless Codec Control Reference"
type: reference
description: "The Stateless Codec control class is intended to support stateless decoder and encoders (i.e. hardware accelerators)."
---

<a id="rst-stateless-codec-control-reference"></a>
<a id="rst-codec-stateless-controls"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

The Stateless Codec control class is intended to support stateless decoder and encoders (i.e. hardware accelerators).

These drivers are typically supported by the [stateless\_decoder](<~kernel/userspace/userspace-api/media-v4l/dev-stateless-decoder#rst-stateless-decoder>), and deal with parsed pixel formats such as V4L2\_PIX\_FMT\_H264\_SLICE.

<a id="rst-stateless-codec-control-id"></a>

## Stateless Codec Control ID

<a id="rst-codec-stateless-control-id"></a>

- **`V4L2_CID_CODEC_STATELESS_CLASS (class)`**

  The Stateless Codec class descriptor.

<a id="rst-v4l2-codec-stateless-h264"></a>

- **`V4L2_CID_STATELESS_H264_SPS (struct)`**

  Specifies the sequence parameter set (as extracted from the bitstream) for the associated H264 slice data. This includes the necessary parameters for configuring a stateless hardware decoding pipeline for H264. The bitstream parameters are defined according to [h264](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-h264>), section 7.4.2.1.1 "Sequence Parameter Set Data Semantics". For further documentation, refer to the above specification, unless there is an explicit comment stating otherwise.

<a id="c-v4l2_ctrl_h264_sps"></a>



```c
v4l2_ctrl_h264_sps
```

<!-- Source LaTeX layout: \small -->

<!-- tabularcolumns: |p{1.2cm}|p{8.6cm}|p{7.5cm}| -->


<table>
<caption>

struct v4l2\_ctrl\_h264\_sps

</caption>
<tbody>
<tr>
<td>



\_\_u8

</td>
<td>



`profile_idc`

</td>
<td>





</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`constraint_set_flags`

</td>
<td>



See [Sequence Parameter Set Constraints Set Flags](<#rst-h264-sps-constraints-set-flags>)

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`level_idc`

</td>
<td>





</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`seq_parameter_set_id`

</td>
<td>





</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`chroma_format_idc`

</td>
<td>





</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`bit_depth_luma_minus8`

</td>
<td>





</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`bit_depth_chroma_minus8`

</td>
<td>





</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`log2_max_frame_num_minus4`

</td>
<td>





</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`pic_order_cnt_type`

</td>
<td>





</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`log2_max_pic_order_cnt_lsb_minus4`

</td>
<td>





</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`max_num_ref_frames`

</td>
<td>





</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`num_ref_frames_in_pic_order_cnt_cycle`

</td>
<td>





</td>
</tr>
<tr>
<td>



\_\_s32

</td>
<td>



`offset_for_ref_frame[255]`

</td>
<td>





</td>
</tr>
<tr>
<td>



\_\_s32

</td>
<td>



`offset_for_non_ref_pic`

</td>
<td>





</td>
</tr>
<tr>
<td>



\_\_s32

</td>
<td>



`offset_for_top_to_bottom_field`

</td>
<td>





</td>
</tr>
<tr>
<td>



\_\_u16

</td>
<td>



`pic_width_in_mbs_minus1`

</td>
<td>





</td>
</tr>
<tr>
<td>



\_\_u16

</td>
<td>



`pic_height_in_map_units_minus1`

</td>
<td>





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



See [Sequence Parameter Set Flags](<#rst-h264-sps-flags>)

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

<a id="rst-h264-sps-constraints-set-flags"></a>

`Sequence Parameter Set Constraints Set Flags`


<table>
<tbody>
<tr>
<td>



`V4L2_H264_SPS_CONSTRAINT_SET0_FLAG`

</td>
<td>



0x00000001

</td>
<td>





</td>
</tr>
<tr>
<td>



`V4L2_H264_SPS_CONSTRAINT_SET1_FLAG`

</td>
<td>



0x00000002

</td>
<td>





</td>
</tr>
<tr>
<td>



`V4L2_H264_SPS_CONSTRAINT_SET2_FLAG`

</td>
<td>



0x00000004

</td>
<td>





</td>
</tr>
<tr>
<td>



`V4L2_H264_SPS_CONSTRAINT_SET3_FLAG`

</td>
<td>



0x00000008

</td>
<td>





</td>
</tr>
<tr>
<td>



`V4L2_H264_SPS_CONSTRAINT_SET4_FLAG`

</td>
<td>



0x00000010

</td>
<td>





</td>
</tr>
<tr>
<td>



`V4L2_H264_SPS_CONSTRAINT_SET5_FLAG`

</td>
<td>



0x00000020

</td>
<td>





</td>
</tr>
</tbody>
</table>

<a id="rst-h264-sps-flags"></a>

`Sequence Parameter Set Flags`


<table>
<tbody>
<tr>
<td>



`V4L2_H264_SPS_FLAG_SEPARATE_COLOUR_PLANE`

</td>
<td>



0x00000001

</td>
<td>





</td>
</tr>
<tr>
<td>



`V4L2_H264_SPS_FLAG_QPPRIME_Y_ZERO_TRANSFORM_BYPASS`

</td>
<td>



0x00000002

</td>
<td>





</td>
</tr>
<tr>
<td>



`V4L2_H264_SPS_FLAG_DELTA_PIC_ORDER_ALWAYS_ZERO`

</td>
<td>



0x00000004

</td>
<td>





</td>
</tr>
<tr>
<td>



`V4L2_H264_SPS_FLAG_GAPS_IN_FRAME_NUM_VALUE_ALLOWED`

</td>
<td>



0x00000008

</td>
<td>





</td>
</tr>
<tr>
<td>



`V4L2_H264_SPS_FLAG_FRAME_MBS_ONLY`

</td>
<td>



0x00000010

</td>
<td>





</td>
</tr>
<tr>
<td>



`V4L2_H264_SPS_FLAG_MB_ADAPTIVE_FRAME_FIELD`

</td>
<td>



0x00000020

</td>
<td>





</td>
</tr>
<tr>
<td>



`V4L2_H264_SPS_FLAG_DIRECT_8X8_INFERENCE`

</td>
<td>



0x00000040

</td>
<td>





</td>
</tr>
</tbody>
</table>

- **`V4L2_CID_STATELESS_H264_PPS (struct)`**

  Specifies the picture parameter set (as extracted from the bitstream) for the associated H264 slice data. This includes the necessary parameters for configuring a stateless hardware decoding pipeline for H264.  The bitstream parameters are defined according to [h264](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-h264>), section 7.4.2.2 "Picture Parameter Set RBSP Semantics". For further documentation, refer to the above specification, unless there is an explicit comment stating otherwise.

<a id="c-v4l2_ctrl_h264_pps"></a>



```c
v4l2_ctrl_h264_pps
```

<!-- Source LaTeX layout: \small -->


<table>
<caption>

struct v4l2\_ctrl\_h264\_pps

</caption>
<tbody>
<tr>
<td>



\_\_u8

</td>
<td>



`pic_parameter_set_id`

</td>
<td>





</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`seq_parameter_set_id`

</td>
<td>





</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`num_slice_groups_minus1`

</td>
<td>





</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`num_ref_idx_l0_default_active_minus1`

</td>
<td>





</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`num_ref_idx_l1_default_active_minus1`

</td>
<td>





</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`weighted_bipred_idc`

</td>
<td>





</td>
</tr>
<tr>
<td>



\_\_s8

</td>
<td>



`pic_init_qp_minus26`

</td>
<td>





</td>
</tr>
<tr>
<td>



\_\_s8

</td>
<td>



`pic_init_qs_minus26`

</td>
<td>





</td>
</tr>
<tr>
<td>



\_\_s8

</td>
<td>



`chroma_qp_index_offset`

</td>
<td>





</td>
</tr>
<tr>
<td>



\_\_s8

</td>
<td>



`second_chroma_qp_index_offset`

</td>
<td>





</td>
</tr>
<tr>
<td>



\_\_u16

</td>
<td>



`flags`

</td>
<td>



See [Picture Parameter Set Flags](<#rst-h264-pps-flags>)

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

<a id="rst-h264-pps-flags"></a>

`Picture Parameter Set Flags`

<!-- Source LaTeX layout: \begingroup
\scriptsize
\setlength{\tabcolsep}{2pt} -->

<!-- tabularcolumns: |p{9.8cm}|p{1.0cm}|p{6.5cm}| -->


<table>
<tbody>
<tr>
<td>



`V4L2_H264_PPS_FLAG_ENTROPY_CODING_MODE`

</td>
<td>



0x0001

</td>
<td>





</td>
</tr>
<tr>
<td>



`V4L2_H264_PPS_FLAG_BOTTOM_FIELD_PIC_ORDER_IN_FRAME_PRESENT`

</td>
<td>



0x0002

</td>
<td>





</td>
</tr>
<tr>
<td>



`V4L2_H264_PPS_FLAG_WEIGHTED_PRED`

</td>
<td>



0x0004

</td>
<td>





</td>
</tr>
<tr>
<td>



`V4L2_H264_PPS_FLAG_DEBLOCKING_FILTER_CONTROL_PRESENT`

</td>
<td>



0x0008

</td>
<td>





</td>
</tr>
<tr>
<td>



`V4L2_H264_PPS_FLAG_CONSTRAINED_INTRA_PRED`

</td>
<td>



0x0010

</td>
<td>





</td>
</tr>
<tr>
<td>



`V4L2_H264_PPS_FLAG_REDUNDANT_PIC_CNT_PRESENT`

</td>
<td>



0x0020

</td>
<td>





</td>
</tr>
<tr>
<td>



`V4L2_H264_PPS_FLAG_TRANSFORM_8X8_MODE`

</td>
<td>



0x0040

</td>
<td>





</td>
</tr>
<tr>
<td>



`V4L2_H264_PPS_FLAG_SCALING_MATRIX_PRESENT`

</td>
<td>



0x0080

</td>
<td>



`V4L2_CID_STATELESS_H264_SCALING_MATRIX` must be used for this picture.

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \endgroup -->

- **`V4L2_CID_STATELESS_H264_SCALING_MATRIX (struct)`**

  Specifies the scaling matrix (as extracted from the bitstream) for the associated H264 slice data. The bitstream parameters are defined according to [h264](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-h264>), section 7.4.2.1.1.1 "Scaling List Semantics". For further documentation, refer to the above specification, unless there is an explicit comment stating otherwise.

<a id="c-v4l2_ctrl_h264_scaling_matrix"></a>



```c
v4l2_ctrl_h264_scaling_matrix
```

<!-- Source LaTeX layout: \small -->

<!-- tabularcolumns: |p{0.6cm}|p{4.8cm}|p{11.9cm}| -->


<table>
<caption>

struct v4l2\_ctrl\_h264\_scaling\_matrix

</caption>
<tbody>
<tr>
<td>



\_\_u8

</td>
<td>



`scaling_list_4x4[6][16]`

</td>
<td>



Scaling matrix after applying the inverse scanning process. Expected list order is Intra Y, Intra Cb, Intra Cr, Inter Y, Inter Cb, Inter Cr. The values on each scaling list are expected in raster scan order.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`scaling_list_8x8[6][64]`

</td>
<td>



Scaling matrix after applying the inverse scanning process. Expected list order is Intra Y, Inter Y, Intra Cb, Inter Cb, Intra Cr, Inter Cr. The values on each scaling list are expected in raster scan order.

</td>
</tr>
</tbody>
</table>

- **`V4L2_CID_STATELESS_H264_SLICE_PARAMS (struct)`**

  Specifies the slice parameters (as extracted from the bitstream) for the associated H264 slice data. This includes the necessary parameters for configuring a stateless hardware decoding pipeline for H264.  The bitstream parameters are defined according to [h264](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-h264>), section 7.4.3 "Slice Header Semantics". For further documentation, refer to the above specification, unless there is an explicit comment stating otherwise.

<a id="c-v4l2_ctrl_h264_slice_params"></a>



```c
v4l2_ctrl_h264_slice_params
```

<!-- Source LaTeX layout: \small -->

<!-- tabularcolumns: |p{4.0cm}|p{5.9cm}|p{7.4cm}| -->


<table>
<caption>

struct v4l2\_ctrl\_h264\_slice\_params

</caption>
<tbody>
<tr>
<td>



\_\_u32

</td>
<td>



`header_bit_size`

</td>
<td>



Offset in bits to slice\_data() from the beginning of this slice.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`first_mb_in_slice`

</td>
<td>





</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`slice_type`

</td>
<td>





</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`colour_plane_id`

</td>
<td>





</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`redundant_pic_cnt`

</td>
<td>





</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`cabac_init_idc`

</td>
<td>





</td>
</tr>
<tr>
<td>



\_\_s8

</td>
<td>



`slice_qp_delta`

</td>
<td>





</td>
</tr>
<tr>
<td>



\_\_s8

</td>
<td>



`slice_qs_delta`

</td>
<td>





</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`disable_deblocking_filter_idc`

</td>
<td>





</td>
</tr>
<tr>
<td>



\_\_s8

</td>
<td>



`slice_alpha_c0_offset_div2`

</td>
<td>





</td>
</tr>
<tr>
<td>



\_\_s8

</td>
<td>



`slice_beta_offset_div2`

</td>
<td>





</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`num_ref_idx_l0_active_minus1`

</td>
<td>



If num\_ref\_idx\_active\_override\_flag is not set, this field must be set to the value of num\_ref\_idx\_l0\_default\_active\_minus1

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`num_ref_idx_l1_active_minus1`

</td>
<td>



If num\_ref\_idx\_active\_override\_flag is not set, this field must be set to the value of num\_ref\_idx\_l1\_default\_active\_minus1

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`reserved`

</td>
<td>



Applications and drivers must set this to zero.

</td>
</tr>
<tr>
<td>



struct `v4l2_h264_reference`

</td>
<td>



`ref_pic_list0[32]`

</td>
<td>



Reference picture list after applying the per-slice modifications

</td>
</tr>
<tr>
<td>



struct `v4l2_h264_reference`

</td>
<td>



`ref_pic_list1[32]`

</td>
<td>



Reference picture list after applying the per-slice modifications

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



See [Slice Parameter Flags](<#rst-h264-slice-flags>)

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

<a id="rst-h264-slice-flags"></a>

`Slice Parameter Set Flags`


<table>
<tbody>
<tr>
<td>



`V4L2_H264_SLICE_FLAG_DIRECT_SPATIAL_MV_PRED`

</td>
<td>



0x00000001

</td>
<td>





</td>
</tr>
<tr>
<td>



`V4L2_H264_SLICE_FLAG_SP_FOR_SWITCH`

</td>
<td>



0x00000002

</td>
<td>





</td>
</tr>
</tbody>
</table>

- **`V4L2_CID_STATELESS_H264_PRED_WEIGHTS (struct)`**

  Prediction weight table defined according to [h264](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-h264>), section 7.4.3.2 "Prediction Weight Table Semantics". The prediction weight table must be passed by applications under the conditions explained in section 7.3.3 "Slice header syntax".

<a id="c-v4l2_ctrl_h264_pred_weights"></a>



```c
v4l2_ctrl_h264_pred_weights
```

<!-- Source LaTeX layout: \small -->

<!-- tabularcolumns: |p{4.9cm}|p{4.9cm}|p{7.5cm}| -->


<table>
<caption>

struct v4l2\_ctrl\_h264\_pred\_weights

</caption>
<tbody>
<tr>
<td>



\_\_u16

</td>
<td>



`luma_log2_weight_denom`

</td>
<td>





</td>
</tr>
<tr>
<td>



\_\_u16

</td>
<td>



`chroma_log2_weight_denom`

</td>
<td>





</td>
</tr>
<tr>
<td>



struct `v4l2_h264_weight_factors`

</td>
<td>



`weight_factors[2]`

</td>
<td>



The weight factors at index 0 are the weight factors for the reference list 0, the one at index 1 for the reference list 1.

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

<a id="c-v4l2_h264_weight_factors"></a>



```c
v4l2_h264_weight_factors
```

<!-- Source LaTeX layout: \small -->

<!-- tabularcolumns: |p{1.0cm}|p{4.5cm}|p{11.8cm}| -->


<table>
<caption>

struct v4l2\_h264\_weight\_factors

</caption>
<tbody>
<tr>
<td>



\_\_s16

</td>
<td>



`luma_weight[32]`

</td>
<td>





</td>
</tr>
<tr>
<td>



\_\_s16

</td>
<td>



`luma_offset[32]`

</td>
<td>





</td>
</tr>
<tr>
<td>



\_\_s16

</td>
<td>



`chroma_weight[32][2]`

</td>
<td>





</td>
</tr>
<tr>
<td>



\_\_s16

</td>
<td>



`chroma_offset[32][2]`

</td>
<td>





</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

`Picture Reference`

<a id="c-v4l2_h264_reference"></a>



```c
v4l2_h264_reference
```


<table>
<caption>

struct v4l2\_h264\_reference

</caption>
<tbody>
<tr>
<td>



\_\_u8

</td>
<td>



`fields`

</td>
<td>



Specifies how the picture is referenced. See [Reference Fields](<#rst-h264-ref-fields>)

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`index`

</td>
<td>



Index into the `v4l2_ctrl_h264_decode_params`.dpb array.

</td>
</tr>
</tbody>
</table>

<a id="rst-h264-ref-fields"></a>

`Reference Fields`

<!-- Source LaTeX layout: \small -->

<!-- tabularcolumns: |p{5.4cm}|p{0.8cm}|p{11.1cm}| -->


<table>
<tbody>
<tr>
<td>



`V4L2_H264_TOP_FIELD_REF`

</td>
<td>



0x1

</td>
<td>



The top field in field pair is used for short-term reference.

</td>
</tr>
<tr>
<td>



`V4L2_H264_BOTTOM_FIELD_REF`

</td>
<td>



0x2

</td>
<td>



The bottom field in field pair is used for short-term reference.

</td>
</tr>
<tr>
<td>



`V4L2_H264_FRAME_REF`

</td>
<td>



0x3

</td>
<td>



The frame (or the top/bottom fields, if it's a field pair) is used for short-term reference.

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

- **`V4L2_CID_STATELESS_H264_DECODE_PARAMS (struct)`**

  Specifies the decode parameters (as extracted from the bitstream) for the associated H264 slice data. This includes the necessary parameters for configuring a stateless hardware decoding pipeline for H264. The bitstream parameters are defined according to [h264](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-h264>). For further documentation, refer to the above specification, unless there is an explicit comment stating otherwise.

<a id="c-v4l2_ctrl_h264_decode_params"></a>



```c
v4l2_ctrl_h264_decode_params
```

<!-- Source LaTeX layout: \small -->

<!-- tabularcolumns: |p{4.0cm}|p{5.9cm}|p{7.4cm}| -->


<table>
<caption>

struct v4l2\_ctrl\_h264\_decode\_params

</caption>
<tbody>
<tr>
<td>



struct `v4l2_h264_dpb_entry`

</td>
<td>



`dpb[16]`

</td>
<td>





</td>
</tr>
<tr>
<td>



\_\_u16

</td>
<td>



`nal_ref_idc`

</td>
<td>



NAL reference ID value coming from the NAL Unit header

</td>
</tr>
<tr>
<td>



\_\_u16

</td>
<td>



`frame_num`

</td>
<td>





</td>
</tr>
<tr>
<td>



\_\_s32

</td>
<td>



`top_field_order_cnt`

</td>
<td>



Picture Order Count for the coded top field

</td>
</tr>
<tr>
<td>



\_\_s32

</td>
<td>



`bottom_field_order_cnt`

</td>
<td>



Picture Order Count for the coded bottom field

</td>
</tr>
<tr>
<td>



\_\_u16

</td>
<td>



`idr_pic_id`

</td>
<td>





</td>
</tr>
<tr>
<td>



\_\_u16

</td>
<td>



`pic_order_cnt_lsb`

</td>
<td>





</td>
</tr>
<tr>
<td>



\_\_s32

</td>
<td>



`delta_pic_order_cnt_bottom`

</td>
<td>





</td>
</tr>
<tr>
<td>



\_\_s32

</td>
<td>



`delta_pic_order_cnt0`

</td>
<td>





</td>
</tr>
<tr>
<td>



\_\_s32

</td>
<td>



`delta_pic_order_cnt1`

</td>
<td>





</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`dec_ref_pic_marking_bit_size`

</td>
<td>



Size in bits of the dec\_ref\_pic\_marking() syntax element.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`pic_order_cnt_bit_size`

</td>
<td>



Combined size in bits of the picture order count related syntax elements: pic\_order\_cnt\_lsb, delta\_pic\_order\_cnt\_bottom, delta\_pic\_order\_cnt0, and delta\_pic\_order\_cnt1.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`slice_group_change_cycle`

</td>
<td>





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



Applications and drivers must set this to zero.

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



See [Decode Parameters Flags](<#rst-h264-decode-params-flags>)

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

<a id="rst-h264-decode-params-flags"></a>

`Decode Parameters Flags`

<!-- Source LaTeX layout: \small -->

<!-- tabularcolumns: |p{8.3cm}|p{2.1cm}|p{6.9cm}| -->


<table>
<tbody>
<tr>
<td>



`V4L2_H264_DECODE_PARAM_FLAG_IDR_PIC`

</td>
<td>



0x00000001

</td>
<td>



That picture is an IDR picture

</td>
</tr>
<tr>
<td>



`V4L2_H264_DECODE_PARAM_FLAG_FIELD_PIC`

</td>
<td>



0x00000002

</td>
<td>





</td>
</tr>
<tr>
<td>



`V4L2_H264_DECODE_PARAM_FLAG_BOTTOM_FIELD`

</td>
<td>



0x00000004

</td>
<td>





</td>
</tr>
<tr>
<td>



`V4L2_H264_DECODE_PARAM_FLAG_PFRAME`

</td>
<td>



0x00000008

</td>
<td>





</td>
</tr>
<tr>
<td>



`V4L2_H264_DECODE_PARAM_FLAG_BFRAME`

</td>
<td>



0x00000010

</td>
<td>





</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

<a id="c-v4l2_h264_dpb_entry"></a>



```c
v4l2_h264_dpb_entry
```

<!-- Source LaTeX layout: \small -->

<!-- tabularcolumns: |p{1.0cm}|p{4.9cm}|p{11.4cm}| -->


<table>
<caption>

struct v4l2\_h264\_dpb\_entry

</caption>
<tbody>
<tr>
<td>



\_\_u64

</td>
<td>



`reference_ts`

</td>
<td>



Timestamp of the V4L2 capture buffer to use as reference, used with B-coded and P-coded frames. The timestamp refers to the `timestamp` field in struct `v4l2_buffer`. Use the `v4l2_timeval_to_ns()` function to convert the struct `timeval` in struct `v4l2_buffer` to a \_\_u64.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`pic_num`

</td>
<td>



For short term references, this must match the derived value PicNum (8-28) and for long term references it must match the derived value LongTermPicNum (8-29). When decoding frames (as opposed to fields) pic\_num is the same as FrameNumWrap.

</td>
</tr>
<tr>
<td>



\_\_u16

</td>
<td>



`frame_num`

</td>
<td>



For short term references, this must match the frame\_num value from the slice header syntax (the driver will wrap the value if needed). For long term references, this must be set to the value of long\_term\_frame\_idx described in the dec\_ref\_pic\_marking() syntax.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`fields`

</td>
<td>



Specifies how the DPB entry is referenced. See [Reference Fields](<#rst-h264-ref-fields>)

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`reserved[5]`

</td>
<td>



Applications and drivers must set this to zero.

</td>
</tr>
<tr>
<td>



\_\_s32

</td>
<td>



`top_field_order_cnt`

</td>
<td>





</td>
</tr>
<tr>
<td>



\_\_s32

</td>
<td>



`bottom_field_order_cnt`

</td>
<td>





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



See [DPB Entry Flags](<#rst-h264-dpb-flags>)

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

<a id="rst-h264-dpb-flags"></a>

`DPB Entries Flags`

<!-- Source LaTeX layout: \small -->

<!-- tabularcolumns: |p{7.7cm}|p{2.1cm}|p{7.5cm}| -->


<table>
<tbody>
<tr>
<td>



`V4L2_H264_DPB_ENTRY_FLAG_VALID`

</td>
<td>



0x00000001

</td>
<td>



The DPB entry is valid (non-empty) and should be considered.

</td>
</tr>
<tr>
<td>



`V4L2_H264_DPB_ENTRY_FLAG_ACTIVE`

</td>
<td>



0x00000002

</td>
<td>



The DPB entry is used for reference.

</td>
</tr>
<tr>
<td>



`V4L2_H264_DPB_ENTRY_FLAG_LONG_TERM`

</td>
<td>



0x00000004

</td>
<td>



The DPB entry is used for long-term reference.

</td>
</tr>
<tr>
<td>



`V4L2_H264_DPB_ENTRY_FLAG_FIELD`

</td>
<td>



0x00000008

</td>
<td>



The DPB entry is a single field or a complementary field pair.

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

- **`V4L2_CID_STATELESS_H264_DECODE_MODE (enum)`**

  Specifies the decoding mode to use. Currently exposes slice-based and frame-based decoding but new modes might be added later on. This control is used as a modifier for V4L2\_PIX\_FMT\_H264\_SLICE pixel format. Applications that support V4L2\_PIX\_FMT\_H264\_SLICE are required to set this control in order to specify the decoding mode that is expected for the buffer. Drivers may expose a single or multiple decoding modes, depending on what they can support.

<a id="c-v4l2_stateless_h264_decode_mode"></a>



```c
v4l2_stateless_h264_decode_mode
```

<!-- Source LaTeX layout: \scriptsize -->

<!-- tabularcolumns: |p{7.4cm}|p{0.3cm}|p{9.6cm}| -->


<table>
<tbody>
<tr>
<td>



`V4L2_STATELESS_H264_DECODE_MODE_SLICE_BASED`

</td>
<td>



0

</td>
<td>



Decoding is done at the slice granularity. The OUTPUT buffer must contain a single slice. When this mode is selected, the `V4L2_CID_STATELESS_H264_SLICE_PARAMS` control shall be set. When multiple slices compose a frame, use of `V4L2_BUF_CAP_SUPPORTS_M2M_HOLD_CAPTURE_BUF` flag is required.

</td>
</tr>
<tr>
<td>



`V4L2_STATELESS_H264_DECODE_MODE_FRAME_BASED`

</td>
<td>



1

</td>
<td>



Decoding is done at the frame granularity, The OUTPUT buffer must contain all slices needed to decode the frame. The OUTPUT buffer must also contain both fields. This mode will be supported by devices that parse the slice(s) header(s) in hardware. When this mode is selected, the `V4L2_CID_STATELESS_H264_SLICE_PARAMS` control shall not be set.

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

- **`V4L2_CID_STATELESS_H264_START_CODE (enum)`**

  Specifies the H264 slice start code expected for each slice. This control is used as a modifier for V4L2\_PIX\_FMT\_H264\_SLICE pixel format. Applications that support V4L2\_PIX\_FMT\_H264\_SLICE are required to set this control in order to specify the start code that is expected for the buffer. Drivers may expose a single or multiple start codes, depending on what they can support.

<a id="c-v4l2_stateless_h264_start_code"></a>



```c
v4l2_stateless_h264_start_code
```

<!-- Source LaTeX layout: \small -->

<!-- tabularcolumns: |p{7.9cm}|p{0.4cm}|p{9.0cm}| -->


<table>
<tbody>
<tr>
<td>



`V4L2_STATELESS_H264_START_CODE_NONE`

</td>
<td>



0

</td>
<td>



Selecting this value specifies that H264 slices are passed to the driver without any start code. The bitstream data should be according to [h264](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-h264>) 7.3.1 NAL unit syntax, hence contains emulation prevention bytes when required.

</td>
</tr>
<tr>
<td>



`V4L2_STATELESS_H264_START_CODE_ANNEX_B`

</td>
<td>



1

</td>
<td>



Selecting this value specifies that H264 slices are expected to be prefixed by Annex B start codes. According to [h264](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-h264>) valid start codes can be 3-bytes 0x000001 or 4-bytes 0x00000001.

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

<a id="rst-codec-stateless-fwht"></a>

- **`V4L2_CID_STATELESS_FWHT_PARAMS (struct)`**

  Specifies the FWHT (Fast Walsh Hadamard Transform) parameters (as extracted from the bitstream) for the associated FWHT data. This includes the necessary parameters for configuring a stateless hardware decoding pipeline for FWHT. This codec is specific to the vicodec test driver.

<a id="c-v4l2_ctrl_fwht_params"></a>



```c
v4l2_ctrl_fwht_params
```

<!-- Source LaTeX layout: \small -->

<!-- tabularcolumns: |p{1.4cm}|p{3.9cm}|p{12.0cm}| -->


<table>
<caption>

struct v4l2\_ctrl\_fwht\_params

</caption>
<tbody>
<tr>
<td>



\_\_u64

</td>
<td>



`backward_ref_ts`

</td>
<td>



Timestamp of the V4L2 capture buffer to use as backward reference, used with P-coded frames. The timestamp refers to the `timestamp` field in struct `v4l2_buffer`. Use the `v4l2_timeval_to_ns()` function to convert the struct `timeval` in struct `v4l2_buffer` to a \_\_u64.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`version`

</td>
<td>



The version of the codec. Set to `V4L2_FWHT_VERSION`.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`width`

</td>
<td>



The width of the frame.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`height`

</td>
<td>



The height of the frame.

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



The flags of the frame, see [FWHT Flags](<#rst-fwht-flags>).

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`colorspace`

</td>
<td>



The colorspace of the frame, from enum `v4l2_colorspace`.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`xfer_func`

</td>
<td>



The transfer function, from enum `v4l2_xfer_func`.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`ycbcr_enc`

</td>
<td>



The Y'CbCr encoding, from enum `v4l2_ycbcr_encoding`.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`quantization`

</td>
<td>



The quantization range, from enum `v4l2_quantization`.

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

<a id="rst-fwht-flags-1"></a>
<a id="rst-fwht-flags"></a>

## FWHT Flags

<!-- Source LaTeX layout: \small -->

<!-- tabularcolumns: |p{7.0cm}|p{2.3cm}|p{8.0cm}| -->


<table>
<tbody>
<tr>
<td>



`V4L2_FWHT_FL_IS_INTERLACED`

</td>
<td>



0x00000001

</td>
<td>



Set if this is an interlaced format.

</td>
</tr>
<tr>
<td>



`V4L2_FWHT_FL_IS_BOTTOM_FIRST`

</td>
<td>



0x00000002

</td>
<td>



Set if this is a bottom-first (NTSC) interlaced format.

</td>
</tr>
<tr>
<td>



`V4L2_FWHT_FL_IS_ALTERNATE`

</td>
<td>



0x00000004

</td>
<td>



Set if each 'frame' contains just one field.

</td>
</tr>
<tr>
<td>



`V4L2_FWHT_FL_IS_BOTTOM_FIELD`

</td>
<td>



0x00000008

</td>
<td>



If V4L2\_FWHT\_FL\_IS\_ALTERNATE was set, then this is set if this 'frame' is the bottom field, else it is the top field.

</td>
</tr>
<tr>
<td>



`V4L2_FWHT_FL_LUMA_IS_UNCOMPRESSED`

</td>
<td>



0x00000010

</td>
<td>



Set if the Y' (luma) plane is uncompressed.

</td>
</tr>
<tr>
<td>



`V4L2_FWHT_FL_CB_IS_UNCOMPRESSED`

</td>
<td>



0x00000020

</td>
<td>



Set if the Cb plane is uncompressed.

</td>
</tr>
<tr>
<td>



`V4L2_FWHT_FL_CR_IS_UNCOMPRESSED`

</td>
<td>



0x00000040

</td>
<td>



Set if the Cr plane is uncompressed.

</td>
</tr>
<tr>
<td>



`V4L2_FWHT_FL_CHROMA_FULL_HEIGHT`

</td>
<td>



0x00000080

</td>
<td>



Set if the chroma plane has the same height as the luma plane, else the chroma plane is half the height of the luma plane.

</td>
</tr>
<tr>
<td>



`V4L2_FWHT_FL_CHROMA_FULL_WIDTH`

</td>
<td>



0x00000100

</td>
<td>



Set if the chroma plane has the same width as the luma plane, else the chroma plane is half the width of the luma plane.

</td>
</tr>
<tr>
<td>



`V4L2_FWHT_FL_ALPHA_IS_UNCOMPRESSED`

</td>
<td>



0x00000200

</td>
<td>



Set if the alpha plane is uncompressed.

</td>
</tr>
<tr>
<td>



`V4L2_FWHT_FL_I_FRAME`

</td>
<td>



0x00000400

</td>
<td>



Set if this is an I-frame.

</td>
</tr>
<tr>
<td>



`V4L2_FWHT_FL_COMPONENTS_NUM_MSK`

</td>
<td>



0x00070000

</td>
<td>



The number of color components minus one.

</td>
</tr>
<tr>
<td>



`V4L2_FWHT_FL_PIXENC_MSK`

</td>
<td>



0x00180000

</td>
<td>



The mask for the pixel encoding.

</td>
</tr>
<tr>
<td>



`V4L2_FWHT_FL_PIXENC_YUV`

</td>
<td>



0x00080000

</td>
<td>



Set if the pixel encoding is YUV.

</td>
</tr>
<tr>
<td>



`V4L2_FWHT_FL_PIXENC_RGB`

</td>
<td>



0x00100000

</td>
<td>



Set if the pixel encoding is RGB.

</td>
</tr>
<tr>
<td>



`V4L2_FWHT_FL_PIXENC_HSV`

</td>
<td>



0x00180000

</td>
<td>



Set if the pixel encoding is HSV.

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

<a id="rst-v4l2-codec-stateless-vp8"></a>

- **`V4L2_CID_STATELESS_VP8_FRAME (struct)`**

  Specifies the frame parameters for the associated VP8 parsed frame data. This includes the necessary parameters for configuring a stateless hardware decoding pipeline for VP8. The bitstream parameters are defined according to [vp8](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-vp8-1>).

<a id="c-v4l2_ctrl_vp8_frame"></a>



```c
v4l2_ctrl_vp8_frame
```

<!-- Source LaTeX layout: \small -->

<!-- tabularcolumns: |p{7.0cm}|p{4.6cm}|p{5.7cm}| -->


<table>
<caption>

struct v4l2\_ctrl\_vp8\_frame

</caption>
<tbody>
<tr>
<td>



struct `v4l2_vp8_segment`

</td>
<td>



`segment`

</td>
<td>



Structure with segment-based adjustments metadata.

</td>
</tr>
<tr>
<td>



struct `v4l2_vp8_loop_filter`

</td>
<td>



`lf`

</td>
<td>



Structure with loop filter level adjustments metadata.

</td>
</tr>
<tr>
<td>



struct `v4l2_vp8_quantization`

</td>
<td>



`quant`

</td>
<td>



Structure with VP8 dequantization indices metadata.

</td>
</tr>
<tr>
<td>



struct `v4l2_vp8_entropy`

</td>
<td>



`entropy`

</td>
<td>



Structure with VP8 entropy coder probabilities metadata.

</td>
</tr>
<tr>
<td>



struct `v4l2_vp8_entropy_coder_state`

</td>
<td>



`coder_state`

</td>
<td>



Structure with VP8 entropy coder state.

</td>
</tr>
<tr>
<td>



\_\_u16

</td>
<td>



`width`

</td>
<td>



The width of the frame. Must be set for all frames.

</td>
</tr>
<tr>
<td>



\_\_u16

</td>
<td>



`height`

</td>
<td>



The height of the frame. Must be set for all frames.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`horizontal_scale`

</td>
<td>



Horizontal scaling factor.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`vertical_scale`

</td>
<td>



Vertical scaling factor.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`version`

</td>
<td>



Bitstream version.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`prob_skip_false`

</td>
<td>



Indicates the probability that the macroblock is not skipped.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`prob_intra`

</td>
<td>



Indicates the probability that a macroblock is intra-predicted.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`prob_last`

</td>
<td>



Indicates the probability that the last reference frame is used for inter-prediction

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`prob_gf`

</td>
<td>



Indicates the probability that the golden reference frame is used for inter-prediction

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`num_dct_parts`

</td>
<td>



Number of DCT coefficients partitions. Must be one of: 1, 2, 4, or 8.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`first_part_size`

</td>
<td>



Size of the first partition, i.e. the control partition.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`first_part_header_bits`

</td>
<td>



Size in bits of the first partition header portion.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`dct_part_sizes[8]`

</td>
<td>



DCT coefficients sizes.

</td>
</tr>
<tr>
<td>



\_\_u64

</td>
<td>



`last_frame_ts`

</td>
<td>



Timestamp for the V4L2 capture buffer to use as last reference frame, used with inter-coded frames. The timestamp refers to the `timestamp` field in struct `v4l2_buffer`. Use the `v4l2_timeval_to_ns()` function to convert the struct `timeval` in struct `v4l2_buffer` to a \_\_u64.

</td>
</tr>
<tr>
<td>



\_\_u64

</td>
<td>



`golden_frame_ts`

</td>
<td>



Timestamp for the V4L2 capture buffer to use as last reference frame, used with inter-coded frames. The timestamp refers to the `timestamp` field in struct `v4l2_buffer`. Use the `v4l2_timeval_to_ns()` function to convert the struct `timeval` in struct `v4l2_buffer` to a \_\_u64.

</td>
</tr>
<tr>
<td>



\_\_u64

</td>
<td>



`alt_frame_ts`

</td>
<td>



Timestamp for the V4L2 capture buffer to use as alternate reference frame, used with inter-coded frames. The timestamp refers to the `timestamp` field in struct `v4l2_buffer`. Use the `v4l2_timeval_to_ns()` function to convert the struct `timeval` in struct `v4l2_buffer` to a \_\_u64.

</td>
</tr>
<tr>
<td>



\_\_u64

</td>
<td>



`flags`

</td>
<td>



See [Frame Flags](<#rst-vp8-frame-flags>)

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

<a id="rst-vp8-frame-flags"></a>

`Frame Flags`

<!-- tabularcolumns: |p{9.8cm}|p{0.8cm}|p{6.7cm}| -->


<table>
<tbody>
<tr>
<td>



`V4L2_VP8_FRAME_FLAG_KEY_FRAME`

</td>
<td>



0x01

</td>
<td>



Indicates if the frame is a key frame.

</td>
</tr>
<tr>
<td>



`V4L2_VP8_FRAME_FLAG_EXPERIMENTAL`

</td>
<td>



0x02

</td>
<td>



Experimental bitstream.

</td>
</tr>
<tr>
<td>



`V4L2_VP8_FRAME_FLAG_SHOW_FRAME`

</td>
<td>



0x04

</td>
<td>



Show frame flag, indicates if the frame is for display.

</td>
</tr>
<tr>
<td>



`V4L2_VP8_FRAME_FLAG_MB_NO_SKIP_COEFF`

</td>
<td>



0x08

</td>
<td>



Enable/disable skipping of macroblocks with no non-zero coefficients.

</td>
</tr>
<tr>
<td>



`V4L2_VP8_FRAME_FLAG_SIGN_BIAS_GOLDEN`

</td>
<td>



0x10

</td>
<td>



Sign of motion vectors when the golden frame is referenced.

</td>
</tr>
<tr>
<td>



`V4L2_VP8_FRAME_FLAG_SIGN_BIAS_ALT`

</td>
<td>



0x20

</td>
<td>



Sign of motion vectors when the alt frame is referenced.

</td>
</tr>
</tbody>
</table>

<a id="c-v4l2_vp8_entropy_coder_state"></a>



```c
v4l2_vp8_entropy_coder_state
```

<!-- tabularcolumns: |p{1.0cm}|p{2.0cm}|p{14.3cm}| -->


<table>
<caption>

struct v4l2\_vp8\_entropy\_coder\_state

</caption>
<tbody>
<tr>
<td>



\_\_u8

</td>
<td>



`range`

</td>
<td>



coder state value for "Range"

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`value`

</td>
<td>



coder state value for "Value"-

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`bit_count`

</td>
<td>



number of bits left.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`padding`

</td>
<td>



Applications and drivers must set this to zero.

</td>
</tr>
</tbody>
</table>

<a id="c-v4l2_vp8_segment"></a>



```c
v4l2_vp8_segment
```

<!-- tabularcolumns: |p{1.2cm}|p{4.0cm}|p{12.1cm}| -->


<table>
<caption>

struct v4l2\_vp8\_segment

</caption>
<tbody>
<tr>
<td>



\_\_s8

</td>
<td>



`quant_update[4]`

</td>
<td>



Signed quantizer value update.

</td>
</tr>
<tr>
<td>



\_\_s8

</td>
<td>



`lf_update[4]`

</td>
<td>



Signed loop filter level value update.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`segment_probs[3]`

</td>
<td>



Segment probabilities.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`padding`

</td>
<td>



Applications and drivers must set this to zero.

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



See [Segment Flags](<#rst-vp8-segment-flags>)

</td>
</tr>
</tbody>
</table>

<a id="rst-vp8-segment-flags"></a>

`Segment Flags`

<!-- Source LaTeX layout: \small -->

<!-- tabularcolumns: |p{10cm}|p{1.0cm}|p{6.3cm}| -->


<table>
<tbody>
<tr>
<td>



`V4L2_VP8_SEGMENT_FLAG_ENABLED`

</td>
<td>



0x01

</td>
<td>



Enable/disable segment-based adjustments.

</td>
</tr>
<tr>
<td>



`V4L2_VP8_SEGMENT_FLAG_UPDATE_MAP`

</td>
<td>



0x02

</td>
<td>



Indicates if the macroblock segmentation map is updated in this frame.

</td>
</tr>
<tr>
<td>



`V4L2_VP8_SEGMENT_FLAG_UPDATE_FEATURE_DATA`

</td>
<td>



0x04

</td>
<td>



Indicates if the segment feature data is updated in this frame.

</td>
</tr>
<tr>
<td>



`V4L2_VP8_SEGMENT_FLAG_DELTA_VALUE_MODE`

</td>
<td>



0x08

</td>
<td>



If is set, the segment feature data mode is delta-value. If cleared, it's absolute-value.

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

<a id="c-v4l2_vp8_loop_filter"></a>



```c
v4l2_vp8_loop_filter
```

<!-- tabularcolumns: |p{1.5cm}|p{3.9cm}|p{11.9cm}| -->


<table>
<caption>

struct v4l2\_vp8\_loop\_filter

</caption>
<tbody>
<tr>
<td>



\_\_s8

</td>
<td>



`ref_frm_delta[4]`

</td>
<td>



Reference adjustment (signed) delta value.

</td>
</tr>
<tr>
<td>



\_\_s8

</td>
<td>



`mb_mode_delta[4]`

</td>
<td>



Macroblock prediction mode adjustment (signed) delta value.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`sharpness_level`

</td>
<td>



Sharpness level

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`level`

</td>
<td>



Filter level

</td>
</tr>
<tr>
<td>



\_\_u16

</td>
<td>



`padding`

</td>
<td>



Applications and drivers must set this to zero.

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



See [Loop Filter Flags](<#rst-vp8-loop-filter-flags>)

</td>
</tr>
</tbody>
</table>

<a id="rst-vp8-loop-filter-flags"></a>

`Loop Filter Flags`

<!-- tabularcolumns: |p{7.0cm}|p{1.2cm}|p{9.1cm}| -->


<table>
<tbody>
<tr>
<td>



`V4L2_VP8_LF_ADJ_ENABLE`

</td>
<td>



0x01

</td>
<td>



Enable/disable macroblock-level loop filter adjustment.

</td>
</tr>
<tr>
<td>



`V4L2_VP8_LF_DELTA_UPDATE`

</td>
<td>



0x02

</td>
<td>



Indicates if the delta values used in an adjustment are updated.

</td>
</tr>
<tr>
<td>



`V4L2_VP8_LF_FILTER_TYPE_SIMPLE`

</td>
<td>



0x04

</td>
<td>



If set, indicates the filter type is simple. If cleared, the filter type is normal.

</td>
</tr>
</tbody>
</table>

<a id="c-v4l2_vp8_quantization"></a>



```c
v4l2_vp8_quantization
```

<!-- tabularcolumns: |p{1.5cm}|p{3.5cm}|p{12.3cm}| -->


<table>
<caption>

struct v4l2\_vp8\_quantization

</caption>
<tbody>
<tr>
<td>



\_\_u8

</td>
<td>



`y_ac_qi`

</td>
<td>



Luma AC coefficient table index.

</td>
</tr>
<tr>
<td>



\_\_s8

</td>
<td>



`y_dc_delta`

</td>
<td>



Luma DC delta value.

</td>
</tr>
<tr>
<td>



\_\_s8

</td>
<td>



`y2_dc_delta`

</td>
<td>



Y2 block DC delta value.

</td>
</tr>
<tr>
<td>



\_\_s8

</td>
<td>



`y2_ac_delta`

</td>
<td>



Y2 block AC delta value.

</td>
</tr>
<tr>
<td>



\_\_s8

</td>
<td>



`uv_dc_delta`

</td>
<td>



Chroma DC delta value.

</td>
</tr>
<tr>
<td>



\_\_s8

</td>
<td>



`uv_ac_delta`

</td>
<td>



Chroma AC delta value.

</td>
</tr>
<tr>
<td>



\_\_u16

</td>
<td>



`padding`

</td>
<td>



Applications and drivers must set this to zero.

</td>
</tr>
</tbody>
</table>

<a id="c-v4l2_vp8_entropy"></a>



```c
v4l2_vp8_entropy
```

<!-- tabularcolumns: |p{1.5cm}|p{5.8cm}|p{10.0cm}| -->


<table>
<caption>

struct v4l2\_vp8\_entropy

</caption>
<tbody>
<tr>
<td>



\_\_u8

</td>
<td>



`coeff_probs[4][8][3][11]`

</td>
<td>



Coefficient update probabilities.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`y_mode_probs[4]`

</td>
<td>



Luma mode update probabilities.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`uv_mode_probs[3]`

</td>
<td>



Chroma mode update probabilities.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`mv_probs[2][19]`

</td>
<td>



MV decoding update probabilities.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`padding[3]`

</td>
<td>



Applications and drivers must set this to zero.

</td>
</tr>
</tbody>
</table>

<a id="rst-v4l2-codec-stateless-mpeg2"></a>

- **`V4L2_CID_STATELESS_MPEG2_SEQUENCE (struct)`**

  Specifies the sequence parameters (as extracted from the bitstream) for the associated MPEG-2 slice data. This includes fields matching the syntax elements from the sequence header and sequence extension parts of the bitstream as specified by [mpeg2part2](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-mpeg2part2>).

<a id="c-v4l2_ctrl_mpeg2_sequence"></a>



```c
v4l2_ctrl_mpeg2_sequence
```

<!-- Source LaTeX layout: \small -->

<!-- tabularcolumns: |p{1.4cm}|p{6.5cm}|p{9.4cm}| -->


<table>
<caption>

struct v4l2\_ctrl\_mpeg2\_sequence

</caption>
<tbody>
<tr>
<td>



\_\_u16

</td>
<td>



`horizontal_size`

</td>
<td>



The width of the displayable part of the frame's luminance component.

</td>
</tr>
<tr>
<td>



\_\_u16

</td>
<td>



`vertical_size`

</td>
<td>



The height of the displayable part of the frame's luminance component.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`vbv_buffer_size`

</td>
<td>



Used to calculate the required size of the video buffering verifier, defined (in bits) as: 16 \* 1024 \* vbv\_buffer\_size.

</td>
</tr>
<tr>
<td>



\_\_u16

</td>
<td>



`profile_and_level_indication`

</td>
<td>



The current profile and level indication as extracted from the bitstream.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`chroma_format`

</td>
<td>



The chrominance sub-sampling format (1: 4:2:0, 2: 4:2:2, 3: 4:4:4).

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`flags`

</td>
<td>



See [MPEG-2 Sequence Flags](<#rst-mpeg2-sequence-flags>).

</td>
</tr>
</tbody>
</table>

<a id="rst-mpeg2-sequence-flags"></a>

`MPEG-2 Sequence Flags`


<table>
<tbody>
<tr>
<td>



`V4L2_MPEG2_SEQ_FLAG_PROGRESSIVE`

</td>
<td>



0x01

</td>
<td>



Indication that all the frames for the sequence are progressive instead of interlaced.

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

- **`V4L2_CID_STATELESS_MPEG2_PICTURE (struct)`**

  Specifies the picture parameters (as extracted from the bitstream) for the associated MPEG-2 slice data. This includes fields matching the syntax elements from the picture header and picture coding extension parts of the bitstream as specified by [mpeg2part2](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-mpeg2part2>).

<a id="c-v4l2_ctrl_mpeg2_picture"></a>



```c
v4l2_ctrl_mpeg2_picture
```

<!-- Source LaTeX layout: \small -->

<!-- tabularcolumns: |p{1.0cm}|p{5.6cm}|p{10.7cm}| -->


<table>
<caption>

struct v4l2\_ctrl\_mpeg2\_picture

</caption>
<tbody>
<tr>
<td>



\_\_u64

</td>
<td>



`backward_ref_ts`

</td>
<td>



Timestamp of the V4L2 capture buffer to use as backward reference, used with B-coded and P-coded frames. The timestamp refers to the `timestamp` field in struct `v4l2_buffer`. Use the `v4l2_timeval_to_ns()` function to convert the struct `timeval` in struct `v4l2_buffer` to a \_\_u64.

</td>
</tr>
<tr>
<td>



\_\_u64

</td>
<td>



`forward_ref_ts`

</td>
<td>



Timestamp for the V4L2 capture buffer to use as forward reference, used with B-coded frames. The timestamp refers to the `timestamp` field in struct `v4l2_buffer`. Use the `v4l2_timeval_to_ns()` function to convert the struct `timeval` in struct `v4l2_buffer` to a \_\_u64.

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



See [MPEG-2 Picture Flags](<#rst-mpeg2-picture-flags>).

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`f_code[2][2]`

</td>
<td>



Motion vector codes.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`picture_coding_type`

</td>
<td>



Picture coding type for the frame covered by the current slice (V4L2\_MPEG2\_PIC\_CODING\_TYPE\_I, V4L2\_MPEG2\_PIC\_CODING\_TYPE\_P or V4L2\_MPEG2\_PIC\_CODING\_TYPE\_B).

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`picture_structure`

</td>
<td>



Picture structure (1: interlaced top field, 2: interlaced bottom field, 3: progressive frame).

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`intra_dc_precision`

</td>
<td>



Precision of Discrete Cosine transform (0: 8 bits precision, 1: 9 bits precision, 2: 10 bits precision, 3: 11 bits precision).

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`reserved[5]`

</td>
<td>



Applications and drivers must set this to zero.

</td>
</tr>
</tbody>
</table>

<a id="rst-mpeg2-picture-flags"></a>

`MPEG-2 Picture Flags`


<table>
<tbody>
<tr>
<td>



`V4L2_MPEG2_PIC_FLAG_TOP_FIELD_FIRST`

</td>
<td>



0x00000001

</td>
<td>



If set and it's an interlaced stream, top field is output first.

</td>
</tr>
<tr>
<td>



`V4L2_MPEG2_PIC_FLAG_FRAME_PRED_DCT`

</td>
<td>



0x00000002

</td>
<td>



If set only frame-DCT and frame prediction are used.

</td>
</tr>
<tr>
<td>



`V4L2_MPEG2_PIC_FLAG_CONCEALMENT_MV`

</td>
<td>



0x00000004

</td>
<td>



If set motion vectors are coded for intra macroblocks.

</td>
</tr>
<tr>
<td>



`V4L2_MPEG2_PIC_FLAG_Q_SCALE_TYPE`

</td>
<td>



0x00000008

</td>
<td>



This flag affects the inverse quantization process.

</td>
</tr>
<tr>
<td>



`V4L2_MPEG2_PIC_FLAG_INTRA_VLC`

</td>
<td>



0x00000010

</td>
<td>



This flag affects the decoding of transform coefficient data.

</td>
</tr>
<tr>
<td>



`V4L2_MPEG2_PIC_FLAG_ALT_SCAN`

</td>
<td>



0x00000020

</td>
<td>



This flag affects the decoding of transform coefficient data.

</td>
</tr>
<tr>
<td>



`V4L2_MPEG2_PIC_FLAG_REPEAT_FIRST`

</td>
<td>



0x00000040

</td>
<td>



This flag affects the decoding process of progressive frames.

</td>
</tr>
<tr>
<td>



`V4L2_MPEG2_PIC_FLAG_PROGRESSIVE`

</td>
<td>



0x00000080

</td>
<td>



Indicates whether the current frame is progressive.

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

- **`V4L2_CID_STATELESS_MPEG2_QUANTISATION (struct)`**

  Specifies quantisation matrices, in zigzag scanning order, for the associated MPEG-2 slice data. This control is initialized by the kernel to the matrices default values. If a bitstream transmits a user-defined quantisation matrices load, applications are expected to use this control. Applications are also expected to set the control loading the default values, if the quantisation matrices need to be reset, for instance on a sequence header. This process is specified by section 6.3.7. "Quant matrix extension" of the specification.

<a id="c-v4l2_ctrl_mpeg2_quantisation"></a>



```c
v4l2_ctrl_mpeg2_quantisation
```

<!-- tabularcolumns: |p{0.8cm}|p{8.0cm}|p{8.5cm}| -->

<!-- Source LaTeX layout: \small -->


<table>
<caption>

struct v4l2\_ctrl\_mpeg2\_quantisation

</caption>
<tbody>
<tr>
<td>



\_\_u8

</td>
<td>



`intra_quantiser_matrix[64]`

</td>
<td>



The quantisation matrix coefficients for intra-coded frames, in zigzag scanning order. It is relevant for both luma and chroma components, although it can be superseded by the chroma-specific matrix for non-4:2:0 YUV formats.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`non_intra_quantiser_matrix[64]`

</td>
<td>



The quantisation matrix coefficients for non-intra-coded frames, in zigzag scanning order. It is relevant for both luma and chroma components, although it can be superseded by the chroma-specific matrix for non-4:2:0 YUV formats.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`chroma_intra_quantiser_matrix[64]`

</td>
<td>



The quantisation matrix coefficients for the chominance component of intra-coded frames, in zigzag scanning order. Only relevant for non-4:2:0 YUV formats.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`chroma_non_intra_quantiser_matrix[64]`

</td>
<td>



The quantisation matrix coefficients for the chrominance component of non-intra-coded frames, in zigzag scanning order. Only relevant for non-4:2:0 YUV formats.

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

<a id="rst-v4l2-codec-stateless-vp9"></a>

- **`V4L2_CID_STATELESS_VP9_COMPRESSED_HDR (struct)`**

  Stores VP9 probabilities updates as parsed from the current compressed frame header. A value of zero in an array element means no update of the relevant probability. Motion vector-related updates contain a new value or zero. All other updates contain values translated with inv\_map\_table\[\] (see 6.3.5 in [vp9](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-vp9-1>)).

<a id="c-v4l2_ctrl_vp9_compressed_hdr"></a>



```c
v4l2_ctrl_vp9_compressed_hdr
```

<!-- tabularcolumns: |p{1cm}|p{4.8cm}|p{11.4cm}| -->


<table>
<caption>

struct v4l2\_ctrl\_vp9\_compressed\_hdr

</caption>
<tbody>
<tr>
<td>



\_\_u8

</td>
<td>



`tx_mode`

</td>
<td>



Specifies the TX mode. See [TX Mode](<#rst-vp9-tx-mode>) for more details.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`tx8[2][1]`

</td>
<td>



TX 8x8 probabilities delta.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`tx16[2][2]`

</td>
<td>



TX 16x16 probabilities delta.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`tx32[2][3]`

</td>
<td>



TX 32x32 probabilities delta.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`coef[4][2][2][6][6][3]`

</td>
<td>



Coefficient probabilities delta.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`skip[3]`

</td>
<td>



Skip probabilities delta.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`inter_mode[7][3]`

</td>
<td>



Inter prediction mode probabilities delta.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`interp_filter[4][2]`

</td>
<td>



Interpolation filter probabilities delta.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`is_inter[4]`

</td>
<td>



Is inter-block probabilities delta.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`comp_mode[5]`

</td>
<td>



Compound prediction mode probabilities delta.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`single_ref[5][2]`

</td>
<td>



Single reference probabilities delta.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`comp_ref[5]`

</td>
<td>



Compound reference probabilities delta.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`y_mode[4][9]`

</td>
<td>



Y prediction mode probabilities delta.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`uv_mode[10][9]`

</td>
<td>



UV prediction mode probabilities delta.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`partition[16][3]`

</td>
<td>



Partition probabilities delta.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`mv.joint[3]`

</td>
<td>



Motion vector joint probabilities delta.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`mv.sign[2]`

</td>
<td>



Motion vector sign probabilities delta.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`mv.classes[2][10]`

</td>
<td>



Motion vector class probabilities delta.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`mv.class0_bit[2]`

</td>
<td>



Motion vector class0 bit probabilities delta.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`mv.bits[2][10]`

</td>
<td>



Motion vector bits probabilities delta.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`mv.class0_fr[2][2][3]`

</td>
<td>



Motion vector class0 fractional bit probabilities delta.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`mv.fr[2][3]`

</td>
<td>



Motion vector fractional bit probabilities delta.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`mv.class0_hp[2]`

</td>
<td>



Motion vector class0 high precision fractional bit probabilities delta.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`mv.hp[2]`

</td>
<td>



Motion vector high precision fractional bit probabilities delta.

</td>
</tr>
</tbody>
</table>

<a id="rst-vp9-tx-mode"></a>

`TX Mode`

<!-- tabularcolumns: |p{6.5cm}|p{0.5cm}|p{10.3cm}| -->


<table>
<tbody>
<tr>
<td>



`V4L2_VP9_TX_MODE_ONLY_4X4`

</td>
<td>



0

</td>
<td>



Transform size is 4x4.

</td>
</tr>
<tr>
<td>



`V4L2_VP9_TX_MODE_ALLOW_8X8`

</td>
<td>



1

</td>
<td>



Transform size can be up to 8x8.

</td>
</tr>
<tr>
<td>



`V4L2_VP9_TX_MODE_ALLOW_16X16`

</td>
<td>



2

</td>
<td>



Transform size can be up to 16x16.

</td>
</tr>
<tr>
<td>



`V4L2_VP9_TX_MODE_ALLOW_32X32`

</td>
<td>



3

</td>
<td>



transform size can be up to 32x32.

</td>
</tr>
<tr>
<td>



`V4L2_VP9_TX_MODE_SELECT`

</td>
<td>



4

</td>
<td>



Bitstream contains the transform size for each block.

</td>
</tr>
</tbody>
</table>

See section '7.3.1 Tx mode semantics' of the [vp9](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-vp9-1>) specification for more details.

- **`V4L2_CID_STATELESS_VP9_FRAME (struct)`**

  Specifies the frame parameters for the associated VP9 frame decode request. This includes the necessary parameters for configuring a stateless hardware decoding pipeline for VP9. The bitstream parameters are defined according to [vp9](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-vp9-1>).

<a id="c-v4l2_ctrl_vp9_frame"></a>



```c
v4l2_ctrl_vp9_frame
```

<!-- Source LaTeX layout: \small -->

<!-- tabularcolumns: |p{4.7cm}|p{5.5cm}|p{7.1cm}| -->


<table>
<caption>

struct v4l2\_ctrl\_vp9\_frame

</caption>
<tbody>
<tr>
<td>



struct `v4l2_vp9_loop_filter`

</td>
<td>



`lf`

</td>
<td>



Loop filter parameters. See struct `v4l2_vp9_loop_filter` for more details.

</td>
</tr>
<tr>
<td>



struct `v4l2_vp9_quantization`

</td>
<td>



`quant`

</td>
<td>



Quantization parameters. See `v4l2_vp9_quantization` for more details.

</td>
</tr>
<tr>
<td>



struct `v4l2_vp9_segmentation`

</td>
<td>



`seg`

</td>
<td>



Segmentation parameters. See `v4l2_vp9_segmentation` for more details.

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



Combination of V4L2\_VP9\_FRAME\_FLAG\_\* flags. See [Frame Flags](<#rst-vp9-frame-flags>).

</td>
</tr>
<tr>
<td>



\_\_u16

</td>
<td>



`compressed_header_size`

</td>
<td>



Compressed header size in bytes.

</td>
</tr>
<tr>
<td>



\_\_u16

</td>
<td>



`uncompressed_header_size`

</td>
<td>



Uncompressed header size in bytes.

</td>
</tr>
<tr>
<td>



\_\_u16

</td>
<td>



`frame_width_minus_1`

</td>
<td>



Add 1 to get the frame width expressed in pixels. See section 7.2.3 in [vp9](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-vp9-1>).

</td>
</tr>
<tr>
<td>



\_\_u16

</td>
<td>



`frame_height_minus_1`

</td>
<td>



Add 1 to get the frame height expressed in pixels. See section 7.2.3 in [vp9](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-vp9-1>).

</td>
</tr>
<tr>
<td>



\_\_u16

</td>
<td>



`render_width_minus_1`

</td>
<td>



Add 1 to get the expected render width expressed in pixels. This is not used during the decoding process but might be used by HW scalers to prepare a frame that's ready for scanout. See section 7.2.4 in [vp9](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-vp9-1>).

</td>
</tr>
<tr>
<td>



\_\_u16

</td>
<td>



render\_height\_minus\_1

</td>
<td>



Add 1 to get the expected render height expressed in pixels. This is not used during the decoding process but might be used by HW scalers to prepare a frame that's ready for scanout. See section 7.2.4 in [vp9](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-vp9-1>).

</td>
</tr>
<tr>
<td>



\_\_u64

</td>
<td>



`last_frame_ts`

</td>
<td>



"last" reference buffer timestamp. The timestamp refers to the `timestamp` field in struct `v4l2_buffer`. Use the `v4l2_timeval_to_ns()` function to convert the struct `timeval` in struct `v4l2_buffer` to a \_\_u64.

</td>
</tr>
<tr>
<td>



\_\_u64

</td>
<td>



`golden_frame_ts`

</td>
<td>



"golden" reference buffer timestamp. The timestamp refers to the `timestamp` field in struct `v4l2_buffer`. Use the `v4l2_timeval_to_ns()` function to convert the struct `timeval` in struct `v4l2_buffer` to a \_\_u64.

</td>
</tr>
<tr>
<td>



\_\_u64

</td>
<td>



`alt_frame_ts`

</td>
<td>



"alt" reference buffer timestamp. The timestamp refers to the `timestamp` field in struct `v4l2_buffer`. Use the `v4l2_timeval_to_ns()` function to convert the struct `timeval` in struct `v4l2_buffer` to a \_\_u64.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`ref_frame_sign_bias`

</td>
<td>



a bitfield specifying whether the sign bias is set for a given reference frame. See [Reference Frame Sign Bias](<#rst-vp9-ref-frame-sign-bias>) for more details.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`reset_frame_context`

</td>
<td>



specifies whether the frame context should be reset to default values. See [Reset Frame Context](<#rst-vp9-reset-frame-context>) for more details.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`frame_context_idx`

</td>
<td>



Frame context that should be used/updated.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`profile`

</td>
<td>



VP9 profile. Can be 0, 1, 2 or 3.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`bit_depth`

</td>
<td>



Component depth in bits. Can be 8, 10 or 12. Note that not all profiles support 10 and/or 12 bits depths.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`interpolation_filter`

</td>
<td>



Specifies the filter selection used for performing inter prediction. See [Interpolation Filter](<#rst-vp9-interpolation-filter>) for more details.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`tile_cols_log2`

</td>
<td>



Specifies the base 2 logarithm of the width of each tile (where the width is measured in units of 8x8 blocks). Shall be less than or equal to 6.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`tile_rows_log2`

</td>
<td>



Specifies the base 2 logarithm of the height of each tile (where the height is measured in units of 8x8 blocks).

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`reference_mode`

</td>
<td>



Specifies the type of inter prediction to be used. See [Reference Mode](<#rst-vp9-reference-mode>) for more details. Note that this is derived as part of the compressed header parsing process and for this reason should have been part of :c:type: `v4l2_ctrl_vp9_compressed_hdr` optional control. It is safe to set this value to zero if the driver does not require compressed headers.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`reserved[7]`

</td>
<td>



Applications and drivers must set this to zero.

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

<a id="rst-vp9-frame-flags"></a>

`Frame Flags`

<!-- tabularcolumns: |p{10.0cm}|p{1.2cm}|p{6.1cm}| -->


<table>
<tbody>
<tr>
<td>



`V4L2_VP9_FRAME_FLAG_KEY_FRAME`

</td>
<td>



0x001

</td>
<td>



The frame is a key frame.

</td>
</tr>
<tr>
<td>



`V4L2_VP9_FRAME_FLAG_SHOW_FRAME`

</td>
<td>



0x002

</td>
<td>



The frame should be displayed.

</td>
</tr>
<tr>
<td>



`V4L2_VP9_FRAME_FLAG_ERROR_RESILIENT`

</td>
<td>



0x004

</td>
<td>



The decoding should be error resilient.

</td>
</tr>
<tr>
<td>



`V4L2_VP9_FRAME_FLAG_INTRA_ONLY`

</td>
<td>



0x008

</td>
<td>



The frame does not reference other frames.

</td>
</tr>
<tr>
<td>



`V4L2_VP9_FRAME_FLAG_ALLOW_HIGH_PREC_MV`

</td>
<td>



0x010

</td>
<td>



The frame can use high precision motion vectors.

</td>
</tr>
<tr>
<td>



`V4L2_VP9_FRAME_FLAG_REFRESH_FRAME_CTX`

</td>
<td>



0x020

</td>
<td>



Frame context should be updated after decoding.

</td>
</tr>
<tr>
<td>



`V4L2_VP9_FRAME_FLAG_PARALLEL_DEC_MODE`

</td>
<td>



0x040

</td>
<td>



Parallel decoding is used.

</td>
</tr>
<tr>
<td>



`V4L2_VP9_FRAME_FLAG_X_SUBSAMPLING`

</td>
<td>



0x080

</td>
<td>



Vertical subsampling is enabled.

</td>
</tr>
<tr>
<td>



`V4L2_VP9_FRAME_FLAG_Y_SUBSAMPLING`

</td>
<td>



0x100

</td>
<td>



Horizontal subsampling is enabled.

</td>
</tr>
<tr>
<td>



`V4L2_VP9_FRAME_FLAG_COLOR_RANGE_FULL_SWING`

</td>
<td>



0x200

</td>
<td>



The full UV range is used.

</td>
</tr>
</tbody>
</table>

<a id="rst-vp9-ref-frame-sign-bias"></a>

`Reference Frame Sign Bias`

<!-- tabularcolumns: |p{7.0cm}|p{1.2cm}|p{9.1cm}| -->


<table>
<tbody>
<tr>
<td>



`V4L2_VP9_SIGN_BIAS_LAST`

</td>
<td>



0x1

</td>
<td>



Sign bias is set for the last reference frame.

</td>
</tr>
<tr>
<td>



`V4L2_VP9_SIGN_BIAS_GOLDEN`

</td>
<td>



0x2

</td>
<td>



Sign bias is set for the golden reference frame.

</td>
</tr>
<tr>
<td>



`V4L2_VP9_SIGN_BIAS_ALT`

</td>
<td>



0x2

</td>
<td>



Sign bias is set for the alt reference frame.

</td>
</tr>
</tbody>
</table>

<a id="rst-vp9-reset-frame-context"></a>

`Reset Frame Context`

<!-- tabularcolumns: |p{7.0cm}|p{1.2cm}|p{9.1cm}| -->


<table>
<tbody>
<tr>
<td>



`V4L2_VP9_RESET_FRAME_CTX_NONE`

</td>
<td>



0

</td>
<td>



Do not reset any frame context.

</td>
</tr>
<tr>
<td>



`V4L2_VP9_RESET_FRAME_CTX_SPEC`

</td>
<td>



1

</td>
<td>



Reset the frame context pointed to by `v4l2_ctrl_vp9_frame`.frame\_context\_idx.

</td>
</tr>
<tr>
<td>



`V4L2_VP9_RESET_FRAME_CTX_ALL`

</td>
<td>



2

</td>
<td>



Reset all frame contexts.

</td>
</tr>
</tbody>
</table>

See section '7.2 Uncompressed header semantics' of the [vp9](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-vp9-1>) specification for more details.

<a id="rst-vp9-interpolation-filter"></a>

`Interpolation Filter`

<!-- tabularcolumns: |p{9.0cm}|p{1.2cm}|p{7.1cm}| -->


<table>
<tbody>
<tr>
<td>



`V4L2_VP9_INTERP_FILTER_EIGHTTAP`

</td>
<td>



0

</td>
<td>



Eight tap filter.

</td>
</tr>
<tr>
<td>



`V4L2_VP9_INTERP_FILTER_EIGHTTAP_SMOOTH`

</td>
<td>



1

</td>
<td>



Eight tap smooth filter.

</td>
</tr>
<tr>
<td>



`V4L2_VP9_INTERP_FILTER_EIGHTTAP_SHARP`

</td>
<td>



2

</td>
<td>



Eeight tap sharp filter.

</td>
</tr>
<tr>
<td>



`V4L2_VP9_INTERP_FILTER_BILINEAR`

</td>
<td>



3

</td>
<td>



Bilinear filter.

</td>
</tr>
<tr>
<td>



`V4L2_VP9_INTERP_FILTER_SWITCHABLE`

</td>
<td>



4

</td>
<td>



Filter selection is signaled at the block level.

</td>
</tr>
</tbody>
</table>

See section '7.2.7 Interpolation filter semantics' of the [vp9](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-vp9-1>) specification for more details.

<a id="rst-vp9-reference-mode"></a>

`Reference Mode`

<!-- tabularcolumns: |p{9.6cm}|p{0.5cm}|p{7.2cm}| -->


<table>
<tbody>
<tr>
<td>



`V4L2_VP9_REFERENCE_MODE_SINGLE_REFERENCE`

</td>
<td>



0

</td>
<td>



Indicates that all the inter blocks use only a single reference frame to generate motion compensated prediction.

</td>
</tr>
<tr>
<td>



`V4L2_VP9_REFERENCE_MODE_COMPOUND_REFERENCE`

</td>
<td>



1

</td>
<td>



Requires all the inter blocks to use compound mode. Single reference frame prediction is not allowed.

</td>
</tr>
<tr>
<td>



`V4L2_VP9_REFERENCE_MODE_SELECT`

</td>
<td>



2

</td>
<td>



Allows each individual inter block to select between single and compound prediction modes.

</td>
</tr>
</tbody>
</table>

See section '7.3.6 Frame reference mode semantics' of the [vp9](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-vp9-1>) specification for more details.

<a id="c-v4l2_vp9_segmentation"></a>



```c
v4l2_vp9_segmentation
```

Encodes the quantization parameters. See section '7.2.10 Segmentation params syntax' of the [vp9](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-vp9-1>) specification for more details.

<!-- tabularcolumns: |p{0.8cm}|p{5cm}|p{11.4cm}| -->


<table>
<caption>

struct v4l2\_vp9\_segmentation

</caption>
<tbody>
<tr>
<td>



\_\_u8

</td>
<td>



`feature_data[8][4]`

</td>
<td>



Data attached to each feature. Data entry is only valid if the feature is enabled. The array shall be indexed with segment number as the first dimension (0..7) and one of V4L2\_VP9\_SEG\_\* as the second dimension. See [Segment Feature IDs](<#rst-vp9-segment-feature>).

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`feature_enabled[8]`

</td>
<td>



Bitmask defining which features are enabled in each segment. The value for each segment is a combination of V4L2\_VP9\_SEGMENT\_FEATURE\_ENABLED(id) values where id is one of V4L2\_VP9\_SEG\_\*. See [Segment Feature IDs](<#rst-vp9-segment-feature>).

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`tree_probs[7]`

</td>
<td>



Specifies the probability values to be used when decoding a Segment-ID. See '5.15 Segmentation map' section of [vp9](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-vp9-1>) for more details.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`pred_probs[3]`

</td>
<td>



Specifies the probability values to be used when decoding a Predicted-Segment-ID. See '6.4.14 Get segment id syntax' section of [vp9](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-vp9-1>) for more details.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`flags`

</td>
<td>



Combination of V4L2\_VP9\_SEGMENTATION\_FLAG\_\* flags. See [Segmentation Flags](<#rst-vp9-segmentation-flags>).

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`reserved[5]`

</td>
<td>



Applications and drivers must set this to zero.

</td>
</tr>
</tbody>
</table>

<a id="rst-vp9-segment-feature"></a>

`Segment feature IDs`

<!-- tabularcolumns: |p{6.0cm}|p{1cm}|p{10.3cm}| -->


<table>
<tbody>
<tr>
<td>



`V4L2_VP9_SEG_LVL_ALT_Q`

</td>
<td>



0

</td>
<td>



Quantizer segment feature.

</td>
</tr>
<tr>
<td>



`V4L2_VP9_SEG_LVL_ALT_L`

</td>
<td>



1

</td>
<td>



Loop filter segment feature.

</td>
</tr>
<tr>
<td>



`V4L2_VP9_SEG_LVL_REF_FRAME`

</td>
<td>



2

</td>
<td>



Reference frame segment feature.

</td>
</tr>
<tr>
<td>



`V4L2_VP9_SEG_LVL_SKIP`

</td>
<td>



3

</td>
<td>



Skip segment feature.

</td>
</tr>
<tr>
<td>



`V4L2_VP9_SEG_LVL_MAX`

</td>
<td>



4

</td>
<td>



Number of segment features.

</td>
</tr>
</tbody>
</table>

<a id="rst-vp9-segmentation-flags"></a>

`Segmentation Flags`

<!-- tabularcolumns: |p{10.6cm}|p{0.8cm}|p{5.9cm}| -->


<table>
<tbody>
<tr>
<td>



`V4L2_VP9_SEGMENTATION_FLAG_ENABLED`

</td>
<td>



0x01

</td>
<td>



Indicates that this frame makes use of the segmentation tool.

</td>
</tr>
<tr>
<td>



`V4L2_VP9_SEGMENTATION_FLAG_UPDATE_MAP`

</td>
<td>



0x02

</td>
<td>



Indicates that the segmentation map should be updated during the decoding of this frame.

</td>
</tr>
<tr>
<td>



`V4L2_VP9_SEGMENTATION_FLAG_TEMPORAL_UPDATE`

</td>
<td>



0x04

</td>
<td>



Indicates that the updates to the segmentation map are coded relative to the existing segmentation map.

</td>
</tr>
<tr>
<td>



`V4L2_VP9_SEGMENTATION_FLAG_UPDATE_DATA`

</td>
<td>



0x08

</td>
<td>



Indicates that new parameters are about to be specified for each segment.

</td>
</tr>
<tr>
<td>



`V4L2_VP9_SEGMENTATION_FLAG_ABS_OR_DELTA_UPDATE`

</td>
<td>



0x10

</td>
<td>



Indicates that the segmentation parameters represent the actual values to be used.

</td>
</tr>
</tbody>
</table>

<a id="c-v4l2_vp9_quantization"></a>



```c
v4l2_vp9_quantization
```

Encodes the quantization parameters. See section '7.2.9 Quantization params syntax' of the VP9 specification for more details.

<!-- tabularcolumns: |p{0.8cm}|p{4cm}|p{12.4cm}| -->


<table>
<caption>

struct v4l2\_vp9\_quantization

</caption>
<tbody>
<tr>
<td>



\_\_u8

</td>
<td>



`base_q_idx`

</td>
<td>



Indicates the base frame qindex.

</td>
</tr>
<tr>
<td>



\_\_s8

</td>
<td>



`delta_q_y_dc`

</td>
<td>



Indicates the Y DC quantizer relative to base\_q\_idx.

</td>
</tr>
<tr>
<td>



\_\_s8

</td>
<td>



`delta_q_uv_dc`

</td>
<td>



Indicates the UV DC quantizer relative to base\_q\_idx.

</td>
</tr>
<tr>
<td>



\_\_s8

</td>
<td>



`delta_q_uv_ac`

</td>
<td>



Indicates the UV AC quantizer relative to base\_q\_idx.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`reserved[4]`

</td>
<td>



Applications and drivers must set this to zero.

</td>
</tr>
</tbody>
</table>

<a id="c-v4l2_vp9_loop_filter"></a>



```c
v4l2_vp9_loop_filter
```

This structure contains all loop filter related parameters. See sections '7.2.8 Loop filter semantics' of the [vp9](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-vp9-1>) specification for more details.

<!-- tabularcolumns: |p{0.8cm}|p{4cm}|p{12.4cm}| -->


<table>
<caption>

struct v4l2\_vp9\_loop\_filter

</caption>
<tbody>
<tr>
<td>



\_\_s8

</td>
<td>



`ref_deltas[4]`

</td>
<td>



Contains the adjustment needed for the filter level based on the chosen reference frame.

</td>
</tr>
<tr>
<td>



\_\_s8

</td>
<td>



`mode_deltas[2]`

</td>
<td>



Contains the adjustment needed for the filter level based on the chosen mode.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`level`

</td>
<td>



Indicates the loop filter strength.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`sharpness`

</td>
<td>



Indicates the sharpness level.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`flags`

</td>
<td>



Combination of V4L2\_VP9\_LOOP\_FILTER\_FLAG\_\* flags. See [Loop Filter Flags](<#rst-vp9-loop-filter-flags>).

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`reserved[7]`

</td>
<td>



Applications and drivers must set this to zero.

</td>
</tr>
</tbody>
</table>

<a id="rst-vp9-loop-filter-flags"></a>

`Loop Filter Flags`

<!-- tabularcolumns: |p{9.6cm}|p{0.5cm}|p{7.2cm}| -->


<table>
<tbody>
<tr>
<td>



`V4L2_VP9_LOOP_FILTER_FLAG_DELTA_ENABLED`

</td>
<td>



0x1

</td>
<td>



When set, the filter level depends on the mode and reference frame used to predict a block.

</td>
</tr>
<tr>
<td>



`V4L2_VP9_LOOP_FILTER_FLAG_DELTA_UPDATE`

</td>
<td>



0x2

</td>
<td>



When set, the bitstream contains additional syntax elements that specify which mode and reference frame deltas are to be updated.

</td>
</tr>
</tbody>
</table>

<a id="rst-v4l2-codec-stateless-hevc"></a>

- **`V4L2_CID_STATELESS_HEVC_SPS (struct)`**

  Specifies the Sequence Parameter Set fields (as extracted from the bitstream) for the associated HEVC slice data. These bitstream parameters are defined according to [hevc](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-hevc>). They are described in section 7.4.3.2 "Sequence parameter set RBSP semantics" of the specification.

<a id="c-v4l2_ctrl_hevc_sps"></a>



```c
v4l2_ctrl_hevc_sps
```

<!-- Source LaTeX layout: \small -->

<!-- tabularcolumns: |p{1.2cm}|p{9.2cm}|p{6.9cm}| -->


<table>
<caption>

struct v4l2\_ctrl\_hevc\_sps

</caption>
<tbody>
<tr>
<td>



\_\_u8

</td>
<td>



`video_parameter_set_id`

</td>
<td>



Specifies the value of the vps\_video\_parameter\_set\_id of the active VPS as described in section "7.4.3.2.1 General sequence parameter set RBSP semantics" of H.265 specifications.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`seq_parameter_set_id`

</td>
<td>



Provides an identifier for the SPS for reference by other syntax elements as described in section "7.4.3.2.1 General sequence parameter set RBSP semantics" of H.265 specifications.

</td>
</tr>
<tr>
<td>



\_\_u16

</td>
<td>



`pic_width_in_luma_samples`

</td>
<td>



Specifies the width of each decoded picture in units of luma samples.

</td>
</tr>
<tr>
<td>



\_\_u16

</td>
<td>



`pic_height_in_luma_samples`

</td>
<td>



Specifies the height of each decoded picture in units of luma samples.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`bit_depth_luma_minus8`

</td>
<td>



This value plus 8 specifies the bit depth of the samples of the luma array.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`bit_depth_chroma_minus8`

</td>
<td>



This value plus 8 specifies the bit depth of the samples of the chroma arrays.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`log2_max_pic_order_cnt_lsb_minus4`

</td>
<td>



Specifies the value of the variable MaxPicOrderCntLsb.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`sps_max_dec_pic_buffering_minus1`

</td>
<td>



This value plus 1 specifies the maximum required size of the decoded picture buffer for the coded video sequence (CVS).

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`sps_max_num_reorder_pics`

</td>
<td>



Indicates the maximum allowed number of pictures.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`sps_max_latency_increase_plus1`

</td>
<td>



Used to signal MaxLatencyPictures, which indicates the maximum number of pictures that can precede any picture in output order and follow that picture in decoding order.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`log2_min_luma_coding_block_size_minus3`

</td>
<td>



This value plus 3 specifies the minimum luma coding block size.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`log2_diff_max_min_luma_coding_block_size`

</td>
<td>



Specifies the difference between the maximum and minimum luma coding block size.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`log2_min_luma_transform_block_size_minus2`

</td>
<td>



This value plus 2 specifies the minimum luma transform block size.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`log2_diff_max_min_luma_transform_block_size`

</td>
<td>



Specifies the difference between the maximum and minimum luma transform block size.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`max_transform_hierarchy_depth_inter`

</td>
<td>



Specifies the maximum hierarchy depth for transform units of coding units coded in inter prediction mode.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`max_transform_hierarchy_depth_intra`

</td>
<td>



Specifies the maximum hierarchy depth for transform units of coding units coded in intra prediction mode.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`pcm_sample_bit_depth_luma_minus1`

</td>
<td>



This value plus 1 specifies the number of bits used to represent each of PCM sample values of the luma component.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`pcm_sample_bit_depth_chroma_minus1`

</td>
<td>



Specifies the number of bits used to represent each of PCM sample values of the chroma components.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`log2_min_pcm_luma_coding_block_size_minus3`

</td>
<td>



Plus 3 specifies the minimum size of coding blocks.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`log2_diff_max_min_pcm_luma_coding_block_size`

</td>
<td>



Specifies the difference between the maximum and minimum size of coding blocks.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`num_short_term_ref_pic_sets`

</td>
<td>



Specifies the number of st\_ref\_pic\_set() syntax structures included in the SPS.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`num_long_term_ref_pics_sps`

</td>
<td>



Specifies the number of candidate long-term reference pictures that are specified in the SPS.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`chroma_format_idc`

</td>
<td>



Specifies the chroma sampling.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`sps_max_sub_layers_minus1`

</td>
<td>



This value plus 1 specifies the maximum number of temporal sub-layers.

</td>
</tr>
<tr>
<td>



\_\_u64

</td>
<td>



`flags`

</td>
<td>



See [Sequence Parameter Set Flags](<#rst-hevc-sps-flags>)

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

<a id="rst-hevc-sps-flags"></a>

`Sequence Parameter Set Flags`

<!-- Source LaTeX layout: \small -->


<table>
<tbody>
<tr>
<td>



`V4L2_HEVC_SPS_FLAG_SEPARATE_COLOUR_PLANE`

</td>
<td>



0x00000001

</td>
<td>





</td>
</tr>
<tr>
<td>



`V4L2_HEVC_SPS_FLAG_SCALING_LIST_ENABLED`

</td>
<td>



0x00000002

</td>
<td>





</td>
</tr>
<tr>
<td>



`V4L2_HEVC_SPS_FLAG_AMP_ENABLED`

</td>
<td>



0x00000004

</td>
<td>





</td>
</tr>
<tr>
<td>



`V4L2_HEVC_SPS_FLAG_SAMPLE_ADAPTIVE_OFFSET`

</td>
<td>



0x00000008

</td>
<td>





</td>
</tr>
<tr>
<td>



`V4L2_HEVC_SPS_FLAG_PCM_ENABLED`

</td>
<td>



0x00000010

</td>
<td>





</td>
</tr>
<tr>
<td>



`V4L2_HEVC_SPS_FLAG_PCM_LOOP_FILTER_DISABLED`

</td>
<td>



0x00000020

</td>
<td>





</td>
</tr>
<tr>
<td>



`V4L2_HEVC_SPS_FLAG_LONG_TERM_REF_PICS_PRESENT`

</td>
<td>



0x00000040

</td>
<td>





</td>
</tr>
<tr>
<td>



`V4L2_HEVC_SPS_FLAG_SPS_TEMPORAL_MVP_ENABLED`

</td>
<td>



0x00000080

</td>
<td>





</td>
</tr>
<tr>
<td>



`V4L2_HEVC_SPS_FLAG_STRONG_INTRA_SMOOTHING_ENABLED`

</td>
<td>



0x00000100

</td>
<td>





</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

- **`V4L2_CID_STATELESS_HEVC_PPS (struct)`**

  Specifies the Picture Parameter Set fields (as extracted from the bitstream) for the associated HEVC slice data. These bitstream parameters are defined according to [hevc](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-hevc>). They are described in section 7.4.3.3 "Picture parameter set RBSP semantics" of the specification.

<a id="c-v4l2_ctrl_hevc_pps"></a>



```c
v4l2_ctrl_hevc_pps
```

<!-- tabularcolumns: |p{1.2cm}|p{8.6cm}|p{7.5cm}| -->


<table>
<caption>

struct v4l2\_ctrl\_hevc\_pps

</caption>
<tbody>
<tr>
<td>



\_\_u8

</td>
<td>



`pic_parameter_set_id`

</td>
<td>



Identifies the PPS for reference by other syntax elements.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`num_extra_slice_header_bits`

</td>
<td>



Specifies the number of extra slice header bits that are present in the slice header RBSP for coded pictures referring to the PPS.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`num_ref_idx_l0_default_active_minus1`

</td>
<td>



This value plus 1 specifies the inferred value of num\_ref\_idx\_l0\_active\_minus1.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`num_ref_idx_l1_default_active_minus1`

</td>
<td>



This value plus 1 specifies the inferred value of num\_ref\_idx\_l1\_active\_minus1.

</td>
</tr>
<tr>
<td>



\_\_s8

</td>
<td>



`init_qp_minus26`

</td>
<td>



This value plus 26 specifies the initial value of SliceQp Y for each slice referring to the PPS.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`diff_cu_qp_delta_depth`

</td>
<td>



Specifies the difference between the luma coding tree block size and the minimum luma coding block size of coding units that convey cu\_qp\_delta\_abs and cu\_qp\_delta\_sign\_flag.

</td>
</tr>
<tr>
<td>



\_\_s8

</td>
<td>



`pps_cb_qp_offset`

</td>
<td>



Specifies the offsets to the luma quantization parameter Cb.

</td>
</tr>
<tr>
<td>



\_\_s8

</td>
<td>



`pps_cr_qp_offset`

</td>
<td>



Specifies the offsets to the luma quantization parameter Cr.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`num_tile_columns_minus1`

</td>
<td>



This value plus 1 specifies the number of tile columns partitioning the picture.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`num_tile_rows_minus1`

</td>
<td>



This value plus 1 specifies the number of tile rows partitioning the picture.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`column_width_minus1[20]`

</td>
<td>



This value plus 1 specifies the width of the i-th tile column in units of coding tree blocks.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`row_height_minus1[22]`

</td>
<td>



This value plus 1 specifies the height of the i-th tile row in units of coding tree blocks.

</td>
</tr>
<tr>
<td>



\_\_s8

</td>
<td>



`pps_beta_offset_div2`

</td>
<td>



Specifies the default deblocking parameter offsets for beta divided by 2.

</td>
</tr>
<tr>
<td>



\_\_s8

</td>
<td>



`pps_tc_offset_div2`

</td>
<td>



Specifies the default deblocking parameter offsets for tC divided by 2.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`log2_parallel_merge_level_minus2`

</td>
<td>



This value plus 2 specifies the value of the variable Log2ParMrgLevel.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`padding[4]`

</td>
<td>



Applications and drivers must set this to zero.

</td>
</tr>
<tr>
<td>



\_\_u64

</td>
<td>



`flags`

</td>
<td>



See [Picture Parameter Set Flags](<#rst-hevc-pps-flags>)

</td>
</tr>
</tbody>
</table>

<a id="rst-hevc-pps-flags"></a>

`Picture Parameter Set Flags`

<!-- Source LaTeX layout: \small -->


<table>
<tbody>
<tr>
<td>



`V4L2_HEVC_PPS_FLAG_DEPENDENT_SLICE_SEGMENT_ENABLED`

</td>
<td>



0x00000001

</td>
<td>





</td>
</tr>
<tr>
<td>



`V4L2_HEVC_PPS_FLAG_OUTPUT_FLAG_PRESENT`

</td>
<td>



0x00000002

</td>
<td>





</td>
</tr>
<tr>
<td>



`V4L2_HEVC_PPS_FLAG_SIGN_DATA_HIDING_ENABLED`

</td>
<td>



0x00000004

</td>
<td>





</td>
</tr>
<tr>
<td>



`V4L2_HEVC_PPS_FLAG_CABAC_INIT_PRESENT`

</td>
<td>



0x00000008

</td>
<td>





</td>
</tr>
<tr>
<td>



`V4L2_HEVC_PPS_FLAG_CONSTRAINED_INTRA_PRED`

</td>
<td>



0x00000010

</td>
<td>





</td>
</tr>
<tr>
<td>



`V4L2_HEVC_PPS_FLAG_TRANSFORM_SKIP_ENABLED`

</td>
<td>



0x00000020

</td>
<td>





</td>
</tr>
<tr>
<td>



`V4L2_HEVC_PPS_FLAG_CU_QP_DELTA_ENABLED`

</td>
<td>



0x00000040

</td>
<td>





</td>
</tr>
<tr>
<td>



`V4L2_HEVC_PPS_FLAG_PPS_SLICE_CHROMA_QP_OFFSETS_PRESENT`

</td>
<td>



0x00000080

</td>
<td>





</td>
</tr>
<tr>
<td>



`V4L2_HEVC_PPS_FLAG_WEIGHTED_PRED`

</td>
<td>



0x00000100

</td>
<td>





</td>
</tr>
<tr>
<td>



`V4L2_HEVC_PPS_FLAG_WEIGHTED_BIPRED`

</td>
<td>



0x00000200

</td>
<td>





</td>
</tr>
<tr>
<td>



`V4L2_HEVC_PPS_FLAG_TRANSQUANT_BYPASS_ENABLED`

</td>
<td>



0x00000400

</td>
<td>





</td>
</tr>
<tr>
<td>



`V4L2_HEVC_PPS_FLAG_TILES_ENABLED`

</td>
<td>



0x00000800

</td>
<td>





</td>
</tr>
<tr>
<td>



`V4L2_HEVC_PPS_FLAG_ENTROPY_CODING_SYNC_ENABLED`

</td>
<td>



0x00001000

</td>
<td>





</td>
</tr>
<tr>
<td>



`V4L2_HEVC_PPS_FLAG_LOOP_FILTER_ACROSS_TILES_ENABLED`

</td>
<td>



0x00002000

</td>
<td>





</td>
</tr>
<tr>
<td>



`V4L2_HEVC_PPS_FLAG_PPS_LOOP_FILTER_ACROSS_SLICES_ENABLED`

</td>
<td>



0x00004000

</td>
<td>





</td>
</tr>
<tr>
<td>



`V4L2_HEVC_PPS_FLAG_DEBLOCKING_FILTER_OVERRIDE_ENABLED`

</td>
<td>



0x00008000

</td>
<td>





</td>
</tr>
<tr>
<td>



`V4L2_HEVC_PPS_FLAG_PPS_DISABLE_DEBLOCKING_FILTER`

</td>
<td>



0x00010000

</td>
<td>





</td>
</tr>
<tr>
<td>



`V4L2_HEVC_PPS_FLAG_LISTS_MODIFICATION_PRESENT`

</td>
<td>



0x00020000

</td>
<td>





</td>
</tr>
<tr>
<td>



`V4L2_HEVC_PPS_FLAG_SLICE_SEGMENT_HEADER_EXTENSION_PRESENT`

</td>
<td>



0x00040000

</td>
<td>





</td>
</tr>
<tr>
<td>



`V4L2_HEVC_PPS_FLAG_DEBLOCKING_FILTER_CONTROL_PRESENT`

</td>
<td>



0x00080000

</td>
<td>



Specifies the presence of deblocking filter control syntax elements in the PPS

</td>
</tr>
<tr>
<td>



`V4L2_HEVC_PPS_FLAG_UNIFORM_SPACING`

</td>
<td>



0x00100000

</td>
<td>



Specifies that tile column boundaries and likewise tile row boundaries are distributed uniformly across the picture

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

- **`V4L2_CID_STATELESS_HEVC_SLICE_PARAMS (struct)`**

  Specifies various slice-specific parameters, especially from the NAL unit header, general slice segment header and weighted prediction parameter parts of the bitstream. These bitstream parameters are defined according to [hevc](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-hevc>). They are described in section 7.4.7 "General slice segment header semantics" of the specification. This control is a dynamically sized 1-dimensional array, V4L2\_CTRL\_FLAG\_DYNAMIC\_ARRAY flag must be set when using it.

<a id="c-v4l2_ctrl_hevc_slice_params"></a>



```c
v4l2_ctrl_hevc_slice_params
```

<!-- Source LaTeX layout: \scriptsize -->

<!-- tabularcolumns: |p{5.4cm}|p{6.8cm}|p{5.1cm}| -->


<table>
<caption>

struct v4l2\_ctrl\_hevc\_slice\_params

</caption>
<tbody>
<tr>
<td>



\_\_u32

</td>
<td>



`bit_size`

</td>
<td>



Size (in bits) of the current slice data.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`data_byte_offset`

</td>
<td>



Offset (in byte) to the video data in the current slice data.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`num_entry_point_offsets`

</td>
<td>



Specifies the number of entry point offset syntax elements in the slice header. When the driver supports it, the `V4L2_CID_STATELESS_HEVC_ENTRY_POINT_OFFSETS` must be set.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`nal_unit_type`

</td>
<td>



Specifies the coding type of the slice (B, P or I).

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`nuh_temporal_id_plus1`

</td>
<td>



Minus 1 specifies a temporal identifier for the NAL unit.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`slice_type`

</td>
<td>



(V4L2\_HEVC\_SLICE\_TYPE\_I, V4L2\_HEVC\_SLICE\_TYPE\_P or V4L2\_HEVC\_SLICE\_TYPE\_B).

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`colour_plane_id`

</td>
<td>



Specifies the colour plane associated with the current slice.

</td>
</tr>
<tr>
<td>



\_\_s32

</td>
<td>



`slice_pic_order_cnt`

</td>
<td>



Specifies the picture order count.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`num_ref_idx_l0_active_minus1`

</td>
<td>



This value plus 1 specifies the maximum reference index for reference picture list 0 that may be used to decode the slice.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`num_ref_idx_l1_active_minus1`

</td>
<td>



This value plus 1 specifies the maximum reference index for reference picture list 1 that may be used to decode the slice.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`collocated_ref_idx`

</td>
<td>



Specifies the reference index of the collocated picture used for temporal motion vector prediction.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`five_minus_max_num_merge_cand`

</td>
<td>



Specifies the maximum number of merging motion vector prediction candidates supported in the slice subtracted from 5.

</td>
</tr>
<tr>
<td>



\_\_s8

</td>
<td>



`slice_qp_delta`

</td>
<td>



Specifies the initial value of QpY to be used for the coding blocks in the slice.

</td>
</tr>
<tr>
<td>



\_\_s8

</td>
<td>



`slice_cb_qp_offset`

</td>
<td>



Specifies a difference to be added to the value of pps\_cb\_qp\_offset.

</td>
</tr>
<tr>
<td>



\_\_s8

</td>
<td>



`slice_cr_qp_offset`

</td>
<td>



Specifies a difference to be added to the value of pps\_cr\_qp\_offset.

</td>
</tr>
<tr>
<td>



\_\_s8

</td>
<td>



`slice_act_y_qp_offset`

</td>
<td>



Specifies the offset to the luma of quantization parameter qP derived in section 8.6.2

</td>
</tr>
<tr>
<td>



\_\_s8

</td>
<td>



`slice_act_cb_qp_offset`

</td>
<td>



Specifies the offset to the cb of quantization parameter qP derived in section 8.6.2

</td>
</tr>
<tr>
<td>



\_\_s8

</td>
<td>



`slice_act_cr_qp_offset`

</td>
<td>



Specifies the offset to the cr of quantization parameter qP derived in section 8.6.2

</td>
</tr>
<tr>
<td>



\_\_s8

</td>
<td>



`slice_beta_offset_div2`

</td>
<td>



Specifies the deblocking parameter offsets for beta divided by 2.

</td>
</tr>
<tr>
<td>



\_\_s8

</td>
<td>



`slice_tc_offset_div2`

</td>
<td>



Specifies the deblocking parameter offsets for tC divided by 2.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`pic_struct`

</td>
<td>



Indicates whether a picture should be displayed as a frame or as one or more fields.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`slice_segment_addr`

</td>
<td>



Specifies the address of the first coding tree block in the slice segment.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`ref_idx_l0[V4L2_HEVC_DPB_ENTRIES_NUM_MAX]`

</td>
<td>



The list of L0 reference elements as indices in the DPB.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`ref_idx_l1[V4L2_HEVC_DPB_ENTRIES_NUM_MAX]`

</td>
<td>



The list of L1 reference elements as indices in the DPB.

</td>
</tr>
<tr>
<td>



\_\_u16

</td>
<td>



`short_term_ref_pic_set_size`

</td>
<td>



Specifies the size, in bits, of the short-term reference picture set, described as st\_ref\_pic\_set() in the specification, included in the slice header or SPS (section 7.3.6.1).

</td>
</tr>
<tr>
<td>



\_\_u16

</td>
<td>



`long_term_ref_pic_set_size`

</td>
<td>



Specifies the size, in bits, of the long-term reference picture set include in the slice header or SPS. It is the number of bits in the conditional block if(long\_term\_ref\_pics\_present\_flag) in section 7.3.6.1 of the specification.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`padding`

</td>
<td>



Applications and drivers must set this to zero.

</td>
</tr>
<tr>
<td>



struct `v4l2_hevc_pred_weight_table`

</td>
<td>



`pred_weight_table`

</td>
<td>



The prediction weight coefficients for inter-picture prediction.

</td>
</tr>
<tr>
<td>



\_\_u64

</td>
<td>



`flags`

</td>
<td>



See [Slice Parameters Flags](<#rst-hevc-slice-params-flags>)

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

<a id="rst-hevc-slice-params-flags"></a>

`Slice Parameters Flags`

<!-- Source LaTeX layout: \scriptsize -->


<table>
<tbody>
<tr>
<td>



`V4L2_HEVC_SLICE_PARAMS_FLAG_SLICE_SAO_LUMA`

</td>
<td>



0x00000001

</td>
<td>





</td>
</tr>
<tr>
<td>



`V4L2_HEVC_SLICE_PARAMS_FLAG_SLICE_SAO_CHROMA`

</td>
<td>



0x00000002

</td>
<td>





</td>
</tr>
<tr>
<td>



`V4L2_HEVC_SLICE_PARAMS_FLAG_SLICE_TEMPORAL_MVP_ENABLED`

</td>
<td>



0x00000004

</td>
<td>





</td>
</tr>
<tr>
<td>



`V4L2_HEVC_SLICE_PARAMS_FLAG_MVD_L1_ZERO`

</td>
<td>



0x00000008

</td>
<td>





</td>
</tr>
<tr>
<td>



`V4L2_HEVC_SLICE_PARAMS_FLAG_CABAC_INIT`

</td>
<td>



0x00000010

</td>
<td>





</td>
</tr>
<tr>
<td>



`V4L2_HEVC_SLICE_PARAMS_FLAG_COLLOCATED_FROM_L0`

</td>
<td>



0x00000020

</td>
<td>





</td>
</tr>
<tr>
<td>



`V4L2_HEVC_SLICE_PARAMS_FLAG_USE_INTEGER_MV`

</td>
<td>



0x00000040

</td>
<td>





</td>
</tr>
<tr>
<td>



`V4L2_HEVC_SLICE_PARAMS_FLAG_SLICE_DEBLOCKING_FILTER_DISABLED`

</td>
<td>



0x00000080

</td>
<td>





</td>
</tr>
<tr>
<td>



`V4L2_HEVC_SLICE_PARAMS_FLAG_SLICE_LOOP_FILTER_ACROSS_SLICES_ENABLED`

</td>
<td>



0x00000100

</td>
<td>





</td>
</tr>
<tr>
<td>



`V4L2_HEVC_SLICE_PARAMS_FLAG_DEPENDENT_SLICE_SEGMENT`

</td>
<td>



0x00000200

</td>
<td>





</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

- **`V4L2_CID_STATELESS_HEVC_ENTRY_POINT_OFFSETS (integer)`**

  Specifies entry point offsets in bytes. This control is a dynamically sized array. The number of entry point offsets is reported by the `elems` field. This bitstream parameter is defined according to [hevc](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-hevc>). They are described in section 7.4.7.1 "General slice segment header semantics" of the specification. When multiple slices are submitted in a request, the length of this array must be the sum of num\_entry\_point\_offsets of all the slices in the request.

- **`V4L2_CID_STATELESS_HEVC_SCALING_MATRIX (struct)`**

  Specifies the HEVC scaling matrix parameters used for the scaling process for transform coefficients. These matrix and parameters are defined according to [hevc](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-hevc>). They are described in section 7.4.5 "Scaling list data semantics" of the specification.

<a id="c-v4l2_ctrl_hevc_scaling_matrix"></a>



```c
v4l2_ctrl_hevc_scaling_matrix
```

<!-- Source LaTeX layout: \scriptsize -->

<!-- tabularcolumns: |p{5.4cm}|p{6.8cm}|p{5.1cm}| -->


<table>
<caption>

struct v4l2\_ctrl\_hevc\_scaling\_matrix

</caption>
<tbody>
<tr>
<td>



\_\_u8

</td>
<td>



`scaling_list_4x4[6][16]`

</td>
<td>



Scaling list is used for the scaling process for transform coefficients. The values on each scaling list are expected in raster scan order.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`scaling_list_8x8[6][64]`

</td>
<td>



Scaling list is used for the scaling process for transform coefficients. The values on each scaling list are expected in raster scan order.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`scaling_list_16x16[6][64]`

</td>
<td>



Scaling list is used for the scaling process for transform coefficients. The values on each scaling list are expected in raster scan order.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`scaling_list_32x32[2][64]`

</td>
<td>



Scaling list is used for the scaling process for transform coefficients. The values on each scaling list are expected in raster scan order.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`scaling_list_dc_coef_16x16[6]`

</td>
<td>



Scaling list is used for the scaling process for transform coefficients. The values on each scaling list are expected in raster scan order.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`scaling_list_dc_coef_32x32[2]`

</td>
<td>



Scaling list is used for the scaling process for transform coefficients. The values on each scaling list are expected in raster scan order.

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

<a id="c-v4l2_hevc_dpb_entry"></a>



```c
v4l2_hevc_dpb_entry
```

<!-- Source LaTeX layout: \small -->

<!-- tabularcolumns: |p{1.0cm}|p{4.2cm}|p{12.1cm}| -->


<table>
<caption>

struct v4l2\_hevc\_dpb\_entry

</caption>
<tbody>
<tr>
<td>



\_\_u64

</td>
<td>



`timestamp`

</td>
<td>



Timestamp of the V4L2 capture buffer to use as reference, used with B-coded and P-coded frames. The timestamp refers to the `timestamp` field in struct `v4l2_buffer`. Use the `v4l2_timeval_to_ns()` function to convert the struct `timeval` in struct `v4l2_buffer` to a \_\_u64.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`flags`

</td>
<td>



Long term flag for the reference frame (V4L2\_HEVC\_DPB\_ENTRY\_LONG\_TERM\_REFERENCE). The flag is set as described in the ITU HEVC specification chapter "8.3.2 Decoding process for reference picture set".

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`field_pic`

</td>
<td>



Whether the reference is a field picture or a frame. See [HEVC dpb field pic Flags](<#rst-hevc-dpb-field-pic-flags>)

</td>
</tr>
<tr>
<td>



\_\_s32

</td>
<td>



`pic_order_cnt_val`

</td>
<td>



The picture order count of the current picture.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`padding[2]`

</td>
<td>



Applications and drivers must set this to zero.

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

<a id="rst-hevc-dpb-field-pic-flags"></a>

`HEVC dpb field pic Flags`

<!-- Source LaTeX layout: \scriptsize -->


<table>
<tbody>
<tr>
<td>



`V4L2_HEVC_SEI_PIC_STRUCT_FRAME`

</td>
<td>



0

</td>
<td>



(progressive) Frame

</td>
</tr>
<tr>
<td>



`V4L2_HEVC_SEI_PIC_STRUCT_TOP_FIELD`

</td>
<td>



1

</td>
<td>



Top field

</td>
</tr>
<tr>
<td>



`V4L2_HEVC_SEI_PIC_STRUCT_BOTTOM_FIELD`

</td>
<td>



2

</td>
<td>



Bottom field

</td>
</tr>
<tr>
<td>



`V4L2_HEVC_SEI_PIC_STRUCT_TOP_BOTTOM`

</td>
<td>



3

</td>
<td>



Top field, bottom field, in that order

</td>
</tr>
<tr>
<td>



`V4L2_HEVC_SEI_PIC_STRUCT_BOTTOM_TOP`

</td>
<td>



4

</td>
<td>



Bottom field, top field, in that order

</td>
</tr>
<tr>
<td>



`V4L2_HEVC_SEI_PIC_STRUCT_TOP_BOTTOM_TOP`

</td>
<td>



5

</td>
<td>



Top field, bottom field, top field repeated, in that order

</td>
</tr>
<tr>
<td>



`V4L2_HEVC_SEI_PIC_STRUCT_BOTTOM_TOP_BOTTOM`

</td>
<td>



6

</td>
<td>



Bottom field, top field, bottom field repeated, in that order

</td>
</tr>
<tr>
<td>



`V4L2_HEVC_SEI_PIC_STRUCT_FRAME_DOUBLING`

</td>
<td>



7

</td>
<td>



Frame doubling

</td>
</tr>
<tr>
<td>



`V4L2_HEVC_SEI_PIC_STRUCT_FRAME_TRIPLING`

</td>
<td>



8

</td>
<td>



Frame tripling

</td>
</tr>
<tr>
<td>



`V4L2_HEVC_SEI_PIC_STRUCT_TOP_PAIRED_PREVIOUS_BOTTOM`

</td>
<td>



9

</td>
<td>



Top field paired with previous bottom field in output order

</td>
</tr>
<tr>
<td>



`V4L2_HEVC_SEI_PIC_STRUCT_BOTTOM_PAIRED_PREVIOUS_TOP`

</td>
<td>



10

</td>
<td>



Bottom field paired with previous top field in output order

</td>
</tr>
<tr>
<td>



`V4L2_HEVC_SEI_PIC_STRUCT_TOP_PAIRED_NEXT_BOTTOM`

</td>
<td>



11

</td>
<td>



Top field paired with next bottom field in output order

</td>
</tr>
<tr>
<td>



`V4L2_HEVC_SEI_PIC_STRUCT_BOTTOM_PAIRED_NEXT_TOP`

</td>
<td>



12

</td>
<td>



Bottom field paired with next top field in output order

</td>
</tr>
</tbody>
</table>

<a id="c-v4l2_hevc_pred_weight_table"></a>



```c
v4l2_hevc_pred_weight_table
```

<!-- Source LaTeX layout: \footnotesize -->

<!-- tabularcolumns: |p{0.8cm}|p{10.6cm}|p{5.9cm}| -->


<table>
<caption>

struct v4l2\_hevc\_pred\_weight\_table

</caption>
<tbody>
<tr>
<td>



\_\_s8

</td>
<td>



`delta_luma_weight_l0[V4L2_HEVC_DPB_ENTRIES_NUM_MAX]`

</td>
<td>



The difference of the weighting factor applied to the luma prediction value for list 0.

</td>
</tr>
<tr>
<td>



\_\_s8

</td>
<td>



`luma_offset_l0[V4L2_HEVC_DPB_ENTRIES_NUM_MAX]`

</td>
<td>



The additive offset applied to the luma prediction value for list 0.

</td>
</tr>
<tr>
<td>



\_\_s8

</td>
<td>



`delta_chroma_weight_l0[V4L2_HEVC_DPB_ENTRIES_NUM_MAX][2]`

</td>
<td>



The difference of the weighting factor applied to the chroma prediction value for list 0.

</td>
</tr>
<tr>
<td>



\_\_s8

</td>
<td>



`chroma_offset_l0[V4L2_HEVC_DPB_ENTRIES_NUM_MAX][2]`

</td>
<td>



The difference of the additive offset applied to the chroma prediction values for list 0.

</td>
</tr>
<tr>
<td>



\_\_s8

</td>
<td>



`delta_luma_weight_l1[V4L2_HEVC_DPB_ENTRIES_NUM_MAX]`

</td>
<td>



The difference of the weighting factor applied to the luma prediction value for list 1.

</td>
</tr>
<tr>
<td>



\_\_s8

</td>
<td>



`luma_offset_l1[V4L2_HEVC_DPB_ENTRIES_NUM_MAX]`

</td>
<td>



The additive offset applied to the luma prediction value for list 1.

</td>
</tr>
<tr>
<td>



\_\_s8

</td>
<td>



`delta_chroma_weight_l1[V4L2_HEVC_DPB_ENTRIES_NUM_MAX][2]`

</td>
<td>



The difference of the weighting factor applied to the chroma prediction value for list 1.

</td>
</tr>
<tr>
<td>



\_\_s8

</td>
<td>



`chroma_offset_l1[V4L2_HEVC_DPB_ENTRIES_NUM_MAX][2]`

</td>
<td>



The difference of the additive offset applied to the chroma prediction values for list 1.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`luma_log2_weight_denom`

</td>
<td>



The base 2 logarithm of the denominator for all luma weighting factors.

</td>
</tr>
<tr>
<td>



\_\_s8

</td>
<td>



`delta_chroma_log2_weight_denom`

</td>
<td>



The difference of the base 2 logarithm of the denominator for all chroma weighting factors.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`padding[6]`

</td>
<td>



Applications and drivers must set this to zero.

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

- **`V4L2_CID_STATELESS_HEVC_DECODE_MODE (enum)`**

  Specifies the decoding mode to use. Currently exposes slice-based and frame-based decoding but new modes might be added later on. This control is used as a modifier for V4L2\_PIX\_FMT\_HEVC\_SLICE pixel format. Applications that support V4L2\_PIX\_FMT\_HEVC\_SLICE are required to set this control in order to specify the decoding mode that is expected for the buffer. Drivers may expose a single or multiple decoding modes, depending on what they can support.

<a id="c-v4l2_stateless_hevc_decode_mode"></a>



```c
v4l2_stateless_hevc_decode_mode
```

<!-- Source LaTeX layout: \small -->

<!-- tabularcolumns: |p{9.4cm}|p{0.6cm}|p{7.3cm}| -->


<table>
<tbody>
<tr>
<td>



`V4L2_STATELESS_HEVC_DECODE_MODE_SLICE_BASED`

</td>
<td>



0

</td>
<td>



Decoding is done at the slice granularity. The OUTPUT buffer must contain a single slice.

</td>
</tr>
<tr>
<td>



`V4L2_STATELESS_HEVC_DECODE_MODE_FRAME_BASED`

</td>
<td>



1

</td>
<td>



Decoding is done at the frame granularity. The OUTPUT buffer must contain all slices needed to decode the frame.

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

- **`V4L2_CID_STATELESS_HEVC_START_CODE (enum)`**

  Specifies the HEVC slice start code expected for each slice. This control is used as a modifier for V4L2\_PIX\_FMT\_HEVC\_SLICE pixel format. Applications that support V4L2\_PIX\_FMT\_HEVC\_SLICE are required to set this control in order to specify the start code that is expected for the buffer. Drivers may expose a single or multiple start codes, depending on what they can support.

<a id="c-v4l2_stateless_hevc_start_code"></a>



```c
v4l2_stateless_hevc_start_code
```

<!-- tabularcolumns: |p{9.2cm}|p{0.6cm}|p{7.5cm}| -->


<table>
<tbody>
<tr>
<td>



`V4L2_STATELESS_HEVC_START_CODE_NONE`

</td>
<td>



0

</td>
<td>



Selecting this value specifies that HEVC slices are passed to the driver without any start code. The bitstream data should be according to [hevc](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-hevc>) 7.3.1.1 General NAL unit syntax, hence contains emulation prevention bytes when required.

</td>
</tr>
<tr>
<td>



`V4L2_STATELESS_HEVC_START_CODE_ANNEX_B`

</td>
<td>



1

</td>
<td>



Selecting this value specifies that HEVC slices are expected to be prefixed by Annex B start codes. According to [hevc](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-hevc>) valid start codes can be 3-bytes 0x000001 or 4-bytes 0x00000001.

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

- **`V4L2_CID_MPEG_VIDEO_BASELAYER_PRIORITY_ID (integer)`**

  Specifies a priority identifier for the NAL unit, which will be applied to the base layer. By default this value is set to 0 for the base layer, and the next layer will have the priority ID assigned as 1, 2, 3 and so on. The video encoder can't decide the priority id to be applied to a layer, so this has to come from client. This is applicable to H264 and valid Range is from 0 to 63. Source Rec. ITU-T H.264 (06/2019); G.7.4.1.1, G.8.8.1.

- **`V4L2_CID_MPEG_VIDEO_LTR_COUNT (integer)`**

  Specifies the maximum number of Long Term Reference (LTR) frames at any given time that the encoder can keep. This is applicable to the H264 and HEVC encoders.

- **`V4L2_CID_MPEG_VIDEO_FRAME_LTR_INDEX (integer)`**

  After setting this control the frame that will be queued next will be marked as a Long Term Reference (LTR) frame and given this LTR index which ranges from 0 to LTR\_COUNT-1. This is applicable to the H264 and HEVC encoders. Source Rec. ITU-T H.264 (06/2019); Table 7.9

- **`V4L2_CID_MPEG_VIDEO_USE_LTR_FRAMES (bitmask)`**

  Specifies the Long Term Reference (LTR) frame(s) to be used for encoding the next frame queued after setting this control. This provides a bitmask which consists of bits \[0, LTR\_COUNT-1\]. This is applicable to the H264 and HEVC encoders.

- **`V4L2_CID_STATELESS_HEVC_DECODE_PARAMS (struct)`**

  Specifies various decode parameters, especially the references picture order count (POC) for all the lists (short, long, before, current, after) and the number of entries for each of them. These parameters are defined according to [hevc](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-hevc>). They are described in section 8.3 "Slice decoding process" of the specification.

<a id="c-v4l2_ctrl_hevc_decode_params"></a>



```c
v4l2_ctrl_hevc_decode_params
```


<table>
<caption>

struct v4l2\_ctrl\_hevc\_decode\_params

</caption>
<tbody>
<tr>
<td>



\_\_s32

</td>
<td>



`pic_order_cnt_val`

</td>
<td>



PicOrderCntVal as described in section 8.3.1 "Decoding process for picture order count" of the specification.

</td>
</tr>
<tr>
<td>



\_\_u16

</td>
<td>



`short_term_ref_pic_set_size`

</td>
<td>



Specifies the size, in bits, of the short-term reference picture set, of the first slice described as st\_ref\_pic\_set() in the specification, included in the slice header or SPS (section 7.3.6.1).

</td>
</tr>
<tr>
<td>



\_\_u16

</td>
<td>



`long_term_ref_pic_set_size`

</td>
<td>



Specifies the size, in bits, of the long-term reference picture set, of the first slice included in the slice header or SPS. It is the number of bits in the conditional block if(long\_term\_ref\_pics\_present\_flag) in section 7.3.6.1 of the specification.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`num_active_dpb_entries`

</td>
<td>



The number of entries in `dpb`.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`num_poc_st_curr_before`

</td>
<td>



The number of reference pictures in the short-term set that come before the current frame.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`num_poc_st_curr_after`

</td>
<td>



The number of reference pictures in the short-term set that come after the current frame.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`num_poc_lt_curr`

</td>
<td>



The number of reference pictures in the long-term set.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`poc_st_curr_before[V4L2_HEVC_DPB_ENTRIES_NUM_MAX]`

</td>
<td>



PocStCurrBefore as described in section 8.3.2 "Decoding process for reference picture set": provides the index of the short term before references in DPB array.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`poc_st_curr_after[V4L2_HEVC_DPB_ENTRIES_NUM_MAX]`

</td>
<td>



PocStCurrAfter as described in section 8.3.2 "Decoding process for reference picture set": provides the index of the short term after references in DPB array.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`poc_lt_curr[V4L2_HEVC_DPB_ENTRIES_NUM_MAX]`

</td>
<td>



PocLtCurr as described in section 8.3.2 "Decoding process for reference picture set": provides the index of the long term references in DPB array.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`num_delta_pocs_of_ref_rps_idx`

</td>
<td>



When the short\_term\_ref\_pic\_set\_sps\_flag in the slice header is equal to 0, it is the same as the derived value NumDeltaPocs\[RefRpsIdx\]. It can be used to parse the RPS data in slice headers instead of skipping it with @short\_term\_ref\_pic\_set\_size. When the value of short\_term\_ref\_pic\_set\_sps\_flag in the slice header is equal to 1, num\_delta\_pocs\_of\_ref\_rps\_idx shall be set to 0.

</td>
</tr>
<tr>
<td>



struct `v4l2_hevc_dpb_entry`

</td>
<td>



`dpb[V4L2_HEVC_DPB_ENTRIES_NUM_MAX]`

</td>
<td>



The decoded picture buffer, for meta-data about reference frames.

</td>
</tr>
<tr>
<td>



\_\_u64

</td>
<td>



`flags`

</td>
<td>



See [Decode Parameters Flags](<#rst-hevc-decode-params-flags>)

</td>
</tr>
</tbody>
</table>

<a id="rst-hevc-decode-params-flags"></a>

`Decode Parameters Flags`


<table>
<tbody>
<tr>
<td>



`V4L2_HEVC_DECODE_PARAM_FLAG_IRAP_PIC`

</td>
<td>



0x00000001

</td>
<td>





</td>
</tr>
<tr>
<td>



`V4L2_HEVC_DECODE_PARAM_FLAG_IDR_PIC`

</td>
<td>



0x00000002

</td>
<td>





</td>
</tr>
<tr>
<td>



`V4L2_HEVC_DECODE_PARAM_FLAG_NO_OUTPUT_OF_PRIOR`

</td>
<td>



0x00000004

</td>
<td>





</td>
</tr>
</tbody>
</table>

- **`V4L2_CID_STATELESS_HEVC_EXT_SPS_LT_RPS (struct)`**

  Subset of the `v4l2_ctrl_hevc_sps` control. It extends it with the list of Long-term reference sets parameters. These parameters are defined according to [hevc](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-hevc>). They are described in section 7.4.3.2.1 "General sequence parameter set RBSP semantics" of the specification. This control is a dynamically sized 1-dimensional array. The values in the array should be ignored when either num\_long\_term\_ref\_pics\_sps is 0 or the V4L2\_HEVC\_SPS\_FLAG\_LONG\_TERM\_REF\_PICS\_PRESENT flag is not set in `v4l2_ctrl_hevc_sps`.

<a id="c-v4l2_ctrl_hevc_ext_sps_lt_rps"></a>



```c
v4l2_ctrl_hevc_ext_sps_lt_rps
```


<table>
<caption>

struct v4l2\_ctrl\_hevc\_ext\_sps\_lt\_rps

</caption>
<tbody>
<tr>
<td>



\_\_u16

</td>
<td>



`lt_ref_pic_poc_lsb_sps`

</td>
<td>



Long term reference picture order count as described in section 7.4.3.2.1 "General sequence parameter set RBSP semantics" of the specification.

</td>
</tr>
<tr>
<td>



\_\_u16

</td>
<td>



`flags`

</td>
<td>



See [Extended Long-Term RPS Flags](<#rst-hevc-ext-sps-lt-rps-flags>)

</td>
</tr>
</tbody>
</table>

<a id="rst-hevc-ext-sps-lt-rps-flags"></a>

`Extended SPS Long-Term RPS Flags`


<table>
<tbody>
<tr>
<td>



`V4L2_HEVC_EXT_SPS_LT_RPS_FLAG_USED_LT`

</td>
<td>



0x00000001

</td>
<td>



Specifies if the long-term reference picture is used 7.4.3.2.1 "General sequence parameter set RBSP semantics" of the specification.

</td>
</tr>
</tbody>
</table>

- **`V4L2_CID_STATELESS_HEVC_EXT_SPS_ST_RPS (struct)`**

  Subset of the `v4l2_ctrl_hevc_sps` control. It extends it with the list of Short-term reference sets parameters. These parameters are defined according to [hevc](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-hevc>). They are described in section 7.4.8 "Short-term reference picture set semantics" of the specification. This control is a dynamically sized 1-dimensional array. The values in the array should be ignored when num\_short\_term\_ref\_pic\_sets is 0.

<a id="c-v4l2_ctrl_hevc_ext_sps_st_rps"></a>



```c
v4l2_ctrl_hevc_ext_sps_st_rps
```


<table>
<caption>

struct v4l2\_ctrl\_hevc\_ext\_sps\_st\_rps

</caption>
<tbody>
<tr>
<td>



\_\_u8

</td>
<td>



`delta_idx_minus1`

</td>
<td>



Specifies the delta compare to the index. See details in section 7.4.8 "Short-term reference picture set semantics" of the specification.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`delta_rps_sign`

</td>
<td>



Sign of the delta as specified in section 7.4.8 "Short-term reference picture set semantics" of the specification.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`num_negative_pics`

</td>
<td>



Number of short-term RPS entries that have picture order count values less than the picture order count value of the current picture.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`num_positive_pics`

</td>
<td>



Number of short-term RPS entries that have picture order count values greater than the picture order count value of the current picture.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`used_by_curr_pic`

</td>
<td>



Bit i specifies if short-term RPS i is used by the current picture.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`use_delta_flag`

</td>
<td>



Bit i specifies if short-term RPS i is included in the short-term RPS entries.

</td>
</tr>
<tr>
<td>



\_\_u16

</td>
<td>



`abs_delta_rps_minus1`

</td>
<td>



Absolute delta RPS as specified in section 7.4.8 "Short-term reference picture set semantics" of the specification.

</td>
</tr>
<tr>
<td>



\_\_u16

</td>
<td>



`delta_poc_s0_minus1[16]`

</td>
<td>



Specifies the negative picture order count delta for the i-th entry in the short-term RPS. See details in section 7.4.8 "Short-term reference picture set semantics" of the specification.

</td>
</tr>
<tr>
<td>



\_\_u16

</td>
<td>



`delta_poc_s1_minus1[16]`

</td>
<td>



Specifies the positive picture order count delta for the i-th entry in the short-term RPS. See details in section 7.4.8 "Short-term reference picture set semantics" of the specification.

</td>
</tr>
<tr>
<td>



\_\_u16

</td>
<td>



`flags`

</td>
<td>



See [Extended Short-Term RPS Flags](<#rst-hevc-ext-sps-st-rps-flags>)

</td>
</tr>
</tbody>
</table>

<a id="rst-hevc-ext-sps-st-rps-flags"></a>

`Extended SPS Short-Term RPS Flags`


<table>
<tbody>
<tr>
<td>



`V4L2_HEVC_EXT_SPS_ST_RPS_FLAG_INTER_REF_PIC_SET_PRED`

</td>
<td>



0x00000001

</td>
<td>



Specifies if the short-term RPS is predicted from another short term RPS. See details in section 7.4.8 "Short-term reference picture set semantics" of the specification.

</td>
</tr>
</tbody>
</table>

<a id="rst-v4l2-codec-stateless-av1"></a>

- **`V4L2_CID_STATELESS_AV1_SEQUENCE (struct)`**

  Represents an AV1 Sequence OBU (Open Bitstream Unit). See section 5.5 "Sequence header OBU syntax" in [av1](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-av1-1>) for more details.

<a id="c-v4l2_ctrl_av1_sequence"></a>



```c
v4l2_ctrl_av1_sequence
```

<!-- tabularcolumns: |p{5.8cm}|p{4.8cm}|p{6.6cm}| -->


<table>
<caption>

struct v4l2\_ctrl\_av1\_sequence

</caption>
<tbody>
<tr>
<td>



\_\_u32

</td>
<td>



`flags`

</td>
<td>



See [AV1 Sequence Flags](<#rst-av1-sequence-flags>).

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`seq_profile`

</td>
<td>



Specifies the features that can be used in the coded video sequence.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`order_hint_bits`

</td>
<td>



Specifies the number of bits used for the order\_hint field at each frame.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`bit_depth`

</td>
<td>



the bit depth to use for the sequence as described in section 5.5.2 "Color config syntax" in [av1](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-av1-1>) for more details.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`reserved`

</td>
<td>



Applications and drivers must set this to zero.

</td>
</tr>
<tr>
<td>



\_\_u16

</td>
<td>



`max_frame_width_minus_1`

</td>
<td>



Specifies the maximum frame width minus 1 for the frames represented by this sequence header.

</td>
</tr>
<tr>
<td>



\_\_u16

</td>
<td>



`max_frame_height_minus_1`

</td>
<td>



Specifies the maximum frame height minus 1 for the frames represented by this sequence header.

</td>
</tr>
</tbody>
</table>

<a id="rst-av1-sequence-flags"></a>

`AV1 Sequence Flags`


<table>
<tbody>
<tr>
<td>



`V4L2_AV1_SEQUENCE_FLAG_STILL_PICTURE`

</td>
<td>



0x00000001

</td>
<td>



If set, specifies that the coded video sequence contains only one coded frame. If not set, specifies that the coded video sequence contains one or more coded frames.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_SEQUENCE_FLAG_USE_128X128_SUPERBLOCK`

</td>
<td>



0x00000002

</td>
<td>



If set, indicates that superblocks contain 128x128 luma samples. When equal to 0, it indicates that superblocks contain 64x64 luma samples. The number of contained chroma samples depends on subsampling\_x and subsampling\_y.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_SEQUENCE_FLAG_ENABLE_FILTER_INTRA`

</td>
<td>



0x00000004

</td>
<td>



If set, specifies that the use\_filter\_intra syntax element may be present. If not set, specifies that the use\_filter\_intra syntax element will not be present.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_SEQUENCE_FLAG_ENABLE_INTRA_EDGE_FILTER`

</td>
<td>



0x00000008

</td>
<td>



Specifies whether the intra edge filtering process should be enabled.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_SEQUENCE_FLAG_ENABLE_INTERINTRA_COMPOUND`

</td>
<td>



0x00000010

</td>
<td>



If set, specifies that the mode info for inter blocks may contain the syntax element interintra. If not set, specifies that the syntax element interintra will not be present.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_SEQUENCE_FLAG_ENABLE_MASKED_COMPOUND`

</td>
<td>



0x00000020

</td>
<td>



If set, specifies that the mode info for inter blocks may contain the syntax element compound\_type. If not set, specifies that the syntax element compound\_type will not be present.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_SEQUENCE_FLAG_ENABLE_WARPED_MOTION`

</td>
<td>



0x00000040

</td>
<td>



If set, indicates that the allow\_warped\_motion syntax element may be present. If not set, indicates that the allow\_warped\_motion syntax element will not be present.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_SEQUENCE_FLAG_ENABLE_DUAL_FILTER`

</td>
<td>



0x00000080

</td>
<td>



If set, indicates that the inter prediction filter type may be specified independently in the horizontal and vertical directions. If the flag is equal to 0, only one filter type may be specified, which is then used in both directions.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_SEQUENCE_FLAG_ENABLE_ORDER_HINT`

</td>
<td>



0x00000100

</td>
<td>



If set, indicates that tools based on the values of order hints may be used. If not set, indicates that tools based on order hints are disabled.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_SEQUENCE_FLAG_ENABLE_JNT_COMP`

</td>
<td>



0x00000200

</td>
<td>



If set, indicates that the distance weights process may be used for inter prediction.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_SEQUENCE_FLAG_ENABLE_REF_FRAME_MVS`

</td>
<td>



0x00000400

</td>
<td>



If set, indicates that the use\_ref\_frame\_mvs syntax element may be present. If not set, indicates that the use\_ref\_frame\_mvs syntax element will not be present.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_SEQUENCE_FLAG_ENABLE_SUPERRES`

</td>
<td>



0x00000800

</td>
<td>



If set, specifies that the use\_superres syntax element will be present in the uncompressed header. If not set, specifies that the use\_superres syntax element will not be present (instead use\_superres will be set to 0 in the uncompressed header without being read).

</td>
</tr>
<tr>
<td>



`V4L2_AV1_SEQUENCE_FLAG_ENABLE_CDEF`

</td>
<td>



0x00001000

</td>
<td>



If set, specifies that cdef filtering may be enabled. If not set, specifies that cdef filtering is disabled.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_SEQUENCE_FLAG_ENABLE_RESTORATION`

</td>
<td>



0x00002000

</td>
<td>



If set, specifies that loop restoration filtering may be enabled. If not set, specifies that loop restoration filtering is disabled.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_SEQUENCE_FLAG_MONO_CHROME`

</td>
<td>



0x00004000

</td>
<td>



If set, indicates that the video does not contain U and V color planes. If not set, indicates that the video contains Y, U, and V color planes.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_SEQUENCE_FLAG_COLOR_RANGE`

</td>
<td>



0x00008000

</td>
<td>



If set, signals full swing representation, i.e. "Full Range Quantization". If not set, signals studio swing representation, i.e. "Limited Range Quantization".

</td>
</tr>
<tr>
<td>



`V4L2_AV1_SEQUENCE_FLAG_SUBSAMPLING_X`

</td>
<td>



0x00010000

</td>
<td>



Specify the chroma subsampling format.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_SEQUENCE_FLAG_SUBSAMPLING_Y`

</td>
<td>



0x00020000

</td>
<td>



Specify the chroma subsampling format.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_SEQUENCE_FLAG_FILM_GRAIN_PARAMS_PRESENT`

</td>
<td>



0x00040000

</td>
<td>



Specifies whether film grain parameters are present in the coded video sequence.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_SEQUENCE_FLAG_SEPARATE_UV_DELTA_Q`

</td>
<td>



0x00080000

</td>
<td>



If set, indicates that the U and V planes may have separate delta quantizer values. If not set, indicates that the U and V planes will share the same delta quantizer value.

</td>
</tr>
</tbody>
</table>

- **`V4L2_CID_STATELESS_AV1_TILE_GROUP_ENTRY (struct)`**

  Represents a single AV1 tile inside an AV1 Tile Group. Note that MiRowStart, MiRowEnd, MiColStart and MiColEnd can be retrieved from struct v4l2\_av1\_tile\_info in struct v4l2\_ctrl\_av1\_frame using tile\_row and tile\_col. See section 6.10.1 "General tile group OBU semantics" in [av1](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-av1-1>) for more details.

<a id="c-v4l2_ctrl_av1_tile_group_entry"></a>



```c
v4l2_ctrl_av1_tile_group_entry
```

<!-- tabularcolumns: |p{5.8cm}|p{4.8cm}|p{6.6cm}| -->


<table>
<caption>

struct v4l2\_ctrl\_av1\_tile\_group\_entry

</caption>
<tbody>
<tr>
<td>



\_\_u32

</td>
<td>



`tile_offset`

</td>
<td>



Offset from the OBU data, i.e. where the coded tile data actually starts.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`tile_size`

</td>
<td>



Specifies the size in bytes of the coded tile. Equivalent to "TileSize" in [av1](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-av1-1>).

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`tile_row`

</td>
<td>



Specifies the row of the current tile. Equivalent to "TileRow" in [av1](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-av1-1>).

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`tile_col`

</td>
<td>



Specifies the column of the current tile. Equivalent to "TileColumn" in [av1](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-av1-1>).

</td>
</tr>
</tbody>
</table>

<a id="c-v4l2_av1_warp_model"></a>



```c
v4l2_av1_warp_model
```

AV1 Warp Model as described in section 3 "Symbols and abbreviated terms" of [av1](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-av1-1>).

<!-- Source LaTeX layout: \scriptsize -->

<!-- tabularcolumns: |p{7.4cm}|p{0.3cm}|p{9.6cm}| -->


<table>
<tbody>
<tr>
<td>



`V4L2_AV1_WARP_MODEL_IDENTITY`

</td>
<td>



0

</td>
<td>



Warp model is just an identity transform.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_WARP_MODEL_TRANSLATION`

</td>
<td>



1

</td>
<td>



Warp model is a pure translation.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_WARP_MODEL_ROTZOOM`

</td>
<td>



2

</td>
<td>



Warp model is a rotation + symmetric zoom + translation.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_WARP_MODEL_AFFINE`

</td>
<td>



3

</td>
<td>



Warp model is a general affine transform.

</td>
</tr>
</tbody>
</table>

<a id="c-v4l2_av1_reference_frame"></a>



```c
v4l2_av1_reference_frame
```

AV1 Reference Frames as described in section 6.10.24 "Ref frames semantics" of [av1](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-av1-1>).

<!-- Source LaTeX layout: \scriptsize -->

<!-- tabularcolumns: |p{7.4cm}|p{0.3cm}|p{9.6cm}| -->


<table>
<tbody>
<tr>
<td>



`V4L2_AV1_REF_INTRA_FRAME`

</td>
<td>



0

</td>
<td>



Intra Frame Reference.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_REF_LAST_FRAME`

</td>
<td>



1

</td>
<td>



Last Frame Reference.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_REF_LAST2_FRAME`

</td>
<td>



2

</td>
<td>



Last2 Frame Reference.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_REF_LAST3_FRAME`

</td>
<td>



3

</td>
<td>



Last3 Frame Reference.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_REF_GOLDEN_FRAME`

</td>
<td>



4

</td>
<td>



Golden Frame Reference.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_REF_BWDREF_FRAME`

</td>
<td>



5

</td>
<td>



BWD Frame Reference.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_REF_ALTREF2_FRAME`

</td>
<td>



6

</td>
<td>



ALTREF2 Frame Reference.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_REF_ALTREF_FRAME`

</td>
<td>



7

</td>
<td>



ALTREF Frame Reference.

</td>
</tr>
</tbody>
</table>

<a id="c-v4l2_av1_global_motion"></a>



```c
v4l2_av1_global_motion
```

AV1 Global Motion parameters as described in section 6.8.17 "Global motion params semantics" of [av1](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-av1-1>).

<!-- tabularcolumns: |p{1.5cm}|p{5.8cm}|p{10.0cm}| -->


<table>
<caption>

struct v4l2\_av1\_global\_motion

</caption>
<tbody>
<tr>
<td>



\_\_u8

</td>
<td>



`flags[V4L2_AV1_TOTAL_REFS_PER_FRAME]`

</td>
<td>



A bitfield containing the flags per reference frame. See [AV1 Global Motion Flags](<#rst-av1-global-motion-flags>) for more details.

</td>
</tr>
<tr>
<td>



enum `v4l2_av1_warp_model`

</td>
<td>



`type[V4L2_AV1_TOTAL_REFS_PER_FRAME]`

</td>
<td>



The type of global motion transform used.

</td>
</tr>
<tr>
<td>



\_\_s32

</td>
<td>



`params[V4L2_AV1_TOTAL_REFS_PER_FRAME][6]`

</td>
<td>



This field has the same meaning as "gm\_params" in [av1](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-av1-1>).

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`invalid`

</td>
<td>



Bitfield indicating whether the global motion params are invalid for a given reference frame. See section 7.11.3.6 Setup shear process and the variable "warpValid". Use V4L2\_AV1\_GLOBAL\_MOTION\_IS\_INVALID(ref) to create a suitable mask.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`reserved[3]`

</td>
<td>



Applications and drivers must set this to zero.

</td>
</tr>
</tbody>
</table>

<a id="rst-av1-global-motion-flags"></a>

`AV1 Global Motion Flags`


<table>
<tbody>
<tr>
<td>



`V4L2_AV1_GLOBAL_MOTION_FLAG_IS_GLOBAL`

</td>
<td>



0x00000001

</td>
<td>



Specifies whether global motion parameters are present for a particular reference frame.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_GLOBAL_MOTION_FLAG_IS_ROT_ZOOM`

</td>
<td>



0x00000002

</td>
<td>



Specifies whether a particular reference frame uses rotation and zoom global motion.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_GLOBAL_MOTION_FLAG_IS_TRANSLATION`

</td>
<td>



0x00000004

</td>
<td>



Specifies whether a particular reference frame uses translation global motion

</td>
</tr>
</tbody>
</table>

<a id="c-v4l2_av1_frame_restoration_type"></a>



```c
v4l2_av1_frame_restoration_type
```

AV1 Frame Restoration Type.

<!-- Source LaTeX layout: \scriptsize -->

<!-- tabularcolumns: |p{7.4cm}|p{0.3cm}|p{9.6cm}| -->


<table>
<tbody>
<tr>
<td>



`V4L2_AV1_FRAME_RESTORE_NONE`

</td>
<td>



0

</td>
<td>



No filtering is applied.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_FRAME_RESTORE_WIENER`

</td>
<td>



1

</td>
<td>



Wiener filter process is invoked.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_FRAME_RESTORE_SGRPROJ`

</td>
<td>



2

</td>
<td>



Self guided filter process is invoked.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_FRAME_RESTORE_SWITCHABLE`

</td>
<td>



3

</td>
<td>



Restoration filter is swichtable.

</td>
</tr>
</tbody>
</table>

<a id="c-v4l2_av1_loop_restoration"></a>



```c
v4l2_av1_loop_restoration
```

AV1 Loop Restoration as described in section 6.10.15 "Loop restoration params semantics" of [av1](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-av1-1>).

<!-- tabularcolumns: |p{1.5cm}|p{5.8cm}|p{10.0cm}| -->


<table>
<caption>

struct v4l2\_av1\_loop\_restoration

</caption>
<tbody>
<tr>
<td>



\_\_u8

</td>
<td>



`flags`

</td>
<td>



See [AV1 Loop Restoration Flags](<#rst-av1-loop-restoration-flags>).

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`lr_unit_shift`

</td>
<td>



Specifies if the luma restoration size should be halved.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`lr_uv_shift`

</td>
<td>



Specifies if the chroma size should be half the luma size.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`reserved`

</td>
<td>



Applications and drivers must set this to zero.

</td>
</tr>
<tr>
<td>



`v4l2_av1_frame_restoration_type`

</td>
<td>



`frame_restoration_type[V4L2_AV1_NUM_PLANES_MAX]`

</td>
<td>



Specifies the type of restoration used for each plane.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`loop_restoration_size[V4L2_AV1_MAX_NUM_PLANES]`

</td>
<td>



Specifies the size of loop restoration units in units of samples in the current plane.

</td>
</tr>
</tbody>
</table>

<a id="rst-av1-loop-restoration-flags"></a>

`AV1 Loop Restoration Flags`


<table>
<tbody>
<tr>
<td>



`V4L2_AV1_LOOP_RESTORATION_FLAG_USES_LR`

</td>
<td>



0x00000001

</td>
<td>



Retains the same meaning as UsesLr in [av1](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-av1-1>).

</td>
</tr>
<tr>
<td>



`V4L2_AV1_LOOP_RESTORATION_FLAG_USES_CHROMA_LR`

</td>
<td>



0x00000002

</td>
<td>



Retains the same meaning as UsesChromaLr in [av1](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-av1-1>).

</td>
</tr>
</tbody>
</table>

<a id="c-v4l2_av1_cdef"></a>



```c
v4l2_av1_cdef
```

AV1 CDEF params semantics as described in section 6.10.14 "CDEF params semantics" of [av1](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-av1-1>).

<!-- tabularcolumns: |p{1.5cm}|p{5.8cm}|p{10.0cm}| -->


<table>
<caption>

struct v4l2\_av1\_cdef

</caption>
<tbody>
<tr>
<td>



\_\_u8

</td>
<td>



`damping_minus_3`

</td>
<td>



Controls the amount of damping in the deringing filter.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`bits`

</td>
<td>



Specifies the number of bits needed to specify which CDEF filter to apply.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`y_pri_strength[V4L2_AV1_CDEF_MAX]`

</td>
<td>



Specifies the strength of the primary filter.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`y_sec_strength[V4L2_AV1_CDEF_MAX]`

</td>
<td>



Specifies the strength of the secondary filter.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`uv_pri_strength[V4L2_AV1_CDEF_MAX]`

</td>
<td>



Specifies the strength of the primary filter.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`uv_sec_strength[V4L2_AV1_CDEF_MAX]`

</td>
<td>



Specifies the strength of the secondary filter.

</td>
</tr>
</tbody>
</table>

<a id="c-v4l2_av1_segment_feature"></a>



```c
v4l2_av1_segment_feature
```

AV1 segment features as described in section 3 "Symbols and abbreviated terms" of [av1](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-av1-1>).

<!-- Source LaTeX layout: \scriptsize -->

<!-- tabularcolumns: |p{7.4cm}|p{0.3cm}|p{9.6cm}| -->


<table>
<tbody>
<tr>
<td>



`V4L2_AV1_SEG_LVL_ALT_Q`

</td>
<td>



0

</td>
<td>



Index for quantizer segment feature.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_SEG_LVL_ALT_LF_Y_V`

</td>
<td>



1

</td>
<td>



Index for vertical luma loop filter segment feature.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_SEG_LVL_REF_FRAME`

</td>
<td>



5

</td>
<td>



Index for reference frame segment feature.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_SEG_LVL_REF_SKIP`

</td>
<td>



6

</td>
<td>



Index for skip segment feature.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_SEG_LVL_REF_GLOBALMV`

</td>
<td>



7

</td>
<td>



Index for global mv feature.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_SEG_LVL_MAX`

</td>
<td>



8

</td>
<td>



Number of segment features.

</td>
</tr>
</tbody>
</table>

<a id="c-v4l2_av1_segmentation"></a>



```c
v4l2_av1_segmentation
```

AV1 Segmentation params as defined in section 6.8.13 "Segmentation params semantics" of [av1](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-av1-1>).

<!-- tabularcolumns: |p{1.5cm}|p{5.8cm}|p{10.0cm}| -->


<table>
<caption>

struct v4l2\_av1\_segmentation

</caption>
<tbody>
<tr>
<td>



\_\_u8

</td>
<td>



`flags`

</td>
<td>



See [AV1 Segmentation Flags](<#rst-av1-segmentation-flags>)

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`last_active_seg_id`

</td>
<td>



Indicates the highest numbered segment id that has some enabled feature. This is used when decoding the segment id to only decode choices corresponding to used segments.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`feature_enabled[V4L2_AV1_MAX_SEGMENTS]`

</td>
<td>



Bitmask defining which features are enabled in each segment. Use V4L2\_AV1\_SEGMENT\_FEATURE\_ENABLED to build a suitable mask.

</td>
</tr>
<tr>
<td>



\_\_u16

</td>
<td>



`feature_data[V4L2_AV1_MAX_SEGMENTS][V4L2_AV1_SEG_LVL_MAX]`

</td>
<td>



Data attached to each feature. Data entry is only valid if the feature is enabled.

</td>
</tr>
</tbody>
</table>

<a id="rst-av1-segmentation-flags"></a>

`AV1 Segmentation Flags`


<table>
<tbody>
<tr>
<td>



`V4L2_AV1_SEGMENTATION_FLAG_ENABLED`

</td>
<td>



0x00000001

</td>
<td>



If set, indicates that this frame makes use of the segmentation tool. If not set, indicates that the frame does not use segmentation.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_SEGMENTATION_FLAG_UPDATE_MAP`

</td>
<td>



0x00000002

</td>
<td>



If set, indicates that the segmentation map are updated during the decoding of this frame. If not set, indicates that the segmentation map from the previous frame is used.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_SEGMENTATION_FLAG_TEMPORAL_UPDATE`

</td>
<td>



0x00000004

</td>
<td>



If set, indicates that the updates to the segmentation map are coded relative to the existing segmentation map. If not set, indicates that the new segmentation map is coded without reference to the existing segmentation map.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_SEGMENTATION_FLAG_UPDATE_DATA`

</td>
<td>



0x00000008

</td>
<td>



If set, indicates that the updates to the segmentation map are coded relative to the existing segmentation map. If not set, indicates that the new segmentation map is coded without reference to the existing segmentation map.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_SEGMENTATION_FLAG_SEG_ID_PRE_SKIP`

</td>
<td>



0x00000010

</td>
<td>



If set, indicates that the segment id will be read before the skip syntax element. If not set, indicates that the skip syntax element will be read first.

</td>
</tr>
</tbody>
</table>

<a id="c-v4l2_av1_loop_filter"></a>



```c
v4l2_av1_loop_filter
```

AV1 Loop filter params as defined in section 6.8.10 "Loop filter semantics" of [av1](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-av1-1>).

<!-- tabularcolumns: |p{1.5cm}|p{5.8cm}|p{10.0cm}| -->


<table>
<caption>

struct v4l2\_av1\_loop\_filter

</caption>
<tbody>
<tr>
<td>



\_\_u8

</td>
<td>



`flags`

</td>
<td>



See [AV1 Loop Filter flags](<#rst-av1-loop-filter-flags>) for more details.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`level[4]`

</td>
<td>



An array containing loop filter strength values. Different loop filter strength values from the array are used depending on the image plane being filtered, and the edge direction (vertical or horizontal) being filtered.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`sharpness`

</td>
<td>



indicates the sharpness level. The loop\_filter\_level and loop\_filter\_sharpness together determine when a block edge is filtered, and by how much the filtering can change the sample values. The loop filter process is described in section 7.14 of [av1](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-av1-1>).

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`ref_deltas[V4L2_AV1_TOTAL_REFS_PER_FRAME]`

</td>
<td>



contains the adjustment needed for the filter level based on the chosen reference frame. If this syntax element is not present, it maintains its previous value.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`mode_deltas[2]`

</td>
<td>



contains the adjustment needed for the filter level based on the chosen mode. If this syntax element is not present, it maintains its previous value.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`delta_lf_res`

</td>
<td>



specifies the left shift which should be applied to decoded loop filter delta values.

</td>
</tr>
</tbody>
</table>

<a id="rst-av1-loop-filter-flags"></a>

`AV1 Loop Filter Flags`


<table>
<tbody>
<tr>
<td>



`V4L2_AV1_LOOP_FILTER_FLAG_DELTA_ENABLED`

</td>
<td>



0x00000001

</td>
<td>



If set, means that the filter level depends on the mode and reference frame used to predict a block. If not set, means that the filter level does not depend on the mode and reference frame.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_LOOP_FILTER_FLAG_DELTA_UPDATE`

</td>
<td>



0x00000002

</td>
<td>



If set, means that additional syntax elements are present that specify which mode and reference frame deltas are to be updated. If not set, means that these syntax elements are not present.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_LOOP_FILTER_FLAG_DELTA_LF_PRESENT`

</td>
<td>



0x00000004

</td>
<td>



Specifies whether loop filter delta values are present

</td>
</tr>
<tr>
<td>



`V4L2_AV1_LOOP_FILTER_FLAG_DELTA_LF_MULTI`

</td>
<td>



0x00000008

</td>
<td>



A value equal to 1 specifies that separate loop filter deltas are sent for horizontal luma edges, vertical luma edges, the U edges, and the V edges. A value of delta\_lf\_multi equal to 0 specifies that the same loop filter delta is used for all edges.

</td>
</tr>
</tbody>
</table>

<a id="c-v4l2_av1_quantization"></a>



```c
v4l2_av1_quantization
```

AV1 Quantization params as defined in section 6.8.11 "Quantization params semantics" of [av1](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-av1-1>).

<!-- tabularcolumns: |p{1.5cm}|p{5.8cm}|p{10.0cm}| -->


<table>
<caption>

struct v4l2\_av1\_quantization

</caption>
<tbody>
<tr>
<td>



\_\_u8

</td>
<td>



`flags`

</td>
<td>



See [AV1 Loop Filter flags](<#rst-av1-quantization-flags>) for more details.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`base_q_idx`

</td>
<td>



Indicates the base frame qindex. This is used for Y AC coefficients and as the base value for the other quantizers.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`delta_q_y_dc`

</td>
<td>



Indicates the Y DC quantizer relative to base\_q\_idx.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`delta_q_u_dc`

</td>
<td>



Indicates the U DC quantizer relative to base\_q\_idx.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`delta_q_u_ac`

</td>
<td>



Indicates the U AC quantizer relative to base\_q\_idx.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`delta_q_v_dc`

</td>
<td>



Indicates the V DC quantizer relative to base\_q\_idx.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`delta_q_v_ac`

</td>
<td>



Indicates the V AC quantizer relative to base\_q\_idx.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`qm_y`

</td>
<td>



Specifies the level in the quantizer matrix that should be used for luma plane decoding.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`qm_u`

</td>
<td>



Specifies the level in the quantizer matrix that should be used for chroma U plane decoding.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`qm_v`

</td>
<td>



Specifies the level in the quantizer matrix that should be used for chroma V plane decoding.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`delta_q_res`

</td>
<td>



Specifies the left shift which should be applied to decoded quantizer index delta values.

</td>
</tr>
</tbody>
</table>

<a id="rst-av1-quantization-flags"></a>

`AV1 Quantization Flags`


<table>
<tbody>
<tr>
<td>



`V4L2_AV1_QUANTIZATION_FLAG_DIFF_UV_DELTA`

</td>
<td>



0x00000001

</td>
<td>



If set, indicates that the U and V delta quantizer values are coded separately. If not set, indicates that the U and V delta quantizer values share a common value.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_QUANTIZATION_FLAG_USING_QMATRIX`

</td>
<td>



0x00000002

</td>
<td>



If set, specifies that the quantizer matrix will be used to compute quantizers.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_QUANTIZATION_FLAG_DELTA_Q_PRESENT`

</td>
<td>



0x00000004

</td>
<td>



Specifies whether quantizer index delta values are present.

</td>
</tr>
</tbody>
</table>

<a id="c-v4l2_av1_tile_info"></a>



```c
v4l2_av1_tile_info
```

AV1 Tile info as defined in section 6.8.14 "Tile info semantics" of ref:`av1`.

<!-- tabularcolumns: |p{1.5cm}|p{5.8cm}|p{10.0cm}| -->


<table>
<caption>

struct v4l2\_av1\_tile\_info

</caption>
<tbody>
<tr>
<td>



\_\_u8

</td>
<td>



`flags`

</td>
<td>



See [AV1 Tile Info flags](<#rst-av1-tile-info-flags>) for more details.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`context_update_tile_id`

</td>
<td>



Specifies which tile to use for the CDF update.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`tile_cols`

</td>
<td>



Specifies the number of tiles across the frame.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`tile_rows`

</td>
<td>



Specifies the number of tiles down the frame.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`mi_col_starts[V4L2_AV1_MAX_TILE_COLS + 1]`

</td>
<td>



An array specifying the start column (in units of 4x4 luma samples) for each tile across the image.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`mi_row_starts[V4L2_AV1_MAX_TILE_ROWS + 1]`

</td>
<td>



An array specifying the start row (in units of 4x4 luma samples) for each tile across the image.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`width_in_sbs_minus_1[V4L2_AV1_MAX_TILE_COLS]`

</td>
<td>



Specifies the width of a tile minus 1 in units of superblocks.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`height_in_sbs_minus_1[V4L2_AV1_MAX_TILE_ROWS]`

</td>
<td>



Specifies the height of a tile minus 1 in units of superblocks.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`tile_size_bytes`

</td>
<td>



Specifies the number of bytes needed to code each tile size.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`reserved[3]`

</td>
<td>



Applications and drivers must set this to zero.

</td>
</tr>
</tbody>
</table>

<a id="rst-av1-tile-info-flags"></a>

`AV1 Tile Info Flags`


<table>
<tbody>
<tr>
<td>



`V4L2_AV1_TILE_INFO_FLAG_UNIFORM_TILE_SPACING`

</td>
<td>



0x00000001

</td>
<td>



If set, means that the tiles are uniformly spaced across the frame. (In other words, all tiles are the same size except for the ones at the right and bottom edge which can be smaller). If not set means that the tile sizes are coded.

</td>
</tr>
</tbody>
</table>

<a id="c-v4l2_av1_frame_type"></a>



```c
v4l2_av1_frame_type
```

AV1 Frame Type

<!-- Source LaTeX layout: \scriptsize -->

<!-- tabularcolumns: |p{7.4cm}|p{0.3cm}|p{9.6cm}| -->


<table>
<tbody>
<tr>
<td>



`V4L2_AV1_KEY_FRAME`

</td>
<td>



0

</td>
<td>



Key frame.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_INTER_FRAME`

</td>
<td>



1

</td>
<td>



Inter frame.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_INTRA_ONLY_FRAME`

</td>
<td>



2

</td>
<td>



Intra-only frame.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_SWITCH_FRAME`

</td>
<td>



3

</td>
<td>



Switch frame.

</td>
</tr>
</tbody>
</table>

<a id="c-v4l2_av1_interpolation_filter"></a>



```c
v4l2_av1_interpolation_filter
```

AV1 Interpolation Filter

<!-- Source LaTeX layout: \scriptsize -->

<!-- tabularcolumns: |p{7.4cm}|p{0.3cm}|p{9.6cm}| -->


<table>
<tbody>
<tr>
<td>



`V4L2_AV1_INTERPOLATION_FILTER_EIGHTTAP`

</td>
<td>



0

</td>
<td>



Eight tap filter.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_INTERPOLATION_FILTER_EIGHTTAP_SMOOTH`

</td>
<td>



1

</td>
<td>



Eight tap smooth filter.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_INTERPOLATION_FILTER_EIGHTTAP_SHARP`

</td>
<td>



2

</td>
<td>



Eight tap sharp filter.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_INTERPOLATION_FILTER_BILINEAR`

</td>
<td>



3

</td>
<td>



Bilinear filter.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_INTERPOLATION_FILTER_SWITCHABLE`

</td>
<td>



4

</td>
<td>



Filter selection is signaled at the block level.

</td>
</tr>
</tbody>
</table>

<a id="c-v4l2_av1_tx_mode"></a>



```c
v4l2_av1_tx_mode
```

AV1 Tx mode as described in section 6.8.21 "TX mode semantics" of [av1](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-av1-1>).

<!-- Source LaTeX layout: \scriptsize -->

<!-- tabularcolumns: |p{7.4cm}|p{0.3cm}|p{9.6cm}| -->


<table>
<tbody>
<tr>
<td>



`V4L2_AV1_TX_MODE_ONLY_4X4`

</td>
<td>



0

</td>
<td>



The inverse transform will use only 4x4 transforms.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_TX_MODE_LARGEST`

</td>
<td>



1

</td>
<td>



The inverse transform will use the largest transform size that fits inside the block.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_TX_MODE_SELECT`

</td>
<td>



2

</td>
<td>



The choice of transform size is specified explicitly for each block.

</td>
</tr>
</tbody>
</table>

- **`V4L2_CID_STATELESS_AV1_FRAME (struct)`**

  Represents a Frame Header OBU. See 6.8 "Frame Header OBU semantics" of [av1](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-av1-1>) for more details.

<a id="c-v4l2_ctrl_av1_frame"></a>



```c
v4l2_ctrl_av1_frame
```

<!-- tabularcolumns: |p{5.8cm}|p{4.8cm}|p{6.6cm}| -->


<table>
<caption>

struct v4l2\_ctrl\_av1\_frame

</caption>
<tbody>
<tr>
<td>



struct `v4l2_av1_tile_info`

</td>
<td>



`tile_info`

</td>
<td>



Tile info

</td>
</tr>
<tr>
<td>



struct `v4l2_av1_quantization`

</td>
<td>



`quantization`

</td>
<td>



Quantization parameters.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`superres_denom`

</td>
<td>



The denominator for the upscaling ratio.

</td>
</tr>
<tr>
<td>



struct `v4l2_av1_segmentation`

</td>
<td>



`segmentation`

</td>
<td>



Segmentation parameters.

</td>
</tr>
<tr>
<td>



struct `v4l2_av1_loop_filter`

</td>
<td>



`loop_filter`

</td>
<td>



Loop filter params

</td>
</tr>
<tr>
<td>



struct `v4l2_av1_cdef`

</td>
<td>



`cdef`

</td>
<td>



CDEF params

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`skip_mode_frame[2]`

</td>
<td>



Specifies the frames to use for compound prediction when skip\_mode is equal to 1.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`primary_ref_frame`

</td>
<td>



Specifies which reference frame contains the CDF values and other state that should be loaded at the start of the frame.

</td>
</tr>
<tr>
<td>



struct `v4l2_av1_loop_restoration`

</td>
<td>



`loop_restoration`

</td>
<td>



Loop restoration parameters.

</td>
</tr>
<tr>
<td>



struct `v4l2_av1_global_motion`

</td>
<td>



`global_motion`

</td>
<td>



Global motion parameters.

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



See [AV1 Frame flags](<#rst-av1-frame-flags>) for more details.

</td>
</tr>
<tr>
<td>



enum `v4l2_av1_frame_type`

</td>
<td>



`frame_type`

</td>
<td>



Specifies the AV1 frame type

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`order_hint`

</td>
<td>



Specifies OrderHintBits least significant bits of the expected output order for this frame.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`upscaled_width`

</td>
<td>



The upscaled width.

</td>
</tr>
<tr>
<td>



enum `v4l2_av1_interpolation_filter`

</td>
<td>



`interpolation_filter`

</td>
<td>



Specifies the filter selection used for performing inter prediction.

</td>
</tr>
<tr>
<td>



enum `v4l2_av1_tx_mode`

</td>
<td>



`tx_mode`

</td>
<td>



Specifies how the transform size is determined.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`frame_width_minus_1`

</td>
<td>



Add 1 to get the frame's width.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`frame_height_minus_1`

</td>
<td>



Add 1 to get the frame's height.

</td>
</tr>
<tr>
<td>



\_\_u16

</td>
<td>



`render_width_minus_1`

</td>
<td>



Add 1 to get the render width of the frame in luma samples.

</td>
</tr>
<tr>
<td>



\_\_u16

</td>
<td>



`render_height_minus_1`

</td>
<td>



Add 1 to get the render height of the frame in luma samples.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`current_frame_id`

</td>
<td>



Specifies the frame id number for the current frame. Frame id numbers are additional information that do not affect the decoding process, but provide decoders with a way of detecting missing reference frames so that appropriate action can be taken.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`buffer_removal_time[V4L2_AV1_MAX_OPERATING_POINTS]`

</td>
<td>



Specifies the frame removal time in units of DecCT clock ticks counted from the removal time of the last random access point for operating point opNum.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`reserved[4]`

</td>
<td>



Applications and drivers must set this to zero.

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`order_hints[V4L2_AV1_TOTAL_REFS_PER_FRAME]`

</td>
<td>



Specifies the expected output order hint for each reference frame. This field corresponds to the OrderHints variable from the specification (section 5.9.2  "Uncompressed header syntax"). As such, this is only used for non-intra frames and ignored otherwise. order\_hints\[0\] is always ignored.

</td>
</tr>
<tr>
<td>



\_\_u64

</td>
<td>



`reference_frame_ts[V4L2_AV1_TOTAL_REFS_PER_FRAME]`

</td>
<td>



The V4L2 timestamp for each of the reference frames enumerated in enum `v4l2_av1_reference_frame` starting at `V4L2_AV1_REF_LAST_FRAME`. This represents the state of reference slot as described in the spec and updated by userland through the "Reference frame update process" in section 7.20 The timestamp refers to the `timestamp` field in struct `v4l2_buffer`. Use the `v4l2_timeval_to_ns()` function to convert the struct `timeval` in struct `v4l2_buffer` to a \_\_u64.

</td>
</tr>
<tr>
<td>



\_\_s8

</td>
<td>



`ref_frame_idx[V4L2_AV1_REFS_PER_FRAME]`

</td>
<td>



An index into `reference_frame_ts` representing the ordered list of references used by inter-frame. Matches the bitstream syntax element of the same name.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`refresh_frame_flags`

</td>
<td>



Contains a bitmask that specifies which reference frame slots will be updated with the current frame after it is decoded.

</td>
</tr>
</tbody>
</table>

<a id="rst-av1-frame-flags"></a>

`AV1 Frame Flags`


<table>
<tbody>
<tr>
<td>



`V4L2_AV1_FRAME_FLAG_SHOW_FRAME`

</td>
<td>



0x00000001

</td>
<td>



If set, specifies that this frame should be immediately output once decoded. If not set, specifies that this frame should not be immediately output; it may be output later if a later uncompressed header uses show\_existing\_frame equal to 1.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_FRAME_FLAG_SHOWABLE_FRAME`

</td>
<td>



0x00000002

</td>
<td>



If set, specifies that the frame may be output using the show\_existing\_frame mechanism. If not set, specifies that this frame will not be output using the show\_existing\_frame mechanism.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_FRAME_FLAG_ERROR_RESILIENT_MODE`

</td>
<td>



0x00000004

</td>
<td>



Specifies whether error resilient mode is enabled.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_FRAME_FLAG_DISABLE_CDF_UPDATE`

</td>
<td>



0x00000008

</td>
<td>



Specifies whether the CDF update in the symbol decoding process should be disabled.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_FRAME_FLAG_ALLOW_SCREEN_CONTENT_TOOLS`

</td>
<td>



0x00000010

</td>
<td>



If set, indicates that intra blocks may use palette encoding. If not set, indicates that palette encoding is never used.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_FRAME_FLAG_FORCE_INTEGER_MV`

</td>
<td>



0x00000020

</td>
<td>



If set, specifies that motion vectors will always be integers. If not set, specifies that motion vectors can contain fractional bits.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_FRAME_FLAG_ALLOW_INTRABC`

</td>
<td>



0x00000040

</td>
<td>



If set, indicates that intra block copy may be used in this frame. If not set, indicates that intra block copy is not allowed in this frame.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_FRAME_FLAG_USE_SUPERRES`

</td>
<td>



0x00000080

</td>
<td>



If set, indicates that upscaling is needed.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_FRAME_FLAG_ALLOW_HIGH_PRECISION_MV`

</td>
<td>



0x00000100

</td>
<td>



If set, specifies that motion vectors are specified to eighth pel precision. If not set, specifies that motion vectors are specified to quarter pel precision;

</td>
</tr>
<tr>
<td>



`V4L2_AV1_FRAME_FLAG_IS_MOTION_MODE_SWITCHABLE`

</td>
<td>



0x00000200

</td>
<td>



If not set, specifies that only the SIMPLE motion mode will be used.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_FRAME_FLAG_USE_REF_FRAME_MVS`

</td>
<td>



0x00000400

</td>
<td>



If set specifies that motion vector information from a previous frame can be used when decoding the current frame. If not set, specifies that this information will not be used.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_FRAME_FLAG_DISABLE_FRAME_END_UPDATE_CDF`

</td>
<td>



0x00000800

</td>
<td>



If set indicates that the end of frame CDF update is disabled. If not set, indicates that the end of frame CDF update is enabled

</td>
</tr>
<tr>
<td>



`V4L2_AV1_FRAME_FLAG_ALLOW_WARPED_MOTION`

</td>
<td>



0x00001000

</td>
<td>



If set, indicates that the syntax element motion\_mode may be present, if not set, indicates that the syntax element motion\_mode will not be present.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_FRAME_FLAG_REFERENCE_SELECT`

</td>
<td>



0x00002000

</td>
<td>



If set, specifies that the mode info for inter blocks contains the syntax element comp\_mode that indicates whether to use single or compound reference prediction. If not set, specifies that all inter blocks will use single prediction.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_FRAME_FLAG_REDUCED_TX_SET`

</td>
<td>



0x00004000

</td>
<td>



If set, specifies that the frame is restricted to a reduced subset of the full set of transform types.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_FRAME_FLAG_SKIP_MODE_ALLOWED`

</td>
<td>



0x00008000

</td>
<td>



This flag retains the same meaning as SkipModeAllowed in [av1](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-av1-1>).

</td>
</tr>
<tr>
<td>



`V4L2_AV1_FRAME_FLAG_SKIP_MODE_PRESENT`

</td>
<td>



0x00010000

</td>
<td>



If set, specifies that the syntax element skip\_mode will be present, if not set, specifies that skip\_mode will not be used for this frame.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_FRAME_FLAG_FRAME_SIZE_OVERRIDE`

</td>
<td>



0x00020000

</td>
<td>



If set, specifies that the frame size will either be specified as the size of one of the reference frames, or computed from the frame\_width\_minus\_1 and frame\_height\_minus\_1 syntax elements. If not set, specifies that the frame size is equal to the size in the sequence header.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_FRAME_FLAG_BUFFER_REMOVAL_TIME_PRESENT`

</td>
<td>



0x00040000

</td>
<td>



If set, specifies that buffer\_removal\_time is present. If not set, specifies that buffer\_removal\_time is not present.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_FRAME_FLAG_FRAME_REFS_SHORT_SIGNALING`

</td>
<td>



0x00080000

</td>
<td>



If set, indicates that only two reference frames are explicitly signaled. If not set, indicates that all reference frames are explicitly signaled.

</td>
</tr>
</tbody>
</table>

- **`V4L2_CID_STATELESS_AV1_FILM_GRAIN (struct)`**

  Represents the optional film grain parameters. See section 6.8.20 "Film grain params semantics" of [av1](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-av1-1>) for more details.

<a id="c-v4l2_ctrl_av1_film_grain"></a>



```c
v4l2_ctrl_av1_film_grain
```

<!-- tabularcolumns: |p{1.5cm}|p{5.8cm}|p{10.0cm}| -->


<table>
<caption>

struct v4l2\_ctrl\_av1\_film\_grain

</caption>
<tbody>
<tr>
<td>



\_\_u8

</td>
<td>



`flags`

</td>
<td>



See [AV1 Film Grain Flags](<#rst-av1-film-grain-flags>).

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`cr_mult`

</td>
<td>



Represents a multiplier for the cr component used in derivation of the input index to the cr component scaling function.

</td>
</tr>
<tr>
<td>



\_\_u16

</td>
<td>



`grain_seed`

</td>
<td>



Specifies the starting value for the pseudo-random numbers used during film grain synthesis.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`film_grain_params_ref_idx`

</td>
<td>



Indicates which reference frame contains the film grain parameters to be used for this frame.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`num_y_points`

</td>
<td>



Specifies the number of points for the piece-wise linear scaling function of the luma component.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`point_y_value[V4L2_AV1_MAX_NUM_Y_POINTS]`

</td>
<td>



Represents the x (luma value) coordinate for the i-th point of the piecewise linear scaling function for luma component. The values are signaled on the scale of 0..255. In case of 10 bit video, these values correspond to luma values divided by 4. In case of 12 bit video, these values correspond to luma values divided by 16.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`point_y_scaling[V4L2_AV1_MAX_NUM_Y_POINTS]`

</td>
<td>



Represents the scaling (output) value for the i-th point of the piecewise linear scaling function for luma component.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`num_cb_points`

</td>
<td>



Specifies the number of points for the piece-wise linear scaling function of the cb component.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`point_cb_value[V4L2_AV1_MAX_NUM_CB_POINTS]`

</td>
<td>



Represents the x coordinate for the i-th point of the piece-wise linear scaling function for cb component. The values are signaled on the scale of 0..255.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`point_cb_scaling[V4L2_AV1_MAX_NUM_CB_POINTS]`

</td>
<td>



Represents the scaling (output) value for the i-th point of the piecewise linear scaling function for cb component.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`num_cr_points`

</td>
<td>



Represents the number of points for the piece-wise linear scaling function of the cr component.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`point_cr_value[V4L2_AV1_MAX_NUM_CR_POINTS]`

</td>
<td>



Represents the x coordinate for the i-th point of the piece-wise linear scaling function for cr component. The values are signaled on the scale of 0..255.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`point_cr_scaling[V4L2_AV1_MAX_NUM_CR_POINTS]`

</td>
<td>



Represents the scaling (output) value for the i-th point of the piecewise linear scaling function for cr component.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`grain_scaling_minus_8`

</td>
<td>



Represents the shift - 8 applied to the values of the chroma component. The grain\_scaling\_minus\_8 can take values of 0..3 and determines the range and quantization step of the standard deviation of film grain.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`ar_coeff_lag`

</td>
<td>



Specifies the number of auto-regressive coefficients for luma and chroma.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`ar_coeffs_y_plus_128[V4L2_AV1_AR_COEFFS_SIZE]`

</td>
<td>



Specifies auto-regressive coefficients used for the Y plane.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`ar_coeffs_cb_plus_128[V4L2_AV1_AR_COEFFS_SIZE]`

</td>
<td>



Specifies auto-regressive coefficients used for the U plane.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`ar_coeffs_cr_plus_128[V4L2_AV1_AR_COEFFS_SIZE]`

</td>
<td>



Specifies auto-regressive coefficients used for the V plane.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`ar_coeff_shift_minus_6`

</td>
<td>



Specifies the range of the auto-regressive coefficients. Values of 0, 1, 2, and 3 correspond to the ranges for auto-regressive coefficients of \[-2, 2), \[-1, 1), \[-0.5, 0.5) and \[-0.25, 0.25) respectively.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`grain_scale_shift`

</td>
<td>



Specifies how much the Gaussian random numbers should be scaled down during the grain synthesis process.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`cb_mult`

</td>
<td>



Represents a multiplier for the cb component used in derivation of the input index to the cb component scaling function.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`cb_luma_mult`

</td>
<td>



Represents a multiplier for the average luma component used in derivation of the input index to the cb component scaling function..

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`cr_luma_mult`

</td>
<td>



Represents a multiplier for the average luma component used in derivation of the input index to the cr component scaling function.

</td>
</tr>
<tr>
<td>



\_\_u16

</td>
<td>



`cb_offset`

</td>
<td>



Represents an offset used in derivation of the input index to the cb component scaling function.

</td>
</tr>
<tr>
<td>



\_\_u16

</td>
<td>



`cr_offset`

</td>
<td>



Represents an offset used in derivation of the input index to the cr component scaling function.

</td>
</tr>
<tr>
<td>



\_\_u8

</td>
<td>



`reserved[4]`

</td>
<td>



Applications and drivers must set this to zero.

</td>
</tr>
</tbody>
</table>

<a id="rst-av1-film-grain-flags"></a>

`AV1 Film Grain Flags`


<table>
<tbody>
<tr>
<td>



`V4L2_AV1_FILM_GRAIN_FLAG_APPLY_GRAIN`

</td>
<td>



0x00000001

</td>
<td>



If set, specifies that film grain should be added to this frame. If not set, specifies that film grain should not be added.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_FILM_GRAIN_FLAG_UPDATE_GRAIN`

</td>
<td>



0x00000002

</td>
<td>



If set, means that a new set of parameters should be sent. If not set, specifies that the previous set of parameters should be used.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_FILM_GRAIN_FLAG_CHROMA_SCALING_FROM_LUMA`

</td>
<td>



0x00000004

</td>
<td>



If set, specifies that the chroma scaling is inferred from the luma scaling.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_FILM_GRAIN_FLAG_OVERLAP`

</td>
<td>



0x00000008

</td>
<td>



If set, indicates that the overlap between film grain blocks shall be applied. If not set, indicates that the overlap between film grain blocks shall not be applied.

</td>
</tr>
<tr>
<td>



`V4L2_AV1_FILM_GRAIN_FLAG_CLIP_TO_RESTRICTED_RANGE`

</td>
<td>



0x00000010

</td>
<td>



If set, indicates that clipping to the restricted (studio, i.e. limited) range shall be applied to the sample values after adding the film grain (see the semantics for color\_range for an explanation of studio swing). If not set, indicates that clipping to the full range shall be applied to the sample values after adding the film grain.

</td>
</tr>
</tbody>
</table>
