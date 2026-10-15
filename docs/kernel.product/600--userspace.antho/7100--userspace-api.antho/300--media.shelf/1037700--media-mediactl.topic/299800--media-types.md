---
title: "Types and flags used to represent the media graph elements"
type: reference
description: "One and only one of MEDIA_PAD_FL_SINK and MEDIA_PAD_FL_SOURCE must be set for every pad."
---

<a id="rst-types-and-flags-used-to-represent-the-media-graph-elements"></a>
<a id="rst-media-controller-types"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- tabularcolumns: |p{8.2cm}|p{9.3cm}| -->

<a id="rst-media-ent-f-dv-encoder"></a>
<a id="rst-media-ent-f-dv-decoder"></a>
<a id="rst-media-ent-f-vid-if-bridge"></a>
<a id="rst-media-ent-f-vid-mux"></a>
<a id="rst-media-ent-f-proc-video-isp"></a>
<a id="rst-media-ent-f-proc-video-decoder"></a>
<a id="rst-media-ent-f-proc-video-encoder"></a>
<a id="rst-media-ent-f-proc-video-statistics"></a>
<a id="rst-media-ent-f-proc-video-scaler"></a>
<a id="rst-media-ent-f-proc-video-lut"></a>
<a id="rst-media-ent-f-proc-video-pixel-enc-conv"></a>
<a id="rst-media-ent-f-proc-video-pixel-formatter"></a>
<a id="rst-media-ent-f-proc-video-composer"></a>
<a id="rst-media-ent-f-audio-mixer"></a>
<a id="rst-media-ent-f-audio-playback"></a>
<a id="rst-media-ent-f-audio-capture"></a>
<a id="rst-media-ent-f-if-aud-decoder"></a>
<a id="rst-media-ent-f-if-vid-decoder"></a>
<a id="rst-media-ent-f-tuner"></a>
<a id="rst-media-ent-f-atv-decoder"></a>
<a id="rst-media-ent-f-lens"></a>
<a id="rst-media-ent-f-flash"></a>
<a id="rst-media-ent-f-cam-sensor"></a>
<a id="rst-media-ent-f-conn-composite"></a>
<a id="rst-media-ent-f-conn-svideo"></a>
<a id="rst-media-ent-f-conn-rf"></a>
<a id="rst-media-ent-f-dtv-net-decap"></a>
<a id="rst-media-ent-f-dtv-ca"></a>
<a id="rst-media-ent-f-ts-demux"></a>
<a id="rst-media-ent-f-dtv-demod"></a>
<a id="rst-media-ent-f-io-dtv"></a>
<a id="rst-media-ent-f-io-swradio"></a>
<a id="rst-media-ent-f-io-vbi"></a>
<a id="rst-media-ent-f-io-v4l"></a>
<a id="rst-media-ent-f-v4l2-subdev-unknown"></a>
<a id="rst-media-ent-f-unknown"></a>
<a id="rst-media-entity-functions"></a>


<table>
<caption>Media entity functions</caption>
<tbody>
<tr>
<td>


`MEDIA_ENT_F_UNKNOWN` and `MEDIA_ENT_F_V4L2_SUBDEV_UNKNOWN`

</td>
<td>


Unknown entity. That generally indicates that a driver didn't initialize properly the entity, which is a Kernel bug

</td>
</tr>
<tr>
<td>


`MEDIA_ENT_F_IO_V4L`

</td>
<td>


Data streaming input and/or output entity.

</td>
</tr>
<tr>
<td>


`MEDIA_ENT_F_IO_VBI`

</td>
<td>


V4L VBI streaming input or output entity

</td>
</tr>
<tr>
<td>


`MEDIA_ENT_F_IO_SWRADIO`

</td>
<td>


V4L Software Digital Radio (SDR) streaming input or output entity

</td>
</tr>
<tr>
<td>


`MEDIA_ENT_F_IO_DTV`

</td>
<td>


DVB Digital TV streaming input or output entity

</td>
</tr>
<tr>
<td>


`MEDIA_ENT_F_DTV_DEMOD`

</td>
<td>


Digital TV demodulator entity.

</td>
</tr>
<tr>
<td>


`MEDIA_ENT_F_TS_DEMUX`

</td>
<td>


MPEG Transport stream demux entity. Could be implemented on hardware or in Kernelspace by the Linux DVB subsystem.

</td>
</tr>
<tr>
<td>


