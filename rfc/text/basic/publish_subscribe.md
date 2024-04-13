# Publish and Subscribe

All of the following features for Publish & Subscribe are mandatory for WAMP Basic Profile implementations supporting the respective roles, i.e. *Publisher*, *Subscriber* and *Broker*.

## Subscribing and Unsubscribing

The message flow between Clients implementing the role of Subscriber and Routers implementing the role of Broker for subscribing and unsubscribing involves the following messages:

1. `SUBSCRIBE`
2. `SUBSCRIBED`
3. `UNSUBSCRIBE`
4. `UNSUBSCRIBED`
5. `ERROR`

{align="left"}
        ,---------.          ,------.             ,----------.
        |Publisher|          |Broker|             |Subscriber|
        `----+----'          `--+---'             `----+-----'
             |                  |                      |
             |                  |                      |
             |                  |       SUBSCRIBE      |
             |                  | <---------------------
             |                  |                      |
             |                  |  SUBSCRIBED or ERROR |
             |                  | --------------------->
             |                  |                      |
             |                  |                      |
             |                  |                      |
             |                  |                      |
             |                  |      UNSUBSCRIBE     |
             |                  | <---------------------
             |                  |                      |
             |                  | UNSUBSCRIBED or ERROR|
             |                  | --------------------->
        ,----+----.          ,--+---.             ,----+-----.
        |Publisher|          |Broker|             |Subscriber|
        `---------'          `------'             `----------'


A Subscriber may subscribe to zero, one or more topics, and a Publisher publishes to topics without knowledge of subscribers.

Upon subscribing to a topic via the `SUBSCRIBE` message, a Subscriber will receive any future events published to the respective topic by Publishers, and will receive those events asynchronously.

A subscription lasts for the duration of a session, unless a Subscriber opts out from a previously established subscription via the `UNSUBSCRIBE` message.

> A Subscriber may have more than one event handler attached to the same subscription. This can be implemented in different ways: a) a Subscriber can recognize itself that it is already subscribed and just attach another handler to the subscription for incoming events, b) or it can send a new `SUBSCRIBE` message to broker (as it would be first) and upon receiving a `SUBSCRIBED.Subscription|id` it already knows about, attach the handler to the existing subscription
>

### SUBSCRIBE

A Subscriber communicates its interest in a topic to a Broker by sending a `SUBSCRIBE` message:

{align="left"}
        [SUBSCRIBE, Request|id, Options|dict, Topic|uri]

where

 * `Request` is a sequential ID in the _session scope_, incremented by the Subscriber and used to correlate the Broker's response with the request.
 * `Options` is a dictionary that allows to provide additional subscription request details in a extensible way. This is described further below.
 * `Topic` is the topic the Subscriber wants to subscribe to and is a URI.

*Example*

{align="left"}
        [32, 713845233, {}, "com.myapp.mytopic1"]

A Broker, receiving a `SUBSCRIBE` message, can fullfill or reject the subscription, so it answers with `SUBSCRIBED` or `ERROR` messages.

### SUBSCRIBED

If the Broker is able to fulfill and allow the subscription, it answers by sending a `SUBSCRIBED` message to the Subscriber

{align="left"}
        [SUBSCRIBED, SUBSCRIBE.Request|id, Subscription|id]

where

 * `SUBSCRIBE.Request` is the ID from the original subscription request.
 * `Subscription` is an ID chosen by the Broker for the subscription.

*Example*

{align="left"}
        [33, 713845233, 5512315355]

> Note. The `Subscription` ID chosen by the broker need not be unique to the subscription of a single Subscriber, but may be assigned to the `Topic`, or the combination of the `Topic` and some or all `Options`, such as the topic pattern matching method to be used. Then this ID may be sent to all Subscribers for the `Topic` or `Topic` /  `Options` combination. This allows the Broker to serialize an event to be delivered only once for all actual receivers of the event.

> In case of receiving a `SUBSCRIBE` message from the same Subscriber and to already subscribed topic, Broker should answer with `SUBSCRIBED` message, containing the existing `Subscription|id`.

### Subscribe ERROR

When the request for subscription cannot be fulfilled by the Broker, the Broker sends back an `ERROR` message to the Subscriber

{align="left"}
        [ERROR, SUBSCRIBE, SUBSCRIBE.Request|id, Details|dict, Error|uri]

where

 * `SUBSCRIBE.Request` is the ID from the original request.
 * `Error` is a URI that gives the error of why the request could not be fulfilled.

*Example*

{align="left"}
        [8, 32, 713845233, {}, "wamp.error.not_authorized"]


### UNSUBSCRIBE

When a Subscriber is no longer interested in receiving events for a subscription it sends an `UNSUBSCRIBE` message

{align="left"}
        [UNSUBSCRIBE, Request|id, SUBSCRIBED.Subscription|id]

where

 * `Request` is a sequential ID in the _session scope_, incremented by the Subscriber and used to correlate the Broker's response with the request.
 * `SUBSCRIBED.Subscription` is the ID for the subscription to unsubscribe from, originally handed out by the Broker to the Subscriber.

*Example*

{align="left"}
        [34, 85346237, 5512315355]

### UNSUBSCRIBED

Upon successful unsubscription, the Broker sends an `UNSUBSCRIBED` message to the Subscriber

{align="left"}
        [UNSUBSCRIBED, UNSUBSCRIBE.Request|id]

where

 * `UNSUBSCRIBE.Request` is the ID from the original request.

*Example*

{align="left"}
        [35, 85346237]


### Unsubscribe ERROR

When the request fails, the Broker sends an `ERROR`

