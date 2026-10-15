---
title: "Digital TV CA open()"
type: reference
description: "Digital TV CA open()"
---

<a id="rst-digital-tv-ca-open"></a>
<a id="rst-ca-fopen"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: DTV.ca -->

<a id="rst-name"></a>

## Name

Digital TV CA open()

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-open"></a>

```c
int open(const char *name, int flags)
```

<a id="rst-arguments"></a>

## Arguments

- **`name`**

  Name of specific Digital TV CA device.

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

This system call opens a named ca device (e.g. `/dev/dvb/adapter?/ca?`) for subsequent use.

When an `open()` call has succeeded, the device will be ready for use. The significance of blocking or non-blocking mode is described in the documentation for functions where there is a difference. It does not affect the semantics of the `open()` call itself. A device opened in blocking mode can later be put into non-blocking mode (and vice versa) using the `F_SETFL` command of the `fcntl` system call. This is a standard system call, documented in the Linux manual page for fcntl. Only one user can open the CA Device in `O_RDWR` mode. All other attempts to open the device in this mode will fail, and an error code will be returned.

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned.

On error -1 is returned, and the `errno` variable is set appropriately.

Generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.
