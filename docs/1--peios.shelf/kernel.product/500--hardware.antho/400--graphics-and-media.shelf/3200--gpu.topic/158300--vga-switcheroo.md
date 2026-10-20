---
title: "VGA Switcheroo"
type: reference
description: "Duplicate implicit target name: \"public functions\"."
---

<a id="rst-vga-switcheroo-1"></a>
<a id="rst-vga-switcheroo"></a>

```{kernel-doc} drivers/gpu/vga/vga_switcheroo.c
:doc: Overview
```

<a id="rst-modes-of-use"></a>

## Modes of Use

<a id="rst-manual-switching-and-manual-power-control"></a>

### Manual switching and manual power control

```{kernel-doc} drivers/gpu/vga/vga_switcheroo.c
:doc: Manual switching and manual power control
```

<a id="rst-driver-power-control"></a>

### Driver power control

```{kernel-doc} drivers/gpu/vga/vga_switcheroo.c
:doc: Driver power control
```

<a id="rst-api"></a>

## API

<a id="rst-public-functions"></a>

### Public functions

```{kernel-doc} drivers/gpu/vga/vga_switcheroo.c
:export:
```

<a id="rst-public-structures"></a>

### Public structures

```{kernel-doc} include/linux/vga_switcheroo.h
:functions: vga_switcheroo_handler
```

```{kernel-doc} include/linux/vga_switcheroo.h
:functions: vga_switcheroo_client_ops
```

<a id="rst-public-constants"></a>

### Public constants

```{kernel-doc} include/linux/vga_switcheroo.h
:functions: vga_switcheroo_handler_flags_t
```

```{kernel-doc} include/linux/vga_switcheroo.h
:functions: vga_switcheroo_client_id
```

```{kernel-doc} include/linux/vga_switcheroo.h
:functions: vga_switcheroo_state
```

<a id="rst-private-structures"></a>

### Private structures

```{kernel-doc} drivers/gpu/vga/vga_switcheroo.c
:functions: vgasr_priv
```

```{kernel-doc} drivers/gpu/vga/vga_switcheroo.c
:functions: vga_switcheroo_client
```

<a id="rst-handlers"></a>

## Handlers

<a id="rst-apple-gmux-handler"></a>

### apple-gmux Handler

```{kernel-doc} drivers/platform/x86/apple-gmux.c
:doc: Overview
```

```{kernel-doc} drivers/platform/x86/apple-gmux.c
:doc: Interrupt
```

<a id="rst-graphics-mux"></a>

#### Graphics mux

```{kernel-doc} drivers/platform/x86/apple-gmux.c
:doc: Graphics mux
```

<a id="rst-power-control"></a>

#### Power control

```{kernel-doc} drivers/platform/x86/apple-gmux.c
:doc: Power control
```

<a id="rst-backlight-control"></a>

#### Backlight control

```{kernel-doc} drivers/platform/x86/apple-gmux.c
:doc: Backlight control
```

<a id="rst-public-functions-1"></a>

#### Public functions

```{kernel-doc} include/linux/apple-gmux.h
:internal:
```
