---
title: "TOMOYO"
type: reference
description: "TOMOYO is a name-based MAC extension (LSM module) for the Linux kernel."
---

> **Peios:** This is reference material for an upstream LSM or its configuration. Peios configures `landlock,lockdown,integrity,pkm`; alternative MAC LSMs are incompatible with PKM, and this article is not an instruction to replace the Peios security stack. See [Peios kernel behaviour](<~kernel/introduction/peios-behaviour>).


<a id="rst-tomoyo"></a>

<a id="rst-what-is-tomoyo"></a>

## What is TOMOYO?

TOMOYO is a name-based MAC extension (LSM module) for the Linux kernel.

LiveCD-based tutorials are available at

[https://tomoyo.sourceforge.net/1.8/ubuntu12.04-live.html](<https://tomoyo.sourceforge.net/1.8/ubuntu12.04-live.html>) [https://tomoyo.sourceforge.net/1.8/centos6-live.html](<https://tomoyo.sourceforge.net/1.8/centos6-live.html>)

Though these tutorials use non-LSM version of TOMOYO, they are useful for you to know what TOMOYO is.

<a id="rst-how-to-enable-tomoyo"></a>

## How to enable TOMOYO?

Build the kernel with `CONFIG_SECURITY_TOMOYO=y` and pass `security=tomoyo` on kernel's command line.

Please see [https://tomoyo.sourceforge.net/2.6/](<https://tomoyo.sourceforge.net/2.6/>) for details.

<a id="rst-where-is-documentation"></a>

## Where is documentation?

User &lt;-&gt; Kernel interface documentation is available at [https://tomoyo.sourceforge.net/2.6/policy-specification/index.html](<https://tomoyo.sourceforge.net/2.6/policy-specification/index.html>) .

Materials we prepared for seminars and symposiums are available at [https://sourceforge.net/projects/tomoyo/files/docs/](<https://sourceforge.net/projects/tomoyo/files/docs/>) . Below lists are chosen from three aspects.

- **What is TOMOYO?**

  - **TOMOYO Linux Overview**

    [https://sourceforge.net/projects/tomoyo/files/docs/lca2009-takeda.pdf](<https://sourceforge.net/projects/tomoyo/files/docs/lca2009-takeda.pdf>)

  - **TOMOYO Linux: pragmatic and manageable security for Linux**

    [https://sourceforge.net/projects/tomoyo/files/docs/freedomhectaipei-tomoyo.pdf](<https://sourceforge.net/projects/tomoyo/files/docs/freedomhectaipei-tomoyo.pdf>)

  - **TOMOYO Linux: A Practical Method to Understand and Protect Your Own Linux Box**

    [https://sourceforge.net/projects/tomoyo/files/docs/PacSec2007-en-no-demo.pdf](<https://sourceforge.net/projects/tomoyo/files/docs/PacSec2007-en-no-demo.pdf>)

- **What can TOMOYO do?**

  - **Deep inside TOMOYO Linux**

    [https://sourceforge.net/projects/tomoyo/files/docs/lca2009-kumaneko.pdf](<https://sourceforge.net/projects/tomoyo/files/docs/lca2009-kumaneko.pdf>)

  - **The role of "pathname based access control" in security.**

    [https://sourceforge.net/projects/tomoyo/files/docs/lfj2008-bof.pdf](<https://sourceforge.net/projects/tomoyo/files/docs/lfj2008-bof.pdf>)

- **History of TOMOYO?**

  - **Realities of Mainlining**

    [https://sourceforge.net/projects/tomoyo/files/docs/lfj2008.pdf](<https://sourceforge.net/projects/tomoyo/files/docs/lfj2008.pdf>)
