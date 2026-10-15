---
title: "Mediatek ALSA BT SCO CVSD/MSBC Driver"
type: reference
description: "Device-tree binding reference for Mediatek ALSA BT SCO CVSD/MSBC Driver."
---

## Required properties:

- compatible = "mediatek,mtk-btcvsd-snd";
- reg: register location and size of PKV and SRAM\_BANK2
- interrupts: should contain BTSCO interrupt
- mediatek,infracfg: the phandles of INFRASYS
- mediatek,offset: Array contains of register offset and mask
  infra\_misc\_offset,
  infra\_conn\_bt\_cvsd\_mask,
  cvsd\_mcu\_read\_offset,
  cvsd\_mcu\_write\_offset,
  cvsd\_packet\_indicator\_offset

## Example:

```dts
	mtk-btcvsd-snd@18000000 {
		compatible = "mediatek,mtk-btcvsd-snd";
		reg=<0 0x18000000 0 0x1000>,
		    <0 0x18080000 0 0x8000>;
		interrupts = <GIC_SPI 286 IRQ_TYPE_LEVEL_LOW>;
		mediatek,infracfg = <&infrasys>;
		mediatek,offset = <0xf00 0x800 0xfd0 0xfd4 0xfd8>;
	};
```
