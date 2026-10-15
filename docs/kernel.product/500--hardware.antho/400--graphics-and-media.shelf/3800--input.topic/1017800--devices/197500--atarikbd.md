---
title: "Intelligent Keyboard (ikbd) Protocol"
type: reference
description: "The Atari Corp. Intelligent Keyboard (ikbd) is a general purpose keyboard controller that is flexible enough that it can be used in a variety of products without modification. The keyboard, with its microcontroller, provides a convenient…"
---

<a id="rst-intelligent-keyboard-ikbd-protocol"></a>

<a id="rst-introduction"></a>

## Introduction

The Atari Corp. Intelligent Keyboard (ikbd) is a general purpose keyboard controller that is flexible enough that it can be used in a variety of products without modification. The keyboard, with its microcontroller, provides a convenient connection point for a mouse and switch-type joysticks. The ikbd processor also maintains a time-of-day clock with one second resolution. The ikbd has been designed to be general enough that it can be used with a variety of new computer products. Product variations in a number of keyswitches, mouse resolution, etc. can be accommodated. The ikbd communicates with the main processor over a high speed bi-directional serial interface. It can function in a variety of modes to facilitate different applications of the keyboard,  joysticks, or mouse. Limited use of the controller is possible in applications in which only a unidirectional communications medium is available by carefully designing the default modes.

<a id="rst-keyboard"></a>

## Keyboard

The keyboard always returns key make/break scan codes. The ikbd generates keyboard scan codes for each key press and release. The key scan make (key closure) codes start at 1, and are defined in Appendix A. For example, the ISO key position in the scan code table should exist even if no keyswitch exists in that position on a particular keyboard. The break code for each key is obtained by ORing 0x80 with the make code.

The special codes 0xF6 through 0xFF are reserved for use as follows:


<table>
<thead>
<tr>
<th>


Code

</th>
<th>


Command

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


0xF6

</td>
<td>


status report

</td>
</tr>
<tr>
<td>


0xF7

</td>
<td>


absolute mouse position record

</td>
</tr>
<tr>
<td>


0xF8-0xFB

</td>
<td>


relative mouse position records (lsbs determined by mouse button states)

</td>
</tr>
<tr>
<td>


0xFC

</td>
<td>


time-of-day

</td>
</tr>
<tr>
<td>


0xFD

</td>
<td>


joystick report (both sticks)

</td>
</tr>
<tr>
<td>


0xFE

</td>
<td>


joystick 0 event

</td>
</tr>
<tr>
<td>


0xFF

</td>
<td>


joystick 1 event

</td>
</tr>
</tbody>
</table>

The two shift keys return different scan codes in this mode. The ENTER key and the RETurn key are also distinct.

<a id="rst-mouse"></a>

## Mouse

The mouse port should be capable of supporting a mouse with resolution of approximately 200 counts (phase changes or 'clicks') per inch of travel. The mouse should be scanned at a rate that will permit accurate tracking at velocities up to 10 inches per second. The ikbd can report mouse motion in three distinctly different ways. It can report relative motion, absolute motion in a coordinate system maintained within the ikbd, or by converting mouse motion into keyboard cursor control key equivalents. The mouse buttons can be treated as part of the mouse or as additional keyboard keys.

<a id="rst-relative-position-reporting"></a>

### Relative Position Reporting

In relative position mode, the ikbd will return relative mouse position records whenever a mouse event occurs. A mouse event consists of a mouse button being pressed or released, or motion in either axis exceeding a settable threshold of motion. Regardless of the threshold, all bits of resolution are returned to the host computer. Note that the ikbd may return mouse relative position reports with significantly more than the threshold delta x or y. This may happen since no relative mouse motion events will be generated: (a) while the keyboard has been 'paused' ( the event will be stored until keyboard communications is resumed) (b) while any event is being transmitted.

The relative mouse position record is a three byte record of the form (regardless of keyboard mode):



```text
%111110xy           ; mouse position record flag
                    ; where y is the right button state
                    ; and x is the left button state
X                   ; delta x as twos complement integer
Y                   ; delta y as twos complement integer
```

Note that the value of the button state bits should be valid even if the MOUSE BUTTON ACTION has set the buttons to act like part of the keyboard. If the accumulated motion before the report packet is generated exceeds the +127...-128 range, the motion is broken into multiple packets. Note that the sign of the delta y reported is a function of the Y origin selected.