`MEDIA_ENT_F_DTV_CA`

</td>
<td>


Digital TV Conditional Access module (CAM) entity

</td>
</tr>
<tr>
<td>


`MEDIA_ENT_F_DTV_NET_DECAP`

</td>
<td>


Digital TV network ULE/MLE desencapsulation entity. Could be implemented on hardware or in Kernelspace

</td>
</tr>
<tr>
<td>


`MEDIA_ENT_F_CONN_RF`

</td>
<td>


Connector for a Radio Frequency (RF) signal.

</td>
</tr>
<tr>
<td>


`MEDIA_ENT_F_CONN_SVIDEO`

</td>
<td>


Connector for a S-Video signal.

</td>
</tr>
<tr>
<td>


`MEDIA_ENT_F_CONN_COMPOSITE`

</td>
<td>


Connector for a RGB composite signal.

</td>
</tr>
<tr>
<td>


`MEDIA_ENT_F_CAM_SENSOR`

</td>
<td>


Camera video sensor entity.

</td>
</tr>
<tr>
<td>


`MEDIA_ENT_F_FLASH`

</td>
<td>


Flash controller entity.

</td>
</tr>
<tr>
<td>


`MEDIA_ENT_F_LENS`

</td>
<td>


Lens controller entity.

</td>
</tr>
<tr>
<td>


`MEDIA_ENT_F_ATV_DECODER`

</td>
<td>


Analog video decoder, the basic function of the video decoder is to accept analogue video from a wide variety of sources such as broadcast, DVD players, cameras and video cassette recorders, in either NTSC, PAL, SECAM or HD format, separating the stream into its component parts, luminance and chrominance, and output it in some digital video standard, with appropriate timing signals.

</td>
</tr>
<tr>
<td>


`MEDIA_ENT_F_TUNER`

</td>
<td>


Digital TV, analog TV, radio and/or software radio tuner, with consists on a PLL tuning stage that converts radio frequency (RF) signal into an Intermediate Frequency (IF). Modern tuners have internally IF-PLL decoders for audio and video, but older models have those stages implemented on separate entities.

</td>
</tr>
<tr>
<td>


`MEDIA_ENT_F_IF_VID_DECODER`

</td>
<td>


IF-PLL video decoder. It receives the IF from a PLL and decodes the analog TV video signal. This is commonly found on some very old analog tuners, like Philips MK3 designs. They all contain a tda9887 (or some software compatible similar chip, like tda9885). Those devices use a different I2C address than the tuner PLL.

</td>
</tr>
<tr>
<td>


`MEDIA_ENT_F_IF_AUD_DECODER`

</td>
<td>


IF-PLL sound decoder. It receives the IF from a PLL and decodes the analog TV audio signal. This is commonly found on some very old analog hardware, like Micronas msp3400, Philips tda9840, tda985x, etc. Those devices use a different I2C address than the tuner PLL and should be controlled together with the IF-PLL video decoder.

</td>
</tr>
<tr>
<td>


`MEDIA_ENT_F_AUDIO_CAPTURE`

</td>
<td>


Audio Capture Function Entity.

</td>
</tr>
<tr>
<td>


`MEDIA_ENT_F_AUDIO_PLAYBACK`

</td>
<td>


Audio Playback Function Entity.

</td>
</tr>
<tr>
<td>


`MEDIA_ENT_F_AUDIO_MIXER`

</td>
<td>


Audio Mixer Function Entity.

</td>
</tr>
<tr>
<td>


`MEDIA_ENT_F_PROC_VIDEO_COMPOSER`

</td>
<td>


Video composer (blender). An entity capable of video composing must have at least two sink pads and one source pad, and composes input video frames onto output video frames. Composition can be performed using alpha blending, color keying, raster operations (ROP), stitching or any other means.

</td>
</tr>
<tr>
<td>


`MEDIA_ENT_F_PROC_VIDEO_PIXEL_FORMATTER`

</td>
<td>


Video pixel formatter. An entity capable of pixel formatting must have at least one sink pad and one source pad. Read pixel formatters read pixels from memory and perform a subset of unpacking, cropping, color keying, alpha multiplication and pixel encoding conversion. Write pixel formatters perform a subset of dithering, pixel encoding conversion and packing and write pixels to memory.

</td>
</tr>
<tr>
<td>


`MEDIA_ENT_F_PROC_VIDEO_PIXEL_ENC_CONV`

</td>
<td>


