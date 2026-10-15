---
title: "OMAP HS USB Host TLL (Transceiver-Less Interface)"
type: reference
description: "Device-tree binding reference for OMAP HS USB Host TLL (Transceiver-Less Interface)."
---

## Required properties:

- compatible : should be "ti,usbhs-tll"
- reg : should contain one register range i.e. start and length
- interrupts : should contain the TLL module's interrupt
- ti,hwmod : must contain "usb\_tll\_hs"

## Optional properties:

- clocks: a list of phandles and clock-specifier pairs, one for each entry in
  clock-names.

```text
- clock-names: should include:
  * "usb_tll_hs_usb_ch0_clk" - USB TLL channel 0 clock
  * "usb_tll_hs_usb_ch1_clk" - USB TLL channel 1 clock
  * "usb_tll_hs_usb_ch2_clk" - USB TLL channel 2 clock
```

## Example:

```dts
	usbhstll: usbhstll@4a062000 {
		compatible = "ti,usbhs-tll";
		reg = <0x4a062000 0x1000>;
		interrupts = <78>;
		ti,hwmods = "usb_tll_hs";
	  };
```
