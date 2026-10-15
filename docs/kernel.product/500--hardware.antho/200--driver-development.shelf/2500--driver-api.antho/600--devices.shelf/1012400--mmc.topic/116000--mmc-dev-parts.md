---
title: "SD and MMC Device Partitions"
type: reference
description: "Device partitions are additional logical block devices present on the SD/MMC device."
---

<a id="rst-sd-and-mmc-device-partitions"></a>

Device partitions are additional logical block devices present on the SD/MMC device.

As of this writing, MMC boot partitions as supported and exposed as /dev/mmcblkXboot0 and /dev/mmcblkXboot1, where X is the index of the parent /dev/mmcblkX.

<a id="rst-mmc-boot-partitions"></a>

## MMC Boot Partitions

Read and write access is provided to the two MMC boot partitions. Due to the sensitive nature of the boot partition contents, which often store a bootloader or bootloader configuration tables crucial to booting the platform, write access is disabled by default to reduce the chance of accidental bricking.

To enable write access to /dev/mmcblkXbootY, disable the forced read-only access with:



```text
echo 0 > /sys/block/mmcblkXbootY/force_ro
```

To re-enable read-only access:



```text
echo 1 > /sys/block/mmcblkXbootY/force_ro
```

The boot partitions can also be locked read only until the next power on, with:



```text
echo 1 > /sys/block/mmcblkXbootY/ro_lock_until_next_power_on
```

This is a feature of the card and not of the kernel. If the card does not support boot partition locking, the file will not exist. If the feature has been disabled on the card, the file will be read-only.

The boot partitions can also be locked permanently, but this feature is not accessible through sysfs in order to avoid accidental or malicious bricking.
