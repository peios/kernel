---
title: "How to set up the Technisat/B2C2 Flexcop devices"
type: reference
description: "Author: Uwe Bugla <uwe.bugla@gmx.de> August 2009"
---

<a id="rst-how-to-set-up-the-technisat-b2c2-flexcop-devices"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

> [!NOTE]
>
> This documentation is outdated.

Author: Uwe Bugla &lt;[uwe.bugla@gmx.de](<mailto:uwe.bugla@gmx.de>)&gt; August 2009

<a id="rst-find-out-what-device-you-have"></a>

## Find out what device you have

Important Notice: The driver does NOT support Technisat USB 2 devices\!

First start your linux box with a shipped kernel:



```none
lspci -vvv for a PCI device (lsusb -vvv for an USB device) will show you for example:
02:0b.0 Network controller: Techsan Electronics Co Ltd B2C2 FlexCopII DVB chip /
Technisat SkyStar2 DVB card (rev 02)

dmesg | grep frontend may show you for example:
DVB: registering frontend 0 (Conexant CX24123/CX24109)...
```

<a id="rst-kernel-compilation"></a>

## Kernel compilation:

If the Flexcop / Technisat is the only DVB / TV / Radio device in your box get rid of unnecessary modules and check this one:

`Multimedia support` =&gt; `Customise analog and hybrid tuner modules to build`

In this directory uncheck every driver which is activated there (except `Simple tuner support` for ATSC 3rd generation only -&gt; see case 9 please).

Then please activate:

- Main module part:

  `Multimedia support` =&gt; `DVB/ATSC adapters` =&gt; `Technisat/B2C2 FlexcopII(b) and FlexCopIII adapters`

  1. =&gt; `Technisat/B2C2 Air/Sky/Cable2PC PCI` (PCI card) or

  2. =&gt; `Technisat/B2C2 Air/Sky/Cable2PC USB` (USB 1.1 adapter) and for troubleshooting purposes:

  3. =&gt; `Enable debug for the B2C2 FlexCop drivers`

- Frontend / Tuner / Demodulator module part:

  - **`Multimedia support` =&gt; `DVB/ATSC adapters`**

    =&gt; `Customise the frontend modules to build` `Customise DVB frontends` =&gt;

  - SkyStar DVB-S Revision 2.3:

    1. =&gt; `Zarlink VP310/MT312/ZL10313 based`

    2. =&gt; `Generic I2C PLL based tuners`

  - SkyStar DVB-S Revision 2.6:

    1. =&gt; `ST STV0299 based`

    2. =&gt; `Generic I2C PLL based tuners`

  - SkyStar DVB-S Revision 2.7:

    1. =&gt; `Samsung S5H1420 based`

    2. =&gt; `Integrant ITD1000 Zero IF tuner for DVB-S/DSS`

    3. =&gt; `ISL6421 SEC controller`

  - SkyStar DVB-S Revision 2.8:

    1. =&gt; `Conexant CX24123 based`

    2. =&gt; `Conexant CX24113/CX24128 tuner for DVB-S/DSS`

    3. =&gt; `ISL6421 SEC controller`

  - AirStar DVB-T card:

    1. =&gt; `Zarlink MT352 based`

    2. =&gt; `Generic I2C PLL based tuners`

  - CableStar DVB-C card:

    1. =&gt; `ST STV0297 based`

    2. =&gt; `Generic I2C PLL based tuners`

  - AirStar ATSC card 1st generation:

    1. =&gt; `Broadcom BCM3510`

  - AirStar ATSC card 2nd generation:

    1. =&gt; `NxtWave Communications NXT2002/NXT2004 based`

    2. =&gt; `Generic I2C PLL based tuners`

  - AirStar ATSC card 3rd generation:

    1. =&gt; `LG Electronics LGDT3302/LGDT3303 based`

    2. `Multimedia support` =&gt; `Customise analog and hybrid tuner modules to build` =&gt; `Simple tuner support`
