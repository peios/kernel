---
title: "Referencing hierarchical data nodes"
type: reference
description: "ACPI in general allows referring to device objects in the tree only. Hierarchical data extension nodes may not be referred to directly, hence this document defines a scheme to implement such references."
---

<a id="rst-referencing-hierarchical-data-nodes"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

<!-- This data file has been placed in the public domain. -->

<!-- Derived from the Unicode character mappings available from
<http://www.w3.org/2003/entities/xml/>.
Processed by unicode2rstsubs.py, part of Docutils:
<https://docutils.sourceforge.io>. -->

**Copyright:** © 2018, 2021 Intel Corporation

**Author:** Sakari Ailus &lt;[sakari.ailus@linux.intel.com](<mailto:sakari.ailus@linux.intel.com>)&gt;

ACPI in general allows referring to device objects in the tree only. Hierarchical data extension nodes may not be referred to directly, hence this document defines a scheme to implement such references.

A reference to a \_DSD hierarchical data node is a string consisting of a device object reference followed by a dot (".") and a relative path to a data node object. Do not use non-string references as this will produce a copy of the hierarchical data node, not a reference\!

The hierarchical data extension node which is referred to shall be located directly under its parent object i.e. either the device object or another hierarchical data extension node \[dsd-guide\].

The keys in the hierarchical data nodes shall consist of the name of the node, "@" character and the number of the node in hexadecimal notation (without pre- or postfixes). The same ACPI object shall include the \_DSD property extension with a property "reg" that shall have the same numerical value as the number of the node.

In case a hierarchical data extensions node has no numerical value, then the "reg" property shall be omitted from the ACPI object's \_DSD properties and the "@" character and the number shall be omitted from the hierarchical data extension key.

<a id="rst-example"></a>

## Example

In the ASL snippet below, the "reference" \_DSD property contains a string reference to a hierarchical data extension node ANOD under DEV0 under the parent of DEV1. ANOD is also the final target node of the reference.



```text
Device (DEV0)
{
    Name (_DSD, Package () {
        ToUUID("dbb8e3e6-5886-4ba6-8795-1319f52a966b"),
        Package () {
            Package () { "node@0", "NOD0" },
            Package () { "node@1", "NOD1" },
        }
    })
    Name (NOD0, Package() {
        ToUUID("daffd814-6eba-4d8c-8a91-bc9bbf4aa301"),
        Package () {
            Package () { "reg", 0 },
            Package () { "random-property", 3 },
        }
    })
    Name (NOD1, Package() {
        ToUUID("dbb8e3e6-5886-4ba6-8795-1319f52a966b"),
        Package () {
            Package () { "reg", 1 },
            Package () { "anothernode", "ANOD" },
        }
    })
    Name (ANOD, Package() {
        ToUUID("daffd814-6eba-4d8c-8a91-bc9bbf4aa301"),
        Package () {
            Package () { "random-property", 0 },
        }
    })
}

Device (DEV1)
{
    Name (_DSD, Package () {
        ToUUID("daffd814-6eba-4d8c-8a91-bc9bbf4aa301"),
        Package () {
            Package () { "reference", "^DEV0.ANOD" }
            },
        }
    })
}
```

Please also see a graph example in [Documentation/firmware-guide/acpi/dsd/graph.rst](~kernel/hardware/firmware-guide/acpi-dsd/graph).

<a id="rst-references"></a>

## References

- **\[dsd-guide\] DSD Guide.**

  [https://github.com/UEFI/DSD-Guide/blob/main/dsd-guide.adoc](<https://github.com/UEFI/DSD-Guide/blob/main/dsd-guide.adoc>), referenced 2021-11-30.
