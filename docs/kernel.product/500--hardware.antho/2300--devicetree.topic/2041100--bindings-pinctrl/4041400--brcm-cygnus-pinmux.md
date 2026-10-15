---
title: "Broadcom Cygnus IOMUX Controller"
type: reference
description: "Device-tree binding reference for Broadcom Cygnus IOMUX Controller."
---

The Cygnus IOMUX controller supports group based mux configuration. In
addition, certain pins can be muxed to GPIO function individually.

## Required properties:

- compatible:
  Must be "brcm,cygnus-pinmux"

- reg:
  Define the base and range of the I/O address space that contains the Cygnus
  IOMUX registers

## Properties in subnodes:

- function:
  The mux function to select

- groups:
  The list of groups to select with a given function

For more details, refer to
[Documentation/devicetree/bindings/pinctrl/pinctrl-bindings.txt](<~kernel/hardware/devicetree/bindings-pinctrl/pinctrl-bindings>)

## For example:

```dts
	pinmux: pinmux@0301d0c8 {
		compatible = "brcm,cygnus-pinmux";
		reg = <0x0301d0c8 0x1b0>;

		pinctrl-names = "default";
		pinctrl-0 = <&i2s0_default>;

		i2s0_default: i2s0_default {
			mux {
				function = "i2s0";
				groups = "i2s0_0_grp", "i2s0_1_grp";
			};
		};
	};
```

## List of supported functions and groups in Cygnus:

"i2s0": "i2s0\_0\_grp", "i2s0\_1\_grp"

"i2s1": "i2s1\_0\_grp", "i2s1\_1\_grp"

"i2s2": "i2s2\_0\_grp", "i2s2\_1\_grp", "i2s2\_2\_grp", "i2s2\_3\_grp", "i2s2\_4\_grp"

"spdif": "spdif\_grp"

"pwm0": "pwm0\_grp"

"pwm1": "pwm1\_grp"

"pwm2": "pwm2\_grp"

"pwm3": "pwm3\_grp"

"pwm4": "pwm4\_grp"

"pwm5": "pwm5\_grp"

"key": "key0\_grp", "key1\_grp", "key2\_grp", "key3\_grp", "key4\_grp", "key5\_grp",
"key6\_grp", "key7\_grp", "key8\_grp", "key9\_grp", "key10\_grp", "key11\_grp",
"key12\_grp", "key13\_grp", "key14\_grp", "key15\_grp"

"audio\_dte": "audio\_dte0\_grp", "audio\_dte1\_grp", "audio\_dte2\_grp", "audio\_dte3\_grp"

"smart\_card0": "smart\_card0\_grp", "smart\_card0\_fcb\_grp"

"smart\_card1": "smart\_card1\_grp", "smart\_card1\_fcb\_grp"

"spi0": "spi0\_grp"

"spi1": "spi1\_grp"

"spi2": "spi2\_grp"

"spi3": "spi3\_grp"

"spi4": "spi4\_0\_grp", "spi4\_1\_grp"

"spi5": "spi5\_grp"

"sw\_led0": "sw\_led0\_0\_grp", "sw\_led0\_1\_grp"

"sw\_led1": "sw\_led1\_grp"

"sw\_led2": "sw\_led2\_0\_grp", "sw\_led2\_1\_grp"

"d1w": "d1w\_grp"

"lcd": "lcd\_grp"

"sram": "sram\_0\_grp", "sram\_1\_grp"

"uart0": "uart0\_grp"

"uart1": "uart1\_grp", "uart1\_dte\_grp"

"uart2": "uart2\_grp"

"uart3": "uart3\_grp"

"uart4": "uart4\_grp"

"qspi": "qspi\_0\_grp", "qspi\_1\_grp"

"nand": "nand\_grp"

"sdio0": "sdio0\_grp", "sdio0\_cd\_grp", "sdio0\_mmc\_grp"

"sdio1": "sdio1\_data\_0\_grp", "sdio1\_data\_1\_grp", "sdio1\_cd\_grp",
"sdio1\_led\_grp", "sdio1\_mmc\_grp"

"can0": "can0\_grp"

"can1": "can1\_grp"

"cam": "cam\_led\_grp", "cam\_0\_grp", "cam\_1\_grp"

"bsc1": "bsc1\_grp"

"pcie\_clkreq": "pcie\_clkreq\_grp"

"usb0\_oc": "usb0\_oc\_grp"

"usb1\_oc": "usb1\_oc\_grp"

"usb2\_oc": "usb2\_oc\_grp"
