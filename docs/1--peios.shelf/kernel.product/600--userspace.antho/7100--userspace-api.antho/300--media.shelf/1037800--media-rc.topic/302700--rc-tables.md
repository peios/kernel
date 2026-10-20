---
title: "Remote controller tables"
type: reference
description: "Unfortunately, for several years, there was no effort to create uniform IR keycodes for different devices. This caused the same IR keyname to be mapped completely differently on different IR devices. This resulted that the same IR keyname…"
---

<a id="rst-remote-controller-tables"></a>
<a id="rst-remote-controllers-tables"></a>

<!-- SPDX-License-Identifier: GPL-2.0 OR GFDL-1.1-no-invariants-or-later -->

Unfortunately, for several years, there was no effort to create uniform IR keycodes for different devices. This caused the same IR keyname to be mapped completely differently on different IR devices. This resulted that the same IR keyname to be mapped completely different on different IR's. Due to that, V4L2 API now specifies a standard for mapping Media keys on IR.

This standard should be used by both V4L/DVB drivers and userspace applications

The modules register the remote as keyboard within the linux input layer. This means that the IR key strokes will look like normal keyboard key strokes (if CONFIG\_INPUT\_KEYBOARD is enabled). Using the event devices (CONFIG\_INPUT\_EVDEV) it is possible for applications to access the remote via /dev/input/event devices.

<a id="rst-rc-standard-keymap"></a>



<!-- tabularcolumns: |p{4.4cm}|p{4.4cm}|p{8.5cm}| -->


<table>
<caption>

IR default keymapping

</caption>
<tbody>
<tr>
<td>



Key code

</td>
<td>



Meaning

</td>
<td>



Key examples on IR

</td>
</tr>
<tr>
<td colspan="3">



<strong>Numeric keys</strong>

</td>
</tr>
<tr>
<td>



`KEY_NUMERIC_0`

</td>
<td>



Keyboard digit 0

</td>
<td>



0

</td>
</tr>
<tr>
<td>



`KEY_NUMERIC_1`

</td>
<td>



Keyboard digit 1

</td>
<td>



1

</td>
</tr>
<tr>
<td>



`KEY_NUMERIC_2`

</td>
<td>



Keyboard digit 2

</td>
<td>



2

</td>
</tr>
<tr>
<td>



`KEY_NUMERIC_3`

</td>
<td>



Keyboard digit 3

</td>
<td>



3

</td>
</tr>
<tr>
<td>



`KEY_NUMERIC_4`

</td>
<td>



Keyboard digit 4

</td>
<td>



4

</td>
</tr>
<tr>
<td>



`KEY_NUMERIC_5`

</td>
<td>



Keyboard digit 5

</td>
<td>



5

</td>
</tr>
<tr>
<td>



`KEY_NUMERIC_6`

</td>
<td>



Keyboard digit 6

</td>
<td>



6

</td>
</tr>
<tr>
<td>



`KEY_NUMERIC_7`

</td>
<td>



Keyboard digit 7

</td>
<td>



7

</td>
</tr>
<tr>
<td>



`KEY_NUMERIC_8`

</td>
<td>



Keyboard digit 8

</td>
<td>



8

</td>
</tr>
<tr>
<td>



`KEY_NUMERIC_9`

</td>
<td>



Keyboard digit 9

</td>
<td>



9

</td>
</tr>
<tr>
<td colspan="3">



<strong>Movie play control</strong>

</td>
</tr>
<tr>
<td>



`KEY_FORWARD`

</td>
<td>



Instantly advance in time

</td>
<td>



&gt;&gt; / FORWARD

</td>
</tr>
<tr>
<td>



`KEY_BACK`

</td>
<td>



Instantly go back in time

</td>
<td>



&lt;&lt;&lt; / BACK

</td>
</tr>
<tr>
<td>



`KEY_FASTFORWARD`

</td>
<td>



Play movie faster

</td>
<td>



```pycon
>>> / FORWARD
```

</td>
</tr>
<tr>
<td>



`KEY_REWIND`

</td>
<td>



Play movie back

</td>
<td>



REWIND / BACKWARD

</td>
</tr>
<tr>
<td>



`KEY_NEXT`

</td>
<td>



Select next chapter / sub-chapter / interval

</td>
<td>



NEXT / SKIP

</td>
</tr>
<tr>
<td>



`KEY_PREVIOUS`

