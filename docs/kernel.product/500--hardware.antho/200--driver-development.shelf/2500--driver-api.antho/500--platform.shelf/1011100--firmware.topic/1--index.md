---
title: "Linux Firmware API"
type: reference
description: "Reference for Linux Firmware API."
---

> **Peios:** File-based firmware loading has an additional Peios signature check. The development profile defaults to logging (`kacs_fwsig=log`); `kacs_fwsig=enforce` requires PeiosTcb trust for that path. This does not cover the separate `FW_UPLOAD` interface. See [Peios kernel behaviour](<~kernel/introduction/peios-behaviour>).


<a id="rst-linux-firmware-api"></a>

- [Introduction](<~kernel/hardware/driver-api/firmware/introduction>)
- [Firmware API core features](<~kernel/hardware/driver-api/firmware/core>)
- [Unified Extensible Firmware Interface (UEFI) Support](<~kernel/hardware/driver-api/firmware-efi/index>)
- [request_firmware API](<~kernel/hardware/driver-api/firmware/request-firmware>)
- [Firmware Upload API](<~kernel/hardware/driver-api/firmware/fw-upload>)
- [Other Firmware Interfaces](<~kernel/hardware/driver-api/firmware/other-interfaces>)
