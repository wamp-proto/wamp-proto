## RawSocket Transport {#rawsocket}

**WAMP-over-RawSocket** is an (alternative) transport for WAMP that uses length-prefixed, binary messages - a message framing different from WebSocket.

Compared to WAMP-over-WebSocket, WAMP-over-RawSocket is simple to implement, since there is no need to implement the WebSocket protocol which has some features that make it non-trivial (like a full HTTP-based opening handshake, message fragmentation, masking and variable length integers).

WAMP-over-RawSocket has even lower overhead than WebSocket, which can be desirable in particular when running on local connections like loopback TCP or Unix domain sockets. It is also expected to allow implementations in microcontrollers in under 2KB RAM.

WAMP-over-RawSocket can run over TCP, TLS, Unix domain sockets or any reliable streaming underlying transport. When run over TLS on the standard port for secure HTTPS (443), it is also able to traverse most locked down networking environments such as enterprise or mobile networks (unless man-in-the-middle TLS intercepting proxies are in use).

However, WAMP-over-RawSocket cannot be used with Web browser clients, since browsers do not allow raw TCP connections. Browser extensions would do, but those need to be installed in a browser. WAMP-over-RawSocket also (currently) does not support transport-level compression as WebSocket does provide (`permessage-deflate` WebSocket extension).

**Endianess**

WAMP-over-RawSocket uses *network byte order* ("big-endian"). That means, given a unsigned 32 bit integer

{align="left"}
        0x 11 22 33 44

the first octet sent out to (or received from) the wire is `0x11` and the last octet sent out (or received) is `0x44`.

Here is how you would convert octets received from the wire into an integer in Python:

{align="left"}
```python
import struct

octets_received = b"\x11\x22\x33\x44"
i = struct.unpack(">L", octets_received)[0]
```

The integer received has the value `287454020`.

And here is how you would send out an integer to the wire in Python:

{align="left"}
```python
octets_to_be_send = struct.pack(">L", i)
```

The octets to be sent are `b"\x11\x22\x33\x44"`.

**Handshake: Client-to-Router Request**

WAMP-over-RawSocket starts with a handshake where the client connecting to a router sends 4 octets:

{align="left"}
        MSB                                 LSB
        31                                    0
        0111 1111 LLLL SSSS RRRR RRRR RRRR RRRR

