---
title: "Random Number Generator (RNG)"
type: reference
description: "Reference for Random Number Generator (RNG)."
---

<a id="rst-random-number-generator-rng"></a>

<a id="rst-random-number-algorithm-definitions"></a>

## Random Number Algorithm Definitions

```{kernel-doc} include/crypto/rng.h
:functions: rng_alg
```

<a id="rst-crypto-api-random-number-api"></a>

## Crypto API Random Number API

```{kernel-doc} include/crypto/rng.h
:doc: Random number generator API
```

```{kernel-doc} include/crypto/rng.h
:functions: crypto_alloc_rng crypto_rng_alg crypto_free_rng crypto_rng_generate crypto_rng_get_bytes crypto_rng_reset crypto_rng_seedsize
```
