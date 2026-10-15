---
title: "PARPORT interface documentation"
type: reference
description: "Described here are the following functions:"
---

<a id="rst-parport-interface-documentation"></a>

**Time-stamp:** &lt;2000-02-24 13:30:20 twaugh&gt;

Described here are the following functions:

Global functions:



```text
parport_register_driver
parport_unregister_driver
parport_enumerate
parport_register_device
parport_unregister_device
parport_claim
parport_claim_or_block
parport_release
parport_yield
parport_yield_blocking
parport_wait_peripheral
parport_poll_peripheral
parport_wait_event
parport_negotiate
parport_read
parport_write
parport_open
parport_close
parport_device_id
parport_device_coords
parport_find_class
parport_find_device
parport_set_timeout
```

Port functions (can be overridden by low-level drivers):

> SPP:
>
>
>
> ```text
> port->ops->read_data
> port->ops->write_data
> port->ops->read_status
> port->ops->read_control
> port->ops->write_control
> port->ops->frob_control
> port->ops->enable_irq
> port->ops->disable_irq
> port->ops->data_forward
> port->ops->data_reverse
> ```
>
> EPP:
>
>
>
> ```text
> port->ops->epp_write_data
> port->ops->epp_read_data
> port->ops->epp_write_addr
> port->ops->epp_read_addr
> ```
>
> ECP:
>
>
>
> ```text
> port->ops->ecp_write_data
> port->ops->ecp_read_data
> port->ops->ecp_write_addr
> ```
>
> Other:
>
>
>
> ```text
> port->ops->nibble_read_data
> port->ops->byte_read_data
> port->ops->compat_write_data
> ```

The parport subsystem comprises `parport` (the core port-sharing code), and a variety of low-level drivers that actually do the port accesses.  Each low-level driver handles a particular style of port (PC, Amiga, and so on).

The parport interface to the device driver author can be broken down into global functions and port functions.

The global functions are mostly for communicating between the device driver and the parport subsystem: acquiring a list of available ports, claiming a port for exclusive use, and so on.  They also include `generic` functions for doing standard things that will work on any IEEE 1284-capable architecture.

The port functions are provided by the low-level drivers, although the core parport module provides generic `defaults` for some routines. The port functions can be split into three groups: SPP, EPP, and ECP.

SPP (Standard Parallel Port) functions modify so-called `SPP` registers: data, status, and control.  The hardware may not actually have registers exactly like that, but the PC does and this interface is modelled after common PC implementations.  Other low-level drivers may be able to emulate most of the functionality.

EPP (Enhanced Parallel Port) functions are provided for reading and writing in IEEE 1284 EPP mode, and ECP (Extended Capabilities Port) functions are used for IEEE 1284 ECP mode. (What about BECP? Does anyone care?)

Hardware assistance for EPP and/or ECP transfers may or may not be available, and if it is available it may or may not be used.  If hardware is not used, the transfer will be software-driven.  In order to cope with peripherals that only tenuously support IEEE 1284, a low-level driver specific function is provided, for altering 'fudge factors'.

<a id="rst-global-functions"></a>

## Global functions

<a id="rst-parport-register-driver-register-a-device-driver-with-parport"></a>

### parport_register_driver - register a device driver with parport

<a id="rst-synopsis"></a>

#### SYNOPSIS



```text
#include <linux/parport.h>

struct parport_driver {
        const char *name;
        void (*attach) (struct parport *);
        void (*detach) (struct parport *);
        struct parport_driver *next;
};
int parport_register_driver (struct parport_driver *driver);
```

<a id="rst-description"></a>

#### DESCRIPTION

In order to be notified about parallel ports when they are detected, parport_register_driver should be called.  Your driver will immediately be notified of all ports that have already been detected, and of each new port as low-level drivers are loaded.

A `struct parport_driver` contains the textual name of your driver, a pointer to a function to handle new ports, and a pointer to a function to handle ports going away due to a low-level driver unloading.  Ports will only be detached if they are not being used (i.e. there are no devices registered on them).

The visible parts of the `struct parport *` argument given to attach/detach are:



```text
struct parport
{
        struct parport *next; /* next parport in list */
        const char *name;     /* port's name */
        unsigned int modes;   /* bitfield of hardware modes */
        struct parport_device_info probe_info;
                        /* IEEE1284 info */
        int number;           /* parport index */
        struct parport_operations *ops;
        ...
};
```

There are other members of the structure, but they should not be touched.

The `modes` member summarises the capabilities of the underlying hardware.  It consists of flags which may be bitwise-ored together:

>
> <table>
> <tbody>
> <tr>
> <td>
>
>
> PARPORT_MODE_PCSPP
>
> </td>
> <td>
>
>
> IBM PC registers are available, i.e. functions that act on data, control and status registers are probably writing directly to the hardware.
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> PARPORT_MODE_TRISTATE
>
> </td>
> <td>
>
>
> The data drivers may be turned off. This allows the data lines to be used for reverse (peripheral to host) transfers.
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> PARPORT_MODE_COMPAT
>
> </td>
> <td>
>
>
> The hardware can assist with compatibility-mode (printer) transfers, i.e. compat_write_block.
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> PARPORT_MODE_EPP
>
> </td>
> <td>
>
>
> The hardware can assist with EPP transfers.
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> PARPORT_MODE_ECP
>
> </td>
> <td>
>
>
> The hardware can assist with ECP transfers.
>
> </td>
> </tr>
> <tr>
> <td>
>
>
> PARPORT_MODE_DMA
>
> </td>
> <td>
>
>
> The hardware can use DMA, so you might want to pass ISA DMA-able memory (i.e. memory allocated using the GFP_DMA flag with kmalloc) to the low-level driver in order to take advantage of it.
>
> </td>
> </tr>
> </tbody>
> </table>

