---
title: "Legacy DVB MPEG Decoder APIs"
type: reference
description: "This API has originally been designed for DVB only and is therefore limited to the legacy_dvb_decoder_formats used in such digital TV-broadcastsystems."
---

<a id="rst-legacy-dvb-mpeg-decoder-apis"></a>
<a id="rst-legacy-dvb-decoder-api"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later OR GPL-2.0 -->

<a id="rst-general-notes"></a>
<a id="rst-legacy-dvb-decoder-notes"></a>

## General Notes

This API has originally been designed for DVB only and is therefore limited to the [Data Formats](<#rst-legacy-dvb-decoder-formats>) used in such digital TV-broadcastsystems.

To circumvent this limitations the more versatile [V4L2](<~kernel/userspace/userspace-api/media-v4l/v4l2#rst-v4l2spec>) API has been designed. Which replaces this part of the DVB API.

Nevertheless there have been projects build around this API. To ensure compatibility this API is kept as it is.

> [!NOTE]
>
> Do **not** use this API in new drivers\!
>
> For audio and video use the [V4L2](<~kernel/userspace/userspace-api/media-v4l/v4l2#rst-v4l2spec>) and ALSA APIs.
>
> Pipelines should be set up using the [Media Controller API](<~kernel/userspace/userspace-api/media-mediactl/media-controller#rst-media-controller>).

Practically the decoders seem to be treated differently. The application typically knows which decoder is in use or it is specially written for one decoder type. Querying capabilities are rarely used because they are already known.

<a id="rst-data-formats"></a>
<a id="rst-legacy-dvb-decoder-formats"></a>

## Data Formats

The API has been designed for DVB and compatible broadcastsystems. Because of that fact the only supported data formats are ISO/IEC 13818-1 compatible MPEG streams. The supported payloads may vary depending on the used decoder.

Timestamps are always MPEG PTS as defined in ITU T-REC-H.222.0 / ISO/IEC 13818-1, if not otherwise noted.

For storing recordings typically TS streams are used, in lesser extent PES. Both variants are commonly accepted for playback, but it may be driver dependent.

<a id="rst-table-of-contents"></a>

## Table of Contents

- [DVB Video Device](<~kernel/userspace/userspace-api/media-dvb/legacy-dvb-video>)
- [DVB Audio Device](<~kernel/userspace/userspace-api/media-dvb/legacy-dvb-audio>)
- [DVB OSD Device](<~kernel/userspace/userspace-api/media-dvb/legacy-dvb-osd>)
