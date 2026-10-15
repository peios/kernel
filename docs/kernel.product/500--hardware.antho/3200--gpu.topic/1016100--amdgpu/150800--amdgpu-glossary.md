---
title: "AMDGPU Glossary"
type: reference
description: "Here you can find some generic acronyms used in the amdgpu driver. Notice that we have a dedicated glossary for Display Core at 'Documentation/gpu/amdgpu/display/dc-glossary.rst'."
---

<a id="rst-amdgpu-glossary"></a>

Here you can find some generic acronyms used in the amdgpu driver. Notice that we have a dedicated glossary for Display Core at '[Documentation/gpu/amdgpu/display/dc-glossary.rst](~kernel/hardware/gpu/amdgpu-display/dc-glossary)'.



- **<a id="rst-term-active-cu-number"></a>active\_cu\_number**

  The number of CUs that are active on the system.  The number of active CUs may be less than SE \* SH \* CU depending on the board configuration.

- **<a id="rst-term-baco"></a>BACO**

  Bus Alive, Chip Off

- **<a id="rst-term-boco"></a>BOCO**

  Bus Off, Chip Off

- **<a id="rst-term-ce"></a>CE**

  Constant Engine

- **<a id="rst-term-cik"></a>CIK**

  Sea Islands

- **<a id="rst-term-cb"></a>CB**

  Color Buffer

- **<a id="rst-term-cp"></a>CP**

  Command Processor

- **<a id="rst-term-cpc"></a>CPC**

  Command Processor Compute

- **<a id="rst-term-cpf"></a>CPF**

  Command Processor Fetch

- **<a id="rst-term-cpg"></a>CPG**

  Command Processor Graphics

- **<a id="rst-term-cplib"></a>CPLIB**

  Content Protection Library

- **<a id="rst-term-cs"></a>CS**

  Command Submission

- **<a id="rst-term-csb"></a>CSB**

  Clear State Indirect Buffer

- **<a id="rst-term-cu"></a>CU**

  Compute Unit

- **<a id="rst-term-db"></a>DB**

  Depth Buffer

- **<a id="rst-term-dfs"></a>DFS**

  Digital Frequency Synthesizer

- **<a id="rst-term-ecp"></a>ECP**

  Enhanced Content Protection

- **<a id="rst-term-eop"></a>EOP**

  End Of Pipe/Pipeline

- **<a id="rst-term-flr"></a>FLR**

  Function Level Reset

- **<a id="rst-term-gart"></a>GART**

  Graphics Address Remapping Table.  This is the name we use for the GPUVM page table used by the GPU kernel driver.  It remaps system resources (memory or MMIO space) into the GPU's address space so the GPU can access them.  The name GART harkens back to the days of AGP when the platform provided an MMU that the GPU could use to get a contiguous view of scattered pages for DMA.  The MMU has since moved on to the GPU, but the name stuck.

- **<a id="rst-term-gc"></a>GC**

  Graphics and Compute

- **<a id="rst-term-gds"></a>GDS**

  Global Data Share

- **<a id="rst-term-ge"></a>GE**

  Geometry Engine

- **<a id="rst-term-gmc"></a>GMC**

  Graphic Memory Controller

- **<a id="rst-term-gpr"></a>GPR**

  General Purpose Register

- **<a id="rst-term-gpuvm"></a>GPUVM**

  GPU Virtual Memory.  This is the GPU's MMU.  The GPU supports multiple virtual address spaces that can be in flight at any given time.  These allow the GPU to remap VRAM and system resources into GPU virtual address spaces for use by the GPU kernel driver and applications using the GPU. These provide memory protection for different applications using the GPU.

- **<a id="rst-term-gtt"></a>GTT**

  Graphics Translation Tables.  This is a memory pool managed through TTM which provides access to system resources (memory or MMIO space) for use by the GPU. These addresses can be mapped into the "GART" GPUVM page table for use by the kernel driver or into per process GPUVM page tables for application usage.

- **<a id="rst-term-gws"></a>GWS**

  Global Wave Sync

- **<a id="rst-term-ih"></a>IH**

  Interrupt Handler

- **<a id="rst-term-iv"></a>IV**

  Interrupt Vector

- **<a id="rst-term-hqd"></a>HQD**

  Hardware Queue Descriptor

- **<a id="rst-term-ib"></a>IB**

  Indirect Buffer

- **<a id="rst-term-imu"></a>IMU**

  Integrated Management Unit (Power Management support)

- **<a id="rst-term-ip"></a>IP**

  Intellectual Property blocks

- **<a id="rst-term-kcq"></a>KCQ**

  Kernel Compute Queue

- **<a id="rst-term-kfd"></a>KFD**

  Kernel Fusion Driver

- **<a id="rst-term-kgq"></a>KGQ**

  Kernel Graphics Queue

