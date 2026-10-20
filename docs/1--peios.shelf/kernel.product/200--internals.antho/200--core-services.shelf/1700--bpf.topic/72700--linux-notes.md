---
title: "Contents"
type: reference
description: "1 Linux implementation notes"
---

<a id="rst-contents"></a>



<a id="rst-linux-implementation-notes"></a>

## 1   Linux implementation notes

This document provides more details specific to the Linux kernel implementation of the eBPF instruction set.

<a id="rst-byte-swap-instructions"></a>

### 1.1   Byte swap instructions

`BPF_FROM_LE` and `BPF_FROM_BE` exist as aliases for `BPF_TO_LE` and `BPF_TO_BE` respectively.

<a id="rst-jump-instructions"></a>

### 1.2   Jump instructions

`BPF_CALL | BPF_X | BPF_JMP` (0x8d), where the helper function integer would be read from a specified register, is not currently supported by the verifier.  Any programs with this instruction will fail to load until such support is added.

<a id="rst-maps"></a>

### 1.3   Maps

Linux only supports the 'map\_val(map)' operation on array maps with a single element.

Linux uses an fd\_array to store maps associated with a BPF program. Thus, map\_by\_idx(imm) uses the fd at that index in the array.

<a id="rst-variables"></a>

### 1.4   Variables

The following 64-bit immediate instruction specifies that a variable address, which corresponds to some integer stored in the 'imm' field, should be loaded:


<table>
<thead>
<tr>
<th>



opcode construction

</th>
<th>



opcode

</th>
<th>



src

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



BPF\_IMM \| BPF\_DW \| BPF\_LD

</td>
<td>



0x18

</td>
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



data pointer

</td>
</tr>
</tbody>
</table>

On Linux, this integer is a BTF ID.

<a id="rst-legacy-bpf-packet-access-instructions"></a>

### 1.5   Legacy BPF Packet access instructions

As mentioned in the [ISA standard documentation](<~kernel/internals/bpf/standardization/instruction-set#rst-legacy-bpf-packet-access-instructions>)<a id="rst-isa-standard-documentation"></a>, Linux has special eBPF instructions for access to packet data that have been carried over from classic BPF to retain the performance of legacy socket filters running in the eBPF interpreter.

The instructions come in two forms: `BPF_ABS | <size> | BPF_LD` and `BPF_IND | <size> | BPF_LD`.

These instructions are used to access packet data and can only be used when the program context is a pointer to a networking packet.  `BPF_ABS` accesses packet data at an absolute offset specified by the immediate data and `BPF_IND` access packet data at an offset that includes the value of a register in addition to the immediate data.

These instructions have seven implicit operands:

- Register R6 is an implicit input that must contain a pointer to a struct sk\_buff.

- Register R0 is an implicit output which contains the data fetched from the packet.

- Registers R1-R5 are scratch registers that are clobbered by the instruction.

These instructions have an implicit program exit condition as well. If an eBPF program attempts access data beyond the packet boundary, the program execution will be aborted.

`BPF_ABS | BPF_W | BPF_LD` (0x20) means:



```text
R0 = ntohl(*(u32 *) ((struct sk_buff *) R6->data + imm))
```

where `ntohl()` converts a 32-bit value from network byte order to host byte order.

`BPF_IND | BPF_W | BPF_LD` (0x40) means:



```text
R0 = ntohl(*(u32 *) ((struct sk_buff *) R6->data + src + imm))
```
