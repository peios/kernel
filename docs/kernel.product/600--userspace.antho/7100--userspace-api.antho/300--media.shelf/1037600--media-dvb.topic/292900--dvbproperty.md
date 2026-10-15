---
title: "Property types"
type: reference
description: "Tuning into a Digital TV physical channel and starting decoding it requires changing a set of parameters, in order to control the tuner, the demodulator, the Linear Low-noise Amplifier (LNA) and to set the antenna subsystem via Satellite…"
---

<a id="rst-property-types"></a>
<a id="rst-frontend-properties"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

Tuning into a Digital TV physical channel and starting decoding it requires changing a set of parameters, in order to control the tuner, the demodulator, the Linear Low-noise Amplifier (LNA) and to set the antenna subsystem via Satellite Equipment Control - SEC (on satellite systems). The actual parameters are specific to each particular digital TV standards, and may change as the digital TV specs evolves.

In the past (up to DVB API version 3 - DVBv3), the strategy used was to have a union with the parameters needed to tune for DVB-S, DVB-C, DVB-T and ATSC delivery systems grouped there. The problem is that, as the second generation standards appeared, the size of such union was not big enough to group the structs that would be required for those new standards. Also, extending it would break userspace.

So, the legacy union/struct based approach was deprecated, in favor of a properties set approach. On such approach, [FE\_GET\_PROPERTY and FE\_SET\_PROPERTY](<~kernel/userspace/userspace-api/media-dvb/fe-get-property#rst-fe-get-property>) are used to setup the frontend and read its status.

The actual action is determined by a set of dtv\_property cmd/data pairs. With one single ioctl, is possible to get/set up to 64 properties.

This section describes the new and recommended way to set the frontend, with supports all digital TV delivery systems.

> [!NOTE]
>
> 1. On Linux DVB API version 3, setting a frontend was done via struct `dvb_frontend_parameters`.
>
> 2. Don't use DVB API version 3 calls on hardware with supports newer standards. Such API provides no support or a very limited support to new standards and/or new hardware.
>
> 3. Nowadays, most frontends support multiple delivery systems. Only with DVB API version 5 calls it is possible to switch between the multiple delivery systems supported by a frontend.
>
> 4. DVB API version 5 is also called <em>S2API</em>, as the first new standard added to it was DVB-S2.

<strong>Example</strong>: in order to set the hardware to tune into a DVB-C channel at 651 kHz, modulated with 256-QAM, FEC 3/4 and symbol rate of 5.217 Mbauds, those properties should be sent to [FE\_SET\_PROPERTY](<~kernel/userspace/userspace-api/media-dvb/fe-get-property#rst-fe-get-property>) ioctl:

> [DTV\_DELIVERY\_SYSTEM](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-delivery-system>) = SYS\_DVBC\_ANNEX\_A
>
> [DTV\_FREQUENCY](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-frequency>) = 651000000
>
> [DTV\_MODULATION](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-modulation>) = QAM\_256
>
> [DTV\_INVERSION](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-inversion>) = INVERSION\_AUTO
>
> [DTV\_SYMBOL\_RATE](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-symbol-rate>) = 5217000
>
> [DTV\_INNER\_FEC](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-inner-fec>) = FEC\_3\_4
>
> [DTV\_TUNE](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters#rst-dtv-tune>)

The code that would that would do the above is show in [dtv-prop-example](<#rst-dtv-prop-example>).

Example: Setting digital TV frontend properties

<a id="rst-dtv-prop-example"></a>



```c
#include <stdio.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <linux/dvb/frontend.h>

static struct dtv_property props[] = {
    { .cmd = DTV_DELIVERY_SYSTEM, .u.data = SYS_DVBC_ANNEX_A },
    { .cmd = DTV_FREQUENCY,       .u.data = 651000000 },
    { .cmd = DTV_MODULATION,      .u.data = QAM_256 },
    { .cmd = DTV_INVERSION,       .u.data = INVERSION_AUTO },
    { .cmd = DTV_SYMBOL_RATE,     .u.data = 5217000 },
    { .cmd = DTV_INNER_FEC,       .u.data = FEC_3_4 },
    { .cmd = DTV_TUNE }
};

static struct dtv_properties dtv_prop = {
    .num = 6, .props = props
};

int main(void)
{
    int fd = open("/dev/dvb/adapter0/frontend0", O_RDWR);

    if (!fd) {
        perror ("open");
        return -1;
    }
    if (ioctl(fd, FE_SET_PROPERTY, &dtv_prop) == -1) {
        perror("ioctl");
        return -1;
    }
    printf("Frontend set\\n");
    return 0;
}
```

> [!NOTE]
>
> While it is possible to directly call the Kernel code like the above example, it is strongly recommended to use [libdvbv5](<https://linuxtv.org/docs/libdvbv5/index.html>), as it provides abstraction to work with the supported digital TV standards and provides methods for usual operations like program scanning and to read/write channel descriptor files.

- [Digital TV property parameters](<~kernel/userspace/userspace-api/media-dvb/fe-property-parameters>)
- [Frontend statistics indicators](<~kernel/userspace/userspace-api/media-dvb/frontend-stat-properties>)
- [Properties used on terrestrial delivery systems](<~kernel/userspace/userspace-api/media-dvb/frontend-property-terrestrial-systems>)
- [Properties used on cable delivery systems](<~kernel/userspace/userspace-api/media-dvb/frontend-property-cable-systems>)
- [Properties used on satellite delivery systems](<~kernel/userspace/userspace-api/media-dvb/frontend-property-satellite-systems>)
- [Frontend uAPI data types](<~kernel/userspace/userspace-api/media-dvb/frontend-header>)
