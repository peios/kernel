---
title: "GPU Power/Thermal Controls and Monitoring"
type: reference
description: "GPU power controls are exposed via sysfs files."
---

<a id="rst-gpu-power-thermal-controls-and-monitoring"></a>

<a id="rst-hwmon-interfaces"></a>

## HWMON Interfaces

```{kernel-doc} drivers/gpu/drm/amd/pm/amdgpu_pm.c
:doc: hwmon
```

<a id="rst-gpu-sysfs-power-state-interfaces"></a>

## GPU sysfs Power State Interfaces

GPU power controls are exposed via sysfs files.

<a id="rst-power-dpm-state"></a>

### power_dpm_state

```{kernel-doc} drivers/gpu/drm/amd/pm/amdgpu_pm.c
:doc: power_dpm_state
```

<a id="rst-power-dpm-force-performance-level"></a>

### power_dpm_force_performance_level

```{kernel-doc} drivers/gpu/drm/amd/pm/amdgpu_pm.c
:doc: power_dpm_force_performance_level
```

<a id="rst-pp-table"></a>

### pp_table

```{kernel-doc} drivers/gpu/drm/amd/pm/amdgpu_pm.c
:doc: pp_table
```

<a id="rst-pp-od-clk-voltage"></a>

### pp_od_clk_voltage

```{kernel-doc} drivers/gpu/drm/amd/pm/amdgpu_pm.c
:doc: pp_od_clk_voltage
```

<a id="rst-pp-dpm"></a>

### pp_dpm\_\*

```{kernel-doc} drivers/gpu/drm/amd/pm/amdgpu_pm.c
:doc: pp_dpm_sclk pp_dpm_mclk pp_dpm_socclk pp_dpm_fclk pp_dpm_dcefclk pp_dpm_pcie
```

<a id="rst-pp-power-profile-mode"></a>

### pp_power_profile_mode

```{kernel-doc} drivers/gpu/drm/amd/pm/amdgpu_pm.c
:doc: pp_power_profile_mode
```

<a id="rst-pm-policy"></a>

### pm_policy

```{kernel-doc} drivers/gpu/drm/amd/pm/amdgpu_pm.c
:doc: pm_policy
```

<a id="rst-busy-percent"></a>

### \*\_busy_percent

```{kernel-doc} drivers/gpu/drm/amd/pm/amdgpu_pm.c
:doc: gpu_busy_percent
```

```{kernel-doc} drivers/gpu/drm/amd/pm/amdgpu_pm.c
:doc: mem_busy_percent
```

<a id="rst-gpu-metrics"></a>

### gpu_metrics

```{kernel-doc} drivers/gpu/drm/amd/pm/amdgpu_pm.c
:doc: gpu_metrics
```

<a id="rst-fan-curve"></a>

### fan_curve

```{kernel-doc} drivers/gpu/drm/amd/pm/amdgpu_pm.c
:doc: fan_curve
```

<a id="rst-acoustic-limit-rpm-threshold"></a>

### acoustic_limit_rpm_threshold

```{kernel-doc} drivers/gpu/drm/amd/pm/amdgpu_pm.c
:doc: acoustic_limit_rpm_threshold
```

<a id="rst-acoustic-target-rpm-threshold"></a>

### acoustic_target_rpm_threshold

```{kernel-doc} drivers/gpu/drm/amd/pm/amdgpu_pm.c
:doc: acoustic_target_rpm_threshold
```

<a id="rst-fan-target-temperature"></a>

### fan_target_temperature

```{kernel-doc} drivers/gpu/drm/amd/pm/amdgpu_pm.c
:doc: fan_target_temperature
```

<a id="rst-fan-minimum-pwm"></a>

### fan_minimum_pwm

```{kernel-doc} drivers/gpu/drm/amd/pm/amdgpu_pm.c
:doc: fan_minimum_pwm
```

<a id="rst-fan-zero-rpm-enable"></a>

### fan_zero_rpm_enable

```{kernel-doc} drivers/gpu/drm/amd/pm/amdgpu_pm.c
:doc: fan_zero_rpm_enable
```

<a id="rst-fan-zero-rpm-stop-temperature"></a>

### fan_zero_rpm_stop_temperature

```{kernel-doc} drivers/gpu/drm/amd/pm/amdgpu_pm.c
:doc: fan_zero_rpm_stop_temperature
```

<a id="rst-gfxoff"></a>

## GFXOFF

GFXOFF is a feature found in most recent GPUs that saves power at runtime. The card's RLC (RunList Controller) firmware powers off the gfx engine dynamically when there is no workload on gfx or compute pipes. GFXOFF is on by default on supported GPUs.

Userspace can interact with GFXOFF through a debugfs interface (all values in `uint32_t`, unless otherwise noted):

<a id="rst-amdgpu-gfxoff"></a>

### `amdgpu_gfxoff`

Use it to enable/disable GFXOFF, and to check if it's current enabled/disabled:



```text
$ xxd -l1 -p /sys/kernel/debug/dri/0/amdgpu_gfxoff
01
```

- Write 0 to disable it, and 1 to enable it.

- Read 0 means it's disabled, 1 it's enabled.

If it's enabled, that means that the GPU is free to enter into GFXOFF mode as needed. Disabled means that it will never enter GFXOFF mode.

<a id="rst-amdgpu-gfxoff-status"></a>

### `amdgpu_gfxoff_status`

Read it to check current GFXOFF's status of a GPU:



```text
$ xxd -l1 -p /sys/kernel/debug/dri/0/amdgpu_gfxoff_status
02
```

- 0: GPU is in GFXOFF state, the gfx engine is powered down.

- 1: Transition out of GFXOFF state

- 2: Not in GFXOFF state

- 3: Transition into GFXOFF state

If GFXOFF is enabled, the value will be transitioning around \[0, 3\], always getting into 0 when possible. When it's disabled, it's always at 2. Returns `-EINVAL` if it's not supported.

<a id="rst-amdgpu-gfxoff-count"></a>

### `amdgpu_gfxoff_count`

Read it to get the total GFXOFF entry count at the time of query since system power-up. The value is an `uint64_t` type, however, due to firmware limitations, it can currently overflow as an `uint32_t`. *Only supported in vangogh*

<a id="rst-amdgpu-gfxoff-residency"></a>

### `amdgpu_gfxoff_residency`

Write 1 to amdgpu_gfxoff_residency to start logging, and 0 to stop. Read it to get average GFXOFF residency % multiplied by 100 during the last logging interval. E.g. a value of 7854 means 78.54% of the time in the last logging interval the GPU was in GFXOFF mode. *Only supported in vangogh*
