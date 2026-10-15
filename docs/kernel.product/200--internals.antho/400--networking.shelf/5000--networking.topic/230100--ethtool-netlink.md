---
title: "Netlink interface for ethtool"
type: reference
description: "Netlink interface for ethtool uses generic netlink family ethtool (userspace application should use macros ETHTOOL_GENL_NAME and ETHTOOL_GENL_VERSION defined in <linux/ethtool_netlink.h> uapi header). This family does not use a specific…"
---

> **Peios:** Linux capability names in this interface retain their API meaning, but KACS evaluates them through native token privileges or compatibility rules. UID 0, `setcap` and Unix mode bits do not independently grant native authority. Object access and PIP checks remain additional constraints where applicable. See [Peios kernel behaviour](<~kernel/introduction/peios-behaviour>) for the mapping and exceptions.


<a id="rst-netlink-interface-for-ethtool"></a>

<a id="rst-basic-information"></a>

## Basic information

Netlink interface for ethtool uses generic netlink family `ethtool` (userspace application should use macros `ETHTOOL_GENL_NAME` and `ETHTOOL_GENL_VERSION` defined in `<linux/ethtool_netlink.h>` uapi header). This family does not use a specific header, all information in requests and replies is passed using netlink attributes.

The ethtool netlink interface uses extended ACK for error and warning reporting, userspace application developers are encouraged to make these messages available to user in a suitable way.

Requests can be divided into three categories: "get" (retrieving information), "set" (setting parameters) and "action" (invoking an action).

All "set" and "action" type requests require admin privileges (`CAP_NET_ADMIN` in the namespace). Most "get" type requests are allowed for anyone but there are exceptions (where the response contains sensitive information). In some cases, the request as such is allowed for anyone but unprivileged users have attributes with sensitive information (e.g. wake-on-lan password) omitted.

<a id="rst-conventions"></a>

## Conventions

Attributes which represent a boolean value usually use NLA_U8 type so that we can distinguish three states: "on", "off" and "not present" (meaning the information is not available in "get" requests or value is not to be changed in "set" requests). For these attributes, the "true" value should be passed as number 1 but any non-zero value should be understood as "true" by recipient. In the tables below, "bool" denotes NLA_U8 attributes interpreted in this way.

In the message structure descriptions below, if an attribute name is suffixed with "+", parent nest can contain multiple attributes of the same type. This implements an array of entries.

Attributes that need to be filled-in by device drivers and that are dumped to user space based on whether they are valid or not should not use zero as a valid value. This avoids the need to explicitly signal the validity of the attribute in the device driver API.

<a id="rst-request-header"></a>

## Request header

Each request or reply message contains a nested attribute with common header. Structure of this header is

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_HEADER_DEV_INDEX`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> device ifindex
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_HEADER_DEV_NAME`
>
> </td>
> <td>
>
>
> string
>
> </td>
> <td>
>
>
> device name
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_HEADER_FLAGS`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> flags common for all requests
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_HEADER_PHY_INDEX`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> phy device index
>
> </td>
> </tr>
> </tbody>
> </table>

`ETHTOOL_A_HEADER_DEV_INDEX` and `ETHTOOL_A_HEADER_DEV_NAME` identify the device message relates to. One of them is sufficient in requests, if both are used, they must identify the same device. Some requests, e.g. global string sets, do not require device identification. Most `GET` requests also allow dump requests without device identification to query the same information for all devices providing it (each device in a separate message).

`ETHTOOL_A_HEADER_FLAGS` is a bitmap of request flags common for all request types. The interpretation of these flags is the same for all request types but the flags may not apply to requests. Recognized flags are:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_FLAG_COMPACT_BITSETS`
>
> </td>
> <td>
>
>
> use compact format bitsets in reply
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_FLAG_OMIT_REPLY`
>
> </td>
> <td>
>
>
> omit optional reply (\_SET and \_ACT)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_FLAG_STATS`
>
> </td>
> <td>
>
>
> include optional device statistics
>
> </td>
> </tr>
> </tbody>
> </table>

New request flags should follow the general idea that if the flag is not set, the behaviour is backward compatible, i.e. requests from old clients not aware of the flag should be interpreted the way the client expects. A client must not set flags it does not understand.

`ETHTOOL_A_HEADER_PHY_INDEX` identifies the Ethernet PHY the message relates to. As there are numerous commands that are related to PHY configuration, and because there may be more than one PHY on the link, the PHY index can be passed in the request for the commands that needs it. It is, however, not mandatory, and if it is not passed for commands that target a PHY, the net_device.phydev pointer is used.

<a id="rst-bit-sets"></a>

## Bit sets

For short bitmaps of (reasonably) fixed length, standard `NLA_BITFIELD32` type is used. For arbitrary length bitmaps, ethtool netlink uses a nested attribute with contents of one of two forms: compact (two binary bitmaps representing bit values and mask of affected bits) and bit-by-bit (list of bits identified by either index or name).

Verbose (bit-by-bit) bitsets allow sending symbolic names for bits together with their values which saves a round trip (when the bitset is passed in a request) or at least a second request (when the bitset is in a reply). This is useful for one shot applications like traditional ethtool command. On the other hand, long running applications like ethtool monitor (displaying notifications) or network management daemons may prefer fetching the names only once and using compact form to save message size. Notifications from ethtool netlink interface always use compact form for bitsets.

A bitset can represent either a value/mask pair (`ETHTOOL_A_BITSET_NOMASK` not set) or a single bitmap (`ETHTOOL_A_BITSET_NOMASK` set). In requests modifying a bitmap, the former changes the bit set in mask to values set in value and preserves the rest; the latter sets the bits set in the bitmap and clears the rest.

Compact form: nested (bitset) attribute contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_BITSET_NOMASK`
>
> </td>
> <td>
>
>
> flag
>
> </td>
> <td>
>
>
> no mask, only a list
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_BITSET_SIZE`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> number of significant bits
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_BITSET_VALUE`
>
> </td>
> <td>
>
>
> binary
>
> </td>
> <td>
>
>
> bitmap of bit values
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_BITSET_MASK`
>
> </td>
> <td>
>
>
> binary
>
> </td>
> <td>
>
>
> bitmap of valid bits
>
> </td>
> </tr>
> </tbody>
> </table>

Value and mask must have length at least `ETHTOOL_A_BITSET_SIZE` bits rounded up to a multiple of 32 bits. They consist of 32-bit words in host byte order, words ordered from least significant to most significant (i.e. the same way as bitmaps are passed with ioctl interface).

For compact form, `ETHTOOL_A_BITSET_SIZE` and `ETHTOOL_A_BITSET_VALUE` are mandatory. `ETHTOOL_A_BITSET_MASK` attribute is mandatory if `ETHTOOL_A_BITSET_NOMASK` is not set (bitset represents a value/mask pair); if `ETHTOOL_A_BITSET_NOMASK` is not set, `ETHTOOL_A_BITSET_MASK` is not allowed (bitset represents a single bitmap.

Kernel bit set length may differ from userspace length if older application is used on newer kernel or vice versa. If userspace bitmap is longer, an error is issued only if the request actually tries to set values of some bits not recognized by kernel.

Bit-by-bit form: nested (bitset) attribute contents:

>
> <table>
> <tbody>
> <tr>
> <td colspan="3">
>
>
> `ETHTOOL_A_BITSET_NOMASK`
>
> </td>
> <td>
>
>
> flag
>
> </td>
> <td>
>
>
> no mask, only a list
>
> </td>
> </tr>
> <tr>
> <td colspan="3">
>
>
> `ETHTOOL_A_BITSET_SIZE`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> number of significant bits
>
> </td>
> </tr>
> <tr>
> <td colspan="3">
>
>
> `ETHTOOL_A_BITSET_BITS`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> array of bits
>
> </td>
> </tr>
> <tr>
> <td>
>
>
>
>
> </td>
> <td colspan="2">
>
>
> `ETHTOOL_A_BITSET_BITS_BIT+`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> one bit
>
> </td>
> </tr>
> <tr>
> <td>
>
>
>
>
> </td>
> <td>
>
>
>
>
> </td>
> <td>
>
>
> `ETHTOOL_A_BITSET_BIT_INDEX`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> bit index (0 for LSB)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
>
>
> </td>
> <td>
>
>
>
>
> </td>
> <td>
>
>
> `ETHTOOL_A_BITSET_BIT_NAME`
>
> </td>
> <td>
>
>
> string
>
> </td>
> <td>
>
>
> bit name
>
> </td>
> </tr>
> <tr>
> <td>
>
>
>
>
> </td>
> <td>
>
>
>
>
> </td>
> <td>
>
>
> `ETHTOOL_A_BITSET_BIT_VALUE`
>
> </td>
> <td>
>
>
> flag
>
> </td>
> <td>
>
>
> present if bit is set
>
> </td>
> </tr>
> </tbody>
> </table>

Bit size is optional for bit-by-bit form. `ETHTOOL_A_BITSET_BITS` nest can only contain `ETHTOOL_A_BITSET_BITS_BIT` attributes but there can be an arbitrary number of them.  A bit may be identified by its index or by its name. When used in requests, listed bits are set to 0 or 1 according to `ETHTOOL_A_BITSET_BIT_VALUE`, the rest is preserved. A request fails if index exceeds kernel bit length or if name is not recognized.

When `ETHTOOL_A_BITSET_NOMASK` flag is present, bitset is interpreted as a simple bitmap. `ETHTOOL_A_BITSET_BIT_VALUE` attributes are not used in such case. Such bitset represents a bitmap with listed bits set and the rest zero.

In requests, application can use either form. Form used by kernel in reply is determined by `ETHTOOL_FLAG_COMPACT_BITSETS` flag in flags field of request header. Semantics of value and mask depends on the attribute.

<a id="rst-list-of-message-types"></a>

## List of message types

All constants identifying message types use `ETHTOOL_CMD_` prefix and suffix according to message purpose:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `_GET`
>
> </td>
> <td>
>
>
> userspace request to retrieve data
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `_SET`
>
> </td>
> <td>
>
>
> userspace request to set data
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `_ACT`
>
> </td>
> <td>
>
>
> userspace request to perform an action
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `_GET_REPLY`
>
> </td>
> <td>
>
>
> kernel reply to a `GET` request
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `_SET_REPLY`
>
> </td>
> <td>
>
>
> kernel reply to a `SET` request
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `_ACT_REPLY`
>
> </td>
> <td>
>
>
> kernel reply to an `ACT` request
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `_NTF`
>
> </td>
> <td>
>
>
> kernel notification
>
> </td>
> </tr>
> </tbody>
> </table>

Userspace to kernel:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_STRSET_GET`
>
> </td>
> <td>
>
>
> get string set
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_LINKINFO_GET`
>
> </td>
> <td>
>
>
> get link settings
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_LINKINFO_SET`
>
> </td>
> <td>
>
>
> set link settings
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_LINKMODES_GET`
>
> </td>
> <td>
>
>
> get link modes info
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_LINKMODES_SET`
>
> </td>
> <td>
>
>
> set link modes info
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_LINKSTATE_GET`
>
> </td>
> <td>
>
>
> get link state
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_DEBUG_GET`
>
> </td>
> <td>
>
>
> get debugging settings
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_DEBUG_SET`
>
> </td>
> <td>
>
>
> set debugging settings
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_WOL_GET`
>
> </td>
> <td>
>
>
> get wake-on-lan settings
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_WOL_SET`
>
> </td>
> <td>
>
>
> set wake-on-lan settings
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_FEATURES_GET`
>
> </td>
> <td>
>
>
> get device features
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_FEATURES_SET`
>
> </td>
> <td>
>
>
> set device features
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_PRIVFLAGS_GET`
>
> </td>
> <td>
>
>
> get private flags
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_PRIVFLAGS_SET`
>
> </td>
> <td>
>
>
> set private flags
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_RINGS_GET`
>
> </td>
> <td>
>
>
> get ring sizes
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_RINGS_SET`
>
> </td>
> <td>
>
>
> set ring sizes
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_CHANNELS_GET`
>
> </td>
> <td>
>
>
> get channel counts
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_CHANNELS_SET`
>
> </td>
> <td>
>
>
> set channel counts
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_COALESCE_GET`
>
> </td>
> <td>
>
>
> get coalescing parameters
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_COALESCE_SET`
>
> </td>
> <td>
>
>
> set coalescing parameters
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_PAUSE_GET`
>
> </td>
> <td>
>
>
> get pause parameters
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_PAUSE_SET`
>
> </td>
> <td>
>
>
> set pause parameters
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_EEE_GET`
>
> </td>
> <td>
>
>
> get EEE settings
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_EEE_SET`
>
> </td>
> <td>
>
>
> set EEE settings
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_TSINFO_GET`
>
> </td>
> <td>
>
>
> get timestamping info
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_CABLE_TEST_ACT`
>
> </td>
> <td>
>
>
> action start cable test
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_CABLE_TEST_TDR_ACT`
>
> </td>
> <td>
>
>
> action start raw TDR cable test
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_TUNNEL_INFO_GET`
>
> </td>
> <td>
>
>
> get tunnel offload info
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_FEC_GET`
>
> </td>
> <td>
>
>
> get FEC settings
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_FEC_SET`
>
> </td>
> <td>
>
>
> set FEC settings
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_MODULE_EEPROM_GET`
>
> </td>
> <td>
>
>
> read SFP module EEPROM
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_STATS_GET`
>
> </td>
> <td>
>
>
> get standard statistics
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_PHC_VCLOCKS_GET`
>
> </td>
> <td>
>
>
> get PHC virtual clocks info
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_MODULE_SET`
>
> </td>
> <td>
>
>
> set transceiver module parameters
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_MODULE_GET`
>
> </td>
> <td>
>
>
> get transceiver module parameters
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_PSE_SET`
>
> </td>
> <td>
>
>
> set PSE parameters
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_PSE_GET`
>
> </td>
> <td>
>
>
> get PSE parameters
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_RSS_GET`
>
> </td>
> <td>
>
>
> get RSS settings
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_PLCA_GET_CFG`
>
> </td>
> <td>
>
>
> get PLCA RS parameters
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_PLCA_SET_CFG`
>
> </td>
> <td>
>
>
> set PLCA RS parameters
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_PLCA_GET_STATUS`
>
> </td>
> <td>
>
>
> get PLCA RS status
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_MM_GET`
>
> </td>
> <td>
>
>
> get MAC merge layer state
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_MM_SET`
>
> </td>
> <td>
>
>
> set MAC merge layer parameters
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_MODULE_FW_FLASH_ACT`
>
> </td>
> <td>
>
>
> flash transceiver module firmware
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_PHY_GET`
>
> </td>
> <td>
>
>
> get Ethernet PHY information
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_TSCONFIG_GET`
>
> </td>
> <td>
>
>
> get hw timestamping configuration
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_TSCONFIG_SET`
>
> </td>
> <td>
>
>
> set hw timestamping configuration
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_RSS_SET`
>
> </td>
> <td>
>
>
> set RSS settings
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_RSS_CREATE_ACT`
>
> </td>
> <td>
>
>
> create an additional RSS context
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_RSS_DELETE_ACT`
>
> </td>
> <td>
>
>
> delete an additional RSS context
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_MSE_GET`
>
> </td>
> <td>
>
>
> get MSE diagnostic data
>
> </td>
> </tr>
> </tbody>
> </table>

