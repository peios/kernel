---
title: "FM Receiver Control Reference"
type: reference
description: "The FM Receiver (FM_RX) class includes controls for common features of FM Reception capable devices."
---

<a id="rst-fm-receiver-control-reference"></a>
<a id="rst-fm-rx-controls"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

The FM Receiver (FM_RX) class includes controls for common features of FM Reception capable devices.

<a id="rst-fm-rx-control-ids"></a>
<a id="rst-fm-rx-control-id"></a>

## FM_RX Control IDs

- **`V4L2_CID_FM_RX_CLASS (class)`**

  The FM_RX class descriptor. Calling [vidioc_queryctrl](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/vidioc-queryctrl.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>) for this control will return a description of this control class.

- **`V4L2_CID_RDS_RECEPTION (boolean)`**

  Enables/disables RDS reception by the radio tuner

- **`V4L2_CID_RDS_RX_PTY (integer)`**

  Gets RDS Programme Type field. This encodes up to 31 pre-defined programme types.

- **`V4L2_CID_RDS_RX_PS_NAME (string)`**

  Gets the Programme Service name (PS_NAME). It is intended for static display on a receiver. It is the primary aid to listeners in programme service identification and selection. In Annex E of [IEC 62106](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-iec62106>), the RDS specification, there is a full description of the correct character encoding for Programme Service name strings. Also from RDS specification, PS is usually a single eight character text. However, it is also possible to find receivers which can scroll strings sized as 8 x N characters. So, this control must be configured with steps of 8 characters. The result is it must always contain a string with size multiple of 8.

- **`V4L2_CID_RDS_RX_RADIO_TEXT (string)`**

  Gets the Radio Text info. It is a textual description of what is being broadcasted. RDS Radio Text can be applied when broadcaster wishes to transmit longer PS names, programme-related information or any other text. In these cases, RadioText can be used in addition to `V4L2_CID_RDS_RX_PS_NAME`. The encoding for Radio Text strings is also fully described in Annex E of [IEC 62106](<~kernel/userspace/userspace-api/media-v4l/biblio#rst-iec62106>). The length of Radio Text strings depends on which RDS Block is being used to transmit it, either 32 (2A block) or 64 (2B block). However, it is also possible to find receivers which can scroll strings sized as 32 x N or 64 x N characters. So, this control must be configured with steps of 32 or 64 characters. The result is it must always contain a string with size multiple of 32 or 64.

- **`V4L2_CID_RDS_RX_TRAFFIC_ANNOUNCEMENT (boolean)`**

  If set, then a traffic announcement is in progress.

- **`V4L2_CID_RDS_RX_TRAFFIC_PROGRAM (boolean)`**

  If set, then the tuned programme carries traffic announcements.

- **`V4L2_CID_RDS_RX_MUSIC_SPEECH (boolean)`**

  If set, then this channel broadcasts music. If cleared, then it broadcasts speech. If the transmitter doesn't make this distinction, then it will be set.

- **`V4L2_CID_TUNE_DEEMPHASIS (enum)`**

  Configures the de-emphasis value for reception. A de-emphasis filter is applied to the broadcast to accentuate the high audio frequencies. Depending on the region, a time constant of either 50 or 75 microseconds is used. The enum v4l2_deemphasis defines possible values for de-emphasis. They are:


<table>
<tbody>
<tr>
<td>


`V4L2_DEEMPHASIS_DISABLED`

</td>
<td>


No de-emphasis is applied.

</td>
</tr>
<tr>
<td>


`V4L2_DEEMPHASIS_50_uS`

</td>
<td>


A de-emphasis of 50 uS is used.

</td>
</tr>
<tr>
<td>


`V4L2_DEEMPHASIS_75_uS`

</td>
<td>


A de-emphasis of 75 uS is used.

</td>
</tr>
</tbody>
</table>
