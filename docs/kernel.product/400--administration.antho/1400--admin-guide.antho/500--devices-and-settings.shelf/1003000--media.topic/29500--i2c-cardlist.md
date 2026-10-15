---
title: "I²C drivers"
type: reference
description: "The I²C (Inter-Integrated Circuit) bus is a three-wires bus used internally at the media cards for communication between different chips. While the bus is not visible to the Linux Kernel, drivers need to send and receive commands via the…"
---

<a id="rst-i2c-drivers"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

The I²C (Inter-Integrated Circuit) bus is a three-wires bus used internally at the media cards for communication between different chips. While the bus is not visible to the Linux Kernel, drivers need to send and receive commands via the bus. The Linux Kernel driver abstraction has support to implement different drivers for each component inside an I²C bus, as if the bus were visible to the main system board.

One of the problems with I²C devices is that sometimes the same device may work with different I²C hardware. This is common, for example, on devices that comes with a tuner for North America market, and another one for Europe. Some drivers have a `tuner=` modprobe parameter to allow using a different tuner number in order to address such issue.

The current supported of I²C drivers (not including staging drivers) are listed below.

<a id="rst-audio-decoders-processors-and-mixers"></a>

## Audio decoders, processors and mixers


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


cs3308

</td>
<td>


Cirrus Logic CS3308 audio ADC

</td>
</tr>
<tr>
<td>


cs5345

</td>
<td>


Cirrus Logic CS5345 audio ADC

</td>
</tr>
<tr>
<td>


cs53l32a

</td>
<td>


Cirrus Logic CS53L32A audio ADC

</td>
</tr>
<tr>
<td>


msp3400

</td>
<td>


Micronas MSP34xx audio decoders

</td>
</tr>
<tr>
<td>


sony-btf-mpx

</td>
<td>


Sony BTF's internal MPX

</td>
</tr>
<tr>
<td>


tda1997x

</td>
<td>


NXP TDA1997x HDMI receiver

</td>
</tr>
<tr>
<td>


tda7432

</td>
<td>


Philips TDA7432 audio processor

</td>
</tr>
<tr>
<td>


tda9840

</td>
<td>


Philips TDA9840 audio processor

</td>
</tr>
<tr>
<td>


tea6415c

</td>
<td>


Philips TEA6415C audio processor

</td>
</tr>
<tr>
<td>


tea6420

</td>
<td>


Philips TEA6420 audio processor

</td>
</tr>
<tr>
<td>


tlv320aic23b

</td>
<td>


Texas Instruments TLV320AIC23B audio codec

</td>
</tr>
<tr>
<td>


tvaudio

</td>
<td>


Simple audio decoder chips

</td>
</tr>
<tr>
<td>


uda1342

</td>
<td>


Philips UDA1342 audio codec

</td>
</tr>
<tr>
<td>


vp27smpx

</td>
<td>


Panasonic VP27's internal MPX

</td>
</tr>
<tr>
<td>


wm8739

</td>
<td>


Wolfson Microelectronics WM8739 stereo audio ADC

</td>
</tr>
<tr>
<td>


wm8775

</td>
<td>


Wolfson Microelectronics WM8775 audio ADC with input mixer

</td>
</tr>
</tbody>
</table>

<a id="rst-audio-video-compression-chips"></a>

## Audio/Video compression chips


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


saa6752hs

</td>
<td>


Philips SAA6752HS MPEG-2 Audio/Video Encoder

</td>
</tr>
</tbody>
</table>

<a id="rst-camera-sensor-devices"></a>

## Camera sensor devices


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


ccs

</td>
<td>


MIPI CCS compliant camera sensors (also SMIA++ and SMIA)

</td>
</tr>
<tr>
<td>


et8ek8

</td>
<td>


ET8EK8 camera sensor

</td>
</tr>
<tr>
<td>


hi556

</td>
<td>


Hynix Hi-556 sensor

</td>
</tr>
<tr>
<td>


hi846

</td>
<td>


Hynix Hi-846 sensor

</td>
</tr>
<tr>
<td>


