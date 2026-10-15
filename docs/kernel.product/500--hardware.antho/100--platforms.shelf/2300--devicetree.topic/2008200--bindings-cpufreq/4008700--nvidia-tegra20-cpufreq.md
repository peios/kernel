---
title: "Binding for NVIDIA Tegra20 CPUFreq"
type: reference
description: "Device-tree binding reference for Binding for NVIDIA Tegra20 CPUFreq."
---

## Required properties:

- clocks: Must contain an entry for the CPU clock.
  See ../clocks/clock-bindings.txt for details.
- operating-points-v2: See ../bindings/opp/opp-v2.yaml for details.
- #cooling-cells: Should be 2. See [../thermal/thermal-cooling-devices.yaml](<~kernel/hardware/devicetree-bindings/dt-thermal/thermal-cooling-devices>) for details.

## For each opp entry in 'operating-points-v2' table:

```text
- opp-supported-hw: Two bitfields indicating:
	On Tegra20:
	1. CPU process ID mask
	2. SoC speedo ID mask
```

## On Tegra30:

1. CPU process ID mask
2. CPU speedo ID mask

```text
	A bitwise AND is performed against these values and if any bit
	matches, the OPP gets enabled.
```

- opp-microvolt: CPU voltage triplet.

## Optional properties:

- cpu-supply: Phandle to the CPU power supply.

## Example:

```dts
	regulators {
		cpu_reg: regulator0 {
			regulator-name = "vdd_cpu";
		};
	};
```

```dts
	cpu0_opp_table: opp_table0 {
		compatible = "operating-points-v2";

		opp@456000000 {
			clock-latency-ns = <125000>;
			opp-microvolt = <825000 825000 1125000>;
			opp-supported-hw = <0x03 0x0001>;
			opp-hz = /bits/ 64 <456000000>;
		};

		...
	};
```

```dts
	cpus {
		cpu@0 {
			compatible = "arm,cortex-a9";
			clocks = <&tegra_car TEGRA20_CLK_CCLK>;
			operating-points-v2 = <&cpu0_opp_table>;
			cpu-supply = <&cpu_reg>;
			#cooling-cells = <2>;
		};
	};
```
