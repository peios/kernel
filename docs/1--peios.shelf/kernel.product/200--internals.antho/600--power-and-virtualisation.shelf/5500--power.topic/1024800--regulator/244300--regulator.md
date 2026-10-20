---
title: "Regulator Driver Interface"
type: reference
description: "The regulator driver interface is relatively simple and designed to allow regulator drivers to register their services with the core framework."
---

<a id="rst-regulator-driver-interface"></a>

The regulator driver interface is relatively simple and designed to allow regulator drivers to register their services with the core framework.

<a id="rst-registration"></a>

## Registration

Drivers can register a regulator by calling:



```text
struct regulator_dev *regulator_register(struct regulator_desc *regulator_desc,
                                         const struct regulator_config *config);
```

This will register the regulator's capabilities and operations to the regulator core.

Regulators can be unregistered by calling:



```text
void regulator_unregister(struct regulator_dev *rdev);
```

<a id="rst-regulator-events"></a>

## Regulator Events

Regulators can send events (e.g. overtemperature, undervoltage, etc) to consumer drivers by calling:



```text
int regulator_notifier_call_chain(struct regulator_dev *rdev,
                                  unsigned long event, void *data);
```
