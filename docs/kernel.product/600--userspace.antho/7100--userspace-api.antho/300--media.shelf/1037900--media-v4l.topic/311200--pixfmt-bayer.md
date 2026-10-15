---
title: "Raw Bayer Formats"
type: reference
description: "The raw Bayer formats are used by image sensors before much if any processing is performed on the image. The formats contain green, red and blue components, with alternating lines of red and green, and blue and green pixels in different…"
---

<a id="rst-raw-bayer-formats"></a>
<a id="rst-pixfmt-bayer"></a>

<a id="rst-description"></a>

## Description

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

The raw Bayer formats are used by image sensors before much if any processing is performed on the image. The formats contain green, red and blue components, with alternating lines of red and green, and blue and green pixels in different orders. See also [the Wikipedia article on Bayer filter](<https://en.wikipedia.org/wiki/Bayer_filter>).

- [V4L2_PIX_FMT_RAW_CRU10 ('CR10'), V4L2_PIX_FMT_RAW_CRU12 ('CR12'), V4L2_PIX_FMT_RAW_CRU14 ('CR14'), V4L2_PIX_FMT_RAW_CRU20 ('CR20')](<~kernel/userspace/userspace-api/media-v4l/pixfmt-rawnn-cru>)
- [V4L2_PIX_FMT_SRGGB8 ('RGGB'), V4L2_PIX_FMT_SGRBG8 ('GRBG'), V4L2_PIX_FMT_SGBRG8 ('GBRG'), V4L2_PIX_FMT_SBGGR8 ('BA81'),](<~kernel/userspace/userspace-api/media-v4l/pixfmt-srggb8>)
- [V4L2_PIX_FMT_PISP_COMP1_RGGB ('PC1R'), V4L2_PIX_FMT_PISP_COMP1_GRBG ('PC1G'), V4L2_PIX_FMT_PISP_COMP1_GBRG ('PC1g'), V4L2_PIX_FMT_PISP_COMP1_BGGR ('PC1B), V4L2_PIX_FMT_PISP_COMP1_MONO ('PC1M'), V4L2_PIX_FMT_PISP_COMP2_RGGB ('PC2R'), V4L2_PIX_FMT_PISP_COMP2_GRBG ('PC2G'), V4L2_PIX_FMT_PISP_COMP2_GBRG ('PC2g'), V4L2_PIX_FMT_PISP_COMP2_BGGR ('PC2B), V4L2_PIX_FMT_PISP_COMP2_MONO ('PC2M')](<~kernel/userspace/userspace-api/media-v4l/pixfmt-srggb8-pisp-comp>)
- [V4L2_PIX_FMT_SRGGB10 ('RG10'), V4L2_PIX_FMT_SGRBG10 ('BA10'), V4L2_PIX_FMT_SGBRG10 ('GB10'), V4L2_PIX_FMT_SBGGR10 ('BG10'),](<~kernel/userspace/userspace-api/media-v4l/pixfmt-srggb10>)
- [V4L2_PIX_FMT_SRGGB10P ('pRAA'), V4L2_PIX_FMT_SGRBG10P ('pgAA'), V4L2_PIX_FMT_SGBRG10P ('pGAA'), V4L2_PIX_FMT_SBGGR10P ('pBAA'),](<~kernel/userspace/userspace-api/media-v4l/pixfmt-srggb10p>)
- [V4L2_PIX_FMT_SBGGR10ALAW8 ('aBA8'), V4L2_PIX_FMT_SGBRG10ALAW8 ('aGA8'), V4L2_PIX_FMT_SGRBG10ALAW8 ('agA8'), V4L2_PIX_FMT_SRGGB10ALAW8 ('aRA8'),](<~kernel/userspace/userspace-api/media-v4l/pixfmt-srggb10alaw8>)
- [V4L2_PIX_FMT_SBGGR10DPCM8 ('bBA8'), V4L2_PIX_FMT_SGBRG10DPCM8 ('bGA8'), V4L2_PIX_FMT_SGRBG10DPCM8 ('BD10'), V4L2_PIX_FMT_SRGGB10DPCM8 ('bRA8'),](<~kernel/userspace/userspace-api/media-v4l/pixfmt-srggb10dpcm8>)
- [pixfmt-srggb10-ipu3](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/pixfmt-srggb10-ipu3.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>)
- [V4L2_PIX_FMT_SRGGB12 ('RG12'), V4L2_PIX_FMT_SGRBG12 ('BA12'), V4L2_PIX_FMT_SGBRG12 ('GB12'), V4L2_PIX_FMT_SBGGR12 ('BG12'),](<~kernel/userspace/userspace-api/media-v4l/pixfmt-srggb12>)
- [V4L2_PIX_FMT_SRGGB12P ('pRCC'), V4L2_PIX_FMT_SGRBG12P ('pgCC'), V4L2_PIX_FMT_SGBRG12P ('pGCC'), V4L2_PIX_FMT_SBGGR12P ('pBCC')](<~kernel/userspace/userspace-api/media-v4l/pixfmt-srggb12p>)
- [V4L2_PIX_FMT_SRGGB14 ('RG14'), V4L2_PIX_FMT_SGRBG14 ('GR14'), V4L2_PIX_FMT_SGBRG14 ('GB14'), V4L2_PIX_FMT_SBGGR14 ('BG14'),](<~kernel/userspace/userspace-api/media-v4l/pixfmt-srggb14>)
- [pixfmt-srggb14p](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/pixfmt-srggb14p.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>)
- [V4L2_PIX_FMT_SRGGB16 ('RG16'), V4L2_PIX_FMT_SGRBG16 ('GR16'), V4L2_PIX_FMT_SGBRG16 ('GB16'), V4L2_PIX_FMT_SBGGR16 ('BYR2'),](<~kernel/userspace/userspace-api/media-v4l/pixfmt-srggb16>)
