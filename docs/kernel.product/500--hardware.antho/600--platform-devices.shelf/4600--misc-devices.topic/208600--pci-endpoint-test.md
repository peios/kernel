---
title: "Driver for PCI Endpoint Test Function"
type: reference
description: "This driver should be used as a host side driver if the root complex is connected to a configurable PCI endpoint running pci_epf_test function driver configured according to 1."
---

<a id="rst-driver-for-pci-endpoint-test-function"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

This driver should be used as a host side driver if the root complex is connected to a configurable PCI endpoint running `pci_epf_test` function driver configured according to <a id="rst-footnote-reference-1"></a>[1](#rst-footnote-1).

The "pci_endpoint_test" driver can be used to perform the following tests.

The PCI driver for the test device performs the following tests:

> 1. verifying addresses programmed in BAR
>
> 2. raise legacy IRQ
>
> 3. raise MSI IRQ
>
> 4. raise MSI-X IRQ
>
> 5. read data
>
> 6. write data
>
> 7. copy data

This misc driver creates /dev/pci-endpoint-test.&lt;num&gt; for every `pci_epf_test` function connected to the root complex and "ioctls" should be used to perform the above tests.

<a id="rst-ioctl"></a>

## ioctl

> - **PCITEST_BAR:**
>
>   Tests the BAR. The number of the BAR to be tested should be passed as argument.
>
> - **PCITEST_LEGACY_IRQ:**
>
>   Tests legacy IRQ
>
> - **PCITEST_MSI:**
>
>   Tests message signalled interrupts. The MSI number to be tested should be passed as argument.
>
> - **PCITEST_MSIX:**
>
>   Tests message signalled interrupts. The MSI-X number to be tested should be passed as argument.
>
> - **PCITEST_SET_IRQTYPE:**
>
>   Changes driver IRQ type configuration. The IRQ type should be passed as argument (0: Legacy, 1:MSI, 2:MSI-X).
>
> - **PCITEST_GET_IRQTYPE:**
>
>   Gets driver IRQ type configuration.
>
> - **PCITEST_WRITE:**
>
>   Perform write tests. The size of the buffer should be passed as argument.
>
> - **PCITEST_READ:**
>
>   Perform read tests. The size of the buffer should be passed as argument.
>
> - **PCITEST_COPY:**
>
>   Perform read tests. The size of the buffer should be passed as argument.

<a id="rst-footnote-1"></a>



**[1]** [Documentation/PCI/endpoint/function/binding/pci-test.rst](~kernel/hardware/pci/endpoint-function-binding/pci-test)
