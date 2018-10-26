### Registration Revocation

Feature status: **alpha**

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