imx208

</td>
<td>


Sony IMX208 sensor

</td>
</tr>
<tr>
<td>


imx214

</td>
<td>


Sony IMX214 sensor

</td>
</tr>
<tr>
<td>


imx219

</td>
<td>


Sony IMX219 sensor

</td>
</tr>
<tr>
<td>


imx258

</td>
<td>


Sony IMX258 sensor

</td>
</tr>
<tr>
<td>


imx274

</td>
<td>


Sony IMX274 sensor

</td>
</tr>
<tr>
<td>


imx290

</td>
<td>


Sony IMX290 sensor

</td>
</tr>
<tr>
<td>


imx319

</td>
<td>


Sony IMX319 sensor

</td>
</tr>
<tr>
<td>


imx334

</td>
<td>


Sony IMX334 sensor

</td>
</tr>
<tr>
<td>


imx355

</td>
<td>


Sony IMX355 sensor

</td>
</tr>
<tr>
<td>


imx412

</td>
<td>


Sony IMX412 sensor

</td>
</tr>
<tr>
<td>


mt9m001

</td>
<td>


mt9m001

</td>
</tr>
<tr>
<td>


mt9m111

</td>
<td>


mt9m111, mt9m112 and mt9m131

</td>
</tr>
<tr>
<td>


mt9p031

</td>
<td>


Aptina MT9P031

</td>
</tr>
<tr>
<td>


mt9t112

</td>
<td>


Aptina MT9T111/MT9T112

</td>
</tr>
<tr>
<td>


mt9v011

</td>
<td>


Micron mt9v011 sensor

</td>
</tr>
<tr>
<td>


mt9v032

</td>
<td>


Micron MT9V032 sensor

</td>
</tr>
<tr>
<td>


mt9v111

</td>
<td>


Aptina MT9V111 sensor

</td>
</tr>
<tr>
<td>


ov13858

</td>
<td>


OmniVision OV13858 sensor

</td>
</tr>
<tr>
<td>


ov13b10

</td>
<td>


OmniVision OV13B10 sensor

</td>
</tr>
<tr>
<td>


ov2640

</td>
<td>


OmniVision OV2640 sensor

</td>
</tr>
<tr>
<td>


ov2659

</td>
<td>


OmniVision OV2659 sensor

</td>
</tr>
<tr>
<td>


ov2680

</td>
<td>


OmniVision OV2680 sensor

</td>
</tr>
<tr>
<td>


ov2685

</td>
<td>


OmniVision OV2685 sensor

</td>
</tr>
<tr>
<td>


ov5640

</td>
<td>


OmniVision OV5640 sensor

</td>
</tr>
<tr>
<td>


ov5645

</td>
<td>


OmniVision OV5645 sensor

</td>
</tr>
<tr>
<td>


ov5647

</td>
<td>


OmniVision OV5647 sensor

</td>
</tr>
<tr>
<td>


ov5670

</td>
<td>


OmniVision OV5670 sensor

</td>
</tr>
<tr>
<td>


ov5675

</td>
<td>


OmniVision OV5675 sensor

</td>
</tr>
<tr>
<td>


ov5695

</td>
<td>


OmniVision OV5695 sensor

</td>
</tr>
<tr>
<td>


ov7251

</td>
<td>


OmniVision OV7251 sensor

</td>
</tr>
<tr>
<td>


ov7640

</td>
<td>


OmniVision OV7640 sensor

</td>
</tr>
<tr>
<td>


ov7670

</td>
<td>


OmniVision OV7670 sensor

</td>
</tr>
<tr>
<td>


ov772x

</td>
<td>


OmniVision OV772x sensor

</td>
</tr>
<tr>
<td>


ov7740

</td>
<td>


OmniVision OV7740 sensor

</td>
</tr>
<tr>
<td>


ov8856

</td>
<td>


OmniVision OV8856 sensor

</td>
</tr>
<tr>
<td>


ov9640

</td>
<td>


OmniVision OV9640 sensor

</td>
</tr>
<tr>
<td>


ov9650

