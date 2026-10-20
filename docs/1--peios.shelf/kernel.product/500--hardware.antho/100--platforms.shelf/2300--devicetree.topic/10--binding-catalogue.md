---
title: "Device-tree binding catalogue"
type: reference
description: "Hardware binding references generated from the kernel device-tree schemas."
---

These references describe how hardware is represented in a device tree. Each
page comes directly from its YAML binding, including descriptions, properties,
child nodes, constraints and examples.

## Reading the rules

“Required here” means a property appears in the required list for that object.
“Not listed as required here” does not guarantee that it is optional: a shared
schema or a conditional rule may still require it. Follow shared-schema links
for the rules they contribute.

- **All of these rules** means every branch must match.
- **At least one** means one or more branches must match.
- **Exactly one** means one branch must match, and the others must not.
- **Condition**, **when it matches** and **when it does not match** retain the
  original if/then/else relationship.
- A false property rule forbids that property in its scope. A true rule adds no
  constraints there; shared device-tree rules can still apply.

Properties not matched by a schema's own property declarations are different
from properties not evaluated by all applicable rules. The references retain
that distinction rather than combining the two restrictions.

The pages show the authored schemas. The dt-schema validator also applies common
device-tree conventions and normalization, including fixed-length item lists.
Use the kernel's binding and device-tree validation commands when checking an
actual device tree; these references do not replace those checks.

The shared definitions used by the catalogue are included from dt-schema 2026.9.
Source notes retain comments and licence notices. The YAML remains authoritative.

## Browse by hardware category

