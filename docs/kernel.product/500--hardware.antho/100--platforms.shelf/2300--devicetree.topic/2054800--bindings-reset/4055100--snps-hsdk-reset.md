---
title: "Binding for the Synopsys HSDK reset controller"
type: reference
description: "Device-tree binding reference for Binding for the Synopsys HSDK reset controller."
---

This binding uses the common reset binding\[1\].

\[1\] [Documentation/devicetree/bindings/reset/reset.txt](<~kernel/hardware/devicetree/bindings-reset/reset>)

## Required properties:

- compatible: should be "snps,hsdk-reset".
- reg: should always contain 2 pairs address - length: first for reset
  configuration register and second for corresponding SW reset and status bits
  register.
- #reset-cells: from common reset binding; Should always be set to 1.

## Example:

```dts
	reset: reset@880 {
		compatible = "snps,hsdk-reset";
		#reset-cells = <1>;
		reg = <0x8A0 0x4>, <0xFF0 0x4>;
	};
```

## Specifying reset lines connected to IP modules:

```dts
	ethernet@.... {
		....
		resets = <&reset HSDK_V1_ETH_RESET>;
		....
	};
```

The index could be found in &lt;dt-bindings/reset/snps,hsdk-reset.h&gt;
