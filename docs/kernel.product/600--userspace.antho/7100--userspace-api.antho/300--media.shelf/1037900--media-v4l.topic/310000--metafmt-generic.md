---
title: "V4L2_META_FMT_GENERIC_8 ('MET8'), V4L2_META_FMT_GENERIC_CSI2_10 ('MC1A'), V4L2_META_FMT_GENERIC_CSI2_12 ('MC1C'), V4L2_META_FMT_GENERIC_CSI2_14 ('MC1E'), V4L2_META_FMT_GENERIC_CSI2_16 ('MC1G'), V4L2_META_FMT_GENERIC_CSI2_20 ('MC1K'), V4L2_META_FMT_GENERIC_CSI2_24 ('MC1O')"
type: reference
description: "Generic line-based metadata formats"
---

<a id="rst-v4l2-meta-fmt-generic-8-met8-v4l2-meta-fmt-generic-csi2-10-mc1a-v4l2-meta-fmt-generic-csi2-12-mc1c-v4l2-meta-fmt-generic-csi2-14-mc1e-v4l2-meta-fmt-generic-csi2-16-mc1g-v4l2-meta-fmt-generic-csi2-20-mc1k-v4l2-meta-fmt-generic-csi2-24-mc1o"></a>

<!-- SPDX-License-Identifier: GPL-2.0 OR GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

Generic line-based metadata formats

<a id="rst-description"></a>

## Description

These generic line-based metadata formats define the memory layout of the data without defining the format or meaning of the metadata itself.

<a id="rst-v4l2-meta-fmt-generic-8-1"></a>
<a id="rst-v4l2-meta-fmt-generic-8"></a>

### V4L2\_META\_FMT\_GENERIC\_8