Video pixel encoding converter. An entity capable of pixel encoding conversion must have at least one sink pad and one source pad, and convert the encoding of pixels received on its sink pad(s) to a different encoding output on its source pad(s). Pixel encoding conversion includes but isn't limited to RGB to/from HSV, RGB to/from YUV and CFA (Bayer) to RGB conversions.

</td>
</tr>
<tr>
<td>


`MEDIA_ENT_F_PROC_VIDEO_LUT`

</td>
<td>


Video look-up table. An entity capable of video lookup table processing must have one sink pad and one source pad. It uses the values of the pixels received on its sink pad to look up entries in internal tables and output them on its source pad. The lookup processing can be performed on all components separately or combine them for multi-dimensional table lookups.

</td>
</tr>
<tr>
<td>


`MEDIA_ENT_F_PROC_VIDEO_SCALER`

</td>
<td>


Video scaler. An entity capable of video scaling must have at least one sink pad and one source pad, and scale the video frame(s) received on its sink pad(s) to a different resolution output on its source pad(s). The range of supported scaling ratios is entity-specific and can differ between the horizontal and vertical directions (in particular scaling can be supported in one direction only). Binning and sub-sampling (occasionally also referred to as skipping) are considered as scaling.

</td>
</tr>
<tr>
<td>


`MEDIA_ENT_F_PROC_VIDEO_STATISTICS`

</td>
<td>


Video statistics computation (histogram, 3A, etc.). An entity capable of statistics computation must have one sink pad and one source pad. It computes statistics over the frames received on its sink pad and outputs the statistics data on its source pad.

</td>
</tr>
<tr>
<td>


`MEDIA_ENT_F_PROC_VIDEO_ENCODER`

</td>
<td>


Video (MPEG, HEVC, VPx, etc.) encoder. An entity capable of compressing video frames. Must have one sink pad and at least one source pad.

</td>
</tr>
<tr>
<td>


`MEDIA_ENT_F_PROC_VIDEO_DECODER`

</td>
<td>


Video (MPEG, HEVC, VPx, etc.) decoder. An entity capable of decompressing a compressed video stream into uncompressed video frames. Must have one sink pad and at least one source pad.

</td>
</tr>
<tr>
<td>


`MEDIA_ENT_F_PROC_VIDEO_ISP`

</td>
<td>


An Image Signal Processor (ISP) device. ISPs generally are one of a kind devices that have their specific control interfaces using a combination of custom V4L2 controls and IOCTLs, and parameters supplied in a metadata buffer.

</td>
</tr>
<tr>
<td>


`MEDIA_ENT_F_VID_MUX`

</td>
<td>


Video multiplexer. An entity capable of multiplexing must have at least two sink pads and one source pad, and must pass the video frame(s) received from the active sink pad to the source pad.

</td>
</tr>
<tr>
<td>


`MEDIA_ENT_F_VID_IF_BRIDGE`

</td>
<td>


Video interface bridge. A video interface bridge entity must have at least one sink pad and at least one source pad. It receives video frames on its sink pad from an input video bus of one type (HDMI, eDP, MIPI CSI-2, etc.), and outputs them on its source pad to an output video bus of another type (eDP, MIPI CSI-2, parallel, etc.).

</td>
</tr>
<tr>
<td>


`MEDIA_ENT_F_DV_DECODER`

</td>
<td>


Digital video decoder. The basic function of the video decoder is to accept digital video from a wide variety of sources and output it in some digital video standard, with appropriate timing signals.

</td>
</tr>
<tr>
<td>


`MEDIA_ENT_F_DV_ENCODER`

</td>
<td>


Digital video encoder. The basic function of the video encoder is to accept digital video from some digital video standard with appropriate timing signals (usually a parallel video bus with sync signals) and output this to a digital video output connector such as HDMI or DisplayPort.

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{5.5cm}|p{12.0cm}| -->

<a id="rst-media-ent-fl-connector"></a>
<a id="rst-media-ent-fl-default"></a>
<a id="rst-media-entity-flag"></a>


<table>
<caption>Media entity flags</caption>
<tbody>
<tr>
<td>


`MEDIA_ENT_FL_DEFAULT`

</td>
<td>


Default entity for its type. Used to discover the default audio, VBI and video devices, the default camera sensor, etc.

</td>
</tr>
<tr>
<td>


`MEDIA_ENT_FL_CONNECTOR`

</td>
<td>


