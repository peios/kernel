---
title: "Kernel driver i2c-viapro"
type: reference
description: "VIA Technologies, Inc. VT82C596A/B Datasheet: Sometimes available at the VIA website"
---

<a id="rst-kernel-driver-i2c-viapro"></a>

- **Supported adapters:**

  - VIA Technologies, Inc. VT82C596A/B Datasheet: Sometimes available at the VIA website

  - VIA Technologies, Inc. VT82C686A/B Datasheet: Sometimes available at the VIA website

  - VIA Technologies, Inc. VT8231, VT8233, VT8233A Datasheet: available on request from VIA

  - VIA Technologies, Inc. VT8235, VT8237R, VT8237A, VT8237S, VT8251 Datasheet: available on request and under NDA from VIA

  - VIA Technologies, Inc. CX700 Datasheet: available on request and under NDA from VIA

  - VIA Technologies, Inc. VX800/VX820 Datasheet: available on [http://linux.via.com.tw](<http://linux.via.com.tw>)

  - VIA Technologies, Inc. VX855/VX875 Datasheet: available on [http://linux.via.com.tw](<http://linux.via.com.tw>)

  - VIA Technologies, Inc. VX900 Datasheet: available on [http://linux.via.com.tw](<http://linux.via.com.tw>)

- **Authors:**

  - Kyösti Mälkki &lt;[kmalkki@cc.hut.fi](<mailto:kmalkki@cc.hut.fi>)&gt;,

  - Mark D. Studebaker &lt;[mdsxyz123@yahoo.com](<mailto:mdsxyz123@yahoo.com>)&gt;,

  - Jean Delvare &lt;[jdelvare@suse.de](<mailto:jdelvare@suse.de>)&gt;

<a id="rst-module-parameters"></a>

## Module Parameters

- force: int Forcibly enable the SMBus controller. DANGEROUS\!

- force_addr: int Forcibly enable the SMBus at the given address. EXTREMELY DANGEROUS\!

<a id="rst-description"></a>

## Description

i2c-viapro is a true SMBus host driver for motherboards with one of the supported VIA south bridges.

Your `lspci -n` listing must show one of these :

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> device 1106:3050
>
> </td>
> <td>
>
>
> (VT82C596A function 3)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> device 1106:3051
>
> </td>
> <td>
>
>
> (VT82C596B function 3)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> device 1106:3057
>
> </td>
> <td>
>
>
> (VT82C686 function 4)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> device 1106:3074
>
> </td>
> <td>
>
>
> (VT8233)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> device 1106:3147
>
> </td>
> <td>
>
>
> (VT8233A)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> device 1106:8235
>
> </td>
> <td>
>
>
> (VT8231 function 4)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> device 1106:3177
>
> </td>
> <td>
>
>
> (VT8235)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> device 1106:3227
>
> </td>
> <td>
>
>
> (VT8237R)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> device 1106:3337
>
> </td>
> <td>
>
>
> (VT8237A)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> device 1106:3372
>
> </td>
> <td>
>
>
> (VT8237S)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> device 1106:3287
>
> </td>
> <td>
>
>
> (VT8251)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> device 1106:8324
>
> </td>
> <td>
>
>
> (CX700)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> device 1106:8353
>
> </td>
> <td>
>
>
> (VX800/VX820)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> device 1106:8409
>
> </td>
> <td>
>
>
> (VX855/VX875)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> device 1106:8410
>
> </td>
> <td>
>
>
> (VX900)
>
> </td>
> </tr>
> </tbody>
> </table>

If none of these show up, you should look in the BIOS for settings like enable ACPI / SMBus or even USB.

Except for the oldest chips (VT82C596A/B, VT82C686A and most probably VT8231), this driver supports I2C block transactions. Such transactions are mainly useful to read from and write to EEPROMs.

The CX700/VX800/VX820 additionally appears to support SMBus PEC, although this driver doesn't implement it yet.