<a id="rst-absolute-position-reporting"></a>

### Absolute Position reporting

The ikbd can also maintain absolute mouse position. Commands exist for resetting the mouse position, setting X/Y scaling, and interrogating the current mouse position.

<a id="rst-mouse-cursor-key-mode"></a>

### Mouse Cursor Key Mode

The ikbd can translate mouse motion into the equivalent cursor keystrokes. The number of mouse clicks per keystroke is independently programmable in each axis. The ikbd internally maintains mouse motion information to the highest resolution available, and merely generates a pair of cursor key events for each multiple of the scale factor. Mouse motion produces the cursor key make code immediately followed by the break code for the appropriate cursor key. The mouse buttons produce scan codes above those normally assigned for the largest envisioned keyboard (i.e. LEFT=0x74 &amp; RIGHT=0x75).

<a id="rst-joystick"></a>

## Joystick

<a id="rst-joystick-event-reporting"></a>

### Joystick Event Reporting

In this mode, the ikbd generates a record whenever the joystick position is changed (i.e. for each opening or closing of a joystick switch or trigger).

The joystick event record is two bytes of the form:



```text
%1111111x           ; Joystick event marker
                    ; where x is Joystick 0 or 1
%x000yyyy           ; where yyyy is the stick position
                    ; and x is the trigger
```

<a id="rst-joystick-interrogation"></a>

### Joystick Interrogation

The current state of the joystick ports may be interrogated at any time in this mode by sending an 'Interrogate Joystick' command to the ikbd.

The ikbd response to joystick interrogation is a three byte report of the form:



```text
0xFD                ; joystick report header
%x000yyyy           ; Joystick 0
%x000yyyy           ; Joystick 1
                    ; where x is the trigger
                    ; and yyy is the stick position
```

<a id="rst-joystick-monitoring"></a>

### Joystick Monitoring

A mode is available that devotes nearly all of the keyboard communications time to reporting the state of the joystick ports at a user specifiable rate. It remains in this mode until reset or commanded into another mode. The PAUSE command in this mode not only stop the output but also temporarily stops scanning the joysticks (samples are not queued).

<a id="rst-fire-button-monitoring"></a>

### Fire Button Monitoring

A mode is provided to permit monitoring a single input bit at a high rate. In this mode the ikbd monitors the state of the Joystick 1 fire button at the maximum rate permitted by the serial communication channel. The data is packed 8 bits per byte for transmission to the host. The ikbd remains in this mode until reset or commanded into another mode. The PAUSE command in this mode not only stops the output but also temporarily stops scanning the button (samples are not queued).

<a id="rst-joystick-key-code-mode"></a>

### Joystick Key Code Mode

The ikbd may be commanded to translate the use of either joystick into the equivalent cursor control keystroke(s). The ikbd provides a single breakpoint velocity joystick cursor. Joystick events produce the make code, immediately followed by the break code for the appropriate cursor motion keys. The trigger or fire buttons of the joysticks produce pseudo key scan codes above those used by the largest key matrix envisioned (i.e. JOYSTICK0=0x74, JOYSTICK1=0x75).

<a id="rst-time-of-day-clock"></a>

## Time-of-Day Clock

The ikbd also maintains a time-of-day clock for the system. Commands are available to set and interrogate the timer-of-day clock. Time-keeping is maintained down to a resolution of one second.

<a id="rst-status-inquiries"></a>

## Status Inquiries

The current state of ikbd modes and parameters may be found by sending status inquiry commands that correspond to the ikbd set commands.

<a id="rst-power-up-mode"></a>

## Power-Up Mode

The keyboard controller will perform a simple self-test on power-up to detect major controller faults (ROM checksum and RAM test) and such things as stuck keys. Any keys down at power-up are presumed to be stuck, and their BREAK (sic) code is returned (which without the preceding MAKE code is a flag for a keyboard error). If the controller self-test completes without error, the code 0xF0 is returned. (This code will be used to indicate the version/release of the ikbd controller. The first release of the ikbd is version 0xF0, should there be a second release it will be 0xF1, and so on.) The ikbd defaults to a mouse position reporting with threshold of 1 unit in either axis and the Y=0 origin at the top of the screen, and joystick event reporting mode for joystick 1, with both buttons being logically assigned to the mouse. After any joystick command, the ikbd assumes that joysticks are connected to both Joystick0 and Joystick1. Any mouse command (except MOUSE DISABLE) then causes port 0 to again be scanned as if it were a mouse, and both buttons are logically connected to it. If a mouse disable command is received while port 0 is presumed to be a mouse, the button is logically assigned to Joystick1 (until the mouse is reenabled by another mouse command).

