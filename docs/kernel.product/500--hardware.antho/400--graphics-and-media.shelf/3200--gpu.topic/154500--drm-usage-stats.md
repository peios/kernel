---
title: "DRM client usage stats"
type: reference
description: "DRM drivers can choose to export partly standardised text output via the fops->show_fdinfo() as part of the driver specific file operations registered in the struct drm_driver object registered with the DRM core."
---

<a id="rst-drm-client-usage-stats-1"></a>
<a id="rst-drm-client-usage-stats"></a>

DRM drivers can choose to export partly standardised text output via the `fops->show_fdinfo()` as part of the driver specific file operations registered in the `struct drm_driver` object registered with the DRM core.

One purpose of this output is to enable writing as generic as practically feasible `top(1)` like userspace monitoring tools.

Given the differences between various DRM drivers the specification of the output is split between common and driver specific parts. Having said that, wherever possible effort should still be made to standardise as much as possible.

<a id="rst-file-format-specification"></a>

## File format specification

- File shall contain one key value pair per one line of text.

- Colon character (`:`) must be used to delimit keys and values.

- All standardised keys shall be prefixed with `drm-`.

- Driver-specific keys shall be prefixed with `driver_name-`, where driver_name should ideally be the same as the `name` field in `struct drm_driver`, although this is not mandatory.

- Whitespace between the delimiter and first non-whitespace character shall be ignored when parsing.

- Keys are not allowed to contain whitespace characters.

- Numerical key value pairs can end with optional unit string.

- Data type of the value is fixed as defined in the specification.

<a id="rst-key-types"></a>

### Key types

1. Mandatory, fully standardised.

2. Optional, fully standardised.

3. Driver specific.

<a id="rst-data-types"></a>

### Data types

- &lt;uint&gt; - Unsigned integer without defining the maximum value.

- &lt;keystr&gt; - String excluding any above defined reserved characters or whitespace.

- &lt;valstr&gt; - String.

<a id="rst-mandatory-fully-standardised-keys"></a>

### Mandatory fully standardised keys

- drm-driver: &lt;valstr&gt;

String shall contain the name this driver registered as via the respective `struct drm_driver` data structure.

<a id="rst-optional-fully-standardised-keys"></a>

### Optional fully standardised keys

<a id="rst-identification"></a>

#### Identification

- drm-pdev: &lt;aaaa:bb.cc.d&gt;

For PCI devices this should contain the PCI slot address of the device in question.

- drm-client-id: &lt;uint&gt;

Unique value relating to the open DRM file descriptor used to distinguish duplicated and shared file descriptors. Conceptually the value should map 1:1 to the in kernel representation of `struct drm_file` instances.

Uniqueness of the value shall be either globally unique, or unique within the scope of each device, in which case `drm-pdev` shall be present as well.

Userspace should make sure to not double account any usage statistics by using the above described criteria in order to associate data to individual clients.

- drm-client-name: &lt;valstr&gt;

String optionally set by userspace using DRM_IOCTL_SET_CLIENT_NAME.

<a id="rst-utilization"></a>

#### Utilization

- drm-engine-&lt;keystr&gt;: &lt;uint&gt; ns

GPUs usually contain multiple execution engines. Each shall be given a stable and unique name (keystr), with possible values documented in the driver specific documentation.

Value shall be in specified time units which the respective GPU engine spent busy executing workloads belonging to this client.

Values are not required to be constantly monotonic if it makes the driver implementation easier, but are required to catch up with the previously reported larger value within a reasonable period. Upon observing a value lower than what was previously read, userspace is expected to stay with that larger previous value until a monotonic update is seen.

- drm-engine-capacity-&lt;keystr&gt;: &lt;uint&gt;

Engine identifier string must be the same as the one specified in the drm-engine-&lt;keystr&gt; tag and shall contain a greater than zero number in case the exported engine corresponds to a group of identical hardware engines.

In the absence of this tag parser shall assume capacity of one. Zero capacity is not allowed.

- drm-cycles-&lt;keystr&gt;: &lt;uint&gt;

Engine identifier string must be the same as the one specified in the drm-engine-&lt;keystr&gt; tag and shall contain the number of busy cycles for the given engine.

