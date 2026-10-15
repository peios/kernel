---
title: "CPU to ISA Version Mapping"
type: reference
description: "Mapping of some CPU versions to relevant ISA versions."
---

<a id="rst-cpu-to-isa-version-mapping"></a>

Mapping of some CPU versions to relevant ISA versions.

Note Power4 and Power4+ are not supported.


<table>
<thead>
<tr>
<th>


CPU

</th>
<th>


Architecture version

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


Power10

</td>
<td>


Power ISA v3.1

</td>
</tr>
<tr>
<td>


Power9

</td>
<td>


Power ISA v3.0B

</td>
</tr>
<tr>
<td>


Power8

</td>
<td>


Power ISA v2.07

</td>
</tr>
<tr>
<td>


e6500

</td>
<td>


Power ISA v2.06 with some exceptions

</td>
</tr>
<tr>
<td>


e5500

</td>
<td>


Power ISA v2.06 with some exceptions, no Altivec

</td>
</tr>
<tr>
<td>


Power7

</td>
<td>


Power ISA v2.06

</td>
</tr>
<tr>
<td>


Power6

</td>
<td>


Power ISA v2.05

</td>
</tr>
<tr>
<td>


PA6T

</td>
<td>


Power ISA v2.04

</td>
</tr>
<tr>
<td>


Cell PPU

</td>
<td>


- Power ISA v2.02 with some minor exceptions

- Plus Altivec/VMX \~= 2.03

</td>
</tr>
<tr>
<td>


Power5++

</td>
<td>


Power ISA v2.04 (no VMX)

</td>
</tr>
<tr>
<td>


Power5+

</td>
<td>


Power ISA v2.03

</td>
</tr>
<tr>
<td>


Power5

</td>
<td>


- PowerPC User Instruction Set Architecture Book I v2.02

- PowerPC Virtual Environment Architecture Book II v2.02

- PowerPC Operating Environment Architecture Book III v2.02

</td>
</tr>
<tr>
<td>


PPC970

</td>
<td>


- PowerPC User Instruction Set Architecture Book I v2.01

- PowerPC Virtual Environment Architecture Book II v2.01

- PowerPC Operating Environment Architecture Book III v2.01

- Plus Altivec/VMX \~= 2.03

</td>
</tr>
<tr>
<td>


Power4+

</td>
<td>


- PowerPC User Instruction Set Architecture Book I v2.01

- PowerPC Virtual Environment Architecture Book II v2.01

- PowerPC Operating Environment Architecture Book III v2.01

</td>
</tr>
<tr>
<td>


Power4

</td>
<td>


- PowerPC User Instruction Set Architecture Book I v2.00

- PowerPC Virtual Environment Architecture Book II v2.00

- PowerPC Operating Environment Architecture Book III v2.00

</td>
</tr>
</tbody>
</table>

<a id="rst-key-features"></a>

## Key Features


<table>
<thead>
<tr>
<th>


CPU

</th>
<th>


VMX (aka. Altivec)

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


Power10

</td>
<td>


Yes

</td>
</tr>
<tr>
<td>


Power9

</td>
<td>


Yes

</td>
</tr>
<tr>
<td>


Power8

</td>
<td>


Yes

</td>
</tr>
<tr>
<td>


e6500

</td>
<td>


Yes

</td>
</tr>
<tr>
<td>


e5500

</td>
<td>


No

</td>
</tr>
<tr>
<td>


Power7

</td>
<td>


Yes

</td>
</tr>
<tr>
<td>


Power6

</td>
<td>


Yes

</td>
</tr>
<tr>
<td>


PA6T

</td>
<td>


Yes

</td>
</tr>
<tr>
<td>


Cell PPU

</td>
<td>


Yes

</td>
</tr>
<tr>
<td>


Power5++

</td>
<td>


No

</td>
</tr>
<tr>
<td>


Power5+

</td>
<td>


No

</td>
</tr>
<tr>
<td>


Power5

</td>
<td>


No

</td>
</tr>
<tr>
<td>


PPC970

</td>
<td>


Yes

</td>
</tr>
<tr>
<td>


Power4+

</td>
<td>


No

</td>
</tr>
<tr>
<td>


Power4

</td>
<td>


No

</td>
</tr>
</tbody>
</table>


<table>
<thead>
<tr>
<th>


CPU

</th>
<th>


VSX

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


Power10

</td>
<td>


Yes

</td>
</tr>
<tr>
<td>


Power9

</td>
<td>


Yes

</td>
</tr>
<tr>
<td>


Power8

</td>
<td>


Yes

</td>
</tr>
<tr>
<td>


e6500

</td>
<td>


No

</td>
</tr>
<tr>
<td>


e5500

</td>
<td>


No

</td>
</tr>
<tr>
<td>


Power7

</td>
<td>


Yes

</td>
</tr>
<tr>
<td>


Power6

</td>
<td>


No

</td>
</tr>
<tr>
<td>


PA6T

</td>
<td>


No

</td>
</tr>
<tr>
<td>


Cell PPU

</td>
<td>


No

</td>
</tr>
<tr>
<td>


Power5++

</td>
<td>


No

</td>
</tr>
<tr>
<td>


Power5+

</td>
<td>


No

</td>
</tr>
<tr>
<td>


Power5

</td>
<td>


No

</td>
</tr>
<tr>
<td>


PPC970

</td>
<td>


No

</td>
</tr>
<tr>
<td>


Power4+

</td>
<td>


No

</td>
</tr>
<tr>
<td>


Power4

</td>
<td>


No

</td>
</tr>
</tbody>
</table>


<table>
<thead>
<tr>
<th>


CPU

</th>
<th>


Transactional Memory

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


Power10

</td>
<td>


No  (\* see Power ISA v3.1, "Appendix A. Notes on the Removal of Transactional Memory from the Architecture")

</td>
</tr>
<tr>
<td>


Power9

</td>
<td>


Yes (\* see transactional_memory.txt)

</td>
</tr>
<tr>
<td>


Power8

</td>
<td>


Yes

</td>
</tr>
<tr>
<td>


e6500

</td>
<td>


No

</td>
</tr>
<tr>
<td>


e5500

</td>
<td>


No

</td>
</tr>
<tr>
<td>


Power7

</td>
<td>


No

</td>
</tr>
<tr>
<td>


Power6

</td>
<td>


No

</td>
</tr>
<tr>
<td>


PA6T

</td>
<td>


No

</td>
</tr>
<tr>
<td>


Cell PPU

</td>
<td>


No

</td>
</tr>
<tr>
<td>


Power5++

</td>
<td>


No

</td>
</tr>
<tr>
<td>


Power5+

</td>
<td>


No

</td>
</tr>
<tr>
<td>


Power5

</td>
<td>


No

</td>
</tr>
<tr>
<td>


PPC970

</td>
<td>


No

</td>
</tr>
<tr>
<td>


Power4+

</td>
<td>


No

</td>
</tr>
<tr>
<td>


Power4

</td>
<td>


No

</td>
</tr>
</tbody>
</table>
