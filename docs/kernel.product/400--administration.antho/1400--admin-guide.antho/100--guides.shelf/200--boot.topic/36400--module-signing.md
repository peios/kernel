---
title: "Kernel module signing facility"
type: reference
description: "Peios module signature enforcement, public trust inputs and the separate signing stage."
---


<a id="rst-kernel-module-signing-facility"></a>

Peios requires a valid trusted signature before loading a kernel module.
Module signing, permission to load a module, and release qualification are
separate requirements.

<a id="rst-overview"></a>

## Overview

A module carries an appended PKCS#7 signature and a module-signature trailer.
The loader verifies the signed bytes against the configured trusted keyrings.
The trailing `~Module signature appended~.` marker indicates a signature is
present; it does not establish that the signature is valid or trusted.

<a id="rst-configuring-module-signing"></a>

## Peios configuration and build outputs

`peios/config/pkm.fragment` enables `CONFIG_MODULE_SIG`,
`CONFIG_MODULE_SIG_FORCE`, `CONFIG_MODULE_SIG_ALL`, SHA-512 and the ML-DSA-65
key type. It also enables the narrow PKCS#7 authenticated-attributes waiver
needed by ML-DSA signing with OpenSSL 3.x. That waiver does not generally admit
RSA/ECDSA module signatures with authenticated attributes.

The controlled build in `peios/build.sh` installs a **public certificate** as
`certs/peios-modsig.pem` and selects it with `CONFIG_MODULE_SIG_KEY`. The
production-configuration development profile uses `peios/keys/dev-modsig.pem`;
KUnit uses `peios/keys/kunit-modsig.pem`. These are development trust roots.
The raw module archive and development package payloads remain **unsigned**.
`CONFIG_MODULE_SIG_ALL=y` does not mean these build targets ran a private-key
signing stage. See [Building Peios](<~kernel/development/start-here/building-peios>).

<a id="rst-generating-signing-keys"></a>

## Signing keys

Private module-signing keys belong to the separate signing process and are not
inputs to the controlled kernel build. A signing key must match a certificate
trusted by the target kernel. The module-signing key is distinct from the key
used for Peios binary/PIP signatures.

The upstream default that generates an RSA key as part of Kbuild is not this
repository's configured workflow. Do not replace the checked-in trust input
with an ad hoc key and assume existing modules will remain trusted. Changing
the certificate changes the kernel's trust roots and requires corresponding
signing and qualification work.

<a id="rst-public-keys-in-the-kernel"></a>

## Public keys in the kernel

Built-in certificates populate `.builtin_trusted_keys`. Module verification
uses the secondary trusted keyring when configured, which links the built-in
ring and imposes certificate-chain restrictions on additions. Keyring access
permissions also apply. A bare `keyctl padd` command is not a way to install
an arbitrary module trust root, and the built-in ring is not an ordinary
user-writable provisioning interface.

<a id="rst-manually-signing-modules"></a>

## Signing a module

The low-level Kbuild signing utility has this form:

```text
scripts/sign-file sha512 <private-key> <x509-certificate> <module.ko>
```

Use a signer with ML-DSA support and a certificate trusted by the target kernel.
`scripts/sign-file.c` handles the OpenSSL 3.x ML-DSA CMS form; the configured
verification waiver is its counterpart. This command describes the signing
primitive, not a completed release procedure. Keep private keys outside the
kernel build inputs. The public-only development build cannot sign its own
module archive.

<a id="rst-signed-modules-and-stripping"></a>

## Signed modules and stripping

Finalize the module bytes, including any stripping, before signing. Changing
the signed module afterwards invalidates the signature. Package compression
must preserve the exact signed payload for the loader's decompression path.
Forcing a module past version checks does not bypass signature enforcement:
the loader treats requests to ignore vermagic or modversions as mangling the
signed input.

<a id="rst-loading-signed-modules"></a>

## Loading signed modules

Module loading requires enabled `SeLoadDriverPrivilege` through the
`CAP_SYS_MODULE` compatibility check, as well as successful signature and
normal loader checks. UID 0, a set-user-ID loader or file capabilities do not
grant that native privilege. A valid signature does not establish that the
module matches this kernel's ABI or has passed runtime qualification.

When the kernel invokes a userspace helper such as `/bin/modprobe`, KACS also
requires the helper executable to meet `PeiosTcb` trust. This helper-image
requirement is distinct from the module's PKCS#7 signature.

<a id="rst-non-valid-signatures-and-unsigned-modules"></a>

## Invalid signatures and unsigned modules

With `CONFIG_MODULE_SIG_FORCE=y`, unsigned modules, unavailable signing keys
and unsupported verification algorithms are rejected. Malformed signatures
and cryptographic failures are also fatal. Enabling a native privilege does
not waive this requirement. `module.sig_enforce` is enable-only and cannot
turn off the configured enforcement policy.

<a id="rst-administering-protecting-the-private-key"></a>

## Protecting and qualifying signing inputs

Keep the private key in the signing service or otherwise outside build and
source-package inputs. Preserve the target kernel, trusted certificate and
signed artifact provenance together. The repository's module-signature
qualification harness requires signed inputs trusted by the supplied kernel;
the unsigned development outputs do not meet that prerequisite. See
`peios/README.md` for the qualification entry points.
