---
title: Authoring Packet Rules
type: how-to
description: Adapt exception, counting, and time-based policy patterns while checking the complete rule forest.
---

These layouts illustrate individual patterns, not complete replacement
policies. Read the existing forest and retain a local recovery path before
changing live access. Registry paths below are relative to
`Machine\System\Network`.

## Apply a pattern safely

1. Identify the layer and the facts available at its seat. Include protocol
   and traffic scope in every gating rule.
2. Choose a pattern below and adapt addresses, ports, names, and priorities.
   Check competing trees; a child is an exception only within its own tree.
3. Apply the reviewed edit, then inspect the accepted kernel generation.
4. Test the intended connection and inspect attribution and loss counters.
   A write or capture alone does not establish packet delivery.

## Allow one inbound connection class

```text
Rules\Flow\inbound          Direction.Equal = in
                              Actions = REJECT
Rules\Flow\inbound\ssh-lan  Protocol.Equal = tcp, DstPort.Equal = 22
                              SrcAddr.Equal = 10.0.0.0/8
                              Actions = PASS
```

The child narrows the parent region. It does not bypass other layers or
higher-priority trees. A rejection on an established TCP flow can terminate
both endpoints; use `DROP` if the intended refusal is silent.

## Count packets or bytes before gating a source

```text
Rules\Packet\dns-count  Protocol.Equal = udp, DstPort.Equal = 53
                          Actions = COUNT(dns)
Rules\Packet\dns-cap    Protocol.Equal = udp, DstPort.Equal = 53
                          Counter.dns(10s, SrcAddr).GreaterThan = 20
                          Actions = REJECT(Prohibited)
```

The counter rule abstains from a verdict. Matching reads the view before the
current evaluation's count, and the window is approximate. Keep the protocol
and port conditions on the gating rule: removing them broadens refusal to
other traffic from that source.

Use `COUNT(egress, Length)` with an outbound packet rule for byte accounting.
A threshold such as `Counter.egress(1m, SrcAddr).GreaterThan = 104857600`
then measures bytes, not packet count. To count connections instead, use a
`Flow` rule with `COUNT(conns)`; reevaluations can run that effect again.

## Distinguish live time from connection start

```text
Rules\Flow\curfew  Direction.Equal = out
                     Start.Hour.Equal = 22-23, 0-5
                     Priority = 10
                     Actions = REJECT(Prohibited), REPORT(3)
```

This example restricts new outbound flows during those UTC hours. Replacing
`Start.Hour` with `Time.Hour` also makes running flows subject to time-edge
reevaluation. `Time.*` and `Start.*` are not interchangeable schedules.

## Tag a flow and observe its reply

```text
Rules\Packet\tag-dns  Protocol.Equal = udp, DstPort.Equal = 53
                        Actions = TAG(dnsq, Add)
Rules\Packet\reply    Protocol.Equal = udp, SrcPort.Equal = 53
                        Tag.dnsq.GreaterThan = 0
                        Actions = REPORT(4)
```

A tag changes observation state, not access. Tags are flow-scoped, retain
state across generations, and obey layer dependency restrictions.

## Use network context deliberately

```text
Rules\Flow\no-ssh       Direction.Equal = in
                           Protocol.Equal = tcp, DstPort.Equal = 22
                           Actions = DROP
Rules\Flow\no-ssh\home  Network.Trust.Equal = home
                           Actions = PASS
```

`home` is an operator label on the identified network, not cryptographic
proof of location. Missing context cannot satisfy that exception. Changing
the context can cause a new judgment on an established flow's next packet.
Interface/profile selection belongs to netd; it is not Wi-Fi association.
