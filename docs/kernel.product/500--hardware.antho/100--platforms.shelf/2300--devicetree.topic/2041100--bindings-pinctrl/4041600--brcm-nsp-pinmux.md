---
title: "Broadcom NSP (Northstar plus) IOMUX Controller"
type: reference
description: "Device-tree binding reference for Broadcom NSP (Northstar plus) IOMUX Controller."
---

The NSP IOMUX controller supports group based mux configuration. In
addition, certain pins can be muxed to GPIO function individually.

## Required properties:

- compatible:
  Must be "brcm,nsp-pinmux"

- reg:
  Should contain the register physical address and length for each of
  GPIO\_CONTROL0, GP\_AUX\_SEL and IPROC\_CONFIG IOMUX registers

## Properties in subnodes:

- function:
  The mux function to select

- groups:
  The list of groups to select with a given function

For more details, refer to
[Documentation/devicetree/bindings/pinctrl/pinctrl-bindings.txt](<~kernel/hardware/devicetree/bindings-pinctrl/pinctrl-bindings>)

## For example:

```dts
	pinmux: pinmux@1803f1c0 {
		compatible = "brcm,nsp-pinmux";
		reg = <0x1803f1c0 0x04>,
		      <0x18030028 0x04>,
		      <0x1803f408 0x04>;

		pinctrl-names = "default";
		pinctrl-0 = <&pwm>, <&gpio_b>, <&nand_sel>;

		pwm: pwm {
			function = "pwm";
			groups = "pwm0_grp", "pwm1_grp";
		};

		gpio_b: gpio_b {
			function = "gpio_b";
			groups = "gpio_b_0_grp", "gpio_b_1_grp";
		};

		nand_sel: nand_sel {
			function = "nand";
			groups = "nand_grp";
		};
	};
```

## List of supported functions and groups in Northstar Plus:

"spi": "spi\_grp"

"i2c": "i2c\_grp"

"mdio": "mdio\_grp"

"pwm": "pwm0\_grp", "pwm1\_grp", "pwm2\_grp", "pwm3\_grp"

"gpio\_b": "gpio\_b\_0\_grp", "gpio\_b\_1\_grp", "gpio\_b\_2\_grp", "gpio\_b\_3\_grp"

"uart1": "uart1\_grp"

"uart2": "uart2\_grp"

"synce": "synce\_grp"

"sata\_led\_grps": "sata0\_led\_grp", "sata1\_led\_grp"

"xtal\_out": "xtal\_out\_grp"

"sdio": "sdio\_pwr\_grp", "sdio\_1p8v\_grp"

"switch\_led": "switch\_p05\_led0\_grp", "switch\_p05\_led1\_grp"

"nand": "nand\_grp"

"emmc": "emmc\_grp"
