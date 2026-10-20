---
title: "Altera Arria10 Partial Reconfiguration IP"
type: reference
description: "Device-tree binding reference for Altera Arria10 Partial Reconfiguration IP."
---

## Required properties:

- compatible : should contain "altr,a10-pr-ip"
- reg        : base address and size for memory mapped io.

## Example:

```dts
	fpga_mgr: fpga-mgr@ff20c000 {
		compatible = "altr,a10-pr-ip";
		reg = <0xff20c000 0x10>;
	};
```
