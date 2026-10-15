---
title: "Texas Instruments SmartReflex binding"
type: reference
description: "Device-tree binding reference for Texas Instruments SmartReflex binding."
---

SmartReflex is used to set and adjust the SoC operating points.

## Required properties:

## compatible: Shall be one of the following:

```text
	    "ti,omap3-smartreflex-core"
	    "ti,omap3-smartreflex-mpu-iva"
	    "ti,omap4-smartreflex-core"
	    "ti,omap4-smartreflex-mpu"
	    "ti,omap4-smartreflex-iva"
```

reg: Shall contain the device instance IO range

interrupts: Shall contain the device instance interrupt

## Optional properties:

ti,hwmods: Shall contain the TI interconnect module name if needed

```text
	   by the SoC
```

## Example:

```dts
	smartreflex_iva: smartreflex@4a0db000 {
		compatible = "ti,omap4-smartreflex-iva";
		reg = <0x4a0db000 0x80>;
		interrupts = <GIC_SPI 102 IRQ_TYPE_LEVEL_HIGH>;
		ti,hwmods = "smartreflex_iva";
	};
```

```dts
	smartreflex_core: smartreflex@4a0dd000 {
		compatible = "ti,omap4-smartreflex-core";
		reg = <0x4a0dd000 0x80>;
		interrupts = <GIC_SPI 19 IRQ_TYPE_LEVEL_HIGH>;
		ti,hwmods = "smartreflex_core";
	};
```

```dts
	smartreflex_mpu: smartreflex@4a0d9000 {
		compatible = "ti,omap4-smartreflex-mpu";
		reg = <0x4a0d9000 0x80>;
		interrupts = <GIC_SPI 18 IRQ_TYPE_LEVEL_HIGH>;
		ti,hwmods = "smartreflex_mpu";
	};
```
