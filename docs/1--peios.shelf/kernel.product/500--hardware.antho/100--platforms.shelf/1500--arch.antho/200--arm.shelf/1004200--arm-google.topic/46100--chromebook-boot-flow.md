---
title: "Chromebook Boot Flow"
type: reference
description: "Most recent Chromebooks that use device tree are using the opensource depthcharge bootloader. Depthcharge expects the OS to be packaged as a FIT Image which contains an OS image as well as a collection of device trees. It is up to…"
---

<a id="rst-chromebook-boot-flow"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

Most recent Chromebooks that use device tree are using the opensource [depthcharge](<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/platform/depthcharge/>) bootloader. [Depthcharge](<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/platform/depthcharge/>) expects the OS to be packaged as a [FIT Image](<https://doc.coreboot.org/lib/payloads/fit.html>) which contains an OS image as well as a collection of device trees. It is up to [depthcharge](<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/platform/depthcharge/>) to pick the right device tree from the [FIT Image](<https://doc.coreboot.org/lib/payloads/fit.html>) and provide it to the OS.

The scheme that [depthcharge](<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/platform/depthcharge/>) uses to pick the device tree takes into account three variables:

- Board name, specified at [depthcharge](<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/platform/depthcharge/>) compile time. This is $(BOARD) below.

- Board revision number, determined at runtime (perhaps by reading GPIO strappings, perhaps via some other method). This is $(REV) below.

- SKU number, read from GPIO strappings at boot time. This is $(SKU) below.

For recent Chromebooks, [depthcharge](<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/platform/depthcharge/>) creates a match list that looks like this:

- google,$(BOARD)-rev$(REV)-sku$(SKU)

- google,$(BOARD)-rev$(REV)

- google,$(BOARD)-sku$(SKU)

- google,$(BOARD)

Note that some older Chromebooks use a slightly different list that may not include SKU matching or may prioritize SKU/rev differently.

Note that for some boards there may be extra board-specific logic to inject extra compatibles into the list, but this is uncommon.

[Depthcharge](<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/platform/depthcharge/>) will look through all device trees in the [FIT Image](<https://doc.coreboot.org/lib/payloads/fit.html>) trying to find one that matches the most specific compatible. It will then look through all device trees in the [FIT Image](<https://doc.coreboot.org/lib/payloads/fit.html>) trying to find the one that matches the *second most* specific compatible, etc.

When searching for a device tree, [depthcharge](<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/platform/depthcharge/>) doesn't care where the compatible string falls within a device tree's root compatible string array. As an example, if we're on board "lazor", rev 4, SKU 0 and we have two device trees:

- "google,lazor-rev5-sku0", "google,lazor-rev4-sku0", "qcom,sc7180"

- "google,lazor", "qcom,sc7180"

Then [depthcharge](<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/platform/depthcharge/>) will pick the first device tree even though "google,lazor-rev4-sku0" was the second compatible listed in that device tree. This is because it is a more specific compatible than "google,lazor".

It should be noted that [depthcharge](<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/platform/depthcharge/>) does not have any smarts to try to match board or SKU revisions that are "close by". That is to say that if [depthcharge](<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/platform/depthcharge/>) knows it's on "rev4" of a board but there is no "rev4" device tree then [depthcharge](<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/platform/depthcharge/>) *won't* look for a "rev3" device tree.

In general when any significant changes are made to a board the board revision number is increased even if none of those changes need to be reflected in the device tree. Thus it's fairly common to see device trees with multiple revisions.

It should be noted that, taking into account the above system that [depthcharge](<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/platform/depthcharge/>) has, the most flexibility is achieved if the device tree supporting the newest revision(s) of a board omits the "-rev\{REV\}" compatible strings. When this is done then if you get a new board revision and try to run old software on it then we'll at pick the newest device tree we know about.

<a id="rst-depthcharge"></a>



<a id="rst-fit-image"></a>
