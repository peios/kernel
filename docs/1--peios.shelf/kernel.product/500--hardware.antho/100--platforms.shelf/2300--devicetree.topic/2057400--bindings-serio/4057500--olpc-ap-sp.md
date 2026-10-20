---
title: "OLPC AP-SP serio interface"
type: reference
description: "Device-tree binding reference for OLPC AP-SP serio interface."
---

## Required properties:

- compatible : "olpc,ap-sp"
- reg : base address and length of SoC's WTM registers
- interrupts : SP-AP interrupt

## Example:

```dts
	ap-sp@d4290000 {
		compatible = "olpc,ap-sp";
		reg = <0xd4290000 0x1000>;
		interrupts = <40>;
	}
```
