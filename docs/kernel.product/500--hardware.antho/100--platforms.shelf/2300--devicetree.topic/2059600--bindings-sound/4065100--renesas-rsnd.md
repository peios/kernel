---
title: "Renesas R-Car sound"
type: reference
description: "Device-tree binding reference for Renesas R-Car sound."
---

---

## \* Modules

Renesas R-Car and RZ/G sound is constructed from below modules
(for Gen2 or later)

```text
 SCU		: Sampling Rate Converter Unit
```

```text
  - SRC		: Sampling Rate Converter
  - CMD
   - CTU	: Channel Transfer Unit
   - MIX	: Mixer
   - DVC	: Digital Volume and Mute Function
 SSIU		: Serial Sound Interface Unit
 SSI		: Serial Sound Interface
```

See detail of each module's channels, connection, limitation on datasheet

---

## \* Multi channel

Multi channel is supported by Multi-SSI, or TDM-SSI.

```text
 Multi-SSI	: 6ch case, you can use stereo x 3 SSI
 TDM-SSI	: 6ch case, you can use TDM
```

---

## \* Enable/Disable each modules

See datasheet to check SRC/CTU/MIX/DVC connect-limitation.
DT controls enabling/disabling module.
${LINUX}/arch/arm/boot/dts/r8a7790-lager.dts can be good example.
This is example of

Playback: \[MEM\] -&gt; \[SRC2\] -&gt; \[DVC0\] -&gt; \[SSIU0/SSI0\] -&gt; \[codec\]
Capture:  \[MEM\] &lt;- \[DVC1\] &lt;- \[SRC3\] &lt;- \[SSIU1/SSI1\] &lt;- \[codec\]

see "Example: simple sound card"

You can use below.
${LINUX}/arch/arm/boot/dts/r8a7790.dts can be good example.

```text
	&src0	&ctu00	&mix0	&dvc0	&ssi0
	&src1	&ctu01	&mix1	&dvc1	&ssi1
	&src2	&ctu02			&ssi2
	&src3	&ctu03			&ssi3
	&src4				&ssi4
	&src5	&ctu10			&ssi5
	&src6	&ctu11			&ssi6
	&src7	&ctu12			&ssi7
	&src8	&ctu13			&ssi8
	&src9				&ssi9
```

---

## \* SRC (Sampling Rate Converter)

```text
 [xx]Hz        [yy]Hz
 ------> [SRC] ------>
```

SRC can convert \[xx\]Hz to \[yy\]Hz. Then, it has below 2 modes

```text
 Asynchronous mode:	input data / output data are based on different clocks.
```

```text
			you can use this mode on Playback / Capture
 Synchronous mode:	input data / output data are based on same clocks.
			This mode will be used if system doesn't have its input clock,
			for example digital TV case.
			you can use this mode on Playback
```

---

## \*\*     Asynchronous mode

You need to use "simple-scu-audio-card" or "audio-graph-scu-card" for it.
see "Example: simple sound card for Asynchronous mode"

---

## \*\*     Synchronous mode

```text
	> amixer set "SRC Out Rate" on
	> aplay xxxx.wav
	> amixer set "SRC Out Rate" 48000
	> amixer set "SRC Out Rate" 44100
```

---

## \* CTU (Channel Transfer Unit)

```text
 [xx]ch        [yy]ch
 ------> [CTU] -------->
```

CTU can convert \[xx\]ch to \[yy\]ch, or exchange outputted channel.
CTU conversion needs matrix settings.
For more detail information, see below

```text
	Renesas R-Car datasheet
	 - Sampling Rate Converter Unit (SCU)
	  - SCU Operation
	   - CMD Block
	    - Functional Blocks in CMD
```

```text
	Renesas R-Car datasheet
	 - Sampling Rate Converter Unit (SCU)
	  - Register Description
	   - CTUn Scale Value exx Register (CTUn_SVxxR)
```

```text
	${LINUX}/sound/soc/renesas/rcar/ctu.c
	 - comment of header
```

You need to use "simple-scu-audio-card" or "audio-graph-scu-card" for it.
see "Example: simple sound card for channel convert"

