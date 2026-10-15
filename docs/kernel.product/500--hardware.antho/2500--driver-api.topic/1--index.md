---
title: "Driver implementer's API guide"
type: reference
description: "The kernel offers a wide variety of interfaces to support the development of device drivers. This document is an only somewhat organized collection of some of those interfaces — it will hopefully get better over time! The available…"
---

<a id="rst-driver-implementer-s-api-guide"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

The kernel offers a wide variety of interfaces to support the development of device drivers.  This document is an only somewhat organized collection of some of those interfaces — it will hopefully get better over time\!  The available subsections can be seen below.

<a id="rst-general-information-for-driver-authors"></a>

## General information for driver authors

This section contains documentation that should, at some point or other, be of interest to most developers working on device drivers.

- [Driver Basics](<~kernel/hardware/driver-api/basics>)
- [Driver Model](<~kernel/hardware/driver-api/driver-model/index>)
- [Device links](<~kernel/hardware/driver-api/device-link>)
- [Device drivers infrastructure](<~kernel/hardware/driver-api/infrastructure>)
- [ioctl based interfaces](<~kernel/hardware/driver-api/ioctl>)
- [CPU and Device Power Management](<~kernel/hardware/driver-api/pm/index>)

<a id="rst-useful-support-libraries"></a>

## Useful support libraries

This section contains documentation that should, at some point or other, be of interest to most developers working on device drivers.

- [Early Userspace](<~kernel/hardware/driver-api/early-userspace/index>)
- [Kernel Connector](<~kernel/hardware/driver-api/connector>)
- [Bus-Independent Device Accesses](<~kernel/hardware/driver-api/device-io>)
- [Device Frequency Scaling](<~kernel/hardware/driver-api/devfreq>)
- [Buffer Sharing and Synchronization (dma-buf)](<~kernel/hardware/driver-api/dma-buf>)
- [Component Helper for Aggregate Drivers](<~kernel/hardware/driver-api/component>)
- [The io_mapping functions](<~kernel/hardware/driver-api/io-mapping>)
- [Ordering I/O writes to memory-mapped addresses](<~kernel/hardware/driver-api/io-ordering>)
- [The Userspace I/O HOWTO](<~kernel/hardware/driver-api/uio-howto>)
- [VFIO Mediated devices](<~kernel/hardware/driver-api/vfio-mediated-device>)
- [VFIO - "Virtual Function I/O" 1](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/driver-api/vfio.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>)
- [Acceptance criteria for vfio-pci device specific driver variants](<~kernel/hardware/driver-api/vfio-pci-device-specific-driver-acceptance>)

<a id="rst-bus-level-documentation"></a>

## Bus-level documentation

