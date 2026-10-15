---
title: "Digital TV demux open()"
type: reference
description: "Digital TV demux open()"
---

<a id="rst-digital-tv-demux-open"></a>
<a id="rst-dmx-fopen"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: DTV.dmx -->

<a id="rst-name"></a>

## Name

Digital TV demux open()

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-open"></a>

```c
int open(const char *deviceName, int flags)
```

<a id="rst-arguments"></a>

## Arguments

- **`name`**

  Name of specific Digital TV demux device.

- **`flags`**

  A bit-wise OR of the following flags:

<!-- tabularcolumns: |p{2.5cm}|p{15.0cm}| -->


<table>
<tbody>
<tr>
<td>


`O_RDONLY`

</td>
<td>


read-only access

</td>
</tr>
<tr>
<td>


`O_RDWR`

</td>
<td>


read/write access

</td>
</tr>
<tr>
<td>


`O_NONBLOCK`

</td>
<td>


open in non-blocking mode (blocking mode is the default)

</td>
</tr>
</tbody>
</table>

<a id="rst-description"></a>

## Description

This system call, used with a device name of `/dev/dvb/adapter?/demux?`, allocates a new filter and returns a handle which can be used for subsequent control of that filter. This call has to be made for each filter to be used, i.e. every returned file descriptor is a reference to a single filter. `/dev/dvb/adapter?/dvr?` is a logical device to be used for retrieving Transport Streams for digital video recording. When reading from this device a transport stream containing the packets from all PES filters set in the corresponding demux device (`/dev/dvb/adapter?/demux?`) having the output set to `DMX_OUT_TS_TAP`. A recorded Transport Stream is replayed by writing to this device.

The significance of blocking or non-blocking mode is described in the documentation for functions where there is a difference. It does not affect the semantics of the `open()` call itself. A device opened in blocking mode can later be put into non-blocking mode (and vice versa) using the `F_SETFL` command of the fcntl system call.

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned.

On error -1 is returned, and the `errno` variable is set appropriately.

<!-- tabularcolumns: |p{2.5cm}|p{15.0cm}| -->


<table>
<tbody>
<tr>
<td>


`EMFILE`

</td>
<td>


"Too many open files", i.e. no more filters available.

</td>
</tr>
</tbody>
</table>

The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
