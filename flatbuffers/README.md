# FlatBuffers and WAMP

## WAMP payload transparency mode

### Motivation

WAMP supports both positional and keyword based request arguments and returns.

For example, the WAMP `CALL` message allows for the following three alternative forms:

1. `[CALL, Request|id, Options|dict, Procedure|uri]`
2. `[CALL, Request|id, Options|dict, Procedure|uri, Arguments|list]`
3. `[CALL, Request|id, Options|dict, Procedure|uri, Arguments|list, ArgumentsKw|dict]`

The actual application payload hence can take **three variants of app payload (XX)**:

1. `-`
2. `Arguments|list`
3. `Arguments|list, ArgumentsKw|dict`

This pattern repeats across **all** WAMP messages that can carry application payload, namely:

* `PUBLISH`
* `EVENT`
* `CALL`
* `INVOCATION`
* `YIELD`
* `RESULT`
* `ERROR`

> Note: should the proposed new WAMP messages `EVENT_RECEIVED` and `SUBSCRIBER_RECEIVED` be introduced,
these also carry application payload, and would follow the same approach.

The approach taken (**XX**) allows for a number of useful features:

1. flexible support of popular dynamically typed serializers, namely: JSON, MsgPack, CBOR and UBJSON
2. allow arbitrary adhoc extensibility (as the router basically does not care about new app payloads)
3. transparantly translate the *application payload* between serialization formats used by different clients connected at the same time.
4. support optional router side application payload validation: both static, and dynamic (calling into user supplied payload validators)

However, a number of downsides have become apparent as well:

1. resource consumption: serialization/deserialization can eat significant chunks of CPU, and produce GC pressure
2. legacy (MQTT) and proprietory payloads that should simply be transported "as is" (passthrough, without ever touching)
3. as apps and systems get larger and more complex, the dynamic typing flexibility turns into a major problem: **the internal and external interfaces and APIs in a microservices based application must be relied upon and their evolution actively managed**

The latter does not mean an "either or" question. You can have important base APIs and external interfaces defined rigorously, using static, strict typing discipline, while at the same time have other parts of your system evolve more freely, basically allowing weakly and dynamically typed data exchange - for limited areas.

---


### Payload Transparency Mode

**Payload Transparancy Mode** adds a 4th application payload variant to above **XX**

4. `[CALL, Request|id, Options|dict, Procedure|uri, Payload|binary]`

where the actual application payload takes this form:

4. `Payload|binary`


## FlatBuffers

FlatBuffers is a zero-copy serialization format open-sourced by Google in 2014 under the Apache 2 license.

Supported operating systems include:

* Android
* Linux
* MacOS X
* Windows

Supported programming languages include:

* C++
* C#
* C
* Go
* Java
* JavaScript
* PHP
* Python

---

## Building

1. Get [cmake](https://cmake.org/)
2. Follow [Building with CMake](https://github.com/google/flatbuffers/blob/master/docs/source/Building.md#building-with-cmake)

Essentially:

```console
git clone https://github.com/google/flatbuffers.git
cd flatbuffers
cmake -G "Unix Makefiles"
make -j4
./flatc --version
```

---

### flatc patches

The following patches are required currently for flatc: [this PR](https://github.com/google/flatbuffers/pull/4711) adds [pieces missing for reflection](https://github.com/google/flatbuffers/pull/4711/files#diff-db35d829e5e236af29f9a061c8352dcb) in the flatc compiler.

---

## Notes

* FlatBuffers [currently lacks](https://github.com/google/flatbuffers/issues/4237) syntax highlighting on GitHub.

---

## References

* [FlatBuffers Homepage](https://google.github.io/flatbuffers/)
* [FlatBuffers Source](https://github.com/google/flatbuffers)
* [flatcc - a FlatBuffers Compiler and Library in C for C](https://github.com/dvidelabs/flatcc)


---
