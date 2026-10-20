---
title: "Mount classes and bootstrap descriptors"
description: "Mount classes and bootstrap descriptors: behaviour and implementation of the Peios kernel."
type: reference
---

<a id="trm-3-9-5-3"></a>

## Mount policy classes

The superblock policy object carries the class ([The Handle Model](<~kernel/internals/kacs/file-security/the-handle-model#trm-3-9-1>)) and, for
synthesise-class mounts, an optional mount-level default template.

The default classifier maps from the superblock's filesystem magic.
`PROC_SUPER_MAGIC` and `SYSFS_MAGIC` are **unmanaged**: these expose
kernel state through inode-shaped handles with no on-disk identity and
no descriptor to consult. <a id="cite-facs.storage.proc-sysfs-unmanaged"></a> `NULL_FS_MAGIC` is unmanaged too — nullfs is
the immutable, permanently empty filesystem the kernel mounts as the
mount-namespace root, with the mutable rootfs mounted on top of it. It
declares no xattr support at all, so it can never carry a descriptor,
and its single root inode is immutable and childless: nothing to stamp
and nothing to protect. <a id="cite-facs.storage.nullfs-unmanaged"></a>

`STRATAFS_SUPER_MAGIC` is fixed at **`facs_deny_missing`** for the
superblock's lifetime, because StrataFS delegates every check to
current provider objects and must never synthesise a descriptor for
its merged namespace. <a id="cite-facs.storage.stratafs-fixed-deny-missing"></a> An attempt to change it fails with
`EOPNOTSUPP`.

`RAMFS_MAGIC`, `NFS_SUPER_MAGIC`, `MSDOS_SUPER_MAGIC`,
`EXFAT_SUPER_MAGIC`, `ISOFS_SUPER_MAGIC` and `CGROUP2_SUPER_MAGIC` are
**`facs_synthesize_ephemeral`** — either no persistent backing at all,
or storage with no native descriptor slot. <a id="cite-facs.storage.ephemeral-magics"></a>

Everything else, including `TMPFS_MAGIC`, `SQUASHFS_MAGIC`,
`EXT4_SUPER_MAGIC` and `BTRFS_SUPER_MAGIC`, defaults to
**`facs_deny_missing`**. <a id="cite-facs.storage.default-deny-missing"></a> These can all carry the descriptor xattr
natively and are expected to on every inode that participates in
access checks.

`TMPFS_MAGIC` covers both userspace tmpfs mounts and the kernel-mounted
instances established before any userspace runs. The latter are not
exempt from the default; they are handled by seeding.

<a id="trm-3-9-5-4"></a>

## Kernel-internal mounts <a id="cite-facs.storage.kernel-internal-mounts"></a>

Two filesystems are mounted by the kernel before any userspace process
exists and before anything can call `kacs_set_mount_policy` or
`kacs_set_sd`: the mutable root filesystem mounted by
`init_mount_tree`, a tmpfs mounted on top of the immutable nullfs
namespace root and made `/` by `set_fs_root`; and the devtmpfs
instance mounted by `devtmpfs_init` and populated by the `kdevtmpfs`
thread.

Both are `TMPFS_MAGIC` and therefore `facs_deny_missing`, and their
root inodes are kernel-created, never passing through a
userspace-supplied artifact, so they carry no descriptor at the moment
they become reachable. To make the class viable the kernel seeds one.

The mutable root filesystem is a tmpfs whatever the command line says.
<a id="cite-facs.storage.rootfs-always-tmpfs"></a> Upstream Linux makes it a ramfs
when the command line carries `root=`, or a `rootfstype=` that does not
name tmpfs, and ramfs stores no extended attributes: the seed below
would have nowhere to go, nothing the boot archive unpacks would
inherit a descriptor, and StrataFS, which reads a provider's stored
descriptor and never a synthesised one, would refuse every view an
initramfs mounts over it. An installed system always boots with
`root=`, so the upstream rule is not followed.

The rootfs root is seeded inside `init_mount_tree`, immediately after
`vfs_kern_mount` returns and before the mount is published into
`init_mnt_ns`, with the inode's `i_rwsem` held. <a id="cite-facs.storage.rootfs-seed-timing"></a> The devtmpfs root is
seeded inside `devtmpfs_init`, after `vfs_kern_mount` and before
`kdevtmpfs` starts, likewise under `i_rwsem`. <a id="cite-facs.storage.devtmpfs-seed-timing"></a> The nullfs root is not
seeded — it is unmanaged, empty, and incapable of xattr storage. <a id="cite-facs.storage.nullfs-not-seeded"></a>

A rootfs seed that fails panics the kernel. <a id="cite-facs.storage.rootfs-seed-failure-is-fatal"></a>
A boot that went on without it would fail later, in whatever first
reached the initramfs through a StrataFS view, with nothing to connect
the refusal to its cause.

The seeded descriptor is byte-for-byte identical in both places: owner
and group SYSTEM (`S-1-5-18`), a DACL of one `ACCESS_ALLOWED` ACE
granting `GENERIC_ALL` to SYSTEM flagged
`OBJECT_INHERIT_ACE | CONTAINER_INHERIT_ACE` so that inheritance
derives a child descriptor for every inode created on the mount
afterwards, and no SACL. <a id="cite-facs.storage.seeded-descriptor-contents"></a>

The writes go through the kernel-internal xattr path, bypassing both
the FACS denial hooks and the LSM setxattr permission hook. <a id="cite-facs.storage.seed-writes-bypass-hooks"></a> They
consult no token — at the point either runs there may be no meaningful
subject — and the seeded descriptor is the sole authority for the
mount until trusted userspace replaces it. They depend on nothing
beyond the LSM scaffold that allocates inode and superblock blobs.

These are not exempt from later management: trusted userspace can
overwrite the per-inode descriptor or change the superblock's class
once it holds the privileges. <a id="cite-facs.storage.seeded-mounts-still-manageable"></a>

<a id="trm-3-9-5-5"></a>

## Boot artifacts <a id="cite-facs.storage.boot-artifacts-not-seeded"></a>

A filesystem shipped as a boot artifact — a squashfs concatenated into
the initrd, a vendor squashfs delivered as a package, a flashed
partition image — defaults to `facs_deny_missing` and the kernel does
**not** seed it. These are already-populated trees the kernel cannot
extend at mount time, and in the read-only case cannot extend at all.

The obligation falls on the build pipeline, which emits
`security.peios.sd` on every inode ordinary access checks will reach.
`mksquashfs`, the ext utilities and the standard userland xattr
surfaces all preserve `security.*` natively.

An artifact without descriptors is a packaging defect. FACS treats
every missing descriptor on a `facs_deny_missing` mount as a
corruption indicator and denies. The operator path is to rebuild the
artifact, or to adopt the superblock under a synthesise class.

<a id="trm-3-9-5-6"></a>

## Administration <a id="cite-facs.storage.set-mount-policy"></a>

The privilege gate below is verified in kernel source
[`8e0e22de3a59cad506bbbf8873de456e16ad272d`](https://github.com/peios/pkm/blob/8e0e22de3a59cad506bbbf8873de456e16ad272d/kacs/capability.c#L613-L637),
including its use by both [set](https://github.com/peios/pkm/blob/8e0e22de3a59cad506bbbf8873de456e16ad272d/kacs/mount_policy.c#L369-L380)
and [get](https://github.com/peios/pkm/blob/8e0e22de3a59cad506bbbf8873de456e16ad272d/kacs/mount_policy.c#L479-L496). This is source-level
verification, not a deployed-kernel test or a historical release boundary.

Trusted userspace adopts a mounted filesystem by calling
`kacs_set_mount_policy` on a descriptor naming any object on the
target superblock; `O_PATH` descriptors are valid targets. The change
applies to the superblock, not the pathname used to reach it.

Setting a policy is volume management: the call requires
`SeManageVolumePrivilege` or `SeTcbPrivilege`, enabled, and must
successfully mark the enabled privilege as used; `kacs_get_mount_policy`
is gated the same way. <a id="cite-facs.storage.set-mount-policy-privilege"></a> Every change writes a
`kacs.mount.policy.changed` record ([Audit Event Schemas](<~kernel/internals/kacs/auditing/event-families-and-delivery#trm-3-c>)), whose subject is the caller
and which names the filesystem's type, the policy set
(`object.mount.policy`), the one it replaced
(`object.mount.policy-previous`) and the new generation
(`object.mount.policy-generation`). Every refusal is decided before the
change, so a record is always of a change made; the template is not
carried. <a id="cite-facs.storage.set-mount-policy-recorded"></a> The
public ABI accepts only the three managed classes; `unmanaged`,
unknown values, nonzero reserved flags and malformed arguments all
fail closed. <a id="cite-facs.storage.set-mount-policy-input-validation"></a> The one
policy the kernel sets on its own initiative is for a tmpfs that a token
without the privilege brought into being inside its own mount namespace,
which is stamped `synth-ephemeral` with a creator-owned template at
`sb_kern_mount` ([A Private Mount Table](<~kernel/internals/kacs/mount-namespaces/a-private-mount-table#trm-3-13-1>)).

The optional template is accepted only with a synthesise class. <a id="cite-facs.storage.template-requires-synthesise"></a> It is
a complete self-relative descriptor rather than a subset, passes
structural validation, and is at most 65535 bytes. <a id="cite-facs.storage.template-validation"></a> A null pointer with
zero length clears it. <a id="cite-facs.storage.template-null-clears"></a> Setting `facs_deny_missing` clears it and
rejects non-empty template input. <a id="cite-facs.storage.deny-missing-clears-template"></a> Pointer and length mismatches and
invalid bytes fail before any state changes.

Policy changes are **lazy**. They do not walk the filesystem and do
not stamp anything. <a id="cite-facs.storage.policy-change-lazy"></a> The superblock carries a monotonic generation
counter, incremented on every successful policy or template
replacement. <a id="cite-facs.storage.generation-counter"></a> Missing-descriptor, ephemeral-synthetic and
not-yet-written-back persistent-synthetic cache entries record the
generation they came from and are discarded and repopulated when it
changes. <a id="cite-facs.storage.generation-discards-synthetic"></a> Xattr-backed and corrupt-descriptor caches are not made valid
by a policy change, and open file descriptions keep their immutable
masks. <a id="cite-facs.storage.policy-change-keeps-xattr-caches"></a>
