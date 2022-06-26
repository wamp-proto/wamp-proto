## Subscription Revocation

Feature status: **alpha**

This feature allows a *Broker* to actively revoke a previously granted subscription.
To achieve this, the existing UNSUBSCRIBED message is extended as described below.

**Feature Announcement**

Support for this feature MUST be announced by *Subscribers* (role := "subscriber") and *Brokers* (role := "broker") via

{align="left"}
        HELLO.Details.roles.<role>.features.
             subscription_revocation|bool := true

If the *Subscriber* does not support subscription_revocation, the *Broker* MAY still revoke a subscription to
support administrative functionality. In this case, the *Broker* MUST NOT send an **UNSUBSCRIBED**
message to the *Subscriber*. The *Subscriber* MAY use the subscription meta event `wamp.subscription.on_unsubscribe`
to determine whether a session is removed from a subscription.

**Extending UNSUBSCRIBED**

When revoking a subscription, the router has no request ID to reply to. So it's set to zero and another argument is
appended to indicate which subscription to revoke. Optionally, a reason why the subscription was revoked is also appended.

{align="left"}
        [UNSUBSCRIBED, 0, Details|dict]

where

 * `Details.subscription|bool` MUST be a previously issued subscription ID.
 * `Details.reason|string` MAY provide a reason as to why the subscription was revoked.

*Example*

{align="left"}
        [35, 0, {"subscription": 1293722, "reason": "no longer authorized"}]