Values are not required to be constantly monotonic if it makes the driver implementation easier, but are required to catch up with the previously reported larger value within a reasonable period. Upon observing a value lower than what was previously read, userspace is expected to stay with that larger previous value until a monotonic update is seen.

- drm-total-cycles-&lt;keystr&gt;: &lt;uint&gt;

Engine identifier string must be the same as the one specified in the drm-cycles-&lt;keystr&gt; tag and shall contain the total number cycles for the given engine.

This is a timestamp in GPU unspecified unit that matches the update rate of drm-cycles-&lt;keystr&gt;. For drivers that implement this interface, the engine utilization can be calculated entirely on the GPU clock domain, without considering the CPU sleep time between 2 samples.

A driver may implement either this key or drm-maxfreq-&lt;keystr&gt;, but not both.

- drm-maxfreq-&lt;keystr&gt;: &lt;uint&gt; \[Hz\|MHz\|KHz\]

Engine identifier string must be the same as the one specified in the drm-engine-&lt;keystr&gt; tag and shall contain the maximum frequency for the given engine.  Taken together with drm-cycles-&lt;keystr&gt;, this can be used to calculate percentage utilization of the engine, whereas drm-engine-&lt;keystr&gt; only reflects time active without considering what frequency the engine is operating as a percentage of its maximum frequency.

A driver may implement either this key or drm-total-cycles-&lt;keystr&gt;, but not both.

<a id="rst-memory"></a>

#### Memory

Each possible memory type which can be used to store buffer objects by the GPU in question shall be given a stable and unique name to be used as the "&lt;region&gt;" string.

The region name "memory" is reserved to refer to normal system memory.

The value shall reflect the amount of storage currently consumed by the buffer objects belong to this client, in the respective memory region.

Default unit shall be bytes with optional unit specifiers of 'KiB' or 'MiB' indicating kibi- or mebi-bytes.

- drm-total-&lt;region&gt;: &lt;uint&gt; \[KiB\|MiB\]

The total size of all requested buffers, including both shared and private memory. The backing store for the buffers does not need to be currently instantiated to count under this category. To avoid double-counting, if a buffer has multiple regions where it can be allocated to, the implementation should consistently select a single region for accounting purposes.

- drm-shared-&lt;region&gt;: &lt;uint&gt; \[KiB\|MiB\]

The total size of buffers that are shared with another file (i.e., have more than one handle). The same requirement to avoid double-counting that applies to drm-total-&lt;region&gt; also applies here.

- drm-resident-&lt;region&gt;: &lt;uint&gt; \[KiB\|MiB\]

The total size of buffers that are resident (i.e., have their backing store present or instantiated) in the specified region.

- drm-memory-&lt;region&gt;: &lt;uint&gt; \[KiB\|MiB\]

This key is deprecated and is only printed by amdgpu; it is an alias for drm-resident-&lt;region&gt;.

- drm-purgeable-&lt;region&gt;: &lt;uint&gt; \[KiB\|MiB\]

The total size of buffers that are resident and purgeable.

For example, drivers that implement functionality similar to 'madvise' can count buffers that have instantiated backing stores but have been marked with an equivalent of MADV_DONTNEED.

- drm-active-&lt;region&gt;: &lt;uint&gt; \[KiB\|MiB\]

The total size of buffers that are active on one or more engines.

One practical example of this could be the presence of unsignaled fences in a GEM buffer reservation object. Therefore, the active category is a subset of the resident category.

<a id="rst-implementation-details"></a>

## Implementation Details

Drivers should use drm_show_fdinfo() in their `struct file_operations`, and implement &amp;drm_driver.show_fdinfo if they wish to provide any stats which are not provided by drm_show_fdinfo().  But even driver specific stats should be documented above and where possible, aligned with other drivers.

<a id="rst-driver-specific-implementations"></a>

### Driver specific implementations

- [i915 DRM client usage stats implementation](<~kernel/hardware/gpu/i915#rst-i915-usage-stats>)

- [panfrost-usage-stats](<~kernel/hardware/gpu/panfrost#rst-panfrost-usage-stats>)

- [panthor-usage-stats](<~kernel/hardware/gpu/panthor#rst-panthor-usage-stats>)

- [Xe DRM client usage stats implementation](<~kernel/hardware/gpu/xe/xe-drm-usage-stats#rst-xe-usage-stats>)
