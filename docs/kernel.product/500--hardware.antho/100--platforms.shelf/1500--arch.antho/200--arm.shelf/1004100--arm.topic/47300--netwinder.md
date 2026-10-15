---
title: "NetWinder specific documentation"
type: reference
description: "The NetWinder is a small low-power computer, primarily designed to run Linux. It is based around the StrongARM RISC processor, DC21285 PCI bridge, with PC-type hardware glued around it."
---

<a id="rst-netwinder-specific-documentation"></a>

The NetWinder is a small low-power computer, primarily designed to run Linux.  It is based around the StrongARM RISC processor, DC21285 PCI bridge, with PC-type hardware glued around it.

<a id="rst-port-usage"></a>

## Port usage


<table>
<thead>
<tr>
<th>


Min

</th>
<th>


Max

</th>
<th>


Description

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


0x0000

</td>
<td>


0x000f

</td>
<td>


DMA1

</td>
</tr>
<tr>
<td>


0x0020

</td>
<td>


0x0021

</td>
<td>


PIC1

</td>
</tr>
<tr>
<td>


0x0060

</td>
<td>


0x006f

</td>
<td>


Keyboard

</td>
</tr>
<tr>
<td>


0x0070

</td>
<td>


0x007f

</td>
<td>


RTC

</td>
</tr>
<tr>
<td>


0x0080

</td>
<td>


0x0087

</td>
<td>


DMA1

</td>
</tr>
<tr>
<td>


0x0088

</td>
<td>


0x008f

</td>
<td>


DMA2

</td>
</tr>
<tr>
<td>


0x00a0

</td>
<td>


0x00a3

</td>
<td>


PIC2

</td>
</tr>
<tr>
<td>


0x00c0

</td>
<td>


0x00df

</td>
<td>


DMA2

</td>
</tr>
<tr>
<td>


0x0180

</td>
<td>


0x0187

</td>
<td>


IRDA

</td>
</tr>
<tr>
<td>


0x01f0

</td>
<td>


0x01f6

</td>
<td>


ide0

</td>
</tr>
<tr>
<td>


0x0201

</td>
<td>




</td>
<td>


Game port

</td>
</tr>
<tr>
<td>


0x0203

</td>
<td>




</td>
<td>


RWA010 configuration read

</td>
</tr>
<tr>
<td>


0x0220

</td>
<td>


?

</td>
<td>


SoundBlaster

</td>
</tr>
<tr>
<td>


0x0250

</td>
<td>


?

</td>
<td>


WaveArtist

</td>
</tr>
<tr>
<td>


0x0279

</td>
<td>




</td>
<td>


RWA010 configuration index

</td>
</tr>
<tr>
<td>


0x02f8

</td>
<td>


0x02ff

</td>
<td>


Serial ttyS1

</td>
</tr>
<tr>
<td>


0x0300

</td>
<td>


0x031f

</td>
<td>


Ether10

</td>
</tr>
<tr>
<td>


0x0338

</td>
<td>




</td>
<td>


GPIO1

</td>
</tr>
<tr>
<td>


0x033a

</td>
<td>




</td>
<td>


GPIO2

</td>
</tr>
<tr>
<td>


0x0370

</td>
<td>


0x0371

</td>
<td>


W83977F configuration registers

</td>
</tr>
<tr>
<td>


0x0388

</td>
<td>


?

</td>
<td>


AdLib

</td>
</tr>
<tr>
<td>


0x03c0

</td>
<td>


0x03df

</td>
<td>


VGA

</td>
</tr>
<tr>
<td>


0x03f6

</td>
<td>




</td>
<td>


ide0

</td>
</tr>
<tr>
<td>


0x03f8

</td>
<td>


0x03ff

</td>
<td>


Serial ttyS0

</td>
</tr>
<tr>
<td>


0x0400

</td>
<td>


0x0408

</td>
<td>


DC21143

</td>
</tr>
<tr>
<td>


0x0480

</td>
<td>


0x0487

</td>
<td>


DMA1

</td>
</tr>
<tr>
<td>


0x0488

</td>
<td>


0x048f

</td>
<td>


DMA2

</td>
</tr>
<tr>
<td>


0x0a79

</td>
<td>




</td>
<td>


RWA010 configuration write

</td>
</tr>
<tr>
<td>


0xe800

</td>
<td>


0xe80f

</td>
<td>


ide0/ide1 BM DMA

</td>
</tr>
</tbody>
</table>

<a id="rst-interrupt-usage"></a>

## Interrupt usage


<table>
<thead>
<tr>
<th>


IRQ

</th>
<th>


type

</th>
<th>


Description

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


0

</td>
<td>


ISA

</td>
<td>


100Hz timer

</td>
</tr>
<tr>
<td>


1

</td>
<td>


ISA

</td>
<td>


Keyboard

</td>
</tr>
<tr>
<td>


2

</td>
<td>


ISA

</td>
<td>


cascade

</td>
</tr>
<tr>
<td>


3

</td>
<td>


ISA

</td>
<td>


Serial ttyS1

</td>
</tr>
<tr>
<td>


4

</td>
<td>


ISA

</td>
<td>


Serial ttyS0

</td>
</tr>
<tr>
<td>


5

</td>
<td>


ISA

</td>
<td>


PS/2 mouse

</td>
</tr>
<tr>
<td>


6

</td>
<td>


ISA

</td>
<td>


IRDA

</td>
</tr>
<tr>
<td>


7

</td>
<td>


ISA

</td>
<td>


Printer

</td>
</tr>
<tr>
<td>


8

</td>
<td>


ISA

</td>
<td>


RTC alarm

</td>
</tr>
<tr>
<td>


9

</td>
<td>


ISA

</td>
<td>




</td>
</tr>
<tr>
<td>


10

</td>
<td>


ISA

</td>
<td>


GP10 (Orange reset button)

</td>
</tr>
<tr>
<td>


11

</td>
<td>


ISA

</td>
<td>




</td>
</tr>
<tr>
<td>


12

</td>
<td>


ISA

</td>
<td>


WaveArtist

</td>
</tr>
<tr>
<td>


13

</td>
<td>


ISA

</td>
<td>




</td>
</tr>
<tr>
<td>


14

</td>
<td>


ISA

</td>
<td>


hda1

</td>
</tr>
<tr>
<td>


15

</td>
<td>


ISA

</td>
<td>




</td>
</tr>
</tbody>
</table>

<a id="rst-dma-usage"></a>

## DMA usage


<table>
<thead>
<tr>
<th>


DMA

</th>
<th>


type

</th>
<th>


Description

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


0

</td>
<td>


ISA

</td>
<td>


IRDA

</td>
</tr>
<tr>
<td>


1

</td>
<td>


ISA

</td>
<td>




</td>
</tr>
<tr>
<td>


2

</td>
<td>


ISA

</td>
<td>


cascade

</td>
</tr>
<tr>
<td>


3

</td>
<td>


ISA

</td>
<td>


WaveArtist

</td>
</tr>
<tr>
<td>


4

</td>
<td>


ISA

</td>
<td>




</td>
</tr>
<tr>
<td>


5

</td>
<td>


ISA

</td>
<td>




</td>
</tr>
<tr>
<td>


6

</td>
<td>


ISA

</td>
<td>




</td>
</tr>
<tr>
<td>


7

</td>
<td>


ISA

</td>
<td>


WaveArtist

</td>
</tr>
</tbody>
</table>
