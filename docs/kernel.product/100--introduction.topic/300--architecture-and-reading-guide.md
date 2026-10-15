---
title: "Architecture and reading guide"
description: "What the Peios kernel is — a Linux kernel with a patch series, the PKM module and a uapi header set compiled into it — and what this manual covers."
type: reference
---

<a id="trm-1-1"></a>

The Peios kernel combines Linux hardware and core services with native access
control, events, configuration, layered storage and packet policy. These
subsystems are built into the kernel; PKM's historical name, “Peios Kernel
Module”, does not mean it is a loadable module.

<a id="trm-1-1-1"></a>

## The native subsystems

| Subsystem | Responsibility | Start reading |
| --- | --- | --- |
| KACS | Tokens, security descriptors, access checks, impersonation and process integrity | [Overview](<~kernel/internals/kacs/start-here/overview#trm-3-1>) |
| KMES | Trusted event stamps, emission and per-CPU delivery rings | [Overview](<~kernel/internals/kmes/overview#trm-2-1>) |
| LCS | Registry objects, layers, watches, transactions and source dispatch | [Overview](<~kernel/internals/lcs/start-here/overview#trm-5-1>) |
| StrataFS | Name resolution and mutation across an ordered stack of directories | [Overview](<~kernel/internals/stratafs/start-here/overview#trm-4-1>) |
| NTFE | Packet snapshots, policy evaluation, flow decisions and policy generations | [Overview](<~kernel/internals/ntfe/overview#trm-6-1>) |

The components share services. KACS supplies identity for KMES stamps and sends
audit events through KMES. LCS uses KACS descriptors for authorization and
userspace registry sources for storage. StrataFS delegates authority to KACS
while controlling provider selection and copy-up. NTFE consumes configuration
through LCS and obtains local socket identity from KACS.

<a id="trm-1-1-2"></a>

## Source ownership

KACS, KMES and LCS live under `security/pkm/`. StrataFS lives in `fs/stratafs/`,
and NTFE's networking integration lives in `net/ntfe/`. Public interfaces are
declared under `include/uapi/pkm/`. Shared Rust semantic code is compiled from
the kernel sources; the host-test workspace in `peios/rust/` provides wrappers
and tests for that same code.

The kernel also changes existing Linux enforcement and integration points.
[Peios kernel behaviour](<~kernel/introduction/peios-behaviour>) explains how
to read inherited Linux documentation in this environment, including retained
compatibility checks and remote filesystem authority.

<a id="trm-1-1-3"></a>

## Choosing a reading path

For the security model, start with KACS tokens ([The Token Model](<~kernel/internals/kacs/tokens/the-token-model#trm-3-2-1>)), follow the process
security state ([The PSB Model](<~kernel/internals/kacs/process-security/state-and-lifetime#trm-3-3-1>)), and then read the AccessCheck overview ([AccessCheck Overview](<~kernel/internals/kacs/access-check/accesscheck-overview#trm-3-8-1>)) and
algorithm ([The Algorithm](<~kernel/internals/kacs/access-check/the-algorithm#trm-3-8-10>)). File authority ([The Handle Model](<~kernel/internals/kacs/file-security/the-handle-model#trm-3-9-1>)) connects that model to StrataFS
copy-up ([Copy-Up](<~kernel/internals/stratafs/mutation/copy-up#trm-4-5-2>)) and descriptor preservation ([Descriptors on Copy-Up](<~kernel/internals/stratafs/security/copy-up-descriptors#trm-4-6-3>)).

For event and configuration services, read the KMES event model ([Event Model](<~kernel/internals/kmes/event-model#trm-2-2>)), rings
([Ring Buffers](<~kernel/internals/kmes/ring-buffers#trm-2-5>)) and emission policy ([Emission Policy](<~kernel/internals/kmes/emission-policy#trm-2-8>)), then LCS data objects ([Hives and Routing](<~kernel/internals/lcs/data-model/hives-and-routing#trm-5-2-1>)), layers ([The Layer Model](<~kernel/internals/lcs/layers/the-layer-model#trm-5-3-1>))
and bootstrap ([The Bootstrap Problem](<~kernel/internals/lcs/bootstrap/dependencies-and-boot-sequence#trm-5-10-1>)). NTFE's overview ([Overview](<~kernel/internals/ntfe/overview#trm-6-1>)) brings together policy ingestion,
packet evaluation and flow state.

For application and service callers, use the native interface references:
KMES syscalls ([Syscall Interface](<~kernel/userspace/native/kmes/emission-and-attachment-syscalls#trm-2-4>)), KACS ABI ([KACS ABI Reference](<~kernel/userspace/native/kacs/generated-syscall-index#trm-3-a>)), LCS descriptors and calls ([The Fd Model](<~kernel/userspace/native/lcs/file-descriptors-and-buffer-conventions#trm-5-5-1>)), and
the NTFE device interface ([NTFE ABI Notes](<~kernel/userspace/native/ntfe/device-operations-and-errors#trm-6-b>)). For operation, start with StrataFS mount
options ([Mount Options](<~kernel/administration/stratafs/mount-options#trm-4-2-2>)). For kernel development, read
[Building Peios](<~kernel/development/start-here/building-peios>) and the
[native subsystem testing guide](<~kernel/development/native-subsystems/overview>).

<a id="trm-1-1-4"></a>

## Scope and specifications

These articles describe the implementation and its interfaces. A documented
code path is not a claim that every configuration or deployment has been
qualified. Generated ABI tables report values and layouts from this tree;
handwritten articles explain behaviour that those tables cannot express.

Cross-system formats and protocols retain their own specifications in
[PCDS](https://learn.peios.org/peios/advanced-peios/pcds) and
[PSPK](https://learn.peios.org/peios/advanced-peios/pspk). The kernel articles
explain how the implementation uses those contracts and call out differences
where relevant.
