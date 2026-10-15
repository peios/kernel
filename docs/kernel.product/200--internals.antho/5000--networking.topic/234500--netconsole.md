---
title: "Netconsole"
type: reference
description: "started by Ingo Molnar <mingo@redhat.com>, 2001.09.17"
---

<a id="rst-netconsole"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

started by Ingo Molnar &lt;[mingo@redhat.com](<mailto:mingo@redhat.com>)&gt;, 2001.09.17

2.6 port and netpoll api by Matt Mackall &lt;[mpm@selenic.com](<mailto:mpm@selenic.com>)&gt;, Sep 9 2003

IPv6 support by Cong Wang &lt;[xiyou.wangcong@gmail.com](<mailto:xiyou.wangcong@gmail.com>)&gt;, Jan 1 2013

Extended console support by Tejun Heo &lt;[tj@kernel.org](<mailto:tj@kernel.org>)&gt;, May 1 2015

Release prepend support by Breno Leitao &lt;[leitao@debian.org](<mailto:leitao@debian.org>)&gt;, Jul 7 2023

Userdata append support by Matthew Wood &lt;[thepacketgeek@gmail.com](<mailto:thepacketgeek@gmail.com>)&gt;, Jan 22 2024

Sysdata append support by Breno Leitao &lt;[leitao@debian.org](<mailto:leitao@debian.org>)&gt;, Jan 15 2025

<a id="rst-introduction"></a>

## Introduction:

This module logs kernel printk messages over UDP allowing debugging of problem where disk logging fails and serial consoles are impractical.

It can be used either built-in or as a module. As a built-in, netconsole initializes immediately after NIC cards and will bring up the specified interface as soon as possible. While this doesn't allow capture of early kernel panics, it does capture most of the boot process.

<a id="rst-sender-and-receiver-configuration"></a>

## Sender and receiver configuration:

It takes a string configuration parameter "netconsole" in the following format:



```text
netconsole=[+][r][src-port]@[src-ip]/[<dev>],[tgt-port]@<tgt-ip>/[tgt-macaddr]

  where
       +             if present, enable extended console support
       r             if present, prepend kernel version (release) to the message
       src-port      source for UDP packets (defaults to 6665)
       src-ip        source IP to use (interface address)
       dev           network interface name (eth0) or MAC address
       tgt-port      port for logging agent (6666)
       tgt-ip        IP address for logging agent
       tgt-macaddr   ethernet MAC address for logging agent (broadcast)
```

Examples:



```text
linux netconsole=4444@10.0.0.1/eth1,9353@10.0.0.2/12:34:56:78:9a:bc
```

or:



```text
insmod netconsole netconsole=@/,@10.0.0.2/
```

or using IPv6:



```text
insmod netconsole netconsole=@/,@fd00:1:2:3::1/
```

or using a MAC address to select the egress interface:



```text
linux netconsole=4444@10.0.0.1/22:33:44:55:66:77,9353@10.0.0.2/12:34:56:78:9a:bc
```

It also supports logging to multiple remote agents by specifying parameters for the multiple agents separated by semicolons and the complete string enclosed in "quotes", thusly:



```text
modprobe netconsole netconsole="@/,@10.0.0.2/;@/eth1,6892@10.0.0.3/"
```

Built-in netconsole starts immediately after the TCP stack is initialized and attempts to bring up the supplied dev at the supplied address.

The remote host has several options to receive the kernel messages, for example:

1. syslogd

2. netcat

   On distributions using a BSD-based netcat version (e.g. Fedora, openSUSE and Ubuntu) the listening port must be specified without the -p switch:



   ```text
   nc -u -l -p <port>' / 'nc -u -l <port>
   ```

   or:



   ```text
   netcat -u -l -p <port>' / 'netcat -u -l <port>
   ```

3. socat



```text
socat udp-recv:<port> -
```

<a id="rst-dynamic-reconfiguration"></a>

## Dynamic reconfiguration:

Dynamic reconfigurability is a useful addition to netconsole that enables remote logging targets to be dynamically added, removed, or have their parameters reconfigured at runtime from a configfs-based userspace interface.

To include this feature, select CONFIG_NETCONSOLE_DYNAMIC when building the netconsole module (or kernel, if netconsole is built-in).

Some examples follow (where configfs is mounted at the /sys/kernel/config mountpoint).

To add a remote logging target (target names can be arbitrary):



