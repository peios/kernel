---
title: "ACPI WMI interface"
type: reference
description: "The ACPI WMI interface is a proprietary extension of the ACPI specification made by Microsoft to allow hardware vendors to embed WMI (Windows Management Instrumentation) objects inside their ACPI firmware. Typical functions implemented…"
---

<a id="rst-acpi-wmi-interface"></a>

<!-- SPDX-License-Identifier: GPL-2.0-or-later -->

The ACPI WMI interface is a proprietary extension of the ACPI specification made by Microsoft to allow hardware vendors to embed WMI (Windows Management Instrumentation) objects inside their ACPI firmware. Typical functions implemented over ACPI WMI are hotkey events on modern notebooks and configuration of BIOS options.

<a id="rst-pnp0c14-acpi-device"></a>

## PNP0C14 ACPI device

Discovery of WMI objects is handled by defining ACPI devices with a PNP ID of `PNP0C14`. These devices will contain a set of ACPI buffers and methods used for mapping and execution of WMI methods and/or queries. If there exist multiple of such devices, then each device is required to have a unique ACPI UID.

<a id="rst-wdg-buffer"></a>

## \_WDG buffer

The `_WDG` buffer is used to discover WMI objects and is required to be static. Its internal structure consists of data blocks with a size of 20 bytes, containing the following data:


<table>
<thead>
<tr>
<th>


Offset

</th>
<th>


Size (in bytes)

</th>
<th>


Content

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


0x00

</td>
<td>


16

</td>
<td>


128 bit Variant 2 object GUID.

</td>
</tr>
<tr>
<td>


0x10

</td>
<td>


2

</td>
<td>


2 character method ID or single byte notification ID.

</td>
</tr>
<tr>
<td>


0x12

</td>
<td>


1

</td>
<td>


Object instance count.

</td>
</tr>
<tr>
<td>


0x13

</td>
<td>


1

</td>
<td>


Object flags.

</td>
</tr>
</tbody>
</table>

The WMI object flags control whether the method or notification ID is used:

- 0x1: Data block is expensive to collect.

- 0x2: Data block contains WMI methods.

- 0x4: Data block contains ASCIZ string.

- 0x8: Data block describes a WMI event, use notification ID instead of method ID.

Each WMI object GUID can appear multiple times inside a system. The method/notification ID is used to construct the ACPI method names used for interacting with the WMI object.

<a id="rst-wqxx-acpi-methods"></a>

## WQxx ACPI methods

If a data block does not contain WMI methods, then its content can be retrieved by this required ACPI method. The last two characters of the ACPI method name are the method ID of the data block to query. Their single parameter is an integer describing the instance which should be queried. This parameter can be omitted if the data block contains only a single instance.

<a id="rst-wsxx-acpi-methods"></a>

## WSxx ACPI methods

Similar to the `WQxx` ACPI methods, except that it is optional and takes an additional buffer as its second argument. The instance argument also cannot be omitted.

<a id="rst-wmxx-acpi-methods"></a>

## WMxx ACPI methods

Used for executing WMI methods associated with a data block. The last two characters of the ACPI method name are the method ID of the data block containing the WMI methods. Their first parameter is a integer describing the instance which methods should be executed. The second parameter is an integer describing the WMI method ID to execute, and the third parameter is a buffer containing the WMI method parameters. If the data block is marked as containing an ASCIZ string, then this buffer should contain an ASCIZ string. The ACPI method will return the result of the executed WMI method.

<a id="rst-wexx-acpi-methods"></a>

## WExx ACPI methods

Used for optionally enabling/disabling WMI events, the last two characters of the ACPI method are the notification ID of the data block describing the WMI event as hexadecimal value. Their first parameter is an integer with a value of 0 if the WMI event should be disabled, other values will enable the WMI event.

Those ACPI methods are always called even for WMI events not registered as being expensive to collect to match the behavior of the Windows driver.

<a id="rst-wcxx-acpi-methods"></a>

## WCxx ACPI methods

Similar to the `WExx` ACPI methods, except that instead of WMI events it controls data collection of data blocks registered as being expensive to collect. Thus the last two characters of the ACPI method name are the method ID of the data block to enable/disable.

Those ACPI methods are also called before setting data blocks to match the behavior of the Windows driver.

<a id="rst-wed-acpi-method"></a>

## \_WED ACPI method

Used to retrieve additional WMI event data, its single parameter is a integer holding the notification ID of the event. This method should be evaluated every time an ACPI notification is received, since some ACPI implementations use a queue to store WMI event data items. This queue will overflow after a couple of WMI events are received without retrieving the associated WMI event data.

<a id="rst-conversion-rules-for-acpi-data-types"></a>

