---
title: "SPEAr SDHCI Controller"
type: reference
description: "Device-tree binding reference for SPEAr SDHCI Controller."
---

This file documents differences between the core properties in [mmc.txt](<~kernel/hardware/devicetree/bindings-mmc/mmc>)
and the properties used by the sdhci-spear driver.

## Required properties:

- compatible: "st,spear300-sdhci"

## Optional properties:

- cd-gpios: card detect gpio, with zero flags.

## Example:

```dts
	sdhci@fc000000 {
		compatible = "st,spear300-sdhci";
		reg = <0xfc000000 0x1000>;
		cd-gpios = <&gpio0 6 0>;
	};
```
