---
title: "STM32 ARM Linux Overview"
type: reference
description: "The STMicroelectronics STM32 family of Cortex-A microprocessors (MPUs) and Cortex-M microcontrollers (MCUs) are supported by the 'STM32' platform of ARM Linux."
---

<a id="rst-stm32-arm-linux-overview"></a>

<a id="rst-introduction"></a>

## Introduction

The STMicroelectronics STM32 family of Cortex-A microprocessors (MPUs) and Cortex-M microcontrollers (MCUs) are supported by the 'STM32' platform of ARM Linux.

<a id="rst-configuration"></a>

## Configuration

- **For MCUs, use the provided default configuration:**

  make stm32_defconfig

- **For MPUs, use multi_v7 configuration:**

  make multi_v7_defconfig

<a id="rst-layout"></a>

## Layout

All the files for multiple machine families are located in the platform code contained in arch/arm/mach-stm32

There is a generic board board-dt.c in the mach folder which support Flattened Device Tree, which means, it works with any compatible board with Device Trees.

**Authors:** 

- Maxime Coquelin &lt;[mcoquelin.stm32@gmail.com](<mailto:mcoquelin.stm32@gmail.com>)&gt;

- Ludovic Barre &lt;[ludovic.barre@st.com](<mailto:ludovic.barre@st.com>)&gt;

- Gerald Baeza &lt;[gerald.baeza@st.com](<mailto:gerald.baeza@st.com>)&gt;