</td>
<td>



Select previous chapter / sub-chapter / interval

</td>
<td>



&lt;&lt; / PREV / PREVIOUS

</td>
</tr>
<tr>
<td>



`KEY_AGAIN`

</td>
<td>



Repeat the video or a video interval

</td>
<td>



REPEAT / LOOP / RECALL

</td>
</tr>
<tr>
<td>



`KEY_PAUSE`

</td>
<td>



Pause stream

</td>
<td>



PAUSE / FREEZE

</td>
</tr>
<tr>
<td>



`KEY_PLAY`

</td>
<td>



Play movie at the normal timeshift

</td>
<td>



NORMAL TIMESHIFT / LIVE / &gt;

</td>
</tr>
<tr>
<td>



`KEY_PLAYPAUSE`

</td>
<td>



Alternate between play and pause

</td>
<td>



PLAY / PAUSE

</td>
</tr>
<tr>
<td>



`KEY_STOP`

</td>
<td>



Stop stream

</td>
<td>



STOP

</td>
</tr>
<tr>
<td>



`KEY_RECORD`

</td>
<td>



Start/stop recording stream

</td>
<td>



CAPTURE / REC / RECORD/PAUSE

</td>
</tr>
<tr>
<td>



`KEY_CAMERA`

</td>
<td>



Take a picture of the image

</td>
<td>



CAMERA ICON / CAPTURE / SNAPSHOT

</td>
</tr>
<tr>
<td>



`KEY_SHUFFLE`

</td>
<td>



Enable shuffle mode

</td>
<td>



SHUFFLE

</td>
</tr>
<tr>
<td>



`KEY_TIME`

</td>
<td>



Activate time shift mode

</td>
<td>



TIME SHIFT

</td>
</tr>
<tr>
<td>



`KEY_TITLE`

</td>
<td>



Allow changing the chapter

</td>
<td>



CHAPTER

</td>
</tr>
<tr>
<td>



`KEY_SUBTITLE`

</td>
<td>



Allow changing the subtitle

</td>
<td>



SUBTITLE

</td>
</tr>
<tr>
<td colspan="3">



<strong>Image control</strong>

</td>
</tr>
<tr>
<td>



`KEY_BRIGHTNESSDOWN`

</td>
<td>



Decrease Brightness

</td>
<td>



BRIGHTNESS DECREASE

</td>
</tr>
<tr>
<td>



`KEY_BRIGHTNESSUP`

</td>
<td>



Increase Brightness

</td>
<td>



BRIGHTNESS INCREASE

</td>
</tr>
<tr>
<td>



`KEY_ANGLE`

</td>
<td>



Switch video camera angle (on videos with more than one angle stored)

</td>
<td>



ANGLE / SWAP

</td>
</tr>
<tr>
<td>



`KEY_EPG`

</td>
<td>



Open the Elecrowonic Play Guide (EPG)

</td>
<td>



EPG / GUIDE

</td>
</tr>
<tr>
<td>



`KEY_TEXT`

</td>
<td>



Activate/change closed caption mode

</td>
<td>



CLOSED CAPTION/TELETEXT / DVD TEXT / TELETEXT / TTX

</td>
</tr>
<tr>
<td colspan="3">



<strong>Audio control</strong>

</td>
</tr>
<tr>
<td>



`KEY_AUDIO`

</td>
<td>



Change audio source

</td>
<td>



AUDIO SOURCE / AUDIO / MUSIC

</td>
</tr>
<tr>
<td>



`KEY_MUTE`

</td>
<td>



Mute/unmute audio

</td>
<td>



MUTE / DEMUTE / UNMUTE

</td>
</tr>
<tr>
<td>



`KEY_VOLUMEDOWN`

</td>
<td>



Decrease volume

</td>
<td>



VOLUME- / VOLUME DOWN

</td>
</tr>
<tr>
<td>



`KEY_VOLUMEUP`

</td>
<td>



Increase volume

</td>
<td>



VOLUME+ / VOLUME UP

</td>
</tr>
<tr>
<td>



`KEY_MODE`

</td>
<td>



Change sound mode

</td>
<td>



MONO/STEREO

</td>
</tr>
<tr>
<td>



`KEY_LANGUAGE`

</td>
<td>



Select Language

</td>
<td>



1ST / 2ND LANGUAGE / DVD LANG / MTS/SAP / MTS SEL

