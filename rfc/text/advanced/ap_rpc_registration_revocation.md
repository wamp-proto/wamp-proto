### Registration Revocation

Feature status: **alpha**

#### Feature Announcement

Support for this feature MUST be announced by *Callees* (role := "callee") and *Dealers* (role := "dealer") via

{align="left"}
        HELLO.Details.roles.<role>.features.
             registration_revocation|bool := true

If the *Callee* does not support registration_revocation, the *Dealer* may still revoke a registration to
support administrative functionality. In this case the *Dealer* MUST NOT send a **UNREGISTERED**
message to the *Callee*. The *Callee* MAY use the registration meta event `wamp.registration.on_unregister`
to determine that a session is removed from a registration.

#### Feature Definition

This feature allows a dealer to actively revoke a previously granted registration.
To achieve this, the existing UNREGISTERED message is extended as described below.

#### Extending UNREGISTERED

When revoking a registration, the router has no request ID to reply to, so it's set to zero and another argument is
appended to indicate which registration to revoke and optionally, a reason why the registration was revoked.

{align="left"}
        [UNREGISTERED, 0, Details|dict]

where

 * `Details.registration|bool` MUST be a previously issued registration ID.
 * `Details.reason|string` MAY be provide a reason, why the subscription was revoked.

*Example*

{align="left"}
        [67, 0, {"registration": 1293722, "reason": "moving endpoint to other callee"}]

#### Feature Announcement

- TBD: Decide which roles to announce this feature on.
