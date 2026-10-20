---
title: "Generated watch ABI"
description: "Generated watch ABI: behaviour and implementation of the Peios kernel."
type: reference
---

<a id="trm-5-a-3-14"></a>

## `struct reg_notify_args` <a id="cite-lcs-abi.struct-reg-notify-args"></a>

Total size 8 bytes.

| Offset | Size | Type | Field |
|---|---|---|---|
| 0 | 4 | `__u32` | `filter` |
| 4 | 1 | `__u8` | `subtree` |
| 5 | 3 | `__u8``[3]` | `_pad` |
