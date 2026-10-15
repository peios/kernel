---
title: "Hisilicon Network Subsystem NIC controller"
type: reference
description: "Device-tree binding reference for Hisilicon Network Subsystem NIC controller."
---

## Required properties:

- compatible: "hisilicon,hns-nic-v1" or "hisilicon,hns-nic-v2".
  "hisilicon,hns-nic-v1" is for hip05.
  "hisilicon,hns-nic-v2" is for Hi1610 and Hi1612.
- ae-handle: accelerator engine handle for hns,
  specifies a reference to the associating hardware driver node.
  see [Documentation/devicetree/bindings/net/hisilicon-hns-dsaf.txt](<~kernel/hardware/devicetree/bindings-net/hisilicon-hns-dsaf>)
- port-id: is the index of port provided by DSAF (the accelerator). DSAF can
  connect to 8 PHYs. Port 0 to 1 are both used for administration purpose. They
  are called debug ports.

```text
  The remaining 6 PHYs are taken according to the mode of DSAF.
```

```text
  In NIC mode of DSAF, all 6 PHYs are taken as ethernet ports to the CPU. The
  port-id can be 2 to 7. Here is the diagram:
```

```text
            +-----+---------------+
            |            CPU      |
            +-+-+-+---+-+-+-+-+-+-+
              | |     | | | | | |
             debug       service
             port         port
             (0,1)       (2-7)
```

```text
  In Switch mode of DSAF, all 6 PHYs are taken as physical ports connect to a
  LAN Switch while the CPU side assume itself have one single NIC connect to
  this switch. In this case, the port-id will be 2 only.
```

```text
            +-----+---------------+
            |            CPU      |
            +-+-+-+---+-+-+-+-+-+-+
              | |   service| port(2)
             debug   +------------+
             port    |   switch   |
             (0,1)   +-+-+-+-+-+-++
                       | | | | | |
                      external port
```

```text
  This attribute is remained for compatible purpose. It is not recommended to
  use it in new code.
```

- port-idx-in-ae: is the index of port provided by AE.
  In NIC mode of DSAF, all 6 PHYs of service DSAF are taken as ethernet ports
  to the CPU. The port-idx-in-ae can be 0 to 5. Here is the diagram:
  +-----+---------------+
  |            CPU      |
  +-+-+-+---+-+-+-+-+-+-+
  |    |   | | | | | |
  debug debug   service
  port  port     port
  (0)   (0)     (0-5)

```text
  In Switch mode of DSAF, all 6 PHYs of service DSAF are taken as physical
  ports connected to a LAN Switch while the CPU side assume itself have one
  single NIC connected to this switch. In this case, the port-idx-in-ae
  will be 0 only.
```

```text
            +-----+-----+------+------+
            |                CPU      |
            +-+-+-+-+-+-+-+-+-+-+-+-+-+
              |    |     service| port(0)
            debug debug  +------------+
            port  port   |   switch   |
            (0)   (0)    +-+-+-+-+-+-++
                          | | | | | |
                         external port
```

- local-mac-address: mac addr of the ethernet interface

## Example:

```dts
	ethernet@0{
		compatible = "hisilicon,hns-nic-v1";
		ae-handle = <&dsaf0>;
		port-idx-in-ae = <0>;
		local-mac-address = [a2 14 e4 4b 56 76];
	};
```
