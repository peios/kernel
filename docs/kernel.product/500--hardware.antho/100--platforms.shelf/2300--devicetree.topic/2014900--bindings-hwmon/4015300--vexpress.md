---
title: "Versatile Express hwmon sensors"
type: reference
description: "Device-tree binding reference for Versatile Express hwmon sensors."
---

## Requires node properties:

- "compatible" value : one of
  "arm,vexpress-volt"
  "arm,vexpress-amp"
  "arm,vexpress-temp"
  "arm,vexpress-power"
  "arm,vexpress-energy"
- "arm,vexpress-sysreg,func" when controlled via vexpress-sysreg
  (see [Documentation/devicetree/bindings/arm/vexpress-config.yaml](<~kernel/hardware/devicetree-bindings/dt-arm/vexpress-config>)
  for more details)

## Optional node properties:

- label : string describing the monitored value

## Example:

```dts
	energy@0 {
		compatible = "arm,vexpress-energy";
		arm,vexpress-sysreg,func = <13 0>;
		label = "A15 Jcore";
	};
```
