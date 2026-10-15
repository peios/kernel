---
title: "Linux kernel networking driver for Marvell's Octeon PCI Endpoint NIC"
type: reference
description: "Network driver for Marvell's Octeon PCI EndPoint NIC. Copyright (c) 2020 Marvell International Ltd."
---

<a id="rst-linux-kernel-networking-driver-for-marvell-s-octeon-pci-endpoint-nic"></a>

<!-- SPDX-License-Identifier: GPL-2.0+ -->

Network driver for Marvell's Octeon PCI EndPoint NIC. Copyright (c) 2020 Marvell International Ltd.

<a id="rst-contents"></a>

## Contents

- [Overview](<#rst-overview>)

- [Supported Devices](<#rst-supported-devices>)

- [Interface Control](<#rst-interface-control>)

<a id="rst-overview"></a>

## Overview

This driver implements networking functionality of Marvell's Octeon PCI EndPoint NIC.

<a id="rst-supported-devices"></a>

## Supported Devices

- **Currently, this driver support following devices:**

  - Network controller: Cavium, Inc. Device b100

  - Network controller: Cavium, Inc. Device b200

  - Network controller: Cavium, Inc. Device b400

  - Network controller: Cavium, Inc. Device b900

  - Network controller: Cavium, Inc. Device ba00

  - Network controller: Cavium, Inc. Device bc00

  - Network controller: Cavium, Inc. Device bd00

<a id="rst-interface-control"></a>

## Interface Control

Network Interface control like changing mtu, link speed, link down/up are done by writing command to mailbox command queue, a mailbox interface implemented through a reserved region in BAR4. This driver writes the commands into the mailbox and the firmware on the Octeon device processes them. The firmware also sends unsolicited notifications to driver for events suchs as link change, through notification queue implemented as part of mailbox interface.
