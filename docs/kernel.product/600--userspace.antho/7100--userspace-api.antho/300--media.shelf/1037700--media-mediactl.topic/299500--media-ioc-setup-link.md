---
title: "ioctl MEDIA_IOC_SETUP_LINK"
type: reference
description: "MEDIA_IOC_SETUP_LINK - Modify the properties of a link"
---

<a id="rst-ioctl-media-ioc-setup-link"></a>
<a id="rst-media-ioc-setup-link"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: MC -->

<a id="rst-name"></a>

## Name

MEDIA_IOC_SETUP_LINK - Modify the properties of a link

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-MEDIA_IOC_SETUP_LINK"></a>

```c
MEDIA_IOC_SETUP_LINK
```

`int ioctl(int fd, MEDIA_IOC_SETUP_LINK, struct media_link_desc *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to struct `media_link_desc`.

<a id="rst-description"></a>

## Description

To change link properties applications fill a struct `media_link_desc` with link identification information (source and sink pad) and the new requested link flags. They then call the MEDIA_IOC_SETUP_LINK ioctl with a pointer to that structure.

The only configurable property is the `ENABLED` link flag to enable/disable a link. Links marked with the `IMMUTABLE` link flag can not be enabled or disabled.

Link configuration has no side effect on other links. If an enabled link at the sink pad prevents the link from being enabled, the driver returns with an `EBUSY` error code.

Only links marked with the `DYNAMIC` link flag can be enabled/disabled while streaming media data. Attempting to enable or disable a streaming non-dynamic link will return an `EBUSY` error code.

If the specified link can't be found the driver returns with an `EINVAL` error code.

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

- **EINVAL**

  The struct `media_link_desc` references a non-existing link, or the link is immutable and an attempt to modify its configuration was made.
