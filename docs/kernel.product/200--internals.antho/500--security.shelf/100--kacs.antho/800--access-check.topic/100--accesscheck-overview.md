---
title: "AccessCheck Overview"
description: "The function that connects tokens to descriptors — its two API variants, and the three state values a right can hold during evaluation."
type: reference
---

<a id="trm-3-8-1"></a>

AccessCheck is the function that connects tokens to security
descriptors. Given a token — who is asking — a descriptor — what the
rules are — and a desired access mask — what they want to do — it
returns a verdict: which of the requested rights are granted, and
whether the request as a whole succeeds.

It is a pipeline, evaluating several layers of policy in a fixed
order. Each layer can grant or constrain access and the layers
interact: integrity policy can block what the DACL would allow,
privileges can override what the DACL denied, and confinement can
revoke what privileges granted. The order is not incidental — it is
the specification.

<a id="trm-3-8-1-1"></a>

## Two API variants

**AccessCheck** is the common case. It returns the granted access
mask, whether the request succeeded, a continuous audit mask derived
from SACL alarm ACEs, and a CAAP staging mismatch flag. <a id="cite-check.accesscheck.returns"></a> When an object
type list is supplied, success requires every listed node to pass and
the returned mask is the intersection across them. The staging
mismatch flag is set when the staged scalar result differs from the
effective scalar result, when any per-node staged grant differs from
the effective per-node grant, or when staged auditing differs from
effective auditing. <a id="cite-check.staging-flag.accesscheck"></a>

**AccessCheckResultList** is the per-property variant and requires an
object type list. <a id="cite-check.result-list.requires-tree"></a> It returns a separate verdict for each node, so a
denial on one property fails that property alone rather than the whole
request. <a id="cite-check.result-list.returns"></a> It returns the same continuous audit mask and staging
mismatch flag, with the flag set when the staged scalar result differs
from the effective one, when any node's staged granted mask differs
from that node's effective granted mask, or when staged auditing
differs from effective auditing — the scalar comparison is not
mode-branched. <a id="cite-check.staging-flag.result-list"></a> Directory services use it,
because one operation there may touch several properties with
independent access rules. Privilege-use auditing in this variant takes
the same per-node view: a privilege counts as successfully used if its
contributed bits survive on *any* node's final granted mask.

Both variants share one evaluation pipeline. Only the collection of
results differs.

<a id="trm-3-8-1-2"></a>

## The three state values

Every access check tracks three masks.

**`decided`** records which bits have been resolved. It enforces
first-writer-wins within the DACL walk: once a bit is decided, no
later ACE in the same walk changes its outcome. Pipeline layers that
operate on top of the DACL result — restricted token intersection,
confinement intersection, PIP revocation, CAAP intersection — may
still revoke granted bits. Those layers narrow the result; they do not
re-open decided bits for re-evaluation through the DACL. <a id="cite-check.state.narrow-not-reopen"></a>

**`granted`** records which bits resolved to yes. During the walk it
is a subset of `decided`. Afterwards the later layers may remove bits
from it, and the final value is what the caller receives.

**`privilege_granted`** records which bits in `granted` came from a
privilege rather than from the DACL. It exists for two reasons: audit
accuracy, so that privilege-granted access is distinguishable from
DACL-granted access, and the restricted token merge, where
privilege-granted bits are restored after the intersection so that
privileges bypass the restricted pass. PIP may revoke
privilege-granted bits.

With an object type list present, each node carries its own `decided`
and `granted` pair.
