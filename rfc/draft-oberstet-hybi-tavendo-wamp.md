% Title = "The Web Application Messaging Protocol"
% abbrev = "WAMP"
% category = "std"
% docName = "draft-oberstet-hybi-tavendo-wamp-02"
% ipr= "trust200902"
% area = "Applications and Real-Time (art)"
% workgroup = "BiDirectional or Server-Initiated HTTP"
% keyword = ["WebSocket, WAMP, real-time, RPC, PubSub"]
%
% date = 2015-10-10T00:00:00Z
%
% [pi]
% toc = "yes"
%
% [[author]]
% initials="T.O."
% surname="Oberstein"
% fullname="Tobias G. Oberstein"
% organization = "Tavendo GmbH"
%   [author.address]
%   email = "tobias.oberstein@tavendo.de"
%
% [[author]]
% initials="A.G."
% surname="Goedde"
% fullname="Alexander Goedde"
% organization = "Tavendo GmbH"
%   [author.address]
%   email = "alexander.goedde@tavendo.de"
%

.# Abstract

This document defines the Web Application Messaging Protocol (WAMP). WAMP is a routed protocol that provides two messaging patterns: Publish & Subscribe and routed Remote Procedure Calls. It is intended to connect application components in distributed applications. WAMP uses WebSocket as its default transport, but can be transmitted via any other protocol that allows for ordered, reliable, bi-directional, and message-oriented communications.

{mainmatter}

# Introduction

## Background

_This section is non-normative._

The WebSocket protocol brings bi-directional real-time connections to the browser. It defines an API at the message level, requiring users who want to use WebSocket connections in their applications to define their own semantics on top of it.

The Web Application Messaging Protocol (WAMP) is intended to provide application developers with the semantics they need to handle messaging between components in distributed applications.

WAMP was initially defined as a WebSocket sub-protocol, which provided Publish & Subscribe (PubSub) functionality as well as Remote Procedure Calls (RPC) for procedures implemented in a WAMP router. Feedback from implementers and users of this was included in a second version of the protocol which this document defines. Among the changes was that WAMP can now run over any transport which is message-oriented, ordered, reliable, and bi-directional.

WAMP is a routed protocol, with all components connecting to a _WAMP Router_, where the WAMP Router performs message routing between the components.

WAMP provides two messaging patterns: _Publish & Subscribe_ and _routed Remote Procedure Calls_.

Publish & Subscribe (PubSub) is an established messaging pattern where a component, the _Subscriber_, informs the router that it wants to receive information on a topic (i.e., it subscribes to a topic). Another component, a _Publisher_, can then publish to this topic, and the router distributes events to all Subscribers.

Routed Remote Procedure Calls (RPCs) rely on the same sort of decoupling that is used by the Publish & Subscribe pattern. A component, the _Callee_, announces to the router that it provides a certain procedure, identified by a procedure name. Other components, _Callers_, can then call the procedure, with the router invoking the procedure on the Callee, receiving the procedure's result, and then forwarding this result back to the Caller. Routed RPCs differ from traditional client-server RPCs in that the router serves as an intermediary between the Caller and the Callee.

The decoupling in routed RPCs arises from the fact that the Caller is no longer required to have knowledge of the Callee; it merely needs to know the identifier of the procedure it wants to call. There is also no longer a need for a direct connection between the caller and the callee, since all traffic is routed. This enables the calling of procedures in components which are not reachable externally (e.g. on a NATted connection) but which can establish an outgoing connection to the WAMP router.

Combining these two patterns into a single protocol allows it to be used for the entire messaging requirements of an application, thus reducing technology stack complexity, as well as networking overheads.


## Protocol Overview

_This section is non-normative._

The PubSub messaging pattern defines three roles: _Subscribers_ and _Publishers_, which communicate via a _Broker_.

The routed RPC messaging pattern also defines three roles: _Callers_ and _Callees_, which communicate via a _Dealer_.

WAMP Connections are established by _Clients_ to a _Router_. Connections can use any transport that is message-based, ordered, reliable and bi-directional, with WebSocket as the default transport.

A Router is a component which implements one or both of the Broker and Dealer roles. A Client is a component which implements any or all of the Subscriber, Publisher, Caller, or Callee roles.

WAMP _Connections_ are established by Clients to a Router. Connections can use any transport which is message-oriented, ordered, reliable and bi-directional, with WebSocket as the default transport.

WAMP _Sessions_ are established over a WAMP Connection. A WAMP Session is joined to a _Realm_ on a Router. Routing occurs only between WAMP Sessions that have joined the same Realm.

The _WAMP Basic Profile_ defines the parts of the protocol that are required to establish a WAMP connection, as well as for basic interactions between the four client and two router roles. WAMP implementations are required to implement the Basic Profile, at minimum.

The _WAMP Advanced Profile_ defines additions to the Basic Profile which greatly extend the utility of WAMP in real-world applications. WAMP implementations may support any subset of the Advanced Profile features. They are required to announce those supported features during session establishment.


## Design Philosophy

_This section is non-normative._

WAMP was designed to be performant, safe and easy to implement. Its entire design was driven by a implement, get feedback, adjust cycle.

An initial version of the protocol was publicly released in March 2012. The intent was to gain insight through implementation and use, and integrate these into a second version of the protocol, where there would be no regard for compatibility between the two versions. Several interoperable, independent implementations were released, and feedback from the implementers and users was collected.

The second version of the protocol, which this RFC covers, integrates this feedback. Routed Remote Procedure Calls are one outcome of this, where the initial version of the protocol only allowed the calling of procedures provided by the router. Another, related outcome was the strict separation of routing and application logic.

While WAMP was originally developed to use WebSocket as a transport, with JSON for serialization, experience in the field revealed that other transports and serialization formats were better suited to some use cases. For instance, with the use of WAMP in the Internet of Things sphere, resource constraints play a much larger role than in the browser, so any reduction of resource usage in WAMP implementations counts. This lead to the decoupling of WAMP from any particular transport or serialization, with the establishment of minimum requirements for both.


### Basic and Advanced Profiles

This document first describes a Basic Profile for WAMP in its entirety, before describing an Advanced Profile which extends the basic functionality of WAMP.

The separation into Basic and Advanced Profiles is intended to extend the reach of the protocol. It allows implementations to start out with a minimal, yet operable and useful set of features, and to expand that set from there. It also allows implementations that are tailored for resource-constrained environments, where larger feature sets would not be possible. Here implementers can weigh between resource constraints and functionality requirements, then implement an optimal feature set for the circumstances.

Advanced Profile features are announced during session establishment, so that different implementations can adjust their interactions to fit the commonly supported feature set.


### Application Code

WAMP is designed for application code to run within Clients, i.e. _Peers_ having the roles Callee, Caller, Publisher, and Subscriber.

Routers, i.e. Peers of the roles Brokers and Dealers are responsible for **generic call and event routing** and do not run application code.

This allows the transparent exchange of Broker and Dealer implementations without affecting the application and to distribute and deploy application components flexibly.

> Note that a **program** that implements, for instance, the Dealer role might at the same time implement, say, a built-in Callee. It is the Dealer and Broker that are generic, not the program.


### Language Agnostic

WAMP is language agnostic, i.e. can be implemented in any programming language. At the level of arguments that may be part of a WAMP message, WAMP takes a 'superset of all' approach. WAMP implementations may support features of the implementing language for use in arguments, e.g. keyword arguments.

### Router Implementation Specifics

This specification only deals with the protcol level. Specific WAMP Broker and Dealer implementations may differ in aspects such as support for:

* router networks (clustering and federation),
* authentication and authorization schemes,
* message persistence, and,
* management and monitoring.

The definition and documentation of such Router features is outside the scope of this document.


## Relationship to WebSocket

WAMP uses WebSocket as its default transport binding, and is a registered WebSocket subprotocol.


# Conformance Requirements

All diagrams, examples, and notes in this specification are non-normative, as are all sections explicitly marked non-normative. Everything else in this specification is normative.

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT",
"SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in
this document are to be interpreted as described in RFC 2119 [@?RFC2119].

Requirements phrased in the imperative as part of algorithms (such as "strip any leading space characters" or "return false and abort these steps") are to be interpreted with the meaning of the key word ("MUST", "SHOULD", "MAY", etc.) used in introducing the algorithm.

Conformance requirements phrased as algorithms or specific steps MAY  be implemented in any manner, so long as the end result is equivalent.

## Terminology and Other Conventions

Key terms such as named algorithms or definitions are indicated like _this_ when they first occur, and are capitalized throughout the text.


