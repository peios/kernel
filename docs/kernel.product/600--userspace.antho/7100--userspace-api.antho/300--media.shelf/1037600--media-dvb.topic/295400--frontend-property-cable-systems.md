---
title: "Properties used on cable delivery systems"
type: reference
description: "The DVB-C Annex-A is the widely used cable standard. Transmission uses QAM modulation."
---

<a id="rst-properties-used-on-cable-delivery-systems"></a>
<a id="rst-frontend-property-cable-systems"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<a id="rst-dvb-c-delivery-system"></a>
<a id="rst-dvbc-params"></a>

## DVB-C delivery system

The DVB-C Annex-A is the widely used cable standard. Transmission uses QAM modulation.

The DVB-C Annex-C is optimized for 6MHz, and is used in Japan. It supports a subset of the Annex A modulation types, and a roll-off of 0.13, instead of 0.15

The following parameters are valid for DVB-C Annex A/C:

- [DTV_API_VERSION](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-api-version>)

- [DTV_DELIVERY_SYSTEM](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-delivery-system>)

- [DTV_TUNE](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-tune>)

- [DTV_CLEAR](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-clear>)

- [DTV_FREQUENCY](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-frequency>)

- [DTV_MODULATION](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-modulation>)

- [DTV_INVERSION](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-inversion>)

- [DTV_SYMBOL_RATE](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-symbol-rate>)

- [DTV_INNER_FEC](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-inner-fec>)

- [DTV_LNA](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-lna>)

In addition, the [DTV QoS statistics](<~kernel/userspace/userspace-api/media-dvb/frontend-stat-properties#rst-frontend-stat-properties>) are also valid.

<a id="rst-dvb-c-annex-b-delivery-system"></a>
<a id="rst-dvbc-annex-b-params"></a>

## DVB-C Annex B delivery system

The DVB-C Annex-B is only used on a few Countries like the United States.

The following parameters are valid for DVB-C Annex B:

- [DTV_API_VERSION](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-api-version>)

- [DTV_DELIVERY_SYSTEM](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-delivery-system>)

- [DTV_TUNE](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-tune>)

- [DTV_CLEAR](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-clear>)

- [DTV_FREQUENCY](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-frequency>)

- [DTV_MODULATION](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-modulation>)

- [DTV_INVERSION](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-inversion>)

- [DTV_LNA](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-lna>)

In addition, the [DTV QoS statistics](<~kernel/userspace/userspace-api/media-dvb/frontend-stat-properties#rst-frontend-stat-properties>) are also valid.
