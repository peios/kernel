---
title: "dm-service-time"
type: reference
description: "dm-service-time is a path selector module for device-mapper targets, which selects a path with the shortest estimated service time for the incoming I/O."
---

<a id="rst-dm-service-time"></a>

dm-service-time is a path selector module for device-mapper targets, which selects a path with the shortest estimated service time for the incoming I/O.

The service time for each path is estimated by dividing the total size of in-flight I/Os on a path with the performance value of the path. The performance value is a relative throughput value among all paths in a path-group, and it can be specified as a table argument.

The path selector name is 'service-time'.

Table parameters for each path:

> - **\[&lt;repeat_count&gt; \[&lt;relative_throughput&gt;\]\]**
>
>   - **&lt;repeat_count&gt;:**
>
>     The number of I/Os to dispatch using the selected path before switching to the next path. If not given, internal default is used.  To check the default value, see the activated table.
>
>   - **&lt;relative_throughput&gt;:**
>
>     The relative throughput value of the path among all paths in the path-group. The valid range is 0-100. If not given, minimum value '1' is used. If '0' is given, the path isn't selected while other paths having a positive value are available.

Status for each path:

> - **&lt;status&gt; &lt;fail-count&gt; &lt;in-flight-size&gt; &lt;relative_throughput&gt;**
>
>   - **&lt;status&gt;:**
>
>     'A' if the path is active, 'F' if the path is failed.
>
>   - **&lt;fail-count&gt;:**
>
>     The number of path failures.
>
>   - **&lt;in-flight-size&gt;:**
>
>     The size of in-flight I/Os on the path.
>
>   - **&lt;relative_throughput&gt;:**
>
>     The relative throughput value of the path among all paths in the path-group.

<a id="rst-algorithm"></a>

## Algorithm

dm-service-time adds the I/O size to 'in-flight-size' when the I/O is dispatched and subtracts when completed. Basically, dm-service-time selects a path having minimum service time which is calculated by:



```text
('in-flight-size' + 'size-of-incoming-io') / 'relative_throughput'
```

However, some optimizations below are used to reduce the calculation as much as possible.

> 1. If the paths have the same 'relative_throughput', skip the division and just compare the 'in-flight-size'.
>
> 2. If the paths have the same 'in-flight-size', skip the division and just compare the 'relative_throughput'.
>
> 3. If some paths have non-zero 'relative_throughput' and others have zero 'relative_throughput', ignore those paths with zero 'relative_throughput'.

If such optimizations can't be applied, calculate service time, and compare service time. If calculated service time is equal, the path having maximum 'relative_throughput' may be better.  So compare 'relative_throughput' then.

<a id="rst-examples"></a>

## Examples

In case that 2 paths (sda and sdb) are used with repeat_count == 128 and sda has an average throughput 1GB/s and sdb has 4GB/s, 'relative_throughput' value may be '1' for sda and '4' for sdb:



```text
# echo "0 10 multipath 0 0 1 1 service-time 0 2 2 8:0 128 1 8:16 128 4" \
  dmsetup create test
#
# dmsetup table
test: 0 10 multipath 0 0 1 1 service-time 0 2 2 8:0 128 1 8:16 128 4
#
# dmsetup status
test: 0 10 multipath 2 0 0 0 1 1 E 0 2 2 8:0 A 0 0 1 8:16 A 0 0 4
```

Or '2' for sda and '8' for sdb would be also true:



```text
# echo "0 10 multipath 0 0 1 1 service-time 0 2 2 8:0 128 2 8:16 128 8" \
  dmsetup create test
#
# dmsetup table
test: 0 10 multipath 0 0 1 1 service-time 0 2 2 8:0 128 2 8:16 128 8
#
# dmsetup status
test: 0 10 multipath 2 0 0 0 1 1 E 0 2 2 8:0 A 0 0 2 8:16 A 0 0 8
```
