## Event History {#pubsub-event-history}

Instead of complex QoS for message delivery, a *Broker* may provide *message history*. A *Subscriber* is 
responsible to handle overlaps (duplicates) when it wants "exactly-once" message processing across restarts.

The event history may be transient or persistent message history (surviving *Broker* restarts).

The *Broker* implementation may allow for configuration of event history on a per-topic or on a per-topic 
pattern basis. Such configuration could enable/disable the feature, event history storage location and 
parameters such as compression, or the event history data retention policy.

To understand what actually event history means lets review the publication flow. When one peer decides to publish
a message to a topic it results in `Publication` WAMP message with concrete `publication_id`, `payload` and `options`
among other attributes. The *Broker* in his turn checks current subscriptions and create an `Event` WAMP message for
every subscription. There can be no subscriptions, one exactly matched to publication topic subscription and zero or 
more pattern-based subscriptions. Every unique subscription (based on topic URI and options) has unique ID. All
subscribers of the same subscription get the same subscription ID.

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

Event History means the events published to concrete subscription in historical order. Let's see an example.

Subscriptions:

1. Subscription to exact match 'com.mycompany.log.auth' topic
2. Subscription to exact match 'com.mycompany.log.basket' topic
3. Subscription to prefix-based 'com.mycompany.log' topic

Publication messages:

1. Publication to topic 'com.mycompany.log.auth'. Delivered as event to 1st and 3rd subscriptions.
2. Publication to topic 'com.mycompany.log.basket'. Delivered as event to 2nd and 3rd subscriptions.
3. Publication to topic 'com.mycompany.log.basket'. Delivered as event to 2nd and 3rd subscriptions.
4. Publication to topic 'com.mycompany.log.basket'. Delivered as event to 2nd and 3rd subscriptions.
5. Publication to topic 'com.mycompany.log.checkout'. Delivered as event to 3rd subscription only.

Event History:

* Event History for 1st subscription includes only 1st publication.
* Event History for 2nd subscription includes 2nd, 3rd, 4th publications.
* Event History for 3rd subscription includes all publications.

**Feature Announcement**

A *Broker* that implements *event history* must indicate 
`HELLO.roles.broker.features.event_history = true` and (also) announce role `HELLO.roles.callee`, 
and provide the builtin procedures described below.

**Receiving Event History**

A *Caller* can request message history by calling the *Broker* procedure

{align="left"}
        wamp.event.history.last

with `Arguments = [subscription|id, limit|integer]` where

* `subscription` is the subscription id to retrieve event history for
* `limit` indicates the number of last N events to retrieve

or by calling

{align="left"}
        wamp.event.history.since

with `Arguments = [subscription|id, timestamp|string]` where

* `subscription` is the subscription id to retrieve event history for
* `timestamp` indicates the UTC timestamp since when to retrieve the events in the ISO-8601 format `yyyy-MM-ddThh:mm:ss:SSSZ` (e.g. `"2013-12-21T13:43:11:000Z"`)

or by calling

{align="left"}
        wamp.event.history.after

with `Arguments = [subscription|id, publication|id]`

* `subscription` is the subscription id to retrieve event history for
* `publication` is the id of an event which marks the start of the events to retrieve from history

The results of all RPC above are the same and looks like an `arguments` array of `Event` objects with additional event 
timestamp and some additional general information about request in `argumentsKw`. It can also be an empty array in case there were no publications to specified subscription yet or all 
events were filtered out by specified criteria.

{align="left"}
```javascript
  [
    {
        "timestamp": "yyyy-MM-ddThh:mm:ss:SSSZ", // Ыtring with event date in ISO-8601 format
        "subscription": 2342423, // The subscription ID of the event
        "publication": 32445235, // The original publication ID of the event
        "details": {},           // The original details of the event
        "args": [],              // The original list arguments payload of the event. May be ommited
        "kwargs": {}             // The original key-value arguments payload of the event. May be ommited
    }
  ]
```

In cases when the events set is pretty big to send it in a single result, router implementations
may provide additional options, like pagination or returning a progressive results. 

As Event History feature operates on `subscription|id` there can be situations when there is no subscribers to topic
of interest yet, but publications happens. In this case the *Broker* can not prematurely know what events to store.
If the *Broker* implementation allows configuration on per-topic basis, it may overcome this situations by 
preinitializing history-enabled topics with subscriptions even if there is no real subscribers yet exists.

Sometimes a client may not be interested in subscribing to a topic just to get a subscription id. In that case
a client may use some [Subscriptions Meta API RPC](#name-procedures-3) for retrieving subscription IDs by topic URIs
if WAMP router supports it.

**Security Aspects**

To be able to request event history, peer must be allowed to subscribe to desired subscription first. Thus, if peer
can not subscribe to a topic (which results in subscription under the hood) it can not receive events history too. 
And second point: peer must be allowed to call related META procedures for getting the event history described above.
Event History RPC calls with prohibited requests must fail with `wamp.error.not_authorized` Error URI.

Original publications may include additional options, like `black-white-listing` that enforces special event 
processing. The same rules must apply to event history requests. For example, if original publication has 
`eligible_authrole = 'admin'`, but request for history came from peer with `authrole = 'user'`, then even if 
`user` is authorized to subscribe to topic and thus is authorized to ask for event history, this publication 
must be filtered out from this concrete request results on the router side.

`black-white-listing` feature also allows to filter events delivery on `session ID` basis. In the context of
event history that can results in unexpected behaviour: `session ID` are generated randomly in runtime for every
session connection so newly connected sessions asking for event history may receive events originally excluded 
or vice versa may not receive expected events due to session ID mismatch. To prevent this unexpected behaviour
all events published with `Options.exclude|list[int]` or `Options.eligible|list[int]` should be ignored by event
history implementation, mean not saved at all.

To wrap it up: event history may operate on rather stable session attributes, for now it is `authrole` and `authid`,
all dynamic attributes like `session ID` or maybe other custom attributes in future should lead to ignore storing
such events by event history implementation.
