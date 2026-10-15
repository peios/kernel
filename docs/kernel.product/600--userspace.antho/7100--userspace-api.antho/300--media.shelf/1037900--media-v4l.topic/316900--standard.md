---
title: "Video Standards"
type: reference
description: "Video devices typically support one or more different video standards or variations of standards. Each video input and output may support another set of standards. This set is reported by the std field of struct v4l2_input and struct…"
---

<a id="rst-video-standards"></a>
<a id="rst-standard"></a>

<!-- SPDX-License-Identifier: GFDL-1.1-no-invariants-or-later -->

<!-- c:namespace: V4L -->

Video devices typically support one or more different video standards or variations of standards. Each video input and output may support another set of standards. This set is reported by the `std` field of struct `v4l2_input` and struct `v4l2_output` returned by the [ioctl VIDIOC_ENUMINPUT](<~kernel/userspace/userspace-api/media-v4l/vidioc-enuminput#rst-vidioc-enuminput>) and [ioctl VIDIOC_ENUMOUTPUT](<~kernel/userspace/userspace-api/media-v4l/vidioc-enumoutput#rst-vidioc-enumoutput>) ioctls, respectively.

V4L2 defines one bit for each analog video standard currently in use worldwide, and sets aside bits for driver defined standards, e. g. hybrid standards to watch NTSC video tapes on PAL TVs and vice versa. Applications can use the predefined bits to select a particular standard, although presenting the user a menu of supported standards is preferred. To enumerate and query the attributes of the supported standards applications use the [vidioc_enumstd](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/vidioc-enumstd.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>) ioctl.

Many of the defined standards are actually just variations of a few major standards. The hardware may in fact not distinguish between them, or do so internal and switch automatically. Therefore enumerated standards also contain sets of one or more standard bits.

Assume a hypothetic tuner capable of demodulating B/PAL, G/PAL and I/PAL signals. The first enumerated standard is a set of B and G/PAL, switched automatically depending on the selected radio frequency in UHF or VHF band. Enumeration gives a "PAL-B/G" or "PAL-I" choice. Similar a Composite input may collapse standards, enumerating "PAL-B/G/H/I", "NTSC-M" and "SECAM-D/K". <a id="rst-footnote-reference-1"></a>[1](#rst-f1)

To query and select the standard used by the current video input or output applications call the [VIDIOC_G_STD](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-std#rst-vidioc-g-std>) and [VIDIOC_S_STD](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-std#rst-vidioc-g-std>) ioctl, respectively. The *received* standard can be sensed with the [ioctl VIDIOC_QUERYSTD, VIDIOC_SUBDEV_QUERYSTD](<~kernel/userspace/userspace-api/media-v4l/vidioc-querystd#rst-vidioc-querystd>) ioctl.

> [!NOTE]
>
> The parameter of all these ioctls is a pointer to a [v4l2_std_id](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/vidioc-enumstd.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>) type (a standard set), *not* an index into the standard enumeration. Drivers must implement all video standard ioctls when the device has one or more video inputs or outputs.

Special rules apply to devices such as USB cameras where the notion of video standards makes little sense. More generally for any capture or output device which is:

- incapable of capturing fields or frames at the nominal rate of the video standard, or

- that does not support the video standard formats at all.

Here the driver shall set the `std` field of struct `v4l2_input` and struct `v4l2_output` to zero and the [VIDIOC_G_STD](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-std#rst-vidioc-g-std>), [VIDIOC_S_STD](<~kernel/userspace/userspace-api/media-v4l/vidioc-g-std#rst-vidioc-g-std>), [ioctl VIDIOC_QUERYSTD, VIDIOC_SUBDEV_QUERYSTD](<~kernel/userspace/userspace-api/media-v4l/vidioc-querystd#rst-vidioc-querystd>) and [vidioc_enumstd](<https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/userspace-api/media/v4l/vidioc-enumstd.rst?id=9021cc14f7d98b4a1d2c932f52c5343d4d0f6b92>) ioctls shall return the `ENOTTY` error code or the `EINVAL` error code.

Applications can make use of the [input-capabilities](<~kernel/userspace/userspace-api/media-v4l/vidioc-enuminput#rst-input-capabilities>) and [output-capabilities](<~kernel/userspace/userspace-api/media-v4l/vidioc-enumoutput#rst-output-capabilities>) flags to determine whether the video standard ioctls can be used with the given input or output.

<a id="rst-example-information-about-the-current-video-standard"></a>

## Example: Information about the current video standard



```c
v4l2_std_id std_id;
struct v4l2_standard standard;

if (-1 == ioctl(fd, VIDIOC_G_STD, &std_id)) {
    /* Note when VIDIOC_ENUMSTD always returns ENOTTY this
       is no video device or it falls under the USB exception,
       and VIDIOC_G_STD returning ENOTTY is no error. */

    perror("VIDIOC_G_STD");
    exit(EXIT_FAILURE);
}

memset(&standard, 0, sizeof(standard));
standard.index = 0;

while (0 == ioctl(fd, VIDIOC_ENUMSTD, &standard)) {
    if (standard.id & std_id) {
           printf("Current video standard: %s\\n", standard.name);
           exit(EXIT_SUCCESS);
    }

    standard.index++;
}

/* EINVAL indicates the end of the enumeration, which cannot be
   empty unless this device falls under the USB exception. */

if (errno == EINVAL || standard.index == 0) {
    perror("VIDIOC_ENUMSTD");
    exit(EXIT_FAILURE);
}
```

<a id="rst-example-listing-the-video-standards-supported-by-the-current-input"></a>

## Example: Listing the video standards supported by the current input



```c
struct v4l2_input input;
struct v4l2_standard standard;

memset(&input, 0, sizeof(input));

if (-1 == ioctl(fd, VIDIOC_G_INPUT, &input.index)) {
    perror("VIDIOC_G_INPUT");
    exit(EXIT_FAILURE);
}

if (-1 == ioctl(fd, VIDIOC_ENUMINPUT, &input)) {
    perror("VIDIOC_ENUM_INPUT");
    exit(EXIT_FAILURE);
}

printf("Current input %s supports:\\n", input.name);

memset(&standard, 0, sizeof(standard));
standard.index = 0;

while (0 == ioctl(fd, VIDIOC_ENUMSTD, &standard)) {
    if (standard.id & input.std)
        printf("%s\\n", standard.name);

    standard.index++;
}

/* EINVAL indicates the end of the enumeration, which cannot be
   empty unless this device falls under the USB exception. */

if (errno != EINVAL || standard.index == 0) {
    perror("VIDIOC_ENUMSTD");
    exit(EXIT_FAILURE);
}
```

<a id="rst-example-selecting-a-new-video-standard"></a>

## Example: Selecting a new video standard



```c
struct v4l2_input input;
v4l2_std_id std_id;

memset(&input, 0, sizeof(input));

if (-1 == ioctl(fd, VIDIOC_G_INPUT, &input.index)) {
    perror("VIDIOC_G_INPUT");
    exit(EXIT_FAILURE);
}

if (-1 == ioctl(fd, VIDIOC_ENUMINPUT, &input)) {
    perror("VIDIOC_ENUM_INPUT");
    exit(EXIT_FAILURE);
}

if (0 == (input.std & V4L2_STD_PAL_BG)) {
    fprintf(stderr, "Oops. B/G PAL is not supported.\\n");
    exit(EXIT_FAILURE);
}

/* Note this is also supposed to work when only B
   or G/PAL is supported. */

std_id = V4L2_STD_PAL_BG;

if (-1 == ioctl(fd, VIDIOC_S_STD, &std_id)) {
    perror("VIDIOC_S_STD");
    exit(EXIT_FAILURE);
}
```

<a id="rst-f1"></a>



**[1]** Some users are already confused by technical terms PAL, NTSC and SECAM. There is no point asking them to distinguish between B, G, D, or K when the software or hardware can do that automatically.
