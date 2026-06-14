#!/usr/bin/env python3
"""
Generate PUBLISH.Options and EVENT.Details validation samples for testsuite.
Outputs JSON samples that can be added to publish.json and event.json.
"""
import json
import sys

def generate_publish_options_samples():
    """Generate all PUBLISH.Options validation samples"""
    samples = []

    # exclude_authid
    samples.extend([
        {
            "description": "PUBLISH.Options.exclude_authid empty list (valid)",
            "test_category": "options_validation",
            "wmsg": [16, 123, {"exclude_authid": []}, "com.example.topic"]
        },
        {
            "description": "PUBLISH.Options.exclude_authid with authids (valid)",
            "test_category": "options_validation",
            "wmsg": [16, 123, {"exclude_authid": ["alice", "bob"]}, "com.example.topic"]
        },
        {
            "description": "PUBLISH.Options.exclude_authid with invalid type string",
            "test_category": "options_validation",
            "wmsg": [16, 123, {"exclude_authid": "hello"}, "com.example.topic"],
            "expected_error": {"type": "protocol_violation", "contains": "exclude_authid"}
        },
        {
            "description": "PUBLISH.Options.exclude_authid with invalid item type int",
            "test_category": "options_validation",
            "wmsg": [16, 123, {"exclude_authid": [123]}, "com.example.topic"],
            "expected_error": {"type": "protocol_violation", "contains": "exclude_authid"}
        },
    ])

    # exclude_authrole
    samples.extend([
        {
            "description": "PUBLISH.Options.exclude_authrole with roles (valid)",
            "test_category": "options_validation",
            "wmsg": [16, 123, {"exclude_authrole": ["manager", "staff"]}, "com.example.topic"]
        },
        {
            "description": "PUBLISH.Options.exclude_authrole with invalid type string",
            "test_category": "options_validation",
            "wmsg": [16, 123, {"exclude_authrole": "manager"}, "com.example.topic"],
            "expected_error": {"type": "protocol_violation", "contains": "exclude_authrole"}
        },
    ])

    # eligible
    samples.extend([
        {
            "description": "PUBLISH.Options.eligible empty list (valid)",
            "test_category": "options_validation",
            "wmsg": [16, 123, {"eligible": []}, "com.example.topic"]
        },
        {
            "description": "PUBLISH.Options.eligible with session IDs (valid)",
            "test_category": "options_validation",
            "wmsg": [16, 123, {"eligible": [123, 456]}, "com.example.topic"]
        },
        {
            "description": "PUBLISH.Options.eligible with invalid type string",
            "test_category": "options_validation",
            "wmsg": [16, 123, {"eligible": "hello"}, "com.example.topic"],
            "expected_error": {"type": "protocol_violation", "contains": "eligible"}
        },
    ])

    # eligible_authid
    samples.extend([
        {
            "description": "PUBLISH.Options.eligible_authid with authids (valid)",
            "test_category": "options_validation",
            "wmsg": [16, 123, {"eligible_authid": ["alice"]}, "com.example.topic"]
        },
        {
            "description": "PUBLISH.Options.eligible_authid with invalid type int",
            "test_category": "options_validation",
            "wmsg": [16, 123, {"eligible_authid": 123}, "com.example.topic"],
            "expected_error": {"type": "protocol_violation", "contains": "eligible_authid"}
        },
    ])

    # eligible_authrole
    samples.extend([
        {
            "description": "PUBLISH.Options.eligible_authrole with roles (valid)",
            "test_category": "options_validation",
            "wmsg": [16, 123, {"eligible_authrole": ["manager"]}, "com.example.topic"]
        },
        {
            "description": "PUBLISH.Options.eligible_authrole with invalid item type int",
            "test_category": "options_validation",
            "wmsg": [16, 123, {"eligible_authrole": [123]}, "com.example.topic"],
            "expected_error": {"type": "protocol_violation", "contains": "eligible_authrole"}
        },
    ])

    # retain
    samples.extend([
        {
            "description": "PUBLISH.Options.retain with value true (valid)",
            "test_category": "options_validation",
            "wmsg": [16, 123, {"retain": True}, "com.example.topic"]
        },
        {
            "description": "PUBLISH.Options.retain with value false (valid)",
            "test_category": "options_validation",
            "wmsg": [16, 123, {"retain": False}, "com.example.topic"]
        },
        {
            "description": "PUBLISH.Options.retain with invalid type string",
            "test_category": "options_validation",
            "wmsg": [16, 123, {"retain": "hello"}, "com.example.topic"],
            "expected_error": {"type": "protocol_violation", "contains": "retain"}
        },
    ])

    # transaction_hash
    samples.extend([
        {
            "description": "PUBLISH.Options.transaction_hash with value (valid)",
            "test_category": "options_validation",
            "wmsg": [16, 123, {"transaction_hash": "abc123"}, "com.example.topic"]
        },
        {
            "description": "PUBLISH.Options.transaction_hash with invalid type int",
            "test_category": "options_validation",
            "wmsg": [16, 123, {"transaction_hash": 123}, "com.example.topic"],
            "expected_error": {"type": "protocol_violation", "contains": "transaction_hash"}
        },
    ])

    # forward_for
    samples.extend([
        {
            "description": "PUBLISH.Options.forward_for empty list (valid)",
            "test_category": "options_validation",
            "wmsg": [16, 123, {"forward_for": []}, "com.example.topic"]
        },
        {
            "description": "PUBLISH.Options.forward_for with router info (valid)",
            "test_category": "options_validation",
            "wmsg": [16, 123, {"forward_for": [{"session": 123, "authid": "router1", "authrole": "router"}]}, "com.example.topic"]
        },
        {
            "description": "PUBLISH.Options.forward_for with invalid type string",
            "test_category": "options_validation",
            "wmsg": [16, 123, {"forward_for": "hello"}, "com.example.topic"],
            "expected_error": {"type": "protocol_violation", "contains": "forward_for"}
        },
    ])

    # E2EE options (only valid with transparent payload)
    payload_hex = "a1666e6f74696365"
    samples.extend([
        {
            "description": "PUBLISH.Options.enc_algo cryptobox (valid with payload)",
            "test_category": "options_validation",
            "wmsg": [16, 123, {"enc_algo": "cryptobox"}, "com.example.topic", payload_hex]
        },
        {
            "description": "PUBLISH.Options.enc_algo with invalid value",
            "test_category": "options_validation",
            "wmsg": [16, 123, {"enc_algo": "invalid"}, "com.example.topic", payload_hex],
            "expected_error": {"type": "protocol_violation", "contains": "enc_algo"}
        },
        {
            "description": "PUBLISH.Options.enc_serializer cbor (valid with payload)",
            "test_category": "options_validation",
            "wmsg": [16, 123, {"enc_algo": "cryptobox", "enc_serializer": "cbor"}, "com.example.topic", payload_hex]
        },
    ])

    return samples


