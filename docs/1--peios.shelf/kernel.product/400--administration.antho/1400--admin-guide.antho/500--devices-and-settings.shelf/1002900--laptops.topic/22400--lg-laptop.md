---
title: "LG Gram laptop extra features"
type: reference
description: "By Matan Ziv-Av <matan@svgalib.org>"
---

<a id="rst-lg-gram-laptop-extra-features"></a>

<!-- SPDX-License-Identifier: GPL-2.0+ -->

By Matan Ziv-Av &lt;[matan@svgalib.org](<mailto:matan@svgalib.org>)&gt;

<a id="rst-hotkeys"></a>

## Hotkeys

The following FN keys are ignored by the kernel without this driver:

- FN-F1 (LG control panel)   - Generates F15

- FN-F5 (Touchpad toggle)    - Generates F21

- FN-F6 (Airplane mode)      - Generates RFKILL

- FN-F9 (Reader mode)        - Generates F14

The rest of the FN keys work without a need for a special driver.

<a id="rst-reader-mode"></a>

## Reader mode

Writing 0/1 to /sys/devices/platform/lg-laptop/reader_mode disables/enables reader mode. In this mode the screen colors change (blue color reduced), and the reader mode indicator LED (on F9 key) turns on.

<a id="rst-fn-lock"></a>

## FN Lock

Writing 0/1 to /sys/devices/platform/lg-laptop/fn_lock disables/enables FN lock.

<a id="rst-battery-care-limit"></a>

## Battery care limit

Writing 80/100 to /sys/class/power_supply/CMB0/charge_control_end_threshold sets the maximum capacity to charge the battery. Limiting the charge reduces battery capacity loss over time.

This value is reset to 100 when the kernel boots.

<a id="rst-fan-mode"></a>

## Fan mode

Writing 0/1/2 to /sys/devices/platform/lg-laptop/fan_mode sets fan mode to Optimal/Silent/Performance respectively.

<a id="rst-usb-charge"></a>

## USB charge

Writing 0/1 to /sys/devices/platform/lg-laptop/usb_charge disables/enables charging another device from the USB port while the device is turned off.

This value is reset to 0 when the kernel boots.

<a id="rst-leds"></a>

### LEDs

The are two LED devices supported by the driver:

<a id="rst-keyboard-backlight"></a>

## Keyboard backlight

A led device named kbd_led controls the keyboard backlight. There are three lighting level: off (0), low (127) and high (255).

The keyboard backlight is also controlled by the key combination FN-F8 which cycles through those levels.

<a id="rst-touchpad-indicator-led"></a>

## Touchpad indicator LED

On the F5 key. Controlled by led device names tpad_led.
