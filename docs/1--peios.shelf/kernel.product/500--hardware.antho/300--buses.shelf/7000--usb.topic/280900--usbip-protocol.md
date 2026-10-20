---
title: "USB/IP protocol"
type: reference
description: "The USB/IP protocol follows a server/client architecture. The server exports the USB devices and the clients import them. The device driver for the exported USB device runs on the client machine."
---

<a id="rst-usb-ip-protocol"></a>

<a id="rst-architecture"></a>

## Architecture

The USB/IP protocol follows a server/client architecture. The server exports the USB devices and the clients import them. The device driver for the exported USB device runs on the client machine.

The client may ask for the list of the exported USB devices. To get the list the client opens a TCP/IP connection to the server, and sends an OP_REQ_DEVLIST packet on top of the TCP/IP connection (so the actual OP_REQ_DEVLIST may be sent in one or more pieces at the low level transport layer). The server sends back the OP_REP_DEVLIST packet which lists the exported USB devices. Finally the TCP/IP connection is closed.



```text
virtual host controller                                 usb host
     "client"                                           "server"
 (imports USB devices)                             (exports USB devices)
         |                                                 |
         |                  OP_REQ_DEVLIST                 |
         | ----------------------------------------------> |
         |                                                 |
         |                  OP_REP_DEVLIST                 |
         | <---------------------------------------------- |
         |                                                 |
```

Once the client knows the list of exported USB devices it may decide to use one of them. First the client opens a TCP/IP connection to the server and sends an OP_REQ_IMPORT packet. The server replies with OP_REP_IMPORT. If the import was successful the TCP/IP connection remains open and will be used to transfer the URB traffic between the client and the server. The client may send two types of packets: the USBIP_CMD_SUBMIT to submit an URB, and USBIP_CMD_UNLINK to unlink a previously submitted URB. The answers of the server may be USBIP_RET_SUBMIT and USBIP_RET_UNLINK respectively.



```text
virtual host controller                                 usb host
     "client"                                           "server"
 (imports USB devices)                             (exports USB devices)
         |                                                 |
         |                  OP_REQ_IMPORT                  |
         | ----------------------------------------------> |
         |                                                 |
         |                  OP_REP_IMPORT                  |
         | <---------------------------------------------- |
         |                                                 |
         |                                                 |
         |            USBIP_CMD_SUBMIT(seqnum = n)         |
         | ----------------------------------------------> |
         |                                                 |
         |            USBIP_RET_SUBMIT(seqnum = n)         |
         | <---------------------------------------------- |
         |                        .                        |
         |                        :                        |
         |                                                 |
         |            USBIP_CMD_SUBMIT(seqnum = m)         |
         | ----------------------------------------------> |
         |                                                 |
         |            USBIP_CMD_SUBMIT(seqnum = m+1)       |
         | ----------------------------------------------> |
         |                                                 |
         |            USBIP_CMD_SUBMIT(seqnum = m+2)       |
         | ----------------------------------------------> |
         |                                                 |
         |            USBIP_RET_SUBMIT(seqnum = m)         |
         | <---------------------------------------------- |
         |                                                 |
         |            USBIP_CMD_SUBMIT(seqnum = m+3)       |
         | ----------------------------------------------> |
         |                                                 |
         |            USBIP_RET_SUBMIT(seqnum = m+1)       |
         | <---------------------------------------------- |
         |                                                 |
         |            USBIP_CMD_SUBMIT(seqnum = m+4)       |
         | ----------------------------------------------> |
         |                                                 |
         |            USBIP_RET_SUBMIT(seqnum = m+2)       |
         | <---------------------------------------------- |
         |                        .                        |
         |                        :                        |
```

For UNLINK, note that after a successful USBIP_RET_UNLINK, the unlinked URB submission would not have a corresponding USBIP_RET_SUBMIT (this is explained in function stub_recv_cmd_unlink of drivers/usb/usbip/stub_rx.c).



