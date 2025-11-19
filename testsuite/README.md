# WAMP Test Vectors / Conformance Test Suite

This directory contains machine-readable test vectors for validating WAMP protocol implementations. The test suite enables automated conformance testing, interoperability validation, and regression prevention across WAMP implementations.

## Overview

**Test vectors** are canonical examples of WAMP messages and interaction sequences that implementations can use to validate correctness. Each test vector specifies:

- The serialized bytes representation (in multiple formats)
- The expected deserialized attributes
- Validation criteria
- Specification references

## Directory Structure

```
testsuite/
├── README.md                    # This file
├── SCHEMA.json                  # JSON Schema for test vector format
│
├── singlemessage/               # Individual WAMP message serialization tests
│   ├── basic/                   # Basic Profile messages
│   │   ├── hello.json
│   │   ├── welcome.json
│   │   ├── abort.json
│   │   ├── goodbye.json
│   │   ├── error.json
│   │   ├── publish.json
│   │   ├── published.json
│   │   ├── subscribe.json
│   │   ├── subscribed.json
│   │   ├── unsubscribe.json
│   │   ├── unsubscribed.json
│   │   ├── event.json
│   │   ├── call.json
│   │   ├── result.json
│   │   ├── register.json
│   │   ├── registered.json
│   │   ├── unregister.json
│   │   ├── unregistered.json
│   │   ├── invocation.json
│   │   └── yield.json
│   │
│   └── advanced/                # Advanced Profile features
│       ├── publisher_identification.json
│       ├── publisher_exclusion.json
│       ├── publisher_inclusion.json
│       ├── subscriber_blacklisting.json
│       ├── subscriber_whitelisting.json
│       ├── pattern_based_subscription.json
│       ├── progressive_call_results.json
│       ├── caller_identification.json
│       ├── shared_registration.json
│       ├── payload_passthru.json
│       └── ...
│
├── singlesession/               # Single client session interaction sequences
│   ├── basic/
│   │   ├── session_establishment.json      # HELLO → WELCOME
│   │   ├── subscribe_and_event.json        # SUBSCRIBE → SUBSCRIBED → EVENT
│   │   ├── call_and_result.json            # CALL → RESULT
│   │   └── session_close.json              # GOODBYE → GOODBYE
│   │
│   └── advanced/
│       ├── progressive_results.json        # CALL → RESULT (progress) → RESULT (final)
│       ├── authenticated_session.json      # HELLO → CHALLENGE → AUTHENTICATE → WELCOME
│       └── ...
│
├── multisession/                # Multiple client sessions (requires router)
│   ├── basic/
│   │   ├── pubsub_basic.json              # Publisher publishes, subscriber receives
│   │   ├── rpc_basic.json                 # Caller invokes, callee receives and yields
│   │   └── ...
│   │
│   └── advanced/
│       ├── publisher_exclusion_enabled.json   # Publisher does NOT receive own EVENT
│       ├── publisher_exclusion_disabled.json  # Publisher DOES receive own EVENT
│       ├── subscriber_whitelist.json          # Only whitelisted subscribers receive EVENT
│       └── ...
│
└── multirouter/                 # Multiple routers (federation, clustering)
    ├── router_to_router_link.json
    └── ...
```

## Test Vector Levels

### Level 1: Single Message (`singlemessage/`)

Tests individual WAMP message serialization and deserialization.

**Purpose**:
- Validate that implementations correctly serialize/deserialize each WAMP message type
- Ensure attribute preservation (WAMP metadata and application payload)
- Test across multiple serialization formats (JSON, MessagePack, CBOR, etc.)

**Test Pattern**:
```
bytes → deserialize() → Message Object → validate attributes
Message Object → serialize() → bytes → compare to canonical
```

**Example**: `singlemessage/basic/event.json` validates EVENT message structure

### Level 2: Single Session (`singlesession/`)

Tests WAMP message sequences within a single client session.