</td>
</tr>
<tr>
<td colspan="3">



<strong>Channel control</strong>

</td>
</tr>
<tr>
<td>



`KEY_CHANNEL`

</td>
<td>



Go to the next favorite channel

</td>
<td>



ALT / CHANNEL / CH SURFING / SURF / FAV

</td>
</tr>
<tr>
<td>



`KEY_CHANNELDOWN`

</td>
<td>



Decrease channel sequentially

</td>
<td>



CHANNEL - / CHANNEL DOWN / DOWN

</td>
</tr>
<tr>
<td>



`KEY_CHANNELUP`

</td>
<td>



Increase channel sequentially

</td>
<td>



CHANNEL + / CHANNEL UP / UP

</td>
</tr>
<tr>
<td>



`KEY_DIGITS`

</td>
<td>



Use more than one digit for channel

</td>
<td>



PLUS / 100/ 1xx / xxx / -/-- / Single Double Triple Digit

</td>
</tr>
<tr>
<td>



`KEY_SEARCH`

</td>
<td>



Start channel autoscan

</td>
<td>



SCAN / AUTOSCAN

</td>
</tr>
<tr>
<td colspan="3">



<strong>Colored keys</strong>

</td>
</tr>
<tr>
<td>



`KEY_BLUE`

</td>
<td>



IR Blue key

</td>
<td>



BLUE

</td>
</tr>
<tr>
<td>



`KEY_GREEN`

</td>
<td>



IR Green Key

</td>
<td>



GREEN

</td>
</tr>
<tr>
<td>



`KEY_RED`

</td>
<td>



IR Red key

</td>
<td>



RED

</td>
</tr>
<tr>
<td>



`KEY_YELLOW`

</td>
<td>



IR Yellow key

</td>
<td>



YELLOW

</td>
</tr>
<tr>
<td colspan="3">



<strong>Media selection</strong>

</td>
</tr>
<tr>
<td>



`KEY_CD`

</td>
<td>



Change input source to Compact Disc

</td>
<td>



CD

</td>
</tr>
<tr>
<td>



`KEY_DVD`

</td>
<td>



Change input to DVD

</td>
<td>



DVD / DVD MENU

</td>
</tr>
<tr>
<td>



`KEY_EJECTCLOSECD`

</td>
<td>



Open/close the CD/DVD player

</td>
<td>



-&gt; ) / CLOSE / OPEN

</td>
</tr>
<tr>
<td>



`KEY_MEDIA`

</td>
<td>



Turn on/off Media application

</td>
<td>



PC/TV / TURN ON/OFF APP

</td>
</tr>
<tr>
<td>



`KEY_PC`

</td>
<td>



Selects from TV to PC

</td>
<td>



PC

</td>
</tr>
<tr>
<td>



`KEY_RADIO`

</td>
<td>



Put into AM/FM radio mode

</td>
<td>



RADIO / TV/FM / TV/RADIO / FM / FM/RADIO

</td>
</tr>
<tr>
<td>



`KEY_TV`

</td>
<td>



Select tv mode

</td>
<td>



TV / LIVE TV

</td>
</tr>
<tr>
<td>



`KEY_TV2`

</td>
<td>



Select Cable mode

</td>
<td>



AIR/CBL

</td>
</tr>
<tr>
<td>



`KEY_VCR`

</td>
<td>



Select VCR mode

</td>
<td>



VCR MODE / DTR

</td>
</tr>
<tr>
<td>



`KEY_VIDEO`

</td>
<td>



Alternate between input modes

</td>
<td>



SOURCE / SELECT / DISPLAY / SWITCH INPUTS / VIDEO

</td>
</tr>
<tr>
<td colspan="3">



<strong>Power control</strong>

</td>
</tr>
<tr>
<td>



`KEY_POWER`

</td>
<td>



Turn on/off computer

</td>
<td>



SYSTEM POWER / COMPUTER POWER

</td>
</tr>
<tr>
<td>



`KEY_POWER2`

</td>
<td>



Turn on/off application

</td>
<td>



TV ON/OFF / POWER

</td>
</tr>
<tr>
<td>



`KEY_SLEEP`

</td>
<td>



Activate sleep timer

</td>
<td>



SLEEP / SLEEP TIMER

</td>
</tr>
<tr>
<td>



`KEY_SUSPEND`

</td>
<td>



Put computer into suspend mode

</td>
<td>



