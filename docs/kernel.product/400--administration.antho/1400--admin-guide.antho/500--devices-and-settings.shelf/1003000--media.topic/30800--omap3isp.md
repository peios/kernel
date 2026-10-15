---
title: "OMAP 3 Image Signal Processor (ISP) driver"
type: reference
description: "Copyright © 2010 Nokia Corporation"
---

<a id="rst-omap-3-image-signal-processor-isp-driver"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

<!-- This data file has been placed in the public domain. -->

<!-- Derived from the Unicode character mappings available from
<http://www.w3.org/2003/entities/xml/>.
Processed by unicode2rstsubs.py, part of Docutils:
<https://docutils.sourceforge.io>. -->

Copyright © 2010 Nokia Corporation

Copyright © 2009 Texas Instruments, Inc.

Contacts: Laurent Pinchart &lt;[laurent.pinchart@ideasonboard.com](<mailto:laurent.pinchart@ideasonboard.com>)&gt;, Sakari Ailus &lt;[sakari.ailus@iki.fi](<mailto:sakari.ailus@iki.fi>)&gt;, David Cohen &lt;[dacohen@gmail.com](<mailto:dacohen@gmail.com>)&gt;

<a id="rst-introduction"></a>

## Introduction

This file documents the Texas Instruments OMAP 3 Image Signal Processor (ISP) driver located under drivers/media/platform/ti/omap3isp. The original driver was written by Texas Instruments but since that it has been rewritten (twice) at Nokia.

The driver has been successfully used on the following versions of OMAP 3:

- 3430

- 3530

- 3630

The driver implements V4L2, Media controller and v4l2_subdev interfaces. Sensor, lens and flash drivers using the v4l2_subdev interface in the kernel are supported.

<a id="rst-split-to-subdevs"></a>

## Split to subdevs

The OMAP 3 ISP is split into V4L2 subdevs, each of the blocks inside the ISP having one subdev to represent it. Each of the subdevs provide a V4L2 subdev interface to userspace.

- OMAP3 ISP CCP2

- OMAP3 ISP CSI2a

- OMAP3 ISP CCDC

- OMAP3 ISP preview

- OMAP3 ISP resizer

- OMAP3 ISP AEWB

- OMAP3 ISP AF

- OMAP3 ISP histogram

Each possible link in the ISP is modelled by a link in the Media controller interface. For an example program see <a id="rst-footnote-reference-1"></a>[1](#rst-footnote-1).

<a id="rst-controlling-the-omap-3-isp"></a>

## Controlling the OMAP 3 ISP

In general, the settings given to the OMAP 3 ISP take effect at the beginning of the following frame. This is done when the module becomes idle during the vertical blanking period on the sensor. In memory-to-memory operation the pipe is run one frame at a time. Applying the settings is done between the frames.

All the blocks in the ISP, excluding the CSI-2 and possibly the CCP2 receiver, insist on receiving complete frames. Sensors must thus never send the ISP partial frames.

Autoidle does have issues with some ISP blocks on the 3430, at least. Autoidle is only enabled on 3630 when the omap3isp module parameter autoidle is non-zero.

<a id="rst-technical-reference-manuals-trms-and-other-documentation"></a>

## Technical reference manuals (TRMs) and other documentation

OMAP 3430 TRM: &lt;URL:http://focus.ti.com/pdfs/wtbu/OMAP34xx_ES3.1.x_PUBLIC_TRM_vZM.zip&gt; Referenced 2011-03-05.

OMAP 35xx TRM: &lt;URL:http://www.ti.com/litv/pdf/spruf98o&gt; Referenced 2011-03-05.

OMAP 3630 TRM: &lt;URL:http://focus.ti.com/pdfs/wtbu/OMAP36xx_ES1.x_PUBLIC_TRM_vQ.zip&gt; Referenced 2011-03-05.

DM 3730 TRM: &lt;URL:http://www.ti.com/litv/pdf/sprugn4h&gt; Referenced 2011-03-06.

<a id="rst-references"></a>

## References

<a id="rst-footnote-1"></a>



**[1]** [http://git.ideasonboard.org/?p=media-ctl.git;a=summary](<http://git.ideasonboard.org/?p=media-ctl.git;a=summary>)