```text
cd /sys/kernel/config/netconsole/
mkdir target1
```

Note that newly created targets have default parameter values (as mentioned above) and are disabled by default -- they must first be enabled by writing "1" to the "enabled" attribute (usually after setting parameters accordingly) as described below.

To remove a target:



```text
rmdir /sys/kernel/config/netconsole/othertarget/
```

The interface exposes these parameters of a netconsole target to userspace:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> enabled
>
> </td>
> <td>
>
>
> Is this target currently enabled?
>
> </td>
> <td>
>
>
> (read-write)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> extended
>
> </td>
> <td>
>
>
> Extended mode enabled
>
> </td>
> <td>
>
>
> (read-write)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> release
>
> </td>
> <td>
>
>
> Prepend kernel release to message
>
> </td>
> <td>
>
>
> (read-write)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> dev_name
>
> </td>
> <td>
>
>
> Local network interface name
>
> </td>
> <td>
>
>
> (read-write)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> local_port
>
> </td>
> <td>
>
>
> Source UDP port to use
>
> </td>
> <td>
>
>
> (read-write)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> remote_port
>
> </td>
> <td>
>
>
> Remote agent's UDP port
>
> </td>
> <td>
>
>
> (read-write)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> local_ip
>
> </td>
> <td>
>
>
> Source IP address to use
>
> </td>
> <td>
>
>
> (read-write)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> remote_ip
>
> </td>
> <td>
>
>
> Remote agent's IP address
>
> </td>
> <td>
>
>
> (read-write)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> local_mac
>
> </td>
> <td>
>
>
> Local interface's MAC address
>
> </td>
> <td>
>
>
> (read-only)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> remote_mac
>
> </td>
> <td>
>
>
> Remote agent's MAC address
>
> </td>
> <td>
>
>
> (read-write)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> transmit_errors
>
> </td>
> <td>
>
>
> Number of packet send errors
>
> </td>
> <td>
>
>
> (read-only)
>
> </td>
> </tr>
> </tbody>
> </table>

The "enabled" attribute is also used to control whether the parameters of a target can be updated or not -- you can modify the parameters of only disabled targets (i.e. if "enabled" is 0).

To update a target's parameters:



```text
cat enabled                            # check if enabled is 1
echo 0 > enabled                       # disable the target (if required)
echo eth2 > dev_name                   # set local interface
echo 10.0.0.4 > remote_ip              # update some parameter
echo cb:a9:87:65:43:21 > remote_mac    # update more parameters
echo 1 > enabled                       # enable target again
```

You can also update the local interface dynamically. This is especially useful if you want to use interfaces that have newly come up (and may not have existed when netconsole was loaded / initialized).

Netconsole targets defined at boot time (or module load time) with the `netconsole=` param are assigned the name `cmdline<index>`.  For example, the first target in the parameter is named `cmdline0`.  You can control and modify these targets by creating configfs directories with the matching name.

Let's suppose you have two netconsole targets defined at boot time:



```text
netconsole=4444@10.0.0.1/eth1,9353@10.0.0.2/12:34:56:78:9a:bc;4444@10.0.0.1/eth1,9353@10.0.0.3/12:34:56:78:9a:bc
```

You can modify these targets in runtime by creating the following targets:



```text
mkdir cmdline0
cat cmdline0/remote_ip
10.0.0.2

mkdir cmdline1
cat cmdline1/remote_ip
10.0.0.3
```

<a id="rst-append-user-data"></a>

### Append User Data

Custom user data can be appended to the end of messages with netconsole dynamic configuration enabled. User data entries can be modified without changing the "enabled" attribute of a target.

Directories (keys) under `userdata` are limited to 53 character length, and data in `userdata/<key>/value` are limited to 200 bytes:



```text
cd /sys/kernel/config/netconsole && mkdir cmdline0
cd cmdline0
mkdir userdata/foo
echo bar > userdata/foo/value
mkdir userdata/qux
echo baz > userdata/qux/value
```

Messages will now include this additional user data:



```text
echo "This is a message" > /dev/kmsg
```

Sends:



```text
12,607,22085407756,-;This is a message
 foo=bar
 qux=baz
```

Preview the userdata that will be appended with:



```text
cd /sys/kernel/config/netconsole/cmdline0/userdata
for f in `ls userdata`; do echo $f=$(cat userdata/$f/value); done
```

