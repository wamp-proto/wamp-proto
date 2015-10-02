# Subscription Meta API

Within an application, it may be desirable for a publisher to know whether a publication to a specific topic currently makes sense, i.e. whether there are any subscribers who would receive an event based on the publication. It may also be desirable to keep a current count of subscribers to a topic to then be able to filter out any subscribers who are not supposed to receive an event.

Subscription _meta-events_ are fired when topics are first created, when clients subscribe/unsubscribe to them, and when topics are deleted. WAMP allows retrieving information about subscriptions via subscription _meta-procedures_.

Support for this feature **must** be announced by _Brokers_ (`role := "broker"`) via

   	HELLO.Details.roles.broker.features.subscription_meta_api|bool := true

Meta-events are created by the router itself. This means that the events as well as the data received when calling a meta-procedure can be accorded the same trust level as the router.


Subscription Meta-Events
------------------------

A client can subscribe to the following session meta-events, which cover the lifecycle of a subscription:

- `wamp.subscription.on_create`: Fired when a subscription is created through a subscription request for a topic which was previously without subscribers.
- `wamp.subscription.on_subscribe`: Fired when a session is added to a subscription.
- `wamp.subscription.on_unsubscribe`: Fired when a session is removed from a subscription.
- `wamp.subscription.on_delete`: Fired when a subscription is deleted after the last session attached to it has been removed.

A `wamp.subscription.on_subscribe` event **shall** always be fired subsequent to a `wamp.subscription.on_create` event, since the first subscribe results in both the creation of the subscription and the addition of a session. Similarly, the `wamp.subscription.on_delete` event **shall** always be preceded by a `wamp.subscription.on_unsubscribe` event.

The WAMP subscription meta events shall be dispatched by the router to the same realm as the WAMP session which triggered the event.


### Meta-Event Specifications

-----------------------------------

#### `wamp.subscription.on_create`

Fired when a subscription is created through a subscription request for a topic which was previously without subscribers.

**Event Arguments**
- `session|id`: ID of the session performing the subscription request.
- `SubscriptionDetails|dict`: Information on the created subscription.

**Object Schemas**

```javascript
SubscriptionDetails :=
{
    "id": subscription|id,
    "created": time_created|iso_8601_string,
    "uri": topic|uri,
    "match": match_policy|string
}
```

See [Pattern-based Subscriptions](pattern-based-subscription.md) for a description of `match_policy`.

-----------------------------------

#### `wamp.subscription.on_subscribe`

Fired when a session is added to a subscription.

**Event Arguments**
- `session|id`: ID of the session being added to a subscription.
- `subscription|id`: ID of the subscription to which the session is being added.

-----------------------------------

#### `wamp.subscription.on_unsubscribe`

Fired when a session is removed from a subscription.

**Event Arguments**
- `session|id`: ID of the session being removed from a subscription.
- `subscription|id`: ID of the subscription from which the session is being removed.

-----------------------------------

#### `wamp.subscription.on_delete`

Fired when a subscription is deleted after the last session attached to it has been removed.

**Arguments**
- `session|id`: ID of the last session being removed from a subscription.
- `subscription|id`: ID of the subscription being deleted.

-----------------------------------


Subscription Meta-Procedures
----------------------------

A client can actively retrieve information about subscriptions via the following meta-procedures:

- `wamp.subscription.list`: Retrieves subscription IDs listed according to match policies.
- `wamp.subscription.lookup`: Obtains the subscription (if any) managing a topic, according to some match policy.
- `wamp.subscription.match`: Retrieves a list of IDs of subscriptions matching a topic URI, irrespective of match policy.
- `wamp.subscription.get`: Retrieves information on a particular subscription.
- `wamp.subscription.list_subscribers`: Retrieves a list of session IDs for sessions currently attached to the subscription.
- `wamp.subscription.count_subscribers`: Obtains the number of sessions currently attached to the subscription.


### Meta-Procedure Specifications

-----------------------------------

#### `wamp.subscription.list`

Retrieves subscription IDs listed according to match policies.

**Arguments**
- None

**Results**
- `SubscriptionLists|dict`: A dictionary with a list of subscription IDs for each match policy.

**Object Schemas**

