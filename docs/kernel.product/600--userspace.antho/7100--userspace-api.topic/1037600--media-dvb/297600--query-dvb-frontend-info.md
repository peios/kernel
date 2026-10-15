---
title: "Querying frontend information"
type: reference
description: "Usually, the first thing to do when the frontend is opened is to check the frontend capabilities. This is done using FE_GET_INFO. This ioctl will enumerate the Digital TV API version and other characteristics about the frontend, and can be…"
---

<a id="rst-querying-frontend-information"></a>
<a id="rst-query-dvb-frontend-info"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

Usually, the first thing to do when the frontend is opened is to check the frontend capabilities. This is done using [ioctl FE_GET_INFO](<~kernel/userspace/userspace-api/media-dvb/fe-get-info#rst-fe-get-info>). This ioctl will enumerate the Digital TV API version and other characteristics about the frontend, and can be opened either in read only or read/write mode.
