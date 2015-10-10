### Call Trust Levels

Feature status: **alpha**


#### Feature Defintion

A *Dealer* may be configured to automatically assign *trust levels* to calls issued by *Callers* according to the *Dealer* configuration on a per-procedure basis and/or depending on the application defined role of the (authenticated) *Caller*.

A *Dealer* supporting trust level will provide

{align="left"}
        INVOCATION.Details.trustlevel|integer

in an `INVOCATION` message sent to a *Callee*. The trustlevel `0` means lowest trust, and higher integers represent (application-defined) higher levels of trust.

*Example*

{align="left"}
        [68, 6131533, 9823526, {"trustlevel": 2}, ["Hello, world!"]]

In above event, the *Dealer* has (by configuration and/or other information) deemed the call (and hence the invocation) to be of trustlevel `2`.


#### Feature Announcement

Support for this feature MUST be announced by *Callees* (`role := "callee"`) and *Dealers* (`role := "dealer"`) via

{align="left"}
        HELLO.Details.roles.<role>.features.call_trustlevels|bool := true