- [Auxiliary Bus](<~kernel/hardware/driver-api/auxiliary-bus>)
- [Compute Express Link](<~kernel/hardware/driver-api/cxl/index>)
- [EISA bus support](<~kernel/hardware/driver-api/eisa>)
- [Firewire (IEEE 1394) driver Interface Guide](<~kernel/hardware/driver-api/firewire>)
- [I3C subsystem](<~kernel/hardware/driver-api/i3c/index>)
- [ISA Drivers](<~kernel/hardware/driver-api/isa>)
- [MEN Chameleon Bus](<~kernel/hardware/driver-api/men-chameleon-bus>)
- [The Linux PCI driver implementer's API guide](<~kernel/hardware/driver-api/pci/index>)
- [The Linux RapidIO Subsystem](<~kernel/hardware/driver-api/rapidio/index>)
- [Linux kernel SLIMbus support](<~kernel/hardware/driver-api/slimbus>)
- [Linux USB API](<~kernel/hardware/driver-api/usb/index>)
- [Virtio](<~kernel/hardware/driver-api/virtio/index>)
- [VME Device Drivers](<~kernel/hardware/driver-api/vme>)
- [W1: Dallas' 1-wire bus](<~kernel/hardware/driver-api/w1>)
- [Xillybus driver for generic FPGA interface](<~kernel/hardware/driver-api/xillybus>)

<a id="rst-subsystem-specific-apis"></a>

## Subsystem-specific APIs

- [Linux 802.11 Driver Developer's Guide](<~kernel/hardware/driver-api/80211/index>)
- [ACPI Support](<~kernel/hardware/driver-api/acpi/index>)
- [Kernel driver lp855x](<~kernel/hardware/driver-api/backlight/lp855x-driver>)
- [The Common Clk Framework](<~kernel/hardware/driver-api/clk>)
- [Confidential Computing](<~kernel/hardware/driver-api/coco/index>)
- [Console Drivers](<~kernel/hardware/driver-api/console>)
- [Crypto Drivers](<~kernel/hardware/driver-api/crypto/index>)
- [DMAEngine documentation](<~kernel/hardware/driver-api/dmaengine/index>)
- [The Linux kernel dpll subsystem](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/driver-api/dpll.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>)
- [Error Detection And Correction (EDAC) Devices](<~kernel/hardware/driver-api/edac>)
- [Extcon Device Subsystem](<~kernel/hardware/driver-api/extcon>)
- [Linux Firmware API](<~kernel/hardware/driver-api/firmware/index>)
- [FPGA Subsystem](<~kernel/hardware/driver-api/fpga/index>)
- [Frame Buffer Library](<~kernel/hardware/driver-api/frame-buffer>)
- [Managing Ownership of the Framebuffer Aperture](<~kernel/hardware/driver-api/aperture>)
- [Generic Counter Interface](<~kernel/hardware/driver-api/generic-counter>)
- [Generic Radix Page Table](<~kernel/hardware/driver-api/generic-pt>)
- [General Purpose Input/Output (GPIO)](<~kernel/hardware/driver-api/gpio/index>)
- [High Speed Synchronous Serial Interface (HSI)](<~kernel/hardware/driver-api/hsi>)
- [The Linux Hardware Timestamping Engine (HTE)](<~kernel/hardware/driver-api/hte/index>)
- [Recoverable Hardware Error Tracking in vmcoreinfo](<~kernel/hardware/driver-api/hw-recoverable-errors>)
- [I2C and SMBus Subsystem](<~kernel/hardware/driver-api/i2c>)
- [Industrial I/O](<~kernel/hardware/driver-api/iio/index>)
- [InfiniBand and Remote DMA (RDMA) Interfaces](<~kernel/hardware/driver-api/infiniband>)
- [Input Subsystem](<~kernel/hardware/driver-api/input>)
- [Generic System Interconnect Subsystem](<~kernel/hardware/driver-api/interconnect>)
- [IPMB Driver for a Satellite MC](<~kernel/hardware/driver-api/ipmb>)
- [The Linux IPMI Driver](<~kernel/hardware/driver-api/ipmi>)
- [libATA Developer's Guide](<~kernel/hardware/driver-api/libata>)
- [The Common Mailbox Framework](<~kernel/hardware/driver-api/mailbox>)
- [RAID](<~kernel/hardware/driver-api/md/index>)
- [Media subsystem kernel internal API](<~kernel/hardware/driver-api/media/index>)
- [Intel(R) Management Engine Interface (Intel(R) MEI)](<~kernel/hardware/driver-api/mei/index>)
- [Memory Controller drivers](<~kernel/hardware/driver-api/memory-devices/index>)
- [Message-based devices](<~kernel/hardware/driver-api/message-based>)
- [Miscellaneous Devices](<~kernel/hardware/driver-api/misc-devices>)
- [Parallel Port Devices](<~kernel/hardware/driver-api/miscellaneous>)
- [MMC/SD/SDIO card support](<~kernel/hardware/driver-api/mmc/index>)
- [Memory Technology Device (MTD)](<~kernel/hardware/driver-api/mtd/index>)
- [MTD NAND Driver Programming Interface](<~kernel/hardware/driver-api/mtdnand>)
- [Near Field Communication](<~kernel/hardware/driver-api/nfc/index>)
- [NTB Drivers](<~kernel/hardware/driver-api/ntb>)
- [Non-Volatile Memory Device (NVDIMM)](<~kernel/hardware/driver-api/nvdimm/index>)
- [NVMEM Subsystem](<~kernel/hardware/driver-api/nvmem>)
- [PARPORT interface documentation](<~kernel/hardware/driver-api/parport-lowlevel>)
- [Generic PHY Framework](<~kernel/hardware/driver-api/phy/index>)
- [PINCTRL (PIN CONTROL) subsystem](<~kernel/hardware/driver-api/pin-control>)
- [PLDM Firmware Flash Update Library](<~kernel/hardware/driver-api/pldmfw/index>)
- [PPS - Pulse Per Second](<~kernel/hardware/driver-api/pps>)
- [PTP hardware clock infrastructure for Linux](<~kernel/hardware/driver-api/ptp>)
- [Pulse Width Modulation (PWM) interface](<~kernel/hardware/driver-api/pwm>)
- [Power Sequencing API](<~kernel/hardware/driver-api/pwrseq>)
- [Voltage and current regulator API](<~kernel/hardware/driver-api/regulator>)
- [Reset controller API](<~kernel/hardware/driver-api/reset>)
- [rfkill - RF kill switch support](<~kernel/hardware/driver-api/rfkill>)
- [Writing s390 channel device drivers](<~kernel/hardware/driver-api/s390-drivers>)
- [SCSI Interfaces Guide](<~kernel/hardware/driver-api/scsi>)
- [Support for Serial devices](<~kernel/hardware/driver-api/serial/index>)
- [SM501 Driver](<~kernel/hardware/driver-api/sm501>)
- [SoundWire Documentation](<~kernel/hardware/driver-api/soundwire/index>)
- [Serial Peripheral Interface (SPI)](<~kernel/hardware/driver-api/spi>)
- [Surface System Aggregator Module (SSAM)](<~kernel/hardware/driver-api/surface-aggregator/index>)
- [Linux Switchtec Support](<~kernel/hardware/driver-api/switchtec>)
- [Sync File API Guide](<~kernel/hardware/driver-api/sync-file>)
- [target and iSCSI Interfaces Guide](<~kernel/hardware/driver-api/target>)
- [TEE (Trusted Execution Environment) driver API](<~kernel/hardware/driver-api/tee>)
- [Thermal](<~kernel/hardware/driver-api/thermal/index>)
- [TTY](<~kernel/hardware/driver-api/tty/index>)
- [WBRF - Wifi Band RFI Mitigations](<~kernel/hardware/driver-api/wbrf>)
- [WMI Driver API](<~kernel/hardware/driver-api/wmi>)
- [Xilinx FPGA](<~kernel/hardware/driver-api/xilinx/index>)
- [Writing Device Drivers for Zorro Devices](<~kernel/hardware/driver-api/zorro>)
