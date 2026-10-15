---
title: "Kernel credentials"
type: reference
description: "Linux credential lifetimes and their relationship to Peios tokens and access checks."
---

> **Peios:** This article explains Linux credential structures and their lifetimes. In Peios, native tokens, security descriptors and PIP determine authority; Unix fields and capability sets are compatibility views. See [Peios kernel behaviour](<~kernel/introduction/peios-behaviour>). Examples of other LSMs describe upstream models.


<a id="rst-credentials-in-linux"></a>

By: David Howells &lt;[dhowells@redhat.com](<mailto:dhowells@redhat.com>)&gt;

<a id="rst-contents"></a>



<a id="rst-overview"></a>

## Overview

An access check relates a subject, an object and a requested operation. In
Peios, KACS evaluates native tokens, object security descriptors (SDs), enabled
privileges and, for process access, process integrity protection (PIP). A
task's Unix IDs and Linux capability sets are not substitutes for that context.

The Linux credential container remains important: `task_struct::real_cred`
is the task's objective credential set, while `task_struct::cred` is its
subjective set, used when it acts on objects. They normally agree, but trusted
kernel code can temporarily override the subjective credentials. KACS attaches
its credential security data, including a token reference and projected IDs,
through the LSM security blob. Native process state has its own lifetime and
synchronization; it is also referenced from task security data.

This does not mean that every Unix field is ignored. Accounting, network
protocols and some inherited subsystem checks still use IDs or mode bits.
For example, `/proc/sys` checks its table permissions against the current
effective UID and groups, with optional subsystem-specific permission callbacks.
Those checks coexist with native authorization where an operation has a KACS
gate. UID 0 is neither a universal bypass nor universally irrelevant.

<a id="rst-types-of-credentials"></a>

## Credential data

- **Native authority:** the effective token supplies the subject for KACS
  checks. Its identity, privileges and restrictions are distinct from numeric
  Unix IDs and stored Linux capability sets. Process SDs and PIP provide
  additional process-access constraints.
- **Unix compatibility fields:** `struct cred` retains real, effective, saved
  and filesystem IDs, supplementary groups and accounting references. The
  Peios `current_fsuid()` and `current_fsgid()` accessors use the KACS projection;
  reading `cred->fsuid` directly is not equivalent. Unix ID setters ordinarily
  preserve the existing identity; they are not a native token-installation or
  privilege-dropping interface.
- **Linux capability sets:** effective, permitted, inheritable, ambient and
  bounding sets remain represented. KACS capability checks consult the token
  or an explicit compatibility rule rather than treating these sets as native
  grants. `capset()` must retain the compatibility-allow bits in the effective,
  permitted and inheritable sets; clearing them fails. Changing other stored
  bits does not grant or remove native privileges. Bounding-set and ambient
  operations also have KACS guards.
- **Securebits:** these flags participate in inherited credential handling;
  they do not turn Unix compatibility credentials into native authority.
- **Keys and keyrings:** per-thread, per-process and session keyring references
  allow subsystems such as network filesystems to obtain authentication
  material. Key permissions and protocol credentials remain separate from a
  Peios token.

See [Peios kernel behaviour](<~kernel/introduction/peios-behaviour>) for the
capability mapping, token-setter behaviour and configured LSMs. AF_KEY manages
networking key material through a separate socket API and is outside this
credential-container discussion.

<a id="rst-file-markings"></a>

## File markings and execution

Managed-file access uses the canonical SD (`security.peios.sd`, or
`system.ntfs_security` on NTFS3). Unix ownership, mode bits and protocol ACLs
may still be exposed, but copying those fields does not reproduce a native SD.
POSIX ACL updates are unsupported by the KACS hooks.

SUID/SGID markings and Linux file capabilities do not grant native token
privileges on `execve()`. Execution must pass file-execute and process security
baseline (PSB) checks. Verified Peios image signatures can establish a PIP
label, subject to the exec transition rules; a PIP label is not a replacement
token. Tracing and `no_new_privs` prevent raising that label above the current
one. Ordinary unsigned images may execute without a PIP label if the other
checks allow it; kernel-initiated usermode helpers require `PeiosTcb` trust.

<a id="rst-task-credentials"></a>

## Task Credentials

`struct cred` is a reference-counted container for Unix credential fields and references to groups, keys and LSM security data. Its publication rules govern the container; referenced native tokens and process-state objects also have their own lifetime and locking rules. Do not infer that every object reachable from a published credential is immutable.

Once a set of credentials has been prepared and committed, it may not be changed, barring the following exceptions:

> 1. its reference count may be changed;
>
> 2. the reference count on the group_info struct it points to may be changed;
>
> 3. the reference count on the security data it points to may be changed;
>
> 4. the reference count on any keyrings it points to may be changed;
>
> 5. any keyrings it points to may be revoked, expired or have their security attributes changed; and
>
> 6. the contents of any keyrings to which it points may be changed (the whole point of keyrings being a shared set of credentials, modifiable by anyone with appropriate access).

