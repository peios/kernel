---
title: "ARECA FIRMWARE SPEC"
type: reference
description: "(All In/Out is in IOP331's view)"
---

<a id="rst-areca-firmware-spec"></a>

<a id="rst-usage-of-iop331-adapter"></a>

## Usage of IOP331 adapter

(All In/Out is in IOP331's view)

<a id="rst-message-0"></a>

### 1. Message 0

- InitThread message and return code

<a id="rst-doorbell-is-used-for-rs-232-emulation"></a>

### 2. Doorbell is used for RS-232 emulation

- **inDoorBell**

  - **bit0**

    data in ready zDRIVER DATA WRITE OK)

  - **bit1**

    data out has been read (DRIVER DATA READ OK)

- **outDooeBell:**

  - **bit0**

    data out ready (IOP331 DATA WRITE OK)

  - **bit1**

    data in has been read (IOP331 DATA READ OK)

<a id="rst-index-memory-usage"></a>

### 3. Index Memory Usage


<table>
<tbody>
<tr>
<td>


offset 0xf00

</td>
<td>


for RS232 out (request buffer)

</td>
</tr>
<tr>
<td>


offset 0xe00

</td>
<td>


for RS232 in  (scratch buffer)

</td>
</tr>
<tr>
<td>


offset 0xa00

</td>
<td>


for inbound message code message_rwbuffer (driver send to IOP331)

</td>
</tr>
<tr>
<td>


offset 0xa00

</td>
<td>


for outbound message code message_rwbuffer (IOP331 send to driver)

</td>
</tr>
</tbody>
</table>

<a id="rst-rs-232-emulation"></a>

### 4. RS-232 emulation

Currently 128 byte buffer is used:


<table>
<tbody>
<tr>
<td>


1st uint32_t

</td>
<td>


Data length (1--124)

</td>
</tr>
<tr>
<td>


Byte 4--127

</td>
<td>


Max 124 bytes of data

</td>
</tr>
</tbody>
</table>

<a id="rst-postq"></a>

### 5. PostQ

All SCSI Command must be sent through postQ:

> - **(inbound queue port)**
>
>   Request frame must be 32 bytes aligned:
>
>   > - **\#bit27--bit31**
>   >
>   >   flag for post ccb
>   >
>   > - **\#bit0--bit26**
>   >
>   >   real address (bit27--bit31) of post arcmsr_cdb
>   >
>   >
>   >   <table>
>   >   <tbody>
>   >   <tr>
>   >   <td>
>   >
>   >
>   >   bit31
>   >
>   >   </td>
>   >   <td>
>   >
>   >
>   >
>   >   <table>
>   >   <tbody>
>   >   <tr>
>   >   <td>
>   >
>   >
>   >   0
>   >
>   >   </td>
>   >   <td>
>   >
>   >
>   >   256 bytes frame
>   >
>   >   </td>
>   >   </tr>
>   >   <tr>
>   >   <td>
>   >
>   >
>   >   1
>   >
>   >   </td>
>   >   <td>
>   >
>   >
>   >   512 bytes frame
>   >
>   >   </td>
>   >   </tr>
>   >   </tbody>
>   >   </table>
>   >
>   >   </td>
>   >   </tr>
>   >   <tr>
>   >   <td>
>   >
>   >
>   >   bit30
>   >
>   >   </td>
>   >   <td>
>   >
>   >
>   >
>   >   <table>
>   >   <tbody>
>   >   <tr>
>   >   <td>
>   >
>   >
>   >   0
>   >
>   >   </td>
>   >   <td>
>   >
>   >
>   >   normal request
>   >
>   >   </td>
>   >   </tr>
>   >   <tr>
>   >   <td>
>   >
>   >
>   >   1
>   >
>   >   </td>
>   >   <td>
>   >
>   >
>   >   BIOS request
>   >
>   >   </td>
>   >   </tr>
>   >   </tbody>
>   >   </table>
>   >
>   >   </td>
>   >   </tr>
>   >   <tr>
>   >   <td>
>   >
>   >
>   >   bit29
>   >
>   >   </td>
>   >   <td>
>   >
>   >
>   >   reserved
>   >
>   >   </td>
>   >   </tr>
>   >   <tr>
>   >   <td>
>   >
>   >
>   >   bit28
>   >
>   >   </td>
>   >   <td>
>   >
>   >
>   >   reserved
>   >
>   >   </td>
>   >   </tr>
>   >   <tr>
>   >   <td>
>   >
>   >
>   >   bit27
>   >
>   >   </td>
>   >   <td>
>   >
>   >
>   >   reserved
>   >
>   >   </td>
>   >   </tr>
>   >   </tbody>
>   >   </table>
>
> - **(outbount queue port)**
>
>   Request reply:
>
>   > - **\#bit27--bit31**
>   >
>   >   flag for reply
>   >
>   > - **\#bit0--bit26**
>   >
>   >   real address (bit27--bit31) of reply arcmsr_cdb
>   >
>   >
>   >   <table>
>   >   <tbody>
>   >   <tr>
>   >   <td>
>   >
>   >
>   >   bit31
>   >
>   >   </td>
>   >   <td>
>   >
>   >
>   >   must be 0 (for this type of reply)
>   >
>   >   </td>
>   >   </tr>
>   >   <tr>
>   >   <td>
>   >
>   >
>   >   bit30
>   >
>   >   </td>
>   >   <td>
>   >
>   >
>   >   reserved for BIOS handshake
>   >
>   >   </td>
>   >   </tr>
>   >   <tr>
>   >   <td>
>   >
>   >
>   >   bit29
>   >
>   >   </td>
>   >   <td>
>   >
>   >
>   >   reserved
>   >
>   >   </td>
>   >   </tr>
>   >   <tr>
>   >   <td>
>   >
>   >
>   >   bit28
>   >
>   >   </td>
>   >   <td>
>   >
>   >
>   >
>   >   <table>
>   >   <tbody>
>   >   <tr>
>   >   <td>
>   >
>   >
>   >   0
>   >
>   >   </td>
>   >   <td>
>   >
>   >
>   >   no error, ignore AdapStatus/DevStatus/SenseData
>   >
>   >   </td>
>   >   </tr>
>   >   <tr>
>   >   <td>
>   >
>   >
>   >   1
>   >
>   >   </td>
>   >   <td>
>   >
>   >
>   >   Error, error code in AdapStatus/DevStatus/SenseData
>   >
>   >   </td>
>   >   </tr>
>   >   </tbody>
>   >   </table>
>   >
>   >   </td>
>   >   </tr>
>   >   <tr>
>   >   <td>
>   >
>   >
>   >   bit27
>   >
>   >   </td>
>   >   <td>
>   >
>   >
>   >   reserved
>   >
>   >   </td>
>   >   </tr>
>   >   </tbody>
>   >   </table>

