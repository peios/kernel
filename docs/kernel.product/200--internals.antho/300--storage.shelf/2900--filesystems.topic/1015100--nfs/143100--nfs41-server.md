---
title: "NFSv4.1 Server Implementation"
type: reference
description: "Server support for minorversion 1 can be controlled using the /proc/fs/nfsd/versions control file. The string output returned by reading this file will contain either \"+4.1\" or \"-4.1\" correspondingly."
---

<a id="rst-nfsv4-1-server-implementation"></a>

Server support for minorversion 1 can be controlled using the /proc/fs/nfsd/versions control file.  The string output returned by reading this file will contain either "+4.1" or "-4.1" correspondingly.

Currently, server support for minorversion 1 is enabled by default. It can be disabled at run time by writing the string "-4.1" to the /proc/fs/nfsd/versions control file.  Note that to write this control file, the nfsd service must be taken down.  You can use rpc.nfsd for this; see rpc.nfsd(8).

(Warning: older servers will interpret "+4.1" and "-4.1" as "+4" and "-4", respectively.  Therefore, code meant to work on both new and old kernels must turn 4.1 on or off *before* turning support for version 4 on or off; rpc.nfsd does this correctly.)

The NFSv4 minorversion 1 (NFSv4.1) implementation in nfsd is based on RFC 5661.

From the many new features in NFSv4.1 the current implementation focuses on the mandatory-to-implement NFSv4.1 Sessions, providing "exactly once" semantics and better control and throttling of the resources allocated for each client.

The table below, taken from the NFSv4.1 document, lists the operations that are mandatory to implement (REQ), optional (OPT), and NFSv4.0 operations that are required not to implement (MNI) in minor version 1.  The first column indicates the operations that are not supported yet by the linux server implementation.

The OPTIONAL features identified and their abbreviations are as follows:

- **pNFS**      Parallel NFS

- **FDELG**     File Delegations

- **DDELG**     Directory Delegations

The following abbreviations indicate the linux server implementation status.

- **I** Implemented NFSv4.1 operations.

- **NS**        Not Supported.

- **NS\***      Unimplemented optional feature.

<a id="rst-operations"></a>

## Operations


<table>
<thead>
<tr>
<th>


Implementation status

</th>
<th>


Operation

</th>
<th>


REQ,REC, OPT or NMI

</th>
<th>


Feature (REQ, REC or OPT)

</th>
<th>


Definition

</th>
</tr>
</thead>
<tbody>
<tr>
<td>




</td>
<td>


ACCESS

</td>
<td>


REQ

</td>
<td>




</td>
<td>


Section 18.1

</td>
</tr>
<tr>
<td>


I

</td>
<td>


BACKCHANNEL_CTL

</td>
<td>


REQ

</td>
<td>




</td>
<td>


Section 18.33

</td>
</tr>
<tr>
<td>


I

</td>
<td>


BIND_CONN_TO_SESSION

</td>
<td>


REQ

</td>
<td>




</td>
<td>


Section 18.34

</td>
</tr>
<tr>
<td>




</td>
<td>


CLOSE

</td>
<td>


REQ

</td>
<td>




</td>
<td>


Section 18.2

</td>
</tr>
<tr>
<td>




</td>
<td>


COMMIT

</td>
<td>


REQ

</td>
<td>




</td>
<td>


Section 18.3

</td>
</tr>
<tr>
<td>




</td>
<td>


CREATE

</td>
<td>


REQ

</td>
<td>




</td>
<td>


Section 18.4

</td>
</tr>
<tr>
<td>


I

</td>
<td>


CREATE_SESSION

</td>
<td>


REQ

</td>
<td>




</td>
<td>


Section 18.36

</td>
</tr>
<tr>
<td>


NS\*

</td>
<td>


DELEGPURGE

</td>
<td>


OPT

</td>
<td>


FDELG (REQ)

</td>
<td>


Section 18.5

</td>
</tr>
<tr>
<td>




</td>
<td>


DELEGRETURN

</td>
<td>


OPT

</td>
<td>


FDELG,

</td>
<td>


Section 18.6

</td>
</tr>
<tr>
<td>




</td>
<td>




</td>
<td>




</td>
<td>


DDELG, pNFS

</td>
<td>




</td>
</tr>
<tr>
<td>




</td>
<td>




</td>
<td>




</td>
<td>


(REQ)

</td>
<td>




</td>
</tr>
<tr>
<td>


I

</td>
<td>


DESTROY_CLIENTID

</td>
<td>


REQ

</td>
<td>




</td>
<td>


Section 18.50

</td>
</tr>
<tr>
<td>


I

</td>
<td>


DESTROY_SESSION

</td>
<td>


