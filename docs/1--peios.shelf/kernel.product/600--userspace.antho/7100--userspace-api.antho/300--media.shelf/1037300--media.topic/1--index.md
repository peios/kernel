---
title: "Linux Media Infrastructure userspace API"
type: reference
description: "This section contains the driver development information and Kernel APIs used by media devices."
---

<a id="rst-linux-media-infrastructure-userspace-api"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

<!-- This data file has been placed in the public domain. -->

<!-- Derived from the Unicode character mappings available from
<http://www.w3.org/2003/entities/xml/>.
Processed by unicode2rstsubs.py, part of Docutils:
<https://docutils.sourceforge.io>. -->

This section contains the  driver development information and Kernel APIs used by media devices.

Please see:

[Documentation/admin-guide/media/index.rst](~kernel/administration/admin-guide/media/index)

> - for usage information about media subsystem and supported drivers;

[Documentation/driver-api/media/index.rst](~kernel/hardware/driver-api/media/index)

> - for driver development information and Kernel APIs used by media devices;

**Table of Contents**

- [Introduction](<~kernel/userspace/userspace-api/media/intro>)
- [Part I - Video for Linux API](<~kernel/userspace/userspace-api/media-v4l/v4l2>)
- [Part II - Digital TV API](<~kernel/userspace/userspace-api/media-dvb/dvbapi>)
- [Part III - Remote Controller API](<~kernel/userspace/userspace-api/media-rc/remote-controllers>)
- [Part IV - Media Controller API](<~kernel/userspace/userspace-api/media-mediactl/media-controller>)
- [Part V - Consumer Electronics Control API](<~kernel/userspace/userspace-api/media-cec/cec-api>)
- [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors>)
- [glossary](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/glossary.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>)
- [GNU Free Documentation License](<~kernel/userspace/userspace-api/media/fdl-appendix>)
- [Video4Linux (V4L)  driver-specific documentation](<~kernel/userspace/userspace-api/media-drivers/index>)

**Copyright** © 2009-2020 : LinuxTV Developers



```text
Permission is granted to copy, distribute and/or modify this document
under the terms of the GNU Free Documentation License, Version 1.1 or
any later version published by the Free Software Foundation, with no
Invariant Sections. A copy of the license is included in the chapter
entitled "GNU Free Documentation License".
```

Please notice that some documents inside the media userspace API, when explicitly mentioned on its source code, are dual-licensed with GNU Free Documentation License  Version 1.1 and with the GNU General Public License:



```text
This documentation is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the Free
Software Foundation; either version 2 of the License, or (at your option) any
later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
more details.

For more details see the file COPYING in the source distribution of Linux.
```
