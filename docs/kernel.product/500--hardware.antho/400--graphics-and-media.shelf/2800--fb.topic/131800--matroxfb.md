---
title: "matroxfb - Framebuffer driver for Matrox devices"
type: reference
description: "This is a driver for a graphic framebuffer for Matrox devices on Alpha, Intel and PPC boxes."
---

<a id="rst-matroxfb-framebuffer-driver-for-matrox-devices"></a>

This is a driver for a graphic framebuffer for Matrox devices on Alpha, Intel and PPC boxes.

Advantages:

> - It provides a nice large console (128 cols + 48 lines with 1024x768) without using tiny, unreadable fonts.
>
> - You can run XF\{68,86\}\_FBDev or XFree86 fbdev driver on top of /dev/fb0
>
> - Most important: boot logo :-)

Disadvantages:

> - graphic mode is slower than text mode... but you should not notice if you use same resolution as you used in textmode.

<a id="rst-how-to-use-it"></a>

## How to use it?

Switching modes is done using the video=matroxfb:vesa:... boot parameter or using `fbset` program.

If you want, for example, enable a resolution of 1280x1024x24bpp you should pass to the kernel this command line: "video=matroxfb:vesa:0x1BB".

You should compile in both vgacon (to boot if you remove you Matrox from box) and matroxfb (for graphics mode). You should not compile-in vesafb unless you have primary display on non-Matrox VBE2.0 device (see [Documentation/fb/vesafb.rst](~kernel/hardware/fb/vesafb) for details).

Currently supported video modes are (through vesa:... interface, PowerMac has \[as addon\] compatibility code):

<a id="rst-graphic-modes"></a>

### Graphic modes


<table>
<thead>
<tr>
<th>


bpp

</th>
<th>


640x400

</th>
<th>


640x480

</th>
<th>


768x576

</th>
<th>


800x600

</th>
<th>


960x720

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


4

</td>
<td>




</td>
<td>


0x12

</td>
<td>




</td>
<td>


0x102

</td>
<td>




</td>
</tr>
<tr>
<td>


8

</td>
<td>


0x100

</td>
<td>


0x101

</td>
<td>


0x180

</td>
<td>


0x103

</td>
<td>


0x188

</td>
</tr>
<tr>
<td>


15

</td>
<td>




</td>
<td>


0x110

</td>
<td>


0x181

</td>
<td>


0x113

</td>
<td>


0x189

</td>
</tr>
<tr>
<td>


16

</td>
<td>




</td>
<td>


0x111

</td>
<td>


0x182

</td>
<td>


0x114

</td>
<td>


0x18A

</td>
</tr>
<tr>
<td>


24

</td>
<td>




</td>
<td>


0x1B2

</td>
<td>


0x184

</td>
<td>


0x1B5

</td>
<td>


0x18C

</td>
</tr>
<tr>
<td>


32

</td>
<td>




</td>
<td>


0x112

</td>
<td>


0x183

</td>
<td>


0x115

</td>
<td>


0x18B

</td>
</tr>
</tbody>
</table>

<a id="rst-graphic-modes-continued"></a>

### Graphic modes (continued)


<table>
<thead>
<tr>
<th>


bpp

</th>
<th>


1024x768

</th>
<th>


1152x864

</th>
<th>


1280x1024

</th>
<th>


1408x1056

</th>
<th>


1600x1200

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


4

</td>
<td>


0x104

</td>
<td>




</td>
<td>


0x106

</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


8

</td>
<td>


0x105

</td>
<td>


0x190

</td>
<td>


0x107

</td>
<td>


0x198

</td>
<td>


0x11C

</td>
</tr>
<tr>
<td>


15

</td>
<td>


0x116

</td>
<td>


0x191

</td>
<td>


0x119

</td>
<td>


0x199

</td>
<td>


0x11D

</td>
</tr>
<tr>
<td>


16

</td>
<td>


0x117

</td>
<td>


0x192

</td>
<td>


0x11A

</td>
<td>


0x19A

</td>
<td>


0x11E

</td>
</tr>
<tr>
<td>


24

</td>
<td>


0x1B8

</td>
<td>


0x194

</td>
<td>


0x1BB

</td>
<td>


0x19C

</td>
<td>


0x1BF

