---
title: "V4L2_PIX_FMT_IPU3_SBGGR10 ('ip3b'), V4L2_PIX_FMT_IPU3_SGBRG10 ('ip3g'), V4L2_PIX_FMT_IPU3_SGRBG10 ('ip3G'), V4L2_PIX_FMT_IPU3_SRGGB10 ('ip3r')"
type: reference
description: "These four pixel formats are used by Intel IPU3 driver, they are raw sRGB / Bayer formats with 10 bits per sample with every 25 pixels packed to 32 bytes leaving 6 most significant bits padding in the last byte. The format is little endian."
---

<a id="rst-v4l2-pix-fmt-ipu3-sbggr10-ip3b-v4l2-pix-fmt-ipu3-sgbrg10-ip3g-v4l2-pix-fmt-ipu3-sgrbg10-ip3g-v4l2-pix-fmt-ipu3-srggb10-ip3r"></a>
<a id="rst-v4l2-pix-fmt-ipu3-srggb10"></a>
<a id="rst-v4l2-pix-fmt-ipu3-sgrbg10"></a>
<a id="rst-v4l2-pix-fmt-ipu3-sgbrg10"></a>
<a id="rst-v4l2-pix-fmt-ipu3-sbggr10"></a>

<a id="rst-bit-bayer-formats"></a>

## 10-bit Bayer formats

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-description"></a>

## Description

These four pixel formats are used by Intel IPU3 driver, they are raw sRGB / Bayer formats with 10 bits per sample with every 25 pixels packed to 32 bytes leaving 6 most significant bits padding in the last byte. The format is little endian.

