---
title: "Leds BlinkM driver"
type: reference
description: "The leds-blinkm driver supports the devices of the BlinkM family."
---

<a id="rst-leds-blinkm-driver"></a>

The leds-blinkm driver supports the devices of the BlinkM family.

They are RGB-LED modules driven by a (AT)tiny microcontroller and communicate through I2C. The default address of these modules is 0x09 but this can be changed through a command. By this you could daisy-chain up to 127 BlinkMs on an I2C bus.

The device accepts RGB and HSB color values through separate commands. Also you can store blinking sequences as "scripts" in the controller and run them. Also fading is an option.

The interface this driver provides is 3-fold:

<a id="rst-a-led-multicolor-class-interface-for-use-with-triggers"></a>

## a) LED multicolor class interface for use with triggers

The registration follows the scheme:



```text
blinkm-<i2c-bus-nr>-<i2c-device-nr>:rgb:indicator

$ ls -h /sys/class/leds/blinkm-1-9:rgb:indicator
brightness  device  max_brightness  multi_index  multi_intensity  power  subsystem  trigger  uevent
```

Hue is controlled by the multi_intensity file and lightness is controlled by the brightness file.

The order in which to write the intensity values can be found in multi_index. Exactly three values between 0 and 255 must be written to multi_intensity to change the color:



```text
$ echo 255 100 50 > multi_intensity
```

The overall lightness be changed by writing a value between 0 and 255 to the brightness file.

<a id="rst-b-led-class-interface-for-use-with-triggers"></a>

## b) LED class interface for use with triggers

The registration follows the scheme:



```text
blinkm-<i2c-bus-nr>-<i2c-device-nr>-<color>

$ ls -h /sys/class/leds/blinkm-6-*
/sys/class/leds/blinkm-6-9-blue:
brightness  device  max_brightness  power  subsystem  trigger  uevent

/sys/class/leds/blinkm-6-9-green:
brightness  device  max_brightness  power  subsystem  trigger  uevent

/sys/class/leds/blinkm-6-9-red:
brightness  device  max_brightness  power  subsystem  trigger  uevent
```

(same is /sys/bus/i2c/devices/6-0009/leds)

We can control the colors separated into red, green and blue and assign triggers on each color.

E.g.:



```text
$ cat blinkm-6-9-blue/brightness
05

$ echo 200 > blinkm-6-9-blue/brightness
$

$ modprobe ledtrig-heartbeat
$ echo heartbeat > blinkm-6-9-green/trigger
$
```

<a id="rst-b-sysfs-group-to-control-rgb-fade-hsb-scripts"></a>

## b) Sysfs group to control rgb, fade, hsb, scripts ...

This extended interface is available as folder blinkm in the sysfs folder of the I2C device. E.g. below /sys/bus/i2c/devices/6-0009/blinkm

> $ ls -h /sys/bus/i2c/devices/6-0009/blinkm/ blue  green  red  test

Currently supported is just setting red, green, blue and a test sequence.

E.g.:



```text
$ cat *
00
00
00
#Write into test to start test sequence!#

$ echo 1 > test
$

$ echo 255 > red
$
```

as of 07/2024

dl9pf &lt;at&gt; gmx &lt;dot&gt; de jstrauss &lt;at&gt; mailbox &lt;dot&gt; org
