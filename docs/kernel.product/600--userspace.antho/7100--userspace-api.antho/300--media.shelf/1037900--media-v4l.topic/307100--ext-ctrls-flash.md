---
title: "Flash Control Reference"
type: reference
description: "The V4L2 flash controls are intended to provide generic access to flash controller devices. Flash controller devices are typically used in digital cameras."
---

<a id="rst-flash-control-reference"></a>
<a id="rst-flash-controls"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

The V4L2 flash controls are intended to provide generic access to flash controller devices. Flash controller devices are typically used in digital cameras.

The interface can support both LED and xenon flash devices. As of writing this, there is no xenon flash driver using this interface.

<a id="rst-supported-use-cases"></a>
<a id="rst-flash-controls-use-cases"></a>

## Supported use cases

<a id="rst-unsynchronised-led-flash-software-strobe"></a>

### Unsynchronised LED flash (software strobe)

Unsynchronised LED flash is controlled directly by the host as the sensor. The flash must be enabled by the host before the exposure of the image starts and disabled once it ends. The host is fully responsible for the timing of the flash.

Example of such device: Nokia N900.

<a id="rst-synchronised-led-flash-hardware-strobe"></a>

### Synchronised LED flash (hardware strobe)

The synchronised LED flash is pre-programmed by the host (power and timeout) but controlled by the sensor through a strobe signal from the sensor to the flash.

The sensor controls the flash duration and timing. This information typically must be made available to the sensor.

<a id="rst-led-flash-as-torch"></a>

### LED flash as torch

LED flash may be used as torch in conjunction with another use case involving camera or individually.

<a id="rst-flash-control-ids"></a>
<a id="rst-flash-control-id"></a>

### Flash Control IDs

- **`V4L2_CID_FLASH_CLASS (class)`**

  The FLASH class descriptor.

<a id="rst-v4l2-cid-flash-led-mode"></a>

- **`V4L2_CID_FLASH_LED_MODE (menu)`**

  Defines the mode of the flash LED, the high-power white LED attached to the flash controller. Setting this control may not be possible in presence of some faults. See V4L2_CID_FLASH_FAULT.

<!-- tabularcolumns: |p{5.7cm}|p{11.8cm}| -->


<table>
<tbody>
<tr>
<td>


`V4L2_FLASH_LED_MODE_NONE`

</td>
<td>


Off.

</td>
</tr>
<tr>
<td>


`V4L2_FLASH_LED_MODE_FLASH`

</td>
<td>


Flash mode.

</td>
</tr>
<tr>
<td>


`V4L2_FLASH_LED_MODE_TORCH`

</td>
<td>


Torch mode.

See V4L2_CID_FLASH_TORCH_INTENSITY.

</td>
</tr>
</tbody>
</table>

<a id="rst-v4l2-cid-flash-strobe-source"></a>

- **`V4L2_CID_FLASH_STROBE_SOURCE (menu)`**

  Defines the source of the flash LED strobe.

<!-- tabularcolumns: |p{7.5cm}|p{7.5cm}| -->


<table>
<tbody>
<tr>
<td>


`V4L2_FLASH_STROBE_SOURCE_SOFTWARE`

</td>
<td>


The flash strobe is triggered by using the V4L2_CID_FLASH_STROBE control.

</td>
</tr>
<tr>
<td>


`V4L2_FLASH_STROBE_SOURCE_EXTERNAL`

</td>
<td>


