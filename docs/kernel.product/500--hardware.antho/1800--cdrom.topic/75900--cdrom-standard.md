---
title: "A Linux CD-ROM standard"
type: reference
description: "Linux is probably the Unix-like operating system that supports the widest variety of hardware devices. The reasons for this are presumably"
---

<a id="rst-a-linux-cd-rom-standard"></a>

**Author:** David van Leeuwen &lt;[david@ElseWare.cistron.nl](<mailto:david@ElseWare.cistron.nl>)&gt;

**Date:** 12 March 1999

**Updated by:** Erik Andersen ([andersee@debian.org](<mailto:andersee@debian.org>))

**Updated by:** Jens Axboe ([axboe@image.dk](<mailto:axboe@image.dk>))

<a id="rst-introduction"></a>

## Introduction

Linux is probably the Unix-like operating system that supports the widest variety of hardware devices. The reasons for this are presumably

- The large list of hardware devices available for the many platforms that Linux now supports (i.e., i386-PCs, Sparc Suns, etc.)

- The open design of the operating system, such that anybody can write a driver for Linux.

- There is plenty of source code around as examples of how to write a driver.

The openness of Linux, and the many different types of available hardware has allowed Linux to support many different hardware devices. Unfortunately, the very openness that has allowed Linux to support all these different devices has also allowed the behavior of each device driver to differ significantly from one device to another. This divergence of behavior has been very significant for CD-ROM devices; the way a particular drive reacts to a `standard` <em>ioctl()</em> call varies greatly from one device driver to another. To avoid making their drivers totally inconsistent, the writers of Linux CD-ROM drivers generally created new device drivers by understanding, copying, and then changing an existing one. Unfortunately, this practice did not maintain uniform behavior across all the Linux CD-ROM drivers.

This document describes an effort to establish Uniform behavior across all the different CD-ROM device drivers for Linux. This document also defines the various <em>ioctl()'s</em>, and how the low-level CD-ROM device drivers should implement them. Currently (as of the Linux 2.1.<em>x</em> development kernels) several low-level CD-ROM device drivers, including both IDE/ATAPI and SCSI, now use this Uniform interface.

When the CD-ROM was developed, the interface between the CD-ROM drive and the computer was not specified in the standards. As a result, many different CD-ROM interfaces were developed. Some of them had their own proprietary design (Sony, Mitsumi, Panasonic, Philips), other manufacturers adopted an existing electrical interface and changed the functionality (CreativeLabs/SoundBlaster, Teac, Funai) or simply adapted their drives to one or more of the already existing electrical interfaces (Aztech, Sanyo, Funai, Vertos, Longshine, Optics Storage and most of the `NoName` manufacturers). In cases where a new drive really brought its own interface or used its own command set and flow control scheme, either a separate driver had to be written, or an existing driver had to be enhanced. History has delivered us CD-ROM support for many of these different interfaces. Nowadays, almost all new CD-ROM drives are either IDE/ATAPI or SCSI, and it is very unlikely that any manufacturer will create a new interface. Even finding drives for the old proprietary interfaces is getting difficult.

