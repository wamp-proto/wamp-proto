## Progressive Calls {#rpc-progressive-calls}

A *Caller* may issue a progressive call. This can be useful in few cases:

* Payload is too big to send it whole in one request. E.g. uploading a file.
* Payload is long term-based, and it is required to start processing it earlier.
* Partial results should be made available to the caller as quickly as possible. This can be accomplished
  in conjunction with Progressive Call Results feature.
* RPC is called too often. So overall processing can be optimized: there is no need to generate new id for request,
  initiate structures for new call, etc.

In this case, a procedure implemented by a *Callee* and registered at a *Dealer* may receive a progressive call.
*Callee* can wait until it receives the whole payload and only after that process and sends result or 
if *Callee*, *Caller* and *Dealer* supports `Progressive Call Results` feature it can even start sending results 
back to *Caller* right after processing received payload chunks.
This results in efficient two-way streams between *Caller* and *Callee*.

**Feature Announcement**

Support for this advanced feature MUST be announced by *Callers* (`role := "caller"`), *Callees* (`role := "callee"`) 
and *Dealers* (`role := "dealer"`) via

{align="left"}
        HELLO.Details.roles.<role>.features.progressive_calls|bool := true

Progressive Calls can work only if all three nodes support and announced this feature. 

Cases when *Caller* sends `CALL` message with `progress := true` without announcing it during `HELLO`
handshake MUST be treated as *PROTOCOL ERRORS* and underlying WAMP connections must be aborted with 
`wamp.error.protocol_violation` error reason.

Cases when *Caller* sends `CALL` message with `progress := true` to *Dealer*, that did not announce 
progressive calls support during `WELCOME` handshake MUST be treated as *PROTOCOL ERRORS* and underlying WAMP
connections must be aborted with `wamp.error.protocol_violation` error reason.

Cases when *Caller* sends `CALL` message with `progress := true` to the *Dealer* that supports this feature,
which then must be routed to the *Callee* which doesn't support progressive calls MUST be treated as *APPLICATION ERRORS*
and *Dealer* MUST respond to *Caller* with `wamp.error.feature_not_supported` error message.

**Message Flow**

The message flow for a progressive call when *Callee* waits for all chunks before processing and sending a single result:

{align="left"}
     ,------.                  ,------.                 ,------.
     |Caller|                  |Dealer|                 |Callee|
     `--+---'                  `--+---'                 `--+---'
        |     CALL (progress)     |                        |
        | ----------------------> |                        |
        |                         | INVOCATION (progress)  |
        |                         | ---------------------->|
        |     CALL (progress)     |                        |
        | ----------------------->|                        |
        |                         | INVOCATION (progress)  |
        |                         | ---------------------->|
        |                         |                        |
        |           ...           |          ...           |
        |                         |                        |
        |     CALL (final)        |                        |
        | ----------------------->|                        |
        |                         |   INVOCATION (final)   |
        |                         | ---------------------->|
        |                         |                        |
        |                         | YIELD (final) or ERROR |
        |                         | <----------------------|
        |                         |                        |
        | RESULT (final) or ERROR |                        |
        | <-----------------------|                        |
     ,--+---.                  ,--+---.                 ,--+---.
     |Caller|                  |Dealer|                 |Callee|
     `------'                  `------'                 `------'

As `progressive` call is still the same call *Caller* must send the same `Request|id` with every `CALL` and *Dealer*
must also send the same `Request|id` with every `INVOCATION` to the *Callee*.


The following message flow illustrates a progressive call when *Callee* starts sending progressive call 
results immediately. Please note that `YIELD` messages don't need to be matched with `CALL`/`INVOCATION` messages. 
E.g. *Caller* can send a few `CALL` messages before starting to receive `RESULTS`, they do not need to be correlated. 

{align="left"}
     ,------.                  ,------.                 ,------.
     |Caller|                  |Dealer|                 |Callee|
     `--+---'                  `--+---'                 `--+---'
        |     CALL (progress)     |                        |
        |------------------------>|                        |
        |                         | INVOCATION (progress)  |
        |                         |----------------------->|
        |                         |                        |
        |                         |   YIELD (progress)     |
        |                         |<-----------------------|
        |                         |                        |
        |   RESULT (progress)     |                        |
        |<------------------------|                        |
        |                         |                        |
        |    CALL (progress)      |                        |
        |------------------------>|                        |
        |                         | INVOCATION (progress)  |
        |                         |----------------------->|
        |                         |                        |
        |    CALL (progress)      |                        |
        |------------------------>|                        |
        |                         | INVOCATION (progress)  |
        |                         |----------------------->|
        |                         |    YIELD (progress)    |
        |                         |<-----------------------|
        |                         |                        |
        |   RESULT (progress)     |                        |
        |<------------------------|                        |
        |                         |                        |
        |                         |    YIELD (progress)    |
        |                         |<-----------------------|
        |                         |                        |
        |   RESULT (progress)     |                        |
        |<------------------------|                        |
        |                         |                        |
        |          ...            |          ...           |
        |                         |                        |
        |      CALL (final)       |                        |
        |------------------------>|                        |
        |                         |   INVOCATION (final)   |
        |                         |----------------------->|
        |                         |                        |
        |                         | YIELD (final) or ERROR |
        |                         |<-----------------------|
        |                         |                        |
        | RESULT (final) or ERROR |                        |
        |<------------------------|                        |
     ,--+---.                  ,--+---.                 ,--+---.
     |Caller|                  |Dealer|                 |Callee|
     `------'                  `------'                 `------'

