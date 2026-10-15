---
title: "Devlink Health"
type: reference
description: "The devlink health mechanism is targeted for Real Time Alerting, in order to know when something bad happened to a PCI device."
---

<a id="rst-devlink-health"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

<a id="rst-background"></a>

## Background

The `devlink` health mechanism is targeted for Real Time Alerting, in order to know when something bad happened to a PCI device.

> - Provide alert debug information.
>
> - Self healing.
>
> - If problem needs vendor support, provide a way to gather all needed debugging information.

<a id="rst-overview"></a>

## Overview

The main idea is to unify and centralize driver health reports in the generic `devlink` instance and allow the user to set different attributes of the health reporting and recovery procedures.

The `devlink` health reporter: Device driver creates a "health reporter" per each error/health type. Error/Health type can be a known/generic (e.g. PCI error, fw error, rx/tx error) or unknown (driver specific). For each registered health reporter a driver can issue error/health reports asynchronously. All health reports handling is done by `devlink`. Device driver can provide specific callbacks for each "health reporter", e.g.:

> - Recovery procedures
>
> - Diagnostics procedures
>
> - Object dump procedures
>
> - Out Of Box initial parameters

Different parts of the driver can register different types of health reporters with different handlers.

<a id="rst-actions"></a>

## Actions

Once an error is reported, devlink health will perform the following actions:

> - A log is being send to the kernel trace events buffer
>
> - Health status and statistics are being updated for the reporter instance
>
> - Object dump is being taken and saved at the reporter instance (as long as auto-dump is set and there is no other dump which is already stored)
>
> - Auto recovery attempt is being done. Depends on:
>
>   - Auto-recovery configuration
>
>   - Grace period (and burst period)  vs. time passed since last recover

<a id="rst-devlink-formatted-message"></a>

## Devlink formatted message

To handle devlink health diagnose and health dump requests, devlink creates a formatted message structure `devlink_fmsg` and send it to the driver's callback to fill the data in using the devlink fmsg API.

Devlink fmsg is a mechanism to pass descriptors between drivers and devlink, in json-like format. The API allows the driver to add nested attributes such as object, object pair and value array, in addition to attributes such as name and value.

Driver should use this API to fill the fmsg context in a format which will be translated by the devlink to the netlink message later. When it needs to send the data using SKBs to the netlink layer, it fragments the data between different SKBs. In order to do this fragmentation, it uses virtual nests attributes, to avoid actual nesting use which cannot be divided between different SKBs.

<a id="rst-user-interface"></a>

## User Interface

User can access/change each reporter's parameters and driver specific callbacks via `devlink`, e.g per error type (per health reporter):

> - Configure reporter's generic parameters (like: disable/enable auto recovery)
>
> - Invoke recovery procedure
>
> - Run diagnostics
>
> - Object dump


<table>
<caption>List of devlink health interfaces</caption>
<tbody>
<tr>
<td>


Name

</td>
<td>


Description

</td>
</tr>
<tr>
<td>


`DEVLINK_CMD_HEALTH_REPORTER_GET`

</td>
<td>


Retrieves status and configuration info per DEV and reporter.

</td>
</tr>
<tr>
<td>


`DEVLINK_CMD_HEALTH_REPORTER_SET`

</td>
<td>


Allows reporter-related configuration setting.

</td>
</tr>
<tr>
<td>


`DEVLINK_CMD_HEALTH_REPORTER_RECOVER`

</td>
<td>


Triggers reporter's recovery procedure.

</td>
</tr>
<tr>
<td>


`DEVLINK_CMD_HEALTH_REPORTER_TEST`

</td>
<td>


Triggers a fake health event on the reporter. The effects of the test event in terms of recovery flow should follow closely that of a real event.

</td>
</tr>
<tr>
<td>


`DEVLINK_CMD_HEALTH_REPORTER_DIAGNOSE`

</td>
<td>


Retrieves current device state related to the reporter.

</td>
</tr>
<tr>
<td>


`DEVLINK_CMD_HEALTH_REPORTER_DUMP_GET`

</td>
<td>


Retrieves the last stored dump. Devlink health saves a single dump. If an dump is not already stored by devlink for this reporter, devlink generates a new dump. Dump output is defined by the reporter.

</td>
</tr>
<tr>
<td>


`DEVLINK_CMD_HEALTH_REPORTER_DUMP_CLEAR`

</td>
<td>


Clears the last saved dump file for the specified reporter.

</td>
</tr>
</tbody>
</table>

The following diagram provides a general overview of `devlink-health`:



```text
                                               netlink
                                      +--------------------------+
                                      |                          |
                                      |            +             |
                                      |            |             |
                                      +--------------------------+
                                                   |request for ops
                                                   |(diagnose,
  driver                               devlink     |recover,
                                                   |dump)
+--------+                            +--------------------------+
|        |                            |    reporter|             |
|        |                            |  +---------v----------+  |
|        |   ops execution            |  |                    |  |
|     <----------------------------------+                    |  |
|        |                            |  |                    |  |
|        |                            |  + ^------------------+  |
|        |                            |    | request for ops     |
|        |                            |    | (recover, dump)     |
|        |                            |    |                     |
|        |                            |  +-+------------------+  |
|        |     health report          |  | health handler     |  |
|        +------------------------------->                    |  |
|        |                            |  +--------------------+  |
|        |     health reporter create |                          |
|        +---------------------------->                          |
+--------+                            +--------------------------+
```
