# Introduction

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


## Terminology {#terminology}

This chapter contains a list of technical terms used in this specification, along with their respective meanings.

Implementations SHOULD use terms as defined here in their public interfaces and documentation,
and SHOULD NOT reinvent or reinterpret terms. Users SHOULD be able to transfer their WAMP knowledge
from one implementation to another.
This is to support the overarching goal of WAMP to free application developers from restrictions when
building distributed applications, both at the network level, and when choosing (or switching) the WAMP
implementations used.

Our goal is to maximize **user choice and experience** when developing WAMP-based applications,
both formally (open protocol and open source) as well as practically (switching costs).


### Fundamental

{align="left"}
| Term                              | Definition                                                                                                 |
|-----------------------------------|------------------------------------------------------------------------------------------------------------|
| *User*                            | A person (or organization) running a WAMP *Client* or *Router*                                             |
| *Client*                          | A program run by a *User*, with application code using WAMP for application-level communications           |
| *Router*                          | A program run by a *User*, with middleware code using WAMP to provide application routing services         |
| *Peer*                            | A WAMP *Client* or *Router*. An implementation might embed, provide or use both roles                      |
| *Realm*                           | Isolated WAMP URI namespace serving as a routing and administrative domain, optionally protected by **AA** |
| *Transport*                       | A message-based, reliable, ordered, bidirectional (full-duplex) channel over which *Peers* communicate     |
| *Connection*                      | An underlying entity (if any) carrying the *Transport*, e.g. a network connection, pipe, queue or such     |
| *Session*                         | Transient conversation between a *Client* and a *Router*, within a *Realm* and over a *Transport*          |
| *Message*                         | Indivisible unit of information transmitted between peers                                                  |
| *Serializer*                      | Encodes WAMP messages, with application payloads, into byte strings for transport                          |


### Authentication and Authorization (AA)

{align="left"}
| Term                               | Definition                                                                                                |
|------------------------------------|-----------------------------------------------------------------------------------------------------------|
| *Authentication*                   | Establishes the identity of a *Session* within a *Realm*                                                  |
| *Principal*                        | A *Principal* (`authid`) is any *User* that can be authenticated under a *Realm* (`realm`) and runs in the security context of a *Role* (`authrole`) within that *Realm*. |
| *Credentials*                      | The authentication information and secrets used during                                                    |
| *Authorization*                    | A decision on permitting a *Principal* to perform a given *Action* on an *URI or URI pattern*             |
| *Access Control*                   | Policy for selective restriction of *Action*s on *URIs or URI patterns* performed by *Principal*s         |
| *Role-based Access Control (RBAC)* | An *Access Control* policy based on *Realm* (`realm`), *Principal*'s *Role* (`authrole`), *URI or URI pattern*, and *Action*   |
| *Discretionary Access Control*     | An *Access Control* policy controlled by *Users* and enforced by *Routers*                                |
| *Mandatory Access Control*         | An *Access Control* policy controlled by *Router Administrators* or *Realm Owners*, and enforced by *Routers* |
| *Capability-based Access Control*  | An *Access Control* policy where *Caller*s, *Callee*s, *Publisher*s, *Subscriber*s directly share capabilities with each other |
| *Subject*                          | The originating *Session* of an *Action* in the context of *Authorization*                                |
| *Object*                           | A (fully qualified) *URI or URI pattern* representing the target of an *Action* in the context of *Authorization* |
| *Action*                           | One of the four core WAMP operations: **register**, **call**, **subscribe**, and **publish**              |


### Remote Procedure Calls

{align="left"}
| Term             | Definition                                                                                                                    |
|------------------|-------------------------------------------------------------------------------------------------------------------------------|
| *Caller*         | A *Caller* is a *Session* that **calls**, with application payloads, a (fully qualified) *Procedure* for call routing         |
| *Callee*         | A *Callee* is a *Session* that responds to *Procedure* call invocations by **yielding** back application result payloads      |
| *Procedure*      | A *Procedure* is an URI or URI pattern that can be registered for call routing by *Callee*s                                   |
| *Registration*   | A *Router* record resulting from a *Callee* successfully **registering** a *Procedure* for call routing                       |
| *Call*           | A transient *Router* record resulting from a *Caller* successfully **calling** a *Procedure* for call routing                 |
| *Invocation*     | A call request and payload that are routed to a *Callee* having a matching *Registration* for the called *Procedure*          |


### Publish and Subscribe

{align="left"}
| Term             | Definition                                                                                                                    |
|------------------|-------------------------------------------------------------------------------------------------------------------------------|
| *Publisher*      | A *Publisher* is a *Session* that **publishes** application payloads to a (fully qualified) *Topic* for event routing         |
| *Subscriber*     | A *Subscriber* is a *Session* that **subscribes** to a *Topic* to receive application payloads on matching events             |
| *Topic*          | A *Topic* is an URI or URI pattern that can be subscribed to for event routing by *Subscriber*s                               |
| *Subscription*   | A *Router* record resulting from a *Subscriber* successfully **subscribing** to a *Topic* for event routing                   |
| *Publication*    | A transient *Router* record resulting from a *Publisher* successfully **publishing** to a *Topic* for event routing           |
| *Event*          | A publication that is routed to *Subscribers* having matching *Subscriptions* to the published *Topic*.                       |


## Protocol Overview

_This section is non-normative._


### Realms, Sessions and Transports

A Realm is a WAMP routing and administrative domain, optionally protected by authentication and authorization. WAMP messages are only routed within a Realm.

A Session is a transient conversation between two Peers attached to a Realm and running over a Transport.

A Transport connects two WAMP Peers and provides a channel over which WAMP messages for a WAMP Session can flow in both directions.

