---
title: "dm-linear"
type: reference
description: "Device-Mapper's \"linear\" target maps a linear range of the Device-Mapper device onto a linear range of another device. This is the basic building block of logical volume managers."
---

<a id="rst-dm-linear"></a>

Device-Mapper's "linear" target maps a linear range of the Device-Mapper device onto a linear range of another device.  This is the basic building block of logical volume managers.

- **Parameters: &lt;dev path&gt; &lt;offset&gt;**

  - **&lt;dev path&gt;:**

    Full pathname to the underlying block-device, or a "major:minor" device-number.

  - **&lt;offset&gt;:**

    Starting sector within the device.

<a id="rst-example-scripts"></a>

## Example scripts



```text
#!/bin/sh
# Create an identity mapping for a device
echo "0 `blockdev --getsz $1` linear $1 0" | dmsetup create identity
```



```text
#!/bin/sh
# Join 2 devices together
size1=`blockdev --getsz $1`
size2=`blockdev --getsz $2`
echo "0 $size1 linear $1 0
$size1 $size2 linear $2 0" | dmsetup create joined
```



```text
#!/usr/bin/perl -w
# Split a device into 4M chunks and then join them together in reverse order.

my $name = "reverse";
my $extent_size = 4 * 1024 * 2;
my $dev = $ARGV[0];
my $table = "";
my $count = 0;

if (!defined($dev)) {
        die("Please specify a device.\n");
}

my $dev_size = `blockdev --getsz $dev`;
my $extents = int($dev_size / $extent_size) -
              (($dev_size % $extent_size) ? 1 : 0);

while ($extents > 0) {
        my $this_start = $count * $extent_size;
        $extents--;
        $count++;
        my $this_offset = $extents * $extent_size;

        $table .= "$this_start $extent_size linear $dev $this_offset\n";
}

`echo \"$table\" | dmsetup create $name`;
```
