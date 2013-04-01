# WAMPv2

## WAMP Messages

WAMP RPC and PubSub are provided via the following messages which are explained in detail in the further sections:

1. **Auxiliary**

        [HELLO,        SessionID|string, HelloDetails|dict]
        [HEARTBEAT,    HeartbeatSequenceNo|integer]
    
2. **RPC**


        [CALL,          CallID|string, Arguments|list]
        [CALL,          CallID|string, Arguments|list, CallOptions|dict]
        [CALL_RESULT,   CallID|string, CallResult|object]
        [CALL_PROGRESS, CallID|string, CallProgress|object]
        [CALL_ERROR,    CallID|string, Error|uri]
        [CALL_ERROR,    CallID|string, Error|uri, ErrorMessage|string]
        [CALL_ERROR,    CallID|string, Error|uri, ErrorMessage|string, ErrorDetails|object]
        [CALL_CANCEL,   CallID|string]
    
3. **PubSub**

        [SUBSCRIBE,    Topic|uri]
        [SUBSCRIBE,    Topic|uri, SubscribeOptions|dict]
        [UNSUBSCRIBE,  Topic|uri]
        [UNSUBSCRIBE,  Topic|uri, UnsubscribeOptions|dict]
        [PUBLISH,      Topic|uri]
        [PUBLISH,      Topic|uri, Event|object]
        [PUBLISH,      Topic|uri, Event|object, PublishOptions|dict]   
        [PUBLISH_ACK,  HeartbeatSequenceNo|integer]
        [EVENT,        Topic|uri]
        [EVENT,        Topic|uri, Event|object]
        [EVENT,        Topic|uri, Event|object, EventDetails|dict]
        [METAEVENT,    Topic|uri, Metatopic|uri]
        [METAEVENT,    Topic|uri, Metatopic|uri, MetaEvent|object]

WAMP message types are identified using the following values:

	MessageType|integer : 

    HELLO         : 1
  	HEARTBEAT	  : 2
  	CALL	      : 3
  	CALL_RESULT	  : 4
  	CALL_PROGRESS : 5
  	CALL_ERROR	  : 6
  	CALL_CANCEL	  : 7
  	SUBSCRIBE	  : 8
  	UNSUBSCRIBE	  : 9
  	PUBLISH	      : 10
  	PUBLISH_ACK	  : 11
  	EVENT	      : 12
  	METAEVENT	  : 13


## No polymorphic messages

WAMPv2 only uses messages that a polymorphic in the *number* of arguments.

This leads to message parsing and validation control flow that is efficient, simple to implement and simple to code for rigorous message format checking.

