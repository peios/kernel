---
title: "Versatile Express voltage regulators"
type: reference
description: "Device-tree binding reference for Versatile Express voltage regulators."
---

## Requires node properties:

- "compatible" value: "arm,vexpress-volt"
- "arm,vexpress-sysreg,func" when controlled via vexpress-sysreg
  (see [Documentation/devicetree/bindings/arm/vexpress-config.yaml](<~kernel/hardware/dt-arm/vexpress-config>)
  for more details)

## Required regulator properties:

- "regulator-name"
- "regulator-always-on"

## Optional regulator properties:

- "regulator-min-microvolt"
- "regulator-max-microvolt"

See [Documentation/devicetree/bindings/regulator/regulator.txt](<~kernel/hardware/devicetree/bindings-regulator/regulator>)
for more details about the regulator properties.

When no "regulator-\[min|max\]-microvolt" properties are defined,
the device is treated as fixed (or rather "read-only") regulator.

## Example:

```dts
	volt@0 {
		compatible = "arm,vexpress-volt";
		arm,vexpress-sysreg,func = <2 0>;
		regulator-name = "Cores";
		regulator-min-microvolt = <800000>;
		regulator-max-microvolt = <1050000>;
		regulator-always-on;
	};
```
