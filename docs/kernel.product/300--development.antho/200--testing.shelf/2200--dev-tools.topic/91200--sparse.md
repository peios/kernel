---
title: "Sparse"
type: reference
description: "Sparse is a semantic checker for C programs; it can be used to find a number of potential problems with kernel code. See https://lwn.net/Articles/689907/ for an overview of sparse; this document contains some kernel-specific sparse…"
---

<a id="rst-sparse"></a>

<!-- Copyright 2004 Linus Torvalds -->

<!-- Copyright 2004 Pavel Machek <pavel@ucw.cz> -->

<!-- Copyright 2006 Bob Copeland <me@bobcopeland.com> -->

Sparse is a semantic checker for C programs; it can be used to find a number of potential problems with kernel code.  See [https://lwn.net/Articles/689907/](<https://lwn.net/Articles/689907/>) for an overview of sparse; this document contains some kernel-specific sparse information. More information on sparse, mainly about its internals, can be found in its official pages at [https://sparse.docs.kernel.org](<https://sparse.docs.kernel.org>).

<a id="rst-using-sparse-for-typechecking"></a>

## Using sparse for typechecking

"\_\_bitwise" is a type attribute, so you have to do something like this:



```text
typedef int __bitwise pm_request_t;

enum pm_request {
        PM_SUSPEND = (__force pm_request_t) 1,
        PM_RESUME = (__force pm_request_t) 2
};
```

which makes PM\_SUSPEND and PM\_RESUME "bitwise" integers (the "\_\_force" is there because sparse will complain about casting to/from a bitwise type, but in this case we really \_do\_ want to force the conversion). And because the enum values are all the same type, now "enum pm\_request" will be that type too.

And with gcc, all the "\_\_bitwise"/"\_\_force stuff" goes away, and it all ends up looking just like integers to gcc.

Quite frankly, you don't need the enum there. The above all really just boils down to one special "int \_\_bitwise" type.

So the simpler way is to just do:



```text
typedef int __bitwise pm_request_t;

#define PM_SUSPEND ((__force pm_request_t) 1)
#define PM_RESUME ((__force pm_request_t) 2)
```

and you now have all the infrastructure needed for strict typechecking.

One small note: the constant integer "0" is special. You can use a constant zero as a bitwise integer type without sparse ever complaining. This is because "bitwise" (as the name implies) was designed for making sure that bitwise types don't get mixed up (little-endian vs big-endian vs cpu-endian vs whatever), and there the constant "0" really \_is\_ special.

<a id="rst-getting-sparse"></a>

## Getting sparse

You can get tarballs of the latest released versions from: [https://www.kernel.org/pub/software/devel/sparse/dist/](<https://www.kernel.org/pub/software/devel/sparse/dist/>)

Alternatively, you can get snapshots of the latest development version of sparse using git to clone:



```text
git://git.kernel.org/pub/scm/devel/sparse/sparse.git
```

Once you have it, just do:



```text
make
make install
```

as a regular user, and it will install sparse in your \~/bin directory.

<a id="rst-using-sparse"></a>

## Using sparse

Do a kernel make with "make C=1" to run sparse on all the C files that get recompiled, or use "make C=2" to run sparse on the files whether they need to be recompiled or not.  The latter is a fast way to check the whole tree if you have already built it.

The optional make variable CF can be used to pass arguments to sparse.  The build system passes -Wbitwise to sparse automatically.

Note that sparse defines the \_\_CHECKER\_\_ preprocessor symbol.
