---
title: "Texas Instruments OMAP4+ Digital Microphone Module"
type: reference
description: "Device-tree binding reference for Texas Instruments OMAP4+ Digital Microphone Module."
---

## Required properties:

- compatible: "ti,omap4-dmic"
- reg: Register location and size as an array:
  &lt;MPU access base address, size&gt;,
  &lt;L3 interconnect address, size&gt;;
- interrupts: Interrupt number for DMIC
- ti,hwmods: Name of the hwmod associated with OMAP dmic IP

## Example:

```dts
dmic: dmic@4012e000 {
	compatible = "ti,omap4-dmic";
	reg = <0x4012e000 0x7f>, /* MPU private access */
	      <0x4902e000 0x7f>; /* L3 Interconnect */
	interrupts = <0 114 0x4>;
	interrupt-parent = <&gic>;
	ti,hwmods = "dmic";
};
```
