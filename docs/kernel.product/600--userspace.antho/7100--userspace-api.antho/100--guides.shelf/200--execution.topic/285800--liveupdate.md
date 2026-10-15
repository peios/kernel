---
title: "Live Update uAPI"
type: reference
description: "Live Update Orchestrator </core-api/liveupdate>"
---

<a id="rst-live-update-uapi"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

**Author:** Pasha Tatashin &lt;[pasha.tatashin@soleen.com](<mailto:pasha.tatashin@soleen.com>)&gt;

<a id="rst-ioctl-interface"></a>

## ioctl interface

```{kernel-doc} kernel/liveupdate/luo_core.c
:doc: LUO ioctl Interface
```

<a id="rst-ioctl-uapi"></a>

## ioctl uAPI

```{kernel-doc} include/uapi/linux/liveupdate.h

```

<a id="rst-see-also"></a>

## See Also

- [Live Update Orchestrator](<~kernel/internals/core-api/liveupdate>)
