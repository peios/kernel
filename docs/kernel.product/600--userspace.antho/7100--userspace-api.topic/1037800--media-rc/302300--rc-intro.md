---
title: "Introduction"
type: reference
description: "Currently, most analog and digital devices have a Infrared input for remote controllers. Each manufacturer has their own type of control. It is not rare for the same manufacturer to ship different types of controls, depending on the device."
---

<a id="rst-introduction"></a>
<a id="rst-remote-controllers-intro"></a>

<!-- SPDX-License-Identifier: GPL-2.0 OR GFDL-1.1-no-invariants-or-later -->

Currently, most analog and digital devices have a Infrared input for remote controllers. Each manufacturer has their own type of control. It is not rare for the same manufacturer to ship different types of controls, depending on the device.

A Remote Controller interface is mapped as a normal evdev/input interface, just like a keyboard or a mouse. So, it uses all ioctls already defined for any other input devices.

However, remove controllers are more flexible than a normal input device, as the IR receiver (and/or transmitter) can be used in conjunction with a wide variety of different IR remotes.

In order to allow flexibility, the Remote Controller subsystem allows controlling the RC-specific attributes via [the sysfs class nodes](<~kernel/userspace/userspace-api/media-rc/rc-sysfs-nodes#rst-remote-controllers-sysfs-nodes>).