Kernel to userspace:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_STRSET_GET_REPLY`
>
> </td>
> <td>
>
>
> string set contents
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_LINKINFO_GET_REPLY`
>
> </td>
> <td>
>
>
> link settings
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_LINKINFO_NTF`
>
> </td>
> <td>
>
>
> link settings notification
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_LINKMODES_GET_REPLY`
>
> </td>
> <td>
>
>
> link modes info
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_LINKMODES_NTF`
>
> </td>
> <td>
>
>
> link modes notification
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_LINKSTATE_GET_REPLY`
>
> </td>
> <td>
>
>
> link state info
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_DEBUG_GET_REPLY`
>
> </td>
> <td>
>
>
> debugging settings
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_DEBUG_NTF`
>
> </td>
> <td>
>
>
> debugging settings notification
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_WOL_GET_REPLY`
>
> </td>
> <td>
>
>
> wake-on-lan settings
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_WOL_NTF`
>
> </td>
> <td>
>
>
> wake-on-lan settings notification
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_FEATURES_GET_REPLY`
>
> </td>
> <td>
>
>
> device features
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_FEATURES_SET_REPLY`
>
> </td>
> <td>
>
>
> optional reply to FEATURES_SET
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_FEATURES_NTF`
>
> </td>
> <td>
>
>
> netdev features notification
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_PRIVFLAGS_GET_REPLY`
>
> </td>
> <td>
>
>
> private flags
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_PRIVFLAGS_NTF`
>
> </td>
> <td>
>
>
> private flags
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_RINGS_GET_REPLY`
>
> </td>
> <td>
>
>
> ring sizes
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_RINGS_NTF`
>
> </td>
> <td>
>
>
> ring sizes
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_CHANNELS_GET_REPLY`
>
> </td>
> <td>
>
>
> channel counts
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_CHANNELS_NTF`
>
> </td>
> <td>
>
>
> channel counts
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_COALESCE_GET_REPLY`
>
> </td>
> <td>
>
>
> coalescing parameters
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_COALESCE_NTF`
>
> </td>
> <td>
>
>
> coalescing parameters
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_PAUSE_GET_REPLY`
>
> </td>
> <td>
>
>
> pause parameters
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_PAUSE_NTF`
>
> </td>
> <td>
>
>
> pause parameters
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_EEE_GET_REPLY`
>
> </td>
> <td>
>
>
> EEE settings
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_EEE_NTF`
>
> </td>
> <td>
>
>
> EEE settings
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_TSINFO_GET_REPLY`
>
> </td>
> <td>
>
>
> timestamping info
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_CABLE_TEST_NTF`
>
> </td>
> <td>
>
>
> Cable test results
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_CABLE_TEST_TDR_NTF`
>
> </td>
> <td>
>
>
> Cable test TDR results
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_TUNNEL_INFO_GET_REPLY`
>
> </td>
> <td>
>
>
> tunnel offload info
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_FEC_GET_REPLY`
>
> </td>
> <td>
>
>
> FEC settings
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_FEC_NTF`
>
> </td>
> <td>
>
>
> FEC settings
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_MODULE_EEPROM_GET_REPLY`
>
> </td>
> <td>
>
>
> read SFP module EEPROM
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_STATS_GET_REPLY`
>
> </td>
> <td>
>
>
> standard statistics
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_PHC_VCLOCKS_GET_REPLY`
>
> </td>
> <td>
>
>
> PHC virtual clocks info
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_MODULE_GET_REPLY`
>
> </td>
> <td>
>
>
> transceiver module parameters
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_PSE_GET_REPLY`
>
> </td>
> <td>
>
>
> PSE parameters
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_RSS_GET_REPLY`
>
> </td>
> <td>
>
>
> RSS settings
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_RSS_NTF`
>
> </td>
> <td>
>
>
> RSS settings
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_PLCA_GET_CFG_REPLY`
>
> </td>
> <td>
>
>
> PLCA RS parameters
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_PLCA_GET_STATUS_REPLY`
>
> </td>
> <td>
>
>
> PLCA RS status
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_PLCA_NTF`
>
> </td>
> <td>
>
>
> PLCA RS parameters
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_MM_GET_REPLY`
>
> </td>
> <td>
>
>
> MAC merge layer status
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_MODULE_FW_FLASH_NTF`
>
> </td>
> <td>
>
>
> transceiver module flash updates
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_PHY_GET_REPLY`
>
> </td>
> <td>
>
>
> Ethernet PHY information
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_PHY_NTF`
>
> </td>
> <td>
>
>
> Ethernet PHY information change
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_TSCONFIG_GET_REPLY`
>
> </td>
> <td>
>
>
> hw timestamping configuration
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_TSCONFIG_SET_REPLY`
>
> </td>
> <td>
>
>
> new hw timestamping configuration
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_PSE_NTF`
>
> </td>
> <td>
>
>
> PSE events notification
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_RSS_NTF`
>
> </td>
> <td>
>
>
> RSS settings notification
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_RSS_CREATE_ACT_REPLY`
>
> </td>
> <td>
>
>
> create an additional RSS context
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_RSS_CREATE_NTF`
>
> </td>
> <td>
>
>
> additional RSS context created
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_RSS_DELETE_NTF`
>
> </td>
> <td>
>
>
> additional RSS context deleted
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_MSG_MSE_GET_REPLY`
>
> </td>
> <td>
>
>
> MSE diagnostic data
>
> </td>
> </tr>
> </tbody>
> </table>

`GET` requests are sent by userspace applications to retrieve device information. They usually do not contain any message specific attributes. Kernel replies with corresponding "GET_REPLY" message. For most types, `GET` request with `NLM_F_DUMP` and no device identification can be used to query the information for all devices supporting the request.

If the data can be also modified, corresponding `SET` message with the same layout as corresponding `GET_REPLY` is used to request changes. Only attributes where a change is requested are included in such request (also, not all attributes may be changed). Replies to most `SET` request consist only of error code and extack; if kernel provides additional data, it is sent in the form of corresponding `SET_REPLY` message which can be suppressed by setting `ETHTOOL_FLAG_OMIT_REPLY` flag in request header.

Data modification also triggers sending a `NTF` message with a notification. These usually bear only a subset of attributes which was affected by the change. The same notification is issued if the data is modified using other means (mostly ioctl ethtool interface). Unlike notifications from ethtool netlink code which are only sent if something actually changed, notifications triggered by ioctl interface may be sent even if the request did not actually change any data.

`ACT` messages request kernel (driver) to perform a specific action. If some information is reported by kernel (which can be suppressed by setting `ETHTOOL_FLAG_OMIT_REPLY` flag in request header), the reply takes form of an `ACT_REPLY` message. Performing an action also triggers a notification (`NTF` message).

Later sections describe the format and semantics of these messages.

<a id="rst-strset-get"></a>

## STRSET_GET

Requests contents of a string set as provided by ioctl commands `ETHTOOL_GSSET_INFO` and `ETHTOOL_GSTRINGS.` String sets are not user writeable so that the corresponding `STRSET_SET` message is only used in kernel replies. There are two types of string sets: global (independent of a device, e.g. device feature names) and device specific (e.g. device private flags).

Request contents:

>
> <table>
> <tbody>
> <tr>
> <td colspan="3">
>
>
> `ETHTOOL_A_STRSET_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> request header
>
> </td>
> </tr>
> <tr>
> <td colspan="3">
>
>
> `ETHTOOL_A_STRSET_STRINGSETS`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> string set to request
>
> </td>
> </tr>
> <tr>
> <td>
>
>
>
>
> </td>
> <td colspan="2">
>
>
> `ETHTOOL_A_STRINGSETS_STRINGSET+`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> one string set
>
> </td>
> </tr>
> <tr>
> <td>
>
>
>
>
> </td>
> <td>
>
>
>
>
> </td>
> <td>
>
>
> `ETHTOOL_A_STRINGSET_ID`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> set id
>
> </td>
> </tr>
> </tbody>
> </table>

Kernel response contents:

>
> <table>
> <tbody>
> <tr>
> <td colspan="5">
>
>
> `ETHTOOL_A_STRSET_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> reply header
>
> </td>
> </tr>
> <tr>
> <td colspan="5">
>
>
> `ETHTOOL_A_STRSET_STRINGSETS`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> array of string sets
>
> </td>
> </tr>
> <tr>
> <td>
>
>
>
>
> </td>
> <td colspan="4">
>
>
> `ETHTOOL_A_STRINGSETS_STRINGSET+`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> one string set
>
> </td>
> </tr>
> <tr>
> <td>
>
>
>
>
> </td>
> <td>
>
>
>
>
> </td>
> <td colspan="3">
>
>
> `ETHTOOL_A_STRINGSET_ID`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> set id
>
> </td>
> </tr>
> <tr>
> <td>
>
>
>
>
> </td>
> <td>
>
>
>
>
> </td>
> <td colspan="3">
>
>
> `ETHTOOL_A_STRINGSET_COUNT`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> number of strings
>
> </td>
> </tr>
> <tr>
> <td>
>
>
>
>
> </td>
> <td>
>
>
>
>
> </td>
> <td colspan="3">
>
>
> `ETHTOOL_A_STRINGSET_STRINGS`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> array of strings
>
> </td>
> </tr>
> <tr>
> <td>
>
>
>
>
> </td>
> <td>
>
>
>
>
> </td>
> <td>
>
>
>
>
> </td>
> <td colspan="2">
>
>
> `ETHTOOL_A_STRINGS_STRING+`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> one string
>
> </td>
> </tr>
> <tr>
> <td>
>
>
>
>
> </td>
> <td>
>
>
>
>
> </td>
> <td>
>
>
>
>
> </td>
> <td>
>
>
>
>
> </td>
> <td>
>
>
> `ETHTOOL_A_STRING_INDEX`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> string index
>
> </td>
> </tr>
> <tr>
> <td>
>
>
>
>
> </td>
> <td>
>
>
>
>
> </td>
> <td>
>
>
>
>
> </td>
> <td>
>
>
>
>
> </td>
> <td>
>
>
> `ETHTOOL_A_STRING_VALUE`
>
> </td>
> <td>
>
>
> string
>
> </td>
> <td>
>
>
> string value
>
> </td>
> </tr>
> <tr>
> <td colspan="5">
>
>
> `ETHTOOL_A_STRSET_COUNTS_ONLY`
>
> </td>
> <td>
>
>
> flag
>
> </td>
> <td>
>
>
> return only counts
>
> </td>
> </tr>
> </tbody>
> </table>

Device identification in request header is optional. Depending on its presence a and `NLM_F_DUMP` flag, there are three type of `STRSET_GET` requests:

> - no `NLM_F_DUMP,` no device: get "global" stringsets
>
> - no `NLM_F_DUMP`, with device: get string sets related to the device
>
> - `NLM_F_DUMP`, no device: get device related string sets for all devices

If there is no `ETHTOOL_A_STRSET_STRINGSETS` array, all string sets of requested type are returned, otherwise only those specified in the request. Flag `ETHTOOL_A_STRSET_COUNTS_ONLY` tells kernel to only return string counts of the sets, not the actual strings.

<a id="rst-linkinfo-get"></a>

## LINKINFO_GET

Requests link settings as provided by `ETHTOOL_GLINKSETTINGS` except for link modes and autonegotiation related information. The request does not use any attributes.

Request contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_LINKINFO_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> request header
>
> </td>
> </tr>
> </tbody>
> </table>

Kernel response contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_LINKINFO_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> reply header
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_LINKINFO_PORT`
>
> </td>
> <td>
>
>
> u8
>
> </td>
> <td>
>
>
> physical port
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_LINKINFO_PHYADDR`
>
> </td>
> <td>
>
>
> u8
>
> </td>
> <td>
>
>
> phy MDIO address
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_LINKINFO_TP_MDIX`
>
> </td>
> <td>
>
>
> u8
>
> </td>
> <td>
>
>
> MDI(-X) status
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_LINKINFO_TP_MDIX_CTRL`
>
> </td>
> <td>
>
>
> u8
>
> </td>
> <td>
>
>
> MDI(-X) control
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_LINKINFO_TRANSCEIVER`
>
> </td>
> <td>
>
>
> u8
>
> </td>
> <td>
>
>
> transceiver
>
> </td>
> </tr>
> </tbody>
> </table>

Attributes and their values have the same meaning as matching members of the corresponding ioctl structures.

`LINKINFO_GET` allows dump requests (kernel returns reply message for all devices supporting the request).

<a id="rst-linkinfo-set"></a>

## LINKINFO_SET

`LINKINFO_SET` request allows setting some of the attributes reported by `LINKINFO_GET`.

Request contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_LINKINFO_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> request header
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_LINKINFO_PORT`
>
> </td>
> <td>
>
>
> u8
>
> </td>
> <td>
>
>
> physical port
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_LINKINFO_PHYADDR`
>
> </td>
> <td>
>
>
> u8
>
> </td>
> <td>
>
>
> phy MDIO address
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_LINKINFO_TP_MDIX_CTRL`
>
> </td>
> <td>
>
>
> u8
>
> </td>
> <td>
>
>
> MDI(-X) control
>
> </td>
> </tr>
> </tbody>
> </table>

MDI(-X) status and transceiver cannot be set, request with the corresponding attributes is rejected.

<a id="rst-linkmodes-get"></a>

## LINKMODES_GET

Requests link modes (supported, advertised and peer advertised) and related information (autonegotiation status, link speed and duplex) as provided by `ETHTOOL_GLINKSETTINGS`. The request does not use any attributes.

Request contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_LINKMODES_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> request header
>
> </td>
> </tr>
> </tbody>
> </table>

Kernel response contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_LINKMODES_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> reply header
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_LINKMODES_AUTONEG`
>
> </td>
> <td>
>
>
> u8
>
> </td>
> <td>
>
>
> autonegotiation status
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_LINKMODES_OURS`
>
> </td>
> <td>
>
>
> bitset
>
> </td>
> <td>
>
>
> advertised link modes
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_LINKMODES_PEER`
>
> </td>
> <td>
>
>
> bitset
>
> </td>
> <td>
>
>
> partner link modes
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_LINKMODES_SPEED`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> link speed (Mb/s)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_LINKMODES_DUPLEX`
>
> </td>
> <td>
>
>
> u8
>
> </td>
> <td>
>
>
> duplex mode
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_LINKMODES_MASTER_SLAVE_CFG`
>
> </td>
> <td>
>
>
> u8
>
> </td>
> <td>
>
>
> Master/slave port mode
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_LINKMODES_MASTER_SLAVE_STATE`
>
> </td>
> <td>
>
>
> u8
>
> </td>
> <td>
>
>
> Master/slave port state
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_LINKMODES_RATE_MATCHING`
>
> </td>
> <td>
>
>
> u8
>
> </td>
> <td>
>
>
> PHY rate matching
>
> </td>
> </tr>
> </tbody>
> </table>

For `ETHTOOL_A_LINKMODES_OURS`, value represents advertised modes and mask represents supported modes. `ETHTOOL_A_LINKMODES_PEER` in the reply is a bit list.

`LINKMODES_GET` allows dump requests (kernel returns reply messages for all devices supporting the request).

<a id="rst-linkmodes-set"></a>

## LINKMODES_SET

Request contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_LINKMODES_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> request header
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_LINKMODES_AUTONEG`
>
> </td>
> <td>
>
>
> u8
>
> </td>
> <td>
>
>
> autonegotiation status
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_LINKMODES_OURS`
>
> </td>
> <td>
>
>
> bitset
>
> </td>
> <td>
>
>
> advertised link modes
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_LINKMODES_PEER`
>
> </td>
> <td>
>
>
> bitset
>
> </td>
> <td>
>
>
> partner link modes
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_LINKMODES_SPEED`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> link speed (Mb/s)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_LINKMODES_DUPLEX`
>
> </td>
> <td>
>
>
> u8
>
> </td>
> <td>
>
>
> duplex mode
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_LINKMODES_MASTER_SLAVE_CFG`
>
> </td>
> <td>
>
>
> u8
>
> </td>
> <td>
>
>
> Master/slave port mode
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_LINKMODES_RATE_MATCHING`
>
> </td>
> <td>
>
>
> u8
>
> </td>
> <td>
>
>
> PHY rate matching
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_LINKMODES_LANES`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> lanes
>
> </td>
> </tr>
> </tbody>
> </table>

`ETHTOOL_A_LINKMODES_OURS` bit set allows setting advertised link modes. If autonegotiation is on (either set now or kept from before), advertised modes are not changed (no `ETHTOOL_A_LINKMODES_OURS` attribute) and at least one of speed, duplex and lanes is specified, kernel adjusts advertised modes to all supported modes matching speed, duplex, lanes or all (whatever is specified). This autoselection is done on ethtool side with ioctl interface, netlink interface is supposed to allow requesting changes without knowing what exactly kernel supports.

<a id="rst-linkstate-get"></a>

## LINKSTATE_GET

Requests link state information. Link up/down flag (as provided by `ETHTOOL_GLINK` ioctl command) is provided. Optionally, extended state might be provided as well. In general, extended state describes reasons for why a port is down, or why it operates in some non-obvious mode. This request does not have any attributes.

Request contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_LINKSTATE_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> request header
>
> </td>
> </tr>
> </tbody>
> </table>

Kernel response contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_LINKSTATE_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> reply header
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_LINKSTATE_LINK`
>
> </td>
> <td>
>
>
> bool
>
> </td>
> <td>
>
>
> link state (up/down)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_LINKSTATE_SQI`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> Current Signal Quality Index
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_LINKSTATE_SQI_MAX`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> Max support SQI value
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_LINKSTATE_EXT_STATE`
>
> </td>
> <td>
>
>
> u8
>
> </td>
> <td>
>
>
> link extended state
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_LINKSTATE_EXT_SUBSTATE`
>
> </td>
> <td>
>
>
> u8
>
> </td>
> <td>
>
>
> link extended substate
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_LINKSTATE_EXT_DOWN_CNT`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> count of link down events
>
> </td>
> </tr>
> </tbody>
> </table>

For most NIC drivers, the value of `ETHTOOL_A_LINKSTATE_LINK` returns carrier flag provided by `netif_carrier_ok()` but there are drivers which define their own handler.

`ETHTOOL_A_LINKSTATE_EXT_STATE` and `ETHTOOL_A_LINKSTATE_EXT_SUBSTATE` are optional values. ethtool core can provide either both `ETHTOOL_A_LINKSTATE_EXT_STATE` and `ETHTOOL_A_LINKSTATE_EXT_SUBSTATE`, or only `ETHTOOL_A_LINKSTATE_EXT_STATE`, or none of them.

`LINKSTATE_GET` allows dump requests (kernel returns reply messages for all devices supporting the request).

Link extended states:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_LINK_EXT_STATE_AUTONEG`
>
> </td>
> <td>
>
>
> States relating to the autonegotiation or issues therein
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_LINK_EXT_STATE_LINK_TRAINING_FAILURE`
>
> </td>
> <td>
>
>
> Failure during link training
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_LINK_EXT_STATE_LINK_LOGICAL_MISMATCH`
>
> </td>
> <td>
>
>
> Logical mismatch in physical coding sublayer or forward error correction sublayer
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_LINK_EXT_STATE_BAD_SIGNAL_INTEGRITY`
>
> </td>
> <td>
>
>
> Signal integrity issues
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_LINK_EXT_STATE_NO_CABLE`
>
> </td>
> <td>
>
>
> No cable connected
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_LINK_EXT_STATE_CABLE_ISSUE`
>
> </td>
> <td>
>
>
> Failure is related to cable, e.g., unsupported cable
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_LINK_EXT_STATE_EEPROM_ISSUE`
>
> </td>
> <td>
>
>
> Failure is related to EEPROM, e.g., failure during reading or parsing the data
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_LINK_EXT_STATE_CALIBRATION_FAILURE`
>
> </td>
> <td>
>
>
> Failure during calibration algorithm
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_LINK_EXT_STATE_POWER_BUDGET_EXCEEDED`
>
> </td>
> <td>
>
>
> The hardware is not able to provide the power required from cable or module
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_LINK_EXT_STATE_OVERHEAT`
>
> </td>
> <td>
>
>
> The module is overheated
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_LINK_EXT_STATE_MODULE`
>
> </td>
> <td>
>
>
> Transceiver module issue
>
> </td>
> </tr>
> </tbody>
> </table>

