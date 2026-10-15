---
title: "Frontend drivers"
type: reference
description: "Reference for Frontend drivers."
---

<a id="rst-frontend-drivers"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

> [!NOTE]
>
> 1. There is no guarantee that every frontend driver works out of the box with every card, because of different wiring.
>
> 2. The demodulator chips can be used with a variety of tuner/PLL chips, and not all combinations are supported. Often the demodulator and tuner/PLL chip are inside a metal box for shielding, and the whole metal box has its own part number.

<a id="rst-common-interface-en50221-controller-drivers"></a>

## Common Interface (EN50221) controller drivers


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


cxd2099

</td>
<td>


Sony CXD2099AR Common Interface driver

</td>
</tr>
<tr>
<td>


sp2

</td>
<td>


CIMaX SP2

</td>
</tr>
</tbody>
</table>

<a id="rst-atsc-north-american-korean-terrestrial-cable-dtv-frontends"></a>

## ATSC (North American/Korean Terrestrial/Cable DTV) frontends


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


au8522_dig

</td>
<td>


Auvitek AU8522 based DTV demod

</td>
</tr>
<tr>
<td>


au8522_decoder

</td>
<td>


Auvitek AU8522 based ATV demod

</td>
</tr>
<tr>
<td>


bcm3510

</td>
<td>


Broadcom BCM3510

</td>
</tr>
<tr>
<td>


lg2160

</td>
<td>


LG Electronics LG216x based

</td>
</tr>
<tr>
<td>


lgdt3305

</td>
<td>


LG Electronics LGDT3304 and LGDT3305 based

</td>
</tr>
<tr>
<td>


lgdt3306a

</td>
<td>


LG Electronics LGDT3306A based

</td>
</tr>
<tr>
<td>


lgdt330x

</td>
<td>


LG Electronics LGDT3302/LGDT3303 based

</td>
</tr>
<tr>
<td>


nxt200x

</td>
<td>


NxtWave Communications NXT2002/NXT2004 based

</td>
</tr>
<tr>
<td>


or51132

</td>
<td>


Oren OR51132 based

</td>
</tr>
<tr>
<td>


or51211

</td>
<td>


Oren OR51211 based

</td>
</tr>
<tr>
<td>


s5h1409

</td>
<td>


Samsung S5H1409 based

</td>
</tr>
<tr>
<td>


s5h1411

</td>
<td>


Samsung S5H1411 based

</td>
</tr>
</tbody>
</table>

<a id="rst-dvb-c-cable-frontends"></a>

## DVB-C (cable) frontends


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


stv0297

</td>
<td>


ST STV0297 based

</td>
</tr>
<tr>
<td>


tda10021

</td>
<td>


Philips TDA10021 based

</td>
</tr>
<tr>
<td>


tda10023

</td>
<td>


Philips TDA10023 based

</td>
</tr>
<tr>
<td>


ves1820

</td>
<td>


VLSI VES1820 based

</td>
</tr>
</tbody>
</table>

<a id="rst-dvb-s-satellite-frontends"></a>

## DVB-S (satellite) frontends


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


cx24110

</td>
<td>


Conexant CX24110 based

</td>
</tr>
<tr>
<td>


cx24116

</td>
<td>


Conexant CX24116 based

</td>
</tr>
<tr>
<td>


cx24117

</td>
<td>


Conexant CX24117 based

</td>
</tr>
<tr>
<td>


cx24120

</td>
<td>


Conexant CX24120 based

</td>
</tr>
<tr>
<td>


cx24123

</td>
<td>


Conexant CX24123 based

</td>
</tr>
<tr>
<td>


ds3000

</td>
<td>


Montage Technology DS3000 based

</td>
</tr>
<tr>
<td>


mb86a16

</td>
<td>


Fujitsu MB86A16 based

</td>
</tr>
<tr>
<td>


mt312

</td>
<td>


Zarlink VP310/MT312/ZL10313 based

</td>
</tr>
<tr>
<td>


s5h1420

</td>
<td>


Samsung S5H1420 based

</td>
</tr>
<tr>
<td>


si21xx

</td>
<td>


Silicon Labs SI21XX based

</td>
</tr>
<tr>
<td>


stb6000

</td>
<td>


ST STB6000 silicon tuner

</td>
</tr>
<tr>
<td>


stv0288

</td>
<td>


ST STV0288 based

</td>
</tr>
<tr>
<td>


stv0299

</td>
<td>


ST STV0299 based

</td>
</tr>
<tr>
<td>


stv0900

</td>
<td>


ST STV0900 based

</td>
</tr>
<tr>
<td>


stv6110

</td>
<td>


ST STV6110 silicon tuner

</td>
</tr>
<tr>
<td>


tda10071

</td>
<td>


NXP TDA10071

</td>
</tr>
<tr>
<td>


tda10086

</td>
<td>


Philips TDA10086 based

</td>
</tr>
<tr>
<td>


tda8083

</td>
<td>


Philips TDA8083 based

</td>
</tr>
<tr>
<td>


tda8261

