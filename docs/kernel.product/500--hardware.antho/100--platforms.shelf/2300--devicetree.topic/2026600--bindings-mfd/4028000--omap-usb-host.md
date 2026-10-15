---
title: "OMAP HS USB Host"
type: reference
description: "Device-tree binding reference for OMAP HS USB Host."
---

## Required properties:

- compatible: should be "ti,usbhs-host"
- reg: should contain one register range i.e. start and length
- ti,hwmods: must contain "usb\_host\_hs"

## Optional properties:

- num-ports: number of USB ports. Usually this is automatically detected
  from the IP's revision register but can be overridden by specifying
  this property. A maximum of 3 ports are supported at the moment.

- portN-mode: String specifying the port mode for port N, where N can be
  from 1 to 3. If the port mode is not specified, that port is treated
  as unused. When specified, it must be one of the following.
  "ehci-phy",
  "ehci-tll",
  "ehci-hsic",
  "ohci-phy-6pin-datse0",
  "ohci-phy-6pin-dpdm",
  "ohci-phy-3pin-datse0",
  "ohci-phy-4pin-dpdm",
  "ohci-tll-6pin-datse0",
  "ohci-tll-6pin-dpdm",
  "ohci-tll-3pin-datse0",
  "ohci-tll-4pin-dpdm",
  "ohci-tll-2pin-datse0",
  "ohci-tll-2pin-dpdm",

- single-ulpi-bypass: Must be present if the controller contains a single
  ULPI bypass control bit. e.g. OMAP3 silicon &lt;= ES2.1

- clocks: a list of phandles and clock-specifier pairs, one for each entry in
  clock-names.

```text
- clock-names: should include:
  For OMAP3
  * "usbhost_120m_fck" - 120MHz Functional clock.
```

```text
  For OMAP4+
```

- "refclk\_60m\_int" - 60MHz internal reference clock for UTMI clock mux
- "refclk\_60m\_ext\_p1" - 60MHz external ref. clock for Port 1's UTMI clock mux.
- "refclk\_60m\_ext\_p2" - 60MHz external ref. clock for Port 2's UTMI clock mux
- "utmi\_p1\_gfclk" - Port 1 UTMI clock mux.
- "utmi\_p2\_gfclk" - Port 2 UTMI clock mux.
- "usb\_host\_hs\_utmi\_p1\_clk" - Port 1 UTMI clock gate.
- "usb\_host\_hs\_utmi\_p2\_clk" - Port 2 UTMI clock gate.
- "usb\_host\_hs\_utmi\_p3\_clk" - Port 3 UTMI clock gate.
- "usb\_host\_hs\_hsic480m\_p1\_clk" - Port 1 480MHz HSIC clock gate.
- "usb\_host\_hs\_hsic480m\_p2\_clk" - Port 2 480MHz HSIC clock gate.
- "usb\_host\_hs\_hsic480m\_p3\_clk" - Port 3 480MHz HSIC clock gate.
- "usb\_host\_hs\_hsic60m\_p1\_clk" - Port 1 60MHz HSIC clock gate.
- "usb\_host\_hs\_hsic60m\_p2\_clk" - Port 2 60MHz HSIC clock gate.
- "usb\_host\_hs\_hsic60m\_p3\_clk" - Port 3 60MHz HSIC clock gate.

## Required properties if child node exists:

- #address-cells: Must be 1
- #size-cells: Must be 1
- ranges: must be present

## Properties for children:

The OMAP HS USB Host subsystem contains EHCI and OHCI controllers.
See [Documentation/devicetree/bindings/usb/generic-ehci.yaml](<~kernel/hardware/devicetree-bindings/dt-usb/generic-ehci>) and
[Documentation/devicetree/bindings/usb/generic-ohci.yaml](<~kernel/hardware/devicetree-bindings/dt-usb/generic-ohci>).

## Example for OMAP4:

```dts
usbhshost: usbhshost@4a064000 {
	compatible = "ti,usbhs-host";
	reg = <0x4a064000 0x800>;
	ti,hwmods = "usb_host_hs";
	#address-cells = <1>;
	#size-cells = <1>;
	ranges;

	usbhsohci: ohci@4a064800 {
		compatible = "ti,ohci-omap3";
		reg = <0x4a064800 0x400>;
		interrupt-parent = <&gic>;
		interrupts = <0 76 0x4>;
	};

	usbhsehci: ehci@4a064c00 {
		compatible = "ti,ehci-omap";
		reg = <0x4a064c00 0x400>;
		interrupt-parent = <&gic>;
		interrupts = <0 77 0x4>;
	};
};
```

```dts
&usbhshost {
	port1-mode = "ehci-phy";
	port2-mode = "ehci-tll";
	port3-mode = "ehci-phy";
};
```

```dts
&usbhsehci {
	phys = <&hsusb1_phy 0 &hsusb3_phy>;
};
```
