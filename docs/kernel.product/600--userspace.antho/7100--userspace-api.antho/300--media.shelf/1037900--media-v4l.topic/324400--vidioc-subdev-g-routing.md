---
title: "ioctl VIDIOC_SUBDEV_G_ROUTING, VIDIOC_SUBDEV_S_ROUTING"
type: reference
description: "VIDIOC_SUBDEV_G_ROUTING - VIDIOC_SUBDEV_S_ROUTING - Get or set routing between streams of media pads in a media entity."
---

<a id="rst-ioctl-vidioc-subdev-g-routing-vidioc-subdev-s-routing"></a>
<a id="rst-vidioc-subdev-g-routing"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

VIDIOC_SUBDEV_G_ROUTING - VIDIOC_SUBDEV_S_ROUTING - Get or set routing between streams of media pads in a media entity.

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-VIDIOC_SUBDEV_G_ROUTING"></a>

```c
VIDIOC_SUBDEV_G_ROUTING
```

`int ioctl(int fd, VIDIOC_SUBDEV_G_ROUTING, struct v4l2_subdev_routing *argp)`





<a id="c-VIDIOC_SUBDEV_S_ROUTING"></a>

```c
VIDIOC_SUBDEV_S_ROUTING
```

`int ioctl(int fd, VIDIOC_SUBDEV_S_ROUTING, struct v4l2_subdev_routing *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by [open()](<~kernel/userspace/userspace-api/media-v4l/func-open#rst-func-open>).

- **`argp`**

  Pointer to struct `v4l2_subdev_routing`.

<a id="rst-description"></a>

## Description

These ioctls are used to get and set the routing in a media entity. The routing configuration determines the flows of data inside an entity.

Drivers report their current routing tables using the `VIDIOC_SUBDEV_G_ROUTING` ioctl and application may enable or disable routes with the `VIDIOC_SUBDEV_S_ROUTING` ioctl, by adding or removing routes and setting or clearing flags of the `flags` field of a struct `v4l2_subdev_route`. Similarly to `VIDIOC_SUBDEV_G_ROUTING`, also `VIDIOC_SUBDEV_S_ROUTING` returns the routes back to the user.

All stream configurations are reset when `VIDIOC_SUBDEV_S_ROUTING` is called. This means that the userspace must reconfigure all stream formats and selections after calling the ioctl with e.g. `VIDIOC_SUBDEV_S_FMT`.

Only subdevices which have both sink and source pads can support routing.

The `len_routes` field indicates the number of routes that can fit in the `routes` array allocated by userspace. It is set by applications for both ioctls to indicate how many routes the kernel can return, and is never modified by the kernel.

The `num_routes` field indicates the number of routes in the routing table. For `VIDIOC_SUBDEV_S_ROUTING`, it is set by userspace to the number of routes that the application stored in the `routes` array. For both ioctls, it is returned by the kernel and indicates how many routes are stored in the subdevice routing table. This may be smaller or larger than the value of `num_routes` set by the application for `VIDIOC_SUBDEV_S_ROUTING`, as drivers may adjust the requested routing table.

The kernel can return a `num_routes` value larger than `len_routes` from both ioctls. This indicates thare are more routes in the routing table than fits the `routes` array. In this case, the `routes` array is filled by the kernel with the first `len_routes` entries of the subdevice routing table. This is not considered to be an error, and the ioctl call succeeds. If the applications wants to retrieve the missing routes, it can issue a new `VIDIOC_SUBDEV_G_ROUTING` call with a large enough `routes` array.

`VIDIOC_SUBDEV_S_ROUTING` may return more routes than the user provided in `num_routes` field due to e.g. hardware properties.

<!-- tabularcolumns: |p{4.4cm}|p{4.4cm}|p{8.7cm}| -->





<a id="c-v4l2_subdev_routing"></a>

```c
v4l2_subdev_routing
```


<table>
<caption>struct v4l2_subdev_routing</caption>
<tbody>
<tr>
<td>


\__u32

</td>
<td>


`which`

</td>
<td>


Routing table to be accessed, from enum [v4l2_subdev_format_whence](<~kernel/userspace/userspace-api/media-v4l/vidioc-subdev-g-fmt#rst-v4l2-subdev-format-whence>).

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`len_routes`

</td>
<td>


The length of the array (as in memory reserved for the array)

</td>
</tr>
<tr>
<td>


struct `v4l2_subdev_route`

</td>
<td>


`routes[]`

</td>
<td>


Array of struct `v4l2_subdev_route` entries

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`num_routes`

</td>
<td>


Number of entries of the routes array

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`reserved`\[11\]

</td>
<td>


Reserved for future extensions. Applications and drivers must set the array to zero.

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{4.4cm}|p{4.4cm}|p{8.7cm}| -->





<a id="c-v4l2_subdev_route"></a>

```c
v4l2_subdev_route
```


<table>
<caption>struct v4l2_subdev_route</caption>
<tbody>
<tr>
<td>


\__u32

</td>
<td>


`sink_pad`

</td>
<td>


Sink pad number.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`sink_stream`

</td>
<td>


Sink pad stream number.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`source_pad`

</td>
<td>


Source pad number.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`source_stream`

</td>
<td>


Source pad stream number.

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


Route enable/disable flags [v4l2_subdev_routing_flags](<#rst-v4l2-subdev-routing-flags>).

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


Reserved for future extensions. Applications and drivers must set the array to zero.

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{6.6cm}|p{2.2cm}|p{8.7cm}| -->

<a id="rst-v4l2-subdev-routing-flags"></a>


<table>
<caption>enum v4l2_subdev_routing_flags</caption>
<tbody>
<tr>
<td>


V4L2_SUBDEV_ROUTE_FL_ACTIVE

</td>
<td>


0x0001

</td>
<td>


The route is enabled. Set by applications.

</td>
</tr>
</tbody>
</table>

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

- **EINVAL**

  The sink or source pad identifiers reference a non-existing pad or reference pads of different types (ie. the sink_pad identifiers refers to a source pad), the `which` field has an unsupported value, or, for `VIDIOC_SUBDEV_S_ROUTING`, the num_routes field set by the application is larger than the len_routes field value.

- **ENXIO**

  The application requested routes cannot be created or the state of the specified routes cannot be modified. Only returned for `VIDIOC_SUBDEV_S_ROUTING`.

- **E2BIG**

  The application provided `num_routes` for `VIDIOC_SUBDEV_S_ROUTING` is larger than the number of routes the driver can handle.
