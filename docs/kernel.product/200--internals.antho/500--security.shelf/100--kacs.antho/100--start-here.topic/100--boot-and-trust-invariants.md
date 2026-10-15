---
title: "Boot and trust invariants"
description: "Boot and trust invariants: behaviour and implementation of the Peios kernel."
type: reference
---

<a id="trm-1-2"></a>

KACS depends on a kernel configuration that protects the kernel trust boundary
and installs its enforcement hooks. The supported build records that
configuration in `peios/config/pkm.fragment` and checks it with
`peios/verify-config.sh`. Kconfig and compile-time assertions impose additional
constraints. These mechanisms have different failure behaviour; a build
requirement is not an init-time check.

<a id="trm-1-2-1"></a>

## The LSM stack invariant

PKM implements KACS through the Linux Security Module framework and direct
integration points. The supported configuration uses
`CONFIG_LSM="landlock,lockdown,integrity,pkm"`. Capability hooks are implicit in
the framework. See [LSM hooks and object state](<~kernel/internals/kacs/integration/lsm-hooks-and-object-state>)
for the registered hooks and direct callers.

<a id="trm-1-2-1-1"></a>

### What the kernel verifies

`security/pkm/Kconfig` requires security support, Rust, a 64-bit target,
`STRICT_DEVMEM` and `MODULE_SIG_FORCE`. It excludes SELinux, AppArmor, SMACK and
TOMOYO. In `security/pkm/kacs/lsm.c`, `pkm_init()` also has `BUILD_BUG_ON`
checks for those MAC LSMs, the BPF LSM, and the two hardening prerequisites.
An incompatible configuration fails to build; it is not a supported path
where the kernel boots and PKM merely declines to activate.

<a id="trm-1-2-1-2"></a>

### The required stack

The supported build disables the conflicting MAC LSMs, BPF LSM and Yama and
checks the exact LSM list. Yama's ptrace policy would introduce an independent
attach decision ahead of KACS. Landlock, lockdown and integrity remain in the
configured stack; their presence does not turn KACS into the authority for
every Linux check. Native process and object policy must be understood
alongside the particular interface's remaining checks.

<a id="trm-1-2-2"></a>

## Module signing

`CONFIG_MODULE_SIG_FORCE=y` is a PKM build prerequisite. Module loading also
has authorization checks, but possession of a loading privilege does not
waive signature verification. The signature establishes trust in executable
kernel code; it does not prove the module is free of defects.

The authoritative operational explanation is
[Module signing](<~kernel/administration/admin-guide/boot/module-signing>),
including Peios's supported signing mechanism and load failures. Kernel
module signatures and executable PIP signatures must not be treated as an
interchangeable format or key-selection mechanism.

<a id="trm-1-2-3"></a>

## The module-loading helper

Kernel-initiated userspace helpers are subject to KACS executable verification
and the helper integrity floor. That is separate from verification of the
module subsequently requested by a helper. The executable must meet the
helper rule, and the module must independently meet module-loading policy.
See process integrity protection ([Process Integrity Protection](<~kernel/internals/kacs/executable-trust/process-integrity-protection#trm-3-7>)) and executable verification ([Binary Signature Verification](<~kernel/internals/kacs/executable-trust/signature-verification#trm-3-6>)).

<a id="trm-1-2-4"></a>

## Memory access restrictions

`CONFIG_STRICT_DEVMEM=y` is a build prerequisite and limits physical-memory
access according to the architecture's implementation. It must not be
described as a universal list of accessible physical regions or as the sole
defence against process-isolation bypasses. KACS also gates relevant device
and physical-memory operations; see process integrity protection ([Process Integrity Protection](<~kernel/internals/kacs/executable-trust/process-integrity-protection#trm-3-7>)).

The status of `/dev/kmem` follows the supported kernel's interfaces and
configuration, rather than being implied by `STRICT_DEVMEM` alone. A native
descriptor grant does not waive another check performed by the device path.

<a id="trm-1-2-5"></a>

## What the kernel will not have

The supported configuration excludes SELinux, AppArmor, SMACK, TOMOYO, BPF LSM
and Yama. The first five are also covered by PKM compile-time assertions.
Keep the distinction between configuration validation and compile-time
enforcement when changing the supported build; do not infer a universal
runtime rejection mechanism from the configuration file.

<a id="trm-1-2-6"></a>

## What about user-space hardening

Service signing and deployment policy are additional requirements. The kernel
derives executable integrity from the verified executable and applies the
rules for the particular exec path. A service being intended as part of the
trusted computing base does not itself assign a PIP tier.

Kernel integrity requirements do not establish that a complete image has the
right service binaries, signatures, descriptors or startup ordering. Those
are properties of the assembled deployment and must be checked there.

<a id="trm-1-2-7"></a>

## The invariant verification

Use the supported build entry points described in
[Building Peios](<~kernel/development/start-here/building-peios>); they apply
and validate the Peios configuration. During PKM initialization,
`pkm_init()` initializes the Rust state, creates bootstrap tokens, constructs
the initial process security state and installs the hooks on success.
Allocation and initialization errors are separate from rejected build
configurations and are not evidence that all boot failures are fail-stop.

The initial userspace program is selected by the boot and init configuration.
The kernel's bootstrap tokens do not by themselves specify the full
prelude/peinit deployment sequence.

<a id="trm-1-2-8"></a>

## Failure modes

A rejected configuration should fail the build or its verification step.
A runtime initialization failure must be diagnosed from the actual init
return path and kernel messages. Do not assume that an ordinary LSM init
error necessarily halts the Linux boot process.

Disabling enforcement prerequisites or changing the LSM stack creates a
different kernel configuration and requires a fresh review of its security
properties. A successful boot alone does not establish that the intended
policy is active. The supported configuration checker and the runtime LSM
list exposed by securityfs provide distinct evidence.

<a id="trm-1-2-9"></a>

## Why these invariants

Native access control assumes that kernel code and data retain their
integrity. Restrictions on loading executable kernel code and accessing
physical memory help protect that boundary. The LSM configuration ensures
that the supported build includes the intended enforcement components.

These are necessary conditions for the intended system, not a proof that
there are no kernel defects or other authority paths. Interface-specific
checks and deployment validation remain relevant.

<a id="trm-1-2-10"></a>

## Where to go next

Read [Peios kernel behaviour](<~kernel/introduction/peios-behaviour>) for the
Linux compatibility boundaries, KACS process integrity ([Process Integrity Protection](<~kernel/internals/kacs/executable-trust/process-integrity-protection#trm-3-7>)) for runtime
protection, and [Building Peios](<~kernel/development/start-here/building-peios>)
for configuration and build validation.
