---
title: "V4L2_META_FMT_UVC_MSXU_1_5 ('UVCM')"
type: reference
description: "Microsoft(R)'s UVC Payload Metadata."
---

<a id="rst-v4l2-meta-fmt-uvc-msxu-1-5-uvcm"></a>
<a id="rst-v4l2-meta-fmt-uvc-msxu-1-5"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

Microsoft(R)'s UVC Payload Metadata.

<a id="rst-description"></a>

## Description

V4L2_META_FMT_UVC_MSXU_1_5 buffers follow the metadata buffer layout of V4L2_META_FMT_UVC with the only difference that it includes all the UVC metadata in the `buffer[]` field, not just the first 2-12 bytes.

The metadata format follows the specification from Microsoft(R) \[1\].

<a id="rst-target-1"></a>

\[1\] [https://docs.microsoft.com/en-us/windows-hardware/drivers/stream/uvc-extensions-1-5](<https://docs.microsoft.com/en-us/windows-hardware/drivers/stream/uvc-extensions-1-5>)
