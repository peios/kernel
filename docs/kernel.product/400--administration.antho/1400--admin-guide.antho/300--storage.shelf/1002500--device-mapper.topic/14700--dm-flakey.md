---
title: "dm-flakey"
type: reference
description: "This target is the same as the linear target except that it exhibits unreliable behaviour periodically. It's been found useful in simulating failing devices for testing purposes."
---

<a id="rst-dm-flakey"></a>

This target is the same as the linear target except that it exhibits unreliable behaviour periodically.  It's been found useful in simulating failing devices for testing purposes.

Starting from the time the table is loaded, the device is available for &lt;up interval&gt; seconds, then exhibits unreliable behaviour for &lt;down interval&gt; seconds, and then this cycle repeats.

Also, consider using this in combination with the dm-delay target too, which can delay reads and writes and/or send them to different underlying devices.

<a id="rst-table-parameters"></a>

## Table parameters



```text
<dev path> <offset> <up interval> <down interval> \
  [<num_features> [<feature arguments>]]
```

Mandatory parameters:

> - **&lt;dev path&gt;:**
>
>   Full pathname to the underlying block-device, or a "major:minor" device-number.
>
> - **&lt;offset&gt;:**
>
>   Starting sector within the device.
>
> - **&lt;up interval&gt;:**
>
>   Number of seconds device is available.
>
> - **&lt;down interval&gt;:**
>
>   Number of seconds device returns errors.

Optional feature parameters:

> If no feature parameters are present, during the periods of unreliability, all I/O returns errors.
>
> - **error_reads:**
>
>   All read I/O is failed with an error signalled. Write I/O is handled correctly.
>
> - **drop_writes:**
>
>   All write I/O is silently ignored. Read I/O is handled correctly.
>
> - **error_writes:**
>
>   All write I/O is failed with an error signalled. Read I/O is handled correctly.
>
> - **corrupt_bio_byte &lt;Nth_byte&gt; &lt;direction&gt; &lt;value&gt; &lt;flags&gt;:**
>
>   > During &lt;down interval&gt;, replace &lt;Nth_byte&gt; of the data of each matching bio with &lt;value&gt;.
>
>   - **&lt;Nth_byte&gt;:**
>
>     The offset of the byte to replace. Counting starts at 1, to replace the first byte.
>
>   - **&lt;direction&gt;:**
>
>     Either 'r' to corrupt reads or 'w' to corrupt writes. 'w' is incompatible with drop_writes.
>
>   - **&lt;value&gt;:**
>
>     The value (from 0-255) to write.
>
>   - **&lt;flags&gt;:**
>
>     Perform the replacement only if bio-&gt;bi_opf has all the selected flags set.
>
> - **random_read_corrupt &lt;probability&gt;**
>
>   During &lt;down interval&gt;, replace random byte in a read bio with a random value. probability is an integer between 0 and 1000000000 meaning 0% to 100% probability of corruption.
>
> - **random_write_corrupt &lt;probability&gt;**
>
>   During &lt;down interval&gt;, replace random byte in a write bio with a random value. probability is an integer between 0 and 1000000000 meaning 0% to 100% probability of corruption.

Examples:

Replaces the 32nd byte of READ bios with the value 1:



```text
corrupt_bio_byte 32 r 1 0
```

Replaces the 224th byte of REQ_META (=32) bios with the value 0:



```text
corrupt_bio_byte 224 w 0 32
```
