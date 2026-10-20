---
title: "No New Privileges Flag"
type: reference
description: "The irreversible exec restriction and its interaction with Peios integrity and tokens."
---

<a id="rst-no-new-privileges-flag"></a>

Any task can set `no_new_privs`. Once set, the bit is inherited across fork,
clone and exec and cannot be unset:

```c
prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0);
```

Linux uses this flag to prevent exec from gaining authority through set-user-ID,
set-group-ID and file-capability transitions. Peios retains the flag and adds
an integrity rule: exec under `no_new_privs` cannot raise the process's PIP type
or trust above its current label. The same cap applies to unsafe traced execs.
Executing a more highly signed image therefore does not automatically raise
the integrity of a process controlled by a less trusted supervisor.

Peios authority comes from native tokens, descriptors and enabled privileges.
Unix-ID setters and `setcap` are not native authority-granting operations, even
without `no_new_privs`. See [Peios kernel behaviour](<~kernel/introduction/peios-behaviour>) for those compatibility rules.

The flag is useful when installing seccomp filters that persist across exec.
The unprivileged filter-installation path requires `no_new_privs`; the alternative
privileged path retains its native capability check. Seccomp and Landlock add
restrictions, rather than granting access refused by KACS.

`no_new_privs` does not revoke the current token, remove already enabled native
privileges or close existing handles. It is not a substitute for native token
restriction. Transfers of descriptors with `SCM_RIGHTS` are not prohibited by
this flag itself; their own access and transfer rules still apply. Nor does
the flag authorize namespace creation or `chroot` on its own.
