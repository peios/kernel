---
title: "TTY Port"
type: reference
description: "TTY Port Functions"
---

<a id="rst-tty-port"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

<a id="rst-contents"></a>



The TTY drivers are advised to use struct tty_port helpers as much as possible. If the drivers implement `tty_port.ops.activate()` and `tty_port.ops.shutdown()`, they can use tty_port_open(), tty_port_close(), and tty_port_hangup() in respective `tty_struct.ops` hooks.

The reference and details are contained in the [TTY Port Reference](<#rst-tty-port-reference>) and [TTY Port Operations Reference](<#rst-tty-port-operations-reference>) sections at the bottom.

<a id="rst-tty-port-functions"></a>

## TTY Port Functions

<a id="rst-init-destroy"></a>

### Init &amp; Destroy

```{kernel-doc} drivers/tty/tty_port.c
:identifiers: tty_port_init tty_port_destroy tty_port_get tty_port_put
```

<a id="rst-open-close-hangup-helpers"></a>

### Open/Close/Hangup Helpers

```{kernel-doc} drivers/tty/tty_port.c
:identifiers: tty_port_install tty_port_open tty_port_block_til_ready tty_port_close tty_port_close_start tty_port_close_end tty_port_hangup tty_port_shutdown
```

<a id="rst-tty-refcounting"></a>

### TTY Refcounting

```{kernel-doc} drivers/tty/tty_port.c
:identifiers: tty_port_tty_get tty_port_tty_set
```

<a id="rst-tty-helpers"></a>

### TTY Helpers

```{kernel-doc} include/linux/tty_port.h
:identifiers: tty_port_tty_hangup tty_port_tty_vhangup
```

```{kernel-doc} drivers/tty/tty_port.c
:identifiers: tty_port_tty_wakeup
```

<a id="rst-modem-signals"></a>

### Modem Signals

```{kernel-doc} drivers/tty/tty_port.c
:identifiers: tty_port_carrier_raised tty_port_raise_dtr_rts tty_port_lower_dtr_rts
```

---

<a id="rst-tty-port-reference"></a>

## TTY Port Reference

```{kernel-doc} include/linux/tty_port.h
:identifiers: tty_port
```

---

<a id="rst-tty-port-operations-reference"></a>

## TTY Port Operations Reference

```{kernel-doc} include/linux/tty_port.h
:identifiers: tty_port_operations
```
