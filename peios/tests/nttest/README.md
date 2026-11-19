# nttest: NT handle semantics runtime checks

A stopgap. These checks should become Provium Lua tests in
[the integration suite](../integration/) (PEI-1744); remove this directory
once they are.

`nttest.c` is a static C program that exercises the NT handle semantics
added by PEI-1720, through the KACS syscalls and ordinary Linux calls, in
one directory:

- control handles and `MAXIMUM_ALLOWED`;
- share modes, for files and directories, including unlink and rename by
  name;
- delete-pending, delete-on-close and POSIX-semantics delete;
- `kacs_rename`;
- byte-range locks;
- leases, including a break and its acknowledgement;
- read-only and Created At (`security.peios.sattr`);
- ancestor pins;
- creator access;
- on StrataFS, when the lower stratum holds `cu`, `cu2`, `cu3` and `cu4`:
  share state and delete-pending across copy-up, rename after copy-up, and
  a masked name. `NTTEST_UPPER` names the upper stratum's directory for the
  masking check.

It prints `PASS` or `FAIL` for each check, with the errno, and a summary
line. Two helper modes stand in for tools the test guest lacks:
`nttest --mount TARGET STRATA` mounts a StrataFS stack, and
`nttest --kmsg` prints the kernel log's warnings and KACS lines.

## Building

From the repository root:

```sh
gcc -static -O2 -Wall -idirafter include/uapi \
    peios/tests/nttest/nttest.c -o nttest
```

It is static because the guest has no matching C library.
`-idirafter` takes the host's `linux/` headers and this tree's `pkm/` ones.

## Running

`run.sh` is the guest script used for PEI-1720. It expects the radius dev
VM's runtime at `/lcl/radius-dev/current` (for `sd`) and the binary at
`/mnt/dev/nttest/nttest`, as the dev VM's shared directory provides. It
runs as SYSTEM and:

1. builds a StrataFS stack over ext4 in `/var/state/ntsfs`;
2. runs `nttest` on `/srv/nt` and `/tmp/nt` (tmpfs), `/var/state/nt`
   (ext4) and the StrataFS mount;
3. checks generic-right mapping through `sd set` and `sd show`;
4. prints the kernel log.

## Limits

Every check runs as SYSTEM, so none tests refusals between users. Only the
lease break uses a second process, and nothing tests races. `kacs_rename`
of a file directly under a StrataFS mount root is untested.