There may be other flags in `modes` as well.

The contents of `modes` is advisory only.  For example, if the hardware is capable of DMA, and PARPORT_MODE_DMA is in `modes`, it doesn't necessarily mean that DMA will always be used when possible. Similarly, hardware that is capable of assisting ECP transfers won't necessarily be used.

<a id="rst-return-value"></a>

#### RETURN VALUE

Zero on success, otherwise an error code.

<a id="rst-errors"></a>

#### ERRORS

None. (Can it fail? Why return int?)

<a id="rst-example"></a>

#### EXAMPLE



```text
static void lp_attach (struct parport *port)
{
        ...
        private = kmalloc (...);
        dev[count++] = parport_register_device (...);
        ...
}

static void lp_detach (struct parport *port)
{
        ...
}

static struct parport_driver lp_driver = {
        "lp",
        lp_attach,
        lp_detach,
        NULL /* always put NULL here */
};

int lp_init (void)
{
        ...
        if (parport_register_driver (&lp_driver)) {
                /* Failed; nothing we can do. */
                return -EIO;
        }
        ...
}
```

<a id="rst-see-also"></a>

#### SEE ALSO

parport_unregister_driver, parport_register_device, parport_enumerate

<a id="rst-parport-unregister-driver-tell-parport-to-forget-about-this-driver"></a>

### parport_unregister_driver - tell parport to forget about this driver

<a id="rst-synopsis-1"></a>

#### SYNOPSIS



```text
#include <linux/parport.h>

struct parport_driver {
        const char *name;
        void (*attach) (struct parport *);
        void (*detach) (struct parport *);
        struct parport_driver *next;
};
void parport_unregister_driver (struct parport_driver *driver);
```

<a id="rst-description-1"></a>

#### DESCRIPTION

This tells parport not to notify the device driver of new ports or of ports going away.  Registered devices belonging to that driver are NOT unregistered: parport_unregister_device must be used for each one.

<a id="rst-example-1"></a>

#### EXAMPLE



```text
void cleanup_module (void)
{
        ...
        /* Stop notifications. */
        parport_unregister_driver (&lp_driver);

        /* Unregister devices. */
        for (i = 0; i < NUM_DEVS; i++)
                parport_unregister_device (dev[i]);
        ...
}
```

<a id="rst-see-also-1"></a>

#### SEE ALSO

parport_register_driver, parport_enumerate

<a id="rst-parport-enumerate-retrieve-a-list-of-parallel-ports-deprecated"></a>

### parport_enumerate - retrieve a list of parallel ports (DEPRECATED)

<a id="rst-synopsis-2"></a>

#### SYNOPSIS



```text
#include <linux/parport.h>

struct parport *parport_enumerate (void);
```

<a id="rst-description-2"></a>

#### DESCRIPTION

Retrieve the first of a list of valid parallel ports for this machine. Successive parallel ports can be found using the `struct parport *next` element of the `struct parport *` that is returned.  If `next` is NULL, there are no more parallel ports in the list.  The number of ports in the list will not exceed PARPORT_MAX.

<a id="rst-return-value-1"></a>

#### RETURN VALUE

A `struct parport *` describing a valid parallel port for the machine, or NULL if there are none.

<a id="rst-errors-1"></a>

#### ERRORS

This function can return NULL to indicate that there are no parallel ports to use.

<a id="rst-example-2"></a>

#### EXAMPLE



```text
int detect_device (void)
{
        struct parport *port;

        for (port = parport_enumerate ();
        port != NULL;
        port = port->next) {
                /* Try to detect a device on the port... */
                ...
        }
        }

        ...
}
```

<a id="rst-notes"></a>

#### NOTES

parport_enumerate is deprecated; parport_register_driver should be used instead.

<a id="rst-see-also-2"></a>

#### SEE ALSO

parport_register_driver, parport_unregister_driver

<a id="rst-parport-register-device-register-to-use-a-port"></a>

### parport_register_device - register to use a port

<a id="rst-synopsis-3"></a>

#### SYNOPSIS



```text
#include <linux/parport.h>

typedef int (*preempt_func) (void *handle);
typedef void (*wakeup_func) (void *handle);
typedef int (*irq_func) (int irq, void *handle, struct pt_regs *);

struct pardevice *parport_register_device(struct parport *port,
                                          const char *name,
                                          preempt_func preempt,
                                          wakeup_func wakeup,
                                          irq_func irq,
                                          int flags,
                                          void *handle);
```

<a id="rst-description-3"></a>

#### DESCRIPTION

Use this function to register your device driver on a parallel port (`port`).  Once you have done that, you will be able to use parport_claim and parport_release in order to use the port.

The (`name`) argument is the name of the device that appears in /proc filesystem. The string must be valid for the whole lifetime of the device (until parport_unregister_device is called).

This function will register three callbacks into your driver: `preempt`, `wakeup` and `irq`.  Each of these may be NULL in order to indicate that you do not want a callback.

When the `preempt` function is called, it is because another driver wishes to use the parallel port.  The `preempt` function should return non-zero if the parallel port cannot be released yet -- if zero is returned, the port is lost to another driver and the port must be re-claimed before use.

The `wakeup` function is called once another driver has released the port and no other driver has yet claimed it.  You can claim the parallel port from within the `wakeup` function (in which case the claim is guaranteed to succeed), or choose not to if you don't need it now.

If an interrupt occurs on the parallel port your driver has claimed, the `irq` function will be called. (Write something about shared interrupts here.)

The `handle` is a pointer to driver-specific data, and is passed to the callback functions.

`flags` may be a bitwise combination of the following flags:

>
> <table>
> <thead>
> <tr>
> <th>
>
>
> Flag
>
> </th>
> <th>
>
>
> Meaning
>
> </th>
> </tr>
> </thead>
> <tbody>
> <tr>
> <td>
>
>
> PARPORT_DEV_EXCL
>
> </td>
> <td>
>
>
> The device cannot share the parallel port at all. Use this only when absolutely necessary.
>
> </td>
> </tr>
> </tbody>
> </table>