## Conversion rules for ACPI data types

Consumers of the ACPI-WMI interface use binary buffers to exchange data with the WMI driver core, with the internal structure of the buffer being only know to the consumers. The WMI driver core is thus responsible for converting the data inside the buffer into an appropriate ACPI data type for consumption by the ACPI firmware. Additionally, any data returned by the various ACPI methods needs to be converted back into a binary buffer.

The layout of said buffers is defined by the MOF description of the WMI method or data block in question <a id="rst-footnote-reference-1"></a>[1](#rst-footnote-1):


<table>
<thead>
<tr>
<th>


Data Type

</th>
<th>


Layout

</th>
<th>


Alignment

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


`string`

</td>
<td>


Starts with an unsigned 16-bit little endian integer specifying the length of the string data in bytes, followed by the string data encoded as UTF-16LE with **optional** NULL termination and padding. Keep in mind that some firmware implementations might depend on the terminating NULL character to be present. Also the padding should always be performed with NULL characters.

</td>
<td>


2 bytes

</td>
</tr>
<tr>
<td>


`boolean`

</td>
<td>


Single byte where 0 means `false` and nonzero means `true`.

</td>
<td>


1 byte

</td>
</tr>
<tr>
<td>


`sint8`

</td>
<td>


Signed 8-bit integer.

</td>
<td>


1 byte

</td>
</tr>
<tr>
<td>


`uint8`

</td>
<td>


Unsigned 8-bit integer.

</td>
<td>


1 byte

</td>
</tr>
<tr>
<td>


`sint16`

</td>
<td>


Signed 16-bit little endian integer.

</td>
<td>


2 bytes

</td>
</tr>
<tr>
<td>


`uint16`

</td>
<td>


Unsigned 16-bit little endian integer.

</td>
<td>


2 bytes

</td>
</tr>
<tr>
<td>


`sint32`

</td>
<td>


Signed 32-bit little endian integer.

</td>
<td>


4 bytes

</td>
</tr>
<tr>
<td>


`uint32`

</td>
<td>


Unsigned 32-bit little endian integer.

</td>
<td>


4 bytes

</td>
</tr>
<tr>
<td>


`sint64`

</td>
<td>


Signed 64-bit little endian integer.

</td>
<td>


8 bytes

</td>
</tr>
<tr>
<td>


`uint64`

</td>
<td>


Unsigned 64-bit little endian integer.

</td>
<td>


8 bytes

</td>
</tr>
<tr>
<td>


`datetime`

</td>
<td>


A fixed-length 25-character UTF-16LE string with the format *yyyymmddhhmmss.mmmmmmsutc* where *yyyy* is the 4-digit year, *mm* is the 2-digit month, *dd* is the 2-digit day, *hh* is the 2-digit hour based on a 24-hour clock, *mm* is the 2-digit minute, *ss* is the 2-digit second, *mmmmmm* is the 6-digit microsecond, *s* is a plus or minus character depending on whether *utc* is a positive or negative offset from UTC (or a colon if the date is an interval). Unpopulated fields should be filled with asterisks.

</td>
<td>


2 bytes

</td>
</tr>
</tbody>
</table>

Arrays should be aligned based on the alignment of their base type, while objects should be aligned based on the largest alignment of an element inside them.

All buffers returned by the WMI driver core are 8-byte aligned. When converting ACPI data types into such buffers the following conversion rules apply:


<table>
<thead>
<tr>
<th>


ACPI Data Type

</th>
<th>


Converted into

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


Buffer

</td>
<td>


Copied as-is.

</td>
</tr>
<tr>
<td>


Integer

</td>
<td>


Converted into a `uint32`.

</td>
</tr>
<tr>
<td>


String

</td>
<td>


Converted into a `string` with a terminating NULL character to match the behavior the of the Windows driver.

</td>
</tr>
<tr>
<td>


Package

</td>
<td>


Each element inside the package is converted with alignment of the resulting data types being respected. Nested packages are not allowed.

</td>
</tr>
</tbody>
</table>

The Windows driver does attempt to handle nested packages, but this results in internal data structures (`_ACPI_METHOD_ARGUMENT_V1`) erroneously being copied into the resulting buffer. ACPI firmware implementations should thus not return nested packages from ACPI methods associated with the ACPI-WMI interface.

<a id="rst-references"></a>

### References

<a id="rst-footnote-1"></a>



**[1]** [https://learn.microsoft.com/en-us/windows-hardware/drivers/kernel/driver-defined-wmi-data-items](<https://learn.microsoft.com/en-us/windows-hardware/drivers/kernel/driver-defined-wmi-data-items>)
