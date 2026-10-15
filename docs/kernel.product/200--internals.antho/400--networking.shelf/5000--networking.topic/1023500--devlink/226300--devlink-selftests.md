---
title: "Devlink Selftests"
type: reference
description: "The devlink-selftests API allows executing selftests on the device."
---

<a id="rst-devlink-selftests"></a>

<!-- SPDX-License-Identifier: (GPL-2.0-only OR BSD-2-Clause) -->

The `devlink-selftests` API allows executing selftests on the device.

<a id="rst-tests-mask"></a>

## Tests Mask

The `devlink-selftests` command should be run with a mask indicating the tests to be executed.

<a id="rst-tests-description"></a>

## Tests Description

The following is a list of tests that drivers may execute.


<table>
<caption>List of tests</caption>
<tbody>
<tr>
<td>


Name

</td>
<td>


Description

</td>
</tr>
<tr>
<td>


`DEVLINK_SELFTEST_FLASH`

</td>
<td>


Devices may have the firmware on non-volatile memory on the board, e.g. flash. This particular test helps to run a flash selftest on the device. Implementation of the test is left to the driver/firmware.

</td>
</tr>
</tbody>
</table>

<a id="rst-example-usage"></a>

### example usage



```shell
# Query selftests supported on the devlink device
$ devlink dev selftests show DEV
# Query selftests supported on all devlink devices
$ devlink dev selftests show
# Executes selftests on the device
$ devlink dev selftests run DEV id flash
```
