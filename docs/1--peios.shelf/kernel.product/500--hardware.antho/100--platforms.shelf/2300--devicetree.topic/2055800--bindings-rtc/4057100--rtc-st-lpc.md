---
title: "STMicroelectronics Low Power Controller (LPC) - RTC"
type: reference
description: "Device-tree binding reference for STMicroelectronics Low Power Controller (LPC) - RTC."
---

LPC currently supports Watchdog OR Real Time Clock OR Clocksource
functionality.

\[See: [../watchdog/st\_lpc\_wdt.txt](<~kernel/hardware/devicetree/bindings-watchdog/st-lpc-wdt>) for Watchdog options\]
\[See: ../timer/st,stih407-lpc for Clocksource options\]

Required properties

- compatible 	: Must be: "st,stih407-lpc"
- reg		: LPC registers base address + size
- interrupts    : LPC interrupt line number and associated flags
- clocks	: Clock used by LPC device (See: [../clock/clock-bindings.txt](<~kernel/hardware/devicetree/bindings-clock/clock-bindings>))
- st,lpc-mode	: The LPC can run either one of three modes:
  ST\_LPC\_MODE\_RTC    \[0\]
  ST\_LPC\_MODE\_WDT    \[1\]
  ST\_LPC\_MODE\_CLKSRC \[2\]
  One (and only one) mode must be selected.

## Example:

```dts
	lpc@fde05000 {
		compatible	= "st,stih407-lpc";
		reg		= <0xfde05000 0x1000>;
		clocks 		= <&clk_s_d3_flexgen CLK_LPC_0>;
		st,lpc-mode	= <ST_LPC_MODE_RTC>;
	};
```
