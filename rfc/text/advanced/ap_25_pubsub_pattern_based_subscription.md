## Pattern-based Subscription {#pattern-based-subscription}

By default, *Subscribers* subscribe to topics with **exact matching policy**. That is an event will only be 
dispatched to a *Subscriber* by the *Broker* if the topic published to (`PUBLISH.Topic`) *exactly* matches the 
topic subscribed to (`SUBSCRIBE.Topic`).

A *Subscriber* might want to subscribe to topics based on a *pattern*. This can be useful to reduce the number of 
individual subscriptions to be set up and to subscribe to topics the *Subscriber* is not aware of at the time of 
subscription, or which do not yet exist at this time.

Let's review the event publication flow. When one peer decides to publish a message to a topic, it results in 
a `PUBLISH` WAMP message with fields for the `Publication` id, `Details` dictionary, and, optionally, 
the payload arguments.

A given event received by the router from a publisher via a `PUBLISH` message will match one or more 
subscriptions:

* zero or one exact subscription
* zero or more prefix subscriptions
* zero or more wildcard subscriptions

The same published event is then forwarded to subscribers for every matching subscription.
Thus, a given event might be sent multiple times to the same client under different subscriptions.
Every subscription instance, based on a topic URI and some options, has a unique ID. All
subscribers of the same subscription are given the same subscription ID.

{align="left"}
                                +----------+            +------------+         +----------+
                                |          |            |   Exact    |         |Subscriber|
                                |          |---Event--->|Subscription|----+--->|   peer   |
                                |          |            +------------+    |    +----------+
   +----------+                 |          |            +------------+    |    +----------+
   |Publisher |                 |  Broker  |            |  Wildcard  |    +--->|Subscriber|
   |   peer   |--Publication--->|          |---Event--->|Subscription|----+--->|   peer   |
   +----------+                 |          |            +------------+    |    +----------+
                                |          |            +------------+    |    +----------+
                                |          |            |   Prefix   |    +--->|Subscriber|
                                |          |---Event--->|Subscription|-------->|   peer   |
                                +----------+            +------------+         +----------+

If the *Broker* and the *Subscriber* support **pattern-based subscriptions**, this matching can happen by

* prefix-matching policy
* wildcard-matching policy

**Feature Announcement**

Support for this feature MUST be announced by *Subscribers* (`role := "subscriber"`) and *Brokers* (`role := "broker"`) via

{align="left"}
        HELLO.Details.roles.<role>.features.
            pattern_based_subscription|bool := true


### Prefix Matching

A *Subscriber* requests **prefix-matching policy** with a subscription request by setting

{align="left"}
        SUBSCRIBE.Options.match|string := "prefix"

*Example*

{align="left"}
```json
    [
        32,
        912873614,
        {
            "match": "prefix"
        },
        "com.myapp.topic.emergency"
    ]
```

When a **prefix-matching policy** is in place, any event with a topic that has `SUBSCRIBE.Topic` as a *prefix* will match the subscription, and potentially be delivered to *Subscribers* on the subscription.

In the above example, events with `PUBLISH.Topic`

* `com.myapp.topic.emergency.11`
* `com.myapp.topic.emergency-low`
* `com.myapp.topic.emergency.category.severe`
* `com.myapp.topic.emergency`

will all apply for dispatching. An event with `PUBLISH.Topic` e.g. `com.myapp.topic.emerge` will not apply.


### Wildcard Matching

A *Subscriber* requests **wildcard-matching policy** with a subscription request by setting

{align="left"}
        SUBSCRIBE.Options.match|string := "wildcard"

Wildcard-matching allows to provide wildcards for **whole** URI components.

*Example*

{align="left"}
```json
    [
        32,
        912873614,
        {
            "match": "wildcard"
        },
        "com.myapp..userevent"
    ]
```

In above subscription request, the 3rd URI component is empty, which signals a wildcard in that URI component position. In this example, events with `PUBLISH.Topic`

* `com.myapp.foo.userevent`
* `com.myapp.bar.userevent`
* `com.myapp.a12.userevent`

will all apply for dispatching. Events with `PUBLISH.Topic`

* `com.myapp.foo.userevent.bar`
* `com.myapp.foo.user`
* `com.myapp2.foo.userevent`

will not apply for dispatching.

### Design Aspects

**No set semantics**

Since each *Subscriber's* subscription "stands on its own", there is no *set semantics* implied by pattern-based subscriptions.

E.g. a *Subscriber* cannot subscribe to a broad pattern, and then unsubscribe from a subset of that broad pattern to form a more complex subscription. Each subscription is separate.

**Events matching multiple subscriptions**

When a single event matches more than one of a *Subscriber's* subscriptions, the event will be delivered for each subscription.

The *Subscriber* can detect the delivery of that same event on multiple subscriptions via `EVENT.PUBLISHED.Publication`, which will be identical.

**Concrete topic published to**

If a subscription was established with a pattern-based matching policy, a *Broker* MUST supply the original `PUBLISH.Topic` as provided by the *Publisher* in

{align="left"}
        EVENT.Details.topic|uri

to the *Subscribers*.

*Example*

{align="left"}
```json
    [
        36,
        5512315355,
        4429313566,
        {
            "topic": "com.myapp.topic.emergency.category.severe"
        },
        ["Hello, world!"]
    ]
```