</td>
</tr>
<tr>
<td>


32

</td>
<td>


0x118

</td>
<td>


0x193

</td>
<td>


0x11B

</td>
<td>


0x19B

</td>
<td>




</td>
</tr>
</tbody>
</table>

<a id="rst-text-modes"></a>

### Text modes


<table>
<thead>
<tr>
<th>


text

</th>
<th>


640x400

</th>
<th>


640x480

</th>
<th>


1056x344

</th>
<th>


1056x400

</th>
<th>


1056x480

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


8x8

</td>
<td>


0x1C0

</td>
<td>


0x108

</td>
<td>


0x10A

</td>
<td>


0x10B

</td>
<td>


0x10C

</td>
</tr>
<tr>
<td>


8x16

</td>
<td>


2, 3, 7

</td>
<td>




</td>
<td>




</td>
<td>


0x109

</td>
<td>




</td>
</tr>
</tbody>
</table>

You can enter these number either hexadecimal (leading `0x`) or decimal (0x100 = 256). You can also use value + 512 to achieve compatibility with your old number passed to vesafb.

Non-listed number can be achieved by more complicated command-line, for example 1600x1200x32bpp can be specified by `video=matroxfb:vesa:0x11C,depth:32`.

<a id="rst-x11"></a>

## X11

XF\{68,86\}\_FBDev should work just fine, but it is non-accelerated. On non-intel architectures there are some glitches for 24bpp videomodes. 8, 16 and 32bpp works fine.

Running another (accelerated) X-Server like XF86_SVGA works too. But (at least) XFree servers have big troubles in multihead configurations (even on first head, not even talking about second). Running XFree86 4.x accelerated mga driver is possible, but you must not enable DRI - if you do, resolution and color depth of your X desktop must match resolution and color depths of your virtual consoles, otherwise X will corrupt accelerator settings.

<a id="rst-svgalib"></a>

## SVGALib

Driver contains SVGALib compatibility code. It is turned on by choosing textual mode for console. You can do it at boot time by using videomode 2,3,7,0x108-0x10C or 0x1C0. At runtime, `fbset -depth 0` does this work. Unfortunately, after SVGALib application exits, screen contents is corrupted. Switching to another console and back fixes it. I hope that it is SVGALib's problem and not mine, but I'm not sure.

<a id="rst-configuration"></a>

## Configuration

You can pass kernel command line options to matroxfb with `video=matroxfb:option1,option2:value2,option3` (multiple options should be separated by comma, values are separated from options by `:`). Accepted options:


<table>
<tbody>
<tr>
<td>


mem:X

</td>
<td>


size of memory (X can be in megabytes, kilobytes or bytes) You can only decrease value determined by driver because of it always probe for memory. Default is to use whole detected memory usable for on-screen display (i.e. max. 8 MB).

</td>
</tr>
<tr>
<td>


disabled

</td>
<td>


do not load driver; you can use also `off`, but `disabled` is here too.

</td>
</tr>
<tr>
<td>


enabled

</td>
<td>


load driver, if you have `video=matroxfb:disabled` in LILO configuration, you can override it by this (you cannot override `off`). It is default.

</td>
</tr>
<tr>
<td>


noaccel

</td>
<td>


do not use acceleration engine. It does not work on Alphas.

</td>
</tr>
<tr>
<td>


accel

</td>
<td>


use acceleration engine. It is default.

</td>
</tr>
<tr>
<td>


nopan

</td>
<td>


create initial consoles with vyres = yres, thus disabling virtual scrolling.

</td>
</tr>
<tr>
<td>


pan

</td>
<td>


create initial consoles as tall as possible (vyres = memory/vxres). It is default.

</td>
</tr>
<tr>
<td>


nopciretry

</td>
<td>


disable PCI retries. It is needed for some broken chipsets, it is autodetected for intel's 82437. In this case device does not comply to PCI 2.1 specs (it will not guarantee that every transaction terminate with success or retry in 32 PCLK).

</td>
</tr>
<tr>
<td>


pciretry

</td>
<td>


enable PCI retries. It is default, except for intel's 82437.

</td>
</tr>
<tr>
<td>


novga

</td>
<td>


disables VGA I/O ports. It is default if BIOS did not enable device. You should not use this option, some boards then do not restart without power off.

