### Shared Registration

Feature status: **alpha**

#### Feature Definition

As a default, only a single **Callee** may register a procedure for an URI.

There are use cases where more flexibility is required. As an example, for an application component with a high computing load, several instances may run, and load balancing of calls across these may be desired. As another example, in an application a second or third component providing a procedure may run, which are only to be called in case the primary component is no longer reachable (hot standby).

When shared registrations are supported, then the first **Callee** to register a procedure for a particular URI MAY determine that additional registrations for this URI are allowed, and what **Invocation Rules** to apply in case such additional registrations are made.

This is done through setting

{align="left"}
        REGISTER.Options.invoke|string := <invocation_policy>

where `<invocation_policy>` is one of

* 'single'
* 'roundrobin'
* 'random'
* 'first'
* 'last'

If the option is not set, 'single' is applied as a default.

With 'single', the **Dealer** MUST fail all subsequent attempts to register a procedure for the URI while the registration remains in existence.

With the other values, the **Dealer** MUST fail all subsequent attempts to register a procedure for the URI where the value for this option does not match that of the initial registration.

##### Load Balancing

For sets of registrations registered using either 'roundrobin' or 'random', load balancing is performed across calls to the URI.

For 'roundrobin', callees are picked subsequently from the list of registrations (ordered by the order of registration), with the picking looping back to the beginning of the list once the end has been reached.

For 'random' a callee is picked randomly from the list of registrations for each call.

##### Hot Stand-By

For sets of registrations registered using either 'first' or 'last', the first respectively last callee on the current list of registrations (ordered by the order of registration) is called.

#### Feature Announcement

Support for this feature MUST be announced by *Callees* (`role := "callee"`) and *Dealers* (`role := "dealer"`) via

{align="left"}
        HELLO.Details.roles.<role>.features.
            shared_registration|bool := true

#### Call Re-Routing

A _CALLEE_ might not be able to attend to a call. This may be due to a multitude of reasons including, but not limited to:

- _CALLEE_ is busy handling other requests and is not able to attend
- _CALLEE_ has dependency issues which prevent it from being able to fulfil the request
- In a HA environment, the _Callee_ knows that it is scheduled to be taken off the HA cluster and as such should not handle the request.

A _unavailable_ response allows for **automatic** reroute of a call by the _Dealer_ without the _CALLER_ ever having to know about it.

When such a situation occurs, the _Callee_ responds to a `INVOCATION` message with the error uri:

{align="left"}
wamp.error.unavailable

When the _Dealer_ receives the `wamp.error.unavailable` message in response to an `INVOCATION`, it will reroute the `CALL` to another _registration_ according to the rerouting rules of the `invocation_policy` of the `procedure`, as given below.

##### Rerouting Rules

The _Dealer_ MUST adhere to the `invocation policy` of the `procedure` when rerouting the `CALL`, while assuming that the `unavailable` registration virtually does not exist.

For different `invocation policy` the _Dealer_ MUST follow:

| Invocation Policy | Operation                                                                                                                           |
| ----------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| `single`          | Responds with a `wamp.error.no_available_callee` error message to the _CALLER_                                                      |
| `roundrobin`      | Picks the next `registration` from the _Registration Queue_ of the _Procedure_                                                      |
| `random`          | Picks another `registration` at random from the Registration Queue of the _Procedure_, as long as it is not the same `registration` |
| `first`           | Picks the `registration` which was registered after the _called_ registration was registered                                        |
| `last`            | Picks the `registration` which was registered right before the _called_ registration was registered                                 |

##### Failure Scenario

In case all available registrations of a _Procedure_ responds with a `wamp.error.unavailable` for a _CALL_, the _Dealer_ MUST respond with a `wamp.error.no_available_callee` to the _CALLER_

##### Feature Announcement

Support for this feature MUST be announced by _Callees_ (`role := "callee"`) and _Dealers_ (`role := "dealer"`) via

{align="left"}
HELLO.Details.roles.<role>.features.call_reroute|bool := true
