---
title: "Request Dispatch"
description: "The RSI is multiplexed — request ids and matching, the single deadline covering three waits, and requests with no caller."
type: reference
---

<a id="trm-5-8-3"></a>

The RSI is multiplexed. LCS sends concurrent requests tagged with
request ids and matches responses back to the kernel threads waiting on
them. A source may process requests in any order. <a id="cite-source.dispatch.responses-may-arrive-in-any-order"></a>

Request ids are allocated per connection, strictly increasing, and
**never reused** while the connection lives — including after a
timeout. <a id="cite-source.dispatch.request-ids-never-reused"></a>

The id is allocated inside the queue lock, after the in-flight limit has
been checked, so a caller queued waiting for a slot does not hold one
yet. <a id="cite-source.dispatch.id-allocated-after-the-limit-check"></a>

`MaxConcurrentRSIRequests`, default 256, bounds how many requests may
be dispatched and awaiting a response at once. <a id="cite-source.dispatch.max-concurrent-bounds-in-flight"></a> It is back-pressure for
a slow source.

<a id="trm-5-8-3-1"></a>

## One deadline covers three waits

`RequestTimeoutMs`, default 30 seconds, is measured from the point a
kernel operation first attempts to **reserve an in-flight slot**, after
local validation and access checks have already passed. One deadline is
computed there and reused for all three legs: waiting for a slot,
waiting for the source to read the queued request, and waiting for the
response. <a id="cite-source.dispatch.one-deadline-covers-three-waits"></a>

If the deadline expires before a slot is reserved, the caller gets
`ETIMEDOUT` and **no request is sent**. <a id="cite-source.dispatch.timeout-before-a-slot-sends-nothing"></a>

