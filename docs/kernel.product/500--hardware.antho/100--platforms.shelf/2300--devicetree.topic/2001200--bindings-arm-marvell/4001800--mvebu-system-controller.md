---
title: "MVEBU System Controller"
type: reference
description: "Device-tree binding reference for MVEBU System Controller."
---

MVEBU (Marvell SOCs: Armada 370/375/XP, Dove, mv78xx0, Kirkwood, Orion5x)

## Required properties:

```text
- compatible: one of:
	- "marvell,orion-system-controller"
	- "marvell,armada-370-xp-system-controller"
	- "marvell,armada-375-system-controller"
- reg: Should contain system controller registers location and length.
```

## Example:

```dts
	system-controller@d0018200 {
		compatible = "marvell,armada-370-xp-system-controller";
		reg = <0xd0018200 0x500>;
	};
```