The typedefs are not actually defined -- they are only shown in order to make the function prototype more readable.

The visible parts of the returned `struct pardevice` are:



```text
struct pardevice {
        struct parport *port;   /* Associated port */
        void *private;          /* Device driver's 'handle' */
        ...
};
```

<a id="rst-return-value-2"></a>

#### RETURN VALUE

A `struct pardevice *`: a handle to the registered parallel port device that can be used for parport_claim, parport_release, etc.

<a id="rst-errors-2"></a>

#### ERRORS

A return value of NULL indicates that there was a problem registering a device on that port.

<a id="rst-example-3"></a>

#### EXAMPLE



```text
static int preempt (void *handle)
{
        if (busy_right_now)
                return 1;

        must_reclaim_port = 1;
        return 0;
}

static void wakeup (void *handle)
{
        struct toaster *private = handle;
        struct pardevice *dev = private->dev;
        if (!dev) return; /* avoid races */

        if (want_port)
                parport_claim (dev);
}

static int toaster_detect (struct toaster *private, struct parport *port)
{
        private->dev = parport_register_device (port, "toaster", preempt,
                                                wakeup, NULL, 0,
                                                private);
        if (!private->dev)
                /* Couldn't register with parport. */
                return -EIO;

        must_reclaim_port = 0;
        busy_right_now = 1;
        parport_claim_or_block (private->dev);
        ...
        /* Don't need the port while the toaster warms up. */
        busy_right_now = 0;
        ...
        busy_right_now = 1;
        if (must_reclaim_port) {
                parport_claim_or_block (private->dev);
                must_reclaim_port = 0;
        }
        ...
}
```

<a id="rst-see-also-3"></a>

#### SEE ALSO

parport_unregister_device, parport_claim

<a id="rst-parport-unregister-device-finish-using-a-port"></a>

### parport_unregister_device - finish using a port

SYNPOPSIS



```text
#include <linux/parport.h>

void parport_unregister_device (struct pardevice *dev);
```

<a id="rst-description-4"></a>

#### DESCRIPTION

This function is the opposite of parport_register_device.  After using parport_unregister_device, `dev` is no longer a valid device handle.

You should not unregister a device that is currently claimed, although if you do it will be released automatically.

<a id="rst-example-4"></a>

#### EXAMPLE



```text
...
kfree (dev->private); /* before we lose the pointer */
parport_unregister_device (dev);
...
```

<a id="rst-see-also-4"></a>

#### SEE ALSO

parport_unregister_driver

<a id="rst-parport-claim-parport-claim-or-block-claim-the-parallel-port-for-a-device"></a>

### parport_claim, parport_claim_or_block - claim the parallel port for a device

<a id="rst-synopsis-4"></a>

#### SYNOPSIS



```text
#include <linux/parport.h>

int parport_claim (struct pardevice *dev);
int parport_claim_or_block (struct pardevice *dev);
```

<a id="rst-description-5"></a>

#### DESCRIPTION

These functions attempt to gain control of the parallel port on which `dev` is registered.  `parport_claim` does not block, but `parport_claim_or_block` may do. (Put something here about blocking interruptibly or non-interruptibly.)

You should not try to claim a port that you have already claimed.

<a id="rst-return-value-3"></a>

#### RETURN VALUE

A return value of zero indicates that the port was successfully claimed, and the caller now has possession of the parallel port.

If `parport_claim_or_block` blocks before returning successfully, the return value is positive.

<a id="rst-errors-3"></a>

#### ERRORS


<table>
<tbody>
<tr>
<td>


-EAGAIN

</td>
<td>


The port is unavailable at the moment, but another attempt to claim it may succeed.

</td>
</tr>
</tbody>
</table>

<a id="rst-see-also-5"></a>

#### SEE ALSO

parport_release

<a id="rst-parport-release-release-the-parallel-port"></a>

### parport_release - release the parallel port

<a id="rst-synopsis-5"></a>

#### SYNOPSIS



```text
#include <linux/parport.h>

void parport_release (struct pardevice *dev);
```

<a id="rst-description-6"></a>

#### DESCRIPTION

Once a parallel port device has been claimed, it can be released using `parport_release`.  It cannot fail, but you should not release a device that you do not have possession of.

<a id="rst-example-5"></a>

#### EXAMPLE



```text
static size_t write (struct pardevice *dev, const void *buf,
                size_t len)
{
        ...
        written = dev->port->ops->write_ecp_data (dev->port, buf,
                                                len);
        parport_release (dev);
        ...
}
```

<a id="rst-see-also-6"></a>

#### SEE ALSO

change_mode, parport_claim, parport_claim_or_block, parport_yield

<a id="rst-parport-yield-parport-yield-blocking-temporarily-release-a-parallel-port"></a>

### parport_yield, parport_yield_blocking - temporarily release a parallel port

<a id="rst-synopsis-6"></a>

#### SYNOPSIS



```text
#include <linux/parport.h>

int parport_yield (struct pardevice *dev)
int parport_yield_blocking (struct pardevice *dev);
```

<a id="rst-description-7"></a>

#### DESCRIPTION

When a driver has control of a parallel port, it may allow another driver to temporarily `borrow` it.  `parport_yield` does not block; `parport_yield_blocking` may do.

<a id="rst-return-value-4"></a>

#### RETURN VALUE

A return value of zero indicates that the caller still owns the port and the call did not block.

A positive return value from `parport_yield_blocking` indicates that the caller still owns the port and the call blocked.

A return value of -EAGAIN indicates that the caller no longer owns the port, and it must be re-claimed before use.

<a id="rst-errors-4"></a>

