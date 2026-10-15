---
title: "ALPS HID Touchpad Protocol"
type: reference
description: "Currently ALPS HID driver supports U1 Touchpad device."
---

<a id="rst-alps-hid-touchpad-protocol"></a>

<a id="rst-introduction"></a>

## Introduction

Currently ALPS HID driver supports U1 Touchpad device.

U1 device basic information.


<table>
<tbody>
<tr>
<td>


Vendor ID

</td>
<td>


0x044E

</td>
</tr>
<tr>
<td>


Product ID

</td>
<td>


0x120B

</td>
</tr>
<tr>
<td>


Version ID

</td>
<td>


0x0121

</td>
</tr>
</tbody>
</table>

<a id="rst-hid-descriptor"></a>

## HID Descriptor


<table>
<thead>
<tr>
<th>


Byte

</th>
<th>


Field

</th>
<th>


Value

</th>
<th>


Notes

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


0

</td>
<td>


wHIDDescLength

</td>
<td>


001E

</td>
<td>


Length of HID Descriptor : 30 bytes

</td>
</tr>
<tr>
<td>


2

</td>
<td>


bcdVersion

</td>
<td>


0100

</td>
<td>


Compliant with Version 1.00

</td>
</tr>
<tr>
<td>


4

</td>
<td>


wReportDescLength

</td>
<td>


00B2

</td>
<td>


Report Descriptor is 178 Bytes (0x00B2)

</td>
</tr>
<tr>
<td>


6

</td>
<td>


wReportDescRegister

</td>
<td>


0002

</td>
<td>


Identifier to read Report Descriptor

</td>
</tr>
<tr>
<td>


8

</td>
<td>


wInputRegister

</td>
<td>


0003

</td>
<td>


Identifier to read Input Report

</td>
</tr>
<tr>
<td>


10

</td>
<td>


wMaxInputLength

</td>
<td>


0053

</td>
<td>


Input Report is 80 Bytes + 2

</td>
</tr>
<tr>
<td>


12

</td>
<td>


wOutputRegister

</td>
<td>


0000

</td>
<td>


Identifier to read Output Report

</td>
</tr>
<tr>
<td>


14

</td>
<td>


wMaxOutputLength

</td>
<td>


0000

</td>
<td>


No Output Reports

</td>
</tr>
<tr>
<td>


16

</td>
<td>


wCommandRegister

</td>
<td>


0005

</td>
<td>


Identifier for Command Register

</td>
</tr>
<tr>
<td>


18

</td>
<td>


wDataRegister

</td>
<td>


0006

</td>
<td>


Identifier for Data Register

</td>
</tr>
<tr>
<td>


20

</td>
<td>


wVendorID

</td>
<td>


044E

</td>
<td>


Vendor ID 0x044E

</td>
</tr>
<tr>
<td>


22

</td>
<td>


wProductID

</td>
<td>


120B

</td>
<td>


Product ID 0x120B

</td>
</tr>
<tr>
<td>


24

</td>
<td>


wVersionID

</td>
<td>


0121

</td>
<td>


Version 01.21

</td>
</tr>
<tr>
<td>


26

</td>
<td>


RESERVED

</td>
<td>


0000

</td>
<td>


RESERVED

</td>
</tr>
</tbody>
</table>

<a id="rst-report-id"></a>

## Report ID


<table>
<tbody>
<tr>
<td>


ReportID-1

</td>
<td>


(Input Reports)

</td>
<td>


(HIDUsage-Mouse) for TP&amp;SP

</td>
</tr>
<tr>
<td>


ReportID-2

</td>
<td>


(Input Reports)

</td>
<td>


(HIDUsage-keyboard) for TP

</td>
</tr>
<tr>
<td>


ReportID-3

</td>
<td>


(Input Reports)

</td>
<td>


(Vendor Usage: Max 10 finger data) for TP

</td>
</tr>
<tr>
<td>


ReportID-4

</td>
<td>


(Input Reports)

</td>
<td>