```text
virtual host controller                                 usb host
     "client"                                           "server"
 (imports USB devices)                             (exports USB devices)
         |                                                 |
         |            USBIP_CMD_SUBMIT(seqnum = p)         |
         | ----------------------------------------------> |
         |                                                 |
         |               USBIP_CMD_UNLINK                  |
         |         (seqnum = p+1, unlink_seqnum = p)       |
         | ----------------------------------------------> |
         |                                                 |
         |               USBIP_RET_UNLINK                  |
         |        (seqnum = p+1, status = -ECONNRESET)     |
         | <---------------------------------------------- |
         |                                                 |
         |         Note: No USBIP_RET_SUBMIT(seqnum = p)   |
         | <--X---X---X---X---X---X---X---X---X---X---X--- |
         |                        .                        |
         |                        :                        |
         |                                                 |
         |            USBIP_CMD_SUBMIT(seqnum = q)         |
         | ----------------------------------------------> |
         |                                                 |
         |            USBIP_RET_SUBMIT(seqnum = q)         |
         | <---------------------------------------------- |
         |                                                 |
         |               USBIP_CMD_UNLINK                  |
         |         (seqnum = q+1, unlink_seqnum = q)       |
         | ----------------------------------------------> |
         |                                                 |
         |               USBIP_RET_UNLINK                  |
         |           (seqnum = q+1, status = 0)            |
         | <---------------------------------------------- |
         |                                                 |
```

The fields are in network (big endian) byte order meaning that the most significant byte (MSB) is stored at the lowest address.

<a id="rst-protocol-version"></a>

## Protocol Version

The documented USBIP version is v1.1.1. The binary representation of this version in message headers is 0x0111.

This is defined in tools/usb/usbip/configure.ac

<a id="rst-message-format"></a>

## Message Format

- **OP_REQ_DEVLIST:**

  Retrieve the list of exported USB devices.


<table>
<thead>
<tr>
<th>


Offset

</th>
<th>


Length

</th>
<th>


Value

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


2

</td>
<td>




</td>
<td>


USBIP version

</td>
</tr>
<tr>
<td>


2

</td>
<td>


2

</td>
<td>


0x8005

</td>
<td>


Command code: Retrieve the list of exported USB devices.

</td>
</tr>
<tr>
<td>


4

</td>
<td>


4

</td>
<td>


0x00000000

</td>
<td>


Status: unused, shall be set to 0

</td>
</tr>
</tbody>
</table>

- **OP_REP_DEVLIST:**

  Reply with the list of exported USB devices.


<table>
<thead>
<tr>
<th>


Offset

</th>
<th>


Length

</th>
<th>


Value

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


2

</td>
<td>




</td>
<td>


USBIP version

</td>
</tr>
<tr>
<td>


2

</td>
<td>


2

</td>
<td>


0x0005

</td>
<td>


Reply code: The list of exported USB devices.

</td>
</tr>
<tr>
<td>


4

</td>
<td>


4

</td>
<td>


0x00000000

</td>
<td>


Status: 0 for OK

</td>
</tr>
<tr>
<td>


8

</td>
<td>


4

</td>
<td>


n

</td>
<td>


Number of exported devices: 0 means no exported devices.

</td>
</tr>
<tr>
<td>


0x0C

</td>
<td>




</td>
<td>




</td>
<td>


From now on the exported n devices are described, if any. If no devices are exported the message ends with the previous "number of exported devices" field.

</td>
</tr>
<tr>
<td>




</td>
<td>


256

</td>
<td>




</td>
<td>


path: Path of the device on the host exporting the USB device, string closed with zero byte, e.g. "/sys/devices/pci0000:00/0000:00:1d.1/usb3/3-2" The unused bytes shall be filled with zero bytes.

</td>
</tr>
<tr>
<td>


0x10C

</td>
<td>


32

</td>
<td>




</td>
<td>


busid: Bus ID of the exported device, string closed with zero byte, e.g. "3-2". The unused bytes shall be filled with zero bytes.

</td>
</tr>
<tr>
<td>


0x12C

</td>
<td>


4

</td>
<td>




</td>
<td>


busnum

</td>
</tr>
<tr>
<td>


0x130

</td>
<td>


4

</td>
<td>




</td>
<td>


devnum

</td>
</tr>
<tr>
<td>


0x134

</td>
<td>


4

</td>
<td>




</td>
<td>


speed

</td>
</tr>
<tr>
<td>


0x138

</td>
<td>


2

</td>
<td>




</td>
<td>


idVendor

</td>
</tr>
<tr>
<td>


0x13A

</td>
<td>


2

</td>
<td>




</td>
<td>


idProduct

</td>
</tr>
<tr>
<td>


0x13C

</td>
<td>


2

</td>
<td>




</td>
<td>


bcdDevice

</td>
</tr>
<tr>
<td>