</td>
</tr>
<tr>
<td>


vga

</td>
<td>


preserve state of VGA I/O ports. It is default. Driver does not enable VGA I/O if BIOS did not it (it is not safe to enable it in most cases).

</td>
</tr>
<tr>
<td>


nobios

</td>
<td>


disables BIOS ROM. It is default if BIOS did not enable BIOS itself. You should not use this option, some boards then do not restart without power off.

</td>
</tr>
<tr>
<td>


bios

</td>
<td>


preserve state of BIOS ROM. It is default. Driver does not enable BIOS if BIOS was not enabled before.

</td>
</tr>
<tr>
<td>


noinit

</td>
<td>


tells driver, that devices were already initialized. You should use it if you have G100 and/or if driver cannot detect memory, you see strange pattern on screen and so on. Devices not enabled by BIOS are still initialized. It is default.

</td>
</tr>
<tr>
<td>


init

</td>
<td>


driver initializes every device it knows about.

</td>
</tr>
<tr>
<td>


memtype

</td>
<td>


specifies memory type, implies 'init'. This is valid only for G200 and G400 and has following meaning:

> - **G200:**
>
>   - 0 -&gt; 2x128Kx32 chips, 2MB onboard, probably sgram
>
>   - 1 -&gt; 2x128Kx32 chips, 4MB onboard, probably sgram
>
>   - 2 -&gt; 2x256Kx32 chips, 4MB onboard, probably sgram
>
>   - 3 -&gt; 2x256Kx32 chips, 8MB onboard, probably sgram
>
>   - 4 -&gt; 2x512Kx16 chips, 8/16MB onboard, probably sdram only
>
>   - 5 -&gt; same as above
>
>   - 6 -&gt; 4x128Kx32 chips, 4MB onboard, probably sgram
>
>   - 7 -&gt; 4x128Kx32 chips, 8MB onboard, probably sgram
>
> - **G400:**
>
>   - 0 -&gt; 2x512Kx16 SDRAM, 16/32MB
>
>   - 2x512Kx32 SGRAM, 16/32MB
>
>   - 1 -&gt; 2x256Kx32 SGRAM, 8/16MB
>
>   - 2 -&gt; 4x128Kx32 SGRAM, 8/16MB
>
>   - 3 -&gt; 4x512Kx32 SDRAM, 32MB
>
>   - 4 -&gt; 4x256Kx32 SGRAM, 16/32MB
>
>   - 5 -&gt; 2x1Mx32 SDRAM, 32MB
>
>   - 6 -&gt; reserved
>
>   - 7 -&gt; reserved

You should use sdram or sgram parameter in addition to memtype parameter.

</td>
</tr>
<tr>
<td>


nomtrr

</td>
<td>


disables write combining on frame buffer. This slows down driver but there is reported minor incompatibility between GUS DMA and XFree under high loads if write combining is enabled (sound dropouts).

</td>
</tr>
<tr>
<td>


mtrr

</td>
<td>


enables write combining on frame buffer. It speeds up video accesses much. It is default. You must have MTRR support enabled in kernel and your CPU must have MTRR (f.e. Pentium II have them).

</td>
</tr>
<tr>
<td>


sgram

</td>
<td>


tells to driver that you have Gxx0 with SGRAM memory. It has no effect without `init`.

</td>
</tr>
<tr>
<td>


sdram

</td>
<td>


tells to driver that you have Gxx0 with SDRAM memory. It is a default.

</td>
</tr>
<tr>
<td>


inv24

</td>
<td>


change timings parameters for 24bpp modes on Millennium and Millennium II. Specify this if you see strange color shadows around  characters.

</td>
</tr>
<tr>
<td>


noinv24

</td>
<td>


use standard timings. It is the default.

</td>
</tr>
<tr>
<td>


inverse

</td>
<td>


invert colors on screen (for LCD displays)

</td>
</tr>
<tr>
<td>


noinverse

</td>
<td>


show true colors on screen. It is default.

</td>
</tr>
<tr>
<td>


dev:X

</td>
<td>


bind driver to device X. Driver numbers device from 0 up to N, where device 0 is first `known` device found, 1 second and so on. lspci lists devices in this order. Default is `every` known device.

</td>
</tr>
<tr>
<td>


nohwcursor