# Realms, Sessions and Transports

A Realm is a WAMP routing and administrative domain, optionally protected by authentication and authorization. WAMP messages are only routed within a Realm.

A Session is a transient conversation between two Peers attached to a Realm and running over a Transport.

A Transport connects two WAMP Peers and provides a channel over which WAMP messages for a WAMP Session can flow in both directions.

WAMP can run over any Transport which is message-based, bidirectional,  reliable and ordered.

The default transport for WAMP is WebSocket [@!RFC6455], where WAMP is an [officially registered](http://www.iana.org/assignments/websocket/websocket.xml) subprotocol.



# Peers and Roles

A WAMP Session connects two Peers, a Client and a Router. Each WAMP Peer MUST implement one role, and MAY implement more roles.

A Client MAY implement any combination of the Roles:

 * Callee
 * Caller
 * Publisher
 * Subscriber

and a Router MAY implement either or both of the Roles:

 * Dealer
 * Broker

> This document describes WAMP as in client-to-router communication. Direct client-to-client communication is not supported by WAMP. Router-to-router communication MAY be defined by a specific router implementation.
>


## Symmetric Messaging

It is important to note that though the establishment of a Transport might have a inherent asymmetry (like a TCP client establishing a WebSocket connection to a server), and Clients establish WAMP sessions by attaching to Realms on Routers, WAMP itself is designed to be fully symmetric for application components.

After the transport and a session have been established, any application component may act as Caller, Callee, Publisher and Subscriber at the same time. And Routers provide the fabric on top of which WAMP runs a symmetric application messaging service.


## Remote Procedure Call Roles

The Remote Procedure Call messaging pattern involves peers of three different roles:

* Callee (Client)
* Caller (Client)
* Dealer (Router)

A Caller issues calls to remote procedures by providing the procedure URI and any arguments for the call.
The Callee will execute the procedure using the supplied arguments to the call and return the result of the call to the Caller.

Callees register procedures they provide with Dealers. Callers initiate procedure calls first to Dealers. Dealers route calls incoming from Callers to Callees implementing the procedure called, and route call results back from Callees to Callers.

The Caller and Callee will usually run application code, while the Dealer works as a generic router for remote procedure calls decoupling Callers and Callees.


## Publish & Subscribe Roles

The Publish & Subscribe messaging pattern involves peers of three different roles:

* Subscriber (Client)
* Publisher (Client)
* Broker (Router)

A Publishers publishes events to topics by providing the topic URI and any payload for the event. Subscribers of the topic will receive the event together with the event payload.

Subscribers subscribe to topics they are interested in with Brokers. Publishers initiate publication first at Brokers. Brokers route events incoming from Publishers to Subscribers that are subscribed to respective topics.

The Publisher and Subscriber will usually run application code, while the Broker works as a generic router for events decoupling Publishers from Subscribers.


## Peers with multiple Roles

Note that Peers might implement more than one role: e.g. a Peer might act as Caller, Publisher and Subscriber at the same time. Another Peer might act as both a Broker and a Dealer.



# Building Blocks

WAMP is defined with respect to the following building blocks

1.  Identifiers
2.  Serializations
3.  Transports

For each building block, WAMP only assumes a defined set of requirements, which allows to run WAMP variants with different concrete bindings.


## Identifiers

### URIs {#uris}

WAMP needs to identify the following **persistent** resources:

1.  Topics
2.  Procedures
3.  Errors

These are identified in WAMP using *Uniform Resource Identifiers* (URIs) [@!RFC3986] that MUST be Unicode strings.

> When using JSON as WAMP serialization format, URIs (as other strings) are transmitted in UTF-8 [@!RFC3629] encoding.

*Examples*

* `com.myapp.mytopic1`
* `com.myapp.myprocedure1`
* `com.myapp.myerror1`

The URIs are understood to form a single, global, hierarchical namespace for WAMP.

> The namespace is unified for topics, procedures and errors - these different resource types do NOT have separate namespaces.
>

To avoid resource naming conflicts, the package naming convention from Java is used, where URIs SHOULD begin with (reversed) domain names owned by the organization defining the URI.

#### Relaxed/Loose URIs

URI components (the parts between two `.`s, the head part up to the first `.`, the tail part after the last `.`) MUST NOT contain a `.`, `#` or whitespace characters and MUST NOT be empty (zero-length strings).

> The restriction not to allow `.` in component strings is due to the fact that `.` is used to separate components, and WAMP associates semantics with resource hierarchies, such as in pattern-based subscriptions that are part of the Advanced Profile. The restriction not to allow empty (zero-length) strings as components is due to the fact that this may be used to denote wildcard components with pattern-based subscriptions and registrations in the Advanced Profile. The character `#` is not allowed since this is reserved for internal use by Dealers and Brokers.

As an example, the following regular expression could be used in Python to check URIs according to above rules:

{align="left"}
``` python
    <CODE BEGINS>
        ## loose URI check disallowing empty URI components
        pattern = re.compile(r"^([^\s\.#]+\.)*([^\s\.#]+)$")
    <CODE ENDS>
```

When empty URI components are allowed (which is the case for specific messages that are part of the Advanced Profile), this following regular expression can be used (shown used in Python):

{align="left"}
``` python
    <CODE BEGINS>
        ## loose URI check allowing empty URI components
        pattern = re.compile(r"^(([^\s\.#]+\.)|\.)*([^\s\.#]+)?$")
    <CODE ENDS>
```

#### Strict URIs

While the above rules MUST be followed, following a stricter URI rule is recommended: URI components SHOULD only contain letters, digits and `_`.

As an example, the following regular expression could be used in Python to check URIs according to the above rules:

{align="left"}
```python
    <CODE BEGINS>
        ## strict URI check disallowing empty URI components
        pattern = re.compile(r"^([0-9a-z_]+\.)*([0-9a-z_]+)$")
    <CODE ENDS>
```

When empty URI components are allowed (which is the case for specific messages that are part of the Advanced Profile), the following regular expression can be used (shown in Python):

{align="left"}
```python
    <CODE BEGINS>
        ## strict URI check allowing empty URI components
        pattern = re.compile(r"^(([0-9a-z_]+\.)|\.)*([0-9a-z_]+)?$")
    <CODE ENDS>
```

> Following the suggested regular expression will make URI components valid identifiers in most languages (modulo URIs starting with a digit and language keywords) and the use of lower-case only will make those identifiers unique in languages that have case-insensitive identifiers. Following this suggestion can allow implementations to map topics, procedures and errors to the language environment in a completely transparent way.

#### Reserved URIs

Further, application URIs MUST NOT use `wamp` as a first URI component, since this is reserved for URIs predefined with the WAMP protocol itself.

*Examples*

* `wamp.error.not_authorized`
* `wamp.error.procedure_already_exists`


### IDs {#ids}

WAMP needs to identify the following ephemeral entities each in the scope noted:

1. Sessions (*global scope*)
2. Publications (*global scope*)
3. Subscriptions (*router scope*)
4. Registrations (*router scope*)
5. Requests (*session scope*)

These are identified in WAMP using IDs that are integers between (inclusive) **0** and **2^53** (9007199254740992):

* IDs in the *global scope* MUST be drawn *randomly* from a *uniform distribution* over the complete range [0, 2^53]
* IDs in the *router scope* can be chosen freely by the specific router implementation
* IDs in the *session scope* SHOULD be incremented by 1 beginning with 1 (for each direction - *Client-to-Router* and *Router-to-Client*)

> The reason to choose the specific upper bound is that 2^53 is the largest integer such that this integer and *all* (positive) smaller integers can be represented exactly in IEEE-754 doubles. Some languages (e.g. JavaScript) use doubles as their sole number type. Most languages do have signed and unsigned 64-bit integer types that both can hold any value from the specified range.
>

The following is a complete list of usage of IDs in the three categories for all WAMP messages. For a full definition of these see [messages section](#messages).

#### Global Scope IDs

* `WELCOME.Session`
* `PUBLISHED.Publication`
* `EVENT.Publication`


#### Router Scope IDs

* `EVENT.Subscription`
* `SUBSCRIBED.Subscription`
* `REGISTERED.Registration`
* `UNSUBSCRIBE.Subscription`
* `UNREGISTER.Registration`
* `INVOCATION.Registration`


#### Session Scope IDs

* `ERROR.Request`
* `PUBLISH.Request`
* `PUBLISHED.Request`
* `SUBSCRIBE.Request`
* `SUBSCRIBED.Request`
* `UNSUBSCRIBE.Request`
* `UNSUBSCRIBED.Request`
* `CALL.Request`
* `CANCEL.Request`
* `RESULT.Request`
* `REGISTER.Request`
* `REGISTERED.Request`
* `UNREGISTER.Request`
* `UNREGISTERED.Request`
* `INVOCATION.Request`
* `INTERRUPT.Request`
* `YIELD.Request`



## Serializations

WAMP is a message based protocol that requires serialization of messages to octet sequences to be sent out on the wire.

A message *serialization* format is assumed that (at least) provides the following types:

* `integer` (non-negative)
* `string` (UTF-8 encoded Unicode)
* `bool`
* `list`
* `dict` (with string keys)

> WAMP *itself* only uses the above types, e.g. it does not use the JSON data types `number` (non-integer) and `null`. The *application payloads* transmitted by WAMP (e.g. in call arguments or event payloads) may use other types a concrete serialization format supports.
>

There is no required serialization or set of serializations for WAMP implementations (but each implementation MUST, of course, implement at least one serialization format). Routers SHOULD implement more than one serialization format, enabling components using different kinds of serializations to connect to each other.

WAMP defines two bindings for message *serialization*:

1. JSON
2. MsgPack

Other bindings for *serialization* may be defined in future WAMP versions.

### JSON

With JSON serialization, each WAMP message is serialized according to the JSON specification as described in RFC4627.

Further, binary data follows a convention for conversion to JSON strings. For details see the Appendix.

### MsgPack

With MsgPack serialization, each WAMP message is serialized according to the MsgPack specification.

> Version 5 or later of MsgPack MUST BE used, since this version is able to differentiate between strings and binary values.


## Transports

WAMP assumes a *transport* with the following characteristics:

1. message-based
2. reliable
3. ordered
4. bidirectional (full-duplex)

There is no required transport or set of transports for WAMP implementations (but each implementation MUST, of course, implement at least one transport). Routers SHOULD implement more than one transport, enabling components using different kinds of transports to connect in an application.


### WebSocket Transport

The default transport binding for WAMP is WebSocket.

In the Basic Profile, WAMP messages are transmitted as WebSocket messages: each WAMP message is transmitted as a separate WebSocket message (not WebSocket frame). The Advanced Profile may define other modes, e.g. a **batched mode** where multiple WAMP messages are transmitted via single WebSocket message.

The WAMP protocol MUST BE negotiated during the WebSocket opening handshake between Peers using the WebSocket subprotocol negotiation mechanism.

WAMP uses the following WebSocket subprotocol identifiers for unbatched modes:

* `wamp.2.json`
* `wamp.2.msgpack`

With `wamp.2.json`, *all* WebSocket messages MUST BE of type **text** (UTF8 encoded payload) and use the JSON message serialization.

With `wamp.2.msgpack`, *all* WebSocket messages MUST BE of type **binary** and use the MsgPack message serialization.

> To avoid incompatibilities merely due to naming conflicts with WebSocket subprotocol identifiers, implementers SHOULD register identifiers for additional serialization formats with the official WebSocket subprotocol registry.


### Transport and Session Lifetime

WAMP implementations MAY choose to tie the lifetime of the underlying transport connection for a WAMP connection to that of a WAMP session, i.e. establish a new transport-layer connection as part of each new session establishment. They MAY equally choose to allow re-use of a transport connection, allowing subsequent WAMP sessions to be established using the same transport connection.

The diagram below illustrates the full transport connection and session lifecycle for an implementation which uses WebSocket over TCP as the transport and allows the re-use of a transport connection.

{align="left"}
        ,------.                                    ,------.
        | Peer |                                    | Peer |
        `--+---'                                    `--+---'

                          TCP established
           |<----------------------------------------->|
           |                                           |
           |               TLS established             |
           |+<--------------------------------------->+|
           |+                                         +|
           |+           WebSocket established         +|
           |+|<------------------------------------->|+|
           |+|                                       |+|
           |+|            WAMP established           |+|
           |+|+<----------------------------------->+|+|
           |+|+                                     +|+|
           |+|+                                     +|+|
           |+|+            WAMP closed              +|+|
           |+|+<----------------------------------->+|+|
           |+|                                       |+|
           |+|                                       |+|
           |+|            WAMP established           |+|
           |+|+<----------------------------------->+|+|
           |+|+                                     +|+|
           |+|+                                     +|+|
           |+|+            WAMP closed              +|+|
           |+|+<----------------------------------->+|+|
           |+|                                       |+|
           |+|           WebSocket closed            |+|
           |+|<------------------------------------->|+|
           |+                                         +|
           |+              TLS closed                 +|
           |+<--------------------------------------->+|
           |                                           |
           |               TCP closed                  |
           |<----------------------------------------->|

        ,--+---.                                    ,--+---.
        | Peer |                                    | Peer |
        `------'                                    `------'

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

Some WAMP messages contain `Options|dict` or `Details|dict` elements. This allows for future extensibility and implementations that only provide subsets of functionality by ignoring unimplemented attributes. Keys in `Options` and `Details` MUST be of type `string` and MUST match the regular expression `[a-z][a-z0-9_]{2,}` for WAMP *predefined* keys. Implementations MAY use implementation-specific keys that MUST match the regular expression `_[a-z0-9_]{3,}`. Attributes unknown to an implementation MUST be ignored.


## No Polymorphism

For a given `MessageType` *and* number of message elements the expected types are uniquely defined. Hence there are no polymorphic messages in WAMP. This leads to a message parsing and validation control flow that is efficient, simple to implement and simple to code for rigorous message format checking.


## Structure

The *application* payload (that is call arguments, call results, event payload etc) is always at the end of the message element list. The rationale is: Brokers and Dealers have no need to inspect (parse) the application payload. Their business is call/event routing. Having the application payload at the end of the list allows Brokers and Dealers to skip parsing it altogether. This can improve efficiency and performance.


## Message Definitions

WAMP defines the following messages that are explained in detail in the following sections.

The messages concerning the WAMP session itself are mandatory for all Peers, i.e. a Client MUST implement `HELLO`, `ABORT` and `GOODBYE`, while a Router MUST implement `WELCOME`, `ABORT` and `GOODBYE`.

All other messages are mandatory *per role*, i.e. in an implementation that only provides a Client with the role of Publisher MUST additionally implement sending `PUBLISH` and receiving `PUBLISHED` and `ERROR` messages.

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
        [ERROR, REQUEST.Type|int, REQUEST.Request|id, Details|dict,
            Error|uri]

        [ERROR, REQUEST.Type|int, REQUEST.Request|id, Details|dict,
            Error|uri, Arguments|list]

        [ERROR, REQUEST.Type|int, REQUEST.Request|id, Details|dict,
            Error|uri, Arguments|list, ArgumentsKw|dict]


### Publish & Subscribe

#### PUBLISH

Sent by a Publisher to a Broker to publish an event.

{align="left"}
        [PUBLISH, Request|id, Options|dict, Topic|uri]

        [PUBLISH, Request|id, Options|dict, Topic|uri,
            Arguments|list]

        [PUBLISH, Request|id, Options|dict, Topic|uri,
            Arguments|list, ArgumentsKw|dict]

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
        [EVENT, SUBSCRIBED.Subscription|id, PUBLISHED.Publication|id,
            Details|dict]

        [EVENT, SUBSCRIBED.Subscription|id, PUBLISHED.Publication|id,
            Details|dict, PUBLISH.Arguments|list]

        [EVENT, SUBSCRIBED.Subscription|id, PUBLISHED.Publication|id,
            Details|dict, PUBLISH.Arguments|list,
            PUBLISH.ArgumentsKw|dict]

> An event is dispatched to a Subscriber for a given `Subscription|id` *only once*. On the other hand, a Subscriber that holds subscriptions with different `Subscription|id`s that all match a given event will receive the event on each matching subscription.
>

### Routed Remote Procedure Calls

#### CALL

Call as originally issued by the *Caller* to the *Dealer*.

{align="left"}
      [CALL, Request|id, Options|dict, Procedure|uri]

      [CALL, Request|id, Options|dict, Procedure|uri, Arguments|list]

      [CALL, Request|id, Options|dict, Procedure|uri, Arguments|list,
          ArgumentsKw|dict]

#### RESULT

Result of a call as returned by *Dealer* to *Caller*.

{align="left"}
        [RESULT, CALL.Request|id, Details|dict]

        [RESULT, CALL.Request|id, Details|dict, YIELD.Arguments|list]

        [RESULT, CALL.Request|id, Details|dict, YIELD.Arguments|list,
            YIELD.ArgumentsKw|dict]

#### REGISTER

A *Callees* request to register an endpoint at a *Dealer*.

{align="left"}
        [REGISTER, Request|id, Options|dict, Procedure|uri]

#### REGISTERED

Acknowledge sent by a *Dealer* to a *Callee* for successful registration.

{align="left"}
        [REGISTERED, REGISTER.Request|id, Registration|id]

#### UNREGISTER

A *Callees* request to unregister a previously established registration.

{align="left"}
        [UNREGISTER, Request|id, REGISTERED.Registration|id]

#### UNREGISTERED

Acknowledge sent by a *Dealer* to a *Callee* for successful unregistration.

{align="left"}
        [UNREGISTERED, UNREGISTER.Request|id]

#### INVOCATION

Actual invocation of an endpoint sent by *Dealer* to a *Callee*.

{align="left"}
        [INVOCATION, Request|id, REGISTERED.Registration|id,
            Details|dict]

        [INVOCATION, Request|id, REGISTERED.Registration|id,
            Details|dict, C* Arguments|list]

        [INVOCATION, Request|id, REGISTERED.Registration|id,
            Details|dict, CALL.Arguments|list, CALL.ArgumentsKw|dict]

#### YIELD

Actual yield from an endpoint sent by a *Callee* to *Dealer*.

{align="left"}
        [YIELD, INVOCATION.Request|id, Options|dict]

        [YIELD, INVOCATION.Request|id, Options|dict, Arguments|list]

        [YIELD, INVOCATION.Request|id, Options|dict, Arguments|list,
            ArgumentsKw|dict]



## Message Codes and Direction

The following table lists the message type code for **all 25 messages defined in the WAMP basic profile** and their direction between peer roles.

Reserved codes may be used to identify additional message types in future standards documents.

> "Tx" indicates the message is sent by the respective role, and "Rx" indicates the message is received by the respective role.

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
        [CALL, Request|id, Options|dict, Procedure|uri,
            Arguments|list]

where `Arguments == []` SHOULD be avoided, and instead

{align="left"}
        [CALL, Request|id, Options|dict, Procedure|uri]

SHOULD be sent.

Implementations SHOULD avoid sending empty `ArgumentsKw` dictionaries.

E.g. a `CALL` message

{align="left"}
        [CALL, Request|id, Options|dict, Procedure|uri,
            Arguments|list, ArgumentsKw|dict]

where `ArgumentsKw == {}` SHOULD be avoided, and instead

{align="left"}
        [CALL, Request|id, Options|dict, Procedure|uri,
            Arguments|list]

SHOULD be sent when `Arguments` is non-empty.


# Sessions

The message flow between *Clients* and *Routers* for opening and closing WAMP sessions involves the following messages:

1. `HELLO`
2. `WELCOME`
3. `ABORT`
4. `GOODBYE`

## Session Establishment

### HELLO

After the underlying transport has been established, the opening of a WAMP session is initiated by the *Client* sending a `HELLO` message to the *Router*

{align="left"}
        [HELLO, Realm|uri, Details|dict]

where

* `Realm` is a string identifying the realm this session should attach to
* `Details` is a dictionary that allows to provide additional opening information (see below).

The `HELLO` message MUST be the very first message sent by the *Client* after the transport has been established.

In the WAMP Basic Profile without session authentication the *Router* will reply with a `WELCOME` or `ABORT` message.

{align="left"}
        ,------.          ,------.
        |Client|          |Router|
        `--+---'          `--+---'
           |      HELLO      |
           | ---------------->
           |                 |
           |     WELCOME     |
           | <----------------
        ,--+---.          ,--+---.
        |Client|          |Router|
        `------'          `------'


A WAMP session starts its lifetime when the *Router* has sent a `WELCOME` message to the *Client*, and ends when the underlying transport closes or when the session is closed explicitly by either peer sending the `GOODBYE` message (see below).

It is a protocol error to receive a second `HELLO` message during the lifetime of the session and the *Peer* must fail the session if that happens.

#### Client: Role and Feature Announcement

WAMP uses *Role & Feature announcement* instead of *protocol versioning* to allow

* implementations only supporting subsets of functionality
* future extensibility

A *Client* must announce the **roles** it supports via `Hello.Details.roles|dict`, with a key mapping to a `Hello.Details.roles.<role>|dict` where `<role>` can be:

* `publisher`
* `subscriber`
* `caller`
* `callee`

A *Client* can support any combination of the above roles but must support at least one role.

The `<role>|dict` is a dictionary describing **features** supported by the peer for that role.

This MUST be empty for WAMP Basic Profile implementations, and MUST be used by implementations implementing parts of the Advanced Profile to list the specific set of features they support.

*Example: A Client that implements the Publisher and Subscriber roles of the WAMP Basic Profile.*

{align="left"}
        [1, "somerealm", {
          "roles": {
              "publisher": {},
              "subscriber": {}
          }
        }]

### WELCOME

A *Router* completes the opening of a WAMP session by sending a `WELCOME` reply message to the *Client*.

{align="left"}
        [WELCOME, Session|id, Details|dict]

where

* `Session` MUST be a randomly generated ID specific to the WAMP session. This applies for the lifetime of the session.
* `Details` is a dictionary that allows to provide additional information regarding the open session (see below).

In the WAMP Basic Profile without session authentication, a `WELCOME` message MUST be the first message sent by the *Router*, directly in response to a `HELLO` message received from the *Client*. Extensions in the Advanced Profile MAY include intermediate steps and messages for authentication.

> Note. The behavior if a requested `Realm` does not presently exist is router-specific. A router may e.g. automatically create the realm, or deny the establishment of the session with a `ABORT` reply message.
>

#### Router: Role and Feature Announcement

Similar to a *Client* announcing *Roles* and *Features* supported in the ``HELLO` message, a *Router* announces its supported *Roles* and *Features* in the `WELCOME` message.

A *Router* MUST announce the **roles** it supports via `Welcome.Details.roles|dict`, with a key mapping to a `Welcome.Details.roles.<role>|dict` where `<role>` can be:

* `broker`
* `dealer`

A *Router* must support at least one role, and MAY support both roles.

The `<role>|dict` is a dictionary describing **features** supported by the peer for that role. With WAMP Basic Profile implementations, this MUST be empty, but MUST be used by implementations implementing parts of the Advanced Profile to list the specific set of features they support

*Example: A Router implementing the Broker role of the WAMP Basic Profile.*

{align="left"}
        [2, 9129137332, {
           "roles": {
              "broker": {}
           }
        }]

### ABORT

Both the *Router* and the *Client* may abort the opening of a WAMP session by sending an `ABORT` message.

{align="left"}
        [ABORT, Details|dict, Reason|uri]

where

* `Reason` MUST be an URI.
* `Details` MUST be a dictionary that allows to provide additional, optional closing information (see below).

No response to an `ABORT` message is expected.

{align="left"}
        ,------.          ,------.
        |Client|          |Router|
        `--+---'          `--+---'
           |      HELLO      |
           | ---------------->
           |                 |
           |      ABORT      |
           | <----------------
        ,--+---.          ,--+---.
        |Client|          |Router|
        `------'          `------'


*Example*

{align="left"}
        [3, {"message": "The realm does not exist."},
            "wamp.error.no_such_realm"]


## Session Closing

A WAMP session starts its lifetime with the *Router* sending a `WELCOME` message to the *Client* and ends when the underlying transport disappears or when the WAMP session is closed explicitly by a `GOODBYE` message sent by one *Peer* and a `GOODBYE` message sent from the other *Peer* in response.

{align="left"}
        [GOODBYE, Details|dict, Reason|uri]

where

* `Reason` MUST be an URI.
* `Details` MUST be a dictionary that allows to provide additional, optional closing information (see below).

{align="left"}
        ,------.          ,------.
        |Client|          |Router|
        `--+---'          `--+---'
           |     GOODBYE     |
           | ---------------->
           |                 |
           |     GOODBYE     |
           | <----------------
        ,--+---.          ,--+---.
        |Client|          |Router|
        `------'          `------'


{align="left"}
        ,------.          ,------.
        |Client|          |Router|
        `--+---'          `--+---'
           |     GOODBYE     |
           | <----------------
           |                 |
           |     GOODBYE     |
           | ---------------->
        ,--+---.          ,--+---.
        |Client|          |Router|
        `------'          `------'

*Example*. One *Peer* initiates closing

{align="left"}
        [6, {"message": "The host is shutting down now."},
            "wamp.error.system_shutdown"]

and the other peer replies

{align="left"}
        [6, {}, "wamp.error.goodbye_and_out"]


*Example*. One *Peer* initiates closing

{align="left"}
        [6, {}, "wamp.error.close_realm"]

and the other peer replies

{align="left"}
        [6, {}, "wamp.error.goodbye_and_out"]


### Difference between ABORT and GOODBYE

The differences between `ABORT` and `GOODBYE` messages are:

1. `ABORT` gets sent only *before* a *Session* is established, while `GOODBYE` is sent only *after* a *Session* is already established.
2. `ABORT` is never replied to by a *Peer*, whereas `GOODBYE` must be replied to by the receiving *Peer*

> Though `ABORT` and `GOODBYE` are structurally identical, using different message types serves to reduce overloaded meaning of messages and simplify message handling code.
>


## Agent Identification

When a software agent operates in a network protocol, it often identifies itself, its application type, operating system, software vendor, or software revision, by submitting a characteristic identification string to its operating peer.

Similar to what browsers do with the `User-Agent` HTTP header, both the `HELLO` and the `WELCOME` message MAY disclose the WAMP implementation in use to its peer:

{align="left"}
        HELLO.Details.agent|string

and

{align="left"}
        WELCOME.Details.agent|string

*Example: A Client "HELLO" message.*

{align="left"}
        [1, "somerealm", {
             "agent": "AutobahnJS-0.9.14",
             "roles": {
                "subscriber": {},
                "publisher": {}
             }
        }]


*Example: A Router "WELCOME" message.*

{align="left"}
        [2, 9129137332, {
            "agent": "Crossbar.io-0.10.11",
            "roles": {
              "broker": {}
            }
        }]


# Publish and Subscribe

All of the following features for Publish & Subscribe are mandatory for WAMP Basic Profile implementations supporting the respective roles, i.e. *Publisher*, *Subscriber* and *Dealer*.


## Subscribing and Unsubscribing

The message flow between *Clients* implementing the role of *Subscriber* and *Routers* implementing the role of *Broker* for subscribing and unsubscribing involves the following messages:

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


A *Subscriber* may subscribe to zero, one or more topics, and a *Publisher* publishes to topics without knowledge of subscribers.

Upon subscribing to a topic via the `SUBSCRIBE` message, a *Subscriber* will receive any future events published to the respective topic by *Publishers*, and will receive those events asynchronously.

A subscription lasts for the duration of a session, unless a *Subscriber* opts out from a previously established subscription via the `UNSUBSCRIBE` message.

> A *Subscriber* may have more than one event handler attached to the same subscription. This can be implemented in different ways: a) a *Subscriber* can recognize itself that it is already subscribed and just attach another handler to the subscription for incoming events, b) or it can send a new `SUBSCRIBE` message to broker (as it would be first) and upon receiving a `SUBSCRIBED.Subscription|id` it already knows about, attach the handler to the existing subscription
>

