---
title: "TTY Internals"
type: reference
description: "Kopen"
---

<a id="rst-tty-internals"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

<a id="rst-contents"></a>



<a id="rst-kopen"></a>

## Kopen

These functions serve for opening a TTY from the kernelspace:

```{kernel-doc} drivers/tty/tty_io.c
:identifiers: tty_kopen_exclusive tty_kopen_shared tty_kclose
```

---

<a id="rst-exported-internal-functions"></a>

## Exported Internal Functions

```{kernel-doc} drivers/tty/tty_io.c
:identifiers: tty_release_struct tty_dev_name_to_number tty_get_icount
```

---

<a id="rst-internal-functions"></a>

## Internal Functions

```{kernel-doc} drivers/tty/tty_io.c
:internal:
```
