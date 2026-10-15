---
title: "Kernel driver i2c-taos-evm"
type: reference
description: "Author: Jean Delvare <jdelvare@suse.de>"
---

<a id="rst-kernel-driver-i2c-taos-evm"></a>

Author: Jean Delvare &lt;[jdelvare@suse.de](<mailto:jdelvare@suse.de>)&gt;

This is a driver for the evaluation modules for TAOS I2C/SMBus chips. The modules include an SMBus master with limited capabilities, which can be controlled over the serial port. Virtually all evaluation modules are supported, but a few lines of code need to be added for each new module to instantiate the right I2C chip on the bus. Obviously, a driver for the chip in question is also needed.

Currently supported devices are:

- TAOS TSL2550 EVM

- **For additional information on TAOS products, please see**

  [http://www.taosinc.com/](<http://www.taosinc.com/>)

<a id="rst-using-this-driver"></a>

## Using this driver

In order to use this driver, you'll need the serport driver, and the inputattach tool, which is part of the input-utils package. The following commands will tell the kernel that you have a TAOS EVM on the first serial port:



```text
# modprobe serport
# inputattach --taos-evm /dev/ttyS0
```

<a id="rst-technical-details"></a>

## Technical details

Only 4 SMBus transaction types are supported by the TAOS evaluation modules: \* Receive Byte \* Send Byte \* Read Byte \* Write Byte

The communication protocol is text-based and pretty simple. It is described in a PDF document on the CD which comes with the evaluation module. The communication is rather slow, because the serial port has to operate at 1200 bps. However, I don't think this is a big concern in practice, as these modules are meant for evaluation and testing only.
