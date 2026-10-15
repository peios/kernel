---
title: "TI Keystone Linux Overview"
type: reference
description: "Keystone range of SoCs are based on ARM Cortex-A15 MPCore Processors and c66x DSP cores. This document describes essential information required for users to run Linux on Keystone based EVMs from Texas Instruments."
---

<a id="rst-ti-keystone-linux-overview"></a>

<a id="rst-introduction"></a>

## Introduction

Keystone range of SoCs are based on ARM Cortex-A15 MPCore Processors and c66x DSP cores. This document describes essential information required for users to run Linux on Keystone based EVMs from Texas Instruments.

Following SoCs  &amp; EVMs are currently supported:-

<a id="rst-k2hk-soc-and-evm"></a>

### K2HK SoC and EVM

a.k.a Keystone 2 Hawking/Kepler SoC TCI6636K2H &amp; TCI6636K2K: See documentation at

> [http://www.ti.com/product/tci6638k2k](<http://www.ti.com/product/tci6638k2k>) [http://www.ti.com/product/tci6638k2h](<http://www.ti.com/product/tci6638k2h>)

- **EVM:**

  [http://www.advantech.com/Support/TI-EVM/EVMK2HX_sd.aspx](<http://www.advantech.com/Support/TI-EVM/EVMK2HX_sd.aspx>)

<a id="rst-k2e-soc-and-evm"></a>

### K2E SoC and EVM

a.k.a Keystone 2 Edison SoC

K2E  -  66AK2E05:

See documentation at

> [http://www.ti.com/product/66AK2E05/technicaldocuments](<http://www.ti.com/product/66AK2E05/technicaldocuments>)

- **EVM:**

  [https://www.einfochips.com/index.php/partnerships/texas-instruments/k2e-evm.html](<https://www.einfochips.com/index.php/partnerships/texas-instruments/k2e-evm.html>)

<a id="rst-k2l-soc-and-evm"></a>

### K2L SoC and EVM

a.k.a Keystone 2 Lamarr SoC

K2L  -  TCI6630K2L:

- **See documentation at**

  [http://www.ti.com/product/TCI6630K2L/technicaldocuments](<http://www.ti.com/product/TCI6630K2L/technicaldocuments>)

- **EVM:**

  [https://www.einfochips.com/index.php/partnerships/texas-instruments/k2l-evm.html](<https://www.einfochips.com/index.php/partnerships/texas-instruments/k2l-evm.html>)

<a id="rst-configuration"></a>

## Configuration

All of the K2 SoCs/EVMs share a common defconfig, keystone_defconfig and same image is used to boot on individual EVMs. The platform configuration is specified through DTS. Following are the DTS used:

> - **K2HK EVM:**
>
>   k2hk-evm.dts
>
> - **K2E EVM:**
>
>   k2e-evm.dts
>
> - **K2L EVM:**
>
>   k2l-evm.dts

The device tree documentation for the keystone machines are located at

> Documentation/devicetree/bindings/arm/ti/ti,keystone.yaml

<a id="rst-document-author"></a>

## Document Author

Murali Karicheri &lt;[m-karicheri2@ti.com](<mailto:m-karicheri2@ti.com>)&gt;

Copyright 2015 Texas Instruments
