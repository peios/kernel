---
title: "Transport and per-message identity"
description: "Transport and per-message identity: behaviour and implementation of the Peios kernel."
type: reference
---

<a id="trm-3-5-3-6"></a>

## Delegation and the network boundary

Locally, Impersonation and Delegation behave identically. The
distinction activates at the network boundary, where a
Delegation-level token carries authorization for Kerberos credential
forwarding to services on other machines.

KACS tracks the level on the token and the socket, and authd checks it
when it needs to perform Kerberos authentication for an impersonating
thread. KACS itself has no Kerberos awareness and no network
awareness: the level is a flag that authd interprets.

<a id="trm-3-5-3-7"></a>

## Per-message identity

The connect-time capture is the first entry in a per-end
**conveyed-identity register**: the peer identity associated with the
data that end has consumed so far. <a id="cite-imp.register.connect-capture-is-first-entry"></a> Identity can also travel with the
data itself, as a `KACS_SCM_TOKEN` ancillary message under the
`SOL_KACS` level, and each such message the reader's position passes
advances the register. The anchor is the read position, never arrival:
a token still queued behind unread data is not yet visible, so a
handler can never be told an identity for a request it has not read. <a id="cite-imp.register.anchored-at-read-position"></a>
`KACS_SO_PEER_TOKEN` returns a fresh fd to an immutable snapshot each
time; two calls may name different tokens, but a token never changes. <a id="cite-imp.peer-token.immutable-snapshot"></a>

**Sending.** A sender conveys identity in one of two ways, and the
receiver cannot tell them apart, because both mean the same thing —
*the kernel verified that the sender could be this identity when it
sent these bytes*:

- Automatically, with `KACS_SO_PASS_TOKEN` set on the sending end:
  every send carries the sender's effective token, derived at the
  lower of the end's impersonation level and the token's own. <a id="cite-imp.pass-token.every-send-carries-effective"></a> The derivation is cached against the
  effective token it was made from, so a run of sends under one
  identity costs one derivation. <a id="cite-imp.pass-token.derivation-cached"></a> A thread that impersonates client A,
  writes to a pooled connection, reverts and writes again conveys A for
  the first write and its own identity for the second, with no change
  to the library doing the writing.
- Explicitly, by attaching a token fd in a `KACS_SCM_TOKEN` cmsg. The
  kernel gates the attach exactly as it would gate impersonating that
  token: the fd must carry `TOKEN_IMPERSONATE`, a primary token is
  first derived to an impersonation token at the lower of the end's
  level and its own, and the
  two-gate model runs with the sender as installer. <a id="cite-imp.scm-token.gated-as-impersonation"></a> An attach the gates
  would cap below the token's own level fails with `EPERM` — an
  explicit act fails loudly where an install would silently downgrade. <a id="cite-imp.scm-token.cap-fails-eperm"></a>
  Attaching a token is therefore never more than impersonating it,
  sending, and reverting; it just avoids the install. A router
  forwarding on behalf of many clients re-attaches each client's token
  to the messages it forwards, and each downstream receiver gets a
  kernel-verified identity through the router.

Anonymous-level tokens attach without a gate, as assuming Anonymous is
always a downgrade. <a id="cite-imp.scm-token.anonymous-attaches-ungated"></a> At most one token per message. <a id="cite-imp.scm-token.one-per-message"></a>

**Receiving.** Every skb a send produces carries the conveyed token, so
a large stream write conveys the same identity on all of its
fragments. <a id="cite-imp.receive.identity-on-every-fragment"></a> A stream read stops at an identity boundary rather than
gluing bytes conveyed under different identities into one return,
which keeps the register exact even on a byte stream; on
`SOCK_SEQPACKET` one send is one message and one identity, which is
why it is the recommended type for Peios-native protocols. <a id="cite-imp.receive.read-stops-at-identity-boundary"></a> As the
reader's position passes conveyed data, the register moves to that
identity. `MSG_PEEK` neither advances the register nor consumes; a
`read()` or `splice()` that consumes data advances it just as
`recvmsg` does, because the register is kept at the point of
consumption, not where ancillary data is copied out. <a id="cite-imp.register.advances-on-consumption-only"></a>

A `KACS_SCM_TOKEN` cmsg — carrying a fresh `TOKEN_QUERY |
TOKEN_IMPERSONATE | TOKEN_DUPLICATE` fd — is delivered with a read when
the receive call
supplied room for it and the read's identity differs from the register
the reader had before the read; otherwise nothing is delivered, and
`MSG_CTRUNC` is set only when a token was due and no room was
supplied. <a id="cite-imp.cmsg.delivered-on-identity-change"></a> A handler that never reads ancillary data still has the
register: `recvmsg`, then `getsockopt(KACS_SO_PEER_TOKEN)`, gives the
identity of what it just read. <a id="cite-imp.register.getsockopt-after-read"></a> Parsing the cmsg is the path for
pipelined or concurrent consumers that need the token bound to a
particular message.

`SOCK_DGRAM` sockets carry no register — many senders share one
receiving socket — so a datagram's token is delivered with every
datagram that carries one and is never retained. <a id="cite-imp.dgram.no-register"></a>

<a id="trm-3-5-3-8"></a>

## Supported transports

Peer-token capture works on two AF_UNIX socket types. <a id="cite-imp.transport.stream-and-seqpacket"></a> `SOCK_STREAM`
is the connection-oriented byte stream, and `SOCK_SEQPACKET` is
connection-oriented with message boundaries and uses the same identity
capture model. Both follow the same lifecycle: capture at `connect()`,
read with `KACS_SO_PEER_TOKEN`, impersonate, revert — with per-message
identity layered on top as described above. `SOCK_DGRAM` supports
per-message identity only: `KACS_SO_PASS_TOKEN` and `KACS_SCM_TOKEN`
work, since a send needs no connection, and
`KACS_SO_IMPERSONATION_LEVEL` bounds them as on any socket, but there
is no register. <a id="cite-imp.dgram.per-message-identity-only"></a>

Where the register does not apply, `KACS_SO_PEER_TOKEN` reports which
case it is. On a datagram socket, or any non-Unix family, the option
fails with `EOPNOTSUPP`. <a id="cite-imp.peer-token.eopnotsupp-non-unix"></a> A `socketpair()` end is connected but starts
with an empty register — no connect happened to capture anything — so
the option fails with `ENODATA` until the peer conveys an identity,
after which the register works as on any connection. <a id="cite-imp.peer-token.socketpair-enodata"></a> A socket that is
not yet connected fails with `ENOTCONN`. <a id="cite-imp.peer-token.enotconn"></a> Pipes and FIFOs are not
sockets at all, so `getsockopt` itself fails with `ENOTSOCK` before
KACS is reached. <a id="cite-imp.peer-token.enotsock-pipes"></a>

For all of these, the universal fallback is explicit token fd
impersonation through `KACS_IOC_IMPERSONATE`, which works regardless
of how the token fd was obtained — the peer-token option, an
`SCM_RIGHTS` transfer, or any other path. <a id="cite-imp.impersonate.any-token-fd"></a>