The V4L2\_META\_FMT\_GENERIC\_8 format is a plain 8-bit metadata format. This format is used on CSI-2 for 8 bits per [Data Unit](<~kernel/userspace/userspace-api/media/glossary#rst-term-data-unit>).

Additionally it is used for 16 bits per Data Unit when two bytes of metadata are packed into one 16-bit Data Unit. Otherwise the 16 bits per pixel dataformat is [V4L2\_META\_FMT\_GENERIC\_CSI2\_16](<#rst-v4l2-meta-fmt-generic-csi2-16>).

<strong>Byte Order Of V4L2\_META\_FMT\_GENERIC\_8.</strong> Each cell is one byte. "M" denotes a byte of metadata.

<!-- tabularcolumns: |p{2.4cm}|p{1.2cm}|p{1.2cm}|p{1.2cm}|p{1.2cm}| -->


<table>
<caption>

Sample 4x2 Metadata Frame

</caption>
<tbody>
<tr>
<td>



start + 0:

</td>
<td>



M<sub>00</sub>

</td>
<td>



M<sub>10</sub>

</td>
<td>



M<sub>20</sub>

</td>
<td>



M<sub>30</sub>

</td>
</tr>
<tr>
<td>



start + 4:

</td>
<td>



M<sub>01</sub>

</td>
<td>



M<sub>11</sub>

</td>
<td>



M<sub>21</sub>

</td>
<td>



M<sub>31</sub>

</td>
</tr>
</tbody>
</table>

<a id="rst-v4l2-meta-fmt-generic-csi2-10-1"></a>
<a id="rst-v4l2-meta-fmt-generic-csi2-10"></a>

### V4L2\_META\_FMT\_GENERIC\_CSI2\_10

V4L2\_META\_FMT\_GENERIC\_CSI2\_10 contains 8-bit generic metadata packed in 10-bit Data Units, with one padding byte after every four bytes of metadata. This format is typically used by CSI-2 receivers with a source that transmits MEDIA\_BUS\_FMT\_META\_10 and the CSI-2 receiver writes the received data to memory as-is.

The packing of the data follows the MIPI CSI-2 specification and the padding of the data is defined in the MIPI CCS specification.

This format is also used in conjunction with 20 bits per [Data Unit](<~kernel/userspace/userspace-api/media/glossary#rst-term-data-unit>) formats that pack two bytes of metadata into one Data Unit. Otherwise the 20 bits per pixel dataformat is [V4L2\_META\_FMT\_GENERIC\_CSI2\_20](<#rst-v4l2-meta-fmt-generic-csi2-20>).

This format is little endian.

<strong>Byte Order Of V4L2\_META\_FMT\_GENERIC\_CSI2\_10.</strong> Each cell is one byte. "M" denotes a byte of metadata and "x" a byte of padding.

<!-- tabularcolumns: |p{2.4cm}|p{1.2cm}|p{1.2cm}|p{1.2cm}|p{1.2cm}|p{1.8cm}| -->


<table>
<caption>

Sample 4x2 Metadata Frame

</caption>
<tbody>
<tr>
<td>



start + 0:

</td>
<td>



M<sub>00</sub>

</td>
<td>



M<sub>10</sub>

</td>
<td>



M<sub>20</sub>

</td>
<td>



M<sub>30</sub>

</td>
<td>



x

</td>
</tr>
<tr>
<td>



start + 5:

</td>
<td>



M<sub>01</sub>

</td>
<td>



M<sub>11</sub>

</td>
<td>



M<sub>21</sub>

</td>
<td>



M<sub>31</sub>

</td>
<td>



x

</td>
</tr>
</tbody>
</table>

<a id="rst-v4l2-meta-fmt-generic-csi2-12-1"></a>
<a id="rst-v4l2-meta-fmt-generic-csi2-12"></a>

### V4L2\_META\_FMT\_GENERIC\_CSI2\_12

V4L2\_META\_FMT\_GENERIC\_CSI2\_12 contains 8-bit generic metadata packed in 12-bit Data Units, with one padding byte after every two bytes of metadata. This format is typically used by CSI-2 receivers with a source that transmits MEDIA\_BUS\_FMT\_META\_12 and the CSI-2 receiver writes the received data to memory as-is.

The packing of the data follows the MIPI CSI-2 specification and the padding of the data is defined in the MIPI CCS specification.

This format is also used in conjunction with 24 bits per [Data Unit](<~kernel/userspace/userspace-api/media/glossary#rst-term-data-unit>) formats that pack two bytes of metadata into one Data Unit. Otherwise the 24 bits per pixel dataformat is [V4L2\_META\_FMT\_GENERIC\_CSI2\_24](<#rst-v4l2-meta-fmt-generic-csi2-24>).

This format is little endian.

<strong>Byte Order Of V4L2\_META\_FMT\_GENERIC\_CSI2\_12.</strong> Each cell is one byte. "M" denotes a byte of metadata and "x" a byte of padding.

<!-- tabularcolumns: |p{2.4cm}|p{1.2cm}|p{1.2cm}|p{1.8cm}|p{1.2cm}|p{1.2cm}|p{1.8cm}| -->


<table>
<caption>

Sample 4x2 Metadata Frame

</caption>
<tbody>
<tr>
<td>



start + 0:

</td>
<td>



M<sub>00</sub>

</td>
<td>



M<sub>10</sub>

</td>
<td>



x

</td>
<td>



M<sub>20</sub>

</td>
<td>



M<sub>30</sub>

</td>
<td>



x

</td>
</tr>
<tr>
<td>



start + 6:

</td>
<td>



M<sub>01</sub>

</td>
<td>



M<sub>11</sub>

</td>
<td>



x

</td>
<td>



M<sub>21</sub>

</td>
<td>



M<sub>31</sub>

</td>
<td>



x

</td>
</tr>
</tbody>
</table>

<a id="rst-v4l2-meta-fmt-generic-csi2-14-1"></a>
<a id="rst-v4l2-meta-fmt-generic-csi2-14"></a>

### V4L2\_META\_FMT\_GENERIC\_CSI2\_14

V4L2\_META\_FMT\_GENERIC\_CSI2\_14 contains 8-bit generic metadata packed in 14-bit Data Units, with three padding bytes after every four bytes of metadata. This format is typically used by CSI-2 receivers with a source that transmits MEDIA\_BUS\_FMT\_META\_14 and the CSI-2 receiver writes the received data to memory as-is.

The packing of the data follows the MIPI CSI-2 specification and the padding of the data is defined in the MIPI CCS specification.

This format is little endian.

<strong>Byte Order Of V4L2\_META\_FMT\_GENERIC\_CSI2\_14.</strong> Each cell is one byte. "M" denotes a byte of metadata and "x" a byte of padding.

<!-- tabularcolumns: |p{2.4cm}|p{1.2cm}|p{1.2cm}|p{1.2cm}|p{1.2cm}|p{1.8cm}|p{1.8cm}|p{1.8cm}| -->


<table>
<caption>

Sample 4x2 Metadata Frame

</caption>
<tbody>
<tr>
<td>



start + 0:

</td>
<td>



M<sub>00</sub>

</td>
<td>



M<sub>10</sub>

</td>
<td>



M<sub>20</sub>

</td>
<td>



M<sub>30</sub>

</td>
<td>



x

</td>
<td>



x

</td>
<td>



x

</td>
</tr>
<tr>
<td>



start + 7:

</td>
<td>



M<sub>01</sub>

</td>
<td>



M<sub>11</sub>

</td>
<td>



M<sub>21</sub>

</td>
<td>



M<sub>31</sub>

</td>
<td>



x

</td>
<td>



x

</td>
<td>



x

</td>
</tr>
</tbody>
</table>

<a id="rst-v4l2-meta-fmt-generic-csi2-16-1"></a>
<a id="rst-v4l2-meta-fmt-generic-csi2-16"></a>

### V4L2\_META\_FMT\_GENERIC\_CSI2\_16

V4L2\_META\_FMT\_GENERIC\_CSI2\_16 contains 8-bit generic metadata packed in 16-bit Data Units, with one padding byte after every byte of metadata. This format is typically used by CSI-2 receivers with a source that transmits MEDIA\_BUS\_FMT\_META\_16 and the CSI-2 receiver writes the received data to memory as-is.

The packing of the data follows the MIPI CSI-2 specification and the padding of the data is defined in the MIPI CCS specification.

Some devices support more efficient packing of metadata in conjunction with 16-bit image data. In that case the dataformat is [V4L2\_META\_FMT\_GENERIC\_8](<#rst-v4l2-meta-fmt-generic-8>).

This format is little endian.

<strong>Byte Order Of V4L2\_META\_FMT\_GENERIC\_CSI2\_16.</strong> Each cell is one byte. "M" denotes a byte of metadata and "x" a byte of padding.

<!-- tabularcolumns: |p{2.4cm}|p{1.2cm}|p{.8cm}|p{1.2cm}|p{.8cm}|p{1.2cm}|p{.8cm}|p{1.2cm}|p{.8cm}| -->


<table>
<caption>

Sample 4x2 Metadata Frame

</caption>
<tbody>
<tr>
<td>



start + 0:

</td>
<td>



M<sub>00</sub>

</td>
<td>



x

</td>
<td>



M<sub>10</sub>

</td>
<td>



x

</td>
<td>



M<sub>20</sub>

</td>
<td>



x

</td>
<td>



M<sub>30</sub>

</td>
<td>



x

</td>
</tr>
<tr>
<td>



start + 8:

</td>
<td>



M<sub>01</sub>

</td>
<td>



x

</td>
<td>



M<sub>11</sub>

</td>
<td>



x

</td>
<td>



M<sub>21</sub>

</td>
<td>



x

</td>
<td>



M<sub>31</sub>

</td>
<td>



x

</td>
</tr>
</tbody>
</table>

<a id="rst-v4l2-meta-fmt-generic-csi2-20-1"></a>
<a id="rst-v4l2-meta-fmt-generic-csi2-20"></a>

### V4L2\_META\_FMT\_GENERIC\_CSI2\_20

V4L2\_META\_FMT\_GENERIC\_CSI2\_20 contains 8-bit generic metadata packed in 20-bit Data Units, with alternating one or two padding bytes after every byte of metadata. This format is typically used by CSI-2 receivers with a source that transmits MEDIA\_BUS\_FMT\_META\_20 and the CSI-2 receiver writes the received data to memory as-is.

The packing of the data follows the MIPI CSI-2 specification and the padding of the data is defined in the MIPI CCS specification.

Some devices support more efficient packing of metadata in conjunction with 16-bit image data. In that case the dataformat is [V4L2\_META\_FMT\_GENERIC\_CSI2\_10](<#rst-v4l2-meta-fmt-generic-csi2-10>).

This format is little endian.

<strong>Byte Order Of V4L2\_META\_FMT\_GENERIC\_CSI2\_20.</strong> Each cell is one byte. "M" denotes a byte of metadata and "x" a byte of padding.

<!-- tabularcolumns: |p{2.4cm}|p{1.2cm}|p{1.2cm}|p{1.2cm}|p{1.2cm}|p{1.8cm}|p{1.2cm}|p{1.2cm}|p{1.2cm}|p{1.2cm}|p{1.8cm} -->


<table>
<caption>

Sample 4x2 Metadata Frame

</caption>
<tbody>
<tr>
<td>



start + 0:

</td>
<td>



M<sub>00</sub>

</td>
<td>



x

</td>
<td>



M<sub>10</sub>

</td>
<td>



x

</td>
<td>



x

</td>
<td>



M<sub>20</sub>

</td>
<td>



x

</td>
<td>



M<sub>30</sub>

</td>
<td>



x

</td>
<td>



x

</td>
</tr>
<tr>
<td>



start + 10:

</td>
<td>



M<sub>01</sub>

</td>
<td>



x

</td>
<td>



M<sub>11</sub>

</td>
<td>



x

</td>
<td>



x

</td>
<td>



M<sub>21</sub>

</td>
<td>



x

</td>
<td>



M<sub>31</sub>

</td>
<td>



x

</td>
<td>



x

</td>
</tr>
</tbody>
</table>

<a id="rst-v4l2-meta-fmt-generic-csi2-24-1"></a>
<a id="rst-v4l2-meta-fmt-generic-csi2-24"></a>

### V4L2\_META\_FMT\_GENERIC\_CSI2\_24

V4L2\_META\_FMT\_GENERIC\_CSI2\_24 contains 8-bit generic metadata packed in 24-bit Data Units, with two padding bytes after every byte of metadata. This format is typically used by CSI-2 receivers with a source that transmits MEDIA\_BUS\_FMT\_META\_24 and the CSI-2 receiver writes the received data to memory as-is.

The packing of the data follows the MIPI CSI-2 specification and the padding of the data is defined in the MIPI CCS specification.

Some devices support more efficient packing of metadata in conjunction with 16-bit image data. In that case the dataformat is [V4L2\_META\_FMT\_GENERIC\_CSI2\_12](<#rst-v4l2-meta-fmt-generic-csi2-12>).

This format is little endian.

<strong>Byte Order Of V4L2\_META\_FMT\_GENERIC\_CSI2\_24.</strong> Each cell is one byte. "M" denotes a byte of metadata and "x" a byte of padding.

<!-- tabularcolumns: |p{2.4cm}|p{1.2cm}|p{.8cm}|p{.8cm}|p{1.2cm}|p{.8cm}|p{.8cm}|p{1.2cm}|p{.8cm}|p{.8cm}|p{1.2cm}|p{.8cm}|p{.8cm}| -->


<table>
<caption>

Sample 4x2 Metadata Frame

</caption>
<tbody>
<tr>
<td>



start + 0:

</td>
<td>



M<sub>00</sub>

</td>
<td>



x

</td>
<td>



x

</td>
<td>



M<sub>10</sub>

</td>
<td>



x

</td>
<td>



x

</td>
<td>



M<sub>20</sub>

</td>
<td>



x

</td>
<td>



x

</td>
<td>



M<sub>30</sub>

</td>
<td>



x

</td>
<td>



x

</td>
</tr>
<tr>
<td>



start + 12:

</td>
<td>



M<sub>01</sub>

</td>
<td>



x

</td>
<td>



x

</td>
<td>



M<sub>11</sub>

</td>
<td>



x

</td>
<td>



x

</td>
<td>



M<sub>21</sub>

</td>
<td>



x

</td>
<td>



x

</td>
<td>



M<sub>31</sub>

</td>
<td>



x

</td>
<td>



x

</td>
</tr>
</tbody>
</table>
