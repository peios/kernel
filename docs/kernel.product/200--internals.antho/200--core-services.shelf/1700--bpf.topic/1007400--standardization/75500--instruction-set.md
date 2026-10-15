---
title: "Contents"
type: reference
description: "1 BPF Instruction Set Architecture (ISA)"
---

<a id="rst-contents"></a>



<a id="rst-bpf-instruction-set-architecture-isa"></a>

## 1   BPF Instruction Set Architecture (ISA)

eBPF, also commonly referred to as BPF, is a technology with origins in the Linux kernel that can run untrusted programs in a privileged context such as an operating system kernel. This document specifies the BPF instruction set architecture (ISA).

As a historical note, BPF originally stood for Berkeley Packet Filter, but now that it can do so much more than packet filtering, the acronym no longer makes sense. BPF is now considered a standalone term that does not stand for anything.  The original BPF is sometimes referred to as cBPF (classic BPF) to distinguish it from the now widely deployed eBPF (extended BPF).

<a id="rst-documentation-conventions"></a>

### 1.1   Documentation conventions

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in BCP 14 [https://www.rfc-editor.org/info/rfc2119](<https://www.rfc-editor.org/info/rfc2119>)<a id="rst-https-www-rfc-editor-org-info-rfc2119"></a> [https://www.rfc-editor.org/info/rfc8174](<https://www.rfc-editor.org/info/rfc8174>)<a id="rst-https-www-rfc-editor-org-info-rfc8174"></a> when, and only when, they appear in all capitals, as shown here.

For brevity and consistency, this document refers to families of types using a shorthand syntax and refers to several expository, mnemonic functions when describing the semantics of instructions. The range of valid values for those types and the semantics of those functions are defined in the following subsections.

<a id="rst-types"></a>

#### 1.1.1   Types

This document refers to integer types with the notation `SN` to specify a type's signedness (`S`) and bit width (`N`), respectively.


<table>
<caption>

Meaning of signedness notation

</caption>
<thead>
<tr>
<th>



S

</th>
<th>



Meaning

</th>
</tr>
</thead>
<tbody>
<tr>
<td>



u

</td>
<td>



unsigned

</td>
</tr>
<tr>
<td>



s

</td>
<td>



signed

</td>
</tr>
</tbody>
</table>


<table>
<caption>

Meaning of bit-width notation

</caption>
<thead>
<tr>
<th>



N

</th>
<th>



Bit width

</th>
</tr>
</thead>
<tbody>
<tr>
<td>



8

</td>
<td>



8 bits

</td>
</tr>
<tr>
<td>



16

</td>
<td>



16 bits

</td>
</tr>
<tr>
<td>



32

</td>
<td>



32 bits

</td>
</tr>
<tr>
<td>



64

</td>
<td>



64 bits

</td>
</tr>
<tr>
<td>



128

</td>
<td>



128 bits

</td>
</tr>
</tbody>
</table>

For example, `u32` is a type whose valid values are all the 32-bit unsigned numbers and `s16` is a type whose valid values are all the 16-bit signed numbers.

<a id="rst-functions"></a>

#### 1.1.2   Functions

The following byteswap functions are direction-agnostic.  That is, the same function is used for conversion in either direction discussed below.

- be16: Takes an unsigned 16-bit number and converts it between host byte order and big-endian ([IEN137](<https://www.rfc-editor.org/ien/ien137.txt>)<a id="rst-ien137"></a>) byte order.

- be32: Takes an unsigned 32-bit number and converts it between host byte order and big-endian byte order.

- be64: Takes an unsigned 64-bit number and converts it between host byte order and big-endian byte order.

- bswap16: Takes an unsigned 16-bit number in either big- or little-endian format and returns the equivalent number with the same bit width but opposite endianness.

- bswap32: Takes an unsigned 32-bit number in either big- or little-endian format and returns the equivalent number with the same bit width but opposite endianness.

- bswap64: Takes an unsigned 64-bit number in either big- or little-endian format and returns the equivalent number with the same bit width but opposite endianness.

- le16: Takes an unsigned 16-bit number and converts it between host byte order and little-endian byte order.

- le32: Takes an unsigned 32-bit number and converts it between host byte order and little-endian byte order.

- le64: Takes an unsigned 64-bit number and converts it between host byte order and little-endian byte order.

<a id="rst-definitions"></a>

#### 1.1.3   Definitions



- **<a id="rst-term-sign-extend"></a>Sign Extend**

  To `sign extend an` `X` `-bit number, A, to a` `Y` `-bit number, B  ,` means to

  1. Copy all `X` bits from `A` to the lower `X` bits of `B`.

  2. Set the value of the remaining `Y` - `X` bits of `B` to the value of the  most-significant bit of `A`.

> [!NOTE]
>
> **Example**
>
> Sign extend an 8-bit number `A` to a 16-bit number `B` on a big-endian platform:
>
>
>
> ```text
> A:          10000110
> B: 11111111 10000110
> ```

<a id="rst-conformance-groups"></a>

#### 1.1.4   Conformance groups

An implementation does not need to support all instructions specified in this document (e.g., deprecated instructions).  Instead, a number of conformance groups are specified.  An implementation MUST support the base32 conformance group and MAY support additional conformance groups, where supporting a conformance group means it MUST support all instructions in that conformance group.

The use of named conformance groups enables interoperability between a runtime that executes instructions, and tools such as compilers that generate instructions for the runtime.  Thus, capability discovery in terms of conformance groups might be done manually by users or automatically by tools.

Each conformance group has a short ASCII label (e.g., "base32") that corresponds to a set of instructions that are mandatory.  That is, each instruction has one or more conformance groups of which it is a member.

This document defines the following conformance groups:

- base32: includes all instructions defined in this specification unless otherwise noted.

- base64: includes base32, plus instructions explicitly noted as being in the base64 conformance group.

- atomic32: includes 32-bit atomic operation instructions (see [Atomic operations](<#rst-atomic-operations>)).

- atomic64: includes atomic32, plus 64-bit atomic operation instructions.

- divmul32: includes 32-bit division, multiplication, and modulo instructions.

- divmul64: includes divmul32, plus 64-bit division, multiplication, and modulo instructions.

- packet: deprecated packet access instructions.

<a id="rst-instruction-encoding"></a>

### 1.2   Instruction encoding

BPF has two instruction encodings:

- the basic instruction encoding, which uses 64 bits to encode an instruction

- the wide instruction encoding, which appends a second 64 bits after the basic instruction for a total of 128 bits.

<a id="rst-basic-instruction-encoding"></a>

#### 1.2.1   Basic instruction encoding

A basic instruction is encoded as follows:



```text
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|    opcode     |     regs      |            offset             |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                              imm                              |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

- **<strong>opcode</strong>**

  operation to perform, encoded as follows:



  ```text
  +-+-+-+-+-+-+-+-+
  |specific |class|
  +-+-+-+-+-+-+-+-+
  ```

  - **<strong>specific</strong>**

    The format of these bits varies by instruction class

  - **<strong>class</strong>**

    The instruction class (see [Instruction classes](<#rst-instruction-classes>))

- **<strong>regs</strong>**

  The source and destination register numbers, encoded as follows on a little-endian host:



  ```text
  +-+-+-+-+-+-+-+-+
  |src_reg|dst_reg|
  +-+-+-+-+-+-+-+-+
  ```

  and as follows on a big-endian host:



  ```text
  +-+-+-+-+-+-+-+-+
  |dst_reg|src_reg|
  +-+-+-+-+-+-+-+-+
  ```

  - **<strong>src\_reg</strong>**

    the source register number (0-10), except where otherwise specified ([64-bit immediate instructions](<#rst-bit-immediate-instructions>) reuse this field for other purposes)

  - **<strong>dst\_reg</strong>**

    destination register number (0-10), unless otherwise specified (future instructions might reuse this field for other purposes)

- **<strong>offset</strong>**

  signed integer offset used with pointer arithmetic, except where otherwise specified (some arithmetic instructions reuse this field for other purposes)

- **<strong>imm</strong>**

  signed integer immediate value

Note that the contents of multi-byte fields ('offset' and 'imm') are stored using big-endian byte ordering on big-endian hosts and little-endian byte ordering on little-endian hosts.

For example:



```text
opcode                  offset imm          assembly
       src_reg dst_reg
07     0       1        00 00  44 33 22 11  r1 += 0x11223344 // little
       dst_reg src_reg
07     1       0        00 00  11 22 33 44  r1 += 0x11223344 // big
```

Note that most instructions do not use all of the fields. Unused fields SHALL be cleared to zero.

<a id="rst-wide-instruction-encoding"></a>

#### 1.2.2   Wide instruction encoding

Some instructions are defined to use the wide instruction encoding, which uses two 32-bit immediate values.  The 64 bits following the basic instruction format contain a pseudo instruction with 'opcode', 'dst\_reg', 'src\_reg', and 'offset' all set to zero.

This is depicted in the following figure:



```text
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|    opcode     |     regs      |            offset             |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                              imm                              |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                           reserved                            |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                           next_imm                            |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

- **<strong>opcode</strong>**

  operation to perform, encoded as explained above

- **<strong>regs</strong>**

  The source and destination register numbers (unless otherwise specified), encoded as explained above

- **<strong>offset</strong>**

  signed integer offset used with pointer arithmetic, unless otherwise specified

- **<strong>imm</strong>**

  signed integer immediate value

- **<strong>reserved</strong>**

  unused, set to zero

- **<strong>next\_imm</strong>**

  second signed integer immediate value

<a id="rst-instruction-classes"></a>

#### 1.2.3   Instruction classes

The three least significant bits of the 'opcode' field store the instruction class:


<table>
<caption>

Instruction class

</caption>
<thead>
<tr>
<th>



class

</th>
<th>



value

</th>
<th>



description

</th>
<th>



reference

</th>
</tr>
</thead>
<tbody>
<tr>
<td>



LD

</td>
<td>



0x0

</td>
<td>



non-standard load operations

</td>
<td>



[Load and store instructions](<#rst-load-and-store-instructions>)

</td>
</tr>
<tr>
<td>



LDX

</td>
<td>



0x1

</td>
<td>



load into register operations

</td>
<td>



[Load and store instructions](<#rst-load-and-store-instructions>)

</td>
</tr>
<tr>
<td>



ST

</td>
<td>



0x2

</td>
<td>



store from immediate operations

</td>
<td>



[Load and store instructions](<#rst-load-and-store-instructions>)

</td>
</tr>
<tr>
<td>



STX

</td>
<td>



0x3

</td>
<td>



store from register operations

</td>
<td>



[Load and store instructions](<#rst-load-and-store-instructions>)

</td>
</tr>
<tr>
<td>



ALU

</td>
<td>



0x4

</td>
<td>



32-bit arithmetic operations

</td>
<td>



[Arithmetic and jump instructions](<#rst-arithmetic-and-jump-instructions>)

</td>
</tr>
<tr>
<td>



JMP

</td>
<td>



0x5

</td>
<td>



64-bit jump operations

</td>
<td>



[Arithmetic and jump instructions](<#rst-arithmetic-and-jump-instructions>)

</td>
</tr>
<tr>
<td>



JMP32

</td>
<td>



0x6

</td>
<td>



32-bit jump operations

</td>
<td>



[Arithmetic and jump instructions](<#rst-arithmetic-and-jump-instructions>)

</td>
</tr>
<tr>
<td>



ALU64

</td>
<td>



0x7

</td>
<td>



64-bit arithmetic operations

</td>
<td>



[Arithmetic and jump instructions](<#rst-arithmetic-and-jump-instructions>)

</td>
</tr>
</tbody>
</table>

<a id="rst-arithmetic-and-jump-instructions"></a>

### 1.3   Arithmetic and jump instructions

For arithmetic and jump instructions (`ALU`, `ALU64`, `JMP` and `JMP32`), the 8-bit 'opcode' field is divided into three parts:



```text
+-+-+-+-+-+-+-+-+
|  code |s|class|
+-+-+-+-+-+-+-+-+
```

- **<strong>code</strong>**

  the operation code, whose meaning varies by instruction class

- **<strong>s (source)</strong>**

  the source operand location, which unless otherwise specified is one of:


  <table>
  <caption>

  Source operand location

  </caption>
  <thead>
  <tr>
  <th>



  source

  </th>
  <th>



  value

  </th>
  <th>



  description

  </th>
  </tr>
  </thead>
  <tbody>
  <tr>
  <td>



  K

  </td>
  <td>



  0

  </td>
  <td>



  use 32-bit 'imm' value as source operand

  </td>
  </tr>
  <tr>
  <td>



  X

  </td>
  <td>



  1

  </td>
  <td>



  use 'src\_reg' register value as source operand

  </td>
  </tr>
  </tbody>
  </table>

- **<strong>instruction class</strong>**

  the instruction class (see [Instruction classes](<#rst-instruction-classes>))

<a id="rst-arithmetic-instructions"></a>

#### 1.3.1   Arithmetic instructions

`ALU` uses 32-bit wide operands while `ALU64` uses 64-bit wide operands for otherwise identical operations. `ALU64` instructions belong to the base64 conformance group unless noted otherwise. The 'code' field encodes the operation as below, where 'src' refers to the the source operand and 'dst' refers to the value of the destination register.


<table>
<caption>

Arithmetic instructions

</caption>
<thead>
<tr>
<th>



name

</th>
<th>



code

</th>
<th>



offset

</th>
<th>



description

</th>
</tr>
</thead>
<tbody>
<tr>
<td>



ADD

</td>
<td>



0x0

</td>
<td>



0

</td>
<td>



dst += src

</td>
</tr>
<tr>
<td>



SUB

</td>
<td>



0x1

</td>
<td>



0

</td>
<td>



dst -= src

</td>
</tr>
<tr>
<td>



MUL

</td>
<td>



0x2

</td>
<td>



0

</td>
<td>



dst \*= src

</td>
</tr>
<tr>
<td>



DIV

</td>
<td>



0x3

</td>
<td>



0

</td>
<td>



dst = (src \!= 0) ? (dst / src) : 0

</td>
</tr>
<tr>
<td>



SDIV

</td>
<td>



0x3

</td>
<td>



1

</td>
<td>



dst = (src == 0) ? 0 : ((src == -1 &amp;&amp; dst == LLONG\_MIN) ? LLONG\_MIN : (dst s/ src))

</td>
</tr>
<tr>
<td>



OR

</td>
<td>



0x4

</td>
<td>



0

</td>
<td>



dst \|= src

</td>
</tr>
<tr>
<td>



AND

</td>
<td>



0x5

</td>
<td>



0

</td>
<td>



dst &amp;= src

</td>
</tr>
<tr>
<td>



LSH

</td>
<td>



0x6

</td>
<td>



0

</td>
<td>



dst &lt;&lt;= (src &amp; mask)

</td>
</tr>
<tr>
<td>



RSH

</td>
<td>



0x7

</td>
<td>



0

</td>
<td>



dst &gt;&gt;= (src &amp; mask)

</td>
</tr>
<tr>
<td>



NEG

</td>
<td>



0x8

</td>
<td>



0

</td>
<td>



dst = -dst

</td>
</tr>
<tr>
<td>



MOD

</td>
<td>



0x9

</td>
<td>



0

</td>
<td>



dst = (src \!= 0) ? (dst % src) : dst

</td>
</tr>
<tr>
<td>



SMOD

</td>
<td>



0x9

</td>
<td>



1

</td>
<td>



dst = (src == 0) ? dst : ((src == -1 &amp;&amp; dst == LLONG\_MIN) ? 0: (dst s% src))

</td>
</tr>
<tr>
<td>



XOR

</td>
<td>



0xa

</td>
<td>



0

</td>
<td>



dst ^= src

</td>
</tr>
<tr>
<td>



MOV

</td>
<td>



0xb

</td>
<td>



0

</td>
<td>



dst = src

</td>
</tr>
<tr>
<td>



MOVSX

</td>
<td>



0xb

</td>
<td>



8/16/32

</td>
<td>



dst = (s8,s16,s32)src

</td>
</tr>
<tr>
<td>



ARSH

</td>
<td>



0xc

</td>
<td>



0

</td>
<td>



[sign extending](<#rst-term-sign-extend>) dst &gt;&gt;= (src &amp; mask)

</td>
</tr>
<tr>
<td>



END

</td>
<td>



0xd

</td>
<td>



0

</td>
<td>



byte swap operations (see [Byte swap instructions](<#rst-byte-swap-instructions>) below)

</td>
</tr>
</tbody>
</table>

Underflow and overflow are allowed during arithmetic operations, meaning the 64-bit or 32-bit value will wrap. If BPF program execution would result in division by zero, the destination register is instead set to zero. Otherwise, for `ALU64`, if execution would result in `LLONG_MIN` divided by -1, the destination register is instead set to `LLONG_MIN`. For `ALU`, if execution would result in `INT_MIN` divided by -1, the destination register is instead set to `INT_MIN`.

If execution would result in modulo by zero, for `ALU64` the value of the destination register is unchanged whereas for `ALU` the upper 32 bits of the destination register are zeroed. Otherwise, for `ALU64`, if execution would resuslt in `LLONG_MIN` modulo -1, the destination register is instead set to 0. For `ALU`, if execution would result in `INT_MIN` modulo -1, the destination register is instead set to 0.

`{ADD, X, ALU}`, where 'code' = `ADD`, 'source' = `X`, and 'class' = `ALU`, means:



```text
dst = (u32) ((u32) dst + (u32) src)
```

where '(u32)' indicates that the upper 32 bits are zeroed.

`{ADD, X, ALU64}` means:



```text
dst = dst + src
```

`{XOR, K, ALU}` means:



```text
dst = (u32) dst ^ (u32) imm
```

`{XOR, K, ALU64}` means:



```text
dst = dst ^ imm
```

Note that most arithmetic instructions have 'offset' set to 0. Only three instructions (`SDIV`, `SMOD`, `MOVSX`) have a non-zero 'offset'.

Division, multiplication, and modulo operations for `ALU` are part of the "divmul32" conformance group, and division, multiplication, and modulo operations for `ALU64` are part of the "divmul64" conformance group. The division and modulo operations support both unsigned and signed flavors.

For unsigned operations (`DIV` and `MOD`), for `ALU`, 'imm' is interpreted as a 32-bit unsigned value. For `ALU64`, 'imm' is first [sign extended](<#rst-term-sign-extend>) from 32 to 64 bits, and then interpreted as a 64-bit unsigned value.

For signed operations (`SDIV` and `SMOD`), for `ALU`, 'imm' is interpreted as a 32-bit signed value. For `ALU64`, 'imm' is first [sign extended](<#rst-term-sign-extend>) from 32 to 64 bits, and then interpreted as a 64-bit signed value.

Note that there are varying definitions of the signed modulo operation when the dividend or divisor are negative, where implementations often vary by language such that Python, Ruby, etc.  differ from C, Go, Java, etc. This specification requires that signed modulo MUST use truncated division (where -13 % 3 == -1) as implemented in C, Go, etc.:



```text
a % n = a - n * trunc(a / n)
```

The `MOVSX` instruction does a move operation with sign extension. `{MOVSX, X, ALU}` [sign extends](<#rst-term-sign-extend>) 8-bit and 16-bit operands into 32-bit operands, and zeroes the remaining upper 32 bits. `{MOVSX, X, ALU64}` [sign extends](<#rst-term-sign-extend>) 8-bit, 16-bit, and 32-bit operands into 64-bit operands.  Unlike other arithmetic instructions, `MOVSX` is only defined for register source operands (`X`).

`{MOV, K, ALU64}` means:



```text
dst = (s64)imm
```

`{MOV, X, ALU}` means:



```text
dst = (u32)src
```

`{MOVSX, X, ALU}` with 'offset' 8 means:



```text
dst = (u32)(s32)(s8)src
```

The `NEG` instruction is only defined when the source bit is clear (`K`).

Shift operations use a mask of 0x3F (63) for 64-bit operations and 0x1F (31) for 32-bit operations.

<a id="rst-byte-swap-instructions"></a>

#### 1.3.2   Byte swap instructions

The byte swap instructions use instruction classes of `ALU` and `ALU64` and a 4-bit 'code' field of `END`.

The byte swap instructions operate on the destination register only and do not use a separate source register or immediate value.

For `ALU`, the 1-bit source operand field in the opcode is used to select what byte order the operation converts from or to. For `ALU64`, the 1-bit source operand field in the opcode is reserved and MUST be set to 0.


<table>
<caption>

Byte swap instructions

</caption>
<thead>
<tr>
<th>



class

</th>
<th>



source

</th>
<th>



value

</th>
<th>



description

</th>
</tr>
</thead>
<tbody>
<tr>
<td>



ALU

</td>
<td>



LE

</td>
<td>



0

</td>
<td>



convert between host byte order and little endian

</td>
</tr>
<tr>
<td>



ALU

</td>
<td>



BE

</td>
<td>



1

</td>
<td>



convert between host byte order and big endian

</td>
</tr>
<tr>
<td>



ALU64

</td>
<td>



Reserved

</td>
<td>



0

</td>
<td>



do byte swap unconditionally

</td>
</tr>
</tbody>
</table>

The 'imm' field encodes the width of the swap operations.  The following widths are supported: 16, 32 and 64.  Width 64 operations belong to the base64 conformance group and other swap operations belong to the base32 conformance group.

Examples:

`{END, LE, ALU}` with 'imm' = 16/32/64 means:



```text
dst = le16(dst)
dst = le32(dst)
dst = le64(dst)
```

`{END, BE, ALU}` with 'imm' = 16/32/64 means:



```text
dst = be16(dst)
dst = be32(dst)
dst = be64(dst)
```

`{END, TO, ALU64}` with 'imm' = 16/32/64 means:



```text
dst = bswap16(dst)
dst = bswap32(dst)
dst = bswap64(dst)
```

<a id="rst-jump-instructions"></a>

#### 1.3.3   Jump instructions

`JMP32` uses 32-bit wide operands and indicates the base32 conformance group, while `JMP` uses 64-bit wide operands for otherwise identical operations, and indicates the base64 conformance group unless otherwise specified. The 'code' field encodes the operation as below:


<table>
<caption>

Jump instructions

</caption>
<thead>
<tr>
<th>



code

</th>
<th>



value

</th>
<th>



src\_reg

</th>
<th>



description

</th>
<th>



notes

</th>
</tr>
</thead>
<tbody>
<tr>
<td>



JA

</td>
<td>



0x0

</td>
<td>



0x0

</td>
<td>



PC += offset

</td>
<td>



\{JA, K, JMP\} only

</td>
</tr>
<tr>
<td>



JA

</td>
<td>



0x0

</td>
<td>



0x0

</td>
<td>



PC += imm

</td>
<td>



\{JA, K, JMP32\} only

</td>
</tr>
<tr>
<td>



JEQ

</td>
<td>



0x1

</td>
<td>



any

</td>
<td>



PC += offset if dst == src

</td>
<td>





</td>
</tr>
<tr>
<td>



JGT

</td>
<td>



0x2

</td>
<td>



any

</td>
<td>



PC += offset if dst &gt; src

</td>
<td>



unsigned

</td>
</tr>
<tr>
<td>



JGE

</td>
<td>



0x3

</td>
<td>



any

</td>
<td>



PC += offset if dst &gt;= src

</td>
<td>



unsigned

</td>
</tr>
<tr>
<td>



JSET

</td>
<td>



0x4

</td>
<td>



any

</td>
<td>



PC += offset if dst &amp; src

</td>
<td>





</td>
</tr>
<tr>
<td>



JNE

</td>
<td>



0x5

</td>
<td>



any

</td>
<td>



PC += offset if dst \!= src

</td>
<td>





</td>
</tr>
<tr>
<td>



JSGT

</td>
<td>



0x6

</td>
<td>



any

</td>
<td>



PC += offset if dst &gt; src

</td>
<td>



signed

</td>
</tr>
<tr>
<td>



JSGE

</td>
<td>



0x7

</td>
<td>



any

</td>
<td>



PC += offset if dst &gt;= src

</td>
<td>



signed

</td>
</tr>
<tr>
<td>



CALL

</td>
<td>



0x8

</td>
<td>



0x0

</td>
<td>



call helper function by static ID

</td>
<td>



\{CALL, K, JMP\} only, see [Helper functions](<#rst-helper-functions>)

</td>
</tr>
<tr>
<td>



CALL

</td>
<td>



0x8

</td>
<td>



0x1

</td>
<td>



call PC += imm

</td>
<td>



\{CALL, K, JMP\} only, see [Program-local functions](<#rst-program-local-functions>)

</td>
</tr>
<tr>
<td>



CALL

</td>
<td>



0x8

</td>
<td>



0x2

</td>
<td>



call helper function by BTF ID

</td>
<td>



\{CALL, K, JMP\} only, see [Helper functions](<#rst-helper-functions>)

</td>
</tr>
<tr>
<td>



EXIT

</td>
<td>



0x9

</td>
<td>



0x0

</td>
<td>



return

</td>
<td>



\{CALL, K, JMP\} only

</td>
</tr>
<tr>
<td>



JLT

</td>
<td>



0xa

</td>
<td>



any

</td>
<td>



PC += offset if dst &lt; src

</td>
<td>



unsigned

</td>
</tr>
<tr>
<td>



JLE

</td>
<td>



0xb

</td>
<td>



any

</td>
<td>



PC += offset if dst &lt;= src

</td>
<td>



unsigned

</td>
</tr>
<tr>
<td>



JSLT

</td>
<td>



0xc

</td>
<td>



any

</td>
<td>



PC += offset if dst &lt; src

</td>
<td>



signed

</td>
</tr>
<tr>
<td>



JSLE

</td>
<td>



0xd

</td>
<td>



any

</td>
<td>



PC += offset if dst &lt;= src

</td>
<td>



signed

</td>
</tr>
</tbody>
</table>

where 'PC' denotes the program counter, and the offset to increment by is in units of 64-bit instructions relative to the instruction following the jump instruction.  Thus 'PC += 1' skips execution of the next instruction if it's a basic instruction or results in undefined behavior if the next instruction is a 128-bit wide instruction.

Example:

`{JSGE, X, JMP32}` means:



```text
if (s32)dst s>= (s32)src goto +offset
```

where 's&gt;=' indicates a signed '&gt;=' comparison.

`{JLE, K, JMP}` means:



```text
if dst <= (u64)(s64)imm goto +offset
```

`{JA, K, JMP32}` means:



```text
gotol +imm
```

where 'imm' means the branch offset comes from the 'imm' field.

Note that there are two flavors of `JA` instructions. The `JMP` class permits a 16-bit jump offset specified by the 'offset' field, whereas the `JMP32` class permits a 32-bit jump offset specified by the 'imm' field. A &gt; 16-bit conditional jump may be converted to a &lt; 16-bit conditional jump plus a 32-bit unconditional jump.

All `CALL` and `JA` instructions belong to the base32 conformance group.

<a id="rst-helper-functions"></a>

##### 1.3.3.1   Helper functions

Helper functions are a concept whereby BPF programs can call into a set of function calls exposed by the underlying platform.

Historically, each helper function was identified by a static ID encoded in the 'imm' field.  Further documentation of helper functions is outside the scope of this document and standardization is left for future work, but use is widely deployed and more information can be found in platform-specific documentation (e.g., Linux kernel documentation).

Platforms that support the BPF Type Format (BTF) support identifying a helper function by a BTF ID encoded in the 'imm' field, where the BTF ID identifies the helper name and type.  Further documentation of BTF is outside the scope of this document and standardization is left for future work, but use is widely deployed and more information can be found in platform-specific documentation (e.g., Linux kernel documentation).

<a id="rst-program-local-functions"></a>

##### 1.3.3.2   Program-local functions

Program-local functions are functions exposed by the same BPF program as the caller, and are referenced by offset from the instruction following the call instruction, similar to `JA`.  The offset is encoded in the 'imm' field of the call instruction. An `EXIT` within the program-local function will return to the caller.

<a id="rst-load-and-store-instructions"></a>

### 1.4   Load and store instructions

For load and store instructions (`LD`, `LDX`, `ST`, and `STX`), the 8-bit 'opcode' field is divided as follows:



```text
+-+-+-+-+-+-+-+-+
|mode |sz |class|
+-+-+-+-+-+-+-+-+
```

- **<strong>mode</strong>**

  The mode modifier is one of:


  <table>
  <caption>

  Mode modifier

  </caption>
  <thead>
  <tr>
  <th>



  mode modifier

  </th>
  <th>



  value

  </th>
  <th>



  description

  </th>
  <th>



  reference

  </th>
  </tr>
  </thead>
  <tbody>
  <tr>
  <td>



  IMM

  </td>
  <td>



  0

  </td>
  <td>



  64-bit immediate instructions

  </td>
  <td>



  [64-bit immediate instructions](<#rst-bit-immediate-instructions>)

  </td>
  </tr>
  <tr>
  <td>



  ABS

  </td>
  <td>



  1

  </td>
  <td>



  legacy BPF packet access (absolute)

  </td>
  <td>



  [Legacy BPF Packet access instructions](<#rst-legacy-bpf-packet-access-instructions>)

  </td>
  </tr>
  <tr>
  <td>



  IND

  </td>
  <td>



  2

  </td>
  <td>



  legacy BPF packet access (indirect)

  </td>
  <td>



  [Legacy BPF Packet access instructions](<#rst-legacy-bpf-packet-access-instructions>)

  </td>
  </tr>
  <tr>
  <td>



  MEM

  </td>
  <td>



  3

  </td>
  <td>



  regular load and store operations

  </td>
  <td>



  [Regular load and store operations](<#rst-regular-load-and-store-operations>)

  </td>
  </tr>
  <tr>
  <td>



  MEMSX

  </td>
  <td>



  4

  </td>
  <td>



  sign-extension load operations

  </td>
  <td>



  [Sign-extension load operations](<#rst-sign-extension-load-operations>)

  </td>
  </tr>
  <tr>
  <td>



  ATOMIC

  </td>
  <td>



  6

  </td>
  <td>



  atomic operations

  </td>
  <td>



  [Atomic operations](<#rst-atomic-operations>)

  </td>
  </tr>
  </tbody>
  </table>

- **<strong>sz (size)</strong>**

  The size modifier is one of:


  <table>
  <caption>

  Size modifier

  </caption>
  <thead>
  <tr>
  <th>



  size

  </th>
  <th>



  value

  </th>
  <th>



  description

  </th>
  </tr>
  </thead>
  <tbody>
  <tr>
  <td>



  W

  </td>
  <td>



  0

  </td>
  <td>



  word        (4 bytes)

  </td>
  </tr>
  <tr>
  <td>



  H

  </td>
  <td>



  1

  </td>
  <td>



  half word   (2 bytes)

  </td>
  </tr>
  <tr>
  <td>



  B

  </td>
  <td>



  2

  </td>
  <td>



  byte

  </td>
  </tr>
  <tr>
  <td>



  DW

  </td>
  <td>



  3

  </td>
  <td>



  double word (8 bytes)

  </td>
  </tr>
  </tbody>
  </table>

  Instructions using `DW` belong to the base64 conformance group.

- **<strong>class</strong>**

  The instruction class (see [Instruction classes](<#rst-instruction-classes>))

<a id="rst-regular-load-and-store-operations"></a>

#### 1.4.1   Regular load and store operations

The `MEM` mode modifier is used to encode regular load and store instructions that transfer data between a register and memory.

`{MEM, <size>, STX}` means:



```text
*(size *) (dst + offset) = src
```

`{MEM, <size>, ST}` means:



```text
*(size *) (dst + offset) = imm
```

`{MEM, <size>, LDX}` means:



```text
dst = *(unsigned size *) (src + offset)
```

Where '&lt;size&gt;' is one of: `B`, `H`, `W`, or `DW`, and 'unsigned size' is one of: u8, u16, u32, or u64.

<a id="rst-sign-extension-load-operations"></a>

#### 1.4.2   Sign-extension load operations

The `MEMSX` mode modifier is used to encode [sign-extension](<#rst-term-sign-extend>) load instructions that transfer data between a register and memory.

`{MEMSX, <size>, LDX}` means:



```text
dst = *(signed size *) (src + offset)
```

Where '&lt;size&gt;' is one of: `B`, `H`, or `W`, and 'signed size' is one of: s8, s16, or s32.

<a id="rst-atomic-operations"></a>

#### 1.4.3   Atomic operations

Atomic operations are operations that operate on memory and can not be interrupted or corrupted by other access to the same memory region by other BPF programs or means outside of this specification.

All atomic operations supported by BPF are encoded as store operations that use the `ATOMIC` mode modifier as follows:

- `{ATOMIC, W, STX}` for 32-bit operations, which are part of the "atomic32" conformance group.

- `{ATOMIC, DW, STX}` for 64-bit operations, which are part of the "atomic64" conformance group.

- 8-bit and 16-bit wide atomic operations are not supported.

The 'imm' field is used to encode the actual atomic operation. Simple atomic operation use a subset of the values defined to encode arithmetic operations in the 'imm' field to encode the atomic operation:


<table>
<caption>

Simple atomic operations

</caption>
<thead>
<tr>
<th>



imm

</th>
<th>



value

</th>
<th>



description

</th>
</tr>
</thead>
<tbody>
<tr>
<td>



ADD

</td>
<td>



0x00

</td>
<td>



atomic add

</td>
</tr>
<tr>
<td>



OR

</td>
<td>



0x40

</td>
<td>



atomic or

</td>
</tr>
<tr>
<td>



AND

</td>
<td>



0x50

</td>
<td>



atomic and

</td>
</tr>
<tr>
<td>



XOR

</td>
<td>



0xa0

</td>
<td>



atomic xor

</td>
</tr>
</tbody>
</table>

`{ATOMIC, W, STX}` with 'imm' = ADD means:



```text
*(u32 *)(dst + offset) += src
```

`{ATOMIC, DW, STX}` with 'imm' = ADD means:



```text
*(u64 *)(dst + offset) += src
```

In addition to the simple atomic operations, there also is a modifier and two complex atomic operations:


<table>
<caption>

Complex atomic operations

</caption>
<thead>
<tr>
<th>



imm

</th>
<th>



value

</th>
<th>



description

</th>
</tr>
</thead>
<tbody>
<tr>
<td>



FETCH

</td>
<td>



0x01

</td>
<td>



modifier: return old value

</td>
</tr>
<tr>
<td>



XCHG

</td>
<td>



0xe0 \| FETCH

</td>
<td>



atomic exchange

</td>
</tr>
<tr>
<td>



CMPXCHG

</td>
<td>



0xf0 \| FETCH

</td>
<td>



atomic compare and exchange

</td>
</tr>
</tbody>
</table>

The `FETCH` modifier is optional for simple atomic operations, and always set for the complex atomic operations.  If the `FETCH` flag is set, then the operation also overwrites `src` with the value that was in memory before it was modified.

The `XCHG` operation atomically exchanges `src` with the value addressed by `dst + offset`.

The `CMPXCHG` operation atomically compares the value addressed by `dst + offset` with `R0`. If they match, the value addressed by `dst + offset` is replaced with `src`. In either case, the value that was at `dst + offset` before the operation is zero-extended and loaded back to `R0`.

<a id="rst-bit-immediate-instructions"></a>

#### 1.4.4   64-bit immediate instructions

Instructions with the `IMM` 'mode' modifier use the wide instruction encoding defined in [Instruction encoding](<#rst-instruction-encoding>), and use the 'src\_reg' field of the basic instruction to hold an opcode subtype.

The following table defines a set of `{IMM, DW, LD}` instructions with opcode subtypes in the 'src\_reg' field, using new terms such as "map" defined further below:


<table>
<caption>

64-bit immediate instructions

</caption>
<thead>
<tr>
<th>



src\_reg

</th>
<th>



pseudocode

</th>
<th>



imm type

</th>
<th>



dst type

</th>
</tr>
</thead>
<tbody>
<tr>
<td>



0x0

</td>
<td>



dst = (next\_imm &lt;&lt; 32) \| imm

</td>
<td>



integer

</td>
<td>



integer

</td>
</tr>
<tr>
<td>



0x1

</td>
<td>



dst = map\_by\_fd(imm)

</td>
<td>



map fd

</td>
<td>



map

</td>
</tr>
<tr>
<td>



0x2

</td>
<td>



dst = map\_val(map\_by\_fd(imm)) + next\_imm

</td>
<td>



map fd

</td>
<td>



data address

</td>
</tr>
<tr>
<td>



0x3

</td>
<td>



dst = var\_addr(imm)

</td>
<td>



variable id

</td>
<td>



data address

</td>
</tr>
<tr>
<td>



0x4

</td>
<td>



dst = code\_addr(imm)

</td>
<td>



integer

</td>
<td>



code address

</td>
</tr>
<tr>
<td>



0x5

</td>
<td>



dst = map\_by\_idx(imm)

</td>
<td>



map index

</td>
<td>



map

</td>
</tr>
<tr>
<td>



0x6

</td>
<td>



dst = map\_val(map\_by\_idx(imm)) + next\_imm

</td>
<td>



map index

</td>
<td>



data address

</td>
</tr>
</tbody>
</table>

where

- map\_by\_fd(imm) means to convert a 32-bit file descriptor into an address of a map (see [Maps](<#rst-maps>))

- map\_by\_idx(imm) means to convert a 32-bit index into an address of a map

- map\_val(map) gets the address of the first value in a given map

- var\_addr(imm) gets the address of a platform variable (see [Platform Variables](<#rst-platform-variables>)) with a given id

- code\_addr(imm) gets the address of the instruction at a specified relative offset in number of (64-bit) instructions

- the 'imm type' can be used by disassemblers for display

- the 'dst type' can be used for verification and JIT compilation purposes

<a id="rst-maps"></a>

##### 1.4.4.1   Maps

Maps are shared memory regions accessible by BPF programs on some platforms. A map can have various semantics as defined in a separate document, and may or may not have a single contiguous memory region, but the 'map\_val(map)' is currently only defined for maps that do have a single contiguous memory region.

Each map can have a file descriptor (fd) if supported by the platform, where 'map\_by\_fd(imm)' means to get the map with the specified file descriptor. Each BPF program can also be defined to use a set of maps associated with the program at load time, and 'map\_by\_idx(imm)' means to get the map with the given index in the set associated with the BPF program containing the instruction.

<a id="rst-platform-variables"></a>

##### 1.4.4.2   Platform Variables

Platform variables are memory regions, identified by integer ids, exposed by the runtime and accessible by BPF programs on some platforms.  The 'var\_addr(imm)' operation means to get the address of the memory region identified by the given id.

<a id="rst-legacy-bpf-packet-access-instructions"></a>

#### 1.4.5   Legacy BPF Packet access instructions

BPF previously introduced special instructions for access to packet data that were carried over from classic BPF. These instructions used an instruction class of `LD`, a size modifier of `W`, `H`, or `B`, and a mode modifier of `ABS` or `IND`.  The 'dst\_reg' and 'offset' fields were set to zero, and 'src\_reg' was set to zero for `ABS`.  However, these instructions are deprecated and SHOULD no longer be used.  All legacy packet access instructions belong to the "packet" conformance group.
