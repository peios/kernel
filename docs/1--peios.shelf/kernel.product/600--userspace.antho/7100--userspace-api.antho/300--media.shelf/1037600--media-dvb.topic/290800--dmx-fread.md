---
title: "Digital TV demux read()"
type: reference
description: "Digital TV demux read()"
---

<a id="rst-digital-tv-demux-read"></a>
<a id="rst-dmx-fread"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: DTV.dmx -->

<a id="rst-name"></a>

## Name

Digital TV demux read()

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-read"></a>

```c
size_t read(int fd, void *buf, size_t count)
```

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  > File descriptor returned by a previous call to `open()`.

  - **`buf`**

    Buffer to be filled

- **`count`**

  Max number of bytes to read

<a id="rst-description"></a>

## Description

This system call returns filtered data, which might be section or Packetized Elementary Stream (PES) data. The filtered data is transferred from the driver's internal circular buffer to `buf`. The maximum amount of data to be transferred is implied by count.

> [!NOTE]
>
> if a section filter created with `DMX_CHECK_CRC <dmx_sct_filter_params>` flag set, data that fails on CRC check will be silently ignored.

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned.

On error -1 is returned, and the `errno` variable is set appropriately.

<!-- tabularcolumns: |p{2.5cm}|p{15.0cm}| -->


<table>
<tbody>
<tr>
<td>


`EWOULDBLOCK`

</td>
<td>


No data to return and `O_NONBLOCK` was specified.

</td>
</tr>
<tr>
<td>


`EOVERFLOW`

</td>
<td>


The filtered data was not read from the buffer in due time, resulting in non-read data being lost. The buffer is flushed.

</td>
</tr>
<tr>
<td>


`ETIMEDOUT`

</td>
<td>


The section was not loaded within the stated timeout period. See ioctl [DMX_SET_FILTER](<~kernel/userspace/userspace-api/media-dvb/dmx-set-filter#rst-dmx-set-filter-1>) for how to set a timeout.

</td>
</tr>
<tr>
<td>


`EFAULT`

</td>
<td>


The driver failed to write to the callers buffer due to an invalid \*buf pointer.

</td>
</tr>
</tbody>
</table>

The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
