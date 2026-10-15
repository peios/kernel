---
title: "Embedded device command line partition parsing"
type: reference
description: "The \"blkdevparts\" command line option adds support for reading the block device partition table from the kernel command line."
---

<a id="rst-embedded-device-command-line-partition-parsing"></a>

The "blkdevparts" command line option adds support for reading the block device partition table from the kernel command line.

It is typically used for fixed block (eMMC) embedded devices. It has no MBR, so saves storage space. Bootloader can be easily accessed by absolute address of data on the block device. Users can easily change the partition.

The format for the command line is just like mtdparts:

- **blkdevparts=&lt;blkdev-def&gt;\[;&lt;blkdev-def&gt;\]**

  - **&lt;blkdev-def&gt; := &lt;blkdev-id&gt;:&lt;partdef&gt;\[,&lt;partdef&gt;\]**

    &lt;partdef&gt; := &lt;size&gt;\[@&lt;offset&gt;\](part-name)

- **&lt;blkdev-id&gt;**

  block device disk name. Embedded device uses fixed block device. Its disk name is also fixed, such as: mmcblk0, mmcblk1, mmcblk0boot0.

- **&lt;size&gt;**

  partition size, in bytes, such as: 512, 1m, 1G. size may contain an optional suffix of (upper or lower case):

  > K, M, G, T, P, E.

  "-" is used to denote all remaining space.

- **&lt;offset&gt;**

  partition start address, in bytes. offset may contain an optional suffix of (upper or lower case):

  > K, M, G, T, P, E.

- **(part-name)**

  partition name. Kernel sends uevent with "PARTNAME". Application can create a link to block device partition with the name "PARTNAME". User space application can access partition by partition name.

- **ro**

  read-only. Flag the partition as read-only.

Example:

> > eMMC disk names are "mmcblk0" and "mmcblk0boot0".
>
> bootargs:
>
>
>
> ```text
> 'blkdevparts=mmcblk0:1G(data0),1G(data1),-;mmcblk0boot0:1m(boot)ro,-(kernel)'
> ```
>
> dmesg:
>
>
>
> ```text
> mmcblk0: p1(data0) p2(data1) p3()
> mmcblk0boot0: p1(boot) p2(kernel)
> ```
