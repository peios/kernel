---
title: "Turtle Beach MultiSound driver notes and utilities"
type: reference
description: "Historical MultiSound driver notes and the accompanying Pinnacle/Fiji utility archive. The notes identify their original driver version and update date."
---

Historical MultiSound driver notes and the accompanying Pinnacle/Fiji utility archive. The notes identify their original driver version and update date.

## Driver notes

### Turtle Beach MultiSound Driver Notes

-- Andrew Veliath &lt;andrewtv@usa.net&gt;

```text
Last update:                      September 10, 1998
Corresponding msnd driver:        0.8.3
```

\*\* This file is a README (top part) and shell archive (bottom part).
  The corresponding archived utility sources can be unpacked by
  running \`sh MultiSound' (the utilities are only needed for the
  Pinnacle and Fiji cards). \*\*

## -=-=- Getting Firmware -=-=-

See the section \`Obtaining and Creating Firmware Files' in this
document for instructions on obtaining the necessary firmware
files.

## Supported Features

Currently, full-duplex digital audio (/dev/dsp only, /dev/audio is
not currently available) and mixer functionality (/dev/mixer) are
supported (memory mapped digital audio is not yet supported).
Digital transfers and monitoring can be done as well if you have
the digital daughterboard (see the section on using the S/PDIF port
for more information).

Support for the Turtle Beach MultiSound Hurricane architecture is
composed of the following modules (these can also operate compiled
into the kernel):

snd-msnd-lib           - MultiSound base (requires snd)

snd-msnd-classic       - Base audio/mixer support for Classic, Monetery and

```text
                         Tahiti cards
```

snd-msnd-pinnacle      - Base audio/mixer support for Pinnacle and Fiji cards

## Important Notes - Read Before Using

The firmware files are not included (may change in future).  You
must obtain these images from Turtle Beach (they are included in
the MultiSound Development Kits), and place them in /etc/sound for
example, and give the full paths in the Linux configuration.  If
you are compiling in support for the MultiSound driver rather than
using it as a module, these firmware files must be accessible
during kernel compilation.

Please note these files must be binary files, not assembler.  See
the section later in this document for instructions to obtain these
files.

## Configuring Card Resources

\*\* This section is very important, as your card may not work at all
   or your machine may crash if you do not do this correctly. \*\*

- Classic/Monterey/Tahiti

These cards are configured through the driver snd-msnd-classic.  You must
know the io port, then the driver will select the irq and memory resources
on the card.  It is up to you to know if these are free locations or now,
a conflict can lock the machine up.

- Pinnacle/Fiji

The Pinnacle and Fiji cards have an extra config port, either
0x250, 0x260 or 0x270.  This port can be disabled to have the card
configured strictly through PnP, however you lose the ability to
access the IDE controller and joystick devices on this card when
using PnP.  The included pinnaclecfg program in this shell archive
can be used to configure the card in non-PnP mode, and in PnP mode
you can use isapnptools.  These are described briefly here.

pinnaclecfg is not required; you can use the snd-msnd-pinnacle module
to fully configure the card as well.  However, pinnaclecfg can be
used to change the resource values of a particular device after the
snd-msnd-pinnacle module has been loaded.  If you are compiling the
driver into the kernel, you must set these values during compile
time, however other peripheral resource values can be changed with
the pinnaclecfg program after the kernel is loaded.

\*\*\* PnP mode

Use pnpdump to obtain a sample configuration if you can; I was able
to obtain one with the command \`pnpdump 1 0x203' -- this may vary
for you (running pnpdump by itself did not work for me).  Then,
edit this file and use isapnp to uncomment and set the card values.
Use these values when inserting the snd-msnd-pinnacle module.  Using
this method, you can set the resources for the DSP and the Kurzweil
synth (Pinnacle).  Since Linux does not directly support PnP
devices, you may have difficulty when using the card in PnP mode
when it the driver is compiled into the kernel.  Using non-PnP mode
is preferable in this case.

Here is an example mypinnacle.conf for isapnp that sets the card to
io base 0x210, irq 5 and mem 0xd8000, and also sets the Kurzweil
synth to 0x330 and irq 9 (may need editing for your system):

(READPORT 0x0203)
(CSN 2)
(IDENTIFY \*)

\# DSP
(CONFIGURE BVJ0440/-1 (LD 0

```text
        (INT 0 (IRQ 5 (MODE +E))) (IO 0 (BASE 0x0210)) (MEM 0 (BASE 0x0d8000))
        (ACT Y)))
```

\# Kurzweil Synth (Pinnacle Only)
(CONFIGURE BVJ0440/-1 (LD 1

```text
        (IO 0 (BASE 0x0330)) (INT 0 (IRQ 9 (MODE +E)))
        (ACT Y)))