```javascript
SubscriptionLists :=
{
    "exact": subscription_ids|list,
    "prefix": subscription_ids|list,
    "wildcard": subscription_ids|list
}
```

See [Pattern-based Subscriptions](pattern-based-subscription.md) for information on match policies.

-----------------------------------

#### `wamp.subscription.lookup`

Obtains the subscription (if any) managing a topic, according to some match policy.

**Arguments**
- `topic|uri`: The URI of the topic.
- (Optional) `options|dict`: Same options as when subscribing to a topic.

**Results**
- (Nullable) `subscription|id`: The ID of the subscription managing the topic, if found, or null.

-----------------------------------

#### `wamp.subscription.match`

Retrieves a list of IDs of subscriptions matching a topic URI, irrespective of match policy.

**Arguments**
- `topic|uri`: The topic to match.

**Results**
- (Nullable) `subscription_ids|list`: A list of all matching subscription IDs, or null.

-----------------------------------

#### `wamp.subscription.get`

Retrieves information on a particular subscription.

**Arguments**
- `subscription|id`: The ID of the subscription to retrieve.

**Results**
- `SubscriptionDetails|dict`: Details on the subscription.

**Error URIs**
- `wamp.error.no_such_subscription`: No subscription with the given ID exists on the router.

**Object Schemas**

```javascript
SubscriptionDetails :=
{
    "id": subscription|id,
    "created": time_created|iso_8601_string,
    "uri": topic|uri,
    "match": match_policy|string
}
```

See [Pattern-based Subscriptions](pattern-based-subscription.md) for information on match policies.

-----------------------------------

#### `wamp.subscription.list_subscribers`

Retrieves a list of session IDs for sessions currently attached to the subscription.

**Arguments**
- `subscription|id`: The ID of the subscription to get subscribers for.

**Results**
- `subscribers_ids|list`: A list of WAMP session IDs of subscribers currently attached to the subscription.

**Error URIs**
- `wamp.error.no_such_subscription`: No subscription with the given ID exists on the router.

-----------------------------------

#### `wamp.subscription.count_subscribers`

Obtains the number of sessions currently attached to a subscription.

**Arguments**
- `subscription|id`: The ID of the subscription to get the number of subscribers for.

**Results**
- `count|int`: The number of sessions currently attached to a subscription.

**Error URIs**
- `wamp.error.no_such_subscription`: No subscription with the given ID exists on the router.

-----------------------------------


## Subscriber Meta Events

> This section is leftover from the initial advanced spec refactoring.

Support for this feature MUST be announced by *Subscribers* (`role := "subscriber"`) and *Brokers* (`role := "broker"`) via

    HELLO.Details.roles.<role>.features.subscriber_metaevents|bool := true

*Example*

    [32, 713845233,
         {"metatopics": ["wamp.metatopic.subscriber.add",
                         "wamp.metatopic.subscriber.remove"]},
         "com.myapp.mytopic1"]

If above subscription request by a *Subscriber 1* succeeds, the *Broker* will dispatch meta events to *Subscriber 1* for every *Subscriber 2, 3, ..* added to or removed from a subscription for `com.myapp.mytopic1`. It will also dispatch "normal" events on the topic `com.myapp.mytopic1` to *Subscriber 1*.

*Example*

    [32, 713845233,
         {"metatopics": ["wamp.metatopic.subscriber.add",
                         "wamp.metatopic.subscriber.remove"],
          "metaonly": 1},
         "com.myapp.mytopic1"]

This subscription works like the previous one, except that "normal" events on the topic `com.myapp.mytopic1` will NOT be dispatched to *Subscriber 1*. Consequently, it is called a "Meta Event only subscription".


Metaevents are always generated by the *Broker* itself and do not contain application payload:

    [EVENT, SUBSCRIBED.Subscription|id, PUBLISHED.Publication|id, Details|dict]

*Example*

    [36, 5512315355, 71415664, {"metatopic": "wamp.metatopic.subscriber.add", "session": 9712478}]

*Example*

    [36, 5512315355, 71415664, {"metatopic": "wamp.metatopic.subscriber.remove", "session": 9712478}]


The following metatopics are currently defined:

 1. `wamp.metatopic.subscriber.add`: A new subscriber is added to the subscription.
 2. `wamp.metatopic.subscriber.remove`: A subscriber is removed from the subscription.
