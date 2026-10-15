---
title: "Devicetree Dynamic Resolver Notes"
type: reference
description: "This document describes the implementation of the in-kernel DeviceTree resolver, residing in drivers/of/resolver.c"
---

<a id="rst-devicetree-dynamic-resolver-notes"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

This document describes the implementation of the in-kernel DeviceTree resolver, residing in drivers/of/resolver.c

<a id="rst-how-the-resolver-works"></a>

## How the resolver works

The resolver is given as an input an arbitrary tree compiled with the proper dtc option and having a /plugin/ tag. This generates the appropriate \_\_fixups\_\_ &amp; \_\_local\_fixups\_\_ nodes.

In sequence the resolver works by the following steps:

1. Get the maximum device tree phandle value from the live tree + 1.

2. Adjust all the local phandles of the tree to resolve by that amount.

3. Using the \_\_local\_\_fixups\_\_ node information adjust all local references by the same amount.

4. For each property in the \_\_fixups\_\_ node locate the node it references in the live tree. This is the label used to tag the node.

5. Retrieve the phandle of the target of the fixup.

6. For each fixup in the property locate the node:property:offset location and replace it with the phandle value.