When (in the 1.3.70's) I looked at the existing software interface, which was expressed through `cdrom.h`, it appeared to be a rather wild set of commands and data formats <a id="rst-footnote-reference-1"></a>[1](#rst-f1). It seemed that many features of the software interface had been added to accommodate the capabilities of a particular drive, in an <em>ad hoc</em> manner. More importantly, it appeared that the behavior of the `standard` commands was different for most of the different drivers: e. g., some drivers close the tray if an <em>open()</em> call occurs when the tray is open, while others do not. Some drivers lock the door upon opening the device, to prevent an incoherent file system, but others don't, to allow software ejection. Undoubtedly, the capabilities of the different drives vary, but even when two drives have the same capability their drivers' behavior was usually different.

<a id="rst-f1"></a>



**[1]** I cannot recollect what kernel version I looked at, then, presumably 1.2.13 and 1.3.34 --- the latest kernel that I was indirectly involved in.

I decided to start a discussion on how to make all the Linux CD-ROM drivers behave more uniformly. I began by contacting the developers of the many CD-ROM drivers found in the Linux kernel. Their reactions encouraged me to write the Uniform CD-ROM Driver which this document is intended to describe. The implementation of the Uniform CD-ROM Driver is in the file `cdrom.c`. This driver is intended to be an additional software layer that sits on top of the low-level device drivers for each CD-ROM drive. By adding this additional layer, it is possible to have all the different CD-ROM devices behave <strong>exactly</strong> the same (insofar as the underlying hardware will allow).

The goal of the Uniform CD-ROM Driver is <strong>not</strong> to alienate driver developers whohave not yet taken steps to support this effort. The goal of Uniform CD-ROM Driver is simply to give people writing application programs for CD-ROM drives <strong>one</strong> Linux CD-ROM interface with consistent behavior for all CD-ROM devices. In addition, this also provides a consistent interface between the low-level device driver code and the Linux kernel. Care is taken that 100% compatibility exists with the data structures and programmer's interface defined in `cdrom.h`. This guide was written to help CD-ROM driver developers adapt their code to use the Uniform CD-ROM Driver code defined in `cdrom.c`.

Personally, I think that the most important hardware interfaces are the IDE/ATAPI drives and, of course, the SCSI drives, but as prices of hardware drop continuously, it is also likely that people may have more than one CD-ROM drive, possibly of mixed types. It is important that these drives behave in the same way. In December 1994, one of the cheapest CD-ROM drives was a Philips cm206, a double-speed proprietary drive. In the months that I was busy writing a Linux driver for it, proprietary drives became obsolete and IDE/ATAPI drives became the standard. At the time of the last update to this document (November 1997) it is becoming difficult to even <strong>find</strong> anything less than a 16 speed CD-ROM drive, and 24 speed drives are common.

<a id="rst-standardizing-through-another-software-level"></a>
<a id="rst-cdrom-api"></a>

## Standardizing through another software level

At the time this document was conceived, all drivers directly implemented the CD-ROM <em>ioctl()</em> calls through their own routines. This led to the danger of different drivers forgetting to do important things like checking that the user was giving the driver valid data. More importantly, this led to the divergence of behavior, which has already been discussed.

For this reason, the Uniform CD-ROM Driver was created to enforce consistent CD-ROM drive behavior, and to provide a common set of services to the various low-level CD-ROM device drivers. The Uniform CD-ROM Driver now provides another software-level, that separates the <em>ioctl()</em> and <em>open()</em> implementation from the actual hardware implementation. Note that this effort has made few changes which will affect a user's application programs. The greatest change involved moving the contents of the various low-level CD-ROM drivers' header files to the kernel's cdrom directory. This was done to help ensure that the user is only presented with only one cdrom interface, the interface defined in `cdrom.h`.

CD-ROM drives are specific enough (i. e., different from other block-devices such as floppy or hard disc drives), to define a set of common <strong>CD-ROM device operations</strong>, <em>&lt;cdrom-device&gt;\_dops</em>. These operations are different from the classical block-device file operations, <em>&lt;block-device&gt;\_fops</em>.

The routines for the Uniform CD-ROM Driver interface level are implemented in the file `cdrom.c`. In this file, the Uniform CD-ROM Driver interfaces with the kernel as a block device by registering the following general <em>struct file\_operations</em>:



```text
struct file_operations cdrom_fops = {
        NULL,                   /* lseek */
        block _read ,           /* read--general block-dev read */
        block _write,           /* write--general block-dev write */
        NULL,                   /* readdir */
        NULL,                   /* select */
        cdrom_ioctl,            /* ioctl */
        NULL,                   /* mmap */
        cdrom_open,             /* open */
        cdrom_release,          /* release */
        NULL,                   /* fsync */
        NULL,                   /* fasync */
        NULL                    /* revalidate */
};
```

Every active CD-ROM device shares this <em>struct</em>. The routines declared above are all implemented in `cdrom.c`, since this file is the place where the behavior of all CD-ROM-devices is defined and standardized. The actual interface to the various types of CD-ROM hardware is still performed by various low-level CD-ROM-device drivers. These routines simply implement certain <strong>capabilities</strong> that are common to all CD-ROM (and really, all removable-media devices).

Registration of a low-level CD-ROM device driver is now done through the general routines in `cdrom.c`, not through the Virtual File System (VFS) any more. The interface implemented in `cdrom.c` is carried out through two general structures that contain information about the capabilities of the driver, and the specific drives on which the driver operates. The structures are:

- **cdrom\_device\_ops**

  This structure contains information about the low-level driver for a CD-ROM device. This structure is conceptually connected to the major number of the device (although some drivers may have different major numbers, as is the case for the IDE driver).

- **cdrom\_device\_info**

  This structure contains information about a particular CD-ROM drive, such as its device name, speed, etc. This structure is conceptually connected to the minor number of the device.

Registering a particular CD-ROM drive with the Uniform CD-ROM Driver is done by the low-level device driver though a call to:



```text
register_cdrom(struct cdrom_device_info * <device>_info)
```

The device information structure, <em>&lt;device&gt;\_info</em>, contains all the information needed for the kernel to interface with the low-level CD-ROM device driver. One of the most important entries in this structure is a pointer to the <em>cdrom\_device\_ops</em> structure of the low-level driver.

The device operations structure, <em>cdrom\_device\_ops</em>, contains a list of pointers to the functions which are implemented in the low-level device driver. When `cdrom.c` accesses a CD-ROM device, it does it through the functions in this structure. It is impossible to know all the capabilities of future CD-ROM drives, so it is expected that this list may need to be expanded from time to time as new technologies are developed. For example, CD-R and CD-R/W drives are beginning to become popular, and support will soon need to be added for them. For now, the current <em>struct</em> is:



```text
struct cdrom_device_ops {
        int (*open)(struct cdrom_device_info *, int)
        void (*release)(struct cdrom_device_info *);
        int (*drive_status)(struct cdrom_device_info *, int);
        unsigned int (*check_events)(struct cdrom_device_info *,
                                     unsigned int, int);
        int (*media_changed)(struct cdrom_device_info *, int);
        int (*tray_move)(struct cdrom_device_info *, int);
        int (*lock_door)(struct cdrom_device_info *, int);
        int (*select_speed)(struct cdrom_device_info *, unsigned long);
        int (*get_last_session) (struct cdrom_device_info *,
                                 struct cdrom_multisession *);
        int (*get_mcn)(struct cdrom_device_info *, struct cdrom_mcn *);
        int (*reset)(struct cdrom_device_info *);
        int (*audio_ioctl)(struct cdrom_device_info *,
                           unsigned int, void *);
        const int capability;           /* capability flags */
        int (*generic_packet)(struct cdrom_device_info *,
                              struct packet_command *);
};
```

When a low-level device driver implements one of these capabilities, it should add a function pointer to this <em>struct</em>. When a particular function is not implemented, however, this <em>struct</em> should contain a NULL instead. The <em>capability</em> flags specify the capabilities of the CD-ROM hardware and/or low-level CD-ROM driver when a CD-ROM drive is registered with the Uniform CD-ROM Driver.

Note that most functions have fewer parameters than their <em>blkdev\_fops</em> counterparts. This is because very little of the information in the structures <em>inode</em> and <em>file</em> is used. For most drivers, the main parameter is the <em>struct</em> <em>cdrom\_device\_info</em>, from which the major and minor number can be extracted. (Most low-level CD-ROM drivers don't even look at the major and minor number though, since many of them only support one device.) This will be available through <em>dev</em> in <em>cdrom\_device\_info</em> described below.

The drive-specific, minor-like information that is registered with `cdrom.c`, currently contains the following fields:



```text
struct cdrom_device_info {
      const struct cdrom_device_ops * ops;    /* device operations for this major */
      struct list_head list;                  /* linked list of all device_info */
      struct gendisk * disk;                  /* matching block layer disk */
      void *  handle;                         /* driver-dependent data */

      int mask;                               /* mask of capability: disables them */
      int speed;                              /* maximum speed for reading data */
      int capacity;                           /* number of discs in a jukebox */

      unsigned int options:30;                /* options flags */
      unsigned mc_flags:2;                    /*  media-change buffer flags */
      unsigned int vfs_events;                /*  cached events for vfs path */
      unsigned int ioctl_events;              /*  cached events for ioctl path */
      int use_count;                          /*  number of times device is opened */
      char name[20];                          /*  name of the device type */

      __u8 sanyo_slot : 2;                    /*  Sanyo 3-CD changer support */
      __u8 keeplocked : 1;                    /*  CDROM_LOCKDOOR status */
      __u8 reserved : 5;                      /*  not used yet */
      int cdda_method;                        /*  see CDDA_* flags */
      __u8 last_sense;                        /*  saves last sense key */
      __u8 media_written;                     /*  dirty flag, DVD+RW bookkeeping */
      unsigned short mmc3_profile;            /*  current MMC3 profile */
      int for_data;                           /*  unknown:TBD */
      int mrw_mode_page;                      /*  which MRW mode page is in use */
};
```

Using this <em>struct</em>, a linked list of the registered minor devices is built, using the <em>next</em> field. The device number, the device operations struct and specifications of properties of the drive are stored in this structure.

The <em>mask</em> flags can be used to mask out some of the capabilities listed in <em>ops-&gt;capability</em>, if a specific drive doesn't support a feature of the driver. The value <em>speed</em> specifies the maximum head-rate of the drive, measured in units of normal audio speed (176kB/sec raw data or 150kB/sec file system data). The parameters are declared <em>const</em> because they describe properties of the drive, which don't change after registration.

A few registers contain variables local to the CD-ROM drive. The flags <em>options</em> are used to specify how the general CD-ROM routines should behave. These various flags registers should provide enough flexibility to adapt to the different users' wishes (and <strong>not</strong> the `arbitrary` wishes of the author of the low-level device driver, as is the case in the old scheme). The register <em>mc\_flags</em> is used to buffer the information from <em>media\_changed()</em> to two separate queues. Other data that is specific to a minor drive, can be accessed through <em>handle</em>, which can point to a data structure specific to the low-level driver. The fields <em>use\_count</em>, <em>next</em>, <em>options</em> and <em>mc\_flags</em> need not be initialized.

The intermediate software layer that `cdrom.c` forms will perform some additional bookkeeping. The use count of the device (the number of processes that have the device opened) is registered in <em>use\_count</em>. The function <em>cdrom\_ioctl()</em> will verify the appropriate user-memory regions for read and write, and in case a location on the CD is transferred, it will `sanitize` the format by making requests to the low-level drivers in a standard format, and translating all formats between the user-software and low level drivers. This relieves much of the drivers' memory checking and format checking and translation. Also, the necessary structures will be declared on the program stack.

The implementation of the functions should be as defined in the following sections. Two functions <strong>must</strong> be implemented, namely <em>open()</em> and <em>release()</em>. Other functions may be omitted, their corresponding capability flags will be cleared upon registration. Generally, a function returns zero on success and negative on error. A function call should return only after the command has completed, but of course waiting for the device should not use processor time.



```text
int open(struct cdrom_device_info *cdi, int purpose)
```

<em>Open()</em> should try to open the device for a specific <em>purpose</em>, which can be either:

- Open for reading data, as done by `mount()` (2), or the user commands `dd` or `cat`.

- Open for <em>ioctl</em> commands, as done by audio-CD playing programs.

Notice that any strategic code (closing tray upon <em>open()</em>, etc.) is done by the calling routine in `cdrom.c`, so the low-level routine should only be concerned with proper initialization, such as spinning up the disc, etc.



```text
void release(struct cdrom_device_info *cdi)
```

Device-specific actions should be taken such as spinning down the device. However, strategic actions such as ejection of the tray, or unlocking the door, should be left over to the general routine <em>cdrom\_release()</em>. This is the only function returning type <em>void</em>.

<a id="rst-cdrom-drive-status"></a>



```text
int drive_status(struct cdrom_device_info *cdi, int slot_nr)
```

The function <em>drive\_status</em>, if implemented, should provide information on the status of the drive (not the status of the disc, which may or may not be in the drive). If the drive is not a changer, <em>slot\_nr</em> should be ignored. In `cdrom.h` the possibilities are listed:



```text
CDS_NO_INFO             /* no information available */
CDS_NO_DISC             /* no disc is inserted, tray is closed */
CDS_TRAY_OPEN           /* tray is opened */
CDS_DRIVE_NOT_READY     /* something is wrong, tray is moving? */
CDS_DISC_OK             /* a disc is loaded and everything is fine */
```



```text
int tray_move(struct cdrom_device_info *cdi, int position)
```

This function, if implemented, should control the tray movement. (No other function should control this.) The parameter <em>position</em> controls the desired direction of movement:

- 0 Close tray

- 1 Open tray

This function returns 0 upon success, and a non-zero value upon error. Note that if the tray is already in the desired position, no action need be taken, and the return value should be 0.



```text
int lock_door(struct cdrom_device_info *cdi, int lock)
```

This function (and no other code) controls locking of the door, if the drive allows this. The value of <em>lock</em> controls the desired locking state:

- 0 Unlock door, manual opening is allowed

- 1 Lock door, tray cannot be ejected manually

This function returns 0 upon success, and a non-zero value upon error. Note that if the door is already in the requested state, no action need be taken, and the return value should be 0.



```text
int select_speed(struct cdrom_device_info *cdi, unsigned long speed)
```

Some CD-ROM drives are capable of changing their head-speed. There are several reasons for changing the speed of a CD-ROM drive. Badly pressed CD-ROM s may benefit from less-than-maximum head rate. Modern CD-ROM drives can obtain very high head rates (up to <em>24x</em> is common). It has been reported that these drives can make reading errors at these high speeds, reducing the speed can prevent data loss in these circumstances. Finally, some of these drives can make an annoyingly loud noise, which a lower speed may reduce.

This function specifies the speed at which data is read or audio is played back. The value of <em>speed</em> specifies the head-speed of the drive, measured in units of standard cdrom speed (176kB/sec raw data or 150kB/sec file system data). So to request that a CD-ROM drive operate at 300kB/sec you would call the CDROM\_SELECT\_SPEED <em>ioctl</em> with <em>speed=2</em>. The special value `0` means `auto-selection`, i. e., maximum data-rate or real-time audio rate. If the drive doesn't have this `auto-selection` capability, the decision should be made on the current disc loaded and the return value should be positive. A negative return value indicates an error.



```text
int get_last_session(struct cdrom_device_info *cdi,
                     struct cdrom_multisession *ms_info)
```

This function should implement the old corresponding <em>ioctl()</em>. For device <em>cdi-&gt;dev</em>, the start of the last session of the current disc should be returned in the pointer argument <em>ms\_info</em>. Note that routines in `cdrom.c` have sanitized this argument: its requested format will <strong>always</strong> be of the type <em>CDROM\_LBA</em> (linear block addressing mode), whatever the calling software requested. But sanitization goes even further: the low-level implementation may return the requested information in <em>CDROM\_MSF</em> format if it wishes so (setting the <em>ms\_info-&gt;addr\_format</em> field appropriately, of course) and the routines in `cdrom.c` will make the transformation if necessary. The return value is 0 upon success.



```text
int get_mcn(struct cdrom_device_info *cdi,
            struct cdrom_mcn *mcn)
```

Some discs carry a `Media Catalog Number` (MCN), also called `Universal Product Code` (UPC). This number should reflect the number that is generally found in the bar-code on the product. Unfortunately, the few discs that carry such a number on the disc don't even use the same format. The return argument to this function is a pointer to a pre-declared memory region of type <em>struct cdrom\_mcn</em>. The MCN is expected as a 13-character string, terminated by a null-character.



```text
int reset(struct cdrom_device_info *cdi)
```

This call should perform a hard-reset on the drive (although in circumstances that a hard-reset is necessary, a drive may very well not listen to commands anymore). Preferably, control is returned to the caller only after the drive has finished resetting. If the drive is no longer listening, it may be wise for the underlying low-level cdrom driver to time out.



```text
int audio_ioctl(struct cdrom_device_info *cdi,
                unsigned int cmd, void *arg)
```

Some of the CD-ROM-<em>ioctl()</em>'s defined in `cdrom.h` can be implemented by the routines described above, and hence the function <em>cdrom\_ioctl</em> will use those. However, most <em>ioctl()</em>'s deal with audio-control. We have decided to leave these to be accessed through a single function, repeating the arguments <em>cmd</em> and <em>arg</em>. Note that the latter is of type <em>void</em>, rather than <em>unsigned long int</em>. The routine <em>cdrom\_ioctl()</em> does do some useful things, though. It sanitizes the address format type to <em>CDROM\_MSF</em> (Minutes, Seconds, Frames) for all audio calls. It also verifies the memory location of <em>arg</em>, and reserves stack-memory for the argument. This makes implementation of the <em>audio\_ioctl()</em> much simpler than in the old driver scheme. For example, you may look up the function <em>cm206\_audio\_ioctl()</em> `cm206.c` that should be updated with this documentation.

An unimplemented ioctl should return <em>-ENOSYS</em>, but a harmless request (e. g., <em>CDROMSTART</em>) may be ignored by returning 0 (success). Other errors should be according to the standards, whatever they are. When an error is returned by the low-level driver, the Uniform CD-ROM Driver tries whenever possible to return the error code to the calling program. (We may decide to sanitize the return value in <em>cdrom\_ioctl()</em> though, in order to guarantee a uniform interface to the audio-player software.)



```text
int dev_ioctl(struct cdrom_device_info *cdi,
              unsigned int cmd, unsigned long arg)
```

Some <em>ioctl()'s</em> seem to be specific to certain CD-ROM drives. That is, they are introduced to service some capabilities of certain drives. In fact, there are 6 different <em>ioctl()'s</em> for reading data, either in some particular kind of format, or audio data. Not many drives support reading audio tracks as data, I believe this is because of protection of copyrights of artists. Moreover, I think that if audio-tracks are supported, it should be done through the VFS and not via <em>ioctl()'s</em>. A problem here could be the fact that audio-frames are 2352 bytes long, so either the audio-file-system should ask for 75264 bytes at once (the least common multiple of 512 and 2352), or the drivers should bend their backs to cope with this incoherence (to which I would be opposed). Furthermore, it is very difficult for the hardware to find the exact frame boundaries, since there are no synchronization headers in audio frames. Once these issues are resolved, this code should be standardized in `cdrom.c`.

Because there are so many <em>ioctl()'s</em> that seem to be introduced to satisfy certain drivers <a id="rst-footnote-reference-2"></a>[2](#rst-f2), any non-standard <em>ioctl()</em>s are routed through the call <em>dev\_ioctl()</em>. In principle, `private` <em>ioctl()</em>'s should be numbered after the device's major number, and not the general CD-ROM <em>ioctl</em> number, `0x53`. Currently the non-supported <em>ioctl()'s</em> are:

> CDROMREADMODE1, CDROMREADMODE2, CDROMREADAUDIO, CDROMREADRAW, CDROMREADCOOKED, CDROMSEEK, CDROMPLAY-BLK and CDROM-READALL

<a id="rst-f2"></a>



**[2]** Is there software around that actually uses these? I'd be interested\!

<a id="rst-cd-rom-capabilities"></a>
<a id="rst-cdrom-capabilities"></a>

### CD-ROM capabilities

Instead of just implementing some <em>ioctl</em> calls, the interface in `cdrom.c` supplies the possibility to indicate the <strong>capabilities</strong> of a CD-ROM drive. This can be done by ORing any number of capability-constants that are defined in `cdrom.h` at the registration phase. Currently, the capabilities are any of:



```text
CDC_CLOSE_TRAY          /* can close tray by software control */
CDC_OPEN_TRAY           /* can open tray */
CDC_LOCK                /* can lock and unlock the door */
CDC_SELECT_SPEED        /* can select speed, in units of * sim*150 ,kB/s */
CDC_SELECT_DISC         /* drive is juke-box */
CDC_MULTI_SESSION       /* can read sessions *> rm1* */
CDC_MCN                 /* can read Media Catalog Number */
CDC_MEDIA_CHANGED       /* can report if disc has changed */
CDC_PLAY_AUDIO          /* can perform audio-functions (play, pause, etc) */
CDC_RESET               /* hard reset device */
CDC_IOCTLS              /* driver has non-standard ioctls */
CDC_DRIVE_STATUS        /* driver implements drive status */
```

The capability flag is declared <em>const</em>, to prevent drivers from accidentally tampering with the contents. The capability flags actually inform `cdrom.c` of what the driver can do. If the drive found by the driver does not have the capability, is can be masked out by the <em>cdrom\_device\_info</em> variable <em>mask</em>. For instance, the SCSI CD-ROM driver has implemented the code for loading and ejecting CD-ROM's, and hence its corresponding flags in <em>capability</em> will be set. But a SCSI CD-ROM drive might be a caddy system, which can't load the tray, and hence for this drive the <em>cdrom\_device\_info</em> struct will have set the <em>CDC\_CLOSE\_TRAY</em> bit in <em>mask</em>.

In the file `cdrom.c` you will encounter many constructions of the type:



```text
if (cdo->capability & ~cdi->mask & CDC _<capability>) ...
```

There is no <em>ioctl</em> to set the mask... The reason is that I think it is better to control the <strong>behavior</strong> rather than the <strong>capabilities</strong>.

<a id="rst-options"></a>

### Options

A final flag register controls the <strong>behavior</strong> of the CD-ROM drives, in order to satisfy different users' wishes, hopefully independently of the ideas of the respective author who happened to have made the drive's support available to the Linux community. The current behavior options are:



```text
CDO_AUTO_CLOSE  /* try to close tray upon device open() */
CDO_AUTO_EJECT  /* try to open tray on last device close() */
CDO_USE_FFLAGS  /* use file_pointer->f_flags to indicate purpose for open() */
CDO_LOCK        /* try to lock door if device is opened */
CDO_CHECK_TYPE  /* ensure disc type is data if opened for data */
```

The initial value of this register is `CDO_AUTO_CLOSE | CDO_USE_FFLAGS | CDO_LOCK`, reflecting my own view on user interface and software standards. Before you protest, there are two new <em>ioctl()'s</em> implemented in `cdrom.c`, that allow you to control the behavior by software. These are:



```text
CDROM_SET_OPTIONS       /* set options specified in (int)arg */
CDROM_CLEAR_OPTIONS     /* clear options specified in (int)arg */
```

One option needs some more explanation: <em>CDO\_USE\_FFLAGS</em>. In the next newsection we explain what the need for this option is.

A software package `setcd`, available from the Debian distribution and `sunsite.unc.edu`, allows user level control of these flags.

<a id="rst-the-need-to-know-the-purpose-of-opening-the-cd-rom-device"></a>

## The need to know the purpose of opening the CD-ROM device

Traditionally, Unix devices can be used in two different `modes`, either by reading/writing to the device file, or by issuing controlling commands to the device, by the device's <em>ioctl()</em> call. The problem with CD-ROM drives, is that they can be used for two entirely different purposes. One is to mount removable file systems, CD-ROM's, the other is to play audio CD's. Audio commands are implemented entirely through <em>ioctl()'s</em>, presumably because the first implementation (SUN?) has been such. In principle there is nothing wrong with this, but a good control of the `CD player` demands that the device can <strong>always</strong> be opened in order to give the <em>ioctl</em> commands, regardless of the state the drive is in.

On the other hand, when used as a removable-media disc drive (what the original purpose of CD-ROM s is) we would like to make sure that the disc drive is ready for operation upon opening the device. In the old scheme, some CD-ROM drivers don't do any integrity checking, resulting in a number of i/o errors reported by the VFS to the kernel when an attempt for mounting a CD-ROM on an empty drive occurs. This is not a particularly elegant way to find out that there is no CD-ROM inserted; it more-or-less looks like the old IBM-PC trying to read an empty floppy drive for a couple of seconds, after which the system complains it can't read from it. Nowadays we can <strong>sense</strong> the existence of a removable medium in a drive, and we believe we should exploit that fact. An integrity check on opening of the device, that verifies the availability of a CD-ROM and its correct type (data), would be desirable.

These two ways of using a CD-ROM drive, principally for data and secondarily for playing audio discs, have different demands for the behavior of the <em>open()</em> call. Audio use simply wants to open the device in order to get a file handle which is needed for issuing <em>ioctl</em> commands, while data use wants to open for correct and reliable data transfer. The only way user programs can indicate what their <em>purpose</em> of opening the device is, is through the <em>flags</em> parameter (see `open(2)`). For CD-ROM devices, these flags aren't implemented (some drivers implement checking for write-related flags, but this is not strictly necessary if the device file has correct permission flags). Most option flags simply don't make sense to CD-ROM devices: <em>O\_CREAT</em>, <em>O\_NOCTTY</em>, <em>O\_TRUNC</em>, <em>O\_APPEND</em>, and <em>O\_SYNC</em> have no meaning to a CD-ROM.

We therefore propose to use the flag <em>O\_NONBLOCK</em> to indicate that the device is opened just for issuing <em>ioctl</em> commands. Strictly, the meaning of <em>O\_NONBLOCK</em> is that opening and subsequent calls to the device don't cause the calling process to wait. We could interpret this as don't wait until someone has inserted some valid data-CD-ROM. Thus, our proposal of the implementation for the <em>open()</em> call for CD-ROM s is:

- If no other flags are set than <em>O\_RDONLY</em>, the device is opened for data transfer, and the return value will be 0 only upon successful initialization of the transfer. The call may even induce some actions on the CD-ROM, such as closing the tray.

- If the option flag <em>O\_NONBLOCK</em> is set, opening will always be successful, unless the whole device doesn't exist. The drive will take no actions whatsoever.

<a id="rst-and-what-about-standards"></a>

### And what about standards?

You might hesitate to accept this proposal as it comes from the Linux community, and not from some standardizing institute. What about SUN, SGI, HP and all those other Unix and hardware vendors? Well, these companies are in the lucky position that they generally control both the hardware and software of their supported products, and are large enough to set their own standard. They do not have to deal with a dozen or more different, competing hardware configurations<a id="rst-footnote-reference-3"></a>[3](#rst-f3).

<a id="rst-f3"></a>



**[3]** Incidentally, I think that SUN's approach to mounting CD-ROM s is very good in origin: under Solaris a volume-daemon automatically mounts a newly inserted CD-ROM under `/cdrom/*<volume-name>*`.

In my opinion they should have pushed this further and have <strong>every</strong> CD-ROM on the local area network be mounted at the similar location, i. e., no matter in which particular machine you insert a CD-ROM, it will always appear at the same position in the directory tree, on every system. When I wanted to implement such a user-program for Linux, I came across the differences in behavior of the various drivers, and the need for an <em>ioctl</em> informing about media changes.

We believe that using <em>O\_NONBLOCK</em> to indicate that a device is being opened for <em>ioctl</em> commands only can be easily introduced in the Linux community. All the CD-player authors will have to be informed, we can even send in our own patches to the programs. The use of <em>O\_NONBLOCK</em> has most likely no influence on the behavior of the CD-players on other operating systems than Linux. Finally, a user can always revert to old behavior by a call to <em>ioctl(file\_descriptor, CDROM\_CLEAR\_OPTIONS, CDO\_USE\_FFLAGS)</em>.

<a id="rst-the-preferred-strategy-of-open"></a>

### The preferred strategy of <em>open()</em>

The routines in `cdrom.c` are designed in such a way that run-time configuration of the behavior of CD-ROM devices (of <strong>any</strong> type) can be carried out, by the <em>CDROM\_SET/CLEAR\_OPTIONS</em> <em>ioctls</em>. Thus, various modes of operation can be set:

- **`CDO_AUTO_CLOSE | CDO_USE_FFLAGS | CDO_LOCK`**

  This is the default setting. (With <em>CDO\_CHECK\_TYPE</em> it will be better, in the future.) If the device is not yet opened by any other process, and if the device is being opened for data (<em>O\_NONBLOCK</em> is not set) and the tray is found to be open, an attempt to close the tray is made. Then, it is verified that a disc is in the drive and, if <em>CDO\_CHECK\_TYPE</em> is set, that it contains tracks of type `data mode 1`. Only if all tests are passed is the return value zero. The door is locked to prevent file system corruption. If the drive is opened for audio (<em>O\_NONBLOCK</em> is set), no actions are taken and a value of 0 will be returned.

- **`CDO_AUTO_CLOSE | CDO_AUTO_EJECT | CDO_LOCK`**

  This mimics the behavior of the current sbpcd-driver. The option flags are ignored, the tray is closed on the first open, if necessary. Similarly, the tray is opened on the last release, i. e., if a CD-ROM is unmounted, it is automatically ejected, such that the user can replace it.

We hope that these option can convince everybody (both driver maintainers and user program developers) to adopt the new CD-ROM driver scheme and option flag interpretation.

<a id="rst-description-of-routines-in-cdrom-c"></a>

## Description of routines in `cdrom.c`

Only a few routines in `cdrom.c` are exported to the drivers. In this new section we will discuss these, as well as the functions that `take over` the CD-ROM interface to the kernel. The header file belonging to `cdrom.c` is called `cdrom.h`. Formerly, some of the contents of this file were placed in the file `ucdrom.h`, but this file has now been merged back into `cdrom.h`.



```text
struct file_operations cdrom_fops
```

The contents of this structure were described in [cdrom\_api](<#rst-cdrom-api>). A pointer to this structure is assigned to the <em>fops</em> field of the <em>struct gendisk</em>.



```text
int register_cdrom(struct cdrom_device_info *cdi)
```

This function is used in about the same way one registers <em>cdrom\_fops</em> with the kernel, the device operations and information structures, as described in [cdrom\_api](<#rst-cdrom-api>), should be registered with the Uniform CD-ROM Driver:



```text
register_cdrom(&<device>_info);
```

This function returns zero upon success, and non-zero upon failure. The structure <em>&lt;device&gt;\_info</em> should have a pointer to the driver's <em>&lt;device&gt;\_dops</em>, as in:



```text
struct cdrom_device_info <device>_info = {
        <device>_dops;
        ...
}
```

Note that a driver must have one static structure, <em>&lt;device&gt;\_dops</em>, while it may have as many structures <em>&lt;device&gt;\_info</em> as there are minor devices active. <em>Register\_cdrom()</em> builds a linked list from these.



```text
void unregister_cdrom(struct cdrom_device_info *cdi)
```

Unregistering device <em>cdi</em> with minor number <em>MINOR(cdi-&gt;dev)</em> removes the minor device from the list. If it was the last registered minor for the low-level driver, this disconnects the registered device-operation routines from the CD-ROM interface. This function returns zero upon success, and non-zero upon failure.



```text
int cdrom_open(struct inode * ip, struct file * fp)
```

This function is not called directly by the low-level drivers, it is listed in the standard <em>cdrom\_fops</em>. If the VFS opens a file, this function becomes active. A strategy is implemented in this routine, taking care of all capabilities and options that are set in the <em>cdrom\_device\_ops</em> connected to the device. Then, the program flow is transferred to the device\_dependent <em>open()</em> call.



```text
void cdrom_release(struct inode *ip, struct file *fp)
```

This function implements the reverse-logic of <em>cdrom\_open()</em>, and then calls the device-dependent <em>release()</em> routine. When the use-count has reached 0, the allocated buffers are flushed by calls to <em>sync\_dev(dev)</em> and <em>invalidate\_buffers(dev)</em>.

<a id="rst-cdrom-ioctl"></a>



```text
int cdrom_ioctl(struct inode *ip, struct file *fp,
                unsigned int cmd, unsigned long arg)
```

This function handles all the standard <em>ioctl</em> requests for CD-ROM devices in a uniform way. The different calls fall into three categories: <em>ioctl()'s</em> that can be directly implemented by device operations, ones that are routed through the call <em>audio\_ioctl()</em>, and the remaining ones, that are presumable device-dependent. Generally, a negative return value indicates an error.

<a id="rst-directly-implemented-ioctl-s"></a>

### Directly implemented <em>ioctl()'s</em>

The following `old` CD-ROM <em>ioctl()</em>'s are implemented by directly calling device-operations in <em>cdrom\_device\_ops</em>, if implemented and not masked:

- **`CDROMMULTISESSION`**

  Requests the last session on a CD-ROM.

- **`CDROMEJECT`**

  Open tray.

- **`CDROMCLOSETRAY`**

  Close tray.

- **`CDROMEJECT_SW`**

  If <em>argnot=0</em>, set behavior to auto-close (close tray on first open) and auto-eject (eject on last release), otherwise set behavior to non-moving on <em>open()</em> and <em>release()</em> calls.

- **`CDROM_GET_MCN`**

  Get the Media Catalog Number from a CD.

<a id="rst-ioctl-s-routed-through-audio-ioctl"></a>

### <em>Ioctl\*s routed through \*audio\_ioctl()</em>

The following set of <em>ioctl()'s</em> are all implemented through a call to the <em>cdrom\_fops</em> function <em>audio\_ioctl()</em>. Memory checks and allocation are performed in <em>cdrom\_ioctl()</em>, and also sanitization of address format (<em>CDROM\_LBA</em>/<em>CDROM\_MSF</em>) is done.

- **`CDROMSUBCHNL`**

  Get sub-channel data in argument <em>arg</em> of type `struct cdrom_subchnl *`.

- **`CDROMREADTOCHDR`**

  Read Table of Contents header, in <em>arg</em> of type `struct cdrom_tochdr *`.

- **`CDROMREADTOCENTRY`**

  Read a Table of Contents entry in <em>arg</em> and specified by <em>arg</em> of type `struct cdrom_tocentry *`.

- **`CDROMPLAYMSF`**

  Play audio fragment specified in Minute, Second, Frame format, delimited by <em>arg</em> of type `struct cdrom_msf *`.

- **`CDROMPLAYTRKIND`**

  Play audio fragment in track-index format delimited by <em>arg</em> of type `struct cdrom_ti *`.

- **`CDROMVOLCTRL`**

  Set volume specified by <em>arg</em> of type `struct cdrom_volctrl *`.

- **`CDROMVOLREAD`**

  Read volume into by <em>arg</em> of type `struct cdrom_volctrl *`.

- **`CDROMSTART`**

  Spin up disc.

- **`CDROMSTOP`**

  Stop playback of audio fragment.

- **`CDROMPAUSE`**

  Pause playback of audio fragment.

- **`CDROMRESUME`**

  Resume playing.

<a id="rst-new-ioctl-s-in-cdrom-c"></a>

### New <em>ioctl()'s</em> in `cdrom.c`

The following <em>ioctl()'s</em> have been introduced to allow user programs to control the behavior of individual CD-ROM devices. New <em>ioctl</em> commands can be identified by the underscores in their names.

- **`CDROM_SET_OPTIONS`**

  Set options specified by <em>arg</em>. Returns the option flag register after modification. Use <em>arg = rm0</em> for reading the current flags.

- **`CDROM_CLEAR_OPTIONS`**

  Clear options specified by <em>arg</em>. Returns the option flag register after modification.

- **`CDROM_SELECT_SPEED`**

  Select head-rate speed of disc specified as by <em>arg</em> in units of standard cdrom speed (176,kB/sec raw data or 150kB/sec file system data). The value 0 means `auto-select`, i. e., play audio discs at real time and data discs at maximum speed. The value <em>arg</em> is checked against the maximum head rate of the drive found in the <em>cdrom\_dops</em>.

- **`CDROM_SELECT_DISC`**

  Select disc numbered <em>arg</em> from a juke-box.

  First disc is numbered 0. The number <em>arg</em> is checked against the maximum number of discs in the juke-box found in the <em>cdrom\_dops</em>.

- **`CDROM_MEDIA_CHANGED`**

  Returns 1 if a disc has been changed since the last call. For juke-boxes, an extra argument <em>arg</em> specifies the slot for which the information is given. The special value <em>CDSL\_CURRENT</em> requests that information about the currently selected slot be returned.

- **`CDROM_TIMED_MEDIA_CHANGE`**

  Checks whether the disc has been changed since a user supplied time and returns the time of the last disc change.

  <em>arg</em> is a pointer to a <em>cdrom\_timed\_media\_change\_info</em> struct. <em>arg-&gt;last\_media\_change</em> may be set by calling code to signal the timestamp of the last known media change (by the caller). Upon successful return, this ioctl call will set <em>arg-&gt;last\_media\_change</em> to the latest media change timestamp (in ms) known by the kernel/driver and set <em>arg-&gt;has\_changed</em> to 1 if that timestamp is more recent than the timestamp set by the caller.

- **`CDROM_DRIVE_STATUS`**

  Returns the status of the drive by a call to <em>drive\_status()</em>. Return values are defined in [cdrom\_drive\_status](<#rst-cdrom-drive-status>). Note that this call doesn't return information on the current playing activity of the drive; this can be polled through an <em>ioctl</em> call to <em>CDROMSUBCHNL</em>. For juke-boxes, an extra argument <em>arg</em> specifies the slot for which (possibly limited) information is given. The special value <em>CDSL\_CURRENT</em> requests that information about the currently selected slot be returned.

- **`CDROM_DISC_STATUS`**

  Returns the type of the disc currently in the drive. It should be viewed as a complement to <em>CDROM\_DRIVE\_STATUS</em>. This <em>ioctl</em> can provide <em>some</em> information about the current disc that is inserted in the drive. This functionality used to be implemented in the low level drivers, but is now carried out entirely in Uniform CD-ROM Driver.

  The history of development of the CD's use as a carrier medium for various digital information has lead to many different disc types. This <em>ioctl</em> is useful only in the case that CDs have emph \{only one\} type of data on them. While this is often the case, it is also very common for CDs to have some tracks with data, and some tracks with audio. Because this is an existing interface, rather than fixing this interface by changing the assumptions it was made under, thereby breaking all user applications that use this function, the Uniform CD-ROM Driver implements this <em>ioctl</em> as follows: If the CD in question has audio tracks on it, and it has absolutely no CD-I, XA, or data tracks on it, it will be reported as <em>CDS\_AUDIO</em>. If it has both audio and data tracks, it will return <em>CDS\_MIXED</em>. If there are no audio tracks on the disc, and if the CD in question has any CD-I tracks on it, it will be reported as <em>CDS\_XA\_2\_2</em>. Failing that, if the CD in question has any XA tracks on it, it will be reported as <em>CDS\_XA\_2\_1</em>. Finally, if the CD in question has any data tracks on it, it will be reported as a data CD (<em>CDS\_DATA\_1</em>).

  This <em>ioctl</em> can return:



  ```text
  CDS_NO_INFO     /* no information available */
  CDS_NO_DISC     /* no disc is inserted, or tray is opened */
  CDS_AUDIO       /* Audio disc (2352 audio bytes/frame) */
  CDS_DATA_1      /* data disc, mode 1 (2048 user bytes/frame) */
  CDS_XA_2_1      /* mixed data (XA), mode 2, form 1 (2048 user bytes) */
  CDS_XA_2_2      /* mixed data (XA), mode 2, form 1 (2324 user bytes) */
  CDS_MIXED       /* mixed audio/data disc */
  ```

  For some information concerning frame layout of the various disc types, see a recent version of `cdrom.h`.

- **`CDROM_CHANGER_NSLOTS`**

  Returns the number of slots in a juke-box.

- **`CDROMRESET`**

  Reset the drive.

- **`CDROM_GET_CAPABILITY`**

  Returns the <em>capability</em> flags for the drive. Refer to section [cdrom\_capabilities](<#rst-cdrom-capabilities>) for more information on these flags.

- **`CDROM_LOCKDOOR`**

  Locks the door of the drive. `arg == 0` unlocks the door, any other value locks it.

- **`CDROM_DEBUG`**

  Turns on debugging info. Only root is allowed to do this. Same semantics as CDROM\_LOCKDOOR.

<a id="rst-device-dependent-ioctl-s"></a>

### Device dependent <em>ioctl()'s</em>

Finally, all other <em>ioctl()'s</em> are passed to the function <em>dev\_ioctl()</em>, if implemented. No memory allocation or verification is carried out.

<a id="rst-how-to-update-your-driver"></a>

## How to update your driver

- Make a backup of your current driver.

- Get hold of the files `cdrom.c` and `cdrom.h`, they should be in the directory tree that came with this documentation.

- Make sure you include `cdrom.h`.

- Change the 3rd argument of <em>register\_blkdev</em> from `&<your-drive>_fops` to `&cdrom_fops`.

- Just after that line, add the following to register with the Uniform CD-ROM Driver:



  ```text
  register_cdrom(&<your-drive>_info);*
  ```

  Similarly, add a call to <em>unregister\_cdrom()</em> at the appropriate place.

- Copy an example of the device-operations <em>struct</em> to your source, e. g., from `cm206.c` <em>cm206\_dops</em>, and change all entries to names corresponding to your driver, or names you just happen to like. If your driver doesn't support a certain function, make the entry <em>NULL</em>. At the entry <em>capability</em> you should list all capabilities your driver currently supports. If your driver has a capability that is not listed, please send me a message.

- Copy the <em>cdrom\_device\_info</em> declaration from the same example driver, and modify the entries according to your needs. If your driver dynamically determines the capabilities of the hardware, this structure should also be declared dynamically.

- Implement all functions in your `<device>_dops` structure, according to prototypes listed in  `cdrom.h`, and specifications given in [cdrom\_api](<#rst-cdrom-api>). Most likely you have already implemented the code in a large part, and you will almost certainly need to adapt the prototype and return values.

- Rename your `<device>_ioctl()` function to <em>audio\_ioctl</em> and change the prototype a little. Remove entries listed in the first part in [cdrom\_ioctl](<#rst-cdrom-ioctl>), if your code was OK, these are just calls to the routines you adapted in the previous step.

- You may remove all remaining memory checking code in the <em>audio\_ioctl()</em> function that deals with audio commands (these are listed in the second part of [cdrom\_ioctl](<#rst-cdrom-ioctl>). There is no need for memory allocation either, so most <em>case\*s in the \*switch</em> statement look similar to:



  ```text
  case CDROMREADTOCENTRY:
          get_toc_entry\bigl((struct cdrom_tocentry *) arg);
  ```

- All remaining <em>ioctl</em> cases must be moved to a separate function, <em>&lt;device&gt;\_ioctl</em>, the device-dependent <em>ioctl()'s</em>. Note that memory checking and allocation must be kept in this code\!

- Change the prototypes of <em>&lt;device&gt;\_open()</em> and <em>&lt;device&gt;\_release()</em>, and remove any strategic code (i. e., tray movement, door locking, etc.).

- Try to recompile the drivers. We advise you to use modules, both for `cdrom.o` and your driver, as debugging is much easier this way.

<a id="rst-thanks"></a>

## Thanks

Thanks to all the people involved. First, Erik Andersen, who has taken over the torch in maintaining `cdrom.c` and integrating much CD-ROM-related code in the 2.1-kernel. Thanks to Scott Snyder and Gerd Knorr, who were the first to implement this interface for SCSI and IDE-CD drivers and added many ideas for extension of the data structures relative to kernel\~2.0. Further thanks to Heiko Eißfeldt, Thomas Quinot, Jon Tombs, Ken Pizzini, Eberhard Mönkeberg and Andrew Kroll, the Linux CD-ROM device driver developers who were kind enough to give suggestions and criticisms during the writing. Finally of course, I want to thank Linus Torvalds for making this possible in the first place.
