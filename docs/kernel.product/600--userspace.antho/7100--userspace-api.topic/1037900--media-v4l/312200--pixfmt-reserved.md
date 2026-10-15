---
title: "Reserved Format Identifiers"
type: reference
description: "These formats are not defined by this specification, they are just listed for reference and to avoid naming conflicts. If you want to register your own format, send an e-mail to the linux-media mailing list https://linuxtv.org/lists.php…"
---

<a id="rst-reserved-format-identifiers"></a>
<a id="rst-pixfmt-reserved"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

These formats are not defined by this specification, they are just listed for reference and to avoid naming conflicts. If you want to register your own format, send an e-mail to the linux-media mailing list [https://linuxtv.org/lists.php](<https://linuxtv.org/lists.php>) for inclusion in the `videodev2.h` file. If you want to share your format with other developers add a link to your documentation and send a copy to the linux-media mailing list for inclusion in this section. If you think your format should be listed in a standard format section please make a proposal on the linux-media mailing list.

<!-- tabularcolumns: |p{6.6cm}|p{2.2cm}|p{8.5cm}| -->

<!-- Source LaTeX layout: \small -->

<a id="rst-reserved-formats"></a>


<table>
<caption>

Reserved Image Formats

</caption>
<thead>
<tr>
<th>



Identifier

</th>
<th>



Code

</th>
<th>



Details

</th>
</tr>
</thead>
<tbody>
<tr>
<td>



`V4L2_PIX_FMT_DV`

</td>
<td>



'dvsd'

</td>
<td>



<a id="rst-v4l2-pix-fmt-dv"></a>

unknown

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_ET61X251`

</td>
<td>



'E625'

</td>
<td>



<a id="rst-v4l2-pix-fmt-et61x251"></a>

Compressed format of the ET61X251 driver.

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_HI240`

</td>
<td>



'HI24'

</td>
<td>



<a id="rst-v4l2-pix-fmt-hi240"></a>

8 bit RGB format used by the BTTV driver.

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_CPIA1`

</td>
<td>



'CPIA'

</td>
<td>



<a id="rst-v4l2-pix-fmt-cpia1"></a>

YUV format used by the gspca cpia1 driver.

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_JPGL`

</td>
<td>



'JPGL'

</td>
<td>



<a id="rst-v4l2-pix-fmt-jpgl"></a>

JPEG-Light format (Pegasus Lossless JPEG) used in Divio webcams NW 80x.

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_SPCA501`

</td>
<td>



'S501'

</td>
<td>



<a id="rst-v4l2-pix-fmt-spca501"></a>

YUYV per line used by the gspca driver.

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_SPCA505`

</td>
<td>



'S505'

</td>
<td>



<a id="rst-v4l2-pix-fmt-spca505"></a>

YYUV per line used by the gspca driver.

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_SPCA508`

</td>
<td>



'S508'

</td>
<td>



<a id="rst-v4l2-pix-fmt-spca508"></a>

YUVY per line used by the gspca driver.

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_SPCA561`

</td>
<td>



'S561'

</td>
<td>



<a id="rst-v4l2-pix-fmt-spca561"></a>

Compressed GBRG Bayer format used by the gspca driver.

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_PAC207`

</td>
<td>



'P207'

</td>
<td>



<a id="rst-v4l2-pix-fmt-pac207"></a>

Compressed BGGR Bayer format used by the gspca driver.

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_MR97310A`

</td>
<td>



'M310'

</td>
<td>



<a id="rst-v4l2-pix-fmt-mr97310a"></a>

Compressed BGGR Bayer format used by the gspca driver.

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_JL2005BCD`

</td>
<td>



'JL20'

</td>
<td>



<a id="rst-v4l2-pix-fmt-jl2005bcd"></a>

JPEG compressed RGGB Bayer format used by the gspca driver.

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_OV511`

</td>
<td>



'O511'

</td>
<td>



<a id="rst-v4l2-pix-fmt-ov511"></a>

OV511 JPEG format used by the gspca driver.

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_OV518`

</td>
<td>



'O518'

</td>
<td>



<a id="rst-v4l2-pix-fmt-ov518"></a>

OV518 JPEG format used by the gspca driver.

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_PJPG`

</td>
<td>



'PJPG'

</td>
<td>



<a id="rst-v4l2-pix-fmt-pjpg"></a>

Pixart 73xx JPEG format used by the gspca driver.

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_SE401`

</td>
<td>



'S401'

</td>
<td>



<a id="rst-v4l2-pix-fmt-se401"></a>

Compressed RGB format used by the gspca se401 driver

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_SQ905C`

</td>
<td>



'905C'

</td>
<td>



<a id="rst-v4l2-pix-fmt-sq905c"></a>

Compressed RGGB bayer format used by the gspca driver.

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_MJPEG`

</td>
<td>



'MJPG'

</td>
<td>



<a id="rst-v4l2-pix-fmt-mjpeg"></a>

Compressed format used by the Zoran driver

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_PWC1`

</td>
<td>



'PWC1'

</td>
<td>



<a id="rst-v4l2-pix-fmt-pwc1"></a>

Compressed format of the PWC driver.

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_PWC2`

</td>
<td>



'PWC2'

</td>
<td>



<a id="rst-v4l2-pix-fmt-pwc2"></a>

Compressed format of the PWC driver.

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_SN9C10X`

</td>
<td>



'S910'

</td>
<td>



<a id="rst-v4l2-pix-fmt-sn9c10x"></a>

Compressed format of the SN9C102 driver.

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_SN9C20X_I420`

</td>
<td>



'S920'

</td>
<td>



<a id="rst-v4l2-pix-fmt-sn9c20x-i420"></a>

YUV 4:2:0 format of the gspca sn9c20x driver.

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_SN9C2028`

</td>
<td>



'SONX'

</td>
<td>



<a id="rst-v4l2-pix-fmt-sn9c2028"></a>

Compressed GBRG bayer format of the gspca sn9c2028 driver.

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_STV0680`

</td>
<td>



'S680'

</td>
<td>



<a id="rst-v4l2-pix-fmt-stv0680"></a>

Bayer format of the gspca stv0680 driver.

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_WNVA`

</td>
<td>



'WNVA'

</td>
<td>



<a id="rst-v4l2-pix-fmt-wnva"></a>

Used by the Winnov Videum driver, [http://www.thedirks.org/winnov/](<http://www.thedirks.org/winnov/>)

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_TM6000`

</td>
<td>



'TM60'

</td>
<td>



<a id="rst-v4l2-pix-fmt-tm6000"></a>

Used by Trident tm6000

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_CIT_YYVYUY`

</td>
<td>



'CITV'

</td>
<td>



<a id="rst-v4l2-pix-fmt-cit-yyvyuy"></a>

Used by xirlink CIT, found at IBM webcams.

Uses one line of Y then 1 line of VYUY

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_KONICA420`

</td>
<td>



'KONI'

</td>
<td>



<a id="rst-v4l2-pix-fmt-konica420"></a>

Used by Konica webcams.

YUV420 planar in blocks of 256 pixels.

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_YYUV`

</td>
<td>



'YYUV'

</td>
<td>



<a id="rst-v4l2-pix-fmt-yyuv"></a>

unknown

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_Y4`

</td>
<td>



'Y04 '

</td>
<td>



<a id="rst-v4l2-pix-fmt-y4"></a>

Old 4-bit greyscale format. Only the most significant 4 bits of each byte are used, the other bits are set to 0.

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_Y6`

</td>
<td>



'Y06 '

</td>
<td>



<a id="rst-v4l2-pix-fmt-y6"></a>

Old 6-bit greyscale format. Only the most significant 6 bits of each byte are used, the other bits are set to 0.

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_S5C_UYVY_JPG`

</td>
<td>



'S5CI'

</td>
<td>



<a id="rst-v4l2-pix-fmt-s5c-uyvy-jpg"></a>

Two-planar format used by Samsung S5C73MX cameras. The first plane contains interleaved JPEG and UYVY image data, followed by meta data in form of an array of offsets to the UYVY data blocks. The actual pointer array follows immediately the interleaved JPEG/UYVY data, the number of entries in this array equals the height of the UYVY image. Each entry is a 4-byte unsigned integer in big endian order and it's an offset to a single pixel line of the UYVY image. The first plane can start either with JPEG or UYVY data chunk. The size of a single UYVY block equals the UYVY image's width multiplied by 2. The size of a JPEG chunk depends on the image and can vary with each line.

The second plane, at an offset of 4084 bytes, contains a 4-byte offset to the pointer array in the first plane. This offset is followed by a 4-byte value indicating size of the pointer array. All numbers in the second plane are also in big endian order. Remaining data in the second plane is undefined. The information in the second plane allows to easily find location of the pointer array, which can be different for each frame. The size of the pointer array is constant for given UYVY image height.

In order to extract UYVY and JPEG frames an application can initially set a data pointer to the start of first plane and then add an offset from the first entry of the pointers table. Such a pointer indicates start of an UYVY image pixel line. Whole UYVY line can be copied to a separate buffer. These steps should be repeated for each line, i.e. the number of entries in the pointer array. Anything what's in between the UYVY lines is JPEG data and should be concatenated to form the JPEG stream.

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_MT21C`

</td>
<td>



'MT21'

</td>
<td>



<a id="rst-v4l2-pix-fmt-mt21c"></a>

Compressed two-planar YVU420 format used by Mediatek MT8173, MT8192, MT8195 and more. The compression is lossless. This format have similitude with `V4L2_PIX_FMT_MM21` in term of alignment and tiling. It remains an opaque intermediate format and the MDP hardware must be used to convert `V4L2_PIX_FMT_MT21C` to `V4L2_PIX_FMT_NV12M`, `V4L2_PIX_FMT_YUV420M` or `V4L2_PIX_FMT_YVU420`.

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_QC08C`

</td>
<td>



'QC08C'

</td>
<td>



<a id="rst-v4l2-pix-fmt-qc08c"></a>

Compressed Macro-tile 8-Bit YUV420 format used by Qualcomm platforms. It is an opaque intermediate format. The used compression is lossless and it is used by various multimedia hardware blocks like GPU, display controllers, ISP and video accelerators. It contains four planes for progressive video and eight planes for interlaced video.

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_QC10C`

</td>
<td>



'QC10C'

</td>
<td>



<a id="rst-v4l2-pix-fmt-qc10c"></a>

Compressed Macro-tile 10-Bit YUV420 format used by Qualcomm platforms. It is an opaque intermediate format. The used compression is lossless and it is used by various multimedia hardware blocks like GPU, display controllers, ISP and video accelerators. It contains four planes for progressive video.

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_AJPG`

</td>
<td>



'AJPG'

</td>
<td>



<a id="rst-v4l2-pix-fmt-ajpg"></a>

ASPEED JPEG format used by the aspeed-video driver on Aspeed platforms, which is generally adapted for remote KVM. On each frame compression, I will compare the new frame with previous one to decide which macroblock's data is changed, and only the changed macroblocks will be compressed.

The implementation is based on AST2600 A3 datasheet, revision 0.9, which is not publicly available. Or you can reference Video stream data format – ASPEED mode compression of SDK\_User\_Guide which available on [github](<https://github.com/AspeedTech-BMC/openbmc/releases/>).

Decoder's implementation can be found here, [aspeed\_codec](<https://github.com/AspeedTech-BMC/aspeed_codec/>)

</td>
</tr>
<tr>
<td>



`V4L2_PIX_FMT_HEXTILE`

</td>
<td>



'HXTL'

</td>
<td>



<a id="rst-v4l2-pix-fmt-hextile"></a>

Compressed format used by Nuvoton NPCM video driver. This format is defined in Remote Framebuffer Protocol (RFC 6143, chapter 7.7.4 Hextile Encoding).

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->
