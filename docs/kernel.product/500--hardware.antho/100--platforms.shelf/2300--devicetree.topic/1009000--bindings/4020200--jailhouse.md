---
title: "Jailhouse non-root cell device tree bindings"
type: reference
description: "Device-tree binding reference for Jailhouse non-root cell device tree bindings."
---

When running in a non-root Jailhouse cell (partition), the device tree of this
platform shall have a top-level "hypervisor" node with the following
properties:

- compatible = "jailhouse,cell"
