---
title: "St,clkgen bindings"
type: reference
description: "Device-tree binding reference for St,clkgen bindings."
---

Binding for a Clockgen hardware block found on
certain STMicroelectronics consumer electronics SoC devices.

A Clockgen node can contain pll, diviser or multiplexer nodes.

We will find only the base address of the Clockgen, this base
address is common of all subnode.

```dts
	clockgen_node {
		reg = <>;

		pll_node {
			...
		};

		quadfs_node {
			...
		};

		mux_node {
			...
		};

		flexgen_node {
			...
		};
		...
	};
```

This binding uses the common clock binding\[1\].
Each subnode should use the binding described in \[2\]..\[7\]

\[1\] [Documentation/devicetree/bindings/clock/clock-bindings.txt](<~kernel/hardware/devicetree/bindings-clock/clock-bindings>)
\[3\] [Documentation/devicetree/bindings/clock/st/st,clkgen-mux.txt](<~kernel/hardware/devicetree/bindings-clock-st/st-clkgen-mux>)
\[4\] [Documentation/devicetree/bindings/clock/st/st,clkgen-pll.txt](<~kernel/hardware/devicetree/bindings-clock-st/st-clkgen-pll>)
\[7\] [Documentation/devicetree/bindings/clock/st/st,quadfs.txt](<~kernel/hardware/devicetree/bindings-clock-st/st-quadfs>)
\[8\] [Documentation/devicetree/bindings/clock/st/st,flexgen.txt](<~kernel/hardware/devicetree/bindings-clock-st/st-flexgen>)

## Required properties:

- reg : A Base address and length of the register set.

## Example:

```dts
	clockgen-a@90ff000 {
		compatible = "st,clkgen-c32";
		reg = <0x90ff000 0x1000>;

		clk_s_a0_pll: clk-s-a0-pll {
			#clock-cells = <1>;
			compatible = "st,clkgen-pll0";

			clocks = <&clk_sysin>;

			clock-output-names = "clk-s-a0-pll-ofd-0";
		};

		clk_s_a0_flexgen: clk-s-a0-flexgen {
			compatible = "st,flexgen";

			#clock-cells = <1>;

			clocks = <&clk_s_a0_pll 0>,
				 <&clk_sysin>;

			clock-output-names = "clk-ic-lmi0";
		};
	};
```
