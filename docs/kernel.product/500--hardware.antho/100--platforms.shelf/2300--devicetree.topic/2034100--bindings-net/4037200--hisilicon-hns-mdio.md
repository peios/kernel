---
title: "Hisilicon MDIO bus controller"
type: reference
description: "Device-tree binding reference for Hisilicon MDIO bus controller."
---

## Properties:

- compatible: can be one of:
  "hisilicon,hns-mdio"
  "hisilicon,mdio"
  "hisilicon,hns-mdio" is recommended to be used for hip05 and later SOCs,
  while "hisilicon,mdio" is optional for backwards compatibility only on
  hip04 Soc.
- reg: The base address of the MDIO bus controller register bank.
- #address-cells: Must be &lt;1&gt;.
- #size-cells: Must be &lt;0&gt;.  MDIO addresses have no size component.

Typically an MDIO bus might have several children.

## Example:

```dts
         mdio@803c0000 {
                   #address-cells = <1>;
                   #size-cells = <0>;
                   compatible = "hisilicon,hns-mdio","hisilicon,mdio";
                   reg = <0x0 0x803c0000 0x0 0x10000>;

                   ethernet-phy@0 {
                            ...
                            reg = <0>;
                   };
         };
```
