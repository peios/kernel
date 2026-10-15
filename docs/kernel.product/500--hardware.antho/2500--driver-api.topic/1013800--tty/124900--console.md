---
title: "Console"
type: reference
description: "Struct Console"
---

<a id="rst-console"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

<a id="rst-contents"></a>



<a id="rst-struct-console"></a>

## Struct Console

```{kernel-doc} include/linux/console.h
:identifiers: console cons_flags
```

<a id="rst-internals"></a>

### Internals

```{kernel-doc} include/linux/console.h
:identifiers: nbcon_state nbcon_prio nbcon_context nbcon_write_context
```

<a id="rst-struct-consw"></a>

## Struct Consw

```{kernel-doc} include/linux/console.h
:identifiers: consw
```

<a id="rst-console-functions"></a>

## Console functions

```{kernel-doc} include/linux/console.h
:identifiers: console_srcu_read_flags console_srcu_write_flags console_is_registered for_each_console_srcu for_each_console
```

```{kernel-doc} drivers/tty/vt/selection.c
:export:
```

```{kernel-doc} drivers/tty/vt/vt.c
:export:
```

<a id="rst-internals-1"></a>

### Internals

```{kernel-doc} drivers/tty/vt/selection.c
:internal:
```

```{kernel-doc} drivers/tty/vt/vt.c
:internal:
```
