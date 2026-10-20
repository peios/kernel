---
title: "ACPI Tables"
type: reference
description: "The expectations of individual ACPI tables are discussed in the list that follows."
---

<a id="rst-acpi-tables"></a>

The expectations of individual ACPI tables are discussed in the list that follows.

If a section number is used, it refers to a section number in the ACPI specification where the object is defined.  If "Signature Reserved" is used, the table signature (the first four bytes of the table) is the only portion of the table recognized by the specification, and the actual table is defined outside of the UEFI Forum (see Section 5.2.6 of the specification).

For ACPI on arm64, tables also fall into the following categories:

> - Required: DSDT, FADT, GTDT, MADT, MCFG, RSDP, SPCR, XSDT
>
> - Recommended: BERT, EINJ, ERST, HEST, PCCT, SSDT
>
> - Optional: AGDI, BGRT, CEDT, CPEP, CSRT, DBG2, DRTM, ECDT, FACS, FPDT, HMAT, IBFT, IORT, MCHI, MPAM, MPST, MSCT, NFIT, PMTT, PPTT, RASF, SBST, SDEI, SLIT, SPMI, SRAT, STAO, TCPA, TPM2, UEFI, XENV
>
> - Not supported: AEST, APMT, BOOT, DBGP, DMAR, ETDT, HPET, IVRS, LPIT, MSDM, OEMx, PDTT, PSDT, RAS2, RSDT, SLIC, WAET, WDAT, WDRT, WPBT


<table>
<thead>
<tr>
<th>


Table

</th>
<th>


Usage for ARMv8 Linux

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


AEST

</td>
<td>


Signature Reserved (signature == "AEST")

**Arm Error Source Table**

This table informs the OS of any error nodes in the system that are compliant with the Arm RAS architecture.

</td>
</tr>
<tr>
<td>


AGDI

</td>
<td>


Signature Reserved (signature == "AGDI")

**Arm Generic diagnostic Dump and Reset Device Interface Table**

This table describes a non-maskable event, that is used by the platform firmware, to request the OS to generate a diagnostic dump and reset the device.

</td>
</tr>
<tr>
<td>


APMT

</td>
<td>


Signature Reserved (signature == "APMT")

**Arm Performance Monitoring Table**

This table describes the properties of PMU support implemented by components in the system.

</td>
</tr>
<tr>
<td>


BERT

</td>
<td>


Section 18.3 (signature == "BERT")

**Boot Error Record Table**

Must be supplied if RAS support is provided by the platform.  It is recommended this table be supplied.

</td>
</tr>
<tr>
<td>


BOOT

</td>
<td>


Signature Reserved (signature == "BOOT")

**simple BOOT flag table**

Microsoft only table, will not be supported.

</td>
</tr>
<tr>
<td>


BGRT

</td>
<td>


Section 5.2.22 (signature == "BGRT")

**Boot Graphics Resource Table**

Optional, not currently supported, with no real use-case for an ARM server.

</td>
</tr>
<tr>
<td>


CEDT

</td>
<td>


Signature Reserved (signature == "CEDT")

**CXL Early Discovery Table**

This table allows the OS to discover any CXL Host Bridges and the Host Bridge registers.

</td>
</tr>
<tr>
<td>


CPEP

</td>
<td>


Section 5.2.18 (signature == "CPEP")

**Corrected Platform Error Polling table**

Optional, not currently supported, and not recommended until such time as ARM-compatible hardware is available, and the specification suitably modified.

</td>
</tr>
<tr>
<td>


CSRT

</td>
<td>


Signature Reserved (signature == "CSRT")

**Core System Resources Table**

Optional, not currently supported.

</td>
</tr>
<tr>
<td>


DBG2

</td>
<td>


Signature Reserved (signature == "DBG2")

**DeBuG port table 2**

License has changed and should be usable.  Optional if used instead of earlycon=&lt;device&gt; on the command line.

</td>
</tr>
<tr>
<td>


DBGP

</td>
<td>


Signature Reserved (signature == "DBGP")

**DeBuG Port table**

Microsoft only table, will not be supported.

</td>
</tr>
<tr>
<td>


DSDT

</td>
<td>


Section 5.2.11.1 (signature == "DSDT")

**Differentiated System Description Table**

A DSDT is required; see also SSDT.

ACPI tables contain only one DSDT but can contain one or more SSDTs, which are optional.  Each SSDT can only add to the ACPI namespace, but cannot modify or replace anything in the DSDT.

