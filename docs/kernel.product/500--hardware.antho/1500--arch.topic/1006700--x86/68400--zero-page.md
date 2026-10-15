---
title: "Zero Page"
type: reference
description: "The additional fields in struct boot_params as a part of 32-bit boot protocol of kernel. These should be filled by bootloader or 16-bit real-mode setup code of the kernel. References/settings to it mainly are in:"
---

<a id="rst-zero-page"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

The additional fields in struct boot_params as a part of 32-bit boot protocol of kernel. These should be filled by bootloader or 16-bit real-mode setup code of the kernel. References/settings to it mainly are in:



```text
arch/x86/include/uapi/asm/bootparam.h
```


<table>
<tbody>
<tr>
<td>


Offset/Size

</td>
<td>


Proto

</td>
<td>


Name

</td>
<td>


Meaning

</td>
</tr>
<tr>
<td>


000/040

</td>
<td>


ALL

</td>
<td>


screen_info

</td>
<td>


Text mode or frame buffer information (struct screen_info)

</td>
</tr>
<tr>
<td>


040/014

</td>
<td>


ALL

</td>
<td>


apm_bios_info

</td>
<td>


APM BIOS information (struct apm_bios_info)

</td>
</tr>
<tr>
<td>


058/008

</td>
<td>


ALL

</td>
<td>


tboot_addr

</td>
<td>


Physical address of tboot shared page

</td>
</tr>
<tr>
<td>


060/010

</td>
<td>


ALL

</td>
<td>


ist_info

</td>
<td>


Intel SpeedStep (IST) BIOS support information (struct ist_info)

</td>
</tr>
<tr>
<td>


070/008

</td>
<td>


ALL

</td>
<td>


acpi_rsdp_addr

</td>
<td>


Physical address of ACPI RSDP table

</td>
</tr>
<tr>
<td>


080/010

</td>
<td>


ALL

</td>
<td>


hd0_info

</td>
<td>


hd0 disk parameter, OBSOLETE\!\!

</td>
</tr>
<tr>
<td>


090/010

</td>
<td>


ALL

</td>
<td>


hd1_info

</td>
<td>


hd1 disk parameter, OBSOLETE\!\!

</td>
</tr>
<tr>
<td>


0A0/010

</td>
<td>


ALL

</td>
<td>


sys_desc_table

</td>
<td>


System description table (struct sys_desc_table), OBSOLETE\!\!

</td>
</tr>
<tr>
<td>


0B0/010

</td>
<td>


ALL

</td>
<td>


olpc_ofw_header

</td>
<td>


OLPC's OpenFirmware CIF and friends

</td>
</tr>
<tr>
<td>


0C0/004

</td>
<td>


ALL

</td>
<td>


ext_ramdisk_image

</td>
<td>


ramdisk_image high 32bits

</td>
</tr>
<tr>
<td>


0C4/004

</td>
<td>


ALL

</td>
<td>


ext_ramdisk_size

</td>
<td>


ramdisk_size high 32bits

</td>
</tr>
<tr>
<td>


0C8/004

</td>
<td>


ALL

</td>
<td>


ext_cmd_line_ptr

</td>
<td>


cmd_line_ptr high 32bits

</td>
</tr>
<tr>
<td>


13C/004

</td>
<td>


ALL

</td>
<td>


cc_blob_address

</td>
<td>


Physical address of Confidential Computing blob

</td>
</tr>
<tr>
<td>


140/080

</td>
<td>


ALL

</td>
<td>


edid_info

</td>
<td>


Video mode setup (struct edid_info)

</td>
</tr>
<tr>
<td>


1C0/020

</td>
<td>


ALL

</td>
<td>


efi_info

</td>
<td>


EFI 32 information (struct efi_info)

</td>
</tr>
<tr>
<td>


1E0/004

</td>
<td>


ALL

</td>
<td>


alt_mem_k

</td>
<td>


Alternative mem check, in KB

</td>
</tr>
<tr>
<td>


1E4/004

</td>
<td>


ALL

</td>
<td>


scratch

</td>
<td>


Scratch field for the kernel setup code

</td>
</tr>
<tr>
<td>


1E8/001

</td>
<td>


ALL

</td>
<td>


e820_entries

</td>
<td>


Number of entries in e820_table (below)

</td>
</tr>
<tr>
<td>


1E9/001

</td>
<td>


ALL

</td>
<td>


eddbuf_entries

</td>
<td>


Number of entries in eddbuf (below)

</td>
</tr>
<tr>
<td>


1EA/001

</td>
<td>


ALL

</td>
<td>


edd_mbr_sig_buf_entries

</td>
<td>


Number of entries in edd_mbr_sig_buffer (below)

</td>
</tr>
<tr>
<td>


1EB/001

</td>
<td>


ALL

</td>
<td>


kbd_status

</td>
<td>


Numlock is enabled

</td>
</tr>
<tr>
<td>


1EC/001

</td>
<td>


ALL

</td>
<td>


secure_boot

</td>
<td>


Secure boot is enabled in the firmware

</td>
</tr>
<tr>
<td>


1EF/001

</td>
<td>


ALL

</td>
<td>


sentinel

</td>
<td>


Used to detect broken bootloaders

</td>
</tr>
<tr>
<td>


290/040

</td>
<td>


ALL

</td>
<td>


edd_mbr_sig_buffer

</td>
<td>


EDD MBR signatures

</td>
</tr>
<tr>
<td>


2D0/A00

</td>
<td>


ALL

</td>
<td>


e820_table

</td>
<td>


E820 memory map table (array of struct e820_entry)

</td>
</tr>
<tr>
<td>


D00/1EC

</td>
<td>


ALL

</td>
<td>


eddbuf

</td>
<td>


EDD data (array of struct edd_info)

</td>
</tr>
</tbody>
</table>
