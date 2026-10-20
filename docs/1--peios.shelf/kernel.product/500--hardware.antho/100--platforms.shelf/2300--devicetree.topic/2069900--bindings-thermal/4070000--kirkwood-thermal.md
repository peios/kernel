---
title: "Kirkwood Thermal"
type: reference
description: "Device-tree binding reference for Kirkwood Thermal."
---

This version is for Kirkwood 88F8262 &amp; 88F6283 SoCs. Other kirkwoods
don't contain a thermal sensor.

## Required properties:

- compatible : "marvell,kirkwood-thermal"
- reg : Address range of the thermal registers

## Example:

```dts
	thermal@10078 {
		compatible = "marvell,kirkwood-thermal";
		reg = <0x10078 0x4>;
	};
```