REQ

</td>
<td>




</td>
<td>


Section 18.37

</td>
</tr>
<tr>
<td>


I

</td>
<td>


EXCHANGE_ID

</td>
<td>


REQ

</td>
<td>




</td>
<td>


Section 18.35

</td>
</tr>
<tr>
<td>


I

</td>
<td>


FREE_STATEID

</td>
<td>


REQ

</td>
<td>




</td>
<td>


Section 18.38

</td>
</tr>
<tr>
<td>




</td>
<td>


GETATTR

</td>
<td>


REQ

</td>
<td>




</td>
<td>


Section 18.7

</td>
</tr>
<tr>
<td>


I

</td>
<td>


GETDEVICEINFO

</td>
<td>


OPT

</td>
<td>


pNFS (REQ)

</td>
<td>


Section 18.40

</td>
</tr>
<tr>
<td>


NS\*

</td>
<td>


GETDEVICELIST

</td>
<td>


OPT

</td>
<td>


pNFS (OPT)

</td>
<td>


Section 18.41

</td>
</tr>
<tr>
<td>




</td>
<td>


GETFH

</td>
<td>


REQ

</td>
<td>




</td>
<td>


Section 18.8

</td>
</tr>
<tr>
<td>


NS\*

</td>
<td>


GET_DIR_DELEGATION

</td>
<td>


OPT

</td>
<td>


DDELG (REQ)

</td>
<td>


Section 18.39

</td>
</tr>
<tr>
<td>


I

</td>
<td>


LAYOUTCOMMIT

</td>
<td>


OPT

</td>
<td>


pNFS (REQ)

</td>
<td>


Section 18.42

</td>
</tr>
<tr>
<td>


I

</td>
<td>


LAYOUTGET

</td>
<td>


OPT

</td>
<td>


pNFS (REQ)

</td>
<td>


Section 18.43

</td>
</tr>
<tr>
<td>


I

</td>
<td>


LAYOUTRETURN

</td>
<td>


OPT

</td>
<td>


pNFS (REQ)

</td>
<td>


Section 18.44

</td>
</tr>
<tr>
<td>




</td>
<td>


LINK

</td>
<td>


OPT

</td>
<td>




</td>
<td>


Section 18.9

</td>
</tr>
<tr>
<td>




</td>
<td>


LOCK

</td>
<td>


REQ

</td>
<td>




</td>
<td>


Section 18.10

</td>
</tr>
<tr>
<td>




</td>
<td>


LOCKT

</td>
<td>


REQ

</td>
<td>




</td>
<td>


Section 18.11

</td>
</tr>
<tr>
<td>




</td>
<td>


LOCKU

</td>
<td>


REQ

</td>
<td>




</td>
<td>


Section 18.12

</td>
</tr>
<tr>
<td>




</td>
<td>


LOOKUP

</td>
<td>


REQ

</td>
<td>




</td>
<td>


Section 18.13

</td>
</tr>
<tr>
<td>




</td>
<td>


LOOKUPP

</td>
<td>


REQ

</td>
<td>




</td>
<td>


Section 18.14

</td>
</tr>
<tr>
<td>




</td>
<td>


NVERIFY

</td>
<td>


REQ

</td>
<td>




</td>
<td>


Section 18.15

</td>
</tr>
<tr>
<td>




</td>
<td>


OPEN

</td>
<td>


REQ

</td>
<td>




</td>
<td>


Section 18.16

</td>
</tr>
<tr>
<td>


NS\*

</td>
<td>


OPENATTR

</td>
<td>


OPT

</td>
<td>




</td>
<td>


Section 18.17

</td>
</tr>
<tr>
<td>




</td>
<td>


OPEN_CONFIRM

</td>
<td>


MNI

</td>
<td>




</td>
<td>


N/A

</td>
</tr>
<tr>
<td>




</td>
<td>


OPEN_DOWNGRADE

</td>
<td>


REQ

</td>
<td>




</td>
<td>


Section 18.18

</td>
</tr>
<tr>
<td>




</td>
<td>


PUTFH

</td>
<td>


REQ

</td>
<td>




</td>
<td>


Section 18.19

</td>
</tr>
<tr>
<td>




</td>
<td>


PUTPUBFH

</td>
<td>


REQ

</td>
<td>




</td>
<td>


Section 18.20

</td>
</tr>
<tr>
<td>




</td>
<td>


PUTROOTFH

</td>
<td>


REQ

</td>
<td>




</td>
<td>


Section 18.21

</td>
</tr>
<tr>
<td>




</td>
<td>


READ

</td>
<td>


REQ

</td>
<td>




</td>
<td>


Section 18.22

</td>
</tr>
<tr>
<td>