### SUBSCRIBE

A *Subscriber* communicates its interest in a topic to a *Broker* by sending a `SUBSCRIBE` message:

{align="left"}
        [SUBSCRIBE, Request|id, Options|dict, Topic|uri]

where

 * `Request` MUST be a random, ephemeral ID chosen by the *Subscriber* and used to correlate the *Broker's* response with the request.
 * `Options` MUST be a dictionary that allows to provide additional subscription request details in a extensible way. This is described further below.
 * `Topic` is the topic the *Subscriber* wants to subscribe to and MUST be an URI.

*Example*

{align="left"}
        [32, 713845233, {}, "com.myapp.mytopic1"]

A *Broker*, receiving a `SUBSCRIBE` message, can fullfill or reject the subscription, so it answers with `SUBSCRIBED` or `ERROR` messages.

### SUBSCRIBED

If the *Broker* is able to fulfill and allow the subscription, it answers by sending a `SUBSCRIBED` message to the *Subscriber*

{align="left"}
        [SUBSCRIBED, SUBSCRIBE.Request|id, Subscription|id]

where

 * `SUBSCRIBE.Request` MUST be the ID from the original request.
 * `Subscription` MUST be an ID chosen by the *Broker* for the subscription.

*Example*

{align="left"}
        [33, 713845233, 5512315355]

