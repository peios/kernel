---
title: "Silicon Errata and Software Workarounds"
type: reference
description: "Author: Will Deacon <will.deacon@arm.com>"
---

<a id="rst-silicon-errata-and-software-workarounds"></a>

Author: Will Deacon &lt;[will.deacon@arm.com](<mailto:will.deacon@arm.com>)&gt;

Date  : 27 November 2015

It is an unfortunate fact of life that hardware is often produced with so-called "errata", which can cause it to deviate from the architecture under specific circumstances.  For hardware produced by ARM, these errata are broadly classified into the following categories:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> Category A
>
> </td>
> <td>
>
>
> A critical error without a viable workaround.
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> Category B
>
> </td>
> <td>
>
>
> A significant or critical error with an acceptable workaround.
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> Category C
>
> </td>
> <td>
>
>
> A minor error that is not expected to occur under normal operation.
>
> </td>
> </tr>
> </tbody>
> </table>

For more information, consult one of the "Software Developers Errata Notice" documents available on infocenter.arm.com (registration required).

As far as Linux is concerned, Category B errata may require some special treatment in the operating system. For example, avoiding a particular sequence of code, or configuring the processor in a particular way. A less common situation may require similar actions in order to declassify a Category A erratum into a Category C erratum. These are collectively known as "software workarounds" and are only required in the minority of cases (e.g. those cases that both require a non-secure workaround *and* can be triggered by Linux).

For software workarounds that may adversely impact systems unaffected by the erratum in question, a Kconfig entry is added under "Kernel Features" -&gt; "ARM errata workarounds via the alternatives framework". With the exception of workarounds for errata deemed "rare" by Arm, these are enabled by default and patched in at runtime when an affected CPU is detected. For less-intrusive workarounds, a Kconfig option is not available and the code is structured (preferably with a comment) in such a way that the erratum will not be hit.

This approach can make it slightly onerous to determine exactly which errata are worked around in an arbitrary kernel source tree, so this file acts as a registry of software workarounds in the Linux Kernel and will be updated when new workarounds are committed and backported to stable kernels.


<table>
<thead>
<tr>
<th>


Implementor

</th>
<th>


Component

</th>
<th>


Erratum ID

</th>
<th>


Kconfig

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


Allwinner

</td>
<td>


A64/R18

</td>
<td>


UNKNOWN1

</td>
<td>


SUN50I_ERRATUM_UNKNOWN1

</td>
</tr>
<tr>
<td>




</td>
<td>




</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


Ampere

</td>
<td>


AmpereOne

</td>
<td>


AC03_CPU_38

</td>
<td>


AMPERE_ERRATUM_AC03_CPU_38

</td>
</tr>
<tr>
<td>


Ampere

</td>
<td>


AmpereOne AC04

</td>
<td>


AC04_CPU_10

</td>
<td>


AMPERE_ERRATUM_AC03_CPU_38

</td>
</tr>
<tr>
<td>


Ampere

</td>
<td>


AmpereOne AC04

</td>
<td>


AC04_CPU_23

</td>
<td>


AMPERE_ERRATUM_AC04_CPU_23

</td>
</tr>
<tr>
<td>




</td>
<td>




</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Cortex-A510

</td>
<td>


\#2457168

</td>
<td>


ARM64_ERRATUM_2457168

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Cortex-A510

</td>
<td>


\#2064142

</td>
<td>


ARM64_ERRATUM_2064142

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Cortex-A510

</td>
<td>


\#2038923

</td>
<td>


ARM64_ERRATUM_2038923

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Cortex-A510

</td>
<td>


\#1902691

</td>
<td>


ARM64_ERRATUM_1902691

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Cortex-A510

</td>
<td>


\#2051678

</td>
<td>


ARM64_ERRATUM_2051678

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Cortex-A510

</td>
<td>


\#2077057

</td>
<td>


ARM64_ERRATUM_2077057

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Cortex-A510

</td>
<td>


\#2441009

</td>
<td>


ARM64_ERRATUM_2441009

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Cortex-A510

</td>
<td>


\#2658417

</td>
<td>


