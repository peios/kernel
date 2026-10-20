---
title: "Linux Security Module Development"
type: reference
description: "Based on https://lore.kernel.org/r/20071026073721.618b4778@laptopd505.fenrus.org, a new LSM is accepted into the kernel when its intent (a description of what it tries to protect against and in what cases one would expect to use it) has…"
---

> **Peios:** The generated declarations below are read from the kernel source. Peios adds native checks at the file, process, IPC and socket boundaries; inherited comments about Unix permissions or capability names are not a complete access policy. See [Peios kernel behaviour](<~kernel/introduction/peios-behaviour>) and the [VFS callback reference](<~kernel/internals/filesystems/vfs>) for the Peios integration contracts.


<a id="rst-linux-security-module-development"></a>

Based on [https://lore.kernel.org/r/20071026073721.618b4778@laptopd505.fenrus.org](<https://lore.kernel.org/r/20071026073721.618b4778@laptopd505.fenrus.org>), a new LSM is accepted into the kernel when its intent (a description of what it tries to protect against and in what cases one would expect to use it) has been appropriately documented in `Documentation/admin-guide/LSM/`. This allows an LSM's code to be easily compared to its goals, and so that end users and distros can make a more informed decision about which LSMs suit their requirements.

For extensive documentation on the available LSM hook interfaces, please see `security/security.c` and associated structures:

```{kernel-doc} security/security.c
:export:
```
