---
title: "Operating the Peios kernel"
type: guide
description: "Choose a guide for configuration, tuning or diagnosis."
---

<a id="rst-the-linux-kernel-user-s-and-administrator-s-guide"></a>
<a id="rst-general-guides-to-kernel-administration"></a>
<a id="rst-booting-the-kernel"></a>
<a id="rst-tracking-down-and-identifying-problems"></a>
<a id="rst-core-kernel-subsystems"></a>
<a id="rst-block-layer-and-filesystem-administration"></a>
<a id="rst-device-specific-guides"></a>
<a id="rst-workload-analysis"></a>
<a id="rst-everything-else"></a>

Use these guides to configure the kernel, understand resource use and investigate
problems on a running system. Device-specific behaviour is grouped separately
from general operating tasks.

- **Boot and configuration:** [Kernel parameters](<~kernel/administration/admin-guide/boot/kernel-parameters>),
  [Boot configuration](<~kernel/administration/admin-guide/boot/bootconfig>) and
  [Runtime settings](<~kernel/administration/admin-guide/sysctl/index>).
- **Resources and performance:** [Control groups v2](<~kernel/administration/admin-guide/resources/cgroup-v2>),
  [Memory tuning](<~kernel/administration/admin-guide/mm/index>),
  [Performance monitoring](<~kernel/administration/admin-guide/perf/index>) and
  [Power management](<~kernel/administration/admin-guide/pm/index>).
- **Storage:** browse the filesystem and storage guides, or start with
  [Device mapper](<~kernel/administration/admin-guide/device-mapper/index>) and
  [NFS](<~kernel/administration/admin-guide/nfs/index>).
- **Troubleshooting and recovery:** [Bug hunting](<~kernel/administration/admin-guide/diagnostics/bug-hunting>),
  [Crash dumps](<~kernel/administration/admin-guide/kdump/index>) and
  [Reporting regressions](<~kernel/administration/admin-guide/diagnostics/reporting-regressions>).
- **Security and reliability:** [CPU vulnerabilities](<~kernel/administration/admin-guide/hw-vuln/index>)
  and [Reliability and hardware errors](<~kernel/administration/admin-guide/ras/index>).
- **Interfaces:** the [Kernel ABI catalogue](<~kernel/administration/admin-guide/abi/abi>)
  complements the [Userspace interface reference](<~kernel/userspace/userspace-api/overview/index>).

Inherited Linux guides may refer to distribution tools or configurations that
differ from Peios. Check the configuration of the system you are operating
before applying a device-specific or platform-specific procedure.