ARM64_ERRATUM_2658417

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Cortex-A510

</td>
<td>


\#3117295

</td>
<td>


ARM64_ERRATUM_3117295

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Cortex-A520

</td>
<td>


\#2966298

</td>
<td>


ARM64_ERRATUM_2966298

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Cortex-A53

</td>
<td>


\#826319

</td>
<td>


ARM64_ERRATUM_826319

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Cortex-A53

</td>
<td>


\#827319

</td>
<td>


ARM64_ERRATUM_827319

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Cortex-A53

</td>
<td>


\#824069

</td>
<td>


ARM64_ERRATUM_824069

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Cortex-A53

</td>
<td>


\#819472

</td>
<td>


ARM64_ERRATUM_819472

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Cortex-A53

</td>
<td>


\#845719

</td>
<td>


ARM64_ERRATUM_845719

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Cortex-A53

</td>
<td>


\#843419

</td>
<td>


ARM64_ERRATUM_843419

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Cortex-A55

</td>
<td>


\#1024718

</td>
<td>


ARM64_ERRATUM_1024718

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Cortex-A55

</td>
<td>


\#1530923

</td>
<td>


ARM64_ERRATUM_1530923

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Cortex-A55

</td>
<td>


\#2441007

</td>
<td>


ARM64_ERRATUM_2441007

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Cortex-A57

</td>
<td>


\#832075

</td>
<td>


ARM64_ERRATUM_832075

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Cortex-A57

</td>
<td>


\#852523

</td>
<td>


N/A

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Cortex-A57

</td>
<td>


\#834220

</td>
<td>


ARM64_ERRATUM_834220

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Cortex-A57

</td>
<td>


\#1319537

</td>
<td>


ARM64_ERRATUM_1319367

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Cortex-A57

</td>
<td>


\#1742098

</td>
<td>


ARM64_ERRATUM_1742098

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Cortex-A72

</td>
<td>


\#853709

</td>
<td>


N/A

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Cortex-A72

</td>
<td>


\#1319367

</td>
<td>


ARM64_ERRATUM_1319367

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Cortex-A72

</td>
<td>


\#1655431

</td>
<td>


ARM64_ERRATUM_1742098

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Cortex-A73

</td>
<td>


\#858921

</td>
<td>


ARM64_ERRATUM_858921

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Cortex-A76

</td>
<td>


\#1188873,1418040

</td>
<td>


ARM64_ERRATUM_1418040

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Cortex-A76

</td>
<td>


\#1165522

</td>
<td>


ARM64_ERRATUM_1165522

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Cortex-A76

</td>
<td>


\#1286807

</td>
<td>


ARM64_ERRATUM_1286807

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Cortex-A76

</td>
<td>


\#1463225

</td>
<td>


ARM64_ERRATUM_1463225

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Cortex-A76

</td>
<td>


\#1490853

</td>
<td>


N/A

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Cortex-A76

</td>
<td>


\#3324349

</td>
<td>


ARM64_ERRATUM_3194386

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Cortex-A77

</td>
<td>


\#1491015

</td>
<td>


N/A

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Cortex-A77

</td>
<td>


\#1508412

</td>
<td>


ARM64_ERRATUM_1508412

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Cortex-A77

</td>
<td>


\#3324348

</td>
<td>


ARM64_ERRATUM_3194386

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Cortex-A78

</td>
<td>


\#3324344

</td>
<td>


ARM64_ERRATUM_3194386

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Cortex-A78C

</td>
<td>


\#3324346,3324347

</td>
<td>


ARM64_ERRATUM_3194386

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Cortex-A710

</td>
<td>


\#2119858

</td>
<td>


ARM64_ERRATUM_2119858

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Cortex-A710

</td>
<td>


\#2054223

</td>
<td>


ARM64_ERRATUM_2054223

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Cortex-A710

</td>
<td>


\#2224489

</td>
<td>


ARM64_ERRATUM_2224489

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Cortex-A710

</td>
<td>


\#3324338

</td>
<td>


ARM64_ERRATUM_3194386

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Cortex-A715

</td>
<td>


\#2645198

