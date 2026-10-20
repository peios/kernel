---
title: "Standard ALSA Control Names"
type: reference
description: "This document describes standard names of mixer controls."
---

<a id="rst-standard-alsa-control-names"></a>

This document describes standard names of mixer controls.

<a id="rst-standard-syntax"></a>

## Standard Syntax

Syntax: \[LOCATION\] SOURCE \[CHANNEL\] \[DIRECTION\] FUNCTION

<a id="rst-direction"></a>

### DIRECTION


<table>
<tbody>
<tr>
<td>


&lt;nothing&gt;

</td>
<td>


both directions

</td>
</tr>
<tr>
<td>


Playback

</td>
<td>


one direction

</td>
</tr>
<tr>
<td>


Capture

</td>
<td>


one direction

</td>
</tr>
<tr>
<td>


Bypass Playback

</td>
<td>


one direction

</td>
</tr>
<tr>
<td>


Bypass Capture

</td>
<td>


one direction

</td>
</tr>
</tbody>
</table>

<a id="rst-function"></a>

### FUNCTION


<table>
<tbody>
<tr>
<td>


Switch

</td>
<td>


on/off switch

</td>
</tr>
<tr>
<td>


Volume

</td>
<td>


amplifier

</td>
</tr>
<tr>
<td>


Route

</td>
<td>


route control, hardware specific

</td>
</tr>
</tbody>
</table>

<a id="rst-channel"></a>

### CHANNEL


<table>
<tbody>
<tr>
<td>


&lt;nothing&gt;

</td>
<td>


channel independent, or applies to all channels

</td>
</tr>
<tr>
<td>


Front

</td>
<td>


front left/right channels

</td>
</tr>
<tr>
<td>


Surround

</td>
<td>


rear left/right in 4.0/5.1 surround

</td>
</tr>
<tr>
<td>


CLFE

</td>
<td>


C/LFE channels

</td>
</tr>
<tr>
<td>


Center

</td>
<td>


center channel

</td>
</tr>
<tr>
<td>


LFE

</td>
<td>


LFE channel

</td>
</tr>
<tr>
<td>


Side

</td>
<td>


side left/right for 7.1 surround

</td>
</tr>
</tbody>
</table>

<a id="rst-location-physical-location-of-source"></a>

### LOCATION (Physical location of source)


<table>
<tbody>
<tr>
<td>


Front

</td>
<td>


front position

</td>
</tr>
<tr>
<td>


Rear

</td>
<td>


rear position

</td>
</tr>
<tr>
<td>


Dock

</td>
<td>


on docking station

</td>
</tr>
<tr>
<td>


Internal

</td>
<td>


internal

</td>
</tr>
</tbody>
</table>

<a id="rst-source"></a>

### SOURCE


<table>
<tbody>
<tr>
<td>


Master

</td>
<td>




</td>
</tr>
<tr>
<td>


Master Mono

</td>
<td>




</td>
</tr>
<tr>
<td>


Hardware Master

</td>
<td>




</td>
</tr>
<tr>
<td>


Speaker

</td>
<td>


internal speaker

</td>
</tr>
<tr>
<td>


Bass Speaker

</td>
<td>


internal LFE speaker

</td>
</tr>
<tr>
<td>


Headphone

</td>
<td>




</td>
</tr>
<tr>
<td>


Line Out

</td>
<td>




</td>
</tr>
<tr>
<td>


Beep

</td>
<td>


beep generator

</td>
</tr>
<tr>
<td>


Phone

</td>
<td>




</td>
</tr>
<tr>
<td>


Phone Input

</td>
<td>




</td>
</tr>
<tr>
<td>


Phone Output

</td>
<td>




</td>
</tr>
<tr>
<td>


Synth

</td>
<td>




</td>
</tr>
<tr>
<td>


FM

</td>
<td>




</td>
</tr>
<tr>
<td>


Mic

</td>
<td>




</td>
</tr>
<tr>
<td>


Headset Mic

</td>
<td>


mic part of combined headset jack - 4-pin headphone + mic

</td>
</tr>
<tr>
<td>


Headphone Mic

</td>
<td>


mic part of either/or - 3-pin headphone or mic

</td>
</tr>
<tr>
<td>


Line

</td>
<td>


input only, use "Line Out" for output

</td>
</tr>
<tr>
<td>


CD

</td>
<td>




</td>
</tr>
<tr>
<td>


Video

</td>
<td>




</td>
</tr>
<tr>
<td>


Zoom Video

</td>
<td>




</td>
</tr>
<tr>
<td>


Aux

</td>
<td>




</td>
</tr>
<tr>
<td>


PCM

</td>
<td>




</td>
</tr>
<tr>
<td>


PCM Pan

</td>
<td>




</td>
</tr>
<tr>
<td>


Loopback

</td>
<td>




</td>
</tr>
<tr>
<td>


Analog Loopback

</td>
<td>


D/A -&gt; A/D loopback

</td>
</tr>
<tr>
<td>


Digital Loopback

</td>
<td>