#### ERRORS


<table>
<tbody>
<tr>
<td>


-EAGAIN

</td>
<td>


Ownership of the parallel port was given away.

</td>
</tr>
</tbody>
</table>

<a id="rst-see-also-7"></a>

#### SEE ALSO

parport_release

<a id="rst-parport-wait-peripheral-wait-for-status-lines-up-to-35ms"></a>

### parport_wait_peripheral - wait for status lines, up to 35ms

<a id="rst-synopsis-7"></a>

#### SYNOPSIS



```text
#include <linux/parport.h>

int parport_wait_peripheral (struct parport *port,
                             unsigned char mask,
                             unsigned char val);
```

<a id="rst-description-8"></a>

#### DESCRIPTION

Wait for the status lines in mask to match the values in val.

<a id="rst-return-value-5"></a>

#### RETURN VALUE


<table>
<tbody>
<tr>
<td>


-EINTR

</td>
<td>


a signal is pending

</td>
</tr>
<tr>
<td>


0

</td>
<td>


the status lines in mask have values in val

</td>
</tr>
<tr>
<td>


1

</td>
<td>


timed out while waiting (35ms elapsed)

</td>
</tr>
</tbody>
</table>

<a id="rst-see-also-8"></a>

#### SEE ALSO

parport_poll_peripheral

<a id="rst-parport-poll-peripheral-wait-for-status-lines-in-usec"></a>

### parport_poll_peripheral - wait for status lines, in usec

<a id="rst-synopsis-8"></a>

#### SYNOPSIS



```text
#include <linux/parport.h>

int parport_poll_peripheral (struct parport *port,
                             unsigned char mask,
                             unsigned char val,
                             int usec);
```

<a id="rst-description-9"></a>

#### DESCRIPTION

Wait for the status lines in mask to match the values in val.

<a id="rst-return-value-6"></a>

#### RETURN VALUE


<table>
<tbody>
<tr>
<td>


-EINTR

</td>
<td>


a signal is pending

</td>
</tr>
<tr>
<td>


0

</td>
<td>


the status lines in mask have values in val

</td>
</tr>
<tr>
<td>


1

</td>
<td>


timed out while waiting (usec microseconds have elapsed)

</td>
</tr>
</tbody>
</table>

<a id="rst-see-also-9"></a>

#### SEE ALSO

parport_wait_peripheral

<a id="rst-parport-wait-event-wait-for-an-event-on-a-port"></a>

### parport_wait_event - wait for an event on a port

<a id="rst-synopsis-9"></a>

#### SYNOPSIS



```text
#include <linux/parport.h>

int parport_wait_event (struct parport *port, signed long timeout)
```

<a id="rst-description-10"></a>

#### DESCRIPTION

Wait for an event (e.g. interrupt) on a port.  The timeout is in jiffies.

<a id="rst-return-value-7"></a>

#### RETURN VALUE


<table>
<tbody>
<tr>
<td>


0

</td>
<td>


success

</td>
</tr>
<tr>
<td>


&lt;0

</td>
<td>


error (exit as soon as possible)

</td>
</tr>
<tr>
<td>


&gt;0

</td>
<td>


timed out

</td>
</tr>
</tbody>
</table>

<a id="rst-parport-negotiate-perform-ieee-1284-negotiation"></a>

### parport_negotiate - perform IEEE 1284 negotiation

<a id="rst-synopsis-10"></a>

#### SYNOPSIS



```text
#include <linux/parport.h>

int parport_negotiate (struct parport *, int mode);
```

<a id="rst-description-11"></a>

#### DESCRIPTION

Perform IEEE 1284 negotiation.

<a id="rst-return-value-8"></a>

#### RETURN VALUE


<table>
<tbody>
<tr>
<td>


0

</td>
<td>


handshake OK; IEEE 1284 peripheral and mode available

</td>
</tr>
<tr>
<td>


-1

</td>
<td>


handshake failed; peripheral not compliant (or none present)

</td>
</tr>
<tr>
<td>


1

</td>
<td>


handshake OK; IEEE 1284 peripheral present but mode not available

</td>
</tr>
</tbody>
</table>

<a id="rst-see-also-10"></a>

#### SEE ALSO

parport_read, parport_write

<a id="rst-parport-read-read-data-from-device"></a>

### parport_read - read data from device

<a id="rst-synopsis-11"></a>

#### SYNOPSIS



```text
#include <linux/parport.h>

ssize_t parport_read (struct parport *, void *buf, size_t len);
```

<a id="rst-description-12"></a>

#### DESCRIPTION

Read data from device in current IEEE 1284 transfer mode.  This only works for modes that support reverse data transfer.

<a id="rst-return-value-9"></a>

#### RETURN VALUE

If negative, an error code; otherwise the number of bytes transferred.

<a id="rst-see-also-11"></a>

#### SEE ALSO

parport_write, parport_negotiate

<a id="rst-parport-write-write-data-to-device"></a>

### parport_write - write data to device

<a id="rst-synopsis-12"></a>

#### SYNOPSIS



```text
#include <linux/parport.h>

ssize_t parport_write (struct parport *, const void *buf, size_t len);
```

<a id="rst-description-13"></a>

#### DESCRIPTION

Write data to device in current IEEE 1284 transfer mode.  This only works for modes that support forward data transfer.

<a id="rst-return-value-10"></a>

#### RETURN VALUE

If negative, an error code; otherwise the number of bytes transferred.

<a id="rst-see-also-12"></a>

#### SEE ALSO

parport_read, parport_negotiate

<a id="rst-parport-open-register-device-for-particular-device-number"></a>

### parport_open - register device for particular device number

<a id="rst-synopsis-13"></a>

#### SYNOPSIS