**Purpose**:
- Validate correct message ordering and state transitions
- Test request/response pairing (request_id matching)
- Ensure session lifecycle handling

**Test Pattern**:
```
Session State → Message In → Process → Expected State → Message Out
```

**Example**: `singlesession/basic/subscribe_and_event.json` validates SUBSCRIBE → SUBSCRIBED → EVENT sequence

### Level 3: Multi-Session (`multisession/`)

Tests interactions between multiple client sessions through a router.

**Purpose**:
- Validate router behavior (message routing, filtering, transformation)
- Test advanced features requiring coordination (publisher exclusion, whitelisting, etc.)
- Ensure correct multi-party semantics

**Test Pattern**:
```
Session A → Message → Router → Process/Route → Message → Session B
                              → Validate routing logic
```

**Example**: `multisession/advanced/publisher_exclusion_disabled.json` validates that publisher receives EVENT when `exclude_me=false`

### Level 4: Multi-Router (`multirouter/`)

Tests router-to-router interactions (federation, clustering).

**Purpose**:
- Validate router federation protocols
- Test cross-realm routing
- Ensure clustering behavior

**Status**: Future - not yet implemented

## Test Vector Format

### Single Message Test Vector

```json
{
  "description": "EVENT message with publisher identification",
  "wamp_message_type": "EVENT",
  "wamp_message_code": 36,
  "feature": "advanced.pubsub.publisher_identification",
  "spec_reference": "https://wamp-proto.org/wamp_latest_ietf.html#name-publisher-identification",

  "samples": [
    {
      "description": "EVENT with publisher identification in Details",

      "serializers": {
        "json": [
          {
            "bytes": "[36, 5512315355, 4429313566, {\"publisher\": 1234}, [], {\"color\": \"orange\"}]",
            "bytes_hex": "5b33362c20353531323331353335352c20343432393331333536362c207b227075626c6973686572223a20313233347d2c205b5d2c207b22636f6c6f72223a20226f72616e6765227d5d"
          }
        ],
        "msgpack": [
          {
            "bytes_hex": "96241a208f8165214a0036e1be81a97075626c697368657219cd04d280a5636f6c6f72a66f72616e6765"
          }
        ]
      },

      "expected_attributes": {
        "message_type": 36,
        "subscription_id": 5512315355,
        "publication_id": 4429313566,
        "details": {
          "publisher": 1234
        },
        "args": [],
        "kwargs": {
          "color": "orange"
        }
      },

      "validation": {
        "autobahn-python": [
          "from autobahn.wamp.message import Event\n\n# Test framework provides 'msg' with deserialized message\nassert isinstance(msg, Event)\nassert msg.subscription == 5512315355\nassert msg.publication == 4429313566\nassert msg.publisher == 1234\nassert msg.kwargs['color'] == 'orange'\n"
        ],
        "autobahn-js": [
          "// Test framework provides 'msg' with deserialized message\nassert(msg.type === 36);\nassert(msg.subscription === 5512315355);\nassert(msg.publication === 4429313566);\nassert(msg.details.publisher === 1234);\nassert(msg.kwargs.color === 'orange');\n"
        ],
        "wampy": [
          "// Wampy.js uses different message structure\nassert(msg.options.subscription === 5512315355);\nassert(msg.options.publication === 4429313566);\nassert(msg.options.publisher === 1234);\nassert(msg.color === 'orange');\n"
        ]
      },

      "construction": {
        "autobahn-python": "from autobahn.wamp.message import Event\n\nmsg = Event(\n    subscription=5512315355,\n    publication=4429313566,\n    publisher=1234,\n    kwargs={'color': 'orange'}\n)\n"
      }
    }
  ],

  "notes": [
    "Publisher identification must be explicitly enabled in subscription options",
    "The publisher field in Details is the WAMP session ID of the publisher"
  ]
}
```

### Multi-Message Sequence Test Vector