Ex) Exchange output channel
 Input -&gt; Output
  1ch  -&gt;  0ch
  0ch  -&gt;  1ch

```text
  example of using matrix
```

```text
	output 0ch = (input 0ch x 0) + (input 1ch x 1)
	output 1ch = (input 0ch x 1) + (input 1ch x 0)
```

```text
	amixer set "CTU Reset" on
	amixer set "CTU Pass" 9,10
	amixer set "CTU SV0" 0,4194304
	amixer set "CTU SV1" 4194304,0
```

```text
 example of changing connection
```

```text
	amixer set "CTU Reset" on
	amixer set "CTU Pass" 2,1
```

---

## \* MIX (Mixer)

MIX merges 2 sounds path. You can see 2 sound interface on system,
and these sounds will be merged by MIX.

```text
	aplay -D plughw:0,0 xxxx.wav &
	aplay -D plughw:0,1 yyyy.wav
```

You need to use "simple-scu-audio-card" or "audio-graph-scu-card" for it.
Ex)

```text
	[MEM] -> [SRC1] -> [CTU02] -+-> [MIX0] -> [DVC0] -> [SSI0]
	                            |
	[MEM] -> [SRC2] -> [CTU03] -+
```

see "Example: simple sound card for MIXer"

---

## \* DVC (Digital Volume and Mute Function)

DVC controls Playback/Capture volume.

Playback Volume

```text
	amixer set "DVC Out" 100%
```

Capture Volume

```text
	amixer set "DVC In" 100%
```

Playback Mute

```text
	amixer set "DVC Out Mute" on
```

Capture Mute

```text
	amixer set "DVC In Mute" on
```

Volume Ramp

```text
	amixer set "DVC Out Ramp Up Rate"   "0.125 dB/64 steps"
	amixer set "DVC Out Ramp Down Rate" "0.125 dB/512 steps"
	amixer set "DVC Out Ramp" on
	aplay xxx.wav &
	amixer set "DVC Out"  80%  // Volume Down
	amixer set "DVC Out" 100%  // Volume Up
```

---

## \* SSIU (Serial Sound Interface Unit)

SSIU can avoid some under/over run error, because it has some buffer.
But you can't use it if SSI was PIO mode.
In DMA mode, you can select not to use SSIU by using "no-busif" via SSI.

SSIU handles BUSIF which will be used for TDM Split mode.
This driver is assuming that audio-graph card will be used.

TDM Split mode merges 4 sounds. You can see 4 sound interface on system,
and these sounds will be merged SSIU/SSI.

```text
	aplay -D plughw:0,0 xxxx.wav &
	aplay -D plughw:0,1 xxxx.wav &
	aplay -D plughw:0,2 xxxx.wav &
	aplay -D plughw:0,3 xxxx.wav
```

```text
	          2ch                     8ch
	[MEM] -> [SSIU 30] -+-> [SSIU 3] --> [Codec]
	          2ch       |
	[MEM] -> [SSIU 31] -+
	          2ch       |
	[MEM] -> [SSIU 32] -+
	          2ch       |
	[MEM] -> [SSIU 33] -+
```

see "Example: simple sound card for TDM Split"

---

## \* SSI (Serial Sound Interface)

\*\*  PIO mode

You can use PIO mode which is for connection check by using.
Note: The system will drop non-SSI modules in PIO mode
even though if DT is selecting other modules.

```dts
	&ssi0 {
		pio-transfer
	};
```

\*\* DMA mode without SSIU

You can use DMA without SSIU.
Note: under/over run, or noise are likely to occur

```dts
	&ssi0 {
		no-busif;
	};
```

\*\* PIN sharing

Each SSI can share WS pin. It is based on platform.
This is example if SSI1 want to share WS pin with SSI0

```dts
	&ssi1 {
		shared-pin;
	};
```

\*\* Multi-SSI

You can use Multi-SSI.
This is example of SSI0/SSI1/SSI2 (= for 6ch)

see "Example: simple sound card for Multi channel"

\*\* TDM-SSI

You can use TDM with SSI.
This is example of TDM 6ch.
Driver can automatically switches TDM &lt;-&gt; stereo mode in this case.

see "Example: simple sound card for TDM"