```text
#include <linux/parport.h>

struct pardevice *parport_open (int devnum, const char *name,
                                int (*pf) (void *),
                                void (*kf) (void *),
                                void (*irqf) (int, void *,
                                              struct pt_regs *),
                                int flags, void *handle);
```

<a id="rst-description-14"></a>

#### DESCRIPTION

This is like parport_register_device but takes a device number instead of a pointer to a struct parport.

<a id="rst-return-value-11"></a>

#### RETURN VALUE

See parport_register_device.  If no device is associated with devnum, NULL is returned.

<a id="rst-see-also-13"></a>

#### SEE ALSO

parport_register_device

<a id="rst-parport-close-unregister-device-for-particular-device-number"></a>

### parport_close - unregister device for particular device number

<a id="rst-synopsis-14"></a>

#### SYNOPSIS



```text
#include <linux/parport.h>

void parport_close (struct pardevice *dev);
```

<a id="rst-description-15"></a>

#### DESCRIPTION

This is the equivalent of parport_unregister_device for parport_open.

<a id="rst-see-also-14"></a>

#### SEE ALSO

parport_unregister_device, parport_open

<a id="rst-parport-device-id-obtain-ieee-1284-device-id"></a>

### parport_device_id - obtain IEEE 1284 Device ID

<a id="rst-synopsis-15"></a>

#### SYNOPSIS



```text
#include <linux/parport.h>

ssize_t parport_device_id (int devnum, char *buffer, size_t len);
```

<a id="rst-description-16"></a>

#### DESCRIPTION

Obtains the IEEE 1284 Device ID associated with a given device.

<a id="rst-return-value-12"></a>

#### RETURN VALUE

If negative, an error code; otherwise, the number of bytes of buffer that contain the device ID.  The format of the device ID is as follows:



```text
[length][ID]
```

The first two bytes indicate the inclusive length of the entire Device ID, and are in big-endian order.  The ID is a sequence of pairs of the form:



```text
key:value;
```

<a id="rst-notes-1"></a>

#### NOTES

Many devices have ill-formed IEEE 1284 Device IDs.

<a id="rst-see-also-15"></a>

#### SEE ALSO

parport_find_class, parport_find_device

<a id="rst-parport-device-coords-convert-device-number-to-device-coordinates"></a>

### parport_device_coords - convert device number to device coordinates

<a id="rst-synopsis-16"></a>

#### SYNOPSIS



```text
#include <linux/parport.h>

int parport_device_coords (int devnum, int *parport, int *mux,
                           int *daisy);
```

<a id="rst-description-17"></a>

#### DESCRIPTION

Convert between device number (zero-based) and device coordinates (port, multiplexor, daisy chain address).

<a id="rst-return-value-13"></a>

#### RETURN VALUE

Zero on success, in which case the coordinates are (`*parport`, `*mux`, `*daisy`).

<a id="rst-see-also-16"></a>

#### SEE ALSO

parport_open, parport_device_id

<a id="rst-parport-find-class-find-a-device-by-its-class"></a>

### parport_find_class - find a device by its class

<a id="rst-synopsis-17"></a>

#### SYNOPSIS



```text
#include <linux/parport.h>

typedef enum {
        PARPORT_CLASS_LEGACY = 0,       /* Non-IEEE1284 device */
        PARPORT_CLASS_PRINTER,
        PARPORT_CLASS_MODEM,
        PARPORT_CLASS_NET,
        PARPORT_CLASS_HDC,              /* Hard disk controller */
        PARPORT_CLASS_PCMCIA,
        PARPORT_CLASS_MEDIA,            /* Multimedia device */
        PARPORT_CLASS_FDC,              /* Floppy disk controller */
        PARPORT_CLASS_PORTS,
        PARPORT_CLASS_SCANNER,
        PARPORT_CLASS_DIGCAM,
        PARPORT_CLASS_OTHER,            /* Anything else */
        PARPORT_CLASS_UNSPEC,           /* No CLS field in ID */
        PARPORT_CLASS_SCSIADAPTER
} parport_device_class;

int parport_find_class (parport_device_class cls, int from);
```

<a id="rst-description-18"></a>

#### DESCRIPTION

Find a device by class.  The search starts from device number from+1.

<a id="rst-return-value-14"></a>

#### RETURN VALUE

The device number of the next device in that class, or -1 if no such device exists.

<a id="rst-notes-2"></a>

#### NOTES

Example usage:



```text
int devnum = -1;
while ((devnum = parport_find_class (PARPORT_CLASS_DIGCAM, devnum)) != -1) {
        struct pardevice *dev = parport_open (devnum, ...);
        ...
}
```

<a id="rst-see-also-17"></a>

#### SEE ALSO

parport_find_device, parport_open, parport_device_id

<a id="rst-parport-find-device-find-a-device-by-its-class"></a>

### parport_find_device - find a device by its class

<a id="rst-synopsis-18"></a>

#### SYNOPSIS



```text
#include <linux/parport.h>

int parport_find_device (const char *mfg, const char *mdl, int from);
```

<a id="rst-description-19"></a>

#### DESCRIPTION

Find a device by vendor and model.  The search starts from device number from+1.

<a id="rst-return-value-15"></a>

#### RETURN VALUE

The device number of the next device matching the specifications, or -1 if no such device exists.

<a id="rst-notes-3"></a>

#### NOTES

Example usage:



```text
int devnum = -1;
while ((devnum = parport_find_device ("IOMEGA", "ZIP+", devnum)) != -1) {
        struct pardevice *dev = parport_open (devnum, ...);
        ...
}
```

<a id="rst-see-also-18"></a>

#### SEE ALSO

parport_find_class, parport_open, parport_device_id

<a id="rst-parport-set-timeout-set-the-inactivity-timeout"></a>

### parport_set_timeout - set the inactivity timeout

<a id="rst-synopsis-19"></a>

#### SYNOPSIS



