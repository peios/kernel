---
title: "nova NVIDIA GPU drivers"
type: reference
description: "The nova driver project consists out of two separate drivers nova-core and nova-drm and intends to supersede the nouveau driver for NVIDIA GPUs based on the GPU System Processor (GSP)."
---

<a id="rst-nova-nvidia-gpu-drivers"></a>

<!-- SPDX-License-Identifier: (GPL-2.0+ OR MIT) -->

The nova driver project consists out of two separate drivers nova-core and nova-drm and intends to supersede the nouveau driver for NVIDIA GPUs based on the GPU System Processor (GSP).

The following documents apply to both nova-core and nova-drm.

- [Guidelines](<~kernel/hardware/gpu/nova/guidelines>)

<a id="rst-nova-core"></a>

## nova-core

The nova-core driver is the core driver for NVIDIA GPUs based on GSP. nova-core, as the 1st level driver, provides an abstraction around the GPUs hard- and firmware interfaces providing a common base for 2nd level drivers, such as the vGPU manager VFIO driver and the nova-drm driver.

- [Guidelines](<~kernel/hardware/gpu/nova-core/guidelines>)
- [Task List](<~kernel/hardware/gpu/nova-core/todo>)
- [VBIOS](<~kernel/hardware/gpu/nova-core/vbios>)
- [Device Initialization (devinit)](<~kernel/hardware/gpu/nova-core/devinit>)
- [FWSEC (Firmware Security)](<~kernel/hardware/gpu/nova-core/fwsec>)
- [Falcon (FAst Logic Controller)](<~kernel/hardware/gpu/nova-core/falcon>)
