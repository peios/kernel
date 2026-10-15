---
title: "Frontend type"
type: reference
description: "For historical reasons, frontend types are named by the type of modulation used in transmission. The fontend types are given by fe_type_t type, defined as:"
---

<a id="rst-frontend-type"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

For historical reasons, frontend types are named by the type of modulation used in transmission. The fontend types are given by fe_type_t type, defined as:





<a id="c-fe_type"></a>

```c
fe_type
```

<!-- tabularcolumns: |p{6.6cm}|p{2.2cm}|p{8.5cm}| -->


<table>
<caption>Frontend types</caption>
<thead>
<tr>
<th>


fe_type

</th>
<th>


Description

</th>
<th>


[DTV_DELIVERY_SYSTEM](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-delivery-system>) equivalent type

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


<a id="rst-fe-qpsk"></a>

`FE_QPSK`

</td>
<td>


For DVB-S standard

</td>
<td>


`SYS_DVBS`

</td>
</tr>
<tr>
<td>


<a id="rst-fe-qam"></a>

`FE_QAM`

</td>
<td>


For DVB-C annex A standard

</td>
<td>


`SYS_DVBC_ANNEX_A`

</td>
</tr>
<tr>
<td>


<a id="rst-fe-ofdm"></a>

`FE_OFDM`

</td>
<td>


For DVB-T standard

</td>
<td>


`SYS_DVBT`

</td>
</tr>
<tr>
<td>


<a id="rst-fe-atsc"></a>

`FE_ATSC`

</td>
<td>


For ATSC standard (terrestrial) or for DVB-C Annex B (cable) used in US.

</td>
<td>


`SYS_ATSC` (terrestrial) or `SYS_DVBC_ANNEX_B` (cable)

</td>
</tr>
</tbody>
</table>

Newer formats like DVB-S2, ISDB-T, ISDB-S and DVB-T2 are not described at the above, as they're supported via the new [FE_GET_PROPERTY/FE_GET_SET_PROPERTY](<~kernel/userspace/userspace-api/media-dvb/fe-get-property#rst-fe-get-property>) ioctl's, using the [DTV_DELIVERY_SYSTEM](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-delivery-system>) parameter.

In the old days, struct `dvb_frontend_info` used to contain `fe_type_t` field to indicate the delivery systems, filled with either `FE_QPSK, FE_QAM, FE_OFDM` or `FE_ATSC`. While this is still filled to keep backward compatibility, the usage of this field is deprecated, as it can report just one delivery system, but some devices support multiple delivery systems. Please use [DTV_ENUM_DELSYS](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-enum-delsys>) instead.

On devices that support multiple delivery systems, struct `dvb_frontend_info`::`fe_type_t` is filled with the currently standard, as selected by the last call to [FE_SET_PROPERTY](<~kernel/userspace/userspace-api/media-dvb/fe-get-property#rst-fe-get-property>) using the [DTV_DELIVERY_SYSTEM](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-delivery-system>) property.
