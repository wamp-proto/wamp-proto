### Progressive Call Results

#### Feature Definition

A procedure implemented by a *Callee* and registered at a *Dealer* may produce progressive results. Progressive results can e.g. be used to return partial results for long-running operations, or to chunk the transmission of larger results sets.

The message flow for progressive results involves:

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

If the *Callee* supports progressive calls, the *Dealer* will forward the *Caller's* willingness to receive progressive results by setting

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
...


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
        4,
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
        4,
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

#### Progressive Call Result Cancellation

Upon receiving a `YIELD` message from a _Callee_ with `YIELD.Options.progress == true` (for a call that is still ongoing), if the original _Caller_ is no longer available (has left the realm), then the _Dealer_ will send an `INTERRUPT` to the _Callee_.  The `INTERRUPT` will have `Options.mode` set to `"killnowait"` to indicate to the client that no response should be sent to the `INTERRUPT`. This `INTERRUPT` in only sent in response to a progressive `YIELD` (`Details.progress == true`), and is not sent in response to a normal or final `YIELD`.
```
[INTERRUPT, INVOCATION.Request|id, Options|dict]
```
Options:
```
INTERRUPT.Options.mode|string == "killnowait"
```

Progressive call result cancellation closes an important safety gap: In cases where progressive results are used to stream data to callers, and network connectivity is unreliable, callers my often get disconnected in the middle of receiving progressive results. Recurring connect, call, disconnect cycles can quickly build up callees streaming results to dead callers. This can overload the router and further degrade network connectivity.

The message flow for progressive results involves:

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
     ,--+---.              |                 |
     |Caller|              |                 |
     `------'              | YIELD (progress)|
      (gone)               | <----------------
                           |                 |
                           |    INTERRUPT    |    
                           | ---------------->    
                           |                 |    
                        ,--+---.          ,--+---.
                        |Dealer|          |Callee|
                        `------'          `------'

Note: Any `ERROR` returned by the Callee, in response to the `INTERRUPT`, is ignored (same as in call canceling when mode="killnowait"). So, it is not necessary for the Callee to send an `ERROR` message.

#### Callee

A Callee that does not support progressive results SHOULD ignore any `INVOCATION.Details.receive_progress` flag.

A Callee that supports progressive results, but does not support call canceling will be considered by the router to not support progressive results.

#### Feature Announcement

Support for this advanced feature MUST be announced by *Callers* (`role := "caller"`), *Callees* (`role := "callee"`) and *Dealers* (`role := "dealer"`) via

{align="left"}
        HELLO.Details.roles.<role>.features.
             progressive_call_results|bool := true

Additionally, _Callees_ and _Dealers_ MUST support Call Canceling, which is required for canceling progressive results if the original _Caller_ leaves the realm. If a _Callee_ supports Progressive Call Results, but not Call Canceling, then the _Dealer_ disregards the _Callees_ Progressive Call Results feature.
