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

The default transport binding is [WebSocket](http://tools.ietf.org/html/rfc6455). With WebSocket, WAMP messages are transmitted as WebSocket messages: each WAMP message is transmitted as a separate WebSocket message (not WebSocket frame).

The WAMP protocol MUST BE negotiated during the opening WebSocket handshakes between peers using the WebSocket subprotocol negotiation mechanism.

WAMPv2 uses the following WebSocket subprotocol identifiers:

 * `wamp.2.json`
 * `wamp.2.msgpack`

With `wamp.2.json`, all WebSocket messages MUST BE of type **text** (UTF8 encoded payload) and use the JSON message serialization.

With `wamp.2.msgpack`, all WebSocket messages MUST BE of type **binary** and use the MsgPack message serialization.

With both WAMP WebSocket subprotocols, the namespace binding MUST BE URIs from the HTTP scheme as described above.

Besides the WebSocket transport, the following WAMP transports are under development:

 * HTTP 1.0/1.1 long-polling
 * HTTP 2.0 ("SPDY")

Other transports might be defined in the future.


## Peer Roles

A transport connect two WAMP peers and provides a channel over which WAMP messages can flow in both directions.

A WAMP peer can have one or more of the following roles.

**RPC**

1. Callee
2. Caller
3. Dealer

*Callee*s register procedures they provide with *Dealer*s.

*Caller*s initiate procedure calls first to *Dealer*s.

*Dealer*s route call incoming from *Caller*s to *Callee*s implementing the procedure called.

**PubSub**

1. Subscriber
2. Publisher
3. Broker

*Subscriber*s subscribe to topics they are interested in with *Broker*s.

*Publisher*s publish events to topics at *Broker*s.

*Broker*s route events incoming from *Publisher*s to *Subscriber*s subscribed to the topic published to.

### Decoupling

*Dealers* are responsible for call routing decoupling *Callers* from *Callees*, whereas *Brokers* are responsible for event routing decoupling *Publishers* from *Subscribers*.

### Symmetry

It's important to note that though the establishment of a transport connection might have a inherent asymmetry (like a *client* establishes a TCP and WebSocket connection to a *server*), WAMP itself is designed to be fully symmetric. After the transport has been established, both peers are equal in principle.

### Peers with multiple Roles

Peers might implement more than one role: e.g. a peer might act as `Caller`, `Publisher` and `Subscriber` at the same time. Another peer might act as both a `Broker` and a `Dealer`. And a `Dealer` might also act as a `Callee`. With the latter, a peer might "route" an incoming call directly to an implementing endpoint within the same program (and hence no actual messaging is happening).


## Messages

### Overview

All WAMP messages are of the same structure:

    [MessageType|integer, ... one or more message type specific arguments ...]

A `list` with a first element `MessageType` followed by one or more message type specific elements.

The notation `Element|type` denotes a message element named `Element` of type `type`:

 * `integer`: a non-negative integer
 * `string`: any UTF8-encoded string, including the empty string
 * `id`: a random (positive) integer
 * `uri`: an UTF8- and percent-encoded string that is a valid URI
 * `dict`: a dictionary (map) with `string` typed keys
 * `list`: a list (array)

WAMP defines the following messages which are explained in detail in the further sections.


### Session Management

#### Any-to-Any

    [HELLO,        		Session|id]
    [HELLO,        		Session|id, Details|dict]
    [GOODBYE,      		Details|dict]
    [HEARTBEAT,    		IncomingSeq|integer, OutgoingSeq|integer]
    [HEARTBEAT,    		IncomingSeq|integer, OutgoingSeq|integer, Discard|string]

### Publish & Subscribe

#### Publisher-to-Broker

    [PUBLISH,      		Request|id, Topic|uri]
    [PUBLISH,      		Request|id, Topic|uri, Event|any]
    [PUBLISH,      		Request|id, Topic|uri, Options|dict, Event|any]

#### Broker-to-Publisher

    [PUBLISHED,  		Request|id]

#### Subscriber-to-Broker

    [SUBSCRIBE,    		Request|id, Topic|uri]
    [SUBSCRIBE,    		Request|id, Topic|uri, Options|dict]
    [UNSUBSCRIBE,  		Request|id, Subscription|id]
    [UNSUBSCRIBE,  		Request|id, Subscription|id, Options|dict]

#### Broker-to-Subscriber

    [SUBSCRIBED,   		Request|id, Subscription|id]
    [UNSUBSCRIBED, 		Request|id]
    [EVENT,        		Subscription|id, Topic|uri]
    [EVENT,        		Subscription|id, Topic|uri, Event|any]
    [EVENT,        		Subscription|id, Topic|uri, Details|dict, Event|any]
    [METAEVENT,    		Subscription|id, Metatopic|uri]
    [METAEVENT,    		Subscription|id, Metatopic|uri, Details|dict]

### Remote Procedure Calls

#### Caller-to-Dealer

    [CALL,         		Request|id, Procedure|uri]
    [CALL,         		Request|id, Procedure|uri, Arguments|list]
    [CALL,         		Request|id, Procedure|uri, Options|dict, Arguments|list]
    [CANCEL_CALL,  		Request|id]
    [CANCEL_CALL,  		Request|id, Options|dict]
    
#### Dealer-to-Caller

    [CALL_PROGRESS,		Request|id]
    [CALL_PROGRESS, 	Request|id, Progress|any]
    [CALL_RESULT,   	Request|id]
    [CALL_RESULT,   	Request|id, Result|any]
    [CALL_ERROR,    	Request|id, Error|uri]
    [CALL_ERROR,    	Request|id, Error|uri, Exception|any]

#### Callee-to-Dealer

    [EXPORT,       		Request|id, Procedure|uri]
    [EXPORT,       		Request|id, Procedure|uri, Options|dict]
    [UNEXPORT,     		Request|id, Endpoint|id]
    [UNEXPORT,     		Request|id, Endpoint|id, Options|dict]

#### Dealer-to-Callee

	[EXPORTED,     		Request|id, Endpoint|id]
    [UNEXPORTED,   		Request|id]
    [INVOCATION,   		Request|id, Endpoint|id]
    [INVOCATION,   		Request|id, Endpoint|id, Arguments|list]
    [INVOCATION_CANCEL,	Request|id]
    [INVOCATION_CANCEL,	Request|id, Options|dict]


________



## Feature Announcement

instead of protocol version negotiation, feature announcement

allows for
graceful degration
only implement subsets of functionality



WAMP message types are identified using the following values:

	MessageType|integer : 

        HELLO         : 0        
     	HEARTBEAT     : 1
        GOODBYE       : 2   
 
		CALL          : 16 + 0 
        CALL_CANCEL   : 16 + 1 

     	PROVIDE       : 32 + 0
     	UNPROVIDE     : 32 + 1 
     	CALL_RESULT   : 32 + 2
     	CALL_PROGRESS : 32 + 3 
        CALL_ERROR    : 32 + 4

       	SUBSCRIBE     : 64 + 0
       	UNSUBSCRIBE   : 64 + 1
       	PUBLISH       : 64 + 2

       	EVENT         : 128 + 0
        METAEVENT     : 128 + 1
        PUBLISH_ACK   : 128 + 2

    
> **Polymorphism**. For a given message type, WAMP only uses messages that are polymorphic in the *number* of message arguments. The message type and the message length uniquely determine the type and semantics of the message arguments.
> This leads to message parsing and validation control flow that is efficient, simple to implement and simple to code for rigorous message format checking.

There is however another requirement (desirable goal) in WAMPv2: the *application* payload (that is call arguments, returns, event payload etc) must be at the end of the WAMP message list. The reason is: *brokers* and *dealers* have no need to inspect (parse) that application payloads. Their business is call/event routing. Having the application payload at the end of the list allows brokers/dealers skip parsing altogether. This improves efficiency/performance and probably even allows to transport application encrypted payload transparently.

> **Extensibility**. Some WAMP messages provide options or details with type of dictionary.
> This allows for future extensibility and implementations that only provide subsets of functionality by ignoring unimplemented attributes.
> 


Session lifetime:
 * starts with HELLO
 * ends with GOODBYE or close of transport


Authentication is a complex area: some apps might want to leverage authentication information coming from the transport underlying WAMP (e.g. cookies or TLS client cert auth), other apps might want to do their own authentication on top of WAMP. So I still don't think it's a good idea to put that into WAMP wire level protocol.




## Sessions

### The HELLO Message

When a WAMP session starts, the peers introduce themselves to each other by sending a

    [HELLO,        SessionID|string, HelloDetails|dict]

message.

The `HELLO` message MUST be the very first message sent by each of the two peers after the transport has been connected.


**Session ID**

The sessionId is a string that is randomly generated by the server and unique to the specific WAMP session.

The sessionId can be used for at least two situations: 1) specifying lists of excluded or eligible clients when publishing event and 2) in the context of performing authentication or authorization. 


