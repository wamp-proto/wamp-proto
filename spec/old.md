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



Authentication is a complex area: some apps might want to leverage authentication information coming from the transport underlying WAMP (e.g. cookies or TLS client cert auth), other apps might want to do their own authentication on top of WAMP. So I still don't think it's a good idea to put that into WAMP wire level protocol.






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
