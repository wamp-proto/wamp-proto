## Publication Trust Levels {#pubsub-pub-trustlevels}

A *Broker* may be configured to automatically assign *trust levels* to events published by *Publishers* according to the *Broker* configuration on a per-topic basis and/or depending on the application defined role of the (authenticated) *Publisher*.

A *Broker* supporting trust level will provide

{align="left"}
        EVENT.Details.trustlevel|integer

in an `EVENT` message sent to a *Subscriber*. The trustlevel `0` means lowest trust, and higher integers represent (application-defined) higher levels of trust.

*Example*

{align="left"}
        [36, 5512315355, 4429313566, {"trustlevel": 2},
            ["Hello, world!"]]

In above event, the *Broker* has (by configuration and/or other information) deemed the event publication to be of trustlevel `2`.


**Feature Announcement**

Support for this feature MUST be announced by *Subscribers* (`role := "subscriber"`) and *Brokers* (`role := "broker"`) via

{align="left"}
        HELLO.Details.roles.<role>.features.
            publication_trustlevels|bool := true