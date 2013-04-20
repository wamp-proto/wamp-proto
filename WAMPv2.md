# WAMPv2

## Introduction

WAMP is an open WebSocket subprotocol that provides two asynchronous messaging patterns: RPC and PubSub.

## Building Blocks

WAMP is based on established Web standards:

   * WebSocket
   * JSON
   * URIs

Though WAMP is currently defined with respect to above concrete standards, effectively it only makes the following assumptions.


### Transport

A *transport* with the following characteristics is assumed:

  1. reliable
  2. message-based
  3. ordered
  4. full-duplex

The default binding is WebSocket as Transport. Other transports might be defined in the future.


### Serialization

Issue: [here](https://github.com/tavendo/wamp/issues/4).

A *transport message serialization format* is assumed that at least provides:

  * `integer`
  * `string`
  * `list`
  * `dict`

types.

The default binding is JSON as Serialization.

Hence, WAMP *itself* does not use the following JSON types:

  * `number` (non-integer)
  * `bool`
  * `null`

Applications MAY use those types in *application payloads* (e.g. for event payloads or call arguments and results).


### Identifier

An ID space that allows global assignment (to organization or persons) and conflict resolution is assumed.

The default binding is URIs from the HTTP or HTTPS scheme as IDs for both topics and procedures.


### Summary

The currently defined WAMP binding:

**WAMP over WebSocket using text (UTF-8) messages with JSON serialization and HTTP(S) URIs for IDs**.

_________


## Feature Announcement

instead of protocol version negotiation, feature announcement

allows for
graceful degration
only implement subsets of functionality

## WAMP Roles

 * Caller
 * Callee
 * Subscriber
 * Publisher
 * Broker


## WAMP Messages

### Overview

All WAMP messages are of the same structure:

    [MessageType|integer, ... zero or more message type specific arguments ...]

A `list` with a first element `MessageType` followed by zero or more message type specific arguments.

The notation `Argument|type` denotes an message argument named `Argument` of type `type`:

 * `integer`: a (non-negative) integer
 * `string`: any (UTF-8) string, including the empty string
 * `id`: a random string
 * `uri`: a string that is a valid URI under the HTTP or HTTPS schemes, possibly with a fragment part, but without a query part.
 * `dict`: a dictionary (map)
 * `list`: a list (array)

WAMP defines the following messages which are explained in detail in the further sections.

________

**Auxiliary**

 Direction: *Any-to-Any*

    [HELLO,        SessionID|string, HelloDetails|dict]    
    [HEARTBEAT,    HeartbeatSequenceNo|integer]
    [HEARTBEAT,    HeartbeatSequenceNo|integer, DiscardMe|string]
    [GOODBYE,      GoodbyeDetails|dict]
________  
**RPC**

Direction: *Caller-to-Callee*

    [CALL,          CallID|string, Endpoint|uri]
    [CALL,          CallID|string, Endpoint|uri, Arguments|list]
    [CALL,          CallID|string, Endpoint|uri, Arguments|list, CallOptions|dict]
    [CALL_CANCEL,   CallID|string]
    [CALL_CANCEL,   CallID|string, CallCancelOptions|dict]
    
Direction: *Callee-to-Caller*

    [CALL_PROGRESS, CallID|string]
    [CALL_PROGRESS, CallID|string, CallProgress|any]
    [CALL_RESULT,   CallID|string]
    [CALL_RESULT,   CallID|string, CallResult|any]
    [CALL_ERROR,    CallID|string, Error|uri]
    [CALL_ERROR,    CallID|string, Error|uri, ErrorMessage|string]
    [CALL_ERROR,    CallID|string, Error|uri, ErrorMessage|string, ErrorDetails|any]
________
    
**PubSub**

Direction: *Publisher-to-Broker*

    [PUBLISH,      Topic|uri]
    [PUBLISH,      Topic|uri, Event|any]
    [PUBLISH,      Topic|uri, Event|any, PublishOptions|dict]

Direction: *Broker-to-Publisher*

    [PUBLISH_ACK,  HeartbeatSequenceNo|integer]

Direction: *Subscriber-to-Broker*

    [SUBSCRIBE,    Topic|uri]
    [SUBSCRIBE,    Topic|uri, SubscribeOptions|dict]
    [UNSUBSCRIBE,  Topic|uri]
    [UNSUBSCRIBE,  Topic|uri, UnsubscribeOptions|dict]

Direction: *Broker-to-Subscriber*

    [EVENT,        Topic|uri]
    [EVENT,        Topic|uri, Event|any]
    [EVENT,        Topic|uri, Event|any, EventDetails|dict]
    [METAEVENT,    Topic|uri, Metatopic|uri]
    [METAEVENT,    Topic|uri, Metatopic|uri, MetaEvent|any]
________

WAMP message types are identified using the following values:

	MessageType|integer : 

        HELLO         : 0        CALL          : 16 + 0        SUBSCRIBE     :  64 + 0
      	HEARTBEAT     : 1        CALL_CANCEL   : 16 + 1        UNSUBSCRIBE   :  64 + 1
        GOODBYE       : 2                                      PUBLISH       :  64 + 2
                                 CALL_RESULT   : 32 + 0
                                 CALL_PROGRESS : 32 + 1        EVENT         : 128 + 0
      	                         CALL_ERROR    : 32 + 2        METAEVENT     : 128 + 1
                                                               PUBLISH_ACK   : 128 + 2

    
> **Polymorphism**. For a given message type, WAMP only uses messages that are polymorphic in the *number* of message arguments. The message type and the message length uniquely determine the type and semantics of the message arguments.
> This leads to message parsing and validation control flow that is efficient, simple to implement and simple to code for rigorous message format checking.


> **Extensibility**. Some WAMP messages provide options or details with type of dictionary.
> This allows for future extensibility and implementations that only provide subsets of functionality by ignoring unimplemented attributes.
> 

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


## Remote Procedure Calls

The *Remote Procedure Call* (RPC) messaging pattern involves two WAMP peers: a *Caller* and a *Callee*.
A WAMP peer that acts as a *Callee* exposes procedures to be called by WAMP peers that act as *Caller*s.

A procedure that is exposed to be called via WAMP is said to be *exported*. An exported procedure is also called *(RPC) endpoint*.
A procedure is always exported under an URI and the respective endpoint can be identified by said URI.

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

The timeout is an integer and specifies the call timeout in seconds.

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
