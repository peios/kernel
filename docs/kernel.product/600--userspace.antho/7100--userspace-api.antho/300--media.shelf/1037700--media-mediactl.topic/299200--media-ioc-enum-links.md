---
title: "ioctl MEDIA_IOC_ENUM_LINKS"
type: reference
description: "MEDIA_IOC_ENUM_LINKS - Enumerate all pads and links for a given entity"
---

<a id="rst-ioctl-media-ioc-enum-links"></a>
<a id="rst-media-ioc-enum-links"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: MC -->

<a id="rst-name"></a>

## Name

MEDIA_IOC_ENUM_LINKS - Enumerate all pads and links for a given entity

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-MEDIA_IOC_ENUM_LINKS"></a>

```c
MEDIA_IOC_ENUM_LINKS
```

`int ioctl(int fd, MEDIA_IOC_ENUM_LINKS, struct media_links_enum *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to struct `media_links_enum`.

<a id="rst-description"></a>

## Description

To enumerate pads and/or links for a given entity, applications set the entity field of a struct `media_links_enum` structure and initialize the struct `media_pad_desc` and struct `media_link_desc` structure arrays pointed by the `pads` and `links` fields. They then call the MEDIA_IOC_ENUM_LINKS ioctl with a pointer to this structure.

If the `pads` field is not NULL, the driver fills the `pads` array with information about the entity's pads. The array must have enough room to store all the entity's pads. The number of pads can be retrieved with [ioctl MEDIA_IOC_ENUM_ENTITIES](<~kernel/userspace/userspace-api/media-mediactl/media-ioc-enum-entities#rst-media-ioc-enum-entities>).

If the `links` field is not NULL, the driver fills the `links` array with information about the entity's outbound links. The array must have enough room to store all the entity's outbound links. The number of outbound links can be retrieved with [ioctl MEDIA_IOC_ENUM_ENTITIES](<~kernel/userspace/userspace-api/media-mediactl/media-ioc-enum-entities#rst-media-ioc-enum-entities>).

Only forward links that originate at one of the entity's source pads are returned during the enumeration process.





<a id="c-media_links_enum"></a>

```c
media_links_enum
```

<!-- tabularcolumns: |p{4.4cm}|p{4.4cm}|p{8.5cm}| -->


<table>
<caption>struct media_links_enum</caption>
<tbody>
<tr>
<td>


\__u32

</td>
<td>


`entity`

</td>
<td>


Entity id, set by the application.

</td>
</tr>
<tr>
<td>


struct `media_pad_desc`

</td>
<td>


\*`pads`

</td>
<td>


Pointer to a pads array allocated by the application. Ignored if NULL.

</td>
</tr>
<tr>
<td>


struct `media_link_desc`

</td>
<td>


\*`links`

</td>
<td>


Pointer to a links array allocated by the application. Ignored if NULL.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`reserved[4]`

</td>
<td>


Reserved for future extensions. Drivers and applications must set the array to zero.

</td>
</tr>
</tbody>
</table>





<a id="c-media_pad_desc"></a>

```c
media_pad_desc
```

<!-- tabularcolumns: |p{4.4cm}|p{4.4cm}|p{8.5cm}| -->


<table>
<caption>struct media_pad_desc</caption>
<tbody>
<tr>
<td>


\__u32

</td>
<td>


`entity`

</td>
<td>


ID of the entity this pad belongs to.

</td>
</tr>
<tr>
<td>


\__u16

</td>
<td>


`index`

</td>
<td>


Pad index, starts at 0.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`flags`

</td>
<td>


Pad flags, see [media-pad-flag](<~kernel/userspace/userspace-api/media-mediactl/media-types#rst-media-pad-flag>) for more details.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`reserved[2]`

</td>
<td>


Reserved for future extensions. Drivers and applications must set the array to zero.

</td>
</tr>
</tbody>
</table>





<a id="c-media_link_desc"></a>

```c
media_link_desc
```

<!-- tabularcolumns: |p{4.4cm}|p{4.4cm}|p{8.5cm}| -->


<table>
<caption>struct media_link_desc</caption>
<tbody>
<tr>
<td>


struct `media_pad_desc`

</td>
<td>


`source`

</td>
<td>


Pad at the origin of this link.

</td>
</tr>
<tr>
<td>


struct `media_pad_desc`

</td>
<td>


`sink`

</td>
<td>


Pad at the target of this link.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`flags`

</td>
<td>


Link flags, see [media-link-flag](<~kernel/userspace/userspace-api/media-mediactl/media-types#rst-media-link-flag>) for more details.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`reserved[2]`

</td>
<td>


Reserved for future extensions. Drivers and applications must set the array to zero.

</td>
</tr>
</tbody>
</table>

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

- **EINVAL**

  The struct `media_links_enum` `id` references a non-existing entity.
