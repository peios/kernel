---
title: "Documentation for /proc/sys"
type: reference
description: "Copyright (c) 1998, 1999, Rik van Riel <riel@nl.linux.org>"
---

<a id="rst-documentation-for-proc-sys"></a>

Copyright (c) 1998, 1999,  Rik van Riel &lt;[riel@nl.linux.org](<mailto:riel@nl.linux.org>)&gt;

---

'Why', I hear you ask, 'would anyone even \_want\_ documentation for them sysctl files? If anybody really needs it, it's all in the source...'

Well, this documentation is written because some people either don't know they need to tweak something, or because they don't have the time or knowledge to read the source code.

Furthermore, the programmers who built sysctl have built it to be actually used, not just for the fun of programming it :-)

---

Legal blurb:

As usual, there are two main things to consider:

1. you get what you pay for

2. it's free

The consequences are that I won't guarantee the correctness of this document, and if you come to me complaining about how you screwed up your system because of wrong documentation, I won't feel sorry for you. I might even laugh at you...

But of course, if you \_do\_ manage to screw up your system using only the sysctl options used in this file, I'd like to hear of it. Not only to have a great laugh, but also to make sure that you're the last RTFMing person to screw up.

In short, e-mail your suggestions, corrections and / or horror stories to: &lt;[riel@nl.linux.org](<mailto:riel@nl.linux.org>)&gt;

Rik van Riel.

---

<a id="rst-introduction"></a>

## Introduction

Sysctl is a means of configuring certain aspects of the kernel at run-time, and the /proc/sys/ directory is there so that you don't even need special tools to do it\! In fact, there are only four things needed to use these config facilities:

- a running Linux system

- root access

- common sense (this is especially hard to come by these days)

- knowledge of what all those values mean

As a quick 'ls /proc/sys' will show, the directory consists of several (arch-dependent?) subdirs. Each subdir is mainly about one part of the kernel, so you can do configuration on a piece by piece basis, or just some 'thematic frobbing'.

This documentation is about:


<table>
<tbody>
<tr>
<td>


abi/

</td>
<td>


execution domains &amp; personalities

</td>
</tr>
<tr>
<td>


&lt;$ARCH&gt;

</td>
<td>


tuning controls for various CPU architecture (e.g. csky, s390)

</td>
</tr>
<tr>
<td>


crypto/

</td>
<td>


&lt;undocumented&gt;

</td>
</tr>
<tr>
<td>


debug/

</td>
<td>


&lt;undocumented&gt;

</td>
</tr>
<tr>
<td>


dev/

</td>
<td>


device specific information (e.g. dev/cdrom/info)

</td>
</tr>
<tr>
<td>


fs/

</td>
<td>


specific filesystems filehandle, inode, dentry and quota tuning binfmt_misc &lt;[Documentation/admin-guide/binfmt-misc.rst](~kernel/administration/admin-guide/binfmt-misc)&gt;

</td>
</tr>
<tr>
<td>


kernel/

</td>
<td>


global kernel info / tuning miscellaneous stuff some architecture-specific controls security (LSM) stuff

</td>
</tr>
<tr>
<td>


net/

</td>
<td>


networking stuff, for documentation look in: &lt;Documentation/networking/&gt;

</td>
</tr>
<tr>
<td>


proc/

</td>
<td>


&lt;empty&gt;

</td>
</tr>
<tr>
<td>


sunrpc/

</td>
<td>


SUN Remote Procedure Call (NFS)

</td>
</tr>
<tr>
<td>


user/

</td>
<td>


Per user namespace limits

</td>
</tr>
<tr>
<td>


vm/

</td>
<td>


memory management tuning buffer and cache management

</td>
</tr>
<tr>
<td>


xen/

</td>
<td>


&lt;undocumented&gt;

</td>
</tr>
</tbody>
</table>

These are the subdirs I have on my system or have been discovered by searching through the source code. There might be more or other subdirs in another setup. If you see another dir, I'd really like to hear about it :-)

- [Documentation for /proc/sys/abi/](<~kernel/administration/admin-guide/sysctl/abi>)
- [Documentation for /proc/sys/fs/](<~kernel/administration/admin-guide/sysctl/fs>)
- [Documentation for /proc/sys/kernel/](<~kernel/administration/admin-guide/sysctl/kernel>)
- [Documentation for /proc/sys/net/](<~kernel/administration/admin-guide/sysctl/net>)
- [Documentation for /proc/sys/sunrpc/](<~kernel/administration/admin-guide/sysctl/sunrpc>)
- [Documentation for /proc/sys/user/](<~kernel/administration/admin-guide/sysctl/user>)
- [Documentation for /proc/sys/vm/](<~kernel/administration/admin-guide/sysctl/vm>)
