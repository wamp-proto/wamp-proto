# WAMP v2 Specification

This document specifies version 2 of the [WAMP](http://wamp.ws/) protocol.


## Introduction

WAMP ("The WebSocket Application Messaging Protocol") is an open application messaging protocol that provides two asynchronous messaging patterns:

 * Remote Procedure Calls
 * Publish & Subscribe


## Building Blocks

WAMP is defined with respect to the following building blocks 

   1. Namespace
   2. Serialization
   3. Transport

For each building block, WAMP only assumes a defined set of requirements, which allows to run WAMP variants with different concrete bindings.


### Namespace

WAMP needs to identify **procedures** for *Remote Procedure Calls* and **topics** for *Publish & Subscribe*.

A (single) *namespace* with the following characteristics is assumed:

 * string-based
 * hierarchical
 * global assignment and conflict resolution

The default *namespace* binding for WAMPv2 (and in fact the only currently defined) is URIs as used on the Web:

Identifiers as used in the WAMP protocol are URIs which MUST conform to [RFC3986](http://tools.ietf.org/html/rfc3986), MUST be from the `HTTP` scheme, MAY contain a fragment part, but MUST NOT contain query parts.

> It's important to note that WAMP only uses `http` scheme URIs as *identifiers*, **not** resource locators (URLs). The use of the `http` scheme does **not** imply use of `http` as a transport protocol.
> 

	http://wamp.ws/error#NotAuthorized

or

	wamp.error.notauthorized

or

	ws.wamp.error.notauthorized


http://docs.oracle.com/javase/specs/jls/se5.0/html/packages.html#7.7
http://en.wikipedia.org/wiki/Java_package
http://docs.oracle.com/javase/tutorial/java/package/namingpkgs.html


### Serialization

WAMP is a message based protocol that requires serialization of messages to octet sequences to be sent out on the wire.

A message *serialization* format is assumed that (at least) provides the following types:

  * `integer` (non-negative)
  * `string` (UTF8 encoded)
  * `list`
  * `dict` (with string keys)

WAMP *itself* only uses above types. The application payloads transmitted by WAMP (e.g. in call arguments or event payloads) may use other types a concrete serialization supports.

WAMPv2 defines two bindings for message *serialization*:

 1. [JSON](http://www.json.org/)
 2. [MsgPack](http://msgpack.org/)

> * As noted above, WAMP *itself* does only use a subset of types - e.g. it does not use the JSON types `number` (non-integer), `bool` and `null`.
> * With MsgPack, the [version 5](https://github.com/msgpack/msgpack/blob/master/spec.md) MUST BE supported - which is able to differentiate between strings and binary values.
> 

Other bindings for *serialization* may be defined in future WAMP versions.


### Transport

WAMP assumes a *transport* with the following characteristics:

  1. message-based
  2. reliable
  3. ordered
  4. full-duplex


#### WebSocket Transport

The default transport binding is [WebSocket](http://tools.ietf.org/html/rfc6455). With WebSocket, WAMP messages are transmitted as WebSocket messages: each WAMP message is transmitted as a separate WebSocket message (not WebSocket frame).

The WAMP protocol MUST BE negotiated during the opening WebSocket handshakes between peers using the WebSocket subprotocol negotiation mechanism.

WAMPv2 uses the following WebSocket subprotocol identifiers:

 * `wamp.2.json`
 * `wamp.2.msgpack`

With `wamp.2.json`, all WebSocket messages MUST BE of type **text** (UTF8 encoded payload) and use the JSON message serialization.

With `wamp.2.msgpack`, all WebSocket messages MUST BE of type **binary** and use the MsgPack message serialization.

With both WAMP WebSocket subprotocols, the namespace binding MUST BE URIs from the HTTP scheme as described above.


#### Other Transports

Besides the WebSocket transport, the following WAMP transports are under development:

 * HTTP 1.0/1.1 long-polling
 * HTTP 2.0 ("SPDY")

Other transports might be defined in the future.


## Peer Roles

A transport connects two WAMP peers and provides a channel over which WAMP messages for a *single* WAMP session can flow in both directions.

A WAMP peer can have one or more of the following roles.

**RPC**

1. Callee
2. Caller
3. Dealer

*Callees* register procedures they provide with *Dealers*.

*Callers* initiate procedure calls first to *Dealers*.

*Dealers* route call incoming from *Callers* to *Callees* implementing the procedure called.

**PubSub**

1. Subscriber
2. Publisher
3. Broker

*Subscribers* subscribe to topics they are interested in with *Brokers*.

*Publishers* publish events to topics at *Brokers*.

*Brokers* route events incoming from *Publishers* to *Subscribers* subscribed to the topic published to.

### Decoupling

*Dealers* are responsible for call routing decoupling *Callers* from *Callees*, whereas *Brokers* are responsible for event routing decoupling *Publishers* from *Subscribers*.

### Symmetry

It's important to note that though the establishment of a transport connection might have a inherent asymmetry (like a *client* establishes a TCP and WebSocket connection to a *server*), WAMP itself is designed to be fully symmetric. After the transport has been established, both peers are equal in principle.

### Peers with multiple Roles

Peers might implement more than one role: e.g. a peer might act as *Caller*, *Publisher* and *Subscriber* at the same time. Another peer might act as both a *Broker* and a *Dealer*. And a *Dealer* might also act as a *Callee*. With the latter, a peer might "route" an incoming call directly to an implementing endpoint within the same program (and hence no actual messaging over a transport is happening).


## Messages

### Overview

All WAMP messages are of the same structure - a `list` with a first element `MessageType` followed by zero or more message type specific elements:

    [MessageType|integer, ... zero or more message type specific elements ...]

The notation `Element|type` denotes a message element named `Element` of type `type`, where `type` is one of:

 * `integer`: a non-negative integer
 * `string`: any UTF8-encoded string, including the empty string
 * `id`: a random (positive) integer
 * `uri`: an UTF8- and percent-encoded string that is a valid URI
 * `dict`: a dictionary (map) with `string` typed keys
 * `list`: a list (array)

WAMP defines the following messages which are explained in detail in the further sections.


### Session Management

#### Any-to-Any

    [HELLO,        			Session|id]
    [HELLO,        			Session|id, Details|dict]
    [GOODBYE]
    [GOODBYE,      			Details|dict]
    [HEARTBEAT,    			IncomingSeq|integer, OutgoingSeq|integer]
    [HEARTBEAT,    			IncomingSeq|integer, OutgoingSeq|integer, Discard|string]

### Publish & Subscribe

#### Publisher-to-Broker

    [PUBLISH,      			Request|id, Topic|uri]
    [PUBLISH,      			Request|id, Topic|uri, Event|any]
    [PUBLISH,      			Request|id, Topic|uri, Options|dict, Event|any]

#### Broker-to-Publisher

    [PUBLISHED,  			PUBLISH.Request|id]
    [PUBLISH_ERROR, 		PUBLISH.Request|id, Error|uri]

#### Subscriber-to-Broker

    [SUBSCRIBE,    			Request|id, Topic|uri]
    [SUBSCRIBE,    			Request|id, Topic|uri, Options|dict]
    [UNSUBSCRIBE,  			Request|id, SUBSCRIBED.Subscription|id]
    [UNSUBSCRIBE,  			Request|id, SUBSCRIBED.Subscription|id, Options|dict]

#### Broker-to-Subscriber

    [SUBSCRIBED,   			SUBSCRIBE.Request|id, Subscription|id]
    [SUBSCRIBE_ERROR, 		SUBSCRIBE.Request|id, Error|uri]
    [UNSUBSCRIBED, 			UNSUBSCRIBE.Request|id]
    [UNSUBSCRIBE_ERROR, 	UNSUBSCRIBE.Request|id, Error|uri]
    [EVENT,        			SUBSCRIBED.Subscription|id, Topic|uri]
    [EVENT,        			SUBSCRIBED.Subscription|id, Topic|uri, Event|any]
    [EVENT,        			SUBSCRIBED.Subscription|id, Topic|uri, Details|dict, Event|any]
    [METAEVENT,    			SUBSCRIBED.Subscription|id, Metatopic|uri]
    [METAEVENT,    			SUBSCRIBED.Subscription|id, Metatopic|uri, Details|dict]

### Remote Procedure Calls

#### Caller-to-Dealer

    [CALL,         			Request|id, Procedure|uri]
    [CALL,         			Request|id, Procedure|uri, Arguments|list]
    [CALL,         			Request|id, Procedure|uri, Options|dict, Arguments|list]
    [CANCEL_CALL,  			CALL.Request|id]
    [CANCEL_CALL,  			CALL.Request|id, Options|dict]
    
#### Dealer-to-Caller

    [CALL_PROGRESS,			CALL.Request|id]
    [CALL_PROGRESS, 		CALL.Request|id, Progress|any]
    [CALL_RESULT,   		CALL.Request|id]
    [CALL_RESULT,   		CALL.Request|id, Result|any]
    [CALL_ERROR,    		CALL.Request|id, Error|uri]
    [CALL_ERROR,    		CALL.Request|id, Error|uri, Exception|any]

#### Callee-to-Dealer

    [REGISTER,     			Request|id, Procedure|uri]
    [REGISTER,     			Request|id, Procedure|uri, Options|dict]
    [UNREGISTER,    		Request|id, REGISTERED.Registration|id]
    [UNREGISTER,     		Request|id, REGISTERED.Registration|id, Options|dict]
    [INVOCATION_PROGRESS,	INVOCATION.Request|id]
    [INVOCATION_PROGRESS, 	INVOCATION.Request|id, Progress|any]
    [INVOCATION_RESULT,   	INVOCATION.Request|id]
    [INVOCATION_RESULT,   	INVOCATION.Request|id, Result|any]
    [INVOCATION_ERROR,    	INVOCATION.Request|id, Error|uri]
    [INVOCATION_ERROR,    	INVOCATION.Request|id, Error|uri, Exception|any]

#### Dealer-to-Callee

	[REGISTERED,     		REGISTER.Request|id, Registration|id]
    [REGISTER_ERROR, 		REGISTER.Request|id, Error|uri]
    [UNREGISTERED,   		UNREGISTER.Request|id]
    [UNREGISTER_ERROR, 		UNREGISTER.Request|id, Error|uri]
    [INVOCATION,   			Request|id, REGISTERED.Registration|id]
    [INVOCATION,   			Request|id, REGISTERED.Registration|id, Arguments|list]
    [CANCEL_INVOCATION,		INVOCATION.Request|id]
    [CANCEL_INVOCATION,		INVOCATION.Request|id, Options|dict]


## Session Management

### Hello and Goodbye

When a WAMP session starts, the peers introduce themselves to each other by sending a

    [HELLO,        			Session|id]
    [HELLO,        			Session|id, Details|dict]

message.

The `HELLO` message MUST be the very first message sent by each of the two peers after the transport has been established.

The `HELLO.Session` MUST BE a randomly generated ID specific to the WAMP session for each direction. Each peer tells it connected peer the `Session` ID under which it is identified (for the lifetime of the WAMP session). 

The `HELLO.Session` can (later) be used for:

 * specifying lists of excluded or eligible receivers when publishing events
 * in the context of performing authentication or authorization 

The `HELLO.Details` is an optional 

Similar to what browsers do with the `User-Agent` HTTP header, the `HELLO` message MAY disclose the WAMP implementation in use to it's peer:

    HELLO.Details.agent|string

*Example*

    [1, 9129137332]

*Example*

    [1, 9129137332, {"agent": "AutobahnPython-0.7.0"}]

A WAMP session starts it's lifetime when both peers have received `HELLO` from the other, and ends when the underlying transport closes or when the session is closed explicitly by using the

    [GOODBYE]
    [GOODBYE,      			Details|dict]

message.

    GOODBYE.Details.reason|uri
    GOODBYE.Details.message|string

*Example*

    [8]

*Example*

    [8, {"reason": "http://api.wamp.ws/error#protocolViolation",
         "message": "Topic in SUBSCRIBE not a valid URI."}]

### Heartbeats

A peer MAY send a `HEARTBEAT` message at any time:

    [HEARTBEAT,    			IncomingSeq|integer, OutgoingSeq|integer]
    [HEARTBEAT,    			IncomingSeq|integer, OutgoingSeq|integer, Discard|string]

The heartbeat allows to keep network intermediaries from closing the underlying transport, notify the peer up to which incoming heartbeat all incoming WAMP messages have been processed, and announce an outgoing hearbeat sequence number in the same message.

The `HEARTBEAT.OutgoingSeq` MUST start with `1` and be incremented by `1` for each `HEARTBEAT` a peer sends.
 
The `HEARTBEAT.IncomingSeq` MUST BE the sequence number from the last received heartbeat for which all previously received WAMP messages have been processed.

The `HEARTBEAT.Discard` is an arbitrary string discarded by the peer. It can be used to exhibit some traffic volume e.g. to keep mobile radio channels in a low-latency, high-power state. The string SHOULD be a random string (otherwise compressing transports might compress away the traffic volume).

Incoming heartbeats are not required to be answered by an outgoing heartbeat, but sending of hearbeats is under independent control with each peer.


## Publish & Subscribe

### Subscribing and Unsubscribing

The message flow between *Subscribers* and a *Broker* for subscribing and unsubscribing involves the following messages:

 1. `SUBSCRIBE`
 2. `SUBSCRIBED`
 3. `SUBSCRIBE_ERROR`
 4. `UNSUBSCRIBE`
 5. `UNSUBSCRIBED`
 6. `UNSUBSCRIBE_ERROR`

![alt text](figure/pubsub_subscribe1.png "RPC Message Flow: Calls")

A *Subscriber* communicates it's interest in a topic to a *Broker* by sending a `SUBSCRIBE` message:

    [SUBSCRIBE,    			Request|id, Topic|uri]
    [SUBSCRIBE,    			Request|id, Topic|uri, Options|dict]

The `Request` is a random ID used to correlate the *Broker's* response with the request. If the *Broker* is able to fulfil and allowing the subscription, it answers by sending a `SUBSCRIBED` message to the *Subscriber*

    [SUBSCRIBED,   			SUBSCRIBE.Request|id, Subscription|id]

The `SUBSCRIBE.Request` is the ID from the original request. `Subscription` is a ID chosen by the *Broker* for the subscription.

> Note. The `Subscription` ID chosen by the broker may be unique only for the `Topic` (and possibly other information from `Options`, such as the topic pattern matching method to be used). The ID might be the same for any *Subscriber* for the same `Topic`. This allows the *Broker* to only serialize an event to be delivered once for all actual receivers of the event.
> 

When the request for subscription cannot be fulfilled by the broker, the broker sends back a `SUBSCRIBE_ERROR` message to the *Subscriber*

    [SUBSCRIBE_ERROR, 		SUBSCRIBE.Request|id, Error|uri]

The `SUBSCRIBE.Request` is the ID from the original request. `Error` is an URI that gives the error of why the request could not be fulfilled:

    wamp.error.notauthorized

When a *Subscriber* is no longer interested in receiving events for a subscription it send an `UNSUBSCRIBE` message

    [UNSUBSCRIBE,  			Request|id, SUBSCRIBED.Subscription|id]
    [UNSUBSCRIBE,  			Request|id, SUBSCRIBED.Subscription|id, Options|dict]

The `Request` is a random ID used to correlate the *Broker's* response with the request. The `SUBSCRIBED.Subscription` is the ID for the subscription originally handed out by the *Broker* to the *Subscriber*.

Upon successful unsubscription, the *Broker* sends an `UNSUBSCRIBED` message to the *Subscriber*

    [UNSUBSCRIBED, 			UNSUBSCRIBE.Request|id]

When the request failed, the *Broker* sends an `UNSUBSCRIBE_ERROR`

    [UNSUBSCRIBE_ERROR, 	UNSUBSCRIBE.Request|id, Error|uri]

The `UNSUBSCRIBE.Request` is the ID from the original request. `Error` is an URI that gives the error of why the request could not be fulfilled:

    wamp.error.nosuchsubscription


### Publishing

The message flow between *Publishers*, a *Broker* and *Subscribers* for publishing and dispatching events involves the following messages:

 1. `PUBLISH`
 2. `PUBLISHED`
 3. `PUBLISH_ERROR`
 4. `EVENT`

![alt text](figure/pubsub_publish1.png "RPC Message Flow: Calls")

When a *Broker* dispatches an event, it will determine a list of actual receivers for that event based on subscribers and possibly other information in the event (such as exclude and eligible receivers).

When a *Subscriber* was deemed to be an actual receiver, the *Broker* will send the *Subscriber* an `EVENT` message:

    [EVENT,        			SUBSCRIBED.Subscription|id, Topic|uri]
    [EVENT,        			SUBSCRIBED.Subscription|id, Topic|uri, Event|any]
    [EVENT,        			SUBSCRIBED.Subscription|id, Topic|uri, Details|dict, Event|any]

The `SUBSCRIBED.Subscription` is the ID for the subscription originally handed out by the *Broker* to the *Subscriber*.


### Pattern-based Subscriptions


### Metaevents

    [METAEVENT,    			SUBSCRIBED.Subscription|id, Metatopic|uri]
    [METAEVENT,    			SUBSCRIBED.Subscription|id, Metatopic|uri, Details|dict]



![alt text](figure/rpc_call1.png "RPC Message Flow: Calls")

![alt text](figure/rpc_call2.png "RPC Message Flow: Calls")

![alt text](figure/rpc_cancel1.png "RPC Message Flow: Calls")

![alt text](figure/rpc_cancel2.png "RPC Message Flow: Calls")

![alt text](figure/rpc_progress1.png "RPC Message Flow: Calls")

![alt text](figure/rpc_provide1.png "RPC Message Flow: Calls")

![alt text](figure/rpc_provide2.png "RPC Message Flow: Calls")

![alt text](figure/pubsub_subscribe2.png "RPC Message Flow: Calls")

![alt text](figure/pubsub_publish2.png "RPC Message Flow: Calls")



## References

1. [Uniform Resource Identifier (URI): Generic Syntax, RFC 3986](http://tools.ietf.org/html/rfc3986)
2. [UTF-8, a transformation format of ISO 10646](http://tools.ietf.org/html/rfc3629)
3. [The WebSocket Protocol](http://tools.ietf.org/html/rfc6455)
4. [The application/json Media Type for JavaScript Object Notation (JSON)](http://tools.ietf.org/html/rfc4627)
5. [MessagePack Format specification](https://github.com/msgpack/msgpack/blob/master/spec.md)