{align="left"}
        [ERROR, UNSUBSCRIBE, UNSUBSCRIBE.Request|id, Details|dict, Error|uri]

where

 * `UNSUBSCRIBE.Request` is the ID from the original request.
 * `Error` is a URI that gives the error of why the request could not be fulfilled.

*Example*

{align="left"}
        [8, 34, 85346237, {}, "wamp.error.no_such_subscription"]

## Publishing and Events

The message flow between Publishers, a Broker and Subscribers for publishing to topics and dispatching events involves the following messages:

 1. `PUBLISH`
 2. `PUBLISHED`
 3. `EVENT`
 4. `ERROR`

{align="left"}
        ,---------.          ,------.          ,----------.
        |Publisher|          |Broker|          |Subscriber|
        `----+----'          `--+---'          `----+-----'
             |     PUBLISH      |                   |
             |------------------>                   |
             |                  |                   |
             |PUBLISHED or ERROR|                   |
             |<------------------                   |
             |                  |                   |
             |                  |       EVENT       |
             |                  | ------------------>
        ,----+----.          ,--+---.          ,----+-----.
        |Publisher|          |Broker|          |Subscriber|
        `---------'          `------'          `----------'


### PUBLISH

When a Publisher requests to publish an event to some topic, it sends a `PUBLISH` message to a Broker:

{align="left"}
        [PUBLISH, Request|id, Options|dict, Topic|uri]

or

{align="left"}
        [PUBLISH, Request|id, Options|dict, Topic|uri, Arguments|list]

or

{align="left"}
        [PUBLISH, Request|id, Options|dict, Topic|uri, Arguments|list,
            ArgumentsKw|dict]

where

* `Request` is a sequential ID in the _session scope_, incremented by the Publisher and used to correlate the Broker's response with the request.
* `Options` is a dictionary that allows to provide additional publication request details in an extensible way. This is described further below.
* `Topic` is the topic published to.
* `Arguments` is a list of application-level event payload elements. The list may be of zero length.
* `ArgumentsKw` is an optional dictionary containing application-level event payload, provided as keyword arguments. The dictionary may be empty.

If the Broker allows and is able to fulfill the publication, the Broker will send the event to all current Subscribers of the topic of the published event.

By default, publications are unacknowledged, and the Broker will not respond, whether the publication was successful indeed or not. This behavior can be changed with the option `PUBLISH.Options.acknowledge|bool` (see below).

*Example*

{align="left"}
        [16, 239714735, {}, "com.myapp.mytopic1"]

*Example*

{align="left"}
        [16, 239714735, {}, "com.myapp.mytopic1", ["Hello, world!"]]

*Example*

{align="left"}
        [16, 239714735, {}, "com.myapp.mytopic1", [], {"color": "orange",
            "sizes": [23, 42, 7]}]


### PUBLISHED

If the Broker is able to fulfill and allowing the publication, and `PUBLISH.Options.acknowledge == true`, the Broker replies by sending a `PUBLISHED` message to the Publisher:

{align="left"}
        [PUBLISHED, PUBLISH.Request|id, Publication|id]

where

* `PUBLISH.Request` is the ID from the original publication request.
* `Publication` is an ID chosen by the Broker for the publication.

*Example*

{align="left"}
        [17, 239714735, 4429313566]


### Publish ERROR

When the request for publication cannot be fulfilled by the Broker, and `PUBLISH.Options.acknowledge == true`, the Broker sends back an `ERROR` message to the Publisher

{align="left"}
        [ERROR, PUBLISH, PUBLISH.Request|id, Details|dict, Error|uri]

where

 * `PUBLISH.Request` is the ID from the original publication request.
 * `Error` is a URI that gives the error of why the request could not be fulfilled.

*Example*

{align="left"}
        [8, 16, 239714735, {}, "wamp.error.not_authorized"]


### EVENT

When a publication is successful and a Broker dispatches the event, it determines a list of receivers for the event based on Subscribers for the topic published to and, possibly, other information in the event.

Note that the Publisher of an event will never receive the published event even if the Publisher is also a Subscriber of the topic published to.

> The Advanced Profile provides options for more detailed control over publication.
>

When a Subscriber is deemed to be a receiver, the Broker sends the Subscriber an `EVENT` message:

{align="left"}
        [EVENT, SUBSCRIBED.Subscription|id, PUBLISHED.Publication|id, Details|dict]

or

{align="left"}
        [EVENT, SUBSCRIBED.Subscription|id, PUBLISHED.Publication|id, Details|dict,
            PUBLISH.Arguments|list]

or

{align="left"}
        [EVENT, SUBSCRIBED.Subscription|id, PUBLISHED.Publication|id, Details|dict,
            PUBLISH.Arguments|list, PUBLISH.ArgumentsKw|dict]

where

* `SUBSCRIBED.Subscription` is the ID for the subscription under which the Subscriber receives the event - the ID for the subscription originally handed out by the Broker to the Subscribe.
* `PUBLISHED.Publication` is the ID of the publication of the published event.
* `Details` is a dictionary that allows the Broker to provide additional event details in a extensible way. This is described further below.
* `PUBLISH.Arguments` is the application-level event payload that was provided with the original publication request.
* `PUBLISH.ArgumentsKw` is the application-level event payload that was provided with the original publication request.

*Example*

{align="left"}
        [36, 5512315355, 4429313566, {}]

*Example*

{align="left"}
        [36, 5512315355, 4429313566, {}, ["Hello, world!"]]

*Example*

{align="left"}
        [36, 5512315355, 4429313566, {}, [], {"color": "orange", "sizes": [23, 42, 7]}]
