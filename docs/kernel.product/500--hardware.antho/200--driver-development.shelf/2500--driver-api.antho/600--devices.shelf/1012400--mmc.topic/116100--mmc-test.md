---
title: "MMC Test Framework"
type: reference
description: "The mmc_test framework is designed to test the performance and reliability of host controller drivers and all devices handled by the MMC subsystem. This includes not only MMC devices but also SD cards and other devices supported by the…"
---

<a id="rst-mmc-test-framework"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

<a id="rst-overview"></a>

## Overview

The `mmc_test` framework is designed to test the performance and reliability of host controller drivers and all devices handled by the MMC subsystem. This includes not only MMC devices but also SD cards and other devices supported by the subsystem.

The framework provides a variety of tests to evaluate different aspects of the host controller and device interactions, such as read and write performance, data integrity, and error handling. These tests help ensure that the host controller drivers and devices operate correctly under various conditions.

The `mmc_test` framework is particularly useful for:

- Verifying the functionality and performance of MMC and SD host controller drivers.

- Ensuring compatibility and reliability of MMC and SD devices.

- Identifying and diagnosing issues in the MMC subsystem.

The results of the tests are logged in the kernel log, providing detailed information about the test outcomes and any encountered issues.

Note: whatever is on your card will be overwritten by these tests.

<a id="rst-initialization"></a>

## Initialization

To use the `mmc_test` framework, follow these steps:

1. **Enable the MMC Test Framework**:

   Ensure that the `CONFIG_MMC_TEST` kernel configuration option is enabled. This can be done by configuring the kernel:



   ```none
   make menuconfig
   ```

   Navigate to:

   - **Device Drivers  ---&gt;**

     - **&lt;\*&gt; MMC/SD/SDIO card support  ---&gt;**

       \[\*\]   MMC host test driver

   Alternatively, you can enable it directly in the kernel configuration file:



   ```none
   echo "CONFIG_MMC_TEST=y" >> .config
   ```

   Rebuild and install the kernel if necessary.

2. **Load the MMC Test Module**:

   If the `mmc_test` framework is built as a module, you need to load it using `modprobe`:



   ```none
   modprobe mmc_test
   ```

<a id="rst-binding-the-mmc-card-for-testing"></a>

## Binding the MMC Card for Testing

To enable MMC testing, you need to unbind the MMC card from the `mmcblk` driver and bind it to the `mmc_test` driver. This allows the `mmc_test` framework to take control of the MMC card for testing purposes.

1. Identify the MMC card:



   ```sh
   ls /sys/bus/mmc/devices/
   ```

   This will list the MMC devices, such as `mmc0:0001`.

2. Unbind the MMC card from the `mmcblk` driver:



   ```sh
   echo 'mmc0:0001' > /sys/bus/mmc/drivers/mmcblk/unbind
   ```

3. Bind the MMC card to the `mmc_test` driver:



   ```sh
   echo 'mmc0:0001' > /sys/bus/mmc/drivers/mmc_test/bind
   ```

After binding, you should see a line in the kernel log indicating that the card has been claimed for testing:



```none
mmc_test mmc0:0001: Card claimed for testing.
```

<a id="rst-usage-debugfs-entries"></a>

## Usage - Debugfs Entries

Once the `mmc_test` framework is enabled, you can interact with the following debugfs entries located in `/sys/kernel/debug/mmc0/mmc0:0001`:

1. **test**:

   This file is used to run specific tests. Write the test number to this file to execute a test.



   ```sh
   echo <test_number> > /sys/kernel/debug/mmc0/mmc0:0001/test
   ```

   The test result is indicated in the kernel log info. You can view the kernel log using the `dmesg` command or by checking the log file in `/var/log/`.



   ```sh
   dmesg | grep mmc0
   ```

   Example:

   To run test number 4 (Basic read with data verification):



   ```sh
   echo 4 > /sys/kernel/debug/mmc0/mmc0:0001/test
   ```

   Check the kernel log for the result:



   ```sh
   dmesg | grep mmc0
   ```

2. **testlist**:

   This file lists all available tests. You can read this file to see the list of tests and their corresponding numbers.



   ```sh
   cat /sys/kernel/debug/mmc0/mmc0:0001/testlist
   ```

   The available tests are listed in the table below:


<table>
<thead>
<tr>
<th>


Test

</th>
<th>


Test Name

</th>
<th>


Test Description

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


0

</td>
<td>


