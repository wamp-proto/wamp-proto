# WAMP Message Attributes: E2E Encryption & Router-to-Router Links

**Status**: Work in Progress
**Date**: 2025-01-14
**Context**: Analysis from autobahn-python test vector development

---

## Executive Summary

Analysis of all 25 WAMP message classes in Autobahn|Python reveals a **perfect architectural pattern** governing payload transparency and router forwarding attributes:

- **Payload transparency attributes** (`payload`, `enc_algo`, `enc_key`, `enc_serializer`) **ALWAYS co-occur** (never partial)
- **Two distinct attribute groups**:
  1. **Payload transparency group**: 4 attributes enabling E2E encryption
  2. **Router forwarding**: `forward_for` attribute enabling router-to-router links
- **Four clear categories** of WAMP messages based on these attribute groups
- **Zero exceptions**: Pattern holds perfectly across all 25 message types

This pattern is **not accidental** but reflects **deep architectural reasons** related to:
1. WAMP End-to-End Encryption (E2EE)
2. WAMP Router-to-Router Messaging (R-Links)

---

## Message Attribute Groups

### Group 1: Payload Transparency (E2E Encryption)

**Attributes** (always co-occur):
- `payload` (bytes) - Opaque application payload (not deserialized by router)
- `enc_algo` (str) - Encryption/encoding scheme identifier
- `enc_key` (str) - Key identifier
- `enc_serializer` (str) - Payload serializer identifier

**Purpose**: Enable End-to-End Encryption where:
- Application payload is encrypted by publisher/caller
- Router forwards payload as opaque bytes (no deserialization)
- Only subscriber/callee can decrypt payload
- Router cannot inspect application data

### Group 2: Router Forwarding (Router-to-Router Links)

**Attribute**:
- `forward_for` (list[dict]) - Forwarding chain metadata

**Purpose**: Enable Router-to-Router Links (R-Links) where:
- Messages are forwarded across multiple routers
- Forwarding chain is tracked
- Prevents loops and enables routing decisions
- Supports distributed WAMP fabrics

---

## The Four Categories

Analysis of all WAMP message classes reveals **exactly 4 categories**:

### Category 1: NEITHER Payload Transparency NOR forward_for (12 messages)

**Messages**: Session lifecycle and acknowledgments
- Abort, Authenticate, Challenge
- EventReceived
- Goodbye, Hello
- Published, Registered, Subscribed
- Unregistered, Unsubscribed
- Welcome

**Characteristics**:
- Local to router-client connection
- Never forwarded across router boundaries
- No application payload (or payload not encrytable)
- Session management only

**Why**: These messages establish, manage, or terminate sessions. They are **local** to a specific router-client connection and have no meaning across router boundaries.

### Category 2: Payload Transparency ONLY (0 messages)

**Messages**: NONE

**Why Category 2 is Empty**: Messages with application payload that needs encryption (payload transparency) **must also** support forwarding (`forward_for`) because:
- E2E encrypted payloads are meant to cross router boundaries
- Multi-router topologies are a primary use case for E2EE
- Encrypted messages must be routable in distributed fabrics

**Architectural Insight**: Payload transparency without router forwarding is **meaningless** - if you're encrypting end-to-end, you inherently need multi-hop routing.

### Category 3: forward_for ONLY (6 messages)

**Messages**: Control/management messages without application payload
- Cancel, Interrupt
- Register, Unregister
- Subscribe, Unsubscribe

**Characteristics**:
- Control plane operations
- No application payload to encrypt
- Must be forwarded across routers (R-Links)
- Carry metadata only (URIs, IDs, options)

**Why**: These messages manage subscriptions, registrations, and invocations across a distributed router fabric. They need `forward_for` to track routing but have no application payload to encrypt.

**Example**: A SUBSCRIBE message from Client A connected to Router 1 for a topic handled by Router 2:
```
Client A → Router 1 → Router 2
```
Router 1 forwards SUBSCRIBE to Router 2, adding itself to `forward_for`. When an EVENT comes back, Router 2 knows to send it to Router 1 (following the `forward_for` chain in reverse).

### Category 4: BOTH Payload Transparency AND forward_for (7 messages)

**Messages**: Application data plane - ALL messages carrying application payload
- **PubSub**: PUBLISH, EVENT
- **RPC**: CALL, RESULT, INVOCATION, YIELD
- **Errors**: ERROR (can carry payload in args/kwargs)

**Characteristics**:
- Carry application payload (args/kwargs or opaque bytes)
- Support E2E encryption (payload transparency)
- Can be routed across multiple routers (R-Links)
- The **only** messages users interact with for data exchange

**Why**: These messages are the **core data plane** of WAMP. They:
1. Carry user application data that may need encryption
2. Must traverse router-to-router links in distributed topologies
3. Require both E2EE and R-Link capabilities