Link extended substates:

> Autoneg substates:
>
>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_LINK_EXT_SUBSTATE_AN_NO_PARTNER_DETECTED`
>
> </td>
> <td>
>
>
> Peer side is down
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_LINK_EXT_SUBSTATE_AN_ACK_NOT_RECEIVED`
>
> </td>
> <td>
>
>
> Ack not received from peer side
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_LINK_EXT_SUBSTATE_AN_NEXT_PAGE_EXCHANGE_FAILED`
>
> </td>
> <td>
>
>
> Next page exchange failed
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_LINK_EXT_SUBSTATE_AN_NO_PARTNER_DETECTED_FORCE_MODE`
>
> </td>
> <td>
>
>
> Peer side is down during force mode or there is no agreement of speed
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_LINK_EXT_SUBSTATE_AN_FEC_MISMATCH_DURING_OVERRIDE`
>
> </td>
> <td>
>
>
> Forward error correction modes in both sides are mismatched
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_LINK_EXT_SUBSTATE_AN_NO_HCD`
>
> </td>
> <td>
>
>
> No Highest Common Denominator
>
> </td>
> </tr>
> </tbody>
> </table>
>
> Link training substates:
>
>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_LINK_EXT_SUBSTATE_LT_KR_FRAME_LOCK_NOT_ACQUIRED`
>
> </td>
> <td>
>
>
> Frames were not recognized, the lock failed
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_LINK_EXT_SUBSTATE_LT_KR_LINK_INHIBIT_TIMEOUT`
>
> </td>
> <td>
>
>
> The lock did not occur before timeout
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_LINK_EXT_SUBSTATE_LT_KR_LINK_PARTNER_DID_NOT_SET_RECEIVER_READY`
>
> </td>
> <td>
>
>
> Peer side did not send ready signal after training process
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_LINK_EXT_SUBSTATE_LT_REMOTE_FAULT`
>
> </td>
> <td>
>
>
> Remote side is not ready yet
>
> </td>
> </tr>
> </tbody>
> </table>
>
> Link logical mismatch substates:
>
>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_LINK_EXT_SUBSTATE_LLM_PCS_DID_NOT_ACQUIRE_BLOCK_LOCK`
>
> </td>
> <td>
>
>
> Physical coding sublayer was not locked in first phase - block lock
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_LINK_EXT_SUBSTATE_LLM_PCS_DID_NOT_ACQUIRE_AM_LOCK`
>
> </td>
> <td>
>
>
> Physical coding sublayer was not locked in second phase - alignment markers lock
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_LINK_EXT_SUBSTATE_LLM_PCS_DID_NOT_GET_ALIGN_STATUS`
>
> </td>
> <td>
>
>
> Physical coding sublayer did not get align status
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_LINK_EXT_SUBSTATE_LLM_FC_FEC_IS_NOT_LOCKED`
>
> </td>
> <td>
>
>
> FC forward error correction is not locked
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_LINK_EXT_SUBSTATE_LLM_RS_FEC_IS_NOT_LOCKED`
>
> </td>
> <td>
>
>
> RS forward error correction is not locked
>
> </td>
> </tr>
> </tbody>
> </table>
>
> Bad signal integrity substates:
>
>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_LINK_EXT_SUBSTATE_BSI_LARGE_NUMBER_OF_PHYSICAL_ERRORS`
>
> </td>
> <td>
>
>
> Large number of physical errors
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_LINK_EXT_SUBSTATE_BSI_UNSUPPORTED_RATE`
>
> </td>
> <td>
>
>
> The system attempted to operate the cable at a rate that is not formally supported, which led to signal integrity issues
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_LINK_EXT_SUBSTATE_BSI_SERDES_REFERENCE_CLOCK_LOST`
>
> </td>
> <td>
>
>
> The external clock signal for SerDes is too weak or unavailable.
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_LINK_EXT_SUBSTATE_BSI_SERDES_ALOS`
>
> </td>
> <td>
>
>
> The received signal for SerDes is too weak because analog loss of signal.
>
> </td>
> </tr>
> </tbody>
> </table>
>
> Cable issue substates:
>
>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_LINK_EXT_SUBSTATE_CI_UNSUPPORTED_CABLE`
>
> </td>
> <td>
>
>
> Unsupported cable
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_LINK_EXT_SUBSTATE_CI_CABLE_TEST_FAILURE`
>
> </td>
> <td>
>
>
> Cable test failure
>
> </td>
> </tr>
> </tbody>
> </table>
>
> Transceiver module issue substates:
>
>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_LINK_EXT_SUBSTATE_MODULE_CMIS_NOT_READY`
>
> </td>
> <td>
>
>
> The CMIS Module State Machine did not reach the ModuleReady state. For example, if the module is stuck at ModuleFault state
>
> </td>
> </tr>
> </tbody>
> </table>

<a id="rst-debug-get"></a>

## DEBUG_GET

Requests debugging settings of a device. At the moment, only message mask is provided.

Request contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_DEBUG_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> request header
>
> </td>
> </tr>
> </tbody>
> </table>

Kernel response contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_DEBUG_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> reply header
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_DEBUG_MSGMASK`
>
> </td>
> <td>
>
>
> bitset
>
> </td>
> <td>
>
>
> message mask
>
> </td>
> </tr>
> </tbody>
> </table>

The message mask (`ETHTOOL_A_DEBUG_MSGMASK`) is equal to message level as provided by `ETHTOOL_GMSGLVL` and set by `ETHTOOL_SMSGLVL` in ioctl interface. While it is called message level there for historical reasons, most drivers and almost all newer drivers use it as a mask of enabled message classes (represented by `NETIF_MSG_*` constants); therefore netlink interface follows its actual use in practice.

`DEBUG_GET` allows dump requests (kernel returns reply messages for all devices supporting the request).

<a id="rst-debug-set"></a>

## DEBUG_SET

Set or update debugging settings of a device. At the moment, only message mask is supported.

Request contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_DEBUG_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> request header
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_DEBUG_MSGMASK`
>
> </td>
> <td>
>
>
> bitset
>
> </td>
> <td>
>
>
> message mask
>
> </td>
> </tr>
> </tbody>
> </table>

`ETHTOOL_A_DEBUG_MSGMASK` bit set allows setting or modifying mask of enabled debugging message types for the device.

<a id="rst-wol-get"></a>

## WOL_GET

Query device wake-on-lan settings. Unlike most "GET" type requests, `ETHTOOL_MSG_WOL_GET` requires (netns) `CAP_NET_ADMIN` privileges as it (potentially) provides SecureOn(tm) password which is confidential.

Request contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_WOL_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> request header
>
> </td>
> </tr>
> </tbody>
> </table>

Kernel response contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_WOL_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> reply header
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_WOL_MODES`
>
> </td>
> <td>
>
>
> bitset
>
> </td>
> <td>
>
>
> mask of enabled WoL modes
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_WOL_SOPASS`
>
> </td>
> <td>
>
>
> binary
>
> </td>
> <td>
>
>
> SecureOn(tm) password
>
> </td>
> </tr>
> </tbody>
> </table>

In reply, `ETHTOOL_A_WOL_MODES` mask consists of modes supported by the device, value of modes which are enabled. `ETHTOOL_A_WOL_SOPASS` is only included in reply if `WAKE_MAGICSECURE` mode is supported.

<a id="rst-wol-set"></a>

## WOL_SET

Set or update wake-on-lan settings.

Request contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_WOL_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> request header
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_WOL_MODES`
>
> </td>
> <td>
>
>
> bitset
>
> </td>
> <td>
>
>
> enabled WoL modes
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_WOL_SOPASS`
>
> </td>
> <td>
>
>
> binary
>
> </td>
> <td>
>
>
> SecureOn(tm) password
>
> </td>
> </tr>
> </tbody>
> </table>

`ETHTOOL_A_WOL_SOPASS` is only allowed for devices supporting `WAKE_MAGICSECURE` mode.

<a id="rst-features-get"></a>

## FEATURES_GET

Gets netdev features like `ETHTOOL_GFEATURES` ioctl request.

Request contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_FEATURES_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> request header
>
> </td>
> </tr>
> </tbody>
> </table>

Kernel response contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_FEATURES_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> reply header
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_FEATURES_HW`
>
> </td>
> <td>
>
>
> bitset
>
> </td>
> <td>
>
>
> dev-&gt;hw_features
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_FEATURES_WANTED`
>
> </td>
> <td>
>
>
> bitset
>
> </td>
> <td>
>
>
> dev-&gt;wanted_features
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_FEATURES_ACTIVE`
>
> </td>
> <td>
>
>
> bitset
>
> </td>
> <td>
>
>
> dev-&gt;features
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_FEATURES_NOCHANGE`
>
> </td>
> <td>
>
>
> bitset
>
> </td>
> <td>
>
>
> NETIF_F_NEVER_CHANGE
>
> </td>
> </tr>
> </tbody>
> </table>

Bitmaps in kernel response have the same meaning as bitmaps used in ioctl interference but attribute names are different (they are based on corresponding members of struct net_device). Legacy "flags" are not provided, if userspace needs them (most likely only ethtool for backward compatibility), it can calculate their values from related feature bits itself. ETHA_FEATURES_HW uses mask consisting of all features recognized by kernel (to provide all names when using verbose bitmap format), the other three use no mask (simple bit lists).

<a id="rst-features-set"></a>

## FEATURES_SET

Request to set netdev features like `ETHTOOL_SFEATURES` ioctl request.

Request contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_FEATURES_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> request header
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_FEATURES_WANTED`
>
> </td>
> <td>
>
>
> bitset
>
> </td>
> <td>
>
>
> requested features
>
> </td>
> </tr>
> </tbody>
> </table>

Kernel response contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_FEATURES_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> reply header
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_FEATURES_WANTED`
>
> </td>
> <td>
>
>
> bitset
>
> </td>
> <td>
>
>
> diff wanted vs. result
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_FEATURES_ACTIVE`
>
> </td>
> <td>
>
>
> bitset
>
> </td>
> <td>
>
>
> diff old vs. new active
>
> </td>
> </tr>
> </tbody>
> </table>

Request contains only one bitset which can be either value/mask pair (request to change specific feature bits and leave the rest) or only a value (request to set all features to specified set).

As request is subject to netdev_change_features() sanity checks, optional kernel reply (can be suppressed by `ETHTOOL_FLAG_OMIT_REPLY` flag in request header) informs client about the actual result. `ETHTOOL_A_FEATURES_WANTED` reports the difference between client request and actual result: mask consists of bits which differ between requested features and result (dev-&gt;features after the operation), value consists of values of these bits in the request (i.e. negated values from resulting features). `ETHTOOL_A_FEATURES_ACTIVE` reports the difference between old and new dev-&gt;features: mask consists of bits which have changed, values are their values in new dev-&gt;features (after the operation).

`ETHTOOL_MSG_FEATURES_NTF` notification is sent not only if device features are modified using `ETHTOOL_MSG_FEATURES_SET` request or on of ethtool ioctl request but also each time features are modified with netdev_update_features() or netdev_change_features().

<a id="rst-privflags-get"></a>

## PRIVFLAGS_GET

Gets private flags like `ETHTOOL_GPFLAGS` ioctl request.

Request contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_PRIVFLAGS_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> request header
>
> </td>
> </tr>
> </tbody>
> </table>

Kernel response contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_PRIVFLAGS_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> reply header
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_PRIVFLAGS_FLAGS`
>
> </td>
> <td>
>
>
> bitset
>
> </td>
> <td>
>
>
> private flags
>
> </td>
> </tr>
> </tbody>
> </table>

`ETHTOOL_A_PRIVFLAGS_FLAGS` is a bitset with values of device private flags. These flags are defined by driver, their number and names (and also meaning) are device dependent. For compact bitset format, names can be retrieved as `ETH_SS_PRIV_FLAGS` string set. If verbose bitset format is requested, response uses all private flags supported by the device as mask so that client gets the full information without having to fetch the string set with names.

<a id="rst-privflags-set"></a>

## PRIVFLAGS_SET

Sets or modifies values of device private flags like `ETHTOOL_SPFLAGS` ioctl request.

Request contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_PRIVFLAGS_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> request header
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_PRIVFLAGS_FLAGS`
>
> </td>
> <td>
>
>
> bitset
>
> </td>
> <td>
>
>
> private flags
>
> </td>
> </tr>
> </tbody>
> </table>

`ETHTOOL_A_PRIVFLAGS_FLAGS` can either set the whole set of private flags or modify only values of some of them.

<a id="rst-rings-get"></a>

## RINGS_GET

Gets ring sizes like `ETHTOOL_GRINGPARAM` ioctl request.

Request contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_RINGS_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> request header
>
> </td>
> </tr>
> </tbody>
> </table>

Kernel response contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_RINGS_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> reply header
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_RINGS_RX_MAX`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> max size of RX ring
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_RINGS_RX_MINI_MAX`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> max size of RX mini ring
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_RINGS_RX_JUMBO_MAX`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> max size of RX jumbo ring
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_RINGS_TX_MAX`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> max size of TX ring
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_RINGS_RX`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> size of RX ring
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_RINGS_RX_MINI`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> size of RX mini ring
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_RINGS_RX_JUMBO`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> size of RX jumbo ring
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_RINGS_TX`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> size of TX ring
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_RINGS_RX_BUF_LEN`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> size of buffers on the ring
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_RINGS_TCP_DATA_SPLIT`
>
> </td>
> <td>
>
>
> u8
>
> </td>
> <td>
>
>
> TCP header / data split
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_RINGS_CQE_SIZE`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> Size of TX/RX CQE
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_RINGS_TX_PUSH`
>
> </td>
> <td>
>
>
> u8
>
> </td>
> <td>
>
>
> flag of TX Push mode
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_RINGS_RX_PUSH`
>
> </td>
> <td>
>
>
> u8
>
> </td>
> <td>
>
>
> flag of RX Push mode
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_RINGS_TX_PUSH_BUF_LEN`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> size of TX push buffer
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_RINGS_TX_PUSH_BUF_LEN_MAX`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> max size of TX push buffer
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_RINGS_HDS_THRESH`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> threshold of header / data split
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_RINGS_HDS_THRESH_MAX`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> max threshold of header / data split
>
> </td>
> </tr>
> </tbody>
> </table>

`ETHTOOL_A_RINGS_TCP_DATA_SPLIT` indicates whether the device is usable with page-flipping TCP zero-copy receive (`getsockopt(TCP_ZEROCOPY_RECEIVE)`). If enabled the device is configured to place frame headers and data into separate buffers. The device configuration must make it possible to receive full memory pages of data, for example because MTU is high enough or through HW-GRO.

`ETHTOOL_A_RINGS_[RX|TX]_PUSH` flag is used to enable descriptor fast path to send or receive packets. In ordinary path, driver fills descriptors in DRAM and notifies NIC hardware. In fast path, driver pushes descriptors to the device through MMIO writes, thus reducing the latency. However, enabling this feature may increase the CPU cost. Drivers may enforce additional per-packet eligibility checks (e.g. on packet size).

`ETHTOOL_A_RINGS_TX_PUSH_BUF_LEN` specifies the maximum number of bytes of a transmitted packet a driver can push directly to the underlying device ('push' mode). Pushing some of the payload bytes to the device has the advantages of reducing latency for small packets by avoiding DMA mapping (same as `ETHTOOL_A_RINGS_TX_PUSH` parameter) as well as allowing the underlying device to process packet headers ahead of fetching its payload. This can help the device to make fast actions based on the packet's headers. This is similar to the "tx-copybreak" parameter, which copies the packet to a preallocated DMA memory area instead of mapping new memory. However, tx-push-buff parameter copies the packet directly to the device to allow the device to take faster actions on the packet.

<a id="rst-rings-set"></a>

## RINGS_SET

Sets ring sizes like `ETHTOOL_SRINGPARAM` ioctl request.

