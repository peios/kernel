---
title: "TTY Struct"
type: reference
description: "Initialization"
---

<a id="rst-tty-struct"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

<a id="rst-contents"></a>



struct tty_struct is allocated by the TTY layer upon the first open of the TTY device and released after the last close. The TTY layer passes this structure to most of struct tty_operation's hooks. Members of tty_struct are documented in [TTY Struct Reference](<#rst-tty-struct-reference>) at the bottom.

<a id="rst-initialization"></a>

## Initialization

```{kernel-doc} drivers/tty/tty_io.c
:identifiers: tty_init_termios
```

<a id="rst-name"></a>

## Name

```{kernel-doc} drivers/tty/tty_io.c
:identifiers: tty_name
```

<a id="rst-reference-counting"></a>

## Reference counting

```{kernel-doc} include/linux/tty.h
:identifiers: tty_kref_get
```

```{kernel-doc} drivers/tty/tty_io.c
:identifiers: tty_kref_put
```

<a id="rst-install"></a>

## Install

```{kernel-doc} drivers/tty/tty_io.c
:identifiers: tty_standard_install
```

<a id="rst-read-write"></a>

## Read &amp; Write

```{kernel-doc} drivers/tty/tty_io.c
:identifiers: tty_put_char
```

<a id="rst-start-stop"></a>

## Start &amp; Stop

```{kernel-doc} drivers/tty/tty_io.c
:identifiers: start_tty stop_tty
```

<a id="rst-wakeup"></a>

## Wakeup

```{kernel-doc} drivers/tty/tty_io.c
:identifiers: tty_wakeup
```

<a id="rst-hangup"></a>

## Hangup

```{kernel-doc} drivers/tty/tty_io.c
:identifiers: tty_hangup tty_vhangup tty_hung_up_p
```

<a id="rst-misc"></a>

## Misc

```{kernel-doc} drivers/tty/tty_io.c
:identifiers: tty_do_resize
```

<a id="rst-tty-struct-flags"></a>

## TTY Struct Flags

```{kernel-doc} include/linux/tty.h
:identifiers: tty_struct_flags
```

<a id="rst-tty-struct-reference"></a>

## TTY Struct Reference

```{kernel-doc} include/linux/tty.h
:identifiers: tty_struct
```
