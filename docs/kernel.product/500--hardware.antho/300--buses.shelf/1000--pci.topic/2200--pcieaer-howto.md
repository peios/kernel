---
title: "The PCI Express Advanced Error Reporting Driver Guide HOWTO"
type: reference
description: "This guide describes the basics of the PCI Express (PCIe) Advanced Error Reporting (AER) driver and provides information on how to use it, as well as how to enable the drivers of Endpoint devices to conform with the PCIe AER driver."
---

<a id="rst-the-pci-express-advanced-error-reporting-driver-guide-howto"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

<!-- This data file has been placed in the public domain. -->

<!-- Derived from the Unicode character mappings available from
<http://www.w3.org/2003/entities/xml/>.
Processed by unicode2rstsubs.py, part of Docutils:
<https://docutils.sourceforge.io>. -->

**Authors:** - - **T.** Long Nguyen &lt;[tom.l.nguyen@intel.com](<mailto:tom.l.nguyen@intel.com>)&gt;

- Yanmin Zhang &lt;[yanmin.zhang@intel.com](<mailto:yanmin.zhang@intel.com>)&gt;

**Copyright:** © 2006 Intel Corporation

<a id="rst-overview"></a>

## Overview

<a id="rst-about-this-guide"></a>

### About this guide

This guide describes the basics of the PCI Express (PCIe) Advanced Error Reporting (AER) driver and provides information on how to use it, as well as how to enable the drivers of Endpoint devices to conform with the PCIe AER driver.

<a id="rst-what-is-the-pcie-aer-driver"></a>

### What is the PCIe AER Driver?

PCIe error signaling can occur on the PCIe link itself or on behalf of transactions initiated on the link. PCIe defines two error reporting paradigms: the baseline capability and the Advanced Error Reporting capability. The baseline capability is required of all PCIe components providing a minimum defined set of error reporting requirements. Advanced Error Reporting capability is implemented with a PCIe Advanced Error Reporting extended capability structure providing more robust error reporting.

The PCIe AER driver provides the infrastructure to support PCIe Advanced Error Reporting capability. The PCIe AER driver provides three basic functions:

> - Gathers the comprehensive error information if errors occurred.
>
> - Reports error to the users.
>
> - Performs error recovery actions.

The AER driver only attaches to Root Ports and RCECs that support the PCIe AER capability.

<a id="rst-user-guide"></a>

## User Guide

<a id="rst-include-the-pcie-aer-root-driver-into-the-linux-kernel"></a>

### Include the PCIe AER Root Driver into the Linux Kernel

The PCIe AER driver is a Root Port service driver attached via the PCIe Port Bus driver. If a user wants to use it, the driver must be compiled. It is enabled with CONFIG_PCIEAER, which depends on CONFIG_PCIEPORTBUS.

<a id="rst-load-pcie-aer-root-driver"></a>

### Load PCIe AER Root Driver

Some systems have AER support in firmware. Enabling Linux AER support at the same time the firmware handles AER would result in unpredictable behavior. Therefore, Linux does not handle AER events unless the firmware grants AER control to the OS via the ACPI \_OSC method. See the PCI Firmware Specification for details regarding \_OSC usage.

<a id="rst-aer-error-output"></a>

### AER error output

When a PCIe AER error is captured, an error message will be output to console. If it's a correctable error, it is output as a warning message. Otherwise, it is printed as an error. So users could choose different log level to filter out correctable error messages.

Below shows an example:



```text
0000:50:00.0: PCIe Bus Error: severity=Uncorrectable (Fatal), type=Transaction Layer, (Requester ID)
0000:50:00.0:   device [8086:0329] error status/mask=00100000/00000000
0000:50:00.0:    [20] UnsupReq               (First)
0000:50:00.0:   TLP Header: 0x04000001 0x00200a03 0x05010000 0x00050100
```

In the example, 'Requester ID' means the ID of the device that sent the error message to the Root Port. Please refer to PCIe specs for other fields.

The 'TLP Header' is the prefix/header of the TLP that caused the error in raw hex format. To decode the TLP Header into human-readable form one may use tlp-tool:

