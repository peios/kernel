---
title: "Cavium, Inc. OCTEON SOC SPI master controller."
type: reference
description: "Device-tree binding reference for Cavium, Inc. OCTEON SOC SPI master controller.."
---

## Required properties:

- compatible : "cavium,octeon-3010-spi"
- reg : The register base for the controller.
- interrupts : One interrupt, used by the controller.
- #address-cells : &lt;1&gt;, as required by generic SPI binding.
- #size-cells : &lt;0&gt;, also as required by generic SPI binding.

Child nodes as per the generic SPI binding.

## Example:

```dts
	spi@1070000001000 {
		compatible = "cavium,octeon-3010-spi";
		reg = <0x10700 0x00001000 0x0 0x100>;
		interrupts = <0 58>;
		#address-cells = <1>;
		#size-cells = <0>;

		eeprom@0 {
			compatible = "st,m95256", "atmel,at25";
			reg = <0>;
			spi-max-frequency = <5000000>;
			spi-cpha;
			spi-cpol;

			pagesize = <64>;
			size = <32768>;
			address-width = <16>;
		};
	};
```