<a id="rst-ikbd-command-set"></a>

## ikbd Command Set

This section contains a list of commands that can be sent to the ikbd. Command codes (such as 0x00) which are not specified should perform no operation (NOPs).

<a id="rst-reset"></a>

### RESET



```text
0x80
0x01
```

N.B. The RESET command is the only two byte command understood by the ikbd. Any byte following an 0x80 command byte other than 0x01 is ignored (and causes the 0x80 to be ignored). A reset may also be caused by sending a break lasting at least 200mS to the ikbd. Executing the RESET command returns the keyboard to its default (power-up) mode and parameter settings. It does not affect the time-of-day clock. The RESET command or function causes the ikbd to perform a simple self-test. If the test is successful, the ikbd will send the code of 0xF0 within 300mS of receipt of the RESET command (or the end of the break, or power-up). The ikbd will then scan the key matrix for any stuck (closed) keys. Any keys found closed will cause the break scan code to be generated (the break code arriving without being preceded by the make code is a flag for a key matrix error).

<a id="rst-set-mouse-button-action"></a>

### SET MOUSE BUTTON ACTION



```text
0x07
%00000mss           ; mouse button action
                    ;       (m is presumed = 1 when in MOUSE KEYCODE mode)
                    ; mss=0xy, mouse button press or release causes mouse
                    ;  position report
                    ;  where y=1, mouse key press causes absolute report
                    ;  and x=1, mouse key release causes absolute report
                    ; mss=100, mouse buttons act like keys
```

This command sets how the ikbd should treat the buttons on the mouse. The default mouse button action mode is %00000000, the buttons are treated as part of the mouse logically. When buttons act like keys, LEFT=0x74 &amp; RIGHT=0x75.

<a id="rst-set-relative-mouse-position-reporting"></a>

### SET RELATIVE MOUSE POSITION REPORTING



```text
0x08
```

Set relative mouse position reporting. (DEFAULT) Mouse position packets are generated asynchronously by the ikbd whenever motion exceeds the setable threshold in either axis (see SET MOUSE THRESHOLD). Depending upon the mouse key mode, mouse position reports may also be generated when either mouse button is pressed or released. Otherwise the mouse buttons behave as if they were keyboard keys.

<a id="rst-set-absolute-mouse-positioning"></a>

### SET ABSOLUTE MOUSE POSITIONING



```text
0x09
XMSB                ; X maximum (in scaled mouse clicks)
XLSB
YMSB                ; Y maximum (in scaled mouse clicks)
YLSB
```

Set absolute mouse position maintenance. Resets the ikbd maintained X and Y coordinates. In this mode, the value of the internally maintained coordinates does NOT wrap between 0 and large positive numbers. Excess motion below 0 is ignored. The command sets the maximum positive value that can be attained in the scaled coordinate system. Motion beyond that value is also ignored.

<a id="rst-set-mouse-keycode-mode"></a>

### SET MOUSE KEYCODE MODE



```text
0x0A
deltax              ; distance in X clicks to return (LEFT) or (RIGHT)
deltay              ; distance in Y clicks to return (UP) or (DOWN)
```

Set mouse monitoring routines to return cursor motion keycodes instead of either RELATIVE or ABSOLUTE motion records. The ikbd returns the appropriate cursor keycode after mouse travel exceeding the user specified deltas in either axis. When the keyboard is in key scan code mode, mouse motion will cause the make code immediately followed by the break code. Note that this command is not affected by the mouse motion origin.

<a id="rst-set-mouse-threshold"></a>

### SET MOUSE THRESHOLD



```text
0x0B
X                   ; x threshold in mouse ticks (positive integers)
Y                   ; y threshold in mouse ticks (positive integers)
```

This command sets the threshold before a mouse event is generated. Note that it does NOT affect the resolution of the data returned to the host. This command is valid only in RELATIVE MOUSE POSITIONING mode. The thresholds default to 1 at RESET (or power-up).

