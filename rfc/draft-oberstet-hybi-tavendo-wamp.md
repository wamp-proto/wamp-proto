% Title = "The Web Application Messaging Protocol"
% abbrev = "WAMP"
% category = "std"
% docName = "draft-oberstet-hybi-tavendo-wamp-02"
% ipr= "trust200902"
% area = "Applications and Real-Time (art)"
% workgroup = "BiDirectional or Server-Initiated HTTP"
% keyword = ["WebSocket, WAMP, real-time, RPC, PubSub"]
%
% date = 2015-10-11T00:00:00Z
%
% [pi]
% toc = "yes"
%
% [[author]]
% initials="T.O."
% surname="Oberstein"
% fullname="Tobias G. Oberstein"
% organization = "Tavendo GmbH"
%   [author.address]
%   email = "tobias.oberstein@tavendo.de"
%
% [[author]]
% initials="A.G."
% surname="Goedde"
% fullname="Alexander Goedde"
% organization = "Tavendo GmbH"
%   [author.address]
%   email = "alexander.goedde@tavendo.de"
%

.# Abstract

This document defines the Web Application Messaging Protocol (WAMP). WAMP is a routed protocol that provides two messaging patterns: Publish & Subscribe and routed Remote Procedure Calls. It is intended to connect application components in distributed applications. WAMP uses WebSocket as its default transport, but can be transmitted via any other protocol that allows for ordered, reliable, bi-directional, and message-oriented communications.

{mainmatter}

# Introduction

{{rfc/text/basic/bp_intro_background.md}}

{{rfc/text/basic/bp_intro_protocol_overview.md}}

{{rfc/text/basic/bp_intro_design_philosophy.md}}


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



<!-- peers and roles -->

{{rfc/text/basic/bp_peers_and_roles.md}}



# Building Blocks

WAMP is defined with respect to the following building blocks

1.  Identifiers
2.  Serializations
3.  Transports

For each building block, WAMP only assumes a defined set of requirements, which allows to run WAMP variants with different concrete bindings.


{{rfc/text/basic/bp_identifiers.md}}

{{rfc/text/basic/bp_serializations.md}}

{{rfc/text/basic/bp_transports.md}}


<!-- messages -->

{{rfc/text/basic/bp_messages.md}}

<!-- sessions -->

{{rfc/text/basic/bp_sessions.md}}


# Publish and Subscribe

All of the following features for Publish & Subscribe are mandatory for WAMP Basic Profile implementations supporting the respective roles, i.e. *Publisher*, *Subscriber* and *Dealer*.


{{rfc/text/basic/bp_pubsub_subscribing_and_unsubscribing.md}}

{{rfc/text/basic/bp_pubsub_publishing_and_events.md}}


# Remote Procedure Calls

All of the following features for Remote Procedure Calls are mandatory for WAMP Basic Profile implementations supporting the respective roles.


{{rfc/text/basic/bp_rpc_registering_and_unregistering.md}}

{{rfc/text/basic/bp_rpc_calling_and_invocation.md}}



# Predefined URIs

WAMP pre-defines the following error URIs for the basic and for the advanced profile. WAMP peers MUST use only the defined error messages.

{{rfc/text/basic/bp_uris.md}}

{{rfc/text/advanced/ap_uris.md}}


<!-- ordering guarantees -->

{{rfc/text/basic/bp_ordering_guarantees.md}}

<!-- security model -->

{{rfc/text/basic/bp_security_model.md}}




# Advanced Profile

While implementations MUST implement the subset of the Basic Profile necessary for the particular set of WAMP roles they provide, they MAY implement any subset of features from the Advanced Profile. Implementers SHOULD implement the maximum of features possible considering the aims of an implementation.

> Note: Features listed here may be experimental or underspecced and yet unimplemented in any implementation. This is part of the specification is very much a work in progress. An approximate status of each feature is given at the beginning of the feature section.

{{rfc/text/advanced/ap_messages.md}}

{{rfc/text/advanced/ap_features.md}}


## Advanced RPC Features

{{rfc/text/advanced/ap_rpc_progressive_call_results.md}}

{{rfc/text/advanced/ap_rpc_progressive_calls.md}}

{{rfc/text/advanced/ap_rpc_call_timeout.md}}

{{rfc/text/advanced/ap_rpc_call_canceling.md}}

{{rfc/text/advanced/ap_rpc_caller_identification.md}}

{{rfc/text/advanced/ap_rpc_call_trustlevels.md}}

{{rfc/text/advanced/ap_rpc_registration_meta_api.md}}

{{rfc/text/advanced/ap_rpc_pattern_based_registration.md}}

{{rfc/text/advanced/ap_rpc_shared_registration.md}}

{{rfc/text/advanced/ap_rpc_sharded_registration.md}}

{{rfc/text/advanced/ap_rpc_registration_revocation.md}}

{{rfc/text/advanced/ap_rpc_procedure_reflection.md}}


## Advanced PubSub Features

{{rfc/text/advanced/ap_pubsub_subscriber_blackwhite_listing.md}}

{{rfc/text/advanced/ap_pubsub_publisher_exclusion.md}}

{{rfc/text/advanced/ap_pubsub_publisher_identification.md}}

{{rfc/text/advanced/ap_pubsub_publication_trustlevels.md}}

{{rfc/text/advanced/ap_pubsub_subscription_meta_api.md}}

{{rfc/text/advanced/ap_pubsub_pattern_based_subscription.md}}

{{rfc/text/advanced/ap_pubsub_sharded_subscription.md}}

{{rfc/text/advanced/ap_pubsub_event_history.md}}

{{rfc/text/advanced/ap_pubsub_subscription_revocation.md}}

{{rfc/text/advanced/ap_pubsub_topic_reflection.md}}


## Other Advanced Features


{{rfc/text/advanced/ap_session_meta_api.md}}


{{rfc/text/advanced/ap_authentication.md}}

{{rfc/text/advanced/ap_authentication_cra.md}}

{{rfc/text/advanced/ap_authentication_ticket.md}}


{{rfc/text/advanced/ap_transports.md}}

{{rfc/text/advanced/ap_transport_rawsocket.md}}

{{rfc/text/advanced/ap_transport_batched_websocket.md}}

{{rfc/text/advanced/ap_transport_http_longpoll.md}}

{{rfc/text/advanced/ap_transport_multiplexed.md}}

{{rfc/text/basic/bp_binary_conversion_of_json.md}}


# Security Considerations

-- write me --

# IANA Considerations

TBD

# Contributors

# Acknowledgements

WAMP was developed in an open process from the beginning, and a lot of people have contributed ideas and other feedback. Here we are listing people who have opted in to being mentioned:

* Konstantin Burkalev (@KSDaemon on GitHub)
* Emile Cormier (@ecorm on GitHub)



{backmatter}
