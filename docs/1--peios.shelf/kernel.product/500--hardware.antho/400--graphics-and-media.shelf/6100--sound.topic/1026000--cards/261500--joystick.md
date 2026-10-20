---
title: "Analog Joystick Support on ALSA Drivers"
type: reference
description: "Oct. 14, 2003"
---

<a id="rst-analog-joystick-support-on-alsa-drivers"></a>

Oct. 14, 2003

Takashi Iwai &lt;[tiwai@suse.de](<mailto:tiwai@suse.de>)&gt;

<a id="rst-general"></a>

## General

First of all, you need to enable GAMEPORT support on Linux kernel for using a joystick with the ALSA driver.  For the details of gameport support, refer to [Documentation/input/joydev/joystick.rst](~kernel/hardware/input/joydev/joystick).

The joystick support of ALSA drivers is different between ISA and PCI cards.  In the case of ISA (PnP) cards, it's usually handled by the independent module (ns558).  Meanwhile, the ALSA PCI drivers have the built-in gameport support.  Hence, when the ALSA PCI driver is built in the kernel, CONFIG_GAMEPORT must be 'y', too.  Otherwise, the gameport support on that card will be (silently) disabled.

Some adapter modules probe the physical connection of the device at the load time.  It'd be safer to plug in the joystick device before loading the module.

<a id="rst-pci-cards"></a>

## PCI Cards

For PCI cards, the joystick is enabled when the appropriate module option is specified.  Some drivers don't need options, and the joystick support is always enabled.  In the former ALSA version, there was a dynamic control API for the joystick activation.  It was changed, however, to the static module options because of the system stability and the resource management.

The following PCI drivers support the joystick natively.


<table>
<thead>
<tr>
<th>


Driver

</th>
<th>


Module Option

</th>
<th>


Available Values

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


als4000

</td>
<td>


joystick_port

</td>
<td>


0 = disable (default), 1 = auto-detect, manual: any address (e.g. 0x200)

</td>
</tr>
<tr>
<td>


au88x0

</td>
<td>


N/A

</td>
<td>


N/A

</td>
</tr>
<tr>
<td>


azf3328

</td>
<td>


joystick

</td>
<td>


0 = disable, 1 = enable, -1 = auto (default)

</td>
</tr>
<tr>
<td>


ens1370

</td>
<td>


joystick

</td>
<td>


0 = disable (default), 1 = enable

</td>
</tr>
<tr>
<td>


ens1371

</td>
<td>


joystick_port

</td>
<td>


0 = disable (default), 1 = auto-detect, manual: 0x200, 0x208, 0x210, 0x218

</td>
</tr>
<tr>
<td>


cmipci

</td>
<td>


joystick_port

</td>
<td>


0 = disable (default), 1 = auto-detect, manual: any address (e.g. 0x200)

</td>
</tr>
<tr>
<td>


cs4281

</td>
<td>


N/A

</td>
<td>


N/A

</td>
</tr>
<tr>
<td>


cs46xx

</td>
<td>


N/A

</td>
<td>


N/A

</td>
</tr>
<tr>
<td>


es1938

</td>
<td>


N/A

</td>
<td>


N/A

</td>
</tr>
<tr>
<td>


es1968

</td>
<td>


joystick

</td>
<td>


0 = disable (default), 1 = enable

</td>
</tr>
<tr>
<td>


sonicvibes

</td>
<td>


N/A

</td>
<td>


N/A

</td>
</tr>
<tr>
<td>


trident

</td>
<td>


N/A

</td>
<td>


N/A

</td>
</tr>
<tr>
<td>


via82xx <a id="rst-footnote-reference-1"></a>[1](#rst-f1)

</td>
<td>


joystick

</td>
<td>


0 = disable (default), 1 = enable

</td>
</tr>
<tr>
<td>


ymfpci

</td>
<td>


joystick_port

</td>
<td>


0 = disable (default), 1 = auto-detect, manual: 0x201, 0x202, 0x204, 0x205 <a id="rst-footnote-reference-2"></a>[2](#rst-f2)

</td>
</tr>
</tbody>
</table>

<a id="rst-f1"></a>



**[1]** VIA686A/B only

<a id="rst-f2"></a>



**[2]** With YMF744/754 chips, the port address can be chosen arbitrarily

The following drivers don't support gameport natively, but there are additional modules.  Load the corresponding module to add the gameport support.


<table>
<thead>
<tr>
<th>


Driver

</th>
<th>


Additional Module

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


emu10k1

</td>
<td>


emu10k1-gp

</td>
</tr>
<tr>
<td>


fm801

</td>
<td>


fm801-gp

</td>
</tr>
</tbody>
</table>

Note: the "pcigame" and "cs461x" modules are for the OSS drivers only. These ALSA drivers (cs46xx, trident and au88x0) have the built-in gameport support.

As mentioned above, ALSA PCI drivers have the built-in gameport support, so you don't have to load ns558 module.  Just load "joydev" and the appropriate adapter module (e.g. "analog").

<a id="rst-isa-cards"></a>

## ISA Cards

ALSA ISA drivers don't have the built-in gameport support. Instead, you need to load "ns558" module in addition to "joydev" and the adapter module (e.g. "analog").