0x13E

</td>
<td>


1

</td>
<td>




</td>
<td>


bDeviceClass

</td>
</tr>
<tr>
<td>


0x13F

</td>
<td>


1

</td>
<td>




</td>
<td>


bDeviceSubClass

</td>
</tr>
<tr>
<td>


0x140

</td>
<td>


1

</td>
<td>




</td>
<td>


bDeviceProtocol

</td>
</tr>
<tr>
<td>


0x141

</td>
<td>


1

</td>
<td>




</td>
<td>


bConfigurationValue

</td>
</tr>
<tr>
<td>


0x142

</td>
<td>


1

</td>
<td>




</td>
<td>


bNumConfigurations

</td>
</tr>
<tr>
<td>


0x143

</td>
<td>


1

</td>
<td>




</td>
<td>


bNumInterfaces

</td>
</tr>
<tr>
<td>


0x144

</td>
<td>




</td>
<td>


m_0

</td>
<td>


From now on each interface is described, all together bNumInterfaces times, with the following 4 fields:

</td>
</tr>
<tr>
<td>




</td>
<td>


1

</td>
<td>




</td>
<td>


bInterfaceClass

</td>
</tr>
<tr>
<td>


0x145

</td>
<td>


1

</td>
<td>




</td>
<td>


bInterfaceSubClass

</td>
</tr>
<tr>
<td>


0x146

</td>
<td>


1

</td>
<td>




</td>
<td>


bInterfaceProtocol

</td>
</tr>
<tr>
<td>


0x147

</td>
<td>


1

</td>
<td>




</td>
<td>


padding byte for alignment, shall be set to zero

</td>
</tr>
<tr>
<td>


0xC + i\*0x138 + m\_(i-1)\*4

</td>
<td>




</td>
<td>




</td>
<td>


The second exported USB device starts at i=1 with the path field.

</td>
</tr>
</tbody>
</table>

- **OP_REQ_IMPORT:**

  Request to import (attach) a remote USB device.


<table>
<thead>
<tr>
<th>


Offset

</th>
<th>


Length

</th>
<th>


Value

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


2

</td>
<td>




</td>
<td>


USBIP version

</td>
</tr>
<tr>
<td>


2

</td>
<td>


2

</td>
<td>


0x8003

</td>
<td>


Command code: import a remote USB device.

</td>
</tr>
<tr>
<td>


4

</td>
<td>


4

</td>
<td>


0x00000000

</td>
<td>


Status: unused, shall be set to 0

</td>
</tr>
<tr>
<td>


8

</td>
<td>


32

</td>
<td>




</td>
<td>


busid: the busid of the exported device on the remote host. The possible values are taken from the message field OP_REP_DEVLIST.busid. A string closed with zero, the unused bytes shall be filled with zeros.

</td>
</tr>
</tbody>
</table>

- **OP_REP_IMPORT:**

  Reply to import (attach) a remote USB device.


<table>
<thead>
<tr>
<th>


Offset

</th>
<th>


Length

</th>
<th>


Value

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


2

</td>
<td>




</td>
<td>


USBIP version

</td>
</tr>
<tr>
<td>


2

</td>
<td>


2

</td>
<td>


0x0003

</td>
<td>


Reply code: Reply to import.

</td>
</tr>
<tr>
<td>


4

</td>
<td>


4

</td>
<td>


0x00000000

</td>
<td>


Status:

> - 0 for OK
>
> - 1 for error

</td>
</tr>
<tr>
<td>


8

</td>
<td>




</td>
<td>




</td>
<td>


From now on comes the details of the imported device, if the previous status field was OK (0), otherwise the reply ends with the status field.

</td>
</tr>
<tr>
<td>




</td>
<td>


256

</td>
<td>




</td>
<td>


path: Path of the device on the host exporting the USB device, string closed with zero byte, e.g. "/sys/devices/pci0000:00/0000:00:1d.1/usb3/3-2" The unused bytes shall be filled with zero bytes.

</td>
</tr>
<tr>
<td>


0x108

</td>
<td>


32

</td>
<td>




</td>
<td>


busid: Bus ID of the exported device, string closed with zero byte, e.g. "3-2". The unused bytes shall be filled with zero bytes.

</td>
</tr>
<tr>
<td>


0x128

</td>
<td>


4

</td>
<td>




</td>
<td>


busnum

</td>
</tr>
<tr>
<td>


