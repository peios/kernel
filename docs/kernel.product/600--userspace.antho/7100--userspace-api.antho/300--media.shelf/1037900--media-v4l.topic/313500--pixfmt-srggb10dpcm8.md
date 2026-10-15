---
title: "V4L2_PIX_FMT_SBGGR10DPCM8 ('bBA8'), V4L2_PIX_FMT_SGBRG10DPCM8 ('bGA8'), V4L2_PIX_FMT_SGRBG10DPCM8 ('BD10'), V4L2_PIX_FMT_SRGGB10DPCM8 ('bRA8'),"
type: reference
description: "man V4L2_PIX_FMT_SBGGR10DPCM8(2)"
---

<a id="rst-v4l2-pix-fmt-sbggr10dpcm8-bba8-v4l2-pix-fmt-sgbrg10dpcm8-bga8-v4l2-pix-fmt-sgrbg10dpcm8-bd10-v4l2-pix-fmt-srggb10dpcm8-bra8"></a>
<a id="rst-v4l2-pix-fmt-srggb10dpcm8"></a>
<a id="rst-v4l2-pix-fmt-sgrbg10dpcm8"></a>
<a id="rst-v4l2-pix-fmt-sgbrg10dpcm8"></a>
<a id="rst-v4l2-pix-fmt-sbggr10dpcm8"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

*man V4L2_PIX_FMT_SBGGR10DPCM8(2)*

V4L2_PIX_FMT_SGBRG10DPCM8 V4L2_PIX_FMT_SGRBG10DPCM8 V4L2_PIX_FMT_SRGGB10DPCM8 10-bit Bayer formats compressed to 8 bits

<a id="rst-description"></a>

## Description

These four pixel formats are raw sRGB / Bayer formats with 10 bits per colour compressed to 8 bits each, using DPCM compression. DPCM, differential pulse-code modulation, is lossy. Each colour component consumes 8 bits of memory. In other respects this format is similar to [V4L2_PIX_FMT_SRGGB10 ('RG10'), V4L2_PIX_FMT_SGRBG10 ('BA10'), V4L2_PIX_FMT_SGBRG10 ('GB10'), V4L2_PIX_FMT_SBGGR10 ('BG10'),](<~kernel/userspace/userspace-api/media-v4l/pixfmt-srggb10#rst-v4l2-pix-fmt-srggb10>).
