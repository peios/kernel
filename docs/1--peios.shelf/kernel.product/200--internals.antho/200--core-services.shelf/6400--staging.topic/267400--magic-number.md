---
title: "Linux magic numbers"
type: reference
description: "This file is a registry of magic numbers which are in use. When you add a magic number to a structure, you should also add it to this file, since it is best if the magic numbers used by various structures are unique."
---

<a id="rst-linux-magic-numbers"></a>
<a id="rst-magicnumbers"></a>

This file is a registry of magic numbers which are in use.  When you add a magic number to a structure, you should also add it to this file, since it is best if the magic numbers used by various structures are unique.

It is a <strong>very</strong> good idea to protect kernel data structures with magic numbers.  This allows you to check at run time whether (a) a structure has been clobbered, or (b) you've passed the wrong structure to a routine.  This last is especially useful --- particularly when you are passing pointers to structures via a void \* pointer.  The tty code, for example, does this frequently to pass driver-specific and line discipline-specific structures back and forth.

The way to use magic numbers is to declare them at the beginning of the structure, like so:



```text
struct tty_ldisc {
        int     magic;
        ...
};
```

Please follow this discipline when you are adding future enhancements to the kernel\!  It has saved me countless hours of debugging, especially in the screwy cases where an array has been overrun and structures following the array have been overwritten.  Using this discipline, these cases get detected quickly and safely.

Changelog:



```text
                                      Theodore Ts'o
                                      31 Mar 94

The magic table is current to Linux 2.1.55.

                                      Michael Chastain
                                      <mailto:mec@shout.net>
                                      22 Sep 1997

Now it should be up to date with Linux 2.1.112. Because
we are in feature freeze time it is very unlikely that
something will change before 2.2.x. The entries are
sorted by number field.

                                      Krzysztof G. Baranowski
                                      <mailto: kgb@knm.org.pl>
                                      29 Jul 1998

Updated the magic table to Linux 2.5.45. Right over the feature freeze,
but it is possible that some new magic numbers will sneak into the
kernel before 2.6.x yet.

                                      Petr Baudis
                                      <pasky@ucw.cz>
                                      03 Nov 2002

Updated the magic table to Linux 2.5.74.

                                      Fabian Frederick
                                      <ffrederick@users.sourceforge.net>
                                      09 Jul 2003
```


<table>
<thead>
<tr>
<th>



Magic Name

</th>
<th>



Number

</th>
<th>



Structure

</th>
<th>



File

</th>
</tr>
</thead>
<tbody>
<tr>
<td>



PG\_MAGIC

</td>
<td>



'P'

</td>
<td>



pg\_\{read,write\}\_hdr

</td>
<td>



`include/uapi/linux/pg.h`

</td>
</tr>
<tr>
<td>



APM\_BIOS\_MAGIC

</td>
<td>



0x4101

</td>
<td>



apm\_user

</td>
<td>



`arch/x86/kernel/apm_32.c`

</td>
</tr>
<tr>
<td>



FASYNC\_MAGIC

</td>
<td>



0x4601

</td>
<td>



fasync\_struct

</td>
<td>



`include/linux/fs.h`

</td>
</tr>
<tr>
<td>



SLIP\_MAGIC

</td>
<td>



0x5302

</td>
<td>



slip

</td>
<td>



`drivers/net/slip/slip.h`

</td>
</tr>
<tr>
<td>



BAYCOM\_MAGIC

</td>
<td>



19730510

</td>
<td>



baycom\_state

</td>
<td>



`drivers/net/hamradio/baycom_epp.c`

</td>
</tr>
<tr>
<td>



HDLCDRV\_MAGIC

</td>
<td>



0x5ac6e778

</td>
<td>



hdlcdrv\_state

</td>
<td>



`include/linux/hdlcdrv.h`

</td>
</tr>
<tr>
<td>



KV\_MAGIC

</td>
<td>



0x5f4b565f

</td>
<td>



kernel\_vars\_s

</td>
<td>



`arch/mips/include/asm/sn/klkernvars.h`

</td>
</tr>
<tr>
<td>



CODA\_MAGIC

</td>
<td>



0xC0DAC0DA

</td>
<td>



coda\_file\_info

</td>
<td>



`fs/coda/coda_fs_i.h`

</td>
</tr>
<tr>
<td>



YAM\_MAGIC

</td>
<td>



0xF10A7654

</td>
<td>



yam\_port

</td>
<td>



`drivers/net/hamradio/yam.c`

</td>
</tr>
<tr>
<td>



CCB\_MAGIC

</td>
<td>



0xf2691ad2

</td>
<td>



ccb

</td>
<td>



`drivers/scsi/ncr53c8xx.c`

</td>
</tr>
<tr>
<td>



QUEUE\_MAGIC\_FREE

</td>
<td>



0xf7e1c9a3

</td>
<td>



queue\_entry

</td>
<td>



`drivers/scsi/arm/queue.c`

</td>
</tr>
<tr>
<td>



QUEUE\_MAGIC\_USED

</td>
<td>



0xf7e1cc33

</td>
<td>



queue\_entry

</td>
<td>



`drivers/scsi/arm/queue.c`

</td>
</tr>
<tr>
<td>



NMI\_MAGIC

</td>
<td>



0x48414d4d455201

</td>
<td>



nmi\_s

</td>
<td>



`arch/mips/include/asm/sn/nmi.h`

</td>
</tr>
</tbody>
</table>
