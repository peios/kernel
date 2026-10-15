---
title: "Floppy Driver"
type: reference
description: "A FAQ list may be found in the fdutils package (see below), and also at <https://fdutils.linux.lu/faq.html>."
---

<a id="rst-floppy-driver"></a>

<a id="rst-faq-list"></a>

## FAQ list:

A FAQ list may be found in the fdutils package (see below), and also at &lt;[https://fdutils.linux.lu/faq.html](<https://fdutils.linux.lu/faq.html>)&gt;.

<a id="rst-lilo-configuration-options-thinkpad-users-read-this"></a>

## LILO configuration options (Thinkpad users, read this)

The floppy driver is configured using the 'floppy=' option in lilo. This option can be typed at the boot prompt, or entered in the lilo configuration file.

Example: If your kernel is called linux-2.6.9, type the following line at the lilo boot prompt (if you have a thinkpad):



```text
linux-2.6.9 floppy=thinkpad
```

You may also enter the following line in /etc/lilo.conf, in the description of linux-2.6.9:



```text
append = "floppy=thinkpad"
```

Several floppy related options may be given, example:



```text
linux-2.6.9 floppy=daring floppy=two_fdc
append = "floppy=daring floppy=two_fdc"
```

If you give options both in the lilo config file and on the boot prompt, the option strings of both places are concatenated, the boot prompt options coming last. That's why there are also options to restore the default behavior.

<a id="rst-module-configuration-options"></a>

## Module configuration options

If you use the floppy driver as a module, use the following syntax:



```text
modprobe floppy floppy="<options>"
```

Example:



```text
modprobe floppy floppy="omnibook messages"
```

If you need certain options enabled every time you load the floppy driver, you can put:



```text
options floppy floppy="omnibook messages"
```

in a configuration file in /etc/modprobe.d/.

The floppy driver related options are:

> - **floppy=asus_pci**
>
>   Sets the bit mask to allow only units 0 and 1. (default)
>
> - **floppy=daring**
>
>   Tells the floppy driver that you have a well behaved floppy controller. This allows more efficient and smoother operation, but may fail on certain controllers. This may speed up certain operations.
>
> - **floppy=0,daring**
>
>   Tells the floppy driver that your floppy controller should be used with caution.
>
> - **floppy=one_fdc**
>
>   Tells the floppy driver that you have only one floppy controller. (default)
>
> - **floppy=two_fdc / floppy=&lt;address&gt;,two_fdc**
>
>   Tells the floppy driver that you have two floppy controllers. The second floppy controller is assumed to be at &lt;address&gt;. This option is not needed if the second controller is at address 0x370, and if you use the 'cmos' option.
>
> - **floppy=thinkpad**
>
>   Tells the floppy driver that you have a Thinkpad. Thinkpads use an inverted convention for the disk change line.
>
> - **floppy=0,thinkpad**
>
>   Tells the floppy driver that you don't have a Thinkpad.
>
> - **floppy=omnibook / floppy=nodma**
>
>   Tells the floppy driver not to use Dma for data transfers. This is needed on HP Omnibooks, which don't have a workable DMA channel for the floppy driver. This option is also useful if you frequently get "Unable to allocate DMA memory" messages. Indeed, dma memory needs to be continuous in physical memory, and is thus harder to find, whereas non-dma buffers may be allocated in virtual memory. However, I advise against this if you have an FDC without a FIFO (8272A or 82072). 82072A and later are OK. You also need at least a 486 to use nodma. If you use nodma mode, I suggest you also set the FIFO threshold to 10 or lower, in order to limit the number of data transfer interrupts.
>
>   If you have a FIFO-able FDC, the floppy driver automatically falls back on non DMA mode if no DMA-able memory can be found. If you want to avoid this, explicitly ask for 'yesdma'.
>
> - **floppy=yesdma**
>
>   Tells the floppy driver that a workable DMA channel is available. (default)
>
> - **floppy=nofifo**
>
>   Disables the FIFO entirely. This is needed if you get "Bus master arbitration error" messages from your Ethernet card (or from other devices) while accessing the floppy.
>
> - **floppy=usefifo**
>
>   Enables the FIFO. (default)
>
> - **floppy=&lt;threshold&gt;,fifo_depth**
>
>   Sets the FIFO threshold. This is mostly relevant in DMA mode. If this is higher, the floppy driver tolerates more interrupt latency, but it triggers more interrupts (i.e. it imposes more load on the rest of the system). If this is lower, the interrupt latency should be lower too (faster processor). The benefit of a lower threshold is less interrupts.
>
>   To tune the fifo threshold, switch on over/underrun messages using 'floppycontrol --messages'. Then access a floppy disk. If you get a huge amount of "Over/Underrun - retrying" messages, then the fifo threshold is too low. Try with a higher value, until you only get an occasional Over/Underrun. It is a good idea to compile the floppy driver as a module when doing this tuning. Indeed, it allows to try different fifo values without rebooting the machine for each test. Note that you need to do 'floppycontrol --messages' every time you re-insert the module.
>
>   Usually, tuning the fifo threshold should not be needed, as the default (0xa) is reasonable.
>
> - **floppy=&lt;drive&gt;,&lt;type&gt;,cmos**
>
>   Sets the CMOS type of &lt;drive&gt; to &lt;type&gt;. This is mandatory if you have more than two floppy drives (only two can be described in the physical CMOS), or if your BIOS uses non-standard CMOS types. The CMOS types are:
>
>   >
>   > <table>
>   > <tbody>
>   > <tr>
>   > <td>
>   >
>   >
>   > 0
>   >
>   > </td>
>   > <td>
>   >
>   >
>   > Use the value of the physical CMOS
>   >
>   > </td>
>   > </tr>
>   > <tr>
>   > <td>
>   >
>   >
>   > 1
>   >
>   > </td>
>   > <td>
>   >
>   >
>   > 5 1/4 DD
>   >
>   > </td>
>   > </tr>
>   > <tr>
>   > <td>
>   >
>   >
>   > 2
>   >
>   > </td>
>   > <td>
>   >
>   >
>   > 5 1/4 HD
>   >
>   > </td>
>   > </tr>
>   > <tr>
>   > <td>
>   >
>   >
>   > 3
>   >
>   > </td>
>   > <td>
>   >
>   >
>   > 3 1/2 DD
>   >
>   > </td>
>   > </tr>
>   > <tr>
>   > <td>
>   >
>   >
>   > 4
>   >
>   > </td>
>   > <td>
>   >
>   >
>   > 3 1/2 HD
>   >
>   > </td>
>   > </tr>
>   > <tr>
>   > <td>
>   >
>   >
>   > 5
>   >
>   > </td>
>   > <td>
>   >
>   >
>   > 3 1/2 ED
>   >
>   > </td>
>   > </tr>
>   > <tr>
>   > <td>
>   >
>   >
>   > 6
>   >
>   > </td>
>   > <td>
>   >
>   >
>   > 3 1/2 ED
>   >
>   > </td>
>   > </tr>
>   > <tr>
>   > <td>
>   >
>   >
>   > 16
>   >
>   > </td>
>   > <td>
>   >
>   >
>   > unknown or not installed
>   >
>   > </td>
>   > </tr>
>   > </tbody>
>   > </table>
>
>   (Note: there are two valid types for ED drives. This is because 5 was initially chosen to represent floppy *tapes*, and 6 for ED drives. AMI ignored this, and used 5 for ED drives. That's why the floppy driver handles both.)
>
> - **floppy=unexpected_interrupts**
>
>   Print a warning message when an unexpected interrupt is received. (default)
>
> - **floppy=no_unexpected_interrupts / floppy=L40SX**
>
>   Don't print a message when an unexpected interrupt is received. This is needed on IBM L40SX laptops in certain video modes. (There seems to be an interaction between video and floppy. The unexpected interrupts affect only performance, and can be safely ignored.)
>
> - **floppy=broken_dcl**
>
>   Don't use the disk change line, but assume that the disk was changed whenever the device node is reopened. Needed on some boxes where the disk change line is broken or unsupported. This should be regarded as a stopgap measure, indeed it makes floppy operation less efficient due to unneeded cache flushings, and slightly more unreliable. Please verify your cable, connection and jumper settings if you have any DCL problems. However, some older drives, and also some laptops are known not to have a DCL.
>
> - **floppy=debug**
>
>   Print debugging messages.
>
> - **floppy=messages**
>
>   Print informational messages for some operations (disk change notifications, warnings about over and underruns, and about autodetection).
>
> - **floppy=silent_dcl_clear**
>
>   Uses a less noisy way to clear the disk change line (which doesn't involve seeks). Implied by 'daring' option.
>
> - **floppy=&lt;nr&gt;,irq**
>
>   Sets the floppy IRQ to &lt;nr&gt; instead of 6.
>
> - **floppy=&lt;nr&gt;,dma**
>
>   Sets the floppy DMA channel to &lt;nr&gt; instead of 2.
>
> - **floppy=slow**
>
>   Use PS/2 stepping rate:
>
>
>
>   ```text
>   PS/2 floppies have much slower step rates than regular floppies.
>   It's been recommended that take about 1/4 of the default speed
>   in some more extreme cases.
>   ```

<a id="rst-supporting-utilities-and-additional-documentation"></a>

## Supporting utilities and additional documentation:

Additional parameters of the floppy driver can be configured at runtime. Utilities which do this can be found in the fdutils package. This package also contains a new version of mtools which allows to access high capacity disks (up to 1992K on a high density 3 1/2 disk\!). It also contains additional documentation about the floppy driver.

The latest version can be found at fdutils homepage:

> [https://fdutils.linux.lu](<https://fdutils.linux.lu>)

The fdutils releases can be found at:

> [https://fdutils.linux.lu/download.html](<https://fdutils.linux.lu/download.html>)
>
> [http://www.tux.org/pub/knaff/fdutils/](<http://www.tux.org/pub/knaff/fdutils/>)
>
> [ftp://metalab.unc.edu/pub/Linux/utils/disk-management/](<ftp://metalab.unc.edu/pub/Linux/utils/disk-management/>)

<a id="rst-reporting-problems-about-the-floppy-driver"></a>

## Reporting problems about the floppy driver

If you have a question or a bug report about the floppy driver, mail me at [Alain.Knaff@poboxes.com](<mailto:Alain.Knaff@poboxes.com>) . If you post to Usenet, preferably use comp.os.linux.hardware. As the volume in these groups is rather high, be sure to include the word "floppy" (or "FLOPPY") in the subject line.  If the reported problem happens when mounting floppy disks, be sure to mention also the type of the filesystem in the subject line.

Be sure to read the FAQ before mailing/posting any bug reports\!

Alain

<a id="rst-changelog"></a>

## Changelog

- **10-30-2004 :**

  Cleanup, updating, add reference to module configuration. James Nelson &lt;[james4765@gmail.com](<mailto:james4765@gmail.com>)&gt;

- **6-3-2000 :**

  Original Document
