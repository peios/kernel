---
title: "V4L2_META_FMT_RK_ISP1_PARAMS ('rk1p'), V4L2_META_FMT_RK_ISP1_STAT_3A ('rk1s'), V4L2_META_FMT_RK_ISP1_EXT_PARAMS ('rk1e')"
type: reference
description: "The configuration of the RkISP1 ISP is performed by userspace by providing parameters for the ISP to the driver using the v4l2_meta_format interface."
---

<a id="rst-v4l2-meta-fmt-rk-isp1-params-rk1p-v4l2-meta-fmt-rk-isp1-stat-3a-rk1s-v4l2-meta-fmt-rk-isp1-ext-params-rk1e"></a>
<a id="rst-v4l2-meta-fmt-rk-isp1-stat-3a"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

<!-- c:namespace: V4L -->

<a id="rst-configuration-parameters"></a>

## Configuration parameters

The configuration of the RkISP1 ISP is performed by userspace by providing parameters for the ISP to the driver using the `v4l2_meta_format` interface.

There are two methods that allow to configure the ISP, the `fixed parameters` configuration format and the `extensible parameters` configuration format.

<a id="rst-fixed-parameters-configuration-format"></a>
<a id="rst-v4l2-meta-fmt-rk-isp1-params"></a>

### Fixed parameters configuration format

When using the fixed configuration format, parameters are passed to the [rkisp1_params](<~kernel/administration/admin-guide/media/rkisp1#rst-rkisp1-params>) metadata output video node, using the `V4L2_META_FMT_RK_ISP1_PARAMS` meta format.

The buffer contains a single instance of the C structure `rkisp1_params_cfg` defined in `rkisp1-config.h`. So the structure can be obtained from the buffer by:



```c
struct rkisp1_params_cfg *params = (struct rkisp1_params_cfg*) buffer;
```

This method supports a subset of the ISP features only, new applications should use the extensible parameters method.

<a id="rst-extensible-parameters-configuration-format"></a>
<a id="rst-v4l2-meta-fmt-rk-isp1-ext-params"></a>

### Extensible parameters configuration format

When using the extensible configuration format, parameters are passed to the [rkisp1_params](<~kernel/administration/admin-guide/media/rkisp1#rst-rkisp1-params>) metadata output video node, using the `V4L2_META_FMT_RK_ISP1_EXT_PARAMS` meta format.

The buffer contains a single instance of the C structure `rkisp1_ext_params_cfg` defined in `rkisp1-config.h`. The `rkisp1_ext_params_cfg` structure is designed to allow userspace to populate the data buffer with only the configuration data for the ISP blocks it intends to configure. The extensible parameters format design allows developers to define new block types to support new configuration parameters, and defines a versioning scheme so that it can be extended and versioned without breaking compatibility with existing applications.

For these reasons, this configuration method is preferred over the `fixed parameters` format alternative.

<!-- rkisp1_stat_buffer -->

<a id="rst-a-and-histogram-statistics"></a>

## 3A and histogram statistics

The ISP1 device collects different statistics over an input Bayer frame. Those statistics are obtained from the [rkisp1_stats](<~kernel/administration/admin-guide/media/rkisp1#rst-rkisp1-stats>) metadata capture video node, using the `v4l2_meta_format` interface. The buffer contains a single instance of the C structure `rkisp1_stat_buffer` defined in `rkisp1-config.h`. So the structure can be obtained from the buffer by:



```c
struct rkisp1_stat_buffer *stats = (struct rkisp1_stat_buffer*) buffer;
```

The statistics collected are Exposure, AWB (Auto-white balance), Histogram and AF (Auto-focus). See `rkisp1_stat_buffer` for details of the statistics.

The 3A statistics and configuration parameters described here are usually consumed and produced by dedicated user space libraries that comprise the important tuning tools using software control loop.

<a id="rst-rkisp1-uapi-data-types"></a>

### rkisp1 uAPI data types

```{kernel-doc} include/uapi/linux/rkisp1-config.h

```
