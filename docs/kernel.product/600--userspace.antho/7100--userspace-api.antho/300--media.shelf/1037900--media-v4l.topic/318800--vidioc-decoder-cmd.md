---
title: "ioctl VIDIOC_DECODER_CMD, VIDIOC_TRY_DECODER_CMD"
type: reference
description: "VIDIOC_DECODER_CMD - VIDIOC_TRY_DECODER_CMD - Execute an decoder command"
---

<a id="rst-ioctl-vidioc-decoder-cmd-vidioc-try-decoder-cmd"></a>
<a id="rst-vidioc-decoder-cmd"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

VIDIOC_DECODER_CMD - VIDIOC_TRY_DECODER_CMD - Execute an decoder command

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-VIDIOC_DECODER_CMD"></a>

```c
VIDIOC_DECODER_CMD
```

`int ioctl(int fd, VIDIOC_DECODER_CMD, struct v4l2_decoder_cmd *argp)`





<a id="c-VIDIOC_TRY_DECODER_CMD"></a>

```c
VIDIOC_TRY_DECODER_CMD
```

`int ioctl(int fd, VIDIOC_TRY_DECODER_CMD, struct v4l2_decoder_cmd *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  pointer to struct `v4l2_decoder_cmd`.

<a id="rst-description"></a>

## Description

These ioctls control an audio/video (usually MPEG-) decoder. `VIDIOC_DECODER_CMD` sends a command to the decoder, `VIDIOC_TRY_DECODER_CMD` can be used to try a command without actually executing it. To send a command applications must initialize all fields of a struct `v4l2_decoder_cmd` and call `VIDIOC_DECODER_CMD` or `VIDIOC_TRY_DECODER_CMD` with a pointer to this structure.

The `cmd` field must contain the command code. Some commands use the `flags` field for additional information.

A `write()` or [ioctl VIDIOC_STREAMON, VIDIOC_STREAMOFF](<~kernel/userspace/userspace-api/media-v4l/vidioc-streamon#rst-vidioc-streamon>) call sends an implicit START command to the decoder if it has not been started yet. Applies to both queues of mem2mem decoders.

A `close()` or [VIDIOC_STREAMOFF](<~kernel/userspace/userspace-api/media-v4l/vidioc-streamon#rst-vidioc-streamon>) call of a streaming file descriptor sends an implicit immediate STOP command to the decoder, and all buffered data is discarded. Applies to both queues of mem2mem decoders.

In principle, these ioctls are optional, not all drivers may support them. They were introduced in Linux 3.3. They are, however, mandatory for stateful mem2mem decoders (as further documented in [Memory-to-Memory Stateful Video Decoder Interface](<~kernel/userspace/userspace-api/media-v4l/dev-decoder#rst-decoder>)).

<!-- tabularcolumns: |p{2.0cm}|p{1.1cm}|p{2.2cm}|p{11.8cm}| -->





<a id="c-v4l2_decoder_cmd"></a>

```c
v4l2_decoder_cmd
```


<table>
<caption>struct v4l2_decoder_cmd</caption>
<tbody>
<tr>
<td>


\__u32

</td>
<td>


`cmd`

</td>
<td>




</td>
<td>


The decoder command, see [decoder-cmds](<#rst-decoder-cmds>).

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`flags`

</td>
<td>




</td>
<td>


Flags to go with the command. If no flags are defined for this command, drivers and applications must set this field to zero.

</td>
</tr>
<tr>
<td>


union \{

</td>
<td colspan="3">


(anonymous)

</td>
</tr>
<tr>
<td>


struct

</td>
<td>


`start`

</td>
<td>




</td>
<td>


Structure containing additional data for the `V4L2_DEC_CMD_START` command.

</td>
</tr>
<tr>
<td>




</td>
<td>


\__s32

</td>
<td>


`speed`

</td>
<td>


Playback speed and direction. The playback speed is defined as `speed`/1000 of the normal speed. So 1000 is normal playback. Negative numbers denote reverse playback, so -1000 does reverse playback at normal speed. Speeds -1, 0 and 1 have special meanings: speed 0 is shorthand for 1000 (normal playback). A speed of 1 steps just one frame forward, a speed of -1 steps just one frame back.

</td>
</tr>
<tr>
<td>




</td>
<td>


\__u32

</td>
<td>


`format`

</td>
<td>


Format restrictions. This field is set by the driver, not the application. Possible values are `V4L2_DEC_START_FMT_NONE` if there are no format restrictions or `V4L2_DEC_START_FMT_GOP` if the decoder operates on full GOPs (*Group Of Pictures*). This is usually the case for reverse playback: the decoder needs full GOPs, which it can then play in reverse order. So to implement reverse playback the application must feed the decoder the last GOP in the video file, then the GOP before that, etc. etc.

</td>
</tr>
<tr>
<td>


struct

</td>
<td>


`stop`

</td>
<td>




</td>
<td>


Structure containing additional data for the `V4L2_DEC_CMD_STOP` command.

</td>
</tr>
<tr>
<td>




</td>
<td>


\__u64

</td>
<td>


`pts`

</td>
<td>


Stop playback at this `pts` or immediately if the playback is already past that timestamp. Leave to 0 if you want to stop after the last frame was decoded.

</td>
</tr>
<tr>
<td>


struct

</td>
<td colspan="3">


`raw`

</td>
</tr>
<tr>
<td>




</td>
<td>


\__u32

</td>
<td>


`data`\[16\]

</td>
<td>


Reserved for future extensions. Drivers and applications must set the array to zero.

</td>
</tr>
<tr>
<td>


\}

</td>
<td colspan="3">




</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{5.6cm}|p{0.6cm}|p{11.1cm}| -->

<a id="rst-decoder-cmds"></a>


<table>
<caption>Decoder Commands</caption>
<tbody>
<tr>
<td>


`V4L2_DEC_CMD_START`

</td>
<td>


0

</td>
<td>


Start the decoder. When the decoder is already running or paused, this command will just change the playback speed. That means that calling `V4L2_DEC_CMD_START` when the decoder was paused will *not* resume the decoder. You have to explicitly call `V4L2_DEC_CMD_RESUME` for that. This command has one flag: `V4L2_DEC_CMD_START_MUTE_AUDIO`. If set, then audio will be muted when playing back at a non-standard speed.

For a device implementing the [Memory-to-Memory Stateful Video Decoder Interface](<~kernel/userspace/userspace-api/media-v4l/dev-decoder#rst-decoder>), once the drain sequence is initiated with the `V4L2_DEC_CMD_STOP` command, it must be driven to completion before this command can be invoked.  Any attempt to invoke the command while the drain sequence is in progress will trigger an `EBUSY` error code.  The command may be also used to restart the decoder in case of an implicit stop initiated by the decoder itself, without the `V4L2_DEC_CMD_STOP` being called explicitly. See [Memory-to-Memory Stateful Video Decoder Interface](<~kernel/userspace/userspace-api/media-v4l/dev-decoder#rst-decoder>) for more details.

</td>
</tr>
<tr>
<td>


`V4L2_DEC_CMD_STOP`

</td>
<td>


1

</td>
<td>


Stop the decoder. When the decoder is already stopped, this command does nothing. This command has two flags: if `V4L2_DEC_CMD_STOP_TO_BLACK` is set, then the decoder will set the picture to black after it stopped decoding. Otherwise the last image will repeat. If `V4L2_DEC_CMD_STOP_IMMEDIATELY` is set, then the decoder stops immediately (ignoring the `pts` value), otherwise it will keep decoding until timestamp &gt;= pts or until the last of the pending data from its internal buffers was decoded.

For a device implementing the [Memory-to-Memory Stateful Video Decoder Interface](<~kernel/userspace/userspace-api/media-v4l/dev-decoder#rst-decoder>), the command will initiate the drain sequence as documented in [Memory-to-Memory Stateful Video Decoder Interface](<~kernel/userspace/userspace-api/media-v4l/dev-decoder#rst-decoder>).  No flags or other arguments are accepted in this case. Any attempt to invoke the command again before the sequence completes will trigger an `EBUSY` error code.

</td>
</tr>
<tr>
<td>


`V4L2_DEC_CMD_PAUSE`

</td>
<td>


2

</td>
<td>


Pause the decoder. When the decoder has not been started yet, the driver will return an `EPERM` error code. When the decoder is already paused, this command does nothing. This command has one flag: if `V4L2_DEC_CMD_PAUSE_TO_BLACK` is set, then set the decoder output to black when paused.

</td>
</tr>
<tr>
<td>


`V4L2_DEC_CMD_RESUME`

</td>
<td>


3

</td>
<td>


Resume decoding after a PAUSE command. When the decoder has not been started yet, the driver will return an `EPERM` error code. When the decoder is already running, this command does nothing. No flags are defined for this command.

</td>
</tr>
<tr>
<td>


`V4L2_DEC_CMD_FLUSH`

</td>
<td>


4

</td>
<td>


Flush any held capture buffers. Only valid for stateless decoders. This command is typically used when the application reached the end of the stream and the last output buffer had the `V4L2_BUF_FLAG_M2M_HOLD_CAPTURE_BUF` flag set. This would prevent dequeueing the capture buffer containing the last decoded frame. So this command can be used to explicitly flush that final decoded frame. This command does nothing if there are no held capture buffers.

</td>
</tr>
</tbody>
</table>

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

- **EBUSY**

  A drain sequence of a device implementing the [Memory-to-Memory Stateful Video Decoder Interface](<~kernel/userspace/userspace-api/media-v4l/dev-decoder#rst-decoder>) is still in progress. It is not allowed to issue another decoder command until it completes.

- **EINVAL**

  The `cmd` field is invalid.

- **EPERM**

  The application sent a PAUSE or RESUME command when the decoder was not running.