- **<a id="rst-term-kiq"></a>KIQ**

  Kernel Interface Queue

- **<a id="rst-term-mc"></a>MC**

  Memory Controller

- **<a id="rst-term-mcbp"></a>MCBP**

  Mid Command Buffer Preemption

- **<a id="rst-term-me"></a>ME**

  MicroEngine (Graphics)

- **<a id="rst-term-mec"></a>MEC**

  MicroEngine Compute

- **<a id="rst-term-mes"></a>MES**

  MicroEngine Scheduler

- **<a id="rst-term-mmhub"></a>MMHUB**

  Multi-Media HUB

- **<a id="rst-term-mqd"></a>MQD**

  Memory Queue Descriptor

- **<a id="rst-term-pa"></a>PA**

  Primitive Assembler / Physical Address

- **<a id="rst-term-pde"></a>PDE**

  Page Directory Entry

- **<a id="rst-term-pfp"></a>PFP**

  Pre-Fetch Parser (Graphics)

- **<a id="rst-term-pplib"></a>PPLib**

  PowerPlay Library - PowerPlay is the power management component.

- **<a id="rst-term-prt"></a>PRT**

  Partially Resident Texture (also known as sparse residency)

- **<a id="rst-term-psp"></a>PSP**

  Platform Security Processor

- **<a id="rst-term-pte"></a>PTE**

  Page Table Entry

- **<a id="rst-term-rb"></a>RB**

  Render Backends. Some people called it ROPs.

- **<a id="rst-term-rlc"></a>RLC**

  RunList Controller. This name is a remnant of past ages and doesn't have much meaning today. It's a group of general-purpose helper engines for the GFX block. It's involved in GFX power management and SR-IOV, among other things.

- **<a id="rst-term-sc"></a>SC**

  Scan Converter

- **<a id="rst-term-sdma"></a>SDMA**

  System DMA

- **<a id="rst-term-se"></a>SE**

  Shader Engine

- **<a id="rst-term-sgpr"></a>SGPR**

  Scalar General-Purpose Registers

- **<a id="rst-term-sh"></a>SH**

  SHader array

- **<a id="rst-term-si"></a>SI**

  Southern Islands

- **<a id="rst-term-smu-smc"></a>SMU/SMC**

  System Management Unit / System Management Controller

- **<a id="rst-term-spi-amdgpu"></a>SPI (AMDGPU)**

  Shader Processor Input

- **<a id="rst-term-srlc"></a>SRLC**

  Save/Restore List Control

- **<a id="rst-term-srlg"></a>SRLG**

  Save/Restore List GPM\_MEM

- **<a id="rst-term-srls"></a>SRLS**

  Save/Restore List SRM\_MEM

- **<a id="rst-term-ss"></a>SS**

  Spread Spectrum

- **<a id="rst-term-sx"></a>SX**

  Shader Export

- **<a id="rst-term-ta"></a>TA**

  Trusted Application

- **<a id="rst-term-tc"></a>TC**

  Texture Cache

- **<a id="rst-term-tcp-amdgpu"></a>TCP (AMDGPU)**

  Texture Cache per Pipe. Even though the name "Texture" is part of this acronym, the TCP represents the path to memory shaders; i.e., it is not related to texture. The name is a leftover from older designs where shader stages had different cache designs; it refers to the L1 cache in older architectures.

- **<a id="rst-term-tmr"></a>TMR**

  Trusted Memory Region

- **<a id="rst-term-tmz"></a>TMZ**

  Trusted Memory Zone

- **<a id="rst-term-toc"></a>TOC**

  Table of Contents

- **<a id="rst-term-umc"></a>UMC**

  Unified Memory Controller

- **<a id="rst-term-umsch"></a>UMSCH**

  User Mode Scheduler

- **<a id="rst-term-utc-amdgpu"></a>UTC (AMDGPU)**

  Unified Translation Cache. UTC is equivalent to TLB. You might see a variation of this acronym with L at the end, i.e., UTCL followed by a number; L means the cache level (e.g., UTCL1 and UTCL2).

- **<a id="rst-term-uvd"></a>UVD**

  Unified Video Decoder

- **<a id="rst-term-vce"></a>VCE**

  Video Compression Engine

- **<a id="rst-term-vcn"></a>VCN**

  Video Codec Next

- **<a id="rst-term-vgpr"></a>VGPR**

  Vector General-Purpose Registers

- **<a id="rst-term-vmid"></a>VMID**

  Virtual Memory ID

- **<a id="rst-term-vpe"></a>VPE**

  Video Processing Engine

- **<a id="rst-term-xcc"></a>XCC**

  Accelerator Core Complex

- **<a id="rst-term-xcp"></a>XCP**

  Accelerator Core Partition
