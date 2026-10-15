---
title: "Common selection definitions"
type: reference
description: "While the V4L2 selection API <selection-api> and V4L2 subdev selection APIs <v4l2-subdev-selections> are very similar, there's one fundamental difference between the two. On sub-device API, the selection rectangle refers to the media bus…"
---

<a id="rst-common-selection-definitions"></a>
<a id="rst-v4l2-selections-common"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

While the [V4L2 selection API](<~kernel/userspace/userspace-api/media-v4l/selection-api#rst-selection-api>) and [V4L2 subdev selection APIs](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/dev-subdev.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>) are very similar, there's one fundamental difference between the two. On sub-device API, the selection rectangle refers to the media bus format, and is bound to a sub-device's pad. On the V4L2 interface the selection rectangles refer to the in-memory pixel format.

This section defines the common definitions of the selection interfaces on the two APIs.

- [v4l2-selection-targets](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/v4l2-selection-targets.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>)
- [v4l2-selection-flags](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/v4l2-selection-flags.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>)
