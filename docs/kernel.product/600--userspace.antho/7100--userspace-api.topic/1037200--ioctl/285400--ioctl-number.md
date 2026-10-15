---
title: "Ioctl Numbers"
type: reference
description: "19 October 1999"
---

<a id="rst-ioctl-numbers"></a>

19 October 1999

Michael Elizabeth Chastain &lt;[mec@shout.net](<mailto:mec@shout.net>)&gt;

If you are adding new ioctl's to the kernel, you should use the \_IO macros defined in &lt;linux/ioctl.h&gt;:

>
> <table>
> <thead>
> <tr>
> <th>
>
>
> macro
>
> </th>
> <th>
>
>
> parameters
>
> </th>
> </tr>
> </thead>
> <tbody>
> <tr>
> <td>
>
>
> \_IO
>
> </td>
> <td>
>
>
> none
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> \_IOW
>
> </td>
> <td>
>
>
> write (read from userspace)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> \_IOR
>
> </td>
> <td>
>
>
> read (write to userspace)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> \_IOWR
>
> </td>
> <td>
>
>
> write and read
>
> </td>
> </tr>
> </tbody>
> </table>

'Write' and 'read' are from the user's point of view, just like the system calls 'write' and 'read'.  For example, a SET_FOO ioctl would be \_IOW, although the kernel would actually read data from user space; a GET_FOO ioctl would be \_IOR, although the kernel would actually write data to user space.

The first argument to the macros is an identifying letter or number from the table below. Because of the large number of drivers, many drivers share a partial letter with other drivers.

If you are writing a driver for a new device and need a letter, pick an unused block with enough room for expansion: 32 to 256 ioctl commands should suffice. You can register the block by patching this file and submitting the patch through [usual patch submission process](<~kernel/development/process/submitting-patches>).

The second argument is a sequence number to distinguish ioctls from each other. The third argument (not applicable to \_IO) is the type of the data going into the kernel or coming out of the kernel (e.g.  'int' or 'struct foo').

> [!NOTE]
>
> Do NOT use sizeof(arg) as the third argument as this results in your ioctl thinking it passes an argument of type size_t.

Some devices use their major number as the identifier; this is OK, as long as it is unique.  Some devices are irregular and don't follow any convention at all.

Following this convention is good because:

1. Keeping the ioctl's globally unique helps error checking: if a program calls an ioctl on the wrong device, it will get an error rather than some unexpected behaviour.

2. The 'strace' build procedure automatically finds ioctl numbers defined with the macros.

3. 'strace' can decode numbers back into useful names when the numbers are unique.

4. People looking for ioctls can grep for them more easily when this convention is used to define the ioctl numbers.

5. When following the convention, the driver code can use generic code to copy the parameters between user and kernel space.

This table lists ioctls visible from userland, excluding ones from drivers/staging/.


<table>
<thead>
<tr>
<th>


Code

</th>
<th>


Seq\# (hex)

</th>
<th>


Include File

</th>
<th>


Comments

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


0x00

</td>
<td>


00-1F

</td>
<td>


linux/fs.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


0x00

</td>
<td>


00-1F

</td>
<td>


scsi/scsi_ioctl.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


0x00

</td>
<td>


00-1F

</td>
<td>


linux/fb.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


0x00

</td>
<td>


00-1F

</td>
<td>


linux/wavefront.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


0x02

</td>
<td>


all

</td>
<td>


linux/fd.h

</td>
<td>




</td>
</tr>
<tr>
<td>


0x03

</td>
<td>


all

</td>
<td>


linux/hdreg.h

</td>
<td>




</td>
</tr>
<tr>
<td>


0x04

</td>
<td>


D2-DC

</td>
<td>


linux/umsdos_fs.h

</td>
<td>


Dead since 2.6.11, but don't reuse these.

</td>
</tr>
<tr>
<td>


0x06

</td>
<td>


all

</td>
<td>


linux/lp.h

</td>
<td>




</td>
</tr>
<tr>
<td>


0x07

</td>
<td>


9F-D0

</td>
<td>


linux/vmw_vmci_defs.h, uapi/linux/vm_sockets.h

</td>
<td>




</td>
</tr>
<tr>
<td>


0x09

</td>
<td>


all

</td>
<td>


linux/raid/md_u.h

</td>
<td>




</td>
</tr>
<tr>
<td>


0x10

</td>
<td>


00-0F

</td>
<td>


drivers/char/s390/vmcp.h

</td>
<td>




</td>
</tr>
<tr>
<td>


0x10

</td>
<td>


10-1F

</td>
<td>


arch/s390/include/uapi/sclp_ctl.h

</td>
<td>




</td>
</tr>
<tr>
<td>


0x10

</td>
<td>


20-2F

</td>
<td>


arch/s390/include/uapi/asm/hypfs.h

</td>
<td>




</td>
</tr>
<tr>
<td>


0x12

</td>
<td>


all

</td>
<td>


linux/fs.h linux/blkpg.h linux/blkzoned.h linux/blk-crypto.h

</td>
<td>


BLK\* ioctls

</td>
</tr>
<tr>
<td>


0x15

</td>
<td>


all

</td>
<td>


linux/fs.h

</td>
<td>


FS_IOC\_\* ioctls

</td>
</tr>
<tr>
<td>


0x1b

</td>
<td>


all

</td>
<td>




</td>
<td>


