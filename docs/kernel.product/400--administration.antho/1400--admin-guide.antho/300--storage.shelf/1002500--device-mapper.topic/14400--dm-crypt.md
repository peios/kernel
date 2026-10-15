---
title: "dm-crypt"
type: reference
description: "Device-Mapper's \"crypt\" target provides transparent encryption of block devices using the kernel crypto API."
---

<a id="rst-dm-crypt"></a>

Device-Mapper's "crypt" target provides transparent encryption of block devices using the kernel crypto API.

For a more detailed description of supported parameters see: [https://gitlab.com/cryptsetup/cryptsetup/wikis/DMCrypt](<https://gitlab.com/cryptsetup/cryptsetup/wikis/DMCrypt>)

Parameters:



```text
<cipher> <key> <iv_offset> <device path> \
<offset> [<#opt_params> <opt_params>]
```

- **&lt;cipher&gt;**

  Encryption cipher, encryption mode and Initial Vector (IV) generator.

  The cipher specifications format is:



  ```text
  cipher[:keycount]-chainmode-ivmode[:ivopts]
  ```

  Examples:



  ```text
  aes-cbc-essiv:sha256
  aes-xts-plain64
  serpent-xts-plain64
  ```

  Cipher format also supports direct specification with kernel crypt API format (selected by capi: prefix). The IV specification is the same as for the first format type. This format is mainly used for specification of authenticated modes.

  The crypto API cipher specifications format is:



  ```text
  capi:cipher_api_spec-ivmode[:ivopts]
  ```

  Examples:



  ```text
  capi:cbc(aes)-essiv:sha256
  capi:xts(aes)-plain64
  ```

  Examples of authenticated modes:



  ```text
  capi:gcm(aes)-random
  capi:authenc(hmac(sha256),xts(aes))-random
  capi:rfc7539(chacha20,poly1305)-random
  ```

  The /proc/crypto contains a list of currently loaded crypto modes.

- **&lt;key&gt;**

  Key used for encryption. It is encoded either as a hexadecimal number or it can be passed as &lt;key_string&gt; prefixed with single colon character (':') for keys residing in kernel keyring service. You can only use key sizes that are valid for the selected cipher in combination with the selected iv mode. Note that for some iv modes the key string can contain additional keys (for example IV seed) so the key contains more parts concatenated into a single string.

- **&lt;key_string&gt;**

  The kernel keyring key is identified by string in following format: &lt;key_size&gt;:&lt;key_type&gt;:&lt;key_description&gt;.

- **&lt;key_size&gt;**

  The encryption key size in bytes. The kernel key payload size must match the value passed in &lt;key_size&gt;.

- **&lt;key_type&gt;**

  Either 'logon', 'user', 'encrypted' or 'trusted' kernel key type.

- **&lt;key_description&gt;**

  The kernel keyring key description crypt target should look for when loading key of &lt;key_type&gt;.

- **&lt;keycount&gt;**

  Multi-key compatibility mode. You can define &lt;keycount&gt; keys and then sectors are encrypted according to their offsets (sector 0 uses key0; sector 1 uses key1 etc.).  &lt;keycount&gt; must be a power of two.

- **&lt;iv_offset&gt;**

  The IV offset is a sector count that is added to the sector number before creating the IV.

- **&lt;device path&gt;**

  This is the device that is going to be used as backend and contains the encrypted data.  You can specify it as a path like /dev/xxx or a device number &lt;major&gt;:&lt;minor&gt;.

- **&lt;offset&gt;**

  Starting sector within the device where the encrypted data begins.

- **&lt;\#opt_params&gt;**

  Number of optional parameters. If there are no optional parameters, the optional parameters section can be skipped or \#opt_params can be zero. Otherwise \#opt_params is the number of following arguments.

  - **Example of optional parameters section:**

    3 allow_discards same_cpu_crypt submit_from_crypt_cpus

- **allow_discards**

  Block discard requests (a.k.a. TRIM) are passed through the crypt device. The default is to ignore discard requests.

  WARNING: Assess the specific security risks carefully before enabling this option.  For example, allowing discards on encrypted devices may lead to the leak of information about the ciphertext device (filesystem type, used space etc.) if the discarded blocks can be located easily on the device later.

- **same_cpu_crypt**

  Perform encryption using the same cpu that IO was submitted on. The default is to use an unbound workqueue so that encryption work is automatically balanced between available CPUs.

- **high_priority**

  Set dm-crypt workqueues and the writer thread to high priority. This improves throughput and latency of dm-crypt while degrading general responsiveness of the system.

- **submit_from_crypt_cpus**

  Disable offloading writes to a separate thread after encryption. There are some situations where offloading write bios from the encryption threads to a single thread degrades performance significantly.  The default is to offload write bios to the same thread because it benefits CFQ to have writes submitted using the same context.

- **no_read_workqueue**

  Bypass dm-crypt internal workqueue and process read requests synchronously.

- **no_write_workqueue**

  Bypass dm-crypt internal workqueue and process write requests synchronously. This option is automatically enabled for host-managed zoned block devices (e.g. host-managed SMR hard-disks).

- **integrity:&lt;bytes&gt;:&lt;type&gt;**

  The device requires additional &lt;bytes&gt; metadata per-sector stored in per-bio integrity structure. This metadata must by provided by underlying dm-integrity target.

  The &lt;type&gt; can be "none" if metadata is used only for persistent IV.

  For Authenticated Encryption with Additional Data (AEAD) the &lt;type&gt; is "aead". An AEAD mode additionally calculates and verifies integrity for the encrypted device. The additional space is then used for storing authentication tag (and persistent IV if needed).

- **integrity_key_size:&lt;bytes&gt;**

  Optionally set the integrity key size if it differs from the digest size. It allows the use of wrapped key algorithms where the key size is independent of the cryptographic key size.

- **sector_size:&lt;bytes&gt;**

  Use &lt;bytes&gt; as the encryption unit instead of 512 bytes sectors. This option can be in range 512 - 4096 bytes and must be power of two. Virtual device will announce this size as a minimal IO and logical sector.

- **iv_large_sectors**

  IV generators will use sector number counted in &lt;sector_size&gt; units instead of default 512 bytes sectors.

  For example, if &lt;sector_size&gt; is 4096 bytes, plain64 IV for the second sector will be 8 (without flag) and 1 if iv_large_sectors is present. The &lt;iv_offset&gt; must be multiple of &lt;sector_size&gt; (in 512 bytes units) if this flag is specified.

- **integrity_key_size:&lt;bytes&gt;**

  Use an integrity key of &lt;bytes&gt; size instead of using an integrity key size of the digest size of the used HMAC algorithm.

- **Module parameters::**

  - **max_read_size**

    Maximum size of read requests. When a request larger than this size is received, dm-crypt will split the request. The splitting improves concurrency (the split requests could be encrypted in parallel by multiple cores), but it also causes overhead. The user should tune this parameters to fit the actual workload.

  - **max_write_size**

    Maximum size of write requests. When a request larger than this size is received, dm-crypt will split the request. The splitting improves concurrency (the split requests could be encrypted in parallel by multiple cores), but it also causes overhead. The user should tune this parameters to fit the actual workload.

<a id="rst-example-scripts"></a>

## Example scripts

LUKS (Linux Unified Key Setup) is now the preferred way to set up disk encryption with dm-crypt using the 'cryptsetup' utility, see [https://gitlab.com/cryptsetup/cryptsetup](<https://gitlab.com/cryptsetup/cryptsetup>)



```text
#!/bin/sh
# Create a crypt device using dmsetup
dmsetup create crypt1 --table "0 `blockdev --getsz $1` crypt aes-cbc-essiv:sha256 babebabebabebabebabebabebabebabe 0 $1 0"
```



```text
#!/bin/sh
# Create a crypt device using dmsetup when encryption key is stored in keyring service
dmsetup create crypt2 --table "0 `blockdev --getsize $1` crypt aes-cbc-essiv:sha256 :32:logon:my_prefix:my_key 0 $1 0"
```



```text
#!/bin/sh
# Create a crypt device using cryptsetup and LUKS header with default cipher
cryptsetup luksFormat $1
cryptsetup luksOpen $1 crypt1
```