> Note. The `Subscription` ID chosen by the broker need not be unique to the subscription of a single *Subscriber*, but may be assigned to the `Topic`, or the combination of the `Topic` and some or all `Options`, such as the topic pattern matching method to be used. Then this ID may be sent to all *Subscribers* for the `Topic` or `Topic` /  `Options` combination. This allows the *Broker* to serialize an event to be delivered only once for all actual receivers of the event.

> In case of receiving a `SUBSCRIBE` message from the same *Subscriber* and to already subscribed topic, *Broker* should answer with `SUBSCRIBED` message, containing the existing `Subscription|id`.

### Subscribe ERROR

When the request for subscription cannot be fulfilled by the *Broker*, the *Broker* sends back an `ERROR` message to the *Subscriber*

{align="left"}
        [ERROR, SUBSCRIBE, SUBSCRIBE.Request|id, Details|dict,
            Error|uri]

where

 * `SUBSCRIBE.Request` MUST be the ID from the original request.
 * `Error` MUST be an URI that gives the error of why the request could not be fulfilled.

*Example*

{align="left"}
        [8, 32, 713845233, {}, "wamp.error.not_authorized"]


### UNSUBSCRIBE

When a *Subscriber* is no longer interested in receiving events for a subscription it sends an `UNSUBSCRIBE` message