In other respects this format is similar to [v4l2-pix-fmt-srggb10](<~kernel/userspace/userspace-api/media-v4l/pixfmt-srggb10#rst-v4l2-pix-fmt-srggb10>). Below is an example of a small image in V4L2\_PIX\_FMT\_IPU3\_SBGGR10 format.

<strong>Byte Order.</strong> Each cell is one byte.

<!-- Source LaTeX layout: \small -->

<!-- tabularcolumns: |p{0.8cm}|p{3.3cm}|p{3.3cm}|p{3.3cm}|p{3.3cm}| -->


<table>
<tbody>
<tr>
<td>



start + 0:

</td>
<td>



B<sub>0000low</sub>

</td>
<td>



G<sub>0001low</sub>(bits 7--2)

B<sub>0000high</sub>(bits 1--0)

</td>
<td>



B<sub>0002low</sub>(bits 7--4)

G<sub>0001high</sub>(bits 3--0)

</td>
<td>



G<sub>0003low</sub>(bits 7--6)

B<sub>0002high</sub>(bits 5--0)

</td>
</tr>
<tr>
<td>



start + 4:

</td>
<td>



G<sub>0003high</sub>

</td>
<td>



B<sub>0004low</sub>

</td>
<td>



G<sub>0005low</sub>(bits 7--2)

B<sub>0004high</sub>(bits 1--0)

</td>
<td>



B<sub>0006low</sub>(bits 7--4)

G<sub>0005high</sub>(bits 3--0)

</td>
</tr>
<tr>
<td>



start + 8:

</td>
<td>



G<sub>0007low</sub>(bits 7--6)

B<sub>0006high</sub>(bits 5--0)

</td>
<td>



G<sub>0007high</sub>

</td>
<td>



B<sub>0008low</sub>

</td>
<td>



G<sub>0009low</sub>(bits 7--2)

B<sub>0008high</sub>(bits 1--0)

</td>
</tr>
<tr>
<td>



start + 12:

</td>
<td>



B<sub>0010low</sub>(bits 7--4)

G<sub>0009high</sub>(bits 3--0)

</td>
<td>



G<sub>0011low</sub>(bits 7--6)

B<sub>0010high</sub>(bits 5--0)

</td>
<td>



G<sub>0011high</sub>

</td>
<td>



B<sub>0012low</sub>

</td>
</tr>
<tr>
<td>



start + 16:

</td>
<td>



G<sub>0013low</sub>(bits 7--2)

B<sub>0012high</sub>(bits 1--0)

</td>
<td>



B<sub>0014low</sub>(bits 7--4)

G<sub>0013high</sub>(bits 3--0)

</td>
<td>



G<sub>0015low</sub>(bits 7--6)

B<sub>0014high</sub>(bits 5--0)

</td>
<td>



G<sub>0015high</sub>

</td>
</tr>
<tr>
<td>



start + 20

</td>
<td>



B<sub>0016low</sub>

</td>
<td>



G<sub>0017low</sub>(bits 7--2)

B<sub>0016high</sub>(bits 1--0)

</td>
<td>



B<sub>0018low</sub>(bits 7--4)

G<sub>0017high</sub>(bits 3--0)

</td>
<td>



G<sub>0019low</sub>(bits 7--6)

B<sub>0018high</sub>(bits 5--0)

</td>
</tr>
<tr>
<td>



start + 24:

</td>
<td>



G<sub>0019high</sub>

</td>
<td>



B<sub>0020low</sub>

</td>
<td>



G<sub>0021low</sub>(bits 7--2)

B<sub>0020high</sub>(bits 1--0)

</td>
<td>



B<sub>0022low</sub>(bits 7--4)

G<sub>0021high</sub>(bits 3--0)

</td>
</tr>
<tr>
<td>



start + 28:

</td>
<td>



G<sub>0023low</sub>(bits 7--6)

B<sub>0022high</sub>(bits 5--0)

</td>
<td>



G<sub>0023high</sub>

</td>
<td>



B<sub>0024low</sub>

</td>
<td>



B<sub>0024high</sub>(bits 1--0)

</td>
</tr>
<tr>
<td>



start + 32:

</td>
<td>



G<sub>0100low</sub>

</td>
<td>



R<sub>0101low</sub>(bits 7--2)

G<sub>0100high</sub>(bits 1--0)

</td>
<td>



G<sub>0102low</sub>(bits 7--4)

R<sub>0101high</sub>(bits 3--0)

</td>
<td>



R<sub>0103low</sub>(bits 7--6)

G<sub>0102high</sub>(bits 5--0)

</td>
</tr>
<tr>
<td>



start + 36:

</td>
<td>



R<sub>0103high</sub>

</td>
<td>



G<sub>0104low</sub>

</td>
<td>



R<sub>0105low</sub>(bits 7--2)

G<sub>0104high</sub>(bits 1--0)

</td>
<td>



G<sub>0106low</sub>(bits 7--4)

R<sub>0105high</sub>(bits 3--0)

</td>
</tr>
<tr>
<td>



start + 40:

</td>
<td>



R<sub>0107low</sub>(bits 7--6)

G<sub>0106high</sub>(bits 5--0)

</td>
<td>



R<sub>0107high</sub>

</td>
<td>



G<sub>0108low</sub>

</td>
<td>



R<sub>0109low</sub>(bits 7--2)

G<sub>0108high</sub>(bits 1--0)

</td>
</tr>
<tr>
<td>



start + 44:

</td>
<td>



G<sub>0110low</sub>(bits 7--4)

R<sub>0109high</sub>(bits 3--0)

</td>
<td>



R<sub>0111low</sub>(bits 7--6)

G<sub>0110high</sub>(bits 5--0)

</td>
<td>



R<sub>0111high</sub>

</td>
<td>



G<sub>0112low</sub>

</td>
</tr>
<tr>
<td>



start + 48:

</td>
<td>



R<sub>0113low</sub>(bits 7--2)

G<sub>0112high</sub>(bits 1--0)

</td>
<td>



G<sub>0114low</sub>(bits 7--4)

R<sub>0113high</sub>(bits 3--0)

</td>
<td>



R<sub>0115low</sub>(bits 7--6)

G<sub>0114high</sub>(bits 5--0)

</td>
<td>



R<sub>0115high</sub>

</td>
</tr>
<tr>
<td>



start + 52:

</td>
<td>



G<sub>0116low</sub>

</td>
<td>



R<sub>0117low</sub>(bits 7--2)

G<sub>0116high</sub>(bits 1--0)

</td>
<td>



G<sub>0118low</sub>(bits 7--4)

R<sub>0117high</sub>(bits 3--0)

</td>
<td>



R<sub>0119low</sub>(bits 7--6)

G<sub>0118high</sub>(bits 5--0)

</td>
</tr>
<tr>
<td>



start + 56:

</td>
<td>



R<sub>0119high</sub>

</td>
<td>



G<sub>0120low</sub>

</td>
<td>



R<sub>0121low</sub>(bits 7--2)

G<sub>0120high</sub>(bits 1--0)

</td>
<td>



G<sub>0122low</sub>(bits 7--4)

R<sub>0121high</sub>(bits 3--0)

</td>
</tr>
<tr>
<td>



start + 60:

</td>
<td>



R<sub>0123low</sub>(bits 7--6)

G<sub>0122high</sub>(bits 5--0)

</td>
<td>



R<sub>0123high</sub>

</td>
<td>



G<sub>0124low</sub>

</td>
<td>



G<sub>0124high</sub>(bits 1--0)

</td>
</tr>
<tr>
<td>



start + 64:

</td>
<td>



B<sub>0200low</sub>

</td>
<td>



G<sub>0201low</sub>(bits 7--2)

B<sub>0200high</sub>(bits 1--0)

</td>
<td>



B<sub>0202low</sub>(bits 7--4)

G<sub>0201high</sub>(bits 3--0)

</td>
<td>



G<sub>0203low</sub>(bits 7--6)

B<sub>0202high</sub>(bits 5--0)

</td>
</tr>
<tr>
<td>



start + 68:

</td>
<td>



G<sub>0203high</sub>

</td>
<td>



B<sub>0204low</sub>

</td>
<td>



G<sub>0205low</sub>(bits 7--2)

B<sub>0204high</sub>(bits 1--0)

</td>
<td>



B<sub>0206low</sub>(bits 7--4)

G<sub>0205high</sub>(bits 3--0)

</td>
</tr>
<tr>
<td>



start + 72:

</td>
<td>



G<sub>0207low</sub>(bits 7--6)

B<sub>0206high</sub>(bits 5--0)

</td>
<td>



G<sub>0207high</sub>

</td>
<td>



B<sub>0208low</sub>

</td>
<td>



G<sub>0209low</sub>(bits 7--2)

B<sub>0208high</sub>(bits 1--0)

</td>
</tr>
<tr>
<td>



start + 76:

</td>
<td>



B<sub>0210low</sub>(bits 7--4)

G<sub>0209high</sub>(bits 3--0)

</td>
<td>



G<sub>0211low</sub>(bits 7--6)

B<sub>0210high</sub>(bits 5--0)

</td>
<td>



G<sub>0211high</sub>

</td>
<td>



B<sub>0212low</sub>

</td>
</tr>
<tr>
<td>



start + 80:

</td>
<td>



G<sub>0213low</sub>(bits 7--2)

B<sub>0212high</sub>(bits 1--0)

</td>
<td>



B<sub>0214low</sub>(bits 7--4)

G<sub>0213high</sub>(bits 3--0)

</td>
<td>



G<sub>0215low</sub>(bits 7--6)

B<sub>0214high</sub>(bits 5--0)

</td>
<td>



G<sub>0215high</sub>

</td>
</tr>
<tr>
<td>



start + 84:

</td>
<td>



B<sub>0216low</sub>

</td>
<td>



G<sub>0217low</sub>(bits 7--2)

B<sub>0216high</sub>(bits 1--0)

</td>
<td>



B<sub>0218low</sub>(bits 7--4)

G<sub>0217high</sub>(bits 3--0)

</td>
<td>



G<sub>0219low</sub>(bits 7--6)

B<sub>0218high</sub>(bits 5--0)

</td>
</tr>
<tr>
<td>



start + 88:

</td>
<td>



G<sub>0219high</sub>

</td>
<td>



B<sub>0220low</sub>

</td>
<td>



G<sub>0221low</sub>(bits 7--2)

B<sub>0220high</sub>(bits 1--0)

</td>
<td>



B<sub>0222low</sub>(bits 7--4)

G<sub>0221high</sub>(bits 3--0)

</td>
</tr>
<tr>
<td>



start + 92:

</td>
<td>



G<sub>0223low</sub>(bits 7--6)

B<sub>0222high</sub>(bits 5--0)

</td>
<td>



G<sub>0223high</sub>

</td>
<td>



B<sub>0224low</sub>

</td>
<td>



B<sub>0224high</sub>(bits 1--0)

</td>
</tr>
<tr>
<td>



start + 96:

</td>
<td>



G<sub>0300low</sub>

</td>
<td>



R<sub>0301low</sub>(bits 7--2)

G<sub>0300high</sub>(bits 1--0)

</td>
<td>



G<sub>0302low</sub>(bits 7--4)

R<sub>0301high</sub>(bits 3--0)

</td>
<td>



R<sub>0303low</sub>(bits 7--6)

G<sub>0302high</sub>(bits 5--0)

</td>
</tr>
<tr>
<td>



start + 100:

</td>
<td>



R<sub>0303high</sub>

</td>
<td>



G<sub>0304low</sub>

</td>
<td>



R<sub>0305low</sub>(bits 7--2)

G<sub>0304high</sub>(bits 1--0)

</td>
<td>



G<sub>0306low</sub>(bits 7--4)

R<sub>0305high</sub>(bits 3--0)

</td>
</tr>
<tr>
<td>



start + 104:

</td>
<td>



R<sub>0307low</sub>(bits 7--6)

G<sub>0306high</sub>(bits 5--0)

</td>
<td>



R<sub>0307high</sub>

</td>
<td>



G<sub>0308low</sub>

</td>
<td>



R<sub>0309low</sub>(bits 7--2)

G<sub>0308high</sub>(bits 1--0)

</td>
</tr>
<tr>
<td>



start + 108:

</td>
<td>



G<sub>0310low</sub>(bits 7--4)

R<sub>0309high</sub>(bits 3--0)

</td>
<td>



R<sub>0311low</sub>(bits 7--6)

G<sub>0310high</sub>(bits 5--0)

</td>
<td>



R<sub>0311high</sub>

</td>
<td>



G<sub>0312low</sub>

</td>
</tr>
<tr>
<td>



start + 112:

</td>
<td>



R<sub>0313low</sub>(bits 7--2)

G<sub>0312high</sub>(bits 1--0)

</td>
<td>



G<sub>0314low</sub>(bits 7--4)

R<sub>0313high</sub>(bits 3--0)

</td>
<td>



R<sub>0315low</sub>(bits 7--6)

G<sub>0314high</sub>(bits 5--0)

</td>
<td>



R<sub>0315high</sub>

</td>
</tr>
<tr>
<td>



start + 116:

</td>
<td>



G<sub>0316low</sub>

</td>
<td>



R<sub>0317low</sub>(bits 7--2)

G<sub>0316high</sub>(bits 1--0)

</td>
<td>



G<sub>0318low</sub>(bits 7--4)

R<sub>0317high</sub>(bits 3--0)

</td>
<td>



R<sub>0319low</sub>(bits 7--6)

G<sub>0318high</sub>(bits 5--0)

</td>
</tr>
<tr>
<td>



start + 120:

</td>
<td>



R<sub>0319high</sub>

</td>
<td>



G<sub>0320low</sub>

</td>
<td>



R<sub>0321low</sub>(bits 7--2)

G<sub>0320high</sub>(bits 1--0)

</td>
<td>



G<sub>0322low</sub>(bits 7--4)

R<sub>0321high</sub>(bits 3--0)

</td>
</tr>
<tr>
<td>



start + 124:

</td>
<td>



R<sub>0323low</sub>(bits 7--6)

G<sub>0322high</sub>(bits 5--0)

</td>
<td>



R<sub>0323high</sub>

</td>
<td>



G<sub>0324low</sub>

</td>
<td>



G<sub>0324high</sub>(bits 1--0)

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->
