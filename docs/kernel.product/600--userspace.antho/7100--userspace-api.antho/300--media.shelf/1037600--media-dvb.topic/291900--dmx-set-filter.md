---
title: "DMX_SET_FILTER"
type: reference
description: "Duplicate implicit target name: \"dmx_set_filter\"."
---

<a id="rst-dmx-set-filter-1"></a>
<a id="rst-dmx-set-filter"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: DTV.dmx -->

<a id="rst-name"></a>

## Name

DMX_SET_FILTER

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-DMX_SET_FILTER"></a>

```c
DMX_SET_FILTER
```

`int ioctl(int fd, DMX_SET_FILTER, struct dmx_sct_filter_params *params)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

`params`

> Pointer to structure containing filter parameters.

<a id="rst-description"></a>

## Description

This ioctl call sets up a filter according to the filter and mask parameters provided. A timeout may be defined stating number of seconds to wait for a section to be loaded. A value of 0 means that no timeout should be applied. Finally there is a flag field where it is possible to state whether a section should be CRC-checked, whether the filter should be a "one-shot" filter, i.e. if the filtering operation should be stopped after the first section is received, and whether the filtering operation should be started immediately (without waiting for a [DMX_START](<~kernel/userspace/userspace-api/media-dvb/dmx-start#rst-dmx-start-1>) ioctl call). If a filter was previously set-up, this filter will be canceled, and the receive buffer will be flushed.

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned.

On error -1 is returned, and the `errno` variable is set appropriately.

The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