```

(WAITFORKEY)

\*\*\* Non-PnP mode

The second way is by running the card in non-PnP mode.  This
actually has some advantages in that you can access some other
devices on the card, such as the joystick and IDE controller.  To
configure the card, unpack this shell archive and build the
pinnaclecfg program.  Using this program, you can assign the
resource values to the card's devices, or disable the devices.  As
an alternative to using pinnaclecfg, you can specify many of the
configuration values when loading the snd-msnd-pinnacle module (or
during kernel configuration when compiling the driver into the
kernel).

If you specify cfg=0x250 for the snd-msnd-pinnacle module, it
automatically configure the card to the given io, irq and memory
values using that config port (the config port is jumper selectable
on the card to 0x250, 0x260 or 0x270).

See the \`snd-msnd-pinnacle Additional Options' section below for more
information on these parameters (also, if you compile the driver
directly into the kernel, these extra parameters can be useful
here).

\*\* It is very easy to cause problems in your machine if you choose a
  resource value which is incorrect. \*\*

## Examples

- MultiSound Classic/Monterey/Tahiti:

```text
modprobe snd
```

insmod snd-msnd-lib
insmod snd-msnd-classic io=0x290 irq=7 mem=0xd0000

- MultiSound Pinnacle in PnP mode:

```text
modprobe snd
```

insmod snd-msnd-lib
isapnp mypinnacle.conf
insmod snd-msnd-pinnacle io=0x210 irq=5 mem=0xd8000 &lt;-- match mypinnacle.conf values

- MultiSound Pinnacle in non-PnP mode (replace 0x250 with your configuration port,
  one of 0x250, 0x260 or 0x270):

```text
modprobe snd
```

insmod snd-msnd-lib
insmod snd-msnd-pinnacle cfg=0x250 io=0x290 irq=5 mem=0xd0000

- To use the MPU-compatible Kurzweil synth on the Pinnacle in PnP
  mode, add the following (assumes you did \`isapnp mypinnacle.conf'):

insmod snd
insmod mpu401 io=0x330 irq=9                    &lt;-- match mypinnacle.conf values

- To use the MPU-compatible Kurzweil synth on the Pinnacle in non-PnP
  mode, add the following.  Note how we first configure the peripheral's
  resources, \_then\_ install a Linux driver for it:

insmod snd
pinnaclecfg 0x250 mpu 0x330 9
insmod mpu401 io=0x330 irq=9

-- OR you can use the following sequence without pinnaclecfg in non-PnP mode:

```text
modprobe snd
```

insmod snd-msnd-lib
insmod snd-msnd-pinnacle cfg=0x250 io=0x290 irq=5 mem=0xd0000 mpu\_io=0x330 mpu\_irq=9
insmod snd
insmod mpu401 io=0x330 irq=9

- To setup the joystick port on the Pinnacle in non-PnP mode (though
  you have to find the actual Linux joystick driver elsewhere), you
  can use pinnaclecfg:

```text
 pinnaclecfg 0x250 joystick 0x200
```

-- OR you can configure this using snd-msnd-pinnacle with the following:

```text
modprobe snd
```

insmod snd-msnd-lib
insmod snd-msnd-pinnacle cfg=0x250 io=0x290 irq=5 mem=0xd0000 joystick\_io=0x200

## snd-msnd-classic, snd-msnd-pinnacle Required Options

If the following options are not given, the module will not load.
Examine the kernel message log for informative error messages.
WARNING--probing isn't supported so try to make sure you have the
correct shared memory area, otherwise you may experience problems.

```text
io                   I/O base of DSP, e.g. io=0x210
irq                  IRQ number, e.g. irq=5
mem                  Shared memory area, e.g. mem=0xd8000
```

## snd-msnd-classic, snd-msnd-pinnacle Additional Options

fifosize             The digital audio FIFOs, in kilobytes.  If not

```text
                     specified, the default will be used.  Increasing
                     this value will reduce the chance of a FIFO
                     underflow at the expense of increasing overall
                     latency.  For example, fifosize=512 will
                     allocate 512kB read and write FIFOs (1MB total).
                     While this may reduce dropouts, a heavy machine
                     load will undoubtedly starve the FIFO of data
                     and you will eventually get dropouts.  One
                     option is to alter the scheduling priority of
                     the playback process, using `nice' or some form
                     of POSIX soft real-time scheduling.
```

calibrate\_signal     Setting this to one calibrates the ADCs to the

```text
                     signal, zero calibrates to the card (defaults
                     to zero).
```

## snd-msnd-pinnacle Additional Options

digital              Specify digital=1 to enable the S/PDIF input

```text
                     if you have the digital daughterboard
                     adapter. This will enable access to the
                     DIGITAL1 input for the soundcard in the mixer.
                     Some mixer programs might have trouble setting
                     the DIGITAL1 source as an input.  If you have
                     trouble, you can try the setdigital.c program
                     at the bottom of this document.
```

