---
title: "AACRAID Driver for Linux (take two)"
type: reference
description: "The aacraid driver adds support for Adaptec (http://www.adaptec.com) RAID controllers. This is a major rewrite from the original Adaptec supplied driver. It has significantly cleaned up both the code and the running binary size (the module…"
---

<a id="rst-aacraid-driver-for-linux-take-two"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

<a id="rst-introduction"></a>

## Introduction

The aacraid driver adds support for Adaptec ([http://www.adaptec.com](<http://www.adaptec.com>)) RAID controllers. This is a major rewrite from the original Adaptec supplied driver. It has significantly cleaned up both the code and the running binary size (the module is less than half the size of the original).

<a id="rst-supported-cards-chipsets"></a>

## Supported Cards/Chipsets

>
> <table>
> <thead>
> <tr>
> <th>
>
>
> PCI ID (pci.ids)
>
> </th>
> <th>
>
>
> OEM
>
> </th>
> <th>
>
>
> Product
>
> </th>
> </tr>
> </thead>
> <tbody>
> <tr>
> <td>
>
>
> 9005:0285:9005:0285
>
> </td>
> <td>
>
>
> Adaptec
>
> </td>
> <td>
>
>
> 2200S (Vulcan)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:9005:0286
>
> </td>
> <td>
>
>
> Adaptec
>
> </td>
> <td>
>
>
> 2120S (Crusader)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:9005:0287
>
> </td>
> <td>
>
>
> Adaptec
>
> </td>
> <td>
>
>
> 2200S (Vulcan-2m)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:9005:0288
>
> </td>
> <td>
>
>
> Adaptec
>
> </td>
> <td>
>
>
> 3230S (Harrier)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:9005:0289
>
> </td>
> <td>
>
>
> Adaptec
>
> </td>
> <td>
>
>
> 3240S (Tornado)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:9005:028a
>
> </td>
> <td>
>
>
> Adaptec
>
> </td>
> <td>
>
>
> 2020ZCR (Skyhawk)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:9005:028b
>
> </td>
> <td>
>
>
> Adaptec
>
> </td>
> <td>
>
>
> 2025ZCR (Terminator)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0286:9005:028c
>
> </td>
> <td>
>
>
> Adaptec
>
> </td>
> <td>
>
>
> 2230S (Lancer)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0286:9005:028c
>
> </td>
> <td>
>
>
> Adaptec
>
> </td>
> <td>
>
>
> 2230SLP (Lancer)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0286:9005:028d
>
> </td>
> <td>
>
>
> Adaptec
>
> </td>
> <td>
>
>
> 2130S (Lancer)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:9005:028e
>
> </td>
> <td>
>
>
> Adaptec
>
> </td>
> <td>
>
>
> 2020SA (Skyhawk)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:9005:028f
>
> </td>
> <td>
>
>
> Adaptec
>
> </td>
> <td>
>
>
> 2025SA (Terminator)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:9005:0290
>
> </td>
> <td>
>
>
> Adaptec
>
> </td>
> <td>
>
>
> 2410SA (Jaguar)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:103c:3227
>
> </td>
> <td>
>
>
> Adaptec
>
> </td>
> <td>
>
>
> 2610SA (Bearcat HP release)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:9005:0293
>
> </td>
> <td>
>
>
> Adaptec
>
> </td>
> <td>
>
>
> 21610SA (Corsair-16)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:9005:0296
>
> </td>
> <td>
>
>
> Adaptec
>
> </td>
> <td>
>
>
> 2240S (SabreExpress)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:9005:0292
>
> </td>
> <td>
>
>
> Adaptec
>
> </td>
> <td>
>
>
> 2810SA (Corsair-8)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:9005:0297
>
> </td>
> <td>
>
>
> Adaptec
>
> </td>
> <td>
>
>
> 4005 (AvonPark)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:9005:0298
>
> </td>
> <td>
>
>
> Adaptec
>
> </td>
> <td>
>
>
> 4000 (BlackBird)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:9005:0299
>
> </td>
> <td>
>
>
> Adaptec
>
> </td>
> <td>
>
>
> 4800SAS (Marauder-X)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:9005:029a
>
> </td>
> <td>
>
>
> Adaptec
>
> </td>
> <td>
>
>
> 4805SAS (Marauder-E)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0286:9005:029b
>
> </td>
> <td>
>
>
> Adaptec
>
> </td>
> <td>
>
>
> 2820SA (Intruder)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0286:9005:029c
>
> </td>
> <td>
>
>
> Adaptec
>
> </td>
> <td>
>
>
> 2620SA (Intruder)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0286:9005:029d
>
> </td>
> <td>
>
>
> Adaptec
>
> </td>
> <td>
>
>
> 2420SA (Intruder HP release)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0286:9005:02ac
>
> </td>
> <td>
>
>
> Adaptec
>
> </td>
> <td>
>
>
> 1800 (Typhoon44)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:9005:02b5
>
> </td>
> <td>
>
>
> Adaptec
>
> </td>
> <td>
>
>
> 5445 (Voodoo44)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:15d9:02b5
>
> </td>
> <td>
>
>
> SMC
>
> </td>
> <td>
>
>
> AOC-USAS-S4i
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:9005:02b6
>
> </td>
> <td>
>
>
> Adaptec
>
> </td>
> <td>
>
>
> 5805 (Voodoo80)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:15d9:02b6
>
> </td>
> <td>
>
>
> SMC
>
> </td>
> <td>
>
>
> AOC-USAS-S8i
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:9005:02b7
>
> </td>
> <td>
>
>
> Adaptec
>
> </td>
> <td>
>
>
> 5085 (Voodoo08)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:9005:02bb
>
> </td>
> <td>
>
>
> Adaptec
>
> </td>
> <td>
>
>
> 3405 (Marauder40LP)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:9005:02bc
>
> </td>
> <td>
>
>
> Adaptec
>
> </td>
> <td>
>
>
> 3805 (Marauder80LP)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:9005:02c7
>
> </td>
> <td>
>
>
> Adaptec
>
> </td>
> <td>
>
>
> 3085 (Marauder08ELP)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:9005:02bd
>
> </td>
> <td>
>
>
> Adaptec
>
> </td>
> <td>
>
>
> 31205 (Marauder120)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:9005:02be
>
> </td>
> <td>
>
>
> Adaptec
>
> </td>
> <td>
>
>
> 31605 (Marauder160)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:9005:02c3
>
> </td>
> <td>
>
>
> Adaptec
>
> </td>
> <td>
>
>
> 51205 (Voodoo120)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:9005:02c4
>
> </td>
> <td>
>
>
> Adaptec
>
> </td>
> <td>
>
>
> 51605 (Voodoo160)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:15d9:02c9
>
> </td>
> <td>
>
>
> SMC
>
> </td>
> <td>
>
>
> AOC-USAS-S4iR
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:15d9:02ca
>
> </td>
> <td>
>
>
> SMC
>
> </td>
> <td>
>
>
> AOC-USAS-S8iR
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:9005:02ce
>
> </td>
> <td>
>
>
> Adaptec
>
> </td>
> <td>
>
>
> 51245 (Voodoo124)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:9005:02cf
>
> </td>
> <td>
>
>
> Adaptec
>
> </td>
> <td>
>
>
> 51645 (Voodoo164)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:9005:02d0
>
> </td>
> <td>
>
>
> Adaptec
>
> </td>
> <td>
>
>
> 52445 (Voodoo244)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:9005:02d1
>
> </td>
> <td>
>
>
> Adaptec
>
> </td>
> <td>
>
>
> 5405 (Voodoo40)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:15d9:02d2
>
> </td>
> <td>
>
>
> SMC
>
> </td>
> <td>
>
>
> AOC-USAS-S8i-LP
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:15d9:02d3
>
> </td>
> <td>
>
>
> SMC
>
> </td>
> <td>
>
>
> AOC-USAS-S8iR-LP
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:9005:02d4
>
> </td>
> <td>
>
>
> Adaptec
>
> </td>
> <td>
>
>
> ASR-2045 (Voodoo04 Lite)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:9005:02d5
>
> </td>
> <td>
>
>
> Adaptec
>
> </td>
> <td>
>
>
> ASR-2405 (Voodoo40 Lite)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:9005:02d6
>
> </td>
> <td>
>
>
> Adaptec
>
> </td>
> <td>
>
>
> ASR-2445 (Voodoo44 Lite)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:9005:02d7
>
> </td>
> <td>
>
>
> Adaptec
>
> </td>
> <td>
>
>
> ASR-2805 (Voodoo80 Lite)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:9005:02d8
>
> </td>
> <td>
>
>
> Adaptec
>
> </td>
> <td>
>
>
> 5405Z (Voodoo40 BLBU)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:9005:02d9
>
> </td>
> <td>
>
>
> Adaptec
>
> </td>
> <td>
>
>
> 5445Z (Voodoo44 BLBU)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:9005:02da
>
> </td>
> <td>
>
>
> Adaptec
>
> </td>
> <td>
>
>
> 5805Z (Voodoo80 BLBU)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 1011:0046:9005:0364
>
> </td>
> <td>
>
>
> Adaptec
>
> </td>
> <td>
>
>
> 5400S (Mustang)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 1011:0046:9005:0365
>
> </td>
> <td>
>
>
> Adaptec
>
> </td>
> <td>
>
>
> 5400S (Mustang)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0287:9005:0800
>
> </td>
> <td>
>
>
> Adaptec
>
> </td>
> <td>
>
>
> Themisto (Jupiter)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0200:9005:0200
>
> </td>
> <td>
>
>
> Adaptec
>
> </td>
> <td>
>
>
> Themisto (Jupiter)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0286:9005:0800
>
> </td>
> <td>
>
>
> Adaptec
>
> </td>
> <td>
>
>
> Callisto (Jupiter)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 1011:0046:9005:1364
>
> </td>
> <td>
>
>
> Dell
>
> </td>
> <td>
>
>
> PERC 2/QC (Quad Channel, Mustang)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 1011:0046:9005:1365
>
> </td>
> <td>
>
>
> Dell
>
> </td>
> <td>
>
>
> PERC 2/QC (Quad Channel, Mustang)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 1028:0001:1028:0001
>
> </td>
> <td>
>
>
> Dell
>
> </td>
> <td>
>
>
> PERC 2/Si (Iguana)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 1028:0003:1028:0003
>
> </td>
> <td>
>
>
> Dell
>
> </td>
> <td>
>
>
> PERC 3/Si (SlimFast)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 1028:0002:1028:0002
>
> </td>
> <td>
>
>
> Dell
>
> </td>
> <td>
>
>
> PERC 3/Di (Opal)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 1028:0004:1028:0004
>
> </td>
> <td>
>
>
> Dell
>
> </td>
> <td>
>
>
> PERC 3/SiF (Iguana)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 1028:0004:1028:00d0
>
> </td>
> <td>
>
>
> Dell
>
> </td>
> <td>
>
>
> PERC 3/DiF (Iguana)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 1028:0002:1028:00d1
>
> </td>
> <td>
>
>
> Dell
>
> </td>
> <td>
>
>
> PERC 3/DiV (Viper)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 1028:0002:1028:00d9
>
> </td>
> <td>
>
>
> Dell
>
> </td>
> <td>
>
>
> PERC 3/DiL (Lexus)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 1028:000a:1028:0106
>
> </td>
> <td>
>
>
> Dell
>
> </td>
> <td>
>
>
> PERC 3/DiJ (Jaguar)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 1028:000a:1028:011b
>
> </td>
> <td>
>
>
> Dell
>
> </td>
> <td>
>
>
> PERC 3/DiD (Dagger)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 1028:000a:1028:0121
>
> </td>
> <td>
>
>
> Dell
>
> </td>
> <td>
>
>
> PERC 3/DiB (Boxster)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:1028:0287
>
> </td>
> <td>
>
>
> Dell
>
> </td>
> <td>
>
>
> PERC 320/DC (Vulcan)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:1028:0291
>
> </td>
> <td>
>
>
> Dell
>
> </td>
> <td>
>
>
> CERC 2 (DellCorsair)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 1011:0046:103c:10c2
>
> </td>
> <td>
>
>
> HP
>
> </td>
> <td>
>
>
> NetRAID-4M (Mustang)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:17aa:0286
>
> </td>
> <td>
>
>
> Legend
>
> </td>
> <td>
>
>
> S220 (Crusader)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:17aa:0287
>
> </td>
> <td>
>
>
> Legend
>
> </td>
> <td>
>
>
> S230 (Vulcan)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:9005:0290
>
> </td>
> <td>
>
>
> IBM
>
> </td>
> <td>
>
>
> ServeRAID 7t (Jaguar)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:1014:02F2
>
> </td>
> <td>
>
>
> IBM
>
> </td>
> <td>
>
>
> ServeRAID 8i (AvonPark)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0286:1014:9540
>
> </td>
> <td>
>
>
> IBM
>
> </td>
> <td>
>
>
> ServeRAID 8k/8k-l4 (AuroraLite)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0286:1014:9580
>
> </td>
> <td>
>
>
> IBM
>
> </td>
> <td>
>
>
> ServeRAID 8k/8k-l8 (Aurora)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:1014:034d
>
> </td>
> <td>
>
>
> IBM
>
> </td>
> <td>
>
>
> ServeRAID 8s (Marauder-E)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0286:9005:029e
>
> </td>
> <td>
>
>
> ICP
>
> </td>
> <td>
>
>
> ICP9024RO (Lancer)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0286:9005:029f
>
> </td>
> <td>
>
>
> ICP
>
> </td>
> <td>
>
>
> ICP9014RO (Lancer)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0286:9005:02a0
>
> </td>
> <td>
>
>
> ICP
>
> </td>
> <td>
>
>
> ICP9047MA (Lancer)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0286:9005:02a1
>
> </td>
> <td>
>
>
> ICP
>
> </td>
> <td>
>
>
> ICP9087MA (Lancer)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:9005:02a4
>
> </td>
> <td>
>
>
> ICP
>
> </td>
> <td>
>
>
> ICP9085LI (Marauder-X)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:9005:02a5
>
> </td>
> <td>
>
>
> ICP
>
> </td>
> <td>
>
>
> ICP5085BR (Marauder-E)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0286:9005:02a6
>
> </td>
> <td>
>
>
> ICP
>
> </td>
> <td>
>
>
> ICP9067MA (Intruder-6)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:9005:02b2
>
> </td>
> <td>
>
>
> ICP
>
> </td>
> <td>
>
>
> (Voodoo 8 internal 8 external)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:9005:02b8
>
> </td>
> <td>
>
>
> ICP
>
> </td>
> <td>
>
>
> ICP5445SL (Voodoo44)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:9005:02b9
>
> </td>
> <td>
>
>
> ICP
>
> </td>
> <td>
>
>
> ICP5085SL (Voodoo80)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:9005:02ba
>
> </td>
> <td>
>
>
> ICP
>
> </td>
> <td>
>
>
> ICP5805SL (Voodoo08)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:9005:02bf
>
> </td>
> <td>
>
>
> ICP
>
> </td>
> <td>
>
>
> ICP5045BL (Marauder40LP)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:9005:02c0
>
> </td>
> <td>
>
>
> ICP
>
> </td>
> <td>
>
>
> ICP5085BL (Marauder80LP)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:9005:02c8
>
> </td>
> <td>
>
>
> ICP
>
> </td>
> <td>
>
>
> ICP5805BL (Marauder08ELP)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:9005:02c1
>
> </td>
> <td>
>
>
> ICP
>
> </td>
> <td>
>
>
> ICP5125BR (Marauder120)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:9005:02c2
>
> </td>
> <td>
>
>
> ICP
>
> </td>
> <td>
>
>
> ICP5165BR (Marauder160)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:9005:02c5
>
> </td>
> <td>
>
>
> ICP
>
> </td>
> <td>
>
>
> ICP5125SL (Voodoo120)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:9005:02c6
>
> </td>
> <td>
>
>
> ICP
>
> </td>
> <td>
>
>
> ICP5165SL (Voodoo160)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0286:9005:02ab
>
> </td>
> <td>
>
>
>
>
> </td>
> <td>
>
>
> (Typhoon40)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0286:9005:02ad
>
> </td>
> <td>
>
>
>
>
> </td>
> <td>
>
>
> (Aurora ARK)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0286:9005:02ae
>
> </td>
> <td>
>
>
>
>
> </td>
> <td>
>
>
> (Aurora Lite ARK)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:9005:02b0
>
> </td>
> <td>
>
>
>
>
> </td>
> <td>
>
>
> (Sunrise Lake ARK)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:9005:02b1
>
> </td>
> <td>
>
>
> Adaptec
>
> </td>
> <td>
>
>
> (Voodoo 8 internal 8 external)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:108e:7aac
>
> </td>
> <td>
>
>
> SUN
>
> </td>
> <td>
>
>
> STK RAID REM (Voodoo44 Coyote)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:108e:0286
>
> </td>
> <td>
>
>
> SUN
>
> </td>
> <td>
>
>
> STK RAID INT (Cougar)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:108e:0287
>
> </td>
> <td>
>
>
> SUN
>
> </td>
> <td>
>
>
> STK RAID EXT (Prometheus)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 9005:0285:108e:7aae
>
> </td>
> <td>
>
>
> SUN
>
> </td>
> <td>
>
>
> STK RAID EM (Narvi)
>
> </td>
> </tr>
> </tbody>
> </table>

<a id="rst-people"></a>

## People

Alan Cox &lt;[alan@lxorguk.ukuu.org.uk](<mailto:alan@lxorguk.ukuu.org.uk>)&gt;

Christoph Hellwig &lt;[hch@infradead.org](<mailto:hch@infradead.org>)&gt;

- updates for new-style PCI probing and SCSI host registration, small cleanups/fixes

Matt Domsch &lt;[matt_domsch@dell.com](<mailto:matt_domsch@dell.com>)&gt;

- revision ioctl, adapter messages

Deanna Bonds

- non-DASD support, PAE fibs and 64 bit, added new adaptec controllers added new ioctls, changed scsi interface to use new error handler, increased the number of fibs and outstanding commands to a container

- fixed 64bit and 64G memory model, changed confusing naming convention where fibs that go to the hardware are consistently called hw_fibs and not just fibs like the name of the driver tracking structure

Mark Salyzyn &lt;[Mark_Salyzyn@adaptec.com](<mailto:Mark_Salyzyn@adaptec.com>)&gt;

- Fixed panic issues and added some new product ids for upcoming hbas.

- Performance tuning, card failover and bug mitigations.

Achim Leubner &lt;[Achim_Leubner@adaptec.com](<mailto:Achim_Leubner@adaptec.com>)&gt;

- Original Driver

---

Adaptec Unix OEM Product Group

<a id="rst-mailing-list"></a>

## Mailing List

[linux-scsi@vger.kernel.org](<mailto:linux-scsi@vger.kernel.org>) (Interested parties troll here) Also note this is very different to Brian's original driver so don't expect him to support it.

Adaptec does support this driver.  Contact Adaptec tech support or [aacraid@adaptec.com](<mailto:aacraid@adaptec.com>)

Original by Brian Boerner February 2001

Rewritten by Alan Cox, November 2001
