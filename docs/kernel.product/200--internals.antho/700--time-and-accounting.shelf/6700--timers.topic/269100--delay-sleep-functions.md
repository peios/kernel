---
title: "Delay and sleep mechanisms"
type: reference
description: "This document seeks to answer the common question: \"What is the RightWay (TM) to insert a delay?\""
---

<a id="rst-delay-and-sleep-mechanisms"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

This document seeks to answer the common question: "What is the RightWay (TM) to insert a delay?"

This question is most often faced by driver writers who have to deal with hardware delays and who may not be the most intimately familiar with the inner workings of the Linux Kernel.

The following table gives a rough overview about the existing function 'families' and their limitations. This overview table does not replace the reading of the function description before usage\!


<table>
<thead>
<tr>
<th>




</th>
<th>


`*delay()`

</th>
<th>


`usleep_range*()`

</th>
<th>


`*sleep()`

</th>
<th>


`fsleep()`

</th>
</tr>
<tr>
<th>




</th>
<th>


busy-wait loop

</th>
<th>


hrtimers based

</th>
<th>


timer list timers based

</th>
<th>


combines the others

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


Usage in atomic Context

</td>
<td>


yes

</td>
<td>


no

</td>
<td>


no

</td>
<td>


no

</td>
</tr>
<tr>
<td>


precise on "short intervals"

</td>
<td>


yes

</td>
<td>


yes

</td>
<td>


depends

</td>
<td>


yes

</td>
</tr>
<tr>
<td>


precise on "long intervals"

</td>
<td>


Do not use\!

</td>
<td>


yes

</td>
<td>


max 12.5% slack

</td>
<td>


yes

</td>
</tr>
<tr>
<td>


interruptible variant

</td>
<td>


no

</td>
<td>


yes

</td>
<td>


yes

</td>
<td>


no

</td>
</tr>
</tbody>
</table>

A generic advice for non atomic contexts could be:

1. Use `fsleep()` whenever unsure (as it combines all the advantages of the others)

2. Use `*sleep()` whenever possible

3. Use `usleep_range*()` whenever accuracy of `*sleep()` is not sufficient

4. Use `*delay()` for very, very short delays

Find some more detailed information about the function 'families' in the next sections.

<a id="rst-delay-family-of-functions"></a>

## `*delay()` family of functions

These functions use the jiffy estimation of clock speed and will busy wait for enough loop cycles to achieve the desired delay. udelay() is the basic implementation and ndelay() as well as mdelay() are variants.

These functions are mainly used to add a delay in atomic context. Please make sure to ask yourself before adding a delay in atomic context: Is this really required?

```{kernel-doc} include/asm-generic/delay.h
:identifiers: udelay ndelay
```

```{kernel-doc} include/linux/delay.h
:identifiers: mdelay
```

<a id="rst-usleep-range-and-sleep-family-of-functions"></a>

## `usleep_range*()` and `*sleep()` family of functions

These functions use hrtimers or timer list timers to provide the requested sleeping duration. In order to decide which function is the right one to use, take some basic information into account:

1. hrtimers are more expensive as they are using an rb-tree (instead of hashing)

2. hrtimers are more expensive when the requested sleeping duration is the first timer which means real hardware has to be programmed

3. timer list timers always provide some sort of slack as they are jiffy based

The generic advice is repeated here:

1. Use `fsleep()` whenever unsure (as it combines all the advantages of the others)

2. Use `*sleep()` whenever possible

3. Use `usleep_range*()` whenever accuracy of `*sleep()` is not sufficient

First check fsleep() function description and to learn more about accuracy, please check msleep() function description.

<a id="rst-usleep-range"></a>

### `usleep_range*()`

```{kernel-doc} include/linux/delay.h
:identifiers: usleep_range usleep_range_idle
```

```{kernel-doc} kernel/time/sleep_timeout.c
:identifiers: usleep_range_state
```

<a id="rst-sleep"></a>

### `*sleep()`

```{kernel-doc} kernel/time/sleep_timeout.c
:identifiers: msleep msleep_interruptible
```

```{kernel-doc} include/linux/delay.h
:identifiers: ssleep fsleep
```
