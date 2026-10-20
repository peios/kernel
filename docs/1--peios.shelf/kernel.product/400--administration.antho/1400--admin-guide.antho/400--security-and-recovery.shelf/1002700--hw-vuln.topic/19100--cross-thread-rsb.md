---
title: "Cross-Thread Return Address Predictions"
type: reference
description: "Certain AMD and Hygon processors are subject to a cross-thread return address predictions vulnerability. When running in SMT mode and one sibling thread transitions out of C0 state, the other sibling thread could use return target…"
---

<a id="rst-cross-thread-return-address-predictions"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

Certain AMD and Hygon processors are subject to a cross-thread return address predictions vulnerability. When running in SMT mode and one sibling thread transitions out of C0 state, the other sibling thread could use return target predictions from the sibling thread that transitioned out of C0.

The Spectre v2 mitigations protect the Linux kernel, as it fills the return address prediction entries with safe targets when context switching to the idle thread. However, KVM does allow a VMM to prevent exiting guest mode when transitioning out of C0. This could result in a guest-controlled return target being consumed by the sibling thread.

<a id="rst-affected-processors"></a>

## Affected processors

The following CPUs are vulnerable:

> - AMD Family 17h processors
>
> - Hygon Family 18h processors

<a id="rst-related-cves"></a>

## Related CVEs

The following CVE entry is related to this issue:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> CVE-2022-27672
>
> </td>
> <td>
>
>
> Cross-Thread Return Address Predictions
>
> </td>
> </tr>
> </tbody>
> </table>

<a id="rst-problem"></a>

## Problem

Affected SMT-capable processors support 1T and 2T modes of execution when SMT is enabled. In 2T mode, both threads in a core are executing code. For the processor core to enter 1T mode, it is required that one of the threads requests to transition out of the C0 state. This can be communicated with the HLT instruction or with an MWAIT instruction that requests non-C0. When the thread re-enters the C0 state, the processor transitions back to 2T mode, assuming the other thread is also still in C0 state.

In affected processors, the return address predictor (RAP) is partitioned depending on the SMT mode. For instance, in 2T mode each thread uses a private 16-entry RAP, but in 1T mode, the active thread uses a 32-entry RAP. Upon transition between 1T/2T mode, the RAP contents are not modified but the RAP pointers (which control the next return target to use for predictions) may change. This behavior may result in return targets from one SMT thread being used by RET predictions in the sibling thread following a 1T/2T switch. In particular, a RET instruction executed immediately after a transition to 1T may use a return target from the thread that just became idle. In theory, this could lead to information disclosure if the return targets used do not come from trustworthy code.

<a id="rst-attack-scenarios"></a>

## Attack scenarios

An attack can be mounted on affected processors by performing a series of CALL instructions with targeted return locations and then transitioning out of C0 state.

<a id="rst-mitigation-mechanism"></a>

## Mitigation mechanism

Before entering idle state, the kernel context switches to the idle thread. The context switch fills the RAP entries (referred to as the RSB in Linux) with safe targets by performing a sequence of CALL instructions.

Prevent a guest VM from directly putting the processor into an idle state by intercepting HLT and MWAIT instructions.

Both mitigations are required to fully address this issue.

<a id="rst-mitigation-control-on-the-kernel-command-line"></a>

## Mitigation control on the kernel command line

Use existing Spectre v2 mitigations that will fill the RSB on context switch.

<a id="rst-mitigation-control-for-kvm-module-parameter"></a>

## Mitigation control for KVM - module parameter

By default, the KVM hypervisor mitigates this issue by intercepting guest attempts to transition out of C0. A VMM can use the KVM_CAP_X86_DISABLE_EXITS capability to override those interceptions, but since this is not common, the mitigation that covers this path is not enabled by default.

The mitigation for the KVM_CAP_X86_DISABLE_EXITS capability can be turned on using the boolean module parameter mitigate_smt_rsb, e.g. `kvm.mitigate_smt_rsb=1`.