The *first octet* is a magic octet with value `0x7F`. This value is chosen to avoid any possible collision with the first octet of a valid HTTP request (see [here](http://www.w3.org/Protocols/rfc2616/rfc2616-sec5.html#sec5.1) and [here](http://www.w3.org/Protocols/rfc2616/rfc2616-sec2.html#sec2.2)). No valid HTTP request can have `0x7F` as its first octet.

> By using a magic first octet that cannot appear in a regular HTTP request, WAMP-over-RawSocket can be run e.g. on the same TCP listening port as WAMP-over-WebSocket or WAMP-over-LongPoll.

The *second octet* consists of a 4 bit `LENGTH` field and a 4 bit `SERIALIZER` field.

The `LENGTH` value is used by the *Client* to signal the **maximum message length** of messages it is willing to **receive**. When the handshake completes successfully, a *Router* MUST NOT send messages larger than this size.

The possible values for `LENGTH` are:

{align="left"}
         0: 2**9 octets
         1: 2**10 octets
        ...
        15: 2**24 octets

This means a *Client* can choose the maximum message length between **512** and **16M** octets.

The `SERIALIZER` value is used by the *Client* to request a specific serializer to be used. When the handshake completes successfully, the *Client* and *Router* will use the serializer requested by the *Client*.

The possible values for `SERIALIZER` are:

{align="left"}
        0: illegal
        1: JSON
        2: MessagePack
        3 - 15: reserved for future serializers

Here is a Python program that prints all (currently) permissible values for the *second octet*:

```python
SERMAP = {
    1: 'json',
    2: 'messagepack'
}

# map serializer / max. msg length to RawSocket handshake
# request or success reply (2nd octet)
for ser in SERMAP:
    for l in range(16):
        octet_2 = (l << 4) | ser
        print("serializer: {}, maxlen: {} => 0x{:02x}".format(SERMAP[ser], 2 ** (l + 9), octet_2))
```

The *third and forth octet* are **reserved** and MUST be all zeros for now.

**Handshake: Router-to-Client Reply**

After a *Client* has connected to a *Router*, the *Router* will first receive the 4 octets handshake request from the *Client*.

If the *first octet* differs from `0x7F`, it is not a WAMP-over-RawSocket request. Unless the *Router* also supports other transports on the connecting port (such as WebSocket or LongPoll), the *Router* MUST **fail the connection**.

Here is an example of how a *Router* could parse the *second octet* in a *Clients* handshake request:

{align="left"}
```python
# map RawSocket handshake request (2nd octet) to
# serializer / max. msg length
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

{align="left"}
        MSB                                 LSB
        31                                    0
        0111 1111 LLLL SSSS RRRR RRRR RRRR RRRR

Again, the *first octet* MUST be the value `0x7F`. The *third and forth octets* are reserved and MUST be all zeros for now.

In the *second octet*, the *Router* MUST echo the serializer value in `SERIALIZER` as requested by the *Client*.

Similar to the *Client*, the *Router* sets the `LENGTH` field to request a limit on the length of messages sent by the *Client*.

During the connection, *Router* MUST NOT send messages to the *Client* longer than the `LENGTH` requested by the *Client*, and the *Client* MUST NOT send messages larger than the maximum requested by the *Router* in its handshake reply.

If a message received during a connection exceeds the limit requested, a *Peer* MUST **fail the connection**.

When the *Router* is unable to speak the serializer requested by the *Client*, or it is denying the *Client* for other reasons, the *Router* replies with an error:

{align="left"}
        MSB                                 LSB
        31                                    0
        0111 1111 EEEE 0000 RRRR RRRR RRRR RRRR

An error reply has 4 octets: the *first octet* is again the magic `0x7F`, and the *third and forth octet* are reserved and MUST all be zeros for now.

The *second octet* has its lower 4 bits zero'ed (which distinguishes the reply from an success/accepting reply) and the upper 4 bits encode the error:

{align="left"}
        0: illegal (must not be used)
        1: serializer unsupported
        2: maximum message length unacceptable
        3: use of reserved bits (unsupported feature)
        4: maximum connection count reached
        5 - 15: reserved for future errors

> Note that the error code `0` MUST NOT be used. This is to allow storage of error state in a host language variable, while allowing `0` to signal the current state "no error"

Here is an example of how a *Router* might create the *second octet* in an error response:

{align="left"}
```python
ERRMAP = {
    0: "illegal (must not be used)",
    1: "serializer unsupported",
    2: "maximum message length unacceptable",
    3: "use of reserved bits (unsupported feature)",
    4: "maximum connection count reached"
}

# map error to RawSocket handshake error reply (2nd octet)
for err in ERRMAP:
    octet_2 = err << 4
    print("error: {} => 0x{:02x}").format(ERRMAP[err], err)
```

The *Client* - after having sent its handshake request - will wait for the 4 octets from *Router* handshake reply.

Here is an example of how a *Client* might parse the *second octet* in a *Router* handshake reply:

{align="left"}
```python
# map RawSocket handshake reply (2nd octet)
for i in range(256):
    ser_id = i & 0x0f
    if ser_id:
        # verify the serializer is the one we requested!
        # if not, fail the connection!
        ser = SERMAP.get(ser_id, 'currently undefined')
        maxlen = 2 ** ((i >> 4) + 9)
        print("{:02x} => serializer: {}, maxlen: {}".format(i, ser, maxlen))
    else:
        err = i >> 4
        print("error: {}".format(ERRMAP.get(err, 'currently undefined')))
```

**Serialization**

To send a WAMP message, the message is serialized according to the WAMP serializer agreed in the handshake (e.g. JSON or MessagePack).

The length of the serialized messages in octets MUST NOT exceed the maximum requested by the *Peer*.

If the serialized length exceed the maximum requested, the WAMP message can not be sent to the *Peer*. Handling situations like the latter is left to the implementation.

E.g. a *Router* that is to forward a WAMP `EVENT` to a *Client* which exceeds the maximum length requested by the *Client* when serialized might:

* drop the event (not forwarding to that specific client) and track dropped events
* prohibit publishing to the topic already
* remove the event payload, and send an event with extra information (`payload_limit_exceeded = true`)


**Framing**

The serialized octets for a message to be sent are prefixed with exactly 4 octets.

{align="left"}
        MSB                                 LSB
        31                                    0
        RRRR RTTT LLLL LLLL LLLL LLLL LLLL LLLL

The *first octet* has the following structure

{align="left"}
        MSB   LSB
        7       0
        RRRR RTTT

The five bits `RRRRR` are reserved for future use and MUST be all zeros for now.

The three bits `TTT` encode the type of the transport message:

{align="left"}
        0: regular WAMP message
        1: PING
        2: PONG
        3-7: reserved

The *three remaining octets* constitute an unsigned 24 bit integer that provides the length of transport message payload following, excluding the 4 octets that constitute the prefix.

For a regular WAMP message (`TTT == 0`), the length is the length of the serialized WAMP message: the number of octets after serialization (excluding the 4 octets of the prefix).

For a `PING` message (`TTT == 1`), the length is the length of the arbitrary payload that follows. A *Peer* MUST reply to each `PING` by sending exactly one `PONG` immediately, and the `PONG` MUST echo back the payload of the `PING` exactly.

For receiving messages with WAMP-over-RawSocket, a *Peer* will usually read exactly 4 octets from the incoming stream, decode the transport level message type and payload length, and then receive as many octets as the length was giving.

When the transport level message type indicates a regular WAMP message, the transport level message payload is unserialized according to the serializer agreed in the handshake and the processed at the WAMP level.
