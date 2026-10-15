---
title: "Other Firmware Interfaces"
type: reference
description: "Some features of the Intel Stratix10 SoC require a level of privilege higher than the kernel is granted. Such secure features include FPGA programming. In terms of the ARMv8 architecture, the kernel runs at Exception Level 1 (EL1), access…"
---

> **Peios:** File-based firmware loading has an additional Peios signature check. The development profile defaults to logging (`kacs_fwsig=log`); `kacs_fwsig=enforce` requires PeiosTcb trust for that path. This does not cover the separate `FW_UPLOAD` interface. See [Peios kernel behaviour](<~kernel/introduction/peios-behaviour>).


<a id="rst-other-firmware-interfaces"></a>

<a id="rst-dmi-interfaces"></a>

## DMI Interfaces

```{kernel-doc} drivers/firmware/dmi_scan.c
:export:
```

<a id="rst-edd-interfaces"></a>

## EDD Interfaces

```{kernel-doc} drivers/firmware/edd.c
:internal:
```

<a id="rst-generic-system-framebuffers-interface"></a>

## Generic System Framebuffers Interface

```{kernel-doc} drivers/firmware/sysfb.c
:export:
```

<a id="rst-intel-stratix10-soc-service-layer"></a>

## Intel Stratix10 SoC Service Layer

Some features of the Intel Stratix10 SoC require a level of privilege higher than the kernel is granted. Such secure features include FPGA programming. In terms of the ARMv8 architecture, the kernel runs at Exception Level 1 (EL1), access to the features requires Exception Level 3 (EL3).

The Intel Stratix10 SoC service layer provides an in kernel API for drivers to request access to the secure features. The requests are queued and processed one by one. ARM’s SMCCC is used to pass the execution of the requests on to a secure monitor (EL3).

```{kernel-doc} include/linux/firmware/intel/stratix10-svc-client.h
:functions: stratix10_svc_command_code
```

```{kernel-doc} include/linux/firmware/intel/stratix10-svc-client.h
:functions: stratix10_svc_client_msg
```

```{kernel-doc} include/linux/firmware/intel/stratix10-svc-client.h
:functions: stratix10_svc_command_config_type
```

```{kernel-doc} include/linux/firmware/intel/stratix10-svc-client.h
:functions: stratix10_svc_cb_data
```

```{kernel-doc} include/linux/firmware/intel/stratix10-svc-client.h
:functions: stratix10_svc_client
```

```{kernel-doc} drivers/firmware/stratix10-svc.c
:export:
```
