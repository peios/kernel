---
title: "Altera Mailbox Driver"
type: reference
description: "Device-tree binding reference for Altera Mailbox Driver."
---

## Required properties:

- compatible :	"altr,mailbox-1.0".
- reg : 	physical base address of the mailbox and length of
  memory mapped region.
- #mbox-cells:	Common mailbox binding property to identify the number
  of cells required for the mailbox specifier. Should be 1.

## Optional properties:

- interrupts :		interrupt number. The interrupt specifier format
  depends on the interrupt controller parent.

## Example:

```dts
	mbox_tx: mailbox@100 {
		compatible = "altr,mailbox-1.0";
		reg = <0x100 0x8>;
		interrupt-parent = < &gic_0 >;
		interrupts = <5>;
		#mbox-cells = <1>;
	};
```

```dts
	mbox_rx: mailbox@200 {
		compatible = "altr,mailbox-1.0";
		reg = <0x200 0x8>;
		interrupt-parent = < &gic_0 >;
		interrupts = <6>;
		#mbox-cells = <1>;
	};
```

## Mailbox client

"mboxes" and the optional "mbox-names" (please see
[Documentation/devicetree/bindings/mailbox/mailbox.txt](<~kernel/hardware/devicetree/bindings-mailbox/mailbox>) for details). Each value
of the mboxes property should contain a phandle to the mailbox controller
device node and second argument is the channel index. It must be 0 (hardware
support only one channel).The equivalent "mbox-names" property value can be
used to give a name to the communication channel to be used by the client user.

## Example:

```dts
	mclient0: mclient0@400 {
		compatible = "client-1.0";
		reg = <0x400 0x10>;
		mbox-names = "mbox-tx", "mbox-rx";
		mboxes = <&mbox_tx 0>,
			 <&mbox_rx 0>;
	};
```
