---
title: "Querying frontend status and statistics"
type: reference
description: "Once FE_SET_PROPERTY <FE_GET_PROPERTY> is called, the frontend will run a kernel thread that will periodically check for the tuner lock status and provide statistics about the quality of the signal."
---

<a id="rst-querying-frontend-status-and-statistics"></a>
<a id="rst-dvb-fe-read-status"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

Once [FE_SET_PROPERTY](<~kernel/userspace/userspace-api/media-dvb/fe-get-property#rst-fe-get-property>) is called, the frontend will run a kernel thread that will periodically check for the tuner lock status and provide statistics about the quality of the signal.

The information about the frontend tuner locking status can be queried using [ioctl FE_READ_STATUS](<~kernel/userspace/userspace-api/media-dvb/fe-read-status#rst-fe-read-status>).

Signal statistics are provided via [ioctl FE_SET_PROPERTY, FE_GET_PROPERTY](<~kernel/userspace/userspace-api/media-dvb/fe-get-property#rst-fe-get-property>).

> [!NOTE]
>
> Most statistics require the demodulator to be fully locked (e. g. with `FE_HAS_LOCK <fe_status>` bit set). See [Frontend statistics indicators](<~kernel/userspace/userspace-api/media-dvb/frontend-stat-properties#rst-frontend-stat-properties>) for more details.