WAMP can run over any Transport which is message-based, bidirectional,  reliable and ordered.

The default transport for WAMP is WebSocket [@!RFC6455], where WAMP is an [officially registered](http://www.iana.org/assignments/websocket/websocket.xml) subprotocol.


### Peers and Roles

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

A _Router_ is a component which implements one or both of the Broker and Dealer roles. A _Client_ is a component which implements any or all of the Subscriber, Publisher, Caller, or Callee roles.

WAMP _Connections_ are established by Clients to a Router. Connections can use any _transport_ that is message-based, ordered, reliable and bi-directional, with WebSocket as the default transport.

WAMP _Sessions_ are established over a WAMP Connection. A WAMP Session is joined to a _Realm_ on a Router. Routing occurs only between WAMP Sessions that have joined the same Realm.

The _WAMP Basic Profile_ defines the parts of the protocol that are required to establish a WAMP connection, as well as for basic interactions between the four client and two router roles. WAMP implementations are required to implement the Basic Profile, at minimum.

The _WAMP Advanced Profile_ defines additions to the Basic Profile which greatly extend the utility of WAMP in real-world applications. WAMP implementations may support any subset of the Advanced Profile features. They are required to announce those supported features during session establishment.


### Publish & Subscribe

The Publish & Subscribe ("PubSub") messaging pattern involves peers of three different roles:

* Subscriber (Client)
* Publisher (Client)
* Broker (Router)

A Publisher publishes events to topics by providing the topic URI and any payload for the event. Subscribers of the topic will receive the event together with the event payload.

Subscribers subscribe to topics they are interested in with Brokers. Publishers initiate publication first at Brokers. Brokers route events incoming from Publishers to Subscribers that are subscribed to respective topics.

The Publisher and Subscriber will usually run application code, while the Broker works as a generic router for events decoupling Publishers from Subscribers.


### Remote Procedure Calls

The (routed) Remote Procedure Call ("RPC") messaging pattern involves peers of three different roles:

* Callee (Client)
* Caller (Client)
* Dealer (Router)

A Caller issues calls to remote procedures by providing the procedure URI and any arguments for the call.
The Callee will execute the procedure using the supplied arguments to the call and return the result of the call to the Caller.

Callees register procedures they provide with Dealers. Callers initiate procedure calls first to Dealers. Dealers route calls incoming from Callers to Callees implementing the procedure called, and route call results back from Callees to Callers.

The Caller and Callee will usually run application code, while the Dealer works as a generic router for remote procedure calls decoupling Callers and Callees.


## Design Aspects

_This section is non-normative._

WAMP was designed to be performant, safe and easy to implement. Its entire design was driven by a implement, get feedback, adjust cycle.

An initial version of the protocol was publicly released in March 2012. The intent was to gain insight through implementation and use, and integrate these into a second version of the protocol, where there would be no regard for compatibility between the two versions. Several interoperable, independent implementations were released, and feedback from the implementers and users was collected.

The second version of the protocol, which this RFC covers, integrates this feedback. Routed Remote Procedure Calls are one outcome of this, where the initial version of the protocol only allowed the calling of procedures provided by the router. Another, related outcome was the strict separation of routing and application logic.

While WAMP was originally developed to use WebSocket as a transport, with JSON for serialization, experience in the field revealed that other transports and serialization formats were better suited to some use cases. For instance, with the use of WAMP in the Internet of Things sphere, resource constraints play a much larger role than in the browser, so any reduction of resource usage in WAMP implementations counts. This lead to the decoupling of WAMP from any particular transport or serialization, with the establishment of minimum requirements for both.


### Application Code

WAMP is designed for application code to run within Clients, i.e. _Peers_ having the roles Callee, Caller, Publisher, and Subscriber.

Routers, i.e. Peers of the roles Brokers and Dealers are responsible for **generic call and event routing** and do not run application code.

This allows the transparent exchange of Broker and Dealer implementations without affecting the application and to distribute and deploy application components flexibly.

> Note that a **program** that implements, for instance, the Dealer role might at the same time implement, say, a built-in Callee. It is the Dealer and Broker that are generic, not the program.


### Language Agnostic

WAMP is language agnostic, i.e. can be implemented in any programming language. At the level of arguments that may be part of a WAMP message, WAMP takes a 'superset of all' approach. WAMP implementations may support features of the implementing language for use in arguments, e.g. keyword arguments.


### Symmetric Messaging

It is important to note that though the establishment of a Transport might have a inherent asymmetry (like a TCP client establishing a WebSocket connection to a server), and Clients establish WAMP sessions by attaching to Realms on Routers, WAMP itself is designed to be fully symmetric for application components.

After the transport and a session have been established, any application component may act as Caller, Callee, Publisher and Subscriber at the same time. And Routers provide the fabric on top of which WAMP runs a symmetric application messaging service.


### Peers with multiple Roles

Note that Peers might implement more than one role: e.g. a Peer might act as Caller, Publisher and Subscriber at the same time. Another Peer might act as both a Broker and a Dealer.


### Relationship to WebSocket

WAMP uses WebSocket as its default transport binding, and is a registered WebSocket subprotocol.


## Basic vs Advanced Profile

This document first describes a Basic Profile for WAMP in its entirety, before describing an Advanced Profile which extends the basic functionality of WAMP.

The separation into Basic and Advanced Profiles is intended to extend the reach of the protocol. It allows implementations to start out with a minimal, yet operable and useful set of features, and to expand that set from there. It also allows implementations that are tailored for resource-constrained environments, where larger feature sets would not be possible. Here implementers can weigh between resource constraints and functionality requirements, then implement an optimal feature set for the circumstances.

Advanced Profile features are announced during session establishment, so that different implementations can adjust their interactions to fit the commonly supported feature set.
