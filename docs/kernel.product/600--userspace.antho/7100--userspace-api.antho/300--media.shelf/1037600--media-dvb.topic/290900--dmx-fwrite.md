---
title: "Digital TV demux write()"
type: reference
description: "Digital TV demux write()"
---

<a id="rst-digital-tv-demux-write"></a>
<a id="rst-dmx-fwrite"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: DTV.dmx -->

<a id="rst-name"></a>

## Name

Digital TV demux write()

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-write"></a>

```c
ssize_t write(int fd, const void *buf, size_t count)
```

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by a previous call to `open()`.

- **`buf`**

  Buffer with data to be written

- **`count`**

  Number of bytes at the buffer

<a id="rst-description"></a>

## Description

This system call is only provided by the logical device `/dev/dvb/adapter?/dvr?`, associated with the physical demux device that provides the actual DVR functionality. It is used for replay of a digitally recorded Transport Stream. Matching filters have to be defined in the corresponding physical demux device, `/dev/dvb/adapter?/demux?`. The amount of data to be transferred is implied by count.

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


No data was written. This might happen if `O_NONBLOCK` was specified and there is no more buffer space available (if `O_NONBLOCK` is not specified the function will block until buffer space is available).

</td>
</tr>
<tr>
<td>


`EBUSY`

</td>
<td>


This error code indicates that there are conflicting requests. The corresponding demux device is setup to receive data from the front- end. Make sure that these filters are stopped and that the filters with input set to `DMX_IN_DVR` are started.

</td>
</tr>
</tbody>
</table>

The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