```text
#include <linux/parport.h>

long parport_set_timeout (struct pardevice *dev, long inactivity);
```

<a id="rst-description-20"></a>

#### DESCRIPTION

Set the inactivity timeout, in jiffies, for a registered device.  The previous timeout is returned.

<a id="rst-return-value-16"></a>

#### RETURN VALUE

The previous timeout, in jiffies.

<a id="rst-notes-4"></a>

#### NOTES

Some of the port-&gt;ops functions for a parport may take time, owing to delays at the peripheral.  After the peripheral has not responded for `inactivity` jiffies, a timeout will occur and the blocking function will return.

A timeout of 0 jiffies is a special case: the function must do as much as it can without blocking or leaving the hardware in an unknown state.  If port operations are performed from within an interrupt handler, for instance, a timeout of 0 jiffies should be used.

Once set for a registered device, the timeout will remain at the set value until set again.

<a id="rst-see-also-19"></a>

#### SEE ALSO

port-&gt;ops-&gt;xxx_read/write_yyy

<a id="rst-port-functions"></a>

## PORT FUNCTIONS

The functions in the port-&gt;ops structure (struct parport_operations) are provided by the low-level driver responsible for that port.

<a id="rst-port-ops-read-data-read-the-data-register"></a>

### port-&gt;ops-&gt;read_data - read the data register

<a id="rst-synopsis-20"></a>

#### SYNOPSIS



```text
#include <linux/parport.h>

struct parport_operations {
        ...
        unsigned char (*read_data) (struct parport *port);
        ...
};
```

<a id="rst-description-21"></a>

#### DESCRIPTION

If port-&gt;modes contains the PARPORT_MODE_TRISTATE flag and the PARPORT_CONTROL_DIRECTION bit in the control register is set, this returns the value on the data pins.  If port-&gt;modes contains the PARPORT_MODE_TRISTATE flag and the PARPORT_CONTROL_DIRECTION bit is not set, the return value \_may\_ be the last value written to the data register.  Otherwise the return value is undefined.

<a id="rst-see-also-20"></a>

#### SEE ALSO

write_data, read_status, write_control

<a id="rst-port-ops-write-data-write-the-data-register"></a>

### port-&gt;ops-&gt;write_data - write the data register

<a id="rst-synopsis-21"></a>

#### SYNOPSIS



```text
#include <linux/parport.h>

struct parport_operations {
        ...
        void (*write_data) (struct parport *port, unsigned char d);
        ...
};
```

<a id="rst-description-22"></a>

#### DESCRIPTION

Writes to the data register.  May have side-effects (a STROBE pulse, for instance).

<a id="rst-see-also-21"></a>

#### SEE ALSO

read_data, read_status, write_control

<a id="rst-port-ops-read-status-read-the-status-register"></a>

### port-&gt;ops-&gt;read_status - read the status register

<a id="rst-synopsis-22"></a>

#### SYNOPSIS



```text
#include <linux/parport.h>

struct parport_operations {
        ...
        unsigned char (*read_status) (struct parport *port);
        ...
};
```

<a id="rst-description-23"></a>

#### DESCRIPTION

Reads from the status register.  This is a bitmask:

- PARPORT_STATUS_ERROR (printer fault, "nFault")

- PARPORT_STATUS_SELECT (on-line, "Select")

- PARPORT_STATUS_PAPEROUT (no paper, "PError")

- PARPORT_STATUS_ACK (handshake, "nAck")

- PARPORT_STATUS_BUSY (busy, "Busy")

There may be other bits set.

<a id="rst-see-also-22"></a>

#### SEE ALSO

read_data, write_data, write_control

<a id="rst-port-ops-read-control-read-the-control-register"></a>

### port-&gt;ops-&gt;read_control - read the control register

<a id="rst-synopsis-23"></a>

#### SYNOPSIS



```text
#include <linux/parport.h>

struct parport_operations {
        ...
        unsigned char (*read_control) (struct parport *port);
        ...
};
```

<a id="rst-description-24"></a>

#### DESCRIPTION

Returns the last value written to the control register (either from write_control or frob_control).  No port access is performed.

<a id="rst-see-also-23"></a>

#### SEE ALSO

read_data, write_data, read_status, write_control

<a id="rst-port-ops-write-control-write-the-control-register"></a>

### port-&gt;ops-&gt;write_control - write the control register

<a id="rst-synopsis-24"></a>

#### SYNOPSIS



```text
#include <linux/parport.h>

struct parport_operations {
        ...
        void (*write_control) (struct parport *port, unsigned char s);
        ...
};
```

<a id="rst-description-25"></a>

#### DESCRIPTION

Writes to the control register. This is a bitmask:



```text
                          _______
- PARPORT_CONTROL_STROBE (nStrobe)
                          _______
- PARPORT_CONTROL_AUTOFD (nAutoFd)
                        _____
- PARPORT_CONTROL_INIT (nInit)
                          _________
- PARPORT_CONTROL_SELECT (nSelectIn)
```

<a id="rst-see-also-24"></a>

#### SEE ALSO

read_data, write_data, read_status, frob_control

<a id="rst-port-ops-frob-control-write-control-register-bits"></a>

### port-&gt;ops-&gt;frob_control - write control register bits

<a id="rst-synopsis-25"></a>

#### SYNOPSIS



```text
#include <linux/parport.h>

struct parport_operations {
        ...
        unsigned char (*frob_control) (struct parport *port,
                                unsigned char mask,
                                unsigned char val);
        ...
};
```

<a id="rst-description-26"></a>

#### DESCRIPTION

This is equivalent to reading from the control register, masking out the bits in mask, exclusive-or'ing with the bits in val, and writing the result to the control register.

As some ports don't allow reads from the control port, a software copy of its contents is maintained, so frob_control is in fact only one port access.

<a id="rst-see-also-25"></a>

