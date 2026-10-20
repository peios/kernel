---
title: "Memfd Preservation via LUO"
type: reference
description: "/core-api/liveupdate"
---

<a id="rst-memfd-preservation-via-luo"></a>

<!-- SPDX-License-Identifier: GPL-2.0-or-later -->

```{kernel-doc} mm/memfd_luo.c
:doc: Memfd Preservation via LUO
```

<a id="rst-memfd-preservation-abi"></a>

## Memfd Preservation ABI

```{kernel-doc} include/linux/kho/abi/memfd.h
:doc: DOC: memfd Live Update ABI
```

```{kernel-doc} include/linux/kho/abi/memfd.h
:internal:
```

<a id="rst-see-also"></a>

## See Also

- [Live Update Orchestrator](<~kernel/internals/core-api/liveupdate>)

- [Kexec Handover Subsystem](<~kernel/internals/core-api/kho/index>)
