---
title: "== ST STMPE PWM controller =="
type: reference
description: "Device-tree binding reference for == ST STMPE PWM controller ==."
---

This is a PWM block embedded in the ST Microelectronics STMPE
(ST Multi-Purpose Expander) chips. The PWM is registered as a
subdevices of the STMPE MFD device.

## Required properties:

```text
- compatible: should be:
  - "st,stmpe-pwm"
- #pwm-cells: should be 2. See pwm.yaml in this directory for a description of
  the cells format.
```

## Example:

```dts
pwm0: pwm {
	compatible = "st,stmpe-pwm";
	#pwm-cells = <2>;
};
```
