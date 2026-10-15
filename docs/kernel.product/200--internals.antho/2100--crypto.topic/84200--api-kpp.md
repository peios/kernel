---
title: "Key-agreement Protocol Primitives (KPP)"
type: reference
description: "Reference for Key-agreement Protocol Primitives (KPP)."
---

<a id="rst-key-agreement-protocol-primitives-kpp"></a>

<a id="rst-key-agreement-protocol-primitives-kpp-cipher-algorithm-definitions"></a>

## Key-agreement Protocol Primitives (KPP) Cipher Algorithm Definitions

```{kernel-doc} include/crypto/kpp.h
:functions: kpp_request crypto_kpp kpp_alg kpp_secret
```

<a id="rst-key-agreement-protocol-primitives-kpp-cipher-api"></a>

## Key-agreement Protocol Primitives (KPP) Cipher API

```{kernel-doc} include/crypto/kpp.h
:doc: Generic Key-agreement Protocol Primitives API
```

```{kernel-doc} include/crypto/kpp.h
:functions: crypto_alloc_kpp crypto_free_kpp crypto_kpp_set_secret crypto_kpp_generate_public_key crypto_kpp_compute_shared_secret crypto_kpp_maxsize
```

<a id="rst-key-agreement-protocol-primitives-kpp-cipher-request-handle"></a>

## Key-agreement Protocol Primitives (KPP) Cipher Request Handle

```{kernel-doc} include/crypto/kpp.h
:functions: kpp_request_alloc kpp_request_free kpp_request_set_callback kpp_request_set_input kpp_request_set_output
```

<a id="rst-ecdh-helper-functions"></a>

## ECDH Helper Functions

```{kernel-doc} include/crypto/ecdh.h
:doc: ECDH Helper Functions
```

```{kernel-doc} include/crypto/ecdh.h
:functions: ecdh crypto_ecdh_key_len crypto_ecdh_encode_key crypto_ecdh_decode_key
```

<a id="rst-dh-helper-functions"></a>

## DH Helper Functions

```{kernel-doc} include/crypto/dh.h
:doc: DH Helper Functions
```

```{kernel-doc} include/crypto/dh.h
:functions: dh crypto_dh_key_len crypto_dh_encode_key crypto_dh_decode_key
```