</td>
<td>


ARM64_ERRATUM_2645198

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Cortex-A715

</td>
<td>


\#3456084

</td>
<td>


ARM64_ERRATUM_3194386

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Cortex-A720

</td>
<td>


\#3456091

</td>
<td>


ARM64_ERRATUM_3194386

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Cortex-A725

</td>
<td>


\#3456106

</td>
<td>


ARM64_ERRATUM_3194386

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Cortex-X1

</td>
<td>


\#1502854

</td>
<td>


N/A

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Cortex-X1

</td>
<td>


\#3324344

</td>
<td>


ARM64_ERRATUM_3194386

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Cortex-X1C

</td>
<td>


\#3324346

</td>
<td>


ARM64_ERRATUM_3194386

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Cortex-X2

</td>
<td>


\#2119858

</td>
<td>


ARM64_ERRATUM_2119858

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Cortex-X2

</td>
<td>


\#2224489

</td>
<td>


ARM64_ERRATUM_2224489

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Cortex-X2

</td>
<td>


\#3324338

</td>
<td>


ARM64_ERRATUM_3194386

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Cortex-X3

</td>
<td>


\#3324335

</td>
<td>


ARM64_ERRATUM_3194386

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Cortex-X4

</td>
<td>


\#3194386

</td>
<td>


ARM64_ERRATUM_3194386

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Cortex-X925

</td>
<td>


\#3324334

</td>
<td>


ARM64_ERRATUM_3194386

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Neoverse-N1

</td>
<td>


\#1188873,1418040

</td>
<td>


ARM64_ERRATUM_1418040

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Neoverse-N1

</td>
<td>


\#1349291

</td>
<td>


N/A

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Neoverse-N1

</td>
<td>


\#1490853

</td>
<td>


N/A

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Neoverse-N1

</td>
<td>


\#1542419

</td>
<td>


ARM64_ERRATUM_1542419

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Neoverse-N1

</td>
<td>


\#3324349

</td>
<td>


ARM64_ERRATUM_3194386

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Neoverse-N2

</td>
<td>


\#2139208

</td>
<td>


ARM64_ERRATUM_2139208

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Neoverse-N2

</td>
<td>


\#2067961

</td>
<td>


ARM64_ERRATUM_2067961

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Neoverse-N2

</td>
<td>


\#2253138

</td>
<td>


ARM64_ERRATUM_2253138

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Neoverse-N2

</td>
<td>


\#3324339

</td>
<td>


ARM64_ERRATUM_3194386

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Neoverse-N3

</td>
<td>


\#3456111

</td>
<td>


ARM64_ERRATUM_3194386

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Neoverse-V1

</td>
<td>


\#1619801

</td>
<td>


N/A

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Neoverse-V1

</td>
<td>


\#3324341

</td>
<td>


ARM64_ERRATUM_3194386

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Neoverse-V2

</td>
<td>


\#3324336

</td>
<td>


ARM64_ERRATUM_3194386

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Neoverse-V3

</td>
<td>


\#3312417

</td>
<td>


ARM64_ERRATUM_3194386

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


Neoverse-V3AE

</td>
<td>


\#3312417

</td>
<td>


ARM64_ERRATUM_3194386

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


MMU-500

</td>
<td>


\#841119,826419 \#562869,1047329

</td>
<td>


ARM_SMMU_MMU_500_CPRE_ERRATA

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


MMU-600

</td>
<td>


\#1076982,1209401

</td>
<td>


N/A

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


MMU-700

</td>
<td>


\#2268618,2812531

</td>
<td>


N/A

</td>
</tr>
<tr>
<td>




</td>
<td>




</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


GIC-700

</td>
<td>


\#2941627

</td>
<td>


ARM64_ERRATUM_2941627

</td>
</tr>
<tr>
<td>


ARM

</td>
<td>


SI L1

</td>
<td>


\#4311569

</td>
<td>


ARM64_ERRATUM_4311569

</td>
</tr>
<tr>
<td>


Broadcom

</td>
<td>


Brahma-B53

</td>
<td>


N/A

</td>
<td>


