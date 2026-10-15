---
title: "AUO in-cell touchscreen controller using Pixcir sensors"
type: reference
description: "Device-tree binding reference for AUO in-cell touchscreen controller using Pixcir sensors."
---

## Required properties:

- compatible: must be "auo,auo\_pixcir\_ts"
- reg: I2C address of the chip
- interrupts: interrupt to which the chip is connected
- gpios: gpios the chip is connected to
  first one is the interrupt gpio and second one the reset gpio
- x-size: horizontal resolution of touchscreen
- y-size: vertical resolution of touchscreen

## Example:

```dts
	i2c@00000000 {
		/* ... */

		auo_pixcir_ts@5c {
			compatible = "auo,auo_pixcir_ts";
			reg = <0x5c>;
			interrupts = <2 IRQ_TYPE_LEVEL_HIGH>;

			gpios = <&gpf 2 0 GPIO_LEVEL_HIGH>, /* INT */
				<&gpf 5 1 GPIO_LEVEL_LOW>; /* RST */

			x-size = <800>;
			y-size = <600>;
		};

		/* ... */
	};
```
