---
title: "InfiniBand and Remote DMA (RDMA) Interfaces"
type: reference
description: "TBD"
---

<a id="rst-infiniband-and-remote-dma-rdma-interfaces"></a>

<a id="rst-introduction-and-overview"></a>

## Introduction and Overview

TBD

<a id="rst-infiniband-core-interfaces"></a>

## InfiniBand core interfaces

```{kernel-doc} drivers/infiniband/core/iwpm_util.h
:internal:
```

```{kernel-doc} drivers/infiniband/core/cq.c
:export:
```

```{kernel-doc} drivers/infiniband/core/cm.c
:export:
```

```{kernel-doc} drivers/infiniband/core/rw.c
:export:
```

```{kernel-doc} drivers/infiniband/core/device.c
:export:
```

```{kernel-doc} drivers/infiniband/core/verbs.c
:export:
```

```{kernel-doc} drivers/infiniband/core/packer.c
:export:
```

```{kernel-doc} drivers/infiniband/core/sa_query.c
:export:
```

```{kernel-doc} drivers/infiniband/core/ud_header.c
:export:
```

```{kernel-doc} drivers/infiniband/core/umem.c
:export:
```

```{kernel-doc} drivers/infiniband/core/umem_odp.c
:export:
```

<a id="rst-rdma-verbs-transport-library"></a>

## RDMA Verbs transport library

```{kernel-doc} drivers/infiniband/sw/rdmavt/mr.c
:export:
```

```{kernel-doc} drivers/infiniband/sw/rdmavt/rc.c
:export:
```

```{kernel-doc} drivers/infiniband/sw/rdmavt/ah.c
:export:
```

```{kernel-doc} drivers/infiniband/sw/rdmavt/vt.c
:export:
```

```{kernel-doc} drivers/infiniband/sw/rdmavt/cq.c
:export:
```

```{kernel-doc} drivers/infiniband/sw/rdmavt/qp.c
:export:
```

```{kernel-doc} drivers/infiniband/sw/rdmavt/mcast.c
:export:
```

<a id="rst-upper-layer-protocols"></a>

## Upper Layer Protocols

<a id="rst-iscsi-extensions-for-rdma-iser"></a>

### iSCSI Extensions for RDMA (iSER)

```{kernel-doc} drivers/infiniband/ulp/iser/iscsi_iser.h
:internal:
```

```{kernel-doc} drivers/infiniband/ulp/iser/iscsi_iser.c
:functions: iscsi_iser_pdu_alloc iser_initialize_task_headers iscsi_iser_task_init iscsi_iser_mtask_xmit iscsi_iser_task_xmit iscsi_iser_cleanup_task iscsi_iser_check_protection iscsi_iser_conn_create iscsi_iser_conn_bind iscsi_iser_conn_start iscsi_iser_conn_stop iscsi_iser_session_destroy iscsi_iser_session_create iscsi_iser_set_param iscsi_iser_ep_connect iscsi_iser_ep_poll iscsi_iser_ep_disconnect
```

```{kernel-doc} drivers/infiniband/ulp/iser/iser_initiator.c
:internal:
```

```{kernel-doc} drivers/infiniband/ulp/iser/iser_verbs.c
:internal:
```

<a id="rst-omni-path-opa-virtual-nic-support"></a>

### Omni-Path (OPA) Virtual NIC support

```{kernel-doc} drivers/infiniband/ulp/opa_vnic/opa_vnic_internal.h
:internal:
```

```{kernel-doc} drivers/infiniband/ulp/opa_vnic/opa_vnic_encap.h
:internal:
```

```{kernel-doc} drivers/infiniband/ulp/opa_vnic/opa_vnic_vema_iface.c
:internal:
```

```{kernel-doc} drivers/infiniband/ulp/opa_vnic/opa_vnic_vema.c
:internal:
```

<a id="rst-infiniband-scsi-rdma-protocol-target-support"></a>

### InfiniBand SCSI RDMA protocol target support

```{kernel-doc} drivers/infiniband/ulp/srpt/ib_srpt.h
:internal:
```

```{kernel-doc} drivers/infiniband/ulp/srpt/ib_srpt.c
:internal:
```

<a id="rst-iscsi-extensions-for-rdma-iser-target-support"></a>

### iSCSI Extensions for RDMA (iSER) target support

```{kernel-doc} drivers/infiniband/ulp/isert/ib_isert.c
:internal:
```