playback -&gt; capture loopback - without analog path

</td>
</tr>
<tr>
<td>


Mono

</td>
<td>




</td>
</tr>
<tr>
<td>


Mono Output

</td>
<td>




</td>
</tr>
<tr>
<td>


Multi

</td>
<td>




</td>
</tr>
<tr>
<td>


ADC

</td>
<td>




</td>
</tr>
<tr>
<td>


Wave

</td>
<td>




</td>
</tr>
<tr>
<td>


Music

</td>
<td>




</td>
</tr>
<tr>
<td>


I2S

</td>
<td>




</td>
</tr>
<tr>
<td>


IEC958

</td>
<td>




</td>
</tr>
<tr>
<td>


HDMI

</td>
<td>




</td>
</tr>
<tr>
<td>


SPDIF

</td>
<td>


output only

</td>
</tr>
<tr>
<td>


SPDIF In

</td>
<td>




</td>
</tr>
<tr>
<td>


Digital In

</td>
<td>




</td>
</tr>
<tr>
<td>


HDMI/DP

</td>
<td>


either HDMI or DisplayPort

</td>
</tr>
</tbody>
</table>

<a id="rst-exceptions-deprecated"></a>

## Exceptions (deprecated)


<table>
<tbody>
<tr>
<td>


\[Analogue\|Digital\] Capture Source

</td>
<td>




</td>
</tr>
<tr>
<td>


\[Analogue\|Digital\] Capture Switch

</td>
<td>


aka input gain switch

</td>
</tr>
<tr>
<td>


\[Analogue\|Digital\] Capture Volume

</td>
<td>


aka input gain volume

</td>
</tr>
<tr>
<td>


\[Analogue\|Digital\] Playback Switch

</td>
<td>


aka output gain switch

</td>
</tr>
<tr>
<td>


\[Analogue\|Digital\] Playback Volume

</td>
<td>


aka output gain volume

</td>
</tr>
<tr>
<td>


Tone Control - Switch

</td>
<td>




</td>
</tr>
<tr>
<td>


Tone Control - Bass

</td>
<td>




</td>
</tr>
<tr>
<td>


Tone Control - Treble

</td>
<td>




</td>
</tr>
<tr>
<td>


3D Control - Switch

</td>
<td>




</td>
</tr>
<tr>
<td>


3D Control - Center

</td>
<td>




</td>
</tr>
<tr>
<td>


3D Control - Depth

</td>
<td>




</td>
</tr>
<tr>
<td>


3D Control - Wide

</td>
<td>




</td>
</tr>
<tr>
<td>


3D Control - Space

</td>
<td>




</td>
</tr>
<tr>
<td>


3D Control - Level

</td>
<td>




</td>
</tr>
<tr>
<td>


Mic Boost \[(?dB)\]

</td>
<td>




</td>
</tr>
</tbody>
</table>

<a id="rst-pcm-interface"></a>

## PCM interface


<table>
<tbody>
<tr>
<td>


Sample Clock Source

</td>
<td>


\{ "Word", "Internal", "AutoSync" \}

</td>
</tr>
<tr>
<td>


Clock Sync Status

</td>
<td>


\{ "Lock", "Sync", "No Lock" \}

</td>
</tr>
<tr>
<td>


External Rate

</td>
<td>


external capture rate

</td>
</tr>
<tr>
<td>


Capture Rate

</td>
<td>


capture rate taken from external source

</td>
</tr>
</tbody>
</table>

<a id="rst-iec958-s-pdif-interface"></a>

## IEC958 (S/PDIF) interface


<table>
<tbody>
<tr>
<td>


IEC958 \[...\] \[Playback\|Capture\] Switch

</td>
<td>


turn on/off the IEC958 interface

</td>
</tr>
<tr>
<td>


IEC958 \[...\] \[Playback\|Capture\] Volume

</td>
<td>


digital volume control

</td>
</tr>
<tr>
<td>


IEC958 \[...\] \[Playback\|Capture\] Default

</td>
<td>


default or global value - read/write

</td>
</tr>
<tr>
<td>


IEC958 \[...\] \[Playback\|Capture\] Mask

</td>
<td>


consumer and professional mask

</td>
</tr>
<tr>
<td>


IEC958 \[...\] \[Playback\|Capture\] Con Mask

</td>
<td>


consumer mask

</td>
</tr>
<tr>
<td>


IEC958 \[...\] \[Playback\|Capture\] Pro Mask

</td>
<td>


professional mask

</td>
</tr>
<tr>
<td>


IEC958 \[...\] \[Playback\|Capture\] PCM Stream

</td>
<td>


the settings assigned to a PCM stream

</td>
</tr>
<tr>
<td>


IEC958 Q-subcode \[Playback\|Capture\] Default

</td>
<td>


Q-subcode bits

</td>
</tr>
<tr>
<td>


IEC958 Preamble \[Playback\|Capture\] Default

</td>
<td>


burst preamble words (4\*16bits)

</td>
</tr>
</tbody>
</table>
