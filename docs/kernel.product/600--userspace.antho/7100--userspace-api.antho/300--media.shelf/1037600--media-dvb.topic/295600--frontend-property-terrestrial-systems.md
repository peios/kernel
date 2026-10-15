---
title: "Properties used on terrestrial delivery systems"
type: reference
description: "The following parameters are valid for DVB-T:"
---

<a id="rst-properties-used-on-terrestrial-delivery-systems"></a>
<a id="rst-frontend-property-terrestrial-systems"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<a id="rst-dvb-t-delivery-system"></a>
<a id="rst-dvbt-params"></a>

## DVB-T delivery system

The following parameters are valid for DVB-T:

- [DTV_API_VERSION](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-api-version>)

- [DTV_DELIVERY_SYSTEM](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-delivery-system>)

- [DTV_TUNE](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-tune>)

- [DTV_CLEAR](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-clear>)

- [DTV_FREQUENCY](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-frequency>)

- [DTV_MODULATION](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-modulation>)

- [DTV_BANDWIDTH_HZ](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-bandwidth-hz>)

- [DTV_INVERSION](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-inversion>)

- [DTV_CODE_RATE_HP](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-code-rate-hp>)

- [DTV_CODE_RATE_LP](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-code-rate-lp>)

- [DTV_GUARD_INTERVAL](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-guard-interval>)

- [DTV_TRANSMISSION_MODE](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-transmission-mode>)

- [DTV_HIERARCHY](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-hierarchy>)

- [DTV_LNA](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-lna>)

