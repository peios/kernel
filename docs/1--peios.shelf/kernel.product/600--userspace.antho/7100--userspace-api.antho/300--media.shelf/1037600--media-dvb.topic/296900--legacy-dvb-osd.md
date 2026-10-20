---
title: "DVB OSD Device"
type: reference
description: "The DVB OSD device controls the OnScreen-Display of the AV7110 based DVB-cards with hardware MPEG2 decoder. It can be accessed through /dev/dvb/adapter?/osd0. Data types and ioctl definitions can be accessed by including linux/dvb/osd.h in…"
---

<a id="rst-dvb-osd-device"></a>
<a id="rst-dvb-osd"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later OR GPL-2.0 -->

<!-- c:namespace: dtv.legacy.osd -->

> [!NOTE]
>
> Do **not** use in new drivers\! See: [General Notes](<~kernel/userspace/userspace-api/media-dvb/legacy-dvb-decoder-api#rst-legacy-dvb-decoder-notes>)

The DVB OSD device controls the OnScreen-Display of the AV7110 based DVB-cards with hardware MPEG2 decoder. It can be accessed through `/dev/dvb/adapter?/osd0`. Data types and ioctl definitions can be accessed by including `linux/dvb/osd.h` in your application.

The OSD is not a frame-buffer like on many other cards. It is a kind of canvas one can draw on. The color-depth is limited depending on the memory size installed. An appropriate palette of colors has to be set up. The installed memory size can be identified with the [OSD_GET_CAPABILITY](<#rst-osd-get-capability>) ioctl.

<a id="rst-osd-data-types"></a>

## OSD Data Types

<a id="rst-osd-command"></a>

### OSD_Command

<a id="rst-synopsis"></a>

#### Synopsis



```c
typedef enum {
    /* All functions return -2 on "not open" */
    OSD_Close = 1,
    OSD_Open,
    OSD_Show,
    OSD_Hide,
    OSD_Clear,
    OSD_Fill,
    OSD_SetColor,
    OSD_SetPalette,
    OSD_SetTrans,
    OSD_SetPixel,
    OSD_GetPixel,
    OSD_SetRow,
    OSD_SetBlock,
    OSD_FillRow,
    OSD_FillBlock,
    OSD_Line,
    OSD_Query,
    OSD_Test,
    OSD_Text,
    OSD_SetWindow,
    OSD_MoveWindow,
    OSD_OpenRaw,
} OSD_Command;
```

<a id="rst-commands"></a>

#### Commands

> [!NOTE]
>
> All functions return -2 on "not open"


<table>
<thead>
<tr>
<th>


Command

</th>
<th>


Used variables of `struct` [osd_cmd_t](<#rst-osd-cmd-t>).  
Usage\{variable\} if alternative use.

</th>
<th colspan="3">


 Description

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


`OSD_Close`

</td>
<td>


- <!-- empty source list item -->

</td>
<td colspan="3">


Disables OSD and releases the buffers.  
Returns 0 on success.

</td>
</tr>
<tr>
<td>


`OSD_Open`

</td>
<td>


x0,y0,x1,y1,  
BitPerPixel\[2/4/8\]\{color&amp;0x0F\},  
mix\[0..15\]\{color&amp;0xF0\}

</td>
<td colspan="3">


Opens OSD with this size and bit depth  
Returns 0 on success,  
-1 on DRAM allocation error,  
-2 on "already open".

</td>
</tr>
<tr>
<td>


`OSD_Show`

</td>
<td>


- <!-- empty source list item -->

</td>
<td colspan="3">


Enables OSD mode.  
Returns 0 on success.

</td>
</tr>
<tr>
<td>


`OSD_Hide`

</td>
<td>


- <!-- empty source list item -->

</td>
<td colspan="3">


Disables OSD mode.  
Returns 0 on success.

</td>
</tr>
<tr>
<td>


`OSD_Clear`

</td>
<td>


- <!-- empty source list item -->

</td>
<td colspan="3">


Sets all pixel to color 0.  
Returns 0 on success.

</td>
</tr>
<tr>
<td>


`OSD_Fill`

</td>
<td>


color

</td>
<td colspan="3">


Sets all pixel to color &lt;color&gt;.  
Returns 0 on success.

</td>
</tr>
<tr>
<td>


`OSD_SetColor`

</td>
<td>


color,  
R\{x0\},G\{y0\},B\{x1\},  
opacity\{y1\}

</td>
<td colspan="3">


Set palette entry &lt;num&gt; to &lt;r,g,b&gt;, &lt;mix&gt; and &lt;trans&gt; apply  
R,G,B: 0..255  
R=Red, G=Green, B=Blue  
opacity=0:      pixel opacity 0% (only video pixel shows)  
opacity=1..254: pixel opacity as specified in header  
opacity=255:    pixel opacity 100% (only OSD pixel shows)  
Returns 0 on success, -1 on error.

</td>
</tr>
<tr>
<td>


`OSD_SetPalette`

</td>
<td>


firstcolor\{color\},  
lastcolor\{x0\},data

</td>
<td colspan="3">


Set a number of entries in the palette.  
Sets the entries "firstcolor" through "lastcolor" from the
array "data".  
Data has 4 byte for each color:  
R,G,B, and a opacity value: 0-&gt;transparent, 1..254-&gt;mix,
255-&gt;pixel

</td>
</tr>
<tr>
<td>


`OSD_SetTrans`

</td>
<td>


transparency\{color\}

</td>
<td colspan="3">


Sets transparency of mixed pixel (0..15).  
Returns 0 on success.

</td>
</tr>
<tr>
<td>


`OSD_SetPixel`

</td>
<td>


x0,y0,color

</td>
<td colspan="3">


Sets pixel &lt;x&gt;,&lt;y&gt; to color number &lt;color&gt;.  
Returns 0 on success, -1 on error.

</td>
</tr>
<tr>
<td>


`OSD_GetPixel`

</td>
<td>


x0,y0

</td>
<td colspan="3">


Returns color number of pixel &lt;x&gt;,&lt;y&gt;,  or -1.  
Command currently not supported by the AV7110\!

</td>
</tr>
<tr>
<td>


`OSD_SetRow`

</td>
<td>


x0,y0,x1,data

</td>
<td colspan="3">


Fills pixels x0,y through  x1,y with the content of data\[\].  
Returns 0 on success, -1 on clipping all pixel (no pixel
drawn).

</td>
</tr>
<tr>
<td>


`OSD_SetBlock`

</td>
<td>


x0,y0,x1,y1,  
increment\{color\},  
data

</td>
<td colspan="3">


Fills pixels x0,y0 through  x1,y1 with the content of data\[\].  
Inc contains the width of one line in the data block,  
inc&lt;=0 uses block width as line width.  
Returns 0 on success, -1 on clipping all pixel.

</td>
</tr>
<tr>
<td>


`OSD_FillRow`

</td>
<td>


x0,y0,x1,color

</td>
<td colspan="3">


Fills pixels x0,y through  x1,y with the color &lt;color&gt;.  
Returns 0 on success, -1 on clipping all pixel.

</td>
</tr>
<tr>
<td>


`OSD_FillBlock`

</td>
<td>


x0,y0,x1,y1,color

</td>
<td colspan="3">


Fills pixels x0,y0 through  x1,y1 with the color &lt;color&gt;.  
Returns 0 on success, -1 on clipping all pixel.

</td>
</tr>
<tr>
<td>


`OSD_Line`

</td>
<td>


x0,y0,x1,y1,color

</td>
<td colspan="3">


Draw a line from x0,y0 to x1,y1 with the color &lt;color&gt;.  
Returns 0 on success.

</td>
</tr>
<tr>
<td>


`OSD_Query`

</td>
<td>


x0,y0,x1,y1,  
xasp\{color\}; yasp=11

</td>
<td colspan="3">


Fills parameters with the picture dimensions and the pixel
aspect ratio.  
Returns 0 on success.  
Command currently not supported by the AV7110\!

</td>
</tr>
<tr>
<td>


`OSD_Test`

</td>
<td>


- <!-- empty source list item -->

</td>
<td colspan="3">


Draws a test picture.  
For debugging purposes only.  
Returns 0 on success.

</td>
</tr>
<tr>
<td>


`OSD_Text`

</td>
<td>


x0,y0,size,color,text

</td>
<td colspan="3">


Draws a text at position x0,y0 with the color &lt;color&gt;.

</td>
</tr>
<tr>
<td>


`OSD_SetWindow`

</td>
<td>


x0

</td>
<td colspan="3">


Set window with number 0&lt;x0&lt;8 as current.

</td>
</tr>
<tr>
<td>


`OSD_MoveWindow`

</td>
<td>


x0,y0

</td>
<td colspan="3">


Move current window to (x0, y0).

</td>
</tr>
<tr>
<td>


`OSD_OpenRaw`

</td>
<td>


x0,y0,x1,y1,  
[osd_raw_window_t](<#rst-osd-raw-window-t>) \{color\}

</td>
<td colspan="3">


Open other types of OSD windows.

</td>
</tr>
</tbody>
</table>

<a id="rst-description"></a>

#### Description

The `OSD_Command` data type is used with the [OSD_SEND_CMD](<#rst-osd-send-cmd>) ioctl to tell the driver which OSD_Command to execute.

---

<a id="rst-osd-cmd-t"></a>

### osd_cmd_t

<a id="rst-synopsis-1"></a>

#### Synopsis



```c
typedef struct osd_cmd_s {
    OSD_Command cmd;
    int x0;
    int y0;
    int x1;
    int y1;
    int color;
    void __user *data;
} osd_cmd_t;
```

<a id="rst-variables"></a>

#### Variables


<table>
<tbody>
<tr>
<td>


`OSD_Command cmd`

</td>
<td>


[OSD_Command](<#rst-osd-command>) to be executed.

</td>
</tr>
<tr>
<td>


`int x0`

</td>
<td>


First horizontal position.

</td>
</tr>
<tr>
<td>


`int y0`

</td>
<td>


First vertical position.

</td>
</tr>
<tr>
<td>


`int x1`

</td>
<td>


Second horizontal position.

</td>
</tr>
<tr>
<td>


`int y1`

</td>
<td>


Second vertical position.

</td>
</tr>
<tr>
<td>


`int color`

</td>
<td>


Number of the color in the palette.

</td>
</tr>
<tr>
<td>


`void __user *data`

</td>
<td>


Command specific Data.

</td>
</tr>
</tbody>
</table>

<a id="rst-description-1"></a>

#### Description

The `osd_cmd_t` data type is used with the [OSD_SEND_CMD](<#rst-osd-send-cmd>) ioctl. It contains the data for the OSD_Command and the [OSD_Command](<#rst-osd-command>) itself. The structure has to be passed to the driver and the components may be modified by it.

---

<a id="rst-osd-raw-window-t"></a>

### osd_raw_window_t

<a id="rst-synopsis-2"></a>

#### Synopsis



```c
typedef enum {
    OSD_BITMAP1,
    OSD_BITMAP2,
    OSD_BITMAP4,
    OSD_BITMAP8,
    OSD_BITMAP1HR,
    OSD_BITMAP2HR,
    OSD_BITMAP4HR,
    OSD_BITMAP8HR,
    OSD_YCRCB422,
    OSD_YCRCB444,
    OSD_YCRCB444HR,
    OSD_VIDEOTSIZE,
    OSD_VIDEOHSIZE,
    OSD_VIDEOQSIZE,
    OSD_VIDEODSIZE,
    OSD_VIDEOTHSIZE,
    OSD_VIDEOTQSIZE,
    OSD_VIDEOTDSIZE,
    OSD_VIDEONSIZE,
    OSD_CURSOR
} osd_raw_window_t;
```

<a id="rst-constants"></a>

#### Constants


<table>
<tbody>
<tr>
<td>


`OSD_BITMAP1`

</td>
<td colspan="2">


 1 bit bitmap

</td>
</tr>
<tr>
<td>


`OSD_BITMAP2`

</td>
<td colspan="2">


2 bit bitmap

</td>
</tr>
<tr>
<td>


`OSD_BITMAP4`

</td>
<td colspan="2">


4 bit bitmap

</td>
</tr>
<tr>
<td>


`OSD_BITMAP8`

</td>
<td colspan="2">


8 bit bitmap

</td>
</tr>
<tr>
<td>


`OSD_BITMAP1HR`

</td>
<td colspan="2">


1 Bit bitmap half resolution

</td>
</tr>
<tr>
<td>


`OSD_BITMAP2HR`

</td>
<td colspan="2">


2 Bit bitmap half resolution

</td>
</tr>
<tr>
<td>


`OSD_BITMAP4HR`

</td>
<td colspan="2">


4 Bit bitmap half resolution

</td>
</tr>
<tr>
<td>


`OSD_BITMAP8HR`

</td>
<td colspan="2">


8 Bit bitmap half resolution

</td>
</tr>
<tr>
<td>


`OSD_YCRCB422`

</td>
<td colspan="2">


4:2:2 YCRCB Graphic Display

</td>
</tr>
<tr>
<td>


`OSD_YCRCB444`

</td>
<td colspan="2">


4:4:4 YCRCB Graphic Display

</td>
</tr>
<tr>
<td>


`OSD_YCRCB444HR`

</td>
<td colspan="2">


4:4:4 YCRCB graphic half resolution

</td>
</tr>
<tr>
<td>


`OSD_VIDEOTSIZE`

</td>
<td colspan="2">


True Size Normal MPEG Video Display

</td>
</tr>
<tr>
<td>


`OSD_VIDEOHSIZE`

</td>
<td colspan="2">


MPEG Video Display Half Resolution

</td>
</tr>
<tr>
<td>


`OSD_VIDEOQSIZE`

</td>
<td colspan="2">


MPEG Video Display Quarter Resolution

</td>
</tr>
<tr>
<td>


`OSD_VIDEODSIZE`

</td>
<td colspan="2">


MPEG Video Display Double Resolution

</td>
</tr>
<tr>
<td>


`OSD_VIDEOTHSIZE`

</td>
<td colspan="2">


True Size MPEG Video Display Half Resolution

</td>
</tr>
<tr>
<td>


`OSD_VIDEOTQSIZE`

</td>
<td colspan="2">


True Size MPEG Video Display Quarter Resolution

</td>
</tr>
<tr>
<td>


`OSD_VIDEOTDSIZE`

</td>
<td colspan="2">


True Size MPEG Video Display Double Resolution

</td>
</tr>
<tr>
<td>


`OSD_VIDEONSIZE`

</td>
<td colspan="2">


Full Size MPEG Video Display

</td>
</tr>
<tr>
<td>


`OSD_CURSOR`

</td>
<td colspan="2">


Cursor

</td>
</tr>
</tbody>
</table>

<a id="rst-description-2"></a>

#### Description

The `osd_raw_window_t` data type is used with the [OSD_Command](<#rst-osd-command>) OSD_OpenRaw to tell the driver which type of OSD to open.

---

<a id="rst-osd-cap-t"></a>

### osd_cap_t

<a id="rst-synopsis-3"></a>

#### Synopsis



```c
typedef struct osd_cap_s {
    int  cmd;
#define OSD_CAP_MEMSIZE         1
    long val;
} osd_cap_t;
```

<a id="rst-variables-1"></a>

#### Variables


<table>
<tbody>
<tr>
<td>


`int  cmd`

</td>
<td>


Capability to query.

</td>
</tr>
<tr>
<td>


`long val`

</td>
<td>


Used to store the Data.

</td>
</tr>
</tbody>
</table>

<a id="rst-supported-capabilities"></a>

#### Supported capabilities


<table>
<tbody>
<tr>
<td>


`OSD_CAP_MEMSIZE`

</td>
<td>


Memory size installed on the card.

</td>
</tr>
</tbody>
</table>

<a id="rst-description-3"></a>

#### Description

This structure of data used with the [OSD_GET_CAPABILITY](<#rst-osd-get-capability>) call.

---

<a id="rst-osd-function-calls"></a>

## OSD Function Calls

<a id="rst-osd-send-cmd"></a>

### OSD_SEND_CMD

<a id="rst-synopsis-4"></a>

#### Synopsis





<a id="c-OSD_SEND_CMD"></a>

```c
OSD_SEND_CMD
```



```c
int ioctl(int fd, int request = OSD_SEND_CMD, enum osd_cmd_t *cmd)
```

<a id="rst-arguments"></a>

#### Arguments


<table>
<tbody>
<tr>
<td>


`int fd`

</td>
<td colspan="2">


 File descriptor returned by a previous call to [open()](<#rst-open>).

</td>
</tr>
<tr>
<td>


`int request`

</td>
<td colspan="2">


Pointer to the location of the structure [osd_cmd_t](<#rst-osd-cmd-t>) for this command.

</td>
</tr>
</tbody>
</table>

<a id="rst-description-4"></a>

#### Description

> [!NOTE]
>
> Do **not** use in new drivers\! See: [General Notes](<~kernel/userspace/userspace-api/media-dvb/legacy-dvb-decoder-api#rst-legacy-dvb-decoder-notes>)

This ioctl sends the [OSD_Command](<#rst-osd-command>) to the card.

<a id="rst-return-value"></a>

#### Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.


<table>
<tbody>
<tr>
<td>


`EINVAL`

</td>
<td>


Command is out of range.

</td>
</tr>
</tbody>
</table>

---

<a id="rst-osd-get-capability"></a>

### OSD_GET_CAPABILITY

<a id="rst-synopsis-5"></a>

#### Synopsis





<a id="c-OSD_GET_CAPABILITY"></a>

```c
OSD_GET_CAPABILITY
```



```c
int ioctl(int fd, int request = OSD_GET_CAPABILITY,
struct osd_cap_t *cap)
```

<a id="rst-arguments-1"></a>

#### Arguments


<table>
<tbody>
<tr>
<td>


`int fd`

</td>
<td colspan="2">


 File descriptor returned by a previous call to [open()](<#rst-open>).

</td>
</tr>
<tr>
<td>


`int request`

</td>
<td colspan="2">


Equals `OSD_GET_CAPABILITY` for this command.

</td>
</tr>
<tr>
<td>


`unsigned int *cap`

</td>
<td colspan="2">


Pointer to the location of the structure [osd_cap_t](<#rst-osd-cap-t>) for this command.

</td>
</tr>
</tbody>
</table>

<a id="rst-description-5"></a>

#### Description

> [!NOTE]
>
> Do **not** use in new drivers\! See: [General Notes](<~kernel/userspace/userspace-api/media-dvb/legacy-dvb-decoder-api#rst-legacy-dvb-decoder-notes>)

This ioctl is used to get the capabilities of the OSD of the AV7110 based DVB-decoder-card in use.

> [!NOTE]
>
> The structure osd_cap_t has to be setup by the user and passed to the driver.

<a id="rst-return-value-1"></a>

#### Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.


<table>
<tbody>
<tr>
<td>


`EINVAL`

</td>
<td>


Unsupported capability.

</td>
</tr>
</tbody>
</table>

---

<a id="rst-open"></a>

### open()

<a id="rst-synopsis-6"></a>

#### Synopsis



```c
#include <fcntl.h>
```





<a id="c-open"></a>

```c
int open(const char *deviceName, int flags)
```

<a id="rst-arguments-2"></a>

#### Arguments


<table>
<tbody>
<tr>
<td>


`const char *deviceName`

</td>
<td colspan="2">


Name of specific OSD device.

</td>
</tr>
<tr>
<td rowspan="4">


 `int flags`

</td>
<td colspan="2">


 A bit-wise OR of the following flags:

</td>
</tr>
<tr>
<td>


`O_RDONLY`

</td>
<td>


read-only access

</td>
</tr>
<tr>
<td>


`O_RDWR`

</td>
<td>


read/write access

</td>
</tr>
<tr>
<td>


`O_NONBLOCK`

</td>
<td>


Open in non-blocking mode  
(blocking mode is the default)

</td>
</tr>
</tbody>
</table>

<a id="rst-description-6"></a>

#### Description

This system call opens a named OSD device (e.g. `/dev/dvb/adapter?/osd0`) for subsequent use.

<a id="rst-return-value-2"></a>

#### Return Value


<table>
<tbody>
<tr>
<td>


`ENODEV`

</td>
<td>


Device driver not loaded/available.

</td>
</tr>
<tr>
<td>


`EINTERNAL`

</td>
<td>


Internal error.

</td>
</tr>
<tr>
<td>


`EBUSY`

</td>
<td>


Device or resource busy.

</td>
</tr>
<tr>
<td>


`EINVAL`

</td>
<td>


Invalid argument.

</td>
</tr>
</tbody>
</table>

---

<a id="rst-close"></a>

### close()

<a id="rst-synopsis-7"></a>

#### Synopsis





<a id="c-close"></a>

```c
int close(int fd)
```

<a id="rst-arguments-3"></a>

#### Arguments


<table>
<tbody>
<tr>
<td>


`int fd`

</td>
<td colspan="2">


 File descriptor returned by a previous call to [open()](<#rst-open>) .

</td>
</tr>
</tbody>
</table>

<a id="rst-description-7"></a>

#### Description

This system call closes a previously opened OSD device.

<a id="rst-return-value-3"></a>

#### Return Value


<table>
<tbody>
<tr>
<td>


`EBADF`

</td>
<td>


fd is not a valid open file descriptor.

</td>
</tr>
</tbody>
</table>
