---
title: "Texas Instruments OMAP2 Display Subsystem"
type: reference
description: "Device-tree binding reference for Texas Instruments OMAP2 Display Subsystem."
---

See [Documentation/devicetree/bindings/display/ti/ti,omap-dss.txt](<~kernel/hardware/devicetree/bindings-display-ti/ti-omap-dss>) for generic
description about OMAP Display Subsystem bindings.

## DSS Core

## Required properties:

- compatible: "ti,omap2-dss"
- reg: address and length of the register space
- ti,hwmods: "dss\_core"

## Optional nodes:

- Video port for DPI output

## DPI Endpoint required properties:

- data-lines: number of lines used

## DISPC

## Required properties:

- compatible: "ti,omap2-dispc"
- reg: address and length of the register space
- ti,hwmods: "dss\_dispc"
- interrupts: the DISPC interrupt

## Optional properties:

- max-memory-bandwidth: Input memory (from main memory to dispc) bandwidth limit
  in bytes per second

## RFBI

## Required properties:

- compatible: "ti,omap2-rfbi"
- reg: address and length of the register space
- ti,hwmods: "dss\_rfbi"

## VENC

## Required properties:

- compatible: "ti,omap2-venc"
- reg: address and length of the register space
- ti,hwmods: "dss\_venc"
- vdda-supply: power supply for DAC

## VENC Endpoint required properties:

## Required properties:

- ti,invert-polarity: invert the polarity of the video signal
- ti,channels: 1 for composite, 2 for s-video
