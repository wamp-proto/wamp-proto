### Event History

#### Feature Definition

Instead of complex QoS for message delivery, a *Broker* may provide *message history*. A *Subscriber* is responsible to handle overlaps (duplicates) when it wants "exactly-once" message processing across restarts.

The *Broker* may allow for configuration on a per-topic basis.

The event history may be transient or persistent message history (surviving *Broker* restarts).

A *Broker* that implements *event history* must (also) announce role `HELLO.roles.callee`, indicate `HELLO.roles.broker.history == 1` and provide the following (builtin) procedures.

A *Caller* can request message history by calling the *Broker* procedure

{align="left"}
        wamp.topic.history.last

with `Arguments = [topic|uri, limit|integer]` where

* `topic` is the topic to retrieve event history for
* `limit` indicates the number of last N events to retrieve

or by calling

{align="left"}
        wamp.topic.history.since

with `Arguments = [topic|uri, timestamp|string]` where

* `topic` is the topic to retrieve event history for
* `timestamp` indicates the UTC timestamp since when to retrieve the events in the ISO-8601 format `yyyy-MM-ddThh:mm:ss:SSSZ` (e.g. `"2013-12-21T13:43:11:000Z"`)

or by calling

{align="left"}
        wamp.topic.history.after

with `Arguments = [topic|uri, publication|id]`

* `topic` is the topic to retrieve event history for
* `publication` is the id of an event which marks the start of the events to retrieve from history


*FIXME*

1. Should we use `topic|uri` or `subscription|id` in `Arguments`?
   - Since we need to be able to get history for pattern-based subscriptions as well, a subscription|id makes more sense: create pattern-based subscription, then get the event history for this.
   - The only restriction then is that we may not get event history without a current subscription covering the events. This is a minor inconvenience at worst.
2. Can `wamp.topic.history.after` be implemented (efficiently) at all?
3. How does that interact with pattern-based subscriptions?
4. The same question as with the subscriber lists applies where: to stay within our separation of roles, we need a broker + a separate peer which implements the callee role. Here we do not have a mechanism to get the history from the broker.


#### Feature Announcement

Support for this feature MUST be announced by *Subscribers* (`role := "subscriber"`) and *Brokers* (`role := "broker"`) via

{align="left"}
        HELLO.Details.roles.<role>.features.event_history|bool := true
