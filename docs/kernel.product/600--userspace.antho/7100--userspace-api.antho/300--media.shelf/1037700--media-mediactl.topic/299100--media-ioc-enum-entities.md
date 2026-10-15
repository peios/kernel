---
title: "ioctl MEDIA_IOC_ENUM_ENTITIES"
type: reference
description: "MEDIA_IOC_ENUM_ENTITIES - Enumerate entities and their properties"
---

<a id="rst-ioctl-media-ioc-enum-entities"></a>
<a id="rst-media-ioc-enum-entities"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: MC -->

<a id="rst-name"></a>

## Name

MEDIA_IOC_ENUM_ENTITIES - Enumerate entities and their properties

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-MEDIA_IOC_ENUM_ENTITIES"></a>

```c
MEDIA_IOC_ENUM_ENTITIES
```

`int ioctl(int fd, MEDIA_IOC_ENUM_ENTITIES, struct media_entity_desc *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to struct `media_entity_desc`.

<a id="rst-description"></a>

## Description

To query the attributes of an entity, applications set the id field of a struct `media_entity_desc` structure and call the MEDIA_IOC_ENUM_ENTITIES ioctl with a pointer to this structure. The driver fills the rest of the structure or returns an EINVAL error code when the id is invalid.

<a id="rst-media-ent-id-flag-next"></a>

Entities can be enumerated by or'ing the id with the `MEDIA_ENT_ID_FLAG_NEXT` flag. The driver will return information about the entity with the smallest id strictly larger than the requested one ('next entity'), or the `EINVAL` error code if there is none.

Entity IDs can be non-contiguous. Applications must *not* try to enumerate entities by calling MEDIA_IOC_ENUM_ENTITIES with increasing id's until they get an error.





<a id="c-media_entity_desc"></a>

```c
media_entity_desc
```

<!-- tabularcolumns: |p{1.5cm}|p{1.7cm}|p{1.6cm}|p{1.5cm}|p{10.6cm}| -->


<table>
<caption>struct media_entity_desc</caption>
<tbody>
<tr>
<td>


\__u32

</td>
<td>


`id`

</td>
<td>




</td>
<td>


Entity ID, set by the application. When the ID is or'ed with `MEDIA_ENT_ID_FLAG_NEXT`, the driver clears the flag and returns the first entity with a larger ID. Do not expect that the ID will always be the same for each instance of the device. In other words, do not hardcode entity IDs in an application.

</td>
</tr>
<tr>
<td>


char

</td>
<td>


`name`\[32\]

</td>
<td>




</td>
<td>


Entity name as an UTF-8 NULL-terminated string. This name must be unique within the media topology.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`type`

</td>
<td>




</td>
<td>


Entity type, see [media-entity-functions](<~kernel/userspace/userspace-api/media-mediactl/media-types#rst-media-entity-functions>) for details.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`revision`

</td>
<td>




</td>
<td>


Entity revision. Always zero (obsolete)

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




</td>
<td>


Entity flags, see [media-entity-flag](<~kernel/userspace/userspace-api/media-mediactl/media-types#rst-media-entity-flag>) for details.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`group_id`

</td>
<td>




</td>
<td>


Entity group ID. Always zero (obsolete)

</td>
</tr>
<tr>
<td>


\__u16

</td>
<td>


`pads`

</td>
<td>




</td>
<td>


Number of pads

</td>
</tr>
<tr>
<td>


\__u16

</td>
<td>


`links`

</td>
<td>




</td>
<td>


Total number of outbound links. Inbound links are not counted in this field.

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




</td>
<td>


Reserved for future extensions. Drivers and applications must set the array to zero.

</td>
</tr>
<tr>
<td>


union \{

</td>
<td colspan="3">


(anonymous)

</td>
</tr>
<tr>
<td>


struct

</td>
<td>


`dev`

</td>
<td>




</td>
<td>


Valid for (sub-)devices that create a single device node.

</td>
</tr>
<tr>
<td>




</td>
<td>


\__u32

</td>
<td>


`major`

</td>
<td>


Device node major number.

</td>
</tr>
<tr>
<td>




</td>
<td>


\__u32

</td>
<td>


`minor`

</td>
<td>


Device node minor number.

</td>
</tr>
<tr>
<td>


\__u8

</td>
<td>


`raw`\[184\]

</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


\}

</td>
<td colspan="3">




</td>
</tr>
</tbody>
</table>

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

- **EINVAL**

  The struct `media_entity_desc` `id` references a non-existing entity.
