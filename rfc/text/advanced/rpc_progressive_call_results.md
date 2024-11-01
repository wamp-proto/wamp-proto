## Progressive Call Results {#rpc-progressive-call-results}

A procedure implemented by a *Callee* and registered at a *Dealer* may produce progressive results. Progressive results can e.g. be used to return partial results for long-running operations, or to chunk the transmission of larger results sets.

**Feature Announcement**

Support for this advanced feature MUST be announced by *Callers* (`role := "caller"`), *Callees* (`role := "callee"`) and *Dealers* (`role := "dealer"`) via

{align="left"}
        HELLO.Details.roles.<role>.features.
             progressive_call_results|bool := true

Additionally, *Callees* and *Dealers* MUST support Call Canceling, which is required for canceling progressive results if the original *Caller* leaves the realm. If a *Callee* supports Progressive Call Results, but not Call Canceling, then the *Dealer* disregards the *Callees* Progressive Call Results feature.

**Message Flow**

The message flow for progressive results involves:

{align="left"}
     ,------.           ,------.          ,------.
     |Caller|           |Dealer|          |Callee|
     `--+---'           `--+---'          `--+---'
        |       CALL       |                 |
        | ----------------->                 |
        |                  |                 |
        |                  |    INVOCATION   |
        |                  | ---------------->
        |                  |                 |
        |                  | YIELD (progress)|
        |                  | <----------------
        |                  |                 |
        | RESULT (progress)|                 |
        | <-----------------                 |
        |                  |                 |
        |                  | YIELD (progress)|
        |                  | <----------------
        |                  |                 |
        | RESULT (progress)|                 |
        | <-----------------                 |
        |                  |                 |
        |                  |                 |
        |       ...        |       ...       |
        |                  |                 |
        |                  |  YIELD or ERROR |
        |                  | <----------------
        |                  |                 |
        |  RESULT or ERROR |                 |
        | <-----------------                 |
     ,--+---.           ,--+---.          ,--+---.
     |Caller|           |Dealer|          |Callee|
     `------'           `------'          `------'


A *Caller* indicates its willingness to receive progressive results by setting

{align="left"}
        CALL.Options.receive_progress|bool := true

*Example.* Caller-to-Dealer `CALL`

{align="left"}
```json
    [
        48,
        77133,
        {
            "receive_progress": true
        },
        "com.myapp.compute_revenue",
        [2010, 2011, 2012]
    ]
```

If the *Callee* supports Progressive Call Results, the *Dealer* will forward the *Caller's* willingness to receive progressive results by setting

{align="left"}
        INVOCATION.Details.receive_progress|bool := true


*Example.* Dealer-to-Callee `INVOCATION`

{align="left"}
```json
    [
        68,
        87683,
        324,
        {
            "receive_progress": true
        },
        [2010, 2011, 2012]
    ]
```

An endpoint implementing the procedure produces progressive results by sending `YIELD` messages to the *Dealer* with

{align="left"}
        YIELD.Options.progress|bool := true


*Example.* Callee-to-Dealer progressive `YIELDs`

{align="left"}
```json
    [
        70,
        87683,
        {
            "progress": true
        },
        ["Y2010", 120]
    ]
```

{align="left"}
```json
    [
        70,
        87683,
        {
            "progress": true
        },
        ["Y2011", 205]
    ]
```

Upon receiving an `YIELD` message from a *Callee* with `YIELD.Options.progress == true` (for a call that is still ongoing), the *Dealer* will **immediately** send a `RESULT` message to the original *Caller* with

{align="left"}
        RESULT.Details.progress|bool := true

*Example.* Dealer-to-Caller progressive `RESULTs`

{align="left"}
```json
    [
        50,
        77133,
        {
            "progress": true
        },
        ["Y2010", 120]
    ]
```

{align="left"}
```json
    [
        50,
        77133,
        {
            "progress": true
        },
        ["Y2011", 205]
    ]
```

and so on...

An invocation MUST *always* end in either a *normal* `RESULT` or `ERROR` message being sent by the *Callee* and received by the *Dealer*.

*Example.* Callee-to-Dealer final `YIELD`

{align="left"}
```json
    [
        70,
        87683,
        {},
        ["Total", 490]
    ]
```

*Example.* Callee-to-Dealer final `ERROR`

{align="left"}
```json
    [
        8,
        68,
        87683,
        {},
        "com.myapp.invalid_revenue_year",
        [1830]
    ]
```

A call MUST *always* end in either a *normal* `RESULT` or `ERROR` message being sent by the *Dealer* and received by the *Caller*.

*Example.* Dealer-to-Caller final `RESULT`

{align="left"}
```json
    [
        50,
        77133,
        {},
        ["Total", 490]
    ]
```

*Example.* Dealer-to-Caller final `ERROR`

{align="left"}
```json
    [
        8,
        68,
        77133,
        {},
        "com.myapp.invalid_revenue_year",
        [1830]
    ]
```

In other words: `YIELD` with `YIELD.Options.progress == true` and `RESULT` with `RESULT.Details.progress == true` messages may only be sent *during* a call or invocation is still ongoing.

The final `YIELD` and final `RESULT` may also be empty, e.g. when all actual results have already been transmitted in progressive result messages.

*Example.* Callee-to-Dealer `YIELDs`

{align="left"}
```
    [70, 87683, {"progress": true}, ["Y2010", 120]]
    [70, 87683, {"progress": true}, ["Y2011", 205]]
     ...
    [70, 87683, {"progress": true}, ["Total", 490]]
    [70, 87683, {}]
```

*Example.* Dealer-to-Caller `RESULTs`

{align="left"}
```
    [50, 77133, {"progress": true}, ["Y2010", 120]]
    [50, 77133, {"progress": true}, ["Y2011", 205]]
     ...
    [50, 77133, {"progress": true}, ["Total", 490]]
    [50, 77133, {}]
```