<a id="rst-bios-request"></a>

### 6. BIOS request

All BIOS request is the same with request from PostQ

Except:

Request frame is sent from configuration space:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> offset: 0x78
>
> </td>
> <td>
>
>
> Request Frame (bit30 == 1)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> offset: 0x18
>
> </td>
> <td>
>
>
> writeonly to generate IRQ to IOP331
>
> </td>
> </tr>
> </tbody>
> </table>

Completion of request:



```text
(bit30 == 0, bit28==err flag)
```

<a id="rst-definition-of-sgl-entry-structure"></a>

### 7. Definition of SGL entry (structure)

<a id="rst-message1-out-diag-status-code"></a>

### 8. Message1 Out - Diag Status Code (????)

<a id="rst-message0-message-code"></a>

### 9. Message0 message code


<table>
<tbody>
<tr>
<td>


0x00

</td>
<td>


NOP

</td>
</tr>
<tr>
<td>


0x01

</td>
<td>


Get Config -&gt;offset 0xa00 :for outbound message code message_rwbuffer (IOP331 send to driver)


<table>
<tbody>
<tr>
<td>


Signature

</td>
<td>


0x87974060(4)

</td>
</tr>
<tr>
<td>


Request len

</td>
<td>


0x00000200(4)

</td>
</tr>
<tr>
<td>


numbers of queue

</td>
<td>


0x00000100(4)

</td>
</tr>
<tr>
<td>


SDRAM Size

</td>
<td>


0x00000100(4)--&gt;256 MB

</td>
</tr>
<tr>
<td>


IDE Channels

</td>
<td>


0x00000008(4)

</td>
</tr>
<tr>
<td>


vendor

</td>
<td>


40 bytes char

</td>
</tr>
<tr>
<td>


model

</td>
<td>


8 bytes char

</td>
</tr>
<tr>
<td>


FirmVer

</td>
<td>


16 bytes char

</td>
</tr>
<tr>
<td>


Device Map

</td>
<td>


16 bytes char

</td>
</tr>
<tr>
<td>


FirmwareVersion

</td>
<td>


DWORD

- Added for checking of new firmware capability

</td>
</tr>
</tbody>
</table>

</td>
</tr>
<tr>
<td>


0x02

</td>
<td>


Set Config -&gt;offset 0xa00 :for inbound message code message_rwbuffer (driver send to IOP331)


<table>
<tbody>
<tr>
<td>


Signature

</td>
<td>


0x87974063(4)

</td>
</tr>
<tr>
<td>


UPPER32 of Request Frame

</td>
<td>


(4)--&gt;Driver Only

</td>
</tr>
</tbody>
</table>

</td>
</tr>
<tr>
<td>


0x03

</td>
<td>


Reset (Abort all queued Command)

</td>
</tr>
<tr>
<td>


0x04

</td>
<td>


Stop Background Activity

</td>
</tr>
<tr>
<td>


0x05

</td>
<td>


Flush Cache

</td>
</tr>
<tr>
<td>


0x06

</td>
<td>


Start Background Activity (re-start if background is halted)

</td>
</tr>
<tr>
<td>


0x07

</td>
<td>


Check If Host Command Pending (Novell May Need This Function)

</td>
</tr>
<tr>
<td>


0x08

</td>
<td>


Set controller time -&gt;offset 0xa00   for inbound message code message_rwbuffer (driver to IOP331)


<table>
<tbody>
<tr>
<td>


byte 0

</td>
<td>


0xaa &lt;-- signature

</td>
</tr>
<tr>
<td>


byte 1

</td>
<td>


0x55 &lt;-- signature

</td>
</tr>
<tr>
<td>


byte 2

</td>
<td>


year (04)

</td>
</tr>
<tr>
<td>


byte 3

</td>
<td>


month (1..12)

</td>
</tr>
<tr>
<td>


byte 4

</td>
<td>


date (1..31)

</td>
</tr>
<tr>
<td>


byte 5

</td>
<td>


hour (0..23)

</td>
</tr>
<tr>
<td>


byte 6

</td>
<td>


minute (0..59)

</td>
</tr>
<tr>
<td>


byte 7

</td>
<td>


second (0..59)

</td>
</tr>
</tbody>
</table>

</td>
</tr>
</tbody>
</table>

<a id="rst-rs-232-interface-for-areca-raid-controller"></a>

## RS-232 Interface for Areca Raid Controller

> The low level command interface is exclusive with VT100 terminal

<a id="rst-sequence-of-command-execution"></a>

### 1. Sequence of command execution

> - **(A)** - **Header**
>
>     3 bytes sequence (0x5E, 0x01, 0x61)
>
> - **(B)** - **Command block**
>
>     variable length of data including length, command code, data and checksum byte
>
> - **(C)** - **Return data**
>
>     variable length of data

<a id="rst-command-block"></a>

### 2. Command block

> - **(A)** - **1st byte**
>
>     command block length (low byte)
>
> - **(B)** - **2nd byte**
>
>     command block length (high byte)
>
>     > [!NOTE]
>     >
>     > command block length shouldn't &gt; 2040 bytes, length excludes these two bytes
>
> - **(C)** - **3rd byte**
>
>     command code
>
> - **(D)** - **4th and following bytes**
>
>     variable length data bytes
>
>   depends on command code
>
> - **(E)** last byte checksum byte (sum of 1st byte until last data byte)

<a id="rst-command-code-and-associated-data"></a>

### 3. Command code and associated data

The following are command code defined in raid controller Command code 0x10--0x1? are used for system level management, no password checking is needed and should be implemented in separate well controlled utility and not for end user access. Command code 0x20--0x?? always check the password, password must be entered to enable these command:



