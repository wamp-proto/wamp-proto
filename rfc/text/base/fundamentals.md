## Fundamentals

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
