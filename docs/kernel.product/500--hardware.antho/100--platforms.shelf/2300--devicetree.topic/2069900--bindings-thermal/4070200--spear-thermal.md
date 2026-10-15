---
title: "SPEAr Thermal"
type: reference
description: "Device-tree binding reference for SPEAr Thermal."
---

## Required properties:

- compatible : "st,thermal-spear1340"
- reg : Address range of the thermal registers
- st,thermal-flags: flags used to enable thermal sensor

## Example:

```dts
	thermal@fc000000 {
		compatible = "st,thermal-spear1340";
		reg = <0xfc000000 0x1000>;
		st,thermal-flags = <0x7000>;
	};
```
