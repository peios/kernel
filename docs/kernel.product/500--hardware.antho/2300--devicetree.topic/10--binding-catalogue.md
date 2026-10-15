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

- [Access controllers bindings](<~kernel/hardware/dt-access-controllers/access-controllers>)
- [Arc bindings](<~kernel/hardware/dt-arc/snps-archs-pct>)
- [ARM platform bindings](<~kernel/hardware/dt-arm/actions>)
- [Ata bindings](<~kernel/hardware/dt-ata/ahci-common>)
- [Auxdisplay bindings](<~kernel/hardware/dt-auxdisplay/arm-versatile-lcd>)
- [Board bindings](<~kernel/hardware/dt-board/fsl-bcsr>)
- [Bus bindings](<~kernel/hardware/dt-bus/allwinner-sun50i-a64-de2>)
- [Cache bindings](<~kernel/hardware/dt-cache/andestech-ax45mp-cache>)
- [Chrome bindings](<~kernel/hardware/dt-chrome/google-cros-ec-typec>)
- [Clock bindings](<~kernel/hardware/dt-clock/actions-owl-cmu>)
- [Common bindings](<~kernel/hardware/dt-common/example-schema>)
- [Connector bindings](<~kernel/hardware/dt-connector/gocontroll-moduline-module-slot>)
- [Counter bindings](<~kernel/hardware/dt-counter/fsl-ftm-quaddec>)
- [Cpu bindings](<~kernel/hardware/dt-cpu/idle-states>)
- [Cpufreq bindings](<~kernel/hardware/dt-cpufreq/airoha-en7581-cpufreq>)
- [Crypto bindings](<~kernel/hardware/dt-crypto/allwinner-sun4i-a10-crypto>)
- [Devfreq bindings](<~kernel/hardware/dt-devfreq/event/rockchip-dfi>)
- [Display bindings](<~kernel/hardware/dt-display/allwinner-sun4i-a10-display-backend>)
- [Dma bindings](<~kernel/hardware/dt-dma/adi-axi-dmac>)
- [Dpll bindings](<~kernel/hardware/dt-dpll/dpll-device>)
- [Dsp bindings](<~kernel/hardware/dt-dsp/fsl-dsp>)
- [Dvfs bindings](<~kernel/hardware/dt-dvfs/performance-domain>)
- [Edac bindings](<~kernel/hardware/dt-edac/altr-socfpga-ecc-manager>)
- [Eeprom bindings](<~kernel/hardware/dt-eeprom/at24>)
- [Embedded controller bindings](<~kernel/hardware/dt-embedded-controller/acer-aspire1-ec>)
- [Extcon bindings](<~kernel/hardware/dt-extcon/extcon-ptn5150>)
- [Firmware bindings](<~kernel/hardware/dt-firmware/amlogic-meson-gxbb-sm>)
- [Fpga bindings](<~kernel/hardware/dt-fpga/altr-fpga-passive-serial>)
- [Fsi bindings](<~kernel/hardware/dt-fsi/aspeed-ast2400-cf-fsi-master>)
- [Fuse bindings](<~kernel/hardware/dt-fuse/nvidia-tegra20-fuse>)
- [Gnss bindings](<~kernel/hardware/dt-gnss/brcm-bcm4751>)
- [Gpio bindings](<~kernel/hardware/dt-gpio/abilis-tb10x-gpio>)
- [Gpu bindings](<~kernel/hardware/dt-gpu/apple-agx>)
- [Hwinfo bindings](<~kernel/hardware/dt-hwinfo/loongson-ls2k-chipid>)
- [Hwlock bindings](<~kernel/hardware/dt-hwlock/allwinner-sun6i-a31-hwspinlock>)
- [Hwmon bindings](<~kernel/hardware/dt-hwmon/adi-ad741x>)
- [I2C bindings](<~kernel/hardware/dt-i2c/allwinner-sun6i-a31-p2wi>)
- [I3c bindings](<~kernel/hardware/dt-i3c/adi-i3c-master>)
- [Industrial I/O bindings](<~kernel/hardware/dt-iio/accel/adi-adis16201>)
- [Input bindings](<~kernel/hardware/dt-input/adafruit-seesaw-gamepad>)
- [Interconnect bindings](<~kernel/hardware/dt-interconnect/fsl-imx8m-noc>)
- [Interrupt controller bindings](<~kernel/hardware/dt-interrupt-controller/abilis-tb10x-ictl>)
- [Iommu bindings](<~kernel/hardware/dt-iommu/allwinner-sun50i-h6-iommu>)
- [Ipmi bindings](<~kernel/hardware/dt-ipmi/aspeed-ast2400-ibt-bmc>)
- [LED bindings](<~kernel/hardware/dt-leds/allwinner-sun50i-a100-ledc>)
- [Loongarch bindings](<~kernel/hardware/dt-loongarch/cpus>)
- [Mailbox bindings](<~kernel/hardware/dt-mailbox/allwinner-sun6i-a31-msgbox>)
- [Media bindings](<~kernel/hardware/dt-media/allegro-al5e>)
- [Memory controllers bindings](<~kernel/hardware/dt-memory-controllers/arm-pl172>)
- [Mfd bindings](<~kernel/hardware/dt-mfd/actions-atc260x>)
- [Mips bindings](<~kernel/hardware/dt-mips/brcm/soc>)
- [Misc bindings](<~kernel/hardware/dt-misc/aspeed-ast2400-cvic>)
- [Mmc bindings](<~kernel/hardware/dt-mmc/allwinner-sun4i-a10-mmc>)
- [Mtd bindings](<~kernel/hardware/dt-mtd/allwinner-sun4i-a10-nand>)
- [Mux bindings](<~kernel/hardware/dt-mux/gpio-mux>)
- [Network bindings](<~kernel/hardware/dt-net/actions-owl-emac>)
- [Npu bindings](<~kernel/hardware/dt-npu/arm-ethos>)
- [Nvme bindings](<~kernel/hardware/dt-nvme/apple-nvme-ans>)
- [Nvmem bindings](<~kernel/hardware/dt-nvmem/airoha-an8855-efuse>)
- [Opp bindings](<~kernel/hardware/dt-opp/allwinner-sun50i-h6-operating-points>)
- [PCI bindings](<~kernel/hardware/dt-pci/altr-pcie-root-port>)
- [Peci bindings](<~kernel/hardware/dt-peci/nuvoton-npcm-peci>)
- [Perf bindings](<~kernel/hardware/dt-perf/amlogic-g12-ddr-pmu>)
- [PHY bindings](<~kernel/hardware/dt-phy/airoha-en7581-pcie-phy>)
- [Pin control bindings](<~kernel/hardware/dt-pinctrl/actions-s500-pinctrl>)
- [Pmem bindings](<~kernel/hardware/dt-pmem/pmem-region>)
- [Power bindings](<~kernel/hardware/dt-power/actions-s500-sps>)
- [Powerpc bindings](<~kernel/hardware/dt-powerpc/fsl/fsl-mpc83xx>)
- [Pps bindings](<~kernel/hardware/dt-pps/pps-gpio>)
- [Ptp bindings](<~kernel/hardware/dt-ptp/amazon-vmclock>)
- [Pwm bindings](<~kernel/hardware/dt-pwm/adi-axi-pwmgen>)
- [Regulator bindings](<~kernel/hardware/dt-regulator/active-semi-act8600>)
- [Remoteproc bindings](<~kernel/hardware/dt-remoteproc/amlogic-meson-mx-ao-arc>)
- [Reserved memory bindings](<~kernel/hardware/dt-reserved-memory/google-open-dice>)
- [Reset bindings](<~kernel/hardware/dt-reset/allwinner-sun6i-a31-clock-reset>)
- [Riscv bindings](<~kernel/hardware/dt-riscv/andes>)
- [Rng bindings](<~kernel/hardware/dt-rng/sunw-n2-rng>)
- [Rtc bindings](<~kernel/hardware/dt-rtc/abracon-abx80x>)
- [Serial bindings](<~kernel/hardware/dt-serial/8250>)
- [Serio bindings](<~kernel/hardware/dt-serio/allwinner-sun4i-a10-ps2>)
- [Shared binding definitions](<~kernel/hardware/dt-shared/cache-controller>)
- [Siox bindings](<~kernel/hardware/dt-siox/eckelmann-siox-gpio>)
- [Slimbus bindings](<~kernel/hardware/dt-slimbus/qcom-slim-ngd>)
- [Soc bindings](<~kernel/hardware/dt-soc/altera/altr-sys-mgr>)
- [Audio bindings](<~kernel/hardware/dt-sound/adi-adau1372>)
- [Soundwire bindings](<~kernel/hardware/dt-soundwire/qcom-soundwire>)
- [Spi bindings](<~kernel/hardware/dt-spi/adi-axi-spi-engine>)
- [Spmi bindings](<~kernel/hardware/dt-spmi/apple-spmi>)
- [Sram bindings](<~kernel/hardware/dt-sram/allwinner-sun4i-a10-system-control>)
- [Thermal bindings](<~kernel/hardware/dt-thermal/airoha-en7581-thermal>)
- [Timer bindings](<~kernel/hardware/dt-timer/actions-owl-timer>)
- [Timestamp bindings](<~kernel/hardware/dt-timestamp/hardware-timestamps-common>)
- [Tpm bindings](<~kernel/hardware/dt-tpm/google-cr50>)
- [Trigger source bindings](<~kernel/hardware/dt-trigger-source/adi-util-sigma-delta-spi>)
- [Ufs bindings](<~kernel/hardware/dt-ufs/amd-versal2-ufs>)
- [USB bindings](<~kernel/hardware/dt-usb/allwinner-sun4i-a10-musb>)
- [Virtio bindings](<~kernel/hardware/dt-virtio/mmio>)
- [W1 bindings](<~kernel/hardware/dt-w1/amd-axi-1wire-host>)
- [Watchdog bindings](<~kernel/hardware/dt-watchdog/airoha-en7581-wdt>)