(Vendor Usage: ON bit data) for GP

</td>
</tr>
<tr>
<td>


ReportID-5

</td>
<td>


(Feature Reports)

</td>
<td>


Feature Reports

</td>
</tr>
<tr>
<td>


ReportID-6

</td>
<td>


(Input Reports)

</td>
<td>


(Vendor Usage: StickPointer data) for SP

</td>
</tr>
<tr>
<td>


ReportID-7

</td>
<td>


(Feature Reports)

</td>
<td>


Flash update (Bootloader)

</td>
</tr>
</tbody>
</table>

<a id="rst-data-pattern"></a>

## Data pattern


<table>
<tbody>
<tr>
<td>


Case1

</td>
<td>


ReportID_1

</td>
<td>


TP/SP

</td>
<td>


Relative/Relative

</td>
</tr>
<tr>
<td>


Case2

</td>
<td>


ReportID_3 ReportID_6

</td>
<td>


TP SP

</td>
<td>


Absolute Absolute

</td>
</tr>
</tbody>
</table>

<a id="rst-command-read-write"></a>

## Command Read/Write

To read/write to RAM, need to send a command to the device.

The command format is as below.

<a id="rst-databyte-set-report"></a>

### DataByte(SET_REPORT)


<table>
<tbody>
<tr>
<td>


Byte1

</td>
<td>


Command Byte

</td>
</tr>
<tr>
<td>


Byte2

</td>
<td>


Address - Byte 0 (LSB)

</td>
</tr>
<tr>
<td>


Byte3

</td>
<td>


Address - Byte 1

</td>
</tr>
<tr>
<td>


Byte4

</td>
<td>


Address - Byte 2

</td>
</tr>
<tr>
<td>


Byte5

</td>
<td>


Address - Byte 3 (MSB)

</td>
</tr>
<tr>
<td>


Byte6

</td>
<td>


Value Byte

</td>
</tr>
<tr>
<td>


Byte7

</td>
<td>


Checksum

</td>
</tr>
</tbody>
</table>

Command Byte is read=0xD1/write=0xD2.

Address is read/write RAM address.

Value Byte is writing data when you send the write commands.

When you read RAM, there is no meaning.

<a id="rst-databyte-get-report"></a>

### DataByte(GET_REPORT)


<table>
<tbody>
<tr>
<td>


Byte1

</td>
<td>


Response Byte

</td>
</tr>
<tr>
<td>


Byte2

</td>
<td>


Address - Byte 0 (LSB)

</td>
</tr>
<tr>
<td>


Byte3

</td>
<td>


Address - Byte 1

</td>
</tr>
<tr>
<td>


Byte4

</td>
<td>


Address - Byte 2

</td>
</tr>
<tr>
<td>


Byte5

</td>
<td>


Address - Byte 3 (MSB)

</td>
</tr>
<tr>
<td>


Byte6

</td>
<td>


Value Byte

</td>
</tr>
<tr>
<td>


Byte7

</td>
<td>


Checksum

</td>
</tr>
</tbody>
</table>

Read value is stored in Value Byte.

<a id="rst-packet-format"></a>

## Packet Format

<a id="rst-touchpad-data-byte"></a>

### Touchpad data byte


<table>
<thead>
<tr>
<th>


- <!-- empty source list item -->

</th>
<th>


b7

</th>
<th>


b6

</th>
<th>


b5

</th>
<th>


b4

</th>
<th>


b3

</th>
<th>


b2

</th>
<th>


b1

</th>
<th>


b0

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


1

</td>
<td>


0

</td>
<td>


0

</td>
<td>


SW6

</td>
<td>


SW5

</td>
<td>


SW4

</td>
<td>


SW3

</td>
<td>


SW2

</td>
<td>


SW1

</td>
</tr>
<tr>
<td>


2

</td>
<td>


0

</td>
<td>


0

</td>
<td>


0

</td>
<td>


Fcv

</td>
<td>


Fn3

</td>
<td>


