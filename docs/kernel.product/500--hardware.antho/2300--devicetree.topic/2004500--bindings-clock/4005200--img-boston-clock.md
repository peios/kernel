---
title: "Binding for Imagination Technologies MIPS Boston clock sources."
type: reference
description: "Device-tree binding reference for Binding for Imagination Technologies MIPS Boston clock sources.."
---

This binding uses the common clock binding\[1\].

\[1\] [Documentation/devicetree/bindings/clock/clock-bindings.txt](<~kernel/hardware/devicetree/bindings-clock/clock-bindings>)

The device node must be a child node of the syscon node corresponding to the
Boston system's platform registers.

## Required properties:

- compatible : Should be "img,boston-clock".
- #clock-cells : Should be set to 1.
  Values available for clock consumers can be found in the header file:
  &lt;dt-bindings/clock/boston-clock.h&gt;

## Example:

```dts
	system-controller@17ffd000 {
		compatible = "img,boston-platform-regs", "syscon";
		reg = <0x17ffd000 0x1000>;

		clk_boston: clock {
			compatible = "img,boston-clock";
			#clock-cells = <1>;
		};
	};
```

```dts
	uart0: uart@17ffe000 {
		/* ... */
		clocks = <&clk_boston BOSTON_CLK_SYS>;
	};
```
