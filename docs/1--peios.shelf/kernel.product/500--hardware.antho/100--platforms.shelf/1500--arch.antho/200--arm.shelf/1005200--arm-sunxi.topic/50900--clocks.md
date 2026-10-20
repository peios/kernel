---
title: "Frequently asked questions about the sunxi clock system"
type: reference
description: "This document contains useful bits of information that people tend to ask about the sunxi clock system, as well as accompanying ASCII art when adequate."
---

<a id="rst-frequently-asked-questions-about-the-sunxi-clock-system"></a>

This document contains useful bits of information that people tend to ask about the sunxi clock system, as well as accompanying ASCII art when adequate.

- **Q: Why is the main 24MHz oscillator gateable? Wouldn't that break the**

  system?

- **A: The 24MHz oscillator allows gating to save power. Indeed, if gated**

  carelessly the system would stop functioning, but with the right steps, one can gate it and keep the system running. Consider this simplified suspend example:

  While the system is operational, you would see something like:



  ```text
  24MHz         32kHz
   |
  PLL1
   \
    \_ CPU Mux
         |
       [CPU]
  ```

  When you are about to suspend, you switch the CPU Mux to the 32kHz oscillator:



  ```text
    24Mhz         32kHz
     |              |
    PLL1            |
                   /
         CPU Mux _/
           |
         [CPU]

  Finally you can gate the main oscillator::

                  32kHz
                    |
                    |
                   /
         CPU Mux _/
           |
         [CPU]
  ```

Q: Were can I learn more about the sunxi clocks?

- **A: The linux-sunxi wiki contains a page documenting the clock registers,**

  you can find it at

  > [http://linux-sunxi.org/A10/CCM](<http://linux-sunxi.org/A10/CCM>)

  The authoritative source for information at this time is the ccmu driver released by Allwinner, you can find it at

  > [https://github.com/linux-sunxi/linux-sunxi/tree/sunxi-3.0/arch/arm/mach-sun4i/clock/ccmu](<https://github.com/linux-sunxi/linux-sunxi/tree/sunxi-3.0/arch/arm/mach-sun4i/clock/ccmu>)
