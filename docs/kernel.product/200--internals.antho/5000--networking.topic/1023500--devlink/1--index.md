---
title: "Linux Devlink Documentation"
type: reference
description: "devlink is an API to expose device information and resources not directly related to any device class, such as chip-wide/switch-ASIC-wide configuration."
---

<a id="rst-linux-devlink-documentation"></a>

devlink is an API to expose device information and resources not directly related to any device class, such as chip-wide/switch-ASIC-wide configuration.

<a id="rst-locking"></a>

## Locking

Driver facing APIs are currently transitioning to allow more explicit locking. Drivers can use the existing `devlink_*` set of APIs, or new APIs prefixed by `devl_*`. The older APIs handle all the locking in devlink core, but don't allow registration of most sub-objects once the main devlink object is itself registered. The newer `devl_*` APIs assume the devlink instance lock is already held. Drivers can take the instance lock by calling `devl_lock()`. It is also held all callbacks of devlink netlink commands.

Drivers are encouraged to use the devlink instance lock for their own needs.

Drivers need to be cautious when taking devlink instance lock and taking RTNL lock at the same time. Devlink instance lock needs to be taken first, only after that RTNL lock could be taken.

<a id="rst-nested-instances"></a>

## Nested instances

Some objects, like linecards or port functions, could have another devlink instances created underneath. In that case, drivers should make sure to respect following rules:

> - Lock ordering should be maintained. If driver needs to take instance lock of both nested and parent instances at the same time, devlink instance lock of the parent instance should be taken first, only then instance lock of the nested instance could be taken.
>
> - Driver should use object-specific helpers to setup the nested relationship:
>
>   - `devl_nested_devlink_set()` - called to setup devlink -&gt; nested devlink relationship (could be user for multiple nested instances.
>
>   - `devl_port_fn_devlink_set()` - called to setup port function -&gt; nested devlink relationship.
>
>   - `devlink_linecard_nested_dl_set()` - called to setup linecard -&gt; nested devlink relationship.

The nested devlink info is exposed to the userspace over object-specific attributes of devlink netlink.

<a id="rst-interface-documentation"></a>

## Interface documentation

The following pages describe various interfaces available through devlink in general.

- [Devlink DPIPE](<~kernel/internals/networking/devlink/devlink-dpipe>)
- [Devlink E-Switch Attribute](<~kernel/internals/networking/devlink/devlink-eswitch-attr>)
- [Devlink Flash](<~kernel/internals/networking/devlink/devlink-flash>)
- [Devlink Health](<~kernel/internals/networking/devlink/devlink-health>)
- [Devlink Info](<~kernel/internals/networking/devlink/devlink-info>)
- [Devlink Line card](<~kernel/internals/networking/devlink/devlink-linecard>)
- [Devlink Params](<~kernel/internals/networking/devlink/devlink-params>)
- [Devlink Port](<~kernel/internals/networking/devlink/devlink-port>)
- [Devlink Region](<~kernel/internals/networking/devlink/devlink-region>)
- [Devlink Reload](<~kernel/internals/networking/devlink/devlink-reload>)
- [Devlink Resource](<~kernel/internals/networking/devlink/devlink-resource>)
- [Devlink Selftests](<~kernel/internals/networking/devlink/devlink-selftests>)
- [Devlink Trap](<~kernel/internals/networking/devlink/devlink-trap>)

<a id="rst-driver-specific-documentation"></a>

## Driver-specific documentation

Each driver that implements `devlink` is expected to document what parameters, info versions, and other features it supports.

- [am65-cpsw-nuss devlink support](<~kernel/internals/networking/devlink/am65-nuss-cpsw-switch>)
- [bnxt devlink support](<~kernel/internals/networking/devlink/bnxt>)
- [etas_es58x devlink support](<~kernel/internals/networking/devlink/etas-es58x>)
- [hns3 devlink support](<~kernel/internals/networking/devlink/hns3>)
- [i40e devlink support](<~kernel/internals/networking/devlink/i40e>)
- [ice devlink support](<~kernel/internals/networking/devlink/ice>)
- [ionic devlink support](<~kernel/internals/networking/devlink/ionic>)
- [iosm devlink support](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/networking/devlink/iosm.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>)
- [ixgbe devlink support](<~kernel/internals/networking/devlink/ixgbe>)
- [kvaser_pciefd devlink support](<~kernel/internals/networking/devlink/kvaser-pciefd>)
- [kvaser_usb devlink support](<~kernel/internals/networking/devlink/kvaser-usb>)
- [mlx4 devlink support](<~kernel/internals/networking/devlink/mlx4>)
- [mlx5 devlink support](<~kernel/internals/networking/devlink/mlx5>)
- [mlxsw devlink support](<~kernel/internals/networking/devlink/mlxsw>)
- [mv88e6xxx devlink support](<~kernel/internals/networking/devlink/mv88e6xxx>)
- [netdevsim devlink support](<~kernel/internals/networking/devlink/netdevsim>)
- [nfp devlink support](<~kernel/internals/networking/devlink/nfp>)
- [octeontx2 devlink support](<~kernel/internals/networking/devlink/octeontx2>)
- [prestera devlink support](<~kernel/internals/networking/devlink/prestera>)
- [qed devlink support](<~kernel/internals/networking/devlink/qed>)
- [sfc devlink support](<~kernel/internals/networking/devlink/sfc>)
- [stmmac (synopsys dwmac) devlink support](<~kernel/internals/networking/devlink/stmmac>)
- [ti-cpsw-switch devlink support](<~kernel/internals/networking/devlink/ti-cpsw-switch>)
- [zl3073x devlink support](<~kernel/internals/networking/devlink/zl3073x>)
