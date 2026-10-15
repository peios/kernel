---
title: "Chrome OS ACPI Device"
type: reference
description: "Hardware functionality specific to Chrome OS is exposed through a Chrome OS ACPI device. The plug and play ID of a Chrome OS ACPI device is GGL0001 and the hardware ID is GOOG0016. The following ACPI objects are supported:"
---

<a id="rst-chrome-os-acpi-device"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

Hardware functionality specific to Chrome OS is exposed through a Chrome OS ACPI device. The plug and play ID of a Chrome OS ACPI device is GGL0001 and the hardware ID is GOOG0016.  The following ACPI objects are supported:


<table>
<caption>Supported ACPI Objects</caption>
<thead>
<tr>
<th>


Object

</th>
<th>


Description

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


CHSW

</td>
<td>


Chrome OS switch positions

</td>
</tr>
<tr>
<td>


HWID

</td>
<td>


Chrome OS hardware ID

</td>
</tr>
<tr>
<td>


FWID

</td>
<td>


Chrome OS firmware version

</td>
</tr>
<tr>
<td>


FRID

</td>
<td>


Chrome OS read-only firmware version

</td>
</tr>
<tr>
<td>


BINF

</td>
<td>


Chrome OS boot information

</td>
</tr>
<tr>
<td>


GPIO

</td>
<td>


Chrome OS GPIO assignments

</td>
</tr>
<tr>
<td>


VBNV

</td>
<td>


Chrome OS NVRAM locations

</td>
</tr>
<tr>
<td>


VDTA

</td>
<td>


Chrome OS verified boot data

</td>
</tr>
<tr>
<td>


FMAP

</td>
<td>


Chrome OS flashmap base address

</td>
</tr>
<tr>
<td>


MLST

</td>
<td>


Chrome OS method list

</td>
</tr>
</tbody>
</table>

<a id="rst-chsw-chrome-os-switch-positions"></a>

## CHSW (Chrome OS switch positions)

This control method returns the switch positions for Chrome OS specific hardware switches.

<a id="rst-arguments"></a>

### Arguments:

None

<a id="rst-result-code"></a>

### Result code:

An integer containing the switch positions as bitfields:


<table>
<tbody>
<tr>
<td>


0x00000002

</td>
<td>


Recovery button was pressed when x86 firmware booted.

</td>
</tr>
<tr>
<td>


0x00000004

</td>
<td>


Recovery button was pressed when EC firmware booted. (required if EC EEPROM is rewritable; otherwise optional)

</td>
</tr>
<tr>
<td>


0x00000020

</td>
<td>


Developer switch was enabled when x86 firmware booted.

</td>
</tr>
<tr>
<td>


0x00000200

</td>
<td>


Firmware write protection was disabled when x86 firmware booted. (required if firmware write protection is controlled through x86 BIOS; otherwise optional)

</td>
</tr>
</tbody>
</table>

All other bits are reserved and should be set to 0.

<a id="rst-hwid-chrome-os-hardware-id"></a>

## HWID (Chrome OS hardware ID)

This control method returns the hardware ID for the Chromebook.

<a id="rst-arguments-1"></a>

### Arguments:

None

<a id="rst-result-code-1"></a>

### Result code:

A null-terminated ASCII string containing the hardware ID from the Model-Specific Data area of EEPROM.

Note that the hardware ID can be up to 256 characters long, including the terminating null.

<a id="rst-fwid-chrome-os-firmware-version"></a>

## FWID (Chrome OS firmware version)

This control method returns the firmware version for the rewritable portion of the main processor firmware.

<a id="rst-arguments-2"></a>

### Arguments:

None

<a id="rst-result-code-2"></a>

### Result code:

A null-terminated ASCII string containing the complete firmware version for the rewritable portion of the main processor firmware.

<a id="rst-frid-chrome-os-read-only-firmware-version"></a>

## FRID (Chrome OS read-only firmware version)

This control method returns the firmware version for the read-only portion of the main processor firmware.

<a id="rst-arguments-3"></a>

### Arguments:

None

<a id="rst-result-code-3"></a>

### Result code:

A null-terminated ASCII string containing the complete firmware version for the read-only (bootstrap + recovery ) portion of the main processor firmware.

<a id="rst-binf-chrome-os-boot-information"></a>

## BINF (Chrome OS boot information)

This control method returns information about the current boot.

<a id="rst-arguments-4"></a>

### Arguments:

None

<a id="rst-result-code-4"></a>

### Result code:



```text
Package {
        Reserved1
        Reserved2
        Active EC Firmware
        Active Main Firmware Type
        Reserved5
}
```


<table>
<thead>
<tr>
<th>


Field

</th>
<th>


Format

</th>
<th>


Description

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


Reserved1

</td>
<td>


DWORD

</td>
<td>


Set to 256 (0x100). This indicates this field is no longer used.

</td>
</tr>
<tr>
<td>


Reserved2

</td>
<td>


DWORD

</td>
<td>


Set to 256 (0x100). This indicates this field is no longer used.

</td>
</tr>
<tr>
<td>


Active EC firmware

</td>
<td>


DWORD

</td>
<td>


The EC firmware which was used during boot.

- 0 - Read-only (recovery) firmware

- 1 - Rewritable firmware.

Set to 0 if EC firmware is always read-only.

</td>
</tr>
<tr>
<td>


Active Main Firmware Type

</td>
<td>


DWORD

</td>
<td>


The main firmware type which was used during boot.

