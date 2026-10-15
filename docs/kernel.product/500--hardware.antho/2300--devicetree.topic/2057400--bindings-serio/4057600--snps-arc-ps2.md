---
title: "ARC PS/2 driver: PS/2 block used in some ARC FPGA's & nSIM OSCI model"
type: reference
description: "Device-tree binding reference for ARC PS/2 driver: PS/2 block used in some ARC FPGA's & nSIM OSCI model."
---

## Required properties:

- compatible		: "snps,arc\_ps2"
- reg			: offset and length (always 0x14) of registers
- interrupts		: interrupt
- interrupt-names	: name of interrupt, must be "arc\_ps2\_irq"

## Example:

```dts
serio@c9000400 {
	compatible = "snps,arc_ps2";
	reg = <0xc9000400 0x14>;
	interrupts = <13>;
	interrupt-names = "arc_ps2_irq";
}
```
