---
title: "MediaTek g3dsys controller"
type: reference
description: "Device-tree binding reference for MediaTek g3dsys controller."
---

The MediaTek g3dsys controller provides various clocks and reset controller to
the GPU.

## Required Properties:

```text
- compatible: Should be:
	- "mediatek,mt2701-g3dsys", "syscon":
		for MT2701 SoC
	- "mediatek,mt7623-g3dsys", "mediatek,mt2701-g3dsys", "syscon":
		for MT7623 SoC
- #clock-cells: Must be 1
- #reset-cells: Must be 1
```

The g3dsys controller uses the common clk binding from
[Documentation/devicetree/bindings/clock/clock-bindings.txt](<~kernel/hardware/devicetree/bindings-clock/clock-bindings>)
The available clocks are defined in dt-bindings/clock/mt\*-clk.h.

## Example:

```dts
g3dsys: clock-controller@13000000 {
	compatible = "mediatek,mt7623-g3dsys",
		     "mediatek,mt2701-g3dsys",
		     "syscon";
	reg = <0 0x13000000 0 0x200>;
	#clock-cells = <1>;
	#reset-cells = <1>;
};
```
