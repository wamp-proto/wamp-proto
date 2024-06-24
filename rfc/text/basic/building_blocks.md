# Building Blocks

WAMP is defined with respect to the following building blocks

1.  Identifiers
2.  Serializers
3.  Transports

For each building block, WAMP only assumes a defined set of requirements, which allows to run WAMP variants with different concrete bindings.

## Identifiers

### URIs {#uris}

WAMP needs to identify the following persistent resources:

1.  Topics
2.  Procedures
3.  Errors

These are identified in WAMP using Uniform Resource Identifiers (URIs) [@!RFC3986] that MUST be Unicode strings.

When using JSON as WAMP serialization format, URIs (as other strings) are transmitted in UTF-8 [@!RFC3629] encoding.

*Examples*

* `com.myapp.mytopic1`
* `com.myapp.myprocedure1`
* `com.myapp.myerror1`

The URIs are understood to form a single, global, hierarchical namespace for WAMP. The namespace is unified for topics, procedures and errors, that is these different resource types do NOT have separate namespaces.

To avoid resource naming conflicts, the package naming convention from Java is used, where URIs SHOULD begin with (reversed) domain names owned by the organization defining the URI.

**Relaxed/Loose URIs**

URI components (the parts between two `.`s, the head part up to the first `.`, the tail part after the last `.`) MUST NOT contain a `.`, `#` or whitespace characters and MUST NOT be empty (zero-length strings).

The restriction not to allow `.` in component strings is due to the fact that `.` is used to separate components, and WAMP associates semantics with resource hierarchies, such as in pattern-based subscriptions that are part of the Advanced Profile. The restriction not to allow empty (zero-length) strings as components is due to the fact that this may be used to denote wildcard components with pattern-based subscriptions and registrations in the Advanced Profile. The character `#` is not allowed since this is reserved for internal use by Dealers and Brokers.

As an example, the following regular expression could be used in Python to check URIs according to the above rules, when **NO empty URI components are allowed**:

{align="left"}
``` python
pattern = re.compile(r"^([^\s\.#]+\.)*([^\s\.#]+)$")
```

When **empty URI components are allowed** (which is the case for specific messages that are part of the Advanced Profile), this following regular expression can be used (shown used in Python):

{align="left"}
``` python
pattern = re.compile(r"^(([^\s\.#]+\.)|\.)*([^\s\.#]+)?$")
```

**Strict URIs**

While the above rules MUST be followed, following a stricter URI rule is recommended: URI components SHOULD only contain lower-case letters, digits and `_`.

As an example, the following regular expression could be used in Python to check URIs according to the above rules, when **NO empty URI components are allowed**:

{align="left"}
```python
pattern = re.compile(r"^([0-9a-z_]+\.)*([0-9a-z_]+)$")
```

When **empty URI components are allowed**, which is the case for specific messages that are part of the Advanced Profile, the following regular expression can be used (shown in Python):

{align="left"}
```python
pattern = re.compile(r"^(([0-9a-z_]+\.)|\.)*([0-9a-z_]+)?$")
```

Following the suggested regular expression for **strict URIs** will make URI components valid identifiers in most languages (modulo URIs starting with a digit and language keywords) and the use of lower-case only will make those identifiers unique in languages that have case-insensitive identifiers. Following this suggestion can allow implementations to map topics, procedures and errors to the language environment in a completely transparent way.


**Reserved URIs**

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

These are identified in WAMP using IDs that are integers between (inclusive) **1** and **2^53** (9007199254740992):