Run all tests

</td>
<td>


Runs all available tests

</td>
</tr>
<tr>
<td>


1

</td>
<td>


Basic write

</td>
<td>


Performs a basic write operation of a single 512-Byte block to the MMC card without data verification.

</td>
</tr>
<tr>
<td>


2

</td>
<td>


Basic read

</td>
<td>


Same for read

</td>
</tr>
<tr>
<td>


3

</td>
<td>


Basic write (with data verification)

</td>
<td>


Performs a basic write operation of a single 512-Byte block to the MMC card with data verification by reading back the written data and comparing it.

</td>
</tr>
<tr>
<td>


4

</td>
<td>


Basic read (with data verification)

</td>
<td>


Same for read

</td>
</tr>
<tr>
<td>


5

</td>
<td>


Multi-block write

</td>
<td>


Performs a multi-block write operation of 8 blocks (each 512 bytes) to the MMC card.

</td>
</tr>
<tr>
<td>


6

</td>
<td>


Multi-block read

</td>
<td>


Same for read

</td>
</tr>
<tr>
<td>


7

</td>
<td>


Power of two block writes

</td>
<td>


Performs write operations with block sizes that are powers of two, starting from 1 byte up to 256 bytes, to the MMC card.

</td>
</tr>
<tr>
<td>


8

</td>
<td>


Power of two block reads

</td>
<td>


Same for read

</td>
</tr>
<tr>
<td>


9

</td>
<td>


Weird sized block writes

</td>
<td>


Performs write operations with varying block sizes starting from 3 bytes and increasing by 7 bytes each iteration, up to 511 bytes, to the MMC card.

</td>
</tr>
<tr>
<td>


10

</td>
<td>


Weird sized block reads

</td>
<td>


same for read

</td>
</tr>
<tr>
<td>


11

</td>
<td>


Badly aligned write

</td>
<td>


Performs write operations with buffers starting at different alignments (0 to 7 bytes offset) to test how the MMC card handles unaligned data transfers.

</td>
</tr>
<tr>
<td>


12

</td>
<td>


Badly aligned read

</td>
<td>


same for read

</td>
</tr>
<tr>
<td>


13

</td>
<td>


Badly aligned multi-block write

</td>
<td>


same for multi-write

</td>
</tr>
<tr>
<td>


14

</td>
<td>


Badly aligned multi-block read

</td>
<td>


same for multi-read

</td>
</tr>
<tr>
<td>


15

</td>
<td>


Proper xfer_size at write (Start failure)

</td>
<td>


intentionally create a broken transfer by modifying the MMC request in a way that it will not perform as expected, e.g. use MMC_WRITE_BLOCK  for a multi-block transfer

</td>
</tr>
<tr>
<td>


16

</td>
<td>


Proper xfer_size at read (Start failure)

</td>
<td>


same for read

</td>
</tr>
<tr>
<td>


17

</td>
<td>


Proper xfer_size at write (Midway failure)

</td>
<td>


same for 2 blocks

</td>
</tr>
<tr>
<td>


18

</td>
<td>


Proper xfer_size at read (Midway failure)

</td>
<td>


same for read

</td>
</tr>
<tr>
<td>


19

</td>
<td>


Highmem write

</td>
<td>


use a high memory page

</td>
</tr>
<tr>
<td>


20

</td>
<td>


Highmem read

</td>
<td>


same for read

</td>
</tr>
<tr>
<td>


21

</td>
<td>


Multi-block highmem write

</td>
<td>


same for multi-write

</td>
</tr>
<tr>
<td>


22

</td>
<td>


Multi-block highmem read

</td>
<td>


same for mult-read

</td>
</tr>
<tr>
<td>


23

</td>
<td>


Best-case read performance

</td>
<td>


Performs 512K sequential read (non sg)

</td>
</tr>
<tr>
<td>


24

</td>
<td>


Best-case write performance

</td>
<td>


same for write

</td>
</tr>
<tr>
<td>


25

</td>
<td>


Best-case read performance (Into scattered pages)

</td>
<td>


Same using sg

</td>
</tr>
<tr>
<td>


26

</td>
<td>


Best-case write performance (From scattered pages)

</td>
<td>


same for write

</td>
</tr>
<tr>
<td>


27

</td>
<td>


Single read performance

</td>
<td>


By transfer size

</td>
</tr>
<tr>
<td>


28

</td>
<td>


Single write performance

</td>
<td>


By transfer size

