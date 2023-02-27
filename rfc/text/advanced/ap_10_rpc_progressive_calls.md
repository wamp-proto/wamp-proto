## Progressive Calls {#rpc-progressive-calls}

A *Caller* may issue a progressive call. This can be useful in a few cases:

* Payload is too big to send it whole in one request, e.g., uploading a file.
* Long-term data transfer that needs to be consumed early, such as a media stream.
* RPC is called too often and overall processing can be optimized: avoid the need to generate a new id for requests,
  initiate data structures for a new call, etc.

In such cases, a procedure implemented by a *Callee* and registered at a *Dealer* may be made to receive progressive calls,
where the *Callee* waits after receiving the entire set of payload chunks before sending the result. 


**Feature Announcement**

Support for this advanced feature MUST be announced by *Callers* (`role := "caller"`), *Callees* (`role := "callee"`) 
and *Dealers* (`role := "dealer"`) via

{align="left"}
        HELLO.Details.roles.<role>.features.progressive_calls|bool := true

Progressive Calls can work only if all three peers support and announce this feature.
In addition, *Callees* MUST announce support of the _Call Cancelling_ feature via

{align="left"}
        HELLO.Details.roles.callee.features.call_cancelling|bool := true

The following cases, where a *Caller* sends a `CALL` message with `progress := true`, MUST be treated as *protocol errors*
with the underlying WAMP sessions being aborted:

- The *Caller* did not announce the progressive calls feature during the `HELLO` handshake.
- The *Dealer* did not announce the progressive calls feature during the `HELLO` handshake.

Otherwise, in cases where the *Caller* sends a `CALL` message with `progress := true` but the *Callee* does not support
progressive calls or call cancelling, the call MUST be treated as an *application error* with the *Dealer* responding
to the *Caller* with the `wamp.error.feature_not_supported` error message.

**Message Flow**

The message flow for a progressive call when a *Callee* waits for all chunks before processing and sending a single result:

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

As a `progressive` call chunks are part of the same overall call, the *Caller* must send the same `Request|id`
for every `CALL` and the *Dealer* must also use the same `Request|id` with every `INVOCATION` to the *Callee*.

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

A call invocation MUST *always* end in a *normal* `CALL` without the `"progress": true` option, or explicitly 
set `"progress": false` which is the default.

**Request Id Verification**

When the *Progressive Calls* feature is supported, a *Caller* MAY use a prior request ID in a `CALL` message to
reference an already active progressive call. However, if a `CALL` request ID refers to an active request that
is not a progressive call, then that shall be considered a protocol violation.

When checking `CALL` request IDs, if a request with the given ID is no longer active, then it shall NOT be
considered a protocol violation. This is necessary to cope with the race condition of a *Caller* sending a
subsequent progressive `CALL` while a *Dealer* concurrently sends an `ERROR` or final `RESULT` back to the *Caller*.
To avoid having to store the history of past requests, the *Dealer* doesn't need to check that the expired request
ID belonged to an actual call.

**Progressive Calls and Shared Registration**

RPCs can have a multiple registrations (see `Shared Registration` feature) with different `<invocation_policies>`.
In this case, progressive `CALL` messages can be routed to different *Callees*, which can lead to unexpected results.
To bind `INVOCATION` messages to the same *Callee*, the *Caller* can specify the `sticky` option during `CALL`

{align="left"}
        CALL.Options.sticky|bool := true


In this case, the *Dealer* must make a first `INVOCATION` based on `<invocation_policy>` and then route all 
subsequent `progressive` calls to the same *Callee*.

If binding all ongoing `progressive` calls to the same *Callee* is not required, the *Caller* can set the `sticky` option to `false`. 

If `CALL.Options.sticky` is not specified, it is treated like `true`, so all `progressive`
calls go to the same *Callee*.


**Progressive Call Cancellation**

If the original *Caller* is no longer available for some reason (has left the realm), then the *Dealer* shall send 
an `INTERRUPT` to the *Callee*. The `INTERRUPT` MUST have `Options.mode` set to `"killnowait"` to indicate to the 
client that no response should be sent to the `INTERRUPT`.

```
[INTERRUPT, INVOCATION.Request|id, Options|dict]
```
Options:
```
INTERRUPT.Options.mode|string == "killnowait"
```

Progressive call cancellation, like in progressive calls, closes an important safety gap: 
In cases where progressive calls are used to stream data from a *Caller*, and network connectivity is unreliable, 
the *Caller* may often get disconnected in the middle of sending progressive data. This can lead to unneeded memory
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
canceling when mode="killnowait"). It is therefore not necessary for the *Callee* to send an `ERROR` message.


**Ignoring Progressive Call Requests**

Unlike some other advanced features, a *Callee* cannot be unaware of progressive call requests.
Therefore, if a *Callee* doesn't support this feature, the *Dealer* MUST respond to the *Caller* with an
`wamp.error.feature_not_supported` error message. 

A *Callee* that supports progressive calls, but does not support call canceling, shall be considered by the *Dealer* 
as not supporting progressive calls.


**Progressive Calls with Progressive Call Results**

Progressive calls may be used in conjunction with *Progressive Call Results* if the *Caller*, *Dealer*, and *Callee* all
support both features. This allows the *Callee* to start sending partial results back to the *Caller* after receiving
one or more initial payload chunks. Efficient two-way streams between a *Caller* and *Callee* can be implemented this way.
  
The following message flow illustrates a progressive call when a *Callee* starts sending progressive call 
results immediately. Note that `YIELD` messages don't need to be matched with `CALL`/`INVOCATION` messages. 
For example, the *caller* can send a few `CALL` messages before starting to receive `RESULT` messages; they do not need
to be matched pairs.

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

Because they are part of the same call operation, the request ID is the same in all `CALL`,
`INVOCATION`, `YIELD`, and `ERROR` messages in the above exchange.


**Freezing of Options in Progressive Calls**

Except for `progress`, items in the `Options` dictionary of the **initiating** progressive `CALL` shall be effective for
the entirety of the progressive call request. Only the `progress` option shall be considered by the *Dealer* in subsequent progressive calls
(within the same overall request). Except for `progress`, items in the `Details`
dictionary of corresponding `INVOCATION` messages shall be based on the initiating progressive `CALL` only.
  
For example, if `disclose_me=true` was specified in the initiating progressive call, all subsequent progressive calls
(within the same request) shall be considered by the *Dealer* to implictly have `disclose_me=true` as well. That is, all
`INVOCATION` messages associated with the overall request shall contain caller identify information.

Note that any option (besides `progress`) can be omitted altogether in subsequent progressive calls. Not having to repeat (and not being able to change) options is more in tune with the concept of a media stream where options are set up initially, and the source (*Caller*) only needs to keep uploading more data thereafter.

For reference, here is a list of options that are frozen upon the initial progressive call:

- `CALL.Options.disclose_me|bool`
- `CALL.Options.ppt_cipher|string`
- `CALL.Options.ppt_keyid|string`
- `CALL.Options.ppt_scheme|string`
- `CALL.Options.ppt_serializer|string`
- `CALL.Options.receive_progress|bool`
- `CALL.Options.rkey`
- `CALL.Options.runmode|string`
- `CALL.Options.sticky|bool`
- `CALL.Options.timeout|integer`
