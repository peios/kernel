---
title: "Pattern format for LED pattern trigger"
type: reference
description: "Device-tree binding reference for Pattern format for LED pattern trigger."
---

The pattern is given by a series of tuples, of brightness and duration (ms).
The LED is expected to traverse the series and each brightness value for the
specified duration. Duration of 0 means brightness should immediately change to
new value, and writing malformed pattern deactivates any active one.

1. For gradual dimming, the dimming interval now is set as 50 milliseconds. So
   the tuple with duration less than dimming interval (50ms) is treated as a step
   change of brightness, i.e. the subsequent brightness will be applied without
   adding intervening dimming intervals.

The gradual dimming format of the software pattern values should be:
"brightness\_1 duration\_1 brightness\_2 duration\_2 brightness\_3 duration\_3 ...".
For example (using sysfs interface):

echo 0 1000 255 2000 &gt; pattern

It will make the LED go gradually from zero-intensity to max (255) intensity in
1000 milliseconds, then back to zero intensity in 2000 milliseconds:

LED brightness

```text
    ^
```

255-|       / \\            / \\            /

```text
    |      /    \         /    \         /
    |     /       \      /       \      /
    |    /          \   /          \   /
  0-|   /             \/             \/
    +---0----1----2----3----4----5----6------------> time (s)
```

2. To make the LED go instantly from one brightness value to another, we should
   use zero-time lengths (the brightness must be same as the previous tuple's). So
   the format should be: "brightness\_1 duration\_1 brightness\_1 0 brightness\_2
   duration\_2 brightness\_2 0 ...".
   For example (using sysfs interface):

echo 0 1000 0 0 255 2000 255 0 &gt; pattern

It will make the LED stay off for one second, then stay at max brightness for
two seconds:

LED brightness

```text
    ^
```

```text
255-|        +---------+    +---------+
```

```text
    |        |         |    |         |
    |        |         |    |         |
    |        |         |    |         |
  0-|   -----+         +----+         +----
    +---0----1----2----3----4----5----6------------> time (s)
```