#### SEE ALSO

read_data, write_data, read_status, write_control

<a id="rst-port-ops-enable-irq-enable-interrupt-generation"></a>

### port-&gt;ops-&gt;enable_irq - enable interrupt generation

<a id="rst-synopsis-26"></a>

#### SYNOPSIS



```text
#include <linux/parport.h>

struct parport_operations {
        ...
        void (*enable_irq) (struct parport *port);
        ...
};
```

<a id="rst-description-27"></a>

#### DESCRIPTION

The parallel port hardware is instructed to generate interrupts at appropriate moments, although those moments are architecture-specific.  For the PC architecture, interrupts are commonly generated on the rising edge of nAck.

<a id="rst-see-also-26"></a>

#### SEE ALSO

disable_irq

<a id="rst-port-ops-disable-irq-disable-interrupt-generation"></a>

### port-&gt;ops-&gt;disable_irq - disable interrupt generation

<a id="rst-synopsis-27"></a>

#### SYNOPSIS



```text
#include <linux/parport.h>

struct parport_operations {
        ...
        void (*disable_irq) (struct parport *port);
        ...
};
```

<a id="rst-description-28"></a>

#### DESCRIPTION

The parallel port hardware is instructed not to generate interrupts. The interrupt itself is not masked.

<a id="rst-see-also-27"></a>

#### SEE ALSO

enable_irq

<a id="rst-port-ops-data-forward-enable-data-drivers"></a>

### port-&gt;ops-&gt;data_forward - enable data drivers

<a id="rst-synopsis-28"></a>

#### SYNOPSIS



```text
#include <linux/parport.h>

struct parport_operations {
        ...
        void (*data_forward) (struct parport *port);
        ...
};
```

<a id="rst-description-29"></a>

#### DESCRIPTION

Enables the data line drivers, for 8-bit host-to-peripheral communications.

<a id="rst-see-also-28"></a>

#### SEE ALSO

data_reverse

<a id="rst-port-ops-data-reverse-tristate-the-buffer"></a>

### port-&gt;ops-&gt;data_reverse - tristate the buffer

<a id="rst-synopsis-29"></a>

#### SYNOPSIS



```text
#include <linux/parport.h>

struct parport_operations {
        ...
        void (*data_reverse) (struct parport *port);
        ...
};
```

<a id="rst-description-30"></a>

#### DESCRIPTION

Places the data bus in a high impedance state, if port-&gt;modes has the PARPORT_MODE_TRISTATE bit set.

<a id="rst-see-also-29"></a>

#### SEE ALSO

data_forward

<a id="rst-port-ops-epp-write-data-write-epp-data"></a>

### port-&gt;ops-&gt;epp_write_data - write EPP data

<a id="rst-synopsis-30"></a>

#### SYNOPSIS



```text
#include <linux/parport.h>

struct parport_operations {
        ...
        size_t (*epp_write_data) (struct parport *port, const void *buf,
                                size_t len, int flags);
        ...
};
```

<a id="rst-description-31"></a>

#### DESCRIPTION

Writes data in EPP mode, and returns the number of bytes written.

The `flags` parameter may be one or more of the following, bitwise-or'ed together:


<table>
<tbody>
<tr>
<td>


PARPORT_EPP_FAST

</td>
<td>


Use fast transfers. Some chips provide 16-bit and 32-bit registers.  However, if a transfer times out, the return value may be unreliable.

</td>
</tr>
</tbody>
</table>

<a id="rst-see-also-30"></a>

#### SEE ALSO

epp_read_data, epp_write_addr, epp_read_addr

<a id="rst-port-ops-epp-read-data-read-epp-data"></a>

### port-&gt;ops-&gt;epp_read_data - read EPP data

<a id="rst-synopsis-31"></a>

#### SYNOPSIS



```text
#include <linux/parport.h>

struct parport_operations {
        ...
        size_t (*epp_read_data) (struct parport *port, void *buf,
                                size_t len, int flags);
        ...
};
```

<a id="rst-description-32"></a>

#### DESCRIPTION

Reads data in EPP mode, and returns the number of bytes read.

The `flags` parameter may be one or more of the following, bitwise-or'ed together:


<table>
<tbody>
<tr>
<td>


PARPORT_EPP_FAST

</td>
<td>


Use fast transfers. Some chips provide 16-bit and 32-bit registers.  However, if a transfer times out, the return value may be unreliable.

</td>
</tr>
</tbody>
</table>

<a id="rst-see-also-31"></a>

#### SEE ALSO

epp_write_data, epp_write_addr, epp_read_addr

<a id="rst-port-ops-epp-write-addr-write-epp-address"></a>

### port-&gt;ops-&gt;epp_write_addr - write EPP address

<a id="rst-synopsis-32"></a>

#### SYNOPSIS



```text
#include <linux/parport.h>

struct parport_operations {
        ...
        size_t (*epp_write_addr) (struct parport *port,
                                const void *buf, size_t len, int flags);
        ...
};
```

<a id="rst-description-33"></a>

#### DESCRIPTION

Writes EPP addresses (8 bits each), and returns the number written.

The `flags` parameter may be one or more of the following, bitwise-or'ed together:


<table>
<tbody>
<tr>
<td>


PARPORT_EPP_FAST

</td>
<td>


Use fast transfers. Some chips provide 16-bit and 32-bit registers.  However, if a transfer times out, the return value may be unreliable.

</td>
</tr>
</tbody>
</table>

(Does PARPORT_EPP_FAST make sense for this function?)

<a id="rst-see-also-32"></a>

#### SEE ALSO

epp_write_data, epp_read_data, epp_read_addr

<a id="rst-port-ops-epp-read-addr-read-epp-address"></a>

### port-&gt;ops-&gt;epp_read_addr - read EPP address

<a id="rst-synopsis-33"></a>

