---
title: "PCI vNTB Function"
type: reference
description: "The difference between PCI NTB function and PCI vNTB function is"
---

<a id="rst-pci-vntb-function"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

**Author:** Frank Li &lt;[Frank.Li@nxp.com](<mailto:Frank.Li@nxp.com>)&gt;

The difference between PCI NTB function and PCI vNTB function is

PCI NTB function need at two endpoint instances and connect HOST1 and HOST2.

PCI vNTB function only use one host and one endpoint(EP), use NTB connect EP and PCI host



```text
+------------+         +---------------------------------------+
|            |         |                                       |
+------------+         |                        +--------------+
| NTB        |         |                        | NTB          |
| NetDev     |         |                        | NetDev       |
+------------+         |                        +--------------+
| NTB        |         |                        | NTB          |
| Transfer   |         |                        | Transfer     |
+------------+         |                        +--------------+
|            |         |                        |              |
|  PCI NTB   |         |                        |              |
|    EPF     |         |                        |              |
|   Driver   |         |                        | PCI Virtual  |
|            |         +---------------+        | NTB Driver   |
|            |         | PCI EP NTB    |<------>|              |
|            |         |  FN Driver    |        |              |
+------------+         +---------------+        +--------------+
|            |         |               |        |              |
|  PCI BUS   | <-----> |  PCI EP BUS   |        |  Virtual PCI |
|            |  PCI    |               |        |     BUS      |
+------------+         +---------------+--------+--------------+
    PCI RC                        PCI EP
```

<a id="rst-constructs-used-for-implementing-vntb"></a>

## Constructs used for Implementing vNTB

> 1. Config Region
>
> 2. Self Scratchpad Registers
>
> 3. Peer Scratchpad Registers
>
> 4. Doorbell (DB) Registers
>
> 5. Memory Window (MW)

<a id="rst-config-region"></a>

### Config Region:

It is same as PCI NTB Function driver

<a id="rst-scratchpad-registers"></a>

### Scratchpad Registers:

It is appended after Config region.



```text
+--------------------------------------------------+ Base
|                                                  |
|                                                  |
|                                                  |
|          Common Config Register                  |
|                                                  |
|                                                  |
|                                                  |
+-----------------------+--------------------------+ Base + span_offset
|                       |                          |
|    Peer Span Space    |    Span Space            |
|                       |                          |
|                       |                          |
+-----------------------+--------------------------+ Base + span_offset
|                       |                          |      + span_count * 4
|                       |                          |
|     Span Space        |   Peer Span Space        |
|                       |                          |
+-----------------------+--------------------------+
      Virtual PCI             Pcie Endpoint
      NTB Driver               NTB Driver
```

<a id="rst-doorbell-registers"></a>

### Doorbell Registers:

> Doorbell Registers are used by the hosts to interrupt each other.

<a id="rst-memory-window"></a>

### Memory Window:

> Actual transfer of data between the two hosts will happen using the memory window.

<a id="rst-modeling-constructs"></a>

## Modeling Constructs:

32-bit BARs.


<table>
<thead>
<tr>
<th>


BAR NO

</th>
<th>


CONSTRUCTS USED

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


BAR0

</td>
<td>


Config Region

</td>
</tr>
<tr>
<td>


BAR1

</td>
<td>


Doorbell

</td>
</tr>
<tr>
<td>


BAR2

</td>
<td>


Memory Window 1

</td>
</tr>
<tr>
<td>


BAR3

</td>
<td>


Memory Window 2

</td>
</tr>
<tr>
<td>


BAR4

</td>
<td>


Memory Window 3

</td>
</tr>
<tr>
<td>


BAR5

</td>
<td>


Memory Window 4

</td>
</tr>
</tbody>
</table>

64-bit BARs.


<table>
<thead>
<tr>
<th>


BAR NO

</th>
<th>


CONSTRUCTS USED

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


BAR0

</td>
<td>


Config Region + Scratchpad

</td>
</tr>
<tr>
<td>


BAR1

</td>
<td>




</td>
</tr>
<tr>
<td>


BAR2

</td>
<td>


Doorbell

</td>
</tr>
<tr>
<td>


BAR3

</td>
<td>




</td>
</tr>
<tr>
<td>


BAR4

</td>
<td>


Memory Window 1

</td>
</tr>
<tr>
<td>


BAR5

</td>
<td>




</td>
</tr>
</tbody>
</table>