[https://github.com/mmpg-x86/tlp-tool](<https://github.com/mmpg-x86/tlp-tool>)

Example usage:



```text
curl -L https://git.kernel.org/linus/2ca1c94ce0b6 | rtlp-tool --aer
```

<a id="rst-aer-ratelimits"></a>

### AER Ratelimits

Since error messages can be generated for each transaction, we may see large volumes of errors reported. To prevent spammy devices from flooding the console/stalling execution, messages are throttled by device and error type (correctable vs. non-fatal uncorrectable).  Fatal errors, including DPC errors, are not ratelimited.

AER uses the default ratelimit of DEFAULT_RATELIMIT_BURST (10 events) over DEFAULT_RATELIMIT_INTERVAL (5 seconds).

Ratelimits are exposed in the form of sysfs attributes and configurable. See Documentation/ABI/testing/sysfs-bus-pci-devices-aer.

<a id="rst-aer-statistics-counters"></a>

### AER Statistics / Counters

When PCIe AER errors are captured, the counters / statistics are also exposed in the form of sysfs attributes which are documented at Documentation/ABI/testing/sysfs-bus-pci-devices-aer.

<a id="rst-developer-guide"></a>

## Developer Guide

To enable error recovery, a software driver must provide callbacks.

To support AER better, developers need to understand how AER works.

PCIe errors are classified into two types: correctable errors and uncorrectable errors. This classification is based on the impact of those errors, which may result in degraded performance or function failure.

Correctable errors pose no impacts on the functionality of the interface. The PCIe protocol can recover without any software intervention or any loss of data. These errors are detected and corrected by hardware.

Unlike correctable errors, uncorrectable errors impact functionality of the interface. Uncorrectable errors can cause a particular transaction or a particular PCIe link to be unreliable. Depending on those error conditions, uncorrectable errors are further classified into non-fatal errors and fatal errors. Non-fatal errors cause the particular transaction to be unreliable, but the PCIe link itself is fully functional. Fatal errors, on the other hand, cause the link to be unreliable.

When PCIe error reporting is enabled, a device will automatically send an error message to the Root Port above it when it captures an error. The Root Port, upon receiving an error reporting message, internally processes and logs the error message in its AER Capability structure. Error information being logged includes storing the error reporting agent's Requester ID into the Error Source Identification Registers and setting the error bits of the Root Error Status Register accordingly. If AER error reporting is enabled in the Root Error Command Register, the Root Port generates an interrupt when an error is detected.

Note that the errors as described above are related to the PCIe hierarchy and links. These errors do not include any device specific errors because device specific errors will still get sent directly to the device driver.

<a id="rst-provide-callbacks"></a>

### Provide callbacks

<a id="rst-pci-error-recovery-callbacks"></a>

#### PCI error-recovery callbacks

The PCIe AER Root driver uses error callbacks to coordinate with downstream device drivers associated with a hierarchy in question when performing error recovery actions.

Data struct pci_driver has a pointer, err_handler, to point to pci_error_handlers who consists of a couple of callback function pointers. The AER driver follows the rules defined in [pci-error-recovery.rst](~kernel/hardware/pci/pci-error-recovery) except PCIe-specific parts (see below). Please refer to [pci-error-recovery.rst](~kernel/hardware/pci/pci-error-recovery) for detailed definitions of the callbacks.

The sections below specify when to call the error callback functions.

<a id="rst-correctable-errors"></a>

#### Correctable errors

Correctable errors pose no impacts on the functionality of the interface. The PCIe protocol can recover without any software intervention or any loss of data. These errors do not require any recovery actions. The AER driver clears the device's correctable error status register accordingly and logs these errors.

<a id="rst-uncorrectable-non-fatal-and-fatal-errors"></a>

#### Uncorrectable (non-fatal and fatal) errors

The AER driver performs a Secondary Bus Reset to recover from uncorrectable errors. The reset is applied at the port above the originating device: If the originating device is an Endpoint, only the Endpoint is reset. If on the other hand the originating device has subordinate devices, those are all affected by the reset as well.

If the originating device is a Root Complex Integrated Endpoint, there's no port above where a Secondary Bus Reset could be applied. In this case, the AER driver instead applies a Function Level Reset.

If an error message indicates a non-fatal error, performing a reset at upstream is not required. The AER driver calls error_detected(dev, pci_channel_io_normal) to all drivers associated within a hierarchy in question. For example:



```text
Endpoint <==> Downstream Port B <==> Upstream Port A <==> Root Port
```

If Upstream Port A captures an AER error, the hierarchy consists of Downstream Port B and Endpoint.

A driver may return PCI_ERS_RESULT_CAN_RECOVER, PCI_ERS_RESULT_DISCONNECT, or PCI_ERS_RESULT_NEED_RESET, depending on whether it can recover without a reset, considers the device unrecoverable or needs a reset for recovery. If all affected drivers agree that they can recover without a reset, it is skipped. Should one driver request a reset, it overrides all other drivers.

If an error message indicates a fatal error, kernel will broadcast error_detected(dev, pci_channel_io_frozen) to all drivers within a hierarchy in question. Then, performing a reset at upstream is necessary. If error_detected returns PCI_ERS_RESULT_CAN_RECOVER to indicate that recovery without a reset is possible, the error handling goes to mmio_enabled, but afterwards a reset is still performed.

In other words, for non-fatal errors, drivers may opt in to a reset. But for fatal errors, they cannot opt out of a reset, based on the assumption that the link is unreliable.

<a id="rst-frequently-asked-questions"></a>

### Frequently Asked Questions

- **Q:**

  What happens if a PCIe device driver does not provide an error recovery handler (pci_driver-&gt;err_handler is equal to NULL)?

- **A:**

  The devices attached with the driver won't be recovered. The kernel will print out informational messages to identify unrecoverable devices.

<a id="rst-software-error-injection"></a>

## Software error injection

Debugging PCIe AER error recovery code is quite difficult because it is hard to trigger real hardware errors. Software based error injection can be used to fake various kinds of PCIe errors.

First you should enable PCIe AER software error injection in kernel configuration, that is, following item should be in your .config.

CONFIG_PCIEAER_INJECT=y or CONFIG_PCIEAER_INJECT=m

After reboot with new kernel or insert the module, a device file named /dev/aer_inject should be created.

Then, you need a user space tool named aer-inject, which can be gotten from:

> [https://github.com/intel/aer-inject.git](<https://github.com/intel/aer-inject.git>)

More information about aer-inject can be found in the document in its source code.