ARM64_ERRATUM_845719

</td>
</tr>
<tr>
<td>


Broadcom

</td>
<td>


Brahma-B53

</td>
<td>


N/A

</td>
<td>


ARM64_ERRATUM_843419

</td>
</tr>
<tr>
<td>




</td>
<td>




</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


Cavium

</td>
<td>


ThunderX ITS

</td>
<td>


\#22375,24313

</td>
<td>


CAVIUM_ERRATUM_22375

</td>
</tr>
<tr>
<td>


Cavium

</td>
<td>


ThunderX ITS

</td>
<td>


\#23144

</td>
<td>


CAVIUM_ERRATUM_23144

</td>
</tr>
<tr>
<td>


Cavium

</td>
<td>


ThunderX GICv3

</td>
<td>


\#23154,38545

</td>
<td>


CAVIUM_ERRATUM_23154

</td>
</tr>
<tr>
<td>


Cavium

</td>
<td>


ThunderX GICv3

</td>
<td>


\#38539

</td>
<td>


N/A

</td>
</tr>
<tr>
<td>


Cavium

</td>
<td>


ThunderX Core

</td>
<td>


\#27456

</td>
<td>


CAVIUM_ERRATUM_27456

</td>
</tr>
<tr>
<td>


Cavium

</td>
<td>


ThunderX Core

</td>
<td>


\#30115

</td>
<td>


CAVIUM_ERRATUM_30115

</td>
</tr>
<tr>
<td>


Cavium

</td>
<td>


ThunderX SMMUv2

</td>
<td>


\#27704

</td>
<td>


N/A

</td>
</tr>
<tr>
<td>


Cavium

</td>
<td>


ThunderX2 SMMUv3

</td>
<td>


\#74

</td>
<td>


N/A

</td>
</tr>
<tr>
<td>


Cavium

</td>
<td>


ThunderX2 SMMUv3

</td>
<td>


\#126

</td>
<td>


N/A

</td>
</tr>
<tr>
<td>


Cavium

</td>
<td>


ThunderX2 Core

</td>
<td>


\#219

</td>
<td>


CAVIUM_TX2_ERRATUM_219

</td>
</tr>
<tr>
<td>




</td>
<td>




</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


Marvell

</td>
<td>


ARM-MMU-500

</td>
<td>


\#582743

</td>
<td>


N/A

</td>
</tr>
<tr>
<td>




</td>
<td>




</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


NVIDIA

</td>
<td>


Carmel Core

</td>
<td>


N/A

</td>
<td>


NVIDIA_CARMEL_CNP_ERRATUM

</td>
</tr>
<tr>
<td>


NVIDIA

</td>
<td>


T241 GICv3/4.x

</td>
<td>


T241-FABRIC-4

</td>
<td>


N/A

</td>
</tr>
<tr>
<td>




</td>
<td>




</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


Freescale/NXP

</td>
<td>


LS2080A/LS1043A

</td>
<td>


A-008585

</td>
<td>


FSL_ERRATUM_A008585

</td>
</tr>
<tr>
<td>




</td>
<td>




</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


Hisilicon

</td>
<td>


Hip0\{5,6,7\}

</td>
<td>


\#161010101

</td>
<td>


HISILICON_ERRATUM_161010101

</td>
</tr>
<tr>
<td>


Hisilicon

</td>
<td>


Hip0\{6,7\}

</td>
<td>


\#161010701

</td>
<td>


N/A

</td>
</tr>
<tr>
<td>


Hisilicon

</td>
<td>


Hip0\{6,7\}

</td>
<td>


\#161010803

</td>
<td>


N/A

</td>
</tr>
<tr>
<td>


Hisilicon

</td>
<td>


Hip07

</td>
<td>


\#161600802

</td>
<td>


HISILICON_ERRATUM_161600802

</td>
</tr>
<tr>
<td>


Hisilicon

</td>
<td>


Hip08 SMMU PMCG

</td>
<td>


\#162001800

</td>
<td>


N/A

</td>
</tr>
<tr>
<td>


Hisilicon

</td>
<td>


Hip\{08,09,09A,10 ,10C,11\} SMMU PMCG

