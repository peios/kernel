---
title: "Numa policy hit/miss statistics"
type: reference
description: "/sys/devices/system/node/node*/numastat"
---

<a id="rst-numa-policy-hit-miss-statistics"></a>

/sys/devices/system/node/node\*/numastat

All units are pages. Hugepages have separate counters.

The numa_hit, numa_miss and numa_foreign counters reflect how well processes are able to allocate memory from nodes they prefer. If they succeed, numa_hit is incremented on the preferred node, otherwise numa_foreign is incremented on the preferred node and numa_miss on the node where allocation succeeded.

Usually preferred node is the one local to the CPU where the process executes, but restrictions such as mempolicies can change that, so there are also two counters based on CPU local node. local_node is similar to numa_hit and is incremented on allocation from a node by CPU on the same node. other_node is similar to numa_miss and is incremented on the node where allocation succeeds from a CPU from a different node. Note there is no counter analogical to numa_foreign.

In more detail:


<table>
<tbody>
<tr>
<td>


numa_hit

</td>
<td>


A process wanted to allocate memory from this node, and succeeded.

</td>
</tr>
<tr>
<td>


numa_miss

</td>
<td>


A process wanted to allocate memory from another node, but ended up with memory from this node.

</td>
</tr>
<tr>
<td>


numa_foreign

</td>
<td>


A process wanted to allocate on this node, but ended up with memory from another node.

</td>
</tr>
<tr>
<td>


local_node

</td>
<td>


A process ran on this node's CPU, and got memory from this node.

</td>
</tr>
<tr>
<td>


other_node

</td>
<td>


A process ran on a different node's CPU and got memory from this node.

</td>
</tr>
<tr>
<td>


interleave_hit

</td>
<td>


Interleaving wanted to allocate from this node and succeeded.

</td>
</tr>
</tbody>
</table>

For easier reading you can use the numastat utility from the numactl package ([http://oss.sgi.com/projects/libnuma/](<http://oss.sgi.com/projects/libnuma/>)). Note that it only works well right now on machines with a small number of CPUs.

Note that on systems with memoryless nodes (where a node has CPUs but no memory) the numa_hit, numa_miss and numa_foreign statistics can be skewed heavily. In the current kernel implementation, if a process prefers a memoryless node (i.e.  because it is running on one of its local CPU), the implementation actually treats one of the nearest nodes with memory as the preferred node. As a result, such allocation will not increase the numa_foreign counter on the memoryless node, and will skew the numa_hit, numa_miss and numa_foreign statistics of the nearest node.
