---
title: "The Linux WatchDog Timer Power Management Guide"
type: reference
description: "Last reviewed: 17-Dec-2018"
---

<a id="rst-the-linux-watchdog-timer-power-management-guide"></a>

Last reviewed: 17-Dec-2018

Wolfram Sang &lt;[wsa+renesas@sang-engineering.com](<mailto:wsa+renesas@sang-engineering.com>)&gt;

<a id="rst-introduction"></a>

## Introduction

This document states rules about watchdog devices and their power management handling to ensure a uniform behaviour for Linux systems.

<a id="rst-ping-on-resume"></a>

## Ping on resume

On resume, a watchdog timer shall be reset to its selected value to give userspace enough time to resume. \[1\] \[2\]

\[1\] [https://patchwork.kernel.org/patch/10252209/](<https://patchwork.kernel.org/patch/10252209/>)

\[2\] [https://patchwork.kernel.org/patch/10711625/](<https://patchwork.kernel.org/patch/10711625/>)