**Example Use Case**: Encrypted RPC across routers
```
Client A → Router 1 → Router 2 → Client B
   (Caller)                        (Callee)

CALL: Encrypted payload via Router 1 and Router 2
- payload: encrypted args/kwargs
- enc_algo: "cryptobox"
- forward_for: [{router: "router1", ...}]

Router 1 cannot decrypt payload (E2EE)
Router 2 cannot decrypt payload (E2EE)
Only Client B (callee) can decrypt
```

---

## Attribute Co-occurrence Table

| Category | payload | enc_algo | enc_key | enc_serializer | forward_for | Count |
|----------|---------|----------|---------|----------------|-------------|-------|
| **1**    | ✗       | ✗        | ✗       | ✗              | ✗           | **12** |
| **2**    | ✓       | ✓        | ✓       | ✓              | ✗           | **0** ← Never occurs! |
| **3**    | ✗       | ✗        | ✗       | ✗              | ✓           | **6** |
| **4**    | ✓       | ✓        | ✓       | ✓              | ✓           | **7** |

**Key Observation**: The 4 payload transparency attributes **ALWAYS appear together** (never partially). This is enforced in Autobahn implementation and should be documented in WAMP spec.

---

## Deep Architectural Reasons

### 1. End-to-End Encryption (E2EE)

**Core Principle**: Only sender and receiver can access plaintext; routers see only opaque bytes.

**Requires**:
- `payload`: Opaque encrypted bytes (not deserialized by router)
- `enc_algo`: Scheme identifier (e.g., "cryptobox", "xbr")
- `enc_serializer`: Payload serializer (e.g., "msgpack", "cbor")
- `enc_key`: Key identifier for decryption

**Use Cases**:
- Financial transactions (sensitive data)
- Healthcare records (HIPAA compliance)
- Proprietary algorithms (IP protection)
- Multi-tenant systems (tenant isolation)

**Example Flow** (PUBLISH with E2EE):
```
Publisher:
  1. Serialize args/kwargs → msgpack bytes
  2. Encrypt bytes with shared key → encrypted payload
  3. Send PUBLISH with payload=<encrypted>, enc_algo="cryptobox"

Router:
  1. Receives PUBLISH
  2. Does NOT deserialize payload (opaque bytes)
  3. Validates WAMP metadata (options, topic)
  4. Routes to subscribers

Subscriber:
  1. Receives EVENT with payload=<encrypted>
  2. Decrypts payload using shared key
  3. Deserializes msgpack → original args/kwargs
```

### 2. Router-to-Router Links (R-Links)

**Core Principle**: WAMP routers form distributed fabrics; messages traverse multiple hops.

**Requires**:
- `forward_for`: List tracking routing chain

**Use Cases**:
- Geo-distributed deployments (multi-datacenter)
- Hierarchical routing (edge → regional → core)
- Federation (cross-organization)
- Scalability (horizontal router scaling)

**Example Flow** (CALL across 2 routers):
```
Caller (Client A) → Router 1 → Router 2 → Callee (Client B)

1. Client A sends CALL to Router 1
   forward_for: []

2. Router 1 forwards to Router 2
   forward_for: [{router: "router1", timestamp: ...}]

3. Router 2 sends INVOCATION to Client B
   forward_for: [{router: "router1", ...}, {router: "router2", ...}]

4. Client B sends YIELD to Router 2
   (forward_for indicates reverse path)

5. Router 2 forwards RESULT to Router 1
   (follows forward_for chain backward)

6. Router 1 forwards RESULT to Client A
```

### 3. Why E2EE and R-Links Must Coexist

**Architectural Necessity**: In distributed systems with E2EE:

1. **Multi-hop routing is essential**: Encrypted payloads MUST traverse router boundaries
   - If Alice (US) wants to send encrypted data to Bob (EU), message crosses routers
   - Router in US cannot decrypt
   - Router in EU cannot decrypt
   - Only Bob can decrypt

2. **Trust boundaries align**: E2EE creates trust boundaries that map to router boundaries
   - Routers are untrusted intermediaries
   - `forward_for` tracks the untrusted path
   - Payload remains encrypted throughout

3. **Use case overlap**: Scenarios requiring E2EE almost always involve multi-router topologies
   - Multi-tenant SaaS (tenant data encrypted, routed across infrastructure)
   - B2B integration (company A → routers → company B, encrypted payloads)
   - IoT edge-to-cloud (edge router → cloud router, sensor data encrypted)

**This is why Category 2 (E2EE without R-Links) is EMPTY**: The use cases don't exist!

---

## Message Classification by Category

### Category 1: Local Session Management (12 messages)

