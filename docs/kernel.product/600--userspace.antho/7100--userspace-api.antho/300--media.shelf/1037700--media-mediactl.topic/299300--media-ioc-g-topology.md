---
title: "ioctl MEDIA_IOC_G_TOPOLOGY"
type: reference
description: "MEDIA_IOC_G_TOPOLOGY - Enumerate the graph topology and graph element properties"
---

<a id="rst-ioctl-media-ioc-g-topology"></a>
<a id="rst-media-ioc-g-topology"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: MC -->

<a id="rst-name"></a>

## Name

MEDIA_IOC_G_TOPOLOGY - Enumerate the graph topology and graph element properties

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-MEDIA_IOC_G_TOPOLOGY"></a>

```c
MEDIA_IOC_G_TOPOLOGY
```

`int ioctl(int fd, MEDIA_IOC_G_TOPOLOGY, struct media_v2_topology *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to struct `media_v2_topology`.

<a id="rst-description"></a>

## Description

The typical usage of this ioctl is to call it twice. On the first call, the structure defined at struct `media_v2_topology` should be zeroed. At return, if no errors happen, this ioctl will return the `topology_version` and the total number of entities, interfaces, pads and links.

Before the second call, the userspace should allocate arrays to store the graph elements that are desired, putting the pointers to them at the ptr_entities, ptr_interfaces, ptr_links and/or ptr_pads, keeping the other values untouched.

If the `topology_version` remains the same, the ioctl should fill the desired arrays with the media graph elements.

<!-- tabularcolumns: |p{1.6cm}|p{3.4cm}|p{12.3cm}| -->





<a id="c-media_v2_topology"></a>

```c
media_v2_topology
```


<table>
<caption>struct media_v2_topology</caption>
<tbody>
<tr>
<td>


\__u64

</td>
<td>


`topology_version`

</td>
<td>


Version of the media graph topology. When the graph is created, this field starts with zero. Every time a graph element is added or removed, this field is incremented.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`num_entities`

</td>
<td>


Number of entities in the graph

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`reserved1`

</td>
<td>


Applications and drivers shall set this to 0.

</td>
</tr>
<tr>
<td>


\__u64

</td>
<td>


`ptr_entities`

</td>
<td>


A pointer to a memory area where the entities array will be stored, converted to a 64-bits integer. It can be zero. if zero, the ioctl won't store the entities. It will just update `num_entities`

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`num_interfaces`

</td>
<td>


Number of interfaces in the graph

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`reserved2`

</td>
<td>


Applications and drivers shall set this to 0.

</td>
</tr>
<tr>
<td>


\__u64

</td>
<td>


`ptr_interfaces`

</td>
<td>


A pointer to a memory area where the interfaces array will be stored, converted to a 64-bits integer. It can be zero. if zero, the ioctl won't store the interfaces. It will just update `num_interfaces`

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`num_pads`

</td>
<td>


Total number of pads in the graph

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`reserved3`

</td>
<td>


Applications and drivers shall set this to 0.

</td>
</tr>
<tr>
<td>


\__u64

</td>
<td>


`ptr_pads`

</td>
<td>


A pointer to a memory area where the pads array will be stored, converted to a 64-bits integer. It can be zero. if zero, the ioctl won't store the pads. It will just update `num_pads`

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`num_links`

</td>
<td>


Total number of data and interface links in the graph

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`reserved4`

</td>
<td>


Applications and drivers shall set this to 0.

</td>
</tr>
<tr>
<td>


\__u64

</td>
<td>


`ptr_links`

</td>
<td>


A pointer to a memory area where the links array will be stored, converted to a 64-bits integer. It can be zero. if zero, the ioctl won't store the links. It will just update `num_links`

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{1.6cm}|p{3.2cm}|p{12.5cm}| -->





<a id="c-media_v2_entity"></a>

```c
media_v2_entity
```


<table>
<caption>struct media_v2_entity</caption>
<tbody>
<tr>
<td>


\__u32

</td>
<td>


`id`

</td>
<td>


Unique ID for the entity. Do not expect that the ID will always be the same for each instance of the device. In other words, do not hardcode entity IDs in an application.

</td>
</tr>
<tr>
<td>


char

</td>
<td>


`name`\[64\]

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


`function`

</td>
<td>


Entity main function, see [media-entity-functions](<~kernel/userspace/userspace-api/media-mediactl/media-types#rst-media-entity-functions>) for details.

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


Entity flags, see [media-entity-flag](<~kernel/userspace/userspace-api/media-mediactl/media-types#rst-media-entity-flag>) for details. Only valid if `MEDIA_V2_ENTITY_HAS_FLAGS(media_version)` returns true. The `media_version` is defined in struct `media_device_info` and can be retrieved using [ioctl MEDIA_IOC_DEVICE_INFO](<~kernel/userspace/userspace-api/media-mediactl/media-ioc-device-info#rst-media-ioc-device-info>).

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`reserved`\[5\]

</td>
<td>


Reserved for future extensions. Drivers and applications must set this array to zero.

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{1.6cm}|p{3.2cm}|p{12.5cm}| -->





<a id="c-media_v2_interface"></a>

```c
media_v2_interface
```


<table>
<caption>struct media_v2_interface</caption>
<tbody>
<tr>
<td>


\__u32

</td>
<td>


`id`

</td>
<td>


Unique ID for the interface. Do not expect that the ID will always be the same for each instance of the device. In other words, do not hardcode interface IDs in an application.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`intf_type`

</td>
<td>


Interface type, see [media-intf-type](<~kernel/userspace/userspace-api/media-mediactl/media-types#rst-media-intf-type>) for details.

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


Interface flags. Currently unused.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`reserved`\[9\]

</td>
<td>


Reserved for future extensions. Drivers and applications must set this array to zero.

</td>
</tr>
<tr>
<td>


struct media_v2_intf_devnode

</td>
<td>


`devnode`

</td>
<td>


Used only for device node interfaces. See `media_v2_intf_devnode` for details.

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{1.6cm}|p{3.2cm}|p{12.5cm}| -->





<a id="c-media_v2_intf_devnode"></a>

```c
media_v2_intf_devnode
```


<table>
<caption>struct media_v2_intf_devnode</caption>
<tbody>
<tr>
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


\__u32

</td>
<td>


`minor`

</td>
<td>


Device node minor number.

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{1.6cm}|p{3.2cm}|p{12.5cm}| -->





<a id="c-media_v2_pad"></a>

```c
media_v2_pad
```


<table>
<caption>struct media_v2_pad</caption>
<tbody>
<tr>
<td>


\__u32

</td>
<td>


`id`

</td>
<td>


Unique ID for the pad. Do not expect that the ID will always be the same for each instance of the device. In other words, do not hardcode pad IDs in an application.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`entity_id`

</td>
<td>


Unique ID for the entity where this pad belongs.

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


`index`

</td>
<td>


Pad index, starts at 0. Only valid if `MEDIA_V2_PAD_HAS_INDEX(media_version)` returns true. The `media_version` is defined in struct `media_device_info` and can be retrieved using [ioctl MEDIA_IOC_DEVICE_INFO](<~kernel/userspace/userspace-api/media-mediactl/media-ioc-device-info#rst-media-ioc-device-info>).

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`reserved`\[4\]

</td>
<td>


Reserved for future extensions. Drivers and applications must set this array to zero.

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{1.6cm}|p{3.2cm}|p{12.5cm}| -->





<a id="c-media_v2_link"></a>

```c
media_v2_link
```


<table>
<caption>struct media_v2_link</caption>
<tbody>
<tr>
<td>


\__u32

</td>
<td>


`id`

</td>
<td>


Unique ID for the link. Do not expect that the ID will always be the same for each instance of the device. In other words, do not hardcode link IDs in an application.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`source_id`

</td>
<td>


On pad to pad links: unique ID for the source pad.

On interface to entity links: unique ID for the interface.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`sink_id`

</td>
<td>


On pad to pad links: unique ID for the sink pad.

On interface to entity links: unique ID for the entity.

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


`reserved`\[6\]

</td>
<td>


Reserved for future extensions. Drivers and applications must set this array to zero.

</td>
</tr>
</tbody>
</table>

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

- **ENOSPC**

  This is returned when either one or more of the num_entities, num_interfaces, num_links or num_pads are non-zero and are smaller than the actual number of elements inside the graph. This may happen if the `topology_version` changed when compared to the last time this ioctl was called. Userspace should usually free the area for the pointers, zero the struct elements and call this ioctl again.
