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

 * `Request` MUST be a random, ephemeral ID chosen by the Subscriber and used to correlate the Broker's response with the request.
 * `Options` MUST be a dictionary that allows to provide additional subscription request details in a extensible way. This is described further below.
 * `Topic` is the topic the Subscriber wants to subscribe to and MUST be a URI.

*Example*

{align="left"}
        [32, 713845233, {}, "com.myapp.mytopic1"]

A Broker, receiving a `SUBSCRIBE` message, can fullfill or reject the subscription, so it answers with `SUBSCRIBED` or `ERROR` messages.

### SUBSCRIBED

If the Broker is able to fulfill and allow the subscription, it answers by sending a `SUBSCRIBED` message to the Subscriber

{align="left"}
        [SUBSCRIBED, SUBSCRIBE.Request|id, Subscription|id]

where

 * `SUBSCRIBE.Request` MUST be the ID from the original request.
 * `Subscription` MUST be an ID chosen by the Broker for the subscription.

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

 * `SUBSCRIBE.Request` MUST be the ID from the original request.
 * `Error` MUST be a URI that gives the error of why the request could not be fulfilled.

*Example*

{align="left"}
        [8, 32, 713845233, {}, "wamp.error.not_authorized"]


### UNSUBSCRIBE

When a Subscriber is no longer interested in receiving events for a subscription it sends an `UNSUBSCRIBE` message

{align="left"}
        [UNSUBSCRIBE, Request|id, SUBSCRIBED.Subscription|id]

where

 * `Request` MUST be a random, ephemeral ID chosen by the Subscriber and used to correlate the Broker's response with the request.
 * `SUBSCRIBED.Subscription` MUST be the ID for the subscription to unsubscribe from, originally handed out by the Broker to the Subscriber.

*Example*

{align="left"}
        [34, 85346237, 5512315355]

### UNSUBSCRIBED

Upon successful unsubscription, the Broker sends an `UNSUBSCRIBED` message to the Subscriber

{align="left"}
        [UNSUBSCRIBED, UNSUBSCRIBE.Request|id]

where

 * `UNSUBSCRIBE.Request` MUST be the ID from the original request.

*Example*

{align="left"}
        [35, 85346237]


### Unsubscribe ERROR

When the request fails, the Broker sends an `ERROR`

{align="left"}
        [ERROR, UNSUBSCRIBE, UNSUBSCRIBE.Request|id, Details|dict, Error|uri]

where

 * `UNSUBSCRIBE.Request` MUST be the ID from the original request.
 * `Error` MUST be a URI that gives the error of why the request could not be fulfilled.

*Example*

{align="left"}
        [8, 34, 85346237, {}, "wamp.error.no_such_subscription"]
