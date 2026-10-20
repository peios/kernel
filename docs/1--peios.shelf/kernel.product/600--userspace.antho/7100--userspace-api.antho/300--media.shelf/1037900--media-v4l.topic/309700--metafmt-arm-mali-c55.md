---
title: "V4L2_META_FMT_MALI_C55_STATS ('C55S'), V4L2_META_FMT_MALI_C55_PARAMS ('C55P')"
type: reference
description: "The ISP device collects different statistics over an input bayer frame. Those statistics can be obtained by userspace from the mali-c55 3a stats <mali-c55-3a-stats> metadata capture video node, using the v4l2_meta_format interface. The…"
---

<a id="rst-v4l2-meta-fmt-mali-c55-stats-c55s-v4l2-meta-fmt-mali-c55-params-c55p"></a>
<a id="rst-v4l2-meta-fmt-mali-c55-stats"></a>
<a id="rst-v4l2-meta-fmt-mali-c55-params"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

<a id="rst-a-statistics"></a>

## 3A Statistics

The ISP device collects different statistics over an input bayer frame. Those statistics can be obtained by userspace from the [mali-c55 3a stats](<~kernel/administration/admin-guide/media/mali-c55#rst-mali-c55-3a-stats>) metadata capture video node, using the `v4l2_meta_format` interface. The buffer contains a single instance of the C structure `mali_c55_stats_buffer` defined in `mali-c55-config.h`, so the structure can be obtained from the buffer by:



```C
struct mali_c55_stats_buffer *stats =
        (struct mali_c55_stats_buffer *)buf;
```

For details of the statistics see `mali_c55_stats_buffer`.

<a id="rst-configuration-parameters"></a>

## Configuration Parameters

The configuration parameters are passed to the [mali-c55 3a params](<~kernel/administration/admin-guide/media/mali-c55#rst-mali-c55-3a-params>) metadata output video node, using the `v4l2_meta_format` interface. Rather than a single struct containing sub-structs for each configurable area of the ISP, parameters for the Mali-C55 use the v4l2-isp parameters system, through which groups of parameters are defined as distinct structs or "blocks" which may be added to the data member of `v4l2_isp_params_buffer`. Userspace is responsible for populating the data member with the blocks that need to be configured by the driver.  Each block-specific struct embeds `v4l2_isp_params_block_header` as its first member and userspace must populate the type member with a value from `mali_c55_param_block_type`.



```c
struct v4l2_isp_params_buffer *params =
        (struct v4l2_isp_params_buffer *)buffer;

params->version = V4L2_ISP_PARAMS_VERSION_V1;
params->data_size = 0;

void *data = (void *)params->data;

struct mali_c55_params_awb_gains *gains =
        (struct mali_c55_params_awb_gains *)data;

gains->header.type = MALI_C55_PARAM_BLOCK_AWB_GAINS;
gains->header.flags |= V4L2_ISP_PARAMS_FL_BLOCK_ENABLE;
gains->header.size = sizeof(struct mali_c55_params_awb_gains);

gains->gain00 = 256;
gains->gain00 = 256;
gains->gain00 = 256;
gains->gain00 = 256;

data += sizeof(struct mali_c55_params_awb_gains);
params->data_size += sizeof(struct mali_c55_params_awb_gains);

struct mali_c55_params_sensor_off_preshading *blc =
        (struct mali_c55_params_sensor_off_preshading *)data;

blc->header.type = MALI_C55_PARAM_BLOCK_SENSOR_OFFS;
blc->header.flags |= V4L2_ISP_PARAMS_FL_BLOCK_ENABLE;
blc->header.size = sizeof(struct mali_c55_params_sensor_off_preshading);

blc->chan00 = 51200;
blc->chan01 = 51200;
blc->chan10 = 51200;
blc->chan11 = 51200;

params->data_size += sizeof(struct mali_c55_params_sensor_off_preshading);
```

<a id="rst-arm-mali-c55-uapi-data-types"></a>

## Arm Mali-C55 uAPI data types

```{kernel-doc} include/uapi/linux/media/arm/mali-c55-config.h

```