* IDs in the *global scope* MUST be drawn *randomly* from a *uniform distribution* over the complete range [1, 2^53]
* IDs in the *router scope* CAN be chosen freely by the specific router implementation
* IDs in the *session scope* MUST be incremented by 1 beginning with 1 and wrapping to 1 after it reached 2^53 (for each direction - *Client-to-Router* and *Router-to-Client*) {#session_scope_id}

> The reason to choose the specific lower bound as 1 rather than 0 is that 0 is the null-like (falsy) value for many programming languages.
> The reason to choose the specific upper bound is that 2^53 is the largest integer such that this integer and *all* (positive) smaller integers can be represented exactly in IEEE-754 doubles. Some languages (e.g. JavaScript) use doubles as their sole number type. Most languages do have signed and unsigned 64-bit integer types that both can hold any value from the specified range.
>

The following is a complete list of usage of IDs in the three categories for all WAMP messages. For a full definition of these see [messages section](#messages).

**Global Scope IDs**

* `WELCOME.Session`
* `PUBLISHED.Publication`
* `EVENT.Publication`


**Router Scope IDs**

* `EVENT.Subscription`
* `SUBSCRIBED.Subscription`
* `REGISTERED.Registration`
* `UNSUBSCRIBE.Subscription`
* `UNREGISTER.Registration`
* `INVOCATION.Registration`


**Session Scope IDs** {#session_scope_ids}

* `SUBSCRIBE.Request`
* `SUBSCRIBED.Request` (mirrored `SUBSCRIBE.Request`)
* `UNSUBSCRIBE.Request`
* `UNSUBSCRIBED.Request` (mirrored `UNSUBSCRIBE.Request`)
* `PUBLISH.Request`
* `PUBLISHED.Request` (mirrored `PUBLISH.Request`)
* `REGISTER.Request`
* `REGISTERED.Request` (mirrored `REGISTER.Request`)
* `UNREGISTER.Request`
* `UNREGISTERED.Request` (mirrored `UNREGISTER.Request`)
* `CALL.Request`
* `RESULT.Request` (mirrored `CALL.Request`)
* `CANCEL.Request` (mirrored `CALL.Request`)
* `INVOCATION.Request`
* `YIELD.Request` (mirrored `INVOCATION.Request`)
* `INTERRUPT.Request` (mirrored `INVOCATION.Request`)
* `ERROR.Request` (mirrored original request ID)


## Serializers

WAMP is a message based protocol that requires serialization of messages to octet sequences to be sent out on the wire.

A message serialization format is assumed that (at least) provides the following types:

* `integer` (non-negative)
* `string` (UTF-8 encoded Unicode)
* `bool`
* `list`
* `dict` (with string keys)

> WAMP *itself* only uses the above types, e.g. it does not use the JSON data types `number` (non-integer) and `null`. The *application payloads* transmitted by WAMP (e.g. in call arguments or event payloads) may use other types a concrete serialization format supports.
>

There is no required serialization or set of serializations for WAMP implementations (but each implementation MUST, of course, implement at least one serialization format). Routers SHOULD implement more than one serialization format, enabling components using different kinds of serializations to connect to each other.

The WAMP Basic Profile defines the following bindings for message serialization:

1. JSON
2. MessagePack
3. CBOR

Other bindings for serialization may be defined in the WAMP Advanced Profile.

With JSON serialization, each WAMP message is serialized according to the JSON specification as described in [@!RFC7159].

Further, binary data follows a convention for conversion to JSON strings. For details see the Appendix.

With [MessagePack](https://msgpack.org/) serialization, each WAMP message is serialized according to the [MessagePack specification](https://github.com/msgpack/msgpack/blob/master/spec.md).

Version 5 or later of MessagePack MUST BE used, since this version is able to differentiate between strings and binary values.

With CBOR serialization, each WAMP message is serialized according to the CBOR specification as described in [@!RFC8949].


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

WAMP uses the following WebSocket subprotocol identifiers (for unbatched modes):

* `wamp.2.json`
* `wamp.2.msgpack`
* `wamp.2.cbor`

With `wamp.2.json`, *all* WebSocket messages MUST BE of type **text** (UTF8 encoded payload) and use the JSON message serialization.

With `wamp.2.msgpack`, *all* WebSocket messages MUST BE of type **binary** and use the MessagePack message serialization.

With `wamp.2.cbor`, *all* WebSocket messages MUST BE of type **binary** and use the CBOR message serialization.

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


### Protocol Errors {#protocol_errors}

WAMP implementations MUST abort sessions (disposing all of their resources such as subscriptions and registrations) on protocol errors caused by offending peers.

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
 - Receiving `YIELD` message with invalid INVOCATION.Request.
 - Receiving message with non-[sequential](#session_scope_id) [session scope](#session_scope_ids) request ID, such as `SUBSCRIBE`, `UNSUBSCRIBE`, `PUBLISH`, `REGISTER`, `UNREGISTER`, and `CALL`. Note that there are exeptions for `CALL` when the _Progressive Call Invocations_ advanced feature is enabled. See the _Progressive Call Invocations_ section in the advanced profile for details.
 - Receiving protocol incompatible message, such as empty array, invalid WAMP message type id, etc.
 - Catching error during message encoding/decoding.
 - Any other exceptional scenario explicitly defined in any relevant section of this specification below (such as receiving a second `HELLO` within the lifetime of a session).

In all such cases WAMP implementations:

1. MUST send an `ABORT` message to the offending peer, having reason `wamp.error.protocol_violation` and optional attributes in ABORT.Details such as a human readable error message.
2. MUST abort the WAMP session by disposing any allocated subscriptions/registrations for that particular client and without waiting for or processing any messages subsequently received from the peer,
3. SHOULD also drop the WAMP connection at transport level (recommended to prevent denial of service attacks)
