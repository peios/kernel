---
title: "Null block device driver"
type: reference
description: "The null block device (/dev/nullb*) is used for benchmarking the various block-layer implementations. It emulates a block device of X gigabytes in size. It does not execute any read/write operation, just mark them as complete in the…"
---

<a id="rst-null-block-device-driver"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

<a id="rst-overview"></a>

## Overview

The null block device (`/dev/nullb*`) is used for benchmarking the various block-layer implementations. It emulates a block device of X gigabytes in size. It does not execute any read/write operation, just mark them as complete in the request queue. The following instances are possible:

> Multi-queue block-layer
>
> > - Request-based.
> >
> > - Configurable submission queues per device.
>
> No block-layer (Known as bio-based)
>
> > - Bio-based. IO requests are submitted directly to the device driver.
> >
> > - Directly accepts bio data structure and returns them.

All of them have a completion queue for each core in the system.

<a id="rst-module-parameters"></a>

## Module parameters

- **queue_mode=\[0-2\]: Default: 2-Multi-queue**

  Selects which block-layer the module should instantiate with.


  <table>
  <tbody>
  <tr>
  <td>


  0

  </td>
  <td>


  Bio-based

  </td>
  </tr>
  <tr>
  <td>


  1

  </td>
  <td>


  Single-queue (deprecated)

  </td>
  </tr>
  <tr>
  <td>


  2

  </td>
  <td>


  Multi-queue

  </td>
  </tr>
  </tbody>
  </table>

- **home_node=\[0--nr_nodes\]: Default: NUMA_NO_NODE**

  Selects what CPU node the data structures are allocated from.

- **gb=\[Size in GB\]: Default: 250GB**

  The size of the device reported to the system.

- **bs=\[Block size (in bytes)\]: Default: 512 bytes**

  The block size reported to the system.

- **nr_devices=\[Number of devices\]: Default: 1**

  Number of block devices instantiated. They are instantiated as /dev/nullb0, etc.

- **irqmode=\[0-2\]: Default: 1-Soft-irq**

  The completion mode used for completing IOs to the block-layer.


  <table>
  <tbody>
  <tr>
  <td>


  0

  </td>
  <td>


  None.

  </td>
  </tr>
  <tr>
  <td>


  1

  </td>
  <td>


  Soft-irq. Uses IPI to complete IOs across CPU nodes. Simulates the overhead when IOs are issued from another CPU node than the home the device is connected to.

  </td>
  </tr>
  <tr>
  <td>


  2

  </td>
  <td>


  Timer: Waits a specific period (completion_nsec) for each IO before completion.

  </td>
  </tr>
  </tbody>
  </table>

- **completion_nsec=\[ns\]: Default: 10,000ns**

  Combined with irqmode=2 (timer). The time each completion event must wait.

- **submit_queues=\[1..nr_cpus\]: Default: 1**

  The number of submission queues attached to the device driver. If unset, it defaults to 1. For multi-queue, it is ignored when use_per_node_hctx module parameter is 1.

- **hw_queue_depth=\[0..qdepth\]: Default: 64**

  The hardware queue depth of the device.

- **memory_backed=\[0/1\]: Default: 0**

  Whether or not to use a memory buffer to respond to IO requests


  <table>
  <tbody>
  <tr>
  <td>


  0

  </td>
  <td>


  Transfer no data in response to IO requests

  </td>
  </tr>
  <tr>
  <td>


  1

  </td>
  <td>


  Use a memory buffer to respond to IO requests

  </td>
  </tr>
  </tbody>
  </table>

- **discard=\[0/1\]: Default: 0**

  Support discard operations (requires memory-backed null_blk device).


  <table>
  <tbody>
  <tr>
  <td>


  0

  </td>
  <td>


  Do not support discard operations

  </td>
  </tr>
  <tr>
  <td>


  1

  </td>
  <td>


  Enable support for discard operations

  </td>
  </tr>
  </tbody>
  </table>

- **cache_size=\[Size in MB\]: Default: 0**

  Cache size in MB for memory-backed device.

- **mbps=\[Maximum bandwidth in MB/s\]: Default: 0 (no limit)**

  Bandwidth limit for device performance.

<a id="rst-multi-queue-specific-parameters"></a>

### Multi-queue specific parameters

- **use_per_node_hctx=\[0/1\]: Default: 0**

  Number of hardware context queues.


  <table>
  <tbody>
  <tr>
  <td>


  0

  </td>
  <td>


  The number of submit queues are set to the value of the submit_queues parameter.

  </td>
  </tr>
  <tr>
  <td>


  1

  </td>
  <td>


  The multi-queue block layer is instantiated with a hardware dispatch queue for each CPU node in the system.

  </td>
  </tr>
  </tbody>
  </table>

- **no_sched=\[0/1\]: Default: 0**

  Enable/disable the io scheduler.


  <table>
  <tbody>
  <tr>
  <td>


  0

  </td>
  <td>


  nullb\* use default blk-mq io scheduler

  </td>
  </tr>
  <tr>
  <td>


  1

  </td>
  <td>


  nullb\* doesn't use io scheduler

  </td>
  </tr>
  </tbody>
  </table>

- **blocking=\[0/1\]: Default: 0**

  Blocking behavior of the request queue.


  <table>
  <tbody>
  <tr>
  <td>


  0

  </td>
  <td>


  Register as a non-blocking blk-mq driver device.

  </td>
  </tr>
  <tr>
  <td>


  1

  </td>
  <td>


  Register as a blocking blk-mq driver device, null_blk will set the BLK_MQ_F_BLOCKING flag, indicating that it sometimes/always needs to block in its -&gt;queue_rq() function.

  </td>
  </tr>
  </tbody>
  </table>

- **shared_tags=\[0/1\]: Default: 0**

  Sharing tags between devices.


  <table>
  <tbody>
  <tr>
  <td>


  0

  </td>
  <td>


  Tag set is not shared.

  </td>
  </tr>
  <tr>
  <td>


  1

  </td>
  <td>


  Tag set shared between devices for blk-mq. Only makes sense with nr_devices &gt; 1, otherwise there's no tag set to share.

  </td>
  </tr>
  </tbody>
  </table>

- **zoned=\[0/1\]: Default: 0**

  Device is a random-access or a zoned block device.


  <table>
  <tbody>
  <tr>
  <td>


  0

  </td>
  <td>


  Block device is exposed as a random-access block device.

  </td>
  </tr>
  <tr>
  <td>


  1

  </td>
  <td>


  Block device is exposed as a host-managed zoned block device. Requires CONFIG_BLK_DEV_ZONED.

  </td>
  </tr>
  </tbody>
  </table>

- **zone_size=\[MB\]: Default: 256**

  Per zone size when exposed as a zoned block device. Must be a power of two.

- **zone_nr_conv=\[nr_conv\]: Default: 0**

  The number of conventional zones to create when block device is zoned.  If zone_nr_conv &gt;= nr_zones, it will be reduced to nr_zones - 1.