{align="left"}
        [UNSUBSCRIBE, Request|id, SUBSCRIBED.Subscription|id]

where

 * `Request` MUST be a random, ephemeral ID chosen by the *Subscriber* and used to correlate the *Broker's* response with the request.
 * `SUBSCRIBED.Subscription` MUST be the ID for the subscription to unsubscribe from, originally handed out by the *Broker* to the *Subscriber*.

*Example*

{align="left"}
        [34, 85346237, 5512315355]

### UNSUBSCRIBED

Upon successful unsubscription, the *Broker* sends an `UNSUBSCRIBED` message to the *Subscriber*

{align="left"}
        [UNSUBSCRIBED, UNSUBSCRIBE.Request|id]

where

 * `UNSUBSCRIBE.Request` MUST be the ID from the original request.

*Example*

{align="left"}
        [35, 85346237]


### Unsubscribe ERROR

When the request fails, the *Broker* sends an `ERROR`

{align="left"}
        [ERROR, UNSUBSCRIBE, UNSUBSCRIBE.Request|id, Details|dict,
            Error|uri]

where

 * `UNSUBSCRIBE.Request` MUST be the ID from the original request.
 * `Error` MUST be an URI that gives the error of why the request could not be fulfilled.

*Example*

{align="left"}
        [8, 34, 85346237, {}, "wamp.error.no_such_subscription"]



## Publishing and Events

The message flow between *Publishers*, a *Broker* and *Subscribers* for publishing to topics and dispatching events involves the following messages:

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

When a *Publisher* requests to publish an event to some topic, it sends a `PUBLISH` message to a *Broker*:

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

* `Request` is a random, ephemeral ID chosen by the *Publisher* and used to correlate the *Broker's* response with the request.
* `Options` is a dictionary that allows to provide additional publication request details in an extensible way. This is described further below.
* `Topic` is the topic published to.
* `Arguments` is a list of application-level event payload elements. The list may be of zero length.
* `ArgumentsKw` is an optional dictionary containing application-level event payload, provided as keyword arguments. The dictionary may be empty.

If the *Broker* is able to fulfill and allowing the publication, the *Broker* will send the event to all current *Subscribers* of the topic of the published event.

By default, publications are unacknowledged, and the *Broker* will not respond, whether the publication was successful indeed or not. This behavior can be changed with the option `PUBLISH.Options.acknowledge|bool` (see below).

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

If the *Broker* is able to fulfill and allowing the publication, and `PUBLISH.Options.acknowledge == true`, the *Broker* replies by sending a `PUBLISHED` message to the *Publisher*:

{align="left"}
        [PUBLISHED, PUBLISH.Request|id, Publication|id]

where

* `PUBLISH.Request` is the ID from the original publication request.
* `Publication` is a ID chosen by the Broker for the publication.

*Example*

{align="left"}
        [17, 239714735, 4429313566]


### Publish ERROR

When the request for publication cannot be fulfilled by the *Broker*, and `PUBLISH.Options.acknowledge == true`, the *Broker* sends back an `ERROR` message to the *Publisher*

{align="left"}
        [ERROR, PUBLISH, PUBLISH.Request|id, Details|dict, Error|uri]

where

 * `PUBLISH.Request` is the ID from the original publication request.
 * `Error` is an URI that gives the error of why the request could not be fulfilled.