```text
enum
{
        GUI_SET_SERIAL=0x10,
        GUI_SET_VENDOR,
        GUI_SET_MODEL,
        GUI_IDENTIFY,
        GUI_CHECK_PASSWORD,
        GUI_LOGOUT,
        GUI_HTTP,
        GUI_SET_ETHERNET_ADDR,
        GUI_SET_LOGO,
        GUI_POLL_EVENT,
        GUI_GET_EVENT,
        GUI_GET_HW_MONITOR,
        //    GUI_QUICK_CREATE=0x20, (function removed)
        GUI_GET_INFO_R=0x20,
        GUI_GET_INFO_V,
        GUI_GET_INFO_P,
        GUI_GET_INFO_S,
        GUI_CLEAR_EVENT,
        GUI_MUTE_BEEPER=0x30,
        GUI_BEEPER_SETTING,
        GUI_SET_PASSWORD,
        GUI_HOST_INTERFACE_MODE,
        GUI_REBUILD_PRIORITY,
        GUI_MAX_ATA_MODE,
        GUI_RESET_CONTROLLER,
        GUI_COM_PORT_SETTING,
        GUI_NO_OPERATION,
        GUI_DHCP_IP,
        GUI_CREATE_PASS_THROUGH=0x40,
        GUI_MODIFY_PASS_THROUGH,
        GUI_DELETE_PASS_THROUGH,
        GUI_IDENTIFY_DEVICE,
        GUI_CREATE_RAIDSET=0x50,
        GUI_DELETE_RAIDSET,
        GUI_EXPAND_RAIDSET,
        GUI_ACTIVATE_RAIDSET,
        GUI_CREATE_HOT_SPARE,
        GUI_DELETE_HOT_SPARE,
        GUI_CREATE_VOLUME=0x60,
        GUI_MODIFY_VOLUME,
        GUI_DELETE_VOLUME,
        GUI_START_CHECK_VOLUME,
        GUI_STOP_CHECK_VOLUME
};
```

<a id="rst-command-description"></a>

#### Command description

- **GUI_SET_SERIAL**

  Set the controller serial\#


  <table>
  <tbody>
  <tr>
  <td>


  byte 0,1

  </td>
  <td>


  length

  </td>
  </tr>
  <tr>
  <td>


  byte 2

  </td>
  <td>


  command code 0x10

  </td>
  </tr>
  <tr>
  <td>


  byte 3

  </td>
  <td>


  password length (should be 0x0f)

  </td>
  </tr>
  <tr>
  <td>


  byte 4-0x13

  </td>
  <td>


  should be "ArEcATecHnoLogY"

  </td>
  </tr>
  <tr>
  <td>


  byte 0x14--0x23

  </td>
  <td>


  Serial number string (must be 16 bytes)

  </td>
  </tr>
  </tbody>
  </table>

- **GUI_SET_VENDOR**

  Set vendor string for the controller


  <table>
  <tbody>
  <tr>
  <td>


  byte 0,1

  </td>
  <td>


  length

  </td>
  </tr>
  <tr>
  <td>


  byte 2

  </td>
  <td>


  command code 0x11

  </td>
  </tr>
  <tr>
  <td>


  byte 3

  </td>
  <td>


  password length (should be 0x08)

  </td>
  </tr>
  <tr>
  <td>


  byte 4-0x13

  </td>
  <td>


  should be "ArEcAvAr"

  </td>
  </tr>
  <tr>
  <td>


  byte 0x14--0x3B

  </td>
  <td>


  vendor string (must be 40 bytes)

  </td>
  </tr>
  </tbody>
  </table>

- **GUI_SET_MODEL**

  Set the model name of the controller


  <table>
  <tbody>
  <tr>
  <td>


  byte 0,1

  </td>
  <td>


  length

  </td>
  </tr>
  <tr>
  <td>


  byte 2

  </td>
  <td>


  command code 0x12

  </td>
  </tr>
  <tr>
  <td>


  byte 3

  </td>
  <td>


  password length (should be 0x08)

  </td>
  </tr>
  <tr>
  <td>


  byte 4-0x13

  </td>
  <td>


  should be "ArEcAvAr"

  </td>
  </tr>
  <tr>
  <td>


  byte 0x14--0x1B

  </td>
  <td>


  model string (must be 8 bytes)

  </td>
  </tr>
  </tbody>
  </table>

- **GUI_IDENTIFY**

  Identify device


  <table>
  <tbody>
  <tr>
  <td>


  byte 0,1

  </td>
  <td>


  length

  </td>
  </tr>
  <tr>
  <td>


  byte 2

  </td>
  <td>


  - **command code 0x13**

    return "Areca RAID Subsystem "

  </td>
  </tr>
  </tbody>
  </table>

- **GUI_CHECK_PASSWORD**

  Verify password


  <table>
  <tbody>
  <tr>
  <td>


  byte 0,1

  </td>
  <td>


  length

  </td>
  </tr>
  <tr>
  <td>


  byte 2

  </td>
  <td>


  command code 0x14

  </td>
  </tr>
  <tr>
  <td>


  byte 3

  </td>
  <td>


  password length

  </td>
  </tr>
  <tr>
  <td>


  byte 4-0x??

  </td>
  <td>


  user password to be checked

  </td>
  </tr>
  </tbody>
  </table>

- **GUI_LOGOUT**

  Logout GUI (force password checking on next command)


  <table>
  <tbody>
  <tr>
  <td>


  byte 0,1

  </td>
  <td>


  length

  </td>
  </tr>
  <tr>
  <td>


  byte 2

  </td>
  <td>


  command code 0x15

  </td>
  </tr>
  </tbody>
  </table>

- **GUI_HTTP**

  HTTP interface (reserved for Http proxy service)(0x16)

- **GUI_SET_ETHERNET_ADDR**

  Set the ethernet MAC address


  <table>
  <tbody>
  <tr>
  <td>


  byte 0,1

  </td>
  <td>


  length

  </td>
  </tr>
  <tr>
  <td>


  byte 2

  </td>
  <td>


  command code 0x17

  </td>
  </tr>
  <tr>
  <td>


  byte 3

  </td>
  <td>


  password length (should be 0x08)

  </td>
  </tr>
  <tr>
  <td>


  byte 4-0x13

  </td>
  <td>


  should be "ArEcAvAr"

  </td>
  </tr>
  <tr>
  <td>


  byte 0x14--0x19

  </td>
  <td>


  Ethernet MAC address (must be 6 bytes)

  </td>
  </tr>
  </tbody>
  </table>

