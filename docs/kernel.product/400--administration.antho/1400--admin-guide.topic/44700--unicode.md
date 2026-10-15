---
title: "Unicode support"
type: reference
description: "Last update: 2005-01-17, version 1.4"
---

<a id="rst-unicode-support"></a>

> Last update: 2005-01-17, version 1.4

Note: The original version of this document, which was maintained at lanana.org as part of the Linux Assigned Names And Numbers Authority (LANANA) project, is no longer existent.  So, this version in the mainline Linux kernel is now the maintained main document.

<a id="rst-introduction"></a>

## Introduction

The Linux kernel code has been rewritten to use Unicode to map characters to fonts.  By downloading a single Unicode-to-font table, both the eight-bit character sets and UTF-8 mode are changed to use the font as indicated.

This changes the semantics of the eight-bit character tables subtly. The four character tables are now:


<table>
<thead>
<tr>
<th>


Map symbol

</th>
<th>


Map name

</th>
<th>


Escape code (G0)

</th>
</tr>
</thead>
<tbody>
<tr>
<td>


LAT1_MAP

</td>
<td>


Latin-1 (ISO 8859-1)

</td>
<td>


ESC ( B

</td>
</tr>
<tr>
<td>


GRAF_MAP

</td>
<td>


DEC VT100 pseudographics

</td>
<td>


ESC ( 0

</td>
</tr>
<tr>
<td>


IBMPC_MAP

</td>
<td>


IBM code page 437

</td>
<td>


ESC ( U

</td>
</tr>
<tr>
<td>


USER_MAP

</td>
<td>


User defined

</td>
<td>


ESC ( K

</td>
</tr>
</tbody>
</table>

In particular, ESC ( U is no longer "straight to font", since the font might be completely different than the IBM character set.  This permits for example the use of block graphics even with a Latin-1 font loaded.

Note that although these codes are similar to ISO 2022, neither the codes nor their uses match ISO 2022; Linux has two 8-bit codes (G0 and G1), whereas ISO 2022 has four 7-bit codes (G0-G3).

In accordance with the Unicode standard/ISO 10646 the range U+F000 to U+F8FF has been reserved for OS-wide allocation (the Unicode Standard refers to this as a "Corporate Zone", since this is inaccurate for Linux we call it the "Linux Zone").  U+F000 was picked as the starting point since it lets the direct-mapping area start on a large power of two (in case 1024- or 2048-character fonts ever become necessary). This leaves U+E000 to U+EFFF as End User Zone.

\[v1.2\]: The Unicodes range from U+F000 and up to U+F7FF have been hard-coded to map directly to the loaded font, bypassing the translation table.  The user-defined map now defaults to U+F000 to U+F0FF, emulating the previous behaviour.  In practice, this range might be shorter; for example, vgacon can only handle 256-character (U+F000..U+F0FF) or 512-character (U+F000..U+F1FF) fonts.

<a id="rst-actual-characters-assigned-in-the-linux-zone"></a>

## Actual characters assigned in the Linux Zone

In addition, the following characters not present in Unicode 1.1.4 have been defined; these are used by the DEC VT graphics map.  \[v1.2\] THIS USE IS OBSOLETE AND SHOULD NO LONGER BE USED; PLEASE SEE BELOW.


<table>
<tbody>
<tr>
<td>


U+F800

</td>
<td>


DEC VT GRAPHICS HORIZONTAL LINE SCAN 1

</td>
</tr>
<tr>
<td>


U+F801

</td>
<td>


DEC VT GRAPHICS HORIZONTAL LINE SCAN 3

</td>
</tr>
<tr>
<td>


U+F803

</td>
<td>


DEC VT GRAPHICS HORIZONTAL LINE SCAN 7

</td>
</tr>
<tr>
<td>


U+F804

</td>
<td>


DEC VT GRAPHICS HORIZONTAL LINE SCAN 9

</td>
</tr>
</tbody>
</table>

The DEC VT220 uses a 6x10 character matrix, and these characters form a smooth progression in the DEC VT graphics character set.  I have omitted the scan 5 line, since it is also used as a block-graphics character, and hence has been coded as U+2500 FORMS LIGHT HORIZONTAL.

\[v1.3\]: These characters have been officially added to Unicode 3.2.0; they are added at U+23BA, U+23BB, U+23BC, U+23BD.  Linux now uses the new values.

\[v1.2\]: The following characters have been added to represent common keyboard symbols that are unlikely to ever be added to Unicode proper since they are horribly vendor-specific.  This, of course, is an excellent example of horrible design.


<table>
<tbody>
<tr>
<td>


U+F810

</td>
<td>


KEYBOARD SYMBOL FLYING FLAG

</td>
</tr>
<tr>
<td>


U+F811

</td>
<td>


KEYBOARD SYMBOL PULLDOWN MENU

</td>
</tr>
<tr>
<td>


U+F812

</td>
<td>


KEYBOARD SYMBOL OPEN APPLE

</td>
</tr>
<tr>
<td>


U+F813

</td>
<td>


KEYBOARD SYMBOL SOLID APPLE

</td>
</tr>
</tbody>
</table>

<a id="rst-klingon-language-support"></a>

## Klingon language support

In 1996, Linux was the first operating system in the world to add support for the artificial language Klingon, created by Marc Okrand for the "Star Trek" television series.  This encoding was later adopted by the ConScript Unicode Registry and proposed (but ultimately rejected) for inclusion in Unicode Plane 1.  Thus, it remains as a Linux/CSUR private assignment in the Linux Zone.

This encoding has been endorsed by the Klingon Language Institute. For more information, contact them at:

> [http://www.kli.org/](<http://www.kli.org/>)

Since the characters in the beginning of the Linux CZ have been more of the dingbats/symbols/forms type and this is a language, I have located it at the end, on a 16-cell boundary in keeping with standard Unicode practice.

> [!NOTE]
>
> This range is now officially managed by the ConScript Unicode Registry.  The normative reference is at:
>
> > [https://www.evertype.com/standards/csur/klingon.html](<https://www.evertype.com/standards/csur/klingon.html>)

Klingon has an alphabet of 26 characters, a positional numeric writing system with 10 digits, and is written left-to-right, top-to-bottom.

Several glyph forms for the Klingon alphabet have been proposed. However, since the set of symbols appear to be consistent throughout, with only the actual shapes being different, in keeping with standard Unicode practice these differences are considered font variants.


<table>
<tbody>
<tr>
<td>


U+F8D0

</td>
<td>


KLINGON LETTER A

</td>
</tr>
<tr>
<td>


U+F8D1

</td>
<td>


KLINGON LETTER B

</td>
</tr>
<tr>
<td>


U+F8D2

</td>
<td>


KLINGON LETTER CH

</td>
</tr>
<tr>
<td>


U+F8D3

</td>
<td>


KLINGON LETTER D

</td>
</tr>
<tr>
<td>


U+F8D4

</td>
<td>


KLINGON LETTER E

</td>
</tr>
<tr>
<td>


U+F8D5

</td>
<td>


KLINGON LETTER GH

</td>
</tr>
<tr>
<td>


U+F8D6

</td>
<td>


KLINGON LETTER H

</td>
</tr>
<tr>
<td>


U+F8D7

</td>
<td>


KLINGON LETTER I

</td>
</tr>
<tr>
<td>


U+F8D8

</td>
<td>


KLINGON LETTER J

</td>
</tr>
<tr>
<td>


U+F8D9

</td>
<td>


KLINGON LETTER L

</td>
</tr>
<tr>
<td>


U+F8DA

</td>
<td>


KLINGON LETTER M

</td>
</tr>
<tr>
<td>


U+F8DB

</td>
<td>


KLINGON LETTER N

</td>
</tr>
<tr>
<td>


U+F8DC

</td>
<td>


KLINGON LETTER NG

</td>
</tr>
<tr>
<td>


U+F8DD

</td>
<td>


KLINGON LETTER O

</td>
</tr>
<tr>
<td>


U+F8DE

</td>
<td>


KLINGON LETTER P

</td>
</tr>
<tr>
<td>


U+F8DF

</td>
<td>


KLINGON LETTER Q - Written &lt;q&gt; in standard Okrand Latin transliteration

</td>
</tr>
<tr>
<td>


U+F8E0

</td>
<td>


KLINGON LETTER QH - Written &lt;Q&gt; in standard Okrand Latin transliteration

</td>
</tr>
<tr>
<td>


U+F8E1

</td>
<td>


KLINGON LETTER R

</td>
</tr>
<tr>
<td>


U+F8E2

</td>
<td>


KLINGON LETTER S

</td>
</tr>
<tr>
<td>


U+F8E3

</td>
<td>


KLINGON LETTER T

</td>
</tr>
<tr>
<td>


U+F8E4

</td>
<td>


KLINGON LETTER TLH

</td>
</tr>
<tr>
<td>


U+F8E5

</td>
<td>


KLINGON LETTER U

</td>
</tr>
<tr>
<td>


U+F8E6

</td>
<td>


KLINGON LETTER V

</td>
</tr>
<tr>
<td>


U+F8E7

</td>
<td>


KLINGON LETTER W

</td>
</tr>
<tr>
<td>


U+F8E8

</td>
<td>


KLINGON LETTER Y

</td>
</tr>
<tr>
<td>


U+F8E9

</td>
<td>


KLINGON LETTER GLOTTAL STOP

</td>
</tr>
<tr>
<td>


U+F8F0

</td>
<td>


KLINGON DIGIT ZERO

</td>
</tr>
<tr>
<td>


U+F8F1

</td>
<td>


KLINGON DIGIT ONE

</td>
</tr>
<tr>
<td>


U+F8F2

</td>
<td>


KLINGON DIGIT TWO

</td>
</tr>
<tr>
<td>


U+F8F3

</td>
<td>


KLINGON DIGIT THREE

</td>
</tr>
<tr>
<td>


U+F8F4

</td>
<td>


KLINGON DIGIT FOUR

</td>
</tr>
<tr>
<td>


U+F8F5

</td>
<td>


KLINGON DIGIT FIVE

</td>
</tr>
<tr>
<td>


U+F8F6

</td>
<td>


KLINGON DIGIT SIX

</td>
</tr>
<tr>
<td>


U+F8F7

</td>
<td>


KLINGON DIGIT SEVEN

</td>
</tr>
<tr>
<td>


U+F8F8

</td>
<td>


KLINGON DIGIT EIGHT

</td>
</tr>
<tr>
<td>


U+F8F9

</td>
<td>


KLINGON DIGIT NINE

</td>
</tr>
<tr>
<td>


U+F8FD

</td>
<td>


KLINGON COMMA

</td>
</tr>
<tr>
<td>


U+F8FE

</td>
<td>


KLINGON FULL STOP

</td>
</tr>
<tr>
<td>


U+F8FF

</td>
<td>


KLINGON SYMBOL FOR EMPIRE

</td>
</tr>
</tbody>
</table>

<a id="rst-other-fictional-and-artificial-scripts"></a>

## Other Fictional and Artificial Scripts

Since the assignment of the Klingon Linux Unicode block, a registry of fictional and artificial scripts has been established by John Cowan &lt;[jcowan@reutershealth.com](<mailto:jcowan@reutershealth.com>)&gt; and Michael Everson &lt;[everson@evertype.com](<mailto:everson@evertype.com>)&gt;. The ConScript Unicode Registry is accessible at:

> [https://www.evertype.com/standards/csur/](<https://www.evertype.com/standards/csur/>)

The ranges used fall at the low end of the End User Zone and can hence not be normatively assigned, but it is recommended that people who wish to encode fictional scripts use these codes, in the interest of interoperability.  For Klingon, CSUR has adopted the Linux encoding. The CSUR people are driving adding Tengwar and Cirth into Unicode Plane 1; the addition of Klingon to Unicode Plane 1 has been rejected and so the above encoding remains official.
