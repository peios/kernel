---
title: "ioctl VIDIOC_G_FBUF, VIDIOC_S_FBUF"
type: reference
description: "VIDIOC_G_FBUF - VIDIOC_S_FBUF - Get or set frame buffer overlay parameters"
---

<a id="rst-ioctl-vidioc-g-fbuf-vidioc-s-fbuf"></a>
<a id="rst-vidioc-g-fbuf"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

VIDIOC\_G\_FBUF - VIDIOC\_S\_FBUF - Get or set frame buffer overlay parameters

<a id="rst-synopsis"></a>

## Synopsis

<a id="c-VIDIOC_G_FBUF"></a>



```c
VIDIOC_G_FBUF
```

`int ioctl(int fd, VIDIOC_G_FBUF, struct v4l2_framebuffer *argp)`

<a id="c-VIDIOC_S_FBUF"></a>



```c
VIDIOC_S_FBUF
```

`int ioctl(int fd, VIDIOC_S_FBUF, const struct v4l2_framebuffer *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to struct `v4l2_framebuffer`.

<a id="rst-description"></a>

## Description

Applications can use the [VIDIOC\_G\_FBUF](<#rst-vidioc-g-fbuf>) and [VIDIOC\_S\_FBUF](<#rst-vidioc-g-fbuf>) ioctl to get and set the framebuffer parameters for a [Video Overlay](<~kernel/userspace/userspace-api/media-v4l/dev-overlay#rst-overlay>) or [Video Output Overlay](<~kernel/userspace/userspace-api/media-v4l/dev-osd#rst-osd>) (OSD). The type of overlay is implied by the device type (capture or output device) and can be determined with the [vidioc\_querycap](<~kernel/userspace/userspace-api/media-v4l/vidioc-querycap#rst-vidioc-querycap>) ioctl. One `/dev/videoN` device must not support both kinds of overlay.

The V4L2 API distinguishes destructive and non-destructive overlays. A destructive overlay copies captured video images into the video memory of a graphics card. A non-destructive overlay blends video images into a VGA signal or graphics into a video signal. <em>Video Output Overlays</em> are always non-destructive.

Destructive overlay support has been removed: with modern GPUs and CPUs this is no longer needed, and it was always a very dangerous feature.

To get the current parameters applications call the [VIDIOC\_G\_FBUF](<#rst-vidioc-g-fbuf>) ioctl with a pointer to a struct `v4l2_framebuffer` structure. The driver fills all fields of the structure or returns an EINVAL error code when overlays are not supported.

To set the parameters for a <em>Video Output Overlay</em>, applications must initialize the `flags` field of a struct `v4l2_framebuffer`. Since the framebuffer is implemented on the TV card all other parameters are determined by the driver. When an application calls [VIDIOC\_S\_FBUF](<#rst-vidioc-g-fbuf>) with a pointer to this structure, the driver prepares for the overlay and returns the framebuffer parameters as [VIDIOC\_G\_FBUF](<#rst-vidioc-g-fbuf>) does, or it returns an error code.

To set the parameters for a <em>Video Capture Overlay</em> applications must initialize the `flags` field, the `fmt` substructure, and call [VIDIOC\_S\_FBUF](<#rst-vidioc-g-fbuf>). Again the driver prepares for the overlay and returns the framebuffer parameters as [VIDIOC\_G\_FBUF](<#rst-vidioc-g-fbuf>) does, or it returns an error code.

<!-- tabularcolumns: |p{3.5cm}|p{3.5cm}|p{3.5cm}|p{6.6cm}| -->

<a id="c-v4l2_framebuffer"></a>



```c
v4l2_framebuffer
```


<table>
<caption>

struct v4l2\_framebuffer

</caption>
<tbody>
<tr>
<td>



\_\_u32

</td>
<td>



`capability`

</td>
<td>





</td>
<td>



Overlay capability flags set by the driver, see [framebuffer-cap](<#rst-framebuffer-cap>).

</td>
</tr>
<tr>
<td>



\_\_u32

</td>
<td>



`flags`

</td>
<td>





</td>
<td>



Overlay control flags set by application and driver, see [framebuffer-flags](<#rst-framebuffer-flags>)

</td>
</tr>
<tr>
<td>



void \*

</td>
<td>



`base`

</td>
<td>





</td>
<td>



Physical base address of the framebuffer, that is the address of the pixel in the top left corner of the framebuffer. For [VIDIOC\_S\_FBUF](<#rst-vidioc-g-fbuf>) this field is no longer supported and the kernel will always set this to NULL. For <em>Video Output Overlays</em> the driver will return a valid base address, so applications can find the corresponding Linux framebuffer device (see [osd](<~kernel/userspace/userspace-api/media-v4l/dev-osd#rst-osd>)). For <em>Video Capture Overlays</em> this field will always be NULL.

</td>
</tr>
<tr>
<td>



struct

</td>
<td>



`fmt`

</td>
<td>





</td>
<td>



Layout of the frame buffer.

</td>
</tr>
<tr>
<td>





</td>
<td>



\_\_u32

</td>
<td>



`width`

</td>
<td>



Width of the frame buffer in pixels.

</td>
</tr>
<tr>
<td>





</td>
<td>



\_\_u32

</td>
<td>



`height`

</td>
<td>



Height of the frame buffer in pixels.

</td>
</tr>
<tr>
<td>





</td>
<td>



\_\_u32

</td>
<td>



`pixelformat`

</td>
<td>



The pixel format of the framebuffer.

</td>
</tr>
<tr>
<td>





</td>
<td>





</td>
<td>





</td>
<td>



For <em>non-destructive Video Overlays</em> this field only defines a format for the struct `v4l2_window` `chromakey` field.

</td>
</tr>
<tr>
<td>





</td>
<td>





</td>
<td>





</td>
<td>



For <em>Video Output Overlays</em> the driver must return a valid format.

</td>
</tr>
<tr>
<td>





</td>
<td>





</td>
<td>





</td>
<td>



Usually this is an RGB format (for example [V4L2\_PIX\_FMT\_RGB565](<~kernel/userspace/userspace-api/media-v4l/pixfmt-rgb#rst-v4l2-pix-fmt-rgb565>)) but YUV formats (only packed YUV formats when chroma keying is used, not including `V4L2_PIX_FMT_YUYV` and `V4L2_PIX_FMT_UYVY`) and the `V4L2_PIX_FMT_PAL8` format are also permitted. The behavior of the driver when an application requests a compressed format is undefined. See [pixfmt](<~kernel/userspace/userspace-api/media-v4l/pixfmt#rst-pixfmt>) for information on pixel formats.

</td>
</tr>
<tr>
<td>





</td>
<td>



enum `v4l2_field`

</td>
<td>



`field`

</td>
<td>



Drivers and applications shall ignore this field. If applicable, the field order is selected with the [VIDIOC\_S\_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-fmt#rst-vidioc-g-fmt>) ioctl, using the `field` field of struct `v4l2_window`.

</td>
</tr>
<tr>
<td>





</td>
<td>



\_\_u32

</td>
<td>



`bytesperline`

</td>
<td>



Distance in bytes between the leftmost pixels in two adjacent lines.

</td>
</tr>
<tr>
<td colspan="4">



This field is irrelevant to <em>non-destructive Video Overlays</em>.

For <em>Video Output Overlays</em> the driver must return a valid value.

Video hardware may access padding bytes, therefore they must reside in accessible memory. Consider for example the case where padding bytes after the last line of an image cross a system page boundary. Capture devices may write padding bytes, the value is undefined. Output devices ignore the contents of padding bytes.

When the image format is planar the `bytesperline` value applies to the first plane and is divided by the same factor as the `width` field for the other planes. For example the Cb and Cr planes of a YUV 4:2:0 image have half as many padding bytes following each line as the Y plane. To avoid ambiguities drivers must return a `bytesperline` value rounded up to a multiple of the scale factor.

</td>
</tr>
<tr>
<td>





</td>
<td>



\_\_u32

</td>
<td>



`sizeimage`

</td>
<td>



This field is irrelevant to <em>non-destructive Video Overlays</em>. For <em>Video Output Overlays</em> the driver must return a valid format.

Together with `base` it defines the framebuffer memory accessible by the driver.

</td>
</tr>
<tr>
<td>





</td>
<td>



enum `v4l2_colorspace`

</td>
<td>



`colorspace`

</td>
<td>



This information supplements the `pixelformat` and must be set by the driver, see [colorspaces](<~kernel/userspace/userspace-api/media-v4l/colorspaces#rst-colorspaces-1>).

</td>
</tr>
<tr>
<td>





</td>
<td>



\_\_u32

</td>
<td>



`priv`

</td>
<td>



Reserved. Drivers and applications must set this field to zero.

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{7.4cm}|p{1.6cm}|p{8.3cm}| -->

<a id="rst-framebuffer-cap"></a>


<table>
<caption>

Frame Buffer Capability Flags

</caption>
<tbody>
<tr>
<td>



`V4L2_FBUF_CAP_EXTERNOVERLAY`

</td>
<td>



0x0001

</td>
<td>



The device is capable of non-destructive overlays. When the driver clears this flag, only destructive overlays are supported. There are no drivers yet which support both destructive and non-destructive overlays. Video Output Overlays are in practice always non-destructive.

</td>
</tr>
<tr>
<td>



`V4L2_FBUF_CAP_CHROMAKEY`

</td>
<td>



0x0002

</td>
<td>



The device supports clipping by chroma-keying the images. That is, image pixels replace pixels in the VGA or video signal only where the latter assume a certain color. Chroma-keying makes no sense for destructive overlays.

</td>
</tr>
<tr>
<td>



`V4L2_FBUF_CAP_LIST_CLIPPING`

</td>
<td>



0x0004

</td>
<td>



The device supports clipping using a list of clip rectangles. Note that this is no longer supported.

</td>
</tr>
<tr>
<td>



`V4L2_FBUF_CAP_BITMAP_CLIPPING`

</td>
<td>



0x0008

</td>
<td>



The device supports clipping using a bit mask. Note that this is no longer supported.

</td>
</tr>
<tr>
<td>



`V4L2_FBUF_CAP_LOCAL_ALPHA`

</td>
<td>



0x0010

</td>
<td>



The device supports clipping/blending using the alpha channel of the framebuffer or VGA signal. Alpha blending makes no sense for destructive overlays.

</td>
</tr>
<tr>
<td>



`V4L2_FBUF_CAP_GLOBAL_ALPHA`

</td>
<td>



0x0020

</td>
<td>



The device supports alpha blending using a global alpha value. Alpha blending makes no sense for destructive overlays.

</td>
</tr>
<tr>
<td>



`V4L2_FBUF_CAP_LOCAL_INV_ALPHA`

</td>
<td>



0x0040

</td>
<td>



The device supports clipping/blending using the inverted alpha channel of the framebuffer or VGA signal. Alpha blending makes no sense for destructive overlays.

</td>
</tr>
<tr>
<td>



`V4L2_FBUF_CAP_SRC_CHROMAKEY`

</td>
<td>



0x0080

</td>
<td>



The device supports Source Chroma-keying. Video pixels with the chroma-key colors are replaced by framebuffer pixels, which is exactly opposite of `V4L2_FBUF_CAP_CHROMAKEY`

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{7.4cm}|p{1.6cm}|p{8.3cm}| -->

<a id="rst-framebuffer-flags"></a>


<table>
<caption>

Frame Buffer Flags

</caption>
<tbody>
<tr>
<td>



`V4L2_FBUF_FLAG_PRIMARY`

</td>
<td>



0x0001

</td>
<td>



The framebuffer is the primary graphics surface. In other words, the overlay is destructive. This flag is typically set by any driver that doesn't have the `V4L2_FBUF_CAP_EXTERNOVERLAY` capability and it is cleared otherwise.

</td>
</tr>
<tr>
<td>



`V4L2_FBUF_FLAG_OVERLAY`

</td>
<td>



0x0002

</td>
<td>



If this flag is set for a video capture device, then the driver will set the initial overlay size to cover the full framebuffer size, otherwise the existing overlay size (as set by [VIDIOC\_S\_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-fmt#rst-vidioc-g-fmt>)) will be used. Only one video capture driver (bttv) supports this flag. The use of this flag for capture devices is deprecated. There is no way to detect which drivers support this flag, so the only reliable method of setting the overlay size is through [VIDIOC\_S\_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-fmt#rst-vidioc-g-fmt>). If this flag is set for a video output device, then the video output overlay window is relative to the top-left corner of the framebuffer and restricted to the size of the framebuffer. If it is cleared, then the video output overlay window is relative to the video output display.

</td>
</tr>
<tr>
<td>



`V4L2_FBUF_FLAG_CHROMAKEY`

</td>
<td>



0x0004

</td>
<td>



Use chroma-keying. The chroma-key color is determined by the `chromakey` field of struct `v4l2_window` and negotiated with the [VIDIOC\_S\_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-fmt#rst-vidioc-g-fmt>) ioctl, see [Video Overlay Interface](<~kernel/userspace/userspace-api/media-v4l/dev-overlay#rst-overlay>) and [osd](<~kernel/userspace/userspace-api/media-v4l/dev-osd#rst-osd>).

</td>
</tr>
<tr>
<td colspan="3">



 There are no flags to enable clipping using a list of clip rectangles or a bitmap. These methods are negotiated with the [VIDIOC\_S\_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-fmt#rst-vidioc-g-fmt>) ioctl, see [Video Overlay Interface](<~kernel/userspace/userspace-api/media-v4l/dev-overlay#rst-overlay>) and [osd](<~kernel/userspace/userspace-api/media-v4l/dev-osd#rst-osd>).

</td>
</tr>
<tr>
<td>



`V4L2_FBUF_FLAG_LOCAL_ALPHA`

</td>
<td>



0x0008

</td>
<td>



Use the alpha channel of the framebuffer to clip or blend framebuffer pixels with video images. The blend function is: output = framebuffer pixel \* alpha + video pixel \* (1 - alpha). The actual alpha depth depends on the framebuffer pixel format.

</td>
</tr>
<tr>
<td>



`V4L2_FBUF_FLAG_GLOBAL_ALPHA`

</td>
<td>



0x0010

</td>
<td>



Use a global alpha value to blend the framebuffer with video images. The blend function is: output = (framebuffer pixel \* alpha + video pixel \* (255 - alpha)) / 255. The alpha value is determined by the `global_alpha` field of struct `v4l2_window` and negotiated with the [VIDIOC\_S\_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-fmt#rst-vidioc-g-fmt>) ioctl, see [Video Overlay Interface](<~kernel/userspace/userspace-api/media-v4l/dev-overlay#rst-overlay>) and [osd](<~kernel/userspace/userspace-api/media-v4l/dev-osd#rst-osd>).

</td>
</tr>
<tr>
<td>



`V4L2_FBUF_FLAG_LOCAL_INV_ALPHA`

</td>
<td>



0x0020

</td>
<td>



Like `V4L2_FBUF_FLAG_LOCAL_ALPHA`, use the alpha channel of the framebuffer to clip or blend framebuffer pixels with video images, but with an inverted alpha value. The blend function is: output = framebuffer pixel \* (1 - alpha) + video pixel \* alpha. The actual alpha depth depends on the framebuffer pixel format.

</td>
</tr>
<tr>
<td>



`V4L2_FBUF_FLAG_SRC_CHROMAKEY`

</td>
<td>



0x0040

</td>
<td>



Use source chroma-keying. The source chroma-key color is determined by the `chromakey` field of struct `v4l2_window` and negotiated with the [VIDIOC\_S\_FMT](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-fmt#rst-vidioc-g-fmt>) ioctl, see [Video Overlay Interface](<~kernel/userspace/userspace-api/media-v4l/dev-overlay#rst-overlay>) and [osd](<~kernel/userspace/userspace-api/media-v4l/dev-osd#rst-osd>). Both chroma-keying are mutual exclusive to each other, so same `chromakey` field of struct `v4l2_window` is being used.

</td>
</tr>
</tbody>
</table>

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

- **EPERM**

  [VIDIOC\_S\_FBUF](<#rst-vidioc-g-fbuf>) can only be called by a privileged user to negotiate the parameters for a destructive overlay.

- **EINVAL**

  The [VIDIOC\_S\_FBUF](<#rst-vidioc-g-fbuf>) parameters are unsuitable.
