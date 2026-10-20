---
title: "AppArmor"
type: reference
description: "AppArmor is MAC style security extension for the Linux kernel. It implements a task centered policy, with task \"profiles\" being created and loaded from user space. Tasks on the system that do not have a profile defined for them run in an…"
---

> **Peios:** This is reference material for an upstream LSM or its configuration. Peios configures `landlock,lockdown,integrity,pkm`; alternative MAC LSMs are incompatible with PKM, and this article is not an instruction to replace the Peios security stack. See [Peios kernel behaviour](<~kernel/introduction/peios-behaviour>).


<a id="rst-apparmor"></a>

<a id="rst-what-is-apparmor"></a>

## What is AppArmor?

AppArmor is MAC style security extension for the Linux kernel.  It implements a task centered policy, with task "profiles" being created and loaded from user space.  Tasks on the system that do not have a profile defined for them run in an unconfined state which is equivalent to standard Linux DAC permissions.

<a id="rst-how-to-enable-disable"></a>

## How to enable/disable

set `CONFIG_SECURITY_APPARMOR=y`

If AppArmor should be selected as the default security module then set:



```text
CONFIG_DEFAULT_SECURITY_APPARMOR=y
```

The CONFIG_LSM parameter manages the order and selection of LSMs. Specify apparmor as the first "major" module (e.g. AppArmor, SELinux, Smack) in the list.

Build the kernel

If AppArmor is not the default security module it can be enabled by passing `security=apparmor` on the kernel's command line.

If AppArmor is the default security module it can be disabled by passing `apparmor=0, security=XXXX` (where `XXXX` is valid security module), on the kernel's command line.

For AppArmor to enforce any restrictions beyond standard Linux DAC permissions policy must be loaded into the kernel from user space (see the Documentation and tools links).

<a id="rst-documentation"></a>

## Documentation

Documentation can be found on the wiki, linked below.

<a id="rst-links"></a>

## Links

Mailing List - [apparmor@lists.ubuntu.com](<mailto:apparmor@lists.ubuntu.com>)

Wiki - [http://wiki.apparmor.net](<http://wiki.apparmor.net>)

User space tools - [https://gitlab.com/apparmor](<https://gitlab.com/apparmor>)

Kernel module - git://git.kernel.org/pub/scm/linux/kernel/git/jj/linux-apparmor