The flash strobe is triggered by an external source. Typically this is a sensor, which makes it possible to synchronise the flash strobe start to exposure start. This method of controlling flash LED strobe has two additional prerequisites: the strobe source's [strobe output](<#rst-v4l2-cid-flash-strobe-oe>) must be enabled (if available) and the flash controller's [flash LED mode](<#rst-v4l2-cid-flash-led-mode>) must be set to `V4L2_FLASH_LED_MODE_FLASH`.

</td>
</tr>
</tbody>
</table>

- **`V4L2_CID_FLASH_STROBE (button)`**

  Strobe flash. Valid when V4L2_CID_FLASH_LED_MODE is set to V4L2_FLASH_LED_MODE_FLASH and V4L2_CID_FLASH_STROBE_SOURCE is set to V4L2_FLASH_STROBE_SOURCE_SOFTWARE. Setting this control may not be possible in presence of some faults. See V4L2_CID_FLASH_FAULT.

- **`V4L2_CID_FLASH_STROBE_STOP (button)`**

  Stop flash strobe immediately.

- **`V4L2_CID_FLASH_STROBE_STATUS (boolean)`**

  Strobe status: whether the flash is strobing at the moment or not. This is a read-only control.

- **`V4L2_CID_FLASH_TIMEOUT (integer)`**

  Hardware timeout for flash. The flash strobe is stopped after this period of time has passed from the start of the strobe.

- **`V4L2_CID_FLASH_INTENSITY (integer)`**

  Intensity of the flash strobe when the flash LED is in flash mode (V4L2_FLASH_LED_MODE_FLASH). The unit should be milliamps (mA) if possible.

- **`V4L2_CID_FLASH_TORCH_INTENSITY (integer)`**

  Intensity of the flash LED in torch mode (V4L2_FLASH_LED_MODE_TORCH). The unit should be milliamps (mA) if possible. Setting this control may not be possible in presence of some faults. See V4L2_CID_FLASH_FAULT.

- **`V4L2_CID_FLASH_INDICATOR_INTENSITY (integer)`**

  Intensity of the indicator LED. The indicator LED may be fully independent of the flash LED. The unit should be microamps (uA) if possible.

- **`V4L2_CID_FLASH_FAULT (bitmask)`**

  Faults related to the flash. The faults tell about specific problems in the flash chip itself or the LEDs attached to it. Faults may prevent further use of some of the flash controls. In particular, V4L2_CID_FLASH_LED_MODE is set to V4L2_FLASH_LED_MODE_NONE if the fault affects the flash LED. Exactly which faults have such an effect is chip dependent. Reading the faults resets the control and returns the chip to a usable state if possible.

<!-- tabularcolumns: |p{8.4cm}|p{9.1cm}| -->


<table>
<tbody>
<tr>
<td>


`V4L2_FLASH_FAULT_OVER_VOLTAGE`

</td>
<td>


Flash controller voltage to the flash LED has exceeded the limit specific to the flash controller.

</td>
</tr>
<tr>
<td>


`V4L2_FLASH_FAULT_TIMEOUT`

</td>
<td>


The flash strobe was still on when the timeout set by the user --- V4L2_CID_FLASH_TIMEOUT control --- has expired. Not all flash controllers may set this in all such conditions.

</td>
</tr>
<tr>
<td>


`V4L2_FLASH_FAULT_OVER_TEMPERATURE`

</td>
<td>


The flash controller has overheated.

</td>
</tr>
<tr>
<td>


`V4L2_FLASH_FAULT_SHORT_CIRCUIT`

</td>
<td>


The short circuit protection of the flash controller has been triggered.

</td>
</tr>
<tr>
<td>


`V4L2_FLASH_FAULT_OVER_CURRENT`

</td>
<td>


Current in the LED power supply has exceeded the limit specific to the flash controller.

</td>
</tr>
<tr>
<td>


`V4L2_FLASH_FAULT_INDICATOR`

</td>
<td>


The flash controller has detected a short or open circuit condition on the indicator LED.

</td>
</tr>
<tr>
<td>


`V4L2_FLASH_FAULT_UNDER_VOLTAGE`

</td>
<td>


Flash controller voltage to the flash LED has been below the minimum limit specific to the flash controller.

</td>
</tr>
<tr>
<td>


`V4L2_FLASH_FAULT_INPUT_VOLTAGE`

</td>
<td>


The input voltage of the flash controller is below the limit under which strobing the flash at full current will not be possible.The condition persists until this flag is no longer set.

</td>
</tr>
<tr>
<td>


`V4L2_FLASH_FAULT_LED_OVER_TEMPERATURE`

</td>
<td>


The temperature of the LED has exceeded its allowed upper limit.

</td>
</tr>
</tbody>
</table>

- **`V4L2_CID_FLASH_CHARGE (boolean)`**

  Enable or disable charging of the xenon flash capacitor.

- **`V4L2_CID_FLASH_READY (boolean)`**

  Is the flash ready to strobe? Xenon flashes require their capacitors charged before strobing. LED flashes often require a cooldown period after strobe during which another strobe will not be possible. This is a read-only control.

<a id="rst-v4l2-cid-flash-duration"></a>

- **`V4L2_CID_FLASH_DURATION (integer)`**

  Duration of the flash strobe pulse generated by the strobe source, when using external strobe. This control shall be implemented by the device generating the hardware flash strobe signal, typically a camera sensor, connected to a flash controller.

  The flash controllers [strobe source](<#rst-v4l2-cid-flash-strobe-source>) must be configured to `V4L2_FLASH_STROBE_SOURCE_EXTERNAL` for this mode of operation. For more details please also take a look at the documentation there.

  The unit should be microseconds (µs) if possible.

<a id="rst-v4l2-cid-flash-strobe-oe"></a>

- **`V4L2_CID_FLASH_STROBE_OE (boolean)`**

  Enables the output of a hardware strobe signal from the strobe source, when using external strobe. This control shall be implemented by the device generating the hardware flash strobe signal, typically a camera sensor, connected to a flash controller.

  Provided the signal generating device driver supports it, the length of the strobe signal can be configured by adjusting its [flash duration](<#rst-v4l2-cid-flash-duration>).

  The flash controllers [strobe source](<#rst-v4l2-cid-flash-strobe-source>) must be configured to `V4L2_FLASH_STROBE_SOURCE_EXTERNAL` for this mode of operation. For more details please also take a look at the documentation there.