Adressed issues: [https://github.com/tavendo/wamp/issues/5](https://github.com/tavendo/wamp/issues/5)


## WAMP URIs

WAMP reserves the [*https://api.wamp.ws*](http://wamp.ws) namespace for identifying WAMP builtin RPC endpoints and topic. WAMP predefines the following URIs:

* WAMP-CRA authentication methods:
  * [https://api.wamp.ws/procedure#authRequ](http://wamp.ws)
  * [https://api.wamp.ws/procedure#auth](http://wamp.ws)
* WAMP reflection methods:
  * [https://api.wamp.ws/procedure#listProcedures](http://wamp.ws)
  * [https://api.wamp.ws/procedure#listTopics](http://wamp.ws)
  * [https://api.wamp.ws/procedure#describeProcedure](http://wamp.ws)
  * [https://api.wamp.ws/procedure#describeTopic](http://wamp.ws)
* WAMP meta topics:
  * [https://api.wamp.ws/metatopic#onSub](http://wamp.ws)
* WAMP errors:
  * [https://api.wamp.ws/error#InvalidArgument](http://wamp.ws)


## WAMP Reflection

*Reflection* denotes the ability of WAMP peers to examine the RPC endpoints and PubSub topics provided by other peers.

I.e. a WAMP peer may be interested in retrieving a machine readable list and description of WAMP RPC endpoints and PubSub topics he is authorized to access in the context of a WAMP session.

documentation
discoverability
generating stubs and proxies

Reflection should be available both from within peers via the WAMP protocol, as well as over the Web via plain old HTTP/GET requests.

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




    AttributeId|integer :

    TIMEOUT     : 1
    EXCLUDE_ME  : 2
    EXCLUDE     : 3
    ELIGIBLE    : 4
    EVENT_ID    : 5
    PUBLISHER   : 6
    IDENTIFY_ME : 7
    MATCH       : 8

    
          

### Auxiliary Messages

    [HELLO,        SessionID|string, FeatureMap|dict]
    [HEARTBEAT,    HeartbeatSequenceNo|integer]

### RPC Messages
    [CALL,         CallID|string, Arguments|list]
    [CALL,         CallID|string, Arguments|list, CallOptions|dict]

    [CALL_RESULT,  CallID|string, CallResult|object]

    [CALL_ERROR,   CallID|string, Error|uri]
    [CALL_ERROR,   CallID|string, Error|uri, ErrorMessage|string]
    [CALL_ERROR,   CallID|string, Error|uri, ErrorMessage|string, ErrorDetails|object]

    [CALL_CANCEL,  CallID|string]

### PubSub Messages

WAMP PubSub is implemented on top of the following messages.

    [SUBSCRIBE,    Topic|uri]
    [SUBSCRIBE,    Topic|uri, SubscribeOptions|dict]

    [UNSUBSCRIBE,  Topic|uri]
    [UNSUBSCRIBE,  Topic|uri, UnsubscribeOptions|dict]

    [PUBLISH,      Topic|uri, Event|object]
    [PUBLISH,      Topic|uri, Event|object, PublishOptions|dict]   
    [PUBLISH_ACK,  HeartbeatSequenceNo|integer]

    [EVENT,        Topic|uri, Event|object]
    [EVENT,        Topic|uri, Event|object, EventDetails|dict]

    [METAEVENT,    Topic|uri, Metatopic|uri, MetaEvent|object]

### Message Options and Details

Some WAMP messages provide options or details with type of dictionary.
This allows for future extensibility and implementations that only provide subsets of functionality by ignoring unimplemented attributes.

#### Call Message

    CallOptions = {TIMEOUT: Timeout|integer}

`TIMEOUT` allows to issue a RPC that is automatically canceled after the specified time. The timeout is in seconds.

#### Subscribe and Unsubscribe Messages

	SubscribeOptions   = {MATCH: ('exact' | 'prefix' | 'wildcard')|string}
	UnsubscribeOptions = {MATCH: ('exact' | 'prefix' | 'wildcard')|string}

#### Publish Message

	PublishOptions = {EXCLUDE_ME:  ExcludeMe|boolean,
				      EXCLUDE:     Exclude|list,
					  ELIGIBLE:    Eligible|list,
                      IDENTIFY_ME: IdentifyMe|boolean}

#### Event Message

	EventDetails = {EVENT_ID:  EventID|string,
                    PUBLISHER: SessionID|string}


Observation: since WAMP presumes an ordered transport, hearbeat and publish event messages are ordered too, and if the peer also processes event publications in-order, we can implement a heartbeat-based group acknowledgement scheme for feedback to event publications.

Publish: returns deferred, that fires when the expiration sequence number of heartbeats arrived. At each point in time, there is only one deferred active. Multiple application handlers attach to those deferreds.


## RPC

The RPC features provided by have worked out quite well and proven to be sufficient for most use cases.

### Symmetric RPC

### Progressive Results

### Canceling of calls

A caller might deliberately want to cancel a RPC that was issued, but has not yet returned. An example where this is useful could be a user triggering a long running operation and now no longer willing to wait or changing his mind.

Canceling an outstanding RPC upon caller initiative requires a new wire level message. The minimal information that needs to be provided is the *call ID* of the call to be canceled. The *call ID* is sufficient to identify the original call, and the peer can stop the callee or interrupt the call processing.

When a call is canceled, a **CallErrorReturn** message is nevertheless generated and sent to the caller. The **CallErrorReturn** message will again identify the call via the *call ID* and provide the error type via an URI `http://wamp.ws/err#CanceledByCaller`.

The **CallCancelReturn** has the following structure:

    [CALL_CANCEL, <call ID>]

for example

    [9, "Jk9N$jsd2"]



### Call timeouts

### Structured exceptions idioms



Wire Efficiency
---------------

  * Implement WebSocket per-frame compression extension.
  * Provide pluggable, text/binary serialization formats.


PREFIX Message
--------------

With WAMPv1, the `PREFIX` message serves two purposes:

 1. ease usage of unwieldy long URIs for developers
 2. reduce wire traffic

See [here](http://wamp.ws/spec#prefix_message).

For WAMPv2, 1. is a feature of the WAMP implementation (i.e. dynamically create stub objects and methods). This provides i.e. auto-completition in IDEs and even more comfort.

For 2., see wire efficiency.

WAMPv2 will 

Both peers maintain a per-session map for mapping shorthands to fully qualified URIs.

The shorthands can be set by the peer via a message. That message can now go in both directions.

     [ MSG_TYPE_MAPURI,  <shorthand | str>,  <FQ URI | str>  ]

Effectively, this establishes two compression dicationaries for URIs with a scope and lifetime of WAMP session.


EVENT Message
-------------

    [ MSG_TYPE_EVENT,     <URI>, <Event> ]
    [ MSG_TYPE_EVENT_P,   <URI>, <Event>, <Publisher Session ID> ]
    [ MSG_TYPE_EVENT_I,   <URI>, <Event>, <Event ID> ]
    [ MSG_TYPE_EVENT_PI,  <URI>, <Event>, <Publisher Session ID>, <Event ID> ]


SUBSCRIBE Message
-----------------

    [ MSG_TYPE_SUBSCRIBE,   <URI> ]
    [ MSG_TYPE_SUBSCRIBE_E, <URI>, { .. extra info ..} ]

