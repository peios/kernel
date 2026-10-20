---
title: "Frame Buffer device internals"
type: reference
description: "This is a first start for some documentation about frame buffer device internals."
---

<a id="rst-frame-buffer-device-internals"></a>

This is a first start for some documentation about frame buffer device internals.

Authors:

- Geert Uytterhoeven &lt;[geert@linux-m68k.org](<mailto:geert@linux-m68k.org>)&gt;, 21 July 1998

- James Simmons &lt;[jsimmons@user.sf.net](<mailto:jsimmons@user.sf.net>)&gt;, Nov 26 2002

---

<a id="rst-structures-used-by-the-frame-buffer-device-api"></a>

## Structures used by the frame buffer device API

The following structures play a role in the game of frame buffer devices. They are defined in &lt;linux/fb.h&gt;.

1. Outside the kernel (user space)

> - struct fb_fix_screeninfo
>
>   Device independent unchangeable information about a frame buffer device and a specific video mode. This can be obtained using the FBIOGET_FSCREENINFO ioctl.
>
> - struct fb_var_screeninfo
>
>   Device independent changeable information about a frame buffer device and a specific video mode. This can be obtained using the FBIOGET_VSCREENINFO ioctl, and updated with the FBIOPUT_VSCREENINFO ioctl. If you want to pan the screen only, you can use the FBIOPAN_DISPLAY ioctl.
>
> - struct fb_cmap
>
>   Device independent colormap information. You can get and set the colormap using the FBIOGETCMAP and FBIOPUTCMAP ioctls.

2. Inside the kernel

> - struct fb_info
>
>   Generic information, API and low level information about a specific frame buffer device instance (slot number, board address, ...).
>
> - struct `par`
>
>   Device dependent information that uniquely defines the video mode for this particular piece of hardware.

<a id="rst-visuals-used-by-the-frame-buffer-device-api"></a>

## Visuals used by the frame buffer device API

<a id="rst-monochrome-fb-visual-mono01-and-fb-visual-mono10"></a>

### Monochrome (FB_VISUAL_MONO01 and FB_VISUAL_MONO10)

Each pixel is either black or white.

<a id="rst-pseudo-color-fb-visual-pseudocolor-and-fb-visual-static-pseudocolor"></a>

### Pseudo color (FB_VISUAL_PSEUDOCOLOR and FB_VISUAL_STATIC_PSEUDOCOLOR)

The whole pixel value is fed through a programmable lookup table that has one color (including red, green, and blue intensities) for each possible pixel value, and that color is displayed.

<a id="rst-true-color-fb-visual-truecolor"></a>

### True color (FB_VISUAL_TRUECOLOR)

The pixel value is broken up into red, green, and blue fields.

<a id="rst-direct-color-fb-visual-directcolor"></a>

### Direct color (FB_VISUAL_DIRECTCOLOR)

The pixel value is broken up into red, green, and blue fields, each of which are looked up in separate red, green, and blue lookup tables.

<a id="rst-grayscale-displays"></a>

### Grayscale displays

Grayscale and static grayscale are special variants of pseudo color and static pseudo color, where the red, green and blue components are always equal to each other.