If a `userdata` entry is created but no data is written to the `value` file, the entry will be omitted from netconsole messages:



```text
cd /sys/kernel/config/netconsole && mkdir cmdline0
cd cmdline0
mkdir userdata/foo
echo bar > userdata/foo/value
mkdir userdata/qux
```

The `qux` key is omitted since it has no value:



```text
echo "This is a message" > /dev/kmsg
12,607,22085407756,-;This is a message
 foo=bar
```

Delete `userdata` entries with `rmdir`:



```text
rmdir /sys/kernel/config/netconsole/cmdline0/userdata/qux
```

> [!WARNING]
>
> When writing strings to user data values, input is broken up per line in configfs store calls and this can cause confusing behavior:
>
>
>
> ```text
> mkdir userdata/testing
> printf "val1\nval2" > userdata/testing/value
> # userdata store value is called twice, first with "val1\n" then "val2"
> # so "val2" is stored, being the last value stored
> cat userdata/testing/value
> val2
> ```
>
> It is recommended to not write user data values with newlines.

<a id="rst-task-name-auto-population-in-userdata"></a>

### Task name auto population in userdata

Inside the netconsole configfs hierarchy, there is a file called `taskname_enabled` under the `userdata` directory. This file is used to enable or disable the automatic task name population feature. This feature automatically populates the current task name that is scheduled in the CPU sneding the message.

To enable task name auto-population:



```text
echo 1 > /sys/kernel/config/netconsole/target1/userdata/taskname_enabled
```

When this option is enabled, the netconsole messages will include an additional line in the userdata field with the format `taskname=<task name>`. This allows the receiver of the netconsole messages to easily find which application was currently scheduled when that message was generated, providing extra context for kernel messages and helping to categorize them.

Example:



```text
echo "This is a message" > /dev/kmsg
12,607,22085407756,-;This is a message
 taskname=echo
```

In this example, the message was generated while "echo" was the current scheduled process.

<a id="rst-kernel-release-auto-population-in-userdata"></a>

### Kernel release auto population in userdata

Within the netconsole configfs hierarchy, there is a file named `release_enabled` located in the `userdata` directory. This file controls the kernel release (version) auto-population feature, which appends the kernel release information to userdata dictionary in every message sent.

To enable the release auto-population:



```text
echo 1 > /sys/kernel/config/netconsole/target1/userdata/release_enabled
```

Example:



```text
echo "This is a message" > /dev/kmsg
12,607,22085407756,-;This is a message
 release=6.14.0-rc6-01219-g3c027fbd941d
```

> [!NOTE]
>
> This feature provides the same data as the "release prepend" feature. However, in this case, the release information is appended to the userdata dictionary rather than being included in the message header.

<a id="rst-cpu-number-auto-population-in-userdata"></a>

### CPU number auto population in userdata

Inside the netconsole configfs hierarchy, there is a file called `cpu_nr` under the `userdata` directory. This file is used to enable or disable the automatic CPU number population feature. This feature automatically populates the CPU number that is sending the message.

To enable the CPU number auto-population:



```text
echo 1 > /sys/kernel/config/netconsole/target1/userdata/cpu_nr
```

When this option is enabled, the netconsole messages will include an additional line in the userdata field with the format `cpu=<cpu_number>`. This allows the receiver of the netconsole messages to easily differentiate and demultiplex messages originating from different CPUs, which is particularly useful when dealing with parallel log output.

Example:



```text
echo "This is a message" > /dev/kmsg
12,607,22085407756,-;This is a message
 cpu=42
```

In this example, the message was sent by CPU 42.

> [!NOTE]
>
> If the user has set a conflicting `cpu` key in the userdata dictionary, both keys will be reported, with the kernel-populated entry appearing after the user one. For example:
>
>
>
> ```text
> # User-defined CPU entry
> mkdir -p /sys/kernel/config/netconsole/target1/userdata/cpu
> echo "1" > /sys/kernel/config/netconsole/target1/userdata/cpu/value
> ```
>
> Output might look like:
>
>
>
> ```text
> 12,607,22085407756,-;This is a message
>  cpu=1
>  cpu=42    # kernel-populated value
> ```

<a id="rst-message-id-auto-population-in-userdata"></a>

### Message ID auto population in userdata

