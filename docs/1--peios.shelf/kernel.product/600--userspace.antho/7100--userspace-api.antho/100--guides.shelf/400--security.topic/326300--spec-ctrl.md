---
title: "Speculation Control"
type: reference
description: "Quite some CPUs have speculation-related misfeatures which are in fact vulnerabilities causing data leaks in various forms even across privilege domains."
---

<a id="rst-speculation-control"></a>

Quite some CPUs have speculation-related misfeatures which are in fact vulnerabilities causing data leaks in various forms even across privilege domains.

The kernel provides mitigation for such vulnerabilities in various forms. Some of these mitigations are compile-time configurable and some can be supplied on the kernel command line.

There is also a class of mitigations which are very expensive, but they can be restricted to a certain set of processes or tasks in controlled environments. The mechanism to control these mitigations is via `prctl(2)`.

There are two prctl options which are related to this:

> - PR_GET_SPECULATION_CTRL
>
> - PR_SET_SPECULATION_CTRL

<a id="rst-pr-get-speculation-ctrl"></a>

## PR_GET_SPECULATION_CTRL

PR_GET_SPECULATION_CTRL returns the state of the speculation misfeature which is selected with arg2 of prctl(2). The return value uses bits 0-3 with the following meaning (with the caveat that PR_SPEC_L1D_FLUSH has less obvious semantics, see documentation for that specific control below):


<table>
<thead>
<tr>
<th>


Bit

</th>
<th>


Define

</th>
<th>


Description

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


0

</td>
<td>


PR_SPEC_PRCTL

</td>
<td>


Mitigation can be controlled per task by PR_SET_SPECULATION_CTRL.

</td>
</tr>
<tr>
<td>


1

</td>
<td>


PR_SPEC_ENABLE

</td>
<td>


The speculation feature is enabled, mitigation is disabled.

</td>
</tr>
<tr>
<td>


2

</td>
<td>


PR_SPEC_DISABLE

</td>
<td>


The speculation feature is disabled, mitigation is enabled.

</td>
</tr>
<tr>
<td>


3

</td>
<td>


PR_SPEC_FORCE_DISABLE

</td>
<td>


Same as PR_SPEC_DISABLE, but cannot be undone. A subsequent prctl(..., PR_SPEC_ENABLE) will fail.

</td>
</tr>
<tr>
<td>


4

</td>
<td>


PR_SPEC_DISABLE_NOEXEC

</td>
<td>


Same as PR_SPEC_DISABLE, but the state will be cleared on `execve(2)`.

</td>
</tr>
</tbody>
</table>

If all bits are 0 the CPU is not affected by the speculation misfeature.

If PR_SPEC_PRCTL is set, then the per-task control of the mitigation is available. If not set, prctl(PR_SET_SPECULATION_CTRL) for the speculation misfeature will fail.

<a id="rst-pr-set-speculation-ctrl"></a>
<a id="rst-set-spec-ctrl"></a>

## PR_SET_SPECULATION_CTRL

PR_SET_SPECULATION_CTRL allows to control the speculation misfeature, which is selected by arg2 of `prctl(2)` per task. arg3 is used to hand in the control value, i.e. either PR_SPEC_ENABLE or PR_SPEC_DISABLE or PR_SPEC_FORCE_DISABLE.

<a id="rst-common-error-codes"></a>

## Common error codes


<table>
<thead>
<tr>
<th>


Value

</th>
<th>


Meaning

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


EINVAL

</td>
<td>


The prctl is not implemented by the architecture or unused prctl(2) arguments are not 0.

</td>
</tr>
<tr>
<td>


ENODEV

</td>
<td>


arg2 is selecting a not supported speculation misfeature.

</td>
</tr>
</tbody>
</table>

<a id="rst-pr-set-speculation-ctrl-error-codes"></a>

## PR_SET_SPECULATION_CTRL error codes


<table>
<thead>
<tr>
<th>


Value

</th>
<th>


Meaning

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


0

</td>
<td>


Success

</td>
</tr>
<tr>
<td>


ERANGE

</td>
<td>


arg3 is incorrect, i.e. it's neither PR_SPEC_ENABLE nor PR_SPEC_DISABLE nor PR_SPEC_FORCE_DISABLE.

</td>
</tr>
<tr>
<td>


ENXIO

</td>
<td>


For PR_SPEC_STORE_BYPASS: control of the selected speculation misfeature is not possible via prctl, because of the system's boot configuration.

</td>
</tr>
<tr>
<td>


EPERM

</td>
<td>


Speculation was disabled with PR_SPEC_FORCE_DISABLE and caller tried to enable it again.

</td>
</tr>
<tr>
<td>


EPERM

</td>
<td>


For PR_SPEC_L1D_FLUSH and PR_SPEC_INDIRECT_BRANCH: control of the mitigation is not possible because of the system's boot configuration.

</td>
</tr>
</tbody>
</table>

<a id="rst-speculation-misfeature-controls"></a>

## Speculation misfeature controls

- PR_SPEC_STORE_BYPASS: Speculative Store Bypass

  - **Invocations:**

    - prctl(PR_GET_SPECULATION_CTRL, PR_SPEC_STORE_BYPASS, 0, 0, 0);

    - prctl(PR_SET_SPECULATION_CTRL, PR_SPEC_STORE_BYPASS, PR_SPEC_ENABLE, 0, 0);

    - prctl(PR_SET_SPECULATION_CTRL, PR_SPEC_STORE_BYPASS, PR_SPEC_DISABLE, 0, 0);

    - prctl(PR_SET_SPECULATION_CTRL, PR_SPEC_STORE_BYPASS, PR_SPEC_FORCE_DISABLE, 0, 0);

    - prctl(PR_SET_SPECULATION_CTRL, PR_SPEC_STORE_BYPASS, PR_SPEC_DISABLE_NOEXEC, 0, 0);

- - **PR_SPEC_INDIR_BRANCH: Indirect Branch Speculation in User Processes**

    (Mitigate Spectre V2 style attacks against user processes)

  - **Invocations:**

    - prctl(PR_GET_SPECULATION_CTRL, PR_SPEC_INDIRECT_BRANCH, 0, 0, 0);

    - prctl(PR_SET_SPECULATION_CTRL, PR_SPEC_INDIRECT_BRANCH, PR_SPEC_ENABLE, 0, 0);

    - prctl(PR_SET_SPECULATION_CTRL, PR_SPEC_INDIRECT_BRANCH, PR_SPEC_DISABLE, 0, 0);

    - prctl(PR_SET_SPECULATION_CTRL, PR_SPEC_INDIRECT_BRANCH, PR_SPEC_FORCE_DISABLE, 0, 0);

- - **PR_SPEC_L1D_FLUSH: Flush L1D Cache on context switch out of the task**

    (works only when tasks run on non SMT cores)

For this control, PR_SPEC_ENABLE means that the **mitigation** is enabled (L1D is flushed), PR_SPEC_DISABLE means it is disabled.

> - **Invocations:**
>
>   - prctl(PR_GET_SPECULATION_CTRL, PR_SPEC_L1D_FLUSH, 0, 0, 0);
>
>   - prctl(PR_SET_SPECULATION_CTRL, PR_SPEC_L1D_FLUSH, PR_SPEC_ENABLE, 0, 0);
>
>   - prctl(PR_SET_SPECULATION_CTRL, PR_SPEC_L1D_FLUSH, PR_SPEC_DISABLE, 0, 0);
