---
title: "Object ACEs and Property-Level Access"
description: "Per-property access control through GUID-scoped ACEs — object type lists, propagation, PRINCIPAL_SELF, and per-node results."
type: reference
---

<a id="trm-3-8-5"></a>

An object ACE carries a GUID identifying the property or property set
its rule applies to, which is what enables per-property access control
on objects with internal structure — Active Directory objects, most
obviously. An object ACE with no GUID, meaning
`ACE_OBJECT_TYPE_PRESENT` is unset, behaves exactly like a basic ACE. <a id="cite-check.object-ace.no-guid-is-basic"></a>

<a id="trm-3-8-5-1"></a>

## Object type lists

To request property-level access the caller supplies an object type
list: a tree of GUIDs representing the properties being asked for.
Each node carries its own `decided` and `granted` pair and is resolved
independently. <a id="cite-check.object-ace.per-node-state"></a>

With no list supplied, object ACEs with GUIDs apply globally, as if
they were basic ACEs. <a id="cite-check.object-ace.no-list-applies-globally"></a> With a list supplied, every ACE that behaves
like a basic ACE — ordinary basic ACEs, and object ACEs without an
`ObjectType` GUID — applies to every node in the tree. <a id="cite-check.object-ace.basic-applies-to-all-nodes"></a> An object ACE
whose GUID does not appear anywhere in the supplied tree is silently
skipped. <a id="cite-check.object-ace.unmatched-guid-skipped"></a>

<a id="trm-3-8-5-2"></a>

## Propagation

Decisions move through the tree in four ways.

**Downward from grants.** A grant on a property set flows to every
attribute within it, each child node still applying first-writer-wins
for itself. <a id="cite-check.object-ace.grant-propagates-down"></a>

**Upward from grants.** When every attribute within a property set has
been granted the same right, that right propagates up to the set's
node. <a id="cite-check.object-ace.grant-propagates-up"></a> The propagation is a per-bit intersection, so a right reaches
the parent only if all siblings share it.

**Upward from denials.** A denial on an attribute propagates to every
ancestor regardless of what its siblings hold, and siblings are
themselves unaffected. <a id="cite-check.object-ace.denial-propagates-up"></a> Ancestors still apply first-writer-wins to the
propagated bits, so a denial cannot overturn something an ancestor had
already decided. <a id="cite-check.object-ace.denial-up-first-writer-wins"></a>

**Downward from denials.** A denial on a property set flows to every
attribute within it, again subject to first-writer-wins. <a id="cite-check.object-ace.denial-propagates-down"></a>

<a id="trm-3-8-5-3"></a>

## PRINCIPAL_SELF

`PRINCIPAL_SELF` (`S-1-5-10`) is a placeholder for the object's
associated principal. An ACE targeting it matches the caller when the
caller's token represents the same principal as the object, which the
caller establishes by passing the object's principal SID as the
`self_sid` parameter. <a id="cite-check.object-ace.principal-self-matches-self-sid"></a> With a null `self_sid`, `PRINCIPAL_SELF` ACEs
match nothing. <a id="cite-check.object-ace.principal-self-null-matches-nothing"></a>

It follows the ordinary deny-only rules: if the caller's matching SID
is deny-only, `PRINCIPAL_SELF` matches deny ACEs but not allow ACEs. <a id="cite-check.object-ace.principal-self-deny-only"></a>

<a id="trm-3-8-5-4"></a>

## Scalar and per-node results

`AccessCheck` requires every node to pass, so a denial on any one
property fails the whole request. <a id="cite-check.object-ace.scalar-requires-all-nodes"></a> `AccessCheckResultList` returns a
separate verdict per node.

The scalar result `AccessCheck` returns is the root node's granted
mask. <a id="cite-check.object-ace.scalar-is-root-mask"></a> That is equivalent to the intersection across all nodes, but by
construction rather than by computation: upward denial propagation
forces every descendant's denial into all of its ancestors' `decided`
sets, which guarantees the root's granted mask is a subset of every
node's.

<a id="trm-3-8-5-5"></a>

## Validation

Object type lists are validated strictly, at parse time.

- A supplied list is non-empty. <a id="cite-check.object-ace.list-non-empty"></a>
- Its first node is at level 0. <a id="cite-check.object-ace.list-first-node-level-zero"></a>
- There is exactly one level-0 node. <a id="cite-check.object-ace.list-one-root"></a>
- There are no level gaps, meaning no node at level N+2 following one
  at level N. <a id="cite-check.object-ace.list-no-level-gaps"></a>
- No GUID appears twice. <a id="cite-check.object-ace.list-no-duplicate-guid"></a>

These checks are stricter than MS-DTYP, which does not specify them.
They exist because a duplicate GUID makes node lookup return the wrong
node, and a level gap makes propagation undefined.