```
Session Lifecycle:
├── HELLO               - Client initiates session
├── WELCOME             - Router accepts session
├── ABORT               - Router rejects session
├── AUTHENTICATE        - Client provides auth credentials
├── CHALLENGE           - Router challenges client
└── GOODBYE             - Session termination

Acknowledgments:
├── PUBLISHED           - Publish acknowledged
├── SUBSCRIBED          - Subscribe confirmed
├── UNSUBSCRIBED        - Unsubscribe confirmed
├── REGISTERED          - Register confirmed
├── UNREGISTERED        - Unregister confirmed
└── EVENTRECEIVED       - Event delivery acknowledged
```

**Common Properties**:
- ✗ No `payload`, `enc_algo`, `enc_key`, `enc_serializer`
- ✗ No `forward_for`
- Local to specific router-client session
- Not routed across router boundaries

### Category 3: Control Plane (6 messages)

```
PubSub Control:
├── SUBSCRIBE           - Request subscription
└── UNSUBSCRIBE         - Cancel subscription

RPC Control:
├── REGISTER            - Register procedure
├── UNREGISTER          - Unregister procedure
├── CANCEL              - Cancel pending call
└── INTERRUPT           - Interrupt running invocation
```

**Common Properties**:
- ✗ No `payload`, `enc_algo`, `enc_key`, `enc_serializer` (no application payload)
- ✓ Has `forward_for` (routed across routers)
- Control plane operations
- Must traverse router boundaries in R-Link scenarios

### Category 4: Data Plane (7 messages)

```
PubSub Data:
├── PUBLISH             - Publish event (publisher → router)
└── EVENT               - Event delivery (router → subscriber)

RPC Data:
├── CALL                - Invoke procedure (caller → router)
├── INVOCATION          - Procedure invocation (router → callee)
├── YIELD               - Procedure result (callee → router)
└── RESULT              - Call result (router → caller)

Errors:
└── ERROR               - Error response (can carry payload)
```

**Common Properties**:
- ✓ Has `payload`, `enc_algo`, `enc_key`, `enc_serializer` (E2EE capable)
- ✓ Has `forward_for` (R-Link capable)
- Application data plane
- User-facing data exchange
- The ONLY messages carrying application payload

---

## Implementation Status

### Autobahn|Python (Reference Implementation)

**Attribute Names** (current):
- `enc_algo` - Scheme identifier
- `enc_serializer` - Serializer identifier
- `enc_key` - Key identifier
- `payload` - Opaque bytes

**Valid Values**:
- `enc_algo`: "null", "cryptobox", "mqtt", "xbr"
- `enc_serializer`: "null", "json", "msgpack", "cbor", "ubjson", "opaque", "flatbuffers"
- `enc_key`: (implementation-specific key ID)

**Code References**:
- `autobahn/wamp/message.py`: Message class definitions
- `autobahn/wamp/interfaces.py`: IPayloadCodec interface
- `autobahn/wamp/types.py`: EncodedPayload wrapper
- `autobahn/wamp/cryptobox.py`: Cryptobox E2EE implementation
- `autobahn/wamp/protocol.py`: Payload codec integration

### Crossbar.io (Router Implementation)

