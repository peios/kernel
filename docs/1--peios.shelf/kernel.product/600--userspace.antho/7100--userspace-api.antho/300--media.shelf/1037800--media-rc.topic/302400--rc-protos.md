---
title: "Remote Controller Protocols and Scancodes"
type: reference
description: "IR is encoded as a series of pulses and spaces, using a protocol. These protocols can encode e.g. an address (which device should respond) and a command: what it should do. The values for these are not always consistent across different…"
---

<a id="rst-remote-controller-protocols-and-scancodes"></a>
<a id="rst-remote-controllers-protocols"></a>

<!-- SPDX-License-Identifier: GPL-2.0 OR GFDL-1.1-no-invariants-or-later -->

IR is encoded as a series of pulses and spaces, using a protocol. These protocols can encode e.g. an address (which device should respond) and a command: what it should do. The values for these are not always consistent across different devices for a given protocol.

Therefore out the output of the IR decoder is a scancode; a single u32 value. Using keymap tables this can be mapped to linux key codes.

Other things can be encoded too. Some IR protocols encode a toggle bit; this is to distinguish whether the same button is being held down, or has been released and pressed again. If has been released and pressed again, the toggle bit will invert from one IR message to the next.

Some remotes have a pointer-type device which can used to control the mouse; some air conditioning systems can have their target temperature target set in IR.

The following are the protocols the kernel knows about and also lists how scancodes are encoded for each protocol.

<a id="rst-rc-5-rc-proto-rc5"></a>

## rc-5 (RC_PROTO_RC5)

