# The Web Application Messaging Protocol
# Part 2: Advanced Features and Aspects

This document specifies version 2 of the [Web Application Messaging Protocol (WAMP)](http://wamp.ws/).

Document Revision: **draft-2**, 2014/02/18

This is part 2 of this document. It describes advanced features and aspects of the protocol and its usage.

This part as a whole is considered partially finished and unstable. Some features are presently underspecified. Features may yet be added or removed, and there is no guarantee that an existing feature in this part will remain unchanged.

Some features, however, are already fully specified and should remain unchanged. These are specifically marked as *STABLE*.


For an introduction to the protocol, and a description of basic features and usage, see part 1 of this document.

**Contents**

1. [Transports](#transports)
   * [WebSocket Transport Modes](#websocket-transport-modes)
2. [Optional Messages](#optional-messages)
    * [Message Definitions](#message-definitions)
    * [Message Codes and Direction](#message-codes-and-direction)
3. [Session Management](#advanced-session-management)
    * [Heartbeats](#heartbeats)
4. [Advanced Publish & Subscribe](#advanced-publish--subscribe)
    * [Subscriber Black- and Whitelisting](#subscriber-black--and-whitelisting)
    * [Publisher Exclusion](#publisher-exclusion)
    * [Publisher Identification](#publisher-identification)
    * [Publication Trust Levels](#publication-trust-levels)
    * [Pattern-based Subscriptions](#pattern-based-subscriptions)
    * [Partitioned Subscriptions & Publications](#partitioned-subscriptions--publications)
    * [Subscriber Meta Events](#subscriber-meta-events)
    * [Subscriber List](#subscriber-list)
    * [Event History](#event-history)
5. [Advanced Remote Procedure Calls](#advanced-remote-procedure-calls)
    * [Callee Black- and Whitelisting](#callee-black--and-whitelisting)
    * [Caller Exclusion](#caller-exclusion)
    * [Caller Identification](#caller-identification)
    * [Call Trust Levels](#call-trust-levels)
    * [Pattern-based Registrations](#pattern-based-registrations)
    * [Partitioned Registrations & Calls](#partitioned-registrations--calls)
    * [Call Timeouts](#call-timeouts)
    * [Canceling Calls](#canceling-calls)
    * [Progressive Call Results](#progressive-call-results)
6. [Authentication](#authentication)
    * [TLS Certificate-based Authentication](#tls-certificate-based-authentication)
    * [HTTP Cookie-based Authentication](#http-cookie-based-authentication)
    * [WAMP Challenge-Response Authentication](#wamp-challenge-response-authentication)
7. [Reflection](#reflection)


## Transports


![alt text](figure/sessions3.png "Transports, Sessions and Peers")


### Other Transports

Besides the WebSocket transport, the following WAMP transports are under development:

 * HTTP 1.0/1.1 long-polling

Here, the bi-directionality requirement for the transport is implemented by using long-polling for the server-side sending of messages.

Other transports such as HTTP 2.0 ("SPDY"), raw TCP or UDP might be defined in the future.


### WebSocket Transport Modes

#### Unbatched Transport

With WebSocket in **unbatched mode**, WAMP messages are transmitted as WebSocket messages: each WAMP message is transmitted as a separate WebSocket message (not WebSocket frame).

The WAMP protocol MUST BE negotiated during the WebSocket opening handshake between peers using the WebSocket subprotocol negotiation mechanism.

WAMPv2 uses the following WebSocket subprotocol identifiers for unbatched modes:

 * `wamp.2.json`
 * `wamp.2.msgpack`

With `wamp.2.json`, *all* WebSocket messages MUST BE of type **text** (UTF8 encoded payload) and use the JSON message serialization.

With `wamp.2.msgpack`, *all* WebSocket messages MUST BE of type **binary** and use the MsgPack message serialization.

#### Batched Transport

WAMPv2 allows to batch one or more WAMP messages into a single WebSocket message if one of the following subprotocols have been negotiated:

 * `wamp.2.json.batched`
 * `wamp.2.msgpack.batched`

Batching with JSON works by serializing each WAMP message to JSON as normally, appending the single ASCII control character `\30` ([record separator](http://en.wikipedia.org/wiki/Record_separator#Field_separators)) byte `0x1e` to *each* serialized messages, and packing a sequence of such serialized messages into a single WebSocket message:

   serialized JSON WAMP Msg 1 | 0x1e | serialized JSON WAMP Msg 2 | 0x1e | ...

Batching with MsgPack works by serializing each WAMP message to MsgPack as normally, prepending a 32 bit unsigned integer (big-endian byte order) with the length of the serialized MsgPack message, and packing a sequence of such serialized (length-prefixed) messages into a single WebSocket message:

   Length of Msg 1 serialization (int32) | serialized MsgPack WAMP Msg 1 | ...

With batched transport, even if only a single WAMP message is sent in a WebSocket message, the (single) WAMP message needs to be framed as described above. In other words, a single WAMP message is sent as a batch of length 1.

Sending a batch of length 0 (no WAMP message) is illegal and a peer MUST fail the transport upon receiving such a transport message.




## Optional Messages

Optional messages are WAMP messages wuht a structure as described in part one of this document.

### Message Definitions

WAMP defines the following OPTIONAL messages which are explained in detail in the following sections.

#### `CHALLENGE`

    [CHALLENGE, Challenge|string, Extra|dict]

#### `AUTHENTICATE`

    [AUTHENTICATE, Signature|string, Extra|dict]

#### `HEARTBEAT`

    [HEARTBEAT, IncomingSeq|integer, OutgoingSeq|integer
    [HEARTBEAT, IncomingSeq|integer, OutgoingSeq|integer, Discard|string]

#### `CANCEL`

    [CANCEL, CALL.Request|id, Options|dict]

#### `INTERRUPT`

    [INTERRUPT, INVOCATION.Request|id, Options|dict]


### Message Codes and Direction

The following table list the message type code for **the OPTIONAL messages** defined in this part of the document and their direction between peer roles.

"Tx" means the message is sent by the respective role, and "Rx" means the message is received by the respective role.

| Code | Message        ||  Publisher  |  Broker  |  Subscriber  ||  Caller  |  Dealer  |  Callee  |
|------|----------------||-------------|----------|--------------||----------|----------|----------|
|  3   | `CHALLENGE`    || Rx          | Tx       | Rx           || Rx       | Tx       | Rx       |
|  4   | `AUTHENTICATE` || Tx          | Rx       | Tx           || Tx       | Rx       | Tx       |
|  6   | `HEARTBEAT`    || Tx/Rx       | Tx/Rx    | Tx/Rx        || Tx/Rx    | Tx/Rx    | Tx/Rx    |
| 49   | `CANCEL`       ||             |          |              || Tx       | Rx       |          |
| 69   | `INTERRUPT`    ||             |          |              ||          | Tx       | Rx       |


## Session Management

### Session Establishment

The message flow between *Endpoints* and *Routers* for establishing and tearing down sessions MAY involve the following messages which authenticate a session:

1. `CHALLENGE`
2. `AUTHENTICATE`

![alt text](figure/hello_authenticated.png "WAMP Session denied")


#### CHALLENGE

An authentication MAY be required for the establishment of a session. Such requirement may be based on the `Realm` the connection is requested for.

To request authentication, the *Router* sends a `CHALLENGE` message to the *Endpoint*.

    [CHALLENGE, Challenge|string, Extra|dict]

* `Challenge` ---- ???? ----
* `Extra` is a dictionary ---- ???? ----

#### AUTHENTICATE

In response to a `CHALLENGE` message, an *Endpoint* MUST send an `AUTHENTICATION` message.

    [AUTHENTICATE, Signature|string, Extra|dict]


## Advanced Session Management

### HEARTBEAT

The heartbeat allows to keep network intermediaries from closing the underlying transport, notify the peer up to which incoming heartbeat all incoming WAMP messages have been processed, and announce an outgoing hearbeat sequence number in the same message.

A peer MAY send a `HEARTBEAT` message at any time:

    [HEARTBEAT, IncomingSeq|integer, OutgoingSeq|integer]

or

    [HEARTBEAT, IncomingSeq|integer, OutgoingSeq|integer, Discard|string]

 * `HEARTBEAT.OutgoingSeq` MUST start with `1` and be incremented by `1` for each `HEARTBEAT` a peer sends.
 * `HEARTBEAT.IncomingSeq` MUST BE the sequence number from the last received heartbeat for which all previously received WAMP messages have been processed or `0` when no `HEARTBEAT` has yet been received
 *  `HEARTBEAT.Discard` is an arbitrary string discarded by the peer.

> The `HEARTBEAT.Discard` can be used to add some traffic volume to the HEARTBEAT message e.g. to keep mobile radio channels in a low-latency, high-power state. The string SHOULD be a random string (otherwise compressing transports might compress away the traffic volume).
>

*Example*

   [3, 0, 1]

*Example*

   [3, 23, 5]

*Example*

   [3, 23, 5, "throw me away ... I am just noise"]

Incoming heartbeats are not required to be answered by an outgoing heartbeat. Sending of hearbeats is under independent control with each peer.


## Advanced Features

In addition to the *basic features* definded in the first part of this document, RPCs and PubSub calls can offer *advanced features*.

*Advanced features* need to be announced by the peer which implements them.

*Example: An Endpoint implementing the roles of Publisher and Subscriber and implementing some advanced features on the Publisher.*

   [1, 9129137332, {
      "roles": {
         "publisher": {
            "features": {
               "publisher_exclusion":     true,
               "publisher_identication":  true
            }
         },
         "subscriber": {

         }
      }
   }]

*Example: A Router implementing the role of Broker and supporting all advanced features.*

   [1, 9129137332, {
      "roles": {
         "broker": {
            "features": {
               "subscriber_blackwhite_listing": true,
               "publisher_exclusion":           true,
               "publisher_identification":      true,
               "publication_trustlevels":       true,
               "pattern_based_subscription":    true,
               "partitioned_pubsub":            true,
               "subscriber_metaevents":         true,
               "subscriber_list":               true,
               "event_history":                 true
            }
         }
   }]

*Feature Announcemenet and Advanced Features*

The use of *feature announcement* in WAMP allows for

 * only implementing subsets of functionality
 * graceful degration


The complete list of *advanced features* currently defined per role is:

| Feature                       |  Publisher  |  Broker  |  Subscriber  |  Caller  |  Dealer  |  Callee  |
|-------------------------------|-------------|----------|--------------|----------|----------|----------|
| **Remote Procedure Calls**    |             |          |              |          |          |          |
| callee_blackwhite_listing     |             |          |              | X        | X        |          |
| caller_exclusion              |             |          |              | X        | X        |          |
| caller_identification         |             |          |              | X        | X        | X        |
| call_trustlevels              |             |          |              |          | X        | X        |
| pattern_based_registration    |             |          |              |          | X        | X        |
| partitioned_rpc               |             |          |              | X        | X        | X        |
| call_timeout                  |             |          |              | X        | X        | X        |
| call_canceling                |             |          |              | X        | X        | X        |
| progressive_call_results      |             |          |              | X        | X        | X        |
|                               |             |          |              |          |          |          |
| **Publish & Subscribe**       |             |          |              |          |          |          |
| subscriber_blackwhite_listing | X           | X        |              |          |          |          |
| publisher_exclusion           | X           | X        |              |          |          |          |
| publisher_identification      | X           | X        | X            |          |          |          |
| publication_trustlevels       |             | X        | X            |          |          |          |
| pattern_based_subscription    |             | X        | X            |          |          |          |
| partitioned_pubsub            | X           | X        | X            |          |          |          |
| subscriber_metaevents         |             | X        | X            |          |          |          |
| subscriber_list               |             | X        | X            |          |          |          |
| event_history                 |             | X        | X            |          |          |          |

*Network Agent*

When a software agent operates in a network protocol, it often identifies itself, its application type, operating system, software vendor, or software revision, by submitting a characteristic identification string to its operating peer.

Similar to what browsers do with the `User-Agent` HTTP header, both the `HELLO` and the `WELCOME` message MAY disclose the WAMP implementation in use to its peer:

   HELLO.Details.agent|string

   WELCOME.Details.agent|string

*Example*

   [1, 9129137332, {
         "agent": "AutobahnPython-0.7.0",
         "roles": {
            "publisher": {}
         }
   }]




## Advanced Publish & Subscribe

All of the following advanced features for Publish & Subscribe are optional.

If a WAMP implementation supports a specific advanced feature, it should announce support in the initial `HELLO` message:

   HELLO.Details.roles.<role>.features.<feature>|bool := true

Otherwise, the feature is assumed to be unsupported.


### Subscriber Black- and Whitelisting

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

    [16, 239714735, {"exclude": [7891255], "eligible": [7891255, 1245751, 9912315]},
      "com.myapp.mytopic1", ["Hello, world!"]]

The above event will get dispatched to WAMP sessions with IDs `1245751` or `9912315` only (since `7891255` is excluded) - but only if those are subscribed to the topic `com.myapp.mytopic1`.


### Publisher Exclusion

Support for this feature MUST be announced by *Publishers* (`role := "publisher"`) and *Brokers* (`role := "broker"`) via

   HELLO.Details.roles.<role>.features.publisher_exclusion|bool := true

By default, a *Publisher* of an event will **not** itself receive an event published, even when subscribed to the `Topic` the *Publisher* is publishing to. This behavior can be overridden via

   PUBLISH.Options.exclude_me|bool

When publishing with `PUBLISH.Options.exclude_me := false`, the *Publisher* of the event will receive that event, if it is subscribed to the `Topic` published to.

*Example*

    [16, 239714735, {"exclude_me": false}, "com.myapp.mytopic1", ["Hello, world!"]]

In this example, the *Publisher* will receive the published event, if it is subscribed to `com.myapp.mytopic1`.


### Publisher Identification

Support for this feature MUST be announced by *Publishers* (`role := "publisher"`), *Brokers* (`role := "broker"`) and *Subscribers* (`role := "subscriber"`) via

   HELLO.Details.roles.<role>.features.publisher_identification|bool := true

A *Publisher* may request the disclosure of its identity (its WAMP session ID) to receivers of a published event by setting

   PUBLISH.Options.disclose_me|bool := true

*Example*

    [16, 239714735, {"disclose_me": true}, "com.myapp.mytopic1", ["Hello, world!"]]

If above event is published by a *Publisher* with WAMP session ID `3335656`, the *Broker* would send an `EVENT` message to *Subscribers* with the *Publisher's* WAMP session ID in `EVENT.Details.publisher`:

*Example*

   [36, 5512315355, 4429313566, {"publisher": 3335656}, ["Hello, world!"]]

Note that a *Broker* may deny a *Publisher's* request to disclose its identity:

*Example*

    [4, 239714735, {}, "wamp.error.disclose_me.not_allowed"]

A *Broker* may also (automatically) disclose the identity of a *Publisher* even without the *Publisher* having explicitly requested to do so when the *Broker* configuration (for the publication topic) is set up to do so.


### Publication Trust Levels

Support for this feature MUST be announced by *Subscribers* (`role := "subscriber"`) and *Brokers* (`role := "broker"`) via

   HELLO.Details.roles.<role>.features.publication_trustlevels|bool := true

A *Broker* may be configured to automatically assign *trust levels* to events published by *Publishers* according to the *Broker* configuration on a per-topic basis and/or depending on the application defined role of the (authenticated) *Publisher*.

A *Broker* supporting trust level will provide

   EVENT.Details.trustlevel|integer

in an `EVENT` message sent to a *Subscriber*. The trustlevel `0` means lowest trust, and higher integers represent (application-defined) higher levels of trust.

*Example*

   [36, 5512315355, 4429313566, {"trustlevel": 2}, ["Hello, world!"]]

In above event, the *Broker* has (by configuration and/or other information) deemed the event publication to be of trustlevel `2`.


### Pattern-based Subscriptions

Support for this feature MUST be announced by *Subscribers* (`role := "subscriber"`) and *Brokers* (`role := "broker"`) via

   HELLO.Details.roles.<role>.features.pattern_based_subscription|bool := true

By default, *Subscribers* subscribe to topics with **exact matching policy**. That is an event will only be dispatched to a *Subscriber* by the *Broker* if the topic published to (`PUBLISH.Topic`) *exactly* matches the topic subscribed to (`SUBSCRIBE.Topic`).

A *Subscriber* might want to subscribe to topics based on a *pattern*. This can be useful to reduce the number of individual subscriptions to be set up and to subscribe to topics the *Subscriber* is not aware of at the time of subscription, or which do not yet exist at this time.

If the *Broker* and the *Subscriber* support **pattern-based subscriptions**, this matching can happen by

 * prefix-matching policy
 * wildcard-matching policy

*Brokers* and *Subscribers* MUST announce support for non-exact matching policies in the `HELLO.Options` (see that chapter).

#### Prefix Matching

A *Subscriber* requests **prefix-matching policy** with a subscription request by setting

   SUBSCRIBE.Options.match|string := "prefix"

*Example*

   [32, 912873614, {"match": "prefix"}, "com.myapp.topic.emergency"]

When a **prefix-matching policy** is in place, any event with a topic that has `SUBSCRIBE.Topic` as a *prefix* will match the subscription, and potentially be delivered to *Subscribers* on the subscription.

In the above example, events with `PUBLISH.Topic`

 * `com.myapp.topic.emergency.11`
 * `com.myapp.topic.emergency-low`
 * `com.myapp.topic.emergency.category.severe`
 * `com.myapp.topic.emergency`

will all apply for dispatching. An event with `PUBLISH.Topic` e.g. `com.myapp.topic.emerge` will not apply.

The *Broker* will apply the prefix-matching based on the UTF-8 encoded byte string for the `PUBLISH.Topic` and the `SUBSCRIBE.Topic`.

#### Wildcard Matching

A *Subscriber* requests **wildcard-matching policy** with a subscription request by setting

   SUBSCRIBE.Options.match|string := "wildcard"

Wildcard-matching allows to provide wildcards for **whole** URI components.

*Example*

   [32, 912873614, {"match": "wildcard"}, "com.myapp..userevent"]

In above subscription request, the 3rd URI component is empty, which signals a wildcard in that URI component position. In this example, events with `PUBLISH.Topic`

 * `com.myapp.foo.userevent`
 * `com.myapp.bar.userevent`
 * `com.myapp.a12.userevent`

will all apply for dispatching. Events with `PUBLISH.Topic`

 * `com.myapp.foo.userevent.bar`
 * `com.myapp.foo.user`
 * `com.myapp2.foo.userevent`

will not apply for dispatching.

#### General

When a single event matches more than one of a *Subscriber's* subscriptions, the event will be delivered for each subscription. The *Subscriber* can detect the delivery of that same event on multiple subscriptions via `EVENT.PUBLISHED.Publication`, which will be identical.

Since each *Subscriber's* subscription "stands on its own", there is no *set semantics* implied by pattern-based subscriptions. E.g. a *Subscriber* cannot subscribe to a broad pattern, and then unsubscribe from a subset of that broad pattern to form a more complex subscription. Each subscription is separate.

If a subscription was established with a pattern-based matching policy, a *Broker* MUST supply the original `PUBLISH.Topic` as provided by the *Publisher* in

   EVENT.Details.topic|uri

to the *Subscribers*.

*Example*

   [36, 5512315355, 4429313566, {"topic": "com.myapp.topic.emergency.category.severe" }, ["Hello, world!"]]


### Partitioned Subscriptions & Publications

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


### Subscriber Meta Events

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


### Subscriber List

A *Broker* may allow to retrieve the current list of *Subscribers* for a given subscription.

Support for this feature MUST be announced by *Subscribers* (`role := "subscriber"`) and *Brokers* (`role := "broker"`) via

   HELLO.Details.roles.<role>.features.subscriber_list|bool := true

A *Broker* that implements *subscriber list* must (also) announce role `HELLO.roles.callee` and provide the following (built in) procedures.

A *Caller* (that is also a *Subscriber*) can request the current list of subscribers for a subscription (it is subscribed to) by calling the *Broker* procedure

   wamp.broker.subscriber.list

with `Arguments = [subscription|id]` where

 * `subscription` is the ID of the subscription as returned from `SUBSCRIBED.Subscription`

and `Result = sessions|list` where

 * `sessions` is a list of WAMP session IDs currently subscribed to the given subscription.

A call to `wamp.broker.subscriber.list` may fail with

   wamp.error.no_such_subscription
   wamp.error.not_authorized

**Open Issues**

 1. What if we have multiple *Brokers* (a cluster)? The call would need to be forwarded.
 2. Should we allow "paging" (`offset|integer` and `limit|integer` arguments)?
 3. Should we allow *Subscribers* to list subscribers for subscription it is not itself subscribed to? How would the *Callee* know the subscription ID it wants to look up without subscribing?
 4. Why retrieve the list for a subscription ID, when the interest may lie in how many subscribers there are to a topic, e.g. if a publisher wants to judge its current reach?
 5. The *Router* needs to implement a *Dealer* role as well in order to be able to route the RPC, since calls can only be addressed to *Dealers*.
 6. We should probably then also have a *Callee* as a separate peer. Otherwise we break the rule that peers can implement Broker/Dealer OR Caller/Callee/Subscriber/Publisher roles.
 7. If we have the separate *Callee*, then how does this get the list? One way would be using subscription meta-events.


### Event History

Support for this feature MUST be announced by *Subscribers* (`role := "subscriber"`) and *Brokers* (`role := "broker"`) via

   HELLO.Details.roles.<role>.features.event_history|bool := true

Instead of complex QoS for message delivery, a *Broker* may provide *message history*. A *Subscriber* is responsible to handle overlaps (duplicates) when it wants "exactly-once" message processing across restarts.

The *Broker* may allow for configuration on a per-topic basis.

The event history may be transient or persistent message history (surviving *Broker* restarts).

A *Broker* that implements *event history* must (also) announce role `HELLO.roles.callee`, indicate `HELLO.roles.broker.history == 1` and provide the following (builtin) procedures.

A *Caller* can request message history by calling the *Broker* procedure

   wamp.topic.history.last

with `Arguments = [topic|uri, limit|integer]` where

 * `topic` is the topic to retrieve event history for
 * `limit` indicates the number of last N events to retrieve

or by calling

   wamp.topic.history.since

with `Arguments = [topic|uri, timestamp|string]` where

 * `topic` is the topic to retrieve event history for
 * `timestamp` indicates the UTC timestamp since when to retrieve the events in the ISO-8601 format `yyyy-MM-ddThh:mm:ss:SSSZ` (e.g. `"2013-12-21T13:43:11:000Z"`)

or by calling

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






## Advanced Remote Procedure Calls

All of the following advanced features for Remote Procedure Calls are optional.

If a WAMP implementation supports a specific advanced feature, it should announce support in the initial `HELLO` message:

   HELLO.Details.roles.<role>.features.<feature>|bool := true

Otherwise, the feature is assumed to be unsupported.


### Callee Black- and Whitelisting

Support for this feature MUST be announced by *Callers* (`role := "caller"`) and *Dealers* (`role := "dealer"`) via

   HELLO.Details.roles.<role>.features.callee_blackwhite_listing|bool := true


A *Caller* may restrict the endpoints that will handle a call beyond those registered via

 * `CALL.Options.exclude|list`
 * `CALL.Options.eligible|list`

`CALL.Options.exclude` is a list of WAMP session IDs (`integer`s) providing an explicit list of (potential) *Callees* that a call won't be forwarded to, even though they might be registered. In other words, `CALL.Options.exclude` is a blacklist of (potential) *Callees*.

`CALL.Options.eligible` is a list of WAMP session IDs (`integer`s) providing an explicit list of (potential) *Callees* that are (potentially) forwarded the call issued. In other words, `CALL.Options.eligible` is a whitelist of (potential) *Callees*.

The *Dealer* will forward a call only to registered *Callees* that are not explicitly excluded via `CALL.Options.exclude` **and** which are explicitly eligible via `CALL.Options.eligible`.

*Example*

   [48, 7814135, {"exclude": [7891255, 1245751]}, "com.myapp.echo", ["Hello, world!"]]

The above call will (potentially) get forwarded to all *Callees* of `com.myapp.echo`, but not WAMP sessions with IDs `7891255` or `1245751` (and also not the calling session).

*Example*

   [48, 7814135, {"eligible": [7891255, 1245751]}, "com.myapp.echo", ["Hello, world!"]]

The above call will (potentially) get forwarded to WAMP sessions with IDs `7891255` or `1245751` only - but only if those are registered for the procedure `com.myapp.echo`.

*Example*

   [48, 7814135, {"exclude": [7891255], "eligible": [7891255, 1245751, 9912315]},
      "com.myapp.echo", ["Hello, world!"]]

The above call will (potentially) get forwarded to WAMP sessions with IDs `1245751` or `9912315` only (since `7891255` is excluded) - but only if those are registered for the procedure `com.myapp.echo`.


### Caller Exclusion

Support for this feature MUST be announced by *Callers* (`role := "caller"`) and *Dealers* (`role := "dealer"`) via

   HELLO.Details.roles.<role>.features.caller_exclusion|bool := true


By default, a *Caller* of a procedure will **never** itself be forwarded the call issued, even when registered for the `Procedure` the *Caller* is publishing to. This behavior can be overridden via

   CALL.Options.exclude_me|bool

When calling with `CALL.Options.exclude_me := false`, the *Caller* of the procedure might be forwarded the call issued - if it is registered for the `Procedure` called.

*Example*

   [48, 7814135, {"exclude_me": false}, "com.myapp.echo", ["Hello, world!"]]

In this example, the *Caller* might be forwarded the call issued, if it is registered for `com.myapp.echo`.


### Caller Identification

Support for this feature MUST be announced by *Callers* (`role := "caller"`), *Callees* (`role := "callee"`) and *Dealers* (`role := "dealer"`) via

   HELLO.Details.roles.<role>.features.caller_identification|bool := true


A *Caller* MAY **request** the disclosure of its identity (its WAMP session ID) to endpoints of a routed call via

   CALL.Options.disclose_me|bool := true

*Example*

   [48, 7814135, {"disclose_me": true}, "com.myapp.echo", ["Hello, world!"]]

If above call is issued by a *Caller* with WAMP session ID `3335656`, the *Dealer* sends an `INVOCATION` message to *Callee* with the *Caller's* WAMP session ID in `INVOCATION.Details.caller`:

*Example*

   [68, 6131533, 9823526, {"caller": 3335656}, ["Hello, world!"]]

Note that a *Dealer* MAY disclose the identity of a *Caller* even without the *Caller* having explicitly requested to do so when the *Dealer* configuration (for the called procedure) is setup to do so.

A *Dealer* MAY deny a *Caller's* request to disclose its identity:

*Example*

    [4, 7814135, "wamp.error.disclose_me.not_allowed"]


### Call Trust Levels

Support for this feature MUST be announced by *Callees* (`role := "callee"`) and *Dealers* (`role := "dealer"`) via

   HELLO.Details.roles.<role>.features.call_trustlevels|bool := true


A *Dealer* may be configured to automatically assign *trust levels* to calls issued by *Callers* according to the *Dealer* configuration on a per-procedure basis and/or depending on the application defined role of the (authenticated) *Caller*.

A *Dealer* supporting trust level will provide

   INVOCATION.Details.trustlevel|integer

in an `INVOCATION` message sent to a *Callee*. The trustlevel `0` means lowest trust, and higher integers represent (application-defined) higher levels of trust.

*Example*

   [68, 6131533, 9823526, {"trustlevel": 2}, ["Hello, world!"]]

In above event, the *Dealer* has (by configuration and/or other information) deemed the call (and hence the invocation) to be of trustlevel `2`.


### Pattern-based Registrations

Support for this feature MUST be announced by *Callees* (`role := "callee"`) and *Dealers* (`role := "dealer"`) via

   HELLO.Details.roles.<role>.features.pattern_based_registration|bool := true


By default, *Callees* register procedures with **exact matching policy**. That is a call will only be routed to a *Callee* by the *Dealer* if the procedure called (`CALL.Procedure`) *exactly* matches the endpoint registered (`REGISTER.Procedure`).

A *Callee* might want to register procedures based on a *pattern*. This can be useful to reduce the number of individual registrations to be set up.

If the *Dealer* and the *Callee* support **pattern-based registrations**, this matching can happen by

 * prefix-matching policy
 * wildcard-matching policy

*Dealers* and *Callees* MUST announce support for non-exact matching policies in the `HELLO.Options` (see that chapter).

#### Prefix Matching

A *Callee* requests **prefix-matching policy** with a registration request by setting

   REGISTER.Options.match|string := "prefix"

*Example*

   [64, 612352435, {"match": "prefix"}, "com.myapp.myobject1"]

When a **prefix-matching policy** is in place, any call with a procedure that has `REGISTER.Procedure` as a *prefix* will match the registration, and potentially be routed to *Callees* on that registration.

In above example, the following calls with `CALL.Procedure`

 * `com.myapp.myobject1.myprocedure1`
 * `com.myapp.myobject1-mysubobject1`
 * `com.myapp.myobject1.mysubobject1.myprocedure1`
 * `com.myapp.myobject1`

will all apply for call routing. A call with one of the following `CALL.Procedure`

 * `com.myapp.myobject2`
 * `com.myapp.myobject`

will not apply.

The *Dealer* will apply the prefix-matching based on the UTF-8 encoded byte string for the `CALL.Procedure` and the `REGISTER.Procedure`.

#### Wildcard Matching

A *Callee* requests **wildcard-matching policy** with a registration request by setting

   REGISTER.Options.match|string := "wildcard"

Wildcard-matching allows to provide wildcards for **whole** URI components.

*Example*

   [64, 612352435, {"match": "wildcard"}, "com.myapp..myprocedure1"]

In the above registration request, the 3rd URI component is empty, which signals a wildcard in that URI component position. In this example, calls with `CALL.Procedure` e.g.

 * `com.myapp.myobject1.myprocedure1`
 * `com.myapp.myobject2.myprocedure1`

will all apply for call routing. Calls with `CALL.Procedure` e.g.

 * `com.myapp.myobject1.myprocedure1.mysubprocedure1`
 * `com.myapp.myobject1.myprocedure2`
 * `com.myapp2.myobject1.myprocedure1`

will not apply for call routing.

When a single call matches more than one of a *Callees* registrations, the call MAY be routed for invocation on multiple registrations, depending on call settings.

--------------
FIXME: The *Callee* can detect the invocation of that same call on multiple registrations via `INVOCATION.CALL.Request`, which will be identical.

Since each *Callees* registrations "stands on it's own", there is no *set semantics* implied by pattern-based registrations. E.g. a *Callee* cannot register to a broad pattern, and then unregister from a subset of that broad pattern to form a more complex registration. Each registration is separate.

If an endpoint was registered with a pattern-based matching policy, a *Dealer* MUST supply the original `CALL.Procedure` as provided by the *Caller* in `INVOCATION.Details.procedure` to the *Callee*.


### Partitioned Registrations & Calls

Support for this feature MUST be announced by *Callers* (`role := "caller"`), *Callees* (`role := "callee"`) and *Dealers* (`role := "dealer"`) via

   HELLO.Details.roles.<role>.features.partitioned_rpc|bool := true


*Partitioned Calls* allows to run a call issued by a *Caller* on one or more endpoints implementing the called procedure.

* all
* any
* partition


`CALL.Options.runon|string := "all" or "any" or "partition"`
`CALL.Options.runmode|string := "gather" or "progressive"`
`CALL.Options.rkey|string`


#### "Any" Calls

If `CALL.Options.runon == "any"`, the call will be routed to one *randomly* selected *Callee* that registered an implementing endpoint for the called procedure. The call will then proceed as for standard (non-distributed) calls.


#### "All" Calls

If `CALL.Options.runon == "all"`, the call will be routed to all *Callees* that registered an implementing endpoint for the called procedure. The calls will run in parallel and asynchronously.

If `CALL.Options.runmode == "gather"` (the default, when `CALL.Options.runmode` is missing), the *Dealer* will gather the individual results received via `YIELD` messages from *Callees* into a single list, and return that in `RESULT` to the original *Caller* - when all results have been received.

If `CALL.Options.runmode == "progressive"`, the *Dealer* will call each endpoint via a standard `INVOCATION` message and immediately forward individual results received via `YIELD` messages from the *Callees* as progressive `RESULT` messages (`RESULT.Details.progress == 1`) to the original *Caller* and send a final `RESULT` message (with empty result) when all individual results have been received.

If any of the individual `INVOCATION`s returns an `ERROR`, the further behavior depends on ..

Fail immediate:

The *Dealer* will immediately return a `ERROR` message to the *Caller* with the error from the `ERROR` message of the respective failing invocation. It will further send `INTERRUPT` messages to all *Callees* for which it not yet has received a response, and ignore any `YIELD` or `ERROR` messages it might receive subsequently for the pending invocations.

The *Dealer* will accumulate ..


#### "Partitioned" Calls

If `CALL.Options.runmode == "partition"`, then `CALL.Options.rkey` MUST be present.

The call is then routed to all endpoints that were registered ..

The call is then processed as for "All" Calls.


### Call Timeouts

Support for this feature MUST be announced by *Callers* (`role := "caller"`), *Callees* (`role := "callee"`) and *Dealers* (`role := "dealer"`) via

   HELLO.Details.roles.<role>.features.call_timeout|bool := true

A *Caller* might want to issue a call providing a *timeout* for the call to finish.

A *timeout* allows to **automatically** cancel a call after a specified time either at the *Callee* or at the *Dealer*.

A *Callee* specifies a timeout by providing

   CALL.Options.timeout|integer

in ms. A timeout value of `0` deactivates automatic call timeout. This is also the default value.

The timeout option is a companion to, but slightly different from the `CANCEL` and `INTERRUPT` messages that allow a *Caller* and *Dealer* to **actively** cancel a call or invocation.

In fact, a timeout timer might run at three places:

 * *Caller*
 * *Dealer*
 * *Callee*


### Canceling Calls

Support for this feature MUST be announced by *Callers* (`role := "caller"`), *Callees* (`role := "callee"`) and *Dealers* (`role := "dealer"`) via

   HELLO.Details.roles.<role>.features.call_canceling|bool := true


A *Caller* might want to actively cancel a call that was issued, but not has yet returned. An example where this is useful could be a user triggering a long running operation and later changing his mind or no longer willing to wait.

The message flow between *Callers*, a *Dealer* and *Callees* for canceling remote procedure calls involves the following messages:

 * `CANCEL`
 * `INTERRUPT`

A call may be cancelled at the *Callee*

![alt text](figure/rpc_cancel1.png "RPC Message Flow: Calls")

A call may be cancelled at the *Dealer*

![alt text](figure/rpc_cancel2.png "RPC Message Flow: Calls")

A *Callee* cancels an remote procedure call initiated (but not yet finished) by sending a `CANCEL` message to the *Dealer*:

    [CANCEL, CALL.Request|id, Options|dict]

A *Dealer* cancels an invocation of an endpoint initiated (but not yet finished) by sending a `INTERRUPT` message to the *Callee*:

    [INTERRUPT, INVOCATION.Request|id, Options|dict]

Options:

   CANCEL.Options.mode|string == "skip" | "kill" | "killnowait"


### Progressive Call Results

Support for this advanced feature MUST be announced by *Callers* (`role := "caller"`), *Callees* (`role := "callee"`) and *Dealers* (`role := "dealer"`) via

   HELLO.Details.roles.<role>.features.progressive_call_results|bool := true


A procedure implemented by a *Callee* and registered at a *Dealer* may produce progressive results (incrementally). The message flow for progressive results involves:

![alt text](figure/rpc_progress1.png "RPC Message Flow: Calls")


A *Caller* indicates it's willingness to receive progressive results by setting

   CALL.Options.receive_progress|bool := true

*Example.* Caller-to-Dealer `CALL`

   [48, 77133, {"receive_progress": true}, "com.myapp.compute_revenue", [2010, 2011, 2012]]

If the *Callee* supports progressive calls, the *Dealer* will forward the *Caller's* willingness to receive progressive results by setting

   INVOCATION.Options.receive_progress|bool := true

*Example.* Dealer-to-Callee `INVOCATION`

   [68, 87683, 324, {"receive_progress": true}, [2010, 2011, 2012]]

An endpoint implementing the procedure produces progressive results by sending `YIELD` messages to the *Dealer* with

   YIELD.Options.progress|bool := true

*Example.* Callee-to-Dealer progressive `YIELDs`

   [70, 87683, {"progress": true}, ["Y2010", 120]]
   [70, 87683, {"progress": true}, ["Y2011", 205]]
   ...

Upon receiving an `YIELD` message from a *Callee* with `YIELD.Options.progress == true` (for a call that is still ongoing), the *Dealer* will **immediately** send a `RESULT` message to the original *Caller* with

   RESULT.Details.progress|bool := true

*Example.* Dealer-to-Caller progressive `RESULTs`

   [50, 77133, {"progress": true}, ["Y2010", 120]]
   [50, 77133, {"progress": true}, ["Y2011", 205]]
   ...

An invocation MUST *always* end in either a *normal* `RESULT` or `ERROR` message being sent by the *Callee* and received by the *Dealer*.

*Example.* Callee-to-Dealer final `YIELD`

   [70, 87683, {}, ["Total", 490]]

*Example.* Callee-to-Dealer final `ERROR`

   [4, 87683, {}, "com.myapp.invalid_revenue_year", [1830]]

A call MUST *always* end in either a *normal* `RESULT` or `ERROR` message being sent by the *Dealer* and received by the *Caller*.

*Example.* Dealer-to-Caller final `RESULT`

   [50, 77133, {}, ["Total", 490]]

*Example.* Dealer-to-Caller final `ERROR`

   [4, 77133, {}, "com.myapp.invalid_revenue_year", [1830]]

In other words: `YIELD` with `YIELD.Options.progress == true` and `RESULT` with `RESULT.Details.progress == true` messages may only be sent *during* a call or invocation is still ongoing.

The final `YIELD` and final `RESULT` may also be empty, e.g. when all actual results have already been transmitted in progressive result messages.

*Example.* Callee-to-Dealer `YIELDs`

   [70, 87683, {"progress": true}, ["Y2010", 120]]
   [70, 87683, {"progress": true}, ["Y2011", 205]]
    ...
   [70, 87683, {"progress": true}, ["Total", 490]]
   [70, 87683, {}]

*Example.* Dealer-to-Caller `RESULTs`

   [50, 77133, {"progress": true}, ["Y2010", 120]]
   [50, 77133, {"progress": true}, ["Y2011", 205]]
    ...
   [50, 77133, {"progress": true}, ["Total", 490]]
   [50, 77133, {}]

The progressive `YIELD` and progressive `RESULT` may also be empty, e.g. when those messages are only used to signal that the procedure is still running and working, and the actual result is completely delivered in the final `YIELD` and `RESULT`:

*Example.* Callee-to-Dealer `YIELDs`

   [70, 87683, {"progress": true}]
   [70, 87683, {"progress": true}]
   ...
   [70, 87683, {}, [["Y2010", 120], ["Y2011", 205], ..., ["Total", 490]]]

*Example.* Dealer-to-Caller `RESULTs`

   [50, 77133, {"progress": true}]
   [50, 77133, {"progress": true}]
   ...
   [50, 77133, {}, [["Y2010", 120], ["Y2011", 205], ..., ["Total", 490]]]

Note that intermediate, progressive results and/or the final result MAY have different structure. The WAMP peer implementation is responsible for mapping everything into a form suitable for consumption in the host language.

*Example.* Callee-to-Dealer `YIELDs`

   [70, 87683, {"progress": true}, ["partial 1", 10]]
   [70, 87683, {"progress": true}, [], {"foo": 10, "bar": "partial 1"}]
    ...
   [70, 87683, {}, [1, 2, 3], {"moo": "hello"}]

*Example.* Dealer-to-Caller `RESULTs`

   [50, 77133, {"progress": true}, ["partial 1", 10]]
   [50, 77133, {"progress": true}, [], {"foo": 10, "bar": "partial 1"}]
    ...
   [50, 77133, {}, [1, 2, 3], {"moo": "hello"}]

Even if a *Caller* has indicated it's expectation to receive progressive results by setting `CALL.Options.receive_progress|bool := true`, a *Callee* is **not required** to produce progressive results. `CALL.Options.receive_progress` and `INVOCATION.Options.receive_progress` are simply indications that the *Callee* is prepared to process progressive results, should there be any produced. In other words, *Callees* are free to ignore such `receive_progress` hints at any time.

<!--

**Errors**


If a *Caller* has not indicated support for progressive results or has sent a `CALL` to the *Dealer* without setting `CALL.Options.receive_progress == true`, and the *Dealer* sends a progressive `RESULT`, the *Caller* MUST fail the complete session with the *Dealer*.

If a *Dealer* has not indicated support for progressive results or the *Dealer* has sent an `INVOCATION` to the *Callee* without setting `INVOCATION.Options.receive_progress == true`, and the *Callee* sends a progressive `YIELD`, the *Dealer* MUST fail the call with error

   wamp.error.unexpected_progress_in_yield

If a *Caller* has not indicated support for progressive results and sends a `CALL` to the *Dealer* while setting `CALL.Options.receive_progress == true`, the *Dealer* MUST fail the call

However, if a *Caller* has *not* indicated it's willingness to receive progressive results in a call, the *Dealer* MUST NOT send progressive `RESULTs`, and a *Callee* MUST NOT produce progressive `YIELDs`.

A *Dealer* that does not support progressive calls MUST ignore any option `CALL.Options.receive_progress` received by a *Caller*, and **not** forward the option to the *Callee*.



If a *Callee* that has not indicated support for progressive results and the *Dealer* sends an `INVOCATION` with `INVOCATION.Options.receive_progress == true


A *Callee* that does not support progressive results SHOULD ignore any `INVOCATION.Options.receive_progress` flag.

If a *Dealer* has not indicated support for progressive results, and it receives a `CALL` from a *Caller* with `CALL.Options.receive_progress == true`, the *Dealer* MUST fail the call with error

   wamp.error.unsupported_feature.dealer.progressive_call_result



*Example.* Dealer-to-Caller `ERROR`

   [4, 87683, {}, "wamp.error.unsupported_feature.dealer.progressive_call_result"]



If the *Caller* does not support receiving *progressive calls*, as indicated by

   HELLO.Details.roles.caller.features.progressive_call_results == false

and *Dealer* receives a `YIELD` message from the *Callee* with `YIELD.Options.progress == true`, the *Dealer* MUST fail the call.

*Example.* Callee-to-Dealer `YIELD`

   [70, 87683, {"progress": true}, ["partial 1", 10]]

*Example.* Dealer-to-Caller `ERROR`

   [4, 87683, {}, "wamp.error.unsupported_feature.caller.progressive_call_result"]

If the *Dealer* does not support processing *progressive invocations*, as indicated by

   HELLO.Details.roles.dealer.features.progressive_call_results == false

and *Dealer* receives a `YIELD` message from the *Callee* with `YIELD.Options.progress == true`, the *Dealer* MUST fail the call.

*Example.* Callee-to-Dealer `YIELD`

   [70, 87683, {"progress": true}, ["partial 1", 10]]

*Example.* Dealer-to-Caller `ERROR`

   [4, 87683, {}, "wamp.error.unsupported_feature.dealer.progressive_call_result"]

-->


## Authentication



![alt text](figure/hello_authenticated.png "WAMP Session denied")

Authentication is a complex area.

Some applications might want to leverage authentication information coming from the transport underlying WAMP, e.g. HTTP cookies or TLS certificates.

Some transports might imply trust or implicit authentication by their very nature, e.g. Unix domain sockets with appropriate file system permissions in place.

Other application might want to perform their own authentication using external mechanisms (completely outside and independent of WAMP).

Some applications might want to perform their own authentication schemes by using basic WAMP mechanisms, e.g. by using application-defined remote procedure calls.

And some applications might want to use a transport independent scheme, nevertheless predefined by WAMP.


### TLS Certificate-based Authentication

When running WAMP over a TLS (either secure WebSocket or raw TCP) transport, a peer may authenticate to the other via the TLS certificate mechanism. A server might authenticate to the client, and a client may authenticate to the server (TLS client-certificate based authentication).

This transport-level authentication information may be forward to the WAMP level within `HELLO.Options.transport.auth|any` in both directions (if available).


### HTTP Cookie-based Authentication

When running WAMP over WebSocket, the transport provides HTTP client cookies during the WebSocket opening handshake. The cookies can be used to authenticate one peer (the client) against the other (the server). The other authentication direction cannot be supported by cookies.

This transport-level authentication information may be forward to the WAMP level within `HELLO.Options.transport.auth|any` in the client-to-server direction.


### WAMP Challenge-Response Authentication

---- now integrated into WAMP session establishment ? ----

WAMP Challenge Response (WAMP-CRA) is a WAMP level authentication procedure implemented on top of standard, predefined WAMP RPC procedures.

A peer may authenticate to its other peer via calling the following procedures

   wamp.cra.request
   wamp.cra.authenticate

WAMP-CRA defines the following errors

   wamp.error.invalid_argument
   wamp.cra.error.no_such_authkey
   wamp.cra.error.authentication_failed
   wamp.cra.error.anonymous_not_allowed
   wamp.cra.error.already_authenticated
   wamp.cra.error.authentication_already_requested

A peer starts WAMP-CRA authentication by calling

   wamp.cra.request

with `Arguments = [auth_key|string, auth_extra|dict]` where

 * `auth_key` is the authentication key, e.g. an application or user identifier, possibly the empty string for "authenticating" as anonymous
 * `auth_extra` is a dictionary of extra authentication information, possibly empty

The other peer then computes an authentication challenge. WRITEME.

The peer then signs the authentication challenge and calls

   wamp.cra.authenticate






## Reflection

*Reflection* denotes the ability of WAMP peers to examine the procedures, topics and errors provided or used by other peers.

I.e. a WAMP *Caller*, *Callee*, *Subscriber* or *Publisher* may be interested in retrieving a machine readable list and description of WAMP procedures and topics it is authorized to access or provide in the context of a WAMP session with a *Dealer* or *Broker*.

Reflection may be useful in the following cases:

 * documentation
 * discoverability
 * generating stubs and proxies

WAMP predefines the following procedures for performing run-time reflection on WAMP peers which act as *Brokers* and/or *Dealers*.

Predefined WAMP reflection procedures to *list* resources by type:

   wamp.reflection.topic.list
   wamp.reflection.procedure.list
   wamp.reflection.error.list

Predefined WAMP reflection procedures to *describe* resources by type:

   wamp.reflection.topic.describe
   wamp.reflection.procedure.describe
   wamp.reflection.error.describe

A peer that acts as a *Broker* SHOULD announce support for the reflection API by sending

   HELLO.Details.roles.broker.reflection|bool := true

A peer that acts as a *Dealer* SHOULD announce support for the reflection API by sending

   HELLO.Details.roles.dealer.reflection|bool := true

> Since *Brokers* might provide (broker) procedures and *Dealers* might provide (dealer) topics, both SHOULD implement the complete API above (even if the peer only implements one of *Broker* or *Dealer* roles).
>