</td>
<td>


disables hardware cursor (use software cursor instead).

</td>
</tr>
<tr>
<td>


hwcursor

</td>
<td>


enables hardware cursor. It is default. If you are using non-accelerated mode (`noaccel` or `fbset -accel false`), software cursor is used (except for text mode).

</td>
</tr>
<tr>
<td>


noblink

</td>
<td>


disables cursor blinking. Cursor in text mode always blinks (hw limitation).

</td>
</tr>
<tr>
<td>


blink

</td>
<td>


enables cursor blinking. It is default.

</td>
</tr>
<tr>
<td>


nofastfont

</td>
<td>


disables fastfont feature. It is default.

</td>
</tr>
<tr>
<td>


fastfont:X

</td>
<td>


enables fastfont feature. X specifies size of memory reserved for font data, it must be &gt;= (fontwidth\*fontheight\*chars_in_font)/8. It is faster on Gx00 series, but slower on older cards.

</td>
</tr>
<tr>
<td>


grayscale

</td>
<td>


enable grayscale summing. It works in PSEUDOCOLOR modes (text, 4bpp, 8bpp). In DIRECTCOLOR modes it is limited to characters displayed through putc/putcs. Direct accesses to framebuffer can paint colors.

</td>
</tr>
<tr>
<td>


nograyscale

</td>
<td>


disable grayscale summing. It is default.

</td>
</tr>
<tr>
<td>


cross4MB

</td>
<td>


enables that pixel line can cross 4MB boundary. It is default for non-Millennium.

</td>
</tr>
<tr>
<td>


nocross4MB

</td>
<td>


pixel line must not cross 4MB boundary. It is default for Millennium I or II, because of these devices have hardware limitations which do not allow this. But this option is incompatible with some (if not all yet released) versions of XF86_FBDev.

</td>
</tr>
<tr>
<td>


dfp

</td>
<td>


enables digital flat panel interface. This option is incompatible with secondary (TV) output - if DFP is active, TV output must be inactive and vice versa. DFP always uses same timing as primary (monitor) output.

</td>
</tr>
<tr>
<td>


dfp:X

</td>
<td>


use settings X for digital flat panel interface. X is number from 0 to 0xFF, and meaning of each individual bit is described in G400 manual, in description of DAC register 0x1F. For normal operation you should set all bits to zero, except lowest bit. This lowest bit selects who is source of display clocks, whether G400, or panel. Default value is now read back from hardware - so you should specify this value only if you are also using `init` parameter.

</td>
</tr>
<tr>
<td>


outputs:XYZ

</td>
<td>


set mapping between CRTC and outputs. Each letter can have value of 0 (for no CRTC), 1 (CRTC1) or 2 (CRTC2), and first letter corresponds to primary analog output, second letter to the secondary analog output and third letter to the DVI output. Default setting is 100 for cards below G400 or G400 without DFP, 101 for G400 with DFP, and 111 for G450 and G550. You can set mapping only on first card, use matroxset for setting up other devices.

</td>
</tr>
<tr>
<td>


vesa:X

</td>
<td>


selects startup videomode. X is number from 0 to 0x1FF, see table above for detailed explanation. Default is 640x480x8bpp if driver has 8bpp support. Otherwise first available of 640x350x4bpp, 640x480x15bpp, 640x480x24bpp, 640x480x32bpp or 80x25 text (80x25 text is always available).

</td>
</tr>
</tbody>
</table>

If you are not satisfied with videomode selected by `vesa` option, you can modify it with these options:


<table>
<tbody>
<tr>
<td>


xres:X

</td>
<td>


horizontal resolution, in pixels. Default is derived from `vesa` option.

</td>
</tr>
<tr>
<td>


yres:X

</td>
<td>


vertical resolution, in pixel lines. Default is derived from `vesa` option.

</td>
</tr>
<tr>
<td>


upper:X

</td>
<td>


top boundary: lines between end of VSYNC pulse and start of first pixel line of picture. Default is derived from `vesa` option.

</td>
</tr>
<tr>
<td>


lower:X

</td>
<td>


bottom boundary: lines between end of picture and start of VSYNC pulse. Default is derived from `vesa` option.

</td>
</tr>
<tr>
<td>


vslen:X

</td>
<td>


