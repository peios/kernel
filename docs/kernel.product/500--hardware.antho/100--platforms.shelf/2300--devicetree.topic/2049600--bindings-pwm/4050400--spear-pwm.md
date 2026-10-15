---
title: "== ST SPEAr SoC PWM controller =="
type: reference
description: "Device-tree binding reference for == ST SPEAr SoC PWM controller ==."
---

## Required properties:

```text
- compatible: should be one of:
  - "st,spear320-pwm"
  - "st,spear1340-pwm"
- reg: physical base address and length of the controller's registers
- #pwm-cells: should be 2. See pwm.yaml in this directory for a description of
  the cells format.
```

## Example:

```dts
        pwm: pwm@a8000000 {
            compatible ="st,spear320-pwm";
            reg = <0xa8000000 0x1000>;
            #pwm-cells = <2>;
        };
```