- **GUI_SET_LOGO**

  Set logo in HTTP


  <table>
  <tbody>
  <tr>
  <td>


  byte 0,1

  </td>
  <td>


  length

  </td>
  </tr>
  <tr>
  <td>


  byte 2

  </td>
  <td>


  command code 0x18

  </td>
  </tr>
  <tr>
  <td>


  byte 3

  </td>
  <td>


  Page\# (0/1/2/3) (0xff --&gt; clear OEM logo)

  </td>
  </tr>
  <tr>
  <td>


  byte 4/5/6/7

  </td>
  <td>


  0x55/0xaa/0xa5/0x5a

  </td>
  </tr>
  <tr>
  <td>


  byte 8

  </td>
  <td>


  TITLE.JPG data (each page must be 2000 bytes)

  > [!NOTE]
  >
  > page0 1st 2 byte must be actual length of the JPG file

  </td>
  </tr>
  </tbody>
  </table>

- **GUI_POLL_EVENT**

  Poll If Event Log Changed


  <table>
  <tbody>
  <tr>
  <td>


  byte 0,1

  </td>
  <td>


  length

  </td>
  </tr>
  <tr>
  <td>


  byte 2

  </td>
  <td>


  command code 0x19

  </td>
  </tr>
  </tbody>
  </table>

- **GUI_GET_EVENT**

  Read Event


  <table>
  <tbody>
  <tr>
  <td>


  byte 0,1

  </td>
  <td>


  length

  </td>
  </tr>
  <tr>
  <td>


  byte 2

  </td>
  <td>


  command code 0x1a

  </td>
  </tr>
  <tr>
  <td>


  byte 3

  </td>
  <td>


  Event Page (0:1st page/1/2/3:last page)

  </td>
  </tr>
  </tbody>
  </table>

- **GUI_GET_HW_MONITOR**

  Get HW monitor data


  <table>
  <tbody>
  <tr>
  <td>


  byte 0,1

  </td>
  <td>


  length

  </td>
  </tr>
  <tr>
  <td>


  byte 2

  </td>
  <td>


  command code 0x1b

  </td>
  </tr>
  <tr>
  <td>


  byte 3

  </td>
  <td>


  \# of FANs(example 2)

  </td>
  </tr>
  <tr>
  <td>


  byte 4

  </td>
  <td>


  \# of Voltage sensor(example 3)

  </td>
  </tr>
  <tr>
  <td>


  byte 5

  </td>
  <td>


  \# of temperature sensor(example 2)

  </td>
  </tr>
  <tr>
  <td>


  byte 6

  </td>
  <td>


  \# of power

  </td>
  </tr>
  <tr>
  <td>


  byte 7/8

  </td>
  <td>


  Fan\#0 (RPM)

  </td>
  </tr>
  <tr>
  <td>


  byte 9/10

  </td>
  <td>


  Fan\#1

  </td>
  </tr>
  <tr>
  <td>


  byte 11/12

  </td>
  <td>


  Voltage\#0 original value in `*1000`

  </td>
  </tr>
  <tr>
  <td>


  byte 13/14

  </td>
  <td>


  Voltage\#0 value

  </td>
  </tr>
  <tr>
  <td>


  byte 15/16

  </td>
  <td>


  Voltage\#1 org

  </td>
  </tr>
  <tr>
  <td>


  byte 17/18

  </td>
  <td>


  Voltage\#1

  </td>
  </tr>
  <tr>
  <td>


  byte 19/20

  </td>
  <td>


  Voltage\#2 org

  </td>
  </tr>
  <tr>
  <td>


  byte 21/22

  </td>
  <td>


  Voltage\#2

  </td>
  </tr>
  <tr>
  <td>


  byte 23

  </td>
  <td>


  Temp\#0

  </td>
  </tr>
  <tr>
  <td>


  byte 24

  </td>
  <td>


  Temp\#1

  </td>
  </tr>
  <tr>
  <td>


  byte 25

  </td>
  <td>


  Power indicator (bit0   power\#0, bit1   power\#1)

  </td>
  </tr>
  <tr>
  <td>


  byte 26

  </td>
  <td>


  UPS indicator

  </td>
  </tr>
  </tbody>
  </table>

- **GUI_QUICK_CREATE**

  > Quick create raid/volume set
  >
  >
  > <table>
  > <tbody>
  > <tr>
  > <td>
  >
  >
  > byte 0,1
  >
  > </td>
  > <td>
  >
  >
  > length
  >
  > </td>
  > </tr>
  > <tr>
  > <td>
  >
  >
  > byte 2
  >
  > </td>
  > <td>
  >
  >
  > command code 0x20
  >
  > </td>
  > </tr>
  > <tr>
  > <td>
  >
  >
  > byte 3/4/5/6
  >
  > </td>
  > <td>
  >
  >
  > raw capacity
  >
  > </td>
  > </tr>
  > <tr>
  > <td>
  >
  >
  > byte 7
  >
  > </td>
  > <td>
  >
  >
  > raid level
  >
  > </td>
  > </tr>
  > <tr>
  > <td>
  >
  >
  > byte 8
  >
  > </td>
  > <td>
  >
  >
  > stripe size
  >
  > </td>
  > </tr>
  > <tr>
  > <td>
  >
  >
  > byte 9
  >
  > </td>
  > <td>
  >
  >
  > spare
  >
  > </td>
  > </tr>
  > <tr>
  > <td>
  >
  >
  > byte 10/11/12/13
  >
  > </td>
  > <td>
  >
  >
  > device mask (the devices to create raid/volume)
  >
  > </td>
  > </tr>
  > </tbody>
  > </table>

  This function is removed, application like to implement quick create function

  need to use GUI_CREATE_RAIDSET and GUI_CREATE_VOLUMESET function.

- **GUI_GET_INFO_R**

  Get Raid Set Information


  <table>
  <tbody>
  <tr>
  <td>


  byte 0,1

  </td>
  <td>


  length

  </td>
  </tr>
  <tr>
  <td>


  byte 2

  </td>
  <td>


  command code 0x20

  </td>
  </tr>
  <tr>
  <td>


  byte 3

  </td>
  <td>


  raidset\#

  </td>
  </tr>
  </tbody>
  </table>



  ```text
  typedef struct sGUI_RAIDSET
  {
          BYTE grsRaidSetName[16];
          DWORD grsCapacity;
          DWORD grsCapacityX;
          DWORD grsFailMask;
          BYTE grsDevArray[32];
          BYTE grsMemberDevices;
          BYTE grsNewMemberDevices;
          BYTE grsRaidState;
          BYTE grsVolumes;
          BYTE grsVolumeList[16];
          BYTE grsRes1;
          BYTE grsRes2;
          BYTE grsRes3;
          BYTE grsFreeSegments;
          DWORD grsRawStripes[8];
          DWORD grsRes4;
          DWORD grsRes5; //     Total to 128 bytes
          DWORD grsRes6; //     Total to 128 bytes
  } sGUI_RAIDSET, *pGUI_RAIDSET;
  ```

- **GUI_GET_INFO_V**

  Get Volume Set Information


  <table>
  <tbody>
  <tr>
  <td>


  byte 0,1

  </td>
  <td>


  length

  </td>
  </tr>
  <tr>
  <td>


  byte 2

  </td>
  <td>


  command code 0x21

  </td>
  </tr>
  <tr>
  <td>


  byte 3

  </td>
  <td>


  volumeset\#

  </td>
  </tr>
  </tbody>
  </table>



  ```text
  typedef struct sGUI_VOLUMESET
  {
          BYTE gvsVolumeName[16]; //     16
          DWORD gvsCapacity;
          DWORD gvsCapacityX;
          DWORD gvsFailMask;
          DWORD gvsStripeSize;
          DWORD gvsNewFailMask;
          DWORD gvsNewStripeSize;
          DWORD gvsVolumeStatus;
          DWORD gvsProgress; //     32
          sSCSI_ATTR gvsScsi;
          BYTE gvsMemberDisks;
          BYTE gvsRaidLevel; //     8
          BYTE gvsNewMemberDisks;
          BYTE gvsNewRaidLevel;
          BYTE gvsRaidSetNumber;
          BYTE gvsRes0; //     4
          BYTE gvsRes1[4]; //     64 bytes
  } sGUI_VOLUMESET, *pGUI_VOLUMESET;
  ```

- **GUI_GET_INFO_P**

  Get Physical Drive Information


  <table>
  <tbody>
  <tr>
  <td>


  byte 0,1

  </td>
  <td>


  length

  </td>
  </tr>
  <tr>
  <td>


  byte 2

  </td>
  <td>


  command code 0x22

  </td>
  </tr>
  <tr>
  <td>


  byte 3

  </td>
  <td>


  drive \# (from 0 to max-channels - 1)

  </td>
  </tr>
  </tbody>
  </table>



  ```text
  typedef struct sGUI_PHY_DRV
  {
          BYTE gpdModelName[40];
          BYTE gpdSerialNumber[20];
          BYTE gpdFirmRev[8];
          DWORD gpdCapacity;
          DWORD gpdCapacityX; //     Reserved for expansion
          BYTE gpdDeviceState;
          BYTE gpdPioMode;
          BYTE gpdCurrentUdmaMode;
          BYTE gpdUdmaMode;
          BYTE gpdDriveSelect;
          BYTE gpdRaidNumber; //     0xff if not belongs to a raid set
          sSCSI_ATTR gpdScsi;
          BYTE gpdReserved[40]; //     Total to 128 bytes
  } sGUI_PHY_DRV, *pGUI_PHY_DRV;
  ```

- **GUI_GET_INFO_S**

  Get System Information


  <table>
  <tbody>
  <tr>
  <td>


  byte 0,1

  </td>
  <td>


  length

  </td>
  </tr>
  <tr>
  <td>


  byte 2

  </td>
  <td>


  command code 0x23

  </td>
  </tr>
  </tbody>
  </table>



  ```text
  typedef struct sCOM_ATTR
  {
          BYTE comBaudRate;
          BYTE comDataBits;
          BYTE comStopBits;
          BYTE comParity;
          BYTE comFlowControl;
  } sCOM_ATTR, *pCOM_ATTR;
  typedef struct sSYSTEM_INFO
  {
          BYTE gsiVendorName[40];
          BYTE gsiSerialNumber[16];
          BYTE gsiFirmVersion[16];
          BYTE gsiBootVersion[16];
          BYTE gsiMbVersion[16];
          BYTE gsiModelName[8];
          BYTE gsiLocalIp[4];
          BYTE gsiCurrentIp[4];
          DWORD gsiTimeTick;
          DWORD gsiCpuSpeed;
          DWORD gsiICache;
          DWORD gsiDCache;
          DWORD gsiScache;
          DWORD gsiMemorySize;
          DWORD gsiMemorySpeed;
          DWORD gsiEvents;
          BYTE gsiMacAddress[6];
          BYTE gsiDhcp;
          BYTE gsiBeeper;
          BYTE gsiChannelUsage;
          BYTE gsiMaxAtaMode;
          BYTE gsiSdramEcc; //     1:if ECC enabled
          BYTE gsiRebuildPriority;
          sCOM_ATTR gsiComA; //     5 bytes
          sCOM_ATTR gsiComB; //     5 bytes
          BYTE gsiIdeChannels;
          BYTE gsiScsiHostChannels;
          BYTE gsiIdeHostChannels;
          BYTE gsiMaxVolumeSet;
          BYTE gsiMaxRaidSet;
          BYTE gsiEtherPort; //     1:if ether net port supported
          BYTE gsiRaid6Engine; //     1:Raid6 engine supported
          BYTE gsiRes[75];
  } sSYSTEM_INFO, *pSYSTEM_INFO;
  ```

- **GUI_CLEAR_EVENT**

  Clear System Event


  <table>
  <tbody>
  <tr>
  <td>


  byte 0,1

  </td>
  <td>


  length

  </td>
  </tr>
  <tr>
  <td>


  byte 2

  </td>
  <td>


  command code 0x24

  </td>
  </tr>
  </tbody>
  </table>

- **GUI_MUTE_BEEPER**

  Mute current beeper


  <table>
  <tbody>
  <tr>
  <td>


  byte 0,1

  </td>
  <td>


  length

  </td>
  </tr>
  <tr>
  <td>


  byte 2

  </td>
  <td>


  command code 0x30

  </td>
  </tr>
  </tbody>
  </table>

- **GUI_BEEPER_SETTING**

  Disable beeper


  <table>
  <tbody>
  <tr>
  <td>


  byte 0,1

  </td>
  <td>


  length

  </td>
  </tr>
  <tr>
  <td>


  byte 2

  </td>
  <td>


  command code 0x31

  </td>
  </tr>
  <tr>
  <td>


  byte 3

  </td>
  <td>


  0-&gt;disable, 1-&gt;enable

  </td>
  </tr>
  </tbody>
  </table>

- **GUI_SET_PASSWORD**

  Change password


  <table>
  <tbody>
  <tr>
  <td>


  byte 0,1

  </td>
  <td>


  length

  </td>
  </tr>
  <tr>
  <td>


  byte 2

  </td>
  <td>


  command code 0x32

  </td>
  </tr>
  <tr>
  <td>


  byte 3

  </td>
  <td>


  pass word length ( must &lt;= 15 )

  </td>
  </tr>
  <tr>
  <td>


  byte 4

  </td>
  <td>


  password (must be alpha-numerical)

  </td>
  </tr>
  </tbody>
  </table>

- **GUI_HOST_INTERFACE_MODE**

  Set host interface mode


  <table>
  <tbody>
  <tr>
  <td>


  byte 0,1

  </td>
  <td>


  length

  </td>
  </tr>
  <tr>
  <td>


  byte 2

  </td>
  <td>


  command code 0x33

  </td>
  </tr>
  <tr>
  <td>


  byte 3

  </td>
  <td>


  0-&gt;Independent, 1-&gt;cluster

  </td>
  </tr>
  </tbody>
  </table>

- **GUI_REBUILD_PRIORITY**

  Set rebuild priority


  <table>
  <tbody>
  <tr>
  <td>


  byte 0,1

  </td>
  <td>


  length

  </td>
  </tr>
  <tr>
  <td>


  byte 2

  </td>
  <td>


  command code 0x34

  </td>
  </tr>
  <tr>
  <td>


  byte 3

  </td>
  <td>


  0/1/2/3 (low-&gt;high)

  </td>
  </tr>
  </tbody>
  </table>

- **GUI_MAX_ATA_MODE**

  Set maximum ATA mode to be used


  <table>
  <tbody>
  <tr>
  <td>


  byte 0,1

  </td>
  <td>


  length

  </td>
  </tr>
  <tr>
  <td>


  byte 2

  </td>
  <td>


  command code 0x35

  </td>
  </tr>
  <tr>
  <td>


  byte 3

  </td>
  <td>


  0/1/2/3 (133/100/66/33)

  </td>
  </tr>
  </tbody>
  </table>

- **GUI_RESET_CONTROLLER**

  Reset Controller


  <table>
  <tbody>
  <tr>
  <td>


  byte 0,1

  </td>
  <td>


  length

  </td>
  </tr>
  <tr>
  <td>


  byte 2

  </td>
  <td>


  command code 0x36 \* Response with VT100 screen (discard it)

  </td>
  </tr>
  </tbody>
  </table>

- **GUI_COM_PORT_SETTING**

  COM port setting


  <table>
  <tbody>
  <tr>
  <td>


  byte 0,1

  </td>
  <td>


  length

  </td>
  </tr>
  <tr>
  <td>


  byte 2

  </td>
  <td>


  command code 0x37

  </td>
  </tr>
  <tr>
  <td>


  byte 3

  </td>
  <td>


  0-&gt;COMA (term port), 1-&gt;COMB (debug port)

  </td>
  </tr>
  <tr>
  <td>


  byte 4

  </td>
  <td>


  0/1/2/3/4/5/6/7 (1200/2400/4800/9600/19200/38400/57600/115200)

  </td>
  </tr>
  <tr>
  <td>


  byte 5

  </td>
  <td>


  data bit (0:7 bit, 1:8 bit   must be 8 bit)

  </td>
  </tr>
  <tr>
  <td>


  byte 6

  </td>
  <td>


  stop bit (0:1, 1:2 stop bits)

  </td>
  </tr>
  <tr>
  <td>


  byte 7

  </td>
  <td>


  parity (0:none, 1:off, 2:even)

  </td>
  </tr>
  <tr>
  <td>


  byte 8

  </td>
  <td>


  flow control (0:none, 1:xon/xoff, 2:hardware =&gt; must use none)

  </td>
  </tr>
  </tbody>
  </table>

- **GUI_NO_OPERATION**

  No operation


  <table>
  <tbody>
  <tr>
  <td>


  byte 0,1

  </td>
  <td>


  length

  </td>
  </tr>
  <tr>
  <td>


  byte 2

  </td>
  <td>


  command code 0x38

  </td>
  </tr>
  </tbody>
  </table>

- **GUI_DHCP_IP**

  Set DHCP option and local IP address


  <table>
  <tbody>
  <tr>
  <td>


  byte 0,1

  </td>
  <td>


  length

  </td>
  </tr>
  <tr>
  <td>


  byte 2

  </td>
  <td>


  command code 0x39

  </td>
  </tr>
  <tr>
  <td>


  byte 3

  </td>
  <td>


  0:dhcp disabled, 1:dhcp enabled

  </td>
  </tr>
  <tr>
  <td>


  byte 4/5/6/7

  </td>
  <td>


  IP address

  </td>
  </tr>
  </tbody>
  </table>

- **GUI_CREATE_PASS_THROUGH**

  Create pass through disk


  <table>
  <tbody>
  <tr>
  <td>


  byte 0,1

  </td>
  <td>


  length

  </td>
  </tr>
  <tr>
  <td>


  byte 2

  </td>
  <td>


  command code 0x40

  </td>
  </tr>
  <tr>
  <td>


  byte 3

  </td>
  <td>


  device \#

  </td>
  </tr>
  <tr>
  <td>


  byte 4

  </td>
  <td>


  scsi channel (0/1)

  </td>
  </tr>
  <tr>
  <td>


  byte 5

  </td>
  <td>


  scsi id (0--&gt;15)

  </td>
  </tr>
  <tr>
  <td>


  byte 6

  </td>
  <td>


  scsi lun (0--&gt;7)

  </td>
  </tr>
  <tr>
  <td>


  byte 7

  </td>
  <td>


  tagged queue (1   enabled)

  </td>
  </tr>
  <tr>
  <td>


  byte 8

  </td>
  <td>


  cache mode (1   enabled)

  </td>
  </tr>
  <tr>
  <td>


  byte 9

  </td>
  <td>


  max speed (0/1/2/3/4, async/20/40/80/160 for scsi) (0/1/2/3/4, 33/66/100/133/150 for ide  )

  </td>
  </tr>
  </tbody>
  </table>

- **GUI_MODIFY_PASS_THROUGH**

  Modify pass through disk


  <table>
  <tbody>
  <tr>
  <td>


  byte 0,1

  </td>
  <td>


  length

  </td>
  </tr>
  <tr>
  <td>


  byte 2

  </td>
  <td>


  command code 0x41

  </td>
  </tr>
  <tr>
  <td>


  byte 3

  </td>
  <td>


  device \#

  </td>
  </tr>
  <tr>
  <td>


  byte 4

  </td>
  <td>


  scsi channel (0/1)

  </td>
  </tr>
  <tr>
  <td>


  byte 5

  </td>
  <td>


  scsi id (0--&gt;15)

  </td>
  </tr>
  <tr>
  <td>


  byte 6

  </td>
  <td>


  scsi lun (0--&gt;7)

  </td>
  </tr>
  <tr>
  <td>


  byte 7

  </td>
  <td>


  tagged queue (1   enabled)

  </td>
  </tr>
  <tr>
  <td>


  byte 8

  </td>
  <td>


  cache mode (1   enabled)

  </td>
  </tr>
  <tr>
  <td>


  byte 9

  </td>
  <td>


  max speed (0/1/2/3/4, async/20/40/80/160 for scsi) (0/1/2/3/4, 33/66/100/133/150 for ide  )

  </td>
  </tr>
  </tbody>
  </table>

- **GUI_DELETE_PASS_THROUGH**

  Delete pass through disk


  <table>
  <tbody>
  <tr>
  <td>


  byte 0,1

  </td>
  <td>


  length

  </td>
  </tr>
  <tr>
  <td>


  byte 2

  </td>
  <td>


  command code 0x42

  </td>
  </tr>
  <tr>
  <td>


  byte 3

  </td>
  <td>


  device\# to be deleted

  </td>
  </tr>
  </tbody>
  </table>

- **GUI_IDENTIFY_DEVICE**

  Identify Device


  <table>
  <tbody>
  <tr>
  <td>


  byte 0,1

  </td>
  <td>


  length

  </td>
  </tr>
  <tr>
  <td>


  byte 2

  </td>
  <td>


  command code 0x43

  </td>
  </tr>
  <tr>
  <td>


  byte 3

  </td>
  <td>


  Flash Method (0:flash selected, 1:flash not selected)

  </td>
  </tr>
  <tr>
  <td>


  byte 4/5/6/7

  </td>
  <td>


  IDE device mask to be flashed .. Note:: no response data available

  </td>
  </tr>
  </tbody>
  </table>

- **GUI_CREATE_RAIDSET**

  Create Raid Set


  <table>
  <tbody>
  <tr>
  <td>


  byte 0,1

  </td>
  <td>


  length

  </td>
  </tr>
  <tr>
  <td>


  byte 2

  </td>
  <td>


  command code 0x50

  </td>
  </tr>
  <tr>
  <td>


  byte 3/4/5/6

  </td>
  <td>


  device mask

  </td>
  </tr>
  <tr>
  <td>


  byte 7-22

  </td>
  <td>


  raidset name (if byte 7 == 0:use default)

  </td>
  </tr>
  </tbody>
  </table>

- **GUI_DELETE_RAIDSET**

  Delete Raid Set


  <table>
  <tbody>
  <tr>
  <td>


  byte 0,1

  </td>
  <td>


  length

  </td>
  </tr>
  <tr>
  <td>


  byte 2

  </td>
  <td>


  command code 0x51

  </td>
  </tr>
  <tr>
  <td>


  byte 3

  </td>
  <td>


  raidset\#

  </td>
  </tr>
  </tbody>
  </table>

- **GUI_EXPAND_RAIDSET**

  Expand Raid Set


  <table>
  <tbody>
  <tr>
  <td>


  byte 0,1

  </td>
  <td>


  length

  </td>
  </tr>
  <tr>
  <td>


  byte 2

  </td>
  <td>


  command code 0x52

  </td>
  </tr>
  <tr>
  <td>


  byte 3

  </td>
  <td>


  raidset\#

  </td>
  </tr>
  <tr>
  <td>


  byte 4/5/6/7

  </td>
  <td>


  device mask for expansion

  </td>
  </tr>
  <tr>
  <td>


  byte 8/9/10

  </td>
  <td>


  (8:0 no change, 1 change, 0xff:terminate, 9:new raid level, 10:new stripe size 0/1/2/3/4/5-&gt;4/8/16/32/64/128K )

  </td>
  </tr>
  <tr>
  <td>


  byte 11/12/13

  </td>
  <td>


  repeat for each volume in the raidset

  </td>
  </tr>
  </tbody>
  </table>

- **GUI_ACTIVATE_RAIDSET**

  Activate incomplete raid set


  <table>
  <tbody>
  <tr>
  <td>


  byte 0,1

  </td>
  <td>


  length

  </td>
  </tr>
  <tr>
  <td>


  byte 2

  </td>
  <td>


  command code 0x53

  </td>
  </tr>
  <tr>
  <td>


  byte 3

  </td>
  <td>


  raidset\#

  </td>
  </tr>
  </tbody>
  </table>

- **GUI_CREATE_HOT_SPARE**

  Create hot spare disk


  <table>
  <tbody>
  <tr>
  <td>


  byte 0,1

  </td>
  <td>


  length

  </td>
  </tr>
  <tr>
  <td>


  byte 2

  </td>
  <td>


  command code 0x54

  </td>
  </tr>
  <tr>
  <td>


  byte 3/4/5/6

  </td>
  <td>


  device mask for hot spare creation

  </td>
  </tr>
  </tbody>
  </table>

- **GUI_DELETE_HOT_SPARE**

  Delete hot spare disk


  <table>
  <tbody>
  <tr>
  <td>


  byte 0,1

  </td>
  <td>


  length

  </td>
  </tr>
  <tr>
  <td>


  byte 2

  </td>
  <td>


  command code 0x55

  </td>
  </tr>
  <tr>
  <td>


  byte 3/4/5/6

  </td>
  <td>


  device mask for hot spare deletion

  </td>
  </tr>
  </tbody>
  </table>

- **GUI_CREATE_VOLUME**

  Create volume set


  <table>
  <tbody>
  <tr>
  <td>


  byte 0,1

  </td>
  <td>


  length

  </td>
  </tr>
  <tr>
  <td>


  byte 2

  </td>
  <td>


  command code 0x60

  </td>
  </tr>
  <tr>
  <td>


  byte 3

  </td>
  <td>


  raidset\#

  </td>
  </tr>
  <tr>
  <td>


  byte 4-19

  </td>
  <td>


  volume set name (if byte4 == 0, use default)

  </td>
  </tr>
  <tr>
  <td>


  byte 20-27

  </td>
  <td>


  volume capacity (blocks)

  </td>
  </tr>
  <tr>
  <td>


  byte 28

  </td>
  <td>


  raid level

  </td>
  </tr>
  <tr>
  <td>


  byte 29

  </td>
  <td>


  stripe size (0/1/2/3/4/5-&gt;4/8/16/32/64/128K)

  </td>
  </tr>
  <tr>
  <td>


  byte 30

  </td>
  <td>


  channel

  </td>
  </tr>
  <tr>
  <td>


  byte 31

  </td>
  <td>


  ID

  </td>
  </tr>
  <tr>
  <td>


  byte 32

  </td>
  <td>


  LUN

  </td>
  </tr>
  <tr>
  <td>


  byte 33

  </td>
  <td>


  1 enable tag

  </td>
  </tr>
  <tr>
  <td>


  byte 34

  </td>
  <td>


  1 enable cache

  </td>
  </tr>
  <tr>
  <td>


  byte 35

  </td>
  <td>


  speed (0/1/2/3/4-&gt;async/20/40/80/160 for scsi) (0/1/2/3/4-&gt;33/66/100/133/150 for IDE  )

  </td>
  </tr>
  <tr>
  <td>


  byte 36

  </td>
  <td>


  1 to select quick init

  </td>
  </tr>
  </tbody>
  </table>

- **GUI_MODIFY_VOLUME**

  Modify volume Set


  <table>
  <tbody>
  <tr>
  <td>


  byte 0,1

  </td>
  <td>


  length

  </td>
  </tr>
  <tr>
  <td>


  byte 2

  </td>
  <td>


  command code 0x61

  </td>
  </tr>
  <tr>
  <td>


  byte 3

  </td>
  <td>


  volumeset\#

  </td>
  </tr>
  <tr>
  <td>


  byte 4-19

  </td>
  <td>


  new volume set name (if byte4 == 0, not change)

  </td>
  </tr>
  <tr>
  <td>


  byte 20-27

  </td>
  <td>


  new volume capacity (reserved)

  </td>
  </tr>
  <tr>
  <td>


  byte 28

  </td>
  <td>


  new raid level

  </td>
  </tr>
  <tr>
  <td>


  byte 29

  </td>
  <td>


  new stripe size (0/1/2/3/4/5-&gt;4/8/16/32/64/128K)

  </td>
  </tr>
  <tr>
  <td>


  byte 30

  </td>
  <td>


  new channel

  </td>
  </tr>
  <tr>
  <td>


  byte 31

  </td>
  <td>


  new ID

  </td>
  </tr>
  <tr>
  <td>


  byte 32

  </td>
  <td>


  new LUN

  </td>
  </tr>
  <tr>
  <td>


  byte 33

  </td>
  <td>


  1 enable tag

  </td>
  </tr>
  <tr>
  <td>


  byte 34

  </td>
  <td>


  1 enable cache

  </td>
  </tr>
  <tr>
  <td>


  byte 35

  </td>
  <td>


  speed (0/1/2/3/4-&gt;async/20/40/80/160 for scsi) (0/1/2/3/4-&gt;33/66/100/133/150 for IDE  )

  </td>
  </tr>
  </tbody>
  </table>

- **GUI_DELETE_VOLUME**

  Delete volume set


  <table>
  <tbody>
  <tr>
  <td>


  byte 0,1

  </td>
  <td>


  length

  </td>
  </tr>
  <tr>
  <td>


  byte 2

  </td>
  <td>


  command code 0x62

  </td>
  </tr>
  <tr>
  <td>


  byte 3

  </td>
  <td>


  volumeset\#

  </td>
  </tr>
  </tbody>
  </table>

- **GUI_START_CHECK_VOLUME**

  Start volume consistency check


  <table>
  <tbody>
  <tr>
  <td>


  byte 0,1

  </td>
  <td>


  length

  </td>
  </tr>
  <tr>
  <td>


  byte 2

  </td>
  <td>


  command code 0x63

  </td>
  </tr>
  <tr>
  <td>


  byte 3

  </td>
  <td>


  volumeset\#

  </td>
  </tr>
  </tbody>
  </table>

- **GUI_STOP_CHECK_VOLUME**

  Stop volume consistency check


  <table>
  <tbody>
  <tr>
  <td>


  byte 0,1

  </td>
  <td>


  length

  </td>
  </tr>
  <tr>
  <td>


  byte 2

  </td>
  <td>


  command code 0x64

  </td>
  </tr>
  </tbody>
  </table>

<a id="rst-returned-data"></a>

### 4. Returned data

- **(A)** Header 3 bytes sequence (0x5E, 0x01, 0x61)

- **(B)** Length 2 bytes (low byte 1st, excludes length and checksum byte)

- **(C)** status or data:

  > 1. If length == 1 ==&gt; 1 byte status code:
  >
  >
  >
  >    ```text
  >    #define GUI_OK                    0x41
  >    #define GUI_RAIDSET_NOT_NORMAL    0x42
  >    #define GUI_VOLUMESET_NOT_NORMAL  0x43
  >    #define GUI_NO_RAIDSET            0x44
  >    #define GUI_NO_VOLUMESET          0x45
  >    #define GUI_NO_PHYSICAL_DRIVE     0x46
  >    #define GUI_PARAMETER_ERROR       0x47
  >    #define GUI_UNSUPPORTED_COMMAND   0x48
  >    #define GUI_DISK_CONFIG_CHANGED   0x49
  >    #define GUI_INVALID_PASSWORD      0x4a
  >    #define GUI_NO_DISK_SPACE         0x4b
  >    #define GUI_CHECKSUM_ERROR        0x4c
  >    #define GUI_PASSWORD_REQUIRED     0x4d
  >    ```
  >
  > 2. If length &gt; 1:
  >
  >    > data block returned from controller and the contents depends on the command code

- **(E)** Checksum checksum of length and status or data byte
