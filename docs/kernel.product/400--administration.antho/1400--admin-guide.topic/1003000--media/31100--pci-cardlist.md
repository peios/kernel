---
title: "PCI drivers"
type: reference
description: "The PCI boards are identified by an identification called PCI ID. The PCI ID is actually composed by two parts:"
---

<a id="rst-pci-drivers"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

The PCI boards are identified by an identification called PCI ID. The PCI ID is actually composed by two parts:

> - Vendor ID and device ID;
>
> - Subsystem ID and Subsystem device ID;

The `lspci -nn` command allows identifying the vendor/device PCI IDs:



```none
 $ lspci -nn
 ...
 00:0a.0 Multimedia controller [0480]: Philips Semiconductors SAA7131/SAA7133/SAA7135 Video Broadcast Decoder [1131:7133] (rev d1)
 00:0b.0 Multimedia controller [0480]: Brooktree Corporation Bt878 Audio Capture [109e:0878] (rev 11)
 01:00.0 Multimedia video controller [0400]: Conexant Systems, Inc. CX23887/8 PCIe Broadcast Audio and Video Decoder with 3D Comb [14f1:8880] (rev 0f)
 02:01.0 Multimedia video controller [0400]: Internext Compression Inc iTVC15 (CX23415) Video Decoder [4444:0803] (rev 01)
 02:02.0 Multimedia video controller [0400]: Conexant Systems, Inc. CX23418 Single-Chip MPEG-2 Encoder with Integrated Analog Video/Broadcast Audio Decoder [14f1:5b7a]
 02:03.0 Multimedia video controller [0400]: Brooktree Corporation Bt878 Video Capture [109e:036e] (rev 11)
 ...
```

The subsystem IDs can be obtained using `lspci -vn`



```none
 $ lspci -vn
 ...
     00:0a.0 0480: 1131:7133 (rev d1)
             Subsystem: 1461:f01d
             Flags: bus master, medium devsel, latency 32, IRQ 209
             Memory at e2002000 (32-bit, non-prefetchable) [size=2K]
             Capabilities: [40] Power Management version 2
 ...
```

At the above example, the first card uses the `saa7134` driver, and has a vendor/device PCI ID equal to `1131:7133` and a PCI subsystem ID equal to `1461:f01d` (see [Saa7134 card list](<~kernel/administration/admin-guide/media/saa7134-cardlist>)).

Unfortunately, sometimes the same PCI subsystem ID is used by different products. So, several media drivers allow passing a `card=` parameter, in order to setup a card number that would match the correct settings for an specific board.

