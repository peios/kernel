---
title: "ioctl CEC_ADAP_G_CONNECTOR_INFO"
type: reference
description: "CEC_ADAP_G_CONNECTOR_INFO - Query HDMI connector information"
---

<a id="rst-ioctl-cec-adap-g-connector-info"></a>
<a id="rst-cec-adap-g-connector-info"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

<!--  -->

<!-- Copyright 2019 Google LLC -->

<!--  -->

<!-- c:namespace: CEC -->

<a id="rst-name"></a>

## Name

CEC_ADAP_G_CONNECTOR_INFO - Query HDMI connector information

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-CEC_ADAP_G_CONNECTOR_INFO"></a>

```c
CEC_ADAP_G_CONNECTOR_INFO
```

`int ioctl(int fd, CEC_ADAP_G_CONNECTOR_INFO, struct cec_connector_info *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

`argp`

<a id="rst-description"></a>

## Description

Using this ioctl an application can learn which HDMI connector this CEC device corresponds to. While calling this ioctl the application should provide a pointer to a cec_connector_info struct which will be populated by the kernel with the info provided by the adapter's driver. This ioctl is only available if the `CEC_CAP_CONNECTOR_INFO` capability is set.

<!-- tabularcolumns: |p{1.0cm}|p{4.4cm}|p{2.5cm}|p{9.2cm}| -->





<a id="c-cec_connector_info"></a>

```c
cec_connector_info
```


<table>
<caption>struct cec_connector_info</caption>
<tbody>
<tr>
<td>


\__u32

</td>
<td>


`type`

</td>
<td>


The type of connector this adapter is associated with.

</td>
</tr>
<tr>
<td>


union \{

</td>
<td colspan="2">


`(anonymous)`

</td>
</tr>
<tr>
<td>


`struct cec_drm_connector_info`

</td>
<td>


drm

</td>
<td>


[cec-drm-connector-info](<#rst-cec-drm-connector-info>)

</td>
</tr>
<tr>
<td>


\}

</td>
<td colspan="2">




</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{4.4cm}|p{2.5cm}|p{10.4cm}| -->

<a id="rst-connector-type"></a>


<table>
<caption>Connector types</caption>
<tbody>
<tr>
<td>


`CEC_CONNECTOR_TYPE_NO_CONNECTOR`

</td>
<td>


0

</td>
<td>


<a id="rst-cec-connector-type-no-connector"></a>

No connector is associated with the adapter/the information is not provided by the driver.

</td>
</tr>
<tr>
<td>


`CEC_CONNECTOR_TYPE_DRM`

</td>
<td>


1

</td>
<td>


<a id="rst-cec-connector-type-drm"></a>

Indicates that a DRM connector is associated with this adapter. Information about the connector can be found in [cec-drm-connector-info](<#rst-cec-drm-connector-info>).

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{4.4cm}|p{2.5cm}|p{10.4cm}| -->





<a id="c-cec_drm_connector_info"></a>

```c
cec_drm_connector_info
```

<a id="rst-cec-drm-connector-info"></a>


<table>
<caption>struct cec_drm_connector_info</caption>
<tbody>
<tr>
<td>


\__u32

</td>
<td>


`card_no`

</td>
<td>


<a id="rst-cec-drm-connector-type-card-no"></a>

DRM card number: the number from a card's path, e.g. 0 in case of /dev/card0.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`connector_id`

</td>
<td>


<a id="rst-cec-drm-connector-type-connector-id"></a>

DRM connector ID.

</td>
</tr>
</tbody>
</table>
