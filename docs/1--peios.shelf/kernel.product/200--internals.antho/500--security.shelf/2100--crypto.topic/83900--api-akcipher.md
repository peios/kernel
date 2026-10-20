---
title: "Asymmetric Cipher"
type: reference
description: "Reference for Asymmetric Cipher."
---

<a id="rst-asymmetric-cipher"></a>

<a id="rst-asymmetric-cipher-algorithm-definitions"></a>

## Asymmetric Cipher Algorithm Definitions

```{kernel-doc} include/crypto/akcipher.h
:functions: akcipher_alg akcipher_request
```

<a id="rst-asymmetric-cipher-api"></a>

## Asymmetric Cipher API

```{kernel-doc} include/crypto/akcipher.h
:doc: Generic Public Key Cipher API
```

```{kernel-doc} include/crypto/akcipher.h
:functions: crypto_alloc_akcipher crypto_free_akcipher crypto_akcipher_set_pub_key crypto_akcipher_set_priv_key crypto_akcipher_maxsize crypto_akcipher_encrypt crypto_akcipher_decrypt
```

<a id="rst-asymmetric-cipher-request-handle"></a>

## Asymmetric Cipher Request Handle

```{kernel-doc} include/crypto/akcipher.h
:functions: akcipher_request_alloc akcipher_request_free akcipher_request_set_callback akcipher_request_set_crypt
```
