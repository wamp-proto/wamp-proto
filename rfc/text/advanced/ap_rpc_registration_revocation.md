### Registration Revocation

Feature status: **alpha**

#### Feature Announcement

Support for this feature MUST be announced by *Callees* (role := "callee") and *Dealers* (role := "dealer") via

{align="left"}
        HELLO.Details.roles.<role>.features.
             registration_revocation|bool := true

If the *Callee* does not support registration_revocation, the *Dealer* may still revoke a registration to
support administrative functionality. In this case, the *Dealer* MUST NOT send an **UNREGISTERED**
message to the *Callee*. The *Callee* MAY use the registration meta event `wamp.registration.on_unregister`
to determine whether a session is removed from a registration.

#### Feature Definition

This feature allows a *Dealer* to actively revoke a previously granted registration.
To achieve this, the existing UNREGISTERED message is extended as described below.

#### Extending UNREGISTERED

When revoking a registration, the router has no request ID to reply to. So it's set to zero and another argument is
appended to indicate which registration to revoke. Optionally, a reason why the registration was revoked is also appended.

{align="left"}
        [UNREGISTERED, 0, Details|dict]

where

 * `Details.registration|bool` MUST be a previously issued registration ID.
 * `Details.reason|string` MAY provide a reason as to why the registration was revoked.

*Example*

{align="left"}
        [67, 0, {"registration": 1293722, "reason": "moving endpoint to other callee"}]
