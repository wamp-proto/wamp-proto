# Abstract

This document defines the Web Application Messaging Protocol (WAMP). WAMP is a routed protocol that provides two messaging patterns: Publish & Subscribe and routed Remote Procedure Calls. It is intended to connect application components in distributed applications. WAMP uses WebSocket as its default transport, but can be transmitted via any other protocol that allows for ordered, reliable, bi-directional, and message-oriented communications.


{{basic/bp_01_introduction.md}}

{{basic/bp_02_building_blocks.md}}

{{basic/bp_03_messages.md}}

{{basic/bp_04_sessions.md}}

{{basic/bp_05_publish_subscribe.md}}

{{basic/bp_06_remote_procedure_call.md}}

{{basic/bp_07_security_model.md}}

{{basic/bp_08_uri_reference.md}}


# IANA Considerations

WAMP uses the Subprotocol Identifier `wamp` registered with the [WebSocket Subprotocol Name Registry](https://www.iana.org/assignments/websocket/websocket.xhtml), operated by the Internet Assigned Numbers Authority (IANA).


# Conformance Requirements

All diagrams, examples, and notes in this specification are non-normative, as are all sections explicitly marked non-normative. Everything else in this specification is normative.

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT",
"SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in
this document are to be interpreted as described in RFC 2119 [@?RFC2119].

Requirements phrased in the imperative as part of algorithms (such as "strip any leading space characters" or "return false and abort these steps") are to be interpreted with the meaning of the key word ("MUST", "SHOULD", "MAY", etc.) used in introducing the algorithm.

Conformance requirements phrased as algorithms or specific steps MAY  be implemented in any manner, so long as the end result is equivalent.

## Terminology and Other Conventions

Key terms such as named algorithms or definitions are indicated like _this_ when they first occur, and are capitalized throughout the text.