</td>
<td>


READDIR

</td>
<td>


REQ

</td>
<td>




</td>
<td>


Section 18.23

</td>
</tr>
<tr>
<td>




</td>
<td>


READLINK

</td>
<td>


OPT

</td>
<td>




</td>
<td>


Section 18.24

</td>
</tr>
<tr>
<td>




</td>
<td>


RECLAIM_COMPLETE

</td>
<td>


REQ

</td>
<td>




</td>
<td>


Section 18.51

</td>
</tr>
<tr>
<td>




</td>
<td>


RELEASE_LOCKOWNER

</td>
<td>


MNI

</td>
<td>




</td>
<td>


N/A

</td>
</tr>
<tr>
<td>




</td>
<td>


REMOVE

</td>
<td>


REQ

</td>
<td>




</td>
<td>


Section 18.25

</td>
</tr>
<tr>
<td>




</td>
<td>


RENAME

</td>
<td>


REQ

</td>
<td>




</td>
<td>


Section 18.26

</td>
</tr>
<tr>
<td>




</td>
<td>


RENEW

</td>
<td>


MNI

</td>
<td>




</td>
<td>


N/A

</td>
</tr>
<tr>
<td>




</td>
<td>


RESTOREFH

</td>
<td>


REQ

</td>
<td>




</td>
<td>


Section 18.27

</td>
</tr>
<tr>
<td>




</td>
<td>


SAVEFH

</td>
<td>


REQ

</td>
<td>




</td>
<td>


Section 18.28

</td>
</tr>
<tr>
<td>




</td>
<td>


SECINFO

</td>
<td>


REQ

</td>
<td>




</td>
<td>


Section 18.29

</td>
</tr>
<tr>
<td>


I

</td>
<td>


SECINFO_NO_NAME

</td>
<td>


REC

</td>
<td>


pNFS files

</td>
<td>


Section 18.45,

</td>
</tr>
<tr>
<td>




</td>
<td>




</td>
<td>




</td>
<td>


layout (REQ)

</td>
<td>


Section 13.12

</td>
</tr>
<tr>
<td>


I

</td>
<td>


SEQUENCE

</td>
<td>


REQ

</td>
<td>




</td>
<td>


Section 18.46

</td>
</tr>
<tr>
<td>




</td>
<td>


SETATTR

</td>
<td>


REQ

</td>
<td>




</td>
<td>


Section 18.30

</td>
</tr>
<tr>
<td>




</td>
<td>


SETCLIENTID

</td>
<td>


MNI

</td>
<td>




</td>
<td>


N/A

</td>
</tr>
<tr>
<td>




</td>
<td>


SETCLIENTID_CONFIRM

</td>
<td>


MNI

</td>
<td>




</td>
<td>


N/A

</td>
</tr>
<tr>
<td>


NS

</td>
<td>


SET_SSV

</td>
<td>


REQ

</td>
<td>




</td>
<td>


Section 18.47

</td>
</tr>
<tr>
<td>


I

</td>
<td>


TEST_STATEID

</td>
<td>


REQ

</td>
<td>




</td>
<td>


Section 18.48

</td>
</tr>
<tr>
<td>




</td>
<td>


VERIFY

</td>
<td>


REQ

</td>
<td>




</td>
<td>


Section 18.31

</td>
</tr>
<tr>
<td>


NS\*

</td>
<td>


WANT_DELEGATION

</td>
<td>


OPT

</td>
<td>


FDELG (OPT)

</td>
<td>


Section 18.49

</td>
</tr>
<tr>
<td>




</td>
<td>


WRITE

</td>
<td>


REQ

</td>
<td>




</td>
<td>


Section 18.32

</td>
</tr>
</tbody>
</table>

<a id="rst-callback-operations"></a>

## Callback Operations


<table>
<thead>
<tr>
<th>


Implementation status

</th>
<th>


Operation

</th>
<th>


REQ,REC, OPT or NMI

</th>
<th>


Feature (REQ, REC or OPT)

</th>
<th>


Definition

</th>
</tr>
</thead>
<tbody>
<tr>
<td>




</td>
<td>


CB_GETATTR

</td>
<td>


OPT

</td>
<td>


FDELG (REQ)

</td>
<td>


Section 20.1

</td>
</tr>
<tr>
<td>


I

</td>
<td>


CB_LAYOUTRECALL

</td>
<td>


OPT

</td>
<td>


pNFS (REQ)

</td>
<td>


Section 20.3

</td>
</tr>
<tr>
<td>


NS\*

</td>
<td>


CB_NOTIFY

</td>
<td>


OPT

</td>
<td>


DDELG (REQ)

</td>
<td>


Section 20.4

</td>
</tr>
<tr>
<td>


