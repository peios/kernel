---
title: "Writing camera sensor drivers"
type: reference
description: "This document covers the in-kernel APIs only. For the best practices on userspace API implementation in camera sensor drivers, please see media_using_camera_sensor_drivers."
---

<a id="rst-writing-camera-sensor-drivers"></a>
<a id="rst-media-writing-camera-sensor-drivers"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

This document covers the in-kernel APIs only. For the best practices on userspace API implementation in camera sensor drivers, please see [Using camera sensor drivers](<~kernel/userspace/userspace-api/media-drivers/camera-sensor#rst-media-using-camera-sensor-drivers>).

<a id="rst-csi-2-parallel-and-bt-656-buses"></a>

## CSI-2, parallel and BT.656 buses

Please see [Pixel data transmitter and receiver drivers](<~kernel/hardware/driver-api/media/tx-rx#rst-transmitter-receiver>).

<a id="rst-handling-clocks"></a>

## Handling clocks

Camera sensors have an internal clock tree including a PLL and a number of divisors. The clock tree is generally configured by the driver based on a few input parameters that are specific to the hardware: the external clock frequency and the link frequency. The two parameters generally are obtained from system firmware. **No other frequencies should be used in any circumstances.**

The reason why the clock frequencies are so important is that the clock signals come out of the SoC, and in many cases a specific frequency is designed to be used in the system. Using another frequency may cause harmful effects elsewhere. Therefore only the pre-determined frequencies are configurable by the user.

The external clock frequency shall be retrieved by obtaining the external clock using the `devm_v4l2_sensor_clk_get()` helper function, and then getting its frequency with `clk_get_rate()`. Usage of the helper function guarantees correct behaviour regardless of whether the sensor is integrated in a DT-based or ACPI-based system.

<a id="rst-acpi"></a>

### ACPI

ACPI-based systems typically don't register the sensor external clock with the kernel, but specify the external clock frequency in the `clock-frequency` \_DSD property. The `devm_v4l2_sensor_clk_get()` helper creates and returns a fixed clock set at that rate.

<a id="rst-devicetree"></a>

### Devicetree

Devicetree-based systems declare the sensor external clock in the device tree and reference it from the sensor node. The preferred way to select the external clock frequency is to use the `assigned-clocks`, `assigned-clock-parents` and `assigned-clock-rates` properties in the sensor node to set the clock rate. See the [clock device tree bindings](<https://github.com/devicetree-org/dt-schema/blob/main/dtschema/schemas/clock/clock.yaml>)<a id="rst-clock-device-tree-bindings"></a> for more information. The `devm_v4l2_sensor_clk_get()` helper retrieves and returns that clock.

This approach has the drawback that there's no guarantee that the frequency hasn't been modified directly or indirectly by another driver, or supported by the board's clock tree to begin with. Changes to the Common Clock Framework API are required to ensure reliability.

<a id="rst-power-management"></a>

## Power management

Camera sensors are used in conjunction with other devices to form a camera pipeline. They must obey the rules listed herein to ensure coherent power management over the pipeline.

Camera sensor drivers are responsible for controlling the power state of the device they otherwise control as well. They shall use runtime PM to manage power states. Runtime PM shall be enabled at probe time and disabled at remove time. Drivers should enable runtime PM autosuspend. Also see [async sub-device registration](<~kernel/hardware/driver-api/media/v4l2-subdev#rst-media-registering-async-subdevs>).

The runtime PM handlers shall handle clocks, regulators, GPIOs, and other system resources required to power the sensor up and down. For drivers that don't use any of those resources (such as drivers that support ACPI systems only), the runtime PM handlers may be left unimplemented.

In general, the device shall be powered on at least when its registers are being accessed and when it is streaming. Drivers should use `pm_runtime_resume_and_get()` when starting streaming and `pm_runtime_put()` or `pm_runtime_put_autosuspend()` when stopping streaming. They may power the device up at probe time (for example to read identification registers), but should not keep it powered unconditionally after probe.

At system suspend time, the whole camera pipeline must stop streaming, and restart when the system is resumed. This requires coordination between the camera sensor and the rest of the camera pipeline. Bridge drivers are responsible for this coordination, and instruct camera sensors to stop and restart streaming by calling the appropriate subdev operations (`.enable_streams()` or `.disable_streams()`). Camera sensor drivers shall therefore **not** keep track of the streaming state to stop streaming in the PM suspend handler and restart it in the resume handler. Drivers should in general not implement the system PM handlers.

Camera sensor drivers shall **not** implement the subdev `.s_power()` operation, as it is deprecated. While this operation is implemented in some existing drivers as they predate the deprecation, new drivers shall use runtime PM instead. If you feel you need to begin calling `.s_power()` from an ISP or a bridge driver, instead add runtime PM support to the sensor driver you are using and drop its `.s_power()` handler.

Please also see [examples](<#rst-media-camera-sensor-examples>).

<a id="rst-control-framework"></a>

### Control framework

`v4l2_ctrl_handler_setup()` function may not be used in the device's runtime PM `runtime_resume` callback, as it has no way to figure out the power state of the device. This is because the power state of the device is only changed after the power state transition has taken place. The `s_ctrl` callback can be used to obtain device's power state after the power state transition:





<a id="c-pm_runtime_get_if_in_use"></a>

```c
int pm_runtime_get_if_in_use(struct device *dev);
```

The function returns a non-zero value if it succeeded getting the power count or runtime PM was disabled, in either of which cases the driver may proceed to access the device.

<a id="rst-rotation-orientation-and-flipping"></a>

## Rotation, orientation and flipping

Use `v4l2_fwnode_device_parse()` to obtain rotation and orientation information from system firmware and `v4l2_ctrl_new_fwnode_properties()` to register the appropriate controls.

<a id="rst-example-drivers"></a>
<a id="rst-media-camera-sensor-examples"></a>

## Example drivers

Features implemented by sensor drivers vary, and depending on the set of supported features and other qualities, particular sensor drivers better serve the purpose of an example. The following drivers are known to be good examples:


<table>
<caption>Example sensor drivers</caption>
<tbody>
<tr>
<td>


Driver name

</td>
<td>


File(s)

</td>
<td>


Driver type

</td>
<td>


Example topic

</td>
</tr>
<tr>
<td>


CCS

</td>
<td>


`drivers/media/i2c/ccs/`

</td>
<td>


Freely configurable

</td>
<td>


Power management (ACPI and DT), UAPI

</td>
</tr>
<tr>
<td>


imx219

</td>
<td>


`drivers/media/i2c/imx219.c`

</td>
<td>


Register list based

</td>
<td>


Power management (DT), UAPI, mode selection

</td>
</tr>
<tr>
<td>


imx319

</td>
<td>


`drivers/media/i2c/imx319.c`

</td>
<td>


Register list based

</td>
<td>


Power management (ACPI and DT)

</td>
</tr>
</tbody>
</table>
