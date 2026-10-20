---
title: "request_firmware API"
type: reference
description: "You would typically load firmware and then load it into your device somehow. The typical firmware work flow is reflected below:"
---

> **Peios:** File-based firmware loading has an additional Peios signature check. The development profile defaults to logging (`kacs_fwsig=log`); `kacs_fwsig=enforce` requires PeiosTcb trust for that path. This does not cover the separate `FW_UPLOAD` interface. See [Peios kernel behaviour](<~kernel/introduction/peios-behaviour>).


<a id="rst-request-firmware-api"></a>

You would typically load firmware and then load it into your device somehow. The typical firmware work flow is reflected below:



```text
if(request_firmware(&fw_entry, $FIRMWARE, device) == 0)
       copy_fw_to_device(fw_entry->data, fw_entry->size);
release_firmware(fw_entry);
```

<a id="rst-synchronous-firmware-requests"></a>

## Synchronous firmware requests

Synchronous firmware requests will wait until the firmware is found or until an error is returned.

<a id="rst-request-firmware"></a>

### request_firmware

```{kernel-doc} drivers/base/firmware_loader/main.c
:functions: request_firmware
```

<a id="rst-firmware-request-nowarn"></a>

### firmware_request_nowarn

```{kernel-doc} drivers/base/firmware_loader/main.c
:functions: firmware_request_nowarn
```

<a id="rst-firmware-request-platform"></a>

### firmware_request_platform

```{kernel-doc} drivers/base/firmware_loader/main.c
:functions: firmware_request_platform
```

<a id="rst-request-firmware-direct"></a>

### request_firmware_direct

```{kernel-doc} drivers/base/firmware_loader/main.c
:functions: request_firmware_direct
```

<a id="rst-request-firmware-into-buf"></a>

### request_firmware_into_buf

```{kernel-doc} drivers/base/firmware_loader/main.c
:functions: request_firmware_into_buf
```

<a id="rst-asynchronous-firmware-requests"></a>

## Asynchronous firmware requests

Asynchronous firmware requests allow driver code to not have to wait until the firmware or an error is returned. Function callbacks are provided so that when the firmware or an error is found the driver is informed through the callback. request_firmware_nowait() cannot be called in atomic contexts.

<a id="rst-request-firmware-nowait"></a>

### request_firmware_nowait

```{kernel-doc} drivers/base/firmware_loader/main.c
:functions: request_firmware_nowait
```

<a id="rst-special-optimizations-on-reboot"></a>

## Special optimizations on reboot

Some devices have an optimization in place to enable the firmware to be retained during system reboot. When such optimizations are used the driver author must ensure the firmware is still available on resume from suspend, this can be done with firmware_request_cache() instead of requesting for the firmware to be loaded.

<a id="rst-firmware-request-cache"></a>

### firmware_request_cache()

```{kernel-doc} drivers/base/firmware_loader/main.c
:functions: firmware_request_cache
```

<a id="rst-request-firmware-api-expected-driver-use"></a>

## request firmware API expected driver use

Once an API call returns you process the firmware and then release the firmware. For example if you used request_firmware() and it returns, the driver has the firmware image accessible in fw_entry-&gt;\{data,size\}. If something went wrong request_firmware() returns non-zero and fw_entry is set to NULL. Once your driver is done with processing the firmware it can call release_firmware(fw_entry) to release the firmware image and any related resource.