</td>
<td>


\#162001900

</td>
<td>


N/A

</td>
</tr>
<tr>
<td>


Hisilicon

</td>
<td>


Hip09

</td>
<td>


\#162100801

</td>
<td>


HISILICON_ERRATUM_162100801

</td>
</tr>
<tr>
<td>




</td>
<td>




</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


Qualcomm Tech.

</td>
<td>


Kryo/Falkor v1

</td>
<td>


E1003

</td>
<td>


QCOM_FALKOR_ERRATUM_1003

</td>
</tr>
<tr>
<td>


Qualcomm Tech.

</td>
<td>


Kryo/Falkor v1

</td>
<td>


E1009

</td>
<td>


QCOM_FALKOR_ERRATUM_1009

</td>
</tr>
<tr>
<td>


Qualcomm Tech.

</td>
<td>


QDF2400 ITS

</td>
<td>


E0065

</td>
<td>


QCOM_QDF2400_ERRATUM_0065

</td>
</tr>
<tr>
<td>


Qualcomm Tech.

</td>
<td>


Falkor v\{1,2\}

</td>
<td>


E1041

</td>
<td>


QCOM_FALKOR_ERRATUM_1041

</td>
</tr>
<tr>
<td>


Qualcomm Tech.

</td>
<td>


Kryo4xx Gold

</td>
<td>


N/A

</td>
<td>


ARM64_ERRATUM_1463225

</td>
</tr>
<tr>
<td>


Qualcomm Tech.

</td>
<td>


Kryo4xx Gold

</td>
<td>


N/A

</td>
<td>


ARM64_ERRATUM_1418040

</td>
</tr>
<tr>
<td>


Qualcomm Tech.

</td>
<td>


Kryo4xx Silver

</td>
<td>


N/A

</td>
<td>


ARM64_ERRATUM_1530923

</td>
</tr>
<tr>
<td>


Qualcomm Tech.

</td>
<td>


Kryo4xx Silver

</td>
<td>


N/A

</td>
<td>


ARM64_ERRATUM_1024718

</td>
</tr>
<tr>
<td>


Qualcomm Tech.

</td>
<td>


Kryo4xx Gold

</td>
<td>


N/A

</td>
<td>


ARM64_ERRATUM_1286807

</td>
</tr>
<tr>
<td>




</td>
<td>




</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


Rockchip

</td>
<td>


RK3588

</td>
<td>


\#3588001

</td>
<td>


ROCKCHIP_ERRATUM_3588001

</td>
</tr>
<tr>
<td>


Rockchip

</td>
<td>


RK3568

</td>
<td>


\#3568002

</td>
<td>


ROCKCHIP_ERRATUM_3568002

</td>
</tr>
<tr>
<td>




</td>
<td>




</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


Fujitsu

</td>
<td>


A64FX

</td>
<td>


E\#010001

</td>
<td>


FUJITSU_ERRATUM_010001

</td>
</tr>
<tr>
<td>




</td>
<td>




</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


ASR

</td>
<td>


ASR8601

</td>
<td>


\#8601001

</td>
<td>


N/A

</td>
</tr>
<tr>
<td>




</td>
<td>




</td>
<td>




</td>
<td>




</td>
</tr>
<tr>
<td>


Microsoft

</td>
<td>


Azure Cobalt 100

</td>
<td>


\#2139208

</td>
<td>


ARM64_ERRATUM_2139208

</td>
</tr>
<tr>
<td>


Microsoft

</td>
<td>


Azure Cobalt 100

</td>
<td>


\#2067961

</td>
<td>


ARM64_ERRATUM_2067961

</td>
</tr>
<tr>
<td>


Microsoft

</td>
<td>


Azure Cobalt 100

</td>
<td>


\#2253138

</td>
<td>


ARM64_ERRATUM_2253138

</td>
</tr>
<tr>
<td>


Microsoft

</td>
<td>


Azure Cobalt 100

</td>
<td>


\#3324339

</td>
<td>


ARM64_ERRATUM_3194386

</td>
</tr>
</tbody>
</table>
