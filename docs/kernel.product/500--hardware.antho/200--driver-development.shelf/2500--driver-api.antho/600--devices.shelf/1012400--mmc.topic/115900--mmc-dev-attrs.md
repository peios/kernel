---
title: "SD and MMC Block Device Attributes"
type: reference
description: "These attributes are defined for the block devices associated with the SD or MMC device."
---

<a id="rst-sd-and-mmc-block-device-attributes"></a>

These attributes are defined for the block devices associated with the SD or MMC device.

The following attributes are read/write.

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> force_ro
>
> </td>
> <td>
>
>
> Enforce read-only access even if write protect                                  switch is off.
>
> </td>
> </tr>
> </tbody>
> </table>

<a id="rst-sd-and-mmc-device-attributes"></a>

## SD and MMC Device Attributes

All attributes are read-only.

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> cid
>
> </td>
> <td>
>
>
> Card Identification Register
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> csd
>
> </td>
> <td>
>
>
> Card Specific Data Register
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> scr
>
> </td>
> <td>
>
>
> SD Card Configuration Register (SD only)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> date
>
> </td>
> <td>
>
>
> Manufacturing Date (from CID Register)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> fwrev
>
> </td>
> <td>
>
>
> Firmware/Product Revision (from CID Register) (SD and MMCv1 only)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> hwrev
>
> </td>
> <td>
>
>
> Hardware/Product Revision (from CID Register) (SD and MMCv1 only)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> manfid
>
> </td>
> <td>
>
>
> Manufacturer ID (from CID Register)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> name
>
> </td>
> <td>
>
>
> Product Name (from CID Register)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> oemid
>
> </td>
> <td>
>
>
> OEM/Application ID (from CID Register)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> prv
>
> </td>
> <td>
>
>
> Product Revision (from CID Register) (SD and MMCv4 only)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> serial
>
> </td>
> <td>
>
>
> Product Serial Number (from CID Register)
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> erase_size
>
> </td>
> <td>
>
>
> Erase group size
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> preferred_erase_size
>
> </td>
> <td>
>
>
> Preferred erase size
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> raw_rpmb_size_mult
>
> </td>
> <td>
>
>
> RPMB partition size
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> rel_sectors
>
> </td>
> <td>
>
>
> Reliable write sector count
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> ocr
>
> </td>
> <td>
>
>
> Operation Conditions Register
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> dsr
>
> </td>
> <td>
>
>
> Driver Stage Register
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> cmdq_en
>
> </td>
> <td>
>
>
> Command Queue enabled:
>
> > 1 =&gt; enabled, 0 =&gt; not enabled
>
> </td>
> </tr>
> </tbody>
> </table>

Note on Erase Size and Preferred Erase Size:

> "erase_size" is the  minimum size, in bytes, of an erase operation.  For MMC, "erase_size" is the erase group size reported by the card.  Note that "erase_size" does not apply to trim or secure trim operations where the minimum size is always one 512 byte sector.  For SD, "erase_size" is 512 if the card is block-addressed, 0 otherwise.
>
> SD/MMC cards can erase an arbitrarily large area up to and including the whole card.  When erasing a large area it may be desirable to do it in smaller chunks for three reasons:
>
> > 1. A single erase command will make all other I/O on the card wait.  This is not a problem if the whole card is being erased, but erasing one partition will make I/O for another partition on the same card wait for the duration of the erase - which could be a several minutes.
> >
> > 2. To be able to inform the user of erase progress.
> >
> > 3. The erase timeout becomes too large to be very useful.  Because the erase timeout contains a margin which is multiplied by the size of the erase area, the value can end up being several minutes for large areas.
>
> "erase_size" is not the most efficient unit to erase (especially for SD where it is just one sector), hence "preferred_erase_size" provides a good chunk size for erasing large areas.
>
> For MMC, "preferred_erase_size" is the high-capacity erase size if a card specifies one, otherwise it is based on the capacity of the card.
>
> For SD, "preferred_erase_size" is the allocation unit size specified by the card.
>
> "preferred_erase_size" is in bytes.

Note on raw_rpmb_size_mult:

> "raw_rpmb_size_mult" is a multiple of 128kB block.
>
> RPMB size in byte is calculated by using the following equation:
>
> > RPMB partition size = 128kB x raw_rpmb_size_mult