</td>
</tr>
<tr>
<td>


29

</td>
<td>


Single trim performance

</td>
<td>


By transfer size

</td>
</tr>
<tr>
<td>


30

</td>
<td>


Consecutive read performance

</td>
<td>


By transfer size

</td>
</tr>
<tr>
<td>


31

</td>
<td>


Consecutive write performance

</td>
<td>


By transfer size

</td>
</tr>
<tr>
<td>


32

</td>
<td>


Consecutive trim performance

</td>
<td>


By transfer size

</td>
</tr>
<tr>
<td>


33

</td>
<td>


Random read performance

</td>
<td>


By transfer size

</td>
</tr>
<tr>
<td>


34

</td>
<td>


Random write performance

</td>
<td>


By transfer size

</td>
</tr>
<tr>
<td>


35

</td>
<td>


Large sequential read

</td>
<td>


Into scattered pages

</td>
</tr>
<tr>
<td>


36

</td>
<td>


Large sequential write

</td>
<td>


From scattered pages

</td>
</tr>
<tr>
<td>


37

</td>
<td>


Write performance

</td>
<td>


With blocking req 4k to 4MB

</td>
</tr>
<tr>
<td>


38

</td>
<td>


Write performance

</td>
<td>


With non-blocking req 4k to 4MB

</td>
</tr>
<tr>
<td>


39

</td>
<td>


Read performance

</td>
<td>


With blocking req 4k to 4MB

</td>
</tr>
<tr>
<td>


40

</td>
<td>


Read performance

</td>
<td>


With non-blocking req 4k to 4MB

</td>
</tr>
<tr>
<td>


41

</td>
<td>


Write performance

</td>
<td>


Blocking req 1 to 512 sg elems

</td>
</tr>
<tr>
<td>


42

</td>
<td>


Write performance

</td>
<td>


Non-blocking req 1 to 512 sg elems

</td>
</tr>
<tr>
<td>


43

</td>
<td>


Read performance

</td>
<td>


Blocking req 1 to 512 sg elems

</td>
</tr>
<tr>
<td>


44

</td>
<td>


Read performance

</td>
<td>


Non-blocking req 1 to 512 sg elems

</td>
</tr>
<tr>
<td>


45

</td>
<td>


Reset test

</td>
<td>




</td>
</tr>
<tr>
<td>


46

</td>
<td>


Commands during read

</td>
<td>


No Set Block Count (CMD23)

</td>
</tr>
<tr>
<td>


47

</td>
<td>


Commands during write

</td>
<td>


No Set Block Count (CMD23)

</td>
</tr>
<tr>
<td>


48

</td>
<td>


Commands during read

</td>
<td>


Use Set Block Count (CMD23)

</td>
</tr>
<tr>
<td>


49

</td>
<td>


Commands during write

</td>
<td>


Use Set Block Count (CMD23)

</td>
</tr>
<tr>
<td>


50

</td>
<td>


Commands during non-blocking

</td>
<td>


Read - use Set Block Count (CMD23)

</td>
</tr>
<tr>
<td>


51

</td>
<td>


Commands during non-blocking

</td>
<td>


Write - use Set Block Count (CMD23)

</td>
</tr>
</tbody>
</table>

<a id="rst-test-results"></a>

## Test Results

The results of the tests are logged in the kernel log. Each test logs the start, end, and result of the test. The possible results are:

- **OK**: The test completed successfully.

- **FAILED**: The test failed.

- **UNSUPPORTED (by host)**: The test is unsupported by the host.

- **UNSUPPORTED (by card)**: The test is unsupported by the card.

- **ERROR**: An error occurred during the test.

<a id="rst-example-kernel-log-output"></a>

## Example Kernel Log Output

When running a test, you will see log entries similar to the following in the kernel log:



```none
[ 1234.567890] mmc0: Starting tests of card mmc0:0001...
[ 1234.567891] mmc0: Test case 4. Basic read (with data verification)...
[ 1234.567892] mmc0: Result: OK
[ 1234.567893] mmc0: Tests completed.
```

In this example, test case 4 (Basic read with data verification) was executed, and the result was OK.

<a id="rst-contributing"></a>

## Contributing

Contributions to the `mmc_test` framework are welcome. Please follow the standard Linux kernel contribution guidelines and submit patches to the appropriate maintainers.

<a id="rst-contact"></a>

## Contact

For more information or to report issues, please contact the MMC subsystem maintainers.
