---
title: "MVEBU CPU Config registers"
type: reference
description: "Device-tree binding reference for MVEBU CPU Config registers."
---

MVEBU (Marvell SOCs: Armada 370/XP)

## Required properties:

```text
- compatible: one of:
	- "marvell,armada-370-cpu-config"
	- "marvell,armada-xp-cpu-config"
```

- reg: Should contain CPU config registers location and length, in
  their per-CPU variant

## Example:

```dts
	cpu-config@21000 {
		compatible = "marvell,armada-xp-cpu-config";
		reg = <0x21000 0x8>;
	};
```
