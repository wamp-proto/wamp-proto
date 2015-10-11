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