<a id="rst-set-mouse-scale"></a>

### SET MOUSE SCALE



```text
0x0C
X                   ; horizontal mouse ticks per internal X
Y                   ; vertical mouse ticks per internal Y
```

This command sets the scale factor for the ABSOLUTE MOUSE POSITIONING mode. In this mode, the specified number of mouse phase changes ('clicks') must occur before the internally maintained coordinate is changed by one (independently scaled for each axis). Remember that the mouse position information is available only by interrogating the ikbd in the ABSOLUTE MOUSE POSITIONING mode unless the ikbd has been commanded to report on button press or release (see SET MOUSE BUTTON ACTION).

<a id="rst-interrogate-mouse-position"></a>

### INTERROGATE MOUSE POSITION



```text
0x0D
Returns:
        0xF7       ; absolute mouse position header
BUTTONS
        0000dcba   ; where a is right button down since last interrogation
                   ; b is right button up since last
                   ; c is left button down since last
                   ; d is left button up since last
        XMSB       ; X coordinate
        XLSB
        YMSB       ; Y coordinate
        YLSB
```

The INTERROGATE MOUSE POSITION command is valid when in the ABSOLUTE MOUSE POSITIONING mode, regardless of the setting of the MOUSE BUTTON ACTION.

<a id="rst-load-mouse-position"></a>

### LOAD MOUSE POSITION



```text
0x0E
0x00                ; filler
XMSB                ; X coordinate
XLSB                ; (in scaled coordinate system)
YMSB                ; Y coordinate
YLSB
```

This command allows the user to preset the internally maintained absolute mouse position.

<a id="rst-set-y-0-at-bottom"></a>

### SET Y=0 AT BOTTOM



```text
0x0F
```

This command makes the origin of the Y axis to be at the bottom of the logical coordinate system internal to the ikbd for all relative or absolute mouse motion. This causes mouse motion toward the user to be negative in sign and away from the user to be positive.

<a id="rst-set-y-0-at-top"></a>

### SET Y=0 AT TOP



```text
0x10
```

Makes the origin of the Y axis to be at the top of the logical coordinate system within the ikbd for all relative or absolute mouse motion. (DEFAULT) This causes mouse motion toward the user to be positive in sign and away from the user to be negative.

<a id="rst-resume"></a>

### RESUME



```text
0x11
```

Resume sending data to the host. Since any command received by the ikbd after its output has been paused also causes an implicit RESUME this command can be thought of as a NO OPERATION command. If this command is received by the ikbd and it is not PAUSED, it is simply ignored.

<a id="rst-disable-mouse"></a>

### DISABLE MOUSE



```text
0x12
```

All mouse event reporting is disabled (and scanning may be internally disabled). Any valid mouse mode command resumes mouse motion monitoring. (The valid mouse mode commands are SET RELATIVE MOUSE POSITION REPORTING, SET ABSOLUTE MOUSE POSITIONING, and SET MOUSE KEYCODE MODE. ) N.B. If the mouse buttons have been commanded to act like keyboard keys, this command DOES affect their actions.

<a id="rst-pause-output"></a>

### PAUSE OUTPUT



```text
0x13
```

Stop sending data to the host until another valid command is received. Key matrix activity is still monitored and scan codes or ASCII characters enqueued (up to the maximum supported by the microcontroller) to be sent when the host allows the output to be resumed. If in the JOYSTICK EVENT REPORTING mode, joystick events are also queued. Mouse motion should be accumulated while the output is paused. If the ikbd is in RELATIVE MOUSE POSITIONING REPORTING mode, motion is accumulated beyond the normal threshold limits to produce the minimum number of packets necessary for transmission when output is resumed. Pressing or releasing either mouse button causes any accumulated motion to be immediately queued as packets, if the mouse is in RELATIVE MOUSE POSITION REPORTING mode. Because of the limitations of the microcontroller memory this command should be used sparingly, and the output should not be shut of for more than &lt;tbd&gt; milliseconds at a time. The output is stopped only at the end of the current 'even'. If the PAUSE OUTPUT command is received in the middle of a multiple byte report, the packet will still be transmitted to conclusion and then the PAUSE will take effect. When the ikbd is in either the JOYSTICK MONITORING mode or the FIRE BUTTON MONITORING mode, the PAUSE OUTPUT command also temporarily stops the monitoring process (i.e. the samples are not enqueued for transmission).