*Example*

{align="left"}
        [8, 16, 239714735, {}, "wamp.error.not_authorized"]


### EVENT

When a publication is successful and a *Broker* dispatches the event, it determines a list of receivers for the event based on *Subscribers* for the topic published to and, possibly, other information in the event.

Note that the *Publisher* of an event will never receive the published event even if the *Publisher* is also a *Subscriber* of the topic published to.

> The Advanced Profile provides options for more detailed control over publication.
>

When a *Subscriber* is deemed to be a receiver, the *Broker* sends the *Subscriber* an `EVENT` message:

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

* `SUBSCRIBED.Subscription` is the ID for the subscription under which the *Subscriber* receives the event - the ID for the subscription originally handed out by the *Broker* to the *Subscriber*.
* `PUBLISHED.Publication` is the ID of the publication of the published event.
* `Details` is a dictionary that allows the *Broker* to provide additional event details in a extensible way. This is described further below.
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



# Remote Procedure Calls

All of the following features for Remote Procedure Calls are mandatory for WAMP Basic Profile implementations supporting the respective roles.


## Registering and Unregistering

The message flow between *Callees* and a *Dealer* for registering and unregistering endpoints to be called over RPC involves the following messages:

1. `REGISTER`
2. `REGISTERED`
4. `UNREGISTER`
5. `UNREGISTERED`
6. `ERROR`

{align="left"}
        ,------.          ,------.               ,------.
        |Caller|          |Dealer|               |Callee|
        `--+---'          `--+---'               `--+---'
           |                 |                      |
           |                 |                      |
           |                 |       REGISTER       |
           |                 | <---------------------
           |                 |                      |
           |                 |  REGISTERED or ERROR |
           |                 | --------------------->
           |                 |                      |
           |                 |                      |
           |                 |                      |
           |                 |                      |
           |                 |                      |
           |                 |      UNREGISTER      |
           |                 | <---------------------
           |                 |                      |
           |                 | UNREGISTERED or ERROR|
           |                 | --------------------->
        ,--+---.          ,--+---.               ,--+---.
        |Caller|          |Dealer|               |Callee|
        `------'          `------'               `------'


### REGISTER

A *Callee* announces the availability of an endpoint implementing a procedure with a *Dealer* by sending a `REGISTER` message:

{align="left"}
        [REGISTER, Request|id, Options|dict, Procedure|uri]

where

* `Request` is a random, ephemeral ID chosen by the *Callee* and used to correlate the *Dealer's* response with the request.
* `Options` is a dictionary that allows to provide additional registration request details in a extensible way. This is described further below.
* `Procedure`is the procedure the *Callee* wants to register

*Example*

{align="left"}
        [64, 25349185, {}, "com.myapp.myprocedure1"]

### REGISTERED

If the *Dealer* is able to fulfill and allowing the registration, it answers by sending a `REGISTERED` message to the `Callee`:

{align="left"}
        [REGISTERED, REGISTER.Request|id, Registration|id]

where

* `REGISTER.Request` is the ID from the original request.
*  `Registration` is an ID chosen by the *Dealer* for the registration.

*Example*

{align="left"}
        [65, 25349185, 2103333224]

### Register ERROR

When the request for registration cannot be fulfilled by the *Dealer*, the *Dealer* sends back an `ERROR` message to the *Callee*:

{align="left"}
        [ERROR, REGISTER, REGISTER.Request|id, Details|dict, Error|uri]

where

* `REGISTER.Request` is the ID from the original request.
* `Error` is an URI that gives the error of why the request could not be fulfilled.

*Example*

{align="left"}
        [8, 64, 25349185, {}, "wamp.error.procedure_already_exists"]

### UNREGISTER

When a *Callee* is no longer willing to provide an implementation of the registered procedure, it sends an `UNREGISTER` message to the *Dealer*:

{align="left"}
        [UNREGISTER, Request|id, REGISTERED.Registration|id]

where

* `Request` is a random, ephemeral ID chosen by the *Callee* and used to correlate the *Dealer's* response with the request.
* `REGISTERED.Registration` is the ID for the registration to revoke, originally handed out by the *Dealer* to the *Callee*.

*Example*

{align="left"}
        [66, 788923562, 2103333224]

### UNREGISTERED

Upon successful unregistration, the *Dealer* sends an `UNREGISTERED` message to the *Callee*:

{align="left"}
        [UNREGISTERED, UNREGISTER.Request|id]

where

* `UNREGISTER.Request` is the ID from the original request.

*Example*

{align="left"}
        [67, 788923562]

### Unregister ERROR

When the unregistration request fails, the *Dealer* sends an `ERROR` message:

{align="left"}
        [ERROR, UNREGISTER, UNREGISTER.Request|id, Details|dict,
            Error|uri]

where

* `UNREGISTER.Request` is the ID from the original request.
* `Error` is an URI that gives the error of why the request could not be fulfilled.

*Example*

{align="left"}
        [8, 66, 788923562, {}, "wamp.error.no_such_registration"]


## Calling and Invocations

The message flow between *Callers*, a *Dealer* and *Callees* for calling procedures and invoking endpoints involves the following messages:

1. `CALL`
2. `RESULT`
3. `INVOCATION`
4. `YIELD`
5. `ERROR`

{align="left"}
        ,------.          ,------.          ,------.
        |Caller|          |Dealer|          |Callee|
        `--+---'          `--+---'          `--+---'
           |       CALL      |                 |
           | ---------------->                 |
           |                 |                 |
           |                 |    INVOCATION   |
           |                 | ---------------->
           |                 |                 |
           |                 |  YIELD or ERROR |
           |                 | <----------------
           |                 |                 |
           | RESULT or ERROR |                 |
           | <----------------                 |
        ,--+---.          ,--+---.          ,--+---.
        |Caller|          |Dealer|          |Callee|
        `------'          `------'          `------'


The execution of remote procedure calls is asynchronous, and there may be more than one call outstanding. A call is called outstanding (from the point of view of the *Caller*), when a (final) result or error has not yet been received by the *Caller*.

### CALL

When a *Caller* wishes to call a remote procedure, it sends a `CALL` message to a *Dealer*:

{align="left"}
        [CALL, Request|id, Options|dict, Procedure|uri]

or

{align="left"}
        [CALL, Request|id, Options|dict, Procedure|uri, Arguments|list]

or

{align="left"}
        [CALL, Request|id, Options|dict, Procedure|uri, Arguments|list,
            ArgumentsKw|dict]

where

* `Request` is a random, ephemeral ID chosen by the *Caller* and used to correlate the *Dealer's* response with the request.
* `Options` is a dictionary that allows to provide additional call request details in an extensible way. This is described further below.
* `Procedure` is the URI of the procedure to be called.
* `Arguments` is a list of positional call arguments (each of arbitrary type). The list may be of zero length.
* `ArgumentsKw` is a dictionary of keyword call arguments (each of arbitrary type). The dictionary may be empty.

*Example*

{align="left"}
        [48, 7814135, {}, "com.myapp.ping"]

*Example*

{align="left"}
        [48, 7814135, {}, "com.myapp.echo", ["Hello, world!"]]

*Example*

{align="left"}
        [48, 7814135, {}, "com.myapp.add2", [23, 7]]

*Example*

{align="left"}
        [48, 7814135, {}, "com.myapp.user.new", ["johnny"],
            {"firstname": "John", "surname": "Doe"}]


### INVOCATION

If the *Dealer* is able to fulfill (mediate) the call and it allows the call, it sends a `INVOCATION` message to the respective *Callee* implementing the procedure:

{align="left"}
        [INVOCATION, Request|id, REGISTERED.Registration|id,
            Details|dict]

or

{align="left"}
        [INVOCATION, Request|id, REGISTERED.Registration|id,
            Details|dict, CALL.Arguments|list]

or

{align="left"}
        [INVOCATION, Request|id, REGISTERED.Registration|id,
            Details|dict, CALL.Arguments|list, CALL.ArgumentsKw|dict]

where

* `Request` is a random, ephemeral ID chosen by the *Dealer* and used to correlate the *Callee's* response with the request.
* `REGISTERED.Registration` is the registration ID under which the procedure was registered at the *Dealer*.
* `Details` is a dictionary that allows to provide additional invocation request details in an extensible way. This is described further below.
* `CALL.Arguments` is the original list of positional call arguments as provided by the *Caller*.
* `CALL.ArgumentsKw` is the original dictionary of keyword call arguments as provided by the *Caller*.

*Example*

{align="left"}
        [68, 6131533, 9823526, {}]

