---
title: "Configuring Git"
type: reference
description: "This chapter describes maintainer level git configuration."
---

> **Peios:** This is inherited Linux development and upstream contribution guidance. For Peios repository changes, follow [Peios Standards and Conventions](https://learn.peios.org/psc/) and use [Building Peios](<~kernel/development/start-here/building-peios>). Upstream mailing lists, maintainer roles and release processes below apply when contributing to Linux upstream.


<a id="rst-configuring-git"></a>

This chapter describes maintainer level git configuration.

Tagged branches used in pull requests (see [Documentation/maintainer/pull-requests.rst](~kernel/development/maintainer/pull-requests)) should be signed with the developers public GPG key. Signed tags can be created by passing `-u <key-id>` to `git tag`. However, since you would *usually* use the same key for the project, you can set it in the configuration and use the `-s` flag. To set the default `key-id` use:



```text
git config user.signingkey "keyname"
```

Alternatively, edit your `.git/config` or `~/.gitconfig` file by hand:



```text
[user]
        name = Jane Developer
        email = jd@domain.org
        signingkey = jd@domain.org
```

You may need to tell `git` to use `gpg2`:



```text
[gpg]
        program = /path/to/gpg2
```

You may also like to tell `gpg` which `tty` to use (add to your shell rc file):



```text
export GPG_TTY=$(tty)
```