Within the netconsole configfs hierarchy, there is a file named `msgid_enabled` located in the `userdata` directory. This file controls the message ID auto-population feature, which assigns a numeric id to each message sent to a given target and appends the ID to userdata dictionary in every message sent.

The message ID is generated using a per-target 32 bit counter that is incremented for every message sent to the target. Note that this counter will eventually wrap around after reaching uint32_t max value, so the message ID is not globally unique over time. However, it can still be used by the target to detect if messages were dropped before reaching the target by identifying gaps in the sequence of IDs.

It is important to distinguish message IDs from the message &lt;sequnum&gt; field. Some kernel messages may never reach netconsole (for example, due to printk rate limiting). Thus, a gap in &lt;sequnum&gt; cannot be solely relied upon to indicate that a message was dropped during transmission, as it may never have been sent via netconsole. The message ID, on the other hand, is only assigned to messages that are actually transmitted via netconsole.

Example:



```text
echo "This is message #1" > /dev/kmsg
echo "This is message #2" > /dev/kmsg
13,434,54928466,-;This is message #1
 msgid=1
13,435,54934019,-;This is message #2
 msgid=2
```

<a id="rst-extended-console"></a>

## Extended console:

If '+' is prefixed to the configuration line or "extended" config file is set to 1, extended console support is enabled. An example boot param follows:



```text
linux netconsole=+4444@10.0.0.1/eth1,9353@10.0.0.2/12:34:56:78:9a:bc
```

Log messages are transmitted with extended metadata header in the following format which is the same as /dev/kmsg:



```text
<level>,<sequnum>,<timestamp>,<contflag>;<message text>
```

If 'r' (release) feature is enabled, the kernel release version is prepended to the start of the message. Example:



```text
6.4.0,6,444,501151268,-;netconsole: network logging started
```

Non printable characters in &lt;message text&gt; are escaped using "xff" notation. If the message contains optional dictionary, verbatim newline is used as the delimiter.

If a message doesn't fit in certain number of bytes (currently 1000), the message is split into multiple fragments by netconsole. These fragments are transmitted with "ncfrag" header field added:



```text
ncfrag=<byte-offset>/<total-bytes>
```

For example, assuming a lot smaller chunk size, a message "the first chunk, the 2nd chunk." may be split as follows:



```text
6,416,1758426,-,ncfrag=0/31;the first chunk,
6,416,1758426,-,ncfrag=16/31; the 2nd chunk.
```

<a id="rst-miscellaneous-notes"></a>

## Miscellaneous notes:

> [!WARNING]
>
> the default target ethernet setting uses the broadcast ethernet address to send packets, which can cause increased load on other systems on the same ethernet segment.

> [!TIP]
>
> some LAN switches may be configured to suppress ethernet broadcasts so it is advised to explicitly specify the remote agents' MAC addresses from the config parameters passed to netconsole.

> [!TIP]
>
> to find out the MAC address of, say, 10.0.0.2, you may try using:
>
>
>
> ```text
> ping -c 1 10.0.0.2 ; /sbin/arp -n | grep 10.0.0.2
> ```

> [!TIP]
>
> in case the remote logging agent is on a separate LAN subnet than the sender, it is suggested to try specifying the MAC address of the default gateway (you may use /sbin/route -n to find it out) as the remote MAC address instead.

> [!NOTE]
>
> the network device (eth1 in the above case) can run any kind of other network traffic, netconsole is not intrusive. Netconsole might cause slight delays in other traffic if the volume of kernel messages is high, but should have no other impact.

> [!NOTE]
>
> if you find that the remote logging agent is not receiving or printing all messages from the sender, it is likely that you have set the "console_loglevel" parameter (on the sender) to only send high priority messages to the console. You can change this at runtime using:
>
>
>
> ```text
> dmesg -n 8
> ```
>
> or by specifying "debug" on the kernel command line at boot, to send all kernel messages to the console. A specific value for this parameter can also be set using the "loglevel" kernel boot option. See the dmesg(8) man page and [Documentation/admin-guide/kernel-parameters.rst](~kernel/administration/admin-guide/kernel-parameters) for details.

Netconsole was designed to be as instantaneous as possible, to enable the logging of even the most critical kernel bugs. It works from IRQ contexts as well, and does not enable interrupts while sending packets. Due to these unique needs, configuration cannot be more automatic, and some fundamental limitations will remain: only IP networks, UDP packets and ethernet devices are supported.