</td>
<td>


Philips TDA8261 based

</td>
</tr>
<tr>
<td>


tda826x

</td>
<td>


Philips TDA826X silicon tuner

</td>
</tr>
<tr>
<td>


ts2020

</td>
<td>


Montage Technology TS2020 based tuners

</td>
</tr>
<tr>
<td>


tua6100

</td>
<td>


Infineon TUA6100 PLL

</td>
</tr>
<tr>
<td>


cx24113

</td>
<td>


Conexant CX24113/CX24128 tuner for DVB-S/DSS

</td>
</tr>
<tr>
<td>


itd1000

</td>
<td>


Integrant ITD1000 Zero IF tuner for DVB-S/DSS

</td>
</tr>
<tr>
<td>


ves1x93

</td>
<td>


VLSI VES1893 or VES1993 based

</td>
</tr>
<tr>
<td>


zl10036

</td>
<td>


Zarlink ZL10036 silicon tuner

</td>
</tr>
<tr>
<td>


zl10039

</td>
<td>


Zarlink ZL10039 silicon tuner

</td>
</tr>
</tbody>
</table>

<a id="rst-dvb-t-terrestrial-frontends"></a>

## DVB-T (terrestrial) frontends


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


af9013

</td>
<td>


Afatech AF9013 demodulator

</td>
</tr>
<tr>
<td>


cx22700

</td>
<td>


Conexant CX22700 based

</td>
</tr>
<tr>
<td>


cx22702

</td>
<td>


Conexant cx22702 demodulator (OFDM)

</td>
</tr>
<tr>
<td>


cxd2820r

</td>
<td>


Sony CXD2820R

</td>
</tr>
<tr>
<td>


cxd2841er

</td>
<td>


Sony CXD2841ER

</td>
</tr>
<tr>
<td>


cxd2880

</td>
<td>


Sony CXD2880 DVB-T2/T tuner + demodulator

</td>
</tr>
<tr>
<td>


dib3000mb

</td>
<td>


DiBcom 3000M-B

</td>
</tr>
<tr>
<td>


dib3000mc

</td>
<td>


DiBcom 3000P/M-C

</td>
</tr>
<tr>
<td>


dib7000m

</td>
<td>


DiBcom 7000MA/MB/PA/PB/MC

</td>
</tr>
<tr>
<td>


dib7000p

</td>
<td>


DiBcom 7000PC

</td>
</tr>
<tr>
<td>


dib9000

</td>
<td>


DiBcom 9000

</td>
</tr>
<tr>
<td>


drxd

</td>
<td>


Micronas DRXD driver

</td>
</tr>
<tr>
<td>


ec100

</td>
<td>


E3C EC100

</td>
</tr>
<tr>
<td>


l64781

</td>
<td>


LSI L64781

</td>
</tr>
<tr>
<td>


mt352

</td>
<td>


Zarlink MT352 based

</td>
</tr>
<tr>
<td>


nxt6000

</td>
<td>


NxtWave Communications NXT6000 based

</td>
</tr>
<tr>
<td>


rtl2830

</td>
<td>


Realtek RTL2830 DVB-T

</td>
</tr>
<tr>
<td>


rtl2832

</td>
<td>


Realtek RTL2832 DVB-T

</td>
</tr>
<tr>
<td>


rtl2832_sdr

</td>
<td>


Realtek RTL2832 SDR

</td>
</tr>
<tr>
<td>


s5h1432

</td>
<td>


Samsung s5h1432 demodulator (OFDM)

</td>
</tr>
<tr>
<td>


si2168

</td>
<td>


Silicon Labs Si2168

</td>
</tr>
<tr>
<td>


sp8870

</td>
<td>


Spase sp8870 based

</td>
</tr>
<tr>
<td>


sp887x

</td>
<td>


Spase sp887x based

</td>
</tr>
<tr>
<td>


stv0367

</td>
<td>


ST STV0367 based

</td>
</tr>
<tr>
<td>


tda10048

</td>
<td>


Philips TDA10048HN based

</td>
</tr>
<tr>
<td>


tda1004x

</td>
<td>


Philips TDA10045H/TDA10046H based

</td>
</tr>
<tr>
<td>


zd1301_demod

</td>
<td>


ZyDAS ZD1301

</td>
</tr>
<tr>
<td>


zl10353

</td>
<td>


Zarlink ZL10353 based

</td>
</tr>
</tbody>
</table>

<a id="rst-digital-terrestrial-only-tuners-pll"></a>

## Digital terrestrial only tuners/PLL


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


dvb-pll

</td>
<td>


Generic I2C PLL based tuners

</td>
</tr>
<tr>
<td>


dib0070

</td>
<td>


DiBcom DiB0070 silicon base-band tuner

</td>
</tr>
<tr>
<td>


dib0090

</td>
<td>


DiBcom DiB0090 silicon base-band tuner

</td>
</tr>
</tbody>
</table>

<a id="rst-isdb-s-satellite-isdb-t-terrestrial-frontends"></a>

