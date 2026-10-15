---
title: "Platform drivers"
type: reference
description: "There are several drivers that are focused on providing support for functionality that are already included at the main board, and don't use neither USB nor PCI bus. Those drivers are called platform drivers, and are very popular on…"
---

<a id="rst-platform-drivers"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

There are several drivers that are focused on providing support for functionality that are already included at the main board, and don't use neither USB nor PCI bus. Those drivers are called platform drivers, and are very popular on embedded devices.

The current supported of platform drivers (not including staging drivers) are listed below


<table>
<thead>
<tr>
<th>


Driver

</th>
<th>


Name

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


am437x-vpfe

</td>
<td>


TI AM437x VPFE

</td>
</tr>
<tr>
<td>


aspeed-video

</td>
<td>


Aspeed AST2400 and AST2500

</td>
</tr>
<tr>
<td>


atmel-isc

</td>
<td>


ATMEL Image Sensor Controller (ISC)

</td>
</tr>
<tr>
<td>


atmel-isi

</td>
<td>


ATMEL Image Sensor Interface (ISI)

</td>
</tr>
<tr>
<td>


cafe_ccic

</td>
<td>


Marvell 88ALP01 (Cafe) CMOS Camera Controller

</td>
</tr>
<tr>
<td>


cdns-csi2rx

</td>
<td>


Cadence MIPI-CSI2 RX Controller

</td>
</tr>
<tr>
<td>


cdns-csi2tx

</td>
<td>


Cadence MIPI-CSI2 TX Controller

</td>
</tr>
<tr>
<td>


coda-vpu

</td>
<td>


Chips&amp;Media Coda multi-standard codec IP

</td>
</tr>
<tr>
<td>


dm355_ccdc

</td>
<td>


TI DM355 CCDC video capture

</td>
</tr>
<tr>
<td>


dm644x_ccdc

</td>
<td>


TI DM6446 CCDC video capture

</td>
</tr>
<tr>
<td>


exynos-fimc-is

</td>
<td>


EXYNOS4x12 FIMC-IS (Imaging Subsystem)

</td>
</tr>
<tr>
<td>


exynos-fimc-lite

</td>
<td>


EXYNOS FIMC-LITE camera interface

</td>
</tr>
<tr>
<td>


exynos-gsc

</td>
<td>


Samsung Exynos G-Scaler

</td>
</tr>
<tr>
<td>


exy

</td>
<td>


Samsung S5P/EXYNOS4 SoC series Camera Subsystem

</td>
</tr>
<tr>
<td>


imx-pxp

</td>
<td>


i.MX Pixel Pipeline (PXP)

</td>
</tr>
<tr>
<td>


isdf

</td>
<td>


TI DM365 ISIF video capture

</td>
</tr>
<tr>
<td>


mmp_camera

</td>
<td>


Marvell Armada 610 integrated camera controller

</td>
</tr>
<tr>
<td>


mtk_jpeg

</td>
<td>


Mediatek JPEG Codec

</td>
</tr>
<tr>
<td>


mtk-mdp

</td>
<td>


Mediatek MDP

</td>
</tr>
<tr>
<td>


mtk-vcodec-dec

</td>
<td>


Mediatek Video Codec

</td>
</tr>
<tr>
<td>


mtk-vpu

</td>
<td>


Mediatek Video Processor Unit

</td>
</tr>
<tr>
<td>


mx2_emmaprp

</td>
<td>


MX2 eMMa-PrP

</td>
</tr>
<tr>
<td>


omap3-isp

</td>
<td>


OMAP 3 Camera

</td>
</tr>
<tr>
<td>


omap-vout

</td>
<td>


OMAP2/OMAP3 V4L2-Display

</td>
</tr>
<tr>
<td>


pxa_camera

</td>
<td>


PXA27x Quick Capture Interface

</td>
</tr>
<tr>
<td>


qcom-camss

</td>
<td>


Qualcomm V4L2 Camera Subsystem

</td>
</tr>
<tr>
<td>


rcar-csi2

</td>
<td>


R-Car MIPI CSI-2 Receiver

</td>
</tr>
<tr>
<td>


rcar_drif

</td>
<td>


Renesas Digital Radio Interface (DRIF)

</td>
</tr>
<tr>
<td>


rcar-fcp

</td>
<td>


Renesas Frame Compression Processor

</td>
</tr>
<tr>
<td>