Fn2

</td>
<td>


Fn1

</td>
<td>


Fn0

</td>
</tr>
<tr>
<td>


3

</td>
<td>


Xa0_7

</td>
<td>


Xa0_6

</td>
<td>


Xa0_5

</td>
<td>


Xa0_4

</td>
<td>


Xa0_3

</td>
<td>


Xa0_2

</td>
<td>


Xa0_1

</td>
<td>


Xa0_0

</td>
</tr>
<tr>
<td>


4

</td>
<td>


Xa0_15

</td>
<td>


Xa0_14

</td>
<td>


Xa0_13

</td>
<td>


Xa0_12

</td>
<td>


Xa0_11

</td>
<td>


Xa0_10

</td>
<td>


Xa0_9

</td>
<td>


Xa0_8

</td>
</tr>
<tr>
<td>


5

</td>
<td>


Ya0_7

</td>
<td>


Ya0_6

</td>
<td>


Ya0_5

</td>
<td>


Ya0_4

</td>
<td>


Ya0_3

</td>
<td>


Ya0_2

</td>
<td>


Ya0_1

</td>
<td>


Ya0_0

</td>
</tr>
<tr>
<td>


6

</td>
<td>


Ya0_15

</td>
<td>


Ya0_14

</td>
<td>


Ya0_13

</td>
<td>


Ya0_12

</td>
<td>


Ya0_11

</td>
<td>


Ya0_10

</td>
<td>


Ya0_9

</td>
<td>


Ya0_8

</td>
</tr>
<tr>
<td>


7

</td>
<td>


LFB0

</td>
<td>


Zs0_6

</td>
<td>


Zs0_5

</td>
<td>


Zs0_4

</td>
<td>


Zs0_3

</td>
<td>


Zs0_2

</td>
<td>


Zs0_1

</td>
<td>


Zs0_0

</td>
</tr>
<tr>
<td>


8

</td>
<td>


Xa1_7

</td>
<td>


Xa1_6

</td>
<td>


Xa1_5

</td>
<td>


Xa1_4

</td>
<td>


Xa1_3

</td>
<td>


Xa1_2

</td>
<td>


Xa1_1

</td>
<td>


Xa1_0

</td>
</tr>
<tr>
<td>


9

</td>
<td>


Xa1_15

</td>
<td>


Xa1_14

</td>
<td>


Xa1_13

</td>
<td>


Xa1_12

</td>
<td>


Xa1_11

</td>
<td>


Xa1_10

</td>
<td>


Xa1_9

</td>
<td>


Xa1_8

</td>
</tr>
<tr>
<td>


10

</td>
<td>


Ya1_7

</td>
<td>


Ya1_6

</td>
<td>


Ya1_5

</td>
<td>


Ya1_4

</td>
<td>


Ya1_3

</td>
<td>


Ya1_2

</td>
<td>


Ya1_1

</td>
<td>


Ya1_0

</td>
</tr>
<tr>
<td>


11

</td>
<td>


Ya1_15

</td>
<td>


Ya1_14

</td>
<td>


Ya1_13

</td>
<td>


Ya1_12

</td>
<td>


Ya1_11

</td>
<td>


Ya1_10

</td>
<td>


Ya1_9

</td>
<td>


Ya1_8

</td>
</tr>
<tr>
<td>


12

</td>
<td>


LFB1

</td>
<td>


Zs1_6

</td>
<td>


Zs1_5

</td>
<td>


Zs1_4

</td>
<td>


Zs1_3

</td>
<td>


Zs1_2

</td>
<td>


Zs1_1

</td>
<td>


Zs1_0

</td>
</tr>
<tr>
<td>


13

</td>
<td>


Xa2_7

</td>
<td>


Xa2_6

</td>
<td>


Xa2_5

</td>
<td>


Xa2_4

</td>
<td>


Xa2_3

</td>
<td>


Xa2_2

</td>
<td>


Xa2_1

</td>
<td>


Xa2_0

