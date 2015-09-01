# Progressive Call Results

Support for this advanced feature MUST be announced by *Callers* (`role := "caller"`), *Callees* (`role := "callee"`) and *Dealers* (`role := "dealer"`) via

    HELLO.Details.roles.<role>.features.progressive_call_results|bool := true


A procedure implemented by a *Callee* and registered at a *Dealer* may produce progressive results (incrementally). The message flow for progressive results involves:

![alt text](../figure/rpc_progress1.png "RPC Message Flow: Calls")


A *Caller* indicates it's willingness to receive progressive results by setting

    CALL.Options.receive_progress|bool := true

*Example.* Caller-to-Dealer `CALL`

    [48, 77133, {"receive_progress": true}, "com.myapp.compute_revenue", [2010, 2011, 2012]]

If the *Callee* supports progressive calls, the *Dealer* will forward the *Caller's* willingness to receive progressive results by setting

    INVOCATION.Options.receive_progress|bool := true

*Example.* Dealer-to-Callee `INVOCATION`

    [68, 87683, 324, {"receive_progress": true}, [2010, 2011, 2012]]

An endpoint implementing the procedure produces progressive results by sending `YIELD` messages to the *Dealer* with

    YIELD.Options.progress|bool := true

*Example.* Callee-to-Dealer progressive `YIELDs`

    [70, 87683, {"progress": true}, ["Y2010", 120]]
    [70, 87683, {"progress": true}, ["Y2011", 205]]
    ...

Upon receiving an `YIELD` message from a *Callee* with `YIELD.Options.progress == true` (for a call that is still ongoing), the *Dealer* will **immediately** send a `RESULT` message to the original *Caller* with

    RESULT.Details.progress|bool := true

*Example.* Dealer-to-Caller progressive `RESULTs`

    [50, 77133, {"progress": true}, ["Y2010", 120]]
    [50, 77133, {"progress": true}, ["Y2011", 205]]
    ...

An invocation MUST *always* end in either a *normal* `RESULT` or `ERROR` message being sent by the *Callee* and received by the *Dealer*.

*Example.* Callee-to-Dealer final `YIELD`

    [70, 87683, {}, ["Total", 490]]

*Example.* Callee-to-Dealer final `ERROR`

    [4, 87683, {}, "com.myapp.invalid_revenue_year", [1830]]

A call MUST *always* end in either a *normal* `RESULT` or `ERROR` message being sent by the *Dealer* and received by the *Caller*.

*Example.* Dealer-to-Caller final `RESULT`

    [50, 77133, {}, ["Total", 490]]

*Example.* Dealer-to-Caller final `ERROR`

    [4, 77133, {}, "com.myapp.invalid_revenue_year", [1830]]

In other words: `YIELD` with `YIELD.Options.progress == true` and `RESULT` with `RESULT.Details.progress == true` messages may only be sent *during* a call or invocation is still ongoing.

The final `YIELD` and final `RESULT` may also be empty, e.g. when all actual results have already been transmitted in progressive result messages.

*Example.* Callee-to-Dealer `YIELDs`

    [70, 87683, {"progress": true}, ["Y2010", 120]]
    [70, 87683, {"progress": true}, ["Y2011", 205]]
     ...
    [70, 87683, {"progress": true}, ["Total", 490]]
    [70, 87683, {}]

*Example.* Dealer-to-Caller `RESULTs`

    [50, 77133, {"progress": true}, ["Y2010", 120]]
    [50, 77133, {"progress": true}, ["Y2011", 205]]
     ...
    [50, 77133, {"progress": true}, ["Total", 490]]
    [50, 77133, {}]

The progressive `YIELD` and progressive `RESULT` may also be empty, e.g. when those messages are only used to signal that the procedure is still running and working, and the actual result is completely delivered in the final `YIELD` and `RESULT`:

*Example.* Callee-to-Dealer `YIELDs`

    [70, 87683, {"progress": true}]
    [70, 87683, {"progress": true}]
    ...
    [70, 87683, {}, [["Y2010", 120], ["Y2011", 205], ..., ["Total", 490]]]

*Example.* Dealer-to-Caller `RESULTs`

    [50, 77133, {"progress": true}]
    [50, 77133, {"progress": true}]
    ...
    [50, 77133, {}, [["Y2010", 120], ["Y2011", 205], ..., ["Total", 490]]]

