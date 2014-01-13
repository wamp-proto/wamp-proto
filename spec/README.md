# WAMP v2 Specification

This document specifies version 2 of the [WAMP](http://wamp.ws/) protocol.

## FIXME

 1. application payload types (use "embedded" / "transparent" serialization)?
 2. *Broker-to-Broker* and *Dealer-to-Dealer* message flows

## Introduction

WAMP ("Web Application Messaging Protocol") is an open application communication protocol that provides two asynchronous messaging patterns **within one** protocol:

 * Publish & Subscribe
 * Remote Procedure Calls

WAMP can run over different *transports*, including [WebSocket](http://tools.ietf.org/html/rfc6455), where it is defined as a proper, officially [registered WebSocket subprotocol](http://www.iana.org/assignments/websocket/websocket.xml).

WAMP also supports different *serialization*, including JSON and MsgPack.


## Building Blocks

WAMP is defined with respect to the following building blocks 

   1. Serialization
   2. Transport

For each building block, WAMP only assumes a defined set of requirements, which allows to run WAMP variants with different concrete bindings.


### Serialization

WAMP is a message based protocol that requires serialization of messages to octet sequences to be sent out on the wire.

A message *serialization* format is assumed that (at least) provides the following types:

  * `integer` (non-negative)
  * `string` (UTF-8 encoded Unicode)
  * `list`
  * `dict` (with string keys)

WAMP *itself* only uses above types. The application payloads transmitted by WAMP (e.g. in call arguments or event payloads) may use other types a concrete serialization format supports.

WAMPv2 defines two bindings for message *serialization*:

 1. [JSON](http://www.json.org/)
 2. [MsgPack](http://msgpack.org/)

> * As noted above, WAMP *itself* does only use a subset of types - e.g. it does not use the JSON types `number` (non-integer), `bool` and `null`.
> * With MsgPack, the [version 5](https://github.com/msgpack/msgpack/blob/master/spec.md) MUST BE supported - which is able to differentiate between strings and binary values.
> 

Other bindings for *serialization* may be defined in future WAMP versions.

#### Conversion

A MsgPack **byte array** is converted to a JSON string as follows:

1. convert the byte array to a Base64 encoded (host language) string
2. prepend the string with a `\0` character
3. serialize the string to a JSON string

*Example*

Consider the byte array (hex representation):

	10e3ff9053075c526f5fc06d4fe37cdb

This will get converted to Base64

	EOP/kFMHXFJvX8BtT+N82w==

prepended with `\0` 

	\x00EOP/kFMHXFJvX8BtT+N82w==

and serialized to a JSON string

	"\\u0000EOP/kFMHXFJvX8BtT+N82w=="

A JSON string is deserialized using the following procedure:

1. Unserialize a JSON string to a host language (Unicode) string
2. If the string starts with a `\0` character, decode the rest (after the first character) using Base64 to a byte array
3. Otherwise, return the Unicode string


### Transport

WAMP assumes a *transport* with the following characteristics:

  1. message-based
  2. reliable
  3. ordered
  4. full-duplex


#### WebSocket Transport

The default transport binding is [WebSocket](http://tools.ietf.org/html/rfc6455). With WebSocket, WAMP messages are transmitted as WebSocket messages: each WAMP message is transmitted as a separate WebSocket message (not WebSocket frame).

The WAMP protocol MUST BE negotiated during the WebSocket opening handshake between peers using the WebSocket subprotocol negotiation mechanism.

WAMPv2 uses the following WebSocket subprotocol identifiers:

 * `wamp.2.json`
 * `wamp.2.msgpack`

With `wamp.2.json`, *all* WebSocket messages MUST BE of type **text** (UTF8 encoded payload) and use the JSON message serialization.

With `wamp.2.msgpack`, *all* WebSocket messages MUST BE of type **binary** and use the MsgPack message serialization.


#### Other Transports

Besides the WebSocket transport, the following WAMP transports are under development:

 * HTTP 1.0/1.1 long-polling

Other transports such as HTTP 2.0 ("SPDY"), raw TCP or UDP might be defined in the future.


## Peer Roles

A transport connects two WAMP peers and provides a channel over which WAMP messages for a *single* WAMP session can flow in both directions.

A WAMP peer can have one or more of the following roles.

**RPC**

1. *Callee*
2. *Caller*
3. *Dealer*

*Callees* register procedures they provide with *Dealers*.

*Callers* initiate procedure calls first to *Dealers*.

*Dealers* route calls incoming from *Callers* to *Callees* implementing the procedure called.

**PubSub**

1. *Subscriber*
2. *Publisher*
3. *Broker*

*Subscribers* subscribe to topics they are interested in with *Brokers*.

*Publishers* publish events to topics at *Brokers*.

*Brokers* route events incoming from *Publishers* to *Subscribers* subscribed to the topic published to.


### Decoupling

*Dealers* are responsible for call routing decoupling *Callers* from *Callees*, whereas *Brokers* are responsible for event routing decoupling *Publishers* from *Subscribers*.


### Application Code

WAMP is designed for application code to run inside peers of the roles:

1. *Callee* and *Caller*
2. *Publisher* and *Subscriber*
 
*Brokers* and *Dealers* are responsible for generic call and event routing and SHOULD NOT run application code. The idea is to be able to transparently switch *Broker* and *Dealer* implementations without affecting the application.

*Brokers* and *Dealers* however might differ in these features:

* clustering
* high-availability and scale-out
* message persistence
* authorization schemes
* management and monitoring


### Symmetry

It's important to note that though the establishment of a transport connection might have a inherent asymmetry (like a *client* establishes a TCP and WebSocket connection to a *server*), WAMP itself is designed to be fully symmetric. After the transport has been established, both peers are equal in principle.


### Peers with multiple Roles

Peers might implement more than one role: e.g. a peer might act as *Caller*, *Publisher* and *Subscriber* at the same time. Another peer might act as both a *Broker* and a *Dealer*. And a *Dealer* might also act as a *Callee*. With the latter, a peer might "route" an incoming call directly to an implementing endpoint within the same program (and hence no actual messaging over a transport is happening).


## URIs

WAMP needs to identify the following *persistent* resources:

  1. Topics
  2. Procedures
  3. Errors

These are identified in WAMP using *Uniform Resource Identifiers* (URIs) that MUST BE UTF-8 encoded Unicode strings.

*Examples*

	com.myapp.mytopic1
	com.myapp.myprocedure1
	com.myapp.myerror1

The URIs are understood to form a single, global, hierarchical namespace for WAMP.

> The namespace is unified for topics, procedures and errors - these different resource types do NOT have separate namespaces.
> 

To avoid resource naming conflicts, we follow the package naming convention from Java where URIs SHOULD begin with (reversed) domain names owned by the organization defining the URI.

URI components (the parts between between `.`) MUST NOT contain `.` and MUST NOT be empty (zero-length strings).

> We cannot allow `.` in component strings, since `.` is used to separate components, and WAMP associates semantics with resource hierarchies such as in pattern-based subscriptions. We cannot allow empty (zero-length) strings as components, since this has special meaning to denote wildcard components with pattern-based subscriptions.

URIs MUST NOT contain `#`, which is reserved for internal use by *Dealers* and *Brokers*.

URI components SHOULD match the regular expression `[a-z][a-z0-9_]*` (that is start with a letter, followed by zero or more letters, digits or `_`).

> Following the suggested regular expression will make URI components valid identifiers in most languages (modulo language keywords) and the use of lower-case only will make those identifiers unique in languages that have case-insensitive identifiers. Following this suggestion can allow implementations to map topics, procedures and errors to the language enviroment in a completely transparent way. 

Further, application URIs MUST NOT use `wamp` as a first URI component, since this is reserved for URIs predefined with the WAMP protocol itself.


## IDs

WAMP needs to identify the following *ephemeral* entities:

 1. Sessions
 2. Requests
 3. Publications
 4. Subscriptions
 5. Registrations

These are identified in WAMP using IDs that are integers between (inclusive) `0` and `2^53` (`9007199254740992L`) and which MUST BE drawn *randomly* from a *uniform distribution* over the specified range.

> The reason to choose the specific upper bound is that `2^53` is the largest integer such that this integer and *all* (positive) smaller integers can be represented exactly in IEEE-754 doubles. Some languages (e.g. JavaScript) use doubles as their sole number type. Most languages do have signed and unsigned 64-bit integer types which both can hold any value from the specified range. 
> 


## Messages

### Overview

All WAMP messages are of the same structure - a `list` with a first element `MessageType` followed by zero or more message type specific elements:

    [MessageType|integer, ... zero or more message type specific elements ...]

The notation `Element|type` denotes a message element named `Element` of type `type`, where `type` is one of:

 * `integer`: a non-negative integer
 * `string`: any UTF-8 encoded Unicode string, including the empty string
 * `id`: an integer ID as defined above
 * `uri`: a string URI as defined above
 * `dict`: a dictionary (map)
 * `list`: a list (array)
 * `any`: any scalar or complex type the serialization supports

> Keys with above `dicts` MUST BE of type `string` and SHOULD match the regular expression `[a-z][a-z0-9_]*`
> 

**Extensibility**
Some WAMP messages contain `Options|dict` or `Details|dict` elements. This allows for future extensibility and implementations that only provide subsets of functionality by ignoring unimplemented attributes.

**Polymorphism**
For a given `MessageType`, the number of expected elements is uniquely defined. Hence there is no polymorphic messages in WAMP at all. This leads to message parsing and validation control flow that is efficient, simple to implement and simple to code for rigorous message format checking.

**Structure**
The *application* payload (that is call arguments, call results, event payload etc) are always at the end of the message element list. The rationale is: *Brokers* and *Dealers* have no need to inspect (parse) that application payloads. Their business is call/event routing. Having the application payload at the end of the list allows *Brokers* and *Dealers* skip parsing altogether. This improves efficiency/performance and probably even allows to transport encrypted application payloads transparently.

**Message Types**
WAMP defines the following messages which are explained in detail in the further sections.


### Direction

| Code | Message        | *Publisher* | *Broker* | *Subscriber* | *Caller* | *Dealer* | *Callee* |
|------|----------------|-------------|----------|--------------|----------|----------|----------|
|  1   | `HELLO`        | Tx/Rx       | Tx/Rx    | Tx/Rx        | Tx/Rx    | Tx/Rx    | Tx/Rx    |
|  2   | `GOODBYE`      | Tx/Rx       | Tx/Rx    | Tx/Rx        | Tx/Rx    | Tx/Rx    | Tx/Rx    |
|  3   | `HEARTBEAT`    | Tx/Rx       | Tx/Rx    | Tx/Rx        | Tx/Rx    | Tx/Rx    | Tx/Rx    |
|  4   | `ERROR`        | Rx          | Tx       | Rx           | Rx       | Tx/Rx    | Tx/Rx    |
| Code | Message        | *Publisher* | *Broker* | *Subscriber* | *Caller* | *Dealer* | *Callee* |
| 16   | `PUBLISH`      | Tx          | Rx       |              |          |          |          |
| 17   | `PUBLISHED`    | Rx          | Tx       |              |          |          |          |
| 32   | `SUBSCRIBE`    |             | Rx       | Tx           |          |          |          |
| 33   | `SUBSCRIBED`   |             | Tx       | Rx           |          |          |          |
| 34   | `UNSUBSCRIBE`  |             | Rx       | Tx           |          |          |          |
| 35   | `UNSUBSCRIBED` |             | Tx       | Rx           |          |          |          |
| 36   | `EVENT`        |             | Tx       | Rx           |          |          |          |
| 48   | `CALL`         |             |          |              | Tx       | Rx       |          |
| 49   | `CANCEL`       |             |          |              | Tx       | Rx       |          |
| 50   | `RESULT`       |             |          |              | Rx       | Tx       |          |
| 64   | `REGISTER`     |             |          |              |          | Rx       | Tx       |
| 65   | `REGISTERED`   |             |          |              |          | Tx       | Rx       |
| 66   | `UNREGISTER`   |             |          |              |          | Rx       | Tx       |
| 67   | `UNREGISTERED` |             |          |              |          | Tx       | Rx       |
| 68   | `INVOCATION`   |             |          |              |          | Tx       | Rx       |
| 69   | `INTERRUPT`    |             |          |              |          | Tx       | Rx       |
| 70   | `YIELD`        |             |          |              |          | Rx       | Tx       |


### Session Management

*Any-to-Any*

    [HELLO, Session|id, Details|dict]
    [GOODBYE, Details|dict]
    [HEARTBEAT, IncomingSeq|integer, OutgoingSeq|integer, Discard|string]

### Publish

*Publisher-to-Broker*

One of the following three forms of **`PUBLISH`** request:

    [PUBLISH, Request|id, Options|dict, Topic|uri]
    [PUBLISH, Request|id, Options|dict, Topic|uri, Payload|list]
    [PUBLISH, Request|id, Options|dict, Topic|uri, Payload|list, PayloadKw|dict]

*Broker-to-Publisher*

In case of success, the following **`PUBLISHED`** response:

    [PUBLISHED, PUBLISH.Request|id, Publication|id]

In case of error, one of the following three forms of **`PUBLISH_ERROR`** response:

    [PUBLISH_ERROR, PUBLISH.Request|id, Error|uri]
    [PUBLISH_ERROR, PUBLISH.Request|id, Error|uri, Exception|list]
    [PUBLISH_ERROR, PUBLISH.Request|id, Error|uri, Exception|list, ExceptionKw|dict]


### Subscribe

*Subscribe-to-Broker*

The following **`SUBSCRIBE`** request:

    [SUBSCRIBE, Request|id, Options|dict, Topic|uri]

*Broker-to-Subscribe*

In case of success, the following **`SUBSCRIBED`** response:

    [SUBSCRIBED, SUBSCRIBE.Request|id, Subscription|id]

In case of error, one of the following three forms of **`ERROR`** response:

    [ERROR, SUBSCRIBE.Request|id, Details|dict, Error|uri]
    [ERROR, SUBSCRIBE.Request|id, Details|dict, Error|uri, Arguments|list]
    [ERROR, SUBSCRIBE.Request|id, Details|dict, Error|uri, Arguments|list, ArgumentsKw|dict]


### Unsubscribe

*Subscriber-to-Broker*

The following **`UNSUBSCRIBE`** request:

    [UNSUBSCRIBE, Request|id, SUBSCRIBED.Subscription|id]

*Broker-to-Subscriber*

In case of success, the following **`UNSUBSCRIBED`** response:

    [UNSUBSCRIBED, UNSUBSCRIBE.Request|id]

In case of error, one of the following three forms of **`UNSUBSCRIBE_ERROR`** response:

    [UNSUBSCRIBE_ERROR, UNSUBSCRIBE.Request|id, Error|uri]
    [UNSUBSCRIBE_ERROR, UNSUBSCRIBE.Request|id, Error|uri, Exception|list]
    [UNSUBSCRIBE_ERROR, UNSUBSCRIBE.Request|id, Error|uri, Exception|list, ExceptionKw|dict]

### Event

*Broker-to-Subscriber*

One of the following three forms of **`EVENT`** notification:

    [EVENT, SUBSCRIBED.Subscription|id, PUBLISHED.Publication|id, Details|dict]
    [EVENT, SUBSCRIBED.Subscription|id, PUBLISHED.Publication|id, Details|dict, PUBLISH.Payload|list]
    [EVENT, SUBSCRIBED.Subscription|id, PUBLISHED.Publication|id, Details|dict, PUBLISH.Payload|list, PUBLISH.PayloadKw|dict]

### Meta Event

*Broker-to-Subscriber*

    [METAEVENT, SUBSCRIBED.Subscription|id, Publication|id, MetaTopic|uri, MetaEvent|any]

### Call

*Caller-to-Dealer*

One of the following three forms of **`CALL`** request:

    [CALL, Request|id, Options|dict, Procedure|uri]
    [CALL, Request|id, Options|dict, Procedure|uri, Arguments|list]
    [CALL, Request|id, Options|dict, Procedure|uri, Arguments|list, ArgumentsKw|dict]

*Dealer-to-Caller*

If the call yields progressive results, one of the following three forms of **`CALL_PROGRESS`**, possibly multiple times:

    [CALL_PROGRESS, CALL.Request|id, INVOCATION_PROGRESS.Details|dict]
    [CALL_PROGRESS, CALL.Request|id, INVOCATION_PROGRESS.Details|dict, INVOCATION_PROGRESS.Progress|list]
    [CALL_PROGRESS, CALL.Request|id, INVOCATION_PROGRESS.Details|dict, INVOCATION_PROGRESS.Progress|list, INVOCATION_PROGRESS.ProgressKw|dict]

If the call is successful, one of the following three forms of **`CALL_RESULT`**:

    [CALL_RESULT, CALL.Request|id, INVOCATION_RESULT.Details|dict]
    [CALL_RESULT, CALL.Request|id, INVOCATION_RESULT.Details|dict, INVOCATION_RESULT.Result|list]
    [CALL_RESULT, CALL.Request|id, INVOCATION_RESULT.Details|dict, INVOCATION_RESULT.Result|list, INVOCATION_RESULT.ResultKw|dict]

If the call fails, one of the following three forms of **`CALL_ERROR`**:

    [CALL_ERROR, CALL.Request|id, INVOCATION_ERROR.Error|uri]
    [CALL_ERROR, CALL.Request|id, INVOCATION_ERROR.Error|uri, INVOCATION_ERROR.Exception|list]
    [CALL_ERROR, CALL.Request|id, INVOCATION_ERROR.Error|uri, INVOCATION_ERROR.Exception|list, INVOCATION_ERROR.ExceptionKw|dict]


### Register

*Callee-to-Dealer*

The following `REGISTER` request:

    [REGISTER, Request|id, Options|dict, Procedure|uri]

*Dealer-to-Callee*

In case of success, the following `REGISTERED` response:

	[REGISTERED, REGISTER.Request|id, Registration|id]

In case of error, one of the following three forms of `REGISTER_ERROR`:

    [REGISTER_ERROR, REGISTER.Request|id, Error|uri]
    [REGISTER_ERROR, REGISTER.Request|id, Error|uri, Exception|list]
    [REGISTER_ERROR, REGISTER.Request|id, Error|uri, Exception|list, Exception|dict]


### Unregister

*Callee-to-Dealer*

The following `UNREGISTER` request:

    [UNREGISTER, Request|id, REGISTERED.Registration|id]

*Dealer-to-Callee*

In case of success, the following `UNREGISTERED` response:

    [UNREGISTERED, UNREGISTER.Request|id]

In case of error, one of the following three forms of `UNREGISTER_ERRROR` response:

    [UNREGISTER_ERROR, UNREGISTER.Request|id, Error|uri]
    [UNREGISTER_ERROR, UNREGISTER.Request|id, Error|uri, Exception|list]
    [UNREGISTER_ERROR, UNREGISTER.Request|id, Error|uri, Exception|list, Exception|dict]


### Invocation

*Dealer-to-Callee*

One of the following three forms of `INVOCATION` request:

    [INVOCATION, Request|id, REGISTERED.Registration|id, Details|dict]
    [INVOCATION, Request|id, REGISTERED.Registration|id, Details|dict, CALL.Arguments|list]
    [INVOCATION, Request|id, REGISTERED.Registration|id, Details|dict, CALL.Arguments|list, CALL.ArgumentsKw|dict]

*Callee-to-Dealer**

If the invocation yields progressive results, one of the following three forms of **`INVOCATION_PROGRESS`**, possibly multiple times:

    [INVOCATION_PROGRESS, INVOCATION.Request|id, Details|dict]
    [INVOCATION_PROGRESS, INVOCATION.Request|id, Details|dict, Progress|list]
    [INVOCATION_PROGRESS, INVOCATION.Request|id, Details|dict, Progress|list, INVOCATION_PROGRESS.ProgressKw|dict]

If the invoation is successful, one of the following three forms of **`INVOCATION_RESULT`**:

    [INVOCATION_RESULT, INVOCATION.Request|id, Details|dict]
    [INVOCATION_RESULT, INVOCATION.Request|id, Details|dict, Result|list]
    [INVOCATION_RESULT, INVOCATION.Request|id, Details|dict, Result|list, ResultKw|dict]

If the invocation fails, one of the following three forms of **`INVOCATION_ERROR`**:

    [INVOCATION_ERROR, INVOCATION.Request|id, Error|uri]
    [INVOCATION_ERROR, INVOCATION.Request|id, Error|uri, Exception|list]
    [INVOCATION_ERROR, INVOCATION.Request|id, Error|uri, Exception|list, Exception|dict]


### Cancel Call

*Caller-to-Dealer*

The following **`CANCEL_CALL`** request:

    [CANCEL_CALL, CALL.Request|id, Options|dict]

*Dealer-to-Callee*

    [CANCEL_INVOCATION,	INVOCATION.Request|id, Options|dict]


## Message Type Codes

	HELLO					:=  1
	GOODBYE					:=  2
	HEARTBEAT				:=  3

	SUBSCRIBE				:= 10
	SUBSCRIBED				:= 11
	SUBSCRIBE_ERROR			:= 12
	
	UNSUBSCRIBE				:= 20
	UNSUBSCRIBED			:= 21
	UNSUBSCRIBE_ERROR		:= 22
	
	PUBLISH					:= 30
	PUBLISHED				:= 31
	PUBLISH_ERROR			:= 32

	EVENT					:= 40
	METAEVENT				:= 41
	
	REGISTER				:= 50
	REGISTERED				:= 51
	REGISTER_ERROR			:= 52

	UNREGISTER				:= 60
	UNREGISTERED			:= 61
	UNREGISTER_ERROR		:= 62

	CALL					:= 70
	CANCEL_CALL				:= 71
	CALL_PROGRESS			:= 72
	CALL_RESULT				:= 73
	CALL_ERROR				:= 74

	INVOCATION				:= 80
	CANCEL_INVOCATION		:= 81
	INVOCATION_PROGRESS		:= 82
	INVOCATION_RESULT		:= 83
	INVOCATION_ERROR		:= 84


## Session Management

### Hello and Goodbye

When a WAMP session starts, the peers introduce themselves to each other by sending a `HELLO` message:

    [HELLO, Session|id, Details|dict]

 * `Session` MUST BE a randomly generated ID specific to the WAMP session for each direction. Each peer tells it connected peer the `Session` ID under which it is identified (for the lifetime of the WAMP session). 
 * `Details` is a dictionary that allows to provide additional opening information (see below).

The `HELLO` message MUST be the very first message sent by each of the two peers after the transport has been established and a peer MUST wait for the `HELLO` message to be received from the other peer before performing anything else. It is a protocol error to receive a second `HELLO` message during the lifetime of the session and the peer MUST fail the session if that happens.

The `HELLO.Session` can (later) be used for:

 * specifying lists of excluded or eligible receivers when publishing events
 * in the context of performing authentication or authorization 

*Example*

    [1, 9129137332, {... see below ...}]

A WAMP peer MUST announce the roles it supports via `Hello.Details.roles|dict`, with a key mapping to a `Hello.Details.roles.<role>|dict` where `<role>` can be:

 * `publisher`
 * `subscriber`
 * `broker`
 * `caller`
 * `callee`
 * `dealer`

A peer can support any combination of above roles but MUST support at least one role.

Further *Publisher* and *Subscriber* peers can only talk to *Broker* peers, and *Caller* and *Callee* peers can only talk to *Dealer* peers.

A *Publisher* peer cannot talk to another peer that only implements e.g. a *Callee* role.  

The `<role>|dict` is a dictionary describing features supported by the peer for that role.

The use of *feature announcement* in WAMP allows for

 * only implement subsets of functionality
 * graceful degration


*Example: A peer that can act as Publisher and Subscriber, but only supports basic features.*

	[1, 9129137332, {
		"roles": {
			"publisher": {},
			"subscriber": {}
		}
	}]

*Example: A peer that can act as a Broker and supports a couple of optional features.*

	[1, 9129137332, {
		"roles": {
			"broker": {
				"exclude": 1,
			 	"eligible": 1,
			 	"exclude_me": 1,
			 	"disclose_me": 1
			}
     	}
	}]

Similar to what browsers do with the `User-Agent` HTTP header, the `HELLO` message MAY disclose the WAMP implementation in use to it's peer:

    HELLO.Details.agent|string

*Example*

    [1, 9129137332, {"agent": "AutobahnPython-0.7.0"}]

A WAMP session starts it's lifetime when both peers have received `HELLO` from the other, and ends when the underlying transport closes or when the session is closed explicitly by sending the `GOODBYE` message

    [GOODBYE, Details|dict]

 * `Details` is a dictionary that allows to provide additional closing information (see below).

*Example*

	[2, {}]

A peer MAY provide additional details of the reason of closing and a message (intended for logging or debugging purposes):

    GOODBYE.Details.reason|uri
    GOODBYE.Details.message|string

*Example*

    [2, {"reason": "wamp.error.system_shutdown", "message": "The host is shutting down now."}]

*Example*

    [2, {"reason": "wamp.error.protocol_violation", "message": "Invalid type for 'topic' in SUBSCRIBE."}]


### Heartbeats

The heartbeat allows to keep network intermediaries from closing the underlying transport, notify the peer up to which incoming heartbeat all incoming WAMP messages have been processed, and announce an outgoing hearbeat sequence number in the same message.

A peer MAY send a `HEARTBEAT` message at any time:

    [HEARTBEAT, IncomingSeq|integer, OutgoingSeq|integer, Discard|string]

 * `HEARTBEAT.OutgoingSeq` MUST start with `1` and be incremented by `1` for each `HEARTBEAT` a peer sends.
 * `HEARTBEAT.IncomingSeq` MUST BE the sequence number from the last received heartbeat for which all previously received WAMP messages have been processed or `0` when no `HEARTBEAT` has still been received
 *  `HEARTBEAT.Discard` is an arbitrary string discarded by the peer.

> The `HEARTBEAT.Discard` can be used to exhibit some traffic volume e.g. to keep mobile radio channels in a low-latency, high-power state. The string SHOULD be a random string (otherwise compressing transports might compress away the traffic volume).
> 

*Example*

	[3, 0, 1, ""]

*Example*

	[3, 23, 5, ""]

*Example*

	[3, 23, 5, "throw me away ... I am just noise"]

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

![alt text](figure/pubsub_subscribe1.png "PubSub: Subscribing and Unsubscribing")

Upon subscribing to a topic via the `SUBSCRIBE` message, a *Subscriber* will be receiving asynchronous events published to the respective topic by *Publishers*. A subscription lasts for the duration of a session, unless a *Subscriber* opts out from a previously established subscription via the `UNSUBSCRIBE` message.

A *Subscriber* communicates it's interest in a topic to a *Broker* by sending a `SUBSCRIBE` message:

    [SUBSCRIBE, Request|id, Options|dict, Topic|uri]

 * `Request` is a random, ephemeral ID chosen by the *Subscriber* and used to correlate the *Broker's* response with the request.
 * `Options` is a dictionary that allows to provide additional subscription request details in a extensible way. This is described further below.
 * `Topic` is the topic the *Subscriber* wants to subscribe to.

A client may subscribe to zero, one or more topics, and clients publish to topics without knowledge of subscribers.

*Example*

	[10, 713845233, {}, "com.myapp.mytopic1"]

If the *Broker* is able to fulfil and allowing the subscription, it answers by sending a `SUBSCRIBED` message to the *Subscriber*

    [SUBSCRIBED, SUBSCRIBE.Request|id, Subscription|id]

 * `SUBSCRIBE.Request` is the ID from the original request.
 * `Subscription` is an ID chosen by the *Broker* for the subscription.

*Example*

	[11, 713845233, 5512315355]

> Note. The `Subscription` ID chosen by the broker may be unique only for the `Topic` (and possibly other information from `Options`, such as the topic pattern matching method to be used). The ID might be the same for any *Subscriber* for the same `Topic`. This allows the *Broker* to serialize an event to be delivered only once for all actual receivers of the event.
> 

When the request for subscription cannot be fulfilled by the *Broker*, the *Broker* sends back a `SUBSCRIBE_ERROR` message to the *Subscriber*

    [SUBSCRIBE_ERROR, SUBSCRIBE.Request|id, Error|uri]

 * `SUBSCRIBE.Request` is the ID from the original request.
 * `Error` is an URI that gives the error of why the request could not be fulfilled.

*Example*

	[12, 713845233, "wamp.error.not_authorized"]

When a *Subscriber* is no longer interested in receiving events for a subscription it sends an `UNSUBSCRIBE` message

    [UNSUBSCRIBE, Request|id, SUBSCRIBED.Subscription|id]

 * `Request` is a random, ephemeral ID chosen by the *Subscriber* and used to correlate the *Broker's* response with the request.
 * `SUBSCRIBED.Subscription` is the ID for the subscription to unsubcribe from, originally handed out by the *Broker* to the *Subscriber*.

*Example*

	[20, 85346237, 5512315355]

Upon successful unsubscription, the *Broker* sends an `UNSUBSCRIBED` message to the *Subscriber*

    [UNSUBSCRIBED, UNSUBSCRIBE.Request|id]

 * `UNSUBSCRIBE.Request` is the ID from the original request.

*Example*

	[21, 85346237]

When the request failed, the *Broker* sends an `UNSUBSCRIBE_ERROR`

    [UNSUBSCRIBE_ERROR, UNSUBSCRIBE.Request|id, Error|uri]

 * `UNSUBSCRIBE.Request` is the ID from the original request.
 * `Error` is an URI that gives the error of why the request could not be fulfilled.

*Example*

	[22, 85346237, "wamp.error.no_such_subscription"]
 

### Publishing

The message flow between *Publishers*, a *Broker* and *Subscribers* for publishing and dispatching events involves the following messages:

 1. `PUBLISH`
 2. `PUBLISHED`
 3. `PUBLISH_ERROR`
 4. `EVENT`

![alt text](figure/pubsub_publish1.png "PubSub: Publishing and Receiving")

When a *Publisher* wishes to publish an event to some topic, it sends a `PUBLISH` message to a *Broker*:

    [PUBLISH, Request|id, Options|dict, Topic|uri, Event|any]

 * `Request` is a random, ephemeral ID chosen by the *Publisher* and used to correlate the *Broker's* response with the request.
 * `Options` is a dictionary that allows to provide additional publication request details in an extensible way. This is described further below.
 * `Event` is an arbitrary application-level event payload.

*Example*

    [30, 239714735, {}, "com.myapp.mytopic1", "Hello, world!"]

*Example*

    [30, 239714735, {}, "com.myapp.mytopic1", {"color": "orange", "sizes": [23, 42, 7]}]

*Example*

    [30, 239714735, {}, "com.myapp.mytopic1", null]

If the *Broker* is able to fulfill and allowing the publication, it answers by sending a `PUBLISHED` message to the *Publisher*:

    [PUBLISHED, PUBLISH.Request|id, Publication|id]

 * `PUBLISH.Request` is the ID from the original publication request.
 * `Publication` is a ID chosen by the Broker for the publication.

*Example*

    [31, 239714735, 4429313566]

When the request for publication cannot be fulfilled by the *Broker*, the *Broker* sends back a `PUBLISH_ERROR` message to the *Publisher*

    [PUBLISH_ERROR, PUBLISH.Request|id, Error|uri]

 * `PUBLISH.Request` is the ID from the original publication request.
 * `Error` is an URI that gives the error of why the request could not be fulfilled.

*Example*

    [32, 239714735, "wamp.error.not_authorized"]

*Example*

    [32, 239714735, "wamp.error.invalid_topic"]

When a publication is successful and a *Broker* dispatches the event, it will determine a list of actual receivers for the event based on subscribers for the topic published to and possibly other information in the event (such as exclude and eligible receivers).

When a *Subscriber* was deemed to be an actual receiver, the *Broker* will send the *Subscriber* an `EVENT` message:

    [EVENT, SUBSCRIBED.Subscription|id, PUBLISHED.Publication|id, Details|dict, PUBLISH.Event|any]

 * `SUBSCRIBED.Subscription` is the ID for the subscription under which the *Subscriber* receives the event - the ID for the subscription originally handed out by the *Broker* to the *Subscriber*.
 * `PUBLISHED.Publication` is the ID of the publication of the published event.
 * `Details` is a dictionary that allows the *Broker* to provide additional event details in a extensible way. This is described further below.
`PUBLISH.Event` is the application-level payload the event has been published with.
 * `PUBLISH.Event` is the application-level event payload that was provided with the original publication request.

*Example*

	[40, 5512315355, 4429313566, {}, "Hello, world!"]

*Example*

	[40, 5512315355, 4429313566, {}, {"color": "orange", "sizes": [23, 42, 7]}]

*Example*

	[40, 5512315355, 4429313566, {}, null]


### Receiver Black- and Whitelisting

A *Publisher* MAY restrict the receivers of an event beyond those subscribed via `PUBLISH.Options.exclude|list` and `PUBLISH.Options.eligible|list`.

`PUBLISH.Options.exclude` is a list of WAMP session IDs (`integer`s) providing an explicit list of (potential) *Subscribers* that won't receive a published event, even though they might be subscribed. In other words, `PUBLISH.Options.exclude` is a blacklist of (potential) *Subscribers*.

`PUBLISH.Options.eligible` is a list of WAMP session IDs (`integer`s) providing an explicit list of (potential) *Subscribers* that are allowed to receive a published event. In other words, `PUBLISH.Options.eligible` is a whitelist of (potential) *Subscribers*.

The *Broker* will dispatch events published only to *Subscribers* that are not explicitly excluded via `PUBLISH.Options.exclude` **and** which are explicitly eligible via `PUBLISH.Options.eligible`.

*Example*

    [30, 239714735,
		{"exclude": [7891255, 1245751]},
		"com.myapp.mytopic1", "Hello, world!"]

The above event will get dispatched to all *Subscribers* of `com.myapp.mytopic1`, but NOT WAMP sessions with IDs `7891255` or `1245751` (and also not the publishing session).

*Example*

    [30, 239714735,
		{"eligible": [7891255, 1245751]},
		"com.myapp.mytopic1", "Hello, world!"]

The above event will get dispatched to WAMP sessions with IDs `7891255` or `1245751` only - but only if those are subscribed to the topic `com.myapp.mytopic1`.

*Example*

    [30, 239714735,
		{"exclude": [7891255], "eligible": [7891255, 1245751, 9912315]},
		"com.myapp.mytopic1", "Hello, world!"]

The above event will get dispatched to WAMP sessions with IDs `1245751` or `9912315` only (since `7891255` is excluded) - but only if those are subscribed to the topic `com.myapp.mytopic1`.


### Publisher Exclusion

By default, a *Publisher* of an event will **not** receive an event published itself, even when subscribed to the `Topic` the *Publisher* is publishing to. This behavior can be overridden via `PUBLISH.Options.exclude_me|integer`.

`PUBLISH.Options.exclude_me` must be a `integer` with value either `0` or `1`. When publishing with `PUBLISH.Options.exclude_me == 0`, the *Publisher* of the event will receive that very event also if it is subscribed to the `Topic` published to.

*Example*

    [30, 239714735, {"exclude_me": 0}, "com.myapp.mytopic1", "Hello, world!"]

In this example, the *Publisher* will receive the published event also, if it is subscribed to `com.myapp.mytopic1`.


### Publisher Identification

A *Publisher* MAY **request** the disclosure of it's identity (it's WAMP session ID) to receivers of a published event via `PUBLISH.Options.disclose_me|integer`:

*Example*

    [30, 239714735, {"disclose_me": 1}, "com.myapp.mytopic1", "Hello, world!"]

If above event would have been published by a *Publisher* with WAMP session ID `3335656`, the *Broker* would send an `EVENT` message to *Subscribers* with the *Publisher's* WAMP session ID in `Details.publisher`:

*Example*

	[40, 5512315355, 4429313566, {"publisher": 3335656}, "Hello, world!"]

Note that a *Broker* MAY disclose the identity of a *Publisher* even without the *Publisher* having explicitly requested to do so when the *Broker* configuration (for the publication topic) is setup to do so.

A *Broker* MAY deny a *Publisher's* request to disclose it's identity:

*Example*

    [32, 239714735, "wamp.error.disclose_me.not_allowed"]


### Publication Trust Levels

A *Broker* may be configured to automatically assign *trust levels* to events published by *Publishers* according to the *Broker* configuration on a per-topic basis and/or depending on the application defined role of the (authenticated) *Publisher*.

A *Broker* must use `Details.trustlevel|integer` in an `EVENT` message sent to a *Subscriber*. The trustlevel `0` means lowest trust, and higher integers represent (application-defined) higher levels of trust.

*Example*

	[40, 5512315355, 4429313566, {"trustlevel": 2}, "Hello, world!"]

In above event, the *Broker* has (by configuration and/or other information) deemed the event publication to be of `trustlevel == 2`.


### Pattern-based Subscriptions

By default, *Subscribers* subscribe to topics with **exact matching policy**. That is an event will only be dispatched to a *Subscriber* by the *Broker* if the topic published to (`PUBLISH.Topic`) matches *exactly* the topic subscribed to (`SUBSCRIBE.Topic`).

A *Subscriber* might want to subscribe to topics based on a *pattern*. This can be useful to reduce the number of individual subscriptions to be set up and to subscribe to topics the *Subscriber* does not know exactly.

If the *Broker* and the *Subscriber* support **pattern-based subscriptions**, this matching can happen by

 * prefix-matching policy
 * wildcard-matching policy

*Brokers* and *Subscribers* MUST announce support for non-exact matching policies in the `HELLO.Options` (see that chapter).

A *Subscriber* requests **prefix-matching policy** with a subscription request by setting `SUBSCRIBE.Options.match|string == "prefix"`.

*Example*

	[10, 912873614, {"match": "prefix"}, "com.myapp.topic.emergency"]

When a **prefix-matching policy** is in place, any event with a topic that has `SUBSCRIBE.Topic` as a *prefix* will match the subscription, and potentially delivered to *Subscribers* on the subscription.

In above example, events with `PUBLISH.Topic` e.g. `com.myapp.topic.emergency.11`, `com.myapp.topic.emergency-low`, `com.myapp.topic.emergency.category.severe` and `com.myapp.topic.emergency` will all apply for dispatching. An event with `PUBLISH.Topic` e.g. `com.myapp.topic.emergenc` will NOT apply.

The *Broker* will apply the prefix-matching based on the UTF-8 encoded byte string for the `PUBLISH.Topic` and the `SUBSCRIBE.Topic`.

A *Subscriber* requests **wildcard-matching policy** with a subscription request by setting `SUBSCRIBE.Options.match|string == "wildcard"`.

Wildcard-matching allows to provide wildcards for **whole** URI components.

*Example*

	[10, 912873614, {"match": "wildcard"}, "com.myapp..userevent"]

In above subscription request, the 3rd URI component is empty, which signals a wildcard in that URI component position. In this example, events with `PUBLISH.Topic` e.g. `com.myapp.foo.userevent`, `com.myapp.bar.userevent` or `com.myapp.a12.userevent` will all apply for dispatching. Events with `PUBLISH.Topic` e.g. `com.myapp.foo.userevent.bar`, `com.myapp.foo.user` or `com.myapp2.foo.userevent` will NOT apply for dispatching.

When a single event matches more than one of a *Subscribers* subscriptions, the event will be delivered for each subscription. The *Subscriber* can detect the delivery of that same event on multiple subscriptions via `EVENT.PUBLISHED.Publication`, which will be identical.

Since each *Subscribers* subscription "stands on it's own", there is no *set semantics* implied by pattern-based subscriptions. E.g. a *Subscriber* cannot subscribe to a broad pattern, and then unsubscribe from a subset of that broad pattern to form a more complex subscription. Each subscription is separate.

If a subscription was established with a pattern-based matching policy, a *Broker* MUST supply the original `PUBLISH.Topic` as provided by the *Publisher* in `EVENT.Details.topic` to the *Subscribers*. 


### Partitioned Subscriptions & Publications

Resource keys: `PUBLISH.Options.rkey|string` is a stable, technical **resource key**.

> E.g. if your sensor as a unique serial identifier, you can use that.


*Example*

    [30, 239714735, {"rkey": "sn239019"}, "com.myapp.sensor.sn239019.temperature", 33.9]


Node keys: `SUBSCRIBE.Options.nkey|string` is a stable, technical **node key**.

> E.g. if your backend process runs on a dedicated host, you can use it's hostname.


*Example*

	[10, 912873614, {"match": "wildcard", "nkey": "node23"}, "com.myapp.sensor..temperature"]


### Meta Events

*Example*

	[10, 713845233,
         {"metatopics": ["wamp.metatopic.subscriber.add",
                         "wamp.metatopic.subscriber.remove"]},
         "com.myapp.mytopic1"]

If above subscription request by a *Subscriber 1* succeeds, the *Broker* will dispatch meta events to *Subscriber 1* for every *Subscriber 2, 3, ..* added to or removed from a subscription for `com.myapp.mytopic1`. It will also dispatch "normal" events on the topic `com.myapp.mytopic1` to *Subscriber 1*.

*Example*

	[10, 713845233,
         {"metatopics": ["wamp.metatopic.subscriber.add",
                         "wamp.metatopic.subscriber.remove"],
          "metaonly": 1},
         "com.myapp.mytopic1"]

This subscription works like the previous one, except that "normal" events on the topic `com.myapp.mytopic1` will NOT be dispatched to *Subscriber 1*. Consequently, it is called a "Meta Event only subscription".


Metaevents are always generated by the *Broker* itself:

    [METAEVENT, SUBSCRIBED.Subscription|id, Publication|id, MetaTopic|uri, MetaEvent|any]

*Example*

	[41, 5512315355, 71415664, "wamp.metatopic.subscriber.add", 71254637]

*Example*

	[41, 5512315355, 35262477, "wamp.metatopic.subscriber.remove", 71254637]


Getting initial (current) list of subscribers


	[10, 713845233,
         {"metatopics": ["wamp.metatopic.subscriber.current",
                         "wamp.metatopic.subscriber.add",
                         "wamp.metatopic.subscriber.remove"]},
         "com.myapp.mytopic1"]


Metatopics

    wamp.metatopic.subscriber.add
    wamp.metatopic.subscriber.remove
	wamp.metatopic.subscriber.current
    wamp.metatopic.publication.error.not_authorized
    wamp.metatopic.publication.statistic.total


### Subscriber List

A *Broker* may allow to retrieve the current list of *Subscribers* for a subscription.

A *Broker* that implements *subscriber list* must (also) announce role `HELLO.roles.callee`, indicate `HELLO.roles.broker.subscriberlist == 1` and provide the following (builtin) procedures.


A *Caller* (that is also a *Subscriber*) can request the current list of subscribers for a subscription (it is subscribed to) by calling the *Broker* procedure

	wamp.broker.subscriber.list

with `Arguments = [subscription|id]` where

 * `subscription` is the ID of the subscription as returned from `SUBSCRIBED.Subscription`

and `Result = sessions|list` where

 * `sessions` is a list of WAMP session IDs currently subscribed to the given subscription.

A call to `wamp.broker.subscriber.list` may fail with

	wamp.error.no_such_subscription
	wamp.error.not_authorized


*FIXME*

 1. What if we have multiple *Brokers* (a cluster)?
 2. Should we allow "paging" (`offset|integer` and `limit|integer` arguments)?
 3. Should we allow *Subscribers* to list subscribers for subscription it is not itself subscribed to?


### Event History

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
 * `publication` indicates the number of last N events to retrieve


*FIXME*

 1. Should we use `topic|uri` or `subscription|id` in `Arguments`?
 2. Can `wamp.topic.history.after` be implemented (efficiently) at all?
 3. How does that interact with pattern-based subscriptions?


## Remote Procedure Calls

### Registering and Unregistering

The message flow between *Callees* and a *Dealer* for registering and unregistering endpoints to be called over RPC involves the following messages:

 1. `REGISTER`
 2. `REGISTERED`
 3. `REGISTER_ERROR`
 4. `UNREGISTER`
 5. `UNREGISTERED`
 6. `UNREGISTER_ERROR`

![alt text](figure/rpc_register1.png "RPC: Registering and Unregistering")

A *Callee* announces the availability of an endpoint implementing a procedure with a *Dealer* by sending a `REGISTER` message:

    [REGISTER, Request|id, Options|dict, Procedure|uri]

 * `Request` is a random, ephemeral ID chosen by the *Callee* and used to correlate the *Dealer's* response with the request.
 * `Options` is a dictionary that allows to provide additional registration request details in a extensible way. This is described further below.
 * `Procedure`is the procedure the *Callee* wants to register

*Example*

	[50, 25349185, {}, "com.myapp.myprocedure1"]

If the *Dealer* is able to fulfill and allowing the registration, it answers by sending a `REGISTERED` message to the `Callee`:

	[REGISTERED, REGISTER.Request|id, Registration|id]

 * `REGISTER.Request` is the ID from the original request.
 *  `Registration` is an ID chosen by the *Dealer* for the registration.

*Example*

	[51, 25349185, 2103333224]

When the request for registration cannot be fullfilled by the *Dealer*, the *Dealer* send back a `REGISTER_ERROR` message to the *Callee*:

    [REGISTER_ERROR, REGISTER.Request|id, Error|uri]

 * `REGISTER.Request` is the ID from the original request.
 * `Error` is an URI that gives the error of why the request could not be fulfilled.

*Example*

	[52, 25349185, "wamp.error.procedure_already_exists"]

When a *Callee* is no longer willing to provide an implementation of the registered procedure, it send an `UNREGISTER` message to the *Dealer*:

    [UNREGISTER, Request|id, REGISTERED.Registration|id]

 * `Request` is a random, ephemeral ID chosen by the *Callee* and used to correlate the *Dealer's* response with the request.
 * `REGISTERED.Registration` is the ID for the registration to revoke, originally handed out by the *Dealer* to the *Callee*.

*Example*

	[60, 788923562, 2103333224]

Upon successful unregistration, the *Dealer* send an `UNREGISTERED` message to the *Callee*:

    [UNREGISTERED, UNREGISTER.Request|id]

 * `UNREGISTER.Request` is the ID from the original request.

*Example*

	[61, 788923562]

When the unregistration request failed, the *Dealer* send an `UNREGISTER_ERROR` message:

    [UNREGISTER_ERROR, UNREGISTER.Request|id, Error|uri]

 * `UNREGISTER.Request` is the ID from the original request.
 * `Error` is an URI that gives the error of why the request could not be fulfilled.

*Example*

	[62, 788923562, "wamp.error.no_such_registration"]


### Calling

The message flow between *Callers*, a *Dealer* and *Callees* for calling remote procedures involves the following messages:

 1. `CALL`
 1. `INVOCATION`
 1. `INVOCATION_RESULT`
 1. `INVOCATION_ERROR`
 1. `CALL_RESULT`
 1. `CALL_ERROR`

![alt text](figure/rpc_call1.png "RPC: Calling")

The execution of remote procedure calls is asynchronous, and there may be more than one call outstanding. A call is called outstanding (from the point of view of the *Caller*), when a (final) result or error has not yet been received by the *Caller*.

When a *Callee* wishes to call a remote procedure, it sends a `CALL` message to a *Dealer*:

    [CALL, Request|id, Options|dict, Procedure|uri, Arguments|list, ArgumentsKw|dict]

 * `Request` is a random, ephemeral ID chosen by the *Callee* and used to correlate the *Dealer's* response with the request.
 * `Options` is a dictionary that allows to provide additional call request details in an extensible way. This is described further below.
 * `Procedure` the URI of the procedure to be called.
 * `Arguments` is a list of positional call arguments (each of arbitrary type). The list may be of zero length.
 * `ArgumentsKw` is a dictionary of keyword call arguments (each of arbitrary type). The dictionary may be empty.

*Example*

	[70, 7814135, {}, "com.myapp.echo", ["Hello, world!"], {}]

*Example*

	[70, 7814135, {}, "com.myapp.add2", [23, 7], {}]

*Example*

	[70, 7814135, {}, "com.myapp.ping", [], {}]

*Example*

	[70, 7814135, {}, "com.myapp.user.new", ["johnny"], {"forname": "John", "surname": "Doe"}]

If the *Dealer* is able to fullfill (mediate) and allowing the call, it sends a `INVOCATION` message to the respective *Callee* implementing the procedure:

    [INVOCATION, Request|id, REGISTERED.Registration|id, Details|dict,
		CALL.Arguments|list, CALL.ArgumentsKw|dict]

 * `Request` is a random, ephemeral ID chosen by the *Dealer* and used to correlate the *Callee's* response with the request.
 * `REGISTERED.Registration` is the registration ID under which the procedure was registered at the *Dealer*.
 * `Details` is a dictionary that allows to provide additional invocation request details in an extensible way. This is described further below.
 * `CALL.Arguments` is the original list of positional call arguments as provided by the *Caller*.
 * `CALL.ArgumentsKw` is the original dictionary of keyword call arguments as provided by the *Caller*.

*Example*

	[80, 6131533, 9823526, {}, ["Hello, world!"], {}]

If the *Callee* is able to successfully process and finish the execution of the call, it answers by sending a `INVOCATION_RESULT` message to the *Dealer*:

    [INVOCATION_RESULT, INVOCATION.Request|id, Result|list, ResultKw|dict]

 * `INVOCATION.Request` is the ID from the original invocation request.
 * `Result` is a list of positional result elements (each of arbitrary type). The list may be of zero length.
 * `ResultKw` is a dictionary of keyword result elements (each of arbitrary type). The dictionary may be empty.

The *Dealer* will then send a `CALL_RESULT` message to the original *Caller*:

    [CALL_RESULT, CALL.Request|id, INVOCATION_RESULT.Result|list, INVOCATION_RESULT.ResultKw|dict]

 * `CALL.Request` is the ID from the original call request.
 * `INVOCATION_RESULT.Result` is the original list of positional result elements as returned by the *Callee*.
 * `INVOCATION_RESULT.ResultKw` is the original dictionary of keyword result elements as returned by the *Callee*.

If the *Callee* is unable to process or finish the execution of the call, or the application code implementing the procedure raises an exception or otherwise runs into an error, the *Callee* sends an `INVOCATION_ERROR` message to the *Dealer*:

    [INVOCATION_ERROR, INVOCATION.Request|id, Error|uri, Exception|any]

 * `INVOCATION.Request` is the ID from the original call request.
 * `Error` is an URI that gives the error of why the request could not be fulfilled.
 * `Exception` is an arbitrary application-defined error payload (possible empty, that is `null`).

The *Dealer* will then send a `CALL_ERROR` message to the original *Caller*:

    [CALL_ERROR, CALL.Request|id, INVOCATION_ERROR.Error|uri, INVOCATION_ERROR.Exception|any]

 * `CALL.Request` is the ID from the original call request.
 * `INVOCATION_ERROR.Error` is the original error URI as returned by the *Callee* to the *Dealer*.
 * `INVOCATION_ERROR.Exception` is the original error payload as returned by the *Callee* to the *Dealer*.

If the original call already failed at the *Dealer* **before** the call would have been forwarded to any *Callee*, the *Dealer* also (and immediately) sends a `CALL_ERROR` message to the *Caller*:

    [CALL_ERROR, CALL.Request|id, Error|uri, Exception|null]

*Example*

	[74, 7814135, "wamp.error.no_such_procedure", null]


### Call Timeouts

A *Caller* might want to issue a call providing a *timeout* for the call to finish.

A *timeout* allows to **automatically** cancel a call after a specified time either at the *Callee* or at the *Dealer*.

A *Callee* specifies a timeout by providing `CALL.Options.timeout|integer` in ms. A timeout value of `0` deactivates automatic call timeout. This is also the default value. 

The timeout option is a companion to, but slightly different from the `CANCEL_CALL` and `CANCEL_INVOCATION` messages that allow a *Caller* and *Broker* to **actively** cancel a call.

In fact, a timeout timer might run at three places:

 * *Caller*
 * *Dealer*
 * *Callee*


### Canceling Calls

A *Caller* might want to actively cancel a call that was issued, but not has yet returned. An example where this is useful could be a user triggering a long running operation and later changing his mind or no longer willing to wait.

The message flow between *Callers*, a *Dealer* and *Callees* for canceling remote procedure calls involves the following messages:

 * `CANCEL_CALL`
 * `CANCEL_INVOCATION`

A call may be cancelled at the *Callee*

![alt text](figure/rpc_cancel1.png "RPC Message Flow: Calls")

A call may be cancelled at the *Dealer*

![alt text](figure/rpc_cancel2.png "RPC Message Flow: Calls")

A *Callee* cancels an remote procedure call initiated (but not yet finished) by sending a `CANCEL_CALL` message to the *Dealer*:

    [CANCEL_CALL, CALL.Request|id, Options|dict]

A *Dealer* cancels an invocation of an endpoint initiated (but not yet finished) by sending a `CANCEL_INVOCATION` message to the *Callee*:

    [CANCEL_INVOCATION,		INVOCATION.Request|id, Options|dict]

Options:

	CANCEL_CALL.Options.mode|string == "skip" | "kill" | "killnowait"


### Progressive Call Results

A procedure implemented by a *Callee* and registered at a *Dealer* may produce progressive results (incrementally). The message flow for progressive results involves:

 * `INVOCATION_PROGRESS`
 * `CALL_PROGRESS`

![alt text](figure/rpc_progress1.png "RPC Message Flow: Calls")

An implementing procedure produces progressive results by sending `INVOCATION_PROGRESS` messages to the *Dealer*

    [INVOCATION_PROGRESS, INVOCATION.Request|id, Progress|list, ProgressKw|dict]

Upon receiving an `INVOCATION_PROGRESS` message from a *Callee* (for a call that is still ongoing), the *Dealer* will immediately send a `CALL_PROGRESS` message to the original *Caller*:

    [CALL_PROGRESS, CALL.Request|id, INVOCATION_PROGRESS.Progress|list, INVOCATION_PROGRESS.ProgressKw|dict]

Nevertheless, a call will *always* end in either a `CALL_RESULT` or `CALL_ERROR` message being sent by the *Dealer* and received by the *Caller* and an invocation will *always* end in either a `INVOCATION_RESULT` or `INVOCATION_ERROR` message being sent by the *Callee* and received by the *Dealer*.

In other words: `CALL_PROGRESS` and `INVOCATION_PROGRESS` messages may only be sent *during* a call or invocation is still on the fly.

If the *Caller* does not support *progressive calls* (as indicated by `HELLO.Details.roles.caller.progressive == 0`), the *Dealer* will gather all individual results receveived by the *Callee* via `INVOCATION_PROGRESS` and the final `INVOCATION_RESULT` into a list and return that as the single result to the *Caller*

*FIXME*

 1. How to handle `ResultKw` in this context?


### Distributed Calls

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

If `CALL.Options.runmode == "gather"` (the default, when `CALL.Options.runmode` is missing), the *Dealer* will gather the individual results received via `INVOCATION_RESULT` messages from *Callees* into a single list, and return that in `CALL_RESULT` to the original *Caller* - when all results have been received.

If `CALL.Options.runmode == "progressive"`, the *Dealer* will call each endpoint via a standard `INVOCATION` message and immediately forward individual results received via `INVOCATION_RESULT` messages from the *Callees* as `CALL_PROGRESS` messages to the original *Caller* and send a final `CALL_RESULT` message (with empty result) when all individual results have been received.

If any of the individual `INVOCATION`s returns an `INVOCATION_ERROR`, the further behavior depends on ..

Fail immediate:

The *Dealer* will immediately return a `CALL_ERROR` message to the *Caller* with the error from the `INVOCATION_RESULT` message of the respective failing call. It will further send `CANCEL_INVOCATION` messages to all *Callees* for which it not yet has received a response, and ignore any `INVOCATION_RESULT` or `INVOCATION_ERROR` messages it might receive subsequently for the pending calls.

The *Dealer* will accumulate ..


#### "Partitioned" Calls

If `CALL.Options.runmode == "partition"`, then `CALL.Options.rkey` MUST be present.

The call is then routed to all endpoints that were registered ..

The call is then processed as for "All" Calls.


### Pattern-based Registrations

By default, *Callees* register procedures with **exact matching policy**. That is a call will only be routed to a *Callee* by the *Dealer* if the procedure called (`CALL.Procedure`) matches *exactly* the endpoint registered (`REGISTER.Procedure`).

A *Callee* might want to register procedures based on a *pattern*. This can be useful to reduce the number of individual registrations to be set up.

If the *Dealer* and the *Callee* support **pattern-based registrations**, this matching can happen by

 * prefix-matching policy
 * wildcard-matching policy

*Dealers* and *Callees* MUST announce support for non-exact matching policies in the `HELLO.Options` (see that chapter).

A *Callee* requests **prefix-matching policy** with a registration request by setting `REGISTER.Options.match|string == "prefix"`.

*Example*

	[50, 612352435, {"match": "prefix"}, "com.myapp.myobject1"]

When a **prefix-matching policy** is in place, any call with a procedure that has `REGISTER.Procedure` as a *prefix* will match the registration, and potentially be routed to *Callees* on taht registration.

In above example, calls with `CALL.Procedure` e.g. `com.myapp.myobject1.myprocedure1`, `com.myapp.myobject1-mysubobject1`, `com.myapp.myobject1.mysubobject1.myprocedure1` and `com.myapp.myobject1` will all apply for call routing. A call with `CALL.Procedure` e.g. `com.myapp.myobject2` or `com.myapp.myobject` will NOT apply.

The *Dealer* will apply the prefix-matching based on the UTF-8 encoded byte string for the `CALL.Procedure` and the `REGISTER.Procedure`.

A *Callee* requests **wildcard-matching policy** with a registration request by setting `REGISTER.Options.match|string == "wildcard"`.

Wildcard-matching allows to provide wildcards for **whole** URI components.

*Example*

	[50, 612352435, {"match": "wildcard"}, "com.myapp..myprocedure1"]

In above registration request, the 3rd URI component is empty, which signals a wildcard in that URI component position. In this example, calls with `CALL.Procedure` e.g. `com.myapp.myobject1.myprocedure1` or `com.myapp.myobject2.myprocedure1` will all apply for call routing. Calls with `CALL.Procedure` e.g. `com.myapp.myobject1.myprocedure1.mysubprocedure1`, `com.myapp.myobject1.myprocedure2` or `com.myapp2.myobject1.myprocedure1` will NOT apply for call routing.

When a single call matches more than one of a *Callees* registrations, the call MAY be routed for invocation on multiple registrations, depending on call settings.

FIXME: The *Callee* can detect the invocation of that same call on multiple registrations via `INVOCATION.CALL.Request`, which will be identical.

Since each *Callees* registrations "stands on it's own", there is no *set semantics* implied by pattern-based registrations. E.g. a *Callee* cannot register to a broad pattern, and then unregister from a subset of that broad pattern to form a more complex registration. Each registration is separate.

If an endpoint was registered with a pattern-based matching policy, a *Dealer* MUST supply the original `CALL.Procedure` as provided by the *Caller* in `INVOCATION.Details.procedure` to the *Callee*. 


### Caller Identification

A *Caller* MAY **request** the disclosure of it's identity (it's WAMP session ID) to endpoints of a routed call via `CALL.Options.disclose_me|integer`:

*Example*

	[70, 7814135, {"disclose_me": 1}, "com.myapp.echo", ["Hello, world!"], {}]

If above call would have been issued by a *Caller* with WAMP session ID `3335656`, the *Dealer* would send an `INVOCATION` message to *Callee* with the *Caller's* WAMP session ID in `INVOCATION.Details.caller`:

*Example*

	[80, 6131533, 9823526, {"caller": 3335656}, "com.myapp.echo", ["Hello, world!"], {}]

Note that a *Dealer* MAY disclose the identity of a *Caller* even without the *Caller* having explicitly requested to do so when the *Dealer* configuration (for the called procedure) is setup to do so.

A *Dealer* MAY deny a *Caller's* request to disclose it's identity:

*Example*

    [32, 7814135, "wamp.error.disclose_me.not_allowed"]


## Ordering Guarantees

### Publish & Subscribe Ordering

Regarding **Publish & Subscribe**, the ordering guarantees are as follows:

If *Subscriber A* is subscribed to both **Topic 1** and **Topic 2**, and *Publisher B* first publishes an **Event 1** to **Topic 1** and then an **Event 2** to **Topic 2**, then *Subscriber A* will first receive **Event 1** and then **Event 2**. This also holds if **Topic 1** and **Topic 2** are identical.

In other words, WAMP guarantees ordering of events between any given *pair* of *Publisher* and *Subscriber*.

Further, if *Subscriber A* subscribes to **Topic 1**, the `SUBSCRIBED` message will be sent by *Broker* to *Subscriber A* before any `EVENT` message for **Topic 1**.

In general, `SUBSCRIBE` is asynchronous, and there is no guarantee on order of return for multiple `SUBSCRIBEs`. The first `SUBSCRIBE` might require the *Broker* to do a time-consuming lookup in some database, whereas the second might be permissible immediately.


### Remote Procedure Call Ordering

Regarding **Remote Procedure Calls**, the ordering guarantees are as follows:

If *Callee A* has registered endpoints for both **Procedure 1** and **Procedure 2**, and *Caller B* first issues a **Call 1** to **Procedure 1** and then a **Call 2** to **Procedure 2**, and both calls are routed to *Callee A*, then *Callee A* will first receive an invocation corresponding to **Call 1** and then **Call 2**. This also holds if **Procedure 1** and **Procedure 2** are identical.

In other words, WAMP guarantees ordering of invocations between any given *pair* of *Caller* and *Callee*.

In general, there are no guarantees on the order of call results and errors in relation to calls, since the execution of calls upon invocation of endpoints in *Callees* is asynchronous. A first call might require an expensive, long-running computation, whereas a second, subsequent call might finish immediately.

Further, if *Callee A* registers for **Procedure 1**, the `REGISTERED` message will be sent by *Dealer* to *Callee A* before any `INVOCATION` message for **Procedure 1**.

In general, `REGISTER` is asynchronous, and there is no guarantee on order of return for multiple `REGISTERs`. The first `REGISTER` might require the *Dealer* to do a time-consuming lookup in some database, whereas the second might be permissible immediately.


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

	HELLO.Details.roles.broker.reflection|integer == 1

A peer that acts as a *Dealer* SHOULD announce support for the reflection API by sending

	HELLO.Details.roles.dealer.reflection|integer == 1

> Since *Brokers* might provide (broker) procedures and *Dealers* might provide (dealer) topics, both SHOULD implement the complete API above (even if the peer only implements one of *Broker* or *Dealer* roles).
> 


## Authentication

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


### WAMP-CRA Authentication

WAMP Challenge Response (WAMP-CRA) is a WAMP level authentication procedure implemented on top of standard, predefined WAMP RPC procedures.

A peer may authenticate to it's other peer via calling the following procedures

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


## Appendix

### Byte Array Conversion

#### Python

Here is a complete example in **Python** showing how byte arrays are converted to and from JSON:

```python
import os, base64, json, sys, binascii
PY3 = sys.version_info >= (3,)
if PY3:
   unicode = str

data_in = os.urandom(16)
print("In:   {}".format(binascii.hexlify(data_in)))

## encoding
encoded = json.dumps('\0' + base64.b64encode(data_in).decode('ascii'))

print("JSON: {}".format(encoded))

## decoding
decoded = json.loads(encoded)
if type(decoded) == unicode:
   if decoded[0] == '\0':
      data_out = base64.b64decode(decoded[1:])
   else:
      data_out = decoded

print("Out:  {}".format(binascii.hexlify(data_out)))

assert(data_out == data_in)
```

#### JavaScript

Here is a complete example in **JavaScript** showing how byte arrays are converted to and from JSON:

```javascript
var data_in = new Uint8Array(new ArrayBuffer(16));

// initialize test data
for (var i = 0; i < data_in.length; ++i) {
   data_in[i] = i;
}
console.log(data_in);

// convert byte array to raw string
var raw_out = '';
for (var i = 0; i < data_in.length; ++i) {
   raw_out += String.fromCharCode(data_in[i]);
}

// base64 encode raw string, prepend with \0 and serialize to JSON
var encoded = JSON.stringify("\0" + window.btoa(raw_out));
console.log(encoded); // "\u0000AAECAwQFBgcICQoLDA0ODw==" 

// unserialize from JSON
var decoded = JSON.parse(encoded);

var data_out;
if (decoded.charCodeAt(0) === 0) {
   // strip first character and decode base64 to raw string
   var raw = window.atob(decoded.substring(1));

   // convert raw string to byte array
   var data_out = new Uint8Array(new ArrayBuffer(raw.length));
   for (var i = 0; i < raw.length; ++i) {
      data_out[i] = raw.charCodeAt(i);
   }
} else {
   data_out = decoded;
}

console.log(data_out);
```


## References

1. [Uniform Resource Identifier (URI): Generic Syntax, RFC 3986](http://tools.ietf.org/html/rfc3986)
2. [UTF-8, a transformation format of ISO 10646](http://tools.ietf.org/html/rfc3629)
3. [The WebSocket Protocol](http://tools.ietf.org/html/rfc6455)
4. [The application/json Media Type for JavaScript Object Notation (JSON)](http://tools.ietf.org/html/rfc4627)
5. [MessagePack Format specification](https://github.com/msgpack/msgpack/blob/master/spec.md)
6. [Consistent Hashing and Random Trees: Distributed Caching Protocols for Relieving Hot Spots on the World Wide Web (1997)](http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.23.3738) 
7. [Web Caching with Consistent Hashing](http://www8.org/w8-papers/2a-webserver/caching/paper2.html)


<!--
![alt text](figure/rpc_call2.png "RPC Message Flow: Calls")
![alt text](figure/rpc_provide2.png "RPC Message Flow: Calls")
![alt text](figure/pubsub_subscribe2.png "RPC Message Flow: Calls")
![alt text](figure/pubsub_publish2.png "RPC Message Flow: Calls")

http://docs.oracle.com/javase/specs/jls/se5.0/html/packages.html#7.7
http://en.wikipedia.org/wiki/Java_package
http://docs.oracle.com/javase/tutorial/java/package/namingpkgs.html
-->