def generate_subscribe_options_samples():
    """Generate all SUBSCRIBE.Options validation samples"""
    samples = []

    # match
    samples.extend([
        {
            "description": "SUBSCRIBE.Options.match exact (valid)",
            "test_category": "options_validation",
            "wmsg": [32, 123, {"match": "exact"}, "com.example.topic"]
        },
        {
            "description": "SUBSCRIBE.Options.match prefix (valid)",
            "test_category": "options_validation",
            "wmsg": [32, 123, {"match": "prefix"}, "com.example.topic"]
        },
        {
            "description": "SUBSCRIBE.Options.match wildcard (valid)",
            "test_category": "options_validation",
            "wmsg": [32, 123, {"match": "wildcard"}, "com.example.topic"]
        },
        {
            "description": "SUBSCRIBE.Options.match with invalid value",
            "test_category": "options_validation",
            "wmsg": [32, 123, {"match": "invalid"}, "com.example.topic"],
            "expected_error": {"type": "protocol_violation", "contains": "match"}
        },
        {
            "description": "SUBSCRIBE.Options.match with invalid type int",
            "test_category": "options_validation",
            "wmsg": [32, 123, {"match": 123}, "com.example.topic"],
            "expected_error": {"type": "protocol_violation", "contains": "match"}
        },
    ])

    # get_retained
    samples.extend([
        {
            "description": "SUBSCRIBE.Options.get_retained with value true (valid)",
            "test_category": "options_validation",
            "wmsg": [32, 123, {"get_retained": True}, "com.example.topic"]
        },
        {
            "description": "SUBSCRIBE.Options.get_retained with value false (valid)",
            "test_category": "options_validation",
            "wmsg": [32, 123, {"get_retained": False}, "com.example.topic"]
        },
        {
            "description": "SUBSCRIBE.Options.get_retained with invalid type string",
            "test_category": "options_validation",
            "wmsg": [32, 123, {"get_retained": "hello"}, "com.example.topic"],
            "expected_error": {"type": "protocol_violation", "contains": "get_retained"}
        },
    ])

    # forward_for
    samples.extend([
        {
            "description": "SUBSCRIBE.Options.forward_for empty list (valid)",
            "test_category": "options_validation",
            "wmsg": [32, 123, {"forward_for": []}, "com.example.topic"]
        },
        {
            "description": "SUBSCRIBE.Options.forward_for with router info (valid)",
            "test_category": "options_validation",
            "wmsg": [32, 123, {"forward_for": [{"session": 123, "authid": "router1", "authrole": "router"}]}, "com.example.topic"]
        },
        {
            "description": "SUBSCRIBE.Options.forward_for with invalid type string",
            "test_category": "options_validation",
            "wmsg": [32, 123, {"forward_for": "hello"}, "com.example.topic"],
            "expected_error": {"type": "protocol_violation", "contains": "forward_for"}
        },
    ])

    return samples


