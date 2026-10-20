---
title: "Device-Tree bindings for Cortina Systems Gemini Poweroff"
type: reference
description: "Device-tree binding reference for Device-Tree bindings for Cortina Systems Gemini Poweroff."
---

This is a special IP block in the Cortina Gemini SoC that only
deals with different ways to power the system down.

## Required properties:

- compatible: should be "cortina,gemini-power-controller"
- reg: should contain the physical memory base and size
- interrupts: should contain the power management interrupt

## Example:

```dts
power-controller@4b000000 {
	compatible = "cortina,gemini-power-controller";
	reg = <0x4b000000 0x100>;
	interrupts = <26 IRQ_TYPE_EDGE_FALLING>;
};
```
