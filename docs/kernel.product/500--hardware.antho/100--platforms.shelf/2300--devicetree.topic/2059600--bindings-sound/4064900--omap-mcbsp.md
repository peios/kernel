---
title: "Texas Instruments OMAP2+ McBSP module"
type: reference
description: "Device-tree binding reference for Texas Instruments OMAP2+ McBSP module."
---

## Required properties:

- compatible: "ti,omap2420-mcbsp" for McBSP on OMAP2420
  "ti,omap2430-mcbsp" for McBSP on OMAP2430
  "ti,omap3-mcbsp" for McBSP on OMAP3
  "ti,omap4-mcbsp" for McBSP on OMAP4 and newer SoC
- reg: Register location and size, for OMAP4+ as an array:
  &lt;MPU access base address, size&gt;,
  &lt;L3 interconnect address, size&gt;;
- reg-names: Array of strings associated with the address space
- interrupts: Interrupt numbers for the McBSP port, as an array in case the
  McBSP IP have more interrupt lines:
  &lt;OCP compliant irq&gt;,
  &lt;TX irq&gt;,
  &lt;RX irq&gt;;
- interrupt-names: Array of strings associated with the interrupt numbers
- ti,buffer-size: Size of the FIFO on the port (OMAP2430 and newer SoC)
- ti,hwmods: Name of the hwmod associated to the McBSP port

## Example:

```dts
mcbsp2: mcbsp@49022000 {
	compatible = "ti,omap3-mcbsp";
	reg = <0x49022000 0xff>,
	      <0x49028000 0xff>;
	reg-names = "mpu", "sidetone";
	interrupts = <0 17 0x4>, /* OCP compliant interrupt */
		     <0 62 0x4>, /* TX interrupt */
		     <0 63 0x4>, /* RX interrupt */
		     <0 4 0x4>;  /* Sidetone */
	interrupt-names = "common", "tx", "rx", "sidetone";
	interrupt-parent = <&intc>;
	ti,buffer-size = <1280>;
	ti,hwmods = "mcbsp2";
};
```