0x12C

</td>
<td>


4

</td>
<td>




</td>
<td>


devnum

</td>
</tr>
<tr>
<td>


0x130

</td>
<td>


4

</td>
<td>




</td>
<td>


speed

</td>
</tr>
<tr>
<td>


0x134

</td>
<td>


2

</td>
<td>




</td>
<td>


idVendor

</td>
</tr>
<tr>
<td>


0x136

</td>
<td>


2

</td>
<td>




</td>
<td>


idProduct

</td>
</tr>
<tr>
<td>


0x138

</td>
<td>


2

</td>
<td>




</td>
<td>


bcdDevice

</td>
</tr>
<tr>
<td>


0x13A

</td>
<td>


1

</td>
<td>




</td>
<td>


bDeviceClass

</td>
</tr>
<tr>
<td>


0x13B

</td>
<td>


1

</td>
<td>




</td>
<td>


bDeviceSubClass

</td>
</tr>
<tr>
<td>


0x13C

</td>
<td>


1

</td>
<td>




</td>
<td>


bDeviceProtocol

</td>
</tr>
<tr>
<td>


0x13D

</td>
<td>


1

</td>
<td>




</td>
<td>


bConfigurationValue

</td>
</tr>
<tr>
<td>


0x13E

</td>
<td>


1

</td>
<td>




</td>
<td>


bNumConfigurations

</td>
</tr>
<tr>
<td>


0x13F

</td>
<td>


1

</td>
<td>




</td>
<td>


bNumInterfaces

</td>
</tr>
</tbody>
</table>

The following four commands have a common basic header called 'usbip_header_basic', and their headers, called 'usbip_header' (before transfer_buffer payload), have the same length, therefore paddings are needed.

usbip_header_basic:


<table>
<thead>
<tr>
<th>


Offset

</th>
<th>


Length

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


4

</td>
<td>


command

</td>
</tr>
<tr>
<td>


4

</td>
<td>


4

</td>
<td>


seqnum: sequential number that identifies requests and corresponding responses; incremented per connection

</td>
</tr>
<tr>
<td>


8

</td>
<td>


4

</td>
<td>


devid: specifies a remote USB device uniquely instead of busnum and devnum; for client (request), this value is ((busnum &lt;&lt; 16) \| devnum); for server (response), this shall be set to 0

</td>
</tr>
<tr>
<td>


0xC

</td>
<td>


4

</td>
<td>


direction:

> - 0: USBIP_DIR_OUT
>
> - 1: USBIP_DIR_IN

only used by client, for server this shall be 0

</td>
</tr>
<tr>
<td>


0x10

</td>
<td>


4

</td>
<td>


ep: endpoint number only used by client, for server this shall be 0; for UNLINK, this shall be 0

</td>
</tr>
</tbody>
</table>

- **USBIP_CMD_SUBMIT:**

  Submit an URB


<table>
<thead>
<tr>
<th>


Offset

</th>
<th>


Length

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


20

</td>
<td>


usbip_header_basic, 'command' shall be 0x00000001

</td>
</tr>
<tr>
<td>


0x14

</td>
<td>


4

</td>
<td>


transfer_flags: possible values depend on the USBIP_URB transfer_flags. Refer to include/uapi/linux/usbip.h and [Documentation/driver-api/usb/URB.rst](~kernel/hardware/driver-api/usb/urb). Refer to usbip_pack_cmd_submit() and tweak_transfer_flags() in drivers/usb/usbip/ usbip_common.c.

</td>
</tr>
<tr>
<td>


0x18

</td>
<td>


4

</td>
<td>


transfer_buffer_length: use URB transfer_buffer_length

</td>
</tr>
<tr>
<td>


0x1C

</td>
<td>


4

</td>
<td>


start_frame: use URB start_frame; initial frame for ISO transfer; shall be set to 0 if not ISO transfer

</td>
</tr>
<tr>
<td>


0x20

</td>
<td>


4

</td>
<td>


number_of_packets: number of ISO packets; shall be set to 0xffffffff if not ISO transfer

</td>
</tr>
<tr>
<td>


0x24

</td>
<td>


4

</td>
<td>


interval: maximum time for the request on the server-side host controller

</td>
</tr>
<tr>
<td>


0x28

</td>
<td>


8

</td>
<td>


setup: data bytes for USB setup, filled with zeros if not used.