This IR protocol uses manchester encoding to encode 14 bits. There is a detailed description here [https://www.sbprojects.net/knowledge/ir/rc5.php](<https://www.sbprojects.net/knowledge/ir/rc5.php>).

The scancode encoding is *not* consistent with the lirc daemon (lircd) rc5 protocol, or the manchester BPF decoder.


<table>
<caption>rc5 bits scancode mapping</caption>
<tbody>
<tr>
<td>


rc-5 bit

</td>
<td>


scancode bit

</td>
<td>


description

</td>
</tr>
<tr>
<td>


1

</td>
<td>


none

</td>
<td>


Start bit, always set

</td>
</tr>
<tr>
<td>


1

</td>
<td>


6 (inverted)

</td>
<td>


2nd start bit in rc5,  re-used as 6th command bit

</td>
</tr>
<tr>
<td>


1

</td>
<td>


none

</td>
<td>


Toggle bit

</td>
</tr>
<tr>
<td>


5

</td>
<td>


8 to 13

</td>
<td>


Address

</td>
</tr>
<tr>
<td>


6

</td>
<td>


0 to 5

</td>
<td>


Command

</td>
</tr>
</tbody>
</table>

There is a variant of rc5 called either rc5x or extended rc5 where there the second stop bit is the 6th command bit, but inverted. This is done so it the scancodes and encoding is compatible with existing schemes. This bit is stored in bit 6 of the scancode, inverted. This is done to keep it compatible with plain rc-5 where there are two start bits.

<a id="rst-rc-5-sz-rc-proto-rc5-sz"></a>

## rc-5-sz (RC_PROTO_RC5_SZ)

This is much like rc-5 but one bit longer. The scancode is encoded differently.


<table>
<caption>rc-5-sz bits scancode mapping</caption>
<tbody>
<tr>
<td>


rc-5-sz bits

</td>
<td>


scancode bit

</td>
<td>


description

</td>
</tr>
<tr>
<td>


1

</td>
<td>


none

</td>
<td>


Start bit, always set

</td>
</tr>
<tr>
<td>


1

</td>
<td>


13

</td>
<td>


Address bit

</td>
</tr>
<tr>
<td>


1

</td>
<td>


none

</td>
<td>


Toggle bit

</td>
</tr>
<tr>
<td>


6

</td>
<td>


6 to 11

</td>
<td>


Address

</td>
</tr>
<tr>
<td>


6

</td>
<td>


0 to 5

</td>
<td>


Command

</td>
</tr>
</tbody>
</table>

<a id="rst-rc-5x-20-rc-proto-rc5x-20"></a>

## rc-5x-20 (RC_PROTO_RC5X_20)

This rc-5 extended to encoded 20 bits. The is a 3555 microseconds space after the 8th bit.


<table>
<caption>rc-5x-20 bits scancode mapping</caption>
<tbody>
<tr>
<td>


rc-5-sz bits

</td>
<td>


scancode bit

</td>
<td>


description

</td>
</tr>
<tr>
<td>


1

</td>
<td>


none

</td>
<td>


Start bit, always set

</td>
</tr>
<tr>
<td>


1

</td>
<td>


14

</td>
<td>


Address bit

</td>
</tr>
<tr>
<td>


1

</td>
<td>


none

</td>
<td>


Toggle bit

</td>
</tr>
<tr>
<td>


5

</td>
<td>


16 to 20

</td>
<td>


Address

</td>
</tr>
<tr>
<td>


6

</td>
<td>


8 to 13

</td>
<td>


Address

</td>
</tr>
<tr>
<td>


6

</td>
<td>


0 to 5

</td>
<td>


Command

</td>
</tr>
</tbody>
</table>

<a id="rst-jvc-rc-proto-jvc"></a>

## jvc (RC_PROTO_JVC)

The jvc protocol is much like nec, without the inverted values. It is described here [https://www.sbprojects.net/knowledge/ir/jvc.php](<https://www.sbprojects.net/knowledge/ir/jvc.php>).

The scancode is a 16 bits value, where the address is the lower 8 bits and the command the higher 8 bits; this is reversed from IR order.

<a id="rst-sony-12-rc-proto-sony12"></a>

## sony-12 (RC_PROTO_SONY12)

The sony protocol is a pulse-width encoding. There are three variants, which just differ in number of bits and scancode encoding.


<table>
<caption>sony-12 bits scancode mapping</caption>
<tbody>
<tr>
<td>


sony-12 bits

</td>
<td>


scancode bit

</td>
<td>


description

</td>
</tr>
<tr>
<td>


5

</td>
<td>


16 to 20

</td>
<td>


device

</td>
</tr>
<tr>
<td>


7

</td>
<td>


0 to 6

</td>
<td>


function

</td>
</tr>
</tbody>
</table>

<a id="rst-sony-15-rc-proto-sony15"></a>

## sony-15 (RC_PROTO_SONY15)

The sony protocol is a pulse-width encoding. There are three variants, which just differ in number of bits and scancode encoding.


<table>
<caption>sony-12 bits scancode mapping</caption>
<tbody>
<tr>
<td>


sony-12 bits

</td>
<td>


scancode bit

</td>
<td>


description

</td>
</tr>
<tr>
<td>


8

</td>
<td>


16 to 23

</td>
<td>


device

</td>
</tr>
<tr>
<td>


7

</td>
<td>


0 to 6

</td>
<td>


function

</td>
</tr>
</tbody>
</table>

<a id="rst-sony-20-rc-proto-sony20"></a>

## sony-20 (RC_PROTO_SONY20)

The sony protocol is a pulse-width encoding. There are three variants, which just differ in number of bits and scancode encoding.


<table>
<caption>sony-20 bits scancode mapping</caption>
<tbody>
<tr>
<td>


sony-20 bits

</td>
<td>


scancode bit

</td>
<td>


description

</td>
</tr>
<tr>
<td>


5

</td>
<td>


16 to 20

</td>
<td>


device

</td>
</tr>
<tr>
<td>


7

</td>
<td>


0 to 7

</td>
<td>


device

</td>
</tr>
<tr>
<td>


8

</td>
<td>


8 to 15

</td>
<td>


extended bits

</td>
</tr>
</tbody>
</table>

<a id="rst-nec-rc-proto-nec"></a>

## nec (RC_PROTO_NEC)

The nec protocol encodes an 8 bit address and an 8 bit command. It is described here [https://www.sbprojects.net/knowledge/ir/nec.php](<https://www.sbprojects.net/knowledge/ir/nec.php>). Note that the protocol sends least significant bit first.

As a check, the nec protocol sends the address and command twice; the second time it is inverted. This is done for verification.

A plain nec IR message has 16 bits; the high 8 bits are the address and the low 8 bits are the command.

<a id="rst-nec-x-rc-proto-necx"></a>

## nec-x (RC_PROTO_NECX)

Extended nec has a 16 bit address and a 8 bit command. This is encoded as a 24 bit value as you would expect, with the lower 8 bits the command and the upper 16 bits the address.

<a id="rst-nec-32-rc-proto-nec32"></a>

## nec-32 (RC_PROTO_NEC32)

nec-32 does not send an inverted address or an inverted command; the entire message, all 32 bits, are used.

For this to be decoded correctly, the second 8 bits must not be the inverted value of the first, and also the last 8 bits must not be the inverted value of the third 8 bit value.

The scancode has a somewhat unusual encoding.


<table>
<caption>nec-32 bits scancode mapping</caption>
<tbody>
<tr>
<td>


nec-32 bits

</td>
<td>


scancode bit

</td>
</tr>
<tr>
<td>


First 8 bits

</td>
<td>


16 to 23

</td>
</tr>
<tr>
<td>


Second 8 bits

</td>
<td>


24 to 31

</td>
</tr>
<tr>
<td>


Third 8 bits

</td>
<td>


0 to 7

</td>
</tr>
<tr>
<td>


Fourth 8 bits

</td>
<td>


8 to 15

</td>
</tr>
</tbody>
</table>

<a id="rst-sanyo-rc-proto-sanyo"></a>

## sanyo (RC_PROTO_SANYO)

The sanyo protocol is like the nec protocol, but with 13 bits address rather than 8 bits. Both the address and the command are followed by their inverted versions, but these are not present in the scancodes.

Bis 8 to 20 of the scancode is the 13 bits address, and the lower 8 bits are the command.

<a id="rst-mcir2-kbd-rc-proto-mcir2-kbd"></a>

## mcir2-kbd (RC_PROTO_MCIR2_KBD)

This protocol is generated by the Microsoft MCE keyboard for keyboard events. Refer to the ir-mce_kbd-decoder.c to see how it is encoded.

<a id="rst-mcir2-mse-rc-proto-mcir2-mse"></a>

## mcir2-mse (RC_PROTO_MCIR2_MSE)

This protocol is generated by the Microsoft MCE keyboard for pointer events. Refer to the ir-mce_kbd-decoder.c to see how it is encoded.

<a id="rst-rc-6-0-rc-proto-rc6-0"></a>

## rc-6-0 (RC_PROTO_RC6_0)

This is the rc-6 in mode 0. rc-6 is described here [https://www.sbprojects.net/knowledge/ir/rc6.php](<https://www.sbprojects.net/knowledge/ir/rc6.php>). The scancode is the exact 16 bits as in the protocol. There is also a toggle bit.

<a id="rst-rc-6-6a-20-rc-proto-rc6-6a-20"></a>

## rc-6-6a-20 (RC_PROTO_RC6_6A_20)

This is the rc-6 in mode 6a, 20 bits. rc-6 is described here [https://www.sbprojects.net/knowledge/ir/rc6.php](<https://www.sbprojects.net/knowledge/ir/rc6.php>). The scancode is the exact 20 bits as in the protocol. There is also a toggle bit.

<a id="rst-rc-6-6a-24-rc-proto-rc6-6a-24"></a>

## rc-6-6a-24 (RC_PROTO_RC6_6A_24)

This is the rc-6 in mode 6a, 24 bits. rc-6 is described here [https://www.sbprojects.net/knowledge/ir/rc6.php](<https://www.sbprojects.net/knowledge/ir/rc6.php>). The scancode is the exact 24 bits as in the protocol. There is also a toggle bit.

<a id="rst-rc-6-6a-32-rc-proto-rc6-6a-32"></a>

## rc-6-6a-32 (RC_PROTO_RC6_6A_32)

This is the rc-6 in mode 6a, 32 bits. rc-6 is described here [https://www.sbprojects.net/knowledge/ir/rc6.php](<https://www.sbprojects.net/knowledge/ir/rc6.php>). The upper 16 bits are the vendor, and the lower 16 bits are the vendor-specific bits. This protocol is for the non-Microsoft MCE variant (vendor \!= 0x800f).

<a id="rst-rc-6-mce-rc-proto-rc6-mce"></a>

## rc-6-mce (RC_PROTO_RC6_MCE)

This is the rc-6 in mode 6a, 32 bits. The upper 16 bits are the vendor, and the lower 16 bits are the vendor-specific bits. This protocol is for the Microsoft MCE variant (vendor = 0x800f). The toggle bit in the protocol itself is ignored, and the 16th bit should be takes as the toggle bit.

<a id="rst-sharp-rc-proto-sharp"></a>

## sharp (RC_PROTO_SHARP)

This is a protocol used by Sharp VCRs, is described here [https://www.sbprojects.net/knowledge/ir/sharp.php](<https://www.sbprojects.net/knowledge/ir/sharp.php>). There is a very long (40ms) space between the normal and inverted values, and some IR receivers cannot decode this.

There is a 5 bit address and a 8 bit command. In the scancode the address is in bits 8 to 12, and the command in bits 0 to 7.

<a id="rst-xmp-rc-proto-xmp"></a>

## xmp (RC_PROTO_XMP)

This protocol has several versions and only version 1 is supported. Refer to the decoder (ir-xmp-decoder.c) to see how it is encoded.

<a id="rst-cec-rc-proto-cec"></a>

## cec (RC_PROTO_CEC)

This is not an IR protocol, this is a protocol over CEC. The CEC infrastructure uses rc-core for handling CEC commands, so that they can easily be remapped.

<a id="rst-imon-rc-proto-imon"></a>

## imon (RC_PROTO_IMON)

This protocol is used by Antec Veris/SoundGraph iMON remotes.

The protocol describes both button presses and pointer movements. The protocol encodes 31 bits, and the scancode is simply the 31 bits with the top bit always 0.

<a id="rst-rc-mm-12-rc-proto-rcmm12"></a>

## rc-mm-12 (RC_PROTO_RCMM12)

The rc-mm protocol is described here [https://www.sbprojects.net/knowledge/ir/rcmm.php](<https://www.sbprojects.net/knowledge/ir/rcmm.php>). The scancode is simply the 12 bits.

<a id="rst-rc-mm-24-rc-proto-rcmm24"></a>

## rc-mm-24 (RC_PROTO_RCMM24)

The rc-mm protocol is described here [https://www.sbprojects.net/knowledge/ir/rcmm.php](<https://www.sbprojects.net/knowledge/ir/rcmm.php>). The scancode is simply the 24 bits.

<a id="rst-rc-mm-32-rc-proto-rcmm32"></a>

## rc-mm-32 (RC_PROTO_RCMM32)

The rc-mm protocol is described here [https://www.sbprojects.net/knowledge/ir/rcmm.php](<https://www.sbprojects.net/knowledge/ir/rcmm.php>). The scancode is simply the 32 bits.

<a id="rst-xbox-dvd-rc-proto-xbox-dvd"></a>

## xbox-dvd (RC_PROTO_XBOX_DVD)

This protocol is used by Xbox DVD Remote, which was made for the original Xbox. There is no in-kernel decoder or encoder for this protocol. The usb device decodes the protocol. There is a BPF decoder available in v4l-utils.
