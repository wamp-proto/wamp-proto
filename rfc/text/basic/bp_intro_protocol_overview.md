## Protocol Overview

_This section is non-normative._


### Realms, Sessions and Transports

A Realm is a WAMP routing and administrative domain, optionally protected by authentication and authorization. WAMP messages are only routed within a Realm.

A Session is a transient conversation between two Peers attached to a Realm and running over a Transport.

A Transport connects two WAMP Peers and provides a channel over which WAMP messages for a WAMP Session can flow in both directions.

WAMP can run over any Transport which is message-based, bidirectional,  reliable and ordered.

The default transport for WAMP is WebSocket [@!RFC6455], where WAMP is an [officially registered](http://www.iana.org/assignments/websocket/websocket.xml) subprotocol.


### Publish & Subscribe and Remote Procedure Calls

The PubSub messaging pattern defines three roles: _Subscribers_ and _Publishers_, which communicate via a _Broker_.

The routed RPC messaging pattern also defines three roles: _Callers_ and _Callees_, which communicate via a _Dealer_.

A _Router_ is a component which implements one or both of the Broker and Dealer roles. A _Client_ is a component which implements any or all of the Subscriber, Publisher, Caller, or Callee roles.

WAMP _Connections_ are established by Clients to a Router. Connections can use any _transport_ that is message-based, ordered, reliable and bi-directional, with WebSocket as the default transport.

WAMP _Sessions_ are established over a WAMP Connection. A WAMP Session is joined to a _Realm_ on a Router. Routing occurs only between WAMP Sessions that have joined the same Realm.

The _WAMP Basic Profile_ defines the parts of the protocol that are required to establish a WAMP connection, as well as for basic interactions between the four client and two router roles. WAMP implementations are required to implement the Basic Profile, at minimum.

The _WAMP Advanced Profile_ defines additions to the Basic Profile which greatly extend the utility of WAMP in real-world applications. WAMP implementations may support any subset of the Advanced Profile features. They are required to announce those supported features during session establishment.