<a id="rst-set-joystick-event-reporting"></a>

### SET JOYSTICK EVENT REPORTING



```text
0x14
```

Enter JOYSTICK EVENT REPORTING mode (DEFAULT). Each opening or closure of a joystick switch or trigger causes a joystick event record to be generated.

<a id="rst-set-joystick-interrogation-mode"></a>

### SET JOYSTICK INTERROGATION MODE



```text
0x15
```

Disables JOYSTICK EVENT REPORTING. Host must send individual JOYSTICK INTERROGATE commands to sense joystick state.

<a id="rst-joystick-interrogate"></a>

### JOYSTICK INTERROGATE



```text
0x16
```

Return a record indicating the current state of the joysticks. This command is valid in either the JOYSTICK EVENT REPORTING mode or the JOYSTICK INTERROGATION MODE.

<a id="rst-set-joystick-monitoring"></a>

### SET JOYSTICK MONITORING



```text
0x17
rate                ; time between samples in hundredths of a second
Returns: (in packets of two as long as in mode)
        %000000xy   ; where y is JOYSTICK1 Fire button
                    ; and x is JOYSTICK0 Fire button
        %nnnnmmmm   ; where m is JOYSTICK1 state
                    ; and n is JOYSTICK0 state
```

Sets the ikbd to do nothing but monitor the serial command line, maintain the time-of-day clock, and monitor the joystick. The rate sets the interval between joystick samples. N.B. The user should not set the rate higher than the serial communications channel will allow the 2 bytes packets to be transmitted.

<a id="rst-set-fire-button-monitoring"></a>

### SET FIRE BUTTON MONITORING



```text
0x18
Returns: (as long as in mode)
        %bbbbbbbb   ; state of the JOYSTICK1 fire button packed
                    ; 8 bits per byte, the first sample if the MSB
```

Set the ikbd to do nothing but monitor the serial command line, maintain the time-of-day clock, and monitor the fire button on Joystick 1. The fire button is scanned at a rate that causes 8 samples to be made in the time it takes for the previous byte to be sent to the host (i.e. scan rate = 8/10 \* baud rate). The sample interval should be as constant as possible.

<a id="rst-set-joystick-keycode-mode"></a>

### SET JOYSTICK KEYCODE MODE



```text
0x19
RX                  ; length of time (in tenths of seconds) until
                    ; horizontal velocity breakpoint is reached
RY                  ; length of time (in tenths of seconds) until
                    ; vertical velocity breakpoint is reached
TX                  ; length (in tenths of seconds) of joystick closure
                    ; until horizontal cursor key is generated before RX
                    ; has elapsed
TY                  ; length (in tenths of seconds) of joystick closure
                    ; until vertical cursor key is generated before RY
                    ; has elapsed
VX                  ; length (in tenths of seconds) of joystick closure
                    ; until horizontal cursor keystrokes are generated
                    ; after RX has elapsed
VY                  ; length (in tenths of seconds) of joystick closure
                    ; until vertical cursor keystrokes are generated
                    ; after RY has elapsed
```

In this mode, joystick 0 is scanned in a way that simulates cursor keystrokes. On initial closure, a keystroke pair (make/break) is generated. Then up to Rn tenths of seconds later, keystroke pairs are generated every Tn tenths of seconds. After the Rn breakpoint is reached, keystroke pairs are generated every Vn tenths of seconds. This provides a velocity (auto-repeat) breakpoint feature. Note that by setting RX and/or Ry to zero, the velocity feature can be disabled. The values of TX and TY then become meaningless, and the generation of cursor 'keystrokes' is set by VX and VY.

<a id="rst-disable-joysticks"></a>

### DISABLE JOYSTICKS



```text
0x1A
```

Disable the generation of any joystick events (and scanning may be internally disabled). Any valid joystick mode command resumes joystick monitoring. (The joystick mode commands are SET JOYSTICK EVENT REPORTING, SET JOYSTICK INTERROGATION MODE, SET JOYSTICK MONITORING, SET FIRE BUTTON MONITORING, and SET JOYSTICK KEYCODE MODE.)

<a id="rst-time-of-day-clock-set"></a>

### TIME-OF-DAY CLOCK SET



