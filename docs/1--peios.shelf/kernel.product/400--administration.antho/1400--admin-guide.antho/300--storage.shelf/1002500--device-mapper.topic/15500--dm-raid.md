---
title: "dm-raid"
type: reference
description: "The device-mapper RAID (dm-raid) target provides a bridge from DM to MD. It allows the MD RAID drivers to be accessed using a device-mapper interface."
---

<a id="rst-dm-raid"></a>

The device-mapper RAID (dm-raid) target provides a bridge from DM to MD. It allows the MD RAID drivers to be accessed using a device-mapper interface.

<a id="rst-mapping-table-interface"></a>

## Mapping Table Interface

The target is named "raid" and it accepts the following parameters:



```text
<raid_type> <#raid_params> <raid_params> \
  <#raid_devs> <metadata_dev0> <dev0> [.. <metadata_devN> <devN>]
```

&lt;raid_type&gt;:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> raid0
>
> </td>
> <td>
>
>
> RAID0 striping (no resilience)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> raid1
>
> </td>
> <td>
>
>
> RAID1 mirroring
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> raid4
>
> </td>
> <td>
>
>
> RAID4 with dedicated last parity disk
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> raid5_n
>
> </td>
> <td>
>
>
> RAID5 with dedicated last parity disk supporting takeover from/to raid1 Same as raid4
>
> - Transitory layout for takeover from/to raid1
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> raid5_la
>
> </td>
> <td>
>
>
> RAID5 left asymmetric
>
> - rotating parity 0 with data continuation
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> raid5_ra
>
> </td>
> <td>
>
>
> RAID5 right asymmetric
>
> - rotating parity N with data continuation
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> raid5_ls
>
> </td>
> <td>
>
>
> RAID5 left symmetric
>
> - rotating parity 0 with data restart
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> raid5_rs
>
> </td>
> <td>
>
>
> RAID5 right symmetric
>
> - rotating parity N with data restart
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> raid6_zr
>
> </td>
> <td>
>
>
> RAID6 zero restart
>
> - rotating parity zero (left-to-right) with data restart
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> raid6_nr
>
> </td>
> <td>
>
>
> RAID6 N restart
>
> - rotating parity N (right-to-left) with data restart
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> raid6_nc
>
> </td>
> <td>
>
>
> RAID6 N continue
>
> - rotating parity N (right-to-left) with data continuation
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> raid6_n_6
>
> </td>
> <td>
>
>
> RAID6 with dedicate parity disks
>
> - parity and Q-syndrome on the last 2 disks; layout for takeover from/to raid0/raid4/raid5_n
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> raid6_la_6
>
> </td>
> <td>
>
>
> Same as "raid_la" plus dedicated last Q-syndrome disk supporting takeover from/to raid5
>
> - layout for takeover from raid5_la from/to raid6
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> raid6_ra_6
>
> </td>
> <td>
>
>
> Same as "raid5_ra" dedicated last Q-syndrome disk
>
> - layout for takeover from raid5_ra from/to raid6
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> raid6_ls_6
>
> </td>
> <td>
>
>
> Same as "raid5_ls" dedicated last Q-syndrome disk
>
> - layout for takeover from raid5_ls from/to raid6
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> raid6_rs_6
>
> </td>
> <td>
>
>
> Same as "raid5_rs" dedicated last Q-syndrome disk
>
> - layout for takeover from raid5_rs from/to raid6
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> raid10
>
> </td>
> <td>
>
>
> Various RAID10 inspired algorithms chosen by additional params (see raid10_format and raid10_copies below)
>
> - RAID10: Striped Mirrors (aka 'Striping on top of mirrors')
>
> - RAID1E: Integrated Adjacent Stripe Mirroring
>
> - RAID1E: Integrated Offset Stripe Mirroring
>
> - and other similar RAID10 variants
>
> </td>
> </tr>
> </tbody>
> </table>
>
> Reference: Chapter 4 of [https://www.snia.org/sites/default/files/SNIA_DDF_Technical_Position_v2.0.pdf](<https://www.snia.org/sites/default/files/SNIA_DDF_Technical_Position_v2.0.pdf>)

&lt;\#raid_params&gt;: The number of parameters that follow.

&lt;raid_params&gt; consists of

> - **Mandatory parameters:**
>
>   - **&lt;chunk_size&gt;:**
>
>     Chunk size in sectors.  This parameter is often known as "stripe size".  It is the only mandatory parameter and is placed first.
>
> - **followed by optional parameters (in any order):**
>
>   - **\[sync\|nosync\]**
>
>     Force or prevent RAID initialization.
>
>   - **\[rebuild &lt;idx&gt;\]**
>
>     Rebuild drive number 'idx' (first drive is 0).
>
>   - **\[daemon_sleep &lt;ms&gt;\]**
>
>     Interval between runs of the bitmap daemon that clear bits.  A longer interval means less bitmap I/O but resyncing after a failure is likely to take longer.
>
>   - **\[min_recovery_rate &lt;kB/sec/disk&gt;\]**
>
>     Throttle RAID initialization
>
>   - **\[max_recovery_rate &lt;kB/sec/disk&gt;\]**
>
>     Throttle RAID initialization
>
>   - **\[write_mostly &lt;idx&gt;\]**
>
>     Mark drive index 'idx' write-mostly.
>
>   - **\[max_write_behind &lt;sectors&gt;\]**
>
>     See '--write-behind=' (man mdadm)
>
>   - **\[stripe_cache &lt;sectors&gt;\]**
>
>     Stripe cache size (RAID 4/5/6 only)
>
>   - **\[region_size &lt;sectors&gt;\]**
>
>     The region_size multiplied by the number of regions is the logical size of the array.  The bitmap records the device synchronisation state for each region.
>
>   - **\[raid10_copies   &lt;\# copies&gt;\], \[raid10_format   &lt;near\|far\|offset&gt;\]**
>
>     These two options are used to alter the default layout of a RAID10 configuration.  The number of copies is can be specified, but the default is 2.  There are also three variations to how the copies are laid down - the default is "near".  Near copies are what most people think of with respect to mirroring.  If these options are left unspecified, or 'raid10_copies 2' and/or 'raid10_format near' are given, then the layouts for 2, 3 and 4 devices are:
>
>
>     <table>
>     <thead>
>     <tr>
>     <th>
>
>
>     2 drives
>
>     </th>
>     <th>
>
>
>     3 drives
>
>     </th>
>     <th>
>
>
>     4 drives
>
>     </th>
>     </tr>
>     </thead>
>     <tbody>
>     <tr>
>     <td>
>
>
>     A1  A1
>
>     </td>
>     <td>
>
>
>     A1  A1  A2
>
>     </td>
>     <td>
>
>
>     A1  A1  A2  A2
>
>     </td>
>     </tr>
>     <tr>
>     <td>
>
>
>     A2  A2
>
>     </td>
>     <td>
>
>
>     A2  A3  A3
>
>     </td>
>     <td>
>
>
>     A3  A3  A4  A4
>
>     </td>
>     </tr>
>     <tr>
>     <td>
>
>
>     A3  A3
>
>     </td>
>     <td>
>
>
>     A4  A4  A5
>
>     </td>
>     <td>
>
>
>     A5  A5  A6  A6
>
>     </td>
>     </tr>
>     <tr>
>     <td>
>
>
>     A4  A4
>
>     </td>
>     <td>
>
>
>     A5  A6  A6
>
>     </td>
>     <td>
>
>
>     A7  A7  A8  A8
>
>     </td>
>     </tr>
>     <tr>
>     <td>
>
>
>     <!-- .. -->
>
>     </td>
>     <td>
>
>
>     <!-- ..  .. -->
>
>     </td>
>     <td>
>
>
>     <!-- ..  ..  .. -->
>
>     </td>
>     </tr>
>     </tbody>
>     </table>
>
>     The 2-device layout is equivalent 2-way RAID1.  The 4-device layout is what a traditional RAID10 would look like.  The 3-device layout is what might be called a 'RAID1E - Integrated Adjacent Stripe Mirroring'.
>
>     If 'raid10_copies 2' and 'raid10_format far', then the layouts for 2, 3 and 4 devices are:
>
>
>     <table>
>     <thead>
>     <tr>
>     <th>
>
>
>     2 drives
>
>     </th>
>     <th>
>
>
>     3 drives
>
>     </th>
>     <th>
>
>
>     4 drives
>
>     </th>
>     </tr>
>     </thead>
>     <tbody>
>     <tr>
>     <td>
>
>
>     A1  A2
>
>     </td>
>     <td>
>
>
>     A1   A2   A3
>
>     </td>
>     <td>
>
>
>     A1   A2   A3   A4
>
>     </td>
>     </tr>
>     <tr>
>     <td>
>
>
>     A3  A4
>
>     </td>
>     <td>
>
>
>     A4   A5   A6
>
>     </td>
>     <td>
>
>
>     A5   A6   A7   A8
>
>     </td>
>     </tr>
>     <tr>
>     <td>
>
>
>     A5  A6
>
>     </td>
>     <td>
>
>
>     A7   A8   A9
>
>     </td>
>     <td>
>
>
>     A9   A10  A11  A12
>
>     </td>
>     </tr>
>     <tr>
>     <td>
>
>
>     <!-- .. -->
>
>     </td>
>     <td>
>
>
>     <!-- ..   .. -->
>
>     </td>
>     <td>
>
>
>     <!-- ..   ..   .. -->
>
>     </td>
>     </tr>
>     <tr>
>     <td>
>
>
>     A2  A1
>
>     </td>
>     <td>
>
>
>     A3   A1   A2
>
>     </td>
>     <td>
>
>
>     A2   A1   A4   A3
>
>     </td>
>     </tr>
>     <tr>
>     <td>
>
>
>     A4  A3
>
>     </td>
>     <td>
>
>
>     A6   A4   A5
>
>     </td>
>     <td>
>
>
>     A6   A5   A8   A7
>
>     </td>
>     </tr>
>     <tr>
>     <td>
>
>
>     A6  A5
>
>     </td>
>     <td>
>
>
>     A9   A7   A8
>
>     </td>
>     <td>
>
>
>     A10  A9   A12  A11
>
>     </td>
>     </tr>
>     <tr>
>     <td>
>
>
>     <!-- .. -->
>
>     </td>
>     <td>
>
>
>     <!-- ..   .. -->
>
>     </td>
>     <td>
>
>
>     <!-- ..   ..   .. -->
>
>     </td>
>     </tr>
>     </tbody>
>     </table>
>
>     If 'raid10_copies 2' and 'raid10_format offset', then the layouts for 2, 3 and 4 devices are:
>
>
>     <table>
>     <thead>
>     <tr>
>     <th>
>
>
>     2 drives
>
>     </th>
>     <th>
>
>
>     3 drives
>
>     </th>
>     <th>
>
>
>     4 drives
>
>     </th>
>     </tr>
>     </thead>
>     <tbody>
>     <tr>
>     <td>
>
>
>     A1  A2
>
>     </td>
>     <td>
>
>
>     A1  A2  A3
>
>     </td>
>     <td>
>
>
>     A1  A2  A3  A4
>
>     </td>
>     </tr>
>     <tr>
>     <td>
>
>
>     A2  A1
>
>     </td>
>     <td>
>
>
>     A3  A1  A2
>
>     </td>
>     <td>
>
>
>     A2  A1  A4  A3
>
>     </td>
>     </tr>
>     <tr>
>     <td>
>
>
>     A3  A4
>
>     </td>
>     <td>
>
>
>     A4  A5  A6
>
>     </td>
>     <td>
>
>
>     A5  A6  A7  A8
>
>     </td>
>     </tr>
>     <tr>
>     <td>
>
>
>     A4  A3
>
>     </td>
>     <td>
>
>
>     A6  A4  A5
>
>     </td>
>     <td>
>
>
>     A6  A5  A8  A7
>
>     </td>
>     </tr>
>     <tr>
>     <td>
>
>
>     A5  A6
>
>     </td>
>     <td>
>
>
>     A7  A8  A9
>
>     </td>
>     <td>
>
>
>     A9  A10 A11 A12
>
>     </td>
>     </tr>
>     <tr>
>     <td>
>
>
>     A6  A5
>
>     </td>
>     <td>
>
>
>     A9  A7  A8
>
>     </td>
>     <td>
>
>
>     A10 A9  A12 A11
>
>     </td>
>     </tr>
>     <tr>
>     <td>
>
>
>     <!-- .. -->
>
>     </td>
>     <td>
>
>
>     <!-- ..  .. -->
>
>     </td>
>     <td>
>
>
>     <!-- ..  ..  .. -->
>
>     </td>
>     </tr>
>     </tbody>
>     </table>
>
>     Here we see layouts closely akin to 'RAID1E - Integrated Offset Stripe Mirroring'.
>
>   - **\[delta_disks &lt;N&gt;\]**
>
>     The delta_disks option value (-251 &lt; N &lt; +251) triggers device removal (negative value) or device addition (positive value) to any reshape supporting raid levels 4/5/6 and 10. RAID levels 4/5/6 allow for addition and removal of devices (metadata and data device tuple), raid10_near and raid10_offset only allow for device addition. raid10_far does not support any reshaping at all. A minimum of devices have to be kept to enforce resilience, which is 3 devices for raid4/5 and 4 devices for raid6.
>
>   - **\[data_offset &lt;sectors&gt;\]**
>
>     This option value defines the offset into each data device where the data starts. This is used to provide out-of-place reshaping space to avoid writing over data while changing the layout of stripes, hence an interruption/crash may happen at any time without the risk of losing data. E.g. when adding devices to an existing raid set during forward reshaping, the out-of-place space will be allocated at the beginning of each raid device. The kernel raid4/5/6/10 MD personalities supporting such device addition will read the data from the existing first stripes (those with smaller number of stripes) starting at data_offset to fill up a new stripe with the larger number of stripes, calculate the redundancy blocks (CRC/Q-syndrome) and write that new stripe to offset 0. Same will be applied to all N-1 other new stripes. This out-of-place scheme is used to change the RAID type (i.e. the allocation algorithm) as well, e.g. changing from raid5_ls to raid5_n.
>
>   - **\[journal_dev &lt;dev&gt;\]**
>
>     This option adds a journal device to raid4/5/6 raid sets and uses it to close the 'write hole' caused by the non-atomic updates to the component devices which can cause data loss during recovery. The journal device is used as writethrough thus causing writes to be throttled versus non-journaled raid4/5/6 sets. Takeover/reshape is not possible with a raid4/5/6 journal device; it has to be deconfigured before requesting these.
>
>   - **\[journal_mode &lt;mode&gt;\]**
>
>     This option sets the caching mode on journaled raid4/5/6 raid sets (see 'journal_dev &lt;dev&gt;' above) to 'writethrough' or 'writeback'. If 'writeback' is selected the journal device has to be resilient and must not suffer from the 'write hole' problem itself (e.g. use raid1 or raid10) to avoid a single point of failure.

- **&lt;\#raid_devs&gt;: The number of devices composing the array.**

  Each device consists of two entries.  The first is the device containing the metadata (if any); the second is the one containing the data. A Maximum of 64 metadata/data device entries are supported up to target version 1.8.0. 1.9.0 supports up to 253 which is enforced by the used MD kernel runtime.

  If a drive has failed or is missing at creation time, a '-' can be given for both the metadata and data drives for a given position.

<a id="rst-example-tables"></a>

## Example Tables



```text
# RAID4 - 4 data drives, 1 parity (no metadata devices)
# No metadata devices specified to hold superblock/bitmap info
# Chunk size of 1MiB
# (Lines separated for easy reading)

0 1960893648 raid \
        raid4 1 2048 \
        5 - 8:17 - 8:33 - 8:49 - 8:65 - 8:81

# RAID4 - 4 data drives, 1 parity (with metadata devices)
# Chunk size of 1MiB, force RAID initialization,
#       min recovery rate at 20 kiB/sec/disk

0 1960893648 raid \
        raid4 4 2048 sync min_recovery_rate 20 \
        5 8:17 8:18 8:33 8:34 8:49 8:50 8:65 8:66 8:81 8:82
```

<a id="rst-status-output"></a>

## Status Output

'dmsetup table' displays the table used to construct the mapping. The optional parameters are always printed in the order listed above with "sync" or "nosync" always output ahead of the other arguments, regardless of the order used when originally loading the table. Arguments that can be repeated are ordered by value.

'dmsetup status' yields information on the state and health of the array. The output is as follows (normally a single line, but expanded here for clarity):



```text
1: <s> <l> raid \
2:      <raid_type> <#devices> <health_chars> \
3:      <sync_ratio> <sync_action> <mismatch_cnt>
```

Line 1 is the standard output produced by device-mapper.

Line 2 &amp; 3 are produced by the raid target and are best explained by example:



```text
0 1960893648 raid raid4 5 AAAAA 2/490221568 init 0
```

Here we can see the RAID type is raid4, there are 5 devices - all of which are 'A'live, and the array is 2/490221568 complete with its initial recovery.  Here is a fuller description of the individual fields:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> &lt;raid_type&gt;
>
> </td>
> <td>
>
>
> Same as the &lt;raid_type&gt; used to create the array.
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> &lt;health_chars&gt;
>
> </td>
> <td>
>
>
> One char for each device, indicating:
>
> - 'A' = alive and in-sync
>
> - 'a' = alive but not in-sync
>
> - 'D' = dead/failed.
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> &lt;sync_ratio&gt;
>
> </td>
> <td>
>
>
> The ratio indicating how much of the array has undergone the process described by 'sync_action'.  If the 'sync_action' is "check" or "repair", then the process of "resync" or "recover" can be considered complete.
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> &lt;sync_action&gt;
>
> </td>
> <td>
>
>
> One of the following possible states:
>
> - **idle**
>
>   - No synchronization action is being performed.
>
> - **frozen**
>
>   - The current action has been halted.
>
> - **resync**
>
>   - Array is undergoing its initial synchronization or is resynchronizing after an unclean shutdown (possibly aided by a bitmap).
>
> - **recover**
>
>   - A device in the array is being rebuilt or replaced.
>
> - **check**
>
>   - A user-initiated full check of the array is being performed.  All blocks are read and checked for consistency.  The number of discrepancies found are recorded in &lt;mismatch_cnt&gt;.  No changes are made to the array by this action.
>
> - **repair**
>
>   - The same as "check", but discrepancies are corrected.
>
> - **reshape**
>
>   - The array is undergoing a reshape.
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> &lt;mismatch_cnt&gt;
>
> </td>
> <td>
>
>
> The number of discrepancies found between mirror copies in RAID1/10 or wrong parity values found in RAID4/5/6. This value is valid only after a "check" of the array is performed.  A healthy array has a 'mismatch_cnt' of 0.
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> &lt;data_offset&gt;
>
> </td>
> <td>
>
>
> The current data offset to the start of the user data on each component device of a raid set (see the respective raid parameter to support out-of-place reshaping).
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> &lt;journal_char&gt;
>
> </td>
> <td>
>
>
> - 'A' - active write-through journal device.
>
> - 'a' - active write-back journal device.
>
> - 'D' - dead journal device.
>
> - '-' - no journal device.
>
> </td>
> </tr>
> </tbody>
> </table>

<a id="rst-message-interface"></a>

## Message Interface

The dm-raid target will accept certain actions through the 'message' interface. ('man dmsetup' for more information on the message interface.)  These actions include:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> "idle"
>
> </td>
> <td>
>
>
> Halt the current sync action.
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> "frozen"
>
> </td>
> <td>
>
>
> Freeze the current sync action.
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> "resync"
>
> </td>
> <td>
>
>
> Initiate/continue a resync.
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> "recover"
>
> </td>
> <td>
>
>
> Initiate/continue a recover process.
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> "check"
>
> </td>
> <td>
>
>
> Initiate a check (i.e. a "scrub") of the array.
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> "repair"
>
> </td>
> <td>
>
>
> Initiate a repair of the array.
>
> </td>
> </tr>
> </tbody>
> </table>

<a id="rst-discard-support"></a>

## Discard Support

The implementation of discard support among hardware vendors varies. When a block is discarded, some storage devices will return zeroes when the block is read.  These devices set the 'discard_zeroes_data' attribute.  Other devices will return random data.  Confusingly, some devices that advertise 'discard_zeroes_data' will not reliably return zeroes when discarded blocks are read\!  Since RAID 4/5/6 uses blocks from a number of devices to calculate parity blocks and (for performance reasons) relies on 'discard_zeroes_data' being reliable, it is important that the devices be consistent.  Blocks may be discarded in the middle of a RAID 4/5/6 stripe and if subsequent read results are not consistent, the parity blocks may be calculated differently at any time; making the parity blocks useless for redundancy.  It is important to understand how your hardware behaves with discards if you are going to enable discards with RAID 4/5/6.

Since the behavior of storage devices is unreliable in this respect, even when reporting 'discard_zeroes_data', by default RAID 4/5/6 discard support is disabled -- this ensures data integrity at the expense of losing some performance.

Storage devices that properly support 'discard_zeroes_data' are increasingly whitelisted in the kernel and can thus be trusted.

For trusted devices, the following dm-raid module parameter can be set to safely enable discard support for RAID 4/5/6:

> 'devices_handle_discards_safely'

<a id="rst-takeover-reshape-support"></a>

## Takeover/Reshape Support

The target natively supports these two types of MDRAID conversions:

o Takeover: Converts an array from one RAID level to another

o Reshape: Changes the internal layout while maintaining the current RAID level

Each operation is only valid under specific constraints imposed by the existing array's layout and configuration.

Takeover: linear -&gt; raid1 with N &gt;= 2 mirrors raid0 -&gt; raid4 (add dedicated parity device) raid0 -&gt; raid5 (add dedicated parity device) raid0 -&gt; raid10 with near layout and N &gt;= 2 mirror groups (raid0 stripes have to become first member within mirror groups) raid1 -&gt; linear raid1 -&gt; raid5 with 2 mirrors raid4 -&gt; raid5 w/ rotating parity raid5 with dedicated parity device -&gt; raid4 raid5 -&gt; raid6 (with dedicated Q-syndrome) raid6 (with dedicated Q-syndrome) -&gt; raid5 raid10 with near layout and even number of disks -&gt; raid0 (select any in-sync device from each mirror group)

Reshape: linear: not possible raid0:  not possible raid1:  change number of mirrors raid4:  add and remove stripes (minimum 3), change stripesize raid5:  add and remove stripes (minimum 3, special case 2 for raid1 takeover), change rotating parity algorithms, change stripesize raid6:  add and remove stripes (minimum 4), change rotating syndrome algorithms, change stripesize raid10 near:   add stripes (minimum 4), change stripesize, no stripe removal possible, change to offset layout raid10 offset: add stripes, change stripesize, no stripe removal possible, change to near layout raid10 far:    not possible

Table line examples:

\#\#\# raid1 -&gt; raid5 \# \# 2 devices limitation in raid1. \# raid5 personality is able to just map 2 like raid1. \# Reshape after takeover to change to full raid5 layout

> 0 1960886272 raid raid1 3 0 region_size 2048 2 /dev/dm-0 /dev/dm-1 /dev/dm-2 /dev/dm-3

\# dm-0 and dm-2 are e.g. 4MiB large metadata devices, dm-1 and dm-3 have to be at least 1960886272 big. \# \# Table line to takeover to raid5

> 0 1960886272 raid raid5 3 0 region_size 2048 2 /dev/dm-0 /dev/dm-1 /dev/dm-2 /dev/dm-3

\# Add required out-of-place reshape space to the beginniong of the given 2 data devices, \# allocate another metadata/data device tuple with the same sizes for the parity space \# and zero the first 4K of the metadata device. \# \# Example table of the out-of-place reshape space addition for one data device, e.g. dm-1

> 0 8192 linear 8:0 0 1960903888 \#  &lt;- must be free space segment 8192 1960886272 linear 8:0 0 2048 \# previous data segment

\# Mapping table for e.g. raid5_rs reshape causing the size of the raid device to double-fold once the reshape finishes. \# Check the status output (e.g. "dmsetup status $RaidDev") for progress.

> 0 $((2 \* 1960886272)) raid raid5 7 0 region_size 2048 data_offset 8192 delta_disk 1 2 /dev/dm-0 /dev/dm-1 /dev/dm-2 /dev/dm-3

<a id="rst-version-history"></a>

## Version History



```text
1.0.0  Initial version.  Support for RAID 4/5/6
1.1.0  Added support for RAID 1
1.2.0  Handle creation of arrays that contain failed devices.
1.3.0  Added support for RAID 10
1.3.1  Allow device replacement/rebuild for RAID 10
1.3.2  Fix/improve redundancy checking for RAID10
1.4.0  Non-functional change.  Removes arg from mapping function.
1.4.1  RAID10 fix redundancy validation checks (commit 55ebbb5).
1.4.2  Add RAID10 "far" and "offset" algorithm support.
1.5.0  Add message interface to allow manipulation of the sync_action.
       New status (STATUSTYPE_INFO) fields: sync_action and mismatch_cnt.
1.5.1  Add ability to restore transiently failed devices on resume.
1.5.2  'mismatch_cnt' is zero unless [last_]sync_action is "check".
1.6.0  Add discard support (and devices_handle_discard_safely module param).
1.7.0  Add support for MD RAID0 mappings.
1.8.0  Explicitly check for compatible flags in the superblock metadata
       and reject to start the raid set if any are set by a newer
       target version, thus avoiding data corruption on a raid set
       with a reshape in progress.
1.9.0  Add support for RAID level takeover/reshape/region size
       and set size reduction.
1.9.1  Fix activation of existing RAID 4/10 mapped devices
1.9.2  Don't emit '- -' on the status table line in case the constructor
       fails reading a superblock. Correctly emit 'maj:min1 maj:min2' and
       'D' on the status line.  If '- -' is passed into the constructor, emit
       '- -' on the table line and '-' as the status line health character.
1.10.0 Add support for raid4/5/6 journal device
1.10.1 Fix data corruption on reshape request
1.11.0 Fix table line argument order
       (wrong raid10_copies/raid10_format sequence)
1.11.1 Add raid4/5/6 journal write-back support via journal_mode option
1.12.1 Fix for MD deadlock between mddev_suspend() and md_write_start() available
1.13.0 Fix dev_health status at end of "recover" (was 'a', now 'A')
1.13.1 Fix deadlock caused by early md_stop_writes().  Also fix size an
       state races.
1.13.2 Fix raid redundancy validation and avoid keeping raid set frozen
1.14.0 Fix reshape race on small devices.  Fix stripe adding reshape
       deadlock/potential data corruption.  Update superblock when
       specific devices are requested via rebuild.  Fix RAID leg
       rebuild errors.
1.15.0 Fix size extensions not being synchronized in case of new MD bitmap
       pages allocated;  also fix those not occurring after previous reductions
1.15.1 Fix argument count and arguments for rebuild/write_mostly/journal_(dev|mode)
       on the status line.
```