To alter anything in the cred struct, the copy-and-replace principle must be adhered to.  First take a copy, then alter the copy and then use RCU to change the task pointer to make it point to the new copy.  There are wrappers to aid with this (see below).

A task may only alter its \_own\_ credentials; it is no longer permitted for a task to alter another's credentials.  This means the `capset()` system call is no longer permitted to take any PID other than the one of the current process. Also `keyctl_instantiate()` and `keyctl_negate()` functions no longer permit attachment to process-specific keyrings in the requesting process as the instantiating process may need to create them.

<a id="rst-immutable-credentials"></a>

### Immutable Credentials

Once a set of credentials has been made public (by calling `commit_creds()` for example), it must be considered immutable, barring two exceptions:

> 1. The reference count may be altered.
>
> 2. While the keyring subscriptions of a set of credentials may not be changed, the keyrings subscribed to may have their contents altered.

To catch accidental credential alteration at compile time, struct task_struct has \_const\_ pointers to its credential sets, as does struct file.  Furthermore, certain functions such as `get_cred()` and `put_cred()` operate on const pointers, thus rendering casts unnecessary, but require to temporarily ditch the const qualification to be able to alter the reference count.

<a id="rst-accessing-task-credentials"></a>

### Accessing Task Credentials

A task can inspect its own current credential pointer without an RCU read-side lock. This does not remove the synchronization requirements of shared referenced objects or of a credential-changing operation. To obtain the current pointer, call:



```text
const struct cred *current_cred()
```

to get a pointer to its credentials structure, and it doesn't have to release it afterwards.

There are convenience wrappers for retrieving specific aspects of a task's credentials (the value is simply returned in each case):



```text
kuid_t current_uid(void)         Current's real UID
kgid_t current_gid(void)         Current's real GID
kuid_t current_euid(void)        Current's effective UID
kgid_t current_egid(void)        Current's effective GID
kuid_t current_fsuid(void)       Current's file access UID
kgid_t current_fsgid(void)       Current's file access GID
kernel_cap_t current_cap(void)  Current's effective capabilities
struct user_struct *current_user(void)  Current's user account
```

There are also convenience wrappers for retrieving specific associated pairs of a task's credentials:



```text
void current_uid_gid(kuid_t *, kgid_t *);
void current_euid_egid(kuid_t *, kgid_t *);
void current_fsuid_fsgid(kuid_t *, kgid_t *);
```

which return these pairs of values through their arguments after retrieving them from the current task's credentials.

In addition, there is a function for obtaining a reference on the current process's current set of credentials:



```text
const struct cred *get_current_cred(void);
```

and functions for getting references to one of the credentials that don't actually live in struct cred:



```text
struct user_struct *get_current_user(void);
struct group_info *get_current_groups(void);
```

which get references to the current process's user accounting structure and supplementary groups list respectively.

Once a reference has been obtained, it must be released with `put_cred()`, `free_uid()` or `put_group_info()` as appropriate.

<a id="rst-accessing-another-task-s-credentials"></a>

### Accessing Another Task's Credentials

While a task may access its own credentials without the need for locking, the same is not true of a task wanting to access another task's credentials.  It must use the RCU read lock and `rcu_dereference()`.

The `rcu_dereference()` is wrapped by:



```text
const struct cred *__task_cred(struct task_struct *task);
```

This should be used inside the RCU read lock, as in the following example:



```text
void foo(struct task_struct *t, struct foo_data *f)
{
        const struct cred *tcred;
        ...
        rcu_read_lock();
        tcred = __task_cred(t);
        f->uid = tcred->uid;
        f->gid = tcred->gid;
        f->groups = get_group_info(tcred->group_info);
        rcu_read_unlock();
        ...
}
```

Should it be necessary to hold another task's credentials for a long period of time, and possibly to sleep while doing so, then the caller should get a reference on them using:



```text
const struct cred *get_task_cred(struct task_struct *task);
```

This does all the RCU magic inside of it.  The caller must call put_cred() on the credentials so obtained when they're finished with.

> [!NOTE]
>
> The result of `__task_cred()` should not be passed directly to `get_cred()` as this may race with `commit_creds()`.

There are a couple of convenience functions to access bits of another task's credentials, hiding the RCU magic from the caller:



```text
kuid_t task_uid(task)            Task's real UID
kuid_t task_euid(task)           Task's effective UID
```

If the caller is holding the RCU read lock at the time anyway, then:



```text
__task_cred(task)->uid
__task_cred(task)->euid
```

