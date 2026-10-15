---
title: "Motorola CPCAP on key"
type: reference
description: "Device-tree binding reference for Motorola CPCAP on key."
---

This module is part of the CPCAP. For more details about the whole
chip see [Documentation/devicetree/bindings/mfd/motorola-cpcap.txt](<~kernel/hardware/devicetree/bindings-mfd/motorola-cpcap>).

This module provides a simple power button event via an Interrupt.

## Required properties:

```text
- compatible: should be one of the following
   - "motorola,cpcap-pwrbutton"
- interrupts: irq specifier for CPCAP's ON IRQ
```

## Example:

```dts
&cpcap {
	cpcap_pwrbutton: pwrbutton {
		compatible = "motorola,cpcap-pwrbutton";
		interrupts = <23 IRQ_TYPE_NONE>;
	};
};
```
