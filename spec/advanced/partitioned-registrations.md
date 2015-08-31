### Distributed Registrations and Calls

Support for this feature MUST be announced by *Callers* (`role := "caller"`), *Callees* (`role := "callee"`) and *Dealers* (`role := "dealer"`) via

    HELLO.Details.roles.<role>.features.partitioned_rpc|bool := true


*Partitioned Calls* allows to run a call issued by a *Caller* on one or more endpoints implementing the called procedure.

* all
* any
* partition


`CALL.Options.runon|string := "all" or "any" or "partition"`
`CALL.Options.runmode|string := "gather" or "progressive"`
`CALL.Options.rkey|string`


#### "Any" Calls

If `CALL.Options.runon == "any"`, the call will be routed to one *randomly* selected *Callee* that registered an implementing endpoint for the called procedure. The call will then proceed as for standard (non-distributed) calls.


#### "All" Calls

If `CALL.Options.runon == "all"`, the call will be routed to all *Callees* that registered an implementing endpoint for the called procedure. The calls will run in parallel and asynchronously.

If `CALL.Options.runmode == "gather"` (the default, when `CALL.Options.runmode` is missing), the *Dealer* will gather the individual results received via `YIELD` messages from *Callees* into a single list, and return that in `RESULT` to the original *Caller* - when all results have been received.

If `CALL.Options.runmode == "progressive"`, the *Dealer* will call each endpoint via a standard `INVOCATION` message and immediately forward individual results received via `YIELD` messages from the *Callees* as progressive `RESULT` messages (`RESULT.Details.progress == 1`) to the original *Caller* and send a final `RESULT` message (with empty result) when all individual results have been received.

If any of the individual `INVOCATION`s returns an `ERROR`, the further behavior depends on ..

Fail immediate:

The *Dealer* will immediately return a `ERROR` message to the *Caller* with the error from the `ERROR` message of the respective failing invocation. It will further send `INTERRUPT` messages to all *Callees* for which it not yet has received a response, and ignore any `YIELD` or `ERROR` messages it might receive subsequently for the pending invocations.

The *Dealer* will accumulate ..


#### "Partitioned" Calls

If `CALL.Options.runmode == "partition"`, then `CALL.Options.rkey` MUST be present.

The call is then routed to all endpoints that were registered ..

The call is then processed as for "All" Calls.