```json
{
  "description": "Publisher exclusion disabled - publisher receives own EVENT",
  "feature": "advanced.pubsub.publisher_exclusion",
  "spec_reference": "https://wamp-proto.org/wamp_latest_ietf.html#name-publisher-exclusion",

  "sessions": [
    {
      "session_id": "session_1",
      "roles": ["publisher", "subscriber"]
    }
  ],

  "sequence": [
    {
      "step": 1,
      "description": "Client subscribes to topic",
      "from": "session_1",
      "to": "router",
      "message": {
        "type": "SUBSCRIBE",
        "request_id": 123,
        "options": {},
        "topic": "com.myapp.topic1"
      }
    },
    {
      "step": 2,
      "description": "Router confirms subscription",
      "from": "router",
      "to": "session_1",
      "message": {
        "type": "SUBSCRIBED",
        "request_id": 123,
        "subscription_id": 456
      }
    },
    {
      "step": 3,
      "description": "Client publishes with exclude_me=false",
      "from": "session_1",
      "to": "router",
      "message": {
        "type": "PUBLISH",
        "request_id": 789,
        "options": {
          "exclude_me": false
        },
        "topic": "com.myapp.topic1",
        "args": ["Hello, world!"]
      }
    },
    {
      "step": 4,
      "description": "Publisher receives EVENT because exclude_me=false",
      "from": "router",
      "to": "session_1",
      "message": {
        "type": "EVENT",
        "subscription_id": 456,
        "publication_id": 999,
        "details": {},
        "args": ["Hello, world!"]
      },
      "assertion": "Publisher MUST receive EVENT when exclude_me=false"
    }
  ],

  "expected_outcome": {
    "session_1_receives_event": true,
    "reason": "exclude_me option was explicitly set to false"
  }
}
```

## Schema Design and Reasoning

### Non-Bijective Serialization

A fundamental principle underlying the test vector schema is that **serialization is not bijective** (except for bencode). This means:

- **One abstract message → Many valid byte representations** (serialization is one-to-many)
- **One byte sequence → One abstract message** (deserialization is one-to-one)

**Example**: JSON serialization variations for the same PUBLISH message:

```json
[16, 239714735, {}, "com.myapp.mytopic1", ["Hello, world!"]]
[16,239714735,{},"com.myapp.mytopic1",["Hello, world!"]]
```

Both are valid JSON representing the identical WAMP message. They differ only in whitespace formatting. Other variations include:

- **JSON**: Whitespace (spaces, newlines, indentation), object key ordering
- **MessagePack**: Integer encoding width (fixint vs uint8 vs uint16 vs uint32), map key ordering
- **CBOR**: Integer encoding width, definite vs indefinite length arrays/maps, canonical ordering

### Multiple Valid Byte Representations

To handle non-bijective serialization, test vectors use **array-of-variants** for each serializer:

```json
{
  "serializers": {
    "json": [
      {
        "bytes": "[16, 239714735, {}, \"com.myapp.mytopic1\", [\"Hello, world!\"]]",
        "bytes_hex": "5b31362c203233393731343733352c207b7d2c2022636f6d2e6d796170702e6d79746f70696331222c205b2248656c6c6f2c20776f726c6421225d5d",
        "note": "With spaces after commas (readable)"
      },
      {
        "bytes": "[16,239714735,{},\"com.myapp.mytopic1\",[\"Hello, world!\"]]",
        "bytes_hex": "5b31362c3233393731343733352c7b7d2c22636f6d2e6d796170702e6d79746f70696331222c5b2248656c6c6f2c20776f726c6421225d5d",
        "note": "Compact (no spaces) - autobahn-python"
      }
    ]
  }
}
```

This array structure allows documenting multiple canonical byte representations for the same abstract message.

### "At Least One" Matching Semantics

Implementations must follow **"at least one" matching semantics**:

**For Serialization** (Message → Bytes):
- An implementation's serialized bytes MUST match **at least one** of the byte variants in the test vector
- Implementations MAY produce any of the documented variants
- Implementations MAY produce other valid representations not yet documented (contributors should add these as new variants)

**For Deserialization** (Bytes → Message):
- An implementation MUST successfully deserialize **all** byte variants to the same abstract message
- All variants MUST produce identical attribute values
- Deserialized message MUST validate against **at least one** validation code block

**Example Test Logic**:

```python
# Serialization: Check if output matches ANY variant
def test_serialize(msg, serializer, expected_variants):
    actual_bytes = serializer.serialize(msg)
    assert any(actual_bytes == variant['bytes'] for variant in expected_variants)

# Deserialization: Check that ALL variants deserialize successfully
def test_deserialize(serializer, expected_variants, validation_codes):
    for variant in expected_variants:
        msg = serializer.deserialize(variant['bytes'])
        # Must validate with at least one validation code
        assert any(validate(msg, code) for code in validation_codes)
```

### Multiple Samples Per Test Vector

Each test vector file can contain **multiple samples** demonstrating different variations of the message type:

```json
{
  "description": "PUBLISH message variants",
  "wamp_message_type": "PUBLISH",
  "samples": [
    {
      "description": "PUBLISH with positional args only",
      "serializers": { ... },
      "expected_attributes": { ... }
    },
    {
      "description": "PUBLISH with keyword args only",
      "serializers": { ... },
      "expected_attributes": { ... }
    },
    {
      "description": "PUBLISH with both positional and keyword args",
      "serializers": { ... },
      "expected_attributes": { ... }
    },
    {
      "description": "PUBLISH with transparent payload (passthru mode)",
      "serializers": { ... },
      "expected_attributes": { ... }
    }
  ]
}
```

**Why Multiple Samples?**

1. **Coverage**: Different code paths (args only vs kwargs only vs both vs payload)
2. **Edge Cases**: Empty args, null values, nested structures
3. **Features**: Basic vs advanced profile options
4. **Modes**: Normal payload vs transparent payload
5. **Pedagogy**: Examples for different use cases

### Multiple WAMP Implementation Support

Test vectors are **implementation-agnostic** but provide **implementation-specific** validation and construction code:

```json
{
  "validation": {
    "autobahn-python": [
      "from autobahn.wamp.message import Publish\nassert isinstance(msg, Publish)\nassert msg.request == 239714735"
    ],
    "autobahn-js": [
      "assert(msg instanceof wamp.Publish);\nassert(msg.request === 239714735);"
    ],
    "wampy": [
      "from wampy.messages.publish import Publish\nassert isinstance(msg, Publish)\nassert msg.request_id == 239714735"
    ]
  },

  "construction": {
    "autobahn-python": "from autobahn.wamp.message import Publish\nmsg = Publish(request=239714735, topic='com.myapp.mytopic1', args=['Hello, world!'])",
    "autobahn-js": "const msg = new wamp.Publish(239714735, {}, 'com.myapp.mytopic1', ['Hello, world!']);",
    "wampy": "from wampy.messages.publish import Publish\nmsg = Publish(request_id=239714735, topic='com.myapp.mytopic1', args=['Hello, world!'])"
  }
}
```

**Why Implementation-Specific Code?**

1. **Different APIs**: Each library has its own message class hierarchy and attribute names
2. **Multiple Validation Approaches**: Different implementations may validate differently (all must be correct)
3. **Runnable Tests**: Code blocks can be `exec()`'ed directly in test frameworks
4. **Documentation**: Shows implementers exactly how to use their library correctly

**Key**: Use implementation names (e.g., `autobahn-python`, `autobahn-js`, `wampy`, `nexus-go`), not language names (e.g., `python`, `javascript`), because:
- Multiple implementations exist per language
- APIs differ significantly between implementations
- Version-specific behavior may need different code blocks

### Design Principles Summary

