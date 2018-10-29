### Subscription Revocation

Feature status: **alpha**

#### Feature Announcement

Support for this feature MUST be announced by *Subscribers* (role := "subscriber") and *Brokers* (role := "broker") via

{align="left"}
        HELLO.Details.roles.<role>.features.
             subscription_revocation|bool := true

If the *Subscriber* does not support subscription_revocation, the *Broker* MAY still revoke a subscription to
support administrative functionality. In this case the *Broker* MUST NOT send a **UNSUBSCRIBED**
message to the *Subscriber*. The *Subscriber* MAY use the subscription meta event `wamp.subscription.on_unsubscribe`
to determine that a session is removed from a subscription.

#### Feature Definition

This feature allows a broker to actively revoke a previously granted subscription.
To achieve this, the existing UNSUBSCRIBED message is extended as described below.

#### Extending UNSUBSCRIBED

When revoking a subscription, the router has no request ID to reply to, so it's set to zero and another argument is
appended to indicate which subscription to revoke and optionally, a reason why the subscription was revoked.

{align="left"}
        [UNSUBSCRIBED, 0, Details|dict]

where

 * `Details.subscription|bool` MUST be a previously issued subscription ID.
 * `Details.reason|string` MAY be provide a reason, why the subscription was revoked.

*Example*

{align="left"}
        [35, 0, {"subscription": 1293722, "reason": "no longer authorized"}]

#### Feature Announcement

- TBD: Decide which roles to announce this feature on.
