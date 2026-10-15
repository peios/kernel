---
title: "Programming Interface"
type: reference
description: "The 1.0 driver uses a new, event based approach to the joystick driver. Instead of the user program polling for the joystick values, the joystick driver now reports only any changes of its state. See joystick-api.txt, joystick.h and…"
---

<a id="rst-programming-interface"></a>
<a id="rst-joystick-api"></a>

**Author:** Ragnar Hojland Espinosa &lt;[ragnar@macula.net](<mailto:ragnar@macula.net>)&gt; - 7 Aug 1998

<a id="rst-introduction"></a>

## Introduction

> [!IMPORTANT]
>
> This document describes legacy `js` interface. Newer clients are encouraged to switch to the generic event (`evdev`) interface.

The 1.0 driver uses a new, event based approach to the joystick driver. Instead of the user program polling for the joystick values, the joystick driver now reports only any changes of its state. See joystick-api.txt, joystick.h and jstest.c included in the joystick package for more information. The joystick device can be used in either blocking or nonblocking mode, and supports select() calls.

For backward compatibility the old (v0.x) interface is still included. Any call to the joystick driver using the old interface will return values that are compatible to the old interface. This interface is still limited to 2 axes, and applications using it usually decode only 2 buttons, although the driver provides up to 32.

<a id="rst-initialization"></a>

## Initialization

Open the joystick device following the usual semantics (that is, with open). Since the driver now reports events instead of polling for changes, immediately after the open it will issue a series of synthetic events (JS_EVENT_INIT) that you can read to obtain the initial state of the joystick.

By default, the device is opened in blocking mode:



```text
int fd = open ("/dev/input/js0", O_RDONLY);
```

<a id="rst-event-reading"></a>

## Event Reading



```text
struct js_event e;
read (fd, &e, sizeof(e));
```

where js_event is defined as:



```text
struct js_event {
        __u32 time;     /* event timestamp in milliseconds */
        __s16 value;    /* value */
        __u8 type;      /* event type */
        __u8 number;    /* axis/button number */
};
```

If the read is successful, it will return sizeof(e), unless you wanted to read more than one event per read as described in section 3.1.

<a id="rst-js-event-type"></a>

### js_event.type

The possible values of `type` are:



```text
#define JS_EVENT_BUTTON         0x01    /* button pressed/released */
#define JS_EVENT_AXIS           0x02    /* joystick moved */
#define JS_EVENT_INIT           0x80    /* initial state of device */
```

As mentioned above, the driver will issue synthetic JS_EVENT_INIT ORed events on open. That is, if it's issuing an INIT BUTTON event, the current type value will be:



```text
int type = JS_EVENT_BUTTON | JS_EVENT_INIT;     /* 0x81 */
```

If you choose not to differentiate between synthetic or real events you can turn off the JS_EVENT_INIT bits:



```text
type &= ~JS_EVENT_INIT;                         /* 0x01 */
```

<a id="rst-js-event-number"></a>

### js_event.number

The values of `number` correspond to the axis or button that generated the event. Note that they carry separate numeration (that is, you have both an axis 0 and a button 0). Generally,

>
> <table>
> <thead>
> <tr>
> <th>
>
>
> Axis
>
> </th>
> <th>
>
>
> number
>
> </th>
> </tr>
> </thead>
> <tbody>
> <tr>
> <td>
>
>
> 1st Axis X
>
> </td>
> <td>
>
>
> 0
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 1st Axis Y
>
> </td>
> <td>
>
>
> 1
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 2nd Axis X
>
> </td>
> <td>
>
>
> 2
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 2nd Axis Y
>
> </td>
> <td>
>
>
> 3
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> ...and so on
>
> </td>
> <td>
>
>
>
>
> </td>
> </tr>
> </tbody>
> </table>

Hats vary from one joystick type to another. Some can be moved in 8 directions, some only in 4. The driver, however, always reports a hat as two independent axes, even if the hardware doesn't allow independent movement.

<a id="rst-js-event-value"></a>

### js_event.value

For an axis, `value` is a signed integer between -32767 and +32767 representing the position of the joystick along that axis. If you don't read a 0 when the joystick is `dead`, or if it doesn't span the full range, you should recalibrate it (with, for example, jscal).

For a button, `value` for a press button event is 1 and for a release button event is 0.

Though this:



```text
if (js_event.type == JS_EVENT_BUTTON) {
        buttons_state ^= (1 << js_event.number);
}
```

may work well if you handle JS_EVENT_INIT events separately,



```text
if ((js_event.type & ~JS_EVENT_INIT) == JS_EVENT_BUTTON) {
        if (js_event.value)
                buttons_state |= (1 << js_event.number);
        else
                buttons_state &= ~(1 << js_event.number);
}
```

is much safer since it can't lose sync with the driver. As you would have to write a separate handler for JS_EVENT_INIT events in the first snippet, this ends up being shorter.

<a id="rst-js-event-time"></a>

### js_event.time

The time an event was generated is stored in `js_event.time`. It's a time in milliseconds since ... well, since sometime in the past.  This eases the task of detecting double clicks, figuring out if movement of axis and button presses happened at the same time, and similar.

<a id="rst-reading"></a>

## Reading

If you open the device in blocking mode, a read will block (that is, wait) forever until an event is generated and effectively read. There are two alternatives if you can't afford to wait forever (which is, admittedly, a long time;)

> - **a)** use select to wait until there's data to be read on fd, or until it timeouts. There's a good example on the select(2) man page.
>
> - **b)** open the device in non-blocking mode (O_NONBLOCK)

<a id="rst-o-nonblock"></a>

### O_NONBLOCK

