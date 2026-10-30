# Peios Kernel coding style

This is the kernel's exception guide to the
[central Peios coding style](https://learn.peios.org/psc/common-coding-rules/scope-and-precedence/),
developed under PEI-1506. The central guide supplies the common engineering rules; this document
identifies where the kernel follows different language or repository conventions.

## Scope

Apply Linux formatting and naming conventions to kernel C and headers, including
new Peios subsystems and changes to inherited Linux code. This keeps the kernel
internally consistent and reduces friction when integrating upstream changes.

Peios-only Python and shell wrappers follow the central language profiles.
Location in the kernel repository alone does not impose C indentation on them.
Inherited upstream tools and generated or vendored files retain their applicable
upstream conventions. Kernel Rust follows the kernel's Rust formatter setup,
not the C profile. For Peios-owned Rust, preserve module and import order:
automatic sorting can detach explanatory comments from the declarations they describe.

## Kernel C deviations

| Subject | Kernel rule | Central rule replaced |
| --- | --- | --- |
| Indentation | Hard tabs displayed at eight columns | Four spaces |
| Line length | Prefer 80 columns; allow justified longer lines | Strong 100-column target |
| Function braces | Opening brace on the next line | Same-line opening brace |
| Control-flow braces | Follow Linux's single-statement omission rules, with the body on a separate line | Omission only for a complete single-line clause |
| Mixed conditional chains | Use braces throughout when a branch requires them | Same intent as central chain rule |
| Type naming | Linux `snake_case` names and established kernel typedef conventions | `PascalCase` type names |
| Continuations and switch layout | Follow the kernel formatter and Linux layout | Common formatter/layout defaults |

Keep non-function opening braces on the control line. Respect Linux's exceptions
requiring braces, including a single nested control statement where omitting
them would obscure structure. Do not turn the shorter line preference into an
unconditional rejection of readable diagnostic strings or other justified lines.

The kernel's [C formatter configuration](../.clang-format) is the local
mechanical reference. Its current 80-column target and eight-column tabs match
the accepted profile. The
[Linux coding-style documentation](https://docs.kernel.org/process/coding-style.html)
provides the broader reference; use the version accompanying the kernel being
worked on when upstream guidance changes.

Use narrow, explained `clang-format off` / `clang-format on` regions when
automatic formatting obscures structure. The trace-event macro tables and event
definitions retain their hand-aligned layout; ordinary declarations around them
remain formatted. The optional KUnit copy branch in `kacs/sd_access.c` also keeps
its conditional-compilation layout so the `else` relationship stays clear. These
exceptions preserve layout only and do not exempt surrounding code from checks.

## Rules that continue to apply

Keep ownership, cleanup, errors, validation, concurrency and unsafe assumptions
clear. Performance remains a design concern from the outset, including the
approved encouragement of minor to moderate proactive complexity increases for
substantial expected relative gains, especially on critical hot paths. The kernel
profile is not an exemption from those engineering rules.

Use explicit struct names and pointer stars beside declared names, with useful
typedef exceptions consistent with kernel practice. Prefer functions over
function-like macros when preprocessor facilities are unnecessary.

Use kernel-specific mechanisms for allocation, locking and error handling.
The central distinction between expected errors and broken invariants does not
require a panic or warning for every internal error.

## Kernel Rust and wrappers

Use the repository's [Rust formatter configuration](../.rustfmt.toml) and
kernel-selected Rust toolchain/edition for kernel Rust. Do not copy the C tab
or brace rules into Rust files.

Apply the central Python and shell profiles to Peios-owned wrapper files
under this directory, excluding generated output and vendored dependencies.
Scope tooling by file ownership and language rather than one blanket setting
for every file in the repository.

## Cutover and checks

Peios-owned additions must meet their applicable rules as part of the migration
cutover. Do not reformat inherited Linux wholesale to impose central Peios style.
Preserve unrelated upstream and documentation work.

Changes to inherited kernel code follow the kernel profile without requiring
a whole-file style rewrite around a small change. The explicit cutover requirement
for Peios-owned additions still applies. Naming cleanup must preserve UAPI, ABI
and other external contracts. Intentional changes to those contracts require
separate functional review.

Use the kernel's existing style tools as inputs to review, with their versions
and invocation recorded when enforcement is implemented. A formatter or
`checkpatch.pl` result alone does not establish correctness or compliance with
all common rules. Explain narrow exceptions rather than disabling broad checks.

The [kernel style commands](style/README.md) now enforce formatter stability,
selected wrapper lint/type checks, and the explicit owned-file scope. They use
the inherited kernel formatter settings, with Rust module/import order preserved.
Generated files, the pinned ppk vendor snapshot and the active documentation
migration are excluded with reasons in `style/scope.json`. Kernel-owned Rust
cores are included; their [Cargo tests](rust/README.md) compile those same files.

Checkpatch remains advisory because it includes soft policies and context-sensitive
findings. Formatting and automated checks do not establish compliance with every
engineering rule, nor replace Kbuild/KUnit qualification.
