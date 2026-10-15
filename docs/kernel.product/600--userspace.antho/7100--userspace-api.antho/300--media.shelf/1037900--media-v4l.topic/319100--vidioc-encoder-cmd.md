---
title: "ioctl VIDIOC_ENCODER_CMD, VIDIOC_TRY_ENCODER_CMD"
type: reference
description: "VIDIOC_ENCODER_CMD - VIDIOC_TRY_ENCODER_CMD - Execute an encoder command"
---

<a id="rst-ioctl-vidioc-encoder-cmd-vidioc-try-encoder-cmd"></a>
<a id="rst-vidioc-encoder-cmd"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

<a id="rst-name"></a>

## Name

VIDIOC_ENCODER_CMD - VIDIOC_TRY_ENCODER_CMD - Execute an encoder command

<a id="rst-synopsis"></a>

## Synopsis





<a id="c-VIDIOC_ENCODER_CMD"></a>

```c
VIDIOC_ENCODER_CMD
```

`int ioctl(int fd, VIDIOC_ENCODER_CMD, struct v4l2_encoder_cmd *argp)`





<a id="c-VIDIOC_TRY_ENCODER_CMD"></a>

```c
VIDIOC_TRY_ENCODER_CMD
```

`int ioctl(int fd, VIDIOC_TRY_ENCODER_CMD, struct v4l2_encoder_cmd *argp)`

<a id="rst-arguments"></a>

## Arguments

- **`fd`**

  File descriptor returned by `open()`.

- **`argp`**

  Pointer to struct `v4l2_encoder_cmd`.

<a id="rst-description"></a>

## Description

These ioctls control an audio/video (usually MPEG-) encoder. `VIDIOC_ENCODER_CMD` sends a command to the encoder, `VIDIOC_TRY_ENCODER_CMD` can be used to try a command without actually executing it.

To send a command applications must initialize all fields of a struct `v4l2_encoder_cmd` and call `VIDIOC_ENCODER_CMD` or `VIDIOC_TRY_ENCODER_CMD` with a pointer to this structure.

The `cmd` field must contain the command code. Some commands use the `flags` field for additional information.

After a STOP command, `read()` calls will read the remaining data buffered by the driver. When the buffer is empty, `read()` will return zero and the next `read()` call will restart the encoder.