The progressive `YIELD` and progressive `RESULT` may also be empty, e.g. when those messages are only used to signal that the procedure is still running and working, and the actual result is completely delivered in the final `YIELD` and `RESULT`:

*Example.* Callee-to-Dealer `YIELDs`

{align="left"}
```
    [70, 87683, {"progress": true}]
    [70, 87683, {"progress": true}]
    ...
    [70, 87683, {}, [["Y2010", 120], ["Y2011", 205], ...,
        ["Total", 490]]]
```

*Example.* Dealer-to-Caller `RESULTs`

{align="left"}
```
    [50, 77133, {"progress": true}]
    [50, 77133, {"progress": true}]
    ...
    [50, 77133, {}, [["Y2010", 120], ["Y2011", 205], ...,
        ["Total", 490]]]
```

> Note that intermediate, progressive results and/or the final result MAY have different structure. The WAMP peer implementation is responsible for mapping everything into a form suitable for consumption in the host language.

*Example.* Callee-to-Dealer `YIELDs`

{align="left"}
```
    [70, 87683, {"progress": true}, ["partial 1", 10]]
    [70, 87683, {"progress": true}, [], {"foo": 10,
        "bar": "partial 1"}]
     ...
    [70, 87683, {}, [1, 2, 3], {"moo": "hello"}]
```

*Example.* Dealer-to-Caller `RESULTs`

{align="left"}
```
    [50, 77133, {"progress": true}, ["partial 1", 10]]
    [50, 77133, {"progress": true}, [], {"foo": 10,
        "bar": "partial 1"}]
     ...
    [50, 77133, {}, [1, 2, 3], {"moo": "hello"}]
```

Even if a *Caller* has indicated its expectation to receive progressive results by setting `CALL.Options.receive_progress|bool := true`, a *Callee* is **not required** to produce progressive results. `CALL.Options.receive_progress` and `INVOCATION.Details.receive_progress` are simply indications that the *Caller* is prepared to process progressive results, should there be any produced. In other words, *Callees* are free to ignore such `receive_progress` hints at any time.

**Caller Leaving**

The *Dealer*'s behavior for when a *Caller* leaves or disconnects during a progressive results call shall be the same as in a basic, non-progressive call. That is, the *Dealer* sends an INTERRUPT to the *Callee* with `mode="killnowait"`. See [Caller Leaving During RPC Invocation] (#rpc-caller-leaving) under the Basic Profile.

{align="left"}
     ,------.           ,------.          ,------.
     |Caller|           |Dealer|          |Callee|
     `--+---'           `--+---'          `--+---'
        |       CALL       |                 |
        | ----------------->                 |
        |                  |    INVOCATION   |
        |                  | ---------------->
        |                  |                 |
        |                  | YIELD (progress)|
        |                  | <----------------
        |                  |                 |
        | RESULT (progress)|                 |
        | <-----------------                 |
     ,--+---.              |                 |
     |Caller|              |                 |
     `------'              |    INTERRUPT    |
      (gone)               | ---------------->
                           |                 |
                        ,--+---.          ,--+---.
                        |Dealer|          |Callee|
                        `------'          `------'

Such cancelation when the caller leaves addresses a potential security vulnerability: In cases where progressive results are used to stream data to *Callers*, and network connectivity is unreliable, *Callers* may often get disconnected in the middle of receiving such progressive results. Without the mandated cancelation behavior, recurring connect-call-disconnect cycles by a *Caller* would result in a rapidly growing backlog of unprocessed streaming results, overloading the router and further degrading network connectivity.


**Callee Leaving**

The *Dealer*'s behavior for when a *Callee* leaves or disconnects during a progressive results call shall be the same as in a basic, non-progressive call. That is, the *Dealer* sends an ERROR message to the *Caller* with the `wamp.error.canceled` URI. See [Callee Leaving During an RPC Invocation] (#rpc-callee-leaving) under the Basic Profile.

{align="left"}
     ,------.           ,------.          ,------.
     |Caller|           |Dealer|          |Callee|
     `--+---'           `--+---'          `--+---'
        |        CALL      |                 |
        | ----------------->                 |
        |                  |    INVOCATION   |
        |                  | ---------------->
        |                  |                 |
        |                  | YIELD (progress)|
        |                  | <----------------
        |                  |                 |
        | RESULT (progress)|                 |
        | <----------------|                 |
        |                  |              ,--+---.
        |                  |              |Callee|
        |                  |              `------'
        |      ERROR       |               (gone)
        | <--------------- |
        |                  |
     ,--+---.           ,--+---.
     |Caller|           |Dealer|
     `------'           `------'


**Ignoring Requests for Progressive Call Results**

A *Callee* that does not support progressive results SHOULD ignore any `INVOCATION.Details.receive_progress` flag.

A *Callee* that supports progressive results, but does not support call canceling is considered by the *Dealer* to not support progressive results.


**Timeouts**

When the *Call Timeouts* feature is used in combination with Progressive Call Results, the `CALL.Options.timeout|integer` option shall represent the time limit between the initial call and the first result, and between results thereafter.

For Dealer-initiated timeouts, this corresponds to
- the time between receipt of the `CALL` message and receipt of the first `YIELD` message, and,
- the time between received `YIELD` messages thereafter.

For Callee-initiated timeouts, this corresponds to
- the time between receipt of the `INVOCATION` message and acquisition of the first result, and,
- the time between acquisition of successive results thereafter.

Note that for progressive results, the timeout value does _not_ correspond to the duration of the complete call from initiation to the final result. The rationale for this is that it would be unfeasible to compute a reasonable timeout value for a call having a non-deterministic number of progressive results.
