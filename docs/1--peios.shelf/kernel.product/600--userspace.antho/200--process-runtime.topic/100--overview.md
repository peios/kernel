---
title: Process Runtime
type: reference
description: Distinguish process syscalls, C runtime wrappers, and Peios security inheritance.
---

Launchers and supervisors need both the kernel task contract and their
language runtime's wrapper behavior. A C function with a familiar syscall
name can add cleanup, synchronization, or another syscall. Confirm the ABI
of the runtime shipped with the application.

This reference separates the contracts:

- [Creation and replacement](~kernel/userspace/process-runtime/creating-processes)
  covers fork, clone flags, exec, and pidfds.
- [Termination and collection](~kernel/userspace/process-runtime/collecting-processes)
  covers exit status, wait operations, and orphan adoption.
- [Thread operations](~kernel/userspace/process-runtime/thread-operations)
  covers thread identifiers, exit notification, and thread-local storage.

Peios security is not the upstream UID/capability model. Read
[token lifecycle](~kernel/internals/kacs/tokens/token-lifecycle) alongside the
creation contract. Process GUIDs, kernel process numbers, token identifiers,
and logon-session identifiers serve different purposes. A successful process
creation does not establish that the child can execute a selected program
or access its resources.
