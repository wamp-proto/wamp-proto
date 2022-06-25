# Messages {#messages}

All WAMP messages are a `list` with a first element `MessageType` followed by one or more message type specific elements:

{align="left"}
        [MessageType|integer, ... one or more message type specific
            elements ...]

The notation `Element|type` denotes a message element named `Element` of type `type`, where `type` is one of

* `uri`: a string URI as defined in [URIs](#uris)
* `id`: an integer ID as defined in [IDs](#ids)
* `integer`: a non-negative integer
* `string`: a Unicode string, including the empty string
* `bool`: a boolean value (`true` or `false`) - integers MUST NOT be used instead of boolean value
* `dict`: a dictionary (map) where keys MUST be strings, keys MUST be unique and serialization order is undefined (left to the serializer being used)
* `list`: a list (array) where items can be again any of this enumeration

*Example*

A `SUBSCRIBE` message has the following format

{align="left"}
        [SUBSCRIBE, Request|id, Options|dict, Topic|uri]

Here is an example message conforming to the above format

{align="left"}
        [32, 713845233, {}, "com.myapp.mytopic1"]


## Extensibility

Some WAMP messages contain `Options|dict` or `Details|dict` elements. This allows for future extensibility and implementations that only provide subsets of functionality by ignoring unimplemented attributes. Keys in `Options` and `Details` MUST be of type `string` and MUST match the regular expression `[a-z][a-z0-9_]{2,}` for WAMP predefined keys. Implementations MAY use implementation-specific keys that MUST match the regular expression `_[a-z0-9_]{3,}`. Attributes unknown to an implementation MUST be ignored.


## No Polymorphism

For a given `MessageType` and number of message elements the expected types are uniquely defined. Hence there are no polymorphic messages in WAMP. This leads to a message parsing and validation control flow that is efficient, simple to implement and simple to code for rigorous message format checking.


## Structure

The application payload (that is call arguments, call results, event payload etc) is always at the end of the message element list. The rationale is: Brokers and Dealers have no need to inspect (parse) the application payload. Their business is call/event routing. Having the application payload at the end of the list allows Brokers and Dealers to skip parsing it altogether. This can improve efficiency and performance.


## Message Definitions

WAMP defines the following messages that are explained in detail in the following sections.

The messages concerning the WAMP session itself are mandatory for all Peers, i.e. a Client MUST implement `HELLO`, `ABORT` and `GOODBYE`, while a Router MUST implement `WELCOME`, `ABORT` and `GOODBYE`.

All other messages are mandatory per role, i.e. in an implementation that only provides a Client with the role of Publisher MUST additionally implement sending `PUBLISH` and receiving `PUBLISHED` and `ERROR` messages.

### Session Lifecycle

#### HELLO

Sent by a Client to initiate opening of a WAMP session to a Router attaching to a Realm.

{align="left"}
        [HELLO, Realm|uri, Details|dict]

#### WELCOME

Sent by a Router to accept a Client. The WAMP session is now open.

{align="left"}
        [WELCOME, Session|id, Details|dict]

#### ABORT

Sent by a Peer*to abort the opening of a WAMP session. No response is expected.

{align="left"}
        [ABORT, Details|dict, Reason|uri]

#### GOODBYE

Sent by a Peer to close a previously opened WAMP session. Must be echo'ed by the receiving Peer.

{align="left"}
        [GOODBYE, Details|dict, Reason|uri]

#### ERROR

Error reply sent by a Peer as an error response to different kinds of requests.

{align="left"}
        [ERROR, REQUEST.Type|int, REQUEST.Request|id, Details|dict, Error|uri]

        [ERROR, REQUEST.Type|int, REQUEST.Request|id, Details|dict, Error|uri,
            Arguments|list]

        [ERROR, REQUEST.Type|int, REQUEST.Request|id, Details|dict, Error|uri,
            Arguments|list, ArgumentsKw|dict]


### Publish & Subscribe

#### PUBLISH

Sent by a Publisher to a Broker to publish an event.

{align="left"}
        [PUBLISH, Request|id, Options|dict, Topic|uri]

        [PUBLISH, Request|id, Options|dict, Topic|uri, Arguments|list]

        [PUBLISH, Request|id, Options|dict, Topic|uri, Arguments|list,
            ArgumentsKw|dict]

#### PUBLISHED

Acknowledge sent by a Broker to a Publisher for acknowledged publications.

{align="left"}
        [PUBLISHED, PUBLISH.Request|id, Publication|id]

#### SUBSCRIBE

Subscribe request sent by a Subscriber to a Broker to subscribe to a topic.

{align="left"}
        [SUBSCRIBE, Request|id, Options|dict, Topic|uri]

#### SUBSCRIBED

Acknowledge sent by a Broker to a Subscriber to acknowledge a subscription.

{align="left"}
        [SUBSCRIBED, SUBSCRIBE.Request|id, Subscription|id]

#### UNSUBSCRIBE

Unsubscribe request sent by a Subscriber to a Broker to unsubscribe a subscription.

{align="left"}
        [UNSUBSCRIBE, Request|id, SUBSCRIBED.Subscription|id]

#### UNSUBSCRIBED

Acknowledge sent by a Broker to a Subscriber to acknowledge unsubscription.

{align="left"}
        [UNSUBSCRIBED, UNSUBSCRIBE.Request|id]

#### EVENT

Event dispatched by Broker to Subscribers for subscriptions the event was matching.

{align="left"}
        [EVENT, SUBSCRIBED.Subscription|id, PUBLISHED.Publication|id, Details|dict]

        [EVENT, SUBSCRIBED.Subscription|id, PUBLISHED.Publication|id, Details|dict,
            PUBLISH.Arguments|list]

        [EVENT, SUBSCRIBED.Subscription|id, PUBLISHED.Publication|id, Details|dict,
            PUBLISH.Arguments|list, PUBLISH.ArgumentsKw|dict]

> An event is dispatched to a Subscriber for a given `Subscription|id` only once. On the other hand, a Subscriber that holds subscriptions with different `Subscription|id`s that all match a given event will receive the event on each matching subscription.
>

### Routed Remote Procedure Calls

#### CALL

Call as originally issued by the Caller to the Dealer.

{align="left"}
      [CALL, Request|id, Options|dict, Procedure|uri]

      [CALL, Request|id, Options|dict, Procedure|uri, Arguments|list]

      [CALL, Request|id, Options|dict, Procedure|uri, Arguments|list,
          ArgumentsKw|dict]

#### RESULT

Result of a call as returned by Dealer to Caller.

{align="left"}
        [RESULT, CALL.Request|id, Details|dict]

        [RESULT, CALL.Request|id, Details|dict, YIELD.Arguments|list]

        [RESULT, CALL.Request|id, Details|dict, YIELD.Arguments|list,
            YIELD.ArgumentsKw|dict]

#### REGISTER

A Callees request to register an endpoint at a Dealer.

{align="left"}
        [REGISTER, Request|id, Options|dict, Procedure|uri]

#### REGISTERED

Acknowledge sent by a Dealer to a Callee for successful registration.

{align="left"}
        [REGISTERED, REGISTER.Request|id, Registration|id]

#### UNREGISTER

A Callees request to unregister a previously established registration.

{align="left"}
        [UNREGISTER, Request|id, REGISTERED.Registration|id]

#### UNREGISTERED

Acknowledge sent by a Dealer to a Callee for successful unregistration.

{align="left"}
        [UNREGISTERED, UNREGISTER.Request|id]

#### INVOCATION

Actual invocation of an endpoint sent by Dealer to a Callee.

{align="left"}
        [INVOCATION, Request|id, REGISTERED.Registration|id, Details|dict]

        [INVOCATION, Request|id, REGISTERED.Registration|id, Details|dict,
            CALL.Arguments|list]

        [INVOCATION, Request|id, REGISTERED.Registration|id, Details|dict,
            CALL.Arguments|list, CALL.ArgumentsKw|dict]

#### YIELD

Actual yield from an endpoint sent by a Callee to Dealer.

{align="left"}
        [YIELD, INVOCATION.Request|id, Options|dict]

        [YIELD, INVOCATION.Request|id, Options|dict, Arguments|list]

        [YIELD, INVOCATION.Request|id, Options|dict, Arguments|list, ArgumentsKw|dict]



## Message Codes and Direction

The following table lists the message type code for all messages defined in the WAMP basic profile and their direction between peer roles.

Reserved codes may be used to identify additional message types in future standards documents.

"Tx" indicates the message is sent by the respective role, and "Rx" indicates the message is received by the respective role.

{align="left"}
| Cod | Message        |  Pub |  Brk | Subs |  Calr | Dealr | Callee|
|-----|----------------|------|------|------|-------|-------|-------|
|  1  | `HELLO`        | Tx   | Rx   | Tx   | Tx    | Rx    | Tx    |
|  2  | `WELCOME`      | Rx   | Tx   | Rx   | Rx    | Tx    | Rx    |
|  3  | `ABORT`        | Rx   | TxRx | Rx   | Rx    | TxRx  | Rx    |
|  6  | `GOODBYE`      | TxRx | TxRx | TxRx | TxRx  | TxRx  | TxRx  |
|     |                |      |      |      |       |       |       |
|  8  | `ERROR`        | Rx   | Tx   | Rx   | Rx    | TxRx  | TxRx  |
|     |                |      |      |      |       |       |       |
| 16  | `PUBLISH`      | Tx   | Rx   |      |       |       |       |
| 17  | `PUBLISHED`    | Rx   | Tx   |      |       |       |       |
|     |                |      |      |      |       |       |       |
| 32  | `SUBSCRIBE`    |      | Rx   | Tx   |       |       |       |
| 33  | `SUBSCRIBED`   |      | Tx   | Rx   |       |       |       |
| 34  | `UNSUBSCRIBE`  |      | Rx   | Tx   |       |       |       |
| 35  | `UNSUBSCRIBED` |      | Tx   | Rx   |       |       |       |
| 36  | `EVENT`        |      | Tx   | Rx   |       |       |       |
|     |                |      |      |      |       |       |       |
| 48  | `CALL`         |      |      |      | Tx    | Rx    |       |
| 50  | `RESULT`       |      |      |      | Rx    | Tx    |       |
|     |                |      |      |      |       |       |       |
| 64  | `REGISTER`     |      |      |      |       | Rx    | Tx    |
| 65  | `REGISTERED`   |      |      |      |       | Tx    | Rx    |
| 66  | `UNREGISTER`   |      |      |      |       | Rx    | Tx    |
| 67  | `UNREGISTERED` |      |      |      |       | Tx    | Rx    |
| 68  | `INVOCATION`   |      |      |      |       | Tx    | Rx    |
| 70  | `YIELD`        |      |      |      |       | Rx    | Tx    |


## Extension Messages

WAMP uses type codes from the core range [0, 255]. Implementations MAY define and use implementation specific messages with message type codes from the extension message range [256, 1023]. For example, a router MAY implement router-to-router communication by using extension messages.

## Empty Arguments and Keyword Arguments

Implementations SHOULD avoid sending empty `Arguments` lists.

E.g. a `CALL` message

{align="left"}
        [CALL, Request|id, Options|dict, Procedure|uri, Arguments|list]

where `Arguments == []` SHOULD be avoided, and instead

{align="left"}
        [CALL, Request|id, Options|dict, Procedure|uri]

SHOULD be sent.

Implementations SHOULD avoid sending empty `ArgumentsKw` dictionaries.

E.g. a `CALL` message

{align="left"}
        [CALL, Request|id, Options|dict, Procedure|uri, Arguments|list, ArgumentsKw|dict]

where `ArgumentsKw == {}` SHOULD be avoided, and instead

{align="left"}
        [CALL, Request|id, Options|dict, Procedure|uri, Arguments|list]

SHOULD be sent when `Arguments` is non-empty.