A *Caller* indicates its willingness to issue a progressive call by setting

{align="left"}
        CALL.Options.progress|bool := true

*Example.* Caller-to-Dealer `CALL`

{align="left"}
```json
    [
        48,
        77245,
        {
            "progress": true
        },
        "com.myapp.get_country_by_coords",
        [50.450001, 30.523333]
    ]
```

If the *Callee* supports progressive calls, the *Dealer* shall forward the *Caller's* willingness to send progressive calls by setting

{align="left"}
        INVOCATION.Details.progress|bool := true


*Example.* Dealer-to-Callee `INVOCATION`

{align="left"}
```json
    [
        68,
        35224,
        379,
        {
            "progress": true
        },
        [50.450001, 30.523333]
    ]
```

A call invocation MUST *always* end in a *normal* `CALL` without `"progress": true` option, or explicitly 
set `"progress": false` which is the default.

**Progressive calls and shared registration**

RPCs can have a multiple registrations (see `Shared Registration` feature) with different `<invocation_policies>`.
In this case `progressive` `CALLs` can be routed to different *Callees*, which can lead to unexpected results.
To bind `INVOCATIONs` to the same *Callee*, the *Caller* can specify the `sticky` option during `CALL`

{align="left"}
        CALL.Options.sticky|bool := true


In this case *Dealer* must make a first `INVOCATION` based on `<invocation_policy>` and then route all 
subsequent `progressive` calls to the same *Callee*.

If binding all ongoing `progressive` calls to the same *Callee* is not required, *Caller* can set the `sticky` option to `FALSE`. 

If `CALL.Options.sticky` is not specified, it is treated like `TRUE`, so all `progressive`
calls go to the same *Callee*.

**Progressive Call Cancellation**

If the original *Caller* is no longer available for some reason (has left the realm), then the *Dealer* will send 
an `INTERRUPT` to the *Callee*. The `INTERRUPT` will have `Options.mode` set to `"killnowait"` to indicate to the 
client that no response should be sent to the `INTERRUPT`.

```
[INTERRUPT, INVOCATION.Request|id, Options|dict]
```
Options:
```
INTERRUPT.Options.mode|string == "killnowait"
```

Progressive call cancellation, like progressive call results cancellation closes an important safety gap: 
In cases where progressive calls are used to stream data from *Caller*, and network connectivity is unreliable, 
*Caller* may often get disconnected in the middle of sending progressive data. This can lead to unneeded memory
consumption for the *Dealer* and *Callee*, due to the need to store temporary metadata about ongoing calls.

The message flow for cancelling progressive calls involves:

{align="left"}
     ,------.            ,------.                 ,------.
     |Caller|            |Dealer|                 |Callee|
     `--+---'            `--+---'                 `--+---'
        |  CALL (progress)  |                        |
        | ----------------->|                        |
        |                   | INVOCATION (progress)  |
        |                   | ---------------------->|
        |  CALL (progress)  |                        |
        | ----------------->|                        |
        |                   | INVOCATION (progress)  |
        |                   | ---------------------->|
     ,--+---.               |                        |
     |Caller|               |                        |
     `------'               |                        |
      (gone)                |                        |
                            |       INTERRUPT        |
                            | ---------------------->|
                            |                        |
                         ,--+---.                 ,--+---.
                         |Dealer|                 |Callee|
                         `------'                 `------'


Note: Any `ERROR` returned by the *Callee*, in response to an `INTERRUPT`, is ignored (same as in regular call 
canceling when mode="killnowait"). So, it is not necessary for the *Callee* to send an `ERROR` message.

**Ignoring Progressive Call Requests**

Unlike other advanced features, the *Callee* cannot be unaware of progressive call requests.
Therefore, if a *Callee* doesn't support this feature, a *Dealer* MUST respond to *Caller* with an
`wamp.error.feature_not_supported` error message. 

A *Callee* that supports progressive calls, but does not support call canceling shall be considered by the *Dealer* 
as not supporting progressive calls.
