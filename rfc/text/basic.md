# Abstract

This document defines the Web Application Messaging Protocol (WAMP). WAMP is a routed protocol that provides two messaging patterns: Publish & Subscribe and routed Remote Procedure Calls. It is intended to connect application components in distributed applications. WAMP uses WebSocket as its default transport, but can be transmitted via any other protocol that allows for ordered, reliable, bi-directional, and message-oriented communications.

# Conformance Requirements

All diagrams, examples, and notes in this specification are non-normative, as are all sections explicitly marked non-normative. Everything else in this specification is normative.

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT",
"SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in
this document are to be interpreted as described in RFC 2119 [@?RFC2119].

Requirements phrased in the imperative as part of algorithms (such as "strip any leading space characters" or "return false and abort these steps") are to be interpreted with the meaning of the key word ("MUST", "SHOULD", "MAY", etc.) used in introducing the algorithm.

Conformance requirements phrased as algorithms or specific steps MAY  be implemented in any manner, so long as the end result is equivalent.

## Terminology and Other Conventions

Key terms such as named algorithms or definitions are indicated like _this_ when they first occur, and are capitalized throughout the text.

# Introduction

{{basic/bp_intro_background.md}}

{{basic/bp_intro_protocol_overview.md}}

{{basic/bp_peers_and_roles.md}}

{{basic/bp_intro_design_aspects.md}}


# Building Blocks

WAMP is defined with respect to the following building blocks

1.  Identifiers
2.  Serializations
3.  Transports

For each building block, WAMP only assumes a defined set of requirements, which allows to run WAMP variants with different concrete bindings.

{{basic/bp_identifiers.md}}

{{basic/bp_serializations.md}}

{{basic/bp_transports.md}}

{{basic/bp_messages.md}}

{{basic/bp_sessions.md}}


# Publish and Subscribe

All of the following features for Publish & Subscribe are mandatory for WAMP Basic Profile implementations supporting the respective roles, i.e. *Publisher*, *Subscriber* and *Broker*.

{{basic/bp_pubsub_subscribing_and_unsubscribing.md}}

{{basic/bp_pubsub_publishing_and_events.md}}


# Remote Procedure Calls

All of the following features for Remote Procedure Calls are mandatory for WAMP Basic Profile implementations supporting the respective roles.

{{basic/bp_rpc_registering_and_unregistering.md}}

{{basic/bp_rpc_calling_and_invocation.md}}


# Ordering Guarantees

{{basic/bp_ordering_guarantees.md}}


# Security Model

{{basic/bp_security_model.md}}


# Predefined URIs

WAMP pre-defines the following error URIs for the basic and for the advanced profile. WAMP peers MUST use only the defined error messages.

{{basic/bp_uris.md}}

{{advanced/ap_uris.md}}


# IANA Considerations

WAMP uses the Subprotocol Identifier `wamp` registered with the [WebSocket Subprotocol Name Registry](https://www.iana.org/assignments/websocket/websocket.xhtml), operated by the Internet Assigned Numbers Authority (IANA).
