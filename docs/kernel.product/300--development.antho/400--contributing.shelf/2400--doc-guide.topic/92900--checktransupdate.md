---
title: "Checking for needed translation updates"
type: reference
description: "This script helps track the translation status of the documentation in different locales, i.e., whether the documentation is up-to-date with the English counterpart."
---

<a id="rst-checking-for-needed-translation-updates"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

This script helps track the translation status of the documentation in different locales, i.e., whether the documentation is up-to-date with the English counterpart.

<a id="rst-how-it-works"></a>

## How it works

It uses `git log` command to track the latest English commit from the translation commit (order by author date) and the latest English commits from HEAD. If any differences occur, the file is considered as out-of-date, then commits that need to be updated will be collected and reported.

Features implemented

- check all files in a certain locale

- check a single file or a set of files

- provide options to change output format

- track the translation status of files that have no translation

<a id="rst-usage"></a>

## Usage



```text
tools/docs/checktransupdate.py --help
```

Please refer to the output of argument parser for usage details.

Samples

- `tools/docs/checktransupdate.py -l zh_CN` This will print all the files that need to be updated in the zh_CN locale.

- `tools/docs/checktransupdate.py Documentation/translations/zh_CN/dev-tools/testing-overview.rst` This will only print the status of the specified file.

Then the output is something like:



```text
Documentation/dev-tools/kfence.rst
No translation in the locale of zh_CN

Documentation/translations/zh_CN/dev-tools/testing-overview.rst
commit 42fb9cfd5b18 ("Documentation: dev-tools: Add link to RV docs")
1 commits needs resolving in total
```

Features to be implemented

- files can be a folder instead of only a file