#### SYNOPSIS



```text
#include <linux/parport.h>

struct parport_operations {
        ...
        size_t (*epp_read_addr) (struct parport *port, void *buf,
                                size_t len, int flags);
        ...
};
```

<a id="rst-description-34"></a>

#### DESCRIPTION

Reads EPP addresses (8 bits each), and returns the number read.

The `flags` parameter may be one or more of the following, bitwise-or'ed together:


<table>
<tbody>
<tr>
<td>


PARPORT_EPP_FAST

</td>
<td>


Use fast transfers. Some chips provide 16-bit and 32-bit registers.  However, if a transfer times out, the return value may be unreliable.

</td>
</tr>
</tbody>
</table>

(Does PARPORT_EPP_FAST make sense for this function?)

<a id="rst-see-also-33"></a>

#### SEE ALSO

epp_write_data, epp_read_data, epp_write_addr

<a id="rst-port-ops-ecp-write-data-write-a-block-of-ecp-data"></a>

### port-&gt;ops-&gt;ecp_write_data - write a block of ECP data

<a id="rst-synopsis-34"></a>

#### SYNOPSIS



```text
#include <linux/parport.h>

struct parport_operations {
        ...
        size_t (*ecp_write_data) (struct parport *port,
                                const void *buf, size_t len, int flags);
        ...
};
```

<a id="rst-description-35"></a>

#### DESCRIPTION

Writes a block of ECP data.  The `flags` parameter is ignored.

<a id="rst-return-value-17"></a>

#### RETURN VALUE

The number of bytes written.

<a id="rst-see-also-34"></a>

#### SEE ALSO

ecp_read_data, ecp_write_addr

<a id="rst-port-ops-ecp-read-data-read-a-block-of-ecp-data"></a>

### port-&gt;ops-&gt;ecp_read_data - read a block of ECP data

<a id="rst-synopsis-35"></a>

#### SYNOPSIS



```text
#include <linux/parport.h>

struct parport_operations {
        ...
        size_t (*ecp_read_data) (struct parport *port,
                                void *buf, size_t len, int flags);
        ...
};
```

<a id="rst-description-36"></a>

#### DESCRIPTION

Reads a block of ECP data.  The `flags` parameter is ignored.

<a id="rst-return-value-18"></a>

#### RETURN VALUE

The number of bytes read.  NB. There may be more unread data in a FIFO.  Is there a way of stunning the FIFO to prevent this?

<a id="rst-see-also-35"></a>

#### SEE ALSO

ecp_write_block, ecp_write_addr

<a id="rst-port-ops-ecp-write-addr-write-a-block-of-ecp-addresses"></a>

### port-&gt;ops-&gt;ecp_write_addr - write a block of ECP addresses

<a id="rst-synopsis-36"></a>

#### SYNOPSIS



```text
#include <linux/parport.h>

struct parport_operations {
        ...
        size_t (*ecp_write_addr) (struct parport *port,
                                const void *buf, size_t len, int flags);
        ...
};
```

<a id="rst-description-37"></a>

#### DESCRIPTION

Writes a block of ECP addresses.  The `flags` parameter is ignored.

<a id="rst-return-value-19"></a>

#### RETURN VALUE

The number of bytes written.

<a id="rst-notes-5"></a>

#### NOTES

This may use a FIFO, and if so shall not return until the FIFO is empty.

<a id="rst-see-also-36"></a>

#### SEE ALSO

ecp_read_data, ecp_write_data

<a id="rst-port-ops-nibble-read-data-read-a-block-of-data-in-nibble-mode"></a>

### port-&gt;ops-&gt;nibble_read_data - read a block of data in nibble mode

<a id="rst-synopsis-37"></a>

#### SYNOPSIS



```text
#include <linux/parport.h>

struct parport_operations {
        ...
        size_t (*nibble_read_data) (struct parport *port,
                                void *buf, size_t len, int flags);
        ...
};
```

<a id="rst-description-38"></a>

#### DESCRIPTION

Reads a block of data in nibble mode.  The `flags` parameter is ignored.

<a id="rst-return-value-20"></a>

#### RETURN VALUE

The number of whole bytes read.

<a id="rst-see-also-37"></a>

#### SEE ALSO

byte_read_data, compat_write_data

<a id="rst-port-ops-byte-read-data-read-a-block-of-data-in-byte-mode"></a>

### port-&gt;ops-&gt;byte_read_data - read a block of data in byte mode

<a id="rst-synopsis-38"></a>

#### SYNOPSIS



```text
#include <linux/parport.h>

struct parport_operations {
        ...
        size_t (*byte_read_data) (struct parport *port,
                                void *buf, size_t len, int flags);
        ...
};
```

<a id="rst-description-39"></a>

#### DESCRIPTION

Reads a block of data in byte mode.  The `flags` parameter is ignored.

<a id="rst-return-value-21"></a>

#### RETURN VALUE

The number of bytes read.

<a id="rst-see-also-38"></a>

#### SEE ALSO

nibble_read_data, compat_write_data

<a id="rst-port-ops-compat-write-data-write-a-block-of-data-in-compatibility-mode"></a>

### port-&gt;ops-&gt;compat_write_data - write a block of data in compatibility mode

<a id="rst-synopsis-39"></a>

#### SYNOPSIS



```text
#include <linux/parport.h>

struct parport_operations {
        ...
        size_t (*compat_write_data) (struct parport *port,
                                const void *buf, size_t len, int flags);
        ...
};
```

<a id="rst-description-40"></a>

#### DESCRIPTION

Writes a block of data in compatibility mode.  The `flags` parameter is ignored.

<a id="rst-return-value-22"></a>

#### RETURN VALUE

The number of bytes written.

<a id="rst-see-also-39"></a>

#### SEE ALSO

nibble_read_data, byte_read_data