```text
0x1B
YY                  ; year (2 least significant digits)
MM                  ; month
DD                  ; day
hh                  ; hour
mm                  ; minute
ss                  ; second
```

All time-of-day data should be sent to the ikbd in packed BCD format. Any digit that is not a valid BCD digit should be treated as a 'don't care' and not alter that particular field of the date or time. This permits setting only some subfields of the time-of-day clock.

<a id="rst-interrogate-time-of-dat-clock"></a>

### INTERROGATE TIME-OF-DAT CLOCK



```text
0x1C
Returns:
        0xFC        ; time-of-day event header
        YY          ; year (2 least significant digits)
        MM          ; month
        DD          ; day
        hh          ; hour
        mm          ; minute
        ss          ; second

All time-of-day is sent in packed BCD format.
```

<a id="rst-memory-load"></a>

### MEMORY LOAD



```text
0x20
ADRMSB              ; address in controller
ADRLSB              ; memory to be loaded
NUM                 ; number of bytes (0-128)
{ data }
```

This command permits the host to load arbitrary values into the ikbd controller memory. The time between data bytes must be less than 20ms.

<a id="rst-memory-read"></a>

### MEMORY READ



```text
0x21
ADRMSB              ; address in controller
ADRLSB              ; memory to be read
Returns:
        0xF6        ; status header
        0x20        ; memory access
        { data }    ; 6 data bytes starting at ADR
```

This command permits the host to read from the ikbd controller memory.

<a id="rst-controller-execute"></a>

### CONTROLLER EXECUTE



```text
0x22
ADRMSB              ; address of subroutine in
ADRLSB              ; controller memory to be called
```

This command allows the host to command the execution of a subroutine in the ikbd controller memory.

<a id="rst-status-inquiries-1"></a>

### STATUS INQUIRIES



```text
Status commands are formed by inclusively ORing 0x80 with the
relevant SET command.

Example:
0x88 (or 0x89 or 0x8A)  ; request mouse mode
Returns:
        0xF6        ; status response header
        mode        ; 0x08 is RELATIVE
                    ; 0x09 is ABSOLUTE
                    ; 0x0A is KEYCODE
        param1      ; 0 is RELATIVE
                    ; XMSB maximum if ABSOLUTE
                    ; DELTA X is KEYCODE
        param2      ; 0 is RELATIVE
                    ; YMSB maximum if ABSOLUTE
                    ; DELTA Y is KEYCODE
        param3      ; 0 if RELATIVE
                    ; or KEYCODE
                    ; YMSB is ABSOLUTE
        param4      ; 0 if RELATIVE
                    ; or KEYCODE
                    ; YLSB is ABSOLUTE
        0           ; pad
        0
```

The STATUS INQUIRY commands request the ikbd to return either the current mode or the parameters associated with a given command. All status reports are padded to form 8 byte long return packets. The responses to the status requests are designed so that the host may store them away (after stripping off the status report header byte) and later send them back as commands to ikbd to restore its state. The 0 pad bytes will be treated as NOPs by the ikbd.

> Valid STATUS INQUIRY commands are:
>
>
>
> ```text
> 0x87    mouse button action
> 0x88    mouse mode
> 0x89
> 0x8A
> 0x8B    mnouse threshold
> 0x8C    mouse scale
> 0x8F    mouse vertical coordinates
> 0x90    ( returns       0x0F Y=0 at bottom
>                 0x10 Y=0 at top )
> 0x92    mouse enable/disable
>         ( returns       0x00 enabled)
>                 0x12 disabled )
> 0x94    joystick mode
> 0x95
> 0x96
> 0x9A    joystick enable/disable
>         ( returns       0x00 enabled
>                 0x1A disabled )
> ```

It is the (host) programmer's responsibility to have only one unanswered inquiry in process at a time. STATUS INQUIRY commands are not valid if the ikbd is in JOYSTICK MONITORING mode or FIRE BUTTON MONITORING mode.

<a id="rst-scan-codes"></a>

## SCAN CODES

The key scan codes returned by the ikbd are chosen to simplify the implementation of GSX.

GSX Standard Keyboard Mapping


<table>
<thead>
<tr>
<th>


Hex

</th>
<th>


Keytop

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


01

</td>
<td>


Esc

</td>
</tr>
<tr>
<td>


02

</td>
<td>


1