Request contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_RINGS_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> reply header
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_RINGS_RX`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> size of RX ring
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_RINGS_RX_MINI`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> size of RX mini ring
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_RINGS_RX_JUMBO`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> size of RX jumbo ring
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_RINGS_TX`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> size of TX ring
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_RINGS_RX_BUF_LEN`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> size of buffers on the ring
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_RINGS_TCP_DATA_SPLIT`
>
> </td>
> <td>
>
>
> u8
>
> </td>
> <td>
>
>
> TCP header / data split
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_RINGS_CQE_SIZE`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> Size of TX/RX CQE
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_RINGS_TX_PUSH`
>
> </td>
> <td>
>
>
> u8
>
> </td>
> <td>
>
>
> flag of TX Push mode
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_RINGS_RX_PUSH`
>
> </td>
> <td>
>
>
> u8
>
> </td>
> <td>
>
>
> flag of RX Push mode
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_RINGS_TX_PUSH_BUF_LEN`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> size of TX push buffer
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_RINGS_HDS_THRESH`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> threshold of header / data split
>
> </td>
> </tr>
> </tbody>
> </table>

Kernel checks that requested ring sizes do not exceed limits reported by driver. Driver may impose additional constraints and may not support all attributes.

`ETHTOOL_A_RINGS_CQE_SIZE` specifies the completion queue event size. Completion queue events (CQE) are the events posted by NIC to indicate the completion status of a packet when the packet is sent (like send success or error) or received (like pointers to packet fragments). The CQE size parameter enables to modify the CQE size other than default size if NIC supports it. A bigger CQE can have more receive buffer pointers, and in turn the NIC can transfer a bigger frame from wire. Based on the NIC hardware, the overall completion queue size can be adjusted in the driver if CQE size is modified.

`ETHTOOL_A_RINGS_HDS_THRESH` specifies the threshold value of header / data split feature. If a received packet size is larger than this threshold value, header and data will be split.

<a id="rst-channels-get"></a>

## CHANNELS_GET

Gets channel counts like `ETHTOOL_GCHANNELS` ioctl request.

Request contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_CHANNELS_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> request header
>
> </td>
> </tr>
> </tbody>
> </table>

Kernel response contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_CHANNELS_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> reply header
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_CHANNELS_RX_MAX`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> max receive channels
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_CHANNELS_TX_MAX`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> max transmit channels
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_CHANNELS_OTHER_MAX`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> max other channels
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_CHANNELS_COMBINED_MAX`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> max combined channels
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_CHANNELS_RX_COUNT`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> receive channel count
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_CHANNELS_TX_COUNT`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> transmit channel count
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_CHANNELS_OTHER_COUNT`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> other channel count
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_CHANNELS_COMBINED_COUNT`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> combined channel count
>
> </td>
> </tr>
> </tbody>
> </table>

<a id="rst-channels-set"></a>

## CHANNELS_SET

Sets channel counts like `ETHTOOL_SCHANNELS` ioctl request.

Request contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_CHANNELS_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> request header
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_CHANNELS_RX_COUNT`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> receive channel count
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_CHANNELS_TX_COUNT`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> transmit channel count
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_CHANNELS_OTHER_COUNT`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> other channel count
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_CHANNELS_COMBINED_COUNT`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> combined channel count
>
> </td>
> </tr>
> </tbody>
> </table>

Kernel checks that requested channel counts do not exceed limits reported by driver. Driver may impose additional constraints and may not support all attributes.

<a id="rst-coalesce-get"></a>

## COALESCE_GET

Gets coalescing parameters like `ETHTOOL_GCOALESCE` ioctl request.

Request contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_COALESCE_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> request header
>
> </td>
> </tr>
> </tbody>
> </table>

Kernel response contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_COALESCE_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> reply header
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_COALESCE_RX_USECS`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> delay (us), normal Rx
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_COALESCE_RX_MAX_FRAMES`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> max packets, normal Rx
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_COALESCE_RX_USECS_IRQ`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> delay (us), Rx in IRQ
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_COALESCE_RX_MAX_FRAMES_IRQ`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> max packets, Rx in IRQ
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_COALESCE_TX_USECS`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> delay (us), normal Tx
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_COALESCE_TX_MAX_FRAMES`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> max packets, normal Tx
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_COALESCE_TX_USECS_IRQ`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> delay (us), Tx in IRQ
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_COALESCE_TX_MAX_FRAMES_IRQ`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> IRQ packets, Tx in IRQ
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_COALESCE_STATS_BLOCK_USECS`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> delay of stats update
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_COALESCE_USE_ADAPTIVE_RX`
>
> </td>
> <td>
>
>
> bool
>
> </td>
> <td>
>
>
> adaptive Rx coalesce
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_COALESCE_USE_ADAPTIVE_TX`
>
> </td>
> <td>
>
>
> bool
>
> </td>
> <td>
>
>
> adaptive Tx coalesce
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_COALESCE_PKT_RATE_LOW`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> threshold for low rate
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_COALESCE_RX_USECS_LOW`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> delay (us), low Rx
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_COALESCE_RX_MAX_FRAMES_LOW`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> max packets, low Rx
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_COALESCE_TX_USECS_LOW`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> delay (us), low Tx
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_COALESCE_TX_MAX_FRAMES_LOW`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> max packets, low Tx
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_COALESCE_PKT_RATE_HIGH`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> threshold for high rate
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_COALESCE_RX_USECS_HIGH`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> delay (us), high Rx
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_COALESCE_RX_MAX_FRAMES_HIGH`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> max packets, high Rx
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_COALESCE_TX_USECS_HIGH`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> delay (us), high Tx
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_COALESCE_TX_MAX_FRAMES_HIGH`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> max packets, high Tx
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_COALESCE_RATE_SAMPLE_INTERVAL`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> rate sampling interval
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_COALESCE_USE_CQE_TX`
>
> </td>
> <td>
>
>
> bool
>
> </td>
> <td>
>
>
> timer reset mode, Tx
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_COALESCE_USE_CQE_RX`
>
> </td>
> <td>
>
>
> bool
>
> </td>
> <td>
>
>
> timer reset mode, Rx
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_COALESCE_TX_AGGR_MAX_BYTES`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> max aggr size, Tx
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_COALESCE_TX_AGGR_MAX_FRAMES`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> max aggr packets, Tx
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_COALESCE_TX_AGGR_TIME_USECS`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> time (us), aggr, Tx
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_COALESCE_RX_PROFILE`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> profile of DIM, Rx
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_COALESCE_TX_PROFILE`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> profile of DIM, Tx
>
> </td>
> </tr>
> </tbody>
> </table>

Attributes are only included in reply if their value is not zero or the corresponding bit in `ethtool_ops::supported_coalesce_params` is set (i.e. they are declared as supported by driver).

Timer reset mode (`ETHTOOL_A_COALESCE_USE_CQE_TX` and `ETHTOOL_A_COALESCE_USE_CQE_RX`) controls the interaction between packet arrival and the various time based delay parameters. By default timers are expected to limit the max delay between any packet arrival/departure and a corresponding interrupt. In this mode timer should be started by packet arrival (sometimes delivery of previous interrupt) and reset when interrupt is delivered. Setting the appropriate attribute to 1 will enable `CQE` mode, where each packet event resets the timer. In this mode timer is used to force the interrupt if queue goes idle, while busy queues depend on the packet limit to trigger interrupts.

Tx aggregation consists of copying frames into a contiguous buffer so that they can be submitted as a single IO operation. `ETHTOOL_A_COALESCE_TX_AGGR_MAX_BYTES` describes the maximum size in bytes for the submitted buffer. `ETHTOOL_A_COALESCE_TX_AGGR_MAX_FRAMES` describes the maximum number of frames that can be aggregated into a single buffer. `ETHTOOL_A_COALESCE_TX_AGGR_TIME_USECS` describes the amount of time in usecs, counted since the first packet arrival in an aggregated block, after which the block should be sent. This feature is mainly of interest for specific USB devices which does not cope well with frequent small-sized URBs transmissions.