</td>
<td>


OmniVision OV9650/OV9652 sensor

</td>
</tr>
<tr>
<td>


rj54n1cb0c

</td>
<td>


Sharp RJ54N1CB0C sensor

</td>
</tr>
<tr>
<td>


s5c73m3

</td>
<td>


Samsung S5C73M3 sensor

</td>
</tr>
<tr>
<td>


s5k4ecgx

</td>
<td>


Samsung S5K4ECGX sensor

</td>
</tr>
<tr>
<td>


s5k5baf

</td>
<td>


Samsung S5K5BAF sensor

</td>
</tr>
<tr>
<td>


s5k6a3

</td>
<td>


Samsung S5K6A3 sensor

</td>
</tr>
</tbody>
</table>

<a id="rst-flash-devices"></a>

## Flash devices


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


adp1653

</td>
<td>


ADP1653 flash

</td>
</tr>
<tr>
<td>


lm3560

</td>
<td>


LM3560 dual flash driver

</td>
</tr>
<tr>
<td>


lm3646

</td>
<td>


LM3646 dual flash driver

</td>
</tr>
</tbody>
</table>

<a id="rst-ir-i2c-driver"></a>

## IR I2C driver


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


ir-kbd-i2c

</td>
<td>


I2C module for IR

</td>
</tr>
</tbody>
</table>

<a id="rst-lens-drivers"></a>

## Lens drivers


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


ad5820

</td>
<td>


AD5820 lens voice coil

</td>
</tr>
<tr>
<td>


ak7375

</td>
<td>


AK7375 lens voice coil

</td>
</tr>
<tr>
<td>


dw9714

</td>
<td>


DW9714 lens voice coil

</td>
</tr>
<tr>
<td>


dw9768

</td>
<td>


DW9768 lens voice coil

</td>
</tr>
<tr>
<td>


dw9807-vcm

</td>
<td>


DW9807 lens voice coil

</td>
</tr>
</tbody>
</table>

<a id="rst-miscellaneous-helper-chips"></a>

## Miscellaneous helper chips


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


video-i2c

</td>
<td>


I2C transport video

</td>
</tr>
<tr>
<td>


m52790

</td>
<td>


Mitsubishi M52790 A/V switch

</td>
</tr>
<tr>
<td>


st-mipid02

</td>
<td>


STMicroelectronics MIPID02 CSI-2 to PARALLEL bridge

</td>
</tr>
<tr>
<td>


ths7303

</td>
<td>


THS7303/53 Video Amplifier

</td>
</tr>
</tbody>
</table>

<a id="rst-rds-decoders"></a>

## RDS decoders


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


saa6588

</td>
<td>


SAA6588 Radio Chip RDS decoder

</td>
</tr>
</tbody>
</table>

<a id="rst-sdr-tuner-chips"></a>

## SDR tuner chips


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


max2175

</td>
<td>


Maxim 2175 RF to Bits tuner

</td>
</tr>
</tbody>
</table>

<a id="rst-video-and-audio-decoders"></a>

## Video and audio decoders


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


cx25840

</td>
<td>


Conexant CX2584x audio/video decoders

</td>
</tr>
<tr>
<td>


saa717x

</td>
<td>


Philips SAA7171/3/4 audio/video decoders

</td>
</tr>
</tbody>
</table>

<a id="rst-video-decoders"></a>

## Video decoders


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


adv7180

</td>
<td>


Analog Devices ADV7180 decoder

</td>
</tr>
<tr>
<td>


adv7183

</td>
<td>


Analog Devices ADV7183 decoder

</td>
</tr>
<tr>
<td>


adv748x

</td>
<td>


Analog Devices ADV748x decoder

</td>
</tr>
<tr>
<td>


adv7604

</td>
<td>


Analog Devices ADV7604 decoder

</td>
</tr>
<tr>
<td>


adv7842

</td>
<td>


Analog Devices ADV7842 decoder

</td>
</tr>
<tr>
<td>


bt819

</td>
<td>


BT819A VideoStream decoder