</td>
</tr>
<tr>
<td>


03

</td>
<td>


2

</td>
</tr>
<tr>
<td>


04

</td>
<td>


3

</td>
</tr>
<tr>
<td>


05

</td>
<td>


4

</td>
</tr>
<tr>
<td>


06

</td>
<td>


5

</td>
</tr>
<tr>
<td>


07

</td>
<td>


6

</td>
</tr>
<tr>
<td>


08

</td>
<td>


7

</td>
</tr>
<tr>
<td>


09

</td>
<td>


8

</td>
</tr>
<tr>
<td>


0A

</td>
<td>


9

</td>
</tr>
<tr>
<td>


0B

</td>
<td>


0

</td>
</tr>
<tr>
<td>


0C

</td>
<td>


-

</td>
</tr>
<tr>
<td>


0D

</td>
<td>


=

</td>
</tr>
<tr>
<td>


0E

</td>
<td>


BS

</td>
</tr>
<tr>
<td>


0F

</td>
<td>


TAB

</td>
</tr>
<tr>
<td>


10

</td>
<td>


Q

</td>
</tr>
<tr>
<td>


11

</td>
<td>


W

</td>
</tr>
<tr>
<td>


12

</td>
<td>


E

</td>
</tr>
<tr>
<td>


13

</td>
<td>


R

</td>
</tr>
<tr>
<td>


14

</td>
<td>


T

</td>
</tr>
<tr>
<td>


15

</td>
<td>


Y

</td>
</tr>
<tr>
<td>


16

</td>
<td>


U

</td>
</tr>
<tr>
<td>


17

</td>
<td>


I

</td>
</tr>
<tr>
<td>


18

</td>
<td>


O

</td>
</tr>
<tr>
<td>


19

</td>
<td>


P

</td>
</tr>
<tr>
<td>


1A

</td>
<td>


\[

</td>
</tr>
<tr>
<td>


1B

</td>
<td>


\]

</td>
</tr>
<tr>
<td>


1C

</td>
<td>


RET

</td>
</tr>
<tr>
<td>


1D

</td>
<td>


CTRL

</td>
</tr>
<tr>
<td>


1E

</td>
<td>


A

</td>
</tr>
<tr>
<td>


1F

</td>
<td>


S

</td>
</tr>
<tr>
<td>


20

</td>
<td>


D

</td>
</tr>
<tr>
<td>


21

</td>
<td>


F

</td>
</tr>
<tr>
<td>


22

</td>
<td>


G

</td>
</tr>
<tr>
<td>


23

</td>
<td>


H

</td>
</tr>
<tr>
<td>


24

</td>
<td>


J

</td>
</tr>
<tr>
<td>


25

</td>
<td>


K

</td>
</tr>
<tr>
<td>


26

</td>
<td>


L

</td>
</tr>
<tr>
<td>


27

</td>
<td>


;

</td>
</tr>
<tr>
<td>


28

</td>
<td>


'

</td>
</tr>
<tr>
<td>


29

</td>
<td>