A `read()` or [VIDIOC_STREAMON](<~kernel/userspace/userspace-api/media-v4l/vidioc-streamon#rst-vidioc-streamon>) call sends an implicit START command to the encoder if it has not been started yet. Applies to both queues of mem2mem encoders.

A `close()` or [VIDIOC_STREAMOFF](<~kernel/userspace/userspace-api/media-v4l/vidioc-streamon#rst-vidioc-streamon>) call of a streaming file descriptor sends an implicit immediate STOP to the encoder, and all buffered data is discarded. Applies to both queues of mem2mem encoders.

These ioctls are optional, not all drivers may support them. They were introduced in Linux 2.6.21. They are, however, mandatory for stateful mem2mem encoders (as further documented in [Memory-to-Memory Stateful Video Encoder Interface](<~kernel/userspace/userspace-api/media-v4l/dev-encoder#rst-encoder>)).

<!-- tabularcolumns: |p{4.4cm}|p{4.4cm}|p{8.5cm}| -->





<a id="c-v4l2_encoder_cmd"></a>

```c
v4l2_encoder_cmd
```


<table>
<caption>struct v4l2_encoder_cmd</caption>
<tbody>
<tr>
<td>


\__u32

</td>
<td>


`cmd`

</td>
<td>


The encoder command, see [encoder-cmds](<#rst-encoder-cmds>).

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


Flags to go with the command, see [encoder-flags](<#rst-encoder-flags>). If no flags are defined for this command, drivers and applications must set this field to zero.

</td>
</tr>
<tr>
<td>


\__u32

</td>
<td>


`data`\[8\]

</td>
<td>


Reserved for future extensions. Drivers and applications must set the array to zero.

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{6.6cm}|p{2.2cm}|p{8.5cm}| -->

<a id="rst-encoder-cmds"></a>


<table>
<caption>Encoder Commands</caption>
<tbody>
<tr>
<td>


`V4L2_ENC_CMD_START`

</td>
<td>


0

</td>
<td>


Start the encoder. When the encoder is already running or paused, this command does nothing. No flags are defined for this command.

For a device implementing the [Memory-to-Memory Stateful Video Encoder Interface](<~kernel/userspace/userspace-api/media-v4l/dev-encoder#rst-encoder>), once the drain sequence is initiated with the `V4L2_ENC_CMD_STOP` command, it must be driven to completion before this command can be invoked.  Any attempt to invoke the command while the drain sequence is in progress will trigger an `EBUSY` error code. See [Memory-to-Memory Stateful Video Encoder Interface](<~kernel/userspace/userspace-api/media-v4l/dev-encoder#rst-encoder>) for more details.

</td>
</tr>
<tr>
<td>


`V4L2_ENC_CMD_STOP`

</td>
<td>


1

</td>
<td>


Stop the encoder. When the `V4L2_ENC_CMD_STOP_AT_GOP_END` flag is set, encoding will continue until the end of the current *Group Of Pictures*, otherwise encoding will stop immediately. When the encoder is already stopped, this command does nothing.

For a device implementing the [Memory-to-Memory Stateful Video Encoder Interface](<~kernel/userspace/userspace-api/media-v4l/dev-encoder#rst-encoder>), the command will initiate the drain sequence as documented in [Memory-to-Memory Stateful Video Encoder Interface](<~kernel/userspace/userspace-api/media-v4l/dev-encoder#rst-encoder>). No flags or other arguments are accepted in this case. Any attempt to invoke the command again before the sequence completes will trigger an `EBUSY` error code.

</td>
</tr>
<tr>
<td>


`V4L2_ENC_CMD_PAUSE`

</td>
<td>


2

</td>
<td>


Pause the encoder. When the encoder has not been started yet, the driver will return an `EPERM` error code. When the encoder is already paused, this command does nothing. No flags are defined for this command.

</td>
</tr>
<tr>
<td>


`V4L2_ENC_CMD_RESUME`

</td>
<td>


3

</td>
<td>


Resume encoding after a PAUSE command. When the encoder has not been started yet, the driver will return an `EPERM` error code. When the encoder is already running, this command does nothing. No flags are defined for this command.

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{6.6cm}|p{2.2cm}|p{8.5cm}| -->

<a id="rst-encoder-flags"></a>


<table>
<caption>Encoder Command Flags</caption>
<tbody>
<tr>
<td>


`V4L2_ENC_CMD_STOP_AT_GOP_END`

</td>
<td>


0x0001

</td>
<td>


Stop encoding at the end of the current *Group Of Pictures*, rather than immediately.

Does not apply to [Memory-to-Memory Stateful Video Encoder Interface](<~kernel/userspace/userspace-api/media-v4l/dev-encoder#rst-encoder>).

</td>
</tr>
</tbody>
</table>

<a id="rst-return-value"></a>

## Return Value

On success 0 is returned, on error -1 and the `errno` variable is set appropriately. The generic error codes are described at the [Generic Error Codes](<~kernel/userspace/userspace-api/media/gen-errors#rst-gen-errors-1>) chapter.

- **EBUSY**

  A drain sequence of a device implementing the [Memory-to-Memory Stateful Video Encoder Interface](<~kernel/userspace/userspace-api/media-v4l/dev-encoder#rst-encoder>) is still in progress. It is not allowed to issue another encoder command until it completes.

- **EINVAL**

  The `cmd` field is invalid.

- **EPERM**

  The application sent a PAUSE or RESUME command when the encoder was not running.
