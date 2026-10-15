---
title: "GPIO Decoder DT bindings"
type: reference
description: "Device-tree binding reference for GPIO Decoder DT bindings."
---

## Required Properties:

- compatible: should be "gpio-decoder"
- gpios: a spec of gpios (at least two) to be decoded to a number with
  first entry representing the MSB.

## Optional Properties:

- decoder-max-value: Maximum possible value that can be reported by
  the gpios.
- linux,axis: the input subsystem axis to map to (ABS\_X/ABS\_Y).
  Defaults to 0 (ABS\_X).

## Example:

```dts
	gpio-decoder0 {
		compatible = "gpio-decoder";
		gpios = <&pca9536 3 GPIO_ACTIVE_HIGH>,
			<&pca9536 2 GPIO_ACTIVE_HIGH>,
			<&pca9536 1 GPIO_ACTIVE_HIGH>,
			<&pca9536 0 GPIO_ACTIVE_HIGH>;
		linux,axis = <0>; /* ABS_X */
		decoder-max-value = <9>;
	};
```
