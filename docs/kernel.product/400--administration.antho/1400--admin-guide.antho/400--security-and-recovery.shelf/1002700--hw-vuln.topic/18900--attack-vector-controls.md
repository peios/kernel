---
title: "Attack Vector Controls"
type: reference
description: "Attack vector controls provide a simple method to configure only the mitigations for CPU vulnerabilities which are relevant given the intended use of a system. Administrators are encouraged to consider which attack vectors are relevant and…"
---

<a id="rst-attack-vector-controls"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

Attack vector controls provide a simple method to configure only the mitigations for CPU vulnerabilities which are relevant given the intended use of a system. Administrators are encouraged to consider which attack vectors are relevant and disable all others in order to recoup system performance.

When new relevant CPU vulnerabilities are found, they will be added to these attack vector controls so administrators will likely not need to reconfigure their command line parameters as mitigations will continue to be correctly applied based on the chosen attack vector controls.

<a id="rst-attack-vectors"></a>

## Attack Vectors

There are 5 sets of attack-vector mitigations currently supported by the kernel:

1. [User-to-Kernel](<#rst-user-kernel>)

2. [User-to-User](<#rst-user-user>)

3. [Guest-to-Host](<#rst-guest-host>)

4. [Guest-to-Guest](<#rst-guest-guest>)

5. [Cross-Thread](<#rst-smt>)

To control the enabled attack vectors, see [Command Line Controls](<#rst-cmdline>).

<a id="rst-user-to-kernel"></a>
<a id="rst-user-kernel"></a>

### User-to-Kernel

The user-to-kernel attack vector involves a malicious userspace program attempting to leak kernel data into userspace by exploiting a CPU vulnerability. The kernel data involved might be limited to certain kernel memory, or include all memory in the system, depending on the vulnerability exploited.

If no untrusted userspace applications are being run, such as with single-user systems, consider disabling user-to-kernel mitigations.

Note that the CPU vulnerabilities mitigated by Linux have generally not been shown to be exploitable from browser-based sandboxes.  User-to-kernel mitigations are therefore mostly relevant if unknown userspace applications may be run by untrusted users.

*user-to-kernel mitigations are enabled by default*

<a id="rst-user-to-user"></a>
<a id="rst-user-user"></a>

### User-to-User

The user-to-user attack vector involves a malicious userspace program attempting to influence the behavior of another unsuspecting userspace program in order to exfiltrate data.  The vulnerability of a userspace program is based on the program itself and the interfaces it provides.

If no untrusted userspace applications are being run, consider disabling user-to-user mitigations.

Note that because the Linux kernel contains a mapping of all physical memory, preventing a malicious userspace program from leaking data from another userspace program requires mitigating user-to-kernel attacks as well for complete protection.

*user-to-user mitigations are enabled by default*

<a id="rst-guest-to-host"></a>
<a id="rst-guest-host"></a>

### Guest-to-Host

The guest-to-host attack vector involves a malicious VM attempting to leak hypervisor data into the VM.  The data involved may be limited, or may potentially include all memory in the system, depending on the vulnerability exploited.

If no untrusted VMs are being run, consider disabling guest-to-host mitigations.

*guest-to-host mitigations are enabled by default if KVM support is present*

<a id="rst-guest-to-guest"></a>
<a id="rst-guest-guest"></a>

### Guest-to-Guest

The guest-to-guest attack vector involves a malicious VM attempting to influence the behavior of another unsuspecting VM in order to exfiltrate data.  The vulnerability of a VM is based on the code inside the VM itself and the interfaces it provides.

If no untrusted VMs, or only a single VM is being run, consider disabling guest-to-guest mitigations.

Similar to the user-to-user attack vector, preventing a malicious VM from leaking data from another VM requires mitigating guest-to-host attacks as well due to the Linux kernel phys map.

*guest-to-guest mitigations are enabled by default if KVM support is present*

<a id="rst-cross-thread"></a>
<a id="rst-smt"></a>

### Cross-Thread

The cross-thread attack vector involves a malicious userspace program or malicious VM either observing or attempting to influence the behavior of code running on the SMT sibling thread in order to exfiltrate data.

Many cross-thread attacks can only be mitigated if SMT is disabled, which will result in reduced CPU core count and reduced performance.

If cross-thread mitigations are fully enabled ('auto,nosmt'), all mitigations for cross-thread attacks will be enabled.  SMT may be disabled depending on which vulnerabilities are present in the CPU.

If cross-thread mitigations are partially enabled ('auto'), mitigations for cross-thread attacks will be enabled but SMT will not be disabled.

If cross-thread mitigations are disabled, no mitigations for cross-thread attacks will be enabled.

Cross-thread mitigation may not be required if core-scheduling or similar techniques are used to prevent untrusted workloads from running on SMT siblings.

*cross-thread mitigations default to partially enabled*

<a id="rst-command-line-controls"></a>
<a id="rst-cmdline"></a>

## Command Line Controls

Attack vectors are controlled through the mitigations= command line option.  The value provided begins with a global option and then may optionally include one or more options to disable various attack vectors.

- **Format:**

  `mitigations=[global]`  
  `mitigations=[global],[attack vectors]`

Global options:


<table>
<thead>
<tr>
<th>


Option

</th>
<th>


Description

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


'off'

</td>
<td>


All attack vectors disabled.

</td>
</tr>
<tr>
<td>


'auto'

</td>
<td>


All attack vectors enabled, partial cross-thread mitigations.

</td>
</tr>
<tr>
<td>


'auto,nosmt'

</td>
<td>


All attack vectors enabled, full cross-thread mitigations.

</td>
</tr>
</tbody>
</table>

Attack vector options:


<table>
<thead>
<tr>
<th>


Option

</th>
<th>


Description

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


'no_user_kernel'

</td>
<td>


Disables user-to-kernel mitigations.

</td>
</tr>
<tr>
<td>


'no_user_user'

</td>
<td>


Disables user-to-user mitigations.

</td>
</tr>
<tr>
<td>


'no_guest_host'

</td>
<td>


Disables guest-to-host mitigations.

</td>
</tr>
<tr>
<td>


'no_guest_guest'

</td>
<td>


Disables guest-to-guest mitigations

</td>
</tr>
<tr>
<td>


'no_cross_thread'

</td>
<td>


Disables all cross-thread mitigations.

</td>
</tr>
</tbody>
</table>

Multiple attack vector options may be specified in a comma-separated list.  If the global option is not specified, it defaults to 'auto'.  The global option 'off' is equivalent to disabling all attack vectors.

- **Examples:**

  `mitigations=auto,no_user_kernel`

  Enable all attack vectors except user-to-kernel.  Partial cross-thread mitigations.

  `mitigations=auto,nosmt,no_guest_host,no_guest_guest`

  Enable all attack vectors and cross-thread mitigations except for guest-to-host and guest-to-guest mitigations.

  `mitigations=,no_cross_thread`

  Enable all attack vectors but not cross-thread mitigations.

<a id="rst-interactions-with-command-line-options"></a>

## Interactions with command-line options

Vulnerability-specific controls (e.g. "retbleed=off") take precedence over all attack vector controls.  Mitigations for individual vulnerabilities may be turned on or off via their command-line options regardless of the attack vector controls.

<a id="rst-summary-of-attack-vector-mitigations"></a>

## Summary of attack-vector mitigations

When a vulnerability is mitigated due to an attack-vector control, the default mitigation option for that particular vulnerability is used.  To use a different mitigation, please use the vulnerability-specific command line option.

The table below summarizes which vulnerabilities are mitigated when different attack vectors are enabled and assuming the CPU is vulnerable.


<table>
<thead>
<tr>
<th>


Vulnerability

</th>
<th>


User-to-Kernel

</th>
<th>


User-to-User

</th>
<th>


Guest-to-Host

</th>
<th>


Guest-to-Guest

</th>
<th>


Cross-Thread

</th>
<th>


Notes

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


BHI

</td>
<td>


X

</td>
<td>




</td>
<td>


X

</td>
<td>




</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


ITS

</td>
<td>


X

</td>
<td>




</td>
<td>


X

</td>
<td>




</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


GDS

</td>
<td>


X

</td>
<td>


X

</td>
<td>


X

</td>
<td>


X

</td>
<td>


- <!-- empty source list item -->

</td>
<td>


(Note 1)

</td>
</tr>
<tr>
<td>


L1TF

</td>
<td>


X

</td>
<td>




</td>
<td>


X

</td>
<td>




</td>
<td>


- <!-- empty source list item -->

</td>
<td>


(Note 2)

</td>
</tr>
<tr>
<td>


MDS

</td>
<td>


X

</td>
<td>


X

</td>
<td>


X

</td>
<td>


X

</td>
<td>


- <!-- empty source list item -->

</td>
<td>


(Note 2)

</td>
</tr>
<tr>
<td>


MMIO

</td>
<td>


X

</td>
<td>


X

</td>
<td>


X

</td>
<td>


X

</td>
<td>


- <!-- empty source list item -->

</td>
<td>


(Note 2)

</td>
</tr>
<tr>
<td>


Meltdown

</td>
<td>


X

</td>
<td>




</td>
<td>




</td>
<td>




</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


Retbleed

</td>
<td>


X

</td>
<td>




</td>
<td>


X

</td>
<td>




</td>
<td>


- <!-- empty source list item -->

</td>
<td>


(Note 3)

</td>
</tr>
<tr>
<td>


RFDS

</td>
<td>


X

</td>
<td>


X

</td>
<td>


X

</td>
<td>


X

</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


Spectre_v1

</td>
<td>


X

</td>
<td>




</td>
<td>




</td>
<td>




</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


Spectre_v2

</td>
<td>


X

</td>
<td>




</td>
<td>


X

</td>
<td>




</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


Spectre_v2_user

</td>
<td>




</td>
<td>


X

</td>
<td>




</td>
<td>


X

</td>
<td>


- <!-- empty source list item -->

</td>
<td>


(Note 1)

</td>
</tr>
<tr>
<td>


SRBDS

</td>
<td>


X

</td>
<td>


X

</td>
<td>


X

</td>
<td>


X

</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


SRSO

</td>
<td>


X

</td>
<td>


X

</td>
<td>


X

</td>
<td>


X

</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


SSB

</td>
<td>




</td>
<td>


X

</td>
<td>




</td>
<td>




</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


TAA

</td>
<td>


X

</td>
<td>


X

</td>
<td>


X

</td>
<td>


X

</td>
<td>


- <!-- empty source list item -->

</td>
<td>


(Note 2)

</td>
</tr>
<tr>
<td>


TSA

</td>
<td>


X

</td>
<td>


X

</td>
<td>


X

</td>
<td>


X

</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


VMSCAPE

</td>
<td>




</td>
<td>




</td>
<td>


X

</td>
<td>




</td>
<td>




</td>
<td>




</td>
</tr>
</tbody>
</table>

- **Notes:**

  1 --  Can be mitigated without disabling SMT.

  2 --  Disables SMT if cross-thread mitigations are fully enabled  and the CPU is vulnerable

  3 --  Disables SMT if cross-thread mitigations are fully enabled, the CPU is vulnerable, and STIBP is not supported

When an attack-vector is disabled, all mitigations for the vulnerabilities listed in the above table are disabled, unless mitigation is required for a different enabled attack-vector or a mitigation is explicitly selected via a vulnerability-specific command line option.