The entity represents a connector.

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{6.5cm}|p{6.0cm}|p{4.8cm}| -->

<a id="rst-media-intf-t-alsa-timer"></a>
<a id="rst-media-intf-t-alsa-sequencer"></a>
<a id="rst-media-intf-t-alsa-hwdep"></a>
<a id="rst-media-intf-t-alsa-rawmidi"></a>
<a id="rst-media-intf-t-alsa-compress"></a>
<a id="rst-media-intf-t-alsa-control"></a>
<a id="rst-media-intf-t-alsa-pcm-playback"></a>
<a id="rst-media-intf-t-alsa-pcm-capture"></a>
<a id="rst-media-intf-t-v4l-touch"></a>
<a id="rst-media-intf-t-v4l-swradio"></a>
<a id="rst-media-intf-t-v4l-subdev"></a>
<a id="rst-media-intf-t-v4l-radio"></a>
<a id="rst-media-intf-t-v4l-vbi"></a>
<a id="rst-media-intf-t-v4l-video"></a>
<a id="rst-media-intf-t-dvb-net"></a>
<a id="rst-media-intf-t-dvb-ca"></a>
<a id="rst-media-intf-t-dvb-dvr"></a>
<a id="rst-media-intf-t-dvb-demux"></a>
<a id="rst-media-intf-t-dvb-fe"></a>
<a id="rst-media-intf-type"></a>


<table>
<caption>Media interface types</caption>
<tbody>
<tr>
<td>


`MEDIA_INTF_T_DVB_FE`

</td>
<td>


Device node interface for the Digital TV frontend

</td>
<td>


typically, /dev/dvb/adapter?/frontend?

</td>
</tr>
<tr>
<td>


`MEDIA_INTF_T_DVB_DEMUX`

</td>
<td>


Device node interface for the Digital TV demux

</td>
<td>


typically, /dev/dvb/adapter?/demux?

</td>
</tr>
<tr>
<td>


`MEDIA_INTF_T_DVB_DVR`

</td>
<td>


Device node interface for the Digital TV DVR

</td>
<td>


typically, /dev/dvb/adapter?/dvr?

</td>
</tr>
<tr>
<td>


`MEDIA_INTF_T_DVB_CA`

</td>
<td>


Device node interface for the Digital TV Conditional Access

</td>
<td>


typically, /dev/dvb/adapter?/ca?

</td>
</tr>
<tr>
<td>


`MEDIA_INTF_T_DVB_NET`

</td>
<td>


Device node interface for the Digital TV network control

</td>
<td>


typically, /dev/dvb/adapter?/net?

</td>
</tr>
<tr>
<td>


`MEDIA_INTF_T_V4L_VIDEO`

</td>
<td>


Device node interface for video (V4L)

</td>
<td>


typically, /dev/video?

</td>
</tr>
<tr>
<td>


`MEDIA_INTF_T_V4L_VBI`

</td>
<td>


Device node interface for VBI (V4L)

</td>
<td>


typically, /dev/vbi?

</td>
</tr>
<tr>
<td>


`MEDIA_INTF_T_V4L_RADIO`

</td>
<td>


Device node interface for radio (V4L)

</td>
<td>


typically, /dev/radio?

</td>
</tr>
<tr>
<td>


`MEDIA_INTF_T_V4L_SUBDEV`

</td>
<td>


Device node interface for a V4L subdevice

</td>
<td>


typically, /dev/v4l-subdev?

</td>
</tr>
<tr>
<td>


`MEDIA_INTF_T_V4L_SWRADIO`

</td>
<td>


Device node interface for Software Defined Radio (V4L)

</td>
<td>


typically, /dev/swradio?

</td>
</tr>
<tr>
<td>


`MEDIA_INTF_T_V4L_TOUCH`

</td>
<td>


Device node interface for Touch device (V4L)

</td>
<td>


typically, /dev/v4l-touch?

</td>
</tr>
<tr>
<td>


`MEDIA_INTF_T_ALSA_PCM_CAPTURE`

</td>
<td>


Device node interface for ALSA PCM Capture

</td>
<td>


typically, /dev/snd/pcmC?D?c

</td>
</tr>
<tr>
<td>


`MEDIA_INTF_T_ALSA_PCM_PLAYBACK`

</td>
<td>


Device node interface for ALSA PCM Playback

</td>
<td>


typically, /dev/snd/pcmC?D?p

</td>
</tr>
<tr>
<td>


