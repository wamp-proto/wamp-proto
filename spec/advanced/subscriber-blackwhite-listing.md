# Subscriber Black- and Whitelisting

Support for this feature MUST be announced by *Publishers* (`role := "publisher"`) and *Brokers* (`role := "broker"`) via

    HELLO.Details.roles.<role>.features.subscriber_blackwhite_listing|bool := true

If the feature is supported, a *Publisher* may restrict the actual receivers of an event from the group of subscribers through the use of

 * `PUBLISH.Options.exclude|list`
 * `PUBLISH.Options.eligible|list`

`PUBLISH.Options.exclude` is a list of WAMP session IDs (`integer`s) providing an explicit list of (potential) *Subscribers* that won't receive a published event, even though they may be subscribed. In other words, `PUBLISH.Options.exclude` is a blacklist of (potential) *Subscribers*.

`PUBLISH.Options.eligible` is a list of WAMP session IDs (`integer`s) providing an explicit list of (potential) *Subscribers* that are allowed to receive a published event. In other words, `PUBLISH.Options.eligible` is a whitelist of (potential) *Subscribers*.

The *Broker* will dispatch events published only to *Subscribers* that are not explicitly excluded via `PUBLISH.Options.exclude` **and** which are explicitly eligible via `PUBLISH.Options.eligible`.

*Example*

    [16, 239714735, {"exclude": [7891255, 1245751]}, "com.myapp.mytopic1", ["Hello, world!"]]

The above event will get dispatched to all *Subscribers* of `com.myapp.mytopic1`, but not WAMP sessions with IDs `7891255` or `1245751` (and also not the publishing session).

*Example*

    [16, 239714735, {"eligible": [7891255, 1245751]}, "com.myapp.mytopic1", ["Hello, world!"]]

The above event will get dispatched to WAMP sessions with IDs `7891255` or `1245751` only - but only if those are subscribed to the topic `com.myapp.mytopic1`.

*Example*

    [16, 239714735, {"exclude": [7891255], "eligible": [7891255, 1245751, 9912315]}, "com.myapp.mytopic1", ["Hello, world!"]]

The above event will get dispatched to WAMP sessions with IDs `1245751` or `9912315` only (since `7891255` is excluded) - but only if those are subscribed to the topic `com.myapp.mytopic1`.
