### Sharded Subscription {#pubsub-sharded-subscription}

Feature status: **alpha**

Support for this feature MUST be announced by *Publishers* (`role := "publisher"`), *Subscribers* (`role := "subscriber"`) and *Brokers* (`role := "broker"`) via

{align="left"}
        HELLO.Details.roles.<role>.features.shareded_subscriptions|
            bool := true

Resource keys: `PUBLISH.Options.rkey|string` is a stable, technical **resource key**.

> E.g. if your sensor has a unique serial identifier, you can use that.

*Example*

{align="left"}
        [16, 239714735, {"rkey": "sn239019"}, "com.myapp.sensor.sn239019.
            temperature", [33.9]]


Node keys: `SUBSCRIBE.Options.nkey|string` is a stable, technical **node key**.

> E.g. if your backend process runs on a dedicated host, you can use its hostname.

*Example*

{align="left"}
        [32, 912873614, {"match": "wildcard", "nkey": "node23"},
            "com.myapp.sensor..temperature"]