NS\*

</td>
<td>


CB_NOTIFY_DEVICEID

</td>
<td>


OPT

</td>
<td>


pNFS (OPT)

</td>
<td>


Section 20.12

</td>
</tr>
<tr>
<td>


NS\*

</td>
<td>


CB_NOTIFY_LOCK

</td>
<td>


OPT

</td>
<td>




</td>
<td>


Section 20.11

</td>
</tr>
<tr>
<td>


NS\*

</td>
<td>


CB_PUSH_DELEG

</td>
<td>


OPT

</td>
<td>


FDELG (OPT)

</td>
<td>


Section 20.5

</td>
</tr>
<tr>
<td>




</td>
<td>


CB_RECALL

</td>
<td>


OPT

</td>
<td>


FDELG,

</td>
<td>


Section 20.2

</td>
</tr>
<tr>
<td>




</td>
<td>




</td>
<td>




</td>
<td>


DDELG, pNFS

</td>
<td>




</td>
</tr>
<tr>
<td>




</td>
<td>




</td>
<td>




</td>
<td>


(REQ)

</td>
<td>




</td>
</tr>
<tr>
<td>


NS\*

</td>
<td>


CB_RECALL_ANY

</td>
<td>


OPT

</td>
<td>


FDELG,

</td>
<td>


Section 20.6

</td>
</tr>
<tr>
<td>




</td>
<td>




</td>
<td>




</td>
<td>


DDELG, pNFS

</td>
<td>




</td>
</tr>
<tr>
<td>




</td>
<td>




</td>
<td>




</td>
<td>


(REQ)

</td>
<td>




</td>
</tr>
<tr>
<td>


NS

</td>
<td>


CB_RECALL_SLOT

</td>
<td>


REQ

</td>
<td>




</td>
<td>


Section 20.8

</td>
</tr>
<tr>
<td>


NS\*

</td>
<td>


CB_RECALLABLE_OBJ_AVAIL

</td>
<td>


OPT

</td>
<td>


DDELG, pNFS

</td>
<td>


Section 20.7

</td>
</tr>
<tr>
<td>




</td>
<td>




</td>
<td>




</td>
<td>


(REQ)

</td>
<td>




</td>
</tr>
<tr>
<td>


I

</td>
<td>


CB_SEQUENCE

</td>
<td>


OPT

</td>
<td>


FDELG,

</td>
<td>


Section 20.9

</td>
</tr>
<tr>
<td>




</td>
<td>




</td>
<td>




</td>
<td>


DDELG, pNFS

</td>
<td>




</td>
</tr>
<tr>
<td>




</td>
<td>




</td>
<td>




</td>
<td>


(REQ)

</td>
<td>




</td>
</tr>
<tr>
<td>


NS\*

</td>
<td>


CB_WANTS_CANCELLED

</td>
<td>


OPT

</td>
<td>


FDELG,

</td>
<td>


Section 20.10

</td>
</tr>
<tr>
<td>




</td>
<td>




</td>
<td>




</td>
<td>


DDELG, pNFS

</td>
<td>




</td>
</tr>
<tr>
<td>




</td>
<td>




</td>
<td>




</td>
<td>


(REQ)

</td>
<td>




</td>
</tr>
</tbody>
</table>

<a id="rst-implementation-notes"></a>

## Implementation notes:

- **SSV:**

  The spec claims this is mandatory, but we don't actually know of any implementations, so we're ignoring it for now.  The server returns NFS4ERR_ENCR_ALG_UNSUPP on EXCHANGE_ID, which should be future-proof.

- **GSS on the backchannel:**

  Again, theoretically required but not widely implemented (in particular, the current Linux client doesn't request it).  We return NFS4ERR_ENCR_ALG_UNSUPP on CREATE_SESSION.

- **DELEGPURGE:**

  mandatory only for servers that support CLAIM_DELEGATE_PREV and/or CLAIM_DELEG_PREV_FH (which allows clients to keep delegations that persist across client reboots).  Thus we need not implement this for now.

- **EXCHANGE_ID:**

  implementation ids are ignored

- **CREATE_SESSION:**

  backchannel attributes are ignored

- **SEQUENCE:**

  no support for dynamic slot table renegotiation (optional)

- **Nonstandard compound limitations:**

  No support for a sessions fore channel RPC compound that requires both a ca_maxrequestsize request and a ca_maxresponsesize reply, so we may fail to live up to the promise we made in CREATE_SESSION fore channel negotiation.

See also [http://wiki.linux-nfs.org/wiki/index.php/Server_4.0_and_4.1_issues](<http://wiki.linux-nfs.org/wiki/index.php/Server_4.0_and_4.1_issues>).
