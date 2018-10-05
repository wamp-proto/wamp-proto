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

* `Request` is a random, ephemeral ID chosen by the Publisher and used to correlate the Broker's response with the request.
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
* `Publication` is a ID chosen by the Broker for the publication.

*Example*

{align="left"}
        [17, 239714735, 4429313566]


### Publish ERROR

When the request for publication cannot be fulfilled by the Broker, and `PUBLISH.Options.acknowledge == true`, the Broker sends back an `ERROR` message to the Publisher

{align="left"}
        [ERROR, PUBLISH, PUBLISH.Request|id, Details|dict, Error|uri]

where

 * `PUBLISH.Request` is the ID from the original publication request.
 * `Error` is an URI that gives the error of why the request could not be fulfilled.

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
        [EVENT, SUBSCRIBED.Subscription|id, PUBLISHED.Publication|id,
            Details|dict]

or

{align="left"}
        [EVENT, SUBSCRIBED.Subscription|id, PUBLISHED.Publication|id,
            Details|dict, PUBLISH.Arguments|list]

or

{align="left"}
        [EVENT, SUBSCRIBED.Subscription|id, PUBLISHED.Publication|id,
        Details|dict, PUBLISH.Arguments|list, PUBLISH.ArgumentKw|dict]

where

* `SUBSCRIBED.Subscription` is the ID for the subscription under which the Subscriber receives the event - the ID for the subscription originally handed out by the Broker to the Subscribe*.
* `PUBLISHED.Publication` is the ID of the publication of the published event.
* `Details` is a dictionary that allows the Broker to provide additional event details in a extensible way. This is described further below.
* `PUBLISH.Arguments` is the application-level event payload that was provided with the original publication request.
* `PUBLISH.ArgumentKw` is the application-level event payload that was provided with the original publication request.

*Example*

{align="left"}
        [36, 5512315355, 4429313566, {}]

*Example*

{align="left"}
        [36, 5512315355, 4429313566, {}, ["Hello, world!"]]

*Example*

{align="left"}
        [36, 5512315355, 4429313566, {}, [], {"color": "orange",
            "sizes": [23, 42, 7]}]