*Example*

{align="left"}
        [68, 6131533, 9823527, {}, ["Hello, world!"]]

*Example*

{align="left"}
        [68, 6131533, 9823528, {}, [23, 7]]

*Example*

{align="left"}
        [68, 6131533, 9823529, {}, ["johnny"], {"firstname": "John",
            "surname": "Doe"}]


### YIELD

If the *Callee* is able to successfully process and finish the execution of the call, it answers by sending a `YIELD` message to the *Dealer*:

{align="left"}
        [YIELD, INVOCATION.Request|id, Options|dict]

or

{align="left"}
        [YIELD, INVOCATION.Request|id, Options|dict, Arguments|list]

or

{align="left"}
        [YIELD, INVOCATION.Request|id, Options|dict, Arguments|list,
            ArgumentsKw|dict]

where

* `INVOCATION.Request` is the ID from the original invocation request.
* `Options`is a dictionary that allows to provide additional options.
* `Arguments` is a list of positional result elements (each of arbitrary type). The list may be of zero length.
* `ArgumentsKw` is a dictionary of keyword result elements (each of arbitrary type). The dictionary may be empty.


*Example*

{align="left"}
        [70, 6131533, {}]

*Example*

{align="left"}
        [70, 6131533, {}, ["Hello, world!"]]

*Example*

{align="left"}
        [70, 6131533, {}, [30]]

*Example*

{align="left"}
        [70, 6131533, {}, [], {"userid": 123, "karma": 10}]


### RESULT

The *Dealer* will then send a `RESULT` message to the original *Caller*:

{align="left"}
        [RESULT, CALL.Request|id, Details|dict]

or

{align="left"}
        [RESULT, CALL.Request|id, Details|dict, YIELD.Arguments|list]

or

{align="left"}
        [RESULT, CALL.Request|id, Details|dict, YIELD.Arguments|list,
            YIELD.ArgumentsKw|dict]

where

* `CALL.Request` is the ID from the original call request.
* `Details` is a dictionary of additional details.
* `YIELD.Arguments` is the original list of positional result elements as returned by the *Callee*.
* `YIELD.ArgumentsKw` is the original dictionary of keyword result elements as returned by the *Callee*.

*Example*

{align="left"}
        [50, 7814135, {}]

*Example*

{align="left"}
        [50, 7814135, {}, ["Hello, world!"]]

*Example*

{align="left"}
        [50, 7814135, {}, [30]]

*Example*

{align="left"}
        [50, 7814135, {}, [], {"userid": 123, "karma": 10}]


### Invocation ERROR


If the *Callee* is unable to process or finish the execution of the call, or the application code implementing the procedure raises an exception or otherwise runs into an error, the *Callee* sends an `ERROR` message to the *Dealer*:

{align="left"}
        [ERROR, INVOCATION, INVOCATION.Request|id, Details|dict,
            Error|uri]

or

{align="left"}
        [ERROR, INVOCATION, INVOCATION.Request|id, Details|dict,
        Error|uri, Arguments|list]

or

{align="left"}
        [ERROR, INVOCATION, INVOCATION.Request|id, Details|dict,
            Error|uri, Arguments|list, ArgumentsKw|dict]

where

* `INVOCATION.Request` is the ID from the original `INVOCATION` request previously sent by the *Dealer* to the *Callee*.
* `Details` is a dictionary with additional error details.
* `Error` is an URI that identifies the error of why the request could not be fulfilled.
* `Arguments` is a list containing arbitrary, application defined, positional error information. This will be forwarded by the *Dealer* to the *Caller* that initiated the call.
* `ArgumentsKw` is a dictionary containing arbitrary, application defined, keyword-based error information. This will be forwarded by the *Dealer* to the *Caller* that initiated the call.

*Example*

{align="left"}
        [8, 68, 6131533, {}, "com.myapp.error.object_write_protected",
            ["Object is write protected."], {"severity": 3}]


### Call ERROR

The *Dealer* will then send a `ERROR` message to the original *Caller*:

{align="left"}
        [ERROR, CALL, CALL.Request|id, Details|dict, Error|uri]

or

{align="left"}
        [ERROR, CALL, CALL.Request|id, Details|dict, Error|uri,
            Arguments|list]

or

{align="left"}
        [ERROR, CALL, CALL.Request|id, Details|dict, Error|uri,
            Arguments|list, ArgumentsKw|dict]

where

* `CALL.Request` is the ID from the original `CALL` request sent by the *Caller* to the *Dealer*.
* `Details` is a dictionary with additional error details.
* `Error` is an URI identifying the type of error as returned by the *Callee* to the *Dealer*.
* `Arguments` is a list containing the original error payload list as returned by the *Callee* to the *Dealer*.
* `ArgumentsKw` is a dictionary containing the original error payload dictionary as returned by the *Callee* to the *Dealer*

*Example*

{align="left"}
        [8, 48, 7814135, {}, "com.myapp.error.object_write_protected",
            ["Object is write protected."], {"severity": 3}]

If the original call already failed at the *Dealer* **before** the call would have been forwarded to any *Callee*, the *Dealer* will send an `ERROR` message to the *Caller*:

{align="left"}
        [ERROR, CALL, CALL.Request|id, Details|dict, Error|uri]

*Example*

{align="left"}
        [8, 48, 7814135, {}, "wamp.error.no_such_procedure"]



# Predefined URIs

WAMP pre-defines the following error URIs as part of this Basic Profile, which cover the full set of error states for the Basic Profile. Additional error URIs are defined as part of the Advanced Profile to cover error states for the Advanced Profile. WAMP peers MUST use only the defined error messages.

## Incorrect URIs

When a *Peer* provides an incorrect URI for any URI-based attribute of a WAMP message (e.g. realm, topic), then the other *Peer* MUST respond with an `ERROR` message and give the following *Error URI*:

{align="left"}
        wamp.error.invalid_uri


## Interaction

*Peer* provided an incorrect URI for any URI-based attribute of WAMP message, such as realm, topic or procedure

{align="left"}
        wamp.error.invalid_uri

A *Dealer* could not perform a call, since no procedure is currently registered under the given URI.

{align="left"}
        wamp.error.no_such_procedure

A procedure could not be registered, since a procedure with the given URI is already registered.

{align="left"}
        wamp.error.procedure_already_exists

A *Dealer* could not perform an unregister, since the given registration is not active.

{align="left"}
        wamp.error.no_such_registration

A *Broker* could not perform an unsubscribe, since the given subscription is not active.

{align="left"}
        wamp.error.no_such_subscription

A call failed since the given argument types or values are not acceptable to the called procedure. In this case the *Callee* may throw this error. Alternatively a *Router* may throw this error if it performed *payload validation* of a call, call result, call error or publish, and the payload did not conform to the requirements.

{align="left"}
        wamp.error.invalid_argument

## Session Close

The *Peer* is shutting down completely - used as a `GOODBYE` (or `ABORT`) reason.

{align="left"}
        wamp.error.system_shutdown

The *Peer* want to leave the realm - used as a `GOODBYE` reason.

{align="left"}
        wamp.error.close_realm

A *Peer* acknowledges ending of a session - used as a `GOODBYE` reply reason.

{align="left"}
        wamp.error.goodbye_and_out

## Authorization

A join, call, register, publish or subscribe failed, since the *Peer* is not authorized to perform the operation.

{align="left"}
        wamp.error.not_authorized

A *Dealer* or *Broker* could not determine if the *Peer* is authorized to perform a join, call, register, publish or subscribe, since the authorization operation *itself* failed. E.g. a custom authorizer did run into an error.

{align="left"}
        wamp.error.authorization_failed

*Peer* wanted to join a non-existing realm (and the *Router* did not allow to auto-create the realm).

{align="left"}
        wamp.error.no_such_realm

A *Peer* was to be authenticated under a Role that does not (or no longer) exists on the Router. For example, the *Peer* was successfully authenticated, but the Role configured does not exists - hence there is some misconfiguration in the Router.

{align="left"}
        wamp.error.no_such_role


# Ordering Guarantees

All WAMP implementations, in particular *Routers* MUST support the following ordering guarantees.

> A WAMP Advanced Profile may provide applications options to relax ordering guarantees, in particular with distributed calls.
>

## Publish & Subscribe Ordering

Regarding **Publish & Subscribe**, the ordering guarantees are as follows:

If *Subscriber A* is subscribed to both **Topic 1** and **Topic 2**, and *Publisher B* first publishes an **Event 1** to **Topic 1** and then an **Event 2** to **Topic 2**, then *Subscriber A* will first receive **Event 1** and then **Event 2**. This also holds if **Topic 1** and **Topic 2** are identical.

