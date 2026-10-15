---
title: "Clock bindings for Marvell PXA chips"
type: reference
description: "Device-tree binding reference for Clock bindings for Marvell PXA chips."
---

## Required properties:

- compatible: Should be "marvell,pxa-clocks"
- #clock-cells: Should be &lt;1&gt;

The clock consumer should specify the desired clock by having the clock
ID in its "clocks" phandle cell (see include/.../pxa-clock.h).

## Examples:

```dts
pxa2xx_clks: pxa2xx_clks@41300004 {
        compatible = "marvell,pxa-clocks";
        #clock-cells = <1>;
};
```
