---
title: "Kernel driver i2c-nvidia-gpu"
type: reference
description: "Datasheet: not publicly available."
---

<a id="rst-kernel-driver-i2c-nvidia-gpu"></a>

Datasheet: not publicly available.

- **Authors:**

  Ajay Gupta &lt;[ajayg@nvidia.com](<mailto:ajayg@nvidia.com>)&gt;

<a id="rst-description"></a>

## Description

i2c-nvidia-gpu is a driver for I2C controller included in NVIDIA Turing and later GPUs and it is used to communicate with Type-C controller on GPUs.

If your `lspci -v` listing shows something like the following:



```text
01:00.3 Serial bus controller [0c80]: NVIDIA Corporation Device 1ad9 (rev a1)
```

then this driver should support the I2C controller of your GPU.