- 0 - Recovery

- 1 - Normal

- 2 - Developer

- 3 - netboot (factory installation only)

Other values are reserved.

</td>
</tr>
<tr>
<td>


Reserved5

</td>
<td>


DWORD

</td>
<td>


Set to 256 (0x100). This indicates this field is no longer used.

</td>
</tr>
</tbody>
</table>

<a id="rst-gpio-chrome-os-gpio-assignments"></a>

## GPIO (Chrome OS GPIO assignments)

This control method returns information about Chrome OS specific GPIO assignments for Chrome OS hardware, so the kernel can directly control that hardware.

<a id="rst-arguments-5"></a>

### Arguments:

None

<a id="rst-result-code-5"></a>

### Result code:



```text
Package {
        Package {
                // First GPIO assignment
                Signal Type        //DWORD
                Attributes         //DWORD
                Controller Offset  //DWORD
                Controller Name    //ASCIIZ
        },
        ...
        Package {
                // Last GPIO assignment
                Signal Type        //DWORD
                Attributes         //DWORD
                Controller Offset  //DWORD
                Controller Name    //ASCIIZ
        }
}
```

Where ASCIIZ means a null-terminated ASCII string.


<table>
<thead>
<tr>
<th>


Field

</th>
<th>


Format

</th>
<th>


Description

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


Signal Type

</td>
<td>


DWORD

</td>
<td>


Type of GPIO signal

- 0x00000001 - Recovery button

- 0x00000002 - Developer mode switch

- 0x00000003 - Firmware write protection switch

- 0x00000100 - Debug header GPIO 0

- ...

- 0x000001FF - Debug header GPIO 255

Other values are reserved.

</td>
</tr>
<tr>
<td>


Attributes

</td>
<td>


DWORD

</td>
<td>


Signal attributes as bitfields:

- 0x00000001 - Signal is active-high (for button, a GPIO value of 1 means the button is pressed; for switches, a GPIO value of 1 means the switch is enabled). If this bit is 0, the signal is active low. Set to 0 for debug header GPIOs.

</td>
</tr>
<tr>
<td>


Controller Offset

</td>
<td>


DWORD

</td>
<td>


GPIO number on the specified controller.

</td>
</tr>
<tr>
<td>


Controller Name

</td>
<td>


ASCIIZ

</td>
<td>


Name of the controller for the GPIO. Currently supported names: "NM10" - Intel NM10 chip

</td>
</tr>
</tbody>
</table>

<a id="rst-vbnv-chrome-os-nvram-locations"></a>

## VBNV (Chrome OS NVRAM locations)

This control method returns information about the NVRAM (CMOS) locations used to communicate with the BIOS.

<a id="rst-arguments-6"></a>

### Arguments:

None

<a id="rst-result-code-6"></a>

### Result code:



```text
Package {
        NV Storage Block Offset  //DWORD
        NV Storage Block Size    //DWORD
}
```


<table>
<thead>
<tr>
<th>


Field

</th>
<th>


Format

</th>
<th>


Description

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


NV Storage Block Offset

</td>
<td>


DWORD

</td>
<td>


Offset in CMOS bank 0 of the verified boot non-volatile storage block, counting from the first writable CMOS byte (that is, offset=0 is the byte following the 14 bytes of clock data).

</td>
</tr>
<tr>
<td>


NV Storage Block Size

</td>
<td>


DWORD

</td>
<td>


Size in bytes of the verified boot non-volatile storage block.

</td>
</tr>
</tbody>
</table>

<a id="rst-fmap-chrome-os-flashmap-address"></a>

## FMAP (Chrome OS flashmap address)

This control method returns the physical memory address of the start of the main processor firmware flashmap.

<a id="rst-arguments-7"></a>

### Arguments:

None

<a id="rst-noneresult-code"></a>

### NoneResult code:

A DWORD containing the physical memory address of the start of the main processor firmware flashmap.

<a id="rst-vdta-chrome-os-verified-boot-data"></a>

## VDTA (Chrome OS verified boot data)

This control method returns the verified boot data block shared between the firmware verification step and the kernel verification step.

<a id="rst-arguments-8"></a>

### Arguments:

None

<a id="rst-result-code-7"></a>

### Result code:

A buffer containing the verified boot data block.

<a id="rst-meck-management-engine-checksum"></a>

## MECK (Management Engine Checksum)

This control method returns the SHA-1 or SHA-256 hash that is read out of the Management Engine extended registers during boot. The hash is exported via ACPI so the OS can verify that the ME firmware has not changed. If Management Engine is not present, or if the firmware was unable to read the extended registers, this buffer can be zero.

<a id="rst-arguments-9"></a>

### Arguments:

None

<a id="rst-result-code-8"></a>

### Result code:

A buffer containing the ME hash.

<a id="rst-mlst-chrome-os-method-list"></a>

## MLST (Chrome OS method list)

This control method returns a list of the other control methods supported by the Chrome OS hardware device.

<a id="rst-arguments-10"></a>

### Arguments:

None

<a id="rst-result-code-9"></a>

### Result code:

A package containing a list of null-terminated ASCII strings, one for each control method supported by the Chrome OS hardware device, not including the MLST method itself. For this version of the specification, the result is:



```text
Package {
        "CHSW",
        "FWID",
        "HWID",
        "FRID",
        "BINF",
        "GPIO",
        "VBNV",
        "FMAP",
        "VDTA",
        "MECK"
}
```
