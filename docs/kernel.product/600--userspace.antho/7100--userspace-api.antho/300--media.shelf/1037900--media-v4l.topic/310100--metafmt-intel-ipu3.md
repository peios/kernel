---
title: "V4L2_META_FMT_IPU3_PARAMS ('ip3p'), V4L2_META_FMT_IPU3_3A ('ip3s')"
type: reference
description: "The IPU3 ImgU 3A statistics accelerators collect different statistics over an input Bayer frame. Those statistics are obtained from the \"ipu3-imgu [01] 3a stat\" metadata capture video nodes, using the v4l2_meta_format interface. They are…"
---

<a id="rst-v4l2-meta-fmt-ipu3-params-ip3p-v4l2-meta-fmt-ipu3-3a-ip3s"></a>
<a id="rst-v4l2-meta-fmt-stat-3a"></a>
<a id="rst-v4l2-meta-fmt-params"></a>

<!-- SPDX-License-Identifier: GPL-2.0 OR GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<!-- ipu3_uapi_stats_3a -->

<a id="rst-a-statistics"></a>

## 3A statistics

The IPU3 ImgU 3A statistics accelerators collect different statistics over an input Bayer frame. Those statistics are obtained from the "ipu3-imgu \[01\] 3a stat" metadata capture video nodes, using the `v4l2_meta_format` interface. They are formatted as described by the `ipu3_uapi_stats_3a` structure.

The statistics collected are AWB (Auto-white balance) RGBS (Red, Green, Blue and Saturation measure) cells, AWB filter response, AF (Auto-focus) filter response, and AE (Auto-exposure) histogram.

The struct `ipu3_uapi_4a_config` saves all configurable parameters.



```c
struct ipu3_uapi_stats_3a {
        struct ipu3_uapi_awb_raw_buffer awb_raw_buffer;
        struct ipu3_uapi_ae_raw_buffer_aligned ae_raw_buffer[IPU3_UAPI_MAX_STRIPES];
        struct ipu3_uapi_af_raw_buffer af_raw_buffer;
        struct ipu3_uapi_awb_fr_raw_buffer awb_fr_raw_buffer;
        struct ipu3_uapi_4a_config stats_4a_config;
        __u32 ae_join_buffers;
        __u8 padding[28];
        struct ipu3_uapi_stats_3a_bubble_info_per_stripe stats_3a_bubble_per_stripe;
        struct ipu3_uapi_ff_status stats_3a_status;
};
```

<!-- ipu3_uapi_params -->

<a id="rst-pipeline-parameters"></a>

## Pipeline parameters

The pipeline parameters are passed to the "ipu3-imgu \[01\] parameters" metadata output video nodes, using the `v4l2_meta_format` interface. They are formatted as described by the `ipu3_uapi_params` structure.

Both 3A statistics and pipeline parameters described here are closely tied to the underlying camera sub-system (CSS) APIs. They are usually consumed and produced by dedicated user space libraries that comprise the important tuning tools, thus freeing the developers from being bothered with the low level hardware and algorithm details.



```c
struct ipu3_uapi_params {
        /* Flags which of the settings below are to be applied */
        struct ipu3_uapi_flags use;

        /* Accelerator cluster parameters */
        struct ipu3_uapi_acc_param acc_param;

        /* ISP vector address space parameters */
        struct ipu3_uapi_isp_lin_vmem_params lin_vmem_params;
        struct ipu3_uapi_isp_tnr3_vmem_params tnr3_vmem_params;
        struct ipu3_uapi_isp_xnr3_vmem_params xnr3_vmem_params;

        /* ISP data memory (DMEM) parameters */
        struct ipu3_uapi_isp_tnr3_params tnr3_dmem_params;
        struct ipu3_uapi_isp_xnr3_params xnr3_dmem_params;

        /* Optical black level compensation */
        struct ipu3_uapi_obgrid_param obgrid_param;
};
```

<a id="rst-intel-ipu3-imgu-uapi-data-types"></a>

## Intel IPU3 ImgU uAPI data types

```{kernel-doc} drivers/staging/media/ipu3/include/uapi/intel-ipu3.h

```