</td>
</tr>
<tr>
<td>


bt856

</td>
<td>


BT856 VideoStream decoder

</td>
</tr>
<tr>
<td>


bt866

</td>
<td>


BT866 VideoStream decoder

</td>
</tr>
<tr>
<td>


ks0127

</td>
<td>


KS0127 video decoder

</td>
</tr>
<tr>
<td>


ml86v7667

</td>
<td>


OKI ML86V7667 video decoder

</td>
</tr>
<tr>
<td>


saa7110

</td>
<td>


Philips SAA7110 video decoder

</td>
</tr>
<tr>
<td>


saa7115

</td>
<td>


Philips SAA7111/3/4/5 video decoders

</td>
</tr>
<tr>
<td>


tc358743

</td>
<td>


Toshiba TC358743 decoder

</td>
</tr>
<tr>
<td>


tvp514x

</td>
<td>


Texas Instruments TVP514x video decoder

</td>
</tr>
<tr>
<td>


tvp5150

</td>
<td>


Texas Instruments TVP5150 video decoder

</td>
</tr>
<tr>
<td>


tvp7002

</td>
<td>


Texas Instruments TVP7002 video decoder

</td>
</tr>
<tr>
<td>


tw2804

</td>
<td>


Techwell TW2804 multiple video decoder

</td>
</tr>
<tr>
<td>


tw9903

</td>
<td>


Techwell TW9903 video decoder

</td>
</tr>
<tr>
<td>


tw9906

</td>
<td>


Techwell TW9906 video decoder

</td>
</tr>
<tr>
<td>


tw9910

</td>
<td>


Techwell TW9910 video decoder

</td>
</tr>
<tr>
<td>


vpx3220

</td>
<td>


vpx3220a, vpx3216b &amp; vpx3214c video decoders

</td>
</tr>
</tbody>
</table>

<a id="rst-video-encoders"></a>

## Video encoders


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


adv7170

</td>
<td>


Analog Devices ADV7170 video encoder

</td>
</tr>
<tr>
<td>


adv7175

</td>
<td>


Analog Devices ADV7175 video encoder

</td>
</tr>
<tr>
<td>


adv7343

</td>
<td>


ADV7343 video encoder

</td>
</tr>
<tr>
<td>


adv7393

</td>
<td>


ADV7393 video encoder

</td>
</tr>
<tr>
<td>


adv7511-v4l2

</td>
<td>


Analog Devices ADV7511 encoder

</td>
</tr>
<tr>
<td>


ak881x

</td>
<td>


AK8813/AK8814 video encoders

</td>
</tr>
<tr>
<td>


saa7127

</td>
<td>


Philips SAA7127/9 digital video encoders

</td>
</tr>
<tr>
<td>


saa7185

</td>
<td>


Philips SAA7185 video encoder

</td>
</tr>
<tr>
<td>


ths8200

</td>
<td>


Texas Instruments THS8200 video encoder

</td>
</tr>
</tbody>
</table>

<a id="rst-video-improvement-chips"></a>

## Video improvement chips


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


upd64031a

</td>
<td>


NEC Electronics uPD64031A Ghost Reduction

</td>
</tr>
<tr>
<td>


upd64083

</td>
<td>


NEC Electronics uPD64083 3-Dimensional Y/C separation

</td>
</tr>
</tbody>
</table>

<a id="rst-tuner-drivers"></a>

## Tuner drivers


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


e4000

</td>
<td>


Elonics E4000 silicon tuner

</td>
</tr>
<tr>
<td>


fc0011

</td>
<td>


Fitipower FC0011 silicon tuner

</td>
</tr>
<tr>
<td>


fc0012

</td>
<td>


Fitipower FC0012 silicon tuner

</td>
</tr>
<tr>
<td>


fc0013

</td>
<td>


Fitipower FC0013 silicon tuner

</td>
</tr>
<tr>
<td>


fc2580

</td>
<td>


FCI FC2580 silicon tuner

</td>
</tr>
<tr>
<td>


it913x

</td>
<td>


ITE Tech IT913x silicon tuner

