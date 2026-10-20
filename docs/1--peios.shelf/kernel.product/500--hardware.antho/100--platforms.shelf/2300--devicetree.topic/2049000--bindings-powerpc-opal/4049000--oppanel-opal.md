---
title: "IBM OPAL Operator Panel Binding"
type: reference
description: "Device-tree binding reference for IBM OPAL Operator Panel Binding."
---

## Required properties:

- compatible : Should be "ibm,opal-oppanel".
- #lines     : Number of lines on the operator panel e.g. &lt;0x2&gt;.
- #length    : Number of characters per line of the operator panel e.g. &lt;0x10&gt;.

## Example:

```dts
	oppanel {
		compatible = "ibm,opal-oppanel";
		#lines = <0x2>;
		#length = <0x10>;
	};
```
