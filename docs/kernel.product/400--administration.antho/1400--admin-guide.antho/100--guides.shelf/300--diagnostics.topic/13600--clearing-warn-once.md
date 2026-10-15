---
title: "Clearing WARN_ONCE"
type: reference
description: "WARN_ONCE / WARN_ON_ONCE / printk_once only emit a message once."
---

<a id="rst-clearing-warn-once"></a>

WARN_ONCE / WARN_ON_ONCE / printk_once only emit a message once.

echo 1 &gt; /sys/kernel/debug/clear_warn_once

clears the state and allows the warnings to print once again. This can be useful after test suite runs to reproduce problems.