## ISDB-S (satellite) &amp; ISDB-T (terrestrial) frontends


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


mn88443x

</td>
<td>


Socionext MN88443x

</td>
</tr>
<tr>
<td>


tc90522

</td>
<td>


Toshiba TC90522

</td>
</tr>
</tbody>
</table>

<a id="rst-isdb-t-terrestrial-frontends"></a>

## ISDB-T (terrestrial) frontends


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


dib8000

</td>
<td>


DiBcom 8000MB/MC

</td>
</tr>
<tr>
<td>


mb86a20s

</td>
<td>


Fujitsu mb86a20s

</td>
</tr>
<tr>
<td>


s921

</td>
<td>


Sharp S921 frontend

</td>
</tr>
</tbody>
</table>

<a id="rst-multistandard-cable-terrestrial-frontends"></a>

## Multistandard (cable + terrestrial) frontends


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


drxk

</td>
<td>


Micronas DRXK based

</td>
</tr>
<tr>
<td>


mn88472

</td>
<td>


Panasonic MN88472

</td>
</tr>
<tr>
<td>


mn88473

</td>
<td>


Panasonic MN88473

</td>
</tr>
<tr>
<td>


si2165

</td>
<td>


Silicon Labs si2165 based

</td>
</tr>
<tr>
<td>


tda18271c2dd

</td>
<td>


NXP TDA18271C2 silicon tuner

</td>
</tr>
</tbody>
</table>

<a id="rst-multistandard-satellite-frontends"></a>

## Multistandard (satellite) frontends


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


m88ds3103

</td>
<td>


Montage Technology M88DS3103

</td>
</tr>
<tr>
<td>


mxl5xx

</td>
<td>


MaxLinear MxL5xx based tuner-demodulators

</td>
</tr>
<tr>
<td>


stb0899

</td>
<td>


STB0899 based

</td>
</tr>
<tr>
<td>


stb6100

</td>
<td>


STB6100 based tuners

</td>
</tr>
<tr>
<td>


stv090x

</td>
<td>


STV0900/STV0903(A/B) based

</td>
</tr>
<tr>
<td>


stv0910

</td>
<td>


STV0910 based

</td>
</tr>
<tr>
<td>


stv6110x

</td>
<td>


STV6110/(A) based tuners

</td>
</tr>
<tr>
<td>


stv6111

</td>
<td>


STV6111 based tuners

</td>
</tr>
</tbody>
</table>

<a id="rst-sec-control-devices-for-dvb-s"></a>

## SEC control devices for DVB-S


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


a8293

</td>
<td>


Allegro A8293

</td>
</tr>
<tr>
<td>


af9033

</td>
<td>


Afatech AF9033 DVB-T demodulator

</td>
</tr>
<tr>
<td>


ascot2e

</td>
<td>


Sony Ascot2E tuner

</td>
</tr>
<tr>
<td>


atbm8830

</td>
<td>


AltoBeam ATBM8830/8831 DMB-TH demodulator

</td>
</tr>
<tr>
<td>


drx39xyj

</td>
<td>


Micronas DRX-J demodulator

</td>
</tr>
<tr>
<td>


helene

</td>
<td>


Sony HELENE Sat/Ter tuner (CXD2858ER)

</td>
</tr>
<tr>
<td>


horus3a

</td>
<td>


Sony Horus3A tuner

</td>
</tr>
<tr>
<td>


isl6405

</td>
<td>


ISL6405 SEC controller

</td>
</tr>
<tr>
<td>


isl6421

</td>
<td>


ISL6421 SEC controller

</td>
</tr>
<tr>
<td>


isl6423

</td>
<td>


ISL6423 SEC controller

</td>
</tr>
<tr>
<td>


ix2505v

</td>
<td>


Sharp IX2505V silicon tuner

</td>
</tr>
<tr>
<td>


lgs8gl5

</td>
<td>


Silicon Legend LGS-8GL5 demodulator (OFDM)

</td>
</tr>
<tr>
<td>


lgs8gxx

</td>
<td>


Legend Silicon LGS8913/LGS8GL5/LGS8GXX DMB-TH demodulator

</td>
</tr>
<tr>
<td>


lnbh25

</td>
<td>


LNBH25 SEC controller

</td>
</tr>
<tr>
<td>


lnbh29

</td>
<td>


LNBH29 SEC controller

</td>
</tr>
<tr>
<td>


lnbp21

</td>
<td>


LNBP21/LNBH24 SEC controllers

</td>
</tr>
<tr>
<td>


lnbp22

</td>
<td>


LNBP22 SEC controllers

</td>
</tr>
<tr>
<td>


m88rs2000

</td>
<td>


M88RS2000 DVB-S demodulator and tuner

</td>
</tr>
<tr>
<td>


tda665x

</td>
<td>


TDA665x tuner

</td>
</tr>
</tbody>
</table>

<a id="rst-tools-to-develop-new-frontends"></a>

## Tools to develop new frontends


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


dvb_dummy_fe

</td>
<td>


Dummy frontend driver

</td>
</tr>
</tbody>
</table>
