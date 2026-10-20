---
title: "Event ring and delivery"
description: "Event ring and delivery: behaviour and implementation of the Peios kernel."
type: reference
---

<a id="trm-6-7"></a>

Every real evaluation — a published forest judged the traversal, or a
fail-closed drop — appends one `struct peios_ntfe_event` to a bounded
ring. <a id="cite-ntfe-stream.each-evaluation-appends-one-event"></a> Permissive traversals emit nothing: there is no decision to
attribute, and the status tells that story instead. <a id="cite-ntfe-stream.permissive-emits-no-event"></a> A packet answered by
its flow's cached sentence emits nothing either: there was no
evaluation, and `flow_cached` counts it. <a id="cite-ntfe-stream.cached-sentence-emits-no-event"></a> The layouts are in [NTFE ABI Reference](<~kernel/userspace/native/ntfe/generated-device-abi#trm-6-a>); this
page is what they mean.

<a id="trm-6-7-2"></a>

## The ring and its reader

The ring holds 4096 events under a spinlock (`irqsave`: emission happens
in softirq). <a id="cite-ntfe-stream.ring-4096-events-irqsave-lock"></a> A full ring overwrites the **oldest** event and counts the
loss in `events_dropped` — the honesty rule: a slow reader loses data
and is told so, in the status and by the gap in sequence numbers. <a id="cite-ntfe-stream.full-ring-overwrites-oldest"></a>

`/dev/peios-ntfe` is a misc device, mode 0600. <a id="cite-ntfe-stream.device-misc-mode-0600"></a> Any number of files may
be open on it, because the status and dump ioctls are asked by tools
while a viewer holds the stream, <a id="cite-ntfe-stream.device-many-openers"></a> but the ring has one drain: the first
file to `read()` claims it until it closes, and another file's `read()`
returns `-EBUSY` meanwhile. <a id="cite-ntfe-stream.first-reader-claims-ring-others-ebusy"></a> `read()` returns whole
records only, up to 64 per call, <a id="cite-ntfe-stream.read-whole-records-up-to-64"></a> and blocks on an empty ring unless
`O_NONBLOCK`; <a id="cite-ntfe-stream.read-blocks-unless-nonblock"></a> `poll()` raises `POLLIN` when events wait. <a id="cite-ntfe-stream.poll-pollin-when-events-wait"></a> A reader that
reconnects resumes from whatever the ring still holds, and catches the
gap from the sequence numbers. <a id="cite-ntfe-stream.reconnect-resumes-from-ring"></a>

The viewer daemon reads it with a small wrinkle worth knowing about: its
own HTTP responses to a viewer are judged traffic too, so every event it
sends produces another event — a feedback loop. pnpd hides events about
its own TCP port from what it serves and counts them (`own_verdicts_hidden`),
which is the same treatment the wire tap gives its own frames. <a id="cite-ntfe-stream.viewer-hides-own-port-events"></a>

## Related explanations

- [Event records and status semantics](<~kernel/userspace/native/ntfe/event-records-and-status-semantics>)