`ETHTOOL_A_COALESCE_RX_PROFILE` and `ETHTOOL_A_COALESCE_TX_PROFILE` refer to DIM parameters, see [Generic Network Dynamic Interrupt Moderation (Net DIM)](<https://www.kernel.org/doc/Documentation/networking/net_dim.rst>)<a id="rst-generic-network-dynamic-interrupt-moderation-net-dim"></a>.

<a id="rst-coalesce-set"></a>

## COALESCE_SET

Sets coalescing parameters like `ETHTOOL_SCOALESCE` ioctl request.

Request contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_COALESCE_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> request header
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_COALESCE_RX_USECS`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> delay (us), normal Rx
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_COALESCE_RX_MAX_FRAMES`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> max packets, normal Rx
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_COALESCE_RX_USECS_IRQ`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> delay (us), Rx in IRQ
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_COALESCE_RX_MAX_FRAMES_IRQ`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> max packets, Rx in IRQ
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_COALESCE_TX_USECS`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> delay (us), normal Tx
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_COALESCE_TX_MAX_FRAMES`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> max packets, normal Tx
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_COALESCE_TX_USECS_IRQ`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> delay (us), Tx in IRQ
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_COALESCE_TX_MAX_FRAMES_IRQ`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> IRQ packets, Tx in IRQ
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_COALESCE_STATS_BLOCK_USECS`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> delay of stats update
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_COALESCE_USE_ADAPTIVE_RX`
>
> </td>
> <td>
>
>
> bool
>
> </td>
> <td>
>
>
> adaptive Rx coalesce
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_COALESCE_USE_ADAPTIVE_TX`
>
> </td>
> <td>
>
>
> bool
>
> </td>
> <td>
>
>
> adaptive Tx coalesce
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_COALESCE_PKT_RATE_LOW`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> threshold for low rate
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_COALESCE_RX_USECS_LOW`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> delay (us), low Rx
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_COALESCE_RX_MAX_FRAMES_LOW`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> max packets, low Rx
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_COALESCE_TX_USECS_LOW`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> delay (us), low Tx
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_COALESCE_TX_MAX_FRAMES_LOW`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> max packets, low Tx
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_COALESCE_PKT_RATE_HIGH`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> threshold for high rate
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_COALESCE_RX_USECS_HIGH`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> delay (us), high Rx
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_COALESCE_RX_MAX_FRAMES_HIGH`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> max packets, high Rx
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_COALESCE_TX_USECS_HIGH`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> delay (us), high Tx
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_COALESCE_TX_MAX_FRAMES_HIGH`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> max packets, high Tx
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_COALESCE_RATE_SAMPLE_INTERVAL`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> rate sampling interval
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_COALESCE_USE_CQE_TX`
>
> </td>
> <td>
>
>
> bool
>
> </td>
> <td>
>
>
> timer reset mode, Tx
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_COALESCE_USE_CQE_RX`
>
> </td>
> <td>
>
>
> bool
>
> </td>
> <td>
>
>
> timer reset mode, Rx
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_COALESCE_TX_AGGR_MAX_BYTES`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> max aggr size, Tx
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_COALESCE_TX_AGGR_MAX_FRAMES`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> max aggr packets, Tx
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_COALESCE_TX_AGGR_TIME_USECS`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> time (us), aggr, Tx
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_COALESCE_RX_PROFILE`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> profile of DIM, Rx
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_COALESCE_TX_PROFILE`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> profile of DIM, Tx
>
> </td>
> </tr>
> </tbody>
> </table>

Request is rejected if it attributes declared as unsupported by driver (i.e. such that the corresponding bit in `ethtool_ops::supported_coalesce_params` is not set), regardless of their values. Driver may impose additional constraints on coalescing parameters and their values.

Compared to requests issued via the `ioctl()` netlink version of this request will try harder to make sure that values specified by the user have been applied and may call the driver twice.

<a id="rst-pause-get"></a>

## PAUSE_GET

Gets pause frame settings like `ETHTOOL_GPAUSEPARAM` ioctl request.

Request contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_PAUSE_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> request header
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_PAUSE_STATS_SRC`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> source of statistics
>
> </td>
> </tr>
> </tbody>
> </table>

`ETHTOOL_A_PAUSE_STATS_SRC` is optional. It takes values from:

```{kernel-doc} include/uapi/linux/ethtool.h
:identifiers: ethtool_mac_stats_src
```

If absent from the request, stats will be provided with an `ETHTOOL_A_PAUSE_STATS_SRC` attribute in the response equal to `ETHTOOL_MAC_STATS_SRC_AGGREGATE`.

Kernel response contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_PAUSE_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> request header
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_PAUSE_AUTONEG`
>
> </td>
> <td>
>
>
> bool
>
> </td>
> <td>
>
>
> pause autonegotiation
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_PAUSE_RX`
>
> </td>
> <td>
>
>
> bool
>
> </td>
> <td>
>
>
> receive pause frames
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_PAUSE_TX`
>
> </td>
> <td>
>
>
> bool
>
> </td>
> <td>
>
>
> transmit pause frames
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_PAUSE_STATS`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> pause statistics
>
> </td>
> </tr>
> </tbody>
> </table>

`ETHTOOL_A_PAUSE_STATS` are reported if `ETHTOOL_FLAG_STATS` was set in `ETHTOOL_A_HEADER_FLAGS`. It will be empty if driver did not report any statistics. Drivers fill in the statistics in the following structure:

```{kernel-doc} include/linux/ethtool.h
:identifiers: ethtool_pause_stats
```

Each member has a corresponding attribute defined.

<a id="rst-pause-set"></a>

## PAUSE_SET

Sets pause parameters like `ETHTOOL_GPAUSEPARAM` ioctl request.

Request contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_PAUSE_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> request header
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_PAUSE_AUTONEG`
>
> </td>
> <td>
>
>
> bool
>
> </td>
> <td>
>
>
> pause autonegotiation
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_PAUSE_RX`
>
> </td>
> <td>
>
>
> bool
>
> </td>
> <td>
>
>
> receive pause frames
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_PAUSE_TX`
>
> </td>
> <td>
>
>
> bool
>
> </td>
> <td>
>
>
> transmit pause frames
>
> </td>
> </tr>
> </tbody>
> </table>

<a id="rst-eee-get"></a>

## EEE_GET

Gets Energy Efficient Ethernet settings like `ETHTOOL_GEEE` ioctl request.

Request contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_EEE_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> request header
>
> </td>
> </tr>
> </tbody>
> </table>

Kernel response contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_EEE_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> request header
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_EEE_MODES_OURS`
>
> </td>
> <td>
>
>
> bool
>
> </td>
> <td>
>
>
> supported/advertised modes
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_EEE_MODES_PEER`
>
> </td>
> <td>
>
>
> bool
>
> </td>
> <td>
>
>
> peer advertised link modes
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_EEE_ACTIVE`
>
> </td>
> <td>
>
>
> bool
>
> </td>
> <td>
>
>
> EEE is actively used
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_EEE_ENABLED`
>
> </td>
> <td>
>
>
> bool
>
> </td>
> <td>
>
>
> EEE is enabled
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_EEE_TX_LPI_ENABLED`
>
> </td>
> <td>
>
>
> bool
>
> </td>
> <td>
>
>
> Tx lpi enabled
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_EEE_TX_LPI_TIMER`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> Tx lpi timeout (in us)
>
> </td>
> </tr>
> </tbody>
> </table>

In `ETHTOOL_A_EEE_MODES_OURS`, mask consists of link modes for which EEE is enabled, value of link modes for which EEE is advertised. Link modes for which peer advertises EEE are listed in `ETHTOOL_A_EEE_MODES_PEER` (no mask). The netlink interface allows reporting EEE status for all link modes but only first 32 are provided by the `ethtool_ops` callback.

<a id="rst-eee-set"></a>

## EEE_SET

Sets Energy Efficient Ethernet parameters like `ETHTOOL_SEEE` ioctl request.

Request contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_EEE_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> request header
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_EEE_MODES_OURS`
>
> </td>
> <td>
>
>
> bool
>
> </td>
> <td>
>
>
> advertised modes
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_EEE_ENABLED`
>
> </td>
> <td>
>
>
> bool
>
> </td>
> <td>
>
>
> EEE is enabled
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_EEE_TX_LPI_ENABLED`
>
> </td>
> <td>
>
>
> bool
>
> </td>
> <td>
>
>
> Tx lpi enabled
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_EEE_TX_LPI_TIMER`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> Tx lpi timeout (in us)
>
> </td>
> </tr>
> </tbody>
> </table>

`ETHTOOL_A_EEE_MODES_OURS` is used to either list link modes to advertise EEE for (if there is no mask) or specify changes to the list (if there is a mask). The netlink interface allows reporting EEE status for all link modes but only first 32 can be set at the moment as that is what the `ethtool_ops` callback supports.

<a id="rst-tsinfo-get"></a>

## TSINFO_GET

Gets timestamping information like `ETHTOOL_GET_TS_INFO` ioctl request.

Request contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_TSINFO_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> request header
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_TSINFO_HWTSTAMP_PROVIDER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> PTP hw clock provider
>
> </td>
> </tr>
> </tbody>
> </table>

Kernel response contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_TSINFO_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> request header
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_TSINFO_TIMESTAMPING`
>
> </td>
> <td>
>
>
> bitset
>
> </td>
> <td>
>
>
> SO_TIMESTAMPING flags
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_TSINFO_TX_TYPES`
>
> </td>
> <td>
>
>
> bitset
>
> </td>
> <td>
>
>
> supported Tx types
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_TSINFO_RX_FILTERS`
>
> </td>
> <td>
>
>
> bitset
>
> </td>
> <td>
>
>
> supported Rx filters
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_TSINFO_PHC_INDEX`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> PTP hw clock index
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_TSINFO_STATS`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> HW timestamping statistics
>
> </td>
> </tr>
> </tbody>
> </table>

`ETHTOOL_A_TSINFO_PHC_INDEX` is absent if there is no associated PHC (there is no special value for this case). The bitset attributes are omitted if they would be empty (no bit set).

Additional hardware timestamping statistics response contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_TS_STAT_TX_PKTS`
>
> </td>
> <td>
>
>
> uint
>
> </td>
> <td>
>
>
> Packets with Tx HW timestamps
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_TS_STAT_TX_LOST`
>
> </td>
> <td>
>
>
> uint
>
> </td>
> <td>
>
>
> Tx HW timestamp not arrived count
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_TS_STAT_TX_ERR`
>
> </td>
> <td>
>
>
> uint
>
> </td>
> <td>
>
>
> HW error request Tx timestamp count
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_TS_STAT_TX_ONESTEP_PKTS_UNCONFIRMED`
>
> </td>
> <td>
>
>
> uint
>
> </td>
> <td>
>
>
> Packets with one-step HW TX timestamps with unconfirmed delivery
>
> </td>
> </tr>
> </tbody>
> </table>

<a id="rst-cable-test"></a>

## CABLE_TEST

Start a cable test.

Request contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_CABLE_TEST_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> request header
>
> </td>
> </tr>
> </tbody>
> </table>

Notification contents:

An Ethernet cable typically contains 1, 2 or 4 pairs. The length of the pair can only be measured when there is a fault in the pair and hence a reflection. Information about the fault may not be available, depending on the specific hardware. Hence the contents of the notify message are mostly optional. The attributes can be repeated an arbitrary number of times, in an arbitrary order, for an arbitrary number of pairs.

The example shows the notification sent when the test is completed for a T2 cable, i.e. two pairs. One pair is OK and hence has no length information. The second pair has a fault and does have length information.

>
> <table>
> <tbody>
> <tr>
> <td colspan="3">
>
>
> `ETHTOOL_A_CABLE_TEST_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> reply header
>
> </td>
> </tr>
> <tr>
> <td colspan="3">
>
>
> `ETHTOOL_A_CABLE_TEST_STATUS`
>
> </td>
> <td>
>
>
> u8
>
> </td>
> <td>
>
>
> completed
>
> </td>
> </tr>
> <tr>
> <td colspan="3">
>
>
> `ETHTOOL_A_CABLE_TEST_NTF_NEST`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> all the results
>
> </td>
> </tr>
> <tr>
> <td>
>
>
>
>
> </td>
> <td colspan="2">
>
>
> `ETHTOOL_A_CABLE_NEST_RESULT`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> cable test result
>
> </td>
> </tr>
> <tr>
> <td>
>
>
>
>
> </td>
> <td>
>
>
>
>
> </td>
> <td>
>
>
> `ETHTOOL_A_CABLE_RESULTS_PAIR`
>
> </td>
> <td>
>
>
> u8
>
> </td>
> <td>
>
>
> pair number
>
> </td>
> </tr>
> <tr>
> <td>
>
>
>
>
> </td>
> <td>
>
>
>
>
> </td>
> <td>
>
>
> `ETHTOOL_A_CABLE_RESULTS_CODE`
>
> </td>
> <td>
>
>
> u8
>
> </td>
> <td>
>
>
> result code
>
> </td>
> </tr>
> <tr>
> <td>
>
>
>
>
> </td>
> <td colspan="2">
>
>
> `ETHTOOL_A_CABLE_NEST_RESULT`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> cable test results
>
> </td>
> </tr>
> <tr>
> <td>
>
>
>
>
> </td>
> <td>
>
>
>
>
> </td>
> <td>
>
>
> `ETHTOOL_A_CABLE_RESULTS_PAIR`
>
> </td>
> <td>
>
>
> u8
>
> </td>
> <td>
>
>
> pair number
>
> </td>
> </tr>
> <tr>
> <td>
>
>
>
>
> </td>
> <td>
>
>
>
>
> </td>
> <td>
>
>
> `ETHTOOL_A_CABLE_RESULTS_CODE`
>
> </td>
> <td>
>
>
> u8
>
> </td>
> <td>
>
>
> result code
>
> </td>
> </tr>
> <tr>
> <td>
>
>
>
>
> </td>
> <td>
>
>
>
>
> </td>
> <td>
>
>
> `ETHTOOL_A_CABLE_RESULT_SRC`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> information source
>
> </td>
> </tr>
> <tr>
> <td>
>
>
>
>
> </td>
> <td colspan="2">
>
>
> `ETHTOOL_A_CABLE_NEST_FAULT_LENGTH`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> cable length
>
> </td>
> </tr>
> <tr>
> <td>
>
>
>
>
> </td>
> <td>
>
>
>
>
> </td>
> <td>
>
>
> `ETHTOOL_A_CABLE_FAULT_LENGTH_PAIR`
>
> </td>
> <td>
>
>
> u8
>
> </td>
> <td>
>
>
> pair number
>
> </td>
> </tr>
> <tr>
> <td>
>
>
>
>
> </td>
> <td>
>
>
>
>
> </td>
> <td>
>
>
> `ETHTOOL_A_CABLE_FAULT_LENGTH_CM`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> length in cm
>
> </td>
> </tr>
> <tr>
> <td>
>
>
>
>
> </td>
> <td>
>
>
>
>
> </td>
> <td>
>
>
> `ETHTOOL_A_CABLE_FAULT_LENGTH_SRC`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> information source
>
> </td>
> </tr>
> </tbody>
> </table>

<a id="rst-cable-test-tdr"></a>

## CABLE_TEST TDR

Start a cable test and report raw TDR data

Request contents:

>
> <table>
> <tbody>
> <tr>
> <td colspan="3">
>
>
> `ETHTOOL_A_CABLE_TEST_TDR_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> reply header
>
> </td>
> </tr>
> <tr>
> <td colspan="3">
>
>
> `ETHTOOL_A_CABLE_TEST_TDR_CFG`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> test configuration
>
> </td>
> </tr>
> <tr>
> <td>
>
>
>
>
> </td>
> <td colspan="2">
>
>
> `ETHTOOL_A_CABLE_STEP_FIRST_DISTANCE`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> first data distance
>
> </td>
> </tr>
> <tr>
> <td>
>
>
>
>
> </td>
> <td colspan="2">
>
>
> `ETHTOOL_A_CABLE_STEP_LAST_DISTANCE`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> last data distance
>
> </td>
> </tr>
> <tr>
> <td>
>
>
>
>
> </td>
> <td colspan="2">
>
>
> `ETHTOOL_A_CABLE_STEP_STEP_DISTANCE`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> distance of each step
>
> </td>
> </tr>
> <tr>
> <td>
>
>
>
>
> </td>
> <td colspan="2">
>
>
> `ETHTOOL_A_CABLE_TEST_TDR_CFG_PAIR`
>
> </td>
> <td>
>
>
> u8
>
> </td>
> <td>
>
>
> pair to test
>
> </td>
> </tr>
> </tbody>
> </table>

The ETHTOOL_A_CABLE_TEST_TDR_CFG is optional, as well as all members of the nest. All distances are expressed in centimeters. The PHY takes the distances as a guide, and rounds to the nearest distance it actually supports. If a pair is passed, only that one pair will be tested. Otherwise all pairs are tested.

Notification contents:

Raw TDR data is gathered by sending a pulse down the cable and recording the amplitude of the reflected pulse for a given distance.

It can take a number of seconds to collect TDR data, especial if the full 100 meters is probed at 1 meter intervals. When the test is started a notification will be sent containing just ETHTOOL_A_CABLE_TEST_TDR_STATUS with the value ETHTOOL_A_CABLE_TEST_NTF_STATUS_STARTED.

When the test has completed a second notification will be sent containing ETHTOOL_A_CABLE_TEST_TDR_STATUS with the value ETHTOOL_A_CABLE_TEST_NTF_STATUS_COMPLETED and the TDR data.

The message may optionally contain the amplitude of the pulse send down the cable. This is measured in mV. A reflection should not be bigger than transmitted pulse.

Before the raw TDR data should be an ETHTOOL_A_CABLE_TDR_NEST_STEP nest containing information about the distance along the cable for the first reading, the last reading, and the step between each reading. Distances are measured in centimeters. These should be the exact values the PHY used. These may be different to what the user requested, if the native measurement resolution is greater than 1 cm.

For each step along the cable, a ETHTOOL_A_CABLE_TDR_NEST_AMPLITUDE is used to report the amplitude of the reflection for a given pair.

>
> <table>
> <tbody>
> <tr>
> <td colspan="3">
>
>
> `ETHTOOL_A_CABLE_TEST_TDR_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> reply header
>
> </td>
> </tr>
> <tr>
> <td colspan="3">
>
>
> `ETHTOOL_A_CABLE_TEST_TDR_STATUS`
>
> </td>
> <td>
>
>
> u8
>
> </td>
> <td>
>
>
> completed
>
> </td>
> </tr>
> <tr>
> <td colspan="3">
>
>
> `ETHTOOL_A_CABLE_TEST_TDR_NTF_NEST`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> all the results
>
> </td>
> </tr>
> <tr>
> <td>
>
>
>
>
> </td>
> <td colspan="2">
>
>
> `ETHTOOL_A_CABLE_TDR_NEST_PULSE`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> TX Pulse amplitude
>
> </td>
> </tr>
> <tr>
> <td>
>
>
>
>
> </td>
> <td>
>
>
>
>
> </td>
> <td>
>
>
> `ETHTOOL_A_CABLE_PULSE_mV`
>
> </td>
> <td>
>
>
> s16
>
> </td>
> <td>
>
>
> Pulse amplitude
>
> </td>
> </tr>
> <tr>
> <td>
>
>
>
>
> </td>
> <td colspan="2">
>
>
> `ETHTOOL_A_CABLE_NEST_STEP`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> TDR step info
>
> </td>
> </tr>
> <tr>
> <td>
>
>
>
>
> </td>
> <td>
>
>
>
>
> </td>
> <td>
>
>
> `ETHTOOL_A_CABLE_STEP_FIRST_DISTANCE`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> First data distance
>
> </td>
> </tr>
> <tr>
> <td>
>
>
>
>
> </td>
> <td>
>
>
>
>
> </td>
> <td>
>
>
> `ETHTOOL_A_CABLE_STEP_LAST_DISTANCE`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> Last data distance
>
> </td>
> </tr>
> <tr>
> <td>
>
>
>
>
> </td>
> <td>
>
>
>
>
> </td>
> <td>
>
>
> `ETHTOOL_A_CABLE_STEP_STEP_DISTANCE`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> distance of each step
>
> </td>
> </tr>
> <tr>
> <td>
>
>
>
>
> </td>
> <td colspan="2">
>
>
> `ETHTOOL_A_CABLE_TDR_NEST_AMPLITUDE`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> Reflection amplitude
>
> </td>
> </tr>
> <tr>
> <td>
>
>
>
>
> </td>
> <td>
>
>
>
>
> </td>
> <td>
>
>
> `ETHTOOL_A_CABLE_RESULTS_PAIR`
>
> </td>
> <td>
>
>
> u8
>
> </td>
> <td>
>
>
> pair number
>
> </td>
> </tr>
> <tr>
> <td>
>
>
>
>
> </td>
> <td>
>
>
>
>
> </td>
> <td>
>
>
> `ETHTOOL_A_CABLE_AMPLITUDE_mV`
>
> </td>
> <td>
>
>
> s16
>
> </td>
> <td>
>
>
> Reflection amplitude
>
> </td>
> </tr>
> <tr>
> <td>
>
>
>
>
> </td>
> <td colspan="2">
>
>
> `ETHTOOL_A_CABLE_TDR_NEST_AMPLITUDE`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> Reflection amplitude
>
> </td>
> </tr>
> <tr>
> <td>
>
>
>
>
> </td>
> <td>
>
>
>
>
> </td>
> <td>
>
>
> `ETHTOOL_A_CABLE_RESULTS_PAIR`
>
> </td>
> <td>
>
>
> u8
>
> </td>
> <td>
>
>
> pair number
>
> </td>
> </tr>
> <tr>
> <td>
>
>
>
>
> </td>
> <td>
>
>
>
>
> </td>
> <td>
>
>
> `ETHTOOL_A_CABLE_AMPLITUDE_mV`
>
> </td>
> <td>
>
>
> s16
>
> </td>
> <td>
>
>
> Reflection amplitude
>
> </td>
> </tr>
> <tr>
> <td>
>
>
>
>
> </td>
> <td colspan="2">
>
>
> `ETHTOOL_A_CABLE_TDR_NEST_AMPLITUDE`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> Reflection amplitude
>
> </td>
> </tr>
> <tr>
> <td>
>
>
>
>
> </td>
> <td>
>
>
>
>
> </td>
> <td>
>
>
> `ETHTOOL_A_CABLE_RESULTS_PAIR`
>
> </td>
> <td>
>
>
> u8
>
> </td>
> <td>
>
>
> pair number
>
> </td>
> </tr>
> <tr>
> <td>
>
>
>
>
> </td>
> <td>
>
>
>
>
> </td>
> <td>
>
>
> `ETHTOOL_A_CABLE_AMPLITUDE_mV`
>
> </td>
> <td>
>
>
> s16
>
> </td>
> <td>
>
>
> Reflection amplitude
>
> </td>
> </tr>
> </tbody>
> </table>

<a id="rst-tunnel-info"></a>

## TUNNEL_INFO

Gets information about the tunnel state NIC is aware of.

Request contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_TUNNEL_INFO_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> request header
>
> </td>
> </tr>
> </tbody>
> </table>

Kernel response contents:

>
> <table>
> <tbody>
> <tr>
> <td colspan="4">
>
>
> `ETHTOOL_A_TUNNEL_INFO_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> reply header
>
> </td>
> </tr>
> <tr>
> <td colspan="4">
>
>
> `ETHTOOL_A_TUNNEL_INFO_UDP_PORTS`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> all UDP port tables
>
> </td>
> </tr>
> <tr>
> <td>
>
>
>
>
> </td>
> <td colspan="3">
>
>
> `ETHTOOL_A_TUNNEL_UDP_TABLE`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> one UDP port table
>
> </td>
> </tr>
> <tr>
> <td>
>
>
>
>
> </td>
> <td>
>
>
>
>
> </td>
> <td colspan="2">
>
>
> `ETHTOOL_A_TUNNEL_UDP_TABLE_SIZE`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> max size of the table
>
> </td>
> </tr>
> <tr>
> <td>
>
>
>
>
> </td>
> <td>
>
>
>
>
> </td>
> <td colspan="2">
>
>
> `ETHTOOL_A_TUNNEL_UDP_TABLE_TYPES`
>
> </td>
> <td>
>
>
> bitset
>
> </td>
> <td>
>
>
> tunnel types which table can hold
>
> </td>
> </tr>
> <tr>
> <td>
>
>
>
>
> </td>
> <td>
>
>
>
>
> </td>
> <td colspan="2">
>
>
> `ETHTOOL_A_TUNNEL_UDP_TABLE_ENTRY`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> offloaded UDP port
>
> </td>
> </tr>
> <tr>
> <td>
>
>
>
>
> </td>
> <td>
>
>
>
>
> </td>
> <td>
>
>
>
>
> </td>
> <td>
>
>
> `ETHTOOL_A_TUNNEL_UDP_ENTRY_PORT`
>
> </td>
> <td>
>
>
> be16
>
> </td>
> <td>
>
>
> UDP port
>
> </td>
> </tr>
> <tr>
> <td>
>
>
>
>
> </td>
> <td>
>
>
>
>
> </td>
> <td>
>
>
>
>
> </td>
> <td>
>
>
> `ETHTOOL_A_TUNNEL_UDP_ENTRY_TYPE`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> tunnel type
>
> </td>
> </tr>
> </tbody>
> </table>

For UDP tunnel table empty `ETHTOOL_A_TUNNEL_UDP_TABLE_TYPES` indicates that the table contains static entries, hard-coded by the NIC.

<a id="rst-fec-get"></a>

## FEC_GET

Gets FEC configuration and state like `ETHTOOL_GFECPARAM` ioctl request.

Request contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_FEC_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> request header
>
> </td>
> </tr>
> </tbody>
> </table>

Kernel response contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_FEC_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> request header
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_FEC_MODES`
>
> </td>
> <td>
>
>
> bitset
>
> </td>
> <td>
>
>
> configured modes
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_FEC_AUTO`
>
> </td>
> <td>
>
>
> bool
>
> </td>
> <td>
>
>
> FEC mode auto selection
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_FEC_ACTIVE`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> index of active FEC mode
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_FEC_STATS`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> FEC statistics
>
> </td>
> </tr>
> </tbody>
> </table>

`ETHTOOL_A_FEC_ACTIVE` is the bit index of the FEC link mode currently active on the interface. This attribute may not be present if device does not support FEC.

`ETHTOOL_A_FEC_MODES` and `ETHTOOL_A_FEC_AUTO` are only meaningful when autonegotiation is disabled. If `ETHTOOL_A_FEC_AUTO` is non-zero driver will select the FEC mode automatically based on the parameters of the SFP module. This is equivalent to the `ETHTOOL_FEC_AUTO` bit of the ioctl interface. `ETHTOOL_A_FEC_MODES` carry the current FEC configuration using link mode bits (rather than old `ETHTOOL_FEC_*` bits).

`ETHTOOL_A_FEC_STATS` are reported if `ETHTOOL_FLAG_STATS` was set in `ETHTOOL_A_HEADER_FLAGS`. Each attribute carries an array of 64bit statistics. First entry in the array contains the total number of events on the port, while the following entries are counters corresponding to lanes/PCS instances. The number of entries in the array will be:


<table>
<tbody>
<tr>
<td>


`0`

</td>
<td>


device does not support FEC statistics

</td>
</tr>
<tr>
<td>


`1`

</td>
<td>


device does not support per-lane break down

</td>
</tr>
<tr>
<td>


`1 + #lanes`

</td>
<td>


device has full support for FEC stats

</td>
</tr>
</tbody>
</table>

Drivers fill in the statistics in the following structure:

```{kernel-doc} include/linux/ethtool.h
:identifiers: ethtool_fec_stats
```

Statistics may have FEC bins histogram attribute `ETHTOOL_A_FEC_STAT_HIST` as defined in IEEE 802.3ck-2022 and 802.3df-2024. Nested attributes will have the range of FEC errors in the bin (inclusive) and the amount of error events in the bin.

<a id="rst-fec-set"></a>

## FEC_SET

Sets FEC parameters like `ETHTOOL_SFECPARAM` ioctl request.

Request contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_FEC_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> request header
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_FEC_MODES`
>
> </td>
> <td>
>
>
> bitset
>
> </td>
> <td>
>
>
> configured modes
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_FEC_AUTO`
>
> </td>
> <td>
>
>
> bool
>
> </td>
> <td>
>
>
> FEC mode auto selection
>
> </td>
> </tr>
> </tbody>
> </table>

`FEC_SET` is only meaningful when autonegotiation is disabled. Otherwise FEC mode is selected as part of autonegotiation.

`ETHTOOL_A_FEC_MODES` selects which FEC mode should be used. It's recommended to set only one bit, if multiple bits are set driver may choose between them in an implementation specific way.

`ETHTOOL_A_FEC_AUTO` requests the driver to choose FEC mode based on SFP module parameters. This does not mean autonegotiation.

<a id="rst-module-eeprom-get"></a>

## MODULE_EEPROM_GET

Fetch module EEPROM data dump. This interface is designed to allow dumps of at most 1/2 page at once. This means only dumps of 128 (or less) bytes are allowed, without crossing half page boundary located at offset 128. For pages other than 0 only high 128 bytes are accessible.

Request contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_MODULE_EEPROM_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> request header
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_MODULE_EEPROM_OFFSET`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> offset within a page
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_MODULE_EEPROM_LENGTH`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> amount of bytes to read
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_MODULE_EEPROM_PAGE`
>
> </td>
> <td>
>
>
> u8
>
> </td>
> <td>
>
>
> page number
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_MODULE_EEPROM_BANK`
>
> </td>
> <td>
>
>
> u8
>
> </td>
> <td>
>
>
> bank number
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_MODULE_EEPROM_I2C_ADDRESS`
>
> </td>
> <td>
>
>
> u8
>
> </td>
> <td>
>
>
> page I2C address
>
> </td>
> </tr>
> </tbody>
> </table>

If `ETHTOOL_A_MODULE_EEPROM_BANK` is not specified, bank 0 is assumed.

Kernel response contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_MODULE_EEPROM_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> reply header
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_MODULE_EEPROM_DATA`
>
> </td>
> <td>
>
>
> binary
>
> </td>
> <td>
>
>
> array of bytes from module EEPROM
>
> </td>
> </tr>
> </tbody>
> </table>

`ETHTOOL_A_MODULE_EEPROM_DATA` has an attribute length equal to the amount of bytes driver actually read.

<a id="rst-stats-get"></a>

## STATS_GET

Get standard statistics for the interface. Note that this is not a re-implementation of `ETHTOOL_GSTATS` which exposed driver-defined stats.

Request contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_STATS_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> request header
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_STATS_SRC`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> source of statistics
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_STATS_GROUPS`
>
> </td>
> <td>
>
>
> bitset
>
> </td>
> <td>
>
>
> requested groups of stats
>
> </td>
> </tr>
> </tbody>
> </table>

Kernel response contents:

>
> <table>
> <tbody>
> <tr>
> <td colspan="2">
>
>
> `ETHTOOL_A_STATS_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> reply header
>
> </td>
> </tr>
> <tr>
> <td colspan="2">
>
>
> `ETHTOOL_A_STATS_SRC`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> source of statistics
>
> </td>
> </tr>
> <tr>
> <td colspan="2">
>
>
> `ETHTOOL_A_STATS_GRP`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> one or more group of stats
>
> </td>
> </tr>
> <tr>
> <td>
>
>
>
>
> </td>
> <td>
>
>
> `ETHTOOL_A_STATS_GRP_ID`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> group ID - `ETHTOOL_STATS_*`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
>
>
> </td>
> <td>
>
>
> `ETHTOOL_A_STATS_GRP_SS_ID`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> string set ID for names
>
> </td>
> </tr>
> <tr>
> <td>
>
>
>
>
> </td>
> <td>
>
>
> `ETHTOOL_A_STATS_GRP_STAT`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> nest containing a statistic
>
> </td>
> </tr>
> <tr>
> <td>
>
>
>
>
> </td>
> <td>
>
>
> `ETHTOOL_A_STATS_GRP_HIST_RX`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> histogram statistic (Rx)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
>
>
> </td>
> <td>
>
>
> `ETHTOOL_A_STATS_GRP_HIST_TX`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> histogram statistic (Tx)
>
> </td>
> </tr>
> </tbody>
> </table>

Users specify which groups of statistics they are requesting via the `ETHTOOL_A_STATS_GROUPS` bitset. Currently defined values are:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> ETHTOOL_STATS_ETH_MAC
>
> </td>
> <td>
>
>
> eth-mac
>
> </td>
> <td>
>
>
> Basic IEEE 802.3 MAC statistics (30.3.1.1.\*)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> ETHTOOL_STATS_ETH_PHY
>
> </td>
> <td>
>
>
> eth-phy
>
> </td>
> <td>
>
>
> Basic IEEE 802.3 PHY statistics (30.3.2.1.\*)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> ETHTOOL_STATS_ETH_CTRL
>
> </td>
> <td>
>
>
> eth-ctrl
>
> </td>
> <td>
>
>
> Basic IEEE 802.3 MAC Ctrl statistics (30.3.3.\*)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> ETHTOOL_STATS_RMON
>
> </td>
> <td>
>
>
> rmon
>
> </td>
> <td>
>
>
> RMON (RFC 2819) statistics
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> ETHTOOL_STATS_PHY
>
> </td>
> <td>
>
>
> phy
>
> </td>
> <td>
>
>
> Additional PHY statistics, not defined by IEEE
>
> </td>
> </tr>
> </tbody>
> </table>

Each group should have a corresponding `ETHTOOL_A_STATS_GRP` in the reply. `ETHTOOL_A_STATS_GRP_ID` identifies which group's statistics nest contains. `ETHTOOL_A_STATS_GRP_SS_ID` identifies the string set ID for the names of the statistics in the group, if available.

Statistics are added to the `ETHTOOL_A_STATS_GRP` nest under `ETHTOOL_A_STATS_GRP_STAT`. `ETHTOOL_A_STATS_GRP_STAT` should contain single 8 byte (u64) attribute inside - the type of that attribute is the statistic ID and the value is the value of the statistic. Each group has its own interpretation of statistic IDs. Attribute IDs correspond to strings from the string set identified by `ETHTOOL_A_STATS_GRP_SS_ID`. Complex statistics (such as RMON histogram entries) are also listed inside `ETHTOOL_A_STATS_GRP` and do not have a string defined in the string set.

RMON "histogram" counters count number of packets within given size range. Because RFC does not specify the ranges beyond the standard 1518 MTU devices differ in definition of buckets. For this reason the definition of packet ranges is left to each driver.

`ETHTOOL_A_STATS_GRP_HIST_RX` and `ETHTOOL_A_STATS_GRP_HIST_TX` nests contain the following attributes:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> ETHTOOL_A_STATS_RMON_HIST_BKT_LOW
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> low bound of the packet size bucket
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> ETHTOOL_A_STATS_RMON_HIST_BKT_HI
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> high bound of the bucket
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> ETHTOOL_A_STATS_RMON_HIST_VAL
>
> </td>
> <td>
>
>
> u64
>
> </td>
> <td>
>
>
> packet counter
>
> </td>
> </tr>
> </tbody>
> </table>

Low and high bounds are inclusive, for example:

>
> <table>
> <thead>
> <tr>
> <th>
>
>
> RFC statistic
>
> </th>
> <th>
>
>
> low
>
> </th>
> <th>
>
>
> high
>
> </th>
> </tr>
> </thead>
> <tbody>
> <tr>
> <td>
>
>
> etherStatsPkts64Octets
>
> </td>
> <td>
>
>
> 0
>
> </td>
> <td>
>
>
> 64
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> etherStatsPkts512to1023Octets
>
> </td>
> <td>
>
>
> 512
>
> </td>
> <td>
>
>
> 1023
>
> </td>
> </tr>
> </tbody>
> </table>

`ETHTOOL_A_STATS_SRC` is optional. Similar to `PAUSE_GET`, it takes values from `enum ethtool_mac_stats_src`. If absent from the request, stats will be provided with an `ETHTOOL_A_STATS_SRC` attribute in the response equal to `ETHTOOL_MAC_STATS_SRC_AGGREGATE`.

<a id="rst-phc-vclocks-get"></a>

## PHC_VCLOCKS_GET

Query device PHC virtual clocks information.

Request contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_PHC_VCLOCKS_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> request header
>
> </td>
> </tr>
> </tbody>
> </table>

Kernel response contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_PHC_VCLOCKS_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> reply header
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_PHC_VCLOCKS_NUM`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> PHC virtual clocks number
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_PHC_VCLOCKS_INDEX`
>
> </td>
> <td>
>
>
> s32
>
> </td>
> <td>
>
>
> PHC index array
>
> </td>
> </tr>
> </tbody>
> </table>

<a id="rst-module-get"></a>

## MODULE_GET

Gets transceiver module parameters.

Request contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_MODULE_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> request header
>
> </td>
> </tr>
> </tbody>
> </table>

Kernel response contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_MODULE_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> reply header
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_MODULE_POWER_MODE_POLICY`
>
> </td>
> <td>
>
>
> u8
>
> </td>
> <td>
>
>
> power mode policy
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_MODULE_POWER_MODE`
>
> </td>
> <td>
>
>
> u8
>
> </td>
> <td>
>
>
> operational power mode
>
> </td>
> </tr>
> </tbody>
> </table>

The optional `ETHTOOL_A_MODULE_POWER_MODE_POLICY` attribute encodes the transceiver module power mode policy enforced by the host. The default policy is driver-dependent, but "auto" is the recommended default and it should be implemented by new drivers and drivers where conformance to a legacy behavior is not critical.

The optional `ETHTHOOL_A_MODULE_POWER_MODE` attribute encodes the operational power mode policy of the transceiver module. It is only reported when a module is plugged-in. Possible values are:

```{kernel-doc} include/uapi/linux/ethtool.h
:identifiers: ethtool_module_power_mode
```

<a id="rst-module-set"></a>

## MODULE_SET

Sets transceiver module parameters.

Request contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_MODULE_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> request header
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_MODULE_POWER_MODE_POLICY`
>
> </td>
> <td>
>
>
> u8
>
> </td>
> <td>
>
>
> power mode policy
>
> </td>
> </tr>
> </tbody>
> </table>

When set, the optional `ETHTOOL_A_MODULE_POWER_MODE_POLICY` attribute is used to set the transceiver module power policy enforced by the host. Possible values are:

```{kernel-doc} include/uapi/linux/ethtool.h
:identifiers: ethtool_module_power_mode_policy
```

For SFF-8636 modules, low power mode is forced by the host according to table 6-10 in revision 2.10a of the specification.

For CMIS modules, low power mode is forced by the host according to table 6-12 in revision 5.0 of the specification.

<a id="rst-pse-get"></a>

## PSE_GET

Gets PSE attributes.

Request contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_PSE_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> request header
>
> </td>
> </tr>
> </tbody>
> </table>

Kernel response contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_PSE_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> reply header
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_PODL_PSE_ADMIN_STATE`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> Operational state of the PoDL PSE functions
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_PODL_PSE_PW_D_STATUS`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> power detection status of the PoDL PSE.
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_C33_PSE_ADMIN_STATE`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> Operational state of the PoE PSE functions.
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_C33_PSE_PW_D_STATUS`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> power detection status of the PoE PSE.
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_C33_PSE_PW_CLASS`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> power class of the PoE PSE.
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_C33_PSE_ACTUAL_PW`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> actual power drawn on the PoE PSE.
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_C33_PSE_EXT_STATE`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> power extended state of the PoE PSE.
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_C33_PSE_EXT_SUBSTATE`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> power extended substatus of the PoE PSE.
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_C33_PSE_AVAIL_PW_LIMIT`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> currently configured power limit of the PoE PSE.
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_C33_PSE_PW_LIMIT_RANGES`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> Supported power limit configuration ranges.
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_PSE_PW_D_ID`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> Index of the PSE power domain
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_PSE_PRIO_MAX`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> Priority maximum configurable on the PoE PSE
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_PSE_PRIO`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> Priority of the PoE PSE currently configured
>
> </td>
> </tr>
> </tbody>
> </table>

When set, the optional `ETHTOOL_A_PODL_PSE_ADMIN_STATE` attribute identifies the operational state of the PoDL PSE functions.  The operational state of the PSE function can be changed using the `ETHTOOL_A_PODL_PSE_ADMIN_CONTROL` action. This attribute corresponds to `IEEE 802.3-2018` 30.15.1.1.2 aPoDLPSEAdminState. Possible values are:

```{kernel-doc} include/uapi/linux/ethtool.h
:identifiers: ethtool_podl_pse_admin_state
```

The same goes for `ETHTOOL_A_C33_PSE_ADMIN_STATE` implementing `IEEE 802.3-2022` 30.9.1.1.2 aPSEAdminState.

```{kernel-doc} include/uapi/linux/ethtool.h
:identifiers: ethtool_c33_pse_admin_state
```

When set, the optional `ETHTOOL_A_PODL_PSE_PW_D_STATUS` attribute identifies the power detection status of the PoDL PSE.  The status depend on internal PSE state machine and automatic PD classification support. This attribute corresponds to `IEEE 802.3-2018` 30.15.1.1.3 aPoDLPSEPowerDetectionStatus. Possible values are:

```{kernel-doc} include/uapi/linux/ethtool.h
:identifiers: ethtool_podl_pse_pw_d_status
```

The same goes for `ETHTOOL_A_C33_PSE_ADMIN_PW_D_STATUS` implementing `IEEE 802.3-2022` 30.9.1.1.5 aPSEPowerDetectionStatus.

```{kernel-doc} include/uapi/linux/ethtool.h
:identifiers: ethtool_c33_pse_pw_d_status
```

When set, the optional `ETHTOOL_A_C33_PSE_PW_CLASS` attribute identifies the power class of the C33 PSE. It depends on the class negotiated between the PSE and the PD. This attribute corresponds to `IEEE 802.3-2022` 30.9.1.1.8 aPSEPowerClassification.

When set, the optional `ETHTOOL_A_C33_PSE_ACTUAL_PW` attribute identifies the actual power drawn by the C33 PSE. This attribute corresponds to `IEEE 802.3-2022` 30.9.1.1.23 aPSEActualPower. Actual power is reported in mW.

When set, the optional `ETHTOOL_A_C33_PSE_EXT_STATE` attribute identifies the extended error state of the C33 PSE. Possible values are:

```{kernel-doc} include/uapi/linux/ethtool.h
:identifiers: ethtool_c33_pse_ext_state
```

When set, the optional `ETHTOOL_A_C33_PSE_EXT_SUBSTATE` attribute identifies the extended error state of the C33 PSE. Possible values are: Possible values are:

```{kernel-doc} include/uapi/linux/ethtool.h
:identifiers: ethtool_c33_pse_ext_substate_class_num_events ethtool_c33_pse_ext_substate_error_condition ethtool_c33_pse_ext_substate_mr_pse_enable ethtool_c33_pse_ext_substate_option_detect_ted ethtool_c33_pse_ext_substate_option_vport_lim ethtool_c33_pse_ext_substate_ovld_detected ethtool_c33_pse_ext_substate_pd_dll_power_type ethtool_c33_pse_ext_substate_power_not_available ethtool_c33_pse_ext_substate_short_detected
```

When set, the optional `ETHTOOL_A_C33_PSE_AVAIL_PW_LIMIT` attribute identifies the C33 PSE power limit in mW.

When set the optional `ETHTOOL_A_C33_PSE_PW_LIMIT_RANGES` nested attribute identifies the C33 PSE power limit ranges through `ETHTOOL_A_C33_PSE_PWR_VAL_LIMIT_RANGE_MIN` and `ETHTOOL_A_C33_PSE_PWR_VAL_LIMIT_RANGE_MAX`. If the controller works with fixed classes, the min and max values will be equal.

The `ETHTOOL_A_PSE_PW_D_ID` attribute identifies the index of PSE power domain.

When set, the optional `ETHTOOL_A_PSE_PRIO_MAX` attribute identifies the PSE maximum priority value. When set, the optional `ETHTOOL_A_PSE_PRIO` attributes is used to identifies the currently configured PSE priority. For a description of PSE priority attributes, see `PSE_SET`.

<a id="rst-pse-set"></a>

## PSE_SET

Sets PSE parameters.

Request contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_PSE_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> request header
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_PODL_PSE_ADMIN_CONTROL`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> Control PoDL PSE Admin state
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_C33_PSE_ADMIN_CONTROL`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> Control PSE Admin state
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_C33_PSE_AVAIL_PWR_LIMIT`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> Control PoE PSE available power limit
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_PSE_PRIO`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> Control priority of the PoE PSE
>
> </td>
> </tr>
> </tbody>
> </table>

When set, the optional `ETHTOOL_A_PODL_PSE_ADMIN_CONTROL` attribute is used to control PoDL PSE Admin functions. This option implements `IEEE 802.3-2018` 30.15.1.2.1 acPoDLPSEAdminControl. See `ETHTOOL_A_PODL_PSE_ADMIN_STATE` for supported values.

The same goes for `ETHTOOL_A_C33_PSE_ADMIN_CONTROL` implementing `IEEE 802.3-2022` 30.9.1.2.1 acPSEAdminControl.

When set, the optional `ETHTOOL_A_C33_PSE_AVAIL_PWR_LIMIT` attribute is used to control the available power value limit for C33 PSE in milliwatts. This attribute corresponds  to the `pse_available_power` variable described in `IEEE 802.3-2022` 33.2.4.4 Variables  and `pse_avail_pwr` in 145.2.5.4 Variables, which are described in power classes.

It was decided to use milliwatts for this interface to unify it with other power monitoring interfaces, which also use milliwatts, and to align with various existing products that document power consumption in watts rather than classes. If power limit configuration based on classes is needed, the conversion can be done in user space, for example by ethtool.

When set, the optional `ETHTOOL_A_PSE_PRIO` attributes is used to control the PSE priority. Allowed priority value are between zero and the value of `ETHTOOL_A_PSE_PRIO_MAX` attribute.

A lower value indicates a higher priority, meaning that a priority value of 0 corresponds to the highest port priority. Port priority serves two functions:

> - Power-up Order: After a reset, ports are powered up in order of their priority from highest to lowest. Ports with higher priority (lower values) power up first.
>
> - Shutdown Order: When the power budget is exceeded, ports with lower priority (higher values) are turned off first.

<a id="rst-pse-ntf"></a>

## PSE_NTF

Notify PSE events.

Notification contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_PSE_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> request header
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_PSE_EVENTS`
>
> </td>
> <td>
>
>
> bitset
>
> </td>
> <td>
>
>
> PSE events
>
> </td>
> </tr>
> </tbody>
> </table>

When set, the optional `ETHTOOL_A_PSE_EVENTS` attribute identifies the PSE events.

```{kernel-doc} include/uapi/linux/ethtool_netlink_generated.h
:identifiers: ethtool_pse_event
```

<a id="rst-rss-get"></a>

## RSS_GET

Get indirection table, hash key and hash function info associated with a RSS context of an interface similar to `ETHTOOL_GRSSH` ioctl request.

Request contents:


<table>
<tbody>
<tr>
<td>


`ETHTOOL_A_RSS_HEADER`

</td>
<td>


nested

</td>
<td>


request header

</td>
</tr>
<tr>
<td>


`ETHTOOL_A_RSS_CONTEXT`

</td>
<td>


u32

</td>
<td>


context number

</td>
</tr>
<tr>
<td>


`ETHTOOL_A_RSS_START_CONTEXT`

</td>
<td>


u32

</td>
<td>


start context number (dumps)

</td>
</tr>
</tbody>
</table>

`ETHTOOL_A_RSS_CONTEXT` specifies which RSS context number to query, if not set context 0 (the main context) is queried. Dumps can be filtered by device (only listing contexts of a given netdev). Filtering single context number is not supported but `ETHTOOL_A_RSS_START_CONTEXT` can be used to start dumping context from the given number (primarily used to ignore context 0s and only dump additional contexts).

Kernel response contents:


<table>
<tbody>
<tr>
<td>


`ETHTOOL_A_RSS_HEADER`

</td>
<td>


nested

</td>
<td>


reply header

</td>
</tr>
<tr>
<td>


`ETHTOOL_A_RSS_CONTEXT`

</td>
<td>


u32

</td>
<td>


context number

</td>
</tr>
<tr>
<td>


`ETHTOOL_A_RSS_HFUNC`

</td>
<td>


u32

</td>
<td>


RSS hash func

</td>
</tr>
<tr>
<td>


`ETHTOOL_A_RSS_INDIR`

</td>
<td>


binary

</td>
<td>


Indir table bytes

</td>
</tr>
<tr>
<td>


`ETHTOOL_A_RSS_HKEY`

</td>
<td>


binary

</td>
<td>


Hash key bytes

</td>
</tr>
<tr>
<td>


`ETHTOOL_A_RSS_INPUT_XFRM`

</td>
<td>


u32

</td>
<td>


RSS input data transformation

</td>
</tr>
<tr>
<td>


`ETHTOOL_A_RSS_FLOW_HASH`

</td>
<td>


nested

</td>
<td>


Header fields included in hash

</td>
</tr>
</tbody>
</table>

ETHTOOL_A_RSS_HFUNC attribute is bitmap indicating the hash function being used. Current supported options are toeplitz, xor or crc32. ETHTOOL_A_RSS_INDIR attribute returns RSS indirection table where each byte indicates queue number. ETHTOOL_A_RSS_INPUT_XFRM attribute is a bitmap indicating the type of transformation applied to the input protocol fields before given to the RSS hfunc. Current supported options are symmetric-xor and symmetric-or-xor. ETHTOOL_A_RSS_FLOW_HASH carries per-flow type bitmask of which header fields are included in the hash calculation.

<a id="rst-rss-set"></a>

## RSS_SET

Request contents:


<table>
<tbody>
<tr>
<td>


`ETHTOOL_A_RSS_HEADER`

</td>
<td>


nested

</td>
<td>


request header

</td>
</tr>
<tr>
<td>


`ETHTOOL_A_RSS_CONTEXT`

</td>
<td>


u32

</td>
<td>


context number

</td>
</tr>
<tr>
<td>


`ETHTOOL_A_RSS_HFUNC`

</td>
<td>


u32

</td>
<td>


RSS hash func

</td>
</tr>
<tr>
<td>


`ETHTOOL_A_RSS_INDIR`

</td>
<td>


binary

</td>
<td>


Indir table bytes

</td>
</tr>
<tr>
<td>


`ETHTOOL_A_RSS_HKEY`

</td>
<td>


binary

</td>
<td>


Hash key bytes

</td>
</tr>
<tr>
<td>


`ETHTOOL_A_RSS_INPUT_XFRM`

</td>
<td>


u32

</td>
<td>


RSS input data transformation

</td>
</tr>
<tr>
<td>


`ETHTOOL_A_RSS_FLOW_HASH`

</td>
<td>


nested

</td>
<td>


Header fields included in hash

</td>
</tr>
</tbody>
</table>

`ETHTOOL_A_RSS_INDIR` is the minimal RSS table the user expects. Kernel and the device driver may replicate the table if its smaller than smallest table size supported by the device. For example if user requests `[0, 1]` but the device needs at least 8 entries - the real table in use will end up being `[0, 1, 0, 1, 0, 1, 0, 1]`. Most devices require the table size to be power of 2, so tables which size is not a power of 2 will likely be rejected. Using table of size 0 will reset the indirection table to the default.

<a id="rst-rss-create-act"></a>

## RSS_CREATE_ACT

Request contents:


<table>
<tbody>
<tr>
<td>


`ETHTOOL_A_RSS_HEADER`

</td>
<td>


nested

</td>
<td>


request header

</td>
</tr>
<tr>
<td>


`ETHTOOL_A_RSS_CONTEXT`

</td>
<td>


u32

</td>
<td>


context number

</td>
</tr>
<tr>
<td>


`ETHTOOL_A_RSS_HFUNC`

</td>
<td>


u32

</td>
<td>


RSS hash func

</td>
</tr>
<tr>
<td>


`ETHTOOL_A_RSS_INDIR`

</td>
<td>


binary

</td>
<td>


Indir table bytes

</td>
</tr>
<tr>
<td>


`ETHTOOL_A_RSS_HKEY`

</td>
<td>


binary

</td>
<td>


Hash key bytes

</td>
</tr>
<tr>
<td>


`ETHTOOL_A_RSS_INPUT_XFRM`

</td>
<td>


u32

</td>
<td>


RSS input data transformation

</td>
</tr>
</tbody>
</table>

Kernel response contents:


<table>
<tbody>
<tr>
<td>


`ETHTOOL_A_RSS_HEADER`

</td>
<td>


nested

</td>
<td>


request header

</td>
</tr>
<tr>
<td>


`ETHTOOL_A_RSS_CONTEXT`

</td>
<td>


u32

</td>
<td>


context number

</td>
</tr>
</tbody>
</table>

Create an additional RSS context, if `ETHTOOL_A_RSS_CONTEXT` is not specified kernel will allocate one automatically.

<a id="rst-rss-delete-act"></a>

## RSS_DELETE_ACT

Request contents:


<table>
<tbody>
<tr>
<td>


`ETHTOOL_A_RSS_HEADER`

</td>
<td>


nested

</td>
<td>


request header

</td>
</tr>
<tr>
<td>


`ETHTOOL_A_RSS_CONTEXT`

</td>
<td>


u32

</td>
<td>


context number

</td>
</tr>
</tbody>
</table>

Delete an additional RSS context.

<a id="rst-plca-get-cfg"></a>

## PLCA_GET_CFG

Gets the IEEE 802.3cg-2019 Clause 148 Physical Layer Collision Avoidance (PLCA) Reconciliation Sublayer (RS) attributes.

Request contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_PLCA_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> request header
>
> </td>
> </tr>
> </tbody>
> </table>

Kernel response contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_PLCA_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> reply header
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_PLCA_VERSION`
>
> </td>
> <td>
>
>
> u16
>
> </td>
> <td>
>
>
> Supported PLCA management interface standard/version
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_PLCA_ENABLED`
>
> </td>
> <td>
>
>
> u8
>
> </td>
> <td>
>
>
> PLCA Admin State
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_PLCA_NODE_ID`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> PLCA unique local node ID
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_PLCA_NODE_CNT`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> Number of PLCA nodes on the network, including the coordinator
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_PLCA_TO_TMR`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> Transmit Opportunity Timer value in bit-times (BT)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_PLCA_BURST_CNT`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> Number of additional packets the node is allowed to send within a single TO
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_PLCA_BURST_TMR`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> Time to wait for the MAC to transmit a new frame before terminating the burst
>
> </td>
> </tr>
> </tbody>
> </table>

When set, the optional `ETHTOOL_A_PLCA_VERSION` attribute indicates which standard and version the PLCA management interface complies to. When not set, the interface is vendor-specific and (possibly) supplied by the driver. The OPEN Alliance SIG specifies a standard register map for 10BASE-T1S PHYs embedding the PLCA Reconciliation Sublayer. See "10BASE-T1S PLCA Management Registers" at [https://www.opensig.org/about/specifications/](<https://www.opensig.org/about/specifications/>).

When set, the optional `ETHTOOL_A_PLCA_ENABLED` attribute indicates the administrative state of the PLCA RS. When not set, the node operates in "plain" CSMA/CD mode. This option is corresponding to `IEEE 802.3cg-2019` 30.16.1.1.1 aPLCAAdminState / 30.16.1.2.1 acPLCAAdminControl.

When set, the optional `ETHTOOL_A_PLCA_NODE_ID` attribute indicates the configured local node ID of the PHY. This ID determines which transmit opportunity (TO) is reserved for the node to transmit into. This option is corresponding to `IEEE 802.3cg-2019` 30.16.1.1.4 aPLCALocalNodeID. The valid range for this attribute is \[0 .. 255\] where 255 means "not configured".

When set, the optional `ETHTOOL_A_PLCA_NODE_CNT` attribute indicates the configured maximum number of PLCA nodes on the mixing-segment. This number determines the total number of transmit opportunities generated during a PLCA cycle. This attribute is relevant only for the PLCA coordinator, which is the node with aPLCALocalNodeID set to 0. Follower nodes ignore this setting. This option is corresponding to `IEEE 802.3cg-2019` 30.16.1.1.3 aPLCANodeCount. The valid range for this attribute is \[1 .. 255\].

When set, the optional `ETHTOOL_A_PLCA_TO_TMR` attribute indicates the configured value of the transmit opportunity timer in bit-times. This value must be set equal across all nodes sharing the medium for PLCA to work correctly. This option is corresponding to `IEEE 802.3cg-2019` 30.16.1.1.5 aPLCATransmitOpportunityTimer. The valid range for this attribute is \[0 .. 255\].

When set, the optional `ETHTOOL_A_PLCA_BURST_CNT` attribute indicates the configured number of extra packets that the node is allowed to send during a single transmit opportunity. By default, this attribute is 0, meaning that the node can only send a single frame per TO. When greater than 0, the PLCA RS keeps the TO after any transmission, waiting for the MAC to send a new frame for up to aPLCABurstTimer BTs. This can only happen a number of times per PLCA cycle up to the value of this parameter. After that, the burst is over and the normal counting of TOs resumes. This option is corresponding to `IEEE 802.3cg-2019` 30.16.1.1.6 aPLCAMaxBurstCount. The valid range for this attribute is \[0 .. 255\].

When set, the optional `ETHTOOL_A_PLCA_BURST_TMR` attribute indicates how many bit-times the PLCA RS waits for the MAC to initiate a new transmission when aPLCAMaxBurstCount is greater than 0. If the MAC fails to send a new frame within this time, the burst ends and the counting of TOs resumes. Otherwise, the new frame is sent as part of the current burst. This option is corresponding to `IEEE 802.3cg-2019` 30.16.1.1.7 aPLCABurstTimer. The valid range for this attribute is \[0 .. 255\]. Although, the value should be set greater than the Inter-Frame-Gap (IFG) time of the MAC (plus some margin) for PLCA burst mode to work as intended.

<a id="rst-plca-set-cfg"></a>

## PLCA_SET_CFG

Sets PLCA RS parameters.

Request contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_PLCA_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> request header
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_PLCA_ENABLED`
>
> </td>
> <td>
>
>
> u8
>
> </td>
> <td>
>
>
> PLCA Admin State
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_PLCA_NODE_ID`
>
> </td>
> <td>
>
>
> u8
>
> </td>
> <td>
>
>
> PLCA unique local node ID
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_PLCA_NODE_CNT`
>
> </td>
> <td>
>
>
> u8
>
> </td>
> <td>
>
>
> Number of PLCA nodes on the network, including the coordinator
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_PLCA_TO_TMR`
>
> </td>
> <td>
>
>
> u8
>
> </td>
> <td>
>
>
> Transmit Opportunity Timer value in bit-times (BT)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_PLCA_BURST_CNT`
>
> </td>
> <td>
>
>
> u8
>
> </td>
> <td>
>
>
> Number of additional packets the node is allowed to send within a single TO
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_PLCA_BURST_TMR`
>
> </td>
> <td>
>
>
> u8
>
> </td>
> <td>
>
>
> Time to wait for the MAC to transmit a new frame before terminating the burst
>
> </td>
> </tr>
> </tbody>
> </table>

For a description of each attribute, see `PLCA_GET_CFG`.

<a id="rst-plca-get-status"></a>

## PLCA_GET_STATUS

Gets PLCA RS status information.

Request contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_PLCA_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> request header
>
> </td>
> </tr>
> </tbody>
> </table>

Kernel response contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_PLCA_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> reply header
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_PLCA_STATUS`
>
> </td>
> <td>
>
>
> u8
>
> </td>
> <td>
>
>
> PLCA RS operational status
>
> </td>
> </tr>
> </tbody>
> </table>

When set, the `ETHTOOL_A_PLCA_STATUS` attribute indicates whether the node is detecting the presence of the BEACON on the network. This flag is corresponding to `IEEE 802.3cg-2019` 30.16.1.1.2 aPLCAStatus.

<a id="rst-mm-get"></a>

## MM_GET

Retrieve 802.3 MAC Merge parameters.

Request contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_MM_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> request header
>
> </td>
> </tr>
> </tbody>
> </table>

Kernel response contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_MM_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> request header
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_MM_PMAC_ENABLED`
>
> </td>
> <td>
>
>
> bool
>
> </td>
> <td>
>
>
> set if RX of preemptible and SMD-V frames is enabled
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_MM_TX_ENABLED`
>
> </td>
> <td>
>
>
> bool
>
> </td>
> <td>
>
>
> set if TX of preemptible frames is administratively enabled (might be inactive if verification failed)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_MM_TX_ACTIVE`
>
> </td>
> <td>
>
>
> bool
>
> </td>
> <td>
>
>
> set if TX of preemptible frames is operationally enabled
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_MM_TX_MIN_FRAG_SIZE`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> minimum size of transmitted non-final fragments, in octets
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_MM_RX_MIN_FRAG_SIZE`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> minimum size of received non-final fragments, in octets
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_MM_VERIFY_ENABLED`
>
> </td>
> <td>
>
>
> bool
>
> </td>
> <td>
>
>
> set if TX of SMD-V frames is administratively enabled
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_MM_VERIFY_STATUS`
>
> </td>
> <td>
>
>
> u8
>
> </td>
> <td>
>
>
> state of the verification function
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_MM_VERIFY_TIME`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> delay between verification attempts
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `` ETHTOOL_A_MM_MAX_VERIFY_TIME` ``
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> maximum verification interval supported by device
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_MM_STATS`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> IEEE 802.3-2018 subclause 30.14.1 oMACMergeEntity statistics counters
>
> </td>
> </tr>
> </tbody>
> </table>

The attributes are populated by the device driver through the following structure:

```{kernel-doc} include/linux/ethtool.h
:identifiers: ethtool_mm_state
```

The `ETHTOOL_A_MM_VERIFY_STATUS` will report one of the values from

```{kernel-doc} include/uapi/linux/ethtool.h
:identifiers: ethtool_mm_verify_status
```

If `ETHTOOL_A_MM_VERIFY_ENABLED` was passed as false in the `MM_SET` command, `ETHTOOL_A_MM_VERIFY_STATUS` will report either `ETHTOOL_MM_VERIFY_STATUS_INITIAL` or `ETHTOOL_MM_VERIFY_STATUS_DISABLED`, otherwise it should report one of the other states.

It is recommended that drivers start with the pMAC disabled, and enable it upon user space request. It is also recommended that user space does not depend upon the default values from `ETHTOOL_MSG_MM_GET` requests.

`ETHTOOL_A_MM_STATS` are reported if `ETHTOOL_FLAG_STATS` was set in `ETHTOOL_A_HEADER_FLAGS`. The attribute will be empty if driver did not report any statistics. Drivers fill in the statistics in the following structure:

```{kernel-doc} include/linux/ethtool.h
:identifiers: ethtool_mm_stats
```

<a id="rst-mm-set"></a>

## MM_SET

Modifies the configuration of the 802.3 MAC Merge layer.

Request contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_MM_VERIFY_TIME`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> see MM_GET description
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_MM_VERIFY_ENABLED`
>
> </td>
> <td>
>
>
> bool
>
> </td>
> <td>
>
>
> see MM_GET description
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_MM_TX_ENABLED`
>
> </td>
> <td>
>
>
> bool
>
> </td>
> <td>
>
>
> see MM_GET description
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_MM_PMAC_ENABLED`
>
> </td>
> <td>
>
>
> bool
>
> </td>
> <td>
>
>
> see MM_GET description
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_MM_TX_MIN_FRAG_SIZE`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> see MM_GET description
>
> </td>
> </tr>
> </tbody>
> </table>

The attributes are propagated to the driver through the following structure:

```{kernel-doc} include/linux/ethtool.h
:identifiers: ethtool_mm_cfg
```

<a id="rst-module-fw-flash-act"></a>

## MODULE_FW_FLASH_ACT

Flashes transceiver module firmware.

Request contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_MODULE_FW_FLASH_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> request header
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_MODULE_FW_FLASH_FILE_NAME`
>
> </td>
> <td>
>
>
> string
>
> </td>
> <td>
>
>
> firmware image file name
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_MODULE_FW_FLASH_PASSWORD`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> transceiver module password
>
> </td>
> </tr>
> </tbody>
> </table>

The firmware update process consists of three logical steps:

1. Downloading a firmware image to the transceiver module and validating it.

2. Running the firmware image.

3. Committing the firmware image so that it is run upon reset.

When flash command is given, those three steps are taken in that order.

This message merely schedules the update process and returns immediately without blocking. The process then runs asynchronously. Since it can take several minutes to complete, during the update process notifications are emitted from the kernel to user space updating it about the status and progress.

The `ETHTOOL_A_MODULE_FW_FLASH_FILE_NAME` attribute encodes the firmware image file name. The firmware image is downloaded to the transceiver module, validated, run and committed.

The optional `ETHTOOL_A_MODULE_FW_FLASH_PASSWORD` attribute encodes a password that might be required as part of the transceiver module firmware update process.

The firmware update process can take several minutes to complete. Therefore, during the update process notifications are emitted from the kernel to user space updating it about the status and progress.

Notification contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_MODULE_FW_FLASH_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> reply header
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_MODULE_FW_FLASH_STATUS`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> status
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_MODULE_FW_FLASH_STATUS_MSG`
>
> </td>
> <td>
>
>
> string
>
> </td>
> <td>
>
>
> status message
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_MODULE_FW_FLASH_DONE`
>
> </td>
> <td>
>
>
> uint
>
> </td>
> <td>
>
>
> progress
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_MODULE_FW_FLASH_TOTAL`
>
> </td>
> <td>
>
>
> uint
>
> </td>
> <td>
>
>
> total
>
> </td>
> </tr>
> </tbody>
> </table>

The `ETHTOOL_A_MODULE_FW_FLASH_STATUS` attribute encodes the current status of the firmware update process. Possible values are:

```{kernel-doc} include/uapi/linux/ethtool.h
:identifiers: ethtool_module_fw_flash_status
```

The `ETHTOOL_A_MODULE_FW_FLASH_STATUS_MSG` attribute encodes a status message string.

The `ETHTOOL_A_MODULE_FW_FLASH_DONE` and `ETHTOOL_A_MODULE_FW_FLASH_TOTAL` attributes encode the completed and total amount of work, respectively.

<a id="rst-phy-get"></a>

## PHY_GET

Retrieve information about a given Ethernet PHY sitting on the link. The DO operation returns all available information about dev-&gt;phydev. User can also specify a PHY_INDEX, in which case the DO request returns information about that specific PHY.

As there can be more than one PHY, the DUMP operation can be used to list the PHYs present on a given interface, by passing an interface index or name in the dump request.

For more information, refer to [PHY link topology](<~kernel/internals/networking/phy-link-topology#rst-phy-link-topology>)

Request contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_PHY_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> request header
>
> </td>
> </tr>
> </tbody>
> </table>

Kernel response contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_PHY_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> request header
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_PHY_INDEX`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> the phy's unique index, that can be used for phy-specific requests
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_PHY_DRVNAME`
>
> </td>
> <td>
>
>
> string
>
> </td>
> <td>
>
>
> the phy driver name
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_PHY_NAME`
>
> </td>
> <td>
>
>
> string
>
> </td>
> <td>
>
>
> the phy device name
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_PHY_UPSTREAM_TYPE`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> the type of device this phy is connected to
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_PHY_UPSTREAM_INDEX`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> the PHY index of the upstream PHY
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_PHY_UPSTREAM_SFP_NAME`
>
> </td>
> <td>
>
>
> string
>
> </td>
> <td>
>
>
> if this PHY is connected to its parent PHY through an SFP bus, the name of this sfp bus
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_PHY_DOWNSTREAM_SFP_NAME`
>
> </td>
> <td>
>
>
> string
>
> </td>
> <td>
>
>
> if the phy controls an sfp bus, the name of the sfp bus
>
> </td>
> </tr>
> </tbody>
> </table>

When `ETHTOOL_A_PHY_UPSTREAM_TYPE` is PHY_UPSTREAM_PHY, the PHY's parent is another PHY.

<a id="rst-tsconfig-get"></a>

## TSCONFIG_GET

Retrieves the information about the current hardware timestamping source and configuration.

It is similar to the deprecated `SIOCGHWTSTAMP` ioctl request.

Request contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_TSCONFIG_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> request header
>
> </td>
> </tr>
> </tbody>
> </table>

Kernel response contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_TSCONFIG_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> request header
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_TSCONFIG_HWTSTAMP_PROVIDER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> PTP hw clock provider
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_TSCONFIG_TX_TYPES`
>
> </td>
> <td>
>
>
> bitset
>
> </td>
> <td>
>
>
> hwtstamp Tx type
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_TSCONFIG_RX_FILTERS`
>
> </td>
> <td>
>
>
> bitset
>
> </td>
> <td>
>
>
> hwtstamp Rx filter
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_TSCONFIG_HWTSTAMP_FLAGS`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> hwtstamp flags
>
> </td>
> </tr>
> </tbody>
> </table>

When set the `ETHTOOL_A_TSCONFIG_HWTSTAMP_PROVIDER` attribute identifies the source of the hw timestamping provider. It is composed by `ETHTOOL_A_TS_HWTSTAMP_PROVIDER_INDEX` attribute which describe the index of the PTP device and `ETHTOOL_A_TS_HWTSTAMP_PROVIDER_QUALIFIER` which describe the qualifier of the timestamp.

When set the `ETHTOOL_A_TSCONFIG_TX_TYPES`, `ETHTOOL_A_TSCONFIG_RX_FILTERS` and the `ETHTOOL_A_TSCONFIG_HWTSTAMP_FLAGS` attributes identify the Tx type, the Rx filter and the flags configured for the current hw timestamping provider. The attributes are propagated to the driver through the following structure:

```{kernel-doc} include/linux/net_tstamp.h
:identifiers: kernel_hwtstamp_config
```

<a id="rst-tsconfig-set"></a>

## TSCONFIG_SET

Set the information about the current hardware timestamping source and configuration.

It is similar to the deprecated `SIOCSHWTSTAMP` ioctl request.

Request contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_TSCONFIG_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> request header
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_TSCONFIG_HWTSTAMP_PROVIDER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> PTP hw clock provider
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_TSCONFIG_TX_TYPES`
>
> </td>
> <td>
>
>
> bitset
>
> </td>
> <td>
>
>
> hwtstamp Tx type
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_TSCONFIG_RX_FILTERS`
>
> </td>
> <td>
>
>
> bitset
>
> </td>
> <td>
>
>
> hwtstamp Rx filter
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_TSCONFIG_HWTSTAMP_FLAGS`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> hwtstamp flags
>
> </td>
> </tr>
> </tbody>
> </table>

Kernel response contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_TSCONFIG_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> request header
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_TSCONFIG_HWTSTAMP_PROVIDER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> PTP hw clock provider
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_TSCONFIG_TX_TYPES`
>
> </td>
> <td>
>
>
> bitset
>
> </td>
> <td>
>
>
> hwtstamp Tx type
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_TSCONFIG_RX_FILTERS`
>
> </td>
> <td>
>
>
> bitset
>
> </td>
> <td>
>
>
> hwtstamp Rx filter
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_TSCONFIG_HWTSTAMP_FLAGS`
>
> </td>
> <td>
>
>
> u32
>
> </td>
> <td>
>
>
> hwtstamp flags
>
> </td>
> </tr>
> </tbody>
> </table>

For a description of each attribute, see `TSCONFIG_GET`.

<a id="rst-mse-get"></a>

## MSE_GET

Retrieves detailed Mean Square Error (MSE) diagnostic information from the PHY.

Request Contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_MSE_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> request header
>
> </td>
> </tr>
> </tbody>
> </table>

Kernel Response Contents:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_MSE_HEADER`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> reply header
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_MSE_CAPABILITIES`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> capability/scale info for MSE measurements
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_MSE_CHANNEL_A`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> snapshot for Channel A
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_MSE_CHANNEL_B`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> snapshot for Channel B
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_MSE_CHANNEL_C`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> snapshot for Channel C
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_MSE_CHANNEL_D`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> snapshot for Channel D
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_MSE_WORST_CHANNEL`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> snapshot for worst channel
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_MSE_LINK`
>
> </td>
> <td>
>
>
> nested
>
> </td>
> <td>
>
>
> snapshot for link-wide aggregate
>
> </td>
> </tr>
> </tbody>
> </table>

<a id="rst-mse-capabilities"></a>

### MSE Capabilities

This nested attribute reports the capability / scaling properties used to interpret snapshot values.

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_MSE_CAPABILITIES_MAX_AVERAGE_MSE`
>
> </td>
> <td>
>
>
> uint
>
> </td>
> <td>
>
>
> max avg_mse scale
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_MSE_CAPABILITIES_MAX_PEAK_MSE`
>
> </td>
> <td>
>
>
> uint
>
> </td>
> <td>
>
>
> max peak_mse scale
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_MSE_CAPABILITIES_REFRESH_RATE_PS`
>
> </td>
> <td>
>
>
> uint
>
> </td>
> <td>
>
>
> sample rate (picoseconds)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_MSE_CAPABILITIES_NUM_SYMBOLS`
>
> </td>
> <td>
>
>
> uint
>
> </td>
> <td>
>
>
> symbols per HW sample
>
> </td>
> </tr>
> </tbody>
> </table>

The max-average/peak fields are included only if the corresponding metric is supported by the PHY. Their absence indicates that the metric is not available.

See `struct phy_mse_capability` kernel documentation in `include/linux/phy.h`.

<a id="rst-mse-snapshot"></a>

### MSE Snapshot

Each per-channel nest contains an atomic snapshot of MSE values for that selector (channel A/B/C/D, worst channel, or link).

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_A_MSE_SNAPSHOT_AVERAGE_MSE`
>
> </td>
> <td>
>
>
> uint
>
> </td>
> <td>
>
>
> average MSE value
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_MSE_SNAPSHOT_PEAK_MSE`
>
> </td>
> <td>
>
>
> uint
>
> </td>
> <td>
>
>
> current peak MSE
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_A_MSE_SNAPSHOT_WORST_PEAK_MSE`
>
> </td>
> <td>
>
>
> uint
>
> </td>
> <td>
>
>
> worst-case peak MSE
>
> </td>
> </tr>
> </tbody>
> </table>

Within each channel nest, only the metrics supported by the PHY will be present.

See `struct phy_mse_snapshot` kernel documentation in `include/linux/phy.h`.

<a id="rst-request-translation"></a>

## Request translation

The following table maps ioctl commands to netlink commands providing their functionality. Entries with "n/a" in right column are commands which do not have their netlink replacement yet. Entries which "n/a" in the left column are netlink only.

>
> <table>
> <thead>
> <tr>
> <th>
>
>
> ioctl command
>
> </th>
> <th>
>
>
> netlink command
>
> </th>
> </tr>
> </thead>
> <tbody>
> <tr>
> <td>
>
>
> `ETHTOOL_GSET`
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_LINKINFO_GET` `ETHTOOL_MSG_LINKMODES_GET`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_SSET`
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_LINKINFO_SET` `ETHTOOL_MSG_LINKMODES_SET`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_GDRVINFO`
>
> </td>
> <td>
>
>
> n/a
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_GREGS`
>
> </td>
> <td>
>
>
> n/a
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_GWOL`
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_WOL_GET`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_SWOL`
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_WOL_SET`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_GMSGLVL`
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_DEBUG_GET`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_SMSGLVL`
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_DEBUG_SET`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_NWAY_RST`
>
> </td>
> <td>
>
>
> n/a
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_GLINK`
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_LINKSTATE_GET`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_GEEPROM`
>
> </td>
> <td>
>
>
> n/a
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_SEEPROM`
>
> </td>
> <td>
>
>
> n/a
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_GCOALESCE`
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_COALESCE_GET`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_SCOALESCE`
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_COALESCE_SET`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_GRINGPARAM`
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_RINGS_GET`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_SRINGPARAM`
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_RINGS_SET`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_GPAUSEPARAM`
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_PAUSE_GET`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_SPAUSEPARAM`
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_PAUSE_SET`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_GRXCSUM`
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_FEATURES_GET`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_SRXCSUM`
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_FEATURES_SET`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_GTXCSUM`
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_FEATURES_GET`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_STXCSUM`
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_FEATURES_SET`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_GSG`
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_FEATURES_GET`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_SSG`
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_FEATURES_SET`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_TEST`
>
> </td>
> <td>
>
>
> n/a
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_GSTRINGS`
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_STRSET_GET`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_PHYS_ID`
>
> </td>
> <td>
>
>
> n/a
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_GSTATS`
>
> </td>
> <td>
>
>
> n/a
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_GTSO`
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_FEATURES_GET`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_STSO`
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_FEATURES_SET`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_GPERMADDR`
>
> </td>
> <td>
>
>
> rtnetlink `RTM_GETLINK`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_GUFO`
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_FEATURES_GET`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_SUFO`
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_FEATURES_SET`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_GGSO`
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_FEATURES_GET`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_SGSO`
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_FEATURES_SET`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_GFLAGS`
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_FEATURES_GET`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_SFLAGS`
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_FEATURES_SET`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_GPFLAGS`
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_PRIVFLAGS_GET`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_SPFLAGS`
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_PRIVFLAGS_SET`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_GRXFH`
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_RSS_GET`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_SRXFH`
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_RSS_SET`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_GGRO`
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_FEATURES_GET`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_SGRO`
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_FEATURES_SET`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_GRXRINGS`
>
> </td>
> <td>
>
>
> n/a
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_GRXCLSRLCNT`
>
> </td>
> <td>
>
>
> n/a
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_GRXCLSRULE`
>
> </td>
> <td>
>
>
> n/a
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_GRXCLSRLALL`
>
> </td>
> <td>
>
>
> n/a
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_SRXCLSRLDEL`
>
> </td>
> <td>
>
>
> n/a
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_SRXCLSRLINS`
>
> </td>
> <td>
>
>
> n/a
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_FLASHDEV`
>
> </td>
> <td>
>
>
> n/a
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_RESET`
>
> </td>
> <td>
>
>
> n/a
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_SRXNTUPLE`
>
> </td>
> <td>
>
>
> n/a
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_GRXNTUPLE`
>
> </td>
> <td>
>
>
> n/a
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_GSSET_INFO`
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_STRSET_GET`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_GRXFHINDIR`
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_RSS_GET`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_SRXFHINDIR`
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_RSS_SET`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_GFEATURES`
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_FEATURES_GET`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_SFEATURES`
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_FEATURES_SET`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_GCHANNELS`
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_CHANNELS_GET`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_SCHANNELS`
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_CHANNELS_SET`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_SET_DUMP`
>
> </td>
> <td>
>
>
> n/a
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_GET_DUMP_FLAG`
>
> </td>
> <td>
>
>
> n/a
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_GET_DUMP_DATA`
>
> </td>
> <td>
>
>
> n/a
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_GET_TS_INFO`
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_TSINFO_GET`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_GMODULEINFO`
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_MODULE_EEPROM_GET`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_GMODULEEEPROM`
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_MODULE_EEPROM_GET`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_GEEE`
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_EEE_GET`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_SEEE`
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_EEE_SET`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_GRSSH`
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_RSS_GET`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_SRSSH`
>
> </td>
> <td>
>
>
> n/a
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_GTUNABLE`
>
> </td>
> <td>
>
>
> n/a
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_STUNABLE`
>
> </td>
> <td>
>
>
> n/a
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_GPHYSTATS`
>
> </td>
> <td>
>
>
> n/a
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_PERQUEUE`
>
> </td>
> <td>
>
>
> n/a
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_GLINKSETTINGS`
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_LINKINFO_GET` `ETHTOOL_MSG_LINKMODES_GET`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_SLINKSETTINGS`
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_LINKINFO_SET` `ETHTOOL_MSG_LINKMODES_SET`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_PHY_GTUNABLE`
>
> </td>
> <td>
>
>
> n/a
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_PHY_STUNABLE`
>
> </td>
> <td>
>
>
> n/a
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_GFECPARAM`
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_FEC_GET`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `ETHTOOL_SFECPARAM`
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_FEC_SET`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> n/a
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_CABLE_TEST_ACT`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> n/a
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_CABLE_TEST_TDR_ACT`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> n/a
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_TUNNEL_INFO_GET`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> n/a
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_PHC_VCLOCKS_GET`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> n/a
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_MODULE_GET`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> n/a
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_MODULE_SET`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> n/a
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_PLCA_GET_CFG`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> n/a
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_PLCA_SET_CFG`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> n/a
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_PLCA_GET_STATUS`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> n/a
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_MM_GET`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> n/a
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_MM_SET`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> n/a
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_MODULE_FW_FLASH_ACT`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> n/a
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_PHY_GET`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `SIOCGHWTSTAMP`
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_TSCONFIG_GET`
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> `SIOCSHWTSTAMP`
>
> </td>
> <td>
>
>
> `ETHTOOL_MSG_TSCONFIG_SET`
>
> </td>
> </tr>
> </tbody>
> </table>
