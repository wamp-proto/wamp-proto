### Distributed Subscriptions and Publications

Support for this feature MUST be announced by *Publishers* (`role := "publisher"`), *Subscribers* (`role := "subscriber"`) and *Brokers* (`role := "broker"`) via

    HELLO.Details.roles.<role>.features.partitioned_pubsub|bool := true

Resource keys: `PUBLISH.Options.rkey|string` is a stable, technical **resource key**.

> E.g. if your sensor has a unique serial identifier, you can use that.


*Example*

    [16, 239714735, {"rkey": "sn239019"}, "com.myapp.sensor.sn239019.temperature", [33.9]]


Node keys: `SUBSCRIBE.Options.nkey|string` is a stable, technical **node key**.

> E.g. if your backend process runs on a dedicated host, you can use its hostname.


*Example*

    [32, 912873614, {"match": "wildcard", "nkey": "node23"}, "com.myapp.sensor..temperature"]