**Features**:
- Payload passthrough mode (router doesn't deserialize payload)
- Router-to-router links (R-Links with forward_for)
- Cryptobox E2EE support
- MQTT bridge (payload transparency for MQTT payloads)

**Code References**:
- `crossbar/router/broker.py`: PubSub payload transparency
- `crossbar/router/dealer.py`: RPC payload transparency
- `crossbar/worker/proxy.py`: R-Link forwarding
- `crossbar/bridge/mqtt/wamp.py`: MQTT payload transparency

### WAMP Specification (Draft)

**Section**: 14.1 Payload Passthru Mode

**Proposed Attribute Names** (spec draft):
- `ppt_scheme` ← maps to `enc_algo`
- `ppt_serializer` ← maps to `enc_serializer`
- `ppt_cipher` ← (not in Autobahn, hardcoded in cryptobox)
- `ppt_keyid` ← maps to `enc_key`

**Attribute Naming Mapping Table**:

| Autobahn Implementation | WAMP Spec 14.1 (Draft) | Description |
|-------------------------|------------------------|-------------|
| `enc_algo`              | `ppt_scheme`           | Encryption/encoding scheme identifier |
| `enc_serializer`        | `ppt_serializer`       | Payload serializer (json, msgpack, cbor, etc.) |
| `enc_key`               | `ppt_keyid`            | Key/credential identifier for decryption |
| (N/A - implicit)        | `ppt_cipher`           | Cipher algorithm (hardcoded in cryptobox) |
| `payload`               | `payload`              | Opaque encrypted/encoded bytes (same in both) |

**Valid Values**:
- `enc_algo` / `ppt_scheme`: `"null"`, `"cryptobox"`, `"mqtt"`, `"xbr"`
- `enc_serializer` / `ppt_serializer`: `"null"`, `"json"`, `"msgpack"`, `"cbor"`, `"ubjson"`, `"opaque"`, `"flatbuffers"`
- `ppt_cipher` (cryptobox only): `"xsalsa20poly1305"`, `"aes256gcm"` (hardcoded, not exposed in Autobahn)

**Status**:
- ⚠️ **Spec text not finalized**
- ⚠️ **Naming mismatch** between spec and implementation
- ⚠️ **Needs alignment** once spec finalized
- ✓ **Semantics aligned** (same concepts, different names)

**Issue**: Need to file issue to align Autobahn with final spec naming

---

## Implications for Test Vectors

### Test Coverage Requirements

**Category 4 messages** (data plane with E2EE + R-Link) need comprehensive test vectors:

1. **PUBLISH** ✅ (Complete - has normal + transparent payload samples)
2. **EVENT** ⚠️ (TODO)
3. **CALL** ⚠️ (TODO)
4. **RESULT** ⚠️ (TODO)
5. **INVOCATION** ⚠️ (TODO)
6. **YIELD** ⚠️ (TODO)
7. **ERROR** ⚠️ (TODO)

**Each test vector should include**:
- **Normal mode**: args/kwargs deserialized
- **Transparent mode**: payload as opaque bytes
- **E2EE metadata**: enc_algo, enc_serializer, enc_key
- **All serializers**: JSON, msgpack, CBOR, UBJSON
- **Validation**: Byte-for-byte payload preservation

### Naming in Test Vectors

**Strategy**:
- Use **Autobahn names** in implementation-specific code
- Document **spec name mapping** in notes
- Add clear comments explaining the relationship

**Example** (from PUBLISH test vector):
```json
{
  "notes": [
    "Attribute Naming: Autobahn vs WAMP Spec",
    "  Autobahn:     | WAMP Spec 14.1:",
    "  enc_algo      | ppt_scheme",
    "  enc_serializer| ppt_serializer",
    "  enc_key       | ppt_keyid",
    "  (N/A)         | ppt_cipher (hardcoded in cryptobox)"
  ]
}
```

---

## Key Takeaways

1. **Perfect Pattern**: Payload transparency attributes always co-occur (no partial sets)

2. **Four Categories**: Clear separation based on E2EE and R-Link requirements

3. **Category 2 is Empty**: E2EE without R-Links is architecturally meaningless

4. **7 Data Plane Messages**: Only these carry application payload and need both E2EE + R-Link

5. **Naming Divergence**: Implementation (Autobahn) and spec (draft) use different names

6. **Test Vector Priority**: Focus on Category 4 messages (data plane) for payload transparency testing

7. **Architectural Insight**: E2EE and R-Links are **co-dependent** features, not independent

---

## Next Steps

### Immediate (Test Vector Development)

- [x] Add naming notes to PUBLISH test vector
- [ ] Create test vectors for remaining Category 4 messages (EVENT, CALL, RESULT, INVOCATION, YIELD, ERROR)
- [ ] Document E2EE use cases in test vector examples
- [ ] Add R-Link (forward_for) samples to test vectors

### Short-term (Specification)

- [ ] File issue: Align Autobahn attribute names with WAMP spec once finalized
- [ ] Finalize WAMP spec 14.1 "Payload Passthru Mode" text
- [ ] Document the 4-category pattern in WAMP spec
- [ ] Add rationale for E2EE + R-Link co-dependency

### Long-term (Implementation)

- [ ] Ensure all Category 4 messages support payload transparency consistently
- [ ] Verify router behavior with E2EE payloads across R-Links
- [ ] Add conformance tests for payload transparency mode
- [ ] Document E2EE + R-Link interplay in architecture docs

---

## References

### Code Analysis

**Source**: `autobahn-python/autobahn/wamp/message.py`
**Date**: 2025-01-14
**Method**: Systematic analysis of all 25 Message subclasses
**Tool**: Python regex pattern matching on `__init__` signatures and docstrings

### Related Specifications

- [WAMP Spec - Advanced Profile](https://wamp-proto.org/wamp_latest_ietf.html)
- [WAMP Spec - Section 14.1: Payload Passthru Mode](https://wamp-proto.org/wamp_latest_ietf.html#name-payload-transparency) (Draft)
- [WAMP E2EE Proposal](https://github.com/wamp-proto/wamp-proto/issues/...) (TODO: add issue number)

### Implementation References

- [Autobahn|Python Documentation](https://autobahn.readthedocs.io/)
- [Crossbar.io Documentation](https://crossbar.io/docs/)
- [WAMP Cryptobox](https://github.com/crossbario/autobahn-python/tree/master/autobahn/wamp/cryptobox.py)

---

**Document Status**: Work in Progress
**Last Updated**: 2025-01-14
**Maintainer**: WAMP Protocol Development Team
**Feedback**: Please file issues at https://github.com/wamp-proto/wamp-proto/issues
