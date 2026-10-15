---
title: "ACPI PRM CXL Address Translation"
type: reference
description: "CXL Revision 3.2, Version 1.0"
---

<a id="rst-acpi-prm-cxl-address-translation"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

<a id="rst-document"></a>

## Document

CXL Revision 3.2, Version 1.0

<a id="rst-license"></a>

## License

SPDX-License Identifier: CC-BY-4.0

<a id="rst-creator-contributors"></a>

## Creator/Contributors

- Robert Richter, AMD et al.

<a id="rst-summary-of-the-change"></a>

## Summary of the Change

The CXL Fixed Memory Window Structures (CFMWS) describe zero or more Host Physical Address (HPA) windows associated with one or more CXL Host Bridges. Each HPA range of a CXL Host Bridge is represented by a CFMWS entry. An HPA range may include addresses currently assigned to CXL.mem devices, or an OS may assign ranges from an address window to a device.

Host-managed Device Memory is Device-attached memory that is mapped to system coherent address space and accessible to the Host using standard write-back semantics. The managed address range is configured in the CXL HDM Decoder registers of the device. An HDM Decoder in a device is responsible for converting HPA into DPA by stripping off specific address bits.

CXL devices and CXL bridges use the same HPA space. It is common across all components that belong to the same host domain. The view of the address region must be consistent on the CXL.mem path between the Host and the Device.

This is described in the *CXL 3.2 specification* (Table 1-1, 3.3.1, 8.2.4.20, 9.13.1, 9.18.1.3). <a id="rst-footnote-reference-1"></a>[1](#rst-cxl-spec-3-2)

Depending on the interconnect architecture of the platform, components attached to a host may not share the same host physical address space. Those platforms need address translation to convert an HPA between the host and the attached component, such as a CXL device. The translation mechanism is host-specific and implementation dependent.

For example, x86 AMD platforms use a Data Fabric that manages access to physical memory. Devices have their own memory space and can be configured to use 'Normalized addresses' different from System Physical Addresses (SPA). Address translation is then needed. For details, see [x86 AMD Address Translation](<~kernel/administration/admin-guide/ras/address-translation>).

Those AMD platforms provide PRM <a id="rst-footnote-reference-2"></a>[3](#rst-prm-spec) handlers in firmware to perform various types of address translation, including for CXL endpoints. AMD Zen5 systems implement the ACPI PRM CXL Address Translation firmware call. The ACPI PRM handler has a specific GUID to uniquely identify platforms with support for Normalized addressing. This is documented in the *ACPI v6.5 Porting Guide* (Address Translation - CXL DPA to System Physical Address). <a id="rst-footnote-reference-3"></a>[2](#rst-amd-ppr-58088)

When in Normalized address mode, HDM decoder address ranges must be configured and handled differently. Hardware addresses used in the HDM decoder configurations of an endpoint are not SPA and need to be translated from the address range of the endpoint to that of the CXL host bridge. This is especially important for finding an endpoint's associated CXL Host Bridge and HPA window described in the CFMWS. Additionally, the interleave decoding is done by the Data Fabric and the endpoint does not perform decoding when converting HPA to DPA. Instead, interleaving is switched off for the endpoint (1-way). Finally, address translation might also be needed to inspect the endpoint's hardware addresses, such as during profiling, tracing, or error handling.

For example, with Normalized addressing the HDM decoders could look as follows:



```text
                         -------------------------------
                         | Root Decoder (CFMWS)        |
                         | SPA Range: 0x850000000      |
                         | Size: 0x8000000000 (512 GB) |
                         | Interleave Ways: 1          |
                         -------------------------------
                                       |
                                       v
                         -------------------------------
                         | Host Bridge Decoder (HDM)   |
                         | SPA Range: 0x850000000      |
                         | Size: 0x8000000000 (512 GB) |
                         | Interleave Ways: 4          |
                         | Targets: endpoint5,8,11,13  |
                         | Granularity: 256            |
                         -------------------------------
                                       |
          -----------------------------+------------------------------
          |                  |                   |                   |
          v                  v                   v                   v
------------------- ------------------- ------------------- -------------------
| endpoint5       | | endpoint8       | | endpoint11      | | endpoint13      |
| decoder5.0      | | decoder8.0      | | decoder11.0     | | decoder13.0     |
| PCIe:           | | PCIe:           | | PCIe:           | | PCIe:           |
|   0000:e2:00.0  | |   0000:e3:00.0  | |   0000:e4:00.0  | |   0000:e1:00.0  |
| DPA:            | | DPA:            | | DPA:            | | DPA:            |
|   Start: 0x0    | |   Start: 0x0    | |   Start: 0x0    | |   Start: 0x0    |
|   Size:         | |   Size:         | |   Size:         | |   Size:         |
|    0x2000000000 | |    0x2000000000 | |    0x2000000000 | |    0x2000000000 |
|    (128 GB)     | |    (128 GB)     | |    (128 GB)     | |    (128 GB)     |
| Interleaving:   | | Interleaving:   | | Interleaving:   | | Interleaving:   |
|   Ways: 1       | |   Ways: 1       | |   Ways: 1       | |   Ways: 1       |
|   Gran: 256     | |   Gran: 256     | |   Gran: 256     | |   Gran: 256     |
------------------- ------------------- ------------------- -------------------
         |                   |                   |                   |
         v                   v                   v                   v
        DPA                 DPA                 DPA                 DPA
```

This shows the representation in sysfs:



```none
/sys/bus/cxl/devices/endpoint5/decoder5.0/interleave_granularity:256
/sys/bus/cxl/devices/endpoint5/decoder5.0/interleave_ways:1
/sys/bus/cxl/devices/endpoint5/decoder5.0/size:0x2000000000
/sys/bus/cxl/devices/endpoint5/decoder5.0/start:0x0
/sys/bus/cxl/devices/endpoint8/decoder8.0/interleave_granularity:256
/sys/bus/cxl/devices/endpoint8/decoder8.0/interleave_ways:1
/sys/bus/cxl/devices/endpoint8/decoder8.0/size:0x2000000000
/sys/bus/cxl/devices/endpoint8/decoder8.0/start:0x0
/sys/bus/cxl/devices/endpoint11/decoder11.0/interleave_granularity:256
/sys/bus/cxl/devices/endpoint11/decoder11.0/interleave_ways:1
/sys/bus/cxl/devices/endpoint11/decoder11.0/size:0x2000000000
/sys/bus/cxl/devices/endpoint11/decoder11.0/start:0x0
/sys/bus/cxl/devices/endpoint13/decoder13.0/interleave_granularity:256
/sys/bus/cxl/devices/endpoint13/decoder13.0/interleave_ways:1
/sys/bus/cxl/devices/endpoint13/decoder13.0/size:0x2000000000
/sys/bus/cxl/devices/endpoint13/decoder13.0/start:0x0
```

Note that the endpoint interleaving configurations use direct mapping (1-way).

With PRM calls, the kernel can determine the following mappings:



```none
cxl decoder5.0: address mapping found for 0000:e2:00.0 (hpa -> spa):
  0x0+0x2000000000 -> 0x850000000+0x8000000000 ways:4 granularity:256
cxl decoder8.0: address mapping found for 0000:e3:00.0 (hpa -> spa):
  0x0+0x2000000000 -> 0x850000000+0x8000000000 ways:4 granularity:256
cxl decoder11.0: address mapping found for 0000:e4:00.0 (hpa -> spa):
  0x0+0x2000000000 -> 0x850000000+0x8000000000 ways:4 granularity:256
cxl decoder13.0: address mapping found for 0000:e1:00.0 (hpa -> spa):
  0x0+0x2000000000 -> 0x850000000+0x8000000000 ways:4 granularity:256
```

The corresponding CXL host bridge (HDM) decoders and root decoder (CFMWS) match the calculated endpoint mappings shown:



```none
/sys/bus/cxl/devices/port1/decoder1.0/interleave_granularity:256
/sys/bus/cxl/devices/port1/decoder1.0/interleave_ways:4
/sys/bus/cxl/devices/port1/decoder1.0/size:0x8000000000
/sys/bus/cxl/devices/port1/decoder1.0/start:0x850000000
/sys/bus/cxl/devices/port1/decoder1.0/target_list:0,1,2,3
/sys/bus/cxl/devices/port1/decoder1.0/target_type:expander
/sys/bus/cxl/devices/root0/decoder0.0/interleave_granularity:256
/sys/bus/cxl/devices/root0/decoder0.0/interleave_ways:1
/sys/bus/cxl/devices/root0/decoder0.0/size:0x8000000000
/sys/bus/cxl/devices/root0/decoder0.0/start:0x850000000
/sys/bus/cxl/devices/root0/decoder0.0/target_list:7
```

The following changes to the specification are needed:

- Allow a CXL device to be in an HPA space other than the host's address space.

- Allow the platform to use implementation-specific address translation when crossing memory domains on the CXL.mem path between the host and the device.

- Define a PRM handler method for converting device addresses to SPAs.

- Specify that the platform shall provide the PRM handler method to the Operating System to detect Normalized addressing and for determining Endpoint SPA ranges and interleaving configurations.

- Add reference to:

  Platform Runtime Mechanism Specification, Version 1.1 – November 2020  
  [https://uefi.org/sites/default/files/resources/PRM_Platform_Runtime_Mechanism_1_1_release_candidate.pdf](<https://uefi.org/sites/default/files/resources/PRM_Platform_Runtime_Mechanism_1_1_release_candidate.pdf>)

<a id="rst-benefits-of-the-change"></a>

## Benefits of the Change

Without the change, the Operating System may be unable to determine the memory region and Root Decoder for an Endpoint and its corresponding HDM decoder. Region creation would fail. Platforms with a different interconnect architecture would fail to set up and use CXL.

<a id="rst-references"></a>

## References

<a id="rst-cxl-spec-3-2"></a>



**[1]** Compute Express Link Specification, Revision 3.2, Version 1.0, [https://www.computeexpresslink.org/](<https://www.computeexpresslink.org/>)

<a id="rst-amd-ppr-58088"></a>



**[2]** AMD Family 1Ah Models 00h–0Fh and Models 10h–1Fh, ACPI v6.5 Porting Guide, Publication \# 58088, [https://www.amd.com/en/search/documentation/hub.html](<https://www.amd.com/en/search/documentation/hub.html>)

<a id="rst-prm-spec"></a>



**[3]** Platform Runtime Mechanism, Version: 1.1, [https://uefi.org/sites/default/files/resources/PRM_Platform_Runtime_Mechanism_1_1_release_candidate.pdf](<https://uefi.org/sites/default/files/resources/PRM_Platform_Runtime_Mechanism_1_1_release_candidate.pdf>)

<a id="rst-detailed-description-of-the-change"></a>

## Detailed Description of the Change

The following describes the necessary changes to the *CXL 3.2 specification* <a id="rst-footnote-reference-4"></a>[1](#rst-cxl-spec-3-2):

Add the following reference to the table:

Table 1-2. Reference Documents


<table>
<thead>
<tr>
<th>


Document

</th>
<th>


Chapter Reference

</th>
<th>


Document No./Location

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


Platform Runtime Mechanism Version: 1.1

</td>
<td>


Chapter 8, 9

</td>
<td>


[https://www.uefi.org/acpi](<https://www.uefi.org/acpi>)

</td>
</tr>
</tbody>
</table>

Add the following paragraphs to the end of the section:

**8.2.4.20 CXL HDM Decoder Capability Structure**

"A device may use an HPA space that is not common to other components of the host domain. The platform is responsible for address translation when crossing HPA spaces. The Operating System must determine the interleaving configuration and perform address translation to the HPA ranges of the HDM decoders as needed. The translation mechanism is host-specific and implementation dependent.

The platform indicates support of independent HPA spaces and the need for address translation by providing a Platform Runtime Mechanism (PRM) handler. The OS shall use that handler to perform the necessary translations from the DPA space to the HPA space. The handler is defined in Section 9.18.4 *PRM Handler for CXL DPA to System Physical Address Translation*."

Add the following section and sub-section including tables:

**9.18.4 PRM Handler for CXL DPA to System Physical Address Translation**

"A platform may be configured to use 'Normalized addresses'. Host physical address (HPA) spaces are component-specific and differ from system physical addresses (SPAs). The endpoint has its own physical address space. All requests presented to the device already use Device Physical Addresses (DPAs). The CXL endpoint decoders have interleaving disabled (1-way interleaving) and the device does not perform HPA decoding to determine a DPA.

The platform provides a PRM handler for CXL DPA to System Physical Address Translation. The PRM handler translates a Device Physical Address (DPA) to a System Physical Address (SPA) for a specified CXL endpoint. In the address space of the host, SPA and HPA are equivalent, and the OS shall use this handler to determine the HPA that corresponds to a device address, for example when configuring HDM decoders on platforms with Normalized addressing. The GUID and the parameter buffer format of the handler are specified in section 9.18.4.1. If the OS identifies the PRM handler, the platform supports Normalized addressing and the OS must perform DPA address translation as needed."

**9.18.4.1 PRM Handler Invocation**

"The OS calls the PRM handler for CXL DPA to System Physical Address Translation using the direct invocation mechanism. Details of calling a PRM handler are described in the Platform Runtime Mechanism (PRM) specification.

The PRM handler is identified by the following GUID:

> EE41B397-25D4-452C-AD54-48C6E3480B94

The caller allocates and prepares a Parameter Buffer, then passes the PRM handler GUID and a pointer to the Parameter Buffer to invoke the handler. The Parameter Buffer is described in Table 9-32."

**Table 9-32. PRM Parameter Buffer used for CXL DPA to System Physical Address Translation**


<table>
<thead>
<tr>
<th>


Byte Offset

</th>
<th>


- **Length in**

  Bytes

</th>
<th>


Description

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


00h

</td>
<td>


8

</td>
<td>


**CXL Device Physical Address (DPA)**: CXL DPA (e.g., from CXL Component Event Log)

</td>
</tr>
<tr>
<td>


08h

</td>
<td>


4

</td>
<td>


**CXL Endpoint SBDF**:

- Byte 3 - PCIe Segment

- Byte 2 - Bus Number

- - **Byte 1:**

    - Device Number Bits\[7:3\]

    - Function Number Bits\[2:0\]

- Byte 0 - RESERVED (MBZ)

</td>
</tr>
<tr>
<td>


0Ch

</td>
<td>


8

</td>
<td>


**Output Buffer**: Virtual Address Pointer to the buffer, as defined in Table 9-33.

</td>
</tr>
</tbody>
</table>

**Table 9-33. PRM Output Buffer used for CXL DPA to System Physical Address Translation**


<table>
<thead>
<tr>
<th>


Byte Offset

</th>
<th>


- **Length in**

  Bytes

</th>
<th>


Description

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


00h

</td>
<td>


8

</td>
<td>


**System Physical Address (SPA)**: The SPA converted from the CXL DPA.

</td>
</tr>
</tbody>
</table>
