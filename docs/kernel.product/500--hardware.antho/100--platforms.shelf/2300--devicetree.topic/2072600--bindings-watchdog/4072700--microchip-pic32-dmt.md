---
title: "Microchip PIC32 Deadman Timer"
type: reference
description: "Device-tree binding reference for Microchip PIC32 Deadman Timer."
---

The deadman timer is used to reset the processor in the event of a software
malfunction. It is a free-running instruction fetch timer, which is clocked
whenever an instruction fetch occurs until a count match occurs.

## Required properties:

- compatible: must be "microchip,pic32mzda-dmt".
- reg: physical base address of the controller and length of memory mapped
  region.
- clocks: phandle of source clk. Should be &lt;&amp;rootclk PB7CLK&gt;.

## Example:

```dts
	watchdog@1f800a00 {
		compatible = "microchip,pic32mzda-dmt";
		reg = <0x1f800a00 0x80>;
		clocks = <&rootclk PB7CLK>;
	};
```