</td>
</tr>
<tr>
<td>


m88rs6000t

</td>
<td>


Montage M88RS6000 internal tuner

</td>
</tr>
<tr>
<td>


max2165

</td>
<td>


Maxim MAX2165 silicon tuner

</td>
</tr>
<tr>
<td>


mc44s803

</td>
<td>


Freescale MC44S803 Low Power CMOS Broadband tuners

</td>
</tr>
<tr>
<td>


msi001

</td>
<td>


Mirics MSi001

</td>
</tr>
<tr>
<td>


mt2060

</td>
<td>


Microtune MT2060 silicon IF tuner

</td>
</tr>
<tr>
<td>


mt2063

</td>
<td>


Microtune MT2063 silicon IF tuner

</td>
</tr>
<tr>
<td>


mt20xx

</td>
<td>


Microtune 2032 / 2050 tuners

</td>
</tr>
<tr>
<td>


mt2131

</td>
<td>


Microtune MT2131 silicon tuner

</td>
</tr>
<tr>
<td>


mt2266

</td>
<td>


Microtune MT2266 silicon tuner

</td>
</tr>
<tr>
<td>


mxl301rf

</td>
<td>


MaxLinear MxL301RF tuner

</td>
</tr>
<tr>
<td>


mxl5005s

</td>
<td>


MaxLinear MSL5005S silicon tuner

</td>
</tr>
<tr>
<td>


mxl5007t

</td>
<td>


MaxLinear MxL5007T silicon tuner

</td>
</tr>
<tr>
<td>


qm1d1b0004

</td>
<td>


Sharp QM1D1B0004 tuner

</td>
</tr>
<tr>
<td>


qm1d1c0042

</td>
<td>


Sharp QM1D1C0042 tuner

</td>
</tr>
<tr>
<td>


qt1010

</td>
<td>


Quantek QT1010 silicon tuner

</td>
</tr>
<tr>
<td>


r820t

</td>
<td>


Rafael Micro R820T silicon tuner

</td>
</tr>
<tr>
<td>


si2157

</td>
<td>


Silicon Labs Si2157 silicon tuner

</td>
</tr>
<tr>
<td>


tuner-types

</td>
<td>


Simple tuner support

</td>
</tr>
<tr>
<td>


tda18212

</td>
<td>


NXP TDA18212 silicon tuner

</td>
</tr>
<tr>
<td>


tda18218

</td>
<td>


NXP TDA18218 silicon tuner

</td>
</tr>
<tr>
<td>


tda18250

</td>
<td>


NXP TDA18250 silicon tuner

</td>
</tr>
<tr>
<td>


tda18271

</td>
<td>


NXP TDA18271 silicon tuner

</td>
</tr>
<tr>
<td>


tda827x

</td>
<td>


Philips TDA827X silicon tuner

</td>
</tr>
<tr>
<td>


tda8290

</td>
<td>


TDA 8290/8295 + 8275(a)/18271 tuner combo

</td>
</tr>
<tr>
<td>


tda9887

</td>
<td>


TDA 9885/6/7 analog IF demodulator

</td>
</tr>
<tr>
<td>


tea5761

</td>
<td>


TEA 5761 radio tuner

</td>
</tr>
<tr>
<td>


tea5767

</td>
<td>


TEA 5767 radio tuner

</td>
</tr>
<tr>
<td>


tua9001

</td>
<td>


Infineon TUA9001 silicon tuner

</td>
</tr>
<tr>
<td>


xc2028

</td>
<td>


XCeive xc2028/xc3028 tuners

</td>
</tr>
<tr>
<td>


xc4000

</td>
<td>


Xceive XC4000 silicon tuner

</td>
</tr>
<tr>
<td>


xc5000

</td>
<td>


Xceive XC5000 silicon tuner

</td>
</tr>
</tbody>
</table>

- [Tuner cards list](<~kernel/administration/admin-guide/media/tuner-cardlist>)
- [Frontend drivers](<~kernel/administration/admin-guide/media/frontend-cardlist>)
