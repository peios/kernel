---
title: "Texas Instruments OMAP3 Display Subsystem"
type: reference
description: "Device-tree binding reference for Texas Instruments OMAP3 Display Subsystem."
---

See [Documentation/devicetree/bindings/display/ti/ti,omap-dss.txt](<~kernel/hardware/devicetree/bindings-display-ti/ti-omap-dss>) for generic
description about OMAP Display Subsystem bindings.

## DSS Core

## Required properties:

- compatible: "ti,omap3-dss"
- reg: address and length of the register space
- ti,hwmods: "dss\_core"
- clocks: handle to fclk
- clock-names: "fck"

## Optional nodes:

```text
- Video ports:
	- Port 0: DPI output
	- Port 1: SDI output
```

## DPI Endpoint required properties:

- data-lines: number of lines used

## SDI Endpoint required properties:

- datapairs: number of datapairs used

## DISPC

## Required properties:

- compatible: "ti,omap3-dispc"
- reg: address and length of the register space
- ti,hwmods: "dss\_dispc"
- interrupts: the DISPC interrupt
- clocks: handle to fclk
- clock-names: "fck"

## Optional properties:

- max-memory-bandwidth: Input memory (from main memory to dispc) bandwidth limit
  in bytes per second

## RFBI

## Required properties:

- compatible: "ti,omap3-rfbi"
- reg: address and length of the register space
- ti,hwmods: "dss\_rfbi"
- clocks: handles to fclk and iclk
- clock-names: "fck", "ick"

## VENC

## Required properties:

- compatible: "ti,omap3-venc"
- reg: address and length of the register space
- ti,hwmods: "dss\_venc"
- vdda-supply: power supply for DAC
- clocks: handle to fclk
- clock-names: "fck"

## VENC Endpoint required properties:

- ti,invert-polarity: invert the polarity of the video signal
- ti,channels: 1 for composite, 2 for s-video

## DSI

## Required properties:

- compatible: "ti,omap3-dsi"
- reg: addresses and lengths of the register spaces for 'proto', 'phy' and 'pll'
- reg-names: "proto", "phy", "pll"
- interrupts: the DSI interrupt line
- ti,hwmods: "dss\_dsi1"
- vdd-supply: power supply for DSI
- clocks: handles to fclk and pll clock
- clock-names: "fck", "sys\_clk"

## DSI Endpoint required properties:

- lanes: list of pin numbers for the DSI lanes: CLK+, CLK-, DATA0+, DATA0-,
  DATA1+, DATA1-, ...
