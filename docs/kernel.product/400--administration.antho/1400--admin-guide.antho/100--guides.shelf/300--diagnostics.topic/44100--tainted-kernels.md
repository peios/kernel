---
title: "Tainted kernels"
type: reference
description: "The kernel will mark itself as 'tainted' when something occurs that might be relevant later when investigating problems. Don't worry too much about this, most of the time it's not a problem to run a tainted kernel; the information is…"
---

<a id="rst-tainted-kernels"></a>

The kernel will mark itself as 'tainted' when something occurs that might be relevant later when investigating problems. Don't worry too much about this, most of the time it's not a problem to run a tainted kernel; the information is mainly of interest once someone wants to investigate some problem, as its real cause might be the event that got the kernel tainted. That's why bug reports from tainted kernels will often be ignored by developers, hence try to reproduce problems with an untainted kernel.

Note the kernel will remain tainted even after you undo what caused the taint (i.e. unload a proprietary kernel module), to indicate the kernel remains not trustworthy. That's also why the kernel will print the tainted state when it notices an internal problem (a 'kernel bug'), a recoverable error ('kernel oops') or a non-recoverable error ('kernel panic') and writes debug information about this to the logs `dmesg` outputs. It's also possible to check the tainted state at runtime through a file in `/proc/`.

<a id="rst-tainted-flag-in-bugs-oops-or-panics-messages"></a>

## Tainted flag in bugs, oops or panics messages

You find the tainted state near the top in a line starting with 'CPU:'; if or why the kernel was tainted is shown after the Process ID ('PID:') and a shortened name of the command ('Comm:') that triggered the event:



```text
BUG: unable to handle kernel NULL pointer dereference at 0000000000000000
Oops: 0002 [#1] SMP PTI
CPU: 0 PID: 4424 Comm: insmod Tainted: P        W  O      4.20.0-0.rc6.fc30 #1
Hardware name: Red Hat KVM, BIOS 0.5.1 01/01/2011
RIP: 0010:my_oops_init+0x13/0x1000 [kpanic]
[...]
```

You'll find a 'Not tainted: ' there if the kernel was not tainted at the time of the event; if it was, then it will print 'Tainted: ' and characters either letters or blanks. In the example above it looks like this:



```text
Tainted: P        W  O
```

The meaning of those characters is explained in the table below. In this case the kernel got tainted earlier because a proprietary Module (`P`) was loaded, a warning occurred (`W`), and an externally-built module was loaded (`O`). To decode other letters use the table below.

<a id="rst-decoding-tainted-state-at-runtime"></a>

## Decoding tainted state at runtime

At runtime, you can query the tainted state by reading `cat /proc/sys/kernel/tainted`. If that returns `0`, the kernel is not tainted; any other number indicates the reasons why it is. The easiest way to decode that number is the script `tools/debugging/kernel-chktaint`, which your distribution might ship as part of a package called `linux-tools` or `kernel-tools`; if it doesn't, you can download the script from [git.kernel.org](<https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/tools/debugging/kernel-chktaint>)<a id="rst-git-kernel-org"></a> and execute it with `sh kernel-chktaint`, which would print something like this on the machine that had the statements in the logs that were quoted earlier:



```text
Kernel is Tainted for following reasons:
 * Proprietary module was loaded (#0)
 * Kernel issued warning (#9)
 * Externally-built ('out-of-tree') module was loaded  (#12)
See Documentation/admin-guide/tainted-kernels.rst in the Linux kernel or
 https://www.kernel.org/doc/html/latest/admin-guide/tainted-kernels.html for
 a more details explanation of the various taint flags.
Raw taint value as int/string: 4609/'P        W  O     '
```

You can try to decode the number yourself. That's easy if there was only one reason that got your kernel tainted, as in this case you can find the number with the table below. If there were multiple reasons you need to decode the number, as it is a bitfield, where each bit indicates the absence or presence of a particular type of taint. It's best to leave that to the aforementioned script, but if you need something quick you can use this shell command to check which bits are set:



```text
$ for i in $(seq 18); do echo $(($i-1)) $(($(cat /proc/sys/kernel/tainted)>>($i-1)&1));done
```

<a id="rst-table-for-decoding-tainted-state"></a>

## Table for decoding tainted state


<table>
<thead>
<tr>
<th>


Bit

</th>
<th>


Log

</th>
<th>


Number

</th>
<th>


Reason that got the kernel tainted

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


0

</td>
<td>


G/P

</td>
<td>


1

</td>
<td>


proprietary module was loaded

</td>
</tr>
<tr>
<td>


1

</td>
<td>


\_/F

</td>
<td>


2

</td>
<td>


module was force loaded

</td>
</tr>
<tr>
<td>


2

</td>
<td>


\_/S

</td>
<td>


4

</td>
<td>


kernel running on an out of specification system

</td>
</tr>
<tr>
<td>


3

</td>
<td>


\_/R

</td>
<td>


8

</td>
<td>


module was force unloaded

</td>
</tr>
<tr>
<td>


4

</td>
<td>


\_/M

</td>
<td>


16

</td>
<td>


processor reported a Machine Check Exception (MCE)

</td>
</tr>
<tr>
<td>


5

</td>
<td>


\_/B

</td>
<td>


32

</td>
<td>


bad page referenced or some unexpected page flags

</td>
</tr>
<tr>
<td>


6

</td>
<td>


\_/U

</td>
<td>


64

</td>
<td>


taint requested by userspace application

</td>
</tr>
<tr>
<td>


7

</td>
<td>


\_/D

</td>
<td>


