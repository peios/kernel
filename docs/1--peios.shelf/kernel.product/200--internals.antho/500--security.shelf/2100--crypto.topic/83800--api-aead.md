---
title: "Authenticated Encryption With Associated Data (AEAD)"
type: reference
description: "Reference for Authenticated Encryption With Associated Data (AEAD)."
---

<a id="rst-authenticated-encryption-with-associated-data-aead"></a>

<a id="rst-authenticated-encryption-with-associated-data-aead-algorithm-definitions"></a>

## Authenticated Encryption With Associated Data (AEAD) Algorithm Definitions

```{kernel-doc} include/crypto/aead.h
:doc: Authenticated Encryption With Associated Data (AEAD) Cipher API
```

```{kernel-doc} include/crypto/aead.h
:functions: aead_request aead_alg
```

<a id="rst-authenticated-encryption-with-associated-data-aead-cipher-api"></a>

## Authenticated Encryption With Associated Data (AEAD) Cipher API

```{kernel-doc} include/crypto/aead.h
:functions: crypto_alloc_aead crypto_free_aead crypto_aead_ivsize crypto_aead_authsize crypto_aead_blocksize crypto_aead_setkey crypto_aead_setauthsize crypto_aead_encrypt crypto_aead_decrypt
```

<a id="rst-asynchronous-aead-request-handle"></a>

## Asynchronous AEAD Request Handle

```{kernel-doc} include/crypto/aead.h
:doc: Asynchronous AEAD Request Handle
```

```{kernel-doc} include/crypto/aead.h
:functions: crypto_aead_reqsize aead_request_set_tfm aead_request_alloc aead_request_free aead_request_set_callback aead_request_set_crypt aead_request_set_ad
```