def generate_event_details_samples():
    """Generate all EVENT.Details validation samples"""
    samples = []

    # publisher
    samples.extend([
        {
            "description": "EVENT.Details.publisher with session ID (valid)",
            "test_category": "details_validation",
            "wmsg": [36, 123, 456, {"publisher": 789}, ["args"]]
        },
        {
            "description": "EVENT.Details.publisher with invalid type string",
            "test_category": "details_validation",
            "wmsg": [36, 123, 456, {"publisher": "hello"}, ["args"]],
            "expected_error": {"type": "protocol_violation", "contains": "publisher"}
        },
    ])

    # publisher_authid
    samples.extend([
        {
            "description": "EVENT.Details.publisher_authid with authid (valid)",
            "test_category": "details_validation",
            "wmsg": [36, 123, 456, {"publisher_authid": "alice"}, ["args"]]
        },
        {
            "description": "EVENT.Details.publisher_authid with invalid type int",
            "test_category": "details_validation",
            "wmsg": [36, 123, 456, {"publisher_authid": 123}, ["args"]],
            "expected_error": {"type": "protocol_violation", "contains": "publisher_authid"}
        },
    ])

    # publisher_authrole
    samples.extend([
        {
            "description": "EVENT.Details.publisher_authrole with role (valid)",
            "test_category": "details_validation",
            "wmsg": [36, 123, 456, {"publisher_authrole": "manager"}, ["args"]]
        },
        {
            "description": "EVENT.Details.publisher_authrole with invalid type int",
            "test_category": "details_validation",
            "wmsg": [36, 123, 456, {"publisher_authrole": 123}, ["args"]],
            "expected_error": {"type": "protocol_violation", "contains": "publisher_authrole"}
        },
    ])

    # topic
    samples.extend([
        {
            "description": "EVENT.Details.topic with URI (valid)",
            "test_category": "details_validation",
            "wmsg": [36, 123, 456, {"topic": "com.example.topic"}, ["args"]]
        },
        {
            "description": "EVENT.Details.topic with invalid type int",
            "test_category": "details_validation",
            "wmsg": [36, 123, 456, {"topic": 123}, ["args"]],
            "expected_error": {"type": "protocol_violation", "contains": "topic"}
        },
    ])

    # retained
    samples.extend([
        {
            "description": "EVENT.Details.retained with value true (valid)",
            "test_category": "details_validation",
            "wmsg": [36, 123, 456, {"retained": True}, ["args"]]
        },
        {
            "description": "EVENT.Details.retained with value false (valid)",
            "test_category": "details_validation",
            "wmsg": [36, 123, 456, {"retained": False}, ["args"]]
        },
        {
            "description": "EVENT.Details.retained with invalid type string",
            "test_category": "details_validation",
            "wmsg": [36, 123, 456, {"retained": "hello"}, ["args"]],
            "expected_error": {"type": "protocol_violation", "contains": "retained"}
        },
    ])

    # transaction_hash
    samples.extend([
        {
            "description": "EVENT.Details.transaction_hash with value (valid)",
            "test_category": "details_validation",
            "wmsg": [36, 123, 456, {"transaction_hash": "abc123"}, ["args"]]
        },
        {
            "description": "EVENT.Details.transaction_hash with invalid type int",
            "test_category": "details_validation",
            "wmsg": [36, 123, 456, {"transaction_hash": 123}, ["args"]],
            "expected_error": {"type": "protocol_violation", "contains": "transaction_hash"}
        },
    ])

    # x_acknowledged_delivery
    samples.extend([
        {
            "description": "EVENT.Details.x_acknowledged_delivery with value true (valid)",
            "test_category": "details_validation",
            "wmsg": [36, 123, 456, {"x_acknowledged_delivery": True}, ["args"]]
        },
        {
            "description": "EVENT.Details.x_acknowledged_delivery with invalid type string",
            "test_category": "details_validation",
            "wmsg": [36, 123, 456, {"x_acknowledged_delivery": "hello"}, ["args"]],
            "expected_error": {"type": "protocol_violation", "contains": "x_acknowledged_delivery"}
        },
    ])

    # forward_for
    samples.extend([
        {
            "description": "EVENT.Details.forward_for empty list (valid)",
            "test_category": "details_validation",
            "wmsg": [36, 123, 456, {"forward_for": []}, ["args"]]
        },
        {
            "description": "EVENT.Details.forward_for with router info (valid)",
            "test_category": "details_validation",
            "wmsg": [36, 123, 456, {"forward_for": [{"session": 789, "authid": "router1", "authrole": "router"}]}, ["args"]]
        },
        {
            "description": "EVENT.Details.forward_for with invalid type string",
            "test_category": "details_validation",
            "wmsg": [36, 123, 456, {"forward_for": "hello"}, ["args"]],
            "expected_error": {"type": "protocol_violation", "contains": "forward_for"}
        },
    ])

    # E2EE options (only valid with transparent payload)
    payload_hex = "a1666e6f74696365"
    samples.extend([
        {
            "description": "EVENT.Details.enc_algo cryptobox (valid with payload)",
            "test_category": "details_validation",
            "wmsg": [36, 123, 456, {"enc_algo": "cryptobox"}, payload_hex]
        },
        {
            "description": "EVENT.Details.enc_algo with invalid value",
            "test_category": "details_validation",
            "wmsg": [36, 123, 456, {"enc_algo": "invalid"}, payload_hex],
            "expected_error": {"type": "protocol_violation", "contains": "enc_algo"}
        },
        {
            "description": "EVENT.Details.enc_serializer cbor (valid with payload)",
            "test_category": "details_validation",
            "wmsg": [36, 123, 456, {"enc_algo": "cryptobox", "enc_serializer": "cbor"}, payload_hex]
        },
    ])

    return samples


if __name__ == "__main__":
    if len(sys.argv) > 1:
        msg_type = sys.argv[1]
        if msg_type == "event":
            samples = generate_event_details_samples()
            print(json.dumps(samples, indent=2))
            print(f"\n# Generated {len(samples)} EVENT.Details validation samples")
        elif msg_type == "subscribe":
            samples = generate_subscribe_options_samples()
            print(json.dumps(samples, indent=2))
            print(f"\n# Generated {len(samples)} SUBSCRIBE.Options validation samples")
        else:
            print(f"Unknown message type: {msg_type}")
            print("Usage: gen_validation_samples.py [publish|event|subscribe]")
    else:
        samples = generate_publish_options_samples()
        print(json.dumps(samples, indent=2))
        print(f"\n# Generated {len(samples)} PUBLISH.Options validation samples")