`MEDIA_INTF_T_ALSA_CONTROL`

</td>
<td>


Device node interface for ALSA Control

</td>
<td>


typically, /dev/snd/controlC?

</td>
</tr>
<tr>
<td>


`MEDIA_INTF_T_ALSA_COMPRESS`

</td>
<td>


Device node interface for ALSA Compress

</td>
<td>


typically, /dev/snd/compr?

</td>
</tr>
<tr>
<td>


`MEDIA_INTF_T_ALSA_RAWMIDI`

</td>
<td>


Device node interface for ALSA Raw MIDI

</td>
<td>


typically, /dev/snd/midi?

</td>
</tr>
<tr>
<td>


`MEDIA_INTF_T_ALSA_HWDEP`

</td>
<td>


Device node interface for ALSA Hardware Dependent

</td>
<td>


typically, /dev/snd/hwC?D?

</td>
</tr>
<tr>
<td>


`MEDIA_INTF_T_ALSA_SEQUENCER`

</td>
<td>


Device node interface for ALSA Sequencer

</td>
<td>


typically, /dev/snd/seq

</td>
</tr>
<tr>
<td>


`MEDIA_INTF_T_ALSA_TIMER`

</td>
<td>


Device node interface for ALSA Timer

</td>
<td>


typically, /dev/snd/timer

</td>
</tr>
</tbody>
</table>

<!-- tabularcolumns: |p{5.5cm}|p{12.0cm}| -->

<a id="rst-media-pad-fl-must-connect"></a>
<a id="rst-media-pad-fl-source"></a>
<a id="rst-media-pad-fl-sink"></a>
<a id="rst-media-pad-flag"></a>


<table>
<caption>Media pad flags</caption>
<tbody>
<tr>
<td>


`MEDIA_PAD_FL_SINK`

</td>
<td>


Input pad, relative to the entity. Input pads sink data and are targets of links.

</td>
</tr>
<tr>
<td>


`MEDIA_PAD_FL_SOURCE`

</td>
<td>


Output pad, relative to the entity. Output pads source data and are origins of links.

</td>
</tr>
<tr>
<td>


`MEDIA_PAD_FL_MUST_CONNECT`

</td>
<td>


If this flag is set, then for this pad to be able to stream, it must be connected by at least one enabled link. There could be temporary reasons (e.g. device configuration dependent) for the pad to need enabled links even when this flag isn't set; the absence of the flag doesn't imply there is none.

</td>
</tr>
</tbody>
</table>

One and only one of `MEDIA_PAD_FL_SINK` and `MEDIA_PAD_FL_SOURCE` must be set for every pad.

<!-- tabularcolumns: |p{5.5cm}|p{12.0cm}| -->

<a id="rst-media-lnk-fl-link-type"></a>
<a id="rst-media-lnk-fl-dynamic"></a>
<a id="rst-media-lnk-fl-immutable"></a>
<a id="rst-media-lnk-fl-enabled"></a>
<a id="rst-media-link-flag"></a>


<table>
<caption>Media link flags</caption>
<tbody>
<tr>
<td>


`MEDIA_LNK_FL_ENABLED`

</td>
<td>


The link is enabled and can be used to transfer media data. When two or more links target a sink pad, only one of them can be enabled at a time.

</td>
</tr>
<tr>
<td>


`MEDIA_LNK_FL_IMMUTABLE`

</td>
<td>


The link enabled state can't be modified at runtime. An immutable link is always enabled.

</td>
</tr>
<tr>
<td>


`MEDIA_LNK_FL_DYNAMIC`

</td>
<td>


The link enabled state can be modified during streaming. This flag is set by drivers and is read-only for applications.

</td>
</tr>
<tr>
<td>


`MEDIA_LNK_FL_LINK_TYPE`

</td>
<td>


This is a bitmask that defines the type of the link. The following link types are currently supported:

<a id="rst-media-lnk-fl-data-link"></a>

`MEDIA_LNK_FL_DATA_LINK` for links that represent a data connection between two pads.

<a id="rst-media-lnk-fl-interface-link"></a>

`MEDIA_LNK_FL_INTERFACE_LINK` for links that associate an entity to its interface.

<a id="rst-media-lnk-fl-ancillary-link"></a>

`MEDIA_LNK_FL_ANCILLARY_LINK` for links that represent a physical relationship between two entities. The link may or may not be immutable, so applications must not assume either case.

</td>
</tr>
</tbody>
</table>
