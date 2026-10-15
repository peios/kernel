---
title: "Devlink Params"
type: reference
description: "devlink provides capability for a driver to expose device parameters for low level device functionality. Since devlink can operate at the device-wide level, it can be used to provide configuration that may affect multiple ports on a single…"
---

<a id="rst-devlink-params"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

`devlink` provides capability for a driver to expose device parameters for low level device functionality. Since devlink can operate at the device-wide level, it can be used to provide configuration that may affect multiple ports on a single device.

This document describes a number of generic parameters that are supported across multiple drivers. Each driver is also free to add their own parameters. Each driver must document the specific parameters they support, whether generic or not.

<a id="rst-configuration-modes"></a>

## Configuration modes

Parameters may be set in different configuration modes.


<table>
<caption>Possible configuration modes</caption>
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


`runtime`

</td>
<td>


set while the driver is running, and takes effect immediately. No reset is required.

</td>
</tr>
<tr>
<td>


`driverinit`

</td>
<td>


applied while the driver initializes. Requires the user to restart the driver using the `devlink` reload command.

</td>
</tr>
<tr>
<td>


`permanent`

</td>
<td>


written to the device's non-volatile memory. A hard reset is required for it to take effect.

</td>
</tr>
</tbody>
</table>

<a id="rst-reloading"></a>

### Reloading

In order for `driverinit` parameters to take effect, the driver must support reloading via the `devlink-reload` command. This command will request a reload of the device driver.

<a id="rst-default-parameter-values"></a>

## Default parameter values

Drivers may optionally export default values for parameters of cmode `runtime` and `permanent`. For `driverinit` parameters, the last value set by the driver will be used as the default value. Drivers can also support resetting params with cmode `runtime` and `permanent` to their default values. Resetting `driverinit` params is supported by devlink core without additional driver support needed.

<a id="rst-generic-configuration-parameters"></a>
<a id="rst-devlink-params-generic"></a>

## Generic configuration parameters

The following is a list of generic configuration parameters that drivers may add. Use of generic parameters is preferred over each driver creating their own name.


<table>
<caption>List of generic parameters</caption>
<tbody>
<tr>
<td>


Name

</td>
<td>


Type

</td>
<td>


Description

</td>
</tr>
<tr>
<td>


`enable_sriov`

</td>
<td>


Boolean

</td>
<td>


Enable Single Root I/O Virtualization (SRIOV) in the device.

</td>
</tr>
<tr>
<td>


`ignore_ari`

</td>
<td>


Boolean

</td>
<td>


Ignore Alternative Routing-ID Interpretation (ARI) capability. If enabled, the adapter will ignore ARI capability even when the platform has support enabled. The device will create the same number of partitions as when the platform does not support ARI.

</td>
</tr>
<tr>
<td>


`msix_vec_per_pf_max`

</td>
<td>


u32

</td>
<td>


Provides the maximum number of MSI-X interrupts that a device can create. Value is the same across all physical functions (PFs) in the device.

</td>
</tr>
<tr>
<td>


`msix_vec_per_pf_min`

</td>
<td>


u32

</td>
<td>


Provides the minimum number of MSI-X interrupts required for the device to initialize. Value is the same across all physical functions (PFs) in the device.

</td>
</tr>
<tr>
<td>


`fw_load_policy`

</td>
<td>


u8

</td>
<td>


- **Control the device's firmware loading policy.**

  - `DEVLINK_PARAM_FW_LOAD_POLICY_VALUE_DRIVER` (0) Load firmware version preferred by the driver.

  - `DEVLINK_PARAM_FW_LOAD_POLICY_VALUE_FLASH` (1) Load firmware currently stored in flash.

  - `DEVLINK_PARAM_FW_LOAD_POLICY_VALUE_DISK` (2) Load firmware currently available on host's disk.

</td>
</tr>
<tr>
<td>


`reset_dev_on_drv_probe`

</td>
<td>


u8

</td>
<td>


