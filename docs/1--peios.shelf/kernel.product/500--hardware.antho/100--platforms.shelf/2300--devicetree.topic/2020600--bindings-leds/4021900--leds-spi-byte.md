---
title: "Single Byte SPI LED Device Driver."
type: reference
description: "Device-tree binding reference for Single Byte SPI LED Device Driver.."
---

The driver can be used for controllers with a very simple SPI protocol:

- one LED is controlled by a single byte on MOSI
- the value of the byte gives the brightness between two values (lowest to
  highest)
- no return value is necessary (no MISO signal)

The value for lowest and highest brightness is dependent on the device and
therefore on the compatible string.

Depending on the compatible string some special functions (like hardware
accelerated blinking) might can be supported too.

The driver currently only supports one LED. The properties of the LED are
configured in a sub-node in the device node.

## Required properties:

```text
- compatible: should be one of
   * "ubnt,acb-spi-led"		microcontroller (SONiX 8F26E611LA) based device
				used for example in Ubiquiti airCube ISP
```

Property rules described in [Documentation/devicetree/bindings/spi/spi-bus.txt](<~kernel/hardware/devicetree/bindings-spi/spi-bus>)
apply.

## LED sub-node properties:

- label:
  see [Documentation/devicetree/bindings/leds/common.txt](<~kernel/hardware/devicetree/bindings-leds/common>)
- default-state:
  see [Documentation/devicetree/bindings/leds/common.txt](<~kernel/hardware/devicetree/bindings-leds/common>)
  Only "on" and "off" are supported.

## Example:

```dts
led-controller@0 {
	compatible = "ubnt,acb-spi-led";
	reg = <0>;
	spi-max-frequency = <100000>;

	led {
		label = "white:status";
		default-state = "on";
	};
};
```
