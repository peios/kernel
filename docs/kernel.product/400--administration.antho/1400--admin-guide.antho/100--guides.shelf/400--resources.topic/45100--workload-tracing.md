---
title: "Discovering Linux kernel subsystems used by a workload"
type: reference
description: "Understanding system resources necessary to build and run a workload is important."
---

<a id="rst-discovering-linux-kernel-subsystems-used-by-a-workload"></a>

<!-- SPDX-License-Identifier: (GPL-2.0+ OR CC-BY-4.0) -->

**Authors:** - Shuah Khan &lt;[skhan@linuxfoundation.org](<mailto:skhan@linuxfoundation.org>)&gt;

- Shefali Sharma &lt;[sshefali021@gmail.com](<mailto:sshefali021@gmail.com>)&gt;

**maintained-by:** Shuah Khan &lt;[skhan@linuxfoundation.org](<mailto:skhan@linuxfoundation.org>)&gt;

<a id="rst-key-points"></a>

## Key Points

> - Understanding system resources necessary to build and run a workload is important.
>
> - Linux tracing and strace can be used to discover the system resources in use by a workload. The completeness of the system usage information depends on the completeness of coverage of a workload.
>
> - Performance and security of the operating system can be analyzed with the help of tools such as: [perf](<https://man7.org/linux/man-pages/man1/perf.1.html>)<a id="rst-perf"></a>, [stress-ng](<https://www.mankier.com/1/stress-ng>)<a id="rst-stress-ng"></a>, [paxtest](<https://github.com/opntr/paxtest-freebsd>)<a id="rst-paxtest"></a>.
>
> - Once we discover and understand the workload needs, we can focus on them to avoid regressions and use it to evaluate safety considerations.

<a id="rst-methodology"></a>

## Methodology

[strace](<https://man7.org/linux/man-pages/man1/strace.1.html>)<a id="rst-strace"></a> is a diagnostic, instructional, and debugging tool and can be used to discover the system resources in use by a workload. Once we discover and understand the workload needs, we can focus on them to avoid regressions and use it to evaluate safety considerations. We use strace tool to trace workloads.

This method of tracing using strace tells us the system calls invoked by the workload and doesn't include all the system calls that can be invoked by it. In addition, this tracing method tells us just the code paths within these system calls that are invoked. As an example, if a workload opens a file and reads from it successfully, then the success path is the one that is traced. Any error paths in that system call will not be traced. If there is a workload that provides full coverage of a workload then the method outlined here will trace and find all possible code paths. The completeness of the system usage information depends on the completeness of coverage of a workload.

The goal is tracing a workload on a system running a default kernel without requiring custom kernel installs.

<a id="rst-how-do-we-gather-fine-grained-system-information"></a>

## How do we gather fine-grained system information?

strace tool can be used to trace system calls made by a process and signals it receives. System calls are the fundamental interface between an application and the operating system kernel. They enable a program to request services from the kernel. For instance, the open() system call in Linux is used to provide access to a file in the file system. strace enables us to track all the system calls made by an application. It lists all the system calls made by a process and their resulting output.

You can generate profiling data combining strace and perf record tools to record the events and information associated with a process. This provides insight into the process. "perf annotate" tool generates the statistics of each instruction of the program. This document goes over the details of how to gather fine-grained information on a workload's usage of system resources.

We used strace to trace the perf, stress-ng, paxtest workloads to illustrate our methodology to discover resources used by a workload. This process can be applied to trace other workloads.

<a id="rst-getting-the-system-ready-for-tracing"></a>

## Getting the system ready for tracing

Before we can get started we will show you how to get your system ready. We assume that you have a Linux distribution running on a physical system or a virtual machine. Most distributions will include strace command. Let’s install other tools that aren’t usually included to build Linux kernel. Please note that the following works on Debian based distributions. You might have to find equivalent packages on other Linux distributions.

Install tools to build Linux kernel and tools in kernel repository. scripts/ver_linux is a good way to check if your system already has the necessary tools:



```text
sudo apt-get install build-essential flex bison yacc
sudo apt install libelf-dev systemtap-sdt-dev libslang2-dev libperl-dev libdw-dev
```

cscope is a good tool to browse kernel sources. Let's install it now:



```text
sudo apt-get install cscope
```

Install stress-ng and paxtest:



```text
apt-get install stress-ng
apt-get install paxtest
```

<a id="rst-workload-overview"></a>

## Workload overview

As mentioned earlier, we used strace to trace perf bench, stress-ng and paxtest workloads to show how to analyze a workload and identify Linux subsystems used by these workloads. Let's start with an overview of these three workloads to get a better understanding of what they do and how to use them.

<a id="rst-perf-bench-all-workload"></a>

### perf bench (all) workload

The perf bench command contains multiple multi-threaded microkernel benchmarks for executing different subsystems in the Linux kernel and system calls. This allows us to easily measure the impact of changes, which can help mitigate performance regressions. It also acts as a common benchmarking framework, enabling developers to easily create test cases, integrate transparently, and use performance-rich tooling subsystems.

<a id="rst-stress-ng-netdev-stressor-workload"></a>

### Stress-ng netdev stressor workload

stress-ng is used for performing stress testing on the kernel. It allows you to exercise various physical subsystems of the computer, as well as interfaces of the OS kernel, using "stressor-s". They are available for CPU, CPU cache, devices, I/O, interrupts, file system, memory, network, operating system, pipelines, schedulers, and virtual machines. Please refer to the [stress-ng man-page](<https://www.mankier.com/1/stress-ng>)<a id="rst-stress-ng-man-page"></a> to find the description of all the available stressor-s. The netdev stressor starts specified number (N) of workers that exercise various netdevice ioctl commands across all the available network devices.

<a id="rst-paxtest-kiddie-workload"></a>

### paxtest kiddie workload

paxtest is a program that tests buffer overflows in the kernel. It tests kernel enforcements over memory usage. Generally, execution in some memory segments makes buffer overflows possible. It runs a set of programs that attempt to subvert memory usage. It is used as a regression test suite for PaX, but might be useful to test other memory protection patches for the kernel. We used paxtest kiddie mode which looks for simple vulnerabilities.

<a id="rst-what-is-strace-and-how-do-we-use-it"></a>

## What is strace and how do we use it?

As mentioned earlier, strace which is a useful diagnostic, instructional, and debugging tool and can be used to discover the system resources in use by a workload. It can be used:

> - To see how a process interacts with the kernel.
>
> - To see why a process is failing or hanging.
>
> - For reverse engineering a process.
>
> - To find the files on which a program depends.
>
> - For analyzing the performance of an application.
>
> - For troubleshooting various problems related to the operating system.

In addition, strace can generate run-time statistics on times, calls, and errors for each system call and report a summary when program exits, suppressing the regular output. This attempts to show system time (CPU time spent running in the kernel) independent of wall clock time. We plan to use these features to get information on workload system usage.

strace command supports basic, verbose, and stats modes. strace command when run in verbose mode gives more detailed information about the system calls invoked by a process.

Running strace -c generates a report of the percentage of time spent in each system call, the total time in seconds, the microseconds per call, the total number of calls, the count of each system call that has failed with an error and the type of system call made.

> - Usage: strace &lt;command we want to trace&gt;
>
> - Verbose mode usage: strace -v &lt;command&gt;
>
> - Gather statistics: strace -c &lt;command&gt;

We used the “-c” option to gather fine-grained run-time statistics in use by three workloads we have chose for this analysis.

> - perf
>
> - stress-ng
>
> - paxtest

<a id="rst-what-is-cscope-and-how-do-we-use-it"></a>

## What is cscope and how do we use it?

Now let’s look at [cscope](<https://cscope.sourceforge.net/>)<a id="rst-cscope"></a>, a command line tool for browsing C, C++ or Java code-bases. We can use it to find all the references to a symbol, global definitions, functions called by a function, functions calling a function, text strings, regular expression patterns, files including a file.

We can use cscope to find which system call belongs to which subsystem. This way we can find the kernel subsystems used by a process when it is executed.

Let’s checkout the latest Linux repository and build cscope database:



```text
git clone git://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git linux
cd linux
cscope -R -p10  # builds cscope.out database before starting browse session
cscope -d -p10  # starts browse session on cscope.out database
```

Note: Run "cscope -R -p10" to build the database and "cscope -d -p10" to enter into the browsing session. cscope by default uses the cscope.out database. To get out of this mode press ctrl+d. -p option is used to specify the number of file path components to display. -p10 is optimal for browsing kernel sources.

<a id="rst-what-is-perf-and-how-do-we-use-it"></a>

## What is perf and how do we use it?

Perf is an analysis tool based on Linux 2.6+ systems, which abstracts the CPU hardware difference in performance measurement in Linux, and provides a simple command line interface. Perf is based on the perf_events interface exported by the kernel. It is very useful for profiling the system and finding performance bottlenecks in an application.

If you haven't already checked out the Linux mainline repository, you can do so and then build kernel and perf tool:



```text
git clone git://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git linux
cd linux
make -j3 all
cd tools/perf
make
```

Note: The perf command can be built without building the kernel in the repository and can be run on older kernels. However matching the kernel and perf revisions gives more accurate information on the subsystem usage.

We used "perf stat" and "perf bench" options. For a detailed information on the perf tool, run "perf -h".

<a id="rst-perf-stat"></a>

### perf stat

The perf stat command generates a report of various hardware and software events. It does so with the help of hardware counter registers found in modern CPUs that keep the count of these activities. "perf stat cal" shows stats for cal command.

<a id="rst-perf-bench"></a>

### Perf bench

The perf bench command contains multiple multi-threaded microkernel benchmarks for executing different subsystems in the Linux kernel and system calls. This allows us to easily measure the impact of changes, which can help mitigate performance regressions. It also acts as a common benchmarking framework, enabling developers to easily create test cases, integrate transparently, and use performance-rich tooling.

"perf bench all" command runs the following benchmarks:

> - sched/messaging
>
> - sched/pipe
>
> - syscall/basic
>
> - mem/memcpy
>
> - mem/memset

<a id="rst-what-is-stress-ng-and-how-do-we-use-it"></a>

## What is stress-ng and how do we use it?

As mentioned earlier, stress-ng is used for performing stress testing on the kernel. It allows you to exercise various physical subsystems of the computer, as well as interfaces of the OS kernel, using stressor-s. They are available for CPU, CPU cache, devices, I/O, interrupts, file system, memory, network, operating system, pipelines, schedulers, and virtual machines.

The netdev stressor starts N workers that exercise various netdevice ioctl commands across all the available network devices. The following ioctls are exercised:

> - SIOCGIFCONF, SIOCGIFINDEX, SIOCGIFNAME, SIOCGIFFLAGS
>
> - SIOCGIFADDR, SIOCGIFNETMASK, SIOCGIFMETRIC, SIOCGIFMTU
>
> - SIOCGIFHWADDR, SIOCGIFMAP, SIOCGIFTXQLEN

The following command runs the stressor:



```text
stress-ng --netdev 1 -t 60 --metrics command.
```

We can use the perf record command to record the events and information associated with a process. This command records the profiling data in the perf.data file in the same directory.

Using the following commands you can record the events associated with the netdev stressor, view the generated report perf.data and annotate the to view the statistics of each instruction of the program:



```text
perf record stress-ng --netdev 1 -t 60 --metrics command.
perf report
perf annotate
```

<a id="rst-what-is-paxtest-and-how-do-we-use-it"></a>

## What is paxtest and how do we use it?

paxtest is a program that tests buffer overflows in the kernel. It tests kernel enforcements over memory usage. Generally, execution in some memory segments makes buffer overflows possible. It runs a set of programs that attempt to subvert memory usage. It is used as a regression test suite for PaX, and will be useful to test other memory protection patches for the kernel.

paxtest provides kiddie and blackhat modes. The paxtest kiddie mode runs in normal mode, whereas the blackhat mode tries to get around the protection of the kernel testing for vulnerabilities. We focus on the kiddie mode here and combine "paxtest kiddie" run with "perf record" to collect CPU stack traces for the paxtest kiddie run to see which function is calling other functions in the performance profile. Then the "dwarf" (DWARF's Call Frame Information) mode can be used to unwind the stack.

The following command can be used to view resulting report in call-graph format:



```text
perf record --call-graph dwarf paxtest kiddie
perf report --stdio
```

<a id="rst-tracing-workloads"></a>

## Tracing workloads

Now that we understand the workloads, let's start tracing them.

<a id="rst-tracing-perf-bench-all-workload"></a>

### Tracing perf bench all workload

Run the following command to trace perf bench all workload:



```text
strace -c perf bench all
```

**System Calls made by the workload**

The below table shows the system calls invoked by the workload, number of times each system call is invoked, and the corresponding Linux subsystem.


<table>
<thead>
<tr>
<th>


System Call

</th>
<th>


\# calls

</th>
<th>


Linux Subsystem

</th>
<th>


System Call (API)

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


getppid

</td>
<td>


10000001

</td>
<td>


Process Mgmt

</td>
<td>


sys_getpid()

</td>
</tr>
<tr>
<td>


clone

</td>
<td>


1077

</td>
<td>


Process Mgmt.

</td>
<td>


sys_clone()

</td>
</tr>
<tr>
<td>


prctl

</td>
<td>


23

</td>
<td>


Process Mgmt.

</td>
<td>


sys_prctl()

</td>
</tr>
<tr>
<td>


prlimit64

</td>
<td>


7

</td>
<td>


Process Mgmt.

</td>
<td>


sys_prlimit64()

</td>
</tr>
<tr>
<td>


getpid

</td>
<td>


10

</td>
<td>


Process Mgmt.

</td>
<td>


sys_getpid()

</td>
</tr>
<tr>
<td>


uname

</td>
<td>


3

</td>
<td>


Process Mgmt.

</td>
<td>


sys_uname()

</td>
</tr>
<tr>
<td>


sysinfo

</td>
<td>


1

</td>
<td>


Process Mgmt.

</td>
<td>


sys_sysinfo()

</td>
</tr>
<tr>
<td>


getuid

</td>
<td>


1

</td>
<td>


Process Mgmt.

</td>
<td>


sys_getuid()

</td>
</tr>
<tr>
<td>


getgid

</td>
<td>


1

</td>
<td>


Process Mgmt.

</td>
<td>


sys_getgid()

</td>
</tr>
<tr>
<td>


geteuid

</td>
<td>


1

</td>
<td>


Process Mgmt.

</td>
<td>


sys_geteuid()

</td>
</tr>
<tr>
<td>


getegid

</td>
<td>


1

</td>
<td>


Process Mgmt.

</td>
<td>


sys_getegid

</td>
</tr>
<tr>
<td>


close

</td>
<td>


49951

</td>
<td>


Filesystem

</td>
<td>


sys_close()

</td>
</tr>
<tr>
<td>


pipe

</td>
<td>


604

</td>
<td>


Filesystem

</td>
<td>


sys_pipe()

</td>
</tr>
<tr>
<td>


openat

</td>
<td>


48560

</td>
<td>


Filesystem

</td>
<td>


sys_opennat()

</td>
</tr>
<tr>
<td>


fstat

</td>
<td>


8338

</td>
<td>


Filesystem

</td>
<td>


sys_fstat()

</td>
</tr>
<tr>
<td>


stat

</td>
<td>


1573

</td>
<td>


Filesystem

</td>
<td>


sys_stat()

</td>
</tr>
<tr>
<td>


pread64

</td>
<td>


9646

</td>
<td>


Filesystem

</td>
<td>


sys_pread64()

</td>
</tr>
<tr>
<td>


getdents64

</td>
<td>


1873

</td>
<td>


Filesystem

</td>
<td>


sys_getdents64()

</td>
</tr>
<tr>
<td>


access

</td>
<td>


3

</td>
<td>


Filesystem

</td>
<td>


sys_access()

</td>
</tr>
<tr>
<td>


lstat

</td>
<td>


1880

</td>
<td>


Filesystem

</td>
<td>


sys_lstat()

</td>
</tr>
<tr>
<td>


lseek

</td>
<td>


6

</td>
<td>


Filesystem

</td>
<td>


sys_lseek()

</td>
</tr>
<tr>
<td>


ioctl

</td>
<td>


3

</td>
<td>


Filesystem

</td>
<td>


sys_ioctl()

</td>
</tr>
<tr>
<td>


dup2

</td>
<td>


1

</td>
<td>


Filesystem

</td>
<td>


sys_dup2()

</td>
</tr>
<tr>
<td>


execve

</td>
<td>


2

</td>
<td>


Filesystem

</td>
<td>


sys_execve()

</td>
</tr>
<tr>
<td>


fcntl

</td>
<td>


8779

</td>
<td>


Filesystem

</td>
<td>


sys_fcntl()

</td>
</tr>
<tr>
<td>


statfs

</td>
<td>


1

</td>
<td>


Filesystem

</td>
<td>


sys_statfs()

</td>
</tr>
<tr>
<td>


epoll_create

</td>
<td>


2

</td>
<td>


Filesystem

</td>
<td>


sys_epoll_create()

</td>
</tr>
<tr>
<td>


epoll_ctl

</td>
<td>


64

</td>
<td>


Filesystem

</td>
<td>


sys_epoll_ctl()

</td>
</tr>
<tr>
<td>


newfstatat

</td>
<td>


8318

</td>
<td>


Filesystem

</td>
<td>


sys_newfstatat()

</td>
</tr>
<tr>
<td>


eventfd2

</td>
<td>


192

</td>
<td>


Filesystem

</td>
<td>


sys_eventfd2()

</td>
</tr>
<tr>
<td>


mmap

</td>
<td>


243

</td>
<td>


Memory Mgmt.

</td>
<td>


sys_mmap()

</td>
</tr>
<tr>
<td>


mprotect

</td>
<td>


32

</td>
<td>


Memory Mgmt.

</td>
<td>


sys_mprotect()

</td>
</tr>
<tr>
<td>


brk

</td>
<td>


21

</td>
<td>


Memory Mgmt.

</td>
<td>


sys_brk()

</td>
</tr>
<tr>
<td>


munmap

</td>
<td>


128

</td>
<td>


Memory Mgmt.

</td>
<td>


sys_munmap()

</td>
</tr>
<tr>
<td>


set_mempolicy

</td>
<td>


156

</td>
<td>


Memory Mgmt.

</td>
<td>


sys_set_mempolicy()

</td>
</tr>
<tr>
<td>


set_tid_address

</td>
<td>


1

</td>
<td>


Process Mgmt.

</td>
<td>


sys_set_tid_address()

</td>
</tr>
<tr>
<td>


set_robust_list

</td>
<td>


1

</td>
<td>


Futex

</td>
<td>


sys_set_robust_list()

</td>
</tr>
<tr>
<td>


futex

</td>
<td>


341

</td>
<td>


Futex

</td>
<td>


sys_futex()

</td>
</tr>
<tr>
<td>


sched_getaffinity

</td>
<td>


79

</td>
<td>


Scheduler

</td>
<td>


sys_sched_getaffinity()

</td>
</tr>
<tr>
<td>


sched_setaffinity

</td>
<td>


223

</td>
<td>


Scheduler

</td>
<td>


sys_sched_setaffinity()

</td>
</tr>
<tr>
<td>


socketpair

</td>
<td>


202

</td>
<td>


Network

</td>
<td>


sys_socketpair()

</td>
</tr>
<tr>
<td>


rt_sigprocmask

</td>
<td>


21

</td>
<td>


Signal

</td>
<td>


sys_rt_sigprocmask()

</td>
</tr>
<tr>
<td>


rt_sigaction

</td>
<td>


36

</td>
<td>


Signal

</td>
<td>


sys_rt_sigaction()

</td>
</tr>
<tr>
<td>


rt_sigreturn

</td>
<td>


2

</td>
<td>


Signal

</td>
<td>


sys_rt_sigreturn()

</td>
</tr>
<tr>
<td>


wait4

</td>
<td>


889

</td>
<td>


Time

</td>
<td>


sys_wait4()

</td>
</tr>
<tr>
<td>


clock_nanosleep

</td>
<td>


37

</td>
<td>


Time

</td>
<td>


sys_clock_nanosleep()

</td>
</tr>
<tr>
<td>


capget

</td>
<td>


4

</td>
<td>


Capability

</td>
<td>


sys_capget()

</td>
</tr>
</tbody>
</table>

<a id="rst-tracing-stress-ng-netdev-stressor-workload"></a>

### Tracing stress-ng netdev stressor workload

Run the following command to trace stress-ng netdev stressor workload:



```text
strace -c  stress-ng --netdev 1 -t 60 --metrics
```

**System Calls made by the workload**

The below table shows the system calls invoked by the workload, number of times each system call is invoked, and the corresponding Linux subsystem.


<table>
<thead>
<tr>
<th>


System Call

</th>
<th>


\# calls

</th>
<th>


Linux Subsystem

</th>
<th>


System Call (API)

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


openat

</td>
<td>


74

</td>
<td>


Filesystem

</td>
<td>


sys_openat()

</td>
</tr>
<tr>
<td>


close

</td>
<td>


75

</td>
<td>


Filesystem

</td>
<td>


sys_close()

</td>
</tr>
<tr>
<td>


read

</td>
<td>


58

</td>
<td>


Filesystem

</td>
<td>


sys_read()

</td>
</tr>
<tr>
<td>


fstat

</td>
<td>


20

</td>
<td>


Filesystem

</td>
<td>


sys_fstat()

</td>
</tr>
<tr>
<td>


flock

</td>
<td>


10

</td>
<td>


Filesystem

</td>
<td>


sys_flock()

</td>
</tr>
<tr>
<td>


write

</td>
<td>


7

</td>
<td>


Filesystem

</td>
<td>


sys_write()

</td>
</tr>
<tr>
<td>


getdents64

</td>
<td>


8

</td>
<td>


Filesystem

</td>
<td>


sys_getdents64()

</td>
</tr>
<tr>
<td>


pread64

</td>
<td>


8

</td>
<td>


Filesystem

</td>
<td>


sys_pread64()

</td>
</tr>
<tr>
<td>


lseek

</td>
<td>


1

</td>
<td>


Filesystem

</td>
<td>


sys_lseek()

</td>
</tr>
<tr>
<td>


access

</td>
<td>


2

</td>
<td>


Filesystem

</td>
<td>


sys_access()

</td>
</tr>
<tr>
<td>


getcwd

</td>
<td>


1

</td>
<td>


Filesystem

</td>
<td>


sys_getcwd()

</td>
</tr>
<tr>
<td>


execve

</td>
<td>


1

</td>
<td>


Filesystem

</td>
<td>


sys_execve()

</td>
</tr>
<tr>
<td>


mmap

</td>
<td>


61

</td>
<td>


Memory Mgmt.

</td>
<td>


sys_mmap()

</td>
</tr>
<tr>
<td>


munmap

</td>
<td>


3

</td>
<td>


Memory Mgmt.

</td>
<td>


sys_munmap()

</td>
</tr>
<tr>
<td>


mprotect

</td>
<td>


20

</td>
<td>


Memory Mgmt.

</td>
<td>


sys_mprotect()

</td>
</tr>
<tr>
<td>


mlock

</td>
<td>


2

</td>
<td>


Memory Mgmt.

</td>
<td>


sys_mlock()

</td>
</tr>
<tr>
<td>


brk

</td>
<td>


3

</td>
<td>


Memory Mgmt.

</td>
<td>


sys_brk()

</td>
</tr>
<tr>
<td>


rt_sigaction

</td>
<td>


21

</td>
<td>


Signal

</td>
<td>


sys_rt_sigaction()

</td>
</tr>
<tr>
<td>


rt_sigprocmask

</td>
<td>


1

</td>
<td>


Signal

</td>
<td>


sys_rt_sigprocmask()

</td>
</tr>
<tr>
<td>


sigaltstack

</td>
<td>


1

</td>
<td>


Signal

</td>
<td>


sys_sigaltstack()

</td>
</tr>
<tr>
<td>


rt_sigreturn

</td>
<td>


1

</td>
<td>


Signal

</td>
<td>


sys_rt_sigreturn()

</td>
</tr>
<tr>
<td>


getpid

</td>
<td>


8

</td>
<td>


Process Mgmt.

</td>
<td>


sys_getpid()

</td>
</tr>
<tr>
<td>


prlimit64

</td>
<td>


5

</td>
<td>


Process Mgmt.

</td>
<td>


sys_prlimit64()

</td>
</tr>
<tr>
<td>


arch_prctl

</td>
<td>


2

</td>
<td>


Process Mgmt.

</td>
<td>


sys_arch_prctl()

</td>
</tr>
<tr>
<td>


sysinfo

</td>
<td>


2

</td>
<td>


Process Mgmt.

</td>
<td>


sys_sysinfo()

</td>
</tr>
<tr>
<td>


getuid

</td>
<td>


2

</td>
<td>


Process Mgmt.

</td>
<td>


sys_getuid()

</td>
</tr>
<tr>
<td>


uname

</td>
<td>


1

</td>
<td>


Process Mgmt.

</td>
<td>


sys_uname()

</td>
</tr>
<tr>
<td>


setpgid

</td>
<td>


1

</td>
<td>


Process Mgmt.

</td>
<td>


sys_setpgid()

</td>
</tr>
<tr>
<td>


getrusage

</td>
<td>


1

</td>
<td>


Process Mgmt.

</td>
<td>


sys_getrusage()

</td>
</tr>
<tr>
<td>


geteuid

</td>
<td>


1

</td>
<td>


Process Mgmt.

</td>
<td>


sys_geteuid()

</td>
</tr>
<tr>
<td>


getppid

</td>
<td>


1

</td>
<td>


Process Mgmt.

</td>
<td>


sys_getppid()

</td>
</tr>
<tr>
<td>


sendto

</td>
<td>


3

</td>
<td>


Network

</td>
<td>


sys_sendto()

</td>
</tr>
<tr>
<td>


connect

</td>
<td>


1

</td>
<td>


Network

</td>
<td>


sys_connect()

</td>
</tr>
<tr>
<td>


socket

</td>
<td>


1

</td>
<td>


Network

</td>
<td>


sys_socket()

</td>
</tr>
<tr>
<td>


clone

</td>
<td>


1

</td>
<td>


Process Mgmt.

</td>
<td>


sys_clone()

</td>
</tr>
<tr>
<td>


set_tid_address

</td>
<td>


1

</td>
<td>


Process Mgmt.

</td>
<td>


sys_set_tid_address()

</td>
</tr>
<tr>
<td>


wait4

</td>
<td>


2

</td>
<td>


Time

</td>
<td>


sys_wait4()

</td>
</tr>
<tr>
<td>


alarm

</td>
<td>


1

</td>
<td>


Time

</td>
<td>


sys_alarm()

</td>
</tr>
<tr>
<td>


set_robust_list

</td>
<td>


1

</td>
<td>


Futex

</td>
<td>


sys_set_robust_list()

</td>
</tr>
</tbody>
</table>

<a id="rst-tracing-paxtest-kiddie-workload"></a>

### Tracing paxtest kiddie workload

Run the following command to trace paxtest kiddie workload:



```text
strace -c paxtest kiddie
```

**System Calls made by the workload**

The below table shows the system calls invoked by the workload, number of times each system call is invoked, and the corresponding Linux subsystem.


<table>
<thead>
<tr>
<th>


System Call

</th>
<th>


\# calls

</th>
<th>


Linux Subsystem

</th>
<th>


System Call (API)

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


read

</td>
<td>


3

</td>
<td>


Filesystem

</td>
<td>


sys_read()

</td>
</tr>
<tr>
<td>


write

</td>
<td>


11

</td>
<td>


Filesystem

</td>
<td>


sys_write()

</td>
</tr>
<tr>
<td>


close

</td>
<td>


41

</td>
<td>


Filesystem

</td>
<td>


sys_close()

</td>
</tr>
<tr>
<td>


stat

</td>
<td>


24

</td>
<td>


Filesystem

</td>
<td>


sys_stat()

</td>
</tr>
<tr>
<td>


fstat

</td>
<td>


2

</td>
<td>


Filesystem

</td>
<td>


sys_fstat()

</td>
</tr>
<tr>
<td>


pread64

</td>
<td>


6

</td>
<td>


Filesystem

</td>
<td>


sys_pread64()

</td>
</tr>
<tr>
<td>


access

</td>
<td>


1

</td>
<td>


Filesystem

</td>
<td>


sys_access()

</td>
</tr>
<tr>
<td>


pipe

</td>
<td>


1

</td>
<td>


Filesystem

</td>
<td>


sys_pipe()

</td>
</tr>
<tr>
<td>


dup2

</td>
<td>


24

</td>
<td>


Filesystem

</td>
<td>


sys_dup2()

</td>
</tr>
<tr>
<td>


execve

</td>
<td>


1

</td>
<td>


Filesystem

</td>
<td>


sys_execve()

</td>
</tr>
<tr>
<td>


fcntl

</td>
<td>


26

</td>
<td>


Filesystem

</td>
<td>


sys_fcntl()

</td>
</tr>
<tr>
<td>


openat

</td>
<td>


14

</td>
<td>


Filesystem

</td>
<td>


sys_openat()

</td>
</tr>
<tr>
<td>


rt_sigaction

</td>
<td>


7

</td>
<td>


Signal

</td>
<td>


sys_rt_sigaction()

</td>
</tr>
<tr>
<td>


rt_sigreturn

</td>
<td>


38

</td>
<td>


Signal

</td>
<td>


sys_rt_sigreturn()

</td>
</tr>
<tr>
<td>


clone

</td>
<td>


38

</td>
<td>


Process Mgmt.

</td>
<td>


sys_clone()

</td>
</tr>
<tr>
<td>


wait4

</td>
<td>


44

</td>
<td>


Time

</td>
<td>


sys_wait4()

</td>
</tr>
<tr>
<td>


mmap

</td>
<td>


7

</td>
<td>


Memory Mgmt.

</td>
<td>


sys_mmap()

</td>
</tr>
<tr>
<td>


mprotect

</td>
<td>


3

</td>
<td>


Memory Mgmt.

</td>
<td>


sys_mprotect()

</td>
</tr>
<tr>
<td>


munmap

</td>
<td>


1

</td>
<td>


Memory Mgmt.

</td>
<td>


sys_munmap()

</td>
</tr>
<tr>
<td>


brk

</td>
<td>


3

</td>
<td>


Memory Mgmt.

</td>
<td>


sys_brk()

</td>
</tr>
<tr>
<td>


getpid

</td>
<td>


1

</td>
<td>


Process Mgmt.

</td>
<td>


sys_getpid()

</td>
</tr>
<tr>
<td>


getuid

</td>
<td>


1

</td>
<td>


Process Mgmt.

</td>
<td>


sys_getuid()

</td>
</tr>
<tr>
<td>


getgid

</td>
<td>


1

</td>
<td>


Process Mgmt.

</td>
<td>


sys_getgid()

</td>
</tr>
<tr>
<td>


geteuid

</td>
<td>


2

</td>
<td>


Process Mgmt.

</td>
<td>


sys_geteuid()

</td>
</tr>
<tr>
<td>


getegid

</td>
<td>


1

</td>
<td>


Process Mgmt.

</td>
<td>


sys_getegid()

</td>
</tr>
<tr>
<td>


getppid

</td>
<td>


1

</td>
<td>


Process Mgmt.

</td>
<td>


sys_getppid()

</td>
</tr>
<tr>
<td>


arch_prctl

</td>
<td>


2

</td>
<td>


Process Mgmt.

</td>
<td>


sys_arch_prctl()

</td>
</tr>
</tbody>
</table>

<a id="rst-conclusion"></a>

## Conclusion

This document is intended to be used as a guide on how to gather fine-grained information on the resources in use by workloads using strace.

<a id="rst-references"></a>

## References

> - [Discovery Linux Kernel Subsystems used by OpenAPS](<https://elisa.tech/blog/2022/02/02/discovery-linux-kernel-subsystems-used-by-openaps>)<a id="rst-discovery-linux-kernel-subsystems-used-by-openaps"></a>
>
> - [ELISA-White-Papers-Discovering Linux kernel subsystems used by a workload](<https://github.com/elisa-tech/ELISA-White-Papers/blob/master/Processes/Discovering_Linux_kernel_subsystems_used_by_a_workload.md>)<a id="rst-elisa-white-papers-discovering-linux-kernel-subsystems-used-by-a-workload"></a>
>
> - [strace](<https://man7.org/linux/man-pages/man1/strace.1.html>)<a id="rst-strace-1"></a>
>
> - [perf](<https://man7.org/linux/man-pages/man1/perf.1.html>)<a id="rst-perf-1"></a>
>
> - [paxtest README](<https://github.com/opntr/paxtest-freebsd/blob/hardenedbsd/0.9.14-hbsd/README>)<a id="rst-paxtest-readme"></a>
>
> - [stress-ng](<https://www.mankier.com/1/stress-ng>)<a id="rst-stress-ng-1"></a>
>
> - [Monitoring and managing system status and performance](<https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/monitoring_and_managing_system_status_and_performance/index>)<a id="rst-monitoring-and-managing-system-status-and-performance"></a>
