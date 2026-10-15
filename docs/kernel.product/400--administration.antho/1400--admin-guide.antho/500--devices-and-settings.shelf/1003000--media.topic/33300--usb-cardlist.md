---
title: "USB drivers"
type: reference
description: "The USB boards are identified by an identification called USB ID."
---

<a id="rst-usb-drivers"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

The USB boards are identified by an identification called USB ID.

The `lsusb` command allows identifying the USB IDs:



```text
$ lsusb
...
Bus 001 Device 015: ID 046d:082d Logitech, Inc. HD Pro Webcam C920
Bus 001 Device 074: ID 2040:b131 Hauppauge
Bus 001 Device 075: ID 2013:024f PCTV Systems nanoStick T2 290e
...
```

Newer camera devices use a standard way to expose themselves as such, via USB Video Class. Those cameras are automatically supported by the `uvc-driver`.

Older cameras and TV USB devices uses USB Vendor Classes: each vendor defines its own way to access the device. This section contains card lists for such vendor-class devices.

While this is not as common as on PCI, sometimes the same USB ID is used by different products. So, several media drivers allow passing a `card=` parameter, in order to setup a card number that would match the correct settings for an specific product type.

The current supported USB cards (not including staging drivers) are listed below<a id="rst-footnote-reference-1"></a>[1](#rst-footnote-1).

<a id="rst-footnote-1"></a>



**[1]** some of the drivers have sub-drivers, not shown at this table. In particular, gspca driver has lots of sub-drivers, for cameras not supported by the USB Video Class (UVC) driver, as shown at [gspca card list](<~kernel/administration/admin-guide/media/gspca-cardlist>).


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


airspy

</td>
<td>


AirSpy

</td>
</tr>
<tr>
<td>


au0828

</td>
<td>


Auvitek AU0828

</td>
</tr>
<tr>
<td>


b2c2-flexcop-usb

</td>
<td>


Technisat/B2C2 Air/Sky/Cable2PC USB

</td>
</tr>
<tr>
<td>


cx231xx

</td>
<td>


Conexant cx231xx USB video capture

</td>
</tr>
<tr>
<td>


dvb-as102

</td>
<td>


Abilis AS102 DVB receiver

</td>
</tr>
<tr>
<td>


dvb-ttusb-budget

</td>
<td>


Technotrend/Hauppauge Nova - USB devices

</td>
</tr>
<tr>
<td>


dvb-usb-a800

</td>
<td>


AVerMedia AverTV DVB-T USB 2.0 (A800)

</td>
</tr>
<tr>
<td>


dvb-usb-af9005

</td>
<td>


Afatech AF9005 DVB-T USB1.1

</td>
</tr>
<tr>
<td>


dvb-usb-af9015

</td>
<td>


Afatech AF9015 DVB-T USB2.0

</td>
</tr>
<tr>
<td>


dvb-usb-af9035

</td>
<td>


Afatech AF9035 DVB-T USB2.0

</td>
</tr>
<tr>
<td>


dvb-usb-anysee

</td>
<td>


Anysee DVB-T/C USB2.0

</td>
</tr>
<tr>
<td>


dvb-usb-au6610

</td>
<td>


Alcor Micro AU6610 USB2.0

</td>
</tr>
<tr>
<td>


dvb-usb-az6007

</td>
<td>


AzureWave 6007 and clones DVB-T/C USB2.0

</td>
</tr>
<tr>
<td>


dvb-usb-az6027

</td>
<td>


Azurewave DVB-S/S2 USB2.0 AZ6027

</td>
</tr>
<tr>
<td>


dvb-usb-ce6230

</td>
<td>


Intel CE6230 DVB-T USB2.0

</td>
</tr>
<tr>
<td>


dvb-usb-cinergyT2

</td>
<td>


Terratec CinergyT2/qanu USB 2.0 DVB-T

</td>
</tr>
<tr>
<td>


dvb-usb-cxusb

</td>
<td>


Conexant USB2.0 hybrid

</td>
</tr>
<tr>
<td>


dvb-usb-dib0700

</td>
<td>


DiBcom DiB0700

</td>
</tr>
<tr>
<td>


dvb-usb-dibusb-common

</td>
<td>


DiBcom DiB3000M-B

</td>
</tr>
<tr>
<td>


dvb-usb-dibusb-mc

</td>
<td>


DiBcom DiB3000M-C/P

</td>
</tr>
<tr>
<td>


dvb-usb-digitv

</td>
<td>


Nebula Electronics uDigiTV DVB-T USB2.0

</td>
</tr>
<tr>
<td>


dvb-usb-dtt200u

</td>
<td>


WideView WT-200U and WT-220U (pen) DVB-T

</td>
</tr>
<tr>
<td>


dvb-usb-dtv5100

</td>
<td>


AME DTV-5100 USB2.0 DVB-T

</td>
</tr>
<tr>
<td>


dvb-usb-dvbsky

</td>
<td>


DVBSky USB

</td>
</tr>
<tr>
<td>


dvb-usb-dw2102

</td>
<td>


DvbWorld &amp; TeVii DVB-S/S2 USB2.0

</td>
</tr>
<tr>
<td>


dvb-usb-ec168

</td>
<td>


E3C EC168 DVB-T USB2.0

</td>
</tr>
<tr>
<td>


dvb-usb-gl861

</td>
<td>


Genesys Logic GL861 USB2.0

</td>
</tr>
<tr>
<td>


dvb-usb-gp8psk

</td>
<td>


GENPIX 8PSK-&gt;USB module

</td>
</tr>
<tr>
<td>


dvb-usb-lmedm04

</td>
<td>


LME DM04/QQBOX DVB-S USB2.0

</td>
</tr>
<tr>
<td>


dvb-usb-m920x

</td>
<td>


Uli m920x DVB-T USB2.0

</td>
</tr>
<tr>
<td>


dvb-usb-nova-t-usb2

</td>
<td>


Hauppauge WinTV-NOVA-T usb2 DVB-T USB2.0

</td>
</tr>
<tr>
<td>


dvb-usb-opera

</td>
<td>


Opera1 DVB-S USB2.0 receiver

</td>
</tr>
<tr>
<td>


dvb-usb-pctv452e

</td>
<td>


Pinnacle PCTV HDTV Pro USB device/TT Connect S2-3600

</td>
</tr>
<tr>
<td>


dvb-usb-rtl28xxu

</td>
<td>


Realtek RTL28xxU DVB USB

</td>
</tr>
<tr>
<td>


dvb-usb-technisat-usb2

</td>
<td>


Technisat DVB-S/S2 USB2.0

</td>
</tr>
<tr>
<td>


dvb-usb-ttusb2

</td>
<td>


Pinnacle 400e DVB-S USB2.0

</td>
</tr>
<tr>
<td>


dvb-usb-umt-010

</td>
<td>


HanfTek UMT-010 DVB-T USB2.0

</td>
</tr>
<tr>
<td>


dvb_usb_v2

</td>
<td>


Support for various USB DVB devices v2

</td>
</tr>
<tr>
<td>


dvb-usb-vp702x

</td>
<td>


TwinhanDTV StarBox and clones DVB-S USB2.0

</td>
</tr>
<tr>
<td>


dvb-usb-vp7045

</td>
<td>


TwinhanDTV Alpha/MagicBoxII, DNTV tinyUSB2, Beetle USB2.0

</td>
</tr>
<tr>
<td>


em28xx

</td>
<td>


Empia EM28xx USB devices

</td>
</tr>
<tr>
<td>


go7007

</td>
<td>


WIS GO7007 MPEG encoder

</td>
</tr>
<tr>
<td>


gspca

</td>
<td>


Drivers for several USB Cameras

</td>
</tr>
<tr>
<td>


hackrf

</td>
<td>


HackRF

</td>
</tr>
<tr>
<td>


hdpvr

</td>
<td>


Hauppauge HD PVR

</td>
</tr>
<tr>
<td>


msi2500

</td>
<td>


Mirics MSi2500

</td>
</tr>
<tr>
<td>


mxl111sf-tuner

</td>
<td>


MxL111SF DTV USB2.0

</td>
</tr>
<tr>
<td>


pvrusb2

</td>
<td>


Hauppauge WinTV-PVR USB2

</td>
</tr>
<tr>
<td>


pwc

</td>
<td>


USB Philips Cameras

</td>
</tr>
<tr>
<td>


s2250

</td>
<td>


Sensoray 2250/2251

</td>
</tr>
<tr>
<td>


s2255drv

</td>
<td>


USB Sensoray 2255 video capture device

</td>
</tr>
<tr>
<td>


smsusb

</td>
<td>


Siano SMS1xxx based MDTV receiver

</td>
</tr>
<tr>
<td>


ttusb_dec

</td>
<td>


Technotrend/Hauppauge USB DEC devices

</td>
</tr>
<tr>
<td>


usbtv

</td>
<td>


USBTV007 video capture

</td>
</tr>
<tr>
<td>


uvcvideo

</td>
<td>


USB Video Class (UVC)

</td>
</tr>
<tr>
<td>


zd1301

</td>
<td>


ZyDAS ZD1301

</td>
</tr>
</tbody>
</table>

- [AU0828 cards list](<~kernel/administration/admin-guide/media/au0828-cardlist>)
- [cx231xx cards list](<~kernel/administration/admin-guide/media/cx231xx-cardlist>)
- [EM28xx cards list](<~kernel/administration/admin-guide/media/em28xx-cardlist>)
- [Siano cards list](<~kernel/administration/admin-guide/media/siano-cardlist>)
- [The gspca cards list](<~kernel/administration/admin-guide/media/gspca-cardlist>)
- [dvb-usb-dib0700 cards list](<~kernel/administration/admin-guide/media/dvb-usb-dib0700-cardlist>)
- [dvb-usb-dibusb-mb cards list](<~kernel/administration/admin-guide/media/dvb-usb-dibusb-mb-cardlist>)
- [dvb-usb-dibusb-mc cards list](<~kernel/administration/admin-guide/media/dvb-usb-dibusb-mc-cardlist>)
- [dvb-usb-a800 cards list](<~kernel/administration/admin-guide/media/dvb-usb-a800-cardlist>)
- [dvb-usb-af9005 cards list](<~kernel/administration/admin-guide/media/dvb-usb-af9005-cardlist>)
- [dvb-usb-az6027 cards list](<~kernel/administration/admin-guide/media/dvb-usb-az6027-cardlist>)
- [dvb-usb-cinergyT2 cards list](<~kernel/administration/admin-guide/media/dvb-usb-cinergyt2-cardlist>)
- [dvb-usb-cxusb cards list](<~kernel/administration/admin-guide/media/dvb-usb-cxusb-cardlist>)
- [dvb-usb-digitv cards list](<~kernel/administration/admin-guide/media/dvb-usb-digitv-cardlist>)
- [dvb-usb-dtt200u cards list](<~kernel/administration/admin-guide/media/dvb-usb-dtt200u-cardlist>)
- [dvb-usb-dtv5100 cards list](<~kernel/administration/admin-guide/media/dvb-usb-dtv5100-cardlist>)
- [dvb-usb-dw2102 cards list](<~kernel/administration/admin-guide/media/dvb-usb-dw2102-cardlist>)
- [dvb-usb-gp8psk cards list](<~kernel/administration/admin-guide/media/dvb-usb-gp8psk-cardlist>)
- [dvb-usb-m920x cards list](<~kernel/administration/admin-guide/media/dvb-usb-m920x-cardlist>)
- [dvb-usb-nova-t-usb2 cards list](<~kernel/administration/admin-guide/media/dvb-usb-nova-t-usb2-cardlist>)
- [dvb-usb-opera1 cards list](<~kernel/administration/admin-guide/media/dvb-usb-opera1-cardlist>)
- [dvb-usb-pctv452e cards list](<~kernel/administration/admin-guide/media/dvb-usb-pctv452e-cardlist>)
- [dvb-usb-technisat-usb2 cards list](<~kernel/administration/admin-guide/media/dvb-usb-technisat-usb2-cardlist>)
- [dvb-usb-ttusb2 cards list](<~kernel/administration/admin-guide/media/dvb-usb-ttusb2-cardlist>)
- [dvb-usb-umt-010 cards list](<~kernel/administration/admin-guide/media/dvb-usb-umt-010-cardlist>)
- [dvb-usb-vp702x cards list](<~kernel/administration/admin-guide/media/dvb-usb-vp702x-cardlist>)
- [dvb-usb-vp7045 cards list](<~kernel/administration/admin-guide/media/dvb-usb-vp7045-cardlist>)
- [dvb-usb-af9015 cards list](<~kernel/administration/admin-guide/media/dvb-usb-af9015-cardlist>)
- [dvb-usb-af9035 cards list](<~kernel/administration/admin-guide/media/dvb-usb-af9035-cardlist>)
- [dvb-usb-anysee cards list](<~kernel/administration/admin-guide/media/dvb-usb-anysee-cardlist>)
- [dvb-usb-au6610 cards list](<~kernel/administration/admin-guide/media/dvb-usb-au6610-cardlist>)
- [dvb-usb-az6007 cards list](<~kernel/administration/admin-guide/media/dvb-usb-az6007-cardlist>)
- [dvb-usb-ce6230 cards list](<~kernel/administration/admin-guide/media/dvb-usb-ce6230-cardlist>)
- [dvb-usb-dvbsky cards list](<~kernel/administration/admin-guide/media/dvb-usb-dvbsky-cardlist>)
- [dvb-usb-ec168 cards list](<~kernel/administration/admin-guide/media/dvb-usb-ec168-cardlist>)
- [dvb-usb-gl861 cards list](<~kernel/administration/admin-guide/media/dvb-usb-gl861-cardlist>)
- [dvb-usb-lmedm04 cards list](<~kernel/administration/admin-guide/media/dvb-usb-lmedm04-cardlist>)
- [dvb-usb-mxl111sf cards list](<~kernel/administration/admin-guide/media/dvb-usb-mxl111sf-cardlist>)
- [dvb-usb-rtl28xxu cards list](<~kernel/administration/admin-guide/media/dvb-usb-rtl28xxu-cardlist>)
- [dvb-usb-zd1301 cards list](<~kernel/administration/admin-guide/media/dvb-usb-zd1301-cardlist>)
- [Other USB cards list](<~kernel/administration/admin-guide/media/other-usb-cardlist>)
