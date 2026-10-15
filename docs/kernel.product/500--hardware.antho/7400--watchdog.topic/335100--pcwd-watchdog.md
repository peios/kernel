---
title: "Berkshire Products PC Watchdog Card"
type: reference
description: "Last reviewed: 10/05/2007"
---

<a id="rst-berkshire-products-pc-watchdog-card"></a>

Last reviewed: 10/05/2007

<a id="rst-support-for-isa-cards-revision-a-and-c"></a>

## Support for ISA Cards  Revision A and C

Documentation and Driver by Ken Hollis &lt;[kenji@bitgate.com](<mailto:kenji@bitgate.com>)&gt;

> The PC Watchdog is a card that offers the same type of functionality that the WDT card does, only it doesn't require an IRQ to run.  Furthermore, the Revision C card allows you to monitor any IO Port to automatically trigger the card into being reset.  This way you can make the card monitor hard drive status, or anything else you need.
>
> The Watchdog Driver has one basic role: to talk to the card and send signals to it so it doesn't reset your computer ... at least during normal operation.
>
> The Watchdog Driver will automatically find your watchdog card, and will attach a running driver for use with that card.  After the watchdog drivers have initialized, you can then talk to the card using a PC Watchdog program.
>
> I suggest putting a "watchdog -d" before the beginning of an fsck, and a "watchdog -e -t 1" immediately after the end of an fsck.  (Remember to run the program with an "&amp;" to run it in the background\!)
>
> If you want to write a program to be compatible with the PC Watchdog driver, simply use of modify the watchdog test program: tools/testing/selftests/watchdog/watchdog-test.c
>
> Other IOCTL functions include:
>
> > - **WDIOC\_GETSUPPORT**
> >
> >   This returns the support of the card itself.  This returns in structure "PCWDS" which returns:
> >
> >   > - **options = WDIOS\_TEMPPANIC**
> >   >
> >   >   (This card supports temperature)
> >   >
> >   > - **firmware\_version = xxxx**
> >   >
> >   >   (Firmware version of the card)
> >
> > - **WDIOC\_GETSTATUS**
> >
> >   This returns the status of the card, with the bits of WDIOF\_\* bitwise-anded into the value.  (The comments are in include/uapi/linux/watchdog.h)
> >
> > - **WDIOC\_GETBOOTSTATUS**
> >
> >   This returns the status of the card that was reported at bootup.
> >
> > - **WDIOC\_GETTEMP**
> >
> >   This returns the temperature of the card.  (You can also read /dev/watchdog, which gives a temperature update every second.)
> >
> > - **WDIOC\_SETOPTIONS**
> >
> >   This lets you set the options of the card.  You can either enable or disable the card this way.
> >
> > - **WDIOC\_KEEPALIVE**
> >
> >   This pings the card to tell it not to reset your computer.
>
> And that's all she wrote\!
>
> — Ken Hollis
> ([kenji@bitgate.com](<mailto:kenji@bitgate.com>))
