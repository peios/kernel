---
title: "Changing default Remote Controller mappings"
type: reference
description: "The event interface provides two ioctls to be used against the /dev/input/event device, to allow changing the default keymapping."
---

<a id="rst-changing-default-remote-controller-mappings"></a>
<a id="rst-remote-controllers-table-change"></a>

<!-- SPDX-License-Identifier: GPL-2.0 OR GFDL-1.1-no-invariants-or-later -->

The event interface provides two ioctls to be used against the /dev/input/event device, to allow changing the default keymapping.

This program demonstrates how to replace the keymap tables.

- [file: uapi/v4l/keytable.c](<~kernel/userspace/userspace-api/media-rc/keytable-c>)