InfiniBand Subsystem &lt;[http://infiniband.sourceforge.net/](<http://infiniband.sourceforge.net/>)&gt;

</td>
</tr>
<tr>
<td>


0x20

</td>
<td>


all

</td>
<td>


drivers/cdrom/cm206.h

</td>
<td>




</td>
</tr>
<tr>
<td>


0x22

</td>
<td>


all

</td>
<td>


scsi/sg.h

</td>
<td>




</td>
</tr>
<tr>
<td>


0x3E

</td>
<td>


00-0F

</td>
<td>


linux/counter.h

</td>
<td>


&lt;[mailto:linux-iio@vger.kernel.org](<mailto:linux-iio@vger.kernel.org>)&gt;

</td>
</tr>
<tr>
<td>


'\!'

</td>
<td>


00-1F

</td>
<td>


uapi/linux/seccomp.h

</td>
<td>




</td>
</tr>
<tr>
<td>


'\#'

</td>
<td>


00-3F

</td>
<td>




</td>
<td>


IEEE 1394 Subsystem Block for the entire subsystem

</td>
</tr>
<tr>
<td>


'$'

</td>
<td>


00-0F

</td>
<td>


linux/perf_counter.h, linux/perf_event.h

</td>
<td>




</td>
</tr>
<tr>
<td>


'%'

</td>
<td>


00-0F

</td>
<td>


include/uapi/linux/stm.h

</td>
<td>


System Trace Module subsystem &lt;[mailto:alexander.shishkin@linux.intel.com](<mailto:alexander.shishkin@linux.intel.com>)&gt;

</td>
</tr>
<tr>
<td>


'&amp;'

</td>
<td>


00-07

</td>
<td>


drivers/firewire/nosy-user.h

</td>
<td>




</td>
</tr>
<tr>
<td>


'\*'

</td>
<td>


00-1F

</td>
<td>


uapi/linux/user_events.h

</td>
<td>


User Events Subsystem &lt;[mailto:linux-trace-kernel@vger.kernel.org](<mailto:linux-trace-kernel@vger.kernel.org>)&gt;

</td>
</tr>
<tr>
<td>


'1'

</td>
<td>


00-1F

</td>
<td>


linux/timepps.h

</td>
<td>


PPS kit from Ulrich Windl &lt;[ftp://ftp.de.kernel.org/pub/linux/daemons/ntp/PPS/](<ftp://ftp.de.kernel.org/pub/linux/daemons/ntp/PPS/>)&gt;

</td>
</tr>
<tr>
<td>


'2'

</td>
<td>


01-04

</td>
<td>


linux/i2o.h

</td>
<td>




</td>
</tr>
<tr>
<td>


'3'

</td>
<td>


00-0F

</td>
<td>


drivers/s390/char/raw3270.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'3'

</td>
<td>


00-1F

</td>
<td>


linux/suspend_ioctls.h, kernel/power/user.c

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'8'

</td>
<td>


all

</td>
<td>




</td>
<td>


SNP8023 advanced NIC card &lt;[mailto:mcr@solidum.com](<mailto:mcr@solidum.com>)&gt;

</td>
</tr>
<tr>
<td>


';'

</td>
<td>


64-7F

</td>
<td>


linux/vfio.h

</td>
<td>




</td>
</tr>
<tr>
<td>


';'

</td>
<td>


80-FF

</td>
<td>


linux/iommufd.h

</td>
<td>




</td>
</tr>
<tr>
<td>


'='

</td>
<td>


00-3f

</td>
<td>


uapi/linux/ptp_clock.h

</td>
<td>


&lt;[mailto:richardcochran@gmail.com](<mailto:richardcochran@gmail.com>)&gt;

</td>
</tr>
<tr>
<td>


'@'

</td>
<td>


00-0F

</td>
<td>


linux/radeonfb.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'@'

</td>
<td>


00-0F

</td>
<td>


drivers/video/aty/aty128fb.c

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'A'

</td>
<td>


00-1F

</td>
<td>


linux/apm_bios.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'A'

</td>
<td>


00-0F

</td>
<td>


linux/agpgart.h, drivers/char/agp/compat_ioctl.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'A'

</td>
<td>


00-7F

</td>
<td>


sound/asound.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'B'

</td>
<td>


00-1F

</td>
<td>


linux/cciss_ioctl.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'B'

</td>
<td>


00-0F

</td>
<td>


include/linux/pmu.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'B'

</td>
<td>


C0-FF

</td>
<td>


advanced bbus

</td>
<td>


&lt;[mailto:maassen@uni-freiburg.de](<mailto:maassen@uni-freiburg.de>)&gt;

</td>
</tr>
<tr>
<td>


'B'

</td>
<td>


00-0F

</td>
<td>


xen/xenbus_dev.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'C'

</td>
<td>


all

</td>
<td>


linux/soundcard.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'C'

</td>
<td>


01-2F

</td>
<td>


linux/capi.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'C'

</td>
<td>


F0-FF

</td>
<td>


drivers/net/wan/cosa.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'D'

</td>
<td>


all

</td>
<td>


arch/s390/include/asm/dasd.h

</td>
<td>




</td>
</tr>
<tr>
<td>


'D'

</td>
<td>


40-5F

</td>
<td>


drivers/scsi/dpt/dtpi_ioctl.h

</td>
<td>


Dead since 2022

</td>
</tr>
<tr>
<td>


'D'

</td>
<td>


05

</td>
<td>


drivers/scsi/pmcraid.h

</td>
<td>




</td>
</tr>
<tr>
<td>


'E'

</td>
<td>


all

</td>
<td>


linux/input.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'E'

</td>
<td>


00-0F

</td>
<td>


xen/evtchn.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'F'

</td>
<td>


all

</td>
<td>


linux/fb.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'F'

</td>
<td>


01-02

</td>
<td>


drivers/scsi/pmcraid.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'F'

</td>
<td>


20

</td>
<td>


drivers/video/fsl-diu-fb.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'F'

</td>
<td>


20

</td>
<td>


linux/ivtvfb.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'F'

</td>
<td>


20

</td>
<td>


linux/matroxfb.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'F'

</td>
<td>


20

</td>
<td>


drivers/video/aty/atyfb_base.c

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'F'

</td>
<td>


00-0F

</td>
<td>


video/da8xx-fb.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'F'

</td>
<td>


80-8F

</td>
<td>


linux/arcfb.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'F'

</td>
<td>


DD

</td>
<td>


video/sstfb.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'G'

</td>
<td>


00-3F

</td>
<td>


drivers/misc/sgi-gru/grulib.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'G'

</td>
<td>


00-0F

</td>
<td>


xen/gntalloc.h, xen/gntdev.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'H'

</td>
<td>


00-7F

</td>
<td>


linux/hiddev.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'H'

</td>
<td>


00-0F

</td>
<td>


linux/hidraw.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'H'

</td>
<td>


01

</td>
<td>


linux/mei.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'H'

</td>
<td>


02

</td>
<td>


linux/mei.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'H'

</td>
<td>


03

</td>
<td>


linux/mei.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'H'

</td>
<td>


00-0F

</td>
<td>


sound/asound.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'H'

</td>
<td>


20-40

</td>
<td>


sound/asound_fm.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'H'

</td>
<td>


80-8F

</td>
<td>


sound/sfnt_info.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'H'

</td>
<td>


10-8F

</td>
<td>


sound/emu10k1.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'H'

</td>
<td>


10-1F

</td>
<td>


sound/sb16_csp.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'H'

</td>
<td>


10-1F

</td>
<td>


sound/hda_hwdep.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'H'

</td>
<td>


40-4F

</td>
<td>


sound/hdspm.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'H'

</td>
<td>


40-4F

</td>
<td>


sound/hdsp.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'H'

</td>
<td>


90

</td>
<td>


sound/usb/usx2y/usb_stream.h

</td>
<td>




</td>
</tr>
<tr>
<td>


'H'

</td>
<td>


00-0F

</td>
<td>


uapi/misc/habanalabs.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'H'

</td>
<td>


A0

</td>
<td>


uapi/linux/usb/cdc-wdm.h

</td>
<td>




</td>
</tr>
<tr>
<td>


'H'

</td>
<td>


C0-F0

</td>
<td>


net/bluetooth/hci.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'H'

</td>
<td>


C0-DF

</td>
<td>


net/bluetooth/hidp/hidp.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'H'

</td>
<td>


C0-DF

</td>
<td>


net/bluetooth/cmtp/cmtp.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'H'

</td>
<td>


C0-DF

</td>
<td>


net/bluetooth/bnep/bnep.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'H'

</td>
<td>


F1

</td>
<td>


linux/hid-roccat.h

</td>
<td>


&lt;[mailto:erazor_de@users.sourceforge.net](<mailto:erazor_de@users.sourceforge.net>)&gt;

</td>
</tr>
<tr>
<td>


'H'

</td>
<td>


F8-FA

</td>
<td>


sound/firewire.h

</td>
<td>




</td>
</tr>
<tr>
<td>


'I'

</td>
<td>


all

</td>
<td>


linux/isdn.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'I'

</td>
<td>


00-0F

</td>
<td>


drivers/isdn/divert/isdn_divert.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'I'

</td>
<td>


40-4F

</td>
<td>


linux/mISDNif.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'K'

</td>
<td>


all

</td>
<td>


linux/kd.h

</td>
<td>




</td>
</tr>
<tr>
<td>


'L'

</td>
<td>


00-1F

</td>
<td>


linux/loop.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'L'

</td>
<td>


10-1F

</td>
<td>


drivers/scsi/mpt3sas/mpt3sas_ctl.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'L'

</td>
<td>


E0-FF

</td>
<td>


linux/ppdd.h

</td>
<td>


encrypted disk device driver &lt;[http://linux01.gwdg.de/\~alatham/ppdd.html](<http://linux01.gwdg.de/~alatham/ppdd.html>)&gt;

</td>
</tr>
<tr>
<td>


'M'

</td>
<td>


all

</td>
<td>


linux/soundcard.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'M'

</td>
<td>


01-16 and

</td>
<td>


mtd/mtd-abi.h drivers/mtd/mtdchar.c

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'M'

</td>
<td>


01-03

</td>
<td>


drivers/scsi/megaraid/megaraid_sas.h

</td>
<td>




</td>
</tr>
<tr>
<td>


'M'

</td>
<td>


00-0F

</td>
<td>


drivers/video/fsl-diu-fb.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'N'

</td>
<td>


00-1F

</td>
<td>


drivers/usb/scanner.h

</td>
<td>




</td>
</tr>
<tr>
<td>


'N'

</td>
<td>


40-7F

</td>
<td>


drivers/block/nvme.c

</td>
<td>




</td>
</tr>
<tr>
<td>


'N'

</td>
<td>


80-8F

</td>
<td>


uapi/linux/ntsync.h

</td>
<td>


NT synchronization primitives &lt;[mailto:wine-devel@winehq.org](<mailto:wine-devel@winehq.org>)&gt;

</td>
</tr>
<tr>
<td>


'O'

</td>
<td>


00-06

</td>
<td>


mtd/ubi-user.h

</td>
<td>


UBI

</td>
</tr>
<tr>
<td>


'P'

</td>
<td>


all

</td>
<td>


linux/soundcard.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'P'

</td>
<td>


60-6F

</td>
<td>


sound/sscape_ioctl.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'P'

</td>
<td>


00-0F

</td>
<td>


drivers/usb/class/usblp.c

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'P'

</td>
<td>


01-09

</td>
<td>


drivers/misc/pci_endpoint_test.c

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'P'

</td>
<td>


00-0F

</td>
<td>


xen/privcmd.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'P'

</td>
<td>


00-05

</td>
<td>


linux/tps6594_pfsm.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'Q'

</td>
<td>


all

</td>
<td>


linux/soundcard.h

</td>
<td>




</td>
</tr>
<tr>
<td>


'R'

</td>
<td>


00-1F

</td>
<td>


linux/random.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'R'

</td>
<td>


01

</td>
<td>


linux/rfkill.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'R'

</td>
<td>


20-2F

</td>
<td>


linux/trace_mmap.h

</td>
<td>




</td>
</tr>
<tr>
<td>


'R'

</td>
<td>


C0-DF

</td>
<td>


net/bluetooth/rfcomm.h

</td>
<td>




</td>
</tr>
<tr>
<td>


'R'

</td>
<td>


E0

</td>
<td>


uapi/linux/fsl_mc.h

</td>
<td>




</td>
</tr>
<tr>
<td>


'S'

</td>
<td>


all

</td>
<td>


linux/cdrom.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'S'

</td>
<td>


80-81

</td>
<td>


scsi/scsi_ioctl.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'S'

</td>
<td>


82-FF

</td>
<td>


scsi/scsi.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'S'

</td>
<td>


00-7F

</td>
<td>


sound/asequencer.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'T'

</td>
<td>


all

</td>
<td>


linux/soundcard.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'T'

</td>
<td>


00-AF

</td>
<td>


sound/asound.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'T'

</td>
<td>


all

</td>
<td>


arch/x86/include/asm/ioctls.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'T'

</td>
<td>


C0-DF

</td>
<td>


linux/if_tun.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'U'

</td>
<td>


all

</td>
<td>


sound/asound.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'U'

</td>
<td>


00-CF

</td>
<td>


linux/uinput.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'U'

</td>
<td>


00-EF

</td>
<td>


linux/usbdevice_fs.h

</td>
<td>




</td>
</tr>
<tr>
<td>


'U'

</td>
<td>


C0-CF

</td>
<td>


drivers/bluetooth/hci_uart.h

</td>
<td>




</td>
</tr>
<tr>
<td>


'V'

</td>
<td>


all

</td>
<td>


linux/vt.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'V'

</td>
<td>


all

</td>
<td>


linux/videodev2.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'V'

</td>
<td>


C0

</td>
<td>


linux/ivtvfb.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'V'

</td>
<td>


C0

</td>
<td>


linux/ivtv.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'V'

</td>
<td>


C0

</td>
<td>


media/si4713.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'W'

</td>
<td>


00-1F

</td>
<td>


linux/watchdog.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'W'

</td>
<td>


00-1F

</td>
<td>


linux/wanrouter.h

</td>
<td>


conflict\! (pre 3.9)

</td>
</tr>
<tr>
<td>


'W'

</td>
<td>


00-3F

</td>
<td>


sound/asound.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'W'

</td>
<td>


40-5F

</td>
<td>


drivers/pci/switch/switchtec.c

</td>
<td>




</td>
</tr>
<tr>
<td>


'W'

</td>
<td>


60-61

</td>
<td>


linux/watch_queue.h

</td>
<td>




</td>
</tr>
<tr>
<td>


'X'

</td>
<td>


all

</td>
<td>


fs/xfs/xfs_fs.h, fs/xfs/linux-2.6/xfs_ioctl32.h, include/linux/falloc.h, linux/fs.h,

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'X'

</td>
<td>


all

</td>
<td>


fs/ocfs2/ocfs_fs.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'Z'

</td>
<td>


14-15

</td>
<td>


drivers/message/fusion/mptctl.h

</td>
<td>




</td>
</tr>
<tr>
<td>


'\['

</td>
<td>


00-3F

</td>
<td>


linux/usb/tmc.h

</td>
<td>


USB Test and Measurement Devices &lt;[mailto:gregkh@linuxfoundation.org](<mailto:gregkh@linuxfoundation.org>)&gt;

</td>
</tr>
<tr>
<td>


'a'

</td>
<td>


all

</td>
<td>


linux/atm\*.h, linux/sonet.h

</td>
<td>


ATM on linux &lt;[http://lrcwww.epfl.ch/](<http://lrcwww.epfl.ch/>)&gt;

</td>
</tr>
<tr>
<td>


'a'

</td>
<td>


00-0F

</td>
<td>


drivers/crypto/qat/qat_common/adf_cfg_common.h

</td>
<td>


conflict\! qat driver

</td>
</tr>
<tr>
<td>


'b'

</td>
<td>


00-FF

</td>
<td>




</td>
<td>


conflict\! bit3 vme host bridge &lt;[mailto:natalia@nikhefk.nikhef.nl](<mailto:natalia@nikhefk.nikhef.nl>)&gt;

</td>
</tr>
<tr>
<td>


'b'

</td>
<td>


00-0F

</td>
<td>


linux/dma-buf.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'c'

</td>
<td>


00-7F

</td>
<td>


linux/comstats.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'c'

</td>
<td>


00-7F

</td>
<td>


linux/coda.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'c'

</td>
<td>


00-1F

</td>
<td>


linux/chio.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'c'

</td>
<td>


80-9F

</td>
<td>


arch/s390/include/asm/chsc.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'c'

</td>
<td>


A0-AF

</td>
<td>


arch/x86/include/asm/msr.h conflict\!

</td>
<td>




</td>
</tr>
<tr>
<td>


'd'

</td>
<td>


00-FF

</td>
<td>


linux/char/drm/drm.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'd'

</td>
<td>


02-40

</td>
<td>


pcmcia/ds.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'd'

</td>
<td>


F0-FF

</td>
<td>


linux/digi1.h

</td>
<td>




</td>
</tr>
<tr>
<td>


'e'

</td>
<td>


all

</td>
<td>


linux/digi1.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'f'

</td>
<td>


00-1F

</td>
<td>


linux/ext2_fs.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'f'

</td>
<td>


00-1F

</td>
<td>


linux/ext3_fs.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'f'

</td>
<td>


00-0F

</td>
<td>


fs/jfs/jfs_dinode.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'f'

</td>
<td>


00-0F

</td>
<td>


fs/ext4/ext4.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'f'

</td>
<td>


00-0F

</td>
<td>


linux/fs.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'f'

</td>
<td>


00-0F

</td>
<td>


fs/ocfs2/ocfs2_fs.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'f'

</td>
<td>


13-27

</td>
<td>


linux/fscrypt.h

</td>
<td>




</td>
</tr>
<tr>
<td>


'f'

</td>
<td>


81-8F

</td>
<td>


linux/fsverity.h

</td>
<td>




</td>
</tr>
<tr>
<td>


'g'

</td>
<td>


00-0F

</td>
<td>


linux/usb/gadgetfs.h

</td>
<td>




</td>
</tr>
<tr>
<td>


'g'

</td>
<td>


20-2F

</td>
<td>


linux/usb/g_printer.h

</td>
<td>




</td>
</tr>
<tr>
<td>


'h'

</td>
<td>


00-7F

</td>
<td>




</td>
<td>


conflict\! Charon filesystem &lt;[mailto:zapman@interlan.net](<mailto:zapman@interlan.net>)&gt;

</td>
</tr>
<tr>
<td>


'h'

</td>
<td>


00-1F

</td>
<td>


linux/hpet.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'h'

</td>
<td>


80-8F

</td>
<td>


fs/hfsplus/ioctl.c

</td>
<td>




</td>
</tr>
<tr>
<td>


'i'

</td>
<td>


00-3F

</td>
<td>


linux/i2o-dev.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'i'

</td>
<td>


0B-1F

</td>
<td>


linux/ipmi.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'i'

</td>
<td>


80-8F

</td>
<td>


linux/i8k.h

</td>
<td>




</td>
</tr>
<tr>
<td>


'i'

</td>
<td>


90-9F

</td>
<td>


`linux/iio/*.h`

</td>
<td>


IIO

</td>
</tr>
<tr>
<td>


'j'

</td>
<td>


00-3F

</td>
<td>


linux/joystick.h

</td>
<td>




</td>
</tr>
<tr>
<td>


'k'

</td>
<td>


00-0F

</td>
<td>


linux/spi/spidev.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'k'

</td>
<td>


00-05

</td>
<td>


video/kyro.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'k'

</td>
<td>


10-17

</td>
<td>


linux/hsi/hsi_char.h

</td>
<td>


HSI character device

</td>
</tr>
<tr>
<td>


'l'

</td>
<td>


00-3F

</td>
<td>


linux/tcfs_fs.h

</td>
<td>


transparent cryptographic file system &lt;[http://web.archive.org/web/%2A/http://mikonos.dia.unisa.it/tcfs](<http://web.archive.org/web/%2A/http://mikonos.dia.unisa.it/tcfs>)&gt;

</td>
</tr>
<tr>
<td>


'l'

</td>
<td>


40-7F

</td>
<td>


linux/udf_fs_i.h

</td>
<td>


in development: &lt;[https://github.com/pali/udftools](<https://github.com/pali/udftools>)&gt;

</td>
</tr>
<tr>
<td>


'm'

</td>
<td>


00-09

</td>
<td>


linux/mmtimer.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'm'

</td>
<td>


all

</td>
<td>


linux/mtio.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'm'

</td>
<td>


all

</td>
<td>


linux/soundcard.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'm'

</td>
<td>


all

</td>
<td>


linux/synclink.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'm'

</td>
<td>


00-19

</td>
<td>


drivers/message/fusion/mptctl.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'm'

</td>
<td>


00

</td>
<td>


drivers/scsi/megaraid/megaraid_ioctl.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'n'

</td>
<td>


00-7F

</td>
<td>


linux/ncp_fs.h and fs/ncpfs/ioctl.c

</td>
<td>




</td>
</tr>
<tr>
<td>


'n'

</td>
<td>


80-8F

</td>
<td>


uapi/linux/nilfs2_api.h

</td>
<td>


NILFS2

</td>
</tr>
<tr>
<td>


'n'

</td>
<td>


E0-FF

</td>
<td>


linux/matroxfb.h

</td>
<td>


matroxfb

</td>
</tr>
<tr>
<td>


'o'

</td>
<td>


00-1F

</td>
<td>


fs/ocfs2/ocfs2_fs.h

</td>
<td>


OCFS2

</td>
</tr>
<tr>
<td>


'o'

</td>
<td>


00-03

</td>
<td>


mtd/ubi-user.h

</td>
<td>


conflict\! (OCFS2 and UBI overlaps)

</td>
</tr>
<tr>
<td>


'o'

</td>
<td>


40-41

</td>
<td>


mtd/ubi-user.h

</td>
<td>


UBI

</td>
</tr>
<tr>
<td>


'o'

</td>
<td>


01-A1

</td>
<td>


`linux/dvb/*.h`

</td>
<td>


DVB

</td>
</tr>
<tr>
<td>


'p'

</td>
<td>


00-0F

</td>
<td>


linux/phantom.h

</td>
<td>


conflict\! (OpenHaptics needs this)

</td>
</tr>
<tr>
<td>


'p'

</td>
<td>


00-1F

</td>
<td>


linux/rtc.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'p'

</td>
<td>


40-7F

</td>
<td>


linux/nvram.h

</td>
<td>




</td>
</tr>
<tr>
<td>


'p'

</td>
<td>


80-9F

</td>
<td>


linux/ppdev.h

</td>
<td>


user-space parport &lt;[mailto:tim@cyberelk.net](<mailto:tim@cyberelk.net>)&gt;

</td>
</tr>
<tr>
<td>


'p'

</td>
<td>


A1-A5

</td>
<td>


linux/pps.h

</td>
<td>


LinuxPPS

</td>
</tr>
<tr>
<td>


'p'

</td>
<td>


B1-B3

</td>
<td>


linux/pps_gen.h

</td>
<td>


LinuxPPS &lt;[mailto:giometti@linux.it](<mailto:giometti@linux.it>)&gt;

</td>
</tr>
<tr>
<td>


'q'

</td>
<td>


00-1F

</td>
<td>


linux/serio.h

</td>
<td>




</td>
</tr>
<tr>
<td>


'q'

</td>
<td>


80-FF

</td>
<td>


linux/telephony.h linux/ixjuser.h

</td>
<td>


Internet PhoneJACK, Internet LineJACK &lt;[http://web.archive.org/web/%2A/http://www.quicknet.net](<http://web.archive.org/web/%2A/http://www.quicknet.net>)&gt;

</td>
</tr>
<tr>
<td>


'r'

</td>
<td>


00-1F

</td>
<td>


linux/msdos_fs.h and fs/fat/dir.c

</td>
<td>




</td>
</tr>
<tr>
<td>


's'

</td>
<td>


all

</td>
<td>


linux/cdk.h

</td>
<td>




</td>
</tr>
<tr>
<td>


't'

</td>
<td>


00-7F

</td>
<td>


linux/ppp-ioctl.h

</td>
<td>




</td>
</tr>
<tr>
<td>


't'

</td>
<td>


80-8F

</td>
<td>


linux/isdn_ppp.h

</td>
<td>




</td>
</tr>
<tr>
<td>


't'

</td>
<td>


90-91

</td>
<td>


linux/toshiba.h

</td>
<td>


toshiba and toshiba_acpi SMM

</td>
</tr>
<tr>
<td>


'u'

</td>
<td>


00-1F

</td>
<td>


linux/smb_fs.h

</td>
<td>


gone

</td>
</tr>
<tr>
<td>


'u'

</td>
<td>


00-2F

</td>
<td>


linux/ublk_cmd.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'u'

</td>
<td>


20-3F

</td>
<td>


linux/uvcvideo.h

</td>
<td>


USB video class host driver

</td>
</tr>
<tr>
<td>


'u'

</td>
<td>


40-4f

</td>
<td>


linux/udmabuf.h

</td>
<td>


userspace dma-buf misc device

</td>
</tr>
<tr>
<td>


'v'

</td>
<td>


00-1F

</td>
<td>


linux/ext2_fs.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'v'

</td>
<td>


00-1F

</td>
<td>


linux/fs.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'v'

</td>
<td>


00-0F

</td>
<td>


linux/sonypi.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'v'

</td>
<td>


00-0F

</td>
<td>


media/v4l2-subdev.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'v'

</td>
<td>


20-27

</td>
<td>


arch/powerpc/include/uapi/asm/vas-api.h

</td>
<td>


VAS API

</td>
</tr>
<tr>
<td>


'v'

</td>
<td>


C0-FF

</td>
<td>


linux/meye.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'w'

</td>
<td>


all

</td>
<td>




</td>
<td>


CERN SCI driver

</td>
</tr>
<tr>
<td>


'y'

</td>
<td>


00-1F

</td>
<td>




</td>
<td>


packet based user level communications &lt;[mailto:zapman@interlan.net](<mailto:zapman@interlan.net>)&gt;

</td>
</tr>
<tr>
<td>


'z'

</td>
<td>


00-3F

</td>
<td>




</td>
<td>


CAN bus card conflict\! &lt;[mailto:hdstich@connectu.ulm.circular.de](<mailto:hdstich@connectu.ulm.circular.de>)&gt;

</td>
</tr>
<tr>
<td>


'z'

</td>
<td>


40-7F

</td>
<td>




</td>
<td>


CAN bus card conflict\! &lt;[mailto:oe@port.de](<mailto:oe@port.de>)&gt;

</td>
</tr>
<tr>
<td>


'z'

</td>
<td>


10-4F

</td>
<td>


drivers/s390/crypto/zcrypt_api.h

</td>
<td>


conflict\!

</td>
</tr>
<tr>
<td>


'\|'

</td>
<td>


00-7F

</td>
<td>


linux/media.h

</td>
<td>




</td>
</tr>
<tr>
<td>


'\|'

</td>
<td>


80-9F

</td>
<td>


samples/

</td>
<td>


Any sample and example drivers

</td>
</tr>
<tr>
<td>


0x80

</td>
<td>


00-1F

</td>
<td>


linux/fb.h

</td>
<td>




</td>
</tr>
<tr>
<td>


0x81

</td>
<td>


00-1F

</td>
<td>


linux/vduse.h

</td>
<td>




</td>
</tr>
<tr>
<td>


0x89

</td>
<td>


00-06

</td>
<td>


arch/x86/include/asm/sockios.h

</td>
<td>




</td>
</tr>
<tr>
<td>


0x89

</td>
<td>


0B-DF

</td>
<td>


linux/sockios.h

</td>
<td>




</td>
</tr>
<tr>
<td>


0x89

</td>
<td>


E0-EF

</td>
<td>


linux/sockios.h

</td>
<td>


SIOCPROTOPRIVATE range

</td>
</tr>
<tr>
<td>


0x89

</td>
<td>


F0-FF

</td>
<td>


linux/sockios.h

</td>
<td>


SIOCDEVPRIVATE range

</td>
</tr>
<tr>
<td>


0x8A

</td>
<td>


00-1F

</td>
<td>


linux/eventpoll.h

</td>
<td>




</td>
</tr>
<tr>
<td>


0x8B

</td>
<td>


all

</td>
<td>


linux/wireless.h

</td>
<td>




</td>
</tr>
<tr>
<td>


0x8C

</td>
<td>


00-3F

</td>
<td>




</td>
<td>


WiNRADiO driver &lt;[http://www.winradio.com.au/](<http://www.winradio.com.au/>)&gt;

</td>
</tr>
<tr>
<td>


0x90

</td>
<td>


00

</td>
<td>


drivers/cdrom/sbpcd.h

</td>
<td>




</td>
</tr>
<tr>
<td>


0x92

</td>
<td>


00-0F

</td>
<td>


drivers/usb/mon/mon_bin.c

</td>
<td>




</td>
</tr>
<tr>
<td>


0x93

</td>
<td>


60-7F

</td>
<td>


linux/auto_fs.h

</td>
<td>




</td>
</tr>
<tr>
<td>


0x94

</td>
<td>


all

</td>
<td>


fs/btrfs/ioctl.h and linux/fs.h

</td>
<td>


Btrfs filesystem some lifted to vfs/generic

</td>
</tr>
<tr>
<td>


0x97

</td>
<td>


00-7F

</td>
<td>


fs/ceph/ioctl.h

</td>
<td>


Ceph file system

</td>
</tr>
<tr>
<td>


0x99

</td>
<td>


00-0F

</td>
<td>




</td>
<td>


537-Addinboard driver &lt;[mailto:buk@buks.ipn.de](<mailto:buk@buks.ipn.de>)&gt;

</td>
</tr>
<tr>
<td>


0x9A

</td>
<td>


00-0F

</td>
<td>


include/uapi/fwctl/fwctl.h

</td>
<td>




</td>
</tr>
<tr>
<td>


0xA0

</td>
<td>


all

</td>
<td>


linux/sdp/sdp.h

</td>
<td>


Industrial Device Project &lt;[mailto:kenji@bitgate.com](<mailto:kenji@bitgate.com>)&gt;

</td>
</tr>
<tr>
<td>


0xA1

</td>
<td>


0

</td>
<td>


linux/vtpm_proxy.h

</td>
<td>


TPM Emulator Proxy Driver

</td>
</tr>
<tr>
<td>


0xA2

</td>
<td>


all

</td>
<td>


uapi/linux/acrn.h

</td>
<td>


ACRN hypervisor

</td>
</tr>
<tr>
<td>


0xA3

</td>
<td>


80-8F

</td>
<td>




</td>
<td>


Port ACL  in development: &lt;[mailto:tlewis@mindspring.com](<mailto:tlewis@mindspring.com>)&gt;

</td>
</tr>
<tr>
<td>


0xA3

</td>
<td>


90-9F

</td>
<td>


linux/dtlk.h

</td>
<td>




</td>
</tr>
<tr>
<td>


0xA4

</td>
<td>


00-1F

</td>
<td>


uapi/linux/tee.h

</td>
<td>


Generic TEE subsystem

</td>
</tr>
<tr>
<td>


0xA4

</td>
<td>


00-1F

</td>
<td>


uapi/asm/sgx.h

</td>
<td>


&lt;[mailto:linux-sgx@vger.kernel.org](<mailto:linux-sgx@vger.kernel.org>)&gt;

</td>
</tr>
<tr>
<td>


0xA5

</td>
<td>


01-05

</td>
<td>


linux/surface_aggregator/cdev.h

</td>
<td>


Microsoft Surface Platform System Aggregator &lt;[mailto:luzmaximilian@gmail.com](<mailto:luzmaximilian@gmail.com>)&gt;

</td>
</tr>
<tr>
<td>


0xA5

</td>
<td>


20-2F

</td>
<td>


linux/surface_aggregator/dtx.h

</td>
<td>


Microsoft Surface DTX driver &lt;[mailto:luzmaximilian@gmail.com](<mailto:luzmaximilian@gmail.com>)&gt;

</td>
</tr>
<tr>
<td>


0xAA

</td>
<td>


00-3F

</td>
<td>


linux/uapi/linux/userfaultfd.h

</td>
<td>




</td>
</tr>
<tr>
<td>


0xAB

</td>
<td>


00-1F

</td>
<td>


linux/nbd.h

</td>
<td>




</td>
</tr>
<tr>
<td>


0xAC

</td>
<td>


00-1F

</td>
<td>


linux/raw.h

</td>
<td>




</td>
</tr>
<tr>
<td>


0xAD

</td>
<td>


00

</td>
<td>




</td>
<td>


Netfilter device in development: &lt;[mailto:rusty@rustcorp.com.au](<mailto:rusty@rustcorp.com.au>)&gt;

</td>
</tr>
<tr>
<td>


0xAE

</td>
<td>


00-1F

</td>
<td>


linux/kvm.h

</td>
<td>


Kernel-based Virtual Machine &lt;[mailto:kvm@vger.kernel.org](<mailto:kvm@vger.kernel.org>)&gt;

</td>
</tr>
<tr>
<td>


0xAE

</td>
<td>


40-FF

</td>
<td>


linux/kvm.h

</td>
<td>


Kernel-based Virtual Machine &lt;[mailto:kvm@vger.kernel.org](<mailto:kvm@vger.kernel.org>)&gt;

</td>
</tr>
<tr>
<td>


0xAE

</td>
<td>


20-3F

</td>
<td>


linux/nitro_enclaves.h

</td>
<td>


Nitro Enclaves

</td>
</tr>
<tr>
<td>


0xAF

</td>
<td>


00-1F

</td>
<td>


linux/fsl_hypervisor.h

</td>
<td>


Freescale hypervisor

</td>
</tr>
<tr>
<td>


0xB0

</td>
<td>


all

</td>
<td>




</td>
<td>


RATIO devices in development: &lt;[mailto:vgo@ratio.de](<mailto:vgo@ratio.de>)&gt;

</td>
</tr>
<tr>
<td>


0xB1

</td>
<td>


00-1F

</td>
<td>




</td>
<td>


PPPoX &lt;[mailto:mostrows@styx.uwaterloo.ca](<mailto:mostrows@styx.uwaterloo.ca>)&gt;

</td>
</tr>
<tr>
<td>


0xB2

</td>
<td>


00

</td>
<td>


arch/powerpc/include/uapi/asm/papr-vpd.h

</td>
<td>


powerpc/pseries VPD API &lt;[mailto:linuxppc-dev@lists.ozlabs.org](<mailto:linuxppc-dev@lists.ozlabs.org>)&gt;

</td>
</tr>
<tr>
<td>


0xB2

</td>
<td>


01-02

</td>
<td>


arch/powerpc/include/uapi/asm/papr-sysparm.h

</td>
<td>


powerpc/pseries system parameter API &lt;[mailto:linuxppc-dev@lists.ozlabs.org](<mailto:linuxppc-dev@lists.ozlabs.org>)&gt;

</td>
</tr>
<tr>
<td>


0xB2

</td>
<td>


03-05

</td>
<td>


arch/powerpc/include/uapi/asm/papr-indices.h

</td>
<td>


powerpc/pseries indices API &lt;[mailto:linuxppc-dev@lists.ozlabs.org](<mailto:linuxppc-dev@lists.ozlabs.org>)&gt;

</td>
</tr>
<tr>
<td>


0xB2

</td>
<td>


06-07

</td>
<td>


arch/powerpc/include/uapi/asm/papr-platform-dump.h

</td>
<td>


powerpc/pseries Platform Dump API &lt;[mailto:linuxppc-dev@lists.ozlabs.org](<mailto:linuxppc-dev@lists.ozlabs.org>)&gt;

</td>
</tr>
<tr>
<td>


0xB2

</td>
<td>


08

</td>
<td>


arch/powerpc/include/uapi/asm/papr-physical-attestation.h

</td>
<td>


powerpc/pseries Physical Attestation API &lt;[mailto:linuxppc-dev@lists.ozlabs.org](<mailto:linuxppc-dev@lists.ozlabs.org>)&gt;

</td>
</tr>
<tr>
<td>


0xB2

</td>
<td>


09

</td>
<td>


arch/powerpc/include/uapi/asm/papr-hvpipe.h

</td>
<td>


powerpc/pseries HVPIPE API &lt;[mailto:linuxppc-dev@lists.ozlabs.org](<mailto:linuxppc-dev@lists.ozlabs.org>)&gt;

</td>
</tr>
<tr>
<td>


0xB3

</td>
<td>


00

</td>
<td>


linux/mmc/ioctl.h

</td>
<td>




</td>
</tr>
<tr>
<td>


0xB4

</td>
<td>


00-0F

</td>
<td>


linux/gpio.h

</td>
<td>


&lt;[mailto:linux-gpio@vger.kernel.org](<mailto:linux-gpio@vger.kernel.org>)&gt;

</td>
</tr>
<tr>
<td>


0xB5

</td>
<td>


00-0F

</td>
<td>


uapi/linux/rpmsg.h

</td>
<td>


&lt;[mailto:linux-remoteproc@vger.kernel.org](<mailto:linux-remoteproc@vger.kernel.org>)&gt;

</td>
</tr>
<tr>
<td>


0xB6

</td>
<td>


all

</td>
<td>


linux/fpga-dfl.h

</td>
<td>




</td>
</tr>
<tr>
<td>


0xB7

</td>
<td>


all

</td>
<td>


uapi/linux/remoteproc_cdev.h

</td>
<td>


&lt;[mailto:linux-remoteproc@vger.kernel.org](<mailto:linux-remoteproc@vger.kernel.org>)&gt;

</td>
</tr>
<tr>
<td>


0xB7

</td>
<td>


all

</td>
<td>


uapi/linux/nsfs.h

</td>
<td>


&lt;[mailto:Andrei](<mailto:Andrei>) Vagin &lt;[avagin@openvz.org](<mailto:avagin@openvz.org>)&gt;&gt;

</td>
</tr>
<tr>
<td>


0xB8

</td>
<td>


01-02

</td>
<td>


uapi/misc/mrvl_cn10k_dpi.h

</td>
<td>


Marvell CN10K DPI driver

</td>
</tr>
<tr>
<td>


0xB8

</td>
<td>


all

</td>
<td>


uapi/linux/mshv.h

</td>
<td>


Microsoft Hyper-V /dev/mshv driver &lt;[mailto:linux-hyperv@vger.kernel.org](<mailto:linux-hyperv@vger.kernel.org>)&gt;

</td>
</tr>
<tr>
<td>


0xBA

</td>
<td>


00-0F

</td>
<td>


uapi/linux/liveupdate.h

</td>
<td>


Pasha Tatashin &lt;[mailto:pasha.tatashin@soleen.com](<mailto:pasha.tatashin@soleen.com>)&gt;

</td>
</tr>
<tr>
<td>


0xC0

</td>
<td>


00-0F

</td>
<td>


linux/usb/iowarrior.h

</td>
<td>




</td>
</tr>
<tr>
<td>


0xCA

</td>
<td>


00-0F

</td>
<td>


uapi/misc/cxl.h

</td>
<td>


Dead since 6.15

</td>
</tr>
<tr>
<td>


0xCA

</td>
<td>


10-2F

</td>
<td>


uapi/misc/ocxl.h

</td>
<td>




</td>
</tr>
<tr>
<td>


0xCA

</td>
<td>


80-BF

</td>
<td>


uapi/scsi/cxlflash_ioctl.h

</td>
<td>


Dead since 6.15

</td>
</tr>
<tr>
<td>


0xCB

</td>
<td>


00-1F

</td>
<td>




</td>
<td>


CBM serial IEC bus in development: &lt;[mailto:michael.klein@puffin.lb.shuttle.de](<mailto:michael.klein@puffin.lb.shuttle.de>)&gt;

</td>
</tr>
<tr>
<td>


0xCC

</td>
<td>


00-0F

</td>
<td>


drivers/misc/ibmvmc.h

</td>
<td>


pseries VMC driver

</td>
</tr>
<tr>
<td>


0xCD

</td>
<td>


01

</td>
<td>


linux/reiserfs_fs.h

</td>
<td>


Dead since 6.13

</td>
</tr>
<tr>
<td>


0xCE

</td>
<td>


01-02

</td>
<td>


uapi/linux/cxl_mem.h

</td>
<td>


Compute Express Link Memory Devices

</td>
</tr>
<tr>
<td>


0xCF

</td>
<td>


02

</td>
<td>


fs/smb/client/cifs_ioctl.h

</td>
<td>




</td>
</tr>
<tr>
<td>


0xDD

</td>
<td>


00-3F

</td>
<td>




</td>
<td>


ZFCP device driver see drivers/s390/scsi/ &lt;[mailto:aherrman@de.ibm.com](<mailto:aherrman@de.ibm.com>)&gt;

</td>
</tr>
<tr>
<td>


0xE5

</td>
<td>


00-3F

</td>
<td>


linux/fuse.h

</td>
<td>




</td>
</tr>
<tr>
<td>


0xEC

</td>
<td>


00-01

</td>
<td>


drivers/platform/chrome/cros_ec_dev.h

</td>
<td>


ChromeOS EC driver

</td>
</tr>
<tr>
<td>


0xEE

</td>
<td>


00-09

</td>
<td>


uapi/linux/pfrut.h

</td>
<td>


Platform Firmware Runtime Update and Telemetry

</td>
</tr>
<tr>
<td>


0xF3

</td>
<td>


00-3F

</td>
<td>


drivers/usb/misc/sisusbvga/sisusb.h

</td>
<td>


sisfb (in development) &lt;[mailto:thomas@winischhofer.net](<mailto:thomas@winischhofer.net>)&gt;

</td>
</tr>
<tr>
<td>


0xF6

</td>
<td>


all

</td>
<td>




</td>
<td>


LTTng Linux Trace Toolkit Next Generation &lt;[mailto:mathieu.desnoyers@efficios.com](<mailto:mathieu.desnoyers@efficios.com>)&gt;

</td>
</tr>
<tr>
<td>


0xF8

</td>
<td>


all

</td>
<td>


arch/x86/include/uapi/asm/amd_hsmp.h

</td>
<td>


AMD HSMP EPYC system management interface driver &lt;[mailto:nchatrad@amd.com](<mailto:nchatrad@amd.com>)&gt;

</td>
</tr>
<tr>
<td>


0xF9

</td>
<td>


00-0F

</td>
<td>


uapi/misc/amd-apml.h

</td>
<td>


AMD side band system management interface driver &lt;[mailto:naveenkrishna.chatradhi@amd.com](<mailto:naveenkrishna.chatradhi@amd.com>)&gt;

</td>
</tr>
<tr>
<td>


0xFD

</td>
<td>


all

</td>
<td>


linux/dm-ioctl.h

</td>
<td>




</td>
</tr>
<tr>
<td>


0xFE

</td>
<td>


all

</td>
<td>


linux/isst_if.h

</td>
<td>




</td>
</tr>
</tbody>
</table>