length of VSYNC pulse, in lines. Default is derived from `vesa` option.

</td>
</tr>
<tr>
<td>


left:X

</td>
<td>


left boundary: pixels between end of HSYNC pulse and first pixel. Default is derived from `vesa` option.

</td>
</tr>
<tr>
<td>


right:X

</td>
<td>


right boundary: pixels between end of picture and start of HSYNC pulse. Default is derived from `vesa` option.

</td>
</tr>
<tr>
<td>


hslen:X

</td>
<td>


length of HSYNC pulse, in pixels. Default is derived from `vesa` option.

</td>
</tr>
<tr>
<td>


pixclock:X

</td>
<td>


dotclocks, in ps (picoseconds). Default is derived from `vesa` option and from `fh` and `fv` options.

</td>
</tr>
<tr>
<td>


sync:X

</td>
<td>


sync. pulse - bit 0 inverts HSYNC polarity, bit 1 VSYNC polarity. If bit 3 (value 0x08) is set, composite sync instead of HSYNC is generated. If bit 5 (value 0x20) is set, sync on green is turned on. Do not forget that if you want sync on green, you also probably want composite sync. Default depends on `vesa`.

</td>
</tr>
<tr>
<td>


depth:X

</td>
<td>


Bits per pixel: 0=text, 4,8,15,16,24 or 32. Default depends on `vesa`.

</td>
</tr>
</tbody>
</table>

If you know capabilities of your monitor, you can specify some (or all) of `maxclk`, `fh` and `fv`. In this case, `pixclock` is computed so that pixclock &lt;= maxclk, real_fh &lt;= fh and real_fv &lt;= fv.


<table>
<tbody>
<tr>
<td>


maxclk:X

</td>
<td>


maximum dotclock. X can be specified in MHz, kHz or Hz. Default is ``don`t care``.

</td>
</tr>
<tr>
<td>


fh:X

</td>
<td>


maximum horizontal synchronization frequency. X can be specified in kHz or Hz. Default is `don't care`.

</td>
</tr>
<tr>
<td>


fv:X

</td>
<td>


maximum vertical frequency. X must be specified in Hz. Default is 70 for modes derived from `vesa` with yres &lt;= 400, 60Hz for yres &gt; 400.

</td>
</tr>
</tbody>
</table>

<a id="rst-limitations"></a>

## Limitations

There are known and unknown bugs, features and misfeatures. Currently there are following known bugs:

> - SVGALib does not restore screen on exit
>
> - generic fbcon-cfbX procedures do not work on Alphas. Due to this, `noaccel` (and cfb4 accel) driver does not work on Alpha. So everyone with access to `/dev/fb*` on Alpha can hang machine (you should restrict access to `/dev/fb*` - everyone with access to this device can destroy your monitor, believe me...).
>
> - 24bpp does not support correctly XF-FBDev on big-endian architectures.
>
> - interlaced text mode is not supported; it looks like hardware limitation, but I'm not sure.
>
> - Gxx0 SGRAM/SDRAM is not autodetected.
>
> - maybe more...

And following misfeatures:

> - SVGALib does not restore screen on exit.
>
> - pixclock for text modes is limited by hardware to
>
>   > - 83 MHz on G200
>   >
>   > - 66 MHz on Millennium I
>   >
>   > - 60 MHz on Millennium II
>
>   Because I have no access to other devices, I do not know specific frequencies for them. So driver does not check this and allows you to set frequency higher that this. It causes sparks, black holes and other pretty effects on screen. Device was not destroyed during tests. :-)
>
> - my Millennium G200 oscillator has frequency range from 35 MHz to 380 MHz (and it works with 8bpp on about 320 MHz dotclocks (and changed mclk)). But Matrox says on product sheet that VCO limit is 50-250 MHz, so I believe them (maybe that chip overheats, but it has a very big cooler (G100 has none), so it should work).
>
> - special mixed video/graphics videomodes of Mystique and Gx00 - 2G8V16 and G16V16 are not supported
>
> - color keying is not supported
>
> - feature connector of Mystique and Gx00 is set to VGA mode (it is disabled by BIOS)
>
> - DDC (monitor detection) is supported through dualhead driver
>
> - some check for input values are not so strict how it should be (you can specify vslen=4000 and so on).
>
> - maybe more...

