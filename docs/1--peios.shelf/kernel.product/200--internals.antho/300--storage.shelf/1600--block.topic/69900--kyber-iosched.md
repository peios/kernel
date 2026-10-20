---
title: "Kyber I/O scheduler tunables"
type: reference
description: "The only two tunables for the Kyber scheduler are the target latencies for reads and synchronous writes. Kyber will throttle requests in order to meet these target latencies."
---

<a id="rst-kyber-i-o-scheduler-tunables"></a>

The only two tunables for the Kyber scheduler are the target latencies for reads and synchronous writes. Kyber will throttle requests in order to meet these target latencies.

<a id="rst-read-lat-nsec"></a>

## read_lat_nsec

Target latency for reads (in nanoseconds).

<a id="rst-write-lat-nsec"></a>

## write_lat_nsec

Target latency for synchronous writes (in nanoseconds).
