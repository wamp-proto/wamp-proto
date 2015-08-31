### Publisher Exclusion

Support for this feature MUST be announced by *Publishers* (`role := "publisher"`) and *Brokers* (`role := "broker"`) via

    HELLO.Details.roles.<role>.features.publisher_exclusion|bool := true

By default, a *Publisher* of an event will **not** itself receive an event published, even when subscribed to the `Topic` the *Publisher* is publishing to. This behavior can be overridden via

    PUBLISH.Options.exclude_me|bool

When publishing with `PUBLISH.Options.exclude_me := false`, the *Publisher* of the event will receive that event, if it is subscribed to the `Topic` published to.

*Example*

    [16, 239714735, {"exclude_me": false}, "com.myapp.mytopic1", ["Hello, world!"]]

In this example, the *Publisher* will receive the published event, if it is subscribed to `com.myapp.mytopic1`.
