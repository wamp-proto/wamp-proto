### Subscription Revocation

Feature status: **alpha**

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
