---
title: "Gadget Testing"
type: reference
description: "This file summarizes information on basic testing of USB functions provided by gadgets."
---

<a id="rst-gadget-testing"></a>

This file summarizes information on basic testing of USB functions provided by gadgets.

<!-- contents

1. ACM function
2. ECM function
3. ECM subset function
4. EEM function
5. FFS function
6. HID function
7. LOOPBACK function
8. MASS STORAGE function
9. MIDI function
10. NCM function
11. OBEX function
12. PHONET function
13. RNDIS function
14. SERIAL function
15. SOURCESINK function
16. UAC1 function (legacy implementation)
17. UAC2 function
18. UVC function
19. PRINTER function
20. UAC1 function (new API)
21. MIDI2 function -->

<a id="rst-acm-function"></a>

## 1. ACM function

The function is provided by usb_f_acm.ko module.

<a id="rst-function-specific-configfs-interface"></a>

### Function-specific configfs interface

The function name to use when creating the function directory is "acm". The ACM function provides just one attribute in its function directory:

> port_num

The attribute is read-only.

There can be at most 4 ACM/generic serial/OBEX ports in the system.

<a id="rst-testing-the-acm-function"></a>

### Testing the ACM function

On the host:



```text
cat > /dev/ttyACM<X>
```

On the device:



```text
cat /dev/ttyGS<Y>
```

then the other way round

On the device:



```text
cat > /dev/ttyGS<Y>
```

On the host:



```text
cat /dev/ttyACM<X>
```

<a id="rst-ecm-function"></a>

## 2. ECM function

The function is provided by usb_f_ecm.ko module.

<a id="rst-function-specific-configfs-interface-1"></a>

### Function-specific configfs interface

The function name to use when creating the function directory is "ecm". The ECM function provides these attributes in its function directory:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> ifname
>
> </td>
> <td>
>
>
> network device interface name associated with this function instance
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> qmult
>
> </td>
> <td>
>
>
> queue length multiplier for high and super speed
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> host_addr
>
> </td>
> <td>
>
>
> MAC address of host's end of this Ethernet over USB link
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> dev_addr
>
> </td>
> <td>
>
>
> MAC address of device's end of this Ethernet over USB link
>
> </td>
> </tr>
> </tbody>
> </table>

and after creating the functions/ecm.&lt;instance name&gt; they contain default values: qmult is 5, dev_addr and host_addr are randomly selected. The ifname can be written to if the function is not bound. A write must be an interface pattern such as "usb%d", which will cause the net core to choose the next free usbX interface. By default, it is set to "usb%d".

<a id="rst-testing-the-ecm-function"></a>

### Testing the ECM function

Configure IP addresses of the device and the host. Then:

On the device:



```text
ping <host's IP>
```

On the host:



```text
ping <device's IP>
```

<a id="rst-ecm-subset-function"></a>

## 3. ECM subset function

The function is provided by usb_f_ecm_subset.ko module.

<a id="rst-function-specific-configfs-interface-2"></a>

### Function-specific configfs interface

The function name to use when creating the function directory is "geth". The ECM subset function provides these attributes in its function directory:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> ifname
>
> </td>
> <td>
>
>
> network device interface name associated with this function instance
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> qmult
>
> </td>
> <td>
>
>
> queue length multiplier for high and super speed
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> host_addr
>
> </td>
> <td>
>
>
> MAC address of host's end of this Ethernet over USB link
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> dev_addr
>
> </td>
> <td>
>
>
> MAC address of device's end of this Ethernet over USB link
>
> </td>
> </tr>
> </tbody>
> </table>

and after creating the functions/ecm.&lt;instance name&gt; they contain default values: qmult is 5, dev_addr and host_addr are randomly selected. The ifname can be written to if the function is not bound. A write must be an interface pattern such as "usb%d", which will cause the net core to choose the next free usbX interface. By default, it is set to "usb%d".

<a id="rst-testing-the-ecm-subset-function"></a>

### Testing the ECM subset function

Configure IP addresses of the device and the host. Then:

On the device:



```text
ping <host's IP>
```

On the host:



```text
ping <device's IP>
```

<a id="rst-eem-function"></a>

## 4. EEM function

The function is provided by usb_f_eem.ko module.

<a id="rst-function-specific-configfs-interface-3"></a>

### Function-specific configfs interface

The function name to use when creating the function directory is "eem". The EEM function provides these attributes in its function directory:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> ifname
>
> </td>
> <td>
>
>
> network device interface name associated with this function instance
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> qmult
>
> </td>
> <td>
>
>
> queue length multiplier for high and super speed
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> host_addr
>
> </td>
> <td>
>
>
> MAC address of host's end of this Ethernet over USB link
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> dev_addr
>
> </td>
> <td>
>
>
> MAC address of device's end of this Ethernet over USB link
>
> </td>
> </tr>
> </tbody>
> </table>

and after creating the functions/eem.&lt;instance name&gt; they contain default values: qmult is 5, dev_addr and host_addr are randomly selected. The ifname can be written to if the function is not bound. A write must be an interface pattern such as "usb%d", which will cause the net core to choose the next free usbX interface. By default, it is set to "usb%d".

<a id="rst-testing-the-eem-function"></a>

### Testing the EEM function

Configure IP addresses of the device and the host. Then:

On the device:



```text
ping <host's IP>
```

On the host:



```text
ping <device's IP>
```

<a id="rst-ffs-function"></a>

## 5. FFS function

The function is provided by usb_f_fs.ko module.

<a id="rst-function-specific-configfs-interface-4"></a>

### Function-specific configfs interface

The function name to use when creating the function directory is "ffs". The function directory is intentionally empty and not modifiable.

After creating the directory there is a new instance (a "device") of FunctionFS available in the system. Once a "device" is available, the user should follow the standard procedure for using FunctionFS (mount it, run the userspace process which implements the function proper). The gadget should be enabled by writing a suitable string to usb_gadget/&lt;gadget&gt;/UDC.

The FFS function provides just one attribute in its function directory:

> ready

The attribute is read-only and signals if the function is ready (1) to be used, E.G. if userspace has written descriptors and strings to ep0, so the gadget can be enabled.

<a id="rst-testing-the-ffs-function"></a>

### Testing the FFS function

On the device: start the function's userspace daemon, enable the gadget

On the host: use the USB function provided by the device

<a id="rst-hid-function"></a>

## 6. HID function

The function is provided by usb_f_hid.ko module.

<a id="rst-function-specific-configfs-interface-5"></a>

### Function-specific configfs interface

The function name to use when creating the function directory is "hid". The HID function provides these attributes in its function directory:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> protocol
>
> </td>
> <td>
>
>
> HID protocol to use
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> report_desc
>
> </td>
> <td>
>
>
> data to be used in HID reports, except data passed with /dev/hidg&lt;X&gt;
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> report_length
>
> </td>
> <td>
>
>
> HID report length
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> subclass
>
> </td>
> <td>
>
>
> HID subclass to use
>
> </td>
> </tr>
> </tbody>
> </table>

For a keyboard the protocol and the subclass are 1, the report_length is 8, while the report_desc is:



```text
$ hd my_report_desc
00000000  05 01 09 06 a1 01 05 07  19 e0 29 e7 15 00 25 01  |..........)...%.|
00000010  75 01 95 08 81 02 95 01  75 08 81 03 95 05 75 01  |u.......u.....u.|
00000020  05 08 19 01 29 05 91 02  95 01 75 03 91 03 95 06  |....).....u.....|
00000030  75 08 15 00 25 65 05 07  19 00 29 65 81 00 c0     |u...%e....)e...|
0000003f
```

Such a sequence of bytes can be stored to the attribute with echo:



```text
$ echo -ne \\x05\\x01\\x09\\x06\\xa1.....
```

<a id="rst-testing-the-hid-function"></a>

### Testing the HID function

Device:

- create the gadget

- connect the gadget to a host, preferably not the one used to control the gadget

- run a program which writes to /dev/hidg&lt;N&gt;, e.g. a userspace program found in [Documentation/usb/gadget_hid.rst](~kernel/hardware/usb/gadget-hid):



  ```text
  $ ./hid_gadget_test /dev/hidg0 keyboard
  ```

Host:

- observe the keystrokes from the gadget

<a id="rst-loopback-function"></a>

## 7. LOOPBACK function

The function is provided by usb_f_ss_lb.ko module.

<a id="rst-function-specific-configfs-interface-6"></a>

### Function-specific configfs interface

The function name to use when creating the function directory is "Loopback". The LOOPBACK function provides these attributes in its function directory:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> qlen
>
> </td>
> <td>
>
>
> depth of loopback queue
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> bulk_buflen
>
> </td>
> <td>
>
>
> buffer length
>
> </td>
> </tr>
> </tbody>
> </table>

<a id="rst-testing-the-loopback-function"></a>

### Testing the LOOPBACK function

device: run the gadget

host: test-usb (tools/usb/testusb.c)

<a id="rst-mass-storage-function"></a>

## 8. MASS STORAGE function

The function is provided by usb_f_mass_storage.ko module.

<a id="rst-function-specific-configfs-interface-7"></a>

### Function-specific configfs interface

The function name to use when creating the function directory is "mass_storage". The MASS STORAGE function provides these attributes in its directory: files:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> stall
>
> </td>
> <td>
>
>
> Set to permit function to halt bulk endpoints. Disabled on some USB devices known not to work correctly. You should set it to true.
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> num_buffers
>
> </td>
> <td>
>
>
> Number of pipeline buffers. Valid numbers are 2..4. Available only if CONFIG_USB_GADGET_DEBUG_FILES is set.
>
> </td>
> </tr>
> </tbody>
> </table>

and a default lun.0 directory corresponding to SCSI LUN \#0.

A new lun can be added with mkdir:



```text
$ mkdir functions/mass_storage.0/partition.5
```

Lun numbering does not have to be continuous, except for lun \#0 which is created by default. A maximum of 8 luns can be specified and they all must be named following the &lt;name&gt;.&lt;number&gt; scheme. The numbers can be 0..8. Probably a good convention is to name the luns "lun.&lt;number&gt;", although it is not mandatory.

In each lun directory there are the following attribute files:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> file
>
> </td>
> <td>
>
>
> The path to the backing file for the LUN. Required if LUN is not marked as removable.
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> ro
>
> </td>
> <td>
>
>
> Flag specifying access to the LUN shall be read-only. This is implied if CD-ROM emulation is enabled as well as when it was impossible to open "filename" in R/W mode.
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> removable
>
> </td>
> <td>
>
>
> Flag specifying that LUN shall be indicated as being removable.
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> cdrom
>
> </td>
> <td>
>
>
> Flag specifying that LUN shall be reported as being a CD-ROM.
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> nofua
>
> </td>
> <td>
>
>
> Flag specifying that FUA flag in SCSI WRITE(10,12)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> forced_eject
>
> </td>
> <td>
>
>
> This write-only file is useful only when the function is active. It causes the backing file to be forcibly detached from the LUN, regardless of whether the host has allowed it. Any non-zero number of bytes written will result in ejection.
>
> </td>
> </tr>
> </tbody>
> </table>

<a id="rst-testing-the-mass-storage-function"></a>

### Testing the MASS STORAGE function

device: connect the gadget, enable it host: dmesg, see the USB drives appear (if system configured to automatically mount)

<a id="rst-midi-function"></a>

## 9. MIDI function

The function is provided by usb_f_midi.ko module.

<a id="rst-function-specific-configfs-interface-8"></a>

### Function-specific configfs interface

The function name to use when creating the function directory is "midi". The MIDI function provides these attributes in its function directory:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> buflen
>
> </td>
> <td>
>
>
> MIDI buffer length
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> id
>
> </td>
> <td>
>
>
> ID string for the USB MIDI adapter
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> in_ports
>
> </td>
> <td>
>
>
> number of MIDI input ports
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> index
>
> </td>
> <td>
>
>
> index value for the USB MIDI adapter
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> out_ports
>
> </td>
> <td>
>
>
> number of MIDI output ports
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> qlen
>
> </td>
> <td>
>
>
> USB read request queue length
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> interface_string
>
> </td>
> <td>
>
>
> USB AudioControl interface string
>
> </td>
> </tr>
> </tbody>
> </table>

<a id="rst-testing-the-midi-function"></a>

### Testing the MIDI function

There are two cases: playing a mid from the gadget to the host and playing a mid from the host to the gadget.

1. Playing a mid from the gadget to the host:

host:



```text
$ arecordmidi -l
 Port    Client name                      Port name
 14:0    Midi Through                     Midi Through Port-0
 24:0    MIDI Gadget                      MIDI Gadget MIDI 1
$ arecordmidi -p 24:0 from_gadget.mid
```

gadget:



```text
$ aplaymidi -l
 Port    Client name                      Port name
 20:0    f_midi                           f_midi

$ aplaymidi -p 20:0 to_host.mid
```

2. Playing a mid from the host to the gadget

gadget:



```text
$ arecordmidi -l
 Port    Client name                      Port name
 20:0    f_midi                           f_midi

$ arecordmidi -p 20:0 from_host.mid
```

host:



```text
$ aplaymidi -l
 Port    Client name                      Port name
 14:0    Midi Through                     Midi Through Port-0
 24:0    MIDI Gadget                      MIDI Gadget MIDI 1

$ aplaymidi -p24:0 to_gadget.mid
```

The from_gadget.mid should sound identical to the to_host.mid.

The from_host.id should sound identical to the to_gadget.mid.

MIDI files can be played to speakers/headphones with e.g. timidity installed:



```text
$ aplaymidi -l
 Port    Client name                      Port name
 14:0    Midi Through                     Midi Through Port-0
 24:0    MIDI Gadget                      MIDI Gadget MIDI 1
128:0    TiMidity                         TiMidity port 0
128:1    TiMidity                         TiMidity port 1
128:2    TiMidity                         TiMidity port 2
128:3    TiMidity                         TiMidity port 3

$ aplaymidi -p 128:0 file.mid
```

MIDI ports can be logically connected using the aconnect utility, e.g.:



```text
$ aconnect 24:0 128:0 # try it on the host
```

After the gadget's MIDI port is connected to timidity's MIDI port, whatever is played at the gadget side with aplaymidi -l is audible in host's speakers/headphones.

<a id="rst-ncm-function"></a>

## 10. NCM function

The function is provided by usb_f_ncm.ko module.

<a id="rst-function-specific-configfs-interface-9"></a>

### Function-specific configfs interface

The function name to use when creating the function directory is "ncm". The NCM function provides these attributes in its function directory:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> ifname
>
> </td>
> <td>
>
>
> network device interface name associated with this function instance
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> qmult
>
> </td>
> <td>
>
>
> queue length multiplier for high and super speed
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> host_addr
>
> </td>
> <td>
>
>
> MAC address of host's end of this Ethernet over USB link
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> dev_addr
>
> </td>
> <td>
>
>
> MAC address of device's end of this Ethernet over USB link
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> max_segment_size
>
> </td>
> <td>
>
>
> Segment size required for P2P connections. This will set MTU to 14 bytes
>
> </td>
> </tr>
> </tbody>
> </table>

and after creating the functions/ncm.&lt;instance name&gt; they contain default values: qmult is 5, dev_addr and host_addr are randomly selected. The ifname can be written to if the function is not bound. A write must be an interface pattern such as "usb%d", which will cause the net core to choose the next free usbX interface. By default, it is set to "usb%d".

<a id="rst-testing-the-ncm-function"></a>

### Testing the NCM function

Configure IP addresses of the device and the host. Then:

On the device:



```text
ping <host's IP>
```

On the host:



```text
ping <device's IP>
```

<a id="rst-obex-function"></a>

## 11. OBEX function

The function is provided by usb_f_obex.ko module.

<a id="rst-function-specific-configfs-interface-10"></a>

### Function-specific configfs interface

The function name to use when creating the function directory is "obex". The OBEX function provides just one attribute in its function directory:

> port_num

The attribute is read-only.

There can be at most 4 ACM/generic serial/OBEX ports in the system.

<a id="rst-testing-the-obex-function"></a>

### Testing the OBEX function

On device:



```text
seriald -f /dev/ttyGS<Y> -s 1024
```

On host:



```text
serialc -v <vendorID> -p <productID> -i<interface#> -a1 -s1024 \
        -t<out endpoint addr> -r<in endpoint addr>
```

where seriald and serialc are Felipe's utilities found here:

> [https://github.com/felipebalbi/usb-tools.git](<https://github.com/felipebalbi/usb-tools.git>) master

<a id="rst-phonet-function"></a>

## 12. PHONET function

The function is provided by usb_f_phonet.ko module.

<a id="rst-function-specific-configfs-interface-11"></a>

### Function-specific configfs interface

The function name to use when creating the function directory is "phonet". The PHONET function provides just one attribute in its function directory:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> ifname
>
> </td>
> <td>
>
>
> network device interface name associated with this function instance
>
> </td>
> </tr>
> </tbody>
> </table>

<a id="rst-testing-the-phonet-function"></a>

### Testing the PHONET function

It is not possible to test the SOCK_STREAM protocol without a specific piece of hardware, so only SOCK_DGRAM has been tested. For the latter to work, in the past I had to apply the patch mentioned here:

[http://www.spinics.net/lists/linux-usb/msg85689.html](<http://www.spinics.net/lists/linux-usb/msg85689.html>)

These tools are required:

git://git.gitorious.org/meego-cellular/phonet-utils.git

On the host:



```text
$ ./phonet -a 0x10 -i usbpn0
$ ./pnroute add 0x6c usbpn0
$./pnroute add 0x10 usbpn0
$ ifconfig usbpn0 up
```

On the device:



```text
$ ./phonet -a 0x6c -i upnlink0
$ ./pnroute add 0x10 upnlink0
$ ifconfig upnlink0 up
```

Then a test program can be used:



```text
http://www.spinics.net/lists/linux-usb/msg85690.html
```

On the device:



```text
$ ./pnxmit -a 0x6c -r
```

On the host:



```text
$ ./pnxmit -a 0x10 -s 0x6c
```

As a result some data should be sent from host to device. Then the other way round:

On the host:



```text
$ ./pnxmit -a 0x10 -r
```

On the device:



```text
$ ./pnxmit -a 0x6c -s 0x10
```

<a id="rst-rndis-function"></a>

## 13. RNDIS function

The function is provided by usb_f_rndis.ko module.

<a id="rst-function-specific-configfs-interface-12"></a>

### Function-specific configfs interface

The function name to use when creating the function directory is "rndis". The RNDIS function provides these attributes in its function directory:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> ifname
>
> </td>
> <td>
>
>
> network device interface name associated with this function instance
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> qmult
>
> </td>
> <td>
>
>
> queue length multiplier for high and super speed
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> host_addr
>
> </td>
> <td>
>
>
> MAC address of host's end of this Ethernet over USB link
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> dev_addr
>
> </td>
> <td>
>
>
> MAC address of device's end of this Ethernet over USB link
>
> </td>
> </tr>
> </tbody>
> </table>

and after creating the functions/rndis.&lt;instance name&gt; they contain default values: qmult is 5, dev_addr and host_addr are randomly selected. The ifname can be written to if the function is not bound. A write must be an interface pattern such as "usb%d", which will cause the net core to choose the next free usbX interface. By default, it is set to "usb%d".

<a id="rst-testing-the-rndis-function"></a>

### Testing the RNDIS function

Configure IP addresses of the device and the host. Then:

On the device:



```text
ping <host's IP>
```

On the host:



```text
ping <device's IP>
```

<a id="rst-serial-function"></a>

## 14. SERIAL function

The function is provided by usb_f_gser.ko module.

<a id="rst-function-specific-configfs-interface-13"></a>

### Function-specific configfs interface

The function name to use when creating the function directory is "gser". The SERIAL function provides just one attribute in its function directory:

> port_num

The attribute is read-only.

There can be at most 4 ACM/generic serial/OBEX ports in the system.

<a id="rst-testing-the-serial-function"></a>

### Testing the SERIAL function

On host:



```text
insmod usbserial
echo VID PID >/sys/bus/usb-serial/drivers/generic/new_id
```

On host:



```text
cat > /dev/ttyUSB<X>
```

On target:



```text
cat /dev/ttyGS<Y>
```

then the other way round

On target:



```text
cat > /dev/ttyGS<Y>
```

On host:



```text
cat /dev/ttyUSB<X>
```

<a id="rst-sourcesink-function"></a>

## 15. SOURCESINK function

The function is provided by usb_f_ss_lb.ko module.

<a id="rst-function-specific-configfs-interface-14"></a>

### Function-specific configfs interface

The function name to use when creating the function directory is "SourceSink". The SOURCESINK function provides these attributes in its function directory:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> pattern
>
> </td>
> <td>
>
>
> 0 (all zeros), 1 (mod63), 2 (none)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> isoc_interval
>
> </td>
> <td>
>
>
> 1..16
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> isoc_maxpacket
>
> </td>
> <td>
>
>
> 0 - 1023 (fs), 0 - 1024 (hs/ss)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> isoc_mult
>
> </td>
> <td>
>
>
> 0..2 (hs/ss only)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> isoc_maxburst
>
> </td>
> <td>
>
>
> 0..15 (ss only)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> bulk_buflen
>
> </td>
> <td>
>
>
> buffer length
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> bulk_maxburst
>
> </td>
> <td>
>
>
> 0..15 (ss only)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> bulk_qlen
>
> </td>
> <td>
>
>
> depth of queue for bulk
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> iso_qlen
>
> </td>
> <td>
>
>
> depth of queue for iso
>
> </td>
> </tr>
> </tbody>
> </table>

<a id="rst-testing-the-sourcesink-function"></a>

### Testing the SOURCESINK function

device: run the gadget

host: test-usb (tools/usb/testusb.c)

<a id="rst-uac1-function-legacy-implementation"></a>

## 16. UAC1 function (legacy implementation)

The function is provided by usb_f_uac1_legacy.ko module.

<a id="rst-function-specific-configfs-interface-15"></a>

### Function-specific configfs interface

The function name to use when creating the function directory is "uac1_legacy". The uac1 function provides these attributes in its function directory:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> audio_buf_size
>
> </td>
> <td>
>
>
> audio buffer size
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> fn_cap
>
> </td>
> <td>
>
>
> capture pcm device file name
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> fn_cntl
>
> </td>
> <td>
>
>
> control device file name
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> fn_play
>
> </td>
> <td>
>
>
> playback pcm device file name
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> req_buf_size
>
> </td>
> <td>
>
>
> ISO OUT endpoint request buffer size
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> req_count
>
> </td>
> <td>
>
>
> ISO OUT endpoint request count
>
> </td>
> </tr>
> </tbody>
> </table>

The attributes have sane default values.

<a id="rst-testing-the-uac1-function"></a>

### Testing the UAC1 function

device: run the gadget

host:



```text
aplay -l # should list our USB Audio Gadget
```

<a id="rst-uac2-function"></a>

## 17. UAC2 function

The function is provided by usb_f_uac2.ko module.

<a id="rst-function-specific-configfs-interface-16"></a>

### Function-specific configfs interface

The function name to use when creating the function directory is "uac2". The uac2 function provides these attributes in its function directory:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> c_chmask
>
> </td>
> <td>
>
>
> capture channel mask
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> c_srate
>
> </td>
> <td>
>
>
> list of capture sampling rates (comma-separated)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> c_ssize
>
> </td>
> <td>
>
>
> capture sample size (bytes)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> c_sync
>
> </td>
> <td>
>
>
> capture synchronization type (async/adaptive)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> c_mute_present
>
> </td>
> <td>
>
>
> capture mute control enable
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> c_volume_present
>
> </td>
> <td>
>
>
> capture volume control enable
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> c_volume_min
>
> </td>
> <td>
>
>
> capture volume control min value (in 1/256 dB)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> c_volume_max
>
> </td>
> <td>
>
>
> capture volume control max value (in 1/256 dB)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> c_volume_res
>
> </td>
> <td>
>
>
> capture volume control resolution (in 1/256 dB)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> c_hs_bint
>
> </td>
> <td>
>
>
> capture bInterval for HS/SS (1-4: fixed, 0: auto)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> fb_max
>
> </td>
> <td>
>
>
> maximum extra bandwidth in async mode
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> p_chmask
>
> </td>
> <td>
>
>
> playback channel mask
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> p_srate
>
> </td>
> <td>
>
>
> list of playback sampling rates (comma-separated)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> p_ssize
>
> </td>
> <td>
>
>
> playback sample size (bytes)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> p_mute_present
>
> </td>
> <td>
>
>
> playback mute control enable
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> p_volume_present
>
> </td>
> <td>
>
>
> playback volume control enable
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> p_volume_min
>
> </td>
> <td>
>
>
> playback volume control min value (in 1/256 dB)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> p_volume_max
>
> </td>
> <td>
>
>
> playback volume control max value (in 1/256 dB)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> p_volume_res
>
> </td>
> <td>
>
>
> playback volume control resolution (in 1/256 dB)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> p_hs_bint
>
> </td>
> <td>
>
>
> playback bInterval for HS/SS (1-4: fixed, 0: auto)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> req_number
>
> </td>
> <td>
>
>
> the number of pre-allocated request for both capture and playback
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> function_name
>
> </td>
> <td>
>
>
> name of the interface
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> if_ctrl_name
>
> </td>
> <td>
>
>
> topology control name
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> clksrc_in_name
>
> </td>
> <td>
>
>
> input clock name
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> clksrc_out_name
>
> </td>
> <td>
>
>
> output clock name
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> p_it_name
>
> </td>
> <td>
>
>
> playback input terminal name
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> p_it_ch_name
>
> </td>
> <td>
>
>
> playback input first channel name
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> p_ot_name
>
> </td>
> <td>
>
>
> playback output terminal name
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> p_fu_vol_name
>
> </td>
> <td>
>
>
> playback function unit name
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> c_it_name
>
> </td>
> <td>
>
>
> capture input terminal name
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> c_it_ch_name
>
> </td>
> <td>
>
>
> capture input first channel name
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> c_ot_name
>
> </td>
> <td>
>
>
> capture output terminal name
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> c_fu_vol_name
>
> </td>
> <td>
>
>
> capture functional unit name
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> c_terminal_type
>
> </td>
> <td>
>
>
> code of the capture terminal type
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> p_terminal_type
>
> </td>
> <td>
>
>
> code of the playback terminal type
>
> </td>
> </tr>
> </tbody>
> </table>

The attributes have sane default values.

<a id="rst-testing-the-uac2-function"></a>

### Testing the UAC2 function

device: run the gadget host: aplay -l \# should list our USB Audio Gadget

This function does not require real hardware support, it just sends a stream of audio data to/from the host. In order to actually hear something at the device side, a command similar to this must be used at the device side:



```text
$ arecord -f dat -t wav -D hw:2,0 | aplay -D hw:0,0 &
```

e.g.:



```text
$ arecord -f dat -t wav -D hw:CARD=UAC2Gadget,DEV=0 | \
  aplay -D default:CARD=OdroidU3
```

<a id="rst-uvc-function"></a>

## 18. UVC function

The function is provided by usb_f_uvc.ko module.

<a id="rst-function-specific-configfs-interface-17"></a>

### Function-specific configfs interface

The function name to use when creating the function directory is "uvc". The uvc function provides these attributes in its function directory:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> streaming_interval
>
> </td>
> <td>
>
>
> interval for polling endpoint for data transfers
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> streaming_maxburst
>
> </td>
> <td>
>
>
> bMaxBurst for super speed companion descriptor
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> streaming_maxpacket
>
> </td>
> <td>
>
>
> maximum packet size this endpoint is capable of sending or receiving when this configuration is selected
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> function_name
>
> </td>
> <td>
>
>
> name of the interface
>
> </td>
> </tr>
> </tbody>
> </table>

There are also "control" and "streaming" subdirectories, each of which contain a number of their subdirectories. There are some sane defaults provided, but the user must provide the following:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> control header
>
> </td>
> <td>
>
>
> create in control/header, link from control/class/fs and/or control/class/ss
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> streaming header
>
> </td>
> <td>
>
>
> create in streaming/header, link from streaming/class/fs and/or streaming/class/hs and/or streaming/class/ss
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> format description
>
> </td>
> <td>
>
>
> create in streaming/mjpeg and/or streaming/uncompressed
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> frame description
>
> </td>
> <td>
>
>
> create in streaming/mjpeg/&lt;format&gt; and/or in streaming/uncompressed/&lt;format&gt;
>
> </td>
> </tr>
> </tbody>
> </table>

Each frame description contains frame interval specification, and each such specification consists of a number of lines with an interval value in each line. The rules stated above are best illustrated with an example:



```text
# mkdir functions/uvc.usb0/control/header/h
# cd functions/uvc.usb0/control/
# ln -s header/h class/fs
# ln -s header/h class/ss
# mkdir -p functions/uvc.usb0/streaming/uncompressed/u/360p
# cat <<EOF > functions/uvc.usb0/streaming/uncompressed/u/360p/dwFrameInterval
666666
1000000
5000000
EOF
# cd $GADGET_CONFIGFS_ROOT
# mkdir functions/uvc.usb0/streaming/header/h
# cd functions/uvc.usb0/streaming/header/h
# ln -s ../../uncompressed/u
# cd ../../class/fs
# ln -s ../../header/h
# cd ../../class/hs
# ln -s ../../header/h
# cd ../../class/ss
# ln -s ../../header/h
```

<a id="rst-testing-the-uvc-function"></a>

### Testing the UVC function

device: run the gadget, modprobe vivid:



```text
# uvc-gadget -u /dev/video<uvc video node #> -v /dev/video<vivid video node #>
```

- **where uvc-gadget is this program:**

  [http://git.ideasonboard.org/uvc-gadget.git](<http://git.ideasonboard.org/uvc-gadget.git>)

with these patches:

> [https://lore.kernel.org/r/1386675637-18243-1-git-send-email-r.baldyga@samsung.com/](<https://lore.kernel.org/r/1386675637-18243-1-git-send-email-r.baldyga@samsung.com/>)

host:



```text
luvcview -f yuv
```

<a id="rst-printer-function"></a>

## 19. PRINTER function

The function is provided by usb_f_printer.ko module.

<a id="rst-function-specific-configfs-interface-18"></a>

### Function-specific configfs interface

The function name to use when creating the function directory is "printer". The printer function provides these attributes in its function directory:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> pnp_string
>
> </td>
> <td>
>
>
> Data to be passed to the host in pnp string
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> q_len
>
> </td>
> <td>
>
>
> Number of requests per endpoint
>
> </td>
> </tr>
> </tbody>
> </table>

<a id="rst-testing-the-printer-function"></a>

### Testing the PRINTER function

The most basic testing:

device: run the gadget:



```text
# ls -l /devices/virtual/usb_printer_gadget/
```

should show g_printer&lt;number&gt;.

If udev is active, then /dev/g_printer&lt;number&gt; should appear automatically.

host:

If udev is active, then e.g. /dev/usb/lp0 should appear.

host-&gt;device transmission:

device:



```text
# cat /dev/g_printer<number>
```

host:



```text
# cat > /dev/usb/lp0
```

device-&gt;host transmission:



```text
# cat > /dev/g_printer<number>
```

host:



```text
# cat /dev/usb/lp0
```

More advanced testing can be done with the prn_example described in [Documentation/usb/gadget_printer.rst](~kernel/hardware/usb/gadget-printer).

<a id="rst-uac1-function-virtual-alsa-card-using-u-audio-api"></a>

## 20. UAC1 function (virtual ALSA card, using u_audio API)

The function is provided by usb_f_uac1.ko module. It will create a virtual ALSA card and the audio streams are simply sinked to and sourced from it.

<a id="rst-function-specific-configfs-interface-19"></a>

### Function-specific configfs interface

The function name to use when creating the function directory is "uac1". The uac1 function provides these attributes in its function directory:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> c_chmask
>
> </td>
> <td>
>
>
> capture channel mask
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> c_srate
>
> </td>
> <td>
>
>
> list of capture sampling rates (comma-separated)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> c_ssize
>
> </td>
> <td>
>
>
> capture sample size (bytes)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> c_mute_present
>
> </td>
> <td>
>
>
> capture mute control enable
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> c_volume_present
>
> </td>
> <td>
>
>
> capture volume control enable
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> c_volume_min
>
> </td>
> <td>
>
>
> capture volume control min value (in 1/256 dB)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> c_volume_max
>
> </td>
> <td>
>
>
> capture volume control max value (in 1/256 dB)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> c_volume_res
>
> </td>
> <td>
>
>
> capture volume control resolution (in 1/256 dB)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> p_chmask
>
> </td>
> <td>
>
>
> playback channel mask
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> p_srate
>
> </td>
> <td>
>
>
> list of playback sampling rates (comma-separated)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> p_ssize
>
> </td>
> <td>
>
>
> playback sample size (bytes)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> p_mute_present
>
> </td>
> <td>
>
>
> playback mute control enable
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> p_volume_present
>
> </td>
> <td>
>
>
> playback volume control enable
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> p_volume_min
>
> </td>
> <td>
>
>
> playback volume control min value (in 1/256 dB)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> p_volume_max
>
> </td>
> <td>
>
>
> playback volume control max value (in 1/256 dB)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> p_volume_res
>
> </td>
> <td>
>
>
> playback volume control resolution (in 1/256 dB)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> req_number
>
> </td>
> <td>
>
>
> the number of pre-allocated requests for both capture and playback
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> function_name
>
> </td>
> <td>
>
>
> name of the interface
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> p_it_name
>
> </td>
> <td>
>
>
> playback input terminal name
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> p_it_ch_name
>
> </td>
> <td>
>
>
> playback channels name
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> p_ot_name
>
> </td>
> <td>
>
>
> playback output terminal name
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> p_fu_vol_name
>
> </td>
> <td>
>
>
> playback mute/volume functional unit name
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> c_it_name
>
> </td>
> <td>
>
>
> capture input terminal name
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> c_it_ch_name
>
> </td>
> <td>
>
>
> capture channels name
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> c_ot_name
>
> </td>
> <td>
>
>
> capture output terminal name
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> c_fu_vol_name
>
> </td>
> <td>
>
>
> capture mute/volume functional unit name
>
> </td>
> </tr>
> </tbody>
> </table>

The attributes have sane default values.

<a id="rst-testing-the-uac1-function-1"></a>

### Testing the UAC1 function

device: run the gadget host: aplay -l \# should list our USB Audio Gadget

This function does not require real hardware support, it just sends a stream of audio data to/from the host. In order to actually hear something at the device side, a command similar to this must be used at the device side:



```text
$ arecord -f dat -t wav -D hw:2,0 | aplay -D hw:0,0 &
```

e.g.:



```text
$ arecord -f dat -t wav -D hw:CARD=UAC1Gadget,DEV=0 | \
  aplay -D default:CARD=OdroidU3
```

<a id="rst-midi2-function"></a>

## 21. MIDI2 function

The function is provided by usb_f_midi2.ko module. It will create a virtual ALSA card containing a UMP rawmidi device where the UMP packet is looped back. In addition, a legacy rawmidi device is created. The UMP rawmidi is bound with ALSA sequencer clients, too.

<a id="rst-function-specific-configfs-interface-20"></a>

### Function-specific configfs interface

The function name to use when creating the function directory is "midi2". The midi2 function provides these attributes in its function directory as the card top-level information:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> process_ump
>
> </td>
> <td>
>
>
> Bool flag to process UMP Stream messages (0 or 1)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> static_block
>
> </td>
> <td>
>
>
> Bool flag for static blocks (0 or 1)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> iface_name
>
> </td>
> <td>
>
>
> Optional interface name string
>
> </td>
> </tr>
> </tbody>
> </table>

The directory contains a subdirectory "ep.0", and this provides the attributes for a UMP Endpoint (which is a pair of USB MIDI Endpoints):

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> protocol_caps
>
> </td>
> <td>
>
>
> MIDI protocol capabilities; 1: MIDI 1.0, 2: MIDI 2.0, or 3: both protocols
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> protocol
>
> </td>
> <td>
>
>
> Default MIDI protocol (either 1 or 2)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> ep_name
>
> </td>
> <td>
>
>
> UMP Endpoint name string
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> product_id
>
> </td>
> <td>
>
>
> Product ID string
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> manufacturer
>
> </td>
> <td>
>
>
> Manufacture ID number (24 bit)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> family
>
> </td>
> <td>
>
>
> Device family ID number (16 bit)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> model
>
> </td>
> <td>
>
>
> Device model ID number (16 bit)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> sw_revision
>
> </td>
> <td>
>
>
> Software revision (32 bit)
>
> </td>
> </tr>
> </tbody>
> </table>

Each Endpoint subdirectory contains a subdirectory "block.0", which represents the Function Block for Block 0 information. Its attributes are:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> name
>
> </td>
> <td>
>
>
> Function Block name string
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> direction
>
> </td>
> <td>
>
>
> Direction of this FB 1: input, 2: output, or 3: bidirectional
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> first_group
>
> </td>
> <td>
>
>
> The first UMP Group number (0-15)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> num_groups
>
> </td>
> <td>
>
>
> The number of groups in this FB (1-16)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> midi1_first_group
>
> </td>
> <td>
>
>
> The first UMP Group number for MIDI 1.0 (0-15)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> midi1_num_groups
>
> </td>
> <td>
>
>
> The number of groups for MIDI 1.0 (0-16)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> ui_hint
>
> </td>
> <td>
>
>
> UI-hint of this FB 0: unknown, 1: receiver, 2: sender, 3: both
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> midi_ci_version
>
> </td>
> <td>
>
>
> Supported MIDI-CI version number (8 bit)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> is_midi1
>
> </td>
> <td>
>
>
> Legacy MIDI 1.0 device (0-2) 0: MIDI 2.0 device, 1: MIDI 1.0 without restriction, or 2: MIDI 1.0 with low speed
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> sysex8_streams
>
> </td>
> <td>
>
>
> Max number of SysEx8 streams (8 bit)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> active
>
> </td>
> <td>
>
>
> Bool flag for FB activity (0 or 1)
>
> </td>
> </tr>
> </tbody>
> </table>

If multiple Function Blocks are required, you can add more Function Blocks by creating subdirectories "block.&lt;num&gt;" with the corresponding Function Block number (1, 2, ....). The FB subdirectories can be dynamically removed, too. Note that the Function Block numbers must be continuous.

Similarly, if you multiple UMP Endpoints are required, you can add more Endpoints by creating subdirectories "ep.&lt;num&gt;". The number must be continuous.

For emulating the old MIDI 2.0 device without UMP v1.1 support, pass 0 to `process_ump` flag. Then the whole UMP v1.1 requests are ignored.

<a id="rst-testing-the-midi2-function"></a>

### Testing the MIDI2 function

On the device: run the gadget, and running:



```text
$ cat /proc/asound/cards
```

will show a new sound card containing a MIDI2 device.

OTOH, on the host:



```text
$ cat /proc/asound/cards
```

will show a new sound card containing either MIDI1 or MIDI2 device, depending on the USB audio driver configuration.

On both, when ALSA sequencer is enabled on the host, you can find the UMP MIDI client such as "MIDI 2.0 Gadget".

As the driver simply loops back the data, there is no need for a real device just for testing.

For testing a MIDI input from the gadget to the host (e.g. emulating a MIDI keyboard), you can send a MIDI stream like the following.

On the gadget:



```text
$ aconnect -o
....
client 20: 'MIDI 2.0 Gadget' [type=kernel,card=1]
    0 'MIDI 2.0        '
    1 'Group 1 (MIDI 2.0 Gadget I/O)'
$ aplaymidi -p 20:1 to_host.mid
```

On the host:



```text
$ aconnect -i
....
client 24: 'MIDI 2.0 Gadget' [type=kernel,card=2]
    0 'MIDI 2.0        '
    1 'Group 1 (MIDI 2.0 Gadget I/O)'
$ arecordmidi -p 24:1 from_gadget.mid
```

If you have a UMP-capable application, you can use the UMP port to send/receive the raw UMP packets, too. For example, aseqdump program with UMP support can receive from UMP port. On the host:



```text
$ aseqdump -u 2 -p 24:1
Waiting for data. Press Ctrl+C to end.
Source  Group    Event                  Ch  Data
 24:1   Group  0, Program change          0, program 0, Bank select 0:0
 24:1   Group  0, Channel pressure        0, value 0x80000000
```

For testing a MIDI output to the gadget to the host (e.g. emulating a MIDI synth), it'll be just other way round.

On the gadget:



```text
$ arecordmidi -p 20:1 from_host.mid
```

On the host:



```text
$ aplaymidi -p 24:1 to_gadget.mid
```

The access to MIDI 1.0 on altset 0 on the host is supported, and it's translated from/to UMP packets on the gadget. It's bound to only Function Block 0.

The current operation mode can be observed in ALSA control element "Operation Mode" for SND_CTL_IFACE_RAWMIDI.  For example:



```text
$ amixer -c1 contents
numid=1,iface=RAWMIDI,name='Operation Mode'
  ; type=INTEGER,access=r--v----,values=1,min=0,max=2,step=0
  : values=2
```

where 0 = unused, 1 = MIDI 1.0 (altset 0), 2 = MIDI 2.0 (altset 1). The example above shows it's running in 2, i.e. MIDI 2.0.