**Agent Name**

Similar to what browsers do with the `User-Agent` HTTP header, the `HELLO` message MAY disclose the WAMP implemtentation in use to it's peer:

    HelloDetails = {"agent": Agent|string}


**Feature Announcement**

WAMP uses a feature announcement scheme instead of protocol level versioning.

The `HELLO` message MAY contain a *features* map

    HelloDetails = {"features": Features|dict}

that lists features implemented by the respective WAMP peer.

    Features = {"ProgressiveResults": 1,
                "CallTimeouts": 1,
                "PartitionedCalls": 1,
                "CancelCalls": 1}

    Features = {"Callee": 1}

Role announcement?

    Roles = {"Callee": 1}


## Heartbeats

Issue: [here](https://github.com/tavendo/wamp/issues/3).

They serve 2 purposes:

  * Make it possible to automatically / adaptively keep the radio state on a mobile connection in low-latency, active state
  * Communicate heartbeat sequence numbers which are used for `PUBLISH_ACK`.

The heartbeat allows to notify the peer up to which incoming heartbeat all incoming WAMP messages have been processed, and announce an outgoing hearbeat sequence number in the same message.

It also allows to inject discarded payload for the radio channel thingy discussed above.


## Remote Procedure Calls

The *Remote Procedure Call* (RPC) messaging pattern involves three WAMP roles:

 1. *Caller*
 2. *Dealer*
 3. *Callee*

A WAMP peer that acts as a *Callee* **provides** procedures for calling by WAMP peers that act as *Callers*. *Callers* and *Callees* are decoupled by *Dealers*. Dealers are responsible for routing calls and call return successes and errors.

> Note that a WAMP peer might act as *Dealer* and *Callee* at the same time. Such a peer might route incoming calls internally to implementing procedures. This is the only architecture that was possible with WAMPv1. With WAMPv2 this is still possible, but addtitionally, the *Callee* can be external to the *Dealer*, which allows for more flexible application architecures.
> 


A procedure that is provided by a *Callee* to be called via WAMP by *Callers* is said to be *exported*. An exported procedure is called **RPC endpoint**.

A procedure is always exported under a fully qualified URI and the respective endpoint can be identified by said URI.

There might be more than one endpoint exported under a given URI.

A *Caller* provides the URI of the RPC endpoint to identify the procedure to be called and any arguments for the call.
The *Callee* will execute the procedure using the arguments supplied with the call and return the result of the call or an error to the *Caller*. 

The *Remote Procedure Call* messaging pattern is realized with the following WAMP messages.

*Caller-to-Callee*:

 * `CALL`
 * `CALL_CANCEL`

*Callee-to-Caller*:

 * `CALL_RESULT`
 * `CALL_ERROR`
 * `CALL_PROGRESS`


### The CALL Message

Inline-style: 
![alt text](figure/rpc_call1.png "RPC Message Flow: Calls")



A *Caller* initiates a RPC by sending a

    [CALL,          CallID|string, Endpoint|uri, Arguments|list]

or

    [CALL,          CallID|string, Endpoint|uri, Arguments|list, CallOptions|dict]

message to the *Callee*.

The message is a `list` consisting of

 1. `CALL` : message type ID as an **integer**
 2. `CallID` : **string** identifying the call
 3. `Endpoint` : URI of the remote procedure to be called
 4. `Arguments` : **list** of zero or more call arguments

and optionally

 5. `CallOptions` : 

The `CallID` MUST be a randomly generated string.

The `CallID` is returned in `CALL_RESULT`, `CALL_PROGRESS` or `CALL_ERROR` messages by the *Callee* and used by the *Caller* to correlate the return messages with the originating call.

The `Endpoint` is a string that identifies the remote procedure to be called and MUST be a valid URI.

When the execution of the remote procedure finishes, the *Callee* responds by sending a message of type `CALL_RESULT` or `CALL_ERROR`.

The execution and sending is asynchronous, and there may be more than one RPC outstanding.
An RPC is called outstanding (from the point of view of the *Caller*), when a (final) result or error has not yet been received by the client.

When the execution of the remote procedure finishes successfully, the *Callee* responds by sending a 

    [CALL_RESULT,   CallID|string, CallResult|any]

message to the *Caller*.

The message is a **list** consisting of `CALL_RESULT`, the message type ID as an **integer**, followed by the `CallID`, the call correlation string that was randomly generated by the client, followed by result, the call result.

The result is always present and can be any JSON serializable value, include the JSON value null.

When the remote procedure call could not be executed, an error or exception occurred during the execution or the execution of the remote procedure finishes unsuccessfully for any other reason, the server responds by sending a either 

    [CALL_ERROR,    CallID|string, Error|uri]
    [CALL_ERROR,    CallID|string, Error|uri, ErrorMessage|string]
    [CALL_ERROR,    CallID|string, Error|uri, ErrorMessage|string, ErrorDetails|any]

The message is a JSON list consisting of `CALL_ERROR`, the message type ID as an integer, followed by the `CallID`, the call correlation string that was randomly generated by the client, followed by `Error`, an URI identifying the error, followed by `ErrorMessage`, a string with an error description.

The `ErrorMessage` is always present, MAY be an empty string, and if non-empty SHOULD be a human-readable description of the error. The description is intended to be understood by developers, not end-users.

If `ErrorDetails` is present, it MUST be not null, and is used to communicate application error details, defined by the `Error`.


### The CALL_PROGRESS Message

Issue: [here](https://github.com/tavendo/wamp/issues/17).

A *Callee* can return *progressive results* via

    [CALL_PROGRESS, CallID|string, CallProgress|any]

In any case, exactly one of `CALL_RESULT` or `CALL_ERROR` will be sent in the end.


### CALL_CANCEL

A caller might actively want to cancel a RPC that was issued, but has not yet returned. An example where this is useful could be a user triggering a long running operation and now no longer willing to wait or changing his mind.

Canceling an outstanding RPC upon caller initiative requires a new wire level message. The minimal information that needs to be provided is the `CallID` of the call to be canceled. The `CallID` is sufficient to identify the original call, and the peer can stop the callee or interrupt the call processing.

The `CALL_CANCEL` message has the following structure:

    [CALL_CANCEL,   CallID|string]

or

    [CALL_CANCEL,   CallID|string, CallCancelOptions|dict]

When a call is canceled, a `CALL_ERROR` message is nevertheless generated and sent to the caller. The `CALL_ERROR` message will again identify the call via the *CallID* and provide the error type via an URI `http://wamp.ws/err#CanceledByCaller`.

    CallCancelOptions = {CANCELMODE: ("skip"|"kill"|"killnowait")|string := "killnowait"}


### Call Options
A `CALL` message can carry *options* that control certain advanced RPC features. Currently, the following options are defined

    CallOptions = {TIMEOUT: Timeout|integer := 0,
                   PKEYS: PartitionKeys|list := [null],
                   PMODE: ("all"|"any")|string := "all"}

**Call Timeouts**

`TIMEOUT` allows to issue a RPC that is *automatically* canceled by the *callee* after the 
specified time.

The timeout is an integer and specifies the call timeout in `ms`.

A timeout of `0` deactivates automatic call timeout. This is also the default value.

The timeout option is a companion to, but slightly different from the `CALL_CANCEL` message that allows a *caller* to *actively* cancel a call.

**Partitioned Calls**

`PKEYS` allows to specify a list of application specific *partition keys*. Applications can use partition keys for data sharding. The RPC is only routed to the database instances that hold the respective partitions.

Results from the individual partitions are returned as progressive results via `CALL_PROGRESS` messages. In any case, the call is completed via a `CALL_RESULT` or `CALL_ERROR` message.

`PMODE` allows to specify the mode of partitioned call: `"all"` or `"any"`.

In mode `"all"` the RPC is routed to all database instances holding data from partitions of the specified list.

In mode `"any"` the RPC is routed to a single database instance, randomly selected from the instances holding data from partitions of the specified list.



## PubSub Messages

WAMP PubSub is implemented on top of the following messages.



The Publish & Subscribe messaging pattern is realized with 4 messages:

    SUBSCRIBE
    UNSUBSCRIBE
    PUBLISH
    EVENT

Upon subscribing to a topic via the SUBSCRIBE message, a client will be receiving asynchronous events published to the respective topic via the EVENT message. Clients publish to a topic via the PUBLISH message. An subscription lasts for the duration of a session, unless a client opts out from a previous subscription via the UNSUBSCRIBE message.

A client may subscribe to zero, one or more topics, and clients publish to topics without knowledge of subscribers.

WAMPv1 has no feedback mechanism for when a subscribe or publish fails, i.e. when the subscription or publication is denied. When a client subscribes or publishes, there is no error feedback and a failed action is just silently ignored by the server.



### Subscribe and Unsubscribe Messages

A client requests access to a valid topicURI (or CURIE from Prefix) to receive events published to the given topicURI.

    [SUBSCRIBE,    Topic|uri]
    [SUBSCRIBE,    Topic|uri, SubscribeOptions|dict]

Upon a successful subscription the session will start receiving messages in the EVENT in the context of the topicURI. The request is asynchronous, the server will not return an acknowledgement of the subscription.

Calling unsubscribe on a topicURI informs the server to stop delivering messages to the client previously subscribed to that topicURI.

    [UNSUBSCRIBE,  Topic|uri]
    [UNSUBSCRIBE,  Topic|uri, UnsubscribeOptions|dict]


**Pattern-based Subscriptions**

Issue: [here](https://github.com/tavendo/wamp/issues/10).

A PubSub consumer may subscribe to topics based on a pattern. This can be useful to reduce the number of individual subscriptions (the number of sent `SUBSCRIBE` messages) and to subscribe to topics the consumer does not know exactly.

	SubscribeOptions   = {MATCH: ('exact' | 'prefix' | 'wildcard')|string}
	UnsubscribeOptions = {MATCH: ('exact' | 'prefix' | 'wildcard')|string}

* There is no set semantics.
* To unsubscribe, the exact same pattern must be given.
* Consumer needs to rematch based on his pattern (the `EVENT` does contain the fully qualified topic, but not the pattern that led to the dispatch).
* wildcard: only "\*" as path components (that is between 2 "/") will be allowed. And "*" must be matched by a non-empty string without "/".


WAMPv2 solves this as follows

1. Subscriber subscribes to some topic or pattern via `options`

         [SUBSCRIBE,    		Request|id, Topic|uri, Options|dict]

2. The broker now acknowledges the subscription

          [SUBSCRIBED,   		Request|id, Subscription|id]

3. Later, when an event is delivered, the broker sends:

          [EVENT,        		Subscription|id, Topic|uri, Event|any]

The broker not only communicates the (concrete) `topic` under which is the event was published, but also the `subscription` under which the subscriber receives that event.



### Publish Message

The client will send an event to all clients connected to the server who have subscribed to the topicURI.

    [PUBLISH,      Topic|uri, Event|any]
    [PUBLISH,      Topic|uri, Event|any, PublishOptions|dict]   

If the client publishing their message to topicURI has also Subscribed to that topicURI they can opt to not receive their published event by passing the optional parameter excludeMe to TRUE.


	PublishOptions = {EXCLUDE_ME:  ExcludeMe|boolean,
				      EXCLUDE:     Exclude|list,
					  ELIGIBLE:    Eligible|list,
                      IDENTIFY_ME: IdentifyMe|boolean}

### Event Message

Subscribers receive PubSub events published by subscribers via the EVENT message. The EVENT message contains the topicURI, the topic under which the event was published, and event, the PubSub event payload. 

    [EVENT,        Topic|uri]
    [EVENT,        Topic|uri, Event|any]
    [EVENT,        Topic|uri, Event|any, EventDetails|dict]

The topicURI MUST be a fully qualified URI for the topic. The event payload MUST always be present, and can be any simple or complex type or null. 

The event message contains the following optional details:

	EventDetails = {EVENT_ID:  EventID|string,
                    PUBLISHER: SessionID|string}


Since WAMP presumes an ordered transport, hearbeat and publish event messages are ordered too, and if the peer also processes event publications in-order, we can implement a heartbeat-based group acknowledgement scheme for feedback to event publications.

    [PUBLISH_ACK,  HeartbeatSequenceNo|integer]

Publish: returns deferred, that fires when the expiration sequence number of heartbeats arrived. At each point in time, there is only one deferred active. Multiple application 
handlers attach to those deferreds.

    [METAEVENT,    Topic|uri, Metatopic|uri, MetaEvent|any]


## WAMP URIs

### Predefined URIs

WAMP reserves the [*http(s)://api.wamp.ws*](https://wamp.ws) namespace for identifying WAMP builtin RPC endpoints, PubSub topics, metaevents and errors.

WAMP predefines the following URIs:

* WAMP Authentication API:
  * [https://api.wamp.ws/procedure#requestAuthentication](https://api.wamp.ws/procedure#requestAuthentication)
  * [https://api.wamp.ws/procedure#authenticate](https://api.wamp.ws/procedure#authenticate)
* WAMP Reflection API:
  * [https://api.wamp.ws/procedure#listProcedures](https://api.wamp.ws/procedure#listProcedures)
  * [https://api.wamp.ws/procedure#listTopics](https://api.wamp.ws/procedure#listTopics)
  * [https://api.wamp.ws/procedure#describeProcedure](https://api.wamp.ws/procedure#describeProcedure)
  * [https://api.wamp.ws/procedure#describeTopic](https://api.wamp.ws/procedure#describeTopic)
* WAMP PubSub Metatopics:
  * [https://api.wamp.ws/metatopic#onSub](https://api.wamp.ws/metatopic#onSub)
* WAMP Errors:
  * [https://api.wamp.ws/error#InvalidArgument](https://api.wamp.ws/error#InvalidArgument)


## WAMP Reflection

*Reflection* denotes the ability of WAMP peers to examine the RPC endpoints and PubSub topics provided by other peers.

I.e. a WAMP peer may be interested in retrieving a machine readable list and description of WAMP RPC endpoints and PubSub topics he is authorized to access in the context of a WAMP session.

Reflection may be useful in the following cases:

* documentation
* discoverability
* generating stubs and proxies

> Reflection should be available both from within peers via the WAMP protocol, as well as over the Web via plain old HTTP/GET requests.
> 


With WAMP Challenge-Response Authentication, the client already gets a list of RPC endpoint URIs (and PubSub topics) he is authorized to use. WAMP-CRA is implemented on top of 2 predefined RPCs


### Reflection via HTTP

WAMP URIs used to identify application-specific or WAMP-predefined RPC endpoints and PubSub topics should be dereferencable via the HTTP or HTTPS protocols.

E.g. when dereferencing the (predefined) topic URI [https://api.wamp.ws/metatopic#onSub](http://wamp.ws), you get back a human readable HTML document that describes the context and meaning of the *onSub* meta topic and structure of respective event payloads.

When a `Content-Type` is specified while doing the HTTP/GET, machine readable reflection data about the API may be returned. I.e. the reflection information may be returned in JSON format.


### Reflection via WAMP

WAMP predefines the following RPC endpoints for performing run-time reflection on WAMP peers:

  * [https://api.wamp.ws/procedure#listProcedures](https://api.wamp.ws/procedure#listProcedures)
  * [https://api.wamp.ws/procedure#listTopics](https://api.wamp.ws/procedure#listTopics)
  * [https://api.wamp.ws/procedure#describeProcedure](https://api.wamp.ws/procedure#describeProcedure)
  * [https://api.wamp.ws/procedure#describeTopic](https://api.wamp.ws/procedure#describeTopic)


## WAMP Authentication

WAMP predefines the following RPC endpoints for performing *Challenge-Response* authentication of peers during a WAMP session:

  * [https://api.wamp.ws/procedure#requestAuthentication](https://api.wamp.ws/procedure#authenticationRequest)
  * [https://api.wamp.ws/procedure#authenticate](https://api.wamp.ws/procedure#authenticate)


## Differences from WAMP Version 1

### Auxiliary

 1. `PREFIX` message deprecated (see issue [here](https://github.com/tavendo/wamp/issues/8)).
 2. `WELCOME` message deprecated, instead ..
 3. New (symmetric) `HELLO` message
 4. New `GOODBYE` message
 5. New `HEARTBEAT` message

### RPC

 1. Arguments in `CALL` message are provided as a `list`
 2. New Variant of `CALL` message with call options
 3. New `CALL_CANCEL` message
 4. New `CALL_PROGRESS` message

### PubSub

Write me.


## References

1. [The WebSocket Protocol](http://tools.ietf.org/html/rfc6455)
2. [UTF-8, a transformation format of ISO 10646](http://tools.ietf.org/html/rfc3629)
3. [The application/json Media Type for JavaScript Object Notation (JSON)](http://tools.ietf.org/html/rfc4627)
4. [Uniform Resource Identifier (URI): Generic Syntax, RFC 3986](http://tools.ietf.org/html/rfc3986)
5. [The application/json Media Type for JavaScript Object Notation (JSON)](http://tools.ietf.org/html/rfc4627)
6. [MessagePack Format specification](http://wiki.msgpack.org/display/MSGPACK/Format+specification)



### Structured exceptions idioms
