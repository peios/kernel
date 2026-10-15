---
title: "VIA/Wondermedia Graphics Engine Controller"
type: reference
description: "Device-tree binding reference for VIA/Wondermedia Graphics Engine Controller."
---

## Required properties:

- compatible : "wm,prizm-ge-rops"
- reg : Should contain 1 register ranges(address and length)

## Example:

```dts
	ge_rops@d8050400 {
		compatible = "wm,prizm-ge-rops";
		reg = <0xd8050400 0x100>;
	};
```
