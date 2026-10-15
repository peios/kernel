---
title: "Current State"
type: reference
description: "The following describes the current state of the NetWinder's floating point emulator."
---

<a id="rst-current-state"></a>

The following describes the current state of the NetWinder's floating point emulator.

In the following nomenclature is used to describe the floating point instructions.  It follows the conventions in the ARM manual.



```text
<S|D|E> = <single|double|extended>, no default
{P|M|Z} = {round to +infinity,round to -infinity,round to zero},
          default = round to nearest
```

Note: items enclosed in \{\} are optional.

<a id="rst-floating-point-coprocessor-data-transfer-instructions-cpdt"></a>

## Floating Point Coprocessor Data Transfer Instructions (CPDT)

LDF/STF - load and store floating

&lt;LDF\|STF&gt;\{cond\}&lt;S\|D\|E&gt; Fd, Rn &lt;LDF\|STF&gt;\{cond\}&lt;S\|D\|E&gt; Fd, \[Rn, \#&lt;expression&gt;\]\{\!\} &lt;LDF\|STF&gt;\{cond\}&lt;S\|D\|E&gt; Fd, \[Rn\], \#&lt;expression&gt;

These instructions are fully implemented.

LFM/SFM - load and store multiple floating

Form 1 syntax: &lt;LFM\|SFM&gt;\{cond\}&lt;S\|D\|E&gt; Fd, &lt;count&gt;, \[Rn\] &lt;LFM\|SFM&gt;\{cond\}&lt;S\|D\|E&gt; Fd, &lt;count&gt;, \[Rn, \#&lt;expression&gt;\]\{\!\} &lt;LFM\|SFM&gt;\{cond\}&lt;S\|D\|E&gt; Fd, &lt;count&gt;, \[Rn\], \#&lt;expression&gt;

Form 2 syntax: &lt;LFM\|SFM&gt;\{cond\}&lt;FD,EA&gt; Fd, &lt;count&gt;, \[Rn\]\{\!\}

These instructions are fully implemented.  They store/load three words for each floating point register into the memory location given in the instruction.  The format in memory is unlikely to be compatible with other implementations, in particular the actual hardware.  Specific mention of this is made in the ARM manuals.

<a id="rst-floating-point-coprocessor-register-transfer-instructions-cprt"></a>

## Floating Point Coprocessor Register Transfer Instructions (CPRT)

Conversions, read/write status/control register instructions

FLT\{cond\}&lt;S,D,E&gt;\{P,M,Z\} Fn, Rd          Convert integer to floating point FIX\{cond\}\{P,M,Z\} Rd, Fn                 Convert floating point to integer WFS\{cond\} Rd                            Write floating point status register RFS\{cond\} Rd                            Read floating point status register WFC\{cond\} Rd                            Write floating point control register RFC\{cond\} Rd                            Read floating point control register

FLT/FIX are fully implemented.

RFS/WFS are fully implemented.

RFC/WFC are fully implemented.  RFC/WFC are supervisor only instructions, and presently check the CPU mode, and do an invalid instruction trap if not called from supervisor mode.

Compare instructions

CMF\{cond\} Fn, Fm        Compare floating CMFE\{cond\} Fn, Fm       Compare floating with exception CNF\{cond\} Fn, Fm        Compare negated floating CNFE\{cond\} Fn, Fm       Compare negated floating with exception

These are fully implemented.

<a id="rst-floating-point-coprocessor-data-instructions-cpdt"></a>

## Floating Point Coprocessor Data Instructions (CPDT)

Dyadic operations:

ADF\{cond\}&lt;S\|D\|E&gt;\{P,M,Z\} Fd, Fn, &lt;Fm,\#value&gt; - add SUF\{cond\}&lt;S\|D\|E&gt;\{P,M,Z\} Fd, Fn, &lt;Fm,\#value&gt; - subtract RSF\{cond\}&lt;S\|D\|E&gt;\{P,M,Z\} Fd, Fn, &lt;Fm,\#value&gt; - reverse subtract MUF\{cond\}&lt;S\|D\|E&gt;\{P,M,Z\} Fd, Fn, &lt;Fm,\#value&gt; - multiply DVF\{cond\}&lt;S\|D\|E&gt;\{P,M,Z\} Fd, Fn, &lt;Fm,\#value&gt; - divide RDV\{cond\}&lt;S\|D\|E&gt;\{P,M,Z\} Fd, Fn, &lt;Fm,\#value&gt; - reverse divide

These are fully implemented.

FML\{cond\}&lt;S\|D\|E&gt;\{P,M,Z\} Fd, Fn, &lt;Fm,\#value&gt; - fast multiply FDV\{cond\}&lt;S\|D\|E&gt;\{P,M,Z\} Fd, Fn, &lt;Fm,\#value&gt; - fast divide FRD\{cond\}&lt;S\|D\|E&gt;\{P,M,Z\} Fd, Fn, &lt;Fm,\#value&gt; - fast reverse divide

These are fully implemented as well.  They use the same algorithm as the non-fast versions.  Hence, in this implementation their performance is equivalent to the MUF/DVF/RDV instructions.  This is acceptable according to the ARM manual.  The manual notes these are defined only for single operands, on the actual FPA11 hardware they do not work for double or extended precision operands.  The emulator currently does not check the requested permissions conditions, and performs the requested operation.

RMF\{cond\}&lt;S\|D\|E&gt;\{P,M,Z\} Fd, Fn, &lt;Fm,\#value&gt; - IEEE remainder

This is fully implemented.

Monadic operations:

MVF\{cond\}&lt;S\|D\|E&gt;\{P,M,Z\} Fd, &lt;Fm,\#value&gt; - move MNF\{cond\}&lt;S\|D\|E&gt;\{P,M,Z\} Fd, &lt;Fm,\#value&gt; - move negated

These are fully implemented.

ABS\{cond\}&lt;S\|D\|E&gt;\{P,M,Z\} Fd, &lt;Fm,\#value&gt; - absolute value SQT\{cond\}&lt;S\|D\|E&gt;\{P,M,Z\} Fd, &lt;Fm,\#value&gt; - square root RND\{cond\}&lt;S\|D\|E&gt;\{P,M,Z\} Fd, &lt;Fm,\#value&gt; - round

These are fully implemented.

URD\{cond\}&lt;S\|D\|E&gt;\{P,M,Z\} Fd, &lt;Fm,\#value&gt; - unnormalized round NRM\{cond\}&lt;S\|D\|E&gt;\{P,M,Z\} Fd, &lt;Fm,\#value&gt; - normalize

These are implemented.  URD is implemented using the same code as the RND instruction.  Since URD cannot return a unnormalized number, NRM becomes a NOP.

Library calls:

POW\{cond\}&lt;S\|D\|E&gt;\{P,M,Z\} Fd, Fn, &lt;Fm,\#value&gt; - power RPW\{cond\}&lt;S\|D\|E&gt;\{P,M,Z\} Fd, Fn, &lt;Fm,\#value&gt; - reverse power POL\{cond\}&lt;S\|D\|E&gt;\{P,M,Z\} Fd, Fn, &lt;Fm,\#value&gt; - polar angle (arctan2)

LOG\{cond\}&lt;S\|D\|E&gt;\{P,M,Z\} Fd, &lt;Fm,\#value&gt; - logarithm to base 10 LGN\{cond\}&lt;S\|D\|E&gt;\{P,M,Z\} Fd, &lt;Fm,\#value&gt; - logarithm to base e EXP\{cond\}&lt;S\|D\|E&gt;\{P,M,Z\} Fd, &lt;Fm,\#value&gt; - exponent SIN\{cond\}&lt;S\|D\|E&gt;\{P,M,Z\} Fd, &lt;Fm,\#value&gt; - sine COS\{cond\}&lt;S\|D\|E&gt;\{P,M,Z\} Fd, &lt;Fm,\#value&gt; - cosine TAN\{cond\}&lt;S\|D\|E&gt;\{P,M,Z\} Fd, &lt;Fm,\#value&gt; - tangent ASN\{cond\}&lt;S\|D\|E&gt;\{P,M,Z\} Fd, &lt;Fm,\#value&gt; - arcsine ACS\{cond\}&lt;S\|D\|E&gt;\{P,M,Z\} Fd, &lt;Fm,\#value&gt; - arccosine ATN\{cond\}&lt;S\|D\|E&gt;\{P,M,Z\} Fd, &lt;Fm,\#value&gt; - arctangent

These are not implemented.  They are not currently issued by the compiler, and are handled by routines in libc.  These are not implemented by the FPA11 hardware, but are handled by the floating point support code.  They should be implemented in future versions.

Signalling:

Signals are implemented.  However current ELF kernels produced by Rebel.com have a bug in them that prevents the module from generating a SIGFPE.  This is caused by a failure to alias fp_current to the kernel variable current_set\[0\] correctly.

The kernel provided with this distribution (vmlinux-nwfpe-0.93) contains a fix for this problem and also incorporates the current version of the emulator directly.  It is possible to run with no floating point module loaded with this kernel.  It is provided as a demonstration of the technology and for those who want to do floating point work that depends on signals.  It is not strictly necessary to use the module.

A module (either the one provided by Russell King, or the one in this distribution) can be loaded to replace the functionality of the emulator built into the kernel.
