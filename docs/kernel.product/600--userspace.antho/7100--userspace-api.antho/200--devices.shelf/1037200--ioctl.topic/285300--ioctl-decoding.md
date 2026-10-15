---
title: "Decoding an IOCTL Magic Number"
type: reference
description: "To decode a hex IOCTL code:"
---

<a id="rst-decoding-an-ioctl-magic-number"></a>

To decode a hex IOCTL code:

Most architectures use this generic format, but check include/ARCH/ioctl.h for specifics, e.g. powerpc uses 3 bits to encode read/write and 13 bits for size.

>
> <table>
> <thead>
> <tr>
> <th>
>
>
> bits
>
> </th>
> <th>
>
>
> meaning
>
> </th>
> </tr>
> </thead>
> <tbody>
> <tr>
> <td>
>
>
> 31-30
>
> </td>
> <td>
>
>
> 00 - no parameters: uses \_IO macro 10 - read: \_IOR 01 - write: \_IOW 11 - read/write: \_IOWR
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 29-16
>
> </td>
> <td>
>
>
> size of arguments
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 15-8
>
> </td>
> <td>
>
>
> ascii character supposedly unique to each driver
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 7-0
>
> </td>
> <td>
>
>
> function \#
>
> </td>
> </tr>
> </tbody>
> </table>

So for example 0x82187201 is a read with arg length of 0x218, character 'r' function 1. Grepping the source reveals this is:



```text
#define VFAT_IOCTL_READDIR_BOTH         _IOR('r', 1, struct dirent [2])
```