</td>
</tr>
<tr>
<td>


DMAR

</td>
<td>


Signature Reserved (signature == "DMAR")

**DMA Remapping table**

x86 only table, will not be supported.

</td>
</tr>
<tr>
<td>


DRTM

</td>
<td>


Signature Reserved (signature == "DRTM")

**Dynamic Root of Trust for Measurement table**

Optional, not currently supported.

</td>
</tr>
<tr>
<td>


ECDT

</td>
<td>


Section 5.2.16 (signature == "ECDT")

**Embedded Controller Description Table**

Optional, not currently supported, but could be used on ARM if and only if one uses the GPE_BIT field to represent an IRQ number, since there are no GPE blocks defined in hardware reduced mode.  This would need to be modified in the ACPI specification.

</td>
</tr>
<tr>
<td>


EINJ

</td>
<td>


Section 18.6 (signature == "EINJ")

**Error Injection table**

This table is very useful for testing platform response to error conditions; it allows one to inject an error into the system as if it had actually occurred.  However, this table should not be shipped with a production system; it should be dynamically loaded and executed with the ACPICA tools only during testing.

</td>
</tr>
<tr>
<td>


ERST

</td>
<td>


Section 18.5 (signature == "ERST")

**Error Record Serialization Table**

On a platform supports RAS, this table must be supplied if it is not UEFI-based; if it is UEFI-based, this table may be supplied. When this table is not present, UEFI run time service will be utilized to save and retrieve hardware error information to and from a persistent store.

</td>
</tr>
<tr>
<td>


ETDT

</td>
<td>


Signature Reserved (signature == "ETDT")

**Event Timer Description Table**

Obsolete table, will not be supported.

</td>
</tr>
<tr>
<td>


FACS

</td>
<td>


Section 5.2.10 (signature == "FACS")

**Firmware ACPI Control Structure**

It is unlikely that this table will be terribly useful.  If it is provided, the Global Lock will NOT be used since it is not part of the hardware reduced profile, and only 64-bit address fields will be considered valid.

</td>
</tr>
<tr>
<td>


FADT

</td>
<td>


Section 5.2.9 (signature == "FACP")

**Fixed ACPI Description Table** Required for arm64.

The HW_REDUCED_ACPI flag must be set.  All of the fields that are to be ignored when HW_REDUCED_ACPI is set are expected to be set to zero.

If an FACS table is provided, the X_FIRMWARE_CTRL field is to be used, not FIRMWARE_CTRL.

If PSCI is used (as is recommended), make sure that ARM_BOOT_ARCH is filled in properly - that the PSCI_COMPLIANT flag is set and that PSCI_USE_HVC is set or unset as needed (see table 5-37).

For the DSDT that is also required, the X_DSDT field is to be used, not the DSDT field.

</td>
</tr>
<tr>
<td>


FPDT

</td>
<td>


Section 5.2.23 (signature == "FPDT")

**Firmware Performance Data Table**

Optional, useful for boot performance profiling.

</td>
</tr>
<tr>
<td>


GTDT

</td>
<td>


Section 5.2.24 (signature == "GTDT")

**Generic Timer Description Table**

Required for arm64.

</td>
</tr>
<tr>
<td>


HEST

</td>
<td>


Section 18.3.2 (signature == "HEST")

**Hardware Error Source Table**

ARM-specific error sources have been defined; please use those or the PCI types such as type 6 (AER Root Port), 7 (AER Endpoint), or 8 (AER Bridge), or use type 9 (Generic Hardware Error Source).  Firmware first error handling is possible if and only if Trusted Firmware is being used on arm64.

Must be supplied if RAS support is provided by the platform.  It is recommended this table be supplied.

</td>
</tr>
<tr>
<td>


HMAT

</td>
<td>


Section 5.2.28 (signature == "HMAT")

**Heterogeneous Memory Attribute Table**

This table describes the memory attributes, such as memory side cache attributes and bandwidth and latency details, related to Memory Proximity Domains. The OS uses this information to optimize the system memory configuration.

</td>
</tr>
<tr>
<td>


HPET

</td>
<td>


Signature Reserved (signature == "HPET")

**High Precision Event timer Table**

x86 only table, will not be supported.

</td>
</tr>
<tr>
<td>


IBFT

</td>
<td>


Signature Reserved (signature == "IBFT")

**iSCSI Boot Firmware Table**