In addition, the [DTV QoS statistics](<~kernel/userspace/userspace-api/media-dvb/frontend-stat-properties#rst-frontend-stat-properties>) are also valid.

<a id="rst-dvb-t2-delivery-system"></a>
<a id="rst-dvbt2-params"></a>

## DVB-T2 delivery system

DVB-T2 support is currently in the early stages of development, so expect that this section may grow and become more detailed with time.

The following parameters are valid for DVB-T2:

- [DTV_API_VERSION](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-api-version>)

- [DTV_DELIVERY_SYSTEM](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-delivery-system>)

- [DTV_TUNE](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-tune>)

- [DTV_CLEAR](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-clear>)

- [DTV_FREQUENCY](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-frequency>)

- [DTV_MODULATION](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-modulation>)

- [DTV_BANDWIDTH_HZ](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-bandwidth-hz>)

- [DTV_INVERSION](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-inversion>)

- [DTV_CODE_RATE_HP](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-code-rate-hp>)

- [DTV_CODE_RATE_LP](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-code-rate-lp>)

- [DTV_GUARD_INTERVAL](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-guard-interval>)

- [DTV_TRANSMISSION_MODE](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-transmission-mode>)

- [DTV_HIERARCHY](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-hierarchy>)

- [DTV_STREAM_ID](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-stream-id>)

- [DTV_LNA](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-lna>)

In addition, the [DTV QoS statistics](<~kernel/userspace/userspace-api/media-dvb/frontend-stat-properties#rst-frontend-stat-properties>) are also valid.

<a id="rst-isdb-t-delivery-system"></a>
<a id="rst-isdbt"></a>

## ISDB-T delivery system

This ISDB-T/ISDB-Tsb API extension should reflect all information needed to tune any ISDB-T/ISDB-Tsb hardware. Of course it is possible that some very sophisticated devices won't need certain parameters to tune.

The information given here should help application writers to know how to handle ISDB-T and ISDB-Tsb hardware using the Linux Digital TV API.

The details given here about ISDB-T and ISDB-Tsb are just enough to basically show the dependencies between the needed parameter values, but surely some information is left out. For more detailed information see the following documents:

ARIB STD-B31 - "Transmission System for Digital Terrestrial Television Broadcasting" and

ARIB TR-B14 - "Operational Guidelines for Digital Terrestrial Television Broadcasting".

In order to understand the ISDB specific parameters, one has to have some knowledge the channel structure in ISDB-T and ISDB-Tsb. I.e. it has to be known to the reader that an ISDB-T channel consists of 13 segments, that it can have up to 3 layer sharing those segments, and things like that.

The following parameters are valid for ISDB-T:

- [DTV_API_VERSION](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-api-version>)

- [DTV_DELIVERY_SYSTEM](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-delivery-system>)

- [DTV_TUNE](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-tune>)

- [DTV_CLEAR](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-clear>)

- [DTV_FREQUENCY](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-frequency>)

- [DTV_BANDWIDTH_HZ](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-bandwidth-hz>)

- [DTV_INVERSION](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-inversion>)

- [DTV_GUARD_INTERVAL](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-guard-interval>)

- [DTV_TRANSMISSION_MODE](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-transmission-mode>)

- [DTV_ISDBT_LAYER_ENABLED](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-isdbt-layer-enabled>)

- [DTV_ISDBT_PARTIAL_RECEPTION](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-isdbt-partial-reception>)

- [DTV_ISDBT_SOUND_BROADCASTING](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-isdbt-sound-broadcasting>)

- [DTV_ISDBT_SB_SUBCHANNEL_ID](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-isdbt-sb-subchannel-id>)

- [DTV_ISDBT_SB_SEGMENT_IDX](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-isdbt-sb-segment-idx>)

- [DTV_ISDBT_SB_SEGMENT_COUNT](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-isdbt-sb-segment-count>)

- [DTV_ISDBT_LAYERA_FEC](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-isdbt-layer-fec>)

- [DTV_ISDBT_LAYERA_MODULATION](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-isdbt-layer-modulation>)

- [DTV_ISDBT_LAYERA_SEGMENT_COUNT](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-isdbt-layer-segment-count>)

- [DTV_ISDBT_LAYERA_TIME_INTERLEAVING](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-isdbt-layer-time-interleaving>)

- [DTV_ISDBT_LAYERB_FEC](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-isdbt-layer-fec>)

- [DTV_ISDBT_LAYERB_MODULATION](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-isdbt-layer-modulation>)

- [DTV_ISDBT_LAYERB_SEGMENT_COUNT](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-isdbt-layer-segment-count>)

- [DTV_ISDBT_LAYERB_TIME_INTERLEAVING](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-isdbt-layer-time-interleaving>)

- [DTV_ISDBT_LAYERC_FEC](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-isdbt-layer-fec>)

- [DTV_ISDBT_LAYERC_MODULATION](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-isdbt-layer-modulation>)

- [DTV_ISDBT_LAYERC_SEGMENT_COUNT](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-isdbt-layer-segment-count>)

- [DTV_ISDBT_LAYERC_TIME_INTERLEAVING](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-isdbt-layer-time-interleaving>)

In addition, the [DTV QoS statistics](<~kernel/userspace/userspace-api/media-dvb/frontend-stat-properties#rst-frontend-stat-properties>) are also valid.

<a id="rst-atsc-delivery-system"></a>
<a id="rst-atsc-params"></a>

## ATSC delivery system

The following parameters are valid for ATSC:

- [DTV_API_VERSION](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-api-version>)

- [DTV_DELIVERY_SYSTEM](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-delivery-system>)

- [DTV_TUNE](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-tune>)

- [DTV_CLEAR](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-clear>)

- [DTV_FREQUENCY](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-frequency>)

- [DTV_MODULATION](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-modulation>)

- [DTV_BANDWIDTH_HZ](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-bandwidth-hz>)

In addition, the [DTV QoS statistics](<~kernel/userspace/userspace-api/media-dvb/frontend-stat-properties#rst-frontend-stat-properties>) are also valid.

<a id="rst-atsc-mh-delivery-system"></a>
<a id="rst-atscmh-params"></a>

## ATSC-MH delivery system

The following parameters are valid for ATSC-MH:

- [DTV_API_VERSION](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-api-version>)

- [DTV_DELIVERY_SYSTEM](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-delivery-system>)

- [DTV_TUNE](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-tune>)

- [DTV_CLEAR](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-clear>)

- [DTV_FREQUENCY](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-frequency>)

- [DTV_BANDWIDTH_HZ](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-bandwidth-hz>)

- [DTV_ATSCMH_FIC_VER](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-atscmh-fic-ver>)

- [DTV_ATSCMH_PARADE_ID](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-atscmh-parade-id>)

- [DTV_ATSCMH_NOG](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-atscmh-nog>)

- [DTV_ATSCMH_TNOG](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-atscmh-tnog>)

- [DTV_ATSCMH_SGN](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-atscmh-sgn>)

- [DTV_ATSCMH_PRC](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-atscmh-prc>)

- [DTV_ATSCMH_RS_FRAME_MODE](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-atscmh-rs-frame-mode>)

- [DTV_ATSCMH_RS_FRAME_ENSEMBLE](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-atscmh-rs-frame-ensemble>)

- [DTV_ATSCMH_RS_CODE_MODE_PRI](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-atscmh-rs-code-mode-pri>)

- [DTV_ATSCMH_RS_CODE_MODE_SEC](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-atscmh-rs-code-mode-sec>)

- [DTV_ATSCMH_SCCC_BLOCK_MODE](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-atscmh-sccc-block-mode>)

- [DTV_ATSCMH_SCCC_CODE_MODE_A](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-atscmh-sccc-code-mode-a>)

- [DTV_ATSCMH_SCCC_CODE_MODE_B](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-atscmh-sccc-code-mode-b>)

- [DTV_ATSCMH_SCCC_CODE_MODE_C](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-atscmh-sccc-code-mode-c>)

- [DTV_ATSCMH_SCCC_CODE_MODE_D](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-atscmh-sccc-code-mode-d>)

In addition, the [DTV QoS statistics](<~kernel/userspace/userspace-api/media-dvb/frontend-stat-properties#rst-frontend-stat-properties>) are also valid.

<a id="rst-dtmb-delivery-system"></a>
<a id="rst-dtmb-params"></a>

## DTMB delivery system

The following parameters are valid for DTMB:

- [DTV_API_VERSION](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-api-version>)

- [DTV_DELIVERY_SYSTEM](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-delivery-system>)

- [DTV_TUNE](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-tune>)

- [DTV_CLEAR](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-clear>)

- [DTV_FREQUENCY](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-frequency>)

- [DTV_MODULATION](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-modulation>)

- [DTV_BANDWIDTH_HZ](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-bandwidth-hz>)

- [DTV_INVERSION](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-inversion>)

- [DTV_INNER_FEC](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-inner-fec>)

- [DTV_GUARD_INTERVAL](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-guard-interval>)

- [DTV_TRANSMISSION_MODE](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-transmission-mode>)

- [DTV_INTERLEAVING](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-interleaving>)

- [DTV_LNA](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-lna>)

In addition, the [DTV QoS statistics](<~kernel/userspace/userspace-api/media-dvb/frontend-stat-properties#rst-frontend-stat-properties>) are also valid.