And following features:

> - 4bpp is available only on Millennium I and Millennium II. It is hardware limitation.
>
> - selection between 1:5:5:5 and 5:6:5 16bpp videomode is done by -rgba option of fbset: "fbset -depth 16 -rgba 5,5,5" selects 1:5:5:5, anything else selects 5:6:5 mode.
>
> - text mode uses 6 bit VGA palette instead of 8 bit (one of 262144 colors instead of one of 16M colors). It is due to hardware limitation of Millennium I/II and SVGALib compatibility.

<a id="rst-benchmarks"></a>

## Benchmarks

It is time to redraw whole screen 1000 times in 1024x768, 60Hz. It is time for draw 6144000 characters on screen through /dev/vcsa (for 32bpp it is about 3GB of data (exactly 3000 MB); for 8x16 font in 16 seconds, i.e. 187 MBps). Times were obtained from one older version of driver, now they are about 3% faster, it is kernel-space only time on P-II/350 MHz, Millennium I in 33 MHz PCI slot, G200 in AGP 2x slot. I did not test vgacon:



```text
NOACCEL
      8x16                 12x22
      Millennium I  G200   Millennium I  G200
8bpp    16.42         9.54   12.33         9.13
16bpp   21.00        15.70   19.11        15.02
24bpp   36.66        36.66   35.00        35.00
32bpp   35.00        30.00   33.85        28.66

ACCEL, nofastfont
      8x16                 12x22                6x11
      Millennium I  G200   Millennium I  G200   Millennium I  G200
8bpp     7.79         7.24   13.55         7.78   30.00        21.01
16bpp    9.13         7.78   16.16         7.78   30.00        21.01
24bpp   14.17        10.72   18.69        10.24   34.99        21.01
32bpp   16.15      16.16   18.73        13.09   34.99        21.01

ACCEL, fastfont
      8x16                 12x22                6x11
      Millennium I  G200   Millennium I  G200   Millennium I  G200
8bpp     8.41         6.01    6.54         4.37   16.00        10.51
16bpp    9.54         9.12    8.76         6.17   17.52        14.01
24bpp   15.00        12.36   11.67        10.00   22.01        18.32
32bpp   16.18        18.29*  12.71        12.74   24.44        21.00

TEXT
      8x16
      Millennium I  G200
TEXT     3.29         1.50

* Yes, it is slower than Millennium I.
```

<a id="rst-dualhead-g400"></a>

## Dualhead G400

- **Driver supports dualhead G400 with some limitations:**

  - secondary head shares videomemory with primary head. It is not problem if you have 32MB of videoram, but if you have only 16MB, you may have to think twice before choosing videomode (for example twice 1880x1440x32bpp is not possible).

  - due to hardware limitation, secondary head can use only 16 and 32bpp videomodes.

  - secondary head is not accelerated. There were bad problems with accelerated XFree when secondary head used to use acceleration.

  - secondary head always powerups in [640x480@60-32](<mailto:640x480@60-32>) videomode. You have to use fbset to change this mode.

  - secondary head always powerups in monitor mode. You have to use fbmatroxset to change it to TV mode. Also, you must select at least 525 lines for NTSC output and 625 lines for PAL output.

  - kernel is not fully multihead ready. So some things are impossible to do.

  - if you compiled it as module, you must insert i2c-matroxfb, matroxfb_maven and matroxfb_crtc2 into kernel.

<a id="rst-dualhead-g450"></a>

## Dualhead G450

- **Driver supports dualhead G450 with some limitations:**

  - secondary head shares videomemory with primary head. It is not problem if you have 32MB of videoram, but if you have only 16MB, you may have to think twice before choosing videomode.

  - due to hardware limitation, secondary head can use only 16 and 32bpp videomodes.

  - secondary head is not accelerated.

  - secondary head always powerups in [640x480@60-32](<mailto:640x480@60-32>) videomode. You have to use fbset to change this mode.

  - TV output is not supported

  - kernel is not fully multihead ready, so some things are impossible to do.

  - if you compiled it as module, you must insert matroxfb_g450 and matroxfb_crtc2 into kernel.

Petr Vandrovec &lt;[vandrove@vc.cvut.cz](<mailto:vandrove@vc.cvut.cz>)&gt;
