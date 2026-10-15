---
title: "MOXA Smartio/Industio Family Device Driver Installation Guide"
type: reference
description: "Copyright (C) 2008, Moxa Inc. Copyright (C) 2021, Jiri Slaby"
---

<a id="rst-moxa-smartio-industio-family-device-driver-installation-guide"></a>

Copyright (C) 2008, Moxa Inc. Copyright (C) 2021, Jiri Slaby

<!-- Content

1. Introduction
2. System Requirement
3. Installation
   3.1 Hardware installation
   3.2 Device naming convention
4. Utilities
5. Setserial
6. Troubleshooting -->

<a id="rst-introduction"></a>

## 1. Introduction

> The Smartio/Industio/UPCI family Linux driver supports following multiport boards:
>
> > - - **2 ports multiport board**
> >
> >     CP-102U, CP-102UL, CP-102UF CP-132U-I, CP-132UL, CP-132, CP-132I, CP132S, CP-132IS, (CP-102, CP-102S)
> >
> > - - **4 ports multiport board**
> >
> >     CP-104EL, CP-104UL, CP-104JU, CP-134U, CP-134U-I, C104H/PCI, C104HS/PCI, CP-114, CP-114I, CP-114S, CP-114IS, CP-114UL, (C114HI, CT-114I), POS-104UL, CB-114, CB-134I
> >
> > - - **8 ports multiport board**
> >
> >     CP-118EL, CP-168EL, CP-118U, CP-168U, C168H/PCI, CB-108
>
> If a compatibility problem occurs, please contact Moxa at [support@moxa.com.tw](<mailto:support@moxa.com.tw>).
>
> In addition to device driver, useful utilities are also provided in this version. They are:
>
> > - - **msdiag**
> >
> >     Diagnostic program for displaying installed Moxa Smartio/Industio boards.
> >
> > - - **msmon**
> >
> >     Monitor program to observe data count and line status signals.
> >
> > - - **msterm     A simple terminal program which is useful in testing serial**
> >
> >     ports.
>
> All the drivers and utilities are published in form of source code under GNU General Public License in this version. Please refer to GNU General Public License announcement in each source code file for more detail.
>
> In Moxa's Web sites, you may always find the latest driver at [https://www.moxa.com/](<https://www.moxa.com/>).
>
> This version of driver can be installed as a Loadable Module (Module driver) or built-in into kernel (Static driver). Before you install the driver, please refer to hardware installation procedure in the User's Manual.
>
> We assume the user should be familiar with following documents:
>
> - Serial-HOWTO
>
> - Kernel-HOWTO

<a id="rst-system-requirement"></a>

## 2. System Requirement

> - Maximum 4 boards can be installed in combination

<a id="rst-installation"></a>

## 3. Installation

<a id="rst-hardware-installation"></a>

### 3.1 Hardware installation

<a id="rst-pci-upci-board"></a>

#### PCI/UPCI board

> You may need to adjust IRQ usage in BIOS to avoid IRQ conflict with other ISA devices. Please refer to hardware installation procedure in User's Manual in advance.

<a id="rst-pci-irq-sharing"></a>

#### PCI IRQ Sharing

> Each port within the same multiport board shares the same IRQ. Up to 4 Moxa Smartio/Industio PCI Family multiport boards can be installed together on one system and they can share the same IRQ.

<a id="rst-device-naming-convention"></a>

### 3.2 Device naming convention

> The device node is named "ttyMxx".

<a id="rst-device-naming-when-more-than-2-boards-installed"></a>

#### Device naming when more than 2 boards installed

> Naming convention for each Smartio/Industio multiport board is pre-defined as below.
>
>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> Board Num.
>
> </td>
> <td>
>
>
> Device node
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 1st board
>
> </td>
> <td>
>
>
> ttyM0  - ttyM7
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 2nd board
>
> </td>
> <td>
>
>
> ttyM8  - ttyM15
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 3rd board
>
> </td>
> <td>
>
>
> ttyM16 - ttyM23
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> 4th board
>
> </td>
> <td>
>
>
> ttyM24 - ttyM31
>
> </td>
> </tr>
> </tbody>
> </table>

<a id="rst-utilities"></a>

## 4. Utilities

> There are 3 utilities contained in this driver. They are msdiag, msmon and msterm. These 3 utilities are released in form of source code. They should be compiled into executable file and copied into /usr/bin.

<a id="rst-msdiag-diagnostic"></a>

### msdiag - Diagnostic

> This utility provides the function to display what Moxa Smartio/Industio board was found by the driver in the system.

<a id="rst-msmon-port-monitoring"></a>

### msmon - Port Monitoring

> This utility gives the user a quick view about all the MOXA ports' activities. One can easily learn each port's total received/transmitted (Rx/Tx) character count since the time when the monitoring is started.
>
> Rx/Tx throughputs per second are also reported in interval basis (e.g. the last 5 seconds) and in average basis (since the time the monitoring is started). You can reset all ports' count by &lt;HOME&gt; key. &lt;+&gt; &lt;-&gt; (plus/minus) keys to change the displaying time interval. Press &lt;ENTER&gt; on the port, that cursor stay, to view the port's communication parameters, signal status, and input/output queue.

<a id="rst-msterm-terminal-emulation"></a>

### msterm - Terminal Emulation

> This utility provides data sending and receiving ability of all tty ports, especially for MOXA ports. It is quite useful for testing simple application, for example, sending AT command to a modem connected to the port or used as a terminal for login purpose. Note that this is only a dumb terminal emulation without handling full screen operation.

<a id="rst-setserial"></a>

## 5. Setserial

> Supported Setserial parameters are listed as below.
>
>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> uart
>
> </td>
> <td>
>
>
> set UART type(16450 --&gt; disable FIFO, 16550A --&gt; enable FIFO)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> close_delay
>
> </td>
> <td>
>
>
> set the amount of time (in 1/100 of a second) that DTR should be kept low while being closed.
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> closing_wait
>
> </td>
> <td>
>
>
> set the amount of time (in 1/100 of a second) that the serial port should wait for data to be drained while being closed, before the receiver is disabled.
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> spd_hi
>
> </td>
> <td>
>
>
> Use 57.6kb when the application requests 38.4kb.
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> spd_vhi
>
> </td>
> <td>
>
>
> Use 115.2kb when the application requests 38.4kb.
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> spd_shi
>
> </td>
> <td>
>
>
> Use 230.4kb when the application requests 38.4kb.
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> spd_warp
>
> </td>
> <td>
>
>
> Use 460.8kb when the application requests 38.4kb.
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> spd_normal
>
> </td>
> <td>
>
>
> Use 38.4kb when the application requests 38.4kb.
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> spd_cust
>
> </td>
> <td>
>
>
> Use the custom divisor to set the speed when the application requests 38.4kb.
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> divisor
>
> </td>
> <td>
>
>
> This option sets the custom division.
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> baud_base
>
> </td>
> <td>
>
>
> This option sets the base baud rate.
>
> </td>
> </tr>
> </tbody>
> </table>

<a id="rst-troubleshooting"></a>

## 6. Troubleshooting

> The boot time error messages and solutions are stated as clearly as possible. If all the possible solutions fail, please contact our technical support team to get more help.
>
> - **Error msg:**
>
>   More than 4 Moxa Smartio/Industio family boards found. Fifth board and after are ignored.
>
> Solution: To avoid this problem, please unplug fifth and after board, because Moxa driver supports up to 4 boards.
