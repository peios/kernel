---
title: "HW consumer"
type: reference
description: "An IIO device can be directly connected to another device in hardware. In this case the buffers between IIO provider and IIO consumer are handled by hardware. The Industrial I/O HW consumer offers a way to bond these IIO devices without…"
---

<a id="rst-hw-consumer"></a>

An IIO device can be directly connected to another device in hardware. In this case the buffers between IIO provider and IIO consumer are handled by hardware. The Industrial I/O HW consumer offers a way to bond these IIO devices without software buffer for data. The implementation can be found under `drivers/iio/buffer/hw-consumer.c`

- struct iio_hw_consumer — Hardware consumer structure

- `iio_hw_consumer_alloc()` — Allocate IIO hardware consumer

- `iio_hw_consumer_free()` — Free IIO hardware consumer

- `iio_hw_consumer_enable()` — Enable IIO hardware consumer

- `iio_hw_consumer_disable()` — Disable IIO hardware consumer

<a id="rst-hw-consumer-setup"></a>

## HW consumer setup

As standard IIO device the implementation is based on IIO provider/consumer. A typical IIO HW consumer setup looks like this:



```text
static struct iio_hw_consumer *hwc;

static const struct iio_info adc_info = {
        .read_raw = adc_read_raw,
};

static int adc_read_raw(struct iio_dev *indio_dev,
                        struct iio_chan_spec const *chan, int *val,
                        int *val2, long mask)
{
        ret = iio_hw_consumer_enable(hwc);

        /* Acquire data */

        ret = iio_hw_consumer_disable(hwc);
}

static int adc_probe(struct platform_device *pdev)
{
        hwc = devm_iio_hw_consumer_alloc(&iio->dev);
}
```

<a id="rst-more-details"></a>

## More details

```{kernel-doc} drivers/iio/buffer/industrialio-hw-consumer.c
:export:
```
