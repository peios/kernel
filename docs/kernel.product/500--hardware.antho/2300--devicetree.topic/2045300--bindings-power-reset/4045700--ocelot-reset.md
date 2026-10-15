---
title: "Microsemi Ocelot reset controller"
type: reference
description: "Device-tree binding reference for Microsemi Ocelot reset controller."
---

The DEVCPU\_GCB:CHIP\_REGS have a SOFT\_RST register that can be used to reset the
SoC core.

The reset registers are both present in the MSCC vcoreiii MIPS and
microchip Sparx5 armv8 SoC's.

## Required Properties:

- compatible: "mscc,ocelot-chip-reset", "mscc,luton-chip-reset",
  "mscc,jaguar2-chip-reset" or "microchip,sparx5-chip-reset"

## Example:

```dts
	reset@1070008 {
		compatible = "mscc,ocelot-chip-reset";
		reg = <0x1070008 0x4>;
	};
```