cfg                  Non-PnP configuration port for the Pinnacle

```text
                     and Fiji (typically 0x250, 0x260 or 0x270,
                     depending on the jumper configuration).  If
                     this option is omitted, then it is assumed
                     that the card is in PnP mode, and that the
                     specified DSP resource values are already
                     configured with PnP (i.e. it won't attempt to
                     do any sort of configuration).
```

When the Pinnacle is in non-PnP mode, you can use the following
options to configure particular devices.  If a full specification
for a device is not given, then the device is not configured.  Note
that you still must use a Linux driver for any of these devices
once their resources are setup (such as the Linux joystick driver,
or the MPU401 driver from OSS for the Kurzweil synth).

```text
mpu_io               I/O port of MPU (on-board Kurzweil synth)
mpu_irq              IRQ of MPU (on-board Kurzweil synth)
ide_io0		First I/O port of IDE controller
ide_io1		Second I/O port of IDE controller
ide_irq		IRQ IDE controller
joystick_io          I/O port of joystick
```

## Obtaining and Creating Firmware Files

## For the Classic/Tahiti/Monterey

Download to /tmp and unzip the following file from Turtle Beach:

```text
     ftp://ftp.voyetra.com/pub/tbs/msndcl/msndvkit.zip
```

When unzipped, unzip the file named MsndFiles.zip.  Then copy the
following firmware files to /etc/sound (note the file renaming):

```text
  cp DSPCODE/MSNDINIT.BIN /etc/sound/msndinit.bin
  cp DSPCODE/MSNDPERM.REB /etc/sound/msndperm.bin
```

When configuring the Linux kernel, specify /etc/sound/msndinit.bin and
/etc/sound/msndperm.bin for the two firmware files (Linux kernel
versions older than 2.2 do not ask for firmware paths, and are
hardcoded to /etc/sound).

If you are compiling the driver into the kernel, these files must
be accessible during compilation, but will not be needed later.
The files must remain, however, if the driver is used as a module.

## For the Pinnacle/Fiji

Download to /tmp and unzip the following file from Turtle Beach (be
sure to use the entire URL; some have had trouble navigating to the
URL):

```text
     ftp://ftp.voyetra.com/pub/tbs/pinn/pnddk100.zip
```

Unpack this shell archive, and run make in the created directory
(you need a C compiler and flex to build the utilities).  This
should give you the executables conv, pinnaclecfg and setdigital.
conv is only used temporarily here to create the firmware files,
while pinnaclecfg is used to configure the Pinnacle or Fiji card in
non-PnP mode, and setdigital can be used to set the S/PDIF input on
the mixer (pinnaclecfg and setdigital should be copied to a
convenient place, possibly run during system initialization).

To generating the firmware files with the \`conv' program, we create
the binary firmware files by doing the following conversion
(assuming the archive unpacked into a directory named PINNDDK):

```text
  ./conv < PINNDDK/dspcode/pndspini.asm > /etc/sound/pndspini.bin
  ./conv < PINNDDK/dspcode/pndsperm.asm > /etc/sound/pndsperm.bin
```

The conv (and conv.l) program is not needed after conversion and can
be safely deleted.  Then, when configuring the Linux kernel, specify
/etc/sound/pndspini.bin and /etc/sound/pndsperm.bin for the two
firmware files (Linux kernel versions older than 2.2 do not ask for
firmware paths, and are hardcoded to /etc/sound).

If you are compiling the driver into the kernel, these files must
be accessible during compilation, but will not be needed later.
The files must remain, however, if the driver is used as a module.

## Using Digital I/O with the S/PDIF Port

If you have a Pinnacle or Fiji with the digital daughterboard and
want to set it as the input source, you can use this program if you
have trouble trying to do it with a mixer program (be sure to
insert the module with the digital=1 option, or say Y to the option
during compiled-in kernel operation).  Upon selection of the S/PDIF
port, you should be able monitor and record from it.

There is something to note about using the S/PDIF port.  Digital
timing is taken from the digital signal, so if a signal is not
connected to the port and it is selected as recording input, you
will find PCM playback to be distorted in playback rate.  Also,
attempting to record at a sampling rate other than the DAT rate may
be problematic (i.e. trying to record at 8000Hz when the DAT signal
is 44100Hz).  If you have a problem with this, set the recording
input to analog if you need to record at a rate other than that of
the DAT rate.

-- Shell archive attached below, just run \`sh MultiSound' to extract.
   Contains Pinnacle/Fiji utilities to convert firmware, configure
   in non-PnP mode, and select the DIGITAL1 input for the mixer.

## Original source and utility archive

```{kernel-include} docs/sources/sound/cards/multisound.sh
:language: bash
```
