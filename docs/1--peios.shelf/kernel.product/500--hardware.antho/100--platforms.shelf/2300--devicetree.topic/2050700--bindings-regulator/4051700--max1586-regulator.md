---
title: "Maxim MAX1586 voltage regulator"
type: reference
description: "Device-tree binding reference for Maxim MAX1586 voltage regulator."
---

## Required properties:

- compatible: must be "maxim,max1586"
- reg: I2C slave address, usually 0x14
- v3-gain: integer specifying the V3 gain as per datasheet
  (1 + R24/R25 + R24/185.5kOhm)
- any required generic properties defined in [regulator.txt](<~kernel/hardware/devicetree/bindings-regulator/regulator>)

## Example:

```dts
	i2c_master {
		max1586@14 {
			compatible = "maxim,max1586";
			reg = <0x14>;
			v3-gain = <1000000>;

			regulators {
				vcc_core: v3 {
					regulator-name = "vcc_core";
					regulator-compatible = "Output_V3";
					regulator-min-microvolt = <1000000>;
					regulator-max-microvolt = <1705000>;
					regulator-always-on;
				};
			};
		};
	};
```
