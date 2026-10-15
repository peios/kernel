---
title: "STMicroelectronics Low Power Controller (LPC) - Watchdog"
type: reference
description: "Device-tree binding reference for STMicroelectronics Low Power Controller (LPC) - Watchdog."
---

LPC currently supports Watchdog OR Real Time Clock OR Clocksource
functionality.

\[See: [../rtc/rtc-st-lpc.txt](<~kernel/hardware/devicetree/bindings-rtc/rtc-st-lpc>) for RTC options\]
\[See: ../timer/st,stih407-lpc for Clocksource options\]

Required properties

- compatible 	: Should be: "st,stih407-lpc"
- reg		: LPC registers base address + size
- interrupts    : LPC interrupt line number and associated flags
- clocks	: Clock used by LPC device (See: [../clock/clock-bindings.txt](<~kernel/hardware/devicetree/bindings-clock/clock-bindings>))
- st,lpc-mode	: The LPC can run either one of three modes:
  ST\_LPC\_MODE\_RTC    \[0\]
  ST\_LPC\_MODE\_WDT    \[1\]
  ST\_LPC\_MODE\_CLKSRC \[2\]
  One (and only one) mode must be selected.

Required properties \[watchdog mode\]

- st,syscfg	: Phandle to syscfg node used to enable watchdog and configure
  CPU reset type.
- timeout-sec	: Watchdog timeout in seconds

Optional properties \[watchdog mode\]

- st,warm-reset	: If present reset type will be 'warm' - if not it will be cold

## Example:

```dts
	lpc@fde05000 {
		compatible	= "st,stih407-lpc";
		reg		= <0xfde05000 0x1000>;
		clocks 		= <&clk_s_d3_flexgen CLK_LPC_0>;
		st,syscfg	= <&syscfg_core>;
		timeout-sec	= <120>;
		st,lpc-mode	= <ST_LPC_MODE_WDT>;
		st,warm-reset;
	};
```
