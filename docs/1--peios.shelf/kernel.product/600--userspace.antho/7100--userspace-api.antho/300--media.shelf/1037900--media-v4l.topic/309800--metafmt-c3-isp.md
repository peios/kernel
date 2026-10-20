---
title: "V4L2_META_FMT_C3ISP_STATS ('C3ST'), V4L2_META_FMT_C3ISP_PARAMS ('C3PM')"
type: reference
description: "The C3 ISP can collect different statistics over an input Bayer frame. Those statistics are obtained from the \"c3-isp-stats\" metadata capture video nodes, using the v4l2_meta_format interface. They are formatted as described by the…"
---

<a id="rst-v4l2-meta-fmt-c3isp-stats-c3st-v4l2-meta-fmt-c3isp-params-c3pm"></a>
<a id="rst-v4l2-meta-fmt-c3isp-params"></a>
<a id="rst-v4l2-meta-fmt-c3isp-stats"></a>

<!-- SPDX-License-Identifier: (GPL-2.0-only OR MIT) -->

<!-- c:namespace: V4L -->

<!-- c3_isp_stats_info -->

<a id="rst-a-statistics"></a>

## 3A Statistics

The C3 ISP can collect different statistics over an input Bayer frame. Those statistics are obtained from the "c3-isp-stats" metadata capture video nodes, using the `v4l2_meta_format` interface. They are formatted as described by the `c3_isp_stats_info` structure.

The statistics collected are  Auto-white balance, Auto-exposure and Auto-focus information.

<!-- c3_isp_params_cfg -->

<a id="rst-configuration-parameters"></a>

## Configuration Parameters

The configuration parameters are passed to the c3-isp-params metadata output video node, using the `v4l2_meta_format` interface. Rather than a single struct containing sub-structs for each configurable area of the ISP, parameters for the C3-ISP are defined as distinct structs or "blocks" which may be added to the data member of `c3_isp_params_cfg`. Userspace is responsible for populating the data member with the blocks that need to be configured by the driver, but need not populate it with **all** the blocks, or indeed with any at all if there are no configuration changes to make. Populated blocks **must** be consecutive in the buffer. To assist both userspace and the driver in identifying the blocks each block-specific struct embeds `c3_isp_params_block_header` as its first member and userspace must populate the type member with a value from `c3_isp_params_block_type`. Once the blocks have been populated into the data buffer, the combined size of all populated blocks shall be set in the data_size member of `c3_isp_params_cfg`. For example:



```c
struct c3_isp_params_cfg *params =
        (struct c3_isp_params_cfg *)buffer;

params->version = C3_ISP_PARAM_BUFFER_V0;
params->data_size = 0;

void *data = (void *)params->data;

struct c3_isp_params_awb_gains *gains =
        (struct c3_isp_params_awb_gains *)data;

gains->header.type = C3_ISP_PARAMS_BLOCK_AWB_GAINS;
gains->header.flags = C3_ISP_PARAMS_BLOCK_FL_ENABLE;
gains->header.size = sizeof(struct c3_isp_params_awb_gains);

gains->gr_gain = 256;
gains->r_gain = 256;
gains->b_gain = 256;
gains->gb_gain = 256;

data += sizeof(struct c3_isp__params_awb_gains);
params->data_size += sizeof(struct c3_isp_params_awb_gains);

struct c3_isp_params_awb_config *awb_cfg =
        (struct c3_isp_params_awb_config *)data;

awb_cfg->header.type = C3_ISP_PARAMS_BLOCK_AWB_CONFIG;
awb_cfg->header.flags = C3_ISP_PARAMS_BLOCK_FL_ENABLE;
awb_cfg->header.size = sizeof(struct c3_isp_params_awb_config);

awb_cfg->tap_point = C3_ISP_AWB_STATS_TAP_BEFORE_WB;
awb_cfg->satur = 1;
awb_cfg->horiz_zones_num = 32;
awb_cfg->vert_zones_num = 24;

params->data_size += sizeof(struct c3_isp_params_awb_config);
```

<a id="rst-amlogic-c3-isp-uapi-data-types"></a>

## Amlogic C3 ISP uAPI data types

```{kernel-doc} include/uapi/linux/media/amlogic/c3-isp-config.h

```
