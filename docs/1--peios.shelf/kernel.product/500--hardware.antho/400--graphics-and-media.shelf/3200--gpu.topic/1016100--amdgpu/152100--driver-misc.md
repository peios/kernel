---
title: "Misc AMDGPU driver information"
type: reference
description: "Information about the GPU can be obtained on certain cards via sysfs"
---

<a id="rst-misc-amdgpu-driver-information"></a>

<a id="rst-gpu-product-information"></a>

## GPU Product Information

Information about the GPU can be obtained on certain cards via sysfs

<a id="rst-product-name"></a>

### product_name

```{kernel-doc} drivers/gpu/drm/amd/amdgpu/amdgpu_fru_eeprom.c
:doc: product_name
```

<a id="rst-product-number"></a>

### product_number

```{kernel-doc} drivers/gpu/drm/amd/amdgpu/amdgpu_fru_eeprom.c
:doc: product_number
```

<a id="rst-serial-number"></a>

### serial_number

```{kernel-doc} drivers/gpu/drm/amd/amdgpu/amdgpu_fru_eeprom.c
:doc: serial_number
```

<a id="rst-fru-id"></a>

### fru_id

```{kernel-doc} drivers/gpu/drm/amd/amdgpu/amdgpu_fru_eeprom.c
:doc: fru_id
```

<a id="rst-manufacturer"></a>

### manufacturer

```{kernel-doc} drivers/gpu/drm/amd/amdgpu/amdgpu_fru_eeprom.c
:doc: manufacturer
```

<a id="rst-unique-id"></a>

### unique_id

```{kernel-doc} drivers/gpu/drm/amd/pm/amdgpu_pm.c
:doc: unique_id
```

<a id="rst-board-info"></a>

### board_info

```{kernel-doc} drivers/gpu/drm/amd/amdgpu/amdgpu_device.c
:doc: board_info
```

<a id="rst-gpu-memory-usage-information"></a>

## GPU Memory Usage Information

Various memory accounting can be accessed via sysfs

<a id="rst-mem-info-vram-total"></a>

### mem_info_vram_total

```{kernel-doc} drivers/gpu/drm/amd/amdgpu/amdgpu_vram_mgr.c
:doc: mem_info_vram_total
```

<a id="rst-mem-info-vram-used"></a>

### mem_info_vram_used

```{kernel-doc} drivers/gpu/drm/amd/amdgpu/amdgpu_vram_mgr.c
:doc: mem_info_vram_used
```

<a id="rst-mem-info-vis-vram-total"></a>

### mem_info_vis_vram_total

```{kernel-doc} drivers/gpu/drm/amd/amdgpu/amdgpu_vram_mgr.c
:doc: mem_info_vis_vram_total
```

<a id="rst-mem-info-vis-vram-used"></a>

### mem_info_vis_vram_used

```{kernel-doc} drivers/gpu/drm/amd/amdgpu/amdgpu_vram_mgr.c
:doc: mem_info_vis_vram_used
```

<a id="rst-mem-info-gtt-total"></a>

### mem_info_gtt_total

```{kernel-doc} drivers/gpu/drm/amd/amdgpu/amdgpu_gtt_mgr.c
:doc: mem_info_gtt_total
```

<a id="rst-mem-info-gtt-used"></a>

### mem_info_gtt_used

```{kernel-doc} drivers/gpu/drm/amd/amdgpu/amdgpu_gtt_mgr.c
:doc: mem_info_gtt_used
```

<a id="rst-pcie-accounting-information"></a>

## PCIe Accounting Information

<a id="rst-pcie-bw"></a>

### pcie_bw

```{kernel-doc} drivers/gpu/drm/amd/pm/amdgpu_pm.c
:doc: pcie_bw
```

<a id="rst-pcie-replay-count"></a>

### pcie_replay_count

```{kernel-doc} drivers/gpu/drm/amd/amdgpu/amdgpu_device.c
:doc: pcie_replay_count
```

<a id="rst-gpu-smartshift-information"></a>

## GPU SmartShift Information

GPU SmartShift information via sysfs

<a id="rst-smartshift-apu-power"></a>

### smartshift_apu_power

```{kernel-doc} drivers/gpu/drm/amd/pm/amdgpu_pm.c
:doc: smartshift_apu_power
```

<a id="rst-smartshift-dgpu-power"></a>

### smartshift_dgpu_power

```{kernel-doc} drivers/gpu/drm/amd/pm/amdgpu_pm.c
:doc: smartshift_dgpu_power
```

<a id="rst-smartshift-bias"></a>

### smartshift_bias

```{kernel-doc} drivers/gpu/drm/amd/pm/amdgpu_pm.c
:doc: smartshift_bias
```

<a id="rst-uma-carveout"></a>

## UMA Carveout

Some versions of Atom ROM expose available options for the VRAM carveout sizes, and allow changes to the carveout size via the ATCS function code 0xA on supported BIOS implementations.

For those platforms, users can use the following files under uma/ to set the carveout size, in a way similar to what Windows users can do in the "Tuning" tab in AMD Adrenalin.

Note that for BIOS implementations that don't support this, these files will not be created at all.

<a id="rst-uma-carveout-options"></a>

### uma/carveout_options

```{kernel-doc} drivers/gpu/drm/amd/amdgpu/amdgpu_device.c
:doc: uma/carveout_options
```

<a id="rst-uma-carveout-1"></a>

### uma/carveout

```{kernel-doc} drivers/gpu/drm/amd/amdgpu/amdgpu_device.c
:doc: uma/carveout
```