</td>
</tr>
<tr>
<td>


14

</td>
<td>


Xa2_15

</td>
<td>


Xa2_14

</td>
<td>


Xa2_13

</td>
<td>


Xa2_12

</td>
<td>


Xa2_11

</td>
<td>


Xa2_10

</td>
<td>


Xa2_9

</td>
<td>


Xa2_8

</td>
</tr>
<tr>
<td>


15

</td>
<td>


Ya2_7

</td>
<td>


Ya2_6

</td>
<td>


Ya2_5

</td>
<td>


Ya2_4

</td>
<td>


Ya2_3

</td>
<td>


Ya2_2

</td>
<td>


Ya2_1

</td>
<td>


Ya2_0

</td>
</tr>
<tr>
<td>


16

</td>
<td>


Ya2_15

</td>
<td>


Ya2_14

</td>
<td>


Ya2_13

</td>
<td>


Ya2_12

</td>
<td>


Ya2_11

</td>
<td>


Ya2_10

</td>
<td>


Ya2_9

</td>
<td>


Ya2_8

</td>
</tr>
<tr>
<td>


17

</td>
<td>


LFB2

</td>
<td>


Zs2_6

</td>
<td>


Zs2_5

</td>
<td>


Zs2_4

</td>
<td>


Zs2_3

</td>
<td>


Zs2_2

</td>
<td>


Zs2_1

</td>
<td>


Zs2_0

</td>
</tr>
<tr>
<td>


18

</td>
<td>


Xa3_7

</td>
<td>


Xa3_6

</td>
<td>


Xa3_5

</td>
<td>


Xa3_4

</td>
<td>


Xa3_3

</td>
<td>


Xa3_2

</td>
<td>


Xa3_1

</td>
<td>


Xa3_0

</td>
</tr>
<tr>
<td>


19

</td>
<td>


Xa3_15

</td>
<td>


Xa3_14

</td>
<td>


Xa3_13

</td>
<td>


Xa3_12

</td>
<td>


Xa3_11

</td>
<td>


Xa3_10

</td>
<td>


Xa3_9

</td>
<td>


Xa3_8

</td>
</tr>
<tr>
<td>


20

</td>
<td>


Ya3_7

</td>
<td>


Ya3_6

</td>
<td>


Ya3_5

</td>
<td>


Ya3_4

</td>
<td>


Ya3_3

</td>
<td>


Ya3_2

</td>
<td>


Ya3_1

</td>
<td>


Ya3_0

</td>
</tr>
<tr>
<td>


21

</td>
<td>


Ya3_15

</td>
<td>


Ya3_14

</td>
<td>


Ya3_13

</td>
<td>


Ya3_12

</td>
<td>


Ya3_11

</td>
<td>


Ya3_10

</td>
<td>


Ya3_9

</td>
<td>


Ya3_8

</td>
</tr>
<tr>
<td>


22

</td>
<td>


LFB3

</td>
<td>


Zs3_6

</td>
<td>


Zs3_5

</td>
<td>


Zs3_4

</td>
<td>


Zs3_3

</td>
<td>


Zs3_2

</td>
<td>


Zs3_1

</td>
<td>


Zs3_0

</td>
</tr>
<tr>
<td>


23

</td>
<td>


Xa4_7

</td>
<td>


Xa4_6

</td>
<td>


Xa4_5

</td>
<td>


Xa4_4

</td>
<td>


Xa4_3

</td>
<td>


Xa4_2

</td>
<td>


Xa4_1

</td>
<td>


Xa4_0

</td>
</tr>
<tr>
<td>


24

</td>
<td>


Xa4_15

</td>
<td>


Xa4_14

</td>
<td>


Xa4_13

</td>
<td>


Xa4_12

</td>
<td>


Xa4_11

</td>
<td>


Xa4_10

</td>
<td>


Xa4_9

</td>
<td>


Xa4_8

</td>
</tr>
<tr>
<td>


25

</td>
<td>


Ya4_7

</td>
<td>