should be used instead.  Similarly, if multiple aspects of a task's credentials need to be accessed, RCU read lock should be used, `__task_cred()` called, the result stored in a temporary pointer and then the credential aspects called from that before dropping the lock.  This prevents the potentially expensive RCU magic from being invoked multiple times.

Should some other single aspect of another task's credentials need to be accessed, then this can be used:



```text
task_cred_xxx(task, member)
```

where 'member' is a non-pointer member of the cred struct.  For instance:



```text
kuid_t task_cred_xxx(task, suid);
```

will retrieve 'struct cred::suid' from the task, doing the appropriate RCU magic.  This may not be used for pointer members as what they point to may disappear the moment the RCU read lock is dropped.

<a id="rst-altering-credentials"></a>

### Altering Credentials

Credential publication is performed by the task whose credentials change. Peios also has coordinated native token-installation paths; use their synchronization and authorization rules rather than writing another task's credential pointer. Copying or changing Unix fields alone does not install a native identity.

To alter the current process's credentials, a function should first prepare a new set of credentials by calling:



```text
struct cred *prepare_creds(void);
```

This allocates a duplicate of the current credentials, takes references to their shared members and calls the LSM preparation hook. It returns NULL on allocation or LSM preparation failure. It does not acquire a `cred_replace_mutex`; callers must obey the synchronization rules of the operation that is changing credentials.

The new credentials set should be altered appropriately, and any security checks and hooks done.  Both the current and the proposed sets of credentials are available for this purpose as current_cred() will return the current set still at this point.

When replacing the group list, the new list must be sorted before it is added to the credential, as a binary search is used to test for membership.  In practice, this means groups_sort() should be called before set_groups() or set_current_groups(). groups_sort() must not be called on a `struct group_info` which is shared as it may permute elements as part of the sorting process even if the array is already sorted.

When the credential set is ready, it should be committed to the current process by calling:



```text
int commit_creds(struct cred *new);
```

This updates credential-related accounting and process state, then publishes the new objective and subjective credentials with `rcu_assign_pointer()`. It notifies interested subsystems and drops the old credential references. It does not release a credential-replacement mutex.

This function is guaranteed to return 0, so that it can be tail-called at the end of such functions as `sys_setresuid()`.

Note that this function consumes the caller's reference to the new credentials. The caller should \_not\_ call `put_cred()` on the new credentials afterwards.

Furthermore, once this function has been called on a new set of credentials, those credentials may \_not\_ be changed further.

Should the security checks fail or some other error occur after `prepare_creds()` has been called, then the following function should be invoked:



```text
void abort_creds(struct cred *new);
```

This drops the reference to the uncommitted new credentials. It does not release a credential-replacement mutex.

A credential-changing operation must perform its real authorization checks before `commit_creds()`, and call `abort_creds()` on failure. There is no generic `security_alter_suid()` hook. Unix ID changes must follow the existing syscall and LSM fixup paths; native token changes must use the native token-installation path.

<a id="rst-managing-credentials"></a>

### Managing Credentials

There are some functions to help manage credentials:

> - `void put_cred(const struct cred *cred);`
>
>   > This releases a reference to the given set of credentials.  If the reference count reaches zero, the credentials will be scheduled for destruction by the RCU system.
>
> - `const struct cred *get_cred(const struct cred *cred);`
>
>   > This gets a reference on a live set of credentials, returning a pointer to that set of credentials.

<a id="rst-open-file-credentials"></a>

## Open file credentials

An opened `struct file` holds a reference to the opening credentials in
`f_cred`. The pointer remains stable for the file's lifetime, so accessing the
container does not require a fresh RCU lookup. Referenced objects retain their
own synchronization rules. Network filesystems can use these credentials when
authenticating operations to a remote server.

KACS separately records a granted-access snapshot on a managed file handle.
Later operations check the rights required by that operation; an SD change is
not general revocation of existing handles. `SCM_RIGHTS` transfers the existing
grant rather than authorizing a new open under the receiver's token. Internal
copy-up handles are rejected by the receive hook.

Do not universally substitute `f_cred` for the current subject in access checks.
Some checks deliberately use the current effective token, including the sysfs
write gate and continuous-access auditing. Follow the specific handle or
operation contract. Likewise, direct reads of `f_cred->fsuid` do not provide the
Peios projected-ID semantics of the current-credential accessors.

<a id="rst-overriding-the-vfs-s-use-of-credentials"></a>

## Overriding the VFS's use of credentials

Trusted kernel code can temporarily install subjective credentials with
`override_creds()` and restore them with `revert_creds()`. This is used by
stacking filesystems and other operations that act in a saved context. The
override must carry the correct LSM subject and obey its lifetime rules;
changing numeric UID fields alone is not a KACS subject switch.

In Peios, `access()` and `faccessat()` do not use the upstream real-UID
credential-override path: that code is excluded under `CONFIG_SECURITY_PKM`.
They perform the check in the current effective context. They therefore must
not be used as a test of what a different native token could access.

