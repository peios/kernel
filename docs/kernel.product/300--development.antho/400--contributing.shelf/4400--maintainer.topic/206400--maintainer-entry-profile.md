---
title: "Maintainer Entry Profile"
type: reference
description: "The Maintainer Entry Profile supplements the top-level process documents (submitting-patches, submitting drivers...) with subsystem/device-driver-local customs as well as details about the patch submission life-cycle. A contributor uses…"
---

> **Peios:** This is inherited Linux development and upstream contribution guidance. For Peios repository changes, follow the workspace `_styleguide` and use [Building Peios](<~kernel/development/start-here/building-peios>). Upstream mailing lists, maintainer roles and release processes below apply when contributing to Linux upstream.


<a id="rst-maintainer-entry-profile"></a>
<a id="rst-maintainerentryprofile"></a>

The Maintainer Entry Profile supplements the top-level process documents (submitting-patches, submitting drivers...) with subsystem/device-driver-local customs as well as details about the patch submission life-cycle. A contributor uses this document to level set their expectations and avoid common mistakes; maintainers may use these profiles to look across subsystems for opportunities to converge on common practices.

<a id="rst-overview"></a>

## Overview

Provide an introduction to how the subsystem operates. While MAINTAINERS tells the contributor where to send patches for which files, it does not convey other subsystem-local infrastructure and mechanisms that aid development.

Example questions to consider:

- Are there notifications when patches are applied to the local tree, or merged upstream?

- Does the subsystem have a patchwork instance? Are patchwork state changes notified?

- Any bots or CI infrastructure that watches the list, or automated testing feedback that the subsystem uses to gate acceptance?

- Git branches that are pulled into -next?

- What branch should contributors submit against?

- Links to any other Maintainer Entry Profiles? For example a device-driver may point to an entry for its parent subsystem. This makes the contributor aware of obligations a maintainer may have for other maintainers in the submission chain.

<a id="rst-submit-checklist-addendum"></a>

## Submit Checklist Addendum

List mandatory and advisory criteria, beyond the common "submit-checklist", for a patch to be considered healthy enough for maintainer attention. For example: "pass checkpatch.pl with no errors, or warning. Pass the unit test detailed at $URI".

The Submit Checklist Addendum can also include details about the status of related hardware specifications. For example, does the subsystem require published specifications at a certain revision before patches will be considered.

<a id="rst-key-cycle-dates"></a>

## Key Cycle Dates

One of the common misunderstandings of submitters is that patches can be sent at any time before the merge window closes and can still be considered for the next -rc1. The reality is that most patches need to be settled in soaking in linux-next in advance of the merge window opening. Clarify for the submitter the key dates (in terms of -rc release week) that patches might be considered for merging and when patches need to wait for the next -rc. At a minimum:

- Last -rc for new feature submissions:

  New feature submissions targeting the next merge window should have their first posting for consideration before this point. Patches that are submitted after this point should be clear that they are targeting the NEXT+1 merge window, or should come with sufficient justification why they should be considered on an expedited schedule. A general guideline is to set expectation with contributors that new feature submissions should appear before -rc5.

- Last -rc to merge features: Deadline for merge decisions

  Indicate to contributors the point at which an as yet un-applied patch set will need to wait for the NEXT+1 merge window. Of course there is no obligation to ever accept any given patchset, but if the review has not concluded by this point the expectation is the contributor should wait and resubmit for the following merge window.

Optional:

- First -rc at which the development baseline branch, listed in the overview section, should be considered ready for new submissions.

<a id="rst-review-cadence"></a>

## Review Cadence

One of the largest sources of contributor angst is how soon to ping after a patchset has been posted without receiving any feedback. In addition to specifying how long to wait before a resubmission this section can also indicate a preferred style of update like, resend the full series, or privately send a reminder email. This section might also list how review works for this code area and methods to get feedback that are not directly from the maintainer.

<a id="rst-existing-profiles"></a>

## Existing profiles

For now, existing maintainer profiles are listed here; we will likely want to do something different in the near future.

- [Documentation subsystem maintainer entry profile](<~kernel/development/doc-guide/maintainer-profile>)
- [LIBNVDIMM Maintainer Entry Profile](<~kernel/hardware/nvdimm/maintainer-entry-profile>)
- [arch/riscv maintenance guidelines for developers](<~kernel/hardware/arch/riscv/patch-acceptance>)
- [SoC Subsystem](<~kernel/development/process/maintainer-soc>)
- [SoC Platforms with DTS Compliance Requirements](<~kernel/development/process/maintainer-soc-clean-dts>)
- [Media Subsystem Profile](<~kernel/hardware/driver-api/media/maintainer-entry-profile>)
- [Networking subsystem (netdev)](<~kernel/development/process/maintainer-netdev>)
- [Acceptance criteria for vfio-pci device specific driver variants](<~kernel/hardware/driver-api/fundamentals/vfio-pci-device-specific-driver-acceptance>)
- [Linux NVMe feature and quirk policy](<~kernel/hardware/nvme/feature-and-quirk-policy>)
- [NFSD Maintainer Entry Profile](<~kernel/internals/filesystems/nfs/nfsd-maintainer-entry-profile>)
- [XFS Maintainer Entry Profile](<~kernel/internals/filesystems/xfs/xfs-maintainer-entry-profile>)
- [DAMON Maintainer Entry Profile](<~kernel/internals/mm/damon/maintainer-profile>)
