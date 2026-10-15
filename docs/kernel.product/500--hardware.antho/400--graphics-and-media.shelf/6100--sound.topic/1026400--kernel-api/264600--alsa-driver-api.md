---
title: "The ALSA Driver API"
type: reference
description: "Reference for The ALSA Driver API."
---

<a id="rst-the-alsa-driver-api"></a>

<a id="rst-management-of-cards-and-devices"></a>

## Management of Cards and Devices

<a id="rst-card-management"></a>

### Card Management

```{kernel-doc} sound/core/init.c

```

<a id="rst-device-components"></a>

### Device Components

```{kernel-doc} sound/core/device.c

```

<a id="rst-module-requests-and-device-file-entries"></a>

### Module requests and Device File Entries

```{kernel-doc} sound/core/sound.c

```

<a id="rst-memory-management-helpers"></a>

### Memory Management Helpers

```{kernel-doc} sound/core/memory.c

```

```{kernel-doc} sound/core/memalloc.c

```

<a id="rst-pcm-api"></a>

## PCM API

<a id="rst-pcm-core"></a>

### PCM Core

```{kernel-doc} sound/core/pcm.c

```

```{kernel-doc} sound/core/pcm_lib.c

```

```{kernel-doc} sound/core/pcm_native.c

```

```{kernel-doc} include/sound/pcm.h

```

<a id="rst-pcm-format-helpers"></a>

### PCM Format Helpers

```{kernel-doc} sound/core/pcm_misc.c

```

<a id="rst-pcm-memory-management"></a>

### PCM Memory Management

```{kernel-doc} sound/core/pcm_memory.c

```

<a id="rst-pcm-dma-engine-api"></a>

### PCM DMA Engine API

```{kernel-doc} sound/core/pcm_dmaengine.c

```

```{kernel-doc} include/sound/dmaengine_pcm.h

```

<a id="rst-control-mixer-api"></a>

## Control/Mixer API

<a id="rst-general-control-interface"></a>

### General Control Interface

```{kernel-doc} sound/core/control.c

```

<a id="rst-ac97-codec-api"></a>

### AC97 Codec API

```{kernel-doc} sound/pci/ac97/ac97_codec.c

```

```{kernel-doc} sound/pci/ac97/ac97_pcm.c

```

<a id="rst-virtual-master-control-api"></a>

### Virtual Master Control API

```{kernel-doc} sound/core/vmaster.c

```

```{kernel-doc} include/sound/control.h

```

<a id="rst-midi-api"></a>

## MIDI API

<a id="rst-raw-midi-api"></a>

### Raw MIDI API

```{kernel-doc} sound/core/rawmidi.c

```

<a id="rst-mpu401-uart-api"></a>

### MPU401-UART API

```{kernel-doc} sound/drivers/mpu401/mpu401_uart.c

```

<a id="rst-proc-info-api"></a>

## Proc Info API

<a id="rst-proc-info-interface"></a>

### Proc Info Interface

```{kernel-doc} sound/core/info.c

```

<a id="rst-compress-offload"></a>

## Compress Offload

<a id="rst-compress-offload-api"></a>

### Compress Offload API

```{kernel-doc} sound/core/compress_offload.c

```

```{kernel-doc} include/uapi/sound/compress_offload.h

```

```{kernel-doc} include/uapi/sound/compress_params.h

```

```{kernel-doc} include/sound/compress_driver.h

```

<a id="rst-asoc"></a>

## ASoC

<a id="rst-asoc-core-api"></a>

### ASoC Core API

```{kernel-doc} include/sound/soc.h

```

```{kernel-doc} sound/soc/soc-core.c

```

```{kernel-doc} sound/soc/soc-devres.c

```

```{kernel-doc} sound/soc/soc-component.c

```

```{kernel-doc} sound/soc/soc-pcm.c

```

```{kernel-doc} sound/soc/soc-ops.c

```

```{kernel-doc} sound/soc/soc-compress.c

```

<a id="rst-asoc-dapm-api"></a>

### ASoC DAPM API

```{kernel-doc} sound/soc/soc-dapm.c

```

<a id="rst-asoc-dma-engine-api"></a>

### ASoC DMA Engine API

```{kernel-doc} sound/soc/soc-generic-dmaengine-pcm.c

```

<a id="rst-miscellaneous-functions"></a>

## Miscellaneous Functions

<a id="rst-hardware-dependent-devices-api"></a>

### Hardware-Dependent Devices API

```{kernel-doc} sound/core/hwdep.c

```

<a id="rst-jack-abstraction-layer-api"></a>

### Jack Abstraction Layer API

```{kernel-doc} include/sound/jack.h

```

```{kernel-doc} sound/core/jack.c

```

```{kernel-doc} sound/soc/soc-jack.c

```

<a id="rst-isa-dma-helpers"></a>

### ISA DMA Helpers

```{kernel-doc} sound/core/isadma.c

```

<a id="rst-other-helper-macros"></a>

### Other Helper Macros

```{kernel-doc} include/sound/core.h

```

```{kernel-doc} sound/sound_core.c

```
