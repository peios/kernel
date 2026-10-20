---
title: "VIA82xx mixer"
type: reference
description: "On many VIA82xx boards, the Input Source Select mixer control does not work. Setting it to Input2 on such boards will cause recording to hang, or fail with EIO (input/output error) via OSS emulation. This control should be left at Input1…"
---

<a id="rst-via82xx-mixer"></a>

On many VIA82xx boards, the `Input Source Select` mixer control does not work. Setting it to `Input2` on such boards will cause recording to hang, or fail with EIO (input/output error) via OSS emulation.  This control should be left at `Input1` for such cards.
