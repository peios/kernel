---
title: "Hisilicon Hi655x Voltage regulators"
type: reference
description: "Device-tree binding reference for Hisilicon Hi655x Voltage regulators."
---

## Note:

The Hi655x regulator control is managed by Hi655x PMIC.
So the node of this regulator must be child node of Hi655x
PMIC node.

The driver uses the regulator core framework, so please also
take the bindings of [regulator.txt](<~kernel/hardware/devicetree/bindings-regulator/regulator>) for reference.

## The valid names for regulators are:

LDO2\_2V8 LDO7\_SDIO LDO10\_2V85 LDO13\_1V8 LDO14\_2V8
LDO15\_1V8 LDO17\_2V5 LDO19\_3V0 LDO21\_1V8 LDO22\_1V2

## Example:

```dts
        pmic: pmic@f8000000 {
                compatible = "hisilicon,hi655x-pmic";
		...
		regulators {
			ldo2: LDO2@a21 {
				regulator-name = "LDO2_2V8";
				regulator-min-microvolt = <2500000>;
				regulator-max-microvolt = <3200000>;
				regulator-enable-ramp-delay = <120>;
			};
			...
		}
	}
```