In other words, WAMP guarantees ordering of events between any given *pair* of *Publisher* and *Subscriber*.

Further, if *Subscriber A* subscribes to **Topic 1**, the `SUBSCRIBED` message will be sent by the *Broker* to *Subscriber A* before any `EVENT` message for **Topic 1**.

There is no guarantee regarding the order of return for multiple subsequent subscribe requests. A subscribe request might require the *Broker* to do a time-consuming lookup in some database, whereas another subscribe request second might be permissible immediately.


## Remote Procedure Call Ordering

Regarding **Remote Procedure Calls**, the ordering guarantees are as follows:

If *Callee A* has registered endpoints for both **Procedure 1** and **Procedure 2**, and *Caller B* first issues a **Call 1** to **Procedure 1** and then a **Call 2** to **Procedure 2**, and both calls are routed to *Callee A*, then *Callee A* will first receive an invocation corresponding to **Call 1** and then **Call 2**. This also holds if **Procedure 1** and **Procedure 2** are identical.

In other words, WAMP guarantees ordering of invocations between any given *pair* of *Caller* and *Callee*.

There are no guarantees on the order of call results and errors in relation to *different* calls, since the execution of calls upon different invocations of endpoints in *Callees* are running independently. A first call might require an expensive, long-running computation, whereas a second, subsequent call might finish immediately.

Further, if *Callee A* registers for **Procedure 1**, the `REGISTERED` message will be sent by *Dealer* to *Callee A* before any `INVOCATION` message for **Procedure 1**.

There is no guarantee regarding the order of return for multiple subsequent register requests. A register request might require the *Broker* to do a time-consuming lookup in some database, whereas another register request second might be permissible immediately.



# Security Model

The following discusses the security model for the Basic Profile. Any changes or extensions to this for the Advanced Profile are discussed further on as part of the Advanced Profile definition.

## Transport Encryption and Integrity

WAMP transports may provide (optional) transport-level encryption and integrity verification. If so, encryption and integrity is point-to-point: between a *Client* and the *Router* it is connected to.

Transport-level encryption and integrity is solely at the transport-level and transparent to WAMP. WAMP itself deliberately does not specify any kind of transport-level encryption.

Implementations that offer TCP based transport such as WAMP-over-WebSocket or WAMP-over-RawSocket SHOULD implement Transport Layer Security (TLS).

WAMP deployments are encouraged to stick to a TLS-only policy with the TLS code and setup being hardened.

Further, when a *Client* connects to a *Router* over a local-only transport such as Unix domain sockets, the integrity of the data transmitted is implicit (the OS kernel is trusted), and the privacy of the data transmitted can be assured using file system permissions (no one can tap a Unix domain socket without appropriate permissions or being root).

## Router Authentication

To authenticate *Routers* to *Clients*, deployments MUST run TLS and *Clients* MUST verify the *Router* server certificate presented. WAMP itself does not provide mechanisms to authenticate a *Router* (only a *Client*).

The verification of the *Router* server certificate can happen

1. against a certificate trust database that comes with the *Clients* operating system
2. against an issuing certificate/key hard-wired into the *Client*
3. by using new mechanisms like DNS-based Authentication of Named Enitities (DNSSEC)/TLSA

Further, when a *Client* connects to a *Router* over a local-only transport such as Unix domain sockets, the file system permissions can be used to create implicit trust. E.g. if only the OS user under which the *Router* runs has the permission to create a Unix domain socket under a specific path, *Clients* connecting to that path can trust in the router authenticity.

## Client Authentication

Authentication of a *Client* to a *Router* at the WAMP level is not part of the basic profile.

When running over TLS, a *Router* MAY authenticate a *Client* at the transport level by doing a *client certificate based authentication*.

### Routers are trusted

*Routers* are *trusted* by *Clients*.

In particular, *Routers* can read (and modify) any application payload transmitted in events, calls, call results and call errors (the `Arguments` or `ArgumentsKw` message fields).

Hence, *Routers* do not provide confidentiality with respect to application payload, and also do not provide authenticity or integrity of application payloads that could be verified by a receiving *Client*.

*Routers* need to read the application payloads in cases of automatic conversion between different serialization formats.

Further, *Routers* are trusted to **actually perform** routing as specified. E.g. a *Client* that publishes an event has to trust a *Router* that the event is actually dispatched to all (eligible) *Subscribers* by the *Router*.

A rogue *Router* might deny normal routing operation without a *Client* taking notice.


# Advanced Profile

While implementations MUST implement the subset of the Basic Profile necessary for the particular set of WAMP roles they provide, they MAY implement any subset of features from the Advanced Profile. Implementers SHOULD implement the maximum of features possible considering the aims of an implementation.

> Note: Features listed here may be experimental or underspecced and yet unimplemented in any implementation. This is part of the specification is very much a work in progress. An approximate status of each feature is given at the beginning of the feature section.

{{rfc/text/adv_messages.md}}

{{rfc/text/adv_features.md}}


## Advanced RPC Features

{{rfc/text/adv_rpc_progressive_call_results.md}}

{{rfc/text/adv_rpc_progressive_calls.md}}

{{rfc/text/adv_rpc_call_timeout.md}}

{{rfc/text/adv_rpc_call_canceling.md}}

{{rfc/text/adv_rpc_caller_identification.md}}

{{rfc/text/adv_rpc_call_trustlevels.md}}

{{rfc/text/adv_rpc_registration_meta_api.md}}

{{rfc/text/adv_rpc_pattern_based_registration.md}}

{{rfc/text/adv_rpc_shared_registration.md}}

{{rfc/text/adv_rpc_sharded_registration.md}}

{{rfc/text/adv_rpc_registration_revocation.md}}

{{rfc/text/adv_rpc_procedure_reflection.md}}


## Advanced PubSub Featrues

{{rfc/text/adv_pubsub_subscriber_blackwhite_listing.md}}

{{rfc/text/adv_pubsub_publisher_exclusion.md}}

{{rfc/text/adv_pubsub_publisher_identification.md}}

{{rfc/text/adv_pubsub_publication_trustlevels.md}}

{{rfc/text/adv_pubsub_session_meta_api.md}}

{{rfc/text/adv_pubsub_subscription_meta_api.md}}

{{rfc/text/adv_pubsub_pattern_based_subscription.md}}

{{rfc/text/adv_pubsub_sharded_subscription.md}}

{{rfc/text/adv_pubsub_event_history.md}}

{{rfc/text/adv_pubsub_topic_reflection.md}}


# Binary conversion of JSON Strings

Binary data follows a convention for conversion to JSON strings.

A **byte array** is converted to a **JSON string** as follows:

1. convert the byte array to a Base64 encoded (host language) string
2. prepend the string with a `\0` character
3. serialize the string to a JSON string

*Example*

Consider the byte array (hex representation):

{align="left"}
        10e3ff9053075c526f5fc06d4fe37cdb

This will get converted to Base64

{align="left"}
        EOP/kFMHXFJvX8BtT+N82w==

prepended with `\0`

{align="left"}
        \x00EOP/kFMHXFJvX8BtT+N82w==

and serialized to a JSON string

{align="left"}
        "\\u0000EOP/kFMHXFJvX8BtT+N82w=="

A **JSON string** is unserialized to either a **string** or a **byte array** using the following procedure:

1. Unserialize a JSON string to a host language (Unicode) string
2. If the string starts with a `\0` character, interpret the rest (after the first character) as Base64 and decode to a byte array
3. Otherwise, return the Unicode string

Below are complete Python and JavaScript code examples for conversion between byte arrays and JSON strings.

## Python

Here is a complete example in Python showing how byte arrays are converted to and from JSON:

{align="left"}
        ```python
        <CODE BEGINS>

        import os, base64, json, sys, binascii
        PY3 = sys.version_info >= (3,)
        if PY3:
           unicode = str

        data_in = os.urandom(16)
        print("In:   {}".format(binascii.hexlify(data_in)))

        ## encoding
        encoded = json.dumps('\0' + base64.b64encode(data_in).
                                              decode('ascii'))

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

        <CODE ENDS>
        ```

## JavaScript

Here is a complete example in JavaScript showing how byte arrays are converted to and from JSON:

{align="left"}
        ```javascript
        <CODE BEGINS>

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

        // base64 encode raw string, prepend with \0
        // and serialize to JSON
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

        <CODE ENDS>
        ```


# Security Considerations

-- write me --

# IANA Considerations

TBD

# Contributors

# Acknowledgements

{backmatter}