- **Controls the device's reset policy on driver probe.**

  - `DEVLINK_PARAM_RESET_DEV_ON_DRV_PROBE_VALUE_UNKNOWN` (0) Unknown or invalid value.

  - `DEVLINK_PARAM_RESET_DEV_ON_DRV_PROBE_VALUE_ALWAYS` (1) Always reset device on driver probe.

  - `DEVLINK_PARAM_RESET_DEV_ON_DRV_PROBE_VALUE_NEVER` (2) Never reset device on driver probe.

  - `DEVLINK_PARAM_RESET_DEV_ON_DRV_PROBE_VALUE_DISK` (3) Reset the device only if firmware can be found in the filesystem.

</td>
</tr>
<tr>
<td>


`enable_roce`

</td>
<td>


Boolean

</td>
<td>


Enable handling of RoCE traffic in the device.

</td>
</tr>
<tr>
<td>


`enable_eth`

</td>
<td>


Boolean

</td>
<td>


When enabled, the device driver will instantiate Ethernet specific auxiliary device of the devlink device.

</td>
</tr>
<tr>
<td>


`enable_rdma`

</td>
<td>


Boolean

</td>
<td>


When enabled, the device driver will instantiate RDMA specific auxiliary device of the devlink device.

</td>
</tr>
<tr>
<td>


`enable_vnet`

</td>
<td>


Boolean

</td>
<td>


When enabled, the device driver will instantiate VDPA networking specific auxiliary device of the devlink device.

</td>
</tr>
<tr>
<td>


`enable_iwarp`

</td>
<td>


Boolean

</td>
<td>


Enable handling of iWARP traffic in the device.

</td>
</tr>
<tr>
<td>


`internal_err_reset`

</td>
<td>


Boolean

</td>
<td>


When enabled, the device driver will reset the device on internal errors.

</td>
</tr>
<tr>
<td>


`max_macs`

</td>
<td>


u32

</td>
<td>


Typically macvlan, vlan net devices mac are also programmed in their parent netdevice's Function rx filter. This parameter limit the maximum number of unicast mac address filters to receive traffic from per ethernet port of this device.

</td>
</tr>
<tr>
<td>


`region_snapshot_enable`

</td>
<td>


Boolean

</td>
<td>


Enable capture of `devlink-region` snapshots.

</td>
</tr>
<tr>
<td>


`enable_remote_dev_reset`

</td>
<td>


Boolean

</td>
<td>


Enable device reset by remote host. When cleared, the device driver will NACK any attempt of other host to reset the device. This parameter is useful for setups where a device is shared by different hosts, such as multi-host setup.

</td>
</tr>
<tr>
<td>


`io_eq_size`

</td>
<td>


u32

</td>
<td>


Control the size of I/O completion EQs.

</td>
</tr>
<tr>
<td>


`event_eq_size`

</td>
<td>


u32

</td>
<td>


Control the size of asynchronous control events EQ.

</td>
</tr>
<tr>
<td>


`enable_phc`

</td>
<td>


Boolean

</td>
<td>


Enable PHC (PTP Hardware Clock) functionality in the device.

</td>
</tr>
<tr>
<td>


`clock_id`

</td>
<td>


u64

</td>
<td>


Clock ID used by the device for registering DPLL devices and pins.

</td>
</tr>
<tr>
<td>


`total_vfs`

</td>
<td>


u32

</td>
<td>


The max number of Virtual Functions (VFs) exposed by the PF. after reboot/pci reset, 'sriov_totalvfs' entry under the device's sysfs directory will report this value.

</td>
</tr>
<tr>
<td>


`num_doorbells`

</td>
<td>


u32

</td>
<td>


Controls the number of doorbells used by the device.

</td>
</tr>
<tr>
<td>


`max_mac_per_vf`

</td>
<td>


u32

</td>
<td>


Controls the maximum number of MAC address filters that can be assigned to a Virtual Function (VF).

</td>
</tr>
</tbody>
</table>