Ya4_6

</td>
<td>


Ya4_5

</td>
<td>


Ya4_4

</td>
<td>


Ya4_3

</td>
<td>


Ya4_2

</td>
<td>


Ya4_1

</td>
<td>


Ya4_0

</td>
</tr>
<tr>
<td>


26

</td>
<td>


Ya4_15

</td>
<td>


Ya4_14

</td>
<td>


Ya4_13

</td>
<td>


Ya4_12

</td>
<td>


Ya4_11

</td>
<td>


Ya4_10

</td>
<td>


Ya4_9

</td>
<td>


Ya4_8

</td>
</tr>
<tr>
<td>


27

</td>
<td>


LFB4

</td>
<td>


Zs4_6

</td>
<td>


Zs4_5

</td>
<td>


Zs4_4

</td>
<td>


Zs4_3

</td>
<td>


Zs4_2

</td>
<td>


Zs4_1

</td>
<td>


Zs4_0

</td>
</tr>
</tbody>
</table>

- **SW1-SW6:**

  SW ON/OFF status

- **Xan_15-0(16bit):**

  X Absolute data of the "n"th finger

- **Yan_15-0(16bit):**

  Y Absolute data of the "n"th finger

- **Zsn_6-0(7bit):**

  Operation area of the "n"th finger

<a id="rst-stickpointer-data-byte"></a>

### StickPointer data byte


<table>
<thead>
<tr>
<th>


- <!-- empty source list item -->

</th>
<th>


b7

</th>
<th>


b6

</th>
<th>


b5

</th>
<th>


b4

</th>
<th>


b3

</th>
<th>


b2

</th>
<th>


b1

</th>
<th>


b0

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


Byte1

</td>
<td>


1

</td>
<td>


1

</td>
<td>


1

</td>
<td>


0

</td>
<td>


1

</td>
<td>


SW3

</td>
<td>


SW2

</td>
<td>


SW1

</td>
</tr>
<tr>
<td>


Byte2

</td>
<td>


X7

</td>
<td>


X6

</td>
<td>


X5

</td>
<td>


X4

</td>
<td>


X3

</td>
<td>


X2

</td>
<td>


X1

</td>
<td>


X0

</td>
</tr>
<tr>
<td>


Byte3

</td>
<td>


X15

</td>
<td>


X14

</td>
<td>


X13

</td>
<td>


X12

</td>
<td>


X11

</td>
<td>


X10

</td>
<td>


X9

</td>
<td>


X8

</td>
</tr>
<tr>
<td>


Byte4

</td>
<td>


Y7

</td>
<td>


Y6

</td>
<td>


Y5

</td>
<td>


Y4

</td>
<td>


Y3

</td>
<td>


Y2

</td>
<td>


Y1

</td>
<td>


Y0

</td>
</tr>
<tr>
<td>


Byte5

</td>
<td>


Y15

</td>
<td>


Y14

</td>
<td>


Y13

</td>
<td>


Y12

</td>
<td>


Y11

</td>
<td>


Y10

</td>
<td>


Y9

</td>
<td>


Y8

</td>
</tr>
<tr>
<td>


Byte6

</td>
<td>


Z7

</td>
<td>


Z6

</td>
<td>


Z5

</td>
<td>


Z4

</td>
<td>


Z3

</td>
<td>


Z2

</td>
<td>


Z1

</td>
<td>


Z0

</td>
</tr>
<tr>
<td>


Byte7

</td>
<td>


T&amp;P

</td>
<td>


Z14

</td>
<td>


Z13

</td>
<td>


Z12

</td>
<td>


Z11

</td>
<td>


Z10

</td>
<td>


Z9

</td>
<td>


Z8

</td>
</tr>
</tbody>
</table>

- **SW1-SW3:**

  SW ON/OFF status

- **Xn_15-0(16bit):**

  X Absolute data

- **Yn_15-0(16bit):**

  Y Absolute data

- **Zn_14-0(15bit):**

  Z