## Peios implementation details

<a id="trm-3-10-1"></a>

KACS tokens are the sole identity-based authorization mechanism, and
Linux applications do not know tokens exist. They call `getuid()`,
`getgid()` and `getgroups()`, read `/proc/self/status`, and assume
those numbers determine their access. KACS projects token identity
onto standard Linux credentials so unmodified applications work.

When a token is installed on a process, the process's Linux
credentials are set to match. <a id="cite-cred.projection.on-token-install"></a> The numbers themselves are **already on
the token**: the user SID's projected uid, the primary group SID's
projected gid, and a projected supplementary gid per group SID are all
computed by authd when the token is minted, and KACS copies them. <a id="cite-cred.projection.uid-from-token"></a>

**KACS never resolves a SID to a number itself.** It holds no directory
handle and consults nothing at install time — which is what makes
projection cheap enough to do on every credential change, and what
keeps a name-service outage from being able to change what a running
process may do.

How a SID becomes a number is therefore not KACS's rule to state, and
this chapter deliberately does not restate it. The authority is the
principal source interface's numeric scope (PSPU [Overview](<~kernel/internals/kmes/overview#trm-2-1>)): identifiers are
**computed** — an authority grants a source a band `(base, count)` and
derives `base + r` from a relative identifier — rather than looked up
per principal, and a source's assertion outside its band is refused
rather than clamped.

`65534` does appear in KACS, but not as a "no attribute was set"
fallback: it is `ANONYMOUS_PROJECTED_ID`, what the projected-id
accessors return for the anonymous identity and for an invalid token
pointer. <a id="cite-cred.projection.anonymous-sentinel"></a> It is a sentinel for *no identity*, not a default for an
identity whose number could not be found.

The consequences are mostly convenient ones. No process runs as UID 0
unless it holds the SYSTEM token — enforced, not merely expected: a
token creation naming a projected UID of 0 with any user SID other
than `S-1-5-18` is rejected, and the projection path refuses it again
at install time. <a id="cite-cred.projection.uid0-system-only"></a> Home directories work naturally, because
`getpwuid(getuid())` returns the right answer when the UID is real and
consistent with NSS. And different services get different UIDs, which
is incidental defence in depth alongside KACS's own enforcement.

<a id="trm-3-10-1-1"></a>

## Projection is one-way <a id="cite-cred.projection.one-way"></a>

Token state flows into credential fields and never the reverse. The
projected credentials are observational compatibility data; the token
is the authority. The `setuid` family restores the old credential
rather than deriving a token from it ([setuid Behaviour](<~kernel/internals/kacs/linux-credentials/setuid-behaviour#trm-3-10-3>)).

Projection reflects **all** groups regardless of enabled state, so
adjusting groups never triggers recalculation. <a id="cite-cred.projection.all-groups"></a>

Projected credentials reflect the **effective** token — the
impersonated one during impersonation, the primary one otherwise. <a id="cite-cred.projection.effective-token"></a> When
a service thread impersonates a client and creates a file, the file is
owned by the client's projected UID, quota is charged to the client,
and audit attributes to the client.

The two accessors deliberately disagree during impersonation.
`current_fsuid()` reads the projected UID from the *effective*
credential, so it yields the client's UID; `getuid()` reads the
*primary* credential's UID, so it yields the service's. During
impersonation `getuid()` returns the service and `current_fsuid()`
returns the client, and that is the intended behaviour rather than an
inconsistency. <a id="cite-cred.projection.getuid-vs-fsuid"></a> Only `getuid()` and `getgid()` are redirected to the
primary credential; `geteuid()` and `getegid()` keep their Linux
meaning and follow the effective credential, so during impersonation
they report the client.

One caveat applies to a credential carrying no token at all — a blank
credential, or one created before KACS initialised. `current_fsuid()`
falls back to `cred->fsuid` in that case, and the capability
switchboard denies before consulting the ALLOW list ([DAC Neutralisation](<~kernel/internals/kacs/linux-credentials/dac-neutralisation#trm-3-10-2>)), so
Linux DAC becomes authoritative for such a task. <a id="cite-cred.projection.tokenless-dac-fallback"></a>

<a id="trm-3-10-1-2"></a>

## Precomputed values

Every token carries precomputed projected UID and GID values,
calculated by authd at creation and stored on the token. KACS never
resolves a SID-to-UID mapping at runtime; the accessors are pure field
reads.

Because SIDs are one namespace while Linux UIDs and GIDs are two,
authd allocates from a **single unified counter** across all principal
types rather than a separate one per namespace, so every SID projects
to a unique number whichever Linux namespace it lands in. A user and a
group can never collide on a number, which is what lets one SID answer
both `getuid()` and `getgid()` questions without ambiguity.