rcar_fdp1

</td>
<td>


Renesas Fine Display Processor

</td>
</tr>
<tr>
<td>


rcar_jpu

</td>
<td>


Renesas JPEG Processing Unit

</td>
</tr>
<tr>
<td>


rcar-vin

</td>
<td>


R-Car Video Input (VIN)

</td>
</tr>
<tr>
<td>


renesas-ceu

</td>
<td>


Renesas Capture Engine Unit (CEU)

</td>
</tr>
<tr>
<td>


rockchip-rga

</td>
<td>


Rockchip Raster 2d Graphic Acceleration Unit

</td>
</tr>
<tr>
<td>


s3c-camif

</td>
<td>


Samsung S3C24XX/S3C64XX SoC Camera Interface

</td>
</tr>
<tr>
<td>


s5p-csis

</td>
<td>


S5P/EXYNOS MIPI-CSI2 receiver (MIPI-CSIS)

</td>
</tr>
<tr>
<td>


s5p-fimc

</td>
<td>


S5P/EXYNOS4 FIMC/CAMIF camera interface

</td>
</tr>
<tr>
<td>


s5p-g2d

</td>
<td>


Samsung S5P and EXYNOS4 G2D 2d graphics accelerator

</td>
</tr>
<tr>
<td>


s5p-jpeg

</td>
<td>


Samsung S5P/Exynos3250/Exynos4 JPEG codec

</td>
</tr>
<tr>
<td>


s5p-mfc

</td>
<td>


Samsung S5P MFC Video Codec

</td>
</tr>
<tr>
<td>


sh_veu

</td>
<td>


SuperH VEU mem2mem video processing

</td>
</tr>
<tr>
<td>


sh_vou

</td>
<td>


SuperH VOU video output

</td>
</tr>
<tr>
<td>


stm32-dcmi

</td>
<td>


STM32 Digital Camera Memory Interface (DCMI)

</td>
</tr>
<tr>
<td>


stm32-dma2d

</td>
<td>


STM32 Chrom-Art Accelerator Unit

</td>
</tr>
<tr>
<td>


sun4i-csi

</td>
<td>


Allwinner A10 CMOS Sensor Interface Support

</td>
</tr>
<tr>
<td>


sun6i-csi

</td>
<td>


Allwinner V3s Camera Sensor Interface

</td>
</tr>
<tr>
<td>


sun8i-di

</td>
<td>


Allwinner Deinterlace

</td>
</tr>
<tr>
<td>


sun8i-rotate

</td>
<td>


Allwinner DE2 rotation

</td>
</tr>
<tr>
<td>


ti-cal

</td>
<td>


TI Memory-to-memory multimedia devices

</td>
</tr>
<tr>
<td>


ti-csc

</td>
<td>


TI DVB platform devices

</td>
</tr>
<tr>
<td>


ti-vpe

</td>
<td>


TI VPE (Video Processing Engine)

</td>
</tr>
<tr>
<td>


venus-enc

</td>
<td>


Qualcomm Venus V4L2 encoder/decoder

</td>
</tr>
<tr>
<td>


via-camera

</td>
<td>


VIAFB camera controller

</td>
</tr>
<tr>
<td>


video-mux

</td>
<td>


Video Multiplexer

</td>
</tr>
<tr>
<td>


vpif_display

</td>
<td>


TI DaVinci VPIF V4L2-Display

</td>
</tr>
<tr>
<td>


vpif_capture

</td>
<td>


TI DaVinci VPIF video capture

</td>
</tr>
<tr>
<td>


vsp1

</td>
<td>


Renesas VSP1 Video Processing Engine

</td>
</tr>
<tr>
<td>


xilinx-tpg

</td>
<td>


Xilinx Video Test Pattern Generator

</td>
</tr>
<tr>
<td>


xilinx-video

</td>
<td>


Xilinx Video IP (EXPERIMENTAL)

</td>
</tr>
<tr>
<td>


xilinx-vtc

</td>
<td>


Xilinx Video Timing Controller

</td>
</tr>
</tbody>
</table>

<a id="rst-mmc-sdio-dvb-adapters"></a>

## MMC/SDIO DVB adapters


<table>
<thead>
<tr>
<th>


Driver

</th>
<th>


Name

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


smssdio

</td>
<td>


Siano SMS1xxx based MDTV via SDIO interface

</td>
</tr>
</tbody>
</table>