Note that intermediate, progressive results and/or the final result MAY have different structure. The WAMP peer implementation is responsible for mapping everything into a form suitable for consumption in the host language.

*Example.* Callee-to-Dealer `YIELDs`

    [70, 87683, {"progress": true}, ["partial 1", 10]]
    [70, 87683, {"progress": true}, [], {"foo": 10, "bar": "partial 1"}]
     ...
    [70, 87683, {}, [1, 2, 3], {"moo": "hello"}]

*Example.* Dealer-to-Caller `RESULTs`

    [50, 77133, {"progress": true}, ["partial 1", 10]]
    [50, 77133, {"progress": true}, [], {"foo": 10, "bar": "partial 1"}]
     ...
    [50, 77133, {}, [1, 2, 3], {"moo": "hello"}]

Even if a *Caller* has indicated it's expectation to receive progressive results by setting `CALL.Options.receive_progress|bool := true`, a *Callee* is **not required** to produce progressive results. `CALL.Options.receive_progress` and `INVOCATION.Options.receive_progress` are simply indications that the *Callee* is prepared to process progressive results, should there be any produced. In other words, *Callees* are free to ignore such `receive_progress` hints at any time.

<!--

**Errors**


If a *Caller* has not indicated support for progressive results or has sent a `CALL` to the *Dealer* without setting `CALL.Options.receive_progress == true`, and the *Dealer* sends a progressive `RESULT`, the *Caller* MUST fail the complete session with the *Dealer*.

If a *Dealer* has not indicated support for progressive results or the *Dealer* has sent an `INVOCATION` to the *Callee* without setting `INVOCATION.Options.receive_progress == true`, and the *Callee* sends a progressive `YIELD`, the *Dealer* MUST fail the call with error

    wamp.error.unexpected_progress_in_yield

If a *Caller* has not indicated support for progressive results and sends a `CALL` to the *Dealer* while setting `CALL.Options.receive_progress == true`, the *Dealer* MUST fail the call

However, if a *Caller* has *not* indicated it's willingness to receive progressive results in a call, the *Dealer* MUST NOT send progressive `RESULTs`, and a *Callee* MUST NOT produce progressive `YIELDs`.

A *Dealer* that does not support progressive calls MUST ignore any option `CALL.Options.receive_progress` received by a *Caller*, and **not** forward the option to the *Callee*.



If a *Callee* that has not indicated support for progressive results and the *Dealer* sends an `INVOCATION` with `INVOCATION.Options.receive_progress == true


A *Callee* that does not support progressive results SHOULD ignore any `INVOCATION.Options.receive_progress` flag.

If a *Dealer* has not indicated support for progressive results, and it receives a `CALL` from a *Caller* with `CALL.Options.receive_progress == true`, the *Dealer* MUST fail the call with error

    wamp.error.unsupported_feature.dealer.progressive_call_result



*Example.* Dealer-to-Caller `ERROR`

    [4, 87683, {}, "wamp.error.unsupported_feature.dealer.progressive_call_result"]



If the *Caller* does not support receiving *progressive calls*, as indicated by

    HELLO.Details.roles.caller.features.progressive_call_results == false

and *Dealer* receives a `YIELD` message from the *Callee* with `YIELD.Options.progress == true`, the *Dealer* MUST fail the call.

*Example.* Callee-to-Dealer `YIELD`

    [70, 87683, {"progress": true}, ["partial 1", 10]]

*Example.* Dealer-to-Caller `ERROR`

    [4, 87683, {}, "wamp.error.unsupported_feature.caller.progressive_call_result"]

If the *Dealer* does not support processing *progressive invocations*, as indicated by

    HELLO.Details.roles.dealer.features.progressive_call_results == false

and *Dealer* receives a `YIELD` message from the *Callee* with `YIELD.Options.progress == true`, the *Dealer* MUST fail the call.

*Example.* Callee-to-Dealer `YIELD`

    [70, 87683, {"progress": true}, ["partial 1", 10]]

*Example.* Dealer-to-Caller `ERROR`

    [4, 87683, {}, "wamp.error.unsupported_feature.dealer.progressive_call_result"]

-->

