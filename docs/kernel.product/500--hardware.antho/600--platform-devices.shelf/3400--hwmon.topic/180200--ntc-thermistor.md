---
title: "Kernel driver ntc_thermistor"
type: reference
description: "Supported thermistors from Murata:"
---

<a id="rst-kernel-driver-ntc-thermistor"></a>

Supported thermistors from Murata:

- Murata NTC Thermistors NCP15WB473, NCP18WB473, NCP21WB473, NCP03WB473, NCP15WL333, NCP03WF104, NCP15XH103

  Prefixes: 'ncp15wb473', 'ncp18wb473', 'ncp21wb473', 'ncp03wb473', 'ncp15wl333', 'ncp03wf104', 'ncp15xh103'

  Datasheet: Publicly available at Murata

Supported thermistors from EPCOS:

- EPCOS NTC Thermistors B57330V2103

  Prefixes: b57330v2103

  Datasheet: Publicly available at EPCOS

Other NTC thermistors can be supported simply by adding compensation tables; e.g., NCP15WL333 support is added by the table ncpXXwl333.

Authors:

> MyungJoo Ham &lt;[myungjoo.ham@samsung.com](<mailto:myungjoo.ham@samsung.com>)&gt;

<a id="rst-description"></a>

## Description

The NTC (Negative Temperature Coefficient) thermistor is a simple thermistor that requires users to provide the resistance and lookup the corresponding compensation table to get the temperature input.

The NTC driver provides lookup tables with a linear approximation function and four circuit models with an option not to use any of the four models.

Using the following convention:



```text
$    resistor
[TH] the thermistor
```

The four circuit models provided are:

1. connect = NTC_CONNECTED_POSITIVE, pullup_ohm &gt; 0:



   ```text
   [pullup_uV]
       |    |
      [TH]  $ (pullup_ohm)
       |    |
       +----+-----------------------[read_uV]
       |
       $ (pulldown_ohm)
       |
      -+- (ground)
   ```

2. connect = NTC_CONNECTED_POSITIVE, pullup_ohm = 0 (not-connected):



   ```text
   [pullup_uV]
       |
      [TH]
       |
       +----------------------------[read_uV]
       |
       $ (pulldown_ohm)
       |
      -+- (ground)
   ```

3. connect = NTC_CONNECTED_GROUND, pulldown_ohm &gt; 0:



   ```text
   [pullup_uV]
       |
       $ (pullup_ohm)
       |
       +----+-----------------------[read_uV]
       |    |
      [TH]  $ (pulldown_ohm)
       |    |
      -+----+- (ground)
   ```

4. connect = NTC_CONNECTED_GROUND, pulldown_ohm = 0 (not-connected):



   ```text
   [pullup_uV]
       |
       $ (pullup_ohm)
       |
       +----------------------------[read_uV]
       |
      [TH]
       |
      -+- (ground)
   ```

When one of the four circuit models is used, read_uV, pullup_uV, pullup_ohm, pulldown_ohm, and connect should be provided. When none of the four models are suitable or the user can get the resistance directly, the user should provide read_ohm and \_not\_ provide the others.

<a id="rst-sysfs-interface"></a>

## Sysfs Interface


<table>
<thead>
<tr>
<th>


name

</th>
<th>




</th>
<th>


the mandatory global attribute, the thermistor name.

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


temp1_type

</td>
<td>


RO

</td>
<td>


always 4 (thermistor)

</td>
</tr>
<tr>
<td>


temp1_input

</td>
<td>


RO

</td>
<td>


measure the temperature and provide the measured value. (reading this file initiates the reading procedure.)

</td>
</tr>
</tbody>
</table>

Note that each NTC thermistor has only \_one\_ thermistor; thus, only temp1 exists.