\`

</td>
</tr>
<tr>
<td>


2A

</td>
<td>


(LEFT) SHIFT

</td>
</tr>
<tr>
<td>


2B

</td>
<td>


\\

</td>
</tr>
<tr>
<td>


2C

</td>
<td>


Z

</td>
</tr>
<tr>
<td>


2D

</td>
<td>


X

</td>
</tr>
<tr>
<td>


2E

</td>
<td>


C

</td>
</tr>
<tr>
<td>


2F

</td>
<td>


V

</td>
</tr>
<tr>
<td>


30

</td>
<td>


B

</td>
</tr>
<tr>
<td>


31

</td>
<td>


N

</td>
</tr>
<tr>
<td>


32

</td>
<td>


M

</td>
</tr>
<tr>
<td>


33

</td>
<td>


,

</td>
</tr>
<tr>
<td>


34

</td>
<td>


.

</td>
</tr>
<tr>
<td>


35

</td>
<td>


/

</td>
</tr>
<tr>
<td>


36

</td>
<td>


(RIGHT) SHIFT

</td>
</tr>
<tr>
<td>


37

</td>
<td>


\{ NOT USED \}

</td>
</tr>
<tr>
<td>


38

</td>
<td>


ALT

</td>
</tr>
<tr>
<td>


39

</td>
<td>


SPACE BAR

</td>
</tr>
<tr>
<td>


3A

</td>
<td>


CAPS LOCK

</td>
</tr>
<tr>
<td>


3B

</td>
<td>


F1

</td>
</tr>
<tr>
<td>


3C

</td>
<td>


F2

</td>
</tr>
<tr>
<td>


3D

</td>
<td>


F3

</td>
</tr>
<tr>
<td>


3E

</td>
<td>


F4

</td>
</tr>
<tr>
<td>


3F

</td>
<td>


F5

</td>
</tr>
<tr>
<td>


40

</td>
<td>


F6

</td>
</tr>
<tr>
<td>


41

</td>
<td>


F7

</td>
</tr>
<tr>
<td>


42

</td>
<td>


F8

</td>
</tr>
<tr>
<td>


43

</td>
<td>


F9

</td>
</tr>
<tr>
<td>


44

</td>
<td>


F10

</td>
</tr>
<tr>
<td>


45

</td>
<td>


\{ NOT USED \}

</td>
</tr>
<tr>
<td>


46

</td>
<td>


\{ NOT USED \}

</td>
</tr>
<tr>
<td>


47

</td>
<td>


HOME

</td>
</tr>
<tr>
<td>


48

</td>
<td>


UP ARROW

</td>
</tr>
<tr>
<td>


49

</td>
<td>


\{ NOT USED \}

</td>
</tr>
<tr>
<td>


4A

</td>
<td>


KEYPAD -

</td>
</tr>
<tr>
<td>


4B

</td>
<td>


LEFT ARROW

</td>
</tr>
<tr>
<td>


4C

</td>
<td>


\{ NOT USED \}

</td>
</tr>
<tr>
<td>


4D

</td>
<td>


RIGHT ARROW

</td>
</tr>
<tr>
<td>


4E

</td>
<td>


KEYPAD +

</td>
</tr>
<tr>
<td>


4F

</td>
<td>


\{ NOT USED \}

</td>
</tr>
<tr>
<td>


50

</td>
<td>


DOWN ARROW

</td>
</tr>
<tr>
<td>


51

</td>
<td>


\{ NOT USED \}

</td>
</tr>
<tr>
<td>


52

</td>
<td>


INSERT

</td>
</tr>
<tr>
<td>


53

</td>
<td>


DEL

</td>
</tr>
<tr>
<td>


54

</td>
<td>


\{ NOT USED \}

</td>
</tr>
<tr>
<td>


5F

</td>
<td>


\{ NOT USED \}

</td>
</tr>
<tr>
<td>


60

</td>
<td>


ISO KEY

</td>
</tr>
<tr>
<td>


61

</td>
<td>


UNDO

</td>
</tr>
<tr>
<td>


62

</td>
<td>


HELP

</td>
</tr>
<tr>
<td>


63

</td>
<td>


KEYPAD (

</td>
</tr>
<tr>
<td>


64

</td>
<td>


KEYPAD /

</td>
</tr>
<tr>
<td>


65

</td>
<td>


KEYPAD \*

</td>
</tr>
<tr>
<td>


66

</td>
<td>


KEYPAD \*

</td>
</tr>
<tr>
<td>


67

</td>
<td>


KEYPAD 7

</td>
</tr>
<tr>
<td>


68

</td>
<td>


KEYPAD 8

</td>
</tr>
<tr>
<td>


69

</td>
<td>


KEYPAD 9

</td>
</tr>
<tr>
<td>


6A

</td>
<td>


KEYPAD 4

</td>
</tr>
<tr>
<td>


6B

</td>
<td>


KEYPAD 5

</td>
</tr>
<tr>
<td>


6C

</td>
<td>


KEYPAD 6

</td>
</tr>
<tr>
<td>


6D

</td>
<td>


KEYPAD 1

</td>
</tr>
<tr>
<td>


6E

</td>
<td>


KEYPAD 2

</td>
</tr>
<tr>
<td>


6F

</td>
<td>


KEYPAD 3

</td>
</tr>
<tr>
<td>


70

</td>
<td>


KEYPAD 0

</td>
</tr>
<tr>
<td>


71

</td>
<td>


KEYPAD .

</td>
</tr>
<tr>
<td>


72

</td>
<td>


KEYPAD ENTER

</td>
</tr>
</tbody>
</table>
