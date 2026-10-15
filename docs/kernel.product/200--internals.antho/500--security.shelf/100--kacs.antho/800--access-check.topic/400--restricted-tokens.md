---
title: "Restricted Tokens"
description: "The second pass a restricted token forces — when it runs, how privileges bypass it, and how owner rights and virtual groups behave in it."
type: reference
---

<a id="trm-3-8-4"></a>

A restricted token carries a secondary SID list, the restricting SIDs.
The second pass runs whenever that list or the restricted device group
list is non-empty, and AccessCheck evaluates the DACL twice. <a id="cite-check.restricted.second-pass-trigger"></a>

The **normal pass** evaluates the DACL against the token's ordinary
identity — user SID and group SIDs — exactly as usual. The
**restricted pass** evaluates the same DACL again with SID matching
drawn only from the restricting SID list; the token's normal groups
are invisible to it. <a id="cite-check.restricted.only-restricting-sids-match"></a> Conditional membership operators — `Member_of`,
`Member_of_Any`, and their device variants — take the same restricted
view, seeing only the restricting SIDs plus any virtual groups
injected from that list. <a id="cite-check.restricted.conditional-membership-restricted"></a>

The restricting SID list is **presence-based**. A SID participates
whenever it appears in the list, and `SE_GROUP_ENABLED` and
`SE_GROUP_USE_FOR_DENY_ONLY` on those entries are ignored both for
restricted-pass SID matching and for restricted-pass non-device
conditional membership. <a id="cite-check.restricted.presence-based"></a> This matches Windows restricted-token
behaviour, where restricting SIDs are always enabled for access
checks.

Access is granted only for rights **both passes agree on** — the
intersection. <a id="cite-check.restricted.intersection"></a> The restricting list acts as a ceiling: the principal
can never receive more access than the restricting SIDs would
independently justify.

<a id="trm-3-8-4-1"></a>

## Write-restricted tokens <a id="cite-check.restricted.write-restricted"></a>

In the write-restricted variant the intersection applies only to
write-category bits, and read and execute access comes from the normal
pass alone. What counts as write is whatever the object type's
GenericMapping maps `GENERIC_WRITE` onto.

<a id="trm-3-8-4-2"></a>

## Privileges bypass the restricted pass <a id="cite-check.restricted.privileges-bypass"></a>

Rights granted by privileges are added back after the intersection.
Privileges are system-level grants from security policy rather than
from the object's DACL: token restriction reduces the identity-based
access surface, and privilege-based grants are orthogonal to it. The
bits restored are the post-PIP privilege-granted set together with the
take-ownership grant. <a id="cite-check.restricted.restored-set"></a>

<a id="trm-3-8-4-3"></a>

## Owner rights and virtual groups in the restricted pass

The restricted pass evaluates owner implicit rights independently. If
the object's owner SID appears in the restricting SID list, the pass
grants `READ_CONTROL` and `WRITE_DAC`, subject to the same `OWNER
RIGHTS` suppression pre-scan as the normal pass; if the owner SID is
not a restricting SID, no implicit rights are granted. <a id="cite-check.restricted.owner-implicit"></a>

Two virtual groups are injected on the same basis. `S-1-3-4` (`OWNER
RIGHTS`) is injected when the object's owner SID is among the
restricting SIDs, and `S-1-5-10` (`PRINCIPAL_SELF`) when `self_sid`
is. <a id="cite-check.restricted.virtual-groups"></a> This keeps the restricted pass consistent in its handling of these
well-known SIDs rather than letting them leak the unrestricted
identity.

Restricted device groups, when the token has them, are swapped in for
the restricted pass so that `Device_Member_of` and its relatives
evaluate against the restricted set rather than the unrestricted
device groups. <a id="cite-check.restricted.device-groups-swapped"></a>
