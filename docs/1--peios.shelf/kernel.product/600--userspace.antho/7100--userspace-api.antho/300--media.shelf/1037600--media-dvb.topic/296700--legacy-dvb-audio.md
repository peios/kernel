---
title: "DVB Audio Device"
type: reference
description: "The DVB audio device controls the MPEG2 audio decoder of the DVB hardware. It can be accessed through /dev/dvb/adapter?/audio?. Data types and ioctl definitions can be accessed by including linux/dvb/audio.h in your application."
---

<a id="rst-dvb-audio-device"></a>
<a id="rst-dvb-audio"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later OR GPL-2.0 -->

<!-- c:namespace: dtv.legacy.audio -->

> [!NOTE]
>
> Do **not** use in new drivers\! See: [General Notes](<~kernel/userspace/userspace-api/media-dvb/legacy-dvb-decoder-api#rst-legacy-dvb-decoder-notes>)

The DVB audio device controls the MPEG2 audio decoder of the DVB hardware. It can be accessed through `/dev/dvb/adapter?/audio?`. Data types and ioctl definitions can be accessed by including `linux/dvb/audio.h` in your application.

Please note that most DVB cards don’t have their own MPEG decoder, which results in the omission of the audio and video device.

These ioctls were also used by V4L2 to control MPEG decoders implemented in V4L2. The use of these ioctls for that purpose has been made obsolete and proper V4L2 ioctls or controls have been created to replace that functionality. Use [V4L2 ioctls](<~kernel/userspace/userspace-api/media-v4l/audio#rst-audio>) for new drivers\!

<a id="rst-audio-data-types"></a>

## Audio Data Types

This section describes the structures, data types and defines used when talking to the audio device.

---

<a id="rst-audio-stream-source-t"></a>

### audio_stream_source_t

<a id="rst-synopsis"></a>

#### Synopsis





<a id="c-enum-audio_stream_source_t"></a>

```c
audio_stream_source_t
```



```c
typedef enum {
AUDIO_SOURCE_DEMUX,
AUDIO_SOURCE_MEMORY
} audio_stream_source_t;
```

<a id="rst-constants"></a>

#### Constants


<table>
<tbody>
<tr>
<td>


`AUDIO_SOURCE_DEMUX`

</td>
<td colspan="2">


 Selects the demultiplexer (fed either by the frontend or the DVR device) as the source of the video stream.

</td>
</tr>
<tr>
<td>


`AUDIO_SOURCE_MEMORY`

</td>
<td colspan="2">


Selects the stream from the application that comes through the [write()](<#rst-write>) system call.

</td>
</tr>
</tbody>
</table>

<a id="rst-description"></a>

#### Description

The audio stream source is set through the [AUDIO_SELECT_SOURCE](<#rst-audio-select-source>) call and can take the following values, depending on whether we are replaying from an internal (demux) or external (user write) source.

The data fed to the decoder is also controlled by the PID-filter. Output selection: `dmx_output` `DMX_OUT_DECODER`.

---

<a id="rst-audio-play-state-t"></a>

### audio_play_state_t

<a id="rst-synopsis-1"></a>

#### Synopsis





<a id="c-enum-audio_play_state_t"></a>

```c
audio_play_state_t
```



```c
typedef enum {
    AUDIO_STOPPED,
    AUDIO_PLAYING,
    AUDIO_PAUSED
} audio_play_state_t;
```

<a id="rst-constants-1"></a>

#### Constants


<table>
<tbody>
<tr>
<td>


`AUDIO_STOPPED`

</td>
<td>


Audio is stopped.

</td>
</tr>
<tr>
<td>


`AUDIO_PLAYING`

</td>
<td>


Audio is currently playing.

</td>
</tr>
<tr>
<td>


`AUDIO_PAUSE`

</td>
<td>


Audio is frozen.

</td>
</tr>
</tbody>
</table>

<a id="rst-description-1"></a>

#### Description

This values can be returned by the [AUDIO_GET_STATUS](<#rst-audio-get-status>) call representing the state of audio playback.

---

<a id="rst-audio-channel-select-t"></a>

### audio_channel_select_t

<a id="rst-synopsis-2"></a>

#### Synopsis





<a id="c-enum-audio_channel_select_t"></a>

```c
audio_channel_select_t
```



```c
typedef enum {
    AUDIO_STEREO,
    AUDIO_MONO_LEFT,
    AUDIO_MONO_RIGHT,
    AUDIO_MONO,
    AUDIO_STEREO_SWAPPED
} audio_channel_select_t;
```

<a id="rst-constants-2"></a>

#### Constants


<table>
<tbody>
<tr>
<td>


`AUDIO_STEREO`

</td>
<td>


Stereo.

</td>
</tr>
<tr>
<td>


`AUDIO_MONO_LEFT`

</td>
<td>


Mono, select left stereo channel as source.

</td>
</tr>
<tr>
<td>


`AUDIO_MONO_RIGHT`

</td>
<td>


Mono, select right stereo channel as source.

</td>
</tr>
<tr>
<td>


`AUDIO_MONO`

</td>
<td>


Mono source only.

</td>
</tr>
<tr>
<td>


`AUDIO_STEREO_SWAPPED`

</td>
<td>


Stereo, swap L &amp; R.

</td>
</tr>
</tbody>
</table>

<a id="rst-description-2"></a>

#### Description

The audio channel selected via [AUDIO_CHANNEL_SELECT](<#rst-audio-channel-select>) is determined by this value.

---

<a id="rst-audio-mixer-t"></a>

### audio_mixer_t

<a id="rst-synopsis-3"></a>

#### Synopsis





<a id="c-struct-audio_mixer"></a>

```c
audio_mixer
```



```c
typedef struct audio_mixer {
    unsigned int volume_left;
    unsigned int volume_right;
} audio_mixer_t;
```

<a id="rst-variables"></a>

#### Variables


<table>
<tbody>
<tr>
<td>


`unsigned int volume_left`

</td>
<td>


Volume left channel. Valid range: 0 ... 255

</td>
</tr>
<tr>
<td>


`unsigned int volume_right`

</td>
<td>


Volume right channel. Valid range: 0 ... 255

</td>
</tr>
</tbody>
</table>

<a id="rst-description-3"></a>

#### Description

This structure is used by the [AUDIO_SET_MIXER](<#rst-audio-set-mixer>) call to set the audio volume.

---

<a id="rst-audio-status"></a>

### audio_status

<a id="rst-synopsis-4"></a>

#### Synopsis





<a id="c-struct-audio_status"></a>

```c
audio_status
```



```c
typedef struct audio_status {
    int AV_sync_state;
    int mute_state;
    audio_play_state_t play_state;
    audio_stream_source_t stream_source;
    audio_channel_select_t channel_select;
    int bypass_mode;
    audio_mixer_t mixer_state;
} audio_status_t;
```

<a id="rst-variables-1"></a>

#### Variables


<table>
<tbody>
<tr>
<td rowspan="3">


 `int AV_sync_state`

</td>
<td colspan="2">


 Shows if A/V synchronization is ON or OFF.

</td>
</tr>
<tr>
<td>


TRUE  ( \!= 0 )

</td>
<td>


AV-sync ON.

</td>
</tr>
<tr>
<td>


FALSE ( == 0 )

</td>
<td>


AV-sync OFF.

</td>
</tr>
<tr>
<td rowspan="3">


 `int mute_state`

</td>
<td colspan="2">


 Indicates if audio is muted or not.

</td>
</tr>
<tr>
<td>


TRUE  ( \!= 0 )

</td>
<td>


mute audio

</td>
</tr>
<tr>
<td>


FALSE ( == 0 )

</td>
<td>


unmute audio

</td>
</tr>
<tr>
<td>


[audio_play_state_t](<#rst-audio-play-state-t>) `play_state`

</td>
<td colspan="2">


Current playback state.

</td>
</tr>
<tr>
<td>


[audio_stream_source_t](<#rst-audio-stream-source-t>) `stream_source`

</td>
<td colspan="2">


Current source of the data.

</td>
</tr>
<tr>
<td rowspan="3">


 `int bypass_mode`

</td>
<td colspan="2">


 Is the decoding of the current Audio stream in the DVB subsystem enabled or disabled.

</td>
</tr>
<tr>
<td>


TRUE  ( \!= 0 )

</td>
<td>


Bypass disabled.

</td>
</tr>
<tr>
<td>


FALSE ( == 0 )

</td>
<td>


Bypass enabled.

</td>
</tr>
<tr>
<td>


[audio_mixer_t](<#rst-audio-mixer-t>) `mixer_state`

</td>
<td colspan="2">


Current volume settings.

</td>
</tr>
</tbody>
</table>

<a id="rst-description-4"></a>

#### Description

The [AUDIO_GET_STATUS](<#rst-audio-get-status>) call returns this structure as information about various states of the playback operation.

---

<a id="rst-audio-encodings"></a>

### audio encodings

<a id="rst-synopsis-5"></a>

#### Synopsis



```c
#define AUDIO_CAP_DTS    1
#define AUDIO_CAP_LPCM   2
#define AUDIO_CAP_MP1    4
#define AUDIO_CAP_MP2    8
#define AUDIO_CAP_MP3   16
#define AUDIO_CAP_AAC   32
#define AUDIO_CAP_OGG   64
#define AUDIO_CAP_SDDS 128
#define AUDIO_CAP_AC3  256
```

<a id="rst-constants-3"></a>

#### Constants


<table>
<tbody>
<tr>
<td>


`AUDIO_CAP_DTS`

</td>
<td colspan="2">


 The hardware accepts DTS audio tracks.

</td>
</tr>
<tr>
<td>


`AUDIO_CAP_LPCM`

</td>
<td colspan="2">


The hardware accepts uncompressed audio with Linear Pulse-Code Modulation (LPCM)

</td>
</tr>
<tr>
<td>


`AUDIO_CAP_MP1`

</td>
<td colspan="2">


The hardware accepts MPEG-1 Audio Layer 1.

</td>
</tr>
<tr>
<td>


`AUDIO_CAP_MP2`

</td>
<td colspan="2">


The hardware accepts MPEG-1 Audio Layer 2. Also known as MUSICAM.

</td>
</tr>
<tr>
<td>


`AUDIO_CAP_MP3`

</td>
<td colspan="2">


The hardware accepts MPEG-1 Audio Layer III. Commonly known as .mp3.

</td>
</tr>
<tr>
<td>


`AUDIO_CAP_AAC`

</td>
<td colspan="2">


The hardware accepts AAC (Advanced Audio Coding).

</td>
</tr>
<tr>
<td>


`AUDIO_CAP_OGG`

</td>
<td colspan="2">


The hardware accepts Vorbis audio tracks.

</td>
</tr>
<tr>
<td>


`AUDIO_CAP_SDDS`

</td>
<td colspan="2">


The hardware accepts Sony Dynamic Digital Sound (SDDS).

</td>
</tr>
<tr>
<td>


`AUDIO_CAP_AC3`

</td>
<td colspan="2">


The hardware accepts Dolby Digital ATSC A/52 audio. Also known as AC-3.

</td>
</tr>
</tbody>
</table>

<a id="rst-description-5"></a>

#### Description

A call to [AUDIO_GET_CAPABILITIES](<#rst-audio-get-capabilities>) returns an unsigned integer with the following bits set according to the hardwares capabilities.

---

<a id="rst-audio-function-calls"></a>

## Audio Function Calls

<a id="rst-audio-stop"></a>

### AUDIO_STOP

<a id="rst-synopsis-6"></a>

#### Synopsis





<a id="c-AUDIO_STOP"></a>

```c
AUDIO_STOP
```



```c
int ioctl(int fd, int request = AUDIO_STOP)
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


 Equals `AUDIO_STOP` for this command.

</td>
</tr>
</tbody>
</table>

<a id="rst-description-6"></a>

#### Description

> [!NOTE]
>
> Do **not** use in new drivers\! See: [General Notes](<~kernel/userspace/userspace-api/media-dvb/legacy-dvb-decoder-api#rst-legacy-dvb-decoder-notes>)

This ioctl call asks the Audio Device to stop playing the current stream.

<a id="rst-return-value"></a>

#### Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

---

<a id="rst-audio-play"></a>

### AUDIO_PLAY

<a id="rst-synopsis-7"></a>

#### Synopsis





<a id="c-AUDIO_PLAY"></a>

```c
AUDIO_PLAY
```



```c
int  ioctl(int fd, int request = AUDIO_PLAY)
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


 Equals `AUDIO_PLAY` for this command.

</td>
</tr>
</tbody>
</table>

<a id="rst-description-7"></a>

#### Description

> [!NOTE]
>
> Do **not** use in new drivers\! See: [General Notes](<~kernel/userspace/userspace-api/media-dvb/legacy-dvb-decoder-api#rst-legacy-dvb-decoder-notes>)

This ioctl call asks the Audio Device to start playing an audio stream from the selected source.

<a id="rst-return-value-1"></a>

#### Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

---

<a id="rst-audio-pause"></a>

### AUDIO_PAUSE

<a id="rst-synopsis-8"></a>

#### Synopsis





<a id="c-AUDIO_PAUSE"></a>

```c
AUDIO_PAUSE
```



```c
int  ioctl(int fd, int request = AUDIO_PAUSE)
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


Equals `AUDIO_PAUSE` for this command.

</td>
</tr>
</tbody>
</table>

<a id="rst-description-8"></a>

#### Description

> [!NOTE]
>
> Do **not** use in new drivers\! See: [General Notes](<~kernel/userspace/userspace-api/media-dvb/legacy-dvb-decoder-api#rst-legacy-dvb-decoder-notes>)

This ioctl call suspends the audio stream being played. Decoding and playing are paused. It is then possible to restart again decoding and playing process of the audio stream using [AUDIO_CONTINUE](<#rst-audio-continue>) command.

<a id="rst-return-value-2"></a>

#### Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

---

<a id="rst-audio-continue"></a>

### AUDIO_CONTINUE

<a id="rst-synopsis-9"></a>

#### Synopsis





<a id="c-AUDIO_CONTINUE"></a>

```c
AUDIO_CONTINUE
```



```c
int  ioctl(int fd, int request = AUDIO_CONTINUE)
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


Equals `AUDIO_CONTINUE` for this command.

</td>
</tr>
</tbody>
</table>

<a id="rst-description-9"></a>

#### Description

> [!NOTE]
>
> Do **not** use in new drivers\! See: [General Notes](<~kernel/userspace/userspace-api/media-dvb/legacy-dvb-decoder-api#rst-legacy-dvb-decoder-notes>)

This ioctl restarts the decoding and playing process previously paused with [AUDIO_PAUSE](<#rst-audio-pause>) command.

<a id="rst-return-value-3"></a>

#### Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

---

<a id="rst-audio-select-source"></a>

### AUDIO_SELECT_SOURCE

<a id="rst-synopsis-10"></a>

#### Synopsis





<a id="c-AUDIO_SELECT_SOURCE"></a>

```c
AUDIO_SELECT_SOURCE
```



```c
int ioctl(int fd, int request = AUDIO_SELECT_SOURCE,
audio_stream_source_t source)
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


Equals `AUDIO_SELECT_SOURCE` for this command.

</td>
</tr>
<tr>
<td>


[audio_stream_source_t](<#rst-audio-stream-source-t>) `source`

</td>
<td colspan="2">


Indicates the source that shall be used for the Audio stream.

</td>
</tr>
</tbody>
</table>

<a id="rst-description-10"></a>

#### Description

> [!NOTE]
>
> Do **not** use in new drivers\! See: [General Notes](<~kernel/userspace/userspace-api/media-dvb/legacy-dvb-decoder-api#rst-legacy-dvb-decoder-notes>)

This ioctl call informs the audio device which source shall be used for the input data. The possible sources are demux or memory. If `AUDIO_SOURCE_MEMORY` is selected, the data is fed to the Audio Device through the write command. If `AUDIO_SOURCE_DEMUX` is selected, the data is directly transferred from the onboard demux-device to the decoder. Note: This only supports DVB-devices with one demux and one decoder so far.

<a id="rst-return-value-4"></a>

#### Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

---

<a id="rst-audio-set-mute"></a>

### AUDIO_SET_MUTE

<a id="rst-synopsis-11"></a>

#### Synopsis





<a id="c-AUDIO_SET_MUTE"></a>

```c
AUDIO_SET_MUTE
```



```c
int  ioctl(int fd, int request = AUDIO_SET_MUTE, int state)
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


 Equals `AUDIO_SET_MUTE` for this command.

</td>
</tr>
<tr>
<td rowspan="3">


 `int state`

</td>
<td colspan="2">


 Indicates if audio device shall mute or not.

</td>
</tr>
<tr>
<td>


TRUE  ( \!= 0 )

</td>
<td>


mute audio

</td>
</tr>
<tr>
<td>


FALSE ( == 0 )

</td>
<td>


unmute audio

</td>
</tr>
</tbody>
</table>

<a id="rst-description-11"></a>

#### Description

> [!NOTE]
>
> Do **not** use in new drivers\! See: [General Notes](<~kernel/userspace/userspace-api/media-dvb/legacy-dvb-decoder-api#rst-legacy-dvb-decoder-notes>)

This ioctl is for DVB devices only. To control a V4L2 decoder use the V4L2 [ioctl VIDIOC_DECODER_CMD, VIDIOC_TRY_DECODER_CMD](<~kernel/userspace/userspace-api/media-v4l/vidioc-decoder-cmd#rst-vidioc-decoder-cmd>) with the `V4L2_DEC_CMD_START_MUTE_AUDIO` flag instead.

This ioctl call asks the audio device to mute the stream that is currently being played.

<a id="rst-return-value-5"></a>

#### Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

---

<a id="rst-audio-set-av-sync"></a>

### AUDIO_SET_AV_SYNC

<a id="rst-synopsis-12"></a>

#### Synopsis





<a id="c-AUDIO_SET_AV_SYNC"></a>

```c
AUDIO_SET_AV_SYNC
```



```c
int  ioctl(int fd, int request = AUDIO_SET_AV_SYNC, int state)
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


 Equals `AUDIO_AV_SYNC` for this command.

</td>
</tr>
<tr>
<td rowspan="3">


 `int state`

</td>
<td colspan="2">


 Tells the DVB subsystem if A/V synchronization shall be ON or OFF.

</td>
</tr>
<tr>
<td>


TRUE  ( \!= 0 )

</td>
<td>


AV-sync ON.

</td>
</tr>
<tr>
<td>


FALSE ( == 0 )

</td>
<td>


AV-sync OFF.

</td>
</tr>
</tbody>
</table>

<a id="rst-description-12"></a>

#### Description

> [!NOTE]
>
> Do **not** use in new drivers\! See: [General Notes](<~kernel/userspace/userspace-api/media-dvb/legacy-dvb-decoder-api#rst-legacy-dvb-decoder-notes>)

This ioctl call asks the Audio Device to turn ON or OFF A/V synchronization.

<a id="rst-return-value-6"></a>

#### Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

---

<a id="rst-audio-set-bypass-mode"></a>

### AUDIO_SET_BYPASS_MODE

<a id="rst-synopsis-13"></a>

#### Synopsis





<a id="c-AUDIO_SET_BYPASS_MODE"></a>

```c
AUDIO_SET_BYPASS_MODE
```



```c
int ioctl(int fd, int request = AUDIO_SET_BYPASS_MODE, int mode)
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


 Equals `AUDIO_SET_BYPASS_MODE` for this command.

</td>
</tr>
<tr>
<td rowspan="3">


 `int mode`

</td>
<td colspan="2">


 Enables or disables the decoding of the current Audio stream in the DVB subsystem.

</td>
</tr>
<tr>
<td>


TRUE  ( \!= 0 )

</td>
<td>


Disable bypass

</td>
</tr>
<tr>
<td>


FALSE ( == 0 )

</td>
<td>


Enable bypass

</td>
</tr>
</tbody>
</table>

<a id="rst-description-13"></a>

#### Description

> [!NOTE]
>
> Do **not** use in new drivers\! See: [General Notes](<~kernel/userspace/userspace-api/media-dvb/legacy-dvb-decoder-api#rst-legacy-dvb-decoder-notes>)

This ioctl call asks the Audio Device to bypass the Audio decoder and forward the stream without decoding. This mode shall be used if streams that can’t be handled by the DVB system shall be decoded. Dolby DigitalTM streams are automatically forwarded by the DVB subsystem if the hardware can handle it.

<a id="rst-return-value-7"></a>

#### Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

---

<a id="rst-audio-channel-select"></a>

### AUDIO_CHANNEL_SELECT

<a id="rst-synopsis-14"></a>

#### Synopsis





<a id="c-AUDIO_CHANNEL_SELECT"></a>

```c
AUDIO_CHANNEL_SELECT
```



```c
int ioctl(int fd, int request = AUDIO_CHANNEL_SELECT,
audio_channel_select_t)
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


Equals `AUDIO_CHANNEL_SELECT` for this command.

</td>
</tr>
<tr>
<td>


[audio_channel_select_t](<#rst-audio-channel-select-t>) `ch`

</td>
<td colspan="2">


Select the output format of the audio (mono left/right, stereo).

</td>
</tr>
</tbody>
</table>

<a id="rst-description-14"></a>

#### Description

> [!NOTE]
>
> Do **not** use in new drivers\! See: [General Notes](<~kernel/userspace/userspace-api/media-dvb/legacy-dvb-decoder-api#rst-legacy-dvb-decoder-notes>)

This ioctl is for DVB devices only. To control a V4L2 decoder use the V4L2 `V4L2_CID_MPEG_AUDIO_DEC_PLAYBACK` control instead.

This ioctl call asks the Audio Device to select the requested channel if possible.

<a id="rst-return-value-8"></a>

#### Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

---

<a id="rst-audio-get-status"></a>

### AUDIO_GET_STATUS

<a id="rst-synopsis-15"></a>

#### Synopsis





<a id="c-AUDIO_GET_STATUS"></a>

```c
AUDIO_GET_STATUS
```



```c
int ioctl(int fd, int request = AUDIO_GET_STATUS,
struct audio_status *status)
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


Equals AUDIO_GET_STATUS for this command.

</td>
</tr>
<tr>
<td>


`struct` [audio_status](<#rst-audio-status>) `*status`

</td>
<td colspan="2">


Returns the current state of Audio Device.

</td>
</tr>
</tbody>
</table>

<a id="rst-description-15"></a>

#### Description

> [!NOTE]
>
> Do **not** use in new drivers\! See: [General Notes](<~kernel/userspace/userspace-api/media-dvb/legacy-dvb-decoder-api#rst-legacy-dvb-decoder-notes>)

This ioctl call asks the Audio Device to return the current state of the Audio Device.

<a id="rst-return-value-9"></a>

#### Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

---

<a id="rst-audio-get-capabilities"></a>

### AUDIO_GET_CAPABILITIES

<a id="rst-synopsis-16"></a>

#### Synopsis





<a id="c-AUDIO_GET_CAPABILITIES"></a>

```c
AUDIO_GET_CAPABILITIES
```



```c
int ioctl(int fd, int request = AUDIO_GET_CAPABILITIES,
unsigned int *cap)
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


Equals `AUDIO_GET_CAPABILITIES` for this command.

</td>
</tr>
<tr>
<td>


`unsigned int *cap`

</td>
<td colspan="2">


Returns a bit array of supported sound formats. Bits are defined in [audio encodings](<#rst-audio-encodings>).

</td>
</tr>
</tbody>
</table>

<a id="rst-description-16"></a>

#### Description

> [!NOTE]
>
> Do **not** use in new drivers\! See: [General Notes](<~kernel/userspace/userspace-api/media-dvb/legacy-dvb-decoder-api#rst-legacy-dvb-decoder-notes>)

This ioctl call asks the Audio Device to tell us about the decoding capabilities of the audio hardware.

<a id="rst-return-value-10"></a>

#### Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

---

<a id="rst-audio-clear-buffer"></a>

### AUDIO_CLEAR_BUFFER

<a id="rst-synopsis-17"></a>

#### Synopsis





<a id="c-AUDIO_CLEAR_BUFFER"></a>

```c
AUDIO_CLEAR_BUFFER
```



```c
int  ioctl(int fd, int request = AUDIO_CLEAR_BUFFER)
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


Equals `AUDIO_CLEAR_BUFFER` for this command.

</td>
</tr>
</tbody>
</table>

<a id="rst-description-17"></a>

#### Description

> [!NOTE]
>
> Do **not** use in new drivers\! See: [General Notes](<~kernel/userspace/userspace-api/media-dvb/legacy-dvb-decoder-api#rst-legacy-dvb-decoder-notes>)

This ioctl call asks the Audio Device to clear all software and hardware buffers of the audio decoder device.

<a id="rst-return-value-11"></a>

#### Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

---

<a id="rst-audio-set-id"></a>

### AUDIO_SET_ID

<a id="rst-synopsis-18"></a>

#### Synopsis





<a id="c-AUDIO_SET_ID"></a>

```c
AUDIO_SET_ID
```



```c
int  ioctl(int fd, int request = AUDIO_SET_ID, int id)
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


Equals `AUDIO_SET_ID` for this command.

</td>
</tr>
<tr>
<td>


`int id`

</td>
<td colspan="2">


Audio sub-stream id.

</td>
</tr>
</tbody>
</table>

<a id="rst-description-18"></a>

#### Description

> [!NOTE]
>
> Do **not** use in new drivers\! See: [General Notes](<~kernel/userspace/userspace-api/media-dvb/legacy-dvb-decoder-api#rst-legacy-dvb-decoder-notes>)

This ioctl selects which sub-stream is to be decoded if a program or system stream is sent to the video device.

If no audio stream type is set the id has to be in range \[0xC0,0xDF\] for MPEG sound, in \[0x80,0x87\] for AC3 and in \[0xA0,0xA7\] for LPCM. See ITU-T H.222.0 \| ISO/IEC 13818-1 for further description.

If the stream type is set with [AUDIO_SET_STREAMTYPE](<#rst-audio-set-streamtype>), specifies the id just the sub-stream id of the audio stream and only the first 5 bits (&amp; 0x1F) are recognized.

<a id="rst-return-value-12"></a>

#### Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

---

<a id="rst-audio-set-mixer"></a>

### AUDIO_SET_MIXER

<a id="rst-synopsis-19"></a>

#### Synopsis





<a id="c-AUDIO_SET_MIXER"></a>

```c
AUDIO_SET_MIXER
```



```c
int ioctl(int fd, int request = AUDIO_SET_MIXER, audio_mixer_t *mix)
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


Equals `AUDIO_SET_MIXER` for this command.

</td>
</tr>
<tr>
<td>


`audio_mixer_t *mix`

</td>
<td colspan="2">


Mixer settings.

</td>
</tr>
</tbody>
</table>

<a id="rst-description-19"></a>

#### Description

> [!NOTE]
>
> Do **not** use in new drivers\! See: [General Notes](<~kernel/userspace/userspace-api/media-dvb/legacy-dvb-decoder-api#rst-legacy-dvb-decoder-notes>)

This ioctl lets you adjust the mixer settings of the audio decoder.

<a id="rst-return-value-13"></a>

#### Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

---

<a id="rst-audio-set-streamtype"></a>

### AUDIO_SET_STREAMTYPE

<a id="rst-synopsis-20"></a>

#### Synopsis





<a id="c-AUDIO_SET_STREAMTYPE"></a>

```c
AUDIO_SET_STREAMTYPE
```



```c
int  ioctl(fd, int request = AUDIO_SET_STREAMTYPE, int type)
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


Equals `AUDIO_SET_STREAMTYPE` for this command.

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

<a id="rst-description-20"></a>

#### Description

> [!NOTE]
>
> Do **not** use in new drivers\! See: [General Notes](<~kernel/userspace/userspace-api/media-dvb/legacy-dvb-decoder-api#rst-legacy-dvb-decoder-notes>)

This ioctl tells the driver which kind of audio stream to expect. This is useful if the stream offers several audio sub-streams like LPCM and AC3.

Stream types defined in ITU-T H.222.0 \| ISO/IEC 13818-1 are used.

<a id="rst-return-value-14"></a>

#### Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.


<table>
<tbody>
<tr>
<td>


`EINVAL`

</td>
<td>


Type is not a valid or supported stream type.

</td>
</tr>
</tbody>
</table>

---

<a id="rst-audio-bilingual-channel-select"></a>

### AUDIO_BILINGUAL_CHANNEL_SELECT

<a id="rst-synopsis-21"></a>

#### Synopsis





<a id="c-AUDIO_BILINGUAL_CHANNEL_SELECT"></a>

```c
AUDIO_BILINGUAL_CHANNEL_SELECT
```



```c
int ioctl(int fd, int request = AUDIO_BILINGUAL_CHANNEL_SELECT,
audio_channel_select_t)
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


Equals `AUDIO_BILINGUAL_CHANNEL_SELECT` for this command.

</td>
</tr>
<tr>
<td>


`audio_channel_select_t ch`

</td>
<td colspan="2">


Select the output format of the audio (mono left/right, stereo).

</td>
</tr>
</tbody>
</table>

<a id="rst-description-21"></a>

#### Description

> [!NOTE]
>
> Do **not** use in new drivers\! See: [General Notes](<~kernel/userspace/userspace-api/media-dvb/legacy-dvb-decoder-api#rst-legacy-dvb-decoder-notes>)

This ioctl has been replaced by the V4L2 `V4L2_CID_MPEG_AUDIO_DEC_MULTILINGUAL_PLAYBACK` control for MPEG decoders controlled through V4L2.

This ioctl call asks the Audio Device to select the requested channel for bilingual streams if possible.

<a id="rst-return-value-15"></a>

#### Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

---

<a id="rst-open"></a>

### open()

<a id="rst-synopsis-22"></a>

#### Synopsis



```c
#include <fcntl.h>
```





<a id="c-open"></a>

```c
int  open(const char *deviceName, int flags)
```

<a id="rst-arguments-16"></a>

#### Arguments


<table>
<tbody>
<tr>
<td>


`const char *deviceName`

</td>
<td colspan="2">


Name of specific audio device.

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

<a id="rst-description-22"></a>

#### Description

This system call opens a named audio device (e.g. `/dev/dvb/adapter0/audio0`) for subsequent use. When an open() call has succeeded, the device will be ready for use. The significance of blocking or non-blocking mode is described in the documentation for functions where there is a difference. It does not affect the semantics of the open() call itself. A device opened in blocking mode can later be put into non-blocking mode (and vice versa) using the F_SETFL command of the fcntl system call. This is a standard system call, documented in the Linux manual page for fcntl. Only one user can open the Audio Device in O_RDWR mode. All other attempts to open the device in this mode will fail, and an error code will be returned. If the Audio Device is opened in O_RDONLY mode, the only ioctl call that can be used is [AUDIO_GET_STATUS](<#rst-audio-get-status>). All other call will return with an error code.

<a id="rst-return-value-16"></a>

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

<a id="rst-synopsis-23"></a>

#### Synopsis





<a id="c-close"></a>

```c
int close(int fd)
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
</tbody>
</table>

<a id="rst-description-23"></a>

#### Description

This system call closes a previously opened audio device.

<a id="rst-return-value-17"></a>

#### Return Value


<table>
<tbody>
<tr>
<td>


`EBADF`

</td>
<td>


Fd is not a valid open file descriptor.

</td>
</tr>
</tbody>
</table>

---

<a id="rst-write"></a>

### write()

<a id="rst-synopsis-24"></a>

#### Synopsis



```c
size_t write(int fd, const void *buf, size_t count)
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

<a id="rst-description-24"></a>

#### Description

This system call can only be used if `AUDIO_SOURCE_MEMORY` is selected in the ioctl call [AUDIO_SELECT_SOURCE](<#rst-audio-select-source>). The data provided shall be in PES format. If `O_NONBLOCK` is not specified the function will block until buffer space is available. The amount of data to be transferred is implied by count.

<a id="rst-return-value-18"></a>

#### Return Value


<table>
<tbody>
<tr>
<td>


`EPERM`

</td>
<td colspan="2">


 Mode `AUDIO_SOURCE_MEMORY` not selected.

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


Fd is not a valid open file descriptor.

</td>
</tr>
</tbody>
</table>
