---
title: "Codec Control Reference"
type: reference
description: "Below all controls within the Codec control class are described. First the generic controls, then controls specific for certain hardware."
---

<a id="rst-codec-control-reference"></a>
<a id="rst-codec-controls"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

Below all controls within the Codec control class are described. First the generic controls, then controls specific for certain hardware.

> [!NOTE]
>
> These controls are applicable to all codecs and not just MPEG. The defines are prefixed with V4L2\_CID\_MPEG/V4L2\_MPEG as the controls were originally made for MPEG codecs and later extended to cover all encoding formats.

<a id="rst-generic-codec-controls"></a>

## Generic Codec Controls

<a id="rst-codec-control-ids"></a>
<a id="rst-mpeg-control-id"></a>

### Codec Control IDs

- **`V4L2_CID_CODEC_CLASS (class)`**

  The Codec class descriptor. Calling [ioctls VIDIOC\_QUERYCTRL, VIDIOC\_QUERY\_EXT\_CTRL and VIDIOC\_QUERYMENU](<~kernel/userspace/userspace-api/media-v4l/vidioc-queryctrl#rst-vidioc-queryctrl>) for this control will return a description of this control class. This description can be used as the caption of a Tab page in a GUI, for example.

<a id="rst-v4l2-mpeg-stream-type"></a>

- **`V4L2_CID_MPEG_STREAM_TYPE`**

  (enum)

- **enum v4l2\_mpeg\_stream\_type -**

  The MPEG-1, -2 or -4 output stream type. One cannot assume anything here. Each hardware MPEG encoder tends to support different subsets of the available MPEG stream types. This control is specific to multiplexed MPEG streams. The currently defined stream types are:


<table>
<tbody>
<tr>
<td>



`V4L2_MPEG_STREAM_TYPE_MPEG2_PS`

</td>
<td>



MPEG-2 program stream

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_STREAM_TYPE_MPEG2_TS`

</td>
<td>



MPEG-2 transport stream

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_STREAM_TYPE_MPEG1_SS`

</td>
<td>



MPEG-1 system stream

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_STREAM_TYPE_MPEG2_DVD`

</td>
<td>



MPEG-2 DVD-compatible stream

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_STREAM_TYPE_MPEG1_VCD`

</td>
<td>



MPEG-1 VCD-compatible stream

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_STREAM_TYPE_MPEG2_SVCD`

</td>
<td>



MPEG-2 SVCD-compatible stream

</td>
</tr>
</tbody>
</table>

- **`V4L2_CID_MPEG_STREAM_PID_PMT (integer)`**

  Program Map Table Packet ID for the MPEG transport stream (default 16)

- **`V4L2_CID_MPEG_STREAM_PID_AUDIO (integer)`**

  Audio Packet ID for the MPEG transport stream (default 256)

- **`V4L2_CID_MPEG_STREAM_PID_VIDEO (integer)`**

  Video Packet ID for the MPEG transport stream (default 260)

- **`V4L2_CID_MPEG_STREAM_PID_PCR (integer)`**

  Packet ID for the MPEG transport stream carrying PCR fields (default 259)

- **`V4L2_CID_MPEG_STREAM_PES_ID_AUDIO (integer)`**

  Audio ID for MPEG PES

- **`V4L2_CID_MPEG_STREAM_PES_ID_VIDEO (integer)`**

  Video ID for MPEG PES

<a id="rst-v4l2-mpeg-stream-vbi-fmt"></a>

- **`V4L2_CID_MPEG_STREAM_VBI_FMT`**

  (enum)

- **enum v4l2\_mpeg\_stream\_vbi\_fmt -**

  Some cards can embed VBI data (e. g. Closed Caption, Teletext) into the MPEG stream. This control selects whether VBI data should be embedded, and if so, what embedding method should be used. The list of possible VBI formats depends on the driver. The currently defined VBI format types are:

<!-- tabularcolumns: |p{6.6 cm}|p{10.9cm}| -->


<table>
<tbody>
<tr>
<td>



`V4L2_MPEG_STREAM_VBI_FMT_NONE`

</td>
<td>



No VBI in the MPEG stream

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_STREAM_VBI_FMT_IVTV`

</td>
<td>



VBI in private packets, IVTV format (documented in the kernel sources in the file `Documentation/userspace-api/media/drivers/cx2341x-uapi.rst`)

</td>
</tr>
</tbody>
</table>

<a id="rst-v4l2-mpeg-audio-sampling-freq"></a>

- **`V4L2_CID_MPEG_AUDIO_SAMPLING_FREQ`**

  (enum)

- **enum v4l2\_mpeg\_audio\_sampling\_freq -**

  MPEG Audio sampling frequency. Possible values are:


<table>
<tbody>
<tr>
<td>



`V4L2_MPEG_AUDIO_SAMPLING_FREQ_44100`

</td>
<td>



44.1 kHz

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_SAMPLING_FREQ_48000`

</td>
<td>



48 kHz

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_SAMPLING_FREQ_32000`

</td>
<td>



32 kHz

</td>
</tr>
</tbody>
</table>

<a id="rst-v4l2-mpeg-audio-encoding"></a>

- **`V4L2_CID_MPEG_AUDIO_ENCODING`**

  (enum)

- **enum v4l2\_mpeg\_audio\_encoding -**

  MPEG Audio encoding. This control is specific to multiplexed MPEG streams. Possible values are:


<table>
<tbody>
<tr>
<td>



`V4L2_MPEG_AUDIO_ENCODING_LAYER_1`

</td>
<td>



MPEG-1/2 Layer I encoding

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_ENCODING_LAYER_2`

</td>
<td>



MPEG-1/2 Layer II encoding

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_ENCODING_LAYER_3`

</td>
<td>



MPEG-1/2 Layer III encoding

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_ENCODING_AAC`

</td>
<td>



MPEG-2/4 AAC (Advanced Audio Coding)

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_ENCODING_AC3`

</td>
<td>



AC-3 aka ATSC A/52 encoding

</td>
</tr>
</tbody>
</table>

<a id="rst-v4l2-mpeg-audio-l1-bitrate"></a>

- **`V4L2_CID_MPEG_AUDIO_L1_BITRATE`**

  (enum)

- **enum v4l2\_mpeg\_audio\_l1\_bitrate -**

  MPEG-1/2 Layer I bitrate. Possible values are:


<table>
<tbody>
<tr>
<td>



`V4L2_MPEG_AUDIO_L1_BITRATE_32K`

</td>
<td>



32 kbit/s

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_L1_BITRATE_64K`

</td>
<td>



64 kbit/s

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_L1_BITRATE_96K`

</td>
<td>



96 kbit/s

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_L1_BITRATE_128K`

</td>
<td>



128 kbit/s

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_L1_BITRATE_160K`

</td>
<td>



160 kbit/s

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_L1_BITRATE_192K`

</td>
<td>



192 kbit/s

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_L1_BITRATE_224K`

</td>
<td>



224 kbit/s

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_L1_BITRATE_256K`

</td>
<td>



256 kbit/s

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_L1_BITRATE_288K`

</td>
<td>



288 kbit/s

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_L1_BITRATE_320K`

</td>
<td>



320 kbit/s

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_L1_BITRATE_352K`

</td>
<td>



352 kbit/s

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_L1_BITRATE_384K`

</td>
<td>



384 kbit/s

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_L1_BITRATE_416K`

</td>
<td>



416 kbit/s

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_L1_BITRATE_448K`

</td>
<td>



448 kbit/s

</td>
</tr>
</tbody>
</table>

<a id="rst-v4l2-mpeg-audio-l2-bitrate"></a>

- **`V4L2_CID_MPEG_AUDIO_L2_BITRATE`**

  (enum)

- **enum v4l2\_mpeg\_audio\_l2\_bitrate -**

  MPEG-1/2 Layer II bitrate. Possible values are:


<table>
<tbody>
<tr>
<td>



`V4L2_MPEG_AUDIO_L2_BITRATE_32K`

</td>
<td>



32 kbit/s

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_L2_BITRATE_48K`

</td>
<td>



48 kbit/s

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_L2_BITRATE_56K`

</td>
<td>



56 kbit/s

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_L2_BITRATE_64K`

</td>
<td>



64 kbit/s

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_L2_BITRATE_80K`

</td>
<td>



80 kbit/s

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_L2_BITRATE_96K`

</td>
<td>



96 kbit/s

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_L2_BITRATE_112K`

</td>
<td>



112 kbit/s

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_L2_BITRATE_128K`

</td>
<td>



128 kbit/s

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_L2_BITRATE_160K`

</td>
<td>



160 kbit/s

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_L2_BITRATE_192K`

</td>
<td>



192 kbit/s

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_L2_BITRATE_224K`

</td>
<td>



224 kbit/s

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_L2_BITRATE_256K`

</td>
<td>



256 kbit/s

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_L2_BITRATE_320K`

</td>
<td>



320 kbit/s

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_L2_BITRATE_384K`

</td>
<td>



384 kbit/s

</td>
</tr>
</tbody>
</table>

<a id="rst-v4l2-mpeg-audio-l3-bitrate"></a>

- **`V4L2_CID_MPEG_AUDIO_L3_BITRATE`**

  (enum)

- **enum v4l2\_mpeg\_audio\_l3\_bitrate -**

  MPEG-1/2 Layer III bitrate. Possible values are:


<table>
<tbody>
<tr>
<td>



`V4L2_MPEG_AUDIO_L3_BITRATE_32K`

</td>
<td>



32 kbit/s

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_L3_BITRATE_40K`

</td>
<td>



40 kbit/s

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_L3_BITRATE_48K`

</td>
<td>



48 kbit/s

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_L3_BITRATE_56K`

</td>
<td>



56 kbit/s

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_L3_BITRATE_64K`

</td>
<td>



64 kbit/s

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_L3_BITRATE_80K`

</td>
<td>



80 kbit/s

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_L3_BITRATE_96K`

</td>
<td>



96 kbit/s

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_L3_BITRATE_112K`

</td>
<td>



112 kbit/s

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_L3_BITRATE_128K`

</td>
<td>



128 kbit/s

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_L3_BITRATE_160K`

</td>
<td>



160 kbit/s

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_L3_BITRATE_192K`

</td>
<td>



192 kbit/s

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_L3_BITRATE_224K`

</td>
<td>



224 kbit/s

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_L3_BITRATE_256K`

</td>
<td>



256 kbit/s

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_L3_BITRATE_320K`

</td>
<td>



320 kbit/s

</td>
</tr>
</tbody>
</table>

- **`V4L2_CID_MPEG_AUDIO_AAC_BITRATE (integer)`**

  AAC bitrate in bits per second.

<a id="rst-v4l2-mpeg-audio-ac3-bitrate"></a>

- **`V4L2_CID_MPEG_AUDIO_AC3_BITRATE`**

  (enum)

- **enum v4l2\_mpeg\_audio\_ac3\_bitrate -**

  AC-3 bitrate. Possible values are:


<table>
<tbody>
<tr>
<td>



`V4L2_MPEG_AUDIO_AC3_BITRATE_32K`

</td>
<td>



32 kbit/s

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_AC3_BITRATE_40K`

</td>
<td>



40 kbit/s

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_AC3_BITRATE_48K`

</td>
<td>



48 kbit/s

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_AC3_BITRATE_56K`

</td>
<td>



56 kbit/s

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_AC3_BITRATE_64K`

</td>
<td>



64 kbit/s

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_AC3_BITRATE_80K`

</td>
<td>



80 kbit/s

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_AC3_BITRATE_96K`

</td>
<td>



96 kbit/s

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_AC3_BITRATE_112K`

</td>
<td>



112 kbit/s

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_AC3_BITRATE_128K`

</td>
<td>



128 kbit/s

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_AC3_BITRATE_160K`

</td>
<td>



160 kbit/s

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_AC3_BITRATE_192K`

</td>
<td>



192 kbit/s

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_AC3_BITRATE_224K`

</td>
<td>



224 kbit/s

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_AC3_BITRATE_256K`

</td>
<td>



256 kbit/s

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_AC3_BITRATE_320K`

</td>
<td>



320 kbit/s

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_AC3_BITRATE_384K`

</td>
<td>



384 kbit/s

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_AC3_BITRATE_448K`

</td>
<td>



448 kbit/s

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_AC3_BITRATE_512K`

</td>
<td>



512 kbit/s

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_AC3_BITRATE_576K`

</td>
<td>



576 kbit/s

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_AC3_BITRATE_640K`

</td>
<td>



640 kbit/s

</td>
</tr>
</tbody>
</table>

<a id="rst-v4l2-mpeg-audio-mode"></a>

- **`V4L2_CID_MPEG_AUDIO_MODE`**

  (enum)

- **enum v4l2\_mpeg\_audio\_mode -**

  MPEG Audio mode. Possible values are:


<table>
<tbody>
<tr>
<td>



`V4L2_MPEG_AUDIO_MODE_STEREO`

</td>
<td>



Stereo

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_MODE_JOINT_STEREO`

</td>
<td>



Joint Stereo

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_MODE_DUAL`

</td>
<td>



Bilingual

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_MODE_MONO`

</td>
<td>



Mono

</td>
</tr>
</tbody>
</table>

<a id="rst-v4l2-mpeg-audio-mode-extension"></a>

- **`V4L2_CID_MPEG_AUDIO_MODE_EXTENSION`**

  (enum)

- **enum v4l2\_mpeg\_audio\_mode\_extension -**

  Joint Stereo audio mode extension. In Layer I and II they indicate which subbands are in intensity stereo. All other subbands are coded in stereo. Layer III is not (yet) supported. Possible values are:

<!-- tabularcolumns: |p{9.1cm}|p{8.4cm}| -->


<table>
<tbody>
<tr>
<td>



`V4L2_MPEG_AUDIO_MODE_EXTENSION_BOUND_4`

</td>
<td>



Subbands 4-31 in intensity stereo

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_MODE_EXTENSION_BOUND_8`

</td>
<td>



Subbands 8-31 in intensity stereo

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_MODE_EXTENSION_BOUND_12`

</td>
<td>



Subbands 12-31 in intensity stereo

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_MODE_EXTENSION_BOUND_16`

</td>
<td>



Subbands 16-31 in intensity stereo

</td>
</tr>
</tbody>
</table>

<a id="rst-v4l2-mpeg-audio-emphasis"></a>

- **`V4L2_CID_MPEG_AUDIO_EMPHASIS`**

  (enum)

- **enum v4l2\_mpeg\_audio\_emphasis -**

  Audio Emphasis. Possible values are:


<table>
<tbody>
<tr>
<td>



`V4L2_MPEG_AUDIO_EMPHASIS_NONE`

</td>
<td>



None

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_EMPHASIS_50_DIV_15_uS`

</td>
<td>



50/15 microsecond emphasis

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_EMPHASIS_CCITT_J17`

</td>
<td>



CCITT J.17

</td>
</tr>
</tbody>
</table>

<a id="rst-v4l2-mpeg-audio-crc"></a>

- **`V4L2_CID_MPEG_AUDIO_CRC`**

  (enum)

- **enum v4l2\_mpeg\_audio\_crc -**

  CRC method. Possible values are:


<table>
<tbody>
<tr>
<td>



`V4L2_MPEG_AUDIO_CRC_NONE`

</td>
<td>



None

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_CRC_CRC16`

</td>
<td>



16 bit parity check

</td>
</tr>
</tbody>
</table>

- **`V4L2_CID_MPEG_AUDIO_MUTE (boolean)`**

  Mutes the audio when capturing. This is not done by muting audio hardware, which can still produce a slight hiss, but in the encoder itself, guaranteeing a fixed and reproducible audio bitstream. 0 = unmuted, 1 = muted.

<a id="rst-v4l2-mpeg-audio-dec-playback"></a>

- **`V4L2_CID_MPEG_AUDIO_DEC_PLAYBACK`**

  (enum)

- **enum v4l2\_mpeg\_audio\_dec\_playback -**

  Determines how monolingual audio should be played back. Possible values are:

<!-- tabularcolumns: |p{9.8cm}|p{7.7cm}| -->


<table>
<tbody>
<tr>
<td>



`V4L2_MPEG_AUDIO_DEC_PLAYBACK_AUTO`

</td>
<td>



Automatically determines the best playback mode.

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_DEC_PLAYBACK_STEREO`

</td>
<td>



Stereo playback.

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_DEC_PLAYBACK_LEFT`

</td>
<td>



Left channel playback.

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_DEC_PLAYBACK_RIGHT`

</td>
<td>



Right channel playback.

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_DEC_PLAYBACK_MONO`

</td>
<td>



Mono playback.

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_AUDIO_DEC_PLAYBACK_SWAPPED_STEREO`

</td>
<td>



Stereo playback with swapped left and right channels.

</td>
</tr>
</tbody>
</table>

<a id="rst-v4l2-mpeg-audio-dec-multilingual-playback"></a>

- **`V4L2_CID_MPEG_AUDIO_DEC_MULTILINGUAL_PLAYBACK`**

  (enum)

- **enum v4l2\_mpeg\_audio\_dec\_playback -**

  Determines how multilingual audio should be played back.

<a id="rst-v4l2-mpeg-video-encoding"></a>

- **`V4L2_CID_MPEG_VIDEO_ENCODING`**

  (enum)

- **enum v4l2\_mpeg\_video\_encoding -**

  MPEG Video encoding method. This control is specific to multiplexed MPEG streams. Possible values are:


<table>
<tbody>
<tr>
<td>



`V4L2_MPEG_VIDEO_ENCODING_MPEG_1`

</td>
<td>



MPEG-1 Video encoding

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_ENCODING_MPEG_2`

</td>
<td>



MPEG-2 Video encoding

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_ENCODING_MPEG_4_AVC`

</td>
<td>



MPEG-4 AVC (H.264) Video encoding

</td>
</tr>
</tbody>
</table>

<a id="rst-v4l2-mpeg-video-aspect"></a>

- **`V4L2_CID_MPEG_VIDEO_ASPECT`**

  (enum)

- **enum v4l2\_mpeg\_video\_aspect -**

  Video aspect. Possible values are:


<table>
<tbody>
<tr>
<td>



`V4L2_MPEG_VIDEO_ASPECT_1x1`

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_ASPECT_4x3`

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_ASPECT_16x9`

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_ASPECT_221x100`

</td>
</tr>
</tbody>
</table>

- **`V4L2_CID_MPEG_VIDEO_B_FRAMES (integer)`**

  Number of B-Frames (default 2)

- **`V4L2_CID_MPEG_VIDEO_GOP_SIZE (integer)`**

  GOP size (default 12)

- **`V4L2_CID_MPEG_VIDEO_GOP_CLOSURE (boolean)`**

  GOP closure (default 1)

- **`V4L2_CID_MPEG_VIDEO_PULLDOWN (boolean)`**

  Enable 3:2 pulldown (default 0)

<a id="rst-v4l2-mpeg-video-bitrate-mode"></a>

- **`V4L2_CID_MPEG_VIDEO_BITRATE_MODE`**

  (enum)

- **enum v4l2\_mpeg\_video\_bitrate\_mode -**

  Video bitrate mode. Possible values are:


<table>
<tbody>
<tr>
<td>



`V4L2_MPEG_VIDEO_BITRATE_MODE_VBR`

</td>
<td>



Variable bitrate

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_BITRATE_MODE_CBR`

</td>
<td>



Constant bitrate

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_BITRATE_MODE_CQ`

</td>
<td>



Constant quality

</td>
</tr>
</tbody>
</table>

- **`V4L2_CID_MPEG_VIDEO_BITRATE (integer)`**

  Average video bitrate in bits per second.

- **`V4L2_CID_MPEG_VIDEO_BITRATE_PEAK (integer)`**

  Peak video bitrate in bits per second. Must be larger or equal to the average video bitrate. It is ignored if the video bitrate mode is set to constant bitrate.

- **`V4L2_CID_MPEG_VIDEO_CONSTANT_QUALITY (integer)`**

  Constant quality level control. This control is applicable when `V4L2_CID_MPEG_VIDEO_BITRATE_MODE` value is `V4L2_MPEG_VIDEO_BITRATE_MODE_CQ`. Valid range is 1 to 100 where 1 indicates lowest quality and 100 indicates highest quality. Encoder will decide the appropriate quantization parameter and bitrate to produce requested frame quality.

`V4L2_CID_MPEG_VIDEO_FRAME_SKIP_MODE (enum)`

- **enum v4l2\_mpeg\_video\_frame\_skip\_mode -**

  Indicates in what conditions the encoder should skip frames. If encoding a frame would cause the encoded stream to be larger then a chosen data limit then the frame will be skipped. Possible values are:

<!-- tabularcolumns: |p{8.2cm}|p{9.3cm}| -->

<!-- Source LaTeX layout: \small -->


<table>
<tbody>
<tr>
<td>



`V4L2_MPEG_VIDEO_FRAME_SKIP_MODE_DISABLED`

</td>
<td>



Frame skip mode is disabled.

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_FRAME_SKIP_MODE_LEVEL_LIMIT`

</td>
<td>



Frame skip mode enabled and buffer limit is set by the chosen level and is defined by the standard.

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_FRAME_SKIP_MODE_BUF_LIMIT`

</td>
<td>



Frame skip mode enabled and buffer limit is set by the [VBV (MPEG1/2/4)](<#rst-v4l2-mpeg-video-vbv-size>) or [CPB (H264) buffer size](<#rst-v4l2-mpeg-video-h264-cpb-size>) control.

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

- **`V4L2_CID_MPEG_VIDEO_TEMPORAL_DECIMATION (integer)`**

  For every captured frame, skip this many subsequent frames (default 0).

- **`V4L2_CID_MPEG_VIDEO_MUTE (boolean)`**

  "Mutes" the video to a fixed color when capturing. This is useful for testing, to produce a fixed video bitstream. 0 = unmuted, 1 = muted.

- **`V4L2_CID_MPEG_VIDEO_MUTE_YUV (integer)`**

  Sets the "mute" color of the video. The supplied 32-bit integer is interpreted as follows (bit 0 = least significant bit):


<table>
<tbody>
<tr>
<td>



Bit 0:7

</td>
<td>



V chrominance information

</td>
</tr>
<tr>
<td>



Bit 8:15

</td>
<td>



U chrominance information

</td>
</tr>
<tr>
<td>



Bit 16:23

</td>
<td>



Y luminance information

</td>
</tr>
<tr>
<td>



Bit 24:31

</td>
<td>



Must be zero.

</td>
</tr>
</tbody>
</table>

<a id="rst-v4l2-mpeg-video-dec-pts"></a>

- **`V4L2_CID_MPEG_VIDEO_DEC_PTS (integer64)`**

  This read-only control returns the 33-bit video Presentation Time Stamp as defined in ITU T-REC-H.222.0 and ISO/IEC 13818-1 of the currently displayed frame. This is the same PTS as is used in [vidioc\_decoder\_cmd](<~kernel/userspace/userspace-api/media-v4l/vidioc-decoder-cmd#rst-vidioc-decoder-cmd>).

<a id="rst-v4l2-mpeg-video-dec-frame"></a>

- **`V4L2_CID_MPEG_VIDEO_DEC_FRAME (integer64)`**

  This read-only control returns the frame counter of the frame that is currently displayed (decoded). This value is reset to 0 whenever the decoder is started.

- **`V4L2_CID_MPEG_VIDEO_DEC_CONCEAL_COLOR (integer64)`**

  This control sets the conceal color in YUV color space. It describes the client preference of the error conceal color in case of an error where the reference frame is missing. The decoder should fill the reference buffer with the preferred color and use it for future decoding. The control is using 16 bits per channel. Applicable to decoders.


<table>
<tbody>
<tr>
<td>





</td>
<td>



8bit  format

</td>
<td>



10bit format

</td>
<td>



12bit format

</td>
</tr>
<tr>
<td>



Y luminance

</td>
<td>



Bit 0:7

</td>
<td>



Bit 0:9

</td>
<td>



Bit 0:11

</td>
</tr>
<tr>
<td>



Cb chrominance

</td>
<td>



Bit 16:23

</td>
<td>



Bit 16:25

</td>
<td>



Bit 16:27

</td>
</tr>
<tr>
<td>



Cr chrominance

</td>
<td>



Bit 32:39

</td>
<td>



Bit 32:41

</td>
<td>



Bit 32:43

</td>
</tr>
<tr>
<td>



Must be zero

</td>
<td>



Bit 48:63

</td>
<td>



Bit 48:63

</td>
<td>



Bit 48:63

</td>
</tr>
</tbody>
</table>

- **`V4L2_CID_MPEG_VIDEO_DECODER_SLICE_INTERFACE (boolean)`**

  If enabled the decoder expects to receive a single slice per buffer, otherwise the decoder expects a single frame in per buffer. Applicable to the decoder, all codecs.

- **`V4L2_CID_MPEG_VIDEO_DEC_DISPLAY_DELAY_ENABLE (boolean)`**

  If the display delay is enabled then the decoder is forced to return a CAPTURE buffer (decoded frame) after processing a certain number of OUTPUT buffers. The delay can be set through `V4L2_CID_MPEG_VIDEO_DEC_DISPLAY_DELAY`. This feature can be used for example for generating thumbnails of videos. Applicable to the decoder.

- **`V4L2_CID_MPEG_VIDEO_DEC_DISPLAY_DELAY (integer)`**

  Display delay value for decoder. The decoder is forced to return a decoded frame after the set 'display delay' number of frames. If this number is low it may result in frames returned out of display order, in addition the hardware may still be using the returned buffer as a reference picture for subsequent frames.

- **`V4L2_CID_MPEG_VIDEO_AU_DELIMITER (boolean)`**

  If enabled then, AUD (Access Unit Delimiter) NALUs will be generated. That could be useful to find the start of a frame without having to fully parse each NALU. Applicable to the H264 and HEVC encoders.

- **`V4L2_CID_MPEG_VIDEO_H264_VUI_SAR_ENABLE (boolean)`**

  Enable writing sample aspect ratio in the Video Usability Information. Applicable to the H264 encoder.

<a id="rst-v4l2-mpeg-video-h264-vui-sar-idc"></a>

- **`V4L2_CID_MPEG_VIDEO_H264_VUI_SAR_IDC`**

  (enum)

- **enum v4l2\_mpeg\_video\_h264\_vui\_sar\_idc -**

  VUI sample aspect ratio indicator for H.264 encoding. The value is defined in the table E-1 in the standard. Applicable to the H264 encoder.


<table>
<tbody>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_VUI_SAR_IDC_UNSPECIFIED`

</td>
<td>



Unspecified

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_VUI_SAR_IDC_1x1`

</td>
<td>



1x1

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_VUI_SAR_IDC_12x11`

</td>
<td>



12x11

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_VUI_SAR_IDC_10x11`

</td>
<td>



10x11

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_VUI_SAR_IDC_16x11`

</td>
<td>



16x11

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_VUI_SAR_IDC_40x33`

</td>
<td>



40x33

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_VUI_SAR_IDC_24x11`

</td>
<td>



24x11

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_VUI_SAR_IDC_20x11`

</td>
<td>



20x11

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_VUI_SAR_IDC_32x11`

</td>
<td>



32x11

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_VUI_SAR_IDC_80x33`

</td>
<td>



80x33

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_VUI_SAR_IDC_18x11`

</td>
<td>



18x11

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_VUI_SAR_IDC_15x11`

</td>
<td>



15x11

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_VUI_SAR_IDC_64x33`

</td>
<td>



64x33

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_VUI_SAR_IDC_160x99`

</td>
<td>



160x99

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_VUI_SAR_IDC_4x3`

</td>
<td>



4x3

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_VUI_SAR_IDC_3x2`

</td>
<td>



3x2

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_VUI_SAR_IDC_2x1`

</td>
<td>



2x1

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_VUI_SAR_IDC_EXTENDED`

</td>
<td>



Extended SAR

</td>
</tr>
</tbody>
</table>

- **`V4L2_CID_MPEG_VIDEO_H264_VUI_EXT_SAR_WIDTH (integer)`**

  Extended sample aspect ratio width for H.264 VUI encoding. Applicable to the H264 encoder.

- **`V4L2_CID_MPEG_VIDEO_H264_VUI_EXT_SAR_HEIGHT (integer)`**

  Extended sample aspect ratio height for H.264 VUI encoding. Applicable to the H264 encoder.

<a id="rst-v4l2-mpeg-video-h264-level"></a>

- **`V4L2_CID_MPEG_VIDEO_H264_LEVEL`**

  (enum)

- **enum v4l2\_mpeg\_video\_h264\_level -**

  The level information for the H264 video elementary stream. Applicable to the H264 encoder. Possible values are:


<table>
<tbody>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_LEVEL_1_0`

</td>
<td>



Level 1.0

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_LEVEL_1B`

</td>
<td>



Level 1B

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_LEVEL_1_1`

</td>
<td>



Level 1.1

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_LEVEL_1_2`

</td>
<td>



Level 1.2

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_LEVEL_1_3`

</td>
<td>



Level 1.3

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_LEVEL_2_0`

</td>
<td>



Level 2.0

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_LEVEL_2_1`

</td>
<td>



Level 2.1

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_LEVEL_2_2`

</td>
<td>



Level 2.2

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_LEVEL_3_0`

</td>
<td>



Level 3.0

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_LEVEL_3_1`

</td>
<td>



Level 3.1

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_LEVEL_3_2`

</td>
<td>



Level 3.2

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_LEVEL_4_0`

</td>
<td>



Level 4.0

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_LEVEL_4_1`

</td>
<td>



Level 4.1

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_LEVEL_4_2`

</td>
<td>



Level 4.2

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_LEVEL_5_0`

</td>
<td>



Level 5.0

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_LEVEL_5_1`

</td>
<td>



Level 5.1

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_LEVEL_5_2`

</td>
<td>



Level 5.2

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_LEVEL_6_0`

</td>
<td>



Level 6.0

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_LEVEL_6_1`

</td>
<td>



Level 6.1

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_LEVEL_6_2`

</td>
<td>



Level 6.2

</td>
</tr>
</tbody>
</table>

<a id="rst-v4l2-mpeg-video-mpeg2-level"></a>

- **`V4L2_CID_MPEG_VIDEO_MPEG2_LEVEL`**

  (enum)

- **enum v4l2\_mpeg\_video\_mpeg2\_level -**

  The level information for the MPEG2 elementary stream. Applicable to MPEG2 codecs. Possible values are:


<table>
<tbody>
<tr>
<td>



`V4L2_MPEG_VIDEO_MPEG2_LEVEL_LOW`

</td>
<td>



Low Level (LL)

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_MPEG2_LEVEL_MAIN`

</td>
<td>



Main Level (ML)

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_MPEG2_LEVEL_HIGH_1440`

</td>
<td>



High-1440 Level (H-14)

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_MPEG2_LEVEL_HIGH`

</td>
<td>



High Level (HL)

</td>
</tr>
</tbody>
</table>

<a id="rst-v4l2-mpeg-video-mpeg4-level"></a>

- **`V4L2_CID_MPEG_VIDEO_MPEG4_LEVEL`**

  (enum)

- **enum v4l2\_mpeg\_video\_mpeg4\_level -**

  The level information for the MPEG4 elementary stream. Applicable to the MPEG4 encoder. Possible values are:


<table>
<tbody>
<tr>
<td>



`V4L2_MPEG_VIDEO_MPEG4_LEVEL_0`

</td>
<td>



Level 0

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_MPEG4_LEVEL_0B`

</td>
<td>



Level 0b

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_MPEG4_LEVEL_1`

</td>
<td>



Level 1

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_MPEG4_LEVEL_2`

</td>
<td>



Level 2

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_MPEG4_LEVEL_3`

</td>
<td>



Level 3

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_MPEG4_LEVEL_3B`

</td>
<td>



Level 3b

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_MPEG4_LEVEL_4`

</td>
<td>



Level 4

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_MPEG4_LEVEL_5`

</td>
<td>



Level 5

</td>
</tr>
</tbody>
</table>

<a id="rst-v4l2-mpeg-video-h264-profile"></a>

- **`V4L2_CID_MPEG_VIDEO_H264_PROFILE`**

  (enum)

- **enum v4l2\_mpeg\_video\_h264\_profile -**

  The profile information for H264. Applicable to the H264 encoder. Possible values are:

<!-- Source LaTeX layout: \small -->

<!-- tabularcolumns: |p{10.2cm}|p{7.3cm}| -->


<table>
<tbody>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_PROFILE_BASELINE`

</td>
<td>



Baseline profile

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_PROFILE_CONSTRAINED_BASELINE`

</td>
<td>



Constrained Baseline profile

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_PROFILE_MAIN`

</td>
<td>



Main profile

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_PROFILE_EXTENDED`

</td>
<td>



Extended profile

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_PROFILE_HIGH`

</td>
<td>



High profile

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_PROFILE_HIGH_10`

</td>
<td>



High 10 profile

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_PROFILE_HIGH_422`

</td>
<td>



High 422 profile

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_PROFILE_HIGH_444_PREDICTIVE`

</td>
<td>



High 444 Predictive profile

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_PROFILE_HIGH_10_INTRA`

</td>
<td>



High 10 Intra profile

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_PROFILE_HIGH_422_INTRA`

</td>
<td>



High 422 Intra profile

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_PROFILE_HIGH_444_INTRA`

</td>
<td>



High 444 Intra profile

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_PROFILE_CAVLC_444_INTRA`

</td>
<td>



CAVLC 444 Intra profile

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_PROFILE_SCALABLE_BASELINE`

</td>
<td>



Scalable Baseline profile

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_PROFILE_SCALABLE_HIGH`

</td>
<td>



Scalable High profile

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_PROFILE_SCALABLE_HIGH_INTRA`

</td>
<td>



Scalable High Intra profile

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_PROFILE_STEREO_HIGH`

</td>
<td>



Stereo High profile

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_PROFILE_MULTIVIEW_HIGH`

</td>
<td>



Multiview High profile

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_PROFILE_CONSTRAINED_HIGH`

</td>
<td>



Constrained High profile

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

<a id="rst-v4l2-mpeg-video-mpeg2-profile"></a>

- **`V4L2_CID_MPEG_VIDEO_MPEG2_PROFILE`**

  (enum)

- **enum v4l2\_mpeg\_video\_mpeg2\_profile -**

  The profile information for MPEG2. Applicable to MPEG2 codecs. Possible values are:

<!-- Source LaTeX layout: \small -->

<!-- tabularcolumns: |p{10.2cm}|p{7.3cm}| -->


<table>
<tbody>
<tr>
<td>



`V4L2_MPEG_VIDEO_MPEG2_PROFILE_SIMPLE`

</td>
<td>



Simple profile (SP)

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_MPEG2_PROFILE_MAIN`

</td>
<td>



Main profile (MP)

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_MPEG2_PROFILE_SNR_SCALABLE`

</td>
<td>



SNR Scalable profile (SNR)

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_MPEG2_PROFILE_SPATIALLY_SCALABLE`

</td>
<td>



Spatially Scalable profile (Spt)

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_MPEG2_PROFILE_HIGH`

</td>
<td>



High profile (HP)

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_MPEG2_PROFILE_MULTIVIEW`

</td>
<td>



Multi-view profile (MVP)

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

<a id="rst-v4l2-mpeg-video-mpeg4-profile"></a>

- **`V4L2_CID_MPEG_VIDEO_MPEG4_PROFILE`**

  (enum)

- **enum v4l2\_mpeg\_video\_mpeg4\_profile -**

  The profile information for MPEG4. Applicable to the MPEG4 encoder. Possible values are:

<!-- Source LaTeX layout: \small -->

<!-- tabularcolumns: |p{11.8cm}|p{5.7cm}| -->


<table>
<tbody>
<tr>
<td>



`V4L2_MPEG_VIDEO_MPEG4_PROFILE_SIMPLE`

</td>
<td>



Simple profile

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_MPEG4_PROFILE_ADVANCED_SIMPLE`

</td>
<td>



Advanced Simple profile

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_MPEG4_PROFILE_CORE`

</td>
<td>



Core profile

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_MPEG4_PROFILE_SIMPLE_SCALABLE`

</td>
<td>



Simple Scalable profile

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_MPEG4_PROFILE_ADVANCED_CODING_EFFICIENCY`

</td>
<td>



Advanced Coding Efficiency profile

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

- **`V4L2_CID_MPEG_VIDEO_MAX_REF_PIC (integer)`**

  The maximum number of reference pictures used for encoding. Applicable to the encoder.

<a id="rst-v4l2-mpeg-video-multi-slice-mode"></a>

- **`V4L2_CID_MPEG_VIDEO_MULTI_SLICE_MODE`**

  (enum)

- **enum v4l2\_mpeg\_video\_multi\_slice\_mode -**

  Determines how the encoder should handle division of frame into slices. Applicable to the encoder. Possible values are:

<!-- tabularcolumns: |p{9.6cm}|p{7.9cm}| -->


<table>
<tbody>
<tr>
<td>



`V4L2_MPEG_VIDEO_MULTI_SLICE_MODE_SINGLE`

</td>
<td>



Single slice per frame.

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_MULTI_SLICE_MODE_MAX_MB`

</td>
<td>



Multiple slices with set maximum number of macroblocks per slice.

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_MULTI_SLICE_MODE_MAX_BYTES`

</td>
<td>



Multiple slice with set maximum size in bytes per slice.

</td>
</tr>
</tbody>
</table>

- **`V4L2_CID_MPEG_VIDEO_MULTI_SLICE_MAX_MB (integer)`**

  The maximum number of macroblocks in a slice. Used when `V4L2_CID_MPEG_VIDEO_MULTI_SLICE_MODE` is set to `V4L2_MPEG_VIDEO_MULTI_SLICE_MODE_MAX_MB`. Applicable to the encoder.

- **`V4L2_CID_MPEG_VIDEO_MULTI_SLICE_MAX_BYTES (integer)`**

  The maximum size of a slice in bytes. Used when `V4L2_CID_MPEG_VIDEO_MULTI_SLICE_MODE` is set to `V4L2_MPEG_VIDEO_MULTI_SLICE_MODE_MAX_BYTES`. Applicable to the encoder.

<a id="rst-v4l2-mpeg-video-h264-loop-filter-mode"></a>

- **`V4L2_CID_MPEG_VIDEO_H264_LOOP_FILTER_MODE`**

  (enum)

- **enum v4l2\_mpeg\_video\_h264\_loop\_filter\_mode -**

  Loop filter mode for H264 encoder. Possible values are:

<!-- Source LaTeX layout: \small -->

<!-- tabularcolumns: |p{13.5cm}|p{4.0cm}| -->


<table>
<tbody>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_LOOP_FILTER_MODE_ENABLED`

</td>
<td>



Loop filter is enabled.

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_LOOP_FILTER_MODE_DISABLED`

</td>
<td>



Loop filter is disabled.

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_LOOP_FILTER_MODE_DISABLED_AT_SLICE_BOUNDARY`

</td>
<td>



Loop filter is disabled at the slice boundary.

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

- **`V4L2_CID_MPEG_VIDEO_H264_LOOP_FILTER_ALPHA (integer)`**

  Loop filter alpha coefficient, defined in the H264 standard. This value corresponds to the slice\_alpha\_c0\_offset\_div2 slice header field, and should be in the range of -6 to +6, inclusive. The actual alpha offset FilterOffsetA is twice this value. Applicable to the H264 encoder.

- **`V4L2_CID_MPEG_VIDEO_H264_LOOP_FILTER_BETA (integer)`**

  Loop filter beta coefficient, defined in the H264 standard. This corresponds to the slice\_beta\_offset\_div2 slice header field, and should be in the range of -6 to +6, inclusive. The actual beta offset FilterOffsetB is twice this value. Applicable to the H264 encoder.

<a id="rst-v4l2-mpeg-video-h264-entropy-mode"></a>

- **`V4L2_CID_MPEG_VIDEO_H264_ENTROPY_MODE`**

  (enum)

- **enum v4l2\_mpeg\_video\_h264\_entropy\_mode -**

  Entropy coding mode for H264 - CABAC/CAVALC. Applicable to the H264 encoder. Possible values are:

<!-- tabularcolumns: |p{9.0cm}|p{8.5cm}| -->


<table>
<tbody>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_ENTROPY_MODE_CAVLC`

</td>
<td>



Use CAVLC entropy coding.

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_ENTROPY_MODE_CABAC`

</td>
<td>



Use CABAC entropy coding.

</td>
</tr>
</tbody>
</table>

- **`V4L2_CID_MPEG_VIDEO_H264_8X8_TRANSFORM (boolean)`**

  Enable 8X8 transform for H264. Applicable to the H264 encoder.

- **`V4L2_CID_MPEG_VIDEO_H264_CONSTRAINED_INTRA_PREDICTION (boolean)`**

  Enable constrained intra prediction for H264. Applicable to the H264 encoder.

- **`V4L2_CID_MPEG_VIDEO_H264_CHROMA_QP_INDEX_OFFSET (integer)`**

  Specify the offset that should be added to the luma quantization parameter to determine the chroma quantization parameter. Applicable to the H264 encoder.

- **`V4L2_CID_MPEG_VIDEO_CYCLIC_INTRA_REFRESH_MB (integer)`**

  Cyclic intra macroblock refresh. This is the number of continuous macroblocks refreshed every frame. Each frame a successive set of macroblocks is refreshed until the cycle completes and starts from the top of the frame. Setting this control to zero means that macroblocks will not be refreshed.  Note that this control will not take effect when `V4L2_CID_MPEG_VIDEO_INTRA_REFRESH_PERIOD` control is set to non zero value. Applicable to H264, H263 and MPEG4 encoder.

`V4L2_CID_MPEG_VIDEO_INTRA_REFRESH_PERIOD_TYPE (enum)`

- **enum v4l2\_mpeg\_video\_intra\_refresh\_period\_type -**

  Sets the type of intra refresh. The period to refresh the whole frame is specified by V4L2\_CID\_MPEG\_VIDEO\_INTRA\_REFRESH\_PERIOD. Note that if this control is not present, then it is undefined what refresh type is used and it is up to the driver to decide. Applicable to H264 and HEVC encoders. Possible values are:

<!-- tabularcolumns: |p{9.6cm}|p{7.9cm}| -->


<table>
<tbody>
<tr>
<td>



`V4L2_MPEG_VIDEO_INTRA_REFRESH_PERIOD_TYPE_RANDOM`

</td>
<td>



The whole frame is completely refreshed randomly after the specified period.

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_INTRA_REFRESH_PERIOD_TYPE_CYCLIC`

</td>
<td>



The whole frame MBs are completely refreshed in cyclic order after the specified period.

</td>
</tr>
</tbody>
</table>

- **`V4L2_CID_MPEG_VIDEO_INTRA_REFRESH_PERIOD (integer)`**

  Intra macroblock refresh period. This sets the period to refresh the whole frame. In other words, this defines the number of frames for which the whole frame will be intra-refreshed.  An example: setting period to 1 means that the whole frame will be refreshed, setting period to 2 means that the half of macroblocks will be intra-refreshed on frameX and the other half of macroblocks will be refreshed in frameX + 1 and so on. Setting the period to zero means no period is specified. Note that if the client sets this control to non zero value the `V4L2_CID_MPEG_VIDEO_CYCLIC_INTRA_REFRESH_MB` control shall be ignored. Applicable to H264 and HEVC encoders.

- **`V4L2_CID_MPEG_VIDEO_FRAME_RC_ENABLE (boolean)`**

  Frame level rate control enable. If this control is disabled then the quantization parameter for each frame type is constant and set with appropriate controls (e.g. `V4L2_CID_MPEG_VIDEO_H263_I_FRAME_QP`). If frame rate control is enabled then quantization parameter is adjusted to meet the chosen bitrate. Minimum and maximum value for the quantization parameter can be set with appropriate controls (e.g. `V4L2_CID_MPEG_VIDEO_H263_MIN_QP`). Applicable to encoders.

- **`V4L2_CID_MPEG_VIDEO_MB_RC_ENABLE (boolean)`**

  Macroblock level rate control enable. Applicable to the MPEG4 and H264 encoders.

- **`V4L2_CID_MPEG_VIDEO_MPEG4_QPEL (boolean)`**

  Quarter pixel motion estimation for MPEG4. Applicable to the MPEG4 encoder.

- **`V4L2_CID_MPEG_VIDEO_H263_I_FRAME_QP (integer)`**

  Quantization parameter for an I frame for H263. Valid range: from 1 to 31.

- **`V4L2_CID_MPEG_VIDEO_H263_MIN_QP (integer)`**

  Minimum quantization parameter for H263. Valid range: from 1 to 31.

- **`V4L2_CID_MPEG_VIDEO_H263_MAX_QP (integer)`**

  Maximum quantization parameter for H263. Valid range: from 1 to 31.

- **`V4L2_CID_MPEG_VIDEO_H263_P_FRAME_QP (integer)`**

  Quantization parameter for an P frame for H263. Valid range: from 1 to 31.

- **`V4L2_CID_MPEG_VIDEO_H263_B_FRAME_QP (integer)`**

  Quantization parameter for an B frame for H263. Valid range: from 1 to 31.

- **`V4L2_CID_MPEG_VIDEO_H264_I_FRAME_QP (integer)`**

  Quantization parameter for an I frame for H264. Valid range: from 0 to 51.

- **`V4L2_CID_MPEG_VIDEO_H264_MIN_QP (integer)`**

  Minimum quantization parameter for H264. Valid range: from 0 to 51.

- **`V4L2_CID_MPEG_VIDEO_H264_MAX_QP (integer)`**

  Maximum quantization parameter for H264. Valid range: from 0 to 51.

- **`V4L2_CID_MPEG_VIDEO_H264_P_FRAME_QP (integer)`**

  Quantization parameter for an P frame for H264. Valid range: from 0 to 51.

- **`V4L2_CID_MPEG_VIDEO_H264_B_FRAME_QP (integer)`**

  Quantization parameter for an B frame for H264. Valid range: from 0 to 51.

- **`V4L2_CID_MPEG_VIDEO_H264_I_FRAME_MIN_QP (integer)`**

  Minimum quantization parameter for the H264 I frame to limit I frame quality to a range. Valid range: from 0 to 51. If V4L2\_CID\_MPEG\_VIDEO\_H264\_MIN\_QP is also set, the quantization parameter should be chosen to meet both requirements.

- **`V4L2_CID_MPEG_VIDEO_H264_I_FRAME_MAX_QP (integer)`**

  Maximum quantization parameter for the H264 I frame to limit I frame quality to a range. Valid range: from 0 to 51. If V4L2\_CID\_MPEG\_VIDEO\_H264\_MAX\_QP is also set, the quantization parameter should be chosen to meet both requirements.

- **`V4L2_CID_MPEG_VIDEO_H264_P_FRAME_MIN_QP (integer)`**

  Minimum quantization parameter for the H264 P frame to limit P frame quality to a range. Valid range: from 0 to 51. If V4L2\_CID\_MPEG\_VIDEO\_H264\_MIN\_QP is also set, the quantization parameter should be chosen to meet both requirements.

- **`V4L2_CID_MPEG_VIDEO_H264_P_FRAME_MAX_QP (integer)`**

  Maximum quantization parameter for the H264 P frame to limit P frame quality to a range. Valid range: from 0 to 51. If V4L2\_CID\_MPEG\_VIDEO\_H264\_MAX\_QP is also set, the quantization parameter should be chosen to meet both requirements.

- **`V4L2_CID_MPEG_VIDEO_H264_B_FRAME_MIN_QP (integer)`**

  Minimum quantization parameter for the H264 B frame to limit B frame quality to a range. Valid range: from 0 to 51. If V4L2\_CID\_MPEG\_VIDEO\_H264\_MIN\_QP is also set, the quantization parameter should be chosen to meet both requirements.

- **`V4L2_CID_MPEG_VIDEO_H264_B_FRAME_MAX_QP (integer)`**

  Maximum quantization parameter for the H264 B frame to limit B frame quality to a range. Valid range: from 0 to 51. If V4L2\_CID\_MPEG\_VIDEO\_H264\_MAX\_QP is also set, the quantization parameter should be chosen to meet both requirements.

- **`V4L2_CID_MPEG_VIDEO_MPEG4_I_FRAME_QP (integer)`**

  Quantization parameter for an I frame for MPEG4. Valid range: from 1 to 31.

- **`V4L2_CID_MPEG_VIDEO_MPEG4_MIN_QP (integer)`**

  Minimum quantization parameter for MPEG4. Valid range: from 1 to 31.

- **`V4L2_CID_MPEG_VIDEO_MPEG4_MAX_QP (integer)`**

  Maximum quantization parameter for MPEG4. Valid range: from 1 to 31.

- **`V4L2_CID_MPEG_VIDEO_MPEG4_P_FRAME_QP (integer)`**

  Quantization parameter for an P frame for MPEG4. Valid range: from 1 to 31.

- **`V4L2_CID_MPEG_VIDEO_MPEG4_B_FRAME_QP (integer)`**

  Quantization parameter for an B frame for MPEG4. Valid range: from 1 to 31.

<a id="rst-v4l2-mpeg-video-vbv-size"></a>

- **`V4L2_CID_MPEG_VIDEO_VBV_SIZE (integer)`**

  The Video Buffer Verifier size in kilobytes, it is used as a limitation of frame skip. The VBV is defined in the standard as a mean to verify that the produced stream will be successfully decoded. The standard describes it as "Part of a hypothetical decoder that is conceptually connected to the output of the encoder. Its purpose is to provide a constraint on the variability of the data rate that an encoder or editing process may produce.". Applicable to the MPEG1, MPEG2, MPEG4 encoders.

<a id="rst-v4l2-mpeg-video-vbv-delay"></a>

- **`V4L2_CID_MPEG_VIDEO_VBV_DELAY (integer)`**

  Sets the initial delay in milliseconds for VBV buffer control.

<a id="rst-v4l2-mpeg-video-hor-search-range"></a>

- **`V4L2_CID_MPEG_VIDEO_MV_H_SEARCH_RANGE (integer)`**

  Horizontal search range defines maximum horizontal search area in pixels to search and match for the present Macroblock (MB) in the reference picture. This V4L2 control macro is used to set horizontal search range for motion estimation module in video encoder.

<a id="rst-v4l2-mpeg-video-vert-search-range"></a>

- **`V4L2_CID_MPEG_VIDEO_MV_V_SEARCH_RANGE (integer)`**

  Vertical search range defines maximum vertical search area in pixels to search and match for the present Macroblock (MB) in the reference picture. This V4L2 control macro is used to set vertical search range for motion estimation module in video encoder.

<a id="rst-v4l2-mpeg-video-force-key-frame"></a>

- **`V4L2_CID_MPEG_VIDEO_FORCE_KEY_FRAME (button)`**

  Force a key frame for the next queued buffer. Applicable to encoders. This is a general, codec-agnostic keyframe control.

<a id="rst-v4l2-mpeg-video-h264-cpb-size"></a>

- **`V4L2_CID_MPEG_VIDEO_H264_CPB_SIZE (integer)`**

  The Coded Picture Buffer size in kilobytes, it is used as a limitation of frame skip. The CPB is defined in the H264 standard as a mean to verify that the produced stream will be successfully decoded. Applicable to the H264 encoder.

- **`V4L2_CID_MPEG_VIDEO_H264_I_PERIOD (integer)`**

  Period between I-frames in the open GOP for H264. In case of an open GOP this is the period between two I-frames. The period between IDR (Instantaneous Decoding Refresh) frames is taken from the GOP\_SIZE control. An IDR frame, which stands for Instantaneous Decoding Refresh is an I-frame after which no prior frames are referenced. This means that a stream can be restarted from an IDR frame without the need to store or decode any previous frames. Applicable to the H264 encoder.

<a id="rst-v4l2-mpeg-video-header-mode"></a>

- **`V4L2_CID_MPEG_VIDEO_HEADER_MODE`**

  (enum)

- **enum v4l2\_mpeg\_video\_header\_mode -**

  Determines whether the header is returned as the first buffer or is it returned together with the first frame. Applicable to encoders. Possible values are:

<!-- Source LaTeX layout: \small -->

<!-- tabularcolumns: |p{10.3cm}|p{7.2cm}| -->


<table>
<tbody>
<tr>
<td>



`V4L2_MPEG_VIDEO_HEADER_MODE_SEPARATE`

</td>
<td>



The stream header is returned separately in the first buffer.

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_HEADER_MODE_JOINED_WITH_1ST_FRAME`

</td>
<td>



The stream header is returned together with the first encoded frame.

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

- **`V4L2_CID_MPEG_VIDEO_REPEAT_SEQ_HEADER (boolean)`**

  Repeat the video sequence headers. Repeating these headers makes random access to the video stream easier. Applicable to the MPEG1, 2 and 4 encoder.

- **`V4L2_CID_MPEG_VIDEO_DECODER_MPEG4_DEBLOCK_FILTER (boolean)`**

  Enabled the deblocking post processing filter for MPEG4 decoder. Applicable to the MPEG4 decoder.

- **`V4L2_CID_MPEG_VIDEO_MPEG4_VOP_TIME_RES (integer)`**

  vop\_time\_increment\_resolution value for MPEG4. Applicable to the MPEG4 encoder.

- **`V4L2_CID_MPEG_VIDEO_MPEG4_VOP_TIME_INC (integer)`**

  vop\_time\_increment value for MPEG4. Applicable to the MPEG4 encoder.

- **`V4L2_CID_MPEG_VIDEO_H264_SEI_FRAME_PACKING (boolean)`**

  Enable generation of frame packing supplemental enhancement information in the encoded bitstream. The frame packing SEI message contains the arrangement of L and R planes for 3D viewing. Applicable to the H264 encoder.

- **`V4L2_CID_MPEG_VIDEO_H264_SEI_FP_CURRENT_FRAME_0 (boolean)`**

  Sets current frame as frame0 in frame packing SEI. Applicable to the H264 encoder.

<a id="rst-v4l2-mpeg-video-h264-sei-fp-arrangement-type"></a>

- **`V4L2_CID_MPEG_VIDEO_H264_SEI_FP_ARRANGEMENT_TYPE`**

  (enum)

- **enum v4l2\_mpeg\_video\_h264\_sei\_fp\_arrangement\_type -**

  Frame packing arrangement type for H264 SEI. Applicable to the H264 encoder. Possible values are:

<!-- Source LaTeX layout: \small -->

<!-- tabularcolumns: |p{12cm}|p{5.5cm}| -->


<table>
<tbody>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_SEI_FP_ARRANGEMENT_TYPE_CHEKERBOARD`

</td>
<td>



Pixels are alternatively from L and R.

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_SEI_FP_ARRANGEMENT_TYPE_COLUMN`

</td>
<td>



L and R are interlaced by column.

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_SEI_FP_ARRANGEMENT_TYPE_ROW`

</td>
<td>



L and R are interlaced by row.

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_SEI_FP_ARRANGEMENT_TYPE_SIDE_BY_SIDE`

</td>
<td>



L is on the left, R on the right.

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_SEI_FP_ARRANGEMENT_TYPE_TOP_BOTTOM`

</td>
<td>



L is on top, R on bottom.

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_SEI_FP_ARRANGEMENT_TYPE_TEMPORAL`

</td>
<td>



One view per frame.

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

- **`V4L2_CID_MPEG_VIDEO_H264_FMO (boolean)`**

  Enables flexible macroblock ordering in the encoded bitstream. It is a technique used for restructuring the ordering of macroblocks in pictures. Applicable to the H264 encoder.

<a id="rst-v4l2-mpeg-video-h264-fmo-map-type"></a>

- **`V4L2_CID_MPEG_VIDEO_H264_FMO_MAP_TYPE`**

  (enum)

- **enum v4l2\_mpeg\_video\_h264\_fmo\_map\_type -**

  When using FMO, the map type divides the image in different scan patterns of macroblocks. Applicable to the H264 encoder. Possible values are:

<!-- Source LaTeX layout: \small -->

<!-- tabularcolumns: |p{12.5cm}|p{5.0cm}| -->


<table>
<tbody>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_FMO_MAP_TYPE_INTERLEAVED_SLICES`

</td>
<td>



Slices are interleaved one after other with macroblocks in run length order.

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_FMO_MAP_TYPE_SCATTERED_SLICES`

</td>
<td>



Scatters the macroblocks based on a mathematical function known to both encoder and decoder.

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_FMO_MAP_TYPE_FOREGROUND_WITH_LEFT_OVER`

</td>
<td>



Macroblocks arranged in rectangular areas or regions of interest.

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_FMO_MAP_TYPE_BOX_OUT`

</td>
<td>



Slice groups grow in a cyclic way from centre to outwards.

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_FMO_MAP_TYPE_RASTER_SCAN`

</td>
<td>



Slice groups grow in raster scan pattern from left to right.

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_FMO_MAP_TYPE_WIPE_SCAN`

</td>
<td>



Slice groups grow in wipe scan pattern from top to bottom.

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_FMO_MAP_TYPE_EXPLICIT`

</td>
<td>



User defined map type.

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

- **`V4L2_CID_MPEG_VIDEO_H264_FMO_SLICE_GROUP (integer)`**

  Number of slice groups in FMO. Applicable to the H264 encoder.

<a id="rst-v4l2-mpeg-video-h264-fmo-change-direction"></a>

- **`V4L2_CID_MPEG_VIDEO_H264_FMO_CHANGE_DIRECTION`**

  (enum)

- **enum v4l2\_mpeg\_video\_h264\_fmo\_change\_dir -**

  Specifies a direction of the slice group change for raster and wipe maps. Applicable to the H264 encoder. Possible values are:

<!-- tabularcolumns: |p{9.6cm}|p{7.9cm}| -->


<table>
<tbody>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_FMO_CHANGE_DIR_RIGHT`

</td>
<td>



Raster scan or wipe right.

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_FMO_CHANGE_DIR_LEFT`

</td>
<td>



Reverse raster scan or wipe left.

</td>
</tr>
</tbody>
</table>

- **`V4L2_CID_MPEG_VIDEO_H264_FMO_CHANGE_RATE (integer)`**

  Specifies the size of the first slice group for raster and wipe map. Applicable to the H264 encoder.

- **`V4L2_CID_MPEG_VIDEO_H264_FMO_RUN_LENGTH (integer)`**

  Specifies the number of consecutive macroblocks for the interleaved map. Applicable to the H264 encoder.

- **`V4L2_CID_MPEG_VIDEO_H264_ASO (boolean)`**

  Enables arbitrary slice ordering in encoded bitstream. Applicable to the H264 encoder.

- **`V4L2_CID_MPEG_VIDEO_H264_ASO_SLICE_ORDER (integer)`**

  Specifies the slice order in ASO. Applicable to the H264 encoder. The supplied 32-bit integer is interpreted as follows (bit 0 = least significant bit):


<table>
<tbody>
<tr>
<td>



Bit 0:15

</td>
<td>



Slice ID

</td>
</tr>
<tr>
<td>



Bit 16:32

</td>
<td>



Slice position or order

</td>
</tr>
</tbody>
</table>

- **`V4L2_CID_MPEG_VIDEO_H264_HIERARCHICAL_CODING (boolean)`**

  Enables H264 hierarchical coding. Applicable to the H264 encoder.

<a id="rst-v4l2-mpeg-video-h264-hierarchical-coding-type"></a>

- **`V4L2_CID_MPEG_VIDEO_H264_HIERARCHICAL_CODING_TYPE`**

  (enum)

- **enum v4l2\_mpeg\_video\_h264\_hierarchical\_coding\_type -**

  Specifies the hierarchical coding type. Applicable to the H264 encoder. Possible values are:


<table>
<tbody>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_HIERARCHICAL_CODING_B`

</td>
<td>



Hierarchical B coding.

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_H264_HIERARCHICAL_CODING_P`

</td>
<td>



Hierarchical P coding.

</td>
</tr>
</tbody>
</table>

- **`V4L2_CID_MPEG_VIDEO_H264_HIERARCHICAL_CODING_LAYER (integer)`**

  Specifies the number of hierarchical coding layers. Applicable to the H264 encoder.

- **`V4L2_CID_MPEG_VIDEO_H264_HIERARCHICAL_CODING_LAYER_QP (integer)`**

  Specifies a user defined QP for each layer. Applicable to the H264 encoder. The supplied 32-bit integer is interpreted as follows (bit 0 = least significant bit):


<table>
<tbody>
<tr>
<td>



Bit 0:15

</td>
<td>



QP value

</td>
</tr>
<tr>
<td>



Bit 16:32

</td>
<td>



Layer number

</td>
</tr>
</tbody>
</table>

- **`V4L2_CID_MPEG_VIDEO_H264_HIER_CODING_L0_BR (integer)`**

  Indicates bit rate (bps) for hierarchical coding layer 0 for H264 encoder.

- **`V4L2_CID_MPEG_VIDEO_H264_HIER_CODING_L1_BR (integer)`**

  Indicates bit rate (bps) for hierarchical coding layer 1 for H264 encoder.

- **`V4L2_CID_MPEG_VIDEO_H264_HIER_CODING_L2_BR (integer)`**

  Indicates bit rate (bps) for hierarchical coding layer 2 for H264 encoder.

- **`V4L2_CID_MPEG_VIDEO_H264_HIER_CODING_L3_BR (integer)`**

  Indicates bit rate (bps) for hierarchical coding layer 3 for H264 encoder.

- **`V4L2_CID_MPEG_VIDEO_H264_HIER_CODING_L4_BR (integer)`**

  Indicates bit rate (bps) for hierarchical coding layer 4 for H264 encoder.

- **`V4L2_CID_MPEG_VIDEO_H264_HIER_CODING_L5_BR (integer)`**

  Indicates bit rate (bps) for hierarchical coding layer 5 for H264 encoder.

- **`V4L2_CID_MPEG_VIDEO_H264_HIER_CODING_L6_BR (integer)`**

  Indicates bit rate (bps) for hierarchical coding layer 6 for H264 encoder.

- **`V4L2_CID_FWHT_I_FRAME_QP (integer)`**

  Quantization parameter for an I frame for FWHT. Valid range: from 1 to 31.

- **`V4L2_CID_FWHT_P_FRAME_QP (integer)`**

  Quantization parameter for a P frame for FWHT. Valid range: from 1 to 31.

- **`V4L2_CID_MPEG_VIDEO_AVERAGE_QP (integer)`**

  This read-only control returns the average QP value of the currently encoded frame. The value applies to the last dequeued capture buffer (VIDIOC\_DQBUF). Its valid range depends on the encoding format and parameters. For H264, its valid range is from 0 to 51. For HEVC, its valid range is from 0 to 51 for 8 bit and from 0 to 63 for 10 bit. For H263 and MPEG4, its valid range is from 1 to 31. For VP8, its valid range is from 0 to 127. For VP9, its valid range is from 0 to 255. If the codec's MIN\_QP and MAX\_QP are set, then the QP will meet both requirements. Codecs need to always use the specified range, rather then a HW custom range. Applicable to encoders

<!-- Source LaTeX layout: \normalsize -->

<a id="rst-mfc-5-1-mpeg-controls"></a>

## MFC 5.1 MPEG Controls

The following MPEG class controls deal with MPEG decoding and encoding settings that are specific to the Multi Format Codec 5.1 device present in the S5P family of SoCs by Samsung.

<a id="rst-mfc-5-1-control-ids"></a>
<a id="rst-mfc51-control-id"></a>

### MFC 5.1 Control IDs

- **`V4L2_CID_MPEG_MFC51_VIDEO_DECODER_H264_DISPLAY_DELAY_ENABLE (boolean)`**

  If the display delay is enabled then the decoder is forced to return a CAPTURE buffer (decoded frame) after processing a certain number of OUTPUT buffers. The delay can be set through `V4L2_CID_MPEG_MFC51_VIDEO_DECODER_H264_DISPLAY_DELAY`. This feature can be used for example for generating thumbnails of videos. Applicable to the H264 decoder.

  > [!NOTE]
  >
  > This control is deprecated. Use the standard `V4L2_CID_MPEG_VIDEO_DEC_DISPLAY_DELAY_ENABLE` control instead.

- **`V4L2_CID_MPEG_MFC51_VIDEO_DECODER_H264_DISPLAY_DELAY (integer)`**

  Display delay value for H264 decoder. The decoder is forced to return a decoded frame after the set 'display delay' number of frames. If this number is low it may result in frames returned out of display order, in addition the hardware may still be using the returned buffer as a reference picture for subsequent frames.

  > [!NOTE]
  >
  > This control is deprecated. Use the standard `V4L2_CID_MPEG_VIDEO_DEC_DISPLAY_DELAY` control instead.

- **`V4L2_CID_MPEG_MFC51_VIDEO_H264_NUM_REF_PIC_FOR_P (integer)`**

  The number of reference pictures used for encoding a P picture. Applicable to the H264 encoder.

- **`V4L2_CID_MPEG_MFC51_VIDEO_PADDING (boolean)`**

  Padding enable in the encoder - use a color instead of repeating border pixels. Applicable to encoders.

- **`V4L2_CID_MPEG_MFC51_VIDEO_PADDING_YUV (integer)`**

  Padding color in the encoder. Applicable to encoders. The supplied 32-bit integer is interpreted as follows (bit 0 = least significant bit):


<table>
<tbody>
<tr>
<td>



Bit 0:7

</td>
<td>



V chrominance information

</td>
</tr>
<tr>
<td>



Bit 8:15

</td>
<td>



U chrominance information

</td>
</tr>
<tr>
<td>



Bit 16:23

</td>
<td>



Y luminance information

</td>
</tr>
<tr>
<td>



Bit 24:31

</td>
<td>



Must be zero.

</td>
</tr>
</tbody>
</table>

- **`V4L2_CID_MPEG_MFC51_VIDEO_RC_REACTION_COEFF (integer)`**

  Reaction coefficient for MFC rate control. Applicable to encoders.

  > [!NOTE]
  >
  > 1. Valid only when the frame level RC is enabled.
  >
  > 2. For tight CBR, this field must be small (ex. 2 \~ 10). For VBR, this field must be large (ex. 100 \~ 1000).
  >
  > 3. It is not recommended to use the greater number than FRAME\_RATE \* (10^9 / BIT\_RATE).

- **`V4L2_CID_MPEG_MFC51_VIDEO_H264_ADAPTIVE_RC_DARK (boolean)`**

  Adaptive rate control for dark region. Valid only when H.264 and macroblock level RC is enabled (`V4L2_CID_MPEG_VIDEO_MB_RC_ENABLE`). Applicable to the H264 encoder.

- **`V4L2_CID_MPEG_MFC51_VIDEO_H264_ADAPTIVE_RC_SMOOTH (boolean)`**

  Adaptive rate control for smooth region. Valid only when H.264 and macroblock level RC is enabled (`V4L2_CID_MPEG_VIDEO_MB_RC_ENABLE`). Applicable to the H264 encoder.

- **`V4L2_CID_MPEG_MFC51_VIDEO_H264_ADAPTIVE_RC_STATIC (boolean)`**

  Adaptive rate control for static region. Valid only when H.264 and macroblock level RC is enabled (`V4L2_CID_MPEG_VIDEO_MB_RC_ENABLE`). Applicable to the H264 encoder.

- **`V4L2_CID_MPEG_MFC51_VIDEO_H264_ADAPTIVE_RC_ACTIVITY (boolean)`**

  Adaptive rate control for activity region. Valid only when H.264 and macroblock level RC is enabled (`V4L2_CID_MPEG_VIDEO_MB_RC_ENABLE`). Applicable to the H264 encoder.

<a id="rst-v4l2-mpeg-mfc51-video-frame-skip-mode"></a>

- **`V4L2_CID_MPEG_MFC51_VIDEO_FRAME_SKIP_MODE`**

  (enum)

  > [!NOTE]
  >
  > This control is deprecated. Use the standard `V4L2_CID_MPEG_VIDEO_FRAME_SKIP_MODE` control instead.

- **enum v4l2\_mpeg\_mfc51\_video\_frame\_skip\_mode -**

  Indicates in what conditions the encoder should skip frames. If encoding a frame would cause the encoded stream to be larger then a chosen data limit then the frame will be skipped. Possible values are:

<!-- tabularcolumns: |p{9.4cm}|p{8.1cm}| -->

<!-- Source LaTeX layout: \small -->


<table>
<tbody>
<tr>
<td>



`V4L2_MPEG_MFC51_VIDEO_FRAME_SKIP_MODE_DISABLED`

</td>
<td>



Frame skip mode is disabled.

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_MFC51_VIDEO_FRAME_SKIP_MODE_LEVEL_LIMIT`

</td>
<td>



Frame skip mode enabled and buffer limit is set by the chosen level and is defined by the standard.

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_MFC51_VIDEO_FRAME_SKIP_MODE_BUF_LIMIT`

</td>
<td>



Frame skip mode enabled and buffer limit is set by the VBV (MPEG1/2/4) or CPB (H264) buffer size control.

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

- **`V4L2_CID_MPEG_MFC51_VIDEO_RC_FIXED_TARGET_BIT (integer)`**

  Enable rate-control with fixed target bit. If this setting is enabled, then the rate control logic of the encoder will calculate the average bitrate for a GOP and keep it below or equal the set bitrate target. Otherwise the rate control logic calculates the overall average bitrate for the stream and keeps it below or equal to the set bitrate. In the first case the average bitrate for the whole stream will be smaller then the set bitrate. This is caused because the average is calculated for smaller number of frames, on the other hand enabling this setting will ensure that the stream will meet tight bandwidth constraints. Applicable to encoders.

<a id="rst-v4l2-mpeg-mfc51-video-force-frame-type"></a>

- **`V4L2_CID_MPEG_MFC51_VIDEO_FORCE_FRAME_TYPE`**

  (enum)

- **enum v4l2\_mpeg\_mfc51\_video\_force\_frame\_type -**

  Force a frame type for the next queued buffer. Applicable to encoders. Possible values are:

<!-- tabularcolumns: |p{9.9cm}|p{7.6cm}| -->


<table>
<tbody>
<tr>
<td>



`V4L2_MPEG_MFC51_FORCE_FRAME_TYPE_DISABLED`

</td>
<td>



Forcing a specific frame type disabled.

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_MFC51_FORCE_FRAME_TYPE_I_FRAME`

</td>
<td>



Force an I-frame.

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_MFC51_FORCE_FRAME_TYPE_NOT_CODED`

</td>
<td>



Force a non-coded frame.

</td>
</tr>
</tbody>
</table>

<a id="rst-cx2341x-mpeg-controls"></a>

## CX2341x MPEG Controls

The following MPEG class controls deal with MPEG encoding settings that are specific to the Conexant CX23415 and CX23416 MPEG encoding chips.

<a id="rst-cx2341x-control-ids"></a>
<a id="rst-cx2341x-control-id"></a>

### CX2341x Control IDs

<a id="rst-v4l2-mpeg-cx2341x-video-spatial-filter-mode"></a>

- **`V4L2_CID_MPEG_CX2341X_VIDEO_SPATIAL_FILTER_MODE`**

  (enum)

- **enum v4l2\_mpeg\_cx2341x\_video\_spatial\_filter\_mode -**

  Sets the Spatial Filter mode (default `MANUAL`). Possible values are:

<!-- tabularcolumns: |p{11.5cm}|p{6.0cm}| -->


<table>
<tbody>
<tr>
<td>



`V4L2_MPEG_CX2341X_VIDEO_SPATIAL_FILTER_MODE_MANUAL`

</td>
<td>



Choose the filter manually

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_CX2341X_VIDEO_SPATIAL_FILTER_MODE_AUTO`

</td>
<td>



Choose the filter automatically

</td>
</tr>
</tbody>
</table>

- **`V4L2_CID_MPEG_CX2341X_VIDEO_SPATIAL_FILTER (integer (0-15))`**

  The setting for the Spatial Filter. 0 = off, 15 = maximum. (Default is 0.)

<a id="rst-luma-spatial-filter-type"></a>

- **`V4L2_CID_MPEG_CX2341X_VIDEO_LUMA_SPATIAL_FILTER_TYPE`**

  (enum)

- **enum v4l2\_mpeg\_cx2341x\_video\_luma\_spatial\_filter\_type -**

  Select the algorithm to use for the Luma Spatial Filter (default `1D_HOR`). Possible values:

<!-- tabularcolumns: |p{13.1cm}|p{4.4cm}| -->

<!-- Source LaTeX layout: \footnotesize -->


<table>
<tbody>
<tr>
<td>



`V4L2_MPEG_CX2341X_VIDEO_LUMA_SPATIAL_FILTER_TYPE_OFF`

</td>
<td>



No filter

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_CX2341X_VIDEO_LUMA_SPATIAL_FILTER_TYPE_1D_HOR`

</td>
<td>



One-dimensional horizontal

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_CX2341X_VIDEO_LUMA_SPATIAL_FILTER_TYPE_1D_VERT`

</td>
<td>



One-dimensional vertical

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_CX2341X_VIDEO_LUMA_SPATIAL_FILTER_TYPE_2D_HV_SEPARABLE`

</td>
<td>



Two-dimensional separable

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_CX2341X_VIDEO_LUMA_SPATIAL_FILTER_TYPE_2D_SYM_NON_SEPARABLE`

</td>
<td>



Two-dimensional symmetrical non-separable

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

<a id="rst-chroma-spatial-filter-type"></a>

- **`V4L2_CID_MPEG_CX2341X_VIDEO_CHROMA_SPATIAL_FILTER_TYPE`**

  (enum)

- **enum v4l2\_mpeg\_cx2341x\_video\_chroma\_spatial\_filter\_type -**

  Select the algorithm for the Chroma Spatial Filter (default `1D_HOR`). Possible values are:

<!-- Source LaTeX layout: \footnotesize -->

<!-- tabularcolumns: |p{11.0cm}|p{6.5cm}| -->


<table>
<tbody>
<tr>
<td>



`V4L2_MPEG_CX2341X_VIDEO_CHROMA_SPATIAL_FILTER_TYPE_OFF`

</td>
<td>



No filter

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_CX2341X_VIDEO_CHROMA_SPATIAL_FILTER_TYPE_1D_HOR`

</td>
<td>



One-dimensional horizontal

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

<a id="rst-v4l2-mpeg-cx2341x-video-temporal-filter-mode"></a>

- **`V4L2_CID_MPEG_CX2341X_VIDEO_TEMPORAL_FILTER_MODE`**

  (enum)

- **enum v4l2\_mpeg\_cx2341x\_video\_temporal\_filter\_mode -**

  Sets the Temporal Filter mode (default `MANUAL`). Possible values are:

<!-- Source LaTeX layout: \footnotesize -->


<table>
<tbody>
<tr>
<td>



`V4L2_MPEG_CX2341X_VIDEO_TEMPORAL_FILTER_MODE_MANUAL`

</td>
<td>



Choose the filter manually

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_CX2341X_VIDEO_TEMPORAL_FILTER_MODE_AUTO`

</td>
<td>



Choose the filter automatically

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

- **`V4L2_CID_MPEG_CX2341X_VIDEO_TEMPORAL_FILTER (integer (0-31))`**

  The setting for the Temporal Filter. 0 = off, 31 = maximum. (Default is 8 for full-scale capturing and 0 for scaled capturing.)

<a id="rst-v4l2-mpeg-cx2341x-video-median-filter-type"></a>

- **`V4L2_CID_MPEG_CX2341X_VIDEO_MEDIAN_FILTER_TYPE`**

  (enum)

- **enum v4l2\_mpeg\_cx2341x\_video\_median\_filter\_type -**

  Median Filter Type (default `OFF`). Possible values are:

<!-- Source LaTeX layout: \small -->

<!-- tabularcolumns: |p{11.0cm}|p{6.5cm}| -->


<table>
<tbody>
<tr>
<td>



`V4L2_MPEG_CX2341X_VIDEO_MEDIAN_FILTER_TYPE_OFF`

</td>
<td>



No filter

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_CX2341X_VIDEO_MEDIAN_FILTER_TYPE_HOR`

</td>
<td>



Horizontal filter

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_CX2341X_VIDEO_MEDIAN_FILTER_TYPE_VERT`

</td>
<td>



Vertical filter

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_CX2341X_VIDEO_MEDIAN_FILTER_TYPE_HOR_VERT`

</td>
<td>



Horizontal and vertical filter

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_CX2341X_VIDEO_MEDIAN_FILTER_TYPE_DIAG`

</td>
<td>



Diagonal filter

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

- **`V4L2_CID_MPEG_CX2341X_VIDEO_LUMA_MEDIAN_FILTER_BOTTOM (integer (0-255))`**

  Threshold above which the luminance median filter is enabled (default 0)

- **`V4L2_CID_MPEG_CX2341X_VIDEO_LUMA_MEDIAN_FILTER_TOP (integer (0-255))`**

  Threshold below which the luminance median filter is enabled (default 255)

- **`V4L2_CID_MPEG_CX2341X_VIDEO_CHROMA_MEDIAN_FILTER_BOTTOM (integer (0-255))`**

  Threshold above which the chroma median filter is enabled (default 0)

- **`V4L2_CID_MPEG_CX2341X_VIDEO_CHROMA_MEDIAN_FILTER_TOP (integer (0-255))`**

  Threshold below which the chroma median filter is enabled (default 255)

- **`V4L2_CID_MPEG_CX2341X_STREAM_INSERT_NAV_PACKETS (boolean)`**

  The CX2341X MPEG encoder can insert one empty MPEG-2 PES packet into the stream between every four video frames. The packet size is 2048 bytes, including the packet\_start\_code\_prefix and stream\_id fields. The stream\_id is 0xBF (private stream 2). The payload consists of 0x00 bytes, to be filled in by the application. 0 = do not insert, 1 = insert packets.

<a id="rst-vpx-control-reference"></a>

## VPX Control Reference

The VPX controls include controls for encoding parameters of VPx video codec.

<a id="rst-vpx-control-ids"></a>
<a id="rst-vpx-control-id"></a>

### VPX Control IDs

<a id="rst-v4l2-vpx-num-partitions"></a>

- **`V4L2_CID_MPEG_VIDEO_VPX_NUM_PARTITIONS`**

  (enum)

- **enum v4l2\_vp8\_num\_partitions -**

  The number of token partitions to use in VP8 encoder. Possible values are:


<table>
<tbody>
<tr>
<td>



`V4L2_CID_MPEG_VIDEO_VPX_1_PARTITION`

</td>
<td>



1 coefficient partition

</td>
</tr>
<tr>
<td>



`V4L2_CID_MPEG_VIDEO_VPX_2_PARTITIONS`

</td>
<td>



2 coefficient partitions

</td>
</tr>
<tr>
<td>



`V4L2_CID_MPEG_VIDEO_VPX_4_PARTITIONS`

</td>
<td>



4 coefficient partitions

</td>
</tr>
<tr>
<td>



`V4L2_CID_MPEG_VIDEO_VPX_8_PARTITIONS`

</td>
<td>



8 coefficient partitions

</td>
</tr>
</tbody>
</table>

- **`V4L2_CID_MPEG_VIDEO_VPX_IMD_DISABLE_4X4 (boolean)`**

  Setting this prevents intra 4x4 mode in the intra mode decision.

<a id="rst-v4l2-vpx-num-ref-frames"></a>

- **`V4L2_CID_MPEG_VIDEO_VPX_NUM_REF_FRAMES`**

  (enum)

- **enum v4l2\_vp8\_num\_ref\_frames -**

  The number of reference pictures for encoding P frames. Possible values are:

<!-- tabularcolumns: |p{7.5cm}|p{7.5cm}| -->

<!-- Source LaTeX layout: \small -->


<table>
<tbody>
<tr>
<td>



`V4L2_CID_MPEG_VIDEO_VPX_1_REF_FRAME`

</td>
<td>



Last encoded frame will be searched

</td>
</tr>
<tr>
<td>



`V4L2_CID_MPEG_VIDEO_VPX_2_REF_FRAME`

</td>
<td>



Two frames will be searched among the last encoded frame, the golden frame and the alternate reference (altref) frame. The encoder implementation will decide which two are chosen.

</td>
</tr>
<tr>
<td>



`V4L2_CID_MPEG_VIDEO_VPX_3_REF_FRAME`

</td>
<td>



The last encoded frame, the golden frame and the altref frame will be searched.

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

- **`V4L2_CID_MPEG_VIDEO_VPX_FILTER_LEVEL (integer)`**

  Indicates the loop filter level. The adjustment of the loop filter level is done via a delta value against a baseline loop filter value.

- **`V4L2_CID_MPEG_VIDEO_VPX_FILTER_SHARPNESS (integer)`**

  This parameter affects the loop filter. Anything above zero weakens the deblocking effect on the loop filter.

- **`V4L2_CID_MPEG_VIDEO_VPX_GOLDEN_FRAME_REF_PERIOD (integer)`**

  Sets the refresh period for the golden frame. The period is defined in number of frames. For a value of 'n', every nth frame starting from the first key frame will be taken as a golden frame. For eg. for encoding sequence of 0, 1, 2, 3, 4, 5, 6, 7 where the golden frame refresh period is set as 4, the frames 0, 4, 8 etc will be taken as the golden frames as frame 0 is always a key frame.

<a id="rst-v4l2-vpx-golden-frame-sel"></a>

- **`V4L2_CID_MPEG_VIDEO_VPX_GOLDEN_FRAME_SEL`**

  (enum)

- **enum v4l2\_vp8\_golden\_frame\_sel -**

  Selects the golden frame for encoding. Possible values are:

<!-- Source LaTeX layout: \scriptsize -->

<!-- tabularcolumns: |p{8.6cm}|p{8.9cm}| -->


<table>
<tbody>
<tr>
<td>



`V4L2_CID_MPEG_VIDEO_VPX_GOLDEN_FRAME_USE_PREV`

</td>
<td>



Use the (n-2)th frame as a golden frame, current frame index being 'n'.

</td>
</tr>
<tr>
<td>



`V4L2_CID_MPEG_VIDEO_VPX_GOLDEN_FRAME_USE_REF_PERIOD`

</td>
<td>



Use the previous specific frame indicated by `V4L2_CID_MPEG_VIDEO_VPX_GOLDEN_FRAME_REF_PERIOD` as a golden frame.

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

- **`V4L2_CID_MPEG_VIDEO_VPX_MIN_QP (integer)`**

  Minimum quantization parameter for VP8.

- **`V4L2_CID_MPEG_VIDEO_VPX_MAX_QP (integer)`**

  Maximum quantization parameter for VP8.

- **`V4L2_CID_MPEG_VIDEO_VPX_I_FRAME_QP (integer)`**

  Quantization parameter for an I frame for VP8.

- **`V4L2_CID_MPEG_VIDEO_VPX_P_FRAME_QP (integer)`**

  Quantization parameter for a P frame for VP8.

<a id="rst-v4l2-mpeg-video-vp8-profile"></a>

- **`V4L2_CID_MPEG_VIDEO_VP8_PROFILE`**

  (enum)

- **enum v4l2\_mpeg\_video\_vp8\_profile -**

  This control allows selecting the profile for VP8 encoder. This is also used to enumerate supported profiles by VP8 encoder or decoder. Possible values are:


<table>
<tbody>
<tr>
<td>



`V4L2_MPEG_VIDEO_VP8_PROFILE_0`

</td>
<td>



Profile 0

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_VP8_PROFILE_1`

</td>
<td>



Profile 1

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_VP8_PROFILE_2`

</td>
<td>



Profile 2

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_VP8_PROFILE_3`

</td>
<td>



Profile 3

</td>
</tr>
</tbody>
</table>

<a id="rst-v4l2-mpeg-video-vp9-profile"></a>

- **`V4L2_CID_MPEG_VIDEO_VP9_PROFILE`**

  (enum)

- **enum v4l2\_mpeg\_video\_vp9\_profile -**

  This control allows selecting the profile for VP9 encoder. This is also used to enumerate supported profiles by VP9 encoder or decoder. Possible values are:


<table>
<tbody>
<tr>
<td>



`V4L2_MPEG_VIDEO_VP9_PROFILE_0`

</td>
<td>



Profile 0

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_VP9_PROFILE_1`

</td>
<td>



Profile 1

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_VP9_PROFILE_2`

</td>
<td>



Profile 2

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_VP9_PROFILE_3`

</td>
<td>



Profile 3

</td>
</tr>
</tbody>
</table>

<a id="rst-v4l2-mpeg-video-vp9-level"></a>

`V4L2_CID_MPEG_VIDEO_VP9_LEVEL (enum)`

- **enum v4l2\_mpeg\_video\_vp9\_level -**

  This control allows selecting the level for VP9 encoder. This is also used to enumerate supported levels by VP9 encoder or decoder. More information can be found at [webmproject](<https://www.webmproject.org/vp9/levels/>). Possible values are:


<table>
<tbody>
<tr>
<td>



`V4L2_MPEG_VIDEO_VP9_LEVEL_1_0`

</td>
<td>



Level 1

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_VP9_LEVEL_1_1`

</td>
<td>



Level 1.1

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_VP9_LEVEL_2_0`

</td>
<td>



Level 2

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_VP9_LEVEL_2_1`

</td>
<td>



Level 2.1

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_VP9_LEVEL_3_0`

</td>
<td>



Level 3

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_VP9_LEVEL_3_1`

</td>
<td>



Level 3.1

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_VP9_LEVEL_4_0`

</td>
<td>



Level 4

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_VP9_LEVEL_4_1`

</td>
<td>



Level 4.1

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_VP9_LEVEL_5_0`

</td>
<td>



Level 5

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_VP9_LEVEL_5_1`

</td>
<td>



Level 5.1

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_VP9_LEVEL_5_2`

</td>
<td>



Level 5.2

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_VP9_LEVEL_6_0`

</td>
<td>



Level 6

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_VP9_LEVEL_6_1`

</td>
<td>



Level 6.1

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_VP9_LEVEL_6_2`

</td>
<td>



Level 6.2

</td>
</tr>
</tbody>
</table>

<a id="rst-high-efficiency-video-coding-hevc-h-265-control-reference"></a>

## High Efficiency Video Coding (HEVC/H.265) Control Reference

The HEVC/H.265 controls include controls for encoding parameters of HEVC/H.265 video codec.

<a id="rst-hevc-h-265-control-ids"></a>
<a id="rst-hevc-control-id"></a>

### HEVC/H.265 Control IDs

- **`V4L2_CID_MPEG_VIDEO_HEVC_MIN_QP (integer)`**

  Minimum quantization parameter for HEVC. Valid range: from 0 to 51 for 8 bit and from 0 to 63 for 10 bit.

- **`V4L2_CID_MPEG_VIDEO_HEVC_MAX_QP (integer)`**

  Maximum quantization parameter for HEVC. Valid range: from 0 to 51 for 8 bit and from 0 to 63 for 10 bit.

- **`V4L2_CID_MPEG_VIDEO_HEVC_I_FRAME_QP (integer)`**

  Quantization parameter for an I frame for HEVC. Valid range: \[V4L2\_CID\_MPEG\_VIDEO\_HEVC\_MIN\_QP, V4L2\_CID\_MPEG\_VIDEO\_HEVC\_MAX\_QP\].

- **`V4L2_CID_MPEG_VIDEO_HEVC_P_FRAME_QP (integer)`**

  Quantization parameter for a P frame for HEVC. Valid range: \[V4L2\_CID\_MPEG\_VIDEO\_HEVC\_MIN\_QP, V4L2\_CID\_MPEG\_VIDEO\_HEVC\_MAX\_QP\].

- **`V4L2_CID_MPEG_VIDEO_HEVC_B_FRAME_QP (integer)`**

  Quantization parameter for a B frame for HEVC. Valid range: \[V4L2\_CID\_MPEG\_VIDEO\_HEVC\_MIN\_QP, V4L2\_CID\_MPEG\_VIDEO\_HEVC\_MAX\_QP\].

- **`V4L2_CID_MPEG_VIDEO_HEVC_I_FRAME_MIN_QP (integer)`**

  Minimum quantization parameter for the HEVC I frame to limit I frame quality to a range. Valid range: from 0 to 51 for 8 bit and from 0 to 63 for 10 bit. If V4L2\_CID\_MPEG\_VIDEO\_HEVC\_MIN\_QP is also set, the quantization parameter should be chosen to meet both requirements.

- **`V4L2_CID_MPEG_VIDEO_HEVC_I_FRAME_MAX_QP (integer)`**

  Maximum quantization parameter for the HEVC I frame to limit I frame quality to a range. Valid range: from 0 to 51 for 8 bit and from 0 to 63 for 10 bit. If V4L2\_CID\_MPEG\_VIDEO\_HEVC\_MAX\_QP is also set, the quantization parameter should be chosen to meet both requirements.

- **`V4L2_CID_MPEG_VIDEO_HEVC_P_FRAME_MIN_QP (integer)`**

  Minimum quantization parameter for the HEVC P frame to limit P frame quality to a range. Valid range: from 0 to 51 for 8 bit and from 0 to 63 for 10 bit. If V4L2\_CID\_MPEG\_VIDEO\_HEVC\_MIN\_QP is also set, the quantization parameter should be chosen to meet both requirements.

- **`V4L2_CID_MPEG_VIDEO_HEVC_P_FRAME_MAX_QP (integer)`**

  Maximum quantization parameter for the HEVC P frame to limit P frame quality to a range. Valid range: from 0 to 51 for 8 bit and from 0 to 63 for 10 bit. If V4L2\_CID\_MPEG\_VIDEO\_HEVC\_MAX\_QP is also set, the quantization parameter should be chosen to meet both requirements.

- **`V4L2_CID_MPEG_VIDEO_HEVC_B_FRAME_MIN_QP (integer)`**

  Minimum quantization parameter for the HEVC B frame to limit B frame quality to a range. Valid range: from 0 to 51 for 8 bit and from 0 to 63 for 10 bit. If V4L2\_CID\_MPEG\_VIDEO\_HEVC\_MIN\_QP is also set, the quantization parameter should be chosen to meet both requirements.

- **`V4L2_CID_MPEG_VIDEO_HEVC_B_FRAME_MAX_QP (integer)`**

  Maximum quantization parameter for the HEVC B frame to limit B frame quality to a range. Valid range: from 0 to 51 for 8 bit and from 0 to 63 for 10 bit. If V4L2\_CID\_MPEG\_VIDEO\_HEVC\_MAX\_QP is also set, the quantization parameter should be chosen to meet both requirements.

- **`V4L2_CID_MPEG_VIDEO_HEVC_HIER_QP (boolean)`**

  HIERARCHICAL\_QP allows the host to specify the quantization parameter values for each temporal layer through HIERARCHICAL\_QP\_LAYER. This is valid only if HIERARCHICAL\_CODING\_LAYER is greater than 1. Setting the control value to 1 enables setting of the QP values for the layers.

<a id="rst-v4l2-hevc-hier-coding-type"></a>

- **`V4L2_CID_MPEG_VIDEO_HEVC_HIER_CODING_TYPE`**

  (enum)

- **enum v4l2\_mpeg\_video\_hevc\_hier\_coding\_type -**

  Selects the hierarchical coding type for encoding. Possible values are:

<!-- Source LaTeX layout: \footnotesize -->

<!-- tabularcolumns: |p{8.2cm}|p{9.3cm}| -->


<table>
<tbody>
<tr>
<td>



`V4L2_MPEG_VIDEO_HEVC_HIERARCHICAL_CODING_B`

</td>
<td>



Use the B frame for hierarchical coding.

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_HEVC_HIERARCHICAL_CODING_P`

</td>
<td>



Use the P frame for hierarchical coding.

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

- **`V4L2_CID_MPEG_VIDEO_HEVC_HIER_CODING_LAYER (integer)`**

  Selects the hierarchical coding layer. In normal encoding (non-hierarchial coding), it should be zero. Possible values are \[0, 6\]. 0 indicates HIERARCHICAL CODING LAYER 0, 1 indicates HIERARCHICAL CODING LAYER 1 and so on.

- **`V4L2_CID_MPEG_VIDEO_HEVC_HIER_CODING_L0_QP (integer)`**

  Indicates quantization parameter for hierarchical coding layer 0. Valid range: \[V4L2\_CID\_MPEG\_VIDEO\_HEVC\_MIN\_QP, V4L2\_CID\_MPEG\_VIDEO\_HEVC\_MAX\_QP\].

- **`V4L2_CID_MPEG_VIDEO_HEVC_HIER_CODING_L1_QP (integer)`**

  Indicates quantization parameter for hierarchical coding layer 1. Valid range: \[V4L2\_CID\_MPEG\_VIDEO\_HEVC\_MIN\_QP, V4L2\_CID\_MPEG\_VIDEO\_HEVC\_MAX\_QP\].

- **`V4L2_CID_MPEG_VIDEO_HEVC_HIER_CODING_L2_QP (integer)`**

  Indicates quantization parameter for hierarchical coding layer 2. Valid range: \[V4L2\_CID\_MPEG\_VIDEO\_HEVC\_MIN\_QP, V4L2\_CID\_MPEG\_VIDEO\_HEVC\_MAX\_QP\].

- **`V4L2_CID_MPEG_VIDEO_HEVC_HIER_CODING_L3_QP (integer)`**

  Indicates quantization parameter for hierarchical coding layer 3. Valid range: \[V4L2\_CID\_MPEG\_VIDEO\_HEVC\_MIN\_QP, V4L2\_CID\_MPEG\_VIDEO\_HEVC\_MAX\_QP\].

- **`V4L2_CID_MPEG_VIDEO_HEVC_HIER_CODING_L4_QP (integer)`**

  Indicates quantization parameter for hierarchical coding layer 4. Valid range: \[V4L2\_CID\_MPEG\_VIDEO\_HEVC\_MIN\_QP, V4L2\_CID\_MPEG\_VIDEO\_HEVC\_MAX\_QP\].

- **`V4L2_CID_MPEG_VIDEO_HEVC_HIER_CODING_L5_QP (integer)`**

  Indicates quantization parameter for hierarchical coding layer 5. Valid range: \[V4L2\_CID\_MPEG\_VIDEO\_HEVC\_MIN\_QP, V4L2\_CID\_MPEG\_VIDEO\_HEVC\_MAX\_QP\].

- **`V4L2_CID_MPEG_VIDEO_HEVC_HIER_CODING_L6_QP (integer)`**

  Indicates quantization parameter for hierarchical coding layer 6. Valid range: \[V4L2\_CID\_MPEG\_VIDEO\_HEVC\_MIN\_QP, V4L2\_CID\_MPEG\_VIDEO\_HEVC\_MAX\_QP\].

<a id="rst-v4l2-hevc-profile"></a>

- **`V4L2_CID_MPEG_VIDEO_HEVC_PROFILE`**

  (enum)

- **enum v4l2\_mpeg\_video\_hevc\_profile -**

  Select the desired profile for HEVC encoder.

<!-- Source LaTeX layout: \footnotesize -->

<!-- tabularcolumns: |p{9.0cm}|p{8.5cm}| -->


<table>
<tbody>
<tr>
<td>



`V4L2_MPEG_VIDEO_HEVC_PROFILE_MAIN`

</td>
<td>



Main profile.

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_HEVC_PROFILE_MAIN_STILL_PICTURE`

</td>
<td>



Main still picture profile.

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_HEVC_PROFILE_MAIN_10`

</td>
<td>



Main 10 profile.

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

<a id="rst-v4l2-hevc-level"></a>

- **`V4L2_CID_MPEG_VIDEO_HEVC_LEVEL`**

  (enum)

- **enum v4l2\_mpeg\_video\_hevc\_level -**

  Selects the desired level for HEVC encoder.


<table>
<tbody>
<tr>
<td>



`V4L2_MPEG_VIDEO_HEVC_LEVEL_1`

</td>
<td>



Level 1.0

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_HEVC_LEVEL_2`

</td>
<td>



Level 2.0

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_HEVC_LEVEL_2_1`

</td>
<td>



Level 2.1

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_HEVC_LEVEL_3`

</td>
<td>



Level 3.0

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_HEVC_LEVEL_3_1`

</td>
<td>



Level 3.1

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_HEVC_LEVEL_4`

</td>
<td>



Level 4.0

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_HEVC_LEVEL_4_1`

</td>
<td>



Level 4.1

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_HEVC_LEVEL_5`

</td>
<td>



Level 5.0

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_HEVC_LEVEL_5_1`

</td>
<td>



Level 5.1

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_HEVC_LEVEL_5_2`

</td>
<td>



Level 5.2

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_HEVC_LEVEL_6`

</td>
<td>



Level 6.0

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_HEVC_LEVEL_6_1`

</td>
<td>



Level 6.1

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_HEVC_LEVEL_6_2`

</td>
<td>



Level 6.2

</td>
</tr>
</tbody>
</table>

- **`V4L2_CID_MPEG_VIDEO_HEVC_FRAME_RATE_RESOLUTION (integer)`**

  Indicates the number of evenly spaced subintervals, called ticks, within one second. This is a 16 bit unsigned integer and has a maximum value up to 0xffff and a minimum value of 1.

<a id="rst-v4l2-hevc-tier"></a>

- **`V4L2_CID_MPEG_VIDEO_HEVC_TIER`**

  (enum)

- **enum v4l2\_mpeg\_video\_hevc\_tier -**

  TIER\_FLAG specifies tiers information of the HEVC encoded picture. Tier were made to deal with applications that differ in terms of maximum bit rate. Setting the flag to 0 selects HEVC tier as Main tier and setting this flag to 1 indicates High tier. High tier is for applications requiring high bit rates.


<table>
<tbody>
<tr>
<td>



`V4L2_MPEG_VIDEO_HEVC_TIER_MAIN`

</td>
<td>



Main tier.

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_HEVC_TIER_HIGH`

</td>
<td>



High tier.

</td>
</tr>
</tbody>
</table>

- **`V4L2_CID_MPEG_VIDEO_HEVC_MAX_PARTITION_DEPTH (integer)`**

  Selects HEVC maximum coding unit depth.

<a id="rst-v4l2-hevc-loop-filter-mode"></a>

- **`V4L2_CID_MPEG_VIDEO_HEVC_LOOP_FILTER_MODE`**

  (enum)

- **enum v4l2\_mpeg\_video\_hevc\_loop\_filter\_mode -**

  Loop filter mode for HEVC encoder. Possible values are:

<!-- Source LaTeX layout: \footnotesize -->

<!-- tabularcolumns: |p{12.1cm}|p{5.4cm}| -->


<table>
<tbody>
<tr>
<td>



`V4L2_MPEG_VIDEO_HEVC_LOOP_FILTER_MODE_DISABLED`

</td>
<td>



Loop filter is disabled.

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_HEVC_LOOP_FILTER_MODE_ENABLED`

</td>
<td>



Loop filter is enabled.

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_HEVC_LOOP_FILTER_MODE_DISABLED_AT_SLICE_BOUNDARY`

</td>
<td>



Loop filter is disabled at the slice boundary.

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

- **`V4L2_CID_MPEG_VIDEO_HEVC_LF_BETA_OFFSET_DIV2 (integer)`**

  Selects HEVC loop filter beta offset. The valid range is \[-6, +6\].

- **`V4L2_CID_MPEG_VIDEO_HEVC_LF_TC_OFFSET_DIV2 (integer)`**

  Selects HEVC loop filter tc offset. The valid range is \[-6, +6\].

<a id="rst-v4l2-hevc-refresh-type"></a>

- **`V4L2_CID_MPEG_VIDEO_HEVC_REFRESH_TYPE`**

  (enum)

- **enum v4l2\_mpeg\_video\_hevc\_hier\_refresh\_type -**

  Selects refresh type for HEVC encoder. Host has to specify the period into V4L2\_CID\_MPEG\_VIDEO\_HEVC\_REFRESH\_PERIOD.

<!-- Source LaTeX layout: \footnotesize -->

<!-- tabularcolumns: |p{6.2cm}|p{11.3cm}| -->


<table>
<tbody>
<tr>
<td>



`V4L2_MPEG_VIDEO_HEVC_REFRESH_NONE`

</td>
<td>



Use the B frame for hierarchical coding.

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_HEVC_REFRESH_CRA`

</td>
<td>



Use CRA (Clean Random Access Unit) picture encoding.

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_HEVC_REFRESH_IDR`

</td>
<td>



Use IDR (Instantaneous Decoding Refresh) picture encoding.

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

- **`V4L2_CID_MPEG_VIDEO_HEVC_REFRESH_PERIOD (integer)`**

  Selects the refresh period for HEVC encoder. This specifies the number of I pictures between two CRA/IDR pictures. This is valid only if REFRESH\_TYPE is not 0.

- **`V4L2_CID_MPEG_VIDEO_HEVC_LOSSLESS_CU (boolean)`**

  Indicates HEVC lossless encoding. Setting it to 0 disables lossless encoding. Setting it to 1 enables lossless encoding.

- **`V4L2_CID_MPEG_VIDEO_HEVC_CONST_INTRA_PRED (boolean)`**

  Indicates constant intra prediction for HEVC encoder. Specifies the constrained intra prediction in which intra largest coding unit (LCU) prediction is performed by using residual data and decoded samples of neighboring intra LCU only. Setting the value to 1 enables constant intra prediction and setting the value to 0 disables constant intra prediction.

- **`V4L2_CID_MPEG_VIDEO_HEVC_WAVEFRONT (boolean)`**

  Indicates wavefront parallel processing for HEVC encoder. Setting it to 0 disables the feature and setting it to 1 enables the wavefront parallel processing.

- **`V4L2_CID_MPEG_VIDEO_HEVC_GENERAL_PB (boolean)`**

  Setting the value to 1 enables combination of P and B frame for HEVC encoder.

- **`V4L2_CID_MPEG_VIDEO_HEVC_TEMPORAL_ID (boolean)`**

  Indicates temporal identifier for HEVC encoder which is enabled by setting the value to 1.

- **`V4L2_CID_MPEG_VIDEO_HEVC_STRONG_SMOOTHING (boolean)`**

  Indicates bi-linear interpolation is conditionally used in the intra prediction filtering process in the CVS when set to 1. Indicates bi-linear interpolation is not used in the CVS when set to 0.

- **`V4L2_CID_MPEG_VIDEO_HEVC_MAX_NUM_MERGE_MV_MINUS1 (integer)`**

  Indicates maximum number of merge candidate motion vectors. Values are from 0 to 4.

- **`V4L2_CID_MPEG_VIDEO_HEVC_TMV_PREDICTION (boolean)`**

  Indicates temporal motion vector prediction for HEVC encoder. Setting it to 1 enables the prediction. Setting it to 0 disables the prediction.

- **`V4L2_CID_MPEG_VIDEO_HEVC_WITHOUT_STARTCODE (boolean)`**

  Specifies if HEVC generates a stream with a size of the length field instead of start code pattern. The size of the length field is configurable through the V4L2\_CID\_MPEG\_VIDEO\_HEVC\_SIZE\_OF\_LENGTH\_FIELD control. Setting the value to 0 disables encoding without startcode pattern. Setting the value to 1 will enables encoding without startcode pattern.

<a id="rst-v4l2-hevc-size-of-length-field"></a>

`V4L2_CID_MPEG_VIDEO_HEVC_SIZE_OF_LENGTH_FIELD` (enum)

- **enum v4l2\_mpeg\_video\_hevc\_size\_of\_length\_field -**

  Indicates the size of length field. This is valid when encoding WITHOUT\_STARTCODE\_ENABLE is enabled.

<!-- Source LaTeX layout: \footnotesize -->

<!-- tabularcolumns: |p{5.5cm}|p{12.0cm}| -->


<table>
<tbody>
<tr>
<td>



`V4L2_MPEG_VIDEO_HEVC_SIZE_0`

</td>
<td>



Generate start code pattern (Normal).

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_HEVC_SIZE_1`

</td>
<td>



Generate size of length field instead of start code pattern and length is 1.

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_HEVC_SIZE_2`

</td>
<td>



Generate size of length field instead of start code pattern and length is 2.

</td>
</tr>
<tr>
<td>



`V4L2_MPEG_VIDEO_HEVC_SIZE_4`

</td>
<td>



Generate size of length field instead of start code pattern and length is 4.

</td>
</tr>
</tbody>
</table>

<!-- Source LaTeX layout: \normalsize -->

- **`V4L2_CID_MPEG_VIDEO_HEVC_HIER_CODING_L0_BR (integer)`**

  Indicates bit rate for hierarchical coding layer 0 for HEVC encoder.

- **`V4L2_CID_MPEG_VIDEO_HEVC_HIER_CODING_L1_BR (integer)`**

  Indicates bit rate for hierarchical coding layer 1 for HEVC encoder.

- **`V4L2_CID_MPEG_VIDEO_HEVC_HIER_CODING_L2_BR (integer)`**

  Indicates bit rate for hierarchical coding layer 2 for HEVC encoder.

- **`V4L2_CID_MPEG_VIDEO_HEVC_HIER_CODING_L3_BR (integer)`**

  Indicates bit rate for hierarchical coding layer 3 for HEVC encoder.

- **`V4L2_CID_MPEG_VIDEO_HEVC_HIER_CODING_L4_BR (integer)`**

  Indicates bit rate for hierarchical coding layer 4 for HEVC encoder.

- **`V4L2_CID_MPEG_VIDEO_HEVC_HIER_CODING_L5_BR (integer)`**

  Indicates bit rate for hierarchical coding layer 5 for HEVC encoder.

- **`V4L2_CID_MPEG_VIDEO_HEVC_HIER_CODING_L6_BR (integer)`**

  Indicates bit rate for hierarchical coding layer 6 for HEVC encoder.

- **`V4L2_CID_MPEG_VIDEO_REF_NUMBER_FOR_PFRAMES (integer)`**

  Selects number of P reference pictures required for HEVC encoder. P-Frame can use 1 or 2 frames for reference.

- **`V4L2_CID_MPEG_VIDEO_PREPEND_SPSPPS_TO_IDR (integer)`**

  Indicates whether to generate SPS and PPS at every IDR. Setting it to 0 disables generating SPS and PPS at every IDR. Setting it to one enables generating SPS and PPS at every IDR.
