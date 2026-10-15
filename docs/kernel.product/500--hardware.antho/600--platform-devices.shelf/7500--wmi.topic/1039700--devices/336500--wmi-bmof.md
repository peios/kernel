---
title: "WMI embedded Binary MOF driver"
type: reference
description: "Many machines embed WMI Binary MOF (Managed Object Format) metadata used to describe the details of their ACPI WMI interfaces. The data can be decoded with tools like bmfdec to obtain a human readable WMI interface description, which is…"
---

<a id="rst-wmi-embedded-binary-mof-driver"></a>

<!-- SPDX-License-Identifier: GPL-2.0-only -->

<a id="rst-introduction"></a>

## Introduction

Many machines embed WMI Binary MOF (Managed Object Format) metadata used to describe the details of their ACPI WMI interfaces. The data can be decoded with tools like [bmfdec](<https://github.com/pali/bmfdec>)<a id="rst-bmfdec"></a> to obtain a human readable WMI interface description, which is useful for developing new WMI drivers.

The Binary MOF data can be retrieved from the `bmof` sysfs attribute of the associated WMI device. Please note that multiple WMI devices containing Binary MOF data can exist on a given system.

<a id="rst-wmi-interface"></a>

## WMI interface

The Binary MOF WMI device is identified by the WMI GUID `05901221-D566-11D1-B2F0-00A0C9062910`. The Binary MOF can be obtained by doing a WMI data block query. The result is then returned as an ACPI buffer with a variable size.