STANDBY / SUSPEND

</td>
</tr>
<tr>
<td colspan="3">



<strong>Window control</strong>

</td>
</tr>
<tr>
<td>



`KEY_CLEAR`

</td>
<td>



Stop stream and return to default input video/audio

</td>
<td>



CLEAR / RESET / BOSS KEY

</td>
</tr>
<tr>
<td>



`KEY_CYCLEWINDOWS`

</td>
<td>



Minimize windows and move to the next one

</td>
<td>



ALT-TAB / MINIMIZE / DESKTOP

</td>
</tr>
<tr>
<td>



`KEY_FAVORITES`

</td>
<td>



Open the favorites stream window

</td>
<td>



TV WALL / Favorites

</td>
</tr>
<tr>
<td>



`KEY_MENU`

</td>
<td>



Call application menu

</td>
<td>



2ND CONTROLS (USA: MENU) / DVD/MENU / SHOW/HIDE CTRL

</td>
</tr>
<tr>
<td>



`KEY_NEW`

</td>
<td>



Open/Close Picture in Picture

</td>
<td>



PIP

</td>
</tr>
<tr>
<td>



`KEY_OK`

</td>
<td>



Send a confirmation code to application

</td>
<td>



OK / ENTER / RETURN

</td>
</tr>
<tr>
<td>



`KEY_ASPECT_RATIO`

</td>
<td>



Select screen aspect ratio

</td>
<td>



4:3 16:9 SELECT

</td>
</tr>
<tr>
<td>



`KEY_FULL_SCREEN`

</td>
<td>



Put device into zoom/full screen mode

</td>
<td>



ZOOM / FULL SCREEN / ZOOM+ / HIDE PANEL / SWITCH

</td>
</tr>
<tr>
<td colspan="3">



<strong>Navigation keys</strong>

</td>
</tr>
<tr>
<td>



`KEY_ESC`

</td>
<td>



Cancel current operation

</td>
<td>



CANCEL / BACK

</td>
</tr>
<tr>
<td>



`KEY_HELP`

</td>
<td>



Open a Help window

</td>
<td>



HELP

</td>
</tr>
<tr>
<td>



`KEY_HOMEPAGE`

</td>
<td>



Navigate to Homepage

</td>
<td>



HOME

</td>
</tr>
<tr>
<td>



`KEY_INFO`

</td>
<td>



Open On Screen Display

</td>
<td>



DISPLAY INFORMATION / OSD

</td>
</tr>
<tr>
<td>



`KEY_WWW`

</td>
<td>



Open the default browser

</td>
<td>



WEB

</td>
</tr>
<tr>
<td>



`KEY_UP`

</td>
<td>



Up key

</td>
<td>



UP

</td>
</tr>
<tr>
<td>



`KEY_DOWN`

</td>
<td>



Down key

</td>
<td>



DOWN

</td>
</tr>
<tr>
<td>



`KEY_LEFT`

</td>
<td>



Left key

</td>
<td>



LEFT

</td>
</tr>
<tr>
<td>



`KEY_RIGHT`

</td>
<td>



Right key

</td>
<td>



RIGHT

</td>
</tr>
<tr>
<td colspan="3">



<strong>Miscellaneous keys</strong>

</td>
</tr>
<tr>
<td>



`KEY_DOT`

</td>
<td>



Return a dot

</td>
<td>



.

</td>
</tr>
<tr>
<td>



`KEY_FN`

</td>
<td>



Select a function

</td>
<td>



FUNCTION

</td>
</tr>
</tbody>
</table>

It should be noted that, sometimes, there some fundamental missing keys at some cheaper IR's. Due to that, it is recommended to:

<a id="rst-rc-keymap-notes"></a>


<table>
<caption>

Notes

</caption>
<tbody>
<tr>
<td>



On simpler IR's, without separate channel keys, you need to map UP as `KEY_CHANNELUP`

</td>
</tr>
<tr>
<td>



On simpler IR's, without separate channel keys, you need to map DOWN as `KEY_CHANNELDOWN`

</td>
</tr>
<tr>
<td>



On simpler IR's, without separate volume keys, you need to map LEFT as `KEY_VOLUMEDOWN`

</td>
</tr>
<tr>
<td>



On simpler IR's, without separate volume keys, you need to map RIGHT as `KEY_VOLUMEUP`

</td>
</tr>
</tbody>
</table>