1. **Non-Bijective Reality**: Acknowledge that serialization produces multiple valid outputs
2. **Array-of-Variants**: Document all known valid byte representations
3. **At-Least-One Semantics**: Flexible matching for serialization, strict for deserialization
4. **Multiple Samples**: Comprehensive coverage within each message type
5. **Implementation-Specific**: Executable code blocks for each WAMP implementation
6. **Machine-Readable**: JSON format enables automated test generation
7. **Human-Readable**: Clear descriptions, notes, and spec references
8. **Version-Controllable**: Git-friendly format for tracking changes
9. **Extensible**: Easy to add new serializers, implementations, samples

## Usage

### For Client Library Developers

Validate that your WAMP client library correctly serializes and deserializes messages:

```python
import json
from my_wamp_library import serializer

# Load test vector
with open('testsuite/singlemessage/basic/event.json') as f:
    test_vector = json.load(f)

# Test deserialization
json_serializer = serializer.JsonSerializer()
bytes_data = test_vector['serializers']['json']['bytes'].encode('utf-8')
msg = json_serializer.deserialize(bytes_data)

# Validate attributes
expected = test_vector['expected_attributes']
assert msg.subscription == expected['subscription_id']
assert msg.publication == expected['publication_id']
assert msg.kwargs == expected['kwargs']

# Test serialization (roundtrip)
serialized = json_serializer.serialize(msg)
msg2 = json_serializer.deserialize(serialized)
assert msg == msg2
```

### For Router Developers

Validate that your WAMP router implements correct routing semantics:

```python
import json

# Load multi-session test vector
with open('testsuite/multisession/advanced/publisher_exclusion_disabled.json') as f:
    test_vector = json.load(f)

# Simulate the message sequence
for step in test_vector['sequence']:
    if step['from'] != 'router':
        # Process incoming message from client
        router.process_message(
            session_id=step['from'],
            message=step['message']
        )
    else:
        # Verify router sends expected message
        sent_msg = router.get_next_outgoing_message(step['to'])
        assert sent_msg == step['message']

# Verify expected outcome
outcome = test_vector['expected_outcome']
assert outcome['session_1_receives_event'] == True
```

## Serialization Formats

Test vectors include byte representations in multiple serialization formats:

- **JSON** - Human-readable, widely supported
- **MessagePack** - Binary, compact, efficient
- **CBOR** - Binary, extensible, standard
- **UBJSON** - Universal Binary JSON (optional)

Not all test vectors include all formats. At minimum, JSON representation is provided.

## Validation Rules

Implementations should validate:

### Message Structure
- ✅ Message type code matches specification
- ✅ Required fields present
- ✅ Optional fields handled correctly
- ✅ Field types match specification

### Attribute Preservation
- ✅ All WAMP metadata preserved (Options, Details, etc.)
- ✅ Application payload preserved (args, kwargs)
- ✅ Binary data preserved byte-for-byte
- ✅ Special values handled (null, empty arrays, nested structures)

### Roundtrip Consistency
- ✅ Deserialize → Serialize → Deserialize yields identical object
- ✅ Attribute equality across serialization formats
- ✅ No data loss or corruption

### Semantic Correctness
- ✅ Request/response ID matching
- ✅ State transitions follow specification
- ✅ Routing logic matches specification
- ✅ Error conditions handled correctly

## Contributing

To contribute new test vectors:

1. Follow the JSON format specified in `SCHEMA.json`
2. Include at least JSON serialization
3. Provide clear description and spec reference
4. Add validation assertions
5. Test against at least one implementation
6. Submit pull request with documentation

## References

- [WAMP Specification](https://wamp-proto.org/wamp_latest_ietf.html)
- [GitHub Issue #556](https://github.com/wamp-proto/wamp-proto/issues/556) - Test Vector Proposal
- [GitHub PR #557](https://github.com/wamp-proto/wamp-proto/pull/557) - Test Vector Implementation

## License

The WAMP test vectors are part of the WAMP specification and follow the same licensing terms.
