---
title: "Kernel driver i2c-pca-isa"
type: reference
description: "Supported adapters:"
---

<a id="rst-kernel-driver-i2c-pca-isa"></a>

Supported adapters:

This driver supports ISA boards using the Philips PCA 9564 Parallel bus to I2C bus controller

Author: Ian Campbell &lt;[icampbell@arcom.com](<mailto:icampbell@arcom.com>)&gt;, Arcom Control Systems

<a id="rst-module-parameters"></a>

## Module Parameters

- - **base int**

    I/O base address

- - **irq int**

    IRQ interrupt

- - **clock int**

    Clock rate as described in table 1 of PCA9564 datasheet

<a id="rst-description"></a>

## Description

This driver supports ISA boards using the Philips PCA 9564 Parallel bus to I2C bus controller
