---
title: "DVB Video Device"
type: reference
description: "The DVB video device controls the MPEG2 video decoder of the DVB hardware. It can be accessed through /dev/dvb/adapter0/video0. Data types and ioctl definitions can be accessed by including linux/dvb/video.h in your application."
---

<a id="rst-dvb-video-device"></a>
<a id="rst-dvb-video"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later OR GPL-2.0 -->

<!-- c:namespace: dtv.legacy.video -->

> [!NOTE]
>
> Do **not** use in new drivers\! See: [General Notes](<~kernel/userspace/userspace-api/media-dvb/legacy-dvb-decoder-api#rst-legacy-dvb-decoder-notes>)

The DVB video device controls the MPEG2 video decoder of the DVB hardware. It can be accessed through `/dev/dvb/adapter0/video0`. Data types and ioctl definitions can be accessed by including `linux/dvb/video.h` in your application.

Note that the DVB video device only controls decoding of the MPEG video stream, not its presentation on the TV or computer screen. On PCs this is typically handled by an associated video4linux device, e.g. `/dev/video`, which allows scaling and defining output windows.

Most DVB cards don’t have their own MPEG decoder, which results in the omission of the audio and video device as well as the video4linux device.

These ioctls were also used by V4L2 to control MPEG decoders implemented in V4L2. The use of these ioctls for that purpose has been made obsolete and proper V4L2 ioctls or controls have been created to replace that functionality. Use [V4L2 ioctls](<~kernel/userspace/userspace-api/media-v4l/video#rst-video>) for new drivers\!

<a id="rst-video-data-types"></a>

## Video Data Types

<a id="rst-video-format-t"></a>

### video_format_t

<a id="rst-synopsis"></a>

#### Synopsis



```c
typedef enum {
    VIDEO_FORMAT_4_3,
    VIDEO_FORMAT_16_9,
    VIDEO_FORMAT_221_1
} video_format_t;
```

<a id="rst-constants"></a>

#### Constants


<table>
<tbody>
<tr>
<td>


`VIDEO_FORMAT_4_3`

</td>
<td>


Select 4:3 format.

</td>
</tr>
<tr>
<td>


`VIDEO_FORMAT_16_9`

</td>
<td>


Select 16:9 format.

</td>
</tr>
<tr>
<td>


`VIDEO_FORMAT_221_1`

</td>
<td>


Select 2.21:1 format.

</td>
</tr>
</tbody>
</table>

<a id="rst-description"></a>

#### Description

The `video_format_t` data type is used in the [VIDEO_SET_FORMAT](<#rst-video-set-format>) function to tell the driver which aspect ratio the output hardware (e.g. TV) has. It is also used in the data structures [video_status](<#rst-video-status>) returned by [VIDEO_GET_STATUS](<#rst-video-get-status>) and [video_event](<#rst-video-event>) returned by [VIDEO_GET_EVENT](<#rst-video-get-event>) which report about the display format of the current video stream.

---

<a id="rst-video-displayformat-t"></a>

### video_displayformat_t

<a id="rst-synopsis-1"></a>

#### Synopsis



```c
typedef enum {
    VIDEO_PAN_SCAN,
    VIDEO_LETTER_BOX,
    VIDEO_CENTER_CUT_OUT
} video_displayformat_t;
```

<a id="rst-constants-1"></a>

#### Constants


<table>
<tbody>
<tr>
<td>


`VIDEO_PAN_SCAN`

</td>
<td>


Use pan and scan format.

</td>
</tr>
<tr>
<td>


`VIDEO_LETTER_BOX`

</td>
<td>


Use letterbox format.

</td>
</tr>
<tr>
<td>


`VIDEO_CENTER_CUT_OUT`

</td>
<td>


Use center cut out format.

</td>
</tr>
</tbody>
</table>

<a id="rst-description-1"></a>

#### Description

In case the display format of the video stream and of the display hardware differ the application has to specify how to handle the cropping of the picture. This can be done using the [VIDEO_SET_DISPLAY_FORMAT](<#rst-video-set-display-format>) call which accepts this enum as argument.

---

<a id="rst-video-size-t"></a>

### video_size_t

<a id="rst-synopsis-2"></a>

#### Synopsis



```c
typedef struct {
    int w;
    int h;
    video_format_t aspect_ratio;
} video_size_t;
```

<a id="rst-variables"></a>

#### Variables


<table>
<tbody>
<tr>
<td>


`int w`

</td>
<td>


Video width in pixels.

</td>
</tr>
<tr>
<td>


`int h`

</td>
<td>


Video height in pixels.

</td>
</tr>
<tr>
<td>


[video_format_t](<#rst-video-format-t>) `aspect_ratio`

</td>
<td>


Aspect ratio.

</td>
</tr>
</tbody>
</table>

<a id="rst-description-2"></a>

#### Description

Used in the struct [video_event](<#rst-video-event>). It stores the resolution and aspect ratio of the video.

---

<a id="rst-video-stream-source-t"></a>

### video_stream_source_t

<a id="rst-synopsis-3"></a>

#### Synopsis



```c
typedef enum {
    VIDEO_SOURCE_DEMUX,
    VIDEO_SOURCE_MEMORY
} video_stream_source_t;
```

<a id="rst-constants-2"></a>

#### Constants


<table>
<tbody>
<tr>
<td>


`VIDEO_SOURCE_DEMUX`

</td>
<td colspan="2">


 Select the demux as the main source.

</td>
</tr>
<tr>
<td>


`VIDEO_SOURCE_MEMORY`

</td>
<td colspan="2">


If this source is selected, the stream comes from the user through the write system call.

</td>
</tr>
</tbody>
</table>

<a id="rst-description-3"></a>

#### Description

The video stream source is set through the [VIDEO_SELECT_SOURCE](<#rst-video-select-source>) call and can take the following values, depending on whether we are replaying from an internal (demuxer) or external (user write) source. VIDEO_SOURCE_DEMUX selects the demultiplexer (fed either by the frontend or the DVR device) as the source of the video stream. If VIDEO_SOURCE_MEMORY is selected the stream comes from the application through the [write()](<#rst-write>) system call.

---

<a id="rst-video-play-state-t"></a>

### video_play_state_t

<a id="rst-synopsis-4"></a>

#### Synopsis



```c
typedef enum {
    VIDEO_STOPPED,
    VIDEO_PLAYING,
    VIDEO_FREEZED
} video_play_state_t;
```

<a id="rst-constants-3"></a>

#### Constants


<table>
<tbody>
<tr>
<td>


`VIDEO_STOPPED`

</td>
<td>


Video is stopped.

</td>
</tr>
<tr>
<td>


`VIDEO_PLAYING`

</td>
<td>


Video is currently playing.

</td>
</tr>
<tr>
<td>


`VIDEO_FREEZED`

</td>
<td>


Video is frozen.

</td>
</tr>
</tbody>
</table>

<a id="rst-description-4"></a>

#### Description

This values can be returned by the [VIDEO_GET_STATUS](<#rst-video-get-status>) call representing the state of video playback.

---

<a id="rst-struct-video-command"></a>

### struct video_command

<a id="rst-synopsis-5"></a>

#### Synopsis



```c
struct video_command {
    __u32 cmd;
    __u32 flags;
    union {
        struct {
            __u64 pts;
        } stop;

        struct {
            __s32 speed;
            __u32 format;
        } play;

        struct {
            __u32 data[16];
        } raw;
    };
};
```

<a id="rst-variables-1"></a>

#### Variables


<table>
<tbody>
<tr>
<td>


`__u32 cmd`

</td>
<td colspan="2">


[Decoder command](<#rst-decoder-command>)

</td>
</tr>
<tr>
<td>


`__u32 flags`

</td>
<td colspan="2">


Flags for the [Decoder command](<#rst-decoder-command>).

</td>
</tr>
<tr>
<td>


`struct stop`

</td>
<td>


`__u64 pts`

</td>
<td>


MPEG PTS

</td>
</tr>
<tr>
<td rowspan="6">


 `stuct play`

</td>
<td rowspan="5">


 `__s32 speed`

</td>
<td>


0 or 1000 specifies normal speed,

</td>
</tr>
<tr>
<td>


1:  specifies forward single stepping,

</td>
</tr>
<tr>
<td>


-1: specifies backward single stepping,

</td>
</tr>
<tr>
<td>


&gt;1: playback at speed / 1000 of the normal speed

</td>
</tr>
<tr>
<td>


&lt;-1: reverse playback at ( -speed / 1000 ) of the normal speed.

</td>
</tr>
<tr>
<td>


`__u32 format`

</td>
<td>


[Play input formats](<#rst-play-input-formats>)

</td>
</tr>
<tr>
<td>


`__u32 data[16]`

</td>
<td colspan="2">


Reserved

</td>
</tr>
</tbody>
</table>

<a id="rst-description-5"></a>

#### Description

The structure must be zeroed before use by the application. This ensures it can be extended safely in the future.

---

<a id="rst-predefined-decoder-commands-and-flags"></a>

### Predefined decoder commands and flags

<a id="rst-synopsis-6"></a>

#### Synopsis



```c
#define VIDEO_CMD_PLAY                      (0)
#define VIDEO_CMD_STOP                      (1)
#define VIDEO_CMD_FREEZE                    (2)
#define VIDEO_CMD_CONTINUE                  (3)

#define VIDEO_CMD_FREEZE_TO_BLACK      (1 << 0)

#define VIDEO_CMD_STOP_TO_BLACK        (1 << 0)
#define VIDEO_CMD_STOP_IMMEDIATELY     (1 << 1)

#define VIDEO_PLAY_FMT_NONE                 (0)
#define VIDEO_PLAY_FMT_GOP                  (1)

#define VIDEO_VSYNC_FIELD_UNKNOWN           (0)
#define VIDEO_VSYNC_FIELD_ODD               (1)
#define VIDEO_VSYNC_FIELD_EVEN              (2)
#define VIDEO_VSYNC_FIELD_PROGRESSIVE       (3)
```

<a id="rst-constants-4"></a>

#### Constants


<table>
<tbody>
<tr>
<td rowspan="4">


 <a id="rst-decoder-command"></a>

</td>
<td>


`VIDEO_CMD_PLAY`

</td>
<td>


Start playback.

</td>
</tr>
<tr>
<td>


`VIDEO_CMD_STOP`

</td>
<td>


Stop playback.

</td>
</tr>
<tr>
<td>


`VIDEO_CMD_FREEZE`

</td>
<td>


Freeze playback.

</td>
</tr>
<tr>
<td>


`VIDEO_CMD_CONTINUE`

</td>
<td>


Continue playback after freeze.

</td>
</tr>
<tr>
<td>


Flags for `VIDEO_CMD_FREEZE`

</td>
<td>


`VIDEO_CMD_FREEZE_TO_BLACK`

</td>
<td>


Show black picture on freeze.

</td>
</tr>
<tr>
<td rowspan="2">


 Flags for `VIDEO_CMD_STOP`

</td>
<td>


`VIDEO_CMD_STOP_TO_BLACK`

</td>
<td>


Show black picture on stop.

</td>
</tr>
<tr>
<td>


`VIDEO_CMD_STOP_IMMEDIATELY`

</td>
<td>


Stop immediately, without emptying buffers.

</td>
</tr>
<tr>
<td rowspan="2">


 <a id="rst-play-input-formats"></a>

</td>
<td>


`VIDEO_PLAY_FMT_NONE`

</td>
<td>


The decoder has no special format requirements

</td>
</tr>
<tr>
<td>


`VIDEO_PLAY_FMT_GOP`

</td>
<td>


The decoder requires full GOPs

</td>
</tr>
<tr>
<td rowspan="4">


 Field order

</td>
<td>


`VIDEO_VSYNC_FIELD_UNKNOWN`

</td>
<td>


FIELD_UNKNOWN can be used if the hardware does not know whether the Vsync is for an odd, even or progressive (i.e. non-interlaced) field.

</td>
</tr>
<tr>
<td>


`VIDEO_VSYNC_FIELD_ODD`

</td>
<td>


Vsync is for an odd field.

</td>
</tr>
<tr>
<td>


`VIDEO_VSYNC_FIELD_EVEN`

</td>
<td>


Vsync is for an even field.

</td>
</tr>
<tr>
<td>


`VIDEO_VSYNC_FIELD_PROGRESSIVE`

</td>
<td>


progressive (i.e. non-interlaced)

</td>
</tr>
</tbody>
</table>

---

<a id="rst-video-event"></a>

### video_event

<a id="rst-synopsis-7"></a>

#### Synopsis



```c
struct video_event {
    __s32 type;
#define VIDEO_EVENT_SIZE_CHANGED        1
#define VIDEO_EVENT_FRAME_RATE_CHANGED  2
#define VIDEO_EVENT_DECODER_STOPPED     3
#define VIDEO_EVENT_VSYNC               4
    long timestamp;
    union {
        video_size_t size;
        unsigned int frame_rate;
        unsigned char vsync_field;
    } u;
};
```

<a id="rst-variables-2"></a>

#### Variables


<table>
<tbody>
<tr>
<td rowspan="5">


 `__s32 type`

</td>
<td colspan="2">


 Event type.

</td>
</tr>
<tr>
<td>


`VIDEO_EVENT_SIZE_CHANGED`

</td>
<td>


Size changed.

</td>
</tr>
<tr>
<td>


`VIDEO_EVENT_FRAME_RATE_CHANGED`

</td>
<td>


Framerate changed.

</td>
</tr>
<tr>
<td>


`VIDEO_EVENT_DECODER_STOPPED`

</td>
<td>


Decoder stopped.

</td>
</tr>
<tr>
<td>


`VIDEO_EVENT_VSYNC`

</td>
<td>


Vsync occurred.

</td>
</tr>
<tr>
<td>


`long timestamp`

</td>
<td colspan="2">


 MPEG PTS at occurrence.

</td>
</tr>
<tr>
<td rowspan="3">


 `union u`

</td>
<td>


[video_size_t](<#rst-video-size-t>) size

</td>
<td>


Resolution and aspect ratio of the video.

</td>
</tr>
<tr>
<td>


`unsigned int frame_rate`

</td>
<td>


in frames per 1000sec

</td>
</tr>
<tr>
<td>


`unsigned char vsync_field`

</td>
<td>


unknown / odd / even / progressive  
See: [Predefined decoder commands and flags](<#rst-predefined-decoder-commands-and-flags>)

</td>
</tr>
</tbody>
</table>

<a id="rst-description-6"></a>

#### Description

This is the structure of a video event as it is returned by the [VIDEO_GET_EVENT](<#rst-video-get-event>) call. See there for more details.

---

<a id="rst-video-status"></a>

### video_status

<a id="rst-synopsis-8"></a>

#### Synopsis

The [VIDEO_GET_STATUS](<#rst-video-get-status>) call returns the following structure informing about various states of the playback operation.



```c
struct video_status {
    int                    video_blank;
    video_play_state_t     play_state;
    video_stream_source_t  stream_source;
    video_format_t         video_format;
    video_displayformat_t  display_format;
};
```

<a id="rst-variables-3"></a>

#### Variables


<table>
<tbody>
<tr>
<td rowspan="3">


 `int video_blank`

</td>
<td colspan="2">


 Show blank video on freeze?

</td>
</tr>
<tr>
<td>


TRUE  ( \!= 0 )

</td>
<td>


Blank screen when freeze.

</td>
</tr>
<tr>
<td>


FALSE ( == 0 )

</td>
<td>


Show last decoded frame.

</td>
</tr>
<tr>
<td>


[video_play_state_t](<#rst-video-play-state-t>) `play_state`

</td>
<td colspan="2">


Current state of playback.

</td>
</tr>
<tr>
<td>


[video_stream_source_t](<#rst-video-stream-source-t>) `stream_source`

</td>
<td colspan="2">


Current source (demux/memory).

</td>
</tr>
<tr>
<td>


[video_format_t](<#rst-video-format-t>) `video_format`

</td>
<td colspan="2">


Current aspect ratio of stream.

</td>
</tr>
<tr>
<td>


[video_displayformat_t](<#rst-video-displayformat-t>) `display_format`

</td>
<td colspan="2">


Applied cropping mode.

</td>
</tr>
</tbody>
</table>

<a id="rst-description-7"></a>

#### Description

If `video_blank` is set `TRUE` video will be blanked out if the channel is changed or if playback is stopped. Otherwise, the last picture will be displayed. `play_state` indicates if the video is currently frozen, stopped, or being played back. The `stream_source` corresponds to the selected source for the video stream. It can come either from the demultiplexer or from memory. The `video_format` indicates the aspect ratio (one of 4:3 or 16:9) of the currently played video stream. Finally, `display_format` corresponds to the applied cropping mode in case the source video format is not the same as the format of the output device.

---

<a id="rst-video-still-picture"></a>

### video_still_picture

<a id="rst-synopsis-9"></a>

#### Synopsis



```c
struct video_still_picture {
char *iFrame;
int32_t size;
};
```

<a id="rst-variables-4"></a>

#### Variables


<table>
<tbody>
<tr>
<td>


`char *iFrame`

</td>
<td>


Pointer to a single iframe in memory.

</td>
</tr>
<tr>
<td>


`int32_t size`

</td>
<td>


Size of the iframe.

</td>
</tr>
</tbody>
</table>

<a id="rst-description-8"></a>

#### Description

An I-frame displayed via the [VIDEO_STILLPICTURE](<#rst-video-stillpicture>) call is passed on within this structure.

---

<a id="rst-video-capabilities"></a>

### video capabilities

<a id="rst-synopsis-10"></a>

#### Synopsis



```c
#define VIDEO_CAP_MPEG1   1
#define VIDEO_CAP_MPEG2   2
#define VIDEO_CAP_SYS     4
#define VIDEO_CAP_PROG    8
```

<a id="rst-constants-5"></a>

#### Constants

Bit definitions for capabilities:


<table>
<tbody>
<tr>
<td>


`VIDEO_CAP_MPEG1`

</td>
<td colspan="2">


 The hardware can decode MPEG1.

</td>
</tr>
<tr>
<td>


`VIDEO_CAP_MPEG2`

</td>
<td colspan="2">


The hardware can decode MPEG2.

</td>
</tr>
<tr>
<td>


`VIDEO_CAP_SYS`

</td>
<td colspan="2">


The video device accepts system stream.

You still have to open the video and the audio device but only send the stream to the video device.

</td>
</tr>
<tr>
<td>


`VIDEO_CAP_PROG`

</td>
<td colspan="2">


The video device accepts program stream.

You still have to open the video and the audio device but only send the stream to the video device.

</td>
</tr>
</tbody>
</table>

<a id="rst-description-9"></a>

#### Description

A call to [VIDEO_GET_CAPABILITIES](<#rst-video-get-capabilities>) returns an unsigned integer with the following bits set according to the hardware's capabilities.

---

<a id="rst-video-function-calls"></a>

## Video Function Calls

<a id="rst-video-stop"></a>

### VIDEO_STOP

<a id="rst-synopsis-11"></a>

#### Synopsis





<a id="c-VIDEO_STOP"></a>

```c
VIDEO_STOP
```



```c
int ioctl(fd, VIDEO_STOP, int mode)
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


 Equals `VIDEO_STOP` for this command.

</td>
</tr>
<tr>
<td rowspan="3">


 `int mode`

</td>
<td colspan="2">


 Indicates how the screen shall be handled.

</td>
</tr>
<tr>
<td>


TRUE  ( \!= 0 )

</td>
<td>


Blank screen when stop.

</td>
</tr>
<tr>
<td>


FALSE ( == 0 )

</td>
<td>


Show last decoded frame.

</td>
</tr>
</tbody>
</table>

<a id="rst-description-10"></a>

#### Description

> [!NOTE]
>
> Do **not** use in new drivers\! See: [General Notes](<~kernel/userspace/userspace-api/media-dvb/legacy-dvb-decoder-api#rst-legacy-dvb-decoder-notes>)

This ioctl is for Digital TV devices only. To control a V4L2 decoder use the V4L2 [ioctl VIDIOC_DECODER_CMD, VIDIOC_TRY_DECODER_CMD](<~kernel/userspace/userspace-api/media-v4l/vidioc-decoder-cmd#rst-vidioc-decoder-cmd>) instead.

This ioctl call asks the Video Device to stop playing the current stream. Depending on the input parameter, the screen can be blanked out or displaying the last decoded frame.

<a id="rst-return-value"></a>

#### Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

---

<a id="rst-video-play"></a>

### VIDEO_PLAY

<a id="rst-synopsis-12"></a>

#### Synopsis





<a id="c-VIDEO_PLAY"></a>

```c
VIDEO_PLAY
```



```c
int ioctl(fd, VIDEO_PLAY)
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


Equals `VIDEO_PLAY` for this command.

</td>
</tr>
</tbody>
</table>

<a id="rst-description-11"></a>

#### Description

> [!NOTE]
>
> Do **not** use in new drivers\! See: [General Notes](<~kernel/userspace/userspace-api/media-dvb/legacy-dvb-decoder-api#rst-legacy-dvb-decoder-notes>)

This ioctl is for Digital TV devices only. To control a V4L2 decoder use the V4L2 [ioctl VIDIOC_DECODER_CMD, VIDIOC_TRY_DECODER_CMD](<~kernel/userspace/userspace-api/media-v4l/vidioc-decoder-cmd#rst-vidioc-decoder-cmd>) instead.

This ioctl call asks the Video Device to start playing a video stream from the selected source.

<a id="rst-return-value-1"></a>

#### Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

---

<a id="rst-video-freeze"></a>

### VIDEO_FREEZE

<a id="rst-synopsis-13"></a>

#### Synopsis





<a id="c-VIDEO_FREEZE"></a>

```c
VIDEO_FREEZE
```



```c
int ioctl(fd, VIDEO_FREEZE)
```

<a id="rst-arguments-2"></a>

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


Equals `VIDEO_FREEZE` for this command.

</td>
</tr>
</tbody>
</table>

<a id="rst-description-12"></a>

#### Description

> [!NOTE]
>
> Do **not** use in new drivers\! See: [General Notes](<~kernel/userspace/userspace-api/media-dvb/legacy-dvb-decoder-api#rst-legacy-dvb-decoder-notes>)

This ioctl is for Digital TV devices only. To control a V4L2 decoder use the V4L2 [ioctl VIDIOC_DECODER_CMD, VIDIOC_TRY_DECODER_CMD](<~kernel/userspace/userspace-api/media-v4l/vidioc-decoder-cmd#rst-vidioc-decoder-cmd>) instead.

This ioctl call suspends the live video stream being played, if VIDEO_SOURCE_DEMUX is selected. Decoding and playing are frozen. It is then possible to restart the decoding and playing process of the video stream using the [VIDEO_CONTINUE](<#rst-video-continue>) command. If VIDEO_SOURCE_MEMORY is selected in the ioctl call [VIDEO_SELECT_SOURCE](<#rst-video-select-source>), the Digital TV subsystem will not decode any more data until the ioctl call [VIDEO_CONTINUE](<#rst-video-continue>) or [VIDEO_PLAY](<#rst-video-play>) is performed.

<a id="rst-return-value-2"></a>

#### Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

---

<a id="rst-video-continue"></a>

### VIDEO_CONTINUE

<a id="rst-synopsis-14"></a>

#### Synopsis





<a id="c-VIDEO_CONTINUE"></a>

```c
VIDEO_CONTINUE
```



```c
int ioctl(fd, VIDEO_CONTINUE)
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


 File descriptor returned by a previous call to [open()](<#rst-open>).

</td>
</tr>
<tr>
<td>


`int request`

</td>
<td colspan="2">


Equals `VIDEO_CONTINUE` for this command.

</td>
</tr>
</tbody>
</table>

<a id="rst-description-13"></a>

#### Description

> [!NOTE]
>
> Do **not** use in new drivers\! See: [General Notes](<~kernel/userspace/userspace-api/media-dvb/legacy-dvb-decoder-api#rst-legacy-dvb-decoder-notes>)

This ioctl is for Digital TV devices only. To control a V4L2 decoder use the V4L2 [ioctl VIDIOC_DECODER_CMD, VIDIOC_TRY_DECODER_CMD](<~kernel/userspace/userspace-api/media-v4l/vidioc-decoder-cmd#rst-vidioc-decoder-cmd>) instead.

This ioctl call restarts decoding and playing processes of the video stream which was played before a call to [VIDEO_FREEZE](<#rst-video-freeze>) was made.

<a id="rst-return-value-3"></a>

#### Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

---

<a id="rst-video-select-source"></a>

### VIDEO_SELECT_SOURCE

<a id="rst-synopsis-15"></a>

#### Synopsis





<a id="c-VIDEO_SELECT_SOURCE"></a>

```c
VIDEO_SELECT_SOURCE
```



```c
int ioctl(fd, VIDEO_SELECT_SOURCE, video_stream_source_t source)
```

<a id="rst-arguments-4"></a>

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


Equals `VIDEO_SELECT_SOURCE` for this command.

</td>
</tr>
<tr>
<td>


[video_stream_source_t](<#rst-video-stream-source-t>) `source`

</td>
<td colspan="2">


Indicates which source shall be used for the Video stream.

</td>
</tr>
</tbody>
</table>

<a id="rst-description-14"></a>

#### Description

> [!NOTE]
>
> Do **not** use in new drivers\! See: [General Notes](<~kernel/userspace/userspace-api/media-dvb/legacy-dvb-decoder-api#rst-legacy-dvb-decoder-notes>)

This ioctl is for Digital TV devices only. This ioctl was also supported by the V4L2 ivtv driver, but that has been replaced by the ivtv-specific `IVTV_IOC_PASSTHROUGH_MODE` ioctl.

This ioctl call informs the video device which source shall be used for the input data. The possible sources are demux or memory. If memory is selected, the data is fed to the video device through the write command using the struct [video_stream_source_t](<#rst-video-stream-source-t>). If demux is selected, the data is directly transferred from the onboard demux-device to the decoder.

The data fed to the decoder is also controlled by the PID-filter. Output selection: `dmx_output` `DMX_OUT_DECODER`.

<a id="rst-return-value-4"></a>

#### Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

---

<a id="rst-video-set-blank"></a>

### VIDEO_SET_BLANK

<a id="rst-synopsis-16"></a>

#### Synopsis





<a id="c-VIDEO_SET_BLANK"></a>

```c
VIDEO_SET_BLANK
```



```c
int ioctl(fd, VIDEO_SET_BLANK, int mode)
```

<a id="rst-arguments-5"></a>

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


 Equals `VIDEO_SET_BLANK` for this command.

</td>
</tr>
<tr>
<td rowspan="3">


 `int mode`

</td>
<td colspan="2">


 Indicates if the screen shall be blanked.

</td>
</tr>
<tr>
<td>


TRUE  ( \!= 0 )

</td>
<td>


Blank screen when stop.

</td>
</tr>
<tr>
<td>


FALSE ( == 0 )

</td>
<td>


Show last decoded frame.

</td>
</tr>
</tbody>
</table>

<a id="rst-description-15"></a>

#### Description

> [!NOTE]
>
> Do **not** use in new drivers\! See: [General Notes](<~kernel/userspace/userspace-api/media-dvb/legacy-dvb-decoder-api#rst-legacy-dvb-decoder-notes>)

This ioctl call asks the Video Device to blank out the picture.

<a id="rst-return-value-5"></a>

#### Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

---

<a id="rst-video-get-status"></a>

### VIDEO_GET_STATUS

<a id="rst-synopsis-17"></a>

#### Synopsis





<a id="c-VIDEO_GET_STATUS"></a>

```c
VIDEO_GET_STATUS
```



```c
int ioctl(fd, int request = VIDEO_GET_STATUS,
struct video_status *status)
```

<a id="rst-arguments-6"></a>

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


Equals `VIDEO_GET_STATUS` for this command.

</td>
</tr>
<tr>
<td>


`struct` [video_status](<#rst-video-status>) `*status`

</td>
<td colspan="2">


Returns the current status of the Video Device.

</td>
</tr>
</tbody>
</table>

<a id="rst-description-16"></a>

#### Description

> [!NOTE]
>
> Do **not** use in new drivers\! See: [General Notes](<~kernel/userspace/userspace-api/media-dvb/legacy-dvb-decoder-api#rst-legacy-dvb-decoder-notes>)

This ioctl call asks the Video Device to return the current status of the device.

<a id="rst-return-value-6"></a>

#### Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

---

<a id="rst-video-get-event"></a>

### VIDEO_GET_EVENT

<a id="rst-synopsis-18"></a>

#### Synopsis





<a id="c-VIDEO_GET_EVENT"></a>

```c
VIDEO_GET_EVENT
```



```c
int ioctl(fd, int request = VIDEO_GET_EVENT,
struct video_event *ev)
```

<a id="rst-arguments-7"></a>

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


Equals `VIDEO_GET_EVENT` for this command.

</td>
</tr>
<tr>
<td>


`struct` [video_event](<#rst-video-event>) `*ev`

</td>
<td colspan="2">


Points to the location where the event, if any, is to be stored.

</td>
</tr>
</tbody>
</table>

<a id="rst-description-17"></a>

#### Description

> [!NOTE]
>
> Do **not** use in new drivers\! See: [General Notes](<~kernel/userspace/userspace-api/media-dvb/legacy-dvb-decoder-api#rst-legacy-dvb-decoder-notes>)

This ioctl is for DVB devices only. To get events from a V4L2 decoder use the V4L2 [ioctl VIDIOC_DQEVENT](<~kernel/userspace/userspace-api/media-v4l/vidioc-dqevent#rst-vidioc-dqevent>) ioctl instead.

This ioctl call returns an event of type [video_event](<#rst-video-event>) if available. A certain number of the latest events will be cued and returned in order of occurrence. Older events may be discarded if not fetched in time. If an event is not available, the behavior depends on whether the device is in blocking or non-blocking mode. In the latter case, the call fails immediately with errno set to `EWOULDBLOCK`. In the former case, the call blocks until an event becomes available. The standard Linux poll() and/or select() system calls can be used with the device file descriptor to watch for new events. For select(), the file descriptor should be included in the exceptfds argument, and for poll(), POLLPRI should be specified as the wake-up condition. Read-only permissions are sufficient for this ioctl call.

<a id="rst-return-value-7"></a>

#### Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.


<table>
<tbody>
<tr>
<td>


`EWOULDBLOCK`

</td>
<td colspan="2">


 There is no event pending, and the device is in non-blocking mode.

</td>
</tr>
<tr>
<td>


`EOVERFLOW`

</td>
<td colspan="2">


Overflow in event queue - one or more events were lost.

</td>
</tr>
</tbody>
</table>

---

<a id="rst-video-set-display-format"></a>

### VIDEO_SET_DISPLAY_FORMAT

<a id="rst-synopsis-19"></a>

#### Synopsis





<a id="c-VIDEO_SET_DISPLAY_FORMAT"></a>

```c
VIDEO_SET_DISPLAY_FORMAT
```



```c
int ioctl(fd, int request = VIDEO_SET_DISPLAY_FORMAT,
video_display_format_t format)
```

<a id="rst-arguments-8"></a>

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


Equals `VIDEO_SET_DISPLAY_FORMAT` for this command.

</td>
</tr>
<tr>
<td>


[video_displayformat_t](<#rst-video-displayformat-t>) `format`

</td>
<td colspan="2">


Selects the video format to be used.

</td>
</tr>
</tbody>
</table>

<a id="rst-description-18"></a>

#### Description

> [!NOTE]
>
> Do **not** use in new drivers\! See: [General Notes](<~kernel/userspace/userspace-api/media-dvb/legacy-dvb-decoder-api#rst-legacy-dvb-decoder-notes>)

This ioctl call asks the Video Device to select the video format to be applied by the MPEG chip on the video.

<a id="rst-return-value-8"></a>

#### Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

---

<a id="rst-video-stillpicture"></a>

### VIDEO_STILLPICTURE

<a id="rst-synopsis-20"></a>

#### Synopsis





<a id="c-VIDEO_STILLPICTURE"></a>

```c
VIDEO_STILLPICTURE
```



```c
int ioctl(fd, int request = VIDEO_STILLPICTURE,
struct video_still_picture *sp)
```

<a id="rst-arguments-9"></a>

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


Equals `VIDEO_STILLPICTURE` for this command.

</td>
</tr>
<tr>
<td>


`struct` [video_still_picture](<#rst-video-still-picture>) `*sp`

</td>
<td colspan="2">


Pointer to the location where the struct with the I-frame and size is stored.

</td>
</tr>
</tbody>
</table>

<a id="rst-description-19"></a>

#### Description

> [!NOTE]
>
> Do **not** use in new drivers\! See: [General Notes](<~kernel/userspace/userspace-api/media-dvb/legacy-dvb-decoder-api#rst-legacy-dvb-decoder-notes>)

This ioctl call asks the Video Device to display a still picture (I-frame). The input data shall be the section of an elementary video stream containing an I-frame. Typically this section is extracted from a TS or PES recording. Resolution and codec (see [video capabilities](<#rst-video-capabilities>)) must be supported by the device. If the pointer is NULL, then the current displayed still picture is blanked.

e.g. The AV7110 supports MPEG1 and MPEG2 with the common PAL-SD resolutions.

<a id="rst-return-value-9"></a>

#### Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

---

<a id="rst-video-fast-forward"></a>

### VIDEO_FAST_FORWARD

<a id="rst-synopsis-21"></a>

#### Synopsis





<a id="c-VIDEO_FAST_FORWARD"></a>

```c
VIDEO_FAST_FORWARD
```



```c
int ioctl(fd, int request = VIDEO_FAST_FORWARD, int nFrames)
```

<a id="rst-arguments-10"></a>

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


Equals `VIDEO_FAST_FORWARD` for this command.

</td>
</tr>
<tr>
<td>


`int nFrames`

</td>
<td colspan="2">


The number of frames to skip.

</td>
</tr>
</tbody>
</table>

<a id="rst-description-20"></a>

#### Description

> [!NOTE]
>
> Do **not** use in new drivers\! See: [General Notes](<~kernel/userspace/userspace-api/media-dvb/legacy-dvb-decoder-api#rst-legacy-dvb-decoder-notes>)

This ioctl call asks the Video Device to skip decoding of N number of I-frames. This call can only be used if `VIDEO_SOURCE_MEMORY` is selected.

<a id="rst-return-value-10"></a>

#### Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.


<table>
<tbody>
<tr>
<td>


`EPERM`

</td>
<td>


Mode `VIDEO_SOURCE_MEMORY` not selected.

</td>
</tr>
</tbody>
</table>

---

<a id="rst-video-slowmotion"></a>

### VIDEO_SLOWMOTION

<a id="rst-synopsis-22"></a>

#### Synopsis





<a id="c-VIDEO_SLOWMOTION"></a>

```c
VIDEO_SLOWMOTION
```



```c
int ioctl(fd, int request = VIDEO_SLOWMOTION, int nFrames)
```

<a id="rst-arguments-11"></a>

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


Equals `VIDEO_SLOWMOTION` for this command.

</td>
</tr>
<tr>
<td>


`int nFrames`

</td>
<td colspan="2">


The number of times to repeat each frame.

</td>
</tr>
</tbody>
</table>

<a id="rst-description-21"></a>

#### Description

> [!NOTE]
>
> Do **not** use in new drivers\! See: [General Notes](<~kernel/userspace/userspace-api/media-dvb/legacy-dvb-decoder-api#rst-legacy-dvb-decoder-notes>)

This ioctl call asks the video device to repeat decoding frames N number of times. This call can only be used if `VIDEO_SOURCE_MEMORY` is selected.

<a id="rst-return-value-11"></a>

#### Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.


<table>
<tbody>
<tr>
<td>


`EPERM`

</td>
<td>


Mode `VIDEO_SOURCE_MEMORY` not selected.

</td>
</tr>
</tbody>
</table>

---

<a id="rst-video-get-capabilities"></a>

### VIDEO_GET_CAPABILITIES

<a id="rst-synopsis-23"></a>

#### Synopsis





<a id="c-VIDEO_GET_CAPABILITIES"></a>

```c
VIDEO_GET_CAPABILITIES
```



```c
int ioctl(fd, int request = VIDEO_GET_CAPABILITIES, unsigned int *cap)
```

<a id="rst-arguments-12"></a>

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


Equals `VIDEO_GET_CAPABILITIES` for this command.

</td>
</tr>
<tr>
<td>


`unsigned int *cap`

</td>
<td colspan="2">


Pointer to a location where to store the capability information.

</td>
</tr>
</tbody>
</table>

<a id="rst-description-22"></a>

#### Description

> [!NOTE]
>
> Do **not** use in new drivers\! See: [General Notes](<~kernel/userspace/userspace-api/media-dvb/legacy-dvb-decoder-api#rst-legacy-dvb-decoder-notes>)

This ioctl call asks the video device about its decoding capabilities. On success it returns an integer which has bits set according to the defines in [video capabilities](<#rst-video-capabilities>).

<a id="rst-return-value-12"></a>

#### Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

---

<a id="rst-video-clear-buffer"></a>

### VIDEO_CLEAR_BUFFER

<a id="rst-synopsis-24"></a>

#### Synopsis





<a id="c-VIDEO_CLEAR_BUFFER"></a>

```c
VIDEO_CLEAR_BUFFER
```



```c
int ioctl(fd, int request = VIDEO_CLEAR_BUFFER)
```

<a id="rst-arguments-13"></a>

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


Equals `VIDEO_CLEAR_BUFFER` for this command.

</td>
</tr>
</tbody>
</table>

<a id="rst-description-23"></a>

#### Description

> [!NOTE]
>
> Do **not** use in new drivers\! See: [General Notes](<~kernel/userspace/userspace-api/media-dvb/legacy-dvb-decoder-api#rst-legacy-dvb-decoder-notes>)

This ioctl call clears all video buffers in the driver and in the decoder hardware.

<a id="rst-return-value-13"></a>

#### Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

---

<a id="rst-video-set-streamtype"></a>

### VIDEO_SET_STREAMTYPE

<a id="rst-synopsis-25"></a>

#### Synopsis





<a id="c-VIDEO_SET_STREAMTYPE"></a>

```c
VIDEO_SET_STREAMTYPE
```



```c
int ioctl(fd, int request = VIDEO_SET_STREAMTYPE, int type)
```

<a id="rst-arguments-14"></a>

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


Equals `VIDEO_SET_STREAMTYPE` for this command.

</td>
</tr>
<tr>
<td>


`int type`

</td>
<td colspan="2">


Stream type.

</td>
</tr>
</tbody>
</table>

<a id="rst-description-24"></a>

#### Description

> [!NOTE]
>
> Do **not** use in new drivers\! See: [General Notes](<~kernel/userspace/userspace-api/media-dvb/legacy-dvb-decoder-api#rst-legacy-dvb-decoder-notes>)

This ioctl tells the driver which kind of stream to expect being written to it. Intelligent decoder might also not support or ignore (like the AV7110) this call and determine the stream type themselves.

Currently used stream types:


<table>
<thead>
<tr>
<th>


Codec

</th>
<th>


Stream type

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


MPEG2

</td>
<td>


0

</td>
</tr>
<tr>
<td>


MPEG4 h.264

</td>
<td>


1

</td>
</tr>
<tr>
<td>


VC1

</td>
<td>


3

</td>
</tr>
<tr>
<td>


MPEG4 Part2

</td>
<td>


4

</td>
</tr>
<tr>
<td>


VC1 SM

</td>
<td>


5

</td>
</tr>
<tr>
<td>


MPEG1

</td>
<td>


6

</td>
</tr>
<tr>
<td>


HEVC h.265

</td>
<td>


7  
DREAMBOX: 22

</td>
</tr>
<tr>
<td>


AVS

</td>
<td>


16

</td>
</tr>
<tr>
<td>


AVS2

</td>
<td>


40

</td>
</tr>
</tbody>
</table>

Not every decoder supports all stream types.

<a id="rst-return-value-14"></a>

#### Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

---

<a id="rst-video-set-format"></a>

### VIDEO_SET_FORMAT

<a id="rst-synopsis-26"></a>

#### Synopsis





<a id="c-VIDEO_SET_FORMAT"></a>

```c
VIDEO_SET_FORMAT
```



```c
int ioctl(fd, int request = VIDEO_SET_FORMAT, video_format_t format)
```

<a id="rst-arguments-15"></a>

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


Equals `VIDEO_SET_FORMAT` for this command.

</td>
</tr>
<tr>
<td>


[video_format_t](<#rst-video-format-t>) `format`

</td>
<td colspan="2">


Video format of TV as defined in section [video_format_t](<#rst-video-format-t>).

</td>
</tr>
</tbody>
</table>

<a id="rst-description-25"></a>

#### Description

> [!NOTE]
>
> Do **not** use in new drivers\! See: [General Notes](<~kernel/userspace/userspace-api/media-dvb/legacy-dvb-decoder-api#rst-legacy-dvb-decoder-notes>)

This ioctl sets the screen format (aspect ratio) of the connected output device (TV) so that the output of the decoder can be adjusted accordingly.

<a id="rst-return-value-15"></a>

#### Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

---

<a id="rst-video-get-size"></a>

### VIDEO_GET_SIZE

<a id="rst-synopsis-27"></a>

#### Synopsis





<a id="c-VIDEO_GET_SIZE"></a>

```c
VIDEO_GET_SIZE
```



```c
int ioctl(int fd, int request = VIDEO_GET_SIZE, video_size_t *size)
```

<a id="rst-arguments-16"></a>

#### Arguments


<table>
<tbody>
<tr>
<td>


`int fd`

</td>
<td colspan="2">


 File descriptor returned by a previous call, to [open()](<#rst-open>).

</td>
</tr>
<tr>
<td>


`int request`

</td>
<td colspan="2">


Equals `VIDEO_GET_SIZE` for this command.

</td>
</tr>
<tr>
<td>


[video_size_t](<#rst-video-size-t>) `*size`

</td>
<td colspan="2">


Returns the size and aspect ratio.

</td>
</tr>
</tbody>
</table>

<a id="rst-description-26"></a>

#### Description

> [!NOTE]
>
> Do **not** use in new drivers\! See: [General Notes](<~kernel/userspace/userspace-api/media-dvb/legacy-dvb-decoder-api#rst-legacy-dvb-decoder-notes>)

This ioctl returns the size and aspect ratio.

<a id="rst-return-value-16"></a>

#### Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

---

<a id="rst-video-get-pts"></a>

### VIDEO_GET_PTS

<a id="rst-synopsis-28"></a>

#### Synopsis





<a id="c-VIDEO_GET_PTS"></a>

```c
VIDEO_GET_PTS
```



```c
int ioctl(int fd, int request = VIDEO_GET_PTS, __u64 *pts)
```

<a id="rst-arguments-17"></a>

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


Equals `VIDEO_GET_PTS` for this command.

</td>
</tr>
<tr>
<td>


`__u64 *pts`

</td>
<td colspan="2">


Returns the 33-bit timestamp as defined in ITU T-REC-H.222.0 / ISO/IEC 13818-1.

The PTS should belong to the currently played frame if possible, but may also be a value close to it like the PTS of the last decoded frame or the last PTS extracted by the PES parser.

</td>
</tr>
</tbody>
</table>

<a id="rst-description-27"></a>

#### Description

> [!NOTE]
>
> Do **not** use in new drivers\! See: [General Notes](<~kernel/userspace/userspace-api/media-dvb/legacy-dvb-decoder-api#rst-legacy-dvb-decoder-notes>)

For V4L2 decoders this ioctl has been replaced by the `V4L2_CID_MPEG_VIDEO_DEC_PTS` control.

This ioctl call asks the Video Device to return the current PTS timestamp.

<a id="rst-return-value-17"></a>

#### Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

---

<a id="rst-video-get-frame-count"></a>

### VIDEO_GET_FRAME_COUNT

<a id="rst-synopsis-29"></a>

#### Synopsis





<a id="c-VIDEO_GET_FRAME_COUNT"></a>

```c
VIDEO_GET_FRAME_COUNT
```



```c
int ioctl(int fd, VIDEO_GET_FRAME_COUNT, __u64 *pts)
```

<a id="rst-arguments-18"></a>

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


Equals `VIDEO_GET_FRAME_COUNT` for this command.

</td>
</tr>
<tr>
<td>


`__u64 *pts`

</td>
<td colspan="2">


Returns the number of frames displayed since the decoder was started.

</td>
</tr>
</tbody>
</table>

<a id="rst-description-28"></a>

#### Description

> [!NOTE]
>
> Do **not** use in new drivers\! See: [General Notes](<~kernel/userspace/userspace-api/media-dvb/legacy-dvb-decoder-api#rst-legacy-dvb-decoder-notes>)

For V4L2 decoders this ioctl has been replaced by the `V4L2_CID_MPEG_VIDEO_DEC_FRAME` control.

This ioctl call asks the Video Device to return the number of displayed frames since the decoder was started.

<a id="rst-return-value-18"></a>

#### Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

---

<a id="rst-video-command"></a>

### VIDEO_COMMAND

<a id="rst-synopsis-30"></a>

#### Synopsis





<a id="c-VIDEO_COMMAND"></a>

```c
VIDEO_COMMAND
```



```c
int ioctl(int fd, int request = VIDEO_COMMAND,
struct video_command *cmd)
```

<a id="rst-arguments-19"></a>

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


Equals `VIDEO_COMMAND` for this command.

</td>
</tr>
<tr>
<td>


[struct video_command](<#rst-struct-video-command>) `*cmd`

</td>
<td colspan="2">


Commands the decoder.

</td>
</tr>
</tbody>
</table>

<a id="rst-description-29"></a>

#### Description

> [!NOTE]
>
> Do **not** use in new drivers\! See: [General Notes](<~kernel/userspace/userspace-api/media-dvb/legacy-dvb-decoder-api#rst-legacy-dvb-decoder-notes>)

For V4L2 decoders this ioctl has been replaced by the [ioctl VIDIOC_DECODER_CMD, VIDIOC_TRY_DECODER_CMD](<~kernel/userspace/userspace-api/media-v4l/vidioc-decoder-cmd#rst-vidioc-decoder-cmd>) ioctl.

This ioctl commands the decoder. The [struct video_command](<#rst-struct-video-command>) is a subset of the `v4l2_decoder_cmd` struct, so refer to the [ioctl VIDIOC_DECODER_CMD, VIDIOC_TRY_DECODER_CMD](<~kernel/userspace/userspace-api/media-v4l/vidioc-decoder-cmd#rst-vidioc-decoder-cmd>) documentation for more information.

<a id="rst-return-value-19"></a>

#### Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

---

<a id="rst-video-try-command"></a>

### VIDEO_TRY_COMMAND

<a id="rst-synopsis-31"></a>

#### Synopsis





<a id="c-VIDEO_TRY_COMMAND"></a>

```c
VIDEO_TRY_COMMAND
```



```c
int ioctl(int fd, int request = VIDEO_TRY_COMMAND,
struct video_command *cmd)
```

<a id="rst-arguments-20"></a>

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


Equals `VIDEO_TRY_COMMAND` for this command.

</td>
</tr>
<tr>
<td>


[struct video_command](<#rst-struct-video-command>) `*cmd`

</td>
<td colspan="2">


Try a decoder command.

</td>
</tr>
</tbody>
</table>

<a id="rst-description-30"></a>

#### Description

> [!NOTE]
>
> Do **not** use in new drivers\! See: [General Notes](<~kernel/userspace/userspace-api/media-dvb/legacy-dvb-decoder-api#rst-legacy-dvb-decoder-notes>)

For V4L2 decoders this ioctl has been replaced by the [VIDIOC_TRY_DECODER_CMD](<~kernel/userspace/userspace-api/media-v4l/vidioc-decoder-cmd#rst-vidioc-decoder-cmd>) ioctl.

This ioctl tries a decoder command. The [struct video_command](<#rst-struct-video-command>) is a subset of the `v4l2_decoder_cmd` struct, so refer to the [VIDIOC_TRY_DECODER_CMD](<~kernel/userspace/userspace-api/media-v4l/vidioc-decoder-cmd#rst-vidioc-decoder-cmd>) documentation for more information.

<a id="rst-return-value-20"></a>

#### Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

---

<a id="rst-open"></a>

### open()

<a id="rst-synopsis-32"></a>

#### Synopsis



```c
#include <fcntl.h>
```





<a id="c-open"></a>

```c
int open(const char *deviceName, int flags)
```

<a id="rst-arguments-21"></a>

#### Arguments


<table>
<tbody>
<tr>
<td>


`const char *deviceName`

</td>
<td colspan="2">


Name of specific video device.

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

<a id="rst-description-31"></a>

#### Description

This system call opens a named video device (e.g. /dev/dvb/adapter?/video?) for subsequent use.

When an open() call has succeeded, the device will be ready for use. The significance of blocking or non-blocking mode is described in the documentation for functions where there is a difference. It does not affect the semantics of the open() call itself. A device opened in blocking mode can later be put into non-blocking mode (and vice versa) using the F_SETFL command of the fcntl system call. This is a standard system call, documented in the Linux manual page for fcntl. Only one user can open the Video Device in O_RDWR mode. All other attempts to open the device in this mode will fail, and an error-code will be returned. If the Video Device is opened in O_RDONLY mode, the only ioctl call that can be used is [VIDEO_GET_STATUS](<#rst-video-get-status>). All other call will return an error code.

<a id="rst-return-value-21"></a>

#### Return Value


<table>
<tbody>
<tr>
<td>


`ENODEV`

</td>
<td colspan="2">


 Device driver not loaded/available.

</td>
</tr>
<tr>
<td>


`EINTERNAL`

</td>
<td colspan="2">


Internal error.

</td>
</tr>
<tr>
<td>


`EBUSY`

</td>
<td colspan="2">


Device or resource busy.

</td>
</tr>
<tr>
<td>


`EINVAL`

</td>
<td colspan="2">


Invalid argument.

</td>
</tr>
</tbody>
</table>

---

<a id="rst-close"></a>

### close()

<a id="rst-synopsis-33"></a>

#### Synopsis





<a id="c-close"></a>

```c
int close(int fd)
```

<a id="rst-arguments-22"></a>

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
</tbody>
</table>

<a id="rst-description-32"></a>

#### Description

This system call closes a previously opened video device.

<a id="rst-return-value-22"></a>

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

---

<a id="rst-write"></a>

### write()

<a id="rst-synopsis-34"></a>

#### Synopsis





<a id="c-write"></a>

```c
size_t write(int fd, const void *buf, size_t count)
```

<a id="rst-arguments-23"></a>

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


`void *buf`

</td>
<td colspan="2">


Pointer to the buffer containing the PES data.

</td>
</tr>
<tr>
<td>


`size_t count`

</td>
<td colspan="2">


Size of buf.

</td>
</tr>
</tbody>
</table>

<a id="rst-description-33"></a>

#### Description

This system call can only be used if VIDEO_SOURCE_MEMORY is selected in the ioctl call [VIDEO_SELECT_SOURCE](<#rst-video-select-source>). The data provided shall be in PES format, unless the capability allows other formats. TS is the most common format for storing DVB-data, it is usually supported too. If O_NONBLOCK is not specified the function will block until buffer space is available. The amount of data to be transferred is implied by count.

> [!NOTE]
>
> See: [DVB Data Formats](<~kernel/userspace/userspace-api/media-dvb/legacy-dvb-decoder-api#rst-legacy-dvb-decoder-formats>)

<a id="rst-return-value-23"></a>

#### Return Value


<table>
<tbody>
<tr>
<td>


`EPERM`

</td>
<td colspan="2">


 Mode `VIDEO_SOURCE_MEMORY` not selected.

</td>
</tr>
<tr>
<td>


`ENOMEM`

</td>
<td colspan="2">


Attempted to write more data than the internal buffer can hold.

</td>
</tr>
<tr>
<td>


`EBADF`

</td>
<td colspan="2">


fd is not a valid open file descriptor.

</td>
</tr>
</tbody>
</table>
