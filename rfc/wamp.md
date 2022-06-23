%%%
title = "The Web Application Messaging Protocol"
abbrev = "WAMP"
ipr = "trust200902"
area = "Applications and Real-Time (art)"
workgroup = "BiDirectional or Server-Initiated HTTP"
submissiontype = "IETF"
keyword = ["WebSocket, WAMP, real-time, RPC, PubSub"]
docName = "draft-oberstet-hybi-crossbar-wamp-04"
date = 2022-06-23T02:28:25+00:00

[seriesInfo]
name = "Internet-Draft"
value = "WAMP"
stream = "IETF"
status = "experimental"

[pi]
toc = "yes"

[[author]]
initials="T."
surname="Oberstein"
fullname="Tobias Oberstein"
organization = "typedef int GmbH"
  [author.address]
  email = "tobias.oberstein@typedefint.eu"
%%%

{mainmatter}

# Abstract

This document defines the Web Application Messaging Protocol (WAMP). WAMP is a routed protocol that provides two messaging patterns: Publish & Subscribe and routed Remote Procedure Calls. It is intended to connect application components in distributed applications. WAMP uses WebSocket as its default transport, but can be transmitted via any other protocol that allows for ordered, reliable, bi-directional, and message-oriented communications.

# Introduction

{{text/basic/bp_intro_background.md}}

{{text/basic/bp_intro_protocol_overview.md}}

{{text/basic/bp_intro_design_philosophy.md}}


## Relationship to WebSocket

WAMP uses WebSocket as its default transport binding, and is a registered WebSocket subprotocol.


# Conformance Requirements

All diagrams, examples, and notes in this specification are non-normative, as are all sections explicitly marked non-normative. Everything else in this specification is normative.

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT",
"SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in
this document are to be interpreted as described in RFC 2119 [@?RFC2119].

Requirements phrased in the imperative as part of algorithms (such as "strip any leading space characters" or "return false and abort these steps") are to be interpreted with the meaning of the key word ("MUST", "SHOULD", "MAY", etc.) used in introducing the algorithm.

Conformance requirements phrased as algorithms or specific steps MAY  be implemented in any manner, so long as the end result is equivalent.

## Terminology and Other Conventions

Key terms such as named algorithms or definitions are indicated like _this_ when they first occur, and are capitalized throughout the text.


# Realms, Sessions and Transports

A Realm is a WAMP routing and administrative domain, optionally protected by authentication and authorization. WAMP messages are only routed within a Realm.

A Session is a transient conversation between two Peers attached to a Realm and running over a Transport.

A Transport connects two WAMP Peers and provides a channel over which WAMP messages for a WAMP Session can flow in both directions.

WAMP can run over any Transport which is message-based, bidirectional,  reliable and ordered.

The default transport for WAMP is WebSocket [@!RFC6455], where WAMP is an [officially registered](http://www.iana.org/assignments/websocket/websocket.xml) subprotocol.

{{text/basic/bp_peers_and_roles.md}}


# Building Blocks

WAMP is defined with respect to the following building blocks

1.  Identifiers
2.  Serializations
3.  Transports

For each building block, WAMP only assumes a defined set of requirements, which allows to run WAMP variants with different concrete bindings.

{{text/basic/bp_identifiers.md}}

{{text/basic/bp_serializations.md}}

{{text/basic/bp_transports.md}}

{{text/basic/bp_messages.md}}

{{text/basic/bp_sessions.md}}


# Publish and Subscribe

All of the following features for Publish & Subscribe are mandatory for WAMP Basic Profile implementations supporting the respective roles, i.e. *Publisher*, *Subscriber* and *Broker*.

{{text/basic/bp_pubsub_subscribing_and_unsubscribing.md}}

{{text/basic/bp_pubsub_publishing_and_events.md}}


# Remote Procedure Calls

All of the following features for Remote Procedure Calls are mandatory for WAMP Basic Profile implementations supporting the respective roles.

{{text/basic/bp_rpc_registering_and_unregistering.md}}

{{text/basic/bp_rpc_calling_and_invocation.md}}


# Ordering Guarantees

{{text/basic/bp_ordering_guarantees.md}}


# Security Model

{{text/basic/bp_security_model.md}}


# Predefined URIs

WAMP pre-defines the following error URIs for the basic and for the advanced profile. WAMP peers MUST use only the defined error messages.

{{text/basic/bp_uris.md}}

{{text/advanced/ap_uris.md}}


# IANA Considerations

TBD


# Contributors

WAMP was developed in an open process from the beginning, and a lot of people have contributed ideas and other feedback. Here we are listing people who have opted in to being mentioned:

* Alexander Goedde
* Amber Brown
* Andrew Gillis
* David Chappelle
* Elvis Stansvik
* Emile Cormier
* Felipe Gasper
* Johan 't Hart
* Josh Soref
* Konstantin Burkalev
* Pahaz Blinov
* Paolo Angioletti
* Roberto Requena
* Roger Erens
* Christoph Herzog
* Tobias Oberstein
* Zhigang Wang


# Acknowledgements

{backmatter}
