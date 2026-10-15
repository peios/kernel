---
title: "KUnit - Linux Kernel Unit Testing"
type: reference
description: "This section details the kernel unit testing framework."
---

<a id="rst-kunit-linux-kernel-unit-testing"></a>

<!-- SPDX-License-Identifier: GPL-2.0 -->

**Contents:**

- [Getting Started](<~kernel/development/dev-tools/kunit/start>)
- [KUnit Architecture](<~kernel/development/dev-tools/kunit/architecture>)
- [Running tests with kunit_tool](<~kernel/development/dev-tools/kunit/run-wrapper>)
- [Run Tests without kunit_tool](<~kernel/development/dev-tools/kunit/run-manual>)
- [Writing Tests](<~kernel/development/dev-tools/kunit/usage>)
- [API Reference](<~kernel/development/dev-tools/kunit-api/index>)
- [Test Style and Nomenclature](<~kernel/development/dev-tools/kunit/style>)
- [Frequently Asked Questions](<~kernel/development/dev-tools/kunit/faq>)
- [Tips For Running KUnit Tests](<~kernel/development/dev-tools/kunit/running-tips>)

This section details the kernel unit testing framework.

<a id="rst-introduction"></a>

## Introduction

KUnit (Kernel unit testing framework) provides a common framework for unit tests within the Linux kernel. Using KUnit, you can define groups of test cases called test suites. The tests either run on kernel boot if built-in, or load as a module. KUnit automatically flags and reports failed test cases in the kernel log. The test results appear in [KTAP (Kernel - Test Anything Protocol) format](<~kernel/development/dev-tools/ktap>). It is inspired by JUnit, Python’s unittest.mock, and GoogleTest/GoogleMock (C++ unit testing framework).

KUnit tests are part of the kernel, written in the C (programming) language, and test parts of the Kernel implementation (example: a C language function). Excluding build time, from invocation to completion, KUnit can run around 100 tests in less than 10 seconds. KUnit can test any kernel component, for example: file system, system calls, memory management, device drivers and so on.

KUnit follows the white-box testing approach. The test has access to internal system functionality. KUnit runs in kernel space and is not restricted to things exposed to user-space.

In addition, KUnit has kunit_tool, a script (`tools/testing/kunit/kunit.py`) that configures the Linux kernel, runs KUnit tests under QEMU or UML ([User Mode Linux](<~kernel/internals/virt/uml/user-mode-linux-howto-v2>)), parses the test results and displays them in a user friendly manner.

<a id="rst-features"></a>

### Features

- Provides a framework for writing unit tests.

- Runs tests on any kernel architecture.

- Runs a test in milliseconds.

<a id="rst-prerequisites"></a>

### Prerequisites

- Any Linux kernel compatible hardware.

- For Kernel under test, Linux kernel version 5.5 or greater.

<a id="rst-unit-testing"></a>

## Unit Testing

A unit test tests a single unit of code in isolation. A unit test is the finest granularity of testing and allows all possible code paths to be tested in the code under test. This is possible if the code under test is small and does not have any external dependencies outside of the test's control like hardware.

<a id="rst-write-unit-tests"></a>

### Write Unit Tests

To write good unit tests, there is a simple but powerful pattern: Arrange-Act-Assert. This is a great way to structure test cases and defines an order of operations.

- Arrange inputs and targets: At the start of the test, arrange the data that allows a function to work. Example: initialize a statement or object.

- Act on the target behavior: Call your function/code under test.

- Assert expected outcome: Verify that the result (or resulting state) is as expected.

<a id="rst-unit-testing-advantages"></a>

### Unit Testing Advantages

- Increases testing speed and development in the long run.

- Detects bugs at initial stage and therefore decreases bug fix cost compared to acceptance testing.

- Improves code quality.

- Encourages writing testable code.

Read also [What is the difference between a unit test and other kinds of tests?](<~kernel/development/dev-tools/kunit/faq#rst-kinds-of-tests>).

<a id="rst-how-do-i-use-it"></a>

## How do I use it?

You can find a step-by-step guide to writing and running KUnit tests in [Documentation/dev-tools/kunit/start.rst](~kernel/development/dev-tools/kunit/start)

Alternatively, feel free to look through the rest of the KUnit documentation, or to experiment with tools/testing/kunit/kunit.py and the example test under lib/kunit/kunit-example-test.c

Happy testing\!
