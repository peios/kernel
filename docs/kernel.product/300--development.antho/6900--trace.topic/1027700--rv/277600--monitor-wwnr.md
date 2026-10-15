---
title: "Monitor wwnr"
type: reference
description: "Name: wwrn - wakeup while not running"
---

<a id="rst-monitor-wwnr"></a>

- Name: wwrn - wakeup while not running

- Type: per-task deterministic automaton

- Author: Daniel Bristot de Oliveira &lt;[bristot@kernel.org](<mailto:bristot@kernel.org>)&gt;

<a id="rst-description"></a>

## Description

This is a per-task sample monitor, with the following definition:



```text
             |
             |
             v
  wakeup   +-------------+
+--------- |             |
|          | not_running |
+--------> |             | <+
           +-------------+  |
             |              |
             | switch_in    | switch_out
             v              |
           +-------------+  |
           |   running   | -+
           +-------------+
```

This model is broken, the reason is that a task can be running in the processor without being set as RUNNABLE. Think about a task about to sleep:



```text
1:      set_current_state(TASK_UNINTERRUPTIBLE);
2:      schedule();
```

And then imagine an IRQ happening in between the lines one and two, waking the task up. BOOM, the wakeup will happen while the task is running.

- Why do we need this model, so?

- To test the reactors.

<a id="rst-specification"></a>

## Specification

Grapviz Dot file in tools/verification/models/wwnr.dot
