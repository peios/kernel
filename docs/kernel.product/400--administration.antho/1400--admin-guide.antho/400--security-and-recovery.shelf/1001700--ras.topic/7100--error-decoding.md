---
title: "Error decoding"
type: reference
description: "Error decoding on AMD systems should be done using the rasdaemon tool: https://github.com/mchehab/rasdaemon/"
---

<a id="rst-error-decoding"></a>

<a id="rst-x86"></a>

## x86

<!-- SPDX-License-Identifier: GPL-2.0 -->

Error decoding on AMD systems should be done using the rasdaemon tool: [https://github.com/mchehab/rasdaemon/](<https://github.com/mchehab/rasdaemon/>)

While the daemon is running, it would automatically log and decode errors. If not, one can still decode such errors by supplying the hardware information from the error:



```text
$ rasdaemon -p --status <STATUS> --ipid <IPID> --smca
```

Also, the user can pass particular family and model to decode the error string:



```text
$ rasdaemon -p --status <STATUS> --ipid <IPID> --smca --family <CPU Family> --model <CPU Model> --bank <BANK_NUM>
```
