### Call Rerouting

#### Feature Definition

A *Callee* might not be able to attend to a call. This may be due to a multitude of reasons including, but not limited to:

* *Callee* is busy handling other requests and is not able to attend
* *Callee* has dependency issues which prevent it from being able to fulfil the request
* In a HA environment, the *Callee* knows that it is scheduled to be taken off the HA cluster and as such should not handle the request.

A *unavailable* response allows for **automatic** reroute of a call by the *Dealer* without the *CALLER* ever having to know about it.

When such a situation occurs, the *Callee* responds to a `INVOCATION` message with the error uri:

{align="left"}
        wamp.error.unavailable

When the *Dealer* receives the `wamp.error.unavailable` message in response to an `INVOCATION`, it will reroute the `CALL` to another fitting *registration*. 

#### Rerouting

The *Dealer* MUST adhere to the `invocation policy` of the `procedure` when rerouting the `CALL`, while assuming that the `unavailable` registration virtually does not exist.

For different `invocation policy` the *Dealer* MUST follow:

|Invocation Policy|Operation|
|-|-|
|`single`|Respond with a `wamp.error.no_available_callee` error message to the *CALLER*|
|`roundrobin`|*Dealer* picks the next `registration` from the *Registration Queue* of the *Procedure*|
|`random`|*Dealer* picks another `registration` at random from the Registration Queue of the *Procedure*, as long as it is not the same `registration`|
|`first`|*Dealer* picks the `registration` which was registered after the *called* registration was registered |
|`last`|*Dealer* picks the `registration` which was registered right before the *called* registration was registered|

#### Failure Scenario
In case all available registrations of a *Procedure* responds with a `wamp.error.unavailable` for a *CALL*, the *Dealer* MUST respond with a `wamp.error.no_available_callee` to the *CALLER*
