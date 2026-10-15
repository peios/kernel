---
title: "Tridentfb"
type: reference
description: "Tridentfb is a framebuffer driver for some Trident chip based cards."
---

<a id="rst-tridentfb"></a>

Tridentfb is a framebuffer driver for some Trident chip based cards.

The following list of chips is thought to be supported although not all are tested:

those from the TGUI series 9440/96XX and with Cyber in their names those from the Image series and with Cyber in their names those with Blade in their names (Blade3D,CyberBlade...) the newer CyberBladeXP family

All families are accelerated. Only PCI/AGP based cards are supported, none of the older Tridents. The driver supports 8, 16 and 32 bits per pixel depths. The TGUI family requires a line length to be power of 2 if acceleration is enabled. This means that range of possible resolutions and bpp is limited comparing to the range if acceleration is disabled (see list of parameters below).

Known bugs:

1. The driver randomly locks up on 3DImage975 chip with acceleration enabled. The same happens in X11 (Xorg).

2. The ramdac speeds require some more fine tuning. It is possible to switch resolution which the chip does not support at some depths for older chips.

<a id="rst-how-to-use-it"></a>

## How to use it?

When booting you can pass the video parameter:



```text
video=tridentfb
```

The parameters for tridentfb are concatenated with a ':' as in this example:



```text
video=tridentfb:800x600-16@75,noaccel
```

The second level parameters that tridentfb understands are:


<table>
<tbody>
<tr>
<td>


noaccel

</td>
<td>


turns off acceleration (when it doesn't work for your card)

</td>
</tr>
<tr>
<td>


fp

</td>
<td>


use flat panel related stuff

</td>
</tr>
<tr>
<td>


crt

</td>
<td>


assume monitor is present instead of fp

</td>
</tr>
<tr>
<td>


center

</td>
<td>


for flat panels and resolutions smaller than native size center the image, otherwise use

</td>
</tr>
<tr>
<td>


stretch

</td>
<td>




</td>
</tr>
<tr>
<td>


memsize

</td>
<td>


integer value in KB, use if your card's memory size is misdetected. look at the driver output to see what it says when initializing.

</td>
</tr>
<tr>
<td>


memdiff

</td>
<td>


integer value in KB, should be nonzero if your card reports more memory than it actually has. For instance mine is 192K less than detection says in all three BIOS selectable situations 2M, 4M, 8M. Only use if your video memory is taken from main memory hence of configurable size. Otherwise use memsize. If in some modes which barely fit the memory you see garbage at the bottom this might help by not letting change to that mode anymore.

</td>
</tr>
<tr>
<td>


nativex

</td>
<td>


the width in pixels of the flat panel.If you know it (usually 1024 800 or 1280) and it is not what the driver seems to detect use it.

</td>
</tr>
<tr>
<td>


bpp

</td>
<td>


bits per pixel (8,16 or 32)

</td>
</tr>
<tr>
<td>


mode

</td>
<td>


a mode name like [800x600-8@75](<mailto:800x600-8@75>) as described in [Documentation/fb/modedb.rst](~kernel/hardware/fb/modedb)

</td>
</tr>
</tbody>
</table>

Using insane values for the above parameters will probably result in driver misbehaviour so take care(for instance memsize=12345678 or memdiff=23784 or nativex=93)

Contact: [jani@astechnix.ro](<mailto:jani@astechnix.ro>)
