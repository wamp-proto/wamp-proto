-- move to: "ap_transport_webrtc.md" --

# WebRTC Transport

**WAMP-over-WebRTC** is a transport binding for WAMP that uses a WebRTC DataChannel for carrying WAMP messages.

WAMP-over-WebRTC allows establishing WAMP sessions over peer-to-peer, NAT-traversing, encrypted WebRTC connections while preserving the reliability and ordering guarantees required by the WAMP protocol.

Using WebRTC as a transport enables deployments in environments where direct TCP or WebSocket connectivity is restricted or unavailable, and additionally supports local, LAN, mobile, and browser-to-browser communication scenarios.

WAMP-over-WebRTC is active once a WebRTC DataChannel has been successfully negotiated and opened via standard WebRTC signaling mechanisms (SDP/ICE). The signaling process itself is out of scope for this specification. Once the DataChannel is open, peers exchange regular WAMP messages using the framing and rules defined in this document.

Each WAMP session uses exactly one WebRTC DataChannel for all message exchange.
No multiplexing of multiple WAMP sessions on a single DataChannel is permitted.

The DataChannel MUST be created with:

<ol>
<li>ordered = true</li>
<li>maxRetransmits = null</li>
<li>maxPacketLifeTime = null</li>
</ol>


This ensures a transport semantics equivalent to a reliable, ordered byte/message stream.

The establishment of the underlying WebRTC PeerConnection, including SDP negotiation, ICE gathering, and NAT traversal, is not described by this specification.
WAMP binds only to the resulting DataChannel once established.

**Message Framing**

WebRTC DataChannels provide message-oriented delivery of binary data.

In REQUIRED Framing Mode, one DataChannel Message per WAMP Message. Each WAMP message is serialized. The serialized payload is sent as a single DataChannel binary message. Message boundaries are preserved by the transport. If the WAMP message exceeds the DataChannel’s maximum message size, the transport MAY fragment and reassemble it transparently, but it MUST deliver whole WAMP messages to the session layer.

**Session Establishment**

A WAMP session begins when the DataChannel transitions to the `open` state. At this point, the transport becomes active, the WAMP HELLO message is sent by the session initiator. Normal WAMP session establishment proceeds (HELLO / WELCOME exchange). No additional transport-level handshake is performed. Whether a peer acts as a client or router is determined solely by the roles declared in the WAMP HELLO message, not by the WebRTC offer/answer direction.

**Message Size, Fragmentation, and Backpressure**

WebRTC DataChannels support messages up to 16 KB. WAMP messages larger than 16 KB MUST be fragmented into multiple DataChannel messages. Each fragment MUST include a single `final` flag indicating whether it is the last chunk. The receiver MUST reassemble fragments in order before delivering the complete message to the WAMP layer.
Use a message assembler that collects fragments until the final-flag fragment is received. Senders SHOULD monitor the DataChannel’s bufferedAmount and throttle sending when necessary to avoid memory pressure or transport overload.

**Session Closure**

#### Clean Closure

A clean shutdown consists of:

<ol>
<li>Exchange of WAMP GOODBYE messages.</li>
<li>Closure of the DataChannel by either side.</li>
</ol>


#### Abnormal Closure

If the DataChannel closes without an exchange of GOODBYE messages:
The WAMP session is considered aborted immediately. Pending requests are canceled. No further messages are exchanged. This mirrors the behavior of other WAMP transports such as RawSocket and WebSocket.