Microsoft defined table, support TBD.

</td>
</tr>
<tr>
<td>


IORT

</td>
<td>


Signature Reserved (signature == "IORT")

**Input Output Remapping Table**

arm64 only table, required in order to describe IO topology, SMMUs, and GIC ITSs, and how those various components are connected together, such as identifying which components are behind which SMMUs/ITSs. This table will only be required on certain SBSA platforms (e.g., when using GICv3-ITS and an SMMU); on SBSA Level 0 platforms, it remains optional.

</td>
</tr>
<tr>
<td>


IVRS

</td>
<td>


Signature Reserved (signature == "IVRS")

**I/O Virtualization Reporting Structure**

x86_64 (AMD) only table, will not be supported.

</td>
</tr>
<tr>
<td>


LPIT

</td>
<td>


Signature Reserved (signature == "LPIT")

**Low Power Idle Table**

x86 only table as of ACPI 5.1; starting with ACPI 6.0, processor descriptions and power states on ARM platforms should use the DSDT and define processor container devices (\_HID ACPI0010, Section 8.4, and more specifically 8.4.3 and 8.4.4).

</td>
</tr>
<tr>
<td>


MADT

</td>
<td>


Section 5.2.12 (signature == "APIC")

**Multiple APIC Description Table**

Required for arm64.  Only the GIC interrupt controller structures should be used (types 0xA - 0xF).

</td>
</tr>
<tr>
<td>


MCFG

</td>
<td>


Signature Reserved (signature == "MCFG")

**Memory-mapped ConFiGuration space**

If the platform supports PCI/PCIe, an MCFG table is required.

</td>
</tr>
<tr>
<td>


MCHI

</td>
<td>


Signature Reserved (signature == "MCHI")

**Management Controller Host Interface table**

Optional, not currently supported.

</td>
</tr>
<tr>
<td>


MPAM

</td>
<td>


Signature Reserved (signature == "MPAM")

**Memory Partitioning And Monitoring table**

This table allows the OS to discover the MPAM controls implemented by the subsystems.

</td>
</tr>
<tr>
<td>


MPST

</td>
<td>


Section 5.2.21 (signature == "MPST")

**Memory Power State Table**

Optional, not currently supported.

</td>
</tr>
<tr>
<td>


MSCT

</td>
<td>


Section 5.2.19 (signature == "MSCT")

**Maximum System Characteristic Table**

Optional, not currently supported.

</td>
</tr>
<tr>
<td>


MSDM

</td>
<td>


Signature Reserved (signature == "MSDM")

**Microsoft Data Management table**

Microsoft only table, will not be supported.

</td>
</tr>
<tr>
<td>


NFIT

</td>
<td>


Section 5.2.25 (signature == "NFIT")

**NVDIMM Firmware Interface Table**

Optional, not currently supported.

</td>
</tr>
<tr>
<td>


OEMx

</td>
<td>


Signature of "OEMx" only

**OEM Specific Tables**

All tables starting with a signature of "OEM" are reserved for OEM use.  Since these are not meant to be of general use but are limited to very specific end users, they are not recommended for use and are not supported by the kernel for arm64.

</td>
</tr>
<tr>
<td>


PCCT

</td>
<td>


