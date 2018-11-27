## Transports

WAMP assumes a transport with the following characteristics:

1. message-based
2. reliable
3. ordered
4. bidirectional (full-duplex)

There is no required transport or set of transports for WAMP implementations (but each implementation MUST, of course, implement at least one transport). Routers SHOULD implement more than one transport, enabling components using different kinds of transports to connect in an application.


### WebSocket Transport

The default transport binding for WAMP is WebSocket ([@!RFC6455]).

In the Basic Profile, WAMP messages are transmitted as WebSocket messages: each WAMP message is transmitted as a separate WebSocket message (not WebSocket frame). The Advanced Profile may define other modes, e.g. a **batched mode** where multiple WAMP messages are transmitted via single WebSocket message.

The WAMP protocol MUST BE negotiated during the WebSocket opening handshake between Peers using the WebSocket subprotocol negotiation mechanism ([@!RFC6455] section 4).

WAMP uses the following WebSocket subprotocol identifiers for unbatched modes:

* `wamp.2.json`
* `wamp.2.msgpack`

With `wamp.2.json`, *all* WebSocket messages MUST BE of type **text** (UTF8 encoded payload) and use the JSON message serialization.

With `wamp.2.msgpack`, *all* WebSocket messages MUST BE of type **binary** and use the MessagePack message serialization.

> To avoid incompatibilities merely due to naming conflicts with WebSocket subprotocol identifiers, implementers SHOULD register identifiers for additional serialization formats with the official WebSocket subprotocol registry.


### Transport and Session Lifetime

WAMP implementations MAY choose to tie the lifetime of the underlying transport connection for a WAMP connection to that of a WAMP session, i.e. establish a new transport-layer connection as part of each new session establishment. They MAY equally choose to allow re-use of a transport connection, allowing subsequent WAMP sessions to be established using the same transport connection.

The diagram below illustrates the full transport connection and session lifecycle for an implementation which uses WebSocket over TCP as the transport and allows the re-use of a transport connection.

{align="left"}
        ,------.                                    ,------.
        | Peer |                                    | Peer |
        `--+---'          TCP established           `--+---'
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


### Protocol errors {#protocol_errors}

WAMP implementations MUST close sessions (disposing all of their resources such as subscriptions and registrations) on protocol errors caused by offending peers.

Following scenarios have to be considered protocol errors:

 - Receiving `WELCOME` message, after session was established.
 - Receiving `HELLO` message, after session was established.
 - Receiving `CHALLENGE` message, after session was established.
 - Receiving `GOODBYE` message, before session was established.
 - Receiving `ERROR` message, before session was established.
 - Receiving `ERROR` message with invalid REQUEST.Type.
 - Receiving `SUBSCRIBED` message, before session was established.
 - Receiving `UNSUBSCRIBED` message, before session was established.
 - Receiving `PUBLISHED` message, before session was established.
 - Receiving `RESULT` message, before session was established.
 - Receiving `REGISTERED` message, before session was established.
 - Receiving `UNREGISTERED` message, before session was established.
 - Receiving `INVOCATION` message, before session was established.
 - Receiving protocol incompatible message, such as empty array, invalid WAMP message type id, etc.
 - Catching error during message encoding/decoding.
 - Any other exceptional scenario explicitly defined in any relevant section of this specification below (such as receiving a second `HELLO` within the lifetime of a session).

In all such cases WAMP implementations:

1. MUST send an `ABORT` message to the offending peer, having reason `wamp.error.protocol_violation` and optional attributes in ABORT.Details such as a human readable error message.
2. MUST close the WAMP session by disposing any allocated subscriptions/registrations for that particular client and without waiting for or processing any messages subsequently received from the peer,
3. SHOULD also drop the WAMP connection at transport level (recommended to prevent denial of service attacks)