</td>
</tr>
<tr>
<td>


0x30

</td>
<td>


n

</td>
<td>


transfer_buffer. If direction is USBIP_DIR_OUT then n equals transfer_buffer_length; otherwise n equals 0. For ISO transfers the padding between each ISO packets is not transmitted.

</td>
</tr>
<tr>
<td>


0x30+n

</td>
<td>


m

</td>
<td>


iso_packet_descriptor

</td>
</tr>
</tbody>
</table>

- **USBIP_RET_SUBMIT:**

  Reply for submitting an URB


<table>
<thead>
<tr>
<th>


Offset

</th>
<th>


Length

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


20

</td>
<td>


usbip_header_basic, 'command' shall be 0x00000003

</td>
</tr>
<tr>
<td>


0x14

</td>
<td>


4

</td>
<td>


status: zero for successful URB transaction, otherwise some kind of error happened.

</td>
</tr>
<tr>
<td>


0x18

</td>
<td>


4

</td>
<td>


actual_length: number of URB data bytes; use URB actual_length

</td>
</tr>
<tr>
<td>


0x1C

</td>
<td>


4

</td>
<td>


start_frame: use URB start_frame; initial frame for ISO transfer; shall be set to 0 if not ISO transfer

</td>
</tr>
<tr>
<td>


0x20

</td>
<td>


4

</td>
<td>


number_of_packets: number of ISO packets; shall be set to 0xffffffff if not ISO transfer

</td>
</tr>
<tr>
<td>


0x24

</td>
<td>


4

</td>
<td>


error_count

</td>
</tr>
<tr>
<td>


0x28

</td>
<td>


8

</td>
<td>


padding, shall be set to 0

</td>
</tr>
<tr>
<td>


0x30

</td>
<td>


n

</td>
<td>


transfer_buffer. If direction is USBIP_DIR_IN then n equals actual_length; otherwise n equals 0. For ISO transfers the padding between each ISO packets is not transmitted.

</td>
</tr>
<tr>
<td>


0x30+n

</td>
<td>


m

</td>
<td>


iso_packet_descriptor

</td>
</tr>
</tbody>
</table>

- **USBIP_CMD_UNLINK:**

  Unlink an URB


<table>
<thead>
<tr>
<th>


Offset

</th>
<th>


Length

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


20

</td>
<td>


usbip_header_basic, 'command' shall be 0x00000002

</td>
</tr>
<tr>
<td>


0x14

</td>
<td>


4

</td>
<td>


unlink_seqnum, of the SUBMIT request to unlink

</td>
</tr>
<tr>
<td>


0x18

</td>
<td>


24

</td>
<td>


padding, shall be set to 0

</td>
</tr>
</tbody>
</table>

- **USBIP_RET_UNLINK:**

  Reply for URB unlink


<table>
<thead>
<tr>
<th>


Offset

</th>
<th>


Length

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


20

</td>
<td>


usbip_header_basic, 'command' shall be 0x00000004

</td>
</tr>
<tr>
<td>


0x14

</td>
<td>


4

</td>
<td>


status: This is similar to the status of USBIP_RET_SUBMIT (share the same memory offset). When UNLINK is successful, status is -ECONNRESET; when USBIP_CMD_UNLINK is after USBIP_RET_SUBMIT status is 0

</td>
</tr>
<tr>
<td>


0x18

</td>
<td>


24

</td>
<td>


padding, shall be set to 0

</td>
</tr>
</tbody>
</table>

<a id="rst-example"></a>

## EXAMPLE

> The following data is captured from wire with Human Interface Devices (HID) payload



```text
CmdIntrIN:  00000001 00000d05 0001000f 00000001 00000001 00000200 00000040 ffffffff 00000000 00000004 00000000 00000000
CmdIntrOUT: 00000001 00000d06 0001000f 00000000 00000001 00000000 00000040 ffffffff 00000000 00000004 00000000 00000000
            ffffffff860008a784ce5ae212376300000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
RetIntrOut: 00000003 00000d06 00000000 00000000 00000000 00000000 00000040 ffffffff 00000000 00000000 00000000 00000000
RetIntrIn:  00000003 00000d05 00000000 00000000 00000000 00000000 00000040 ffffffff 00000000 00000000 00000000 00000000
            ffffffff860011a784ce5ae2123763612891b1020100000400000000000000000000000000000000000000000000000000000000000000000000000000000000
```