- [Access controllers bindings](<~kernel/hardware/devicetree-bindings/dt-access-controllers/access-controllers>)
- [Arc bindings](<~kernel/hardware/devicetree-bindings/dt-arc/snps-archs-pct>)
- [ARM platform bindings](<~kernel/hardware/devicetree-bindings/dt-arm/actions>)
- [Ata bindings](<~kernel/hardware/devicetree-bindings/dt-ata/ahci-common>)
- [Auxdisplay bindings](<~kernel/hardware/devicetree-bindings/dt-auxdisplay/arm-versatile-lcd>)
- [Board bindings](<~kernel/hardware/devicetree-bindings/dt-board/fsl-bcsr>)
- [Bus bindings](<~kernel/hardware/devicetree-bindings/dt-bus/allwinner-sun50i-a64-de2>)
- [Cache bindings](<~kernel/hardware/devicetree-bindings/dt-cache/andestech-ax45mp-cache>)
- [Chrome bindings](<~kernel/hardware/devicetree-bindings/dt-chrome/google-cros-ec-typec>)
- [Clock bindings](<~kernel/hardware/devicetree-bindings/dt-clock/actions-owl-cmu>)
- [Common bindings](<~kernel/hardware/devicetree-bindings/dt-common/example-schema>)
- [Connector bindings](<~kernel/hardware/devicetree-bindings/dt-connector/gocontroll-moduline-module-slot>)
- [Counter bindings](<~kernel/hardware/devicetree-bindings/dt-counter/fsl-ftm-quaddec>)
- [Cpu bindings](<~kernel/hardware/devicetree-bindings/dt-cpu/idle-states>)
- [Cpufreq bindings](<~kernel/hardware/devicetree-bindings/dt-cpufreq/airoha-en7581-cpufreq>)
- [Crypto bindings](<~kernel/hardware/devicetree-bindings/dt-crypto/allwinner-sun4i-a10-crypto>)
- [Devfreq bindings](<~kernel/hardware/devicetree-bindings/dt-devfreq/event/rockchip-dfi>)
- [Display bindings](<~kernel/hardware/devicetree-bindings/dt-display/allwinner-sun4i-a10-display-backend>)
- [Dma bindings](<~kernel/hardware/devicetree-bindings/dt-dma/adi-axi-dmac>)
- [Dpll bindings](<~kernel/hardware/devicetree-bindings/dt-dpll/dpll-device>)
- [Dsp bindings](<~kernel/hardware/devicetree-bindings/dt-dsp/fsl-dsp>)
- [Dvfs bindings](<~kernel/hardware/devicetree-bindings/dt-dvfs/performance-domain>)
- [Edac bindings](<~kernel/hardware/devicetree-bindings/dt-edac/altr-socfpga-ecc-manager>)
- [Eeprom bindings](<~kernel/hardware/devicetree-bindings/dt-eeprom/at24>)
- [Embedded controller bindings](<~kernel/hardware/devicetree-bindings/dt-embedded-controller/acer-aspire1-ec>)
- [Extcon bindings](<~kernel/hardware/devicetree-bindings/dt-extcon/extcon-ptn5150>)
- [Firmware bindings](<~kernel/hardware/devicetree-bindings/dt-firmware/amlogic-meson-gxbb-sm>)
- [Fpga bindings](<~kernel/hardware/devicetree-bindings/dt-fpga/altr-fpga-passive-serial>)
- [Fsi bindings](<~kernel/hardware/devicetree-bindings/dt-fsi/aspeed-ast2400-cf-fsi-master>)
- [Fuse bindings](<~kernel/hardware/devicetree-bindings/dt-fuse/nvidia-tegra20-fuse>)
- [Gnss bindings](<~kernel/hardware/devicetree-bindings/dt-gnss/brcm-bcm4751>)
- [Gpio bindings](<~kernel/hardware/devicetree-bindings/dt-gpio/abilis-tb10x-gpio>)
- [Gpu bindings](<~kernel/hardware/devicetree-bindings/dt-gpu/apple-agx>)
- [Hwinfo bindings](<~kernel/hardware/devicetree-bindings/dt-hwinfo/loongson-ls2k-chipid>)
- [Hwlock bindings](<~kernel/hardware/devicetree-bindings/dt-hwlock/allwinner-sun6i-a31-hwspinlock>)
- [Hwmon bindings](<~kernel/hardware/devicetree-bindings/dt-hwmon/adi-ad741x>)
- [I2C bindings](<~kernel/hardware/devicetree-bindings/dt-i2c/allwinner-sun6i-a31-p2wi>)
- [I3c bindings](<~kernel/hardware/devicetree-bindings/dt-i3c/adi-i3c-master>)
- [Industrial I/O bindings](<~kernel/hardware/devicetree-bindings/dt-iio/accel/adi-adis16201>)
- [Input bindings](<~kernel/hardware/devicetree-bindings/dt-input/adafruit-seesaw-gamepad>)
- [Interconnect bindings](<~kernel/hardware/devicetree-bindings/dt-interconnect/fsl-imx8m-noc>)
- [Interrupt controller bindings](<~kernel/hardware/devicetree-bindings/dt-interrupt-controller/abilis-tb10x-ictl>)
- [Iommu bindings](<~kernel/hardware/devicetree-bindings/dt-iommu/allwinner-sun50i-h6-iommu>)
- [Ipmi bindings](<~kernel/hardware/devicetree-bindings/dt-ipmi/aspeed-ast2400-ibt-bmc>)
- [LED bindings](<~kernel/hardware/devicetree-bindings/dt-leds/allwinner-sun50i-a100-ledc>)
- [Loongarch bindings](<~kernel/hardware/devicetree-bindings/dt-loongarch/cpus>)
- [Mailbox bindings](<~kernel/hardware/devicetree-bindings/dt-mailbox/allwinner-sun6i-a31-msgbox>)
- [Media bindings](<~kernel/hardware/devicetree-bindings/dt-media/allegro-al5e>)
- [Memory controllers bindings](<~kernel/hardware/devicetree-bindings/dt-memory-controllers/arm-pl172>)
- [Mfd bindings](<~kernel/hardware/devicetree-bindings/dt-mfd/actions-atc260x>)
- [Mips bindings](<~kernel/hardware/devicetree-bindings/dt-mips/brcm/soc>)
- [Misc bindings](<~kernel/hardware/devicetree-bindings/dt-misc/aspeed-ast2400-cvic>)
- [Mmc bindings](<~kernel/hardware/devicetree-bindings/dt-mmc/allwinner-sun4i-a10-mmc>)
- [Mtd bindings](<~kernel/hardware/devicetree-bindings/dt-mtd/allwinner-sun4i-a10-nand>)
- [Mux bindings](<~kernel/hardware/devicetree-bindings/dt-mux/gpio-mux>)
- [Network bindings](<~kernel/hardware/devicetree-bindings/dt-net/actions-owl-emac>)
- [Npu bindings](<~kernel/hardware/devicetree-bindings/dt-npu/arm-ethos>)
- [Nvme bindings](<~kernel/hardware/devicetree-bindings/dt-nvme/apple-nvme-ans>)
- [Nvmem bindings](<~kernel/hardware/devicetree-bindings/dt-nvmem/airoha-an8855-efuse>)
- [Opp bindings](<~kernel/hardware/devicetree-bindings/dt-opp/allwinner-sun50i-h6-operating-points>)
- [PCI bindings](<~kernel/hardware/devicetree-bindings/dt-pci/altr-pcie-root-port>)
- [Peci bindings](<~kernel/hardware/devicetree-bindings/dt-peci/nuvoton-npcm-peci>)
- [Perf bindings](<~kernel/hardware/devicetree-bindings/dt-perf/amlogic-g12-ddr-pmu>)
- [PHY bindings](<~kernel/hardware/devicetree-bindings/dt-phy/airoha-en7581-pcie-phy>)
- [Pin control bindings](<~kernel/hardware/devicetree-bindings/dt-pinctrl/actions-s500-pinctrl>)
- [Pmem bindings](<~kernel/hardware/devicetree-bindings/dt-pmem/pmem-region>)
- [Power bindings](<~kernel/hardware/devicetree-bindings/dt-power/actions-s500-sps>)
- [Powerpc bindings](<~kernel/hardware/devicetree-bindings/dt-powerpc/fsl/fsl-mpc83xx>)
- [Pps bindings](<~kernel/hardware/devicetree-bindings/dt-pps/pps-gpio>)
- [Ptp bindings](<~kernel/hardware/devicetree-bindings/dt-ptp/amazon-vmclock>)
- [Pwm bindings](<~kernel/hardware/devicetree-bindings/dt-pwm/adi-axi-pwmgen>)
- [Regulator bindings](<~kernel/hardware/devicetree-bindings/dt-regulator/active-semi-act8600>)
- [Remoteproc bindings](<~kernel/hardware/devicetree-bindings/dt-remoteproc/amlogic-meson-mx-ao-arc>)
- [Reserved memory bindings](<~kernel/hardware/devicetree-bindings/dt-reserved-memory/google-open-dice>)
- [Reset bindings](<~kernel/hardware/devicetree-bindings/dt-reset/allwinner-sun6i-a31-clock-reset>)
- [Riscv bindings](<~kernel/hardware/devicetree-bindings/dt-riscv/andes>)
- [Rng bindings](<~kernel/hardware/devicetree-bindings/dt-rng/sunw-n2-rng>)
- [Rtc bindings](<~kernel/hardware/devicetree-bindings/dt-rtc/abracon-abx80x>)
- [Serial bindings](<~kernel/hardware/devicetree-bindings/dt-serial/8250>)
- [Serio bindings](<~kernel/hardware/devicetree-bindings/dt-serio/allwinner-sun4i-a10-ps2>)
- [Shared binding definitions](<~kernel/hardware/devicetree-bindings/dt-shared/cache-controller>)
- [Siox bindings](<~kernel/hardware/devicetree-bindings/dt-siox/eckelmann-siox-gpio>)
- [Slimbus bindings](<~kernel/hardware/devicetree-bindings/dt-slimbus/qcom-slim-ngd>)
- [Soc bindings](<~kernel/hardware/devicetree-bindings/dt-soc/altera/altr-sys-mgr>)
- [Audio bindings](<~kernel/hardware/devicetree-bindings/dt-sound/adi-adau1372>)
- [Soundwire bindings](<~kernel/hardware/devicetree-bindings/dt-soundwire/qcom-soundwire>)
- [Spi bindings](<~kernel/hardware/devicetree-bindings/dt-spi/adi-axi-spi-engine>)
- [Spmi bindings](<~kernel/hardware/devicetree-bindings/dt-spmi/apple-spmi>)
- [Sram bindings](<~kernel/hardware/devicetree-bindings/dt-sram/allwinner-sun4i-a10-system-control>)
- [Thermal bindings](<~kernel/hardware/devicetree-bindings/dt-thermal/airoha-en7581-thermal>)
- [Timer bindings](<~kernel/hardware/devicetree-bindings/dt-timer/actions-owl-timer>)
- [Timestamp bindings](<~kernel/hardware/devicetree-bindings/dt-timestamp/hardware-timestamps-common>)
- [Tpm bindings](<~kernel/hardware/devicetree-bindings/dt-tpm/google-cr50>)
- [Trigger source bindings](<~kernel/hardware/devicetree-bindings/dt-trigger-source/adi-util-sigma-delta-spi>)
- [Ufs bindings](<~kernel/hardware/devicetree-bindings/dt-ufs/amd-versal2-ufs>)
- [USB bindings](<~kernel/hardware/devicetree-bindings/dt-usb/allwinner-sun4i-a10-musb>)
- [Virtio bindings](<~kernel/hardware/devicetree-bindings/dt-virtio/mmio>)
- [W1 bindings](<~kernel/hardware/devicetree-bindings/dt-w1/amd-axi-1wire-host>)
- [Watchdog bindings](<~kernel/hardware/devicetree-bindings/dt-watchdog/airoha-en7581-wdt>)
