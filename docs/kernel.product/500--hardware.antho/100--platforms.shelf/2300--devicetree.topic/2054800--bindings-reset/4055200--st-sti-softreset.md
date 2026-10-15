---
title: "STMicroelectronics STi family Sysconfig Peripheral SoftReset Controller"
type: reference
description: "Device-tree binding reference for STMicroelectronics STi family Sysconfig Peripheral SoftReset Controller."
---

This binding describes a reset controller device that is used to enable and
disable on-chip peripheral controllers such as USB and SATA, using
"softreset" control bits found in the STi family SoC system configuration
registers.

The actual action taken when softreset is asserted is hardware dependent.
However, when asserted it may not be possible to access the hardware's
registers and after an assert/deassert sequence the hardware's previous state
may no longer be valid.

Please refer to [reset.txt](<~kernel/hardware/devicetree/bindings-reset/reset>) in this directory for common reset
controller binding usage.

## Required properties:

- compatible: Should be "st,stih407-softreset";
- #reset-cells: 1, see below

## example:

```dts
	softreset: softreset-controller {
		#reset-cells = <1>;
		compatible = "st,stih407-softreset";
	};
```

## Specifying softreset control of devices

Device nodes should specify the reset channel required in their "resets"
property, containing a phandle to the softreset device node and an
index specifying which channel to use, as described in [reset.txt](<~kernel/hardware/devicetree/bindings-reset/reset>)

## example:

```dts
	ethernet0{
		resets			= <&softreset STIH415_ETH0_SOFTRESET>;
	};
```

Macro definitions for the supported reset channels can be found in:

include/dt-bindings/reset/stih407-resets.h
