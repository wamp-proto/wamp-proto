### Message Batching {#batchedwebsocket}

*WAMP-over-Batched-WebSocket* is a variant of WAMP-over-WebSocket where multiple WAMP messages are sent in one WebSocket message.

Using WAMP message batching can increase wire level efficiency further. In particular when using TLS and the WebSocket implementation is forcing every WebSocket message into a new TLS segment.

WAMP-over-Batched-WebSocket is negotiated between Peers in the WebSocket opening handshake by agreeing on one of the following WebSocket subprotocols:

* `wamp.2.json.batched`
* `wamp.2.msgpack.batched`

Batching with JSON works by serializing each WAMP message to JSON as normally, appending the single ASCII control character `\30` ([record separator](http://en.wikipedia.org/wiki/Record_separator#Field_separators)) octet `0x1e` to *each* serialized messages, and packing a sequence of such serialized messages into a single WebSocket message:

{align="left"}
        Serialized JSON WAMP Msg 1 | 0x1e |
            Serialized JSON WAMP Msg 2 | 0x1e | ...

Batching with MessagePack works by serializing each WAMP message to MessagePack as normally, prepending a 32 bit unsigned integer (4 octets in big-endian byte order) with the length of the serialized MessagePack message (excluding the 4 octets for the length prefix), and packing a sequence of such serialized (length-prefixed) messages into a single WebSocket message:

{align="left"}
        Length of Msg 1 serialization (uint32) |
            serialized MessagePack WAMP Msg 1 | ...

With batched transport, even if only a single WAMP message is to be sent in a WebSocket message, the (single) WAMP message needs to be framed as described above. In other words, a single WAMP message is sent as a batch of length **1**. Sending a batch of length **0** (no WAMP message) is illegal and a *Peer* MUST fail the transport upon receiving such a transport message.
