---
title: "SoC Platforms with DTS Compliance Requirements"
type: reference
description: "SoC platforms or subarchitectures should follow all the rules from Documentation/process/maintainer-soc.rst. This document referenced in MAINTAINERS impose additional requirements listed below."
---

<a id="rst-soc-platforms-with-dts-compliance-requirements"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

<a id="rst-overview"></a>

## Overview

SoC platforms or subarchitectures should follow all the rules from [Documentation/process/maintainer-soc.rst](~kernel/development/process/maintainer-soc).  This document referenced in MAINTAINERS impose additional requirements listed below.

<a id="rst-strict-dts-dt-schema-and-dtc-compliance"></a>

## Strict DTS DT Schema and dtc Compliance

No changes to the SoC platform Devicetree sources (DTS files) should introduce new `make dtbs_check W=1` warnings.  Warnings in a new board DTS, which are results of issues in an included DTSI file, are considered existing, not new warnings.  For series split between different trees (DT bindings go via driver subsystem tree), warnings on linux-next are decisive.  The platform maintainers have automation in place which should point out any new warnings.

If a commit introducing new warnings gets accepted somehow, the resulting issues shall be fixed in reasonable time (e.g. within one release) or the commit reverted.
