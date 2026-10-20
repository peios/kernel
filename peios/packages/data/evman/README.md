# Kernel Event Catalogs

These `.evman` fragments define kernel events and their fields. Kernel
packaging installs them under `/usr/share/evman`, where the `evman` command
reads them. They describe record meaning; they do not collect events.

## Ownership

The fragments are the maintained definitions. Keep event-specific prose
with its event and general field meaning with its field. Shared roots and
common role fields belong to `kernel.evman`. Subsystem fragments own their
domain-specific fields and events:

| Fragment | Subject |
|---|---|
| `kernel.evman` | Header fields, generic roots, and common role fields |
| `kacs.evman` | Access checks, identity, signatures, and process security |
| `kmes.evman` | Event transport, configuration, and loss |
| `lcs.evman` | Registry operations and source diagnostics |
| `ntfe.evman` | Network policy and verdicts |
| `stratafs.evman` | Stratum changes and filesystem operations |

Userspace components maintain and package their own fragments in their own
repositories. An event can carry a field another fragment defines. Defining
a new field changes the shared vocabulary; review that interface separately
from an editorial clarification.

The format and ownership rules are defined in
[PGSS's catalog specification](https://learn.peios.org/specifications/pgss/events/the-catalogue/).
Use `include:` for a named field group and `field:` for an event's presence
rule and any narrower explanation of the field.

## Verify an edit

Run `evman lint` on the complete set of fragments that will be installed
together. It checks duplicate definitions, field references, ownership,
presence expressions, and conflicting value and map paths. Linting a single
fragment cannot establish consistency with the complete catalog.

Review the rendered event and field cards with `evman`. The first sentence
of a record is its index summary. Write a complete sentence and preserve
field-specific explanations when editing the surrounding event prose.

Catalog validation does not verify producer behavior. Check emission sites
under `security/pkm/`, semantic cores under `peios/rust/`, and the relevant
`include/uapi/pkm/` declarations when changing types, values, or presence
rules. A field defined for future use must not be described as already
emitted.

The retired staging event book was generated from these definitions.
Maintaining a separate browsable event reference is deferred. Continue to
edit and ship the fragments; no generated Learn book needs updating.