128

</td>
<td>


kernel died recently, i.e. there was an OOPS or BUG

</td>
</tr>
<tr>
<td>


8

</td>
<td>


\_/A

</td>
<td>


256

</td>
<td>


ACPI table overridden by user

</td>
</tr>
<tr>
<td>


9

</td>
<td>


\_/W

</td>
<td>


512

</td>
<td>


kernel issued warning

</td>
</tr>
<tr>
<td>


10

</td>
<td>


\_/C

</td>
<td>


1024

</td>
<td>


staging driver was loaded

</td>
</tr>
<tr>
<td>


11

</td>
<td>


\_/I

</td>
<td>


2048

</td>
<td>


workaround for bug in platform firmware applied

</td>
</tr>
<tr>
<td>


12

</td>
<td>


\_/O

</td>
<td>


4096

</td>
<td>


externally-built ("out-of-tree") module was loaded

</td>
</tr>
<tr>
<td>


13

</td>
<td>


\_/E

</td>
<td>


8192

</td>
<td>


unsigned module was loaded

</td>
</tr>
<tr>
<td>


14

</td>
<td>


\_/L

</td>
<td>


16384

</td>
<td>


soft lockup occurred

</td>
</tr>
<tr>
<td>


15

</td>
<td>


\_/K

</td>
<td>


32768

</td>
<td>


kernel has been live patched

</td>
</tr>
<tr>
<td>


16

</td>
<td>


\_/X

</td>
<td>


65536

</td>
<td>


auxiliary taint, defined for and used by distros

</td>
</tr>
<tr>
<td>


17

</td>
<td>


\_/T

</td>
<td>


131072

</td>
<td>


kernel was built with the struct randomization plugin

</td>
</tr>
<tr>
<td>


18

</td>
<td>


\_/N

</td>
<td>


262144

</td>
<td>


an in-kernel test has been run

</td>
</tr>
<tr>
<td>


19

</td>
<td>


\_/J

</td>
<td>


524288

</td>
<td>


userspace used a mutating debug operation in fwctl

</td>
</tr>
</tbody>
</table>

Note: The character `_` is representing a blank in this table to make reading easier.

<a id="rst-more-detailed-explanation-for-tainting"></a>

## More detailed explanation for tainting

> 0. `G` if all modules loaded have a GPL or compatible license, `P` if any proprietary module has been loaded.  Modules without a MODULE_LICENSE or with a MODULE_LICENSE that is not recognised by insmod as GPL compatible are assumed to be proprietary.
>
> 1. `F` if any module was force loaded by `insmod -f`, `' '` if all modules were loaded normally.
>
> 2. `S` if the kernel is running on a processor or system that is out of specification: hardware has been put into an unsupported configuration, therefore proper execution cannot be guaranteed. Kernel will be tainted if, for example:
>
>    - on x86: PAE is forced through forcepae on intel CPUs (such as Pentium M) which do not report PAE but may have a functional implementation, an SMP kernel is running on non officially capable SMP Athlon CPUs, MSRs are being poked at from userspace.
>
>    - on arm: kernel running on certain CPUs (such as Keystone 2) without having certain kernel features enabled.
>
>    - on arm64: there are mismatched hardware features between CPUs, the bootloader has booted CPUs in different modes.
>
>    - certain drivers are being used on non supported architectures (such as scsi/snic on something else than x86_64, scsi/ips on non x86/x86_64/itanium, have broken firmware settings for the irqchip/irq-gic on arm64 ...).
>
>    - x86/x86_64: Microcode late loading is dangerous and will result in tainting the kernel. It requires that all CPUs rendezvous to make sure the update happens when the system is as quiescent as possible. However, a higher priority MCE/SMI/NMI can move control flow away from that rendezvous and interrupt the update, which can be detrimental to the machine.
>
> 3. `R` if a module was force unloaded by `rmmod -f`, `' '` if all modules were unloaded normally.
>
> 4. `M` if any processor has reported a Machine Check Exception, `' '` if no Machine Check Exceptions have occurred.
>
> 5. `B` If a page-release function has found a bad page reference or some unexpected page flags. This indicates a hardware problem or a kernel bug; there should be other information in the log indicating why this tainting occurred.
>
> 6. `U` if a user or user application specifically requested that the Tainted flag be set, `' '` otherwise.
>
> 7. `D` if the kernel has died recently, i.e. there was an OOPS or BUG.
>
> 8. `A` if an ACPI table has been overridden.
>
> 9. `W` if a warning has previously been issued by the kernel. (Though some warnings may set more specific taint flags.)
>
> 10. `C` if a staging driver has been loaded.
>
> 11. `I` if the kernel is working around a severe bug in the platform firmware (BIOS or similar).
>
> 12. `O` if an externally-built ("out-of-tree") module has been loaded.
>
> 13. `E` if an unsigned module has been loaded in a kernel supporting module signature.
>
> 14. `L` if a soft lockup has previously occurred on the system.
>
> 15. `K` if the kernel has been live patched.
>
> 16. `X` Auxiliary taint, defined for and used by Linux distributors.
>
> 17. `T` Kernel was build with the randstruct plugin, which can intentionally produce extremely unusual kernel structure layouts (even performance pathological ones), which is important to know when debugging. Set at build time.
>
> 18. `N` if an in-kernel test, such as a KUnit test, has been run.
>
> 19. `J` if userspace opened /dev/fwctl/\* and performed a FWTCL_RPC_DEBUG_WRITE to use the devices debugging features. Device debugging features could cause the device to malfunction in undefined ways.