If read returns -1 when reading in O_NONBLOCK mode, this isn't necessarily a "real" error (check errno(3)); it can just mean there are no events pending to be read on the driver queue. You should read all events on the queue (that is, until you get a -1).

For example,



```text
while (1) {
        while (read (fd, &e, sizeof(e)) > 0) {
                process_event (e);
        }
        /* EAGAIN is returned when the queue is empty */
        if (errno != EAGAIN) {
                /* error */
        }
        /* do something interesting with processed events */
}
```

One reason for emptying the queue is that if it gets full you'll start missing events since the queue is finite, and older events will get overwritten.

The other reason is that you want to know all that happened, and not delay the processing till later.

Why can the queue get full? Because you don't empty the queue as mentioned, or because too much time elapses from one read to another and too many events to store in the queue get generated. Note that high system load may contribute to space those reads even more.

If time between reads is enough to fill the queue and lose an event, the driver will switch to startup mode and next time you read it, synthetic events (JS_EVENT_INIT) will be generated to inform you of the actual state of the joystick.

> [!NOTE]
>
> As of version 1.2.8, the queue is circular and able to hold 64 events. You can increment this size bumping up JS_BUFF_SIZE in joystick.h and recompiling the driver.

In the above code, you might as well want to read more than one event at a time using the typical read(2) functionality. For that, you would replace the read above with something like:



```text
struct js_event mybuffer[0xff];
int i = read (fd, mybuffer, sizeof(mybuffer));
```

In this case, read would return -1 if the queue was empty, or some other value in which the number of events read would be i / sizeof(js_event)  Again, if the buffer was full, it's a good idea to process the events and keep reading it until you empty the driver queue.

<a id="rst-ioctls"></a>

## IOCTLs

The joystick driver defines the following ioctl(2) operations:



```text
                        /* function                     3rd arg  */
#define JSIOCGAXES      /* get number of axes           char     */
#define JSIOCGBUTTONS   /* get number of buttons        char     */
#define JSIOCGVERSION   /* get driver version           int      */
#define JSIOCGNAME(len) /* get identifier string        char     */
#define JSIOCSCORR      /* set correction values        &js_corr */
#define JSIOCGCORR      /* get correction values        &js_corr */
```

For example, to read the number of axes:



```text
char number_of_axes;
ioctl (fd, JSIOCGAXES, &number_of_axes);
```

<a id="rst-jsiogcversion"></a>

### JSIOGCVERSION

JSIOGCVERSION is a good way to check in run-time whether the running driver is 1.0+ and supports the event interface. If it is not, the IOCTL will fail. For a compile-time decision, you can test the JS_VERSION symbol:



```text
#ifdef JS_VERSION
#if JS_VERSION > 0xsomething
```

<a id="rst-jsiocgname"></a>

### JSIOCGNAME

JSIOCGNAME(len) allows you to get the name string of the joystick - the same as is being printed at boot time. The 'len' argument is the length of the buffer provided by the application asking for the name. It is used to avoid possible overrun should the name be too long:



```text
char name[128];
if (ioctl(fd, JSIOCGNAME(sizeof(name)), name) < 0)
        strscpy(name, "Unknown", sizeof(name));
printf("Name: %s\n", name);
```

<a id="rst-jsioc-sg-corr"></a>

### JSIOC\[SG\]CORR

For usage on JSIOC\[SG\]CORR I suggest you to look into jscal.c  They are not needed in a normal program, only in joystick calibration software such as jscal or kcmjoy. These IOCTLs and data types aren't considered to be in the stable part of the API, and therefore may change without warning in following releases of the driver.

Both JSIOCSCORR and JSIOCGCORR expect &amp;js_corr to be able to hold information for all axes. That is, struct js_corr corr\[MAX_AXIS\];

struct js_corr is defined as:



```text
struct js_corr {
        __s32 coef[8];
        __u16 prec;
        __u16 type;
};
```

and `type`:



```text
#define JS_CORR_NONE            0x00    /* returns raw values */
#define JS_CORR_BROKEN          0x01    /* broken line */
```

<a id="rst-backward-compatibility"></a>

## Backward compatibility

The 0.x joystick driver API is quite limited and its usage is deprecated. The driver offers backward compatibility, though. Here's a quick summary:



```text
struct JS_DATA_TYPE js;
while (1) {
        if (read (fd, &js, JS_RETURN) != JS_RETURN) {
                /* error */
        }
        usleep (1000);
}
```

As you can figure out from the example, the read returns immediately, with the actual state of the joystick:



```text
struct JS_DATA_TYPE {
        int buttons;    /* immediate button state */
        int x;          /* immediate x axis value */
        int y;          /* immediate y axis value */
};
```

and JS_RETURN is defined as:



```text
#define JS_RETURN       sizeof(struct JS_DATA_TYPE)
```

To test the state of the buttons,



```text
first_button_state  = js.buttons & 1;
second_button_state = js.buttons & 2;
```

The axis values do not have a defined range in the original 0.x driver, except that the values are non-negative. The 1.2.8+ drivers use a fixed range for reporting the values, 1 being the minimum, 128 the center, and 255 maximum value.

The v0.8.0.2 driver also had an interface for 'digital joysticks', (now called Multisystem joysticks in this driver), under /dev/djsX. This driver doesn't try to be compatible with that interface.

<a id="rst-final-notes"></a>

## Final Notes



```text
____/|        Comments, additions, and specially corrections are welcome.
\ o.O|        Documentation valid for at least version 1.2.8 of the joystick
 =(_)=        driver and as usual, the ultimate source for documentation is
   U          to "Use The Source Luke" or, at your convenience, Vojtech ;)
```