The current supported PCI/PCIe cards (not including staging drivers) are listed below<a id="rst-footnote-reference-1"></a>[1](#rst-footnote-1).

<a id="rst-footnote-1"></a>



**[1]** some of the drivers have sub-drivers, not shown at this table


<table>
<thead>
<tr>
<th>



Driver

</th>
<th>



Name

</th>
</tr>
</thead>
<tbody>
<tr>
<td>



altera-ci

</td>
<td>



Altera FPGA based CI module

</td>
</tr>
<tr>
<td>



b2c2-flexcop-pci

</td>
<td>



Technisat/B2C2 Air/Sky/Cable2PC PCI

</td>
</tr>
<tr>
<td>



bt878

</td>
<td>



DVB/ATSC Support for bt878 based TV cards

</td>
</tr>
<tr>
<td>



bttv

</td>
<td>



BT8x8 Video For Linux

</td>
</tr>
<tr>
<td>



cobalt

</td>
<td>



Cisco Cobalt

</td>
</tr>
<tr>
<td>



cx18

</td>
<td>



Conexant cx23418 MPEG encoder

</td>
</tr>
<tr>
<td>



cx23885

</td>
<td>



Conexant cx23885 (2388x successor)

</td>
</tr>
<tr>
<td>



cx25821

</td>
<td>



Conexant cx25821

</td>
</tr>
<tr>
<td>



cx88xx

</td>
<td>



Conexant 2388x (bt878 successor)

</td>
</tr>
<tr>
<td>



ddbridge

</td>
<td>



Digital Devices bridge

</td>
</tr>
<tr>
<td>



dm1105

</td>
<td>



SDMC DM1105 based PCI cards

</td>
</tr>
<tr>
<td>



dt3155

</td>
<td>



DT3155 frame grabber

</td>
</tr>
<tr>
<td>



dvb-ttpci

</td>
<td>



AV7110 cards

</td>
</tr>
<tr>
<td>



earth-pt1

</td>
<td>



PT1 cards

</td>
</tr>
<tr>
<td>



earth-pt3

</td>
<td>



Earthsoft PT3 cards

</td>
</tr>
<tr>
<td>



hexium\_gemini

</td>
<td>



Hexium Gemini frame grabber

</td>
</tr>
<tr>
<td>



hexium\_orion

</td>
<td>



Hexium HV-PCI6 and Orion frame grabber

</td>
</tr>
<tr>
<td>



hopper

</td>
<td>



HOPPER based cards

</td>
</tr>
<tr>
<td>



ipu3-cio2

</td>
<td>



Intel ipu3-cio2 driver

</td>
</tr>
<tr>
<td>



ivtv

</td>
<td>



Conexant cx23416/cx23415 MPEG encoder/decoder

</td>
</tr>
<tr>
<td>



ivtvfb

</td>
<td>



Conexant cx23415 framebuffer

</td>
</tr>
<tr>
<td>



mantis

</td>
<td>



MANTIS based cards

</td>
</tr>
<tr>
<td>



mgb4

</td>
<td>



Digiteq Automotive MGB4 frame grabber

</td>
</tr>
<tr>
<td>



mxb

</td>
<td>



Siemens-Nixdorf 'Multimedia eXtension Board'

</td>
</tr>
<tr>
<td>



netup-unidvb

</td>
<td>



NetUP Universal DVB card

</td>
</tr>
<tr>
<td>



ngene

</td>
<td>



Micronas nGene

</td>
</tr>
<tr>
<td>



pluto2

</td>
<td>



Pluto2 cards

</td>
</tr>
<tr>
<td>



saa7134

</td>
<td>



Philips SAA7134

</td>
</tr>
<tr>
<td>



saa7164

</td>
<td>



NXP SAA7164

</td>
</tr>
<tr>
<td>



smipcie

</td>
<td>



SMI PCIe DVBSky cards

</td>
</tr>
<tr>
<td>



solo6x10

</td>
<td>



Bluecherry / Softlogic 6x10 capture cards (MPEG-4/H.264)

</td>
</tr>
<tr>
<td>



tw5864

</td>
<td>



Techwell TW5864 video/audio grabber and encoder

</td>
</tr>
<tr>
<td>



tw686x

</td>
<td>



Intersil/Techwell TW686x

</td>
</tr>
<tr>
<td>



tw68

</td>
<td>



Techwell tw68x Video For Linux

</td>
</tr>
<tr>
<td>



zoran

</td>
<td>



Zoran-36057/36067 JPEG codec

</td>
</tr>
</tbody>
</table>

Some of those drivers support multiple devices, as shown at the card lists below:

- [BTTV cards list](<~kernel/administration/admin-guide/media/bttv-cardlist>)
- [CX18 cards list](<~kernel/administration/admin-guide/media/cx18-cardlist>)
- [cx23885 cards list](<~kernel/administration/admin-guide/media/cx23885-cardlist>)
- [CX88 cards list](<~kernel/administration/admin-guide/media/cx88-cardlist>)
- [IVTV cards list](<~kernel/administration/admin-guide/media/ivtv-cardlist>)
- [SAA7134 cards list](<~kernel/administration/admin-guide/media/saa7134-cardlist>)
- [SAA7164 cards list](<~kernel/administration/admin-guide/media/saa7164-cardlist>)
- [Zoran cards list](<~kernel/administration/admin-guide/media/zoran-cardlist>)
