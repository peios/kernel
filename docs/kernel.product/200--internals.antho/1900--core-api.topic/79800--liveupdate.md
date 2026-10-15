---
title: "Live Update Orchestrator"
type: reference
description: "The following types of file descriptors can be preserved"
---

<a id="rst-live-update-orchestrator"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

**Author:** Pasha Tatashin &lt;[pasha.tatashin@soleen.com](<mailto:pasha.tatashin@soleen.com>)&gt;

```{kernel-doc} kernel/liveupdate/luo_core.c
:doc: Live Update Orchestrator (LUO)
```

<a id="rst-luo-sessions"></a>

## LUO Sessions

```{kernel-doc} kernel/liveupdate/luo_session.c
:doc: LUO Sessions
```

<a id="rst-luo-preserving-file-descriptors"></a>

## LUO Preserving File Descriptors

```{kernel-doc} kernel/liveupdate/luo_file.c
:doc: LUO File Descriptors
```

<a id="rst-luo-file-lifecycle-bound-global-data"></a>

## LUO File Lifecycle Bound Global Data

```{kernel-doc} kernel/liveupdate/luo_flb.c
:doc: LUO File Lifecycle Bound Global Data
```

<a id="rst-live-update-orchestrator-abi"></a>

## Live Update Orchestrator ABI

```{kernel-doc} include/linux/kho/abi/luo.h
:doc: Live Update Orchestrator ABI
```

The following types of file descriptors can be preserved

- [Memfd Preservation via LUO](<~kernel/internals/mm/memfd-preservation>)

<a id="rst-public-api"></a>

## Public API

```{kernel-doc} include/linux/liveupdate.h

```

```{kernel-doc} include/linux/kho/abi/luo.h
:functions:
```

```{kernel-doc} kernel/liveupdate/luo_core.c
:export:
```

```{kernel-doc} kernel/liveupdate/luo_flb.c
:export:
```

```{kernel-doc} kernel/liveupdate/luo_file.c
:export:
```

<a id="rst-internal-api"></a>

## Internal API

```{kernel-doc} kernel/liveupdate/luo_core.c
:internal:
```

```{kernel-doc} kernel/liveupdate/luo_flb.c
:internal:
```

```{kernel-doc} kernel/liveupdate/luo_session.c
:internal:
```

```{kernel-doc} kernel/liveupdate/luo_file.c
:internal:
```

<a id="rst-see-also"></a>

## See Also

- [Live Update uAPI](<~kernel/userspace/userspace-api/liveupdate>)

- [Kexec Handover Subsystem](<~kernel/internals/core-api/kho/index>)
