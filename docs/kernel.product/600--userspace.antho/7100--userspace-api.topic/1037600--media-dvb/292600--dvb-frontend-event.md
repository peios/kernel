---
title: "frontend events"
type: reference
description: "Reference for frontend events."
---

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->





<a id="c-dvb_frontend_event"></a>

```c
dvb_frontend_event
```

<a id="rst-frontend-events"></a>

## frontend events



```c
struct dvb_frontend_event {
    fe_status_t status;
    struct dvb_frontend_parameters parameters;
};
```