If it expires after dispatch, the caller gets `ETIMEDOUT` and
late-response handling applies ([Failure and Late Responses](<~kernel/internals/lcs/sources/failure-and-late-responses#trm-5-8-5>)). <a id="cite-source.dispatch.timeout-after-dispatch-is-etimedout"></a>

The deadline is checked before admission is attempted, not only after a
contention round is lost. <a id="cite-source.dispatch.deadline-checked-before-admission"></a> It used to be the latter, which meant a request
finding a slot immediately free was dispatched with an already-expired
deadline and timed out in the wait leg instead — so the rule above held
only under contention, the one case where it is hardest to observe.

<a id="trm-5-8-3-2"></a>

## Timed-out requests keep their slot

For every dispatched request LCS keeps a **request record** until a
matching response is processed or the connection is torn down. <a id="cite-source.dispatch.record-kept-until-response-or-teardown"></a>

The record holds the request id, the operation code, the transaction
id, the key GUID it concerns, the runtime limits in force, and any
retained effect the kernel will need if the source later reports
success. <a id="cite-source.dispatch.record-contents"></a>

When the deadline expires after dispatch, LCS detaches the waiting
caller from the record and returns `ETIMEDOUT`. <a id="cite-source.dispatch.timeout-detaches-caller-from-record"></a>

A signal that interrupts the wait after dispatch detaches the caller
the same way, and the call fails with `EINTR` or is restarted. As after
a timeout, the source may still apply the request when it answers. A
response that completed before the caller could be detached wins: the
caller gets that response's result, with the signal still pending. <a id="cite-source.dispatch.completion-beats-a-signal"></a>

**The record stays in the in-flight table and keeps counting against
`MaxConcurrentRSIRequests`.** A timeout does not free a slot; only a
response or a teardown does. <a id="cite-source.dispatch.timeout-does-not-free-a-slot"></a>

A source that accumulates timed-out requests can therefore exhaust its
own in-flight slots until it answers or disconnects. That is the
intended shape: a source that stops answering stops being usable.

<a id="trm-5-8-3-3"></a>

## Requests with no caller

LCS dispatches some requests with nobody waiting: `RSI_DROP_KEY` after
the last fd to an orphaned key closes ([Deletion and Orphans](<~kernel/internals/lcs/data-model/deletion-and-orphans#trm-5-2-9>)), and
`RSI_ABORT_TRANSACTION` cleaning up source transaction state. <a id="cite-source.dispatch.callerless-requests-are-dispatched"></a>

Such a record occupies an in-flight slot and is retained like any
other, and its response is validated normally and released normally. <a id="cite-source.dispatch.callerless-record-occupies-a-slot"></a>

But it is **not** a late response, and the retained-effect recovery
rules do not apply to it merely because nobody is waiting. <a id="cite-source.dispatch.callerless-is-not-a-late-response"></a>

The kernel tracks the difference explicitly, with two booleans: whether
a waiter is attached now, and whether one was ever attached. A record
that never had a caller is not a timed-out request; only one whose
caller was detached after its deadline is. <a id="cite-source.dispatch.timed-out-means-caller-detached-after-deadline"></a>

This is load-bearing rather than pedantic. `RSI_DROP_KEY` is a mutating
operation, so without the distinction a perfectly ordinary answer to a
caller-less cleanup request would look like a mutation the kernel could
not account for, and would tear the source down.

<a id="trm-5-8-3-4"></a>

## The channel

`/dev/pkm_registry` is message-oriented. One `read()` returns exactly
one complete request; a buffer too small for the next one returns
`EMSGSIZE` **without consuming it**. <a id="cite-source.dispatch.read-returns-one-request-or-emsgsize"></a>

An empty queue blocks, or returns `EAGAIN` under `O_NONBLOCK`, or
returns 0 if the fd is closing. <a id="cite-source.dispatch.empty-queue-blocks-or-eagain"></a>

One `write()` submits exactly one complete response, and its length
must equal the response's own `total_len` exactly. <a id="cite-source.dispatch.write-submits-one-response-of-exact-length"></a>

`poll` reports the fd readable when a request is queued, writable while
the slot is Active, and `POLLHUP | POLLERR` when the slot is Down or
the fd is closing. <a id="cite-source.dispatch.poll-reports-queue-and-slot-state"></a>

An fd that is open but has not yet registered reports nothing at all. <a id="cite-source.dispatch.unregistered-fd-polls-nothing"></a>

Any rejected `write()` — short, over-long, an unknown or duplicate
request id, an operation code that does not match the request, a
response for another connection — returns `EINVAL` **and tears the
connection down**. <a id="cite-source.dispatch.rejected-write-is-einval-and-tears-down"></a> A source that cannot speak the protocol correctly is
not one whose other answers are worth believing.

<a id="trm-5-8-3-5"></a>

## Negotiated lifetime control

Sources may negotiate lifetime extension version 1 with `REG_SRC_NEGOTIATE`
before `REG_SRC_REGISTER`. Pass version 1, zero flags and zero session; the
kernel returns a nonzero session identifier unique to the open source file.
The RSI request and response frame layouts are unchanged. Sources that do not
negotiate retain the legacy protocol; current loregd requires this extension.
<a id="cite-source.dispatch.lifetime-extension-is-negotiated-before-registration"></a>

After reading a request and before responding, `REG_SRC_REQUEST_CONTEXT` takes
that session and request id and returns three absolute `CLOCK_MONOTONIC`
nanosecond timestamps: the request deadline, transaction lifetime deadline and
cleanup lease deadline. Zero lifetime means an operation-owned transaction
with no separate lifetime ceiling. Zero lease means there is no live transaction
owner. Request metadata remains queryable after caller detachment until the
response is accepted, so cleanup and late-response handling still work.
<a id="cite-source.dispatch.context-preserves-the-original-request-deadline"></a>

`REG_SRC_RENEW` takes the session and transaction id and returns the original
lifetime deadline plus a renewed cleanup deadline, at most five seconds from
now and never beyond the lifetime deadline. It succeeds only for an existing,
nonterminal transaction owned by a live file object or kernel operation on
this source session. Unknown, released, expired and foreign-session identities
return `ESTALE`. Once a lease expires, renewal cannot resurrect it. These
control ioctls consume no ordinary request slots, so request-queue saturation
does not starve renewal.
<a id="cite-source.dispatch.lease-renewal-requires-a-live-owner-and-session"></a>

Final owner release and abort prevent renewal before abort-message delivery.
Client lifetime expiration also prevents renewal. Sources must reject new
operations after expiry and serialize rollback with operations and commit;
an already-admitted commit must resolve its actual outcome. Lease cleanup
does not change the kernel's treatment of late commit responses ([Failure and Late Responses](<~kernel/internals/lcs/sources/failure-and-late-responses#trm-5-8-5>)).
<a id="cite-source.dispatch.lease-expiry-does-not-infer-a-commit-outcome"></a>
