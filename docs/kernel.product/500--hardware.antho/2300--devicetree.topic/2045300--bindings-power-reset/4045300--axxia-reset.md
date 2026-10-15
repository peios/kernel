---
title: "Axxia Restart Driver"
type: reference
description: "Device-tree binding reference for Axxia Restart Driver."
---

This driver can do reset of the Axxia SoC. It uses the registers in the syscon
block to initiate a chip reset.

## Required Properties:

```text
  -compatible: "lsi,axm55xx-reset"
  -syscon: phandle to the syscon node.
```

## Example:

```dts
	syscon: syscon@2010030000 {
		compatible = "lsi,axxia-syscon", "syscon";
		reg = <0x20 0x10030000 0 0x2000>;
	};
```

```dts
	reset: reset@2010031000 {
		compatible = "lsi,axm55xx-reset";
		syscon = <&syscon>;
	};
```
