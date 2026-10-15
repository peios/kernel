---
title: "Binding for Texas Instruments clockdomain."
type: reference
description: "Device-tree binding reference for Binding for Texas Instruments clockdomain.."
---

This binding uses the common clock binding\[1\] in consumer role.
Every clock on TI SoC belongs to one clockdomain, but software
only needs this information for specific clocks which require
their parent clockdomain to be controlled when the clock is
enabled/disabled. This binding doesn't define a new clock
binding type, it is used to group existing clock nodes under
hardware hierarchy.

\[1\] [Documentation/devicetree/bindings/clock/clock-bindings.txt](<~kernel/hardware/devicetree/bindings-clock/clock-bindings>)

## Required properties:

- compatible : shall be "ti,clockdomain"
- #clock-cells : from common clock binding; shall be set to 0.
- clocks : link phandles of clocks within this domain

## Optional properties:

- clock-output-names : from common clock binding.

## Examples:

```dts
	dss_clkdm: dss_clkdm {
		compatible = "ti,clockdomain";
		clocks = <&dss1_alwon_fck_3430es2>, <&dss_ick_3430es2>;
	};
```
