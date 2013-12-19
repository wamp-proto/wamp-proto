## Feature Announcement

instead of protocol version negotiation, feature announcement

allows for
graceful degration
only implement subsets of functionality

    
> **Polymorphism**. For a given message type, WAMP only uses messages that are polymorphic in the *number* of message arguments. The message type and the message length uniquely determine the type and semantics of the message arguments.
> This leads to message parsing and validation control flow that is efficient, simple to implement and simple to code for rigorous message format checking.

There is however another requirement (desirable goal) in WAMPv2: the *application* payload (that is call arguments, returns, event payload etc) must be at the end of the WAMP message list. The reason is: *brokers* and *dealers* have no need to inspect (parse) that application payloads. Their business is call/event routing. Having the application payload at the end of the list allows brokers/dealers skip parsing altogether. This improves efficiency/performance and probably even allows to transport application encrypted payload transparently.

> **Extensibility**. Some WAMP messages provide options or details with type of dictionary.
> This allows for future extensibility and implementations that only provide subsets of functionality by ignoring unimplemented attributes.
> 

Authentication is a complex area: some apps might want to leverage authentication information coming from the transport underlying WAMP (e.g. cookies or TLS client cert auth), other apps might want to do their own authentication on top of WAMP. So I still don't think it's a good idea to put that into WAMP wire level protocol.


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



The execution and sending is asynchronous, and there may be more than one RPC outstanding.
An RPC is called outstanding (from the point of view of the *Caller*), when a (final) result or error has not yet been received by the client.

A caller might actively want to cancel a RPC that was issued, but has not yet returned. An example where this is useful could be a user triggering a long running operation and now no longer willing to wait or changing his mind.


    CallCancelOptions = {CANCELMODE: ("skip"|"kill"|"killnowait")|string := "killnowait"}

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


Upon subscribing to a topic via the SUBSCRIBE message, a client will be receiving asynchronous events published to the respective topic via the EVENT message. Clients publish to a topic via the PUBLISH message. An subscription lasts for the duration of a session, unless a client opts out from a previous subscription via the UNSUBSCRIBE message.

A client may subscribe to zero, one or more topics, and clients publish to topics without knowledge of subscribers.

WAMPv1 has no feedback mechanism for when a subscribe or publish fails, i.e. when the subscription or publication is denied. When a client subscribes or publishes, there is no error feedback and a failed action is just silently ignored by the server.


**Pattern-based Subscriptions**

Issue: [here](https://github.com/tavendo/wamp/issues/10).

A PubSub consumer may subscribe to topics based on a pattern. This can be useful to reduce the number of individual subscriptions (the number of sent `SUBSCRIBE` messages) and to subscribe to topics the consumer does not know exactly.

	SubscribeOptions   = {MATCH: ('exact' | 'prefix' | 'wildcard')|string}
	UnsubscribeOptions = {MATCH: ('exact' | 'prefix' | 'wildcard')|string}

* There is no set semantics.
* To unsubscribe, the exact same pattern must be given.
* Consumer needs to rematch based on his pattern (the `EVENT` does contain the fully qualified topic, but not the pattern that led to the dispatch).
* wildcard: only "\*" as path components (that is between 2 "/") will be allowed. And "*" must be matched by a non-empty string without "/".

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