Section 14.1 (signature == "PCCT)

**Platform Communications Channel Table**

Recommend for use on arm64; use of PCC is recommended when using CPPC to control performance and power for platform processors.

</td>
</tr>
<tr>
<td>


PDTT

</td>
<td>


Section 5.2.29 (signature == "PDTT")

**Platform Debug Trigger Table**

This table describes PCC channels used to gather debug logs of non-architectural features.

</td>
</tr>
<tr>
<td>


PMTT

</td>
<td>


Section 5.2.21.12 (signature == "PMTT")

**Platform Memory Topology Table**

Optional, not currently supported.

</td>
</tr>
<tr>
<td>


PPTT

</td>
<td>


Section 5.2.30 (signature == "PPTT")

**Processor Properties Topology Table**

This table provides the processor and cache topology.

</td>
</tr>
<tr>
<td>


PSDT

</td>
<td>


Section 5.2.11.3 (signature == "PSDT")

**Persistent System Description Table**

Obsolete table, will not be supported.

</td>
</tr>
<tr>
<td>


RAS2

</td>
<td>


Section 5.2.21 (signature == "RAS2")

**RAS Features 2 table**

This table provides interfaces for the RAS capabilities implemented in the platform.

</td>
</tr>
<tr>
<td>


RASF

</td>
<td>


Section 5.2.20 (signature == "RASF")

**RAS Feature table**

Optional, not currently supported.

</td>
</tr>
<tr>
<td>


RSDP

</td>
<td>


Section 5.2.5 (signature == "RSD PTR")

**Root System Description PoinTeR**

Required for arm64.

</td>
</tr>
<tr>
<td>


RSDT

</td>
<td>


Section 5.2.7 (signature == "RSDT")

**Root System Description Table**

Since this table can only provide 32-bit addresses, it is deprecated on arm64, and will not be used.  If provided, it will be ignored.

</td>
</tr>
<tr>
<td>


SBST

</td>
<td>


Section 5.2.14 (signature == "SBST")

**Smart Battery Subsystem Table**

Optional, not currently supported.

</td>
</tr>
<tr>
<td>


SDEI

</td>
<td>


Signature Reserved (signature == "SDEI")

**Software Delegated Exception Interface table**

This table advertises the presence of the SDEI interface.

</td>
</tr>
<tr>
<td>


SLIC

</td>
<td>


Signature Reserved (signature == "SLIC")

**Software LIcensing table**

Microsoft only table, will not be supported.

</td>
</tr>
<tr>
<td>


SLIT

</td>
<td>


Section 5.2.17 (signature == "SLIT")

**System Locality distance Information Table**

Optional in general, but required for NUMA systems.

</td>
</tr>
<tr>
<td>


SPCR

</td>
<td>


Signature Reserved (signature == "SPCR")

**Serial Port Console Redirection table**

Required for arm64.

</td>
</tr>
<tr>
<td>


SPMI

</td>
<td>


Signature Reserved (signature == "SPMI")

**Server Platform Management Interface table**

Optional, not currently supported.

</td>
</tr>
<tr>
<td>


SRAT

</td>
<td>


Section 5.2.16 (signature == "SRAT")

**System Resource Affinity Table**

Optional, but if used, only the GICC Affinity structures are read. To support arm64 NUMA, this table is required.

</td>
</tr>
<tr>
<td>


SSDT

</td>
<td>


Section 5.2.11.2 (signature == "SSDT")

**Secondary System Description Table**

These tables are a continuation of the DSDT; these are recommended for use with devices that can be added to a running system, but can also serve the purpose of dividing up device descriptions into more manageable pieces.

An SSDT can only ADD to the ACPI namespace.  It cannot modify or replace existing device descriptions already in the namespace.

These tables are optional, however.  ACPI tables should contain only one DSDT but can contain many SSDTs.

</td>
</tr>
<tr>
<td>


STAO

</td>
<td>


Signature Reserved (signature == "STAO")

**\_STA Override table**

Optional, but only necessary in virtualized environments in order to hide devices from guest OSs.

</td>
</tr>
<tr>
<td>


TCPA

</td>
<td>


Signature Reserved (signature == "TCPA")

**Trusted Computing Platform Alliance table**

Optional, not currently supported, and may need changes to fully interoperate with arm64.

</td>
</tr>
<tr>
<td>


TPM2

</td>
<td>


Signature Reserved (signature == "TPM2")

**Trusted Platform Module 2 table**

Optional, not currently supported, and may need changes to fully interoperate with arm64.

</td>
</tr>
<tr>
<td>


UEFI

</td>
<td>


Signature Reserved (signature == "UEFI")

**UEFI ACPI data table**

Optional, not currently supported.  No known use case for arm64, at present.

</td>
</tr>
<tr>
<td>


WAET

</td>
<td>


Signature Reserved (signature == "WAET")

**Windows ACPI Emulated devices Table**

Microsoft only table, will not be supported.

</td>
</tr>
<tr>
<td>


WDAT

</td>
<td>


Signature Reserved (signature == "WDAT")

**Watch Dog Action Table**

Microsoft only table, will not be supported.

</td>
</tr>
<tr>
<td>


WDRT

</td>
<td>


Signature Reserved (signature == "WDRT")

**Watch Dog Resource Table**

Microsoft only table, will not be supported.

</td>
</tr>
<tr>
<td>


WPBT

</td>
<td>


Signature Reserved (signature == "WPBT")

**Windows Platform Binary Table**

Microsoft only table, will not be supported.

</td>
</tr>
<tr>
<td>


XENV

</td>
<td>


Signature Reserved (signature == "XENV")

**Xen project table**

Optional, used only by Xen at present.

</td>
</tr>
<tr>
<td>


XSDT

</td>
<td>


Section 5.2.8 (signature == "XSDT")

**eXtended System Description Table**

Required for arm64.

</td>
</tr>
</tbody>
</table>

<a id="rst-acpi-objects"></a>

## ACPI Objects

The expectations on individual ACPI objects that are likely to be used are shown in the list that follows; any object not explicitly mentioned below should be used as needed for a particular platform or particular subsystem, such as power management or PCI.


<table>
<thead>
<tr>
<th>


Name

</th>
<th>


Section

</th>
<th>


Usage for ARMv8 Linux

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


\_CCA

</td>
<td>


6.2.17

</td>
<td>


This method must be defined for all bus masters on arm64 - there are no assumptions made about whether such devices are cache coherent or not. The \_CCA value is inherited by all descendants of these devices so it does not need to be repeated. Without \_CCA on arm64, the kernel does not know what to do about setting up DMA for the device.

NB: this method provides default cache coherency attributes; the presence of an SMMU can be used to modify that, however.  For example, a master could default to non-coherent, but be made coherent with the appropriate SMMU configuration (see Table 17 of the IORT specification, ARM Document DEN 0049B).

</td>
</tr>
<tr>
<td>


\_CID

</td>
<td>


6.1.2

</td>
<td>


Use as needed, see also \_HID.

</td>
</tr>
<tr>
<td>


\_CLS

</td>
<td>


6.1.3

</td>
<td>


Use as needed, see also \_HID.

</td>
</tr>
<tr>
<td>


\_CPC

</td>
<td>


8.4.7.1

</td>
<td>


Use as needed, power management specific.  CPPC is recommended on arm64.

</td>
</tr>
<tr>
<td>


\_CRS

</td>
<td>


6.2.2

</td>
<td>


Required on arm64.

</td>
</tr>
<tr>
<td>


\_CSD

</td>
<td>


8.4.2.2

</td>
<td>


Use as needed, used only in conjunction with \_CST.

</td>
</tr>
<tr>
<td>


\_CST

</td>
<td>


8.4.2.1

</td>
<td>


Low power idle states (8.4.4) are recommended instead of C-states.

</td>
</tr>
<tr>
<td>


\_DDN

</td>
<td>


6.1.4

</td>
<td>


This field can be used for a device name.  However, it is meant for DOS device names (e.g., COM1), so be careful of its use across OSes.

</td>
</tr>
<tr>
<td>


\_DSD

</td>
<td>


6.2.5

</td>
<td>


To be used with caution.  If this object is used, try to use it within the constraints already defined by the Device Properties UUID.  Only in rare circumstances should it be necessary to create a new \_DSD UUID.

In either case, submit the \_DSD definition along with any driver patches for discussion, especially when device properties are used.  A driver will not be considered complete without a corresponding \_DSD description.  Once approved by kernel maintainers, the UUID or device properties must then be registered with the UEFI Forum; this may cause some iteration as more than one OS will be registering entries.

</td>
</tr>
<tr>
<td>


\_DSM

</td>
<td>


9.1.1

</td>
<td>


Do not use this method.  It is not standardized, the return values are not well documented, and it is currently a frequent source of error.

</td>
</tr>
<tr>
<td>


\_GL

</td>
<td>


5.7.1

</td>
<td>


This object is not to be used in hardware reduced mode, and therefore should not be used on arm64.

</td>
</tr>
<tr>
<td>


\_GLK

</td>
<td>


6.5.7

</td>
<td>


This object requires a global lock be defined; there is no global lock on arm64 since it runs in hardware reduced mode.  Hence, do not use this object on arm64.

</td>
</tr>
<tr>
<td>


\_GPE

</td>
<td>


5.3.1

</td>
<td>


This namespace is for x86 use only.  Do not use it on arm64.

</td>
</tr>
<tr>
<td>


\_HID

</td>
<td>


6.1.5

</td>
<td>


This is the primary object to use in device probing, though \_CID and \_CLS may also be used.

</td>
</tr>
<tr>
<td>


\_INI

</td>
<td>


6.5.1

</td>
<td>


Not required, but can be useful in setting up devices when UEFI leaves them in a state that may not be what the driver expects before it starts probing.

</td>
</tr>
<tr>
<td>


\_LPI

</td>
<td>


8.4.4.3

</td>
<td>


Recommended for use with processor definitions (\_HID ACPI0010) on arm64.  See also \_RDI.

</td>
</tr>
<tr>
<td>


\_MLS

</td>
<td>


6.1.7

</td>
<td>


Highly recommended for use in internationalization.

</td>
</tr>
<tr>
<td>


\_OFF

</td>
<td>


7.2.2

</td>
<td>


It is recommended to define this method for any device that can be turned on or off.

</td>
</tr>
<tr>
<td>


\_ON

</td>
<td>


7.2.3

</td>
<td>


It is recommended to define this method for any device that can be turned on or off.

</td>
</tr>
<tr>
<td>


\_OS

</td>
<td>


5.7.3

</td>
<td>


This method will return "Linux" by default (this is the value of the macro ACPI_OS_NAME on Linux).  The command line parameter acpi_os=&lt;string&gt; can be used to set it to some other value.

</td>
</tr>
<tr>
<td>


\_OSC

</td>
<td>


6.2.11

</td>
<td>


This method can be a global method in ACPI (i.e., \_SB.\_OSC), or it may be associated with a specific device (e.g., \_SB.DEV0.\_OSC), or both.  When used as a global method, only capabilities published in the ACPI specification are allowed.  When used as a device-specific method, the process described for using \_DSD MUST be used to create an \_OSC definition; out-of-process use of \_OSC is not allowed.  That is, submit the device-specific \_OSC usage description as part of the kernel driver submission, get it approved by the kernel community, then register it with the UEFI Forum.

</td>
</tr>
<tr>
<td>


\_OSI

</td>
<td>


5.7.2

</td>
<td>


Deprecated on ARM64.  As far as ACPI firmware is concerned, \_OSI is not to be used to determine what sort of system is being used or what functionality is provided.  The \_OSC method is to be used instead.

</td>
</tr>
<tr>
<td>


\_PDC

</td>
<td>


8.4.1

</td>
<td>


Deprecated, do not use on arm64.

</td>
</tr>
<tr>
<td>


\_PIC

</td>
<td>


5.8.1

</td>
<td>


The method should not be used.  On arm64, the only interrupt model available is GIC.

</td>
</tr>
<tr>
<td>


\_PR

</td>
<td>


5.3.1

</td>
<td>


This namespace is for x86 use only on legacy systems. Do not use it on arm64.

</td>
</tr>
<tr>
<td>


\_PRT

</td>
<td>


6.2.13

</td>
<td>


Required as part of the definition of all PCI root devices.

</td>
</tr>
<tr>
<td>


\_PRx

</td>
<td>


7.3.8-11

</td>
<td>


Use as needed; power management specific.  If \_PR0 is defined, \_PR3 must also be defined.

</td>
</tr>
<tr>
<td>


\_PSx

</td>
<td>


7.3.2-5

</td>
<td>


Use as needed; power management specific.  If \_PS0 is defined, \_PS3 must also be defined.  If clocks or regulators need adjusting to be consistent with power usage, change them in these methods.

</td>
</tr>
<tr>
<td>


\_RDI

</td>
<td>


8.4.4.4

</td>
<td>


Recommended for use with processor definitions (\_HID ACPI0010) on arm64.  This should only be used in conjunction with \_LPI.

</td>
</tr>
<tr>
<td>


\_REV

</td>
<td>


5.7.4

</td>
<td>


Always returns the latest version of ACPI supported.

</td>
</tr>
<tr>
<td>


\_SB

</td>
<td>


5.3.1

</td>
<td>


Required on arm64; all devices must be defined in this namespace.

</td>
</tr>
<tr>
<td>


\_SLI

</td>
<td>


6.2.15

</td>
<td>


Use is recommended when SLIT table is in use.

</td>
</tr>
<tr>
<td>


\_STA

</td>
<td>


6.3.7, 7.2.4

</td>
<td>


It is recommended to define this method for any device that can be turned on or off.  See also the STAO table that provides overrides to hide devices in virtualized environments.

</td>
</tr>
<tr>
<td>


\_SRS

</td>
<td>


6.2.16

</td>
<td>


Use as needed; see also \_PRS.

</td>
</tr>
<tr>
<td>


\_STR

</td>
<td>


6.1.10

</td>
<td>


Recommended for conveying device names to end users; this is preferred over using \_DDN.

</td>
</tr>
<tr>
<td>


\_SUB

</td>
<td>


6.1.9

</td>
<td>


Use as needed; \_HID or \_CID are preferred.

</td>
</tr>
<tr>
<td>


\_SUN

</td>
<td>


6.1.11

</td>
<td>


Use as needed, but recommended.

</td>
</tr>
<tr>
<td>


\_SWS

</td>
<td>


7.4.3

</td>
<td>


Use as needed; power management specific; this may require specification changes for use on arm64.

</td>
</tr>
<tr>
<td>


\_UID

</td>
<td>


6.1.12

</td>
<td>


Recommended for distinguishing devices of the same class; define it if at all possible.

</td>
</tr>
</tbody>
</table>

<a id="rst-acpi-event-model"></a>

## ACPI Event Model

Do not use GPE block devices; these are not supported in the hardware reduced profile used by arm64.  Since there are no GPE blocks defined for use on ARM platforms, ACPI events must be signaled differently.

There are two options: GPIO-signaled interrupts (Section 5.6.5), and interrupt-signaled events (Section 5.6.9).  Interrupt-signaled events are a new feature in the ACPI 6.1 specification.  Either - or both - can be used on a given platform, and which to use may be dependent of limitations in any given SoC.  If possible, interrupt-signaled events are recommended.

<a id="rst-acpi-processor-control"></a>

## ACPI Processor Control

Section 8 of the ACPI specification changed significantly in version 6.0. Processors should now be defined as Device objects with \_HID ACPI0007; do not use the deprecated Processor statement in ASL.  All multiprocessor systems should also define a hierarchy of processors, done with Processor Container Devices (see Section 8.4.3.1, \_HID ACPI0010); do not use processor aggregator devices (Section 8.5) to describe processor topology.  Section 8.4 of the specification describes the semantics of these object definitions and how they interrelate.

Most importantly, the processor hierarchy defined also defines the low power idle states that are available to the platform, along with the rules for determining which processors can be turned on or off and the circumstances that control that.  Without this information, the processors will run in whatever power state they were left in by UEFI.

Note too, that the processor Device objects defined and the entries in the MADT for GICs are expected to be in synchronization.  The \_UID of the Device object must correspond to processor IDs used in the MADT.

It is recommended that CPPC (8.4.5) be used as the primary model for processor performance control on arm64.  C-states and P-states may become available at some point in the future, but most current design work appears to favor CPPC.

Further, it is essential that the ARMv8 SoC provide a fully functional implementation of PSCI; this will be the only mechanism supported by ACPI to control CPU power state.  Booting of secondary CPUs using the ACPI parking protocol is possible, but discouraged, since only PSCI is supported for ARM servers.

<a id="rst-acpi-system-address-map-interfaces"></a>

## ACPI System Address Map Interfaces

In Section 15 of the ACPI specification, several methods are mentioned as possible mechanisms for conveying memory resource information to the kernel. For arm64, we will only support UEFI for booting with ACPI, hence the UEFI GetMemoryMap() boot service is the only mechanism that will be used.

<a id="rst-acpi-platform-error-interfaces-apei"></a>

## ACPI Platform Error Interfaces (APEI)

The APEI tables supported are described above.

APEI requires the equivalent of an SCI and an NMI on ARMv8.  The SCI is used to notify the OSPM of errors that have occurred but can be corrected and the system can continue correct operation, even if possibly degraded.  The NMI is used to indicate fatal errors that cannot be corrected, and require immediate attention.

Since there is no direct equivalent of the x86 SCI or NMI, arm64 handles these slightly differently.  The SCI is handled as a high priority interrupt; given that these are corrected (or correctable) errors being reported, this is sufficient.  The NMI is emulated as the highest priority interrupt possible.  This implies some caution must be used since there could be interrupts at higher privilege levels or even interrupts at the same priority as the emulated NMI.  In Linux, this should not be the case but one should be aware it could happen.

<a id="rst-acpi-objects-not-supported-on-arm64"></a>

## ACPI Objects Not Supported on ARM64

While this may change in the future, there are several classes of objects that can be defined, but are not currently of general interest to ARM servers. Some of these objects have x86 equivalents, and may actually make sense in ARM servers.  However, there is either no hardware available at present, or there may not even be a non-ARM implementation yet.  Hence, they are not currently supported.

The following classes of objects are not supported:

> - Section 9.2: ambient light sensor devices
>
> - Section 9.3: battery devices
>
> - Section 9.4: lids (e.g., laptop lids)
>
> - Section 9.8.2: IDE controllers
>
> - Section 9.9: floppy controllers
>
> - Section 9.10: GPE block devices
>
> - Section 9.15: PC/AT RTC/CMOS devices
>
> - Section 9.16: user presence detection devices
>
> - Section 9.17: I/O APIC devices; all GICs must be enumerable via MADT
>
> - Section 9.18: time and alarm devices (see 9.15)
>
> - Section 10: power source and power meter devices
>
> - Section 11: thermal management
>
> - Section 12: embedded controllers interface
>
> - Section 13: SMBus interfaces

This also means that there is no support for the following objects:


<table>
<thead>
<tr>
<th>


Name

</th>
<th>


Section

</th>
<th>


Name

</th>
<th>


Section

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


\_ALC

</td>
<td>


9.3.4

</td>
<td>


\_FDM

</td>
<td>


9.10.3

</td>
</tr>
<tr>
<td>


\_ALI

</td>
<td>


9.3.2

</td>
<td>


\_FIX

</td>
<td>


6.2.7

</td>
</tr>
<tr>
<td>


\_ALP

</td>
<td>


9.3.6

</td>
<td>


\_GAI

</td>
<td>


10.4.5

</td>
</tr>
<tr>
<td>


\_ALR

</td>
<td>


9.3.5

</td>
<td>


\_GHL

</td>
<td>


10.4.7

</td>
</tr>
<tr>
<td>


\_ALT

</td>
<td>


9.3.3

</td>
<td>


\_GTM

</td>
<td>


9.9.2.1.1

</td>
</tr>
<tr>
<td>


\_BCT

</td>
<td>


10.2.2.10

</td>
<td>


\_LID

</td>
<td>


9.5.1

</td>
</tr>
<tr>
<td>


\_BDN

</td>
<td>


6.5.3

</td>
<td>


\_PAI

</td>
<td>


10.4.4

</td>
</tr>
<tr>
<td>


\_BIF

</td>
<td>


10.2.2.1

</td>
<td>


\_PCL

</td>
<td>


10.3.2

</td>
</tr>
<tr>
<td>


\_BIX

</td>
<td>


10.2.2.1

</td>
<td>


\_PIF

</td>
<td>


10.3.3

</td>
</tr>
<tr>
<td>


\_BLT

</td>
<td>


9.2.3

</td>
<td>


\_PMC

</td>
<td>


10.4.1

</td>
</tr>
<tr>
<td>


\_BMA

</td>
<td>


10.2.2.4

</td>
<td>


\_PMD

</td>
<td>


10.4.8

</td>
</tr>
<tr>
<td>


\_BMC

</td>
<td>


10.2.2.12

</td>
<td>


\_PMM

</td>
<td>


10.4.3

</td>
</tr>
<tr>
<td>


\_BMD

</td>
<td>


10.2.2.11

</td>
<td>


\_PRL

</td>
<td>


10.3.4

</td>
</tr>
<tr>
<td>


\_BMS

</td>
<td>


10.2.2.5

</td>
<td>


\_PSR

</td>
<td>


10.3.1

</td>
</tr>
<tr>
<td>


\_BST

</td>
<td>


10.2.2.6

</td>
<td>


\_PTP

</td>
<td>


10.4.2

</td>
</tr>
<tr>
<td>


\_BTH

</td>
<td>


10.2.2.7

</td>
<td>


\_SBS

</td>
<td>


10.1.3

</td>
</tr>
<tr>
<td>


\_BTM

</td>
<td>


10.2.2.9

</td>
<td>


\_SHL

</td>
<td>


10.4.6

</td>
</tr>
<tr>
<td>


\_BTP

</td>
<td>


10.2.2.8

</td>
<td>


\_STM

</td>
<td>


9.9.2.1.1

</td>
</tr>
<tr>
<td>


\_DCK

</td>
<td>


6.5.2

</td>
<td>


\_UPD

</td>
<td>


9.16.1

</td>
</tr>
<tr>
<td>


\_EC

</td>
<td>


12.12

</td>
<td>


\_UPP

</td>
<td>


9.16.2

</td>
</tr>
<tr>
<td>


\_FDE

</td>
<td>


9.10.1

</td>
<td>


\_WPC

</td>
<td>


10.5.2

</td>
</tr>
<tr>
<td>


\_FDI

</td>
<td>


9.10.2

</td>
<td>


\_WPP

</td>
<td>


10.5.3

</td>
</tr>
</tbody>
</table>
