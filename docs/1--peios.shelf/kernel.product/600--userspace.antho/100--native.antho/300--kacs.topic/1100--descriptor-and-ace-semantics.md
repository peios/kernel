---
title: "Descriptor and ACE semantics"
description: "Descriptor and ACE semantics: behaviour and implementation of the Peios kernel."
type: reference
---

<a id="trm-3-d-1"></a>

## ACE types with no evaluator behaviour <a id="cite-abi-notes.opaque-ace-types"></a>

Two of the ACE type constants in [KACS ABI Reference](<~kernel/userspace/native/kacs/generated-syscall-index#trm-3-a>) have a constant and nothing
behind it. The ACE parser in `kacs-core` dispatches on 0x00–0x03,
0x05–0x14 and classifies every other value as opaque, so an ACE of type
0x04 or 0x15 is skipped during evaluation and written back
byte-for-byte on serialisation. The constants exist so that a decoder
can put a name to the byte. libpeios' SDDL codec does, printing 0x15 as
`SYSTEM_ACCESS_FILTER`; the `sd` utility does not, and renders both as
`OTHER(0x04)` and `OTHER(0x15)`. [PCDS ACE types](https://learn.peios.org/specifications/pcds/security-descriptor/ace-types) records the same state
normatively.
