# The Web Application Messaging Protocol

This document specifies the *Advanced Profile* of the [Web Application Messaging Protocol (WAMP)](http://wamp.ws/).

Document Revision: **alpha-2**, 2014/02/26

> For the *Basic Profile*, please see [The Web Application Messaging Protocol, Part 1: Basic Profile](basic.md). For the (deprecated) WAMP version 1 specification, please see [here](http://wamp.ws/spec/wamp1/).
> 

Copyright (c) 2014 [Tavendo GmbH](http://www.tavendo.com). Licensed under the [Creative Commons CC-BY-SA license](http://creativecommons.org/licenses/by-sa/3.0/). "WAMP", "Crossbar.io" and "Tavendo" are trademarks of Tavendo GmbH.

# Part 2: Advanced Profile

**Contents**

1. [Transports](#transports)
   * [RawSocket Transport](#rawsocket-transport)
   * [Batched WebSocket Transport](#batched-websocket-transport)
   * [LongPoll Transport](#longpoll-transport)
   * [Multiplexed Transport](#multiplexed-transport)
2. [Messages](#messages)
    * [Message Definitions](#message-definitions)
    * [Message Codes and Direction](#message-codes-and-direction)
3. [Session Management](#session-management)
    * [Heartbeats](#heartbeats)
4. [Publish & Subscribe](#publish--subscribe)
    * [Subscriber Black- and Whitelisting](#subscriber-black--and-whitelisting) [stable]
    * [Publisher Exclusion](#publisher-exclusion) [stable]
    * [Publisher Identification](#publisher-identification) [stable]
    * [Publication Trust Levels](#publication-trust-levels)
    * [Pattern-based Subscriptions](#pattern-based-subscriptions)
    * [Distributed Subscriptions & Publications](#distributed-subscriptions--publications)
    * [Subscriber Meta Events](#subscriber-meta-events)
    * [Subscriber List](#subscriber-list)
    * [Event History](#event-history)
5. [Remote Procedure Calls](#remote-procedure-calls)
    * [Caller Identification](#caller-identification) [stable]
    * [Progressive Call Results](#progressive-call-results) [stable]
    * [Canceling Calls](#canceling-calls) [stable]
    * [Call Timeouts](#call-timeouts)
    * [Call Trust Levels](#call-trust-levels)
    * [Pattern-based Registrations](#pattern-based-registrations)
    * [Distributed Registrations & Calls](#distributed-registrations--calls)
    * [Callee Black- and Whitelisting](#callee-black--and-whitelisting)
    * [Caller Exclusion](#caller-exclusion)
6. [Authentication](#authentication)
    * [TLS Certificate-based Authentication](#tls-certificate-based-authentication)
    * [HTTP Cookie-based Authentication](#http-cookie-based-authentication)
    * [WAMP Challenge-Response Authentication](#wamp-challenge-response-authentication)
    * [Ticket-based Authentication](#ticket-based-authentication)
    * [One Time Token Authentication](#one-time-token-authentication)
7. [Reflection](#reflection)
8. [Appendix](#appendix)
    * [Predefined URIs](#predefined-uris) 
    * [Authentication examples](#authentication-examples)

## Preface

This is *part 2* of the WAMP specification. It describes advanced features and aspects of the protocol and its usage from the **WAMP Advanced Profile**.

This part as a whole is considered partially finished and unstable. Some features are presently underspecified. Features may yet be added or removed, and there is no guarantee that an existing feature in this part will remain unchanged.

Some features, however, are already specified and should remain unchanged. These are specifically marked as *STABLE*.

For an introduction to the protocol, and a description of basic features and usage that are part of the **WAMP Basic Profile**, please see [The Web Application Messaging Protocol, Part 1: Basic Profile](basic.md)


## Transports

Besides the WebSocket transport, the following WAMP transports are currently specified:

* [RawSocket Transport](#rawsocket-transport)
* [Batched WebSocket Transport](#batched-websocket-transport)
* [LongPoll Transport](#longpoll-transport)
* [Multiplexed Transport](#multiplexed-transport)

Other transports such as HTTP 2.0 ("SPDY") or UDP might be defined in the future. As mentioned in the [Basic Profile](basic.md), the only requirements that WAMP expects from a transport are:

 * message based
 * bidirectional
 * reliable
 * ordered


### RawSocket Transport

**WAMP-over-RawSocket** is an (alternative) transport for WAMP that uses length-prefixed, binary messages - a message framing different from WebSocket.

Compared to WAMP-over-WebSocket, WAMP-over-RawSocket is simple to implement, since there is no need to implement the WebSocket protocol which has some features that make it non-trivial (like a full HTTP-based opening handshake, message fragmentation, masking and variable length integers).

WAMP-over-RawSocket has even lower overhead than WebSocket, which can be desirable in particular when running on local connections like loopback TCP or Unix domain sockets. It is also expected to allow implementations in microcontrollers in under 2KB RAM.

WAMP-over-RawSocket can run over TCP, TLS, Unix domain sockets or any reliable streaming underlying transport. When run over TLS on a (misused) standard Web port (443), it is also able to traverse most locked down networking environments such as enterprise or mobile networks (unless man-in-the-middle TLS intercepting proxies are in use).

However, WAMP-over-RawSocket cannot be used with Web browser clients, since browsers don't allow raw TCP connections. Browser extensions would do, but those need to be installed in a browser. WAMP-over-RawSocket also (currently) does not support transport-level compression as WebSocket does provide (`permessage-deflate` WebSocket extension).


#### Endianess

WAMP-over-RawSocket uses *network byte order* ("big-endian"). That means, given a unsigned 32 bit integer

   0x 11 22 33 44

the first octet sent out to (or received from) the wire is `0x11` and the last octet sent out (or received) is `0x44`.

Here is how you would convert octets received from the wire into an integer in Python:

```python
import struct

octets_received = b"\x11\x22\x33\x44"
i = struct.unpack(">L", octets_received)[0]
``` 

The integer received has the value `287454020`.

And here is how you would send out an integer to the wire in Python:

```python
octets_to_be_send = struct.pack(">L", i)
```

The octets to be sent are `b"\x11\x22\x33\x44"`.


#### Handshake

**Client-to-Router Request**

WAMP-over-RawSocket starts with a handshake where the client connecting to a router sends 4 octets:

    MSB                                 LSB
    31                                    0
    0111 1111 LLLL SSSS RRRR RRRR RRRR RRRR

The *first octet* is a magic octet with value `0x7F`. This value is chosen to avoid any possible collision with the first octet of a valid HTTP request (see [here](http://www.w3.org/Protocols/rfc2616/rfc2616-sec5.html#sec5.1) and [here](http://www.w3.org/Protocols/rfc2616/rfc2616-sec2.html#sec2.2)). No valid HTTP request can have `0x7F` as its first octet.

> By using a magic first octet that cannot appear in a regular HTTP request, WAMP-over-RawSocket can be run e.g. on the same TCP listening port as WAMP-over-WebSocket or WAMP-over-LongPoll.

The *second octet* `0xLS` consists of a 4 bit `LENGTH` field and a 4 bit `SERIALIZER` field.

The `SERIALIZER` value is used by the *Client* to request a specific serializer to be used. When the handshake completes successfully, the *Client* and *Router* will use the serializer requested by the *Client*.

The possible values for `SERIALIZER` are:

    0: illegal
    1: JSON
    2: MsgPack
    3 - 15: reserved for future serializers

The `LENGTH` value is used by the *Client* to signal the **maximum message length** of messages it is willing to **receive**. When the handshake completes successfully, a *Router* MUST NOT send messages larger than this size.

The possible values for `LENGTH` are:

     0: 2**9 octets
     1: 2**10 octets
    ...
    15: 2**24 octets

This means a *Client* can choose the maximum message length between **512** and **16M** octets.

Here is a Python program that prints all (currently) permissible values for the *second octet*:

```python
SERMAP = {
   1: 'json',
   2: 'msgpack'
}

## map serializer / max. msg length to RawSocket handshake request or success reply (2nd octet)
##
for ser in SERMAP:
   for l in range(16):
      octet_2 = (l << 4) | ser
      print("serializer: {}, maxlen: {} => 0x{:02x}".format(SERMAP[ser], 2 ** (l + 9), octet_2))
```

The *third and forth octet* are **reserved** and MUST be all zeros for now.


**Router-to-Client Reply**

After a *Client* has connected to a *Router*, the *Router* will first receive the 4 octets handshake request from the *Client*.

If the *first octet* differs from `0x7F`, it is not a WAMP-over-RawSocket request. Unless the *Router* also supports other transports on the connecting port (such as WebSocket or LongPoll), the *Router* MUST **fail the connection**.

Here is an example of how a *Router* could parse the *second octet* in a *Clients* handshake request:

```python
## map RawSocket handshake request (2nd octet) to serializer / max. msg length
##
for i in range(256):
   ser_id = i & 0x0f
   if ser_id != 0:
      ser = SERMAP.get(ser_id, 'currently undefined')
      maxlen = 2 ** ((i >> 4) + 9)
      print("{:02x} => serializer: {}, maxlen: {}".format(i, ser, maxlen))
   else:
      print("fail the connection: illegal serializer value")
```

When the *Router* is willing to speak the serializer requested by the *Client*, it will answer with a 4 octets response of identical structure as the *Client* request:

    MSB                                 LSB
    31                                    0
    0111 1111 LLLL SSSS RRRR RRRR RRRR RRRR

Again, the *first octet* MUST be the value `0x7F`. The *third and forth octets* are reserved and MUST be all zeros for now.

In the *second octet*, the *Router* MUST echo the serializer value in `SERIALIZER` as requested by the *Client*.

Similar to the *Client*, the *Router* sets the `LENGTH` field to request a limit on the length of messages sent by the *Client*.

During the connection, *Router* MUST NOT send messages to the *Client* longer than the `LENGTH` requested by the *Client*, and the *Client* MUST NOT send messages larger than the maximum requested by the *Router* in it's handshake reply.

If a message received during a connection exceeds the limit requested, a *Peer* MUST **fail the connection**.

When the *Router* is unable to speak the serializer requested by the *Client*, or it is denying the *Client* for other reasons, the *Router* replies with an error:

    MSB                       LSB
    31                          0
    0111 1111 EEEE 0000 RRRR RRRR

An error reply has 4 octets: the *first octet* is again the magic `0x7F`, and the *third and forth octet* are reserved and MUST BE all zeros for now.

The *second octet* has its lower 4 bits zero'ed (which distinguishes the reply from an success/accepting reply) and the upper 4 bits encode the error:

    0: serializer unsupported
    1: maximum message length unacceptable
    2: use of reserved bits (unsupported feature)
    3: maximum connection count reached
    4 - 15: reserved for future errors

Here is an example of how a *Router* might create the *second octet* in an error response:

```python
ERRMAP = {
   0: "serializer unsupported",
   1: "maximum message length unacceptable",
   2: "use of reserved bits (unsupported feature)",
   3: "maximum connection count reached"
}

## map error to RawSocket handshake error reply (2nd octet)
##
for err in ERRMAP:
   octet_2 = err << 4
   print("error: {} => 0x{:02x}").format(ERRMAP[err], err)
```

The *Client* - after having sent its handshake request - will wait for the 4 octets from *Router* handshake reply.

Here is an example of how a *Client* might parse the *second octet* in a *Router* handshake reply:


```python
## map RawSocket handshake reply (2nd octet)
##
for i in range(256):
   ser_id = i & 0x0f
   if ser_id:
      ## verify the serializer is the one we requested! if not, fail the connection!
      ser = SERMAP.get(ser_id, 'currently undefined')
      maxlen = 2 ** ((i >> 4) + 9)
      print("{:02x} => serializer: {}, maxlen: {}".format(i, ser, maxlen))
   else:
      err = i >> 4
      print("error: {}".format(ERRMAP.get(err, 'currently undefined')))
```
 

#### Serialization

To send a WAMP message, the message is serialized according to the WAMP serializer agreed in the handshake (e.g. JSON or MsgPack).

The length of the serialized messages in octets MUST NOT exceed the maximum requested by the *Peer*.

If the serialized length exceed the maximum requested, the WAMP message can not be sent to the *Peer*. Handling situations like the latter is left to the implementation.

E.g. a *Router* that is to forward a WAMP `EVENT` to a *Client* which exceeds the maximum length requested by the *Client* when serialized might:

* drop the event (not forwarding to that specific client) and track dropped events
* prohibit publishing to the topic already
* remove the event payload, and send an event with extra information (`payload_limit_exceeded = true`)


#### Framing

The serialized octets for a message to be sent are prefixed with exactly 4 octets:

    0x FF LL LL LL

The *first octet* `0xFF` has the following structure

    MSB   LSB
    7       0
    RRRR RTTT

The five bits `RRRRR` are reserved for future use and MUST be all zeros for now.

The three bits `TTT` encode the type of the transport message:

    0: regular WAMP message
    1: PING
    2: PONG
    3-7: reserved

The *three octets* `0x LL LL LL` constitute an unsigned 24 bit integer that provides the length of transport message payload following, excluding the 4 octets that constitute the prefix.

For a regular WAMP message (`TTT == 0`), the length is the length of the serialized WAMP message: the number of octets after serialization (excluding the 4 octets of the prefix).

For a `PING` message (`TTT == 1`), the length is the length of the arbitrary payload that follows. A *Peer* MUST reply to each `PING` by sending exactly one `PONG` immediately, and the `PONG` MUST echo back the payload of the `PING` exactly.   

For receiving messages with WAMP-over-RawSocket, a *Peer* will usually read exactly 4 octets from the incoming stream, decode the transport level message type and payload length, and then receive as many octets as the length was giving.

When the transport level message type indicates a regular WAMP message, the transport level message payload is unserialized according to the serializer agreed in the handshake.


### Batched WebSocket Transport

*WAMP-over-Batched-WebSocket* is a variant of *WAMP-over-WebSocket* where multiple WAMP messages are sent in one WebSocket message.

Using WAMP message batching can increase wire level efficiency further. In particular when using TLS and the WebSocket implementation is forcing every WebSocket message into a new TLS segment.

*WAMP-over-Batched-WebSocket* is negotiated between *Peers* in the WebSocket opening handshake by agreeing on one of the following WebSocket subprotocols:

 * `wamp.2.json.batched`
 * `wamp.2.msgpack.batched`

Batching with JSON works by serializing each WAMP message to JSON as normally, appending the single ASCII control character `\30` ([record separator](http://en.wikipedia.org/wiki/Record_separator#Field_separators)) octet `0x1e` to *each* serialized messages, and packing a sequence of such serialized messages into a single WebSocket message:

   	Serialized JSON WAMP Msg 1 | 0x1e | Serialized JSON WAMP Msg 2 | 0x1e | ...

Batching with MsgPack works by serializing each WAMP message to MsgPack as normally, prepending a 32 bit unsigned integer (4 octets in big-endian byte order) with the length of the serialized MsgPack message (excluding the 4 octets for the length prefix), and packing a sequence of such serialized (length-prefixed) messages into a single WebSocket message:

   	Length of Msg 1 serialization (uint32) | serialized MsgPack WAMP Msg 1 | ...

With batched transport, even if only a single WAMP message is to be sent in a WebSocket message, the (single) WAMP message needs to be framed as described above. In other words, a single WAMP message is sent as a batch of length **1**. Sending a batch of length **0** (no WAMP message) is illegal and a *Peer* MUST fail the transport upon receiving such a transport message.


### Long-Poll Transport

The *Long-Poll Transport* is able to transmit a WAMP session over plain old HTTP 1.0/1.1. This is realized by the *Client* issuing HTTP/POSTs requests, one for sending, and one for receiving. Those latter requests are kept open at the server when there are no messages currently pending to be received.

**Opening a Session**

With the *Long-Poll Transport*, a *Client* opens a new WAMP session by sending a HTTP/POST request to a well-known URL, e.g.

	http://mypp.com/longpoll/open

Here, `http://mypp.com/longpoll` is the base URL for the *Long-Poll Transport* and `/open` is a path dedicated for opening new sessions.

The HTTP/POST request *SHOULD* have a `Content-Type` header set to `application/json` and *MUST* have a request body with a JSON document that is a dictionary:

```javascript
{
   "protocols": ["wamp.2.json.batched"]
}
``` 

The (mandatory) `protocols` attribute specifies the protocols the client is willing to speak. The server will chose one from this list when establishing the session or fail the request when no protocol overlap was found.

The valid protocols are:

 * `wamp.2.json.batched`
 * `wamp.2.json`
 * `wamp.2.msgpack.batched`
 * `wamp.2.msgpack`

> The request path with this and subsequently described HTTP/POST requests *MAY* contain a query parameter `x` with some random or sequentially incremented value: 
> 
> 	http://mypp.com/longpoll/open?x=382913
> 
> The value is ignored, but may help in certain situations to prevent intermediaries from caching the request.
> 

Returned is a JSON document containing a transport ID and the protocol to speak:

```javascript
{
   "protocol": "wamp.2.json.batched",
   "transport": "kjmd3sBLOUnb3Fyr"
}
```

As an implied side-effect, two HTTP endpoints are created

	http://mypp.com/longpoll/<transport_id>/receive
	http://mypp.com/longpoll/<transport_id>/send

where `transport_id` is the transport ID returned from `open`, e.g.

	http://mypp.com/longpoll/kjmd3sBLOUnb3Fyr/receive
	http://mypp.com/longpoll/kjmd3sBLOUnb3Fyr/send


**Receiving WAMP Messages**

The *Client* will then issue HTTP/POST requests (with empty request body) to

	http://mypp.com/longpoll/kjmd3sBLOUnb3Fyr/receive

When there are WAMP messages pending downstream, a request will return with a single WAMP message (unbatched modes) or a batch of serialized WAMP messages (batched mode).

The serialization format used is the one agreed during opening the session.

The batching uses the same scheme as with `wamp.2.json.batched` and `wamp.2.msgpack.batched` transport over WebSocket (see below).

> Note: In unbatched mode, when there is more than one message pending, there will be at most one message returned for each request. The other pending messages must be retrieved by new requests. With batched mode, all messages pending at request time will be returned in one batch of messages.
> 

**Sending WAMP Messages**

For sending WAMP messages, the *Client* will issue HTTP/POST requests to

	http://mypp.com/longpoll/kjmd3sBLOUnb3Fyr/send

with request body being a single WAMP message (unbatched modes) or a batch of serialized WAMP messages (batched mode).

The serialization format used is the one agreed during opening the session.

The batching uses the same scheme as with `wamp.2.json.batched` and `wamp.2.msgpack.batched` transport over WebSocket (see below).

Upon success, the request will return with HTTP status code 202 ("no content"). Upon error, the request will return with HTTP status code 400 ("bad request").


**Closing a Session**

To orderly close a session, a *Client* will issue a HTTP/POST to 

	http://mypp.com/longpoll/kjmd3sBLOUnb3Fyr/close

with an empty request body. Upon success, the request will return with HTTP status code 202 ("no content"). 


### Multiplexed Transport

A *Transport* may support the multiplexing of multiple logical channels over a single "physical" connection.

By using such a *Transport*, multiple WAMP sessions can be transported over a single underlying connection at the same time.

![alt text](figure/sessions3.png "Transports, Sessions and Peers")

As an example, the proposed [WebSocket extension "permessage-priority"](https://github.com/oberstet/permessage-priority/blob/master/draft-oberstein-hybi-permessage-priority.txt) would allow creating multiple logical *Transports* for WAMP over a single underlying WebSocket connection.


## Messages

WAMP Advanced Profile defines the following additional messages which are explained in detail in the following sections.

### Message Definitions

The following 5 message types are used in the WAMP Advanced Profile.

#### `CHALLENGE`

During authenticated session establishment, a *Router* sends a challenge message.

    [CHALLENGE, AuthMethod|string, Extra|dict]

#### `AUTHENTICATE`

A *Client* having received a challenge is expected to respond by sending a signature or token.

    [AUTHENTICATE, Signature|string, Extra|dict]

#### `HEARTBEAT`

Each *Peer* can send heartbeats signaling WAMP message processing advance.

    [HEARTBEAT, IncomingSeq|integer, OutgoingSeq|integer
    [HEARTBEAT, IncomingSeq|integer, OutgoingSeq|integer, Discard|string]

#### `CANCEL`

A *Caller* can cancel and issued call actively by sending a cancel message to the *Dealer*.

    [CANCEL, CALL.Request|id, Options|dict]

#### `INTERRUPT`

Upon receiving a cancel for a pending call, a *Dealer* will issue an interrupt to the *Callee*.

    [INTERRUPT, INVOCATION.Request|id, Options|dict]


### Message Codes and Direction

The following table list the message type code for **the OPTIONAL messages** defined in this part of the document and their direction between peer roles.

> "Tx" means the message is sent by the respective role, and "Rx" means the message is received by the respective role.
> 

| Code | Message        |  Profile |  Publisher  |  Broker  |  Subscriber  |  Caller  |  Dealer  |  Callee  |
|------|----------------|----------|-------------|----------|--------------|----------|----------|----------|
|  4   | `CHALLENGE`    | advanced | Rx          | Tx       | Rx           | Rx       | Tx       | Rx       |
|  5   | `AUTHENTICATE` | advanced | Tx          | Rx       | Tx           | Tx       | Rx       | Tx       |
|  7   | `HEARTBEAT`    | advanced | Tx/Rx       | Tx/Rx    | Tx/Rx        | Tx/Rx    | Tx/Rx    | Tx/Rx    |
| 49   | `CANCEL`       | advanced |             |          |              | Tx       | Rx       |          |
| 69   | `INTERRUPT`    | advanced |             |          |              |          | Tx       | Rx       |


## Session Management

### Session Establishment

The message flow between *Clients* and *Routers* for establishing and tearing down sessions MAY involve the following messages which authenticate a session:

1. `CHALLENGE`
2. `AUTHENTICATE`

![alt text](figure/hello_authenticated.png "WAMP Session denied")


#### CHALLENGE

An authentication MAY be required for the establishment of a session. Such requirement may be based on the `Realm` the connection is requested for.

To request authentication, the *Router* sends a `CHALLENGE` message to the *Endpoint*.

    [CHALLENGE, AuthMethod|string, Extra|dict]


#### AUTHENTICATE

In response to a `CHALLENGE` message, an *Endpoint* MUST send an `AUTHENTICATION` message.

    [AUTHENTICATE, Signature|string, Extra|dict]


## Advanced Session Management

### HEARTBEAT

The heartbeat allows to keep network intermediaries from closing the underlying transport, notify the peer up to which incoming heartbeat all incoming WAMP messages have been processed, and announce an outgoing heartbeat sequence number in the same message.

A peer MAY send a `HEARTBEAT` message at any time:

    [HEARTBEAT, IncomingSeq|integer, OutgoingSeq|integer]

or

    [HEARTBEAT, IncomingSeq|integer, OutgoingSeq|integer, Discard|string]

 * `HEARTBEAT.OutgoingSeq` MUST start with `1` and be incremented by `1` for each `HEARTBEAT` a peer sends.
 * `HEARTBEAT.IncomingSeq` MUST BE the sequence number from the last received heartbeat for which all previously received WAMP messages have been processed or `0` when no `HEARTBEAT` has yet been received
 *  `HEARTBEAT.Discard` is an arbitrary string discarded by the peer.

> The `HEARTBEAT.Discard` can be used to add some traffic volume to the HEARTBEAT message e.g. to keep mobile radio channels in a low-latency, high-power state. The string SHOULD be a random string (otherwise compressing transports might compress away the traffic volume).
>

*Example*

   	[7, 0, 1]

*Example*

   	[7, 23, 5]

*Example*

   	[7, 23, 5, "throw me away ... I am just noise"]

Incoming heartbeats are not required to be answered by an outgoing heartbeat. Sending of heartbeats is under independent control with each peer.


## Advanced Features

In addition to the *basic features* defined in the first part of this document, RPCs and PubSub calls can offer *advanced features*.

*Advanced features* need to be announced by the peer which implements them.

*Example: An Endpoint implementing the roles of Publisher and Subscriber and implementing some advanced features on the Publisher.*

   	[1, 9129137332, {
      "roles": {
         "publisher": {
            "features": {
               "publisher_exclusion":      true,
               "publisher_identification": true
            }
         },
         "subscriber": {

         }
      }
   	}]

*Example: A Router implementing the role of Broker and supporting all advanced features.*

   	[1, 9129137332, {
      "roles": {
         "broker": {
            "features": {
               "subscriber_blackwhite_listing": true,
               "publisher_exclusion":           true,
               "publisher_identification":      true,
               "publication_trustlevels":       true,
               "pattern_based_subscription":    true,
               "partitioned_pubsub":            true,
               "subscriber_metaevents":         true,
               "subscriber_list":               true,
               "event_history":                 true
            }
         }
   	}]

*Feature Announcement and Advanced Features*

The use of *feature announcement* in WAMP allows for

 * only implementing subsets of functionality
 * graceful degration


The complete list of *advanced features* currently defined per role is:

| Feature                       |  Publisher  |  Broker  |  Subscriber  |  Caller  |  Dealer  |  Callee  |
|-------------------------------|-------------|----------|--------------|----------|----------|----------|
| **Remote Procedure Calls**    |             |          |              |          |          |          |
| callee_blackwhite_listing     |             |          |              | X        | X        |          |
| caller_exclusion              |             |          |              | X        | X        |          |
| caller_identification         |             |          |              | X        | X        | X        |
| call_trustlevels              |             |          |              |          | X        | X        |
| pattern_based_registration    |             |          |              |          | X        | X        |
| partitioned_rpc               |             |          |              | X        | X        | X        |
| call_timeout                  |             |          |              | X        | X        | X        |
| call_canceling                |             |          |              | X        | X        | X        |
| progressive_call_results      |             |          |              | X        | X        | X        |
|                               |             |          |              |          |          |          |
| **Publish & Subscribe**       |             |          |              |          |          |          |
| subscriber_blackwhite_listing | X           | X        |              |          |          |          |
| publisher_exclusion           | X           | X        |              |          |          |          |
| publisher_identification      | X           | X        | X            |          |          |          |
| publication_trustlevels       |             | X        | X            |          |          |          |
| pattern_based_subscription    |             | X        | X            |          |          |          |
| partitioned_pubsub            | X           | X        | X            |          |          |          |
| subscriber_metaevents         |             | X        | X            |          |          |          |
| subscriber_list               |             | X        | X            |          |          |          |
| event_history                 |             | X        | X            |          |          |          |

*Network Agent*

When a software agent operates in a network protocol, it often identifies itself, its application type, operating system, software vendor, or software revision, by submitting a characteristic identification string to its operating peer.

Similar to what browsers do with the `User-Agent` HTTP header, both the `HELLO` and the `WELCOME` message MAY disclose the WAMP implementation in use to its peer:

   	HELLO.Details.agent|string

and

   	WELCOME.Details.agent|string

*Example*

   	[1, 9129137332, {
         "agent": "AutobahnPython-0.7.0",
         "roles": {
            "publisher": {}
         }
   	}]




## Publish & Subscribe

All of the following advanced features for Publish & Subscribe are optional.

If a WAMP implementation supports a specific advanced feature, it should announce support in the initial `HELLO` message:

	HELLO.Details.roles.<role>.features.<feature>|bool := true

Otherwise, the feature is assumed to be unsupported.


### Subscriber Black- and Whitelisting

Support for this feature MUST be announced by *Publishers* (`role := "publisher"`) and *Brokers* (`role := "broker"`) via

   	HELLO.Details.roles.<role>.features.subscriber_blackwhite_listing|bool := true

If the feature is supported, a *Publisher* may restrict the actual receivers of an event from the group of subscribers through the use of

 * `PUBLISH.Options.exclude|list`
 * `PUBLISH.Options.eligible|list`

`PUBLISH.Options.exclude` is a list of WAMP session IDs (`integer`s) providing an explicit list of (potential) *Subscribers* that won't receive a published event, even though they may be subscribed. In other words, `PUBLISH.Options.exclude` is a blacklist of (potential) *Subscribers*.

`PUBLISH.Options.eligible` is a list of WAMP session IDs (`integer`s) providing an explicit list of (potential) *Subscribers* that are allowed to receive a published event. In other words, `PUBLISH.Options.eligible` is a whitelist of (potential) *Subscribers*.

The *Broker* will dispatch events published only to *Subscribers* that are not explicitly excluded via `PUBLISH.Options.exclude` **and** which are explicitly eligible via `PUBLISH.Options.eligible`.

*Example*

    [16, 239714735, {"exclude": [7891255, 1245751]}, "com.myapp.mytopic1", ["Hello, world!"]]

The above event will get dispatched to all *Subscribers* of `com.myapp.mytopic1`, but not WAMP sessions with IDs `7891255` or `1245751` (and also not the publishing session).

*Example*

    [16, 239714735, {"eligible": [7891255, 1245751]}, "com.myapp.mytopic1", ["Hello, world!"]]

The above event will get dispatched to WAMP sessions with IDs `7891255` or `1245751` only - but only if those are subscribed to the topic `com.myapp.mytopic1`.

*Example*

    [16, 239714735, {"exclude": [7891255], "eligible": [7891255, 1245751, 9912315]}, "com.myapp.mytopic1", ["Hello, world!"]]

The above event will get dispatched to WAMP sessions with IDs `1245751` or `9912315` only (since `7891255` is excluded) - but only if those are subscribed to the topic `com.myapp.mytopic1`.


### Publisher Exclusion

Support for this feature MUST be announced by *Publishers* (`role := "publisher"`) and *Brokers* (`role := "broker"`) via

   	HELLO.Details.roles.<role>.features.publisher_exclusion|bool := true

By default, a *Publisher* of an event will **not** itself receive an event published, even when subscribed to the `Topic` the *Publisher* is publishing to. This behavior can be overridden via

   	PUBLISH.Options.exclude_me|bool

When publishing with `PUBLISH.Options.exclude_me := false`, the *Publisher* of the event will receive that event, if it is subscribed to the `Topic` published to.

*Example*

    [16, 239714735, {"exclude_me": false}, "com.myapp.mytopic1", ["Hello, world!"]]

In this example, the *Publisher* will receive the published event, if it is subscribed to `com.myapp.mytopic1`.


### Publisher Identification

Support for this feature MUST be announced by *Publishers* (`role := "publisher"`), *Brokers* (`role := "broker"`) and *Subscribers* (`role := "subscriber"`) via

   	HELLO.Details.roles.<role>.features.publisher_identification|bool := true

A *Publisher* may request the disclosure of its identity (its WAMP session ID) to receivers of a published event by setting

   	PUBLISH.Options.disclose_me|bool := true

*Example*

    [16, 239714735, {"disclose_me": true}, "com.myapp.mytopic1", ["Hello, world!"]]

If above event is published by a *Publisher* with WAMP session ID `3335656`, the *Broker* would send an `EVENT` message to *Subscribers* with the *Publisher's* WAMP session ID in `EVENT.Details.publisher`:

*Example*

   	[36, 5512315355, 4429313566, {"publisher": 3335656}, ["Hello, world!"]]

Note that a *Broker* may deny a *Publisher's* request to disclose its identity:

*Example*

    [4, 239714735, {}, "wamp.error.option_disallowed.disclose_me"]

A *Broker* may also (automatically) disclose the identity of a *Publisher* even without the *Publisher* having explicitly requested to do so when the *Broker* configuration (for the publication topic) is set up to do so.


### Publication Trust Levels

Support for this feature MUST be announced by *Subscribers* (`role := "subscriber"`) and *Brokers* (`role := "broker"`) via

   	HELLO.Details.roles.<role>.features.publication_trustlevels|bool := true

A *Broker* may be configured to automatically assign *trust levels* to events published by *Publishers* according to the *Broker* configuration on a per-topic basis and/or depending on the application defined role of the (authenticated) *Publisher*.

A *Broker* supporting trust level will provide

   	EVENT.Details.trustlevel|integer

in an `EVENT` message sent to a *Subscriber*. The trustlevel `0` means lowest trust, and higher integers represent (application-defined) higher levels of trust.

*Example*

   	[36, 5512315355, 4429313566, {"trustlevel": 2}, ["Hello, world!"]]

In above event, the *Broker* has (by configuration and/or other information) deemed the event publication to be of trustlevel `2`.


### Pattern-based Subscriptions

Support for this feature MUST be announced by *Subscribers* (`role := "subscriber"`) and *Brokers* (`role := "broker"`) via

   	HELLO.Details.roles.<role>.features.pattern_based_subscription|bool := true

By default, *Subscribers* subscribe to topics with **exact matching policy**. That is an event will only be dispatched to a *Subscriber* by the *Broker* if the topic published to (`PUBLISH.Topic`) *exactly* matches the topic subscribed to (`SUBSCRIBE.Topic`).

A *Subscriber* might want to subscribe to topics based on a *pattern*. This can be useful to reduce the number of individual subscriptions to be set up and to subscribe to topics the *Subscriber* is not aware of at the time of subscription, or which do not yet exist at this time.

If the *Broker* and the *Subscriber* support **pattern-based subscriptions**, this matching can happen by

 * prefix-matching policy
 * wildcard-matching policy

*Brokers* and *Subscribers* MUST announce support for non-exact matching policies in the `HELLO.Options` (see that chapter).

#### Prefix Matching

A *Subscriber* requests **prefix-matching policy** with a subscription request by setting

   	SUBSCRIBE.Options.match|string := "prefix"

*Example*

   	[32, 912873614, {"match": "prefix"}, "com.myapp.topic.emergency"]

When a **prefix-matching policy** is in place, any event with a topic that has `SUBSCRIBE.Topic` as a *prefix* will match the subscription, and potentially be delivered to *Subscribers* on the subscription.

In the above example, events with `PUBLISH.Topic`

 * `com.myapp.topic.emergency.11`
 * `com.myapp.topic.emergency-low`
 * `com.myapp.topic.emergency.category.severe`
 * `com.myapp.topic.emergency`

will all apply for dispatching. An event with `PUBLISH.Topic` e.g. `com.myapp.topic.emerge` will not apply.

The *Broker* will apply the prefix-matching based on the UTF-8 encoded byte string for the `PUBLISH.Topic` and the `SUBSCRIBE.Topic`.

#### Wildcard Matching

A *Subscriber* requests **wildcard-matching policy** with a subscription request by setting

   	SUBSCRIBE.Options.match|string := "wildcard"

Wildcard-matching allows to provide wildcards for **whole** URI components.

*Example*

   	[32, 912873614, {"match": "wildcard"}, "com.myapp..userevent"]

In above subscription request, the 3rd URI component is empty, which signals a wildcard in that URI component position. In this example, events with `PUBLISH.Topic`

 * `com.myapp.foo.userevent`
 * `com.myapp.bar.userevent`
 * `com.myapp.a12.userevent`

will all apply for dispatching. Events with `PUBLISH.Topic`

 * `com.myapp.foo.userevent.bar`
 * `com.myapp.foo.user`
 * `com.myapp2.foo.userevent`

will not apply for dispatching.

#### General

When a single event matches more than one of a *Subscriber's* subscriptions, the event will be delivered for each subscription. The *Subscriber* can detect the delivery of that same event on multiple subscriptions via `EVENT.PUBLISHED.Publication`, which will be identical.

Since each *Subscriber's* subscription "stands on its own", there is no *set semantics* implied by pattern-based subscriptions. E.g. a *Subscriber* cannot subscribe to a broad pattern, and then unsubscribe from a subset of that broad pattern to form a more complex subscription. Each subscription is separate.

If a subscription was established with a pattern-based matching policy, a *Broker* MUST supply the original `PUBLISH.Topic` as provided by the *Publisher* in

   	EVENT.Details.topic|uri

to the *Subscribers*.

*Example*

   	[36, 5512315355, 4429313566, {"topic": "com.myapp.topic.emergency.category.severe" }, ["Hello, world!"]]


### Partitioned Subscriptions & Publications

Support for this feature MUST be announced by *Publishers* (`role := "publisher"`), *Subscribers* (`role := "subscriber"`) and *Brokers* (`role := "broker"`) via

   	HELLO.Details.roles.<role>.features.partitioned_pubsub|bool := true

Resource keys: `PUBLISH.Options.rkey|string` is a stable, technical **resource key**.

> E.g. if your sensor has a unique serial identifier, you can use that.


*Example*

    [16, 239714735, {"rkey": "sn239019"}, "com.myapp.sensor.sn239019.temperature", [33.9]]


Node keys: `SUBSCRIBE.Options.nkey|string` is a stable, technical **node key**.

> E.g. if your backend process runs on a dedicated host, you can use its hostname.


*Example*

   	[32, 912873614, {"match": "wildcard", "nkey": "node23"}, "com.myapp.sensor..temperature"]


### Subscriber Meta Events

Support for this feature MUST be announced by *Subscribers* (`role := "subscriber"`) and *Brokers* (`role := "broker"`) via

   	HELLO.Details.roles.<role>.features.subscriber_metaevents|bool := true

*Example*

   	[32, 713845233,
         {"metatopics": ["wamp.metatopic.subscriber.add",
                         "wamp.metatopic.subscriber.remove"]},
         "com.myapp.mytopic1"]

If above subscription request by a *Subscriber 1* succeeds, the *Broker* will dispatch meta events to *Subscriber 1* for every *Subscriber 2, 3, ..* added to or removed from a subscription for `com.myapp.mytopic1`. It will also dispatch "normal" events on the topic `com.myapp.mytopic1` to *Subscriber 1*.

*Example*

   	[32, 713845233,
         {"metatopics": ["wamp.metatopic.subscriber.add",
                         "wamp.metatopic.subscriber.remove"],
          "metaonly": 1},
         "com.myapp.mytopic1"]

This subscription works like the previous one, except that "normal" events on the topic `com.myapp.mytopic1` will NOT be dispatched to *Subscriber 1*. Consequently, it is called a "Meta Event only subscription".


Metaevents are always generated by the *Broker* itself and do not contain application payload:

   	[EVENT, SUBSCRIBED.Subscription|id, PUBLISHED.Publication|id, Details|dict]

*Example*

   	[36, 5512315355, 71415664, {"metatopic": "wamp.metatopic.subscriber.add", "session": 9712478}]

*Example*

   	[36, 5512315355, 71415664, {"metatopic": "wamp.metatopic.subscriber.remove", "session": 9712478}]


The following metatopics are currently defined:

 1. `wamp.metatopic.subscriber.add`: A new subscriber is added to the subscription.
 2. `wamp.metatopic.subscriber.remove`: A subscriber is removed from the subscription.


### Subscriber List

A *Broker* may allow to retrieve the current list of *Subscribers* for a given subscription.

Support for this feature MUST be announced by *Subscribers* (`role := "subscriber"`) and *Brokers* (`role := "broker"`) via

   	HELLO.Details.roles.<role>.features.subscriber_list|bool := true

A *Broker* that implements *subscriber list* must (also) announce role `HELLO.roles.callee` and provide the following (built in) procedures.

A *Caller* (that is also a *Subscriber*) can request the current list of subscribers for a subscription (it is subscribed to) by calling the *Broker* procedure

   	wamp.broker.subscriber.list

with `Arguments = [subscription|id]` where

 * `subscription` is the ID of the subscription as returned from `SUBSCRIBED.Subscription`

and `Result = sessions|list` where

 * `sessions` is a list of WAMP session IDs currently subscribed to the given subscription.

A call to `wamp.broker.subscriber.list` may fail with

   	wamp.error.no_such_subscription
   	wamp.error.not_authorized

**Open Issues**

 1. What if we have multiple *Brokers* (a cluster)? The call would need to be forwarded.
 2. Should we allow "paging" (`offset|integer` and `limit|integer` arguments)?
 3. Should we allow *Subscribers* to list subscribers for subscription it is not itself subscribed to? How would the *Callee* know the subscription ID it wants to look up without subscribing?
 4. Why retrieve the list for a subscription ID, when the interest may lie in how many subscribers there are to a topic, e.g. if a publisher wants to judge its current reach?
 5. The *Router* needs to implement a *Dealer* role as well in order to be able to route the RPC, since calls can only be addressed to *Dealers*.
 6. We should probably then also have a *Callee* as a separate peer. Otherwise we break the rule that peers can implement Broker/Dealer OR Caller/Callee/Subscriber/Publisher roles.
 7. If we have the separate *Callee*, then how does this get the list? One way would be using subscription meta-events.


### Event History

Support for this feature MUST be announced by *Subscribers* (`role := "subscriber"`) and *Brokers* (`role := "broker"`) via

   	HELLO.Details.roles.<role>.features.event_history|bool := true

Instead of complex QoS for message delivery, a *Broker* may provide *message history*. A *Subscriber* is responsible to handle overlaps (duplicates) when it wants "exactly-once" message processing across restarts.

The *Broker* may allow for configuration on a per-topic basis.

The event history may be transient or persistent message history (surviving *Broker* restarts).

A *Broker* that implements *event history* must (also) announce role `HELLO.roles.callee`, indicate `HELLO.roles.broker.history == 1` and provide the following (builtin) procedures.

A *Caller* can request message history by calling the *Broker* procedure

   	wamp.topic.history.last

with `Arguments = [topic|uri, limit|integer]` where

 * `topic` is the topic to retrieve event history for
 * `limit` indicates the number of last N events to retrieve

or by calling

   	wamp.topic.history.since

with `Arguments = [topic|uri, timestamp|string]` where

 * `topic` is the topic to retrieve event history for
 * `timestamp` indicates the UTC timestamp since when to retrieve the events in the ISO-8601 format `yyyy-MM-ddThh:mm:ss:SSSZ` (e.g. `"2013-12-21T13:43:11:000Z"`)

or by calling

   	wamp.topic.history.after

with `Arguments = [topic|uri, publication|id]`

 * `topic` is the topic to retrieve event history for
 * `publication` is the id of an event which marks the start of the events to retrieve from history


*FIXME*

 1. Should we use `topic|uri` or `subscription|id` in `Arguments`?
      - Since we need to be able to get history for pattern-based subscriptions as well, a subscription|id makes more sense: create pattern-based subscription, then get the event history for this.
      - The only restriction then is that we may not get event history without a current subscription covering the events. This is a minor inconvenience at worst.
 2. Can `wamp.topic.history.after` be implemented (efficiently) at all?
 3. How does that interact with pattern-based subscriptions?
 4. The same question as with the subscriber lists applies where: to stay within our separation of roles, we need a broker + a separate peer which implements the callee role. Here we do not have a mechanism to get the history from the broker.






## Remote Procedure Calls

All of the following advanced features for Remote Procedure Calls are optional.

If a WAMP implementation supports a specific advanced feature, it should announce support in the initial `HELLO` message:

   	HELLO.Details.roles.<role>.features.<feature>|bool := true

Otherwise, the feature is assumed to be unsupported.


### Callee Black- and Whitelisting

Support for this feature MUST be announced by *Callers* (`role := "caller"`) and *Dealers* (`role := "dealer"`) via

   	HELLO.Details.roles.<role>.features.callee_blackwhite_listing|bool := true


A *Caller* may restrict the endpoints that will handle a call beyond those registered via

 * `CALL.Options.exclude|list`
 * `CALL.Options.eligible|list`

`CALL.Options.exclude` is a list of WAMP session IDs (`integer`s) providing an explicit list of (potential) *Callees* that a call won't be forwarded to, even though they might be registered. In other words, `CALL.Options.exclude` is a blacklist of (potential) *Callees*.

`CALL.Options.eligible` is a list of WAMP session IDs (`integer`s) providing an explicit list of (potential) *Callees* that are (potentially) forwarded the call issued. In other words, `CALL.Options.eligible` is a whitelist of (potential) *Callees*.

The *Dealer* will forward a call only to registered *Callees* that are not explicitly excluded via `CALL.Options.exclude` **and** which are explicitly eligible via `CALL.Options.eligible`.

*Example*

   	[48, 7814135, {"exclude": [7891255, 1245751]}, "com.myapp.echo", ["Hello, world!"]]

The above call will (potentially) get forwarded to all *Callees* of `com.myapp.echo`, but not WAMP sessions with IDs `7891255` or `1245751` (and also not the calling session).

*Example*

   	[48, 7814135, {"eligible": [7891255, 1245751]}, "com.myapp.echo", ["Hello, world!"]]

The above call will (potentially) get forwarded to WAMP sessions with IDs `7891255` or `1245751` only - but only if those are registered for the procedure `com.myapp.echo`.

*Example*

   	[48, 7814135, {"exclude": [7891255], "eligible": [7891255, 1245751, 9912315]},
      "com.myapp.echo", ["Hello, world!"]]

The above call will (potentially) get forwarded to WAMP sessions with IDs `1245751` or `9912315` only (since `7891255` is excluded) - but only if those are registered for the procedure `com.myapp.echo`.


### Caller Exclusion

Support for this feature MUST be announced by *Callers* (`role := "caller"`) and *Dealers* (`role := "dealer"`) via

   	HELLO.Details.roles.<role>.features.caller_exclusion|bool := true


By default, a *Caller* of a procedure will **never** itself be forwarded the call issued, even when registered for the `Procedure` the *Caller* is publishing to. This behavior can be overridden via

   	CALL.Options.exclude_me|bool

When calling with `CALL.Options.exclude_me := false`, the *Caller* of the procedure might be forwarded the call issued - if it is registered for the `Procedure` called.

*Example*

   	[48, 7814135, {"exclude_me": false}, "com.myapp.echo", ["Hello, world!"]]

In this example, the *Caller* might be forwarded the call issued, if it is registered for `com.myapp.echo`.


### Caller Identification

Support for this feature MUST be announced by *Callers* (`role := "caller"`), *Callees* (`role := "callee"`) and *Dealers* (`role := "dealer"`) via

   	HELLO.Details.roles.<role>.features.caller_identification|bool := true


A *Caller* MAY **request** the disclosure of its identity (its WAMP session ID) to endpoints of a routed call via

   	CALL.Options.disclose_me|bool := true

*Example*

   	[48, 7814135, {"disclose_me": true}, "com.myapp.echo", ["Hello, world!"]]

If above call is issued by a *Caller* with WAMP session ID `3335656`, the *Dealer* sends an `INVOCATION` message to *Callee* with the *Caller's* WAMP session ID in `INVOCATION.Details.caller`:

*Example*

   	[68, 6131533, 9823526, {"caller": 3335656}, ["Hello, world!"]]

Note that a *Dealer* MAY disclose the identity of a *Caller* even without the *Caller* having explicitly requested to do so when the *Dealer* configuration (for the called procedure) is setup to do so.

A *Dealer* MAY deny a *Caller's* request to disclose its identity:

*Example*

    [4, 7814135, "wamp.error.disclose_me.not_allowed"]


### Call Trust Levels

Support for this feature MUST be announced by *Callees* (`role := "callee"`) and *Dealers* (`role := "dealer"`) via

   	HELLO.Details.roles.<role>.features.call_trustlevels|bool := true


A *Dealer* may be configured to automatically assign *trust levels* to calls issued by *Callers* according to the *Dealer* configuration on a per-procedure basis and/or depending on the application defined role of the (authenticated) *Caller*.

A *Dealer* supporting trust level will provide

   	INVOCATION.Details.trustlevel|integer

in an `INVOCATION` message sent to a *Callee*. The trustlevel `0` means lowest trust, and higher integers represent (application-defined) higher levels of trust.

*Example*

   	[68, 6131533, 9823526, {"trustlevel": 2}, ["Hello, world!"]]

In above event, the *Dealer* has (by configuration and/or other information) deemed the call (and hence the invocation) to be of trustlevel `2`.


### Pattern-based Registrations

Support for this feature MUST be announced by *Callees* (`role := "callee"`) and *Dealers* (`role := "dealer"`) via

   	HELLO.Details.roles.<role>.features.pattern_based_registration|bool := true


By default, *Callees* register procedures with **exact matching policy**. That is a call will only be routed to a *Callee* by the *Dealer* if the procedure called (`CALL.Procedure`) *exactly* matches the endpoint registered (`REGISTER.Procedure`).

A *Callee* might want to register procedures based on a *pattern*. This can be useful to reduce the number of individual registrations to be set up.

If the *Dealer* and the *Callee* support **pattern-based registrations**, this matching can happen by

 * prefix-matching policy
 * wildcard-matching policy

*Dealers* and *Callees* MUST announce support for non-exact matching policies in the `HELLO.Options` (see that chapter).

#### Prefix Matching

A *Callee* requests **prefix-matching policy** with a registration request by setting

   	REGISTER.Options.match|string := "prefix"

*Example*

   	[64, 612352435, {"match": "prefix"}, "com.myapp.myobject1"]

When a **prefix-matching policy** is in place, any call with a procedure that has `REGISTER.Procedure` as a *prefix* will match the registration, and potentially be routed to *Callees* on that registration.

In above example, the following calls with `CALL.Procedure`

 * `com.myapp.myobject1.myprocedure1`
 * `com.myapp.myobject1-mysubobject1`
 * `com.myapp.myobject1.mysubobject1.myprocedure1`
 * `com.myapp.myobject1`

will all apply for call routing. A call with one of the following `CALL.Procedure`

 * `com.myapp.myobject2`
 * `com.myapp.myobject`

will not apply.

The *Dealer* will apply the prefix-matching based on the UTF-8 encoded byte string for the `CALL.Procedure` and the `REGISTER.Procedure`.

#### Wildcard Matching

A *Callee* requests **wildcard-matching policy** with a registration request by setting

   	REGISTER.Options.match|string := "wildcard"

Wildcard-matching allows to provide wildcards for **whole** URI components.

*Example*

   	[64, 612352435, {"match": "wildcard"}, "com.myapp..myprocedure1"]

In the above registration request, the 3rd URI component is empty, which signals a wildcard in that URI component position. In this example, calls with `CALL.Procedure` e.g.

 * `com.myapp.myobject1.myprocedure1`
 * `com.myapp.myobject2.myprocedure1`

will all apply for call routing. Calls with `CALL.Procedure` e.g.

 * `com.myapp.myobject1.myprocedure1.mysubprocedure1`
 * `com.myapp.myobject1.myprocedure2`
 * `com.myapp2.myobject1.myprocedure1`

will not apply for call routing.

When a single call matches more than one of a *Callees* registrations, the call MAY be routed for invocation on multiple registrations, depending on call settings.

--------------
FIXME: The *Callee* can detect the invocation of that same call on multiple registrations via `INVOCATION.CALL.Request`, which will be identical.

Since each *Callees* registrations "stands on it's own", there is no *set semantics* implied by pattern-based registrations. E.g. a *Callee* cannot register to a broad pattern, and then unregister from a subset of that broad pattern to form a more complex registration. Each registration is separate.

If an endpoint was registered with a pattern-based matching policy, a *Dealer* MUST supply the original `CALL.Procedure` as provided by the *Caller* in `INVOCATION.Details.procedure` to the *Callee*.


### Partitioned Registrations & Calls

Support for this feature MUST be announced by *Callers* (`role := "caller"`), *Callees* (`role := "callee"`) and *Dealers* (`role := "dealer"`) via

   	HELLO.Details.roles.<role>.features.partitioned_rpc|bool := true


*Partitioned Calls* allows to run a call issued by a *Caller* on one or more endpoints implementing the called procedure.

* all
* any
* partition


`CALL.Options.runon|string := "all" or "any" or "partition"`
`CALL.Options.runmode|string := "gather" or "progressive"`
`CALL.Options.rkey|string`


#### "Any" Calls

If `CALL.Options.runon == "any"`, the call will be routed to one *randomly* selected *Callee* that registered an implementing endpoint for the called procedure. The call will then proceed as for standard (non-distributed) calls.


#### "All" Calls

If `CALL.Options.runon == "all"`, the call will be routed to all *Callees* that registered an implementing endpoint for the called procedure. The calls will run in parallel and asynchronously.

If `CALL.Options.runmode == "gather"` (the default, when `CALL.Options.runmode` is missing), the *Dealer* will gather the individual results received via `YIELD` messages from *Callees* into a single list, and return that in `RESULT` to the original *Caller* - when all results have been received.

If `CALL.Options.runmode == "progressive"`, the *Dealer* will call each endpoint via a standard `INVOCATION` message and immediately forward individual results received via `YIELD` messages from the *Callees* as progressive `RESULT` messages (`RESULT.Details.progress == 1`) to the original *Caller* and send a final `RESULT` message (with empty result) when all individual results have been received.

If any of the individual `INVOCATION`s returns an `ERROR`, the further behavior depends on ..

Fail immediate:

The *Dealer* will immediately return a `ERROR` message to the *Caller* with the error from the `ERROR` message of the respective failing invocation. It will further send `INTERRUPT` messages to all *Callees* for which it not yet has received a response, and ignore any `YIELD` or `ERROR` messages it might receive subsequently for the pending invocations.

The *Dealer* will accumulate ..


#### "Partitioned" Calls

If `CALL.Options.runmode == "partition"`, then `CALL.Options.rkey` MUST be present.

The call is then routed to all endpoints that were registered ..

The call is then processed as for "All" Calls.


### Call Timeouts

Support for this feature MUST be announced by *Callers* (`role := "caller"`), *Callees* (`role := "callee"`) and *Dealers* (`role := "dealer"`) via

   	HELLO.Details.roles.<role>.features.call_timeout|bool := true

A *Caller* might want to issue a call providing a *timeout* for the call to finish.

A *timeout* allows to **automatically** cancel a call after a specified time either at the *Callee* or at the *Dealer*.

A *Callee* specifies a timeout by providing

   	CALL.Options.timeout|integer

in ms. A timeout value of `0` deactivates automatic call timeout. This is also the default value.

The timeout option is a companion to, but slightly different from the `CANCEL` and `INTERRUPT` messages that allow a *Caller* and *Dealer* to **actively** cancel a call or invocation.

In fact, a timeout timer might run at three places:

 * *Caller*
 * *Dealer*
 * *Callee*


### Canceling Calls

Support for this feature MUST be announced by *Callers* (`role := "caller"`), *Callees* (`role := "callee"`) and *Dealers* (`role := "dealer"`) via

   	HELLO.Details.roles.<role>.features.call_canceling|bool := true


A *Caller* might want to actively cancel a call that was issued, but not has yet returned. An example where this is useful could be a user triggering a long running operation and later changing his mind or no longer willing to wait.

The message flow between *Callers*, a *Dealer* and *Callees* for canceling remote procedure calls involves the following messages:

 * `CANCEL`
 * `INTERRUPT`

A call may be cancelled at the *Callee*

![alt text](figure/rpc_cancel1.png "RPC Message Flow: Calls")

A call may be cancelled at the *Dealer*

![alt text](figure/rpc_cancel2.png "RPC Message Flow: Calls")

A *Caller* cancels a remote procedure call initiated (but not yet finished) by sending a `CANCEL` message to the *Dealer*:

    [CANCEL, CALL.Request|id, Options|dict]

A *Dealer* cancels an invocation of an endpoint initiated (but not yet finished) by sending a `INTERRUPT` message to the *Callee*:

    [INTERRUPT, INVOCATION.Request|id, Options|dict]

Options:

   	CANCEL.Options.mode|string == "skip" | "kill" | "killnowait"


### Progressive Call Results

Support for this advanced feature MUST be announced by *Callers* (`role := "caller"`), *Callees* (`role := "callee"`) and *Dealers* (`role := "dealer"`) via

   	HELLO.Details.roles.<role>.features.progressive_call_results|bool := true


A procedure implemented by a *Callee* and registered at a *Dealer* may produce progressive results (incrementally). The message flow for progressive results involves:

![alt text](figure/rpc_progress1.png "RPC Message Flow: Calls")


A *Caller* indicates it's willingness to receive progressive results by setting

   	CALL.Options.receive_progress|bool := true

*Example.* Caller-to-Dealer `CALL`

   	[48, 77133, {"receive_progress": true}, "com.myapp.compute_revenue", [2010, 2011, 2012]]

If the *Callee* supports progressive calls, the *Dealer* will forward the *Caller's* willingness to receive progressive results by setting

   	INVOCATION.Options.receive_progress|bool := true

*Example.* Dealer-to-Callee `INVOCATION`

   	[68, 87683, 324, {"receive_progress": true}, [2010, 2011, 2012]]

An endpoint implementing the procedure produces progressive results by sending `YIELD` messages to the *Dealer* with

   	YIELD.Options.progress|bool := true

*Example.* Callee-to-Dealer progressive `YIELDs`

   	[70, 87683, {"progress": true}, ["Y2010", 120]]
   	[70, 87683, {"progress": true}, ["Y2011", 205]]
   	...

Upon receiving an `YIELD` message from a *Callee* with `YIELD.Options.progress == true` (for a call that is still ongoing), the *Dealer* will **immediately** send a `RESULT` message to the original *Caller* with

   	RESULT.Details.progress|bool := true

*Example.* Dealer-to-Caller progressive `RESULTs`

   	[50, 77133, {"progress": true}, ["Y2010", 120]]
   	[50, 77133, {"progress": true}, ["Y2011", 205]]
   	...

An invocation MUST *always* end in either a *normal* `RESULT` or `ERROR` message being sent by the *Callee* and received by the *Dealer*.

*Example.* Callee-to-Dealer final `YIELD`

   	[70, 87683, {}, ["Total", 490]]

*Example.* Callee-to-Dealer final `ERROR`

   	[4, 87683, {}, "com.myapp.invalid_revenue_year", [1830]]

A call MUST *always* end in either a *normal* `RESULT` or `ERROR` message being sent by the *Dealer* and received by the *Caller*.

*Example.* Dealer-to-Caller final `RESULT`

   	[50, 77133, {}, ["Total", 490]]

*Example.* Dealer-to-Caller final `ERROR`

   	[4, 77133, {}, "com.myapp.invalid_revenue_year", [1830]]

In other words: `YIELD` with `YIELD.Options.progress == true` and `RESULT` with `RESULT.Details.progress == true` messages may only be sent *during* a call or invocation is still ongoing.

The final `YIELD` and final `RESULT` may also be empty, e.g. when all actual results have already been transmitted in progressive result messages.

*Example.* Callee-to-Dealer `YIELDs`

   	[70, 87683, {"progress": true}, ["Y2010", 120]]
   	[70, 87683, {"progress": true}, ["Y2011", 205]]
   	 ...
   	[70, 87683, {"progress": true}, ["Total", 490]]
   	[70, 87683, {}]

*Example.* Dealer-to-Caller `RESULTs`

   	[50, 77133, {"progress": true}, ["Y2010", 120]]
   	[50, 77133, {"progress": true}, ["Y2011", 205]]
   	 ...
   	[50, 77133, {"progress": true}, ["Total", 490]]
   	[50, 77133, {}]

The progressive `YIELD` and progressive `RESULT` may also be empty, e.g. when those messages are only used to signal that the procedure is still running and working, and the actual result is completely delivered in the final `YIELD` and `RESULT`:

*Example.* Callee-to-Dealer `YIELDs`

   	[70, 87683, {"progress": true}]
   	[70, 87683, {"progress": true}]
   	...
   	[70, 87683, {}, [["Y2010", 120], ["Y2011", 205], ..., ["Total", 490]]]

*Example.* Dealer-to-Caller `RESULTs`

   	[50, 77133, {"progress": true}]
   	[50, 77133, {"progress": true}]
   	...
   	[50, 77133, {}, [["Y2010", 120], ["Y2011", 205], ..., ["Total", 490]]]

Note that intermediate, progressive results and/or the final result MAY have different structure. The WAMP peer implementation is responsible for mapping everything into a form suitable for consumption in the host language.

*Example.* Callee-to-Dealer `YIELDs`

   	[70, 87683, {"progress": true}, ["partial 1", 10]]
   	[70, 87683, {"progress": true}, [], {"foo": 10, "bar": "partial 1"}]
   	 ...
   	[70, 87683, {}, [1, 2, 3], {"moo": "hello"}]

*Example.* Dealer-to-Caller `RESULTs`

   	[50, 77133, {"progress": true}, ["partial 1", 10]]
   	[50, 77133, {"progress": true}, [], {"foo": 10, "bar": "partial 1"}]
   	 ...
   	[50, 77133, {}, [1, 2, 3], {"moo": "hello"}]

Even if a *Caller* has indicated it's expectation to receive progressive results by setting `CALL.Options.receive_progress|bool := true`, a *Callee* is **not required** to produce progressive results. `CALL.Options.receive_progress` and `INVOCATION.Options.receive_progress` are simply indications that the *Callee* is prepared to process progressive results, should there be any produced. In other words, *Callees* are free to ignore such `receive_progress` hints at any time.

<!--

**Errors**


If a *Caller* has not indicated support for progressive results or has sent a `CALL` to the *Dealer* without setting `CALL.Options.receive_progress == true`, and the *Dealer* sends a progressive `RESULT`, the *Caller* MUST fail the complete session with the *Dealer*.

If a *Dealer* has not indicated support for progressive results or the *Dealer* has sent an `INVOCATION` to the *Callee* without setting `INVOCATION.Options.receive_progress == true`, and the *Callee* sends a progressive `YIELD`, the *Dealer* MUST fail the call with error

   	wamp.error.unexpected_progress_in_yield

If a *Caller* has not indicated support for progressive results and sends a `CALL` to the *Dealer* while setting `CALL.Options.receive_progress == true`, the *Dealer* MUST fail the call

However, if a *Caller* has *not* indicated it's willingness to receive progressive results in a call, the *Dealer* MUST NOT send progressive `RESULTs`, and a *Callee* MUST NOT produce progressive `YIELDs`.

A *Dealer* that does not support progressive calls MUST ignore any option `CALL.Options.receive_progress` received by a *Caller*, and **not** forward the option to the *Callee*.



If a *Callee* that has not indicated support for progressive results and the *Dealer* sends an `INVOCATION` with `INVOCATION.Options.receive_progress == true


A *Callee* that does not support progressive results SHOULD ignore any `INVOCATION.Options.receive_progress` flag.

If a *Dealer* has not indicated support for progressive results, and it receives a `CALL` from a *Caller* with `CALL.Options.receive_progress == true`, the *Dealer* MUST fail the call with error

   	wamp.error.unsupported_feature.dealer.progressive_call_result



*Example.* Dealer-to-Caller `ERROR`

   	[4, 87683, {}, "wamp.error.unsupported_feature.dealer.progressive_call_result"]



If the *Caller* does not support receiving *progressive calls*, as indicated by

   	HELLO.Details.roles.caller.features.progressive_call_results == false

and *Dealer* receives a `YIELD` message from the *Callee* with `YIELD.Options.progress == true`, the *Dealer* MUST fail the call.

*Example.* Callee-to-Dealer `YIELD`

   	[70, 87683, {"progress": true}, ["partial 1", 10]]

*Example.* Dealer-to-Caller `ERROR`

   	[4, 87683, {}, "wamp.error.unsupported_feature.caller.progressive_call_result"]

If the *Dealer* does not support processing *progressive invocations*, as indicated by

   	HELLO.Details.roles.dealer.features.progressive_call_results == false

and *Dealer* receives a `YIELD` message from the *Callee* with `YIELD.Options.progress == true`, the *Dealer* MUST fail the call.

*Example.* Callee-to-Dealer `YIELD`

   	[70, 87683, {"progress": true}, ["partial 1", 10]]

*Example.* Dealer-to-Caller `ERROR`

   	[4, 87683, {}, "wamp.error.unsupported_feature.dealer.progressive_call_result"]

-->


## Authentication



![alt text](figure/hello_authenticated.png "WAMP Session denied")

Authentication is a complex area.

Some applications might want to leverage authentication information coming from the transport underlying WAMP, e.g. HTTP cookies or TLS certificates.

Some transports might imply trust or implicit authentication by their very nature, e.g. Unix domain sockets with appropriate file system permissions in place.

Other application might want to perform their own authentication using external mechanisms (completely outside and independent of WAMP).

Some applications might want to perform their own authentication schemes by using basic WAMP mechanisms, e.g. by using application-defined remote procedure calls.

And some applications might want to use a transport independent scheme, nevertheless predefined by WAMP.


### TLS Certificate-based Authentication

When running WAMP over a TLS (either secure WebSocket or raw TCP) transport, a peer may authenticate to the other via the TLS certificate mechanism. A server might authenticate to the client, and a client may authenticate to the server (TLS client-certificate based authentication).

This transport-level authentication information may be forward to the WAMP level within `HELLO.Options.transport.auth|any` in both directions (if available).


### HTTP Cookie-based Authentication

When running WAMP over WebSocket, the transport provides HTTP client cookies during the WebSocket opening handshake. The cookies can be used to authenticate one peer (the client) against the other (the server). The other authentication direction cannot be supported by cookies.

This transport-level authentication information may be forward to the WAMP level within `HELLO.Options.transport.auth|any` in the client-to-server direction.


### WAMP Challenge-Response Authentication

WAMP Challenge-Response ("WAMP-CRA") authentication is a simple, secure authentication mechanism using a shared secret. The client and the server share a *secret*. The secret never travels the wire, hence WAMP-CRA can be used via non-TLS connections. The actual pre-sharing of the secret is outside the scope of the authentication mechanism.

A typical authentication begins with the client sending a `HELLO` message specifying the `wampcra` method as (one of) the authentication methods:

```javascript
[1, "realm1",
	{
		"roles": ...,
		"authmethods": ["wampcra"],
		"authid": "peter"
	}
]
```

The `HELLO.Options.authmethods|list` is used by the client to announce the authentication methods it is prepared to perform. For WAMP-CRA, this MUST include `"wampcra"`.

The `HELLO.Options.authid|string` is the authentication ID (e.g. username) the client wishes to authenticate as. For WAMP-CRA, this MUST be provided.

If the server is unwilling or unable to perform WAMP-CRA authentication, it'll either skip forward trying other authentication methods (if the client announced any) or send an `ABORT` message.

If the server is willing to let the client authenticate using WAMP-CRA, and the server recognizes the provided `authid`, it'll send a `CHALLENGE` message:

```javascript
[4, "wampcra",
	{
		"challenge": "{\"nonce\": \"LHRTC9zeOIrt_9U3\", \"authprovider\": \"userdb\", \"authid\": \"peter\",
                       \"timestamp\": \"2014-06-22T16:36:25.448Z\", \"authrole\": \"user\",
                       \"authmethod\": \"wampcra\", \"session\": 3251278072152162}"
	}
]
```

The `CHALLENGE.Details.challenge|string` is a string the client needs to create a signature for. The string MUST BE a JSON serialized object which MUST contain:

 1. `authid|string`: The authentication ID the client will be authenticated as when the authentication succeeds.
 2. `authrole|string`: The authentication role the client will be authenticated as when the authentication succeeds.
 3. `authmethod|string`: The authentication methods, here `"wampcra"`
 4. `authprovider|string`: The actual provider of authentication. For WAMP-CRA, this can be freely chosen by the app, e.g. `userdb`.
 5. `nonce|string`: A random value.
 6. `timestamp|string`: The UTC timestamp (ISO8601 format) the authentication was started, e.g. `2014-06-22T16:51:41.643Z`.
 7. `session|int`: The WAMP session ID that will be assigned to the session once it is authenticated successfully.

The client needs to compute the signature as follows:

	signature := HMAC[SHA256]_{secret} (challenge)

That is, compute the HMAC-SHA256 using the shared `secret` over the `challenge`.

After computing the signature, the client will send an `AUTHENTICATE` message containing the signature:

```javascript
[5, "gir1mSx+deCDUV7wRM5SGIn/+R/ClqLZuH4m7FJeBVI=", {}]
```

The server will then check if

* the signature matches the one expected
* the `AUTHENTICATE` message was sent in due time

If the authentication succeeds, the server will finally respond with a `WELCOME` message:

```javascript
[2, 3251278072152162,
	{
		"authid": "peter",
		"authrole": "user",
		"authmethod": "wampcra",
		"authprovider": "userdb",
		"roles": ...
	}
]
```

The `WELCOME.Details` again contain the actual authentication information active.

If the authentication fails, the server will response with an `ABORT` message.


#### Server-side Verification

The challenge sent during WAMP-CRA contains

1. random information (the `nonce`) to make WAMP-CRA robust against replay attacks
2. timestamp information (the `timestamp`) to allow WAMP-CRA timeout on authentication requests that took too long
3. session information (the `session`) to bind the authentication to a WAMP session ID
4. all the authentication information that relates to authorization like `authid` and `authrole`


#### Three-legged Authentication

The signing of the challenge sent by the server usually is done directly on the client. However, this is no strict requirement.

E.g. a client might forward the challenge to another party (hence the "three-legged") for creating the signature. This can be used when the client was previously already authenticated to that third party, and WAMP-CRA should run piggy packed on that authentication.

The third party would, upon receiving a signing request, simply check if the client is already authenticated, and if so, create a signature for WAMP-CRA.

In this case, the secret is actually shared between the WAMP server who wants to authenticate clients using WAMP-CRA and the third party server, who shares a secret with the WAMP server.

This scenario is also the reason the challenge sent with WAMP-CRA is not simply a random value, but a JSON serialized object containing sufficient authentication information for the thrid party to check.


#### Password Salting

WAMP-CRA operates using a shared secret. While the secret is never sent over the wire, a shared secret often requires storage of that secret on the client and the server - and storing a password verbatim (unencrypted) is not recommended in general.

WAMP-CRA allows the use of salted passwords following the [PBKDF2](http://en.wikipedia.org/wiki/PBKDF2) key derivation scheme. With salted passwords, the password itself is never stored, but only a key derived from the password and a password salt. This derived key is then practically working as the new shared secret.

When the password is salted, the server will during WAMP-CRA send a `CHALLENGE` message containing additional information:

```javascript
[4, "wampcra",
	{
		"challenge": "{\"nonce\": \"LHRTC9zeOIrt_9U3\", \"authprovider\": \"userdb\", \"authid\": \"peter\",
                       \"timestamp\": \"2014-06-22T16:36:25.448Z\", \"authrole\": \"user\",
                       \"authmethod\": \"wampcra\", \"session\": 3251278072152162}",
		"salt": "salt123",
		"keylen": 32,
		"iterations": 1000
	}
]
```

The `CHALLENGE.Details.salt|string` is the password salt in use. The `CHALLENGE.Details.keylen|int` and `CHALLENGE.Details.iterations|int` are parameters for the PBKDF2 algorithm.



### Ticket-based Authentication

With *Ticket-based authentication*, the client needs to present the server an authentication "ticket" - some magic value to authenticate itself to the server.

This "ticket" could be a long-lived, pre-agreed secret (e.g. a user password) or a short-lived authentication token (like a Kerberos token). WAMP does not care or interpret the ticket presented by the client.

> Caution: This scheme is extremely simple and flexible, but the resulting security may be limited. E.g., the ticket value will be sent over the wire. If the transport WAMP is running over is not encrypted, a man-in-the-middle can sniff and possibly hijack the ticket. If the ticket value is reused, that might enable replay attacks.
> 

A typical authentication begins with the client sending a `HELLO` message specifying the `ticket` method as (one of) the authentication methods:

```javascript
[1, "realm1",
	{
		"roles": ...,
		"authmethods": ["ticket"],
		"authid": "joe"
	}
]
```

The `HELLO.Options.authmethods|list` is used by the client to announce the authentication methods it is prepared to perform. For Ticket-based, this MUST include `"ticket"`.

The `HELLO.Options.authid|string` is the authentication ID (e.g. username) the client wishes to authenticate as. For Ticket-based authentication, this MUST be provided.

If the server is unwilling or unable to perform Ticket-based authentication, it'll either skip forward trying other authentication methods (if the client announced any) or send an `ABORT` message.

If the server is willing to let the client authenticate using a ticket and the server recognizes the provided `authid`, it'll send a `CHALLENGE` message:

```javascript
[4, "ticket", {}]
```

The client will send an `AUTHENTICATE` message containing a ticket:

```javascript
[5, "secret!!!", {}]
```

The server will then check if the ticket provided is permissible (for the `authid` given).

If the authentication succeeds, the server will finally respond with a `WELCOME` message:

```javascript
[2, 3251278072152162,
	{
		"authid": "joe",
		"authrole": "user",
		"authmethod": "ticket",
		"authprovider": "static",
		"roles": ...
	}
]
```

where

 1. `authid|string`: The authentication ID the client was (actually) authenticated as.
 2. `authrole|string`: The authentication role the client was authenticated for.
 3. `authmethod|string`: The authentication method, here `"ticket"`
 4. `authprovider|string`: The actual provider of authentication. For Ticket-based authentication, this can be freely chosen by the app, e.g. `static` or `dynamic`.

The `WELCOME.Details` again contain the actual authentication information active. If the authentication fails, the server will response with an `ABORT` message.



## Reflection

*Reflection* denotes the ability of WAMP peers to examine the procedures, topics and errors provided or used by other peers.

I.e. a WAMP *Caller*, *Callee*, *Subscriber* or *Publisher* may be interested in retrieving a machine readable list and description of WAMP procedures and topics it is authorized to access or provide in the context of a WAMP session with a *Dealer* or *Broker*.

Reflection may be useful in the following cases:

 * documentation
 * discoverability
 * generating stubs and proxies

WAMP predefines the following procedures for performing run-time reflection on WAMP peers which act as *Brokers* and/or *Dealers*.

Predefined WAMP reflection procedures to *list* resources by type:

   	wamp.reflection.topic.list
   	wamp.reflection.procedure.list
   	wamp.reflection.error.list

Predefined WAMP reflection procedures to *describe* resources by type:

   	wamp.reflection.topic.describe
   	wamp.reflection.procedure.describe
   	wamp.reflection.error.describe

A peer that acts as a *Broker* SHOULD announce support for the reflection API by sending

   	HELLO.Details.roles.broker.reflection|bool := true

A peer that acts as a *Dealer* SHOULD announce support for the reflection API by sending

   	HELLO.Details.roles.dealer.reflection|bool := true

> Since *Brokers* might provide (broker) procedures and *Dealers* might provide (dealer) topics, both SHOULD implement the complete API above (even if the peer only implements one of *Broker* or *Dealer* roles).


## Appendix

### Predefined URIs

WAMP predefines the following URIs in the *advanced profile*. For URIs, used in *basic profile*, please, see appendix in basic profile specification.

#### Predefined Errors

*Dealer* or *Callee* canceled a call previously issued

	wamp.error.canceled

A *Peer* requested an interaction with an option that was disallowed by the *Router*

	wamp.error.option_not_allowed

A *Dealer* could not perform a call, since a procedure with the given URI is registered, but *Callee Black- and Whitelisting* and/or *Caller Exclusion* lead to the exclusion of (any) *Callee* providing the procedure.

	wamp.error.no_eligible_callee

A *Router* rejected client request to disclose its identity

	wamp.error.option_disallowed.disclose_me

### Authentication examples

#### Example 1

Client sends `HELLO` message:

```javascript
[
   1, 
   "com.tavendo.clandeck", 
   {
      "authmethods": [
         "cookie", 
         "anonymous"
      ], 
      "roles": {
         "callee": {
            "features": {
               "progressive_call_results": true
            }
         }, 
         "caller": {
            "features": {
               "caller_identification": true, 
               "progressive_call_results": true
            }
         }, 
         "publisher": {
            "features": {
               "publisher_exclusion": true, 
               "publisher_identification": true, 
               "subscriber_blackwhite_listing": true
            }
         }, 
         "subscriber": {
            "features": {
               "publisher_identification": true
            }
         }
      }
   }
]
```

Router sends `WELCOME` message:

```javascript
[
   2, 
   2134435219590102, 
   {
      "authid": "Z269J2NM6lWuB5UjxEH3cMHa", 
      "authmethod": "anonymous", 
      "authrole": "com.tavendo.community.role.anonymous", 
      "roles": {
         "broker": {
            "features": {
               "publisher_exclusion": true, 
               "publisher_identification": true, 
               "subscriber_blackwhite_listing": true
            }
         }, 
         "dealer": {
            "features": {
               "caller_identification": true, 
               "progressive_call_results": true
            }
         }
      }
   }
]
```

#### Example 2

Client sends `HELLO` message:

```javascript
[
   1, 
   "com.tavendo.clandeck", 
   {
      "authmethods": [
         "cookie", 
         "mozilla_persona"
      ], 
      "roles": {
         "callee": {
            "features": {
               "progressive_call_results": true
            }
         }, 
         "caller": {
            "features": {
               "caller_identification": true, 
               "progressive_call_results": true
            }
         }, 
         "publisher": {
            "features": {
               "publisher_exclusion": true, 
               "publisher_identification": true, 
               "subscriber_blackwhite_listing": true
            }
         }, 
         "subscriber": {
            "features": {
               "publisher_identification": true
            }
         }
      }
   }
]
```

Router sends `CHALLENGE` message:

```javascript
[
   4, 
   "mozilla-persona", 
   {}
]
```

Client sends `AUTHENTICATE` message:

```javascript
[
   5,  "eyJhbGciOiJSUzI1NiJ9.eyJwdWJsaWMta2V5Ijp7ImFsZ29yaXRobSI6IkRTIiwieSI6ImE5NzBiNzRmYWVmMWVlNzhhZjAzODk2MWZhMGEwMWZhMGM1NTgwY2RiNWZiNTc4YTkzNDIwMjQ4ZTllZWE1ZTIzYzNhOTU1MmZiYjExMTk0ZjVjNTc4NjE3N2Y5OGNkZWEzNzA0MDBmYThmZjJhMzNhMWNiOTdmYmM2ZDUyZjRmNzVjNjAxMmVjZDQ3YThiNWY2ZGRhMjk0MjhmMzZmMWJiM2UyZDM5MjUzM2E2YTY5ODFmMjE5NjAwM2FiNDA0NjgxNjcxMjNmMDI3NWZjMjYyMjBlNzliZGM2ZDQ1ZTkxOWU4MzdkZmQ4ZTQ5NjZkNDQzZDRlYzhjMjYxNDljYjIiLCJwIjoiZmY2MDA0ODNkYjZhYmZjNWI0NWVhYjc4NTk0YjM1MzNkNTUwZDlmMWJmMmE5OTJhN2E4ZGFhNmRjMzRmODA0NWFkNGU2ZTBjNDI5ZDMzNGVlZWFhZWZkN2UyM2Q0ODEwYmUwMGU0Y2MxNDkyY2JhMzI1YmE4MWZmMmQ1YTViMzA1YThkMTdlYjNiZjRhMDZhMzQ5ZDM5MmUwMGQzMjk3NDRhNTE3OTM4MDM0NGU4MmExOGM0NzkzMzQzOGY4OTFlMjJhZWVmODEyZDY5YzhmNzVlMzI2Y2I3MGVhMDAwYzNmNzc2ZGZkYmQ2MDQ2MzhjMmVmNzE3ZmMyNmQwMmUxNyIsInEiOiJlMjFlMDRmOTExZDFlZDc5OTEwMDhlY2FhYjNiZjc3NTk4NDMwOWMzIiwiZyI6ImM1MmE0YTBmZjNiN2U2MWZkZjE4NjdjZTg0MTM4MzY5YTYxNTRmNGFmYTkyOTY2ZTNjODI3ZTI1Y2ZhNmNmNTA4YjkwZTVkZTQxOWUxMzM3ZTA3YTJlOWUyYTNjZDVkZWE3MDRkMTc1ZjhlYmY2YWYzOTdkNjllMTEwYjk2YWZiMTdjN2EwMzI1OTMyOWU0ODI5YjBkMDNiYmM3ODk2YjE1YjRhZGU1M2UxMzA4NThjYzM0ZDk2MjY5YWE4OTA0MWY0MDkxMzZjNzI0MmEzODg5NWM5ZDViY2NhZDRmMzg5YWYxZDdhNGJkMTM5OGJkMDcyZGZmYTg5NjIzMzM5N2EifSwicHJpbmNpcGFsIjp7ImVtYWlsIjoidG9iaWFzLm9iZXJzdGVpbkBnbWFpbC5jb20ifSwiaWF0IjoxMzk5OTA4NzgyMzkwLCJleHAiOjEzOTk5MTIzOTIzOTAsImlzcyI6ImdtYWlsLmxvZ2luLnBlcnNvbmEub3JnIn0.eWg3M1prvcTiiaihzOvjdoZb_m01xs3MokNTeYOMHRflJFe-R526WdGP0wnFTgTXs5nwLId3eLBQr425v3ImoVKVuzJjpib_tT_O38xKEmmA4RBaiDRk_WKFXh1vDvEa2G70fb_cyxrisCoPgScs5df6DWse6-DVI3h4rPpXIQCk04rawblCErcd28lBK7aJ2EKV4PRJFSRg8h59DUDpg7J0N5VCrBXMdgXNs9_fifWJFsW9YeQx-1xHHJkXV-I8NIrV2hVSBwtns6R0uKbHTmgMgWPqCjs1v8gUW_yi---OFnR2g_eoxKyUOyTNHkspi0yxmW208Ayve1jQkzz5Kg~eyJhbGciOiJEUzEyOCJ9.eyJleHAiOjEzOTk5MDg5MTI5MTEsImF1ZCI6Imh0dHBzOi8vMTI3LjAuMC4xOjgwOTAifQ.kjwsBOIf-vrriJ1gfJ4Xqlj3MA15UiWI5wm4rpedBv4B3_LpvxJgGA", 
   {}
]
```

Router sends `WELCOME` message:

```javascript
[
   2, 
   1665486214880871, 
   {
      "authid": "tobias.oberstein@gmail.com", 
      "authmethod": "mozilla_persona", 
      "authrole": "com.tavendo.community.role.user", 
      "roles": {
         "broker": {
            "features": {
               "publisher_exclusion": true, 
               "publisher_identification": true, 
               "subscriber_blackwhite_listing": true
            }
         }, 
         "dealer": {
            "features": {
               "caller_identification": true, 
               "progressive_call_results": true
            }
         }
      }
   }
]
```

#### Example 3

Client sends `HELLO` message:

```javascript
[
   1, 
   "com.tavendo.clandeck", 
   {
      "authmethods": [
         "cookie", 
         "anonymous"
      ], 
      "roles": {
         "callee": {
            "features": {
               "progressive_call_results": true
            }
         }, 
         "caller": {
            "features": {
               "caller_identification": true, 
               "progressive_call_results": true
            }
         }, 
         "publisher": {
            "features": {
               "publisher_exclusion": true, 
               "publisher_identification": true, 
               "subscriber_blackwhite_listing": true
            }
         }, 
         "subscriber": {
            "features": {
               "publisher_identification": true
            }
         }
      }
   }
]
```

Router sends `WELCOME` message:

```javascript
[
   2, 
   7286787554810878, 
   {
      "authid": "tobias.oberstein@gmail.com", 
      "authmethod": "mozilla_persona", 
      "authrole": "com.tavendo.community.role.user", 
      "roles": {
         "broker": {
            "features": {
               "publisher_exclusion": true, 
               "publisher_identification": true, 
               "subscriber_blackwhite_listing": true
            }
         }, 
         "dealer": {
            "features": {
               "caller_identification": true, 
               "progressive_call_results": true
            }
         }
      }
   }
]
```
