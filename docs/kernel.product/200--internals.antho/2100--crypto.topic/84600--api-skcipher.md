---
title: "Symmetric Key Cipher"
type: reference
description: "Reference for Symmetric Key Cipher."
---

<a id="rst-symmetric-key-cipher"></a>

<a id="rst-block-cipher-algorithm-definitions"></a>

## Block Cipher Algorithm Definitions

```{kernel-doc} include/linux/crypto.h
:doc: Block Cipher Algorithm Definitions
```

```{kernel-doc} include/linux/crypto.h
:functions: crypto_alg cipher_alg compress_alg
```

<a id="rst-symmetric-key-cipher-api"></a>

## Symmetric Key Cipher API

```{kernel-doc} include/crypto/skcipher.h
:doc: Symmetric Key Cipher API
```

```{kernel-doc} include/crypto/skcipher.h
:functions: crypto_alloc_skcipher crypto_free_skcipher crypto_has_skcipher crypto_skcipher_ivsize crypto_skcipher_blocksize crypto_skcipher_setkey crypto_skcipher_reqtfm crypto_skcipher_encrypt crypto_skcipher_decrypt
```

<a id="rst-symmetric-key-cipher-request-handle"></a>

## Symmetric Key Cipher Request Handle

```{kernel-doc} include/crypto/skcipher.h
:doc: Symmetric Key Cipher Request Handle
```

```{kernel-doc} include/crypto/skcipher.h
:functions: crypto_skcipher_reqsize skcipher_request_set_tfm skcipher_request_alloc skcipher_request_free skcipher_request_set_callback skcipher_request_set_crypt
```

<a id="rst-single-block-cipher-api"></a>

## Single Block Cipher API

```{kernel-doc} include/crypto/internal/cipher.h
:doc: Single Block Cipher API
```

```{kernel-doc} include/crypto/internal/cipher.h
:functions: crypto_alloc_cipher crypto_free_cipher crypto_has_cipher crypto_cipher_blocksize crypto_cipher_setkey crypto_cipher_encrypt_one crypto_cipher_decrypt_one
```
