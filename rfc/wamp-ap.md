%%%
title = "WAMP Advanced Profile"
abbrev = "WAMP-AP"
ipr = "trust200902"
area = "Applications and Real-Time (art)"
workgroup = "BiDirectional or Server-Initiated HTTP"
submissiontype = "IETF"
keyword = ["WebSocket, WAMP, real-time, RPC, PubSub"]
docName = "draft-oberstet-hybi-crossbar-wamp-04"
date = 2022-06-23T00:59:20+00:00

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

# Advanced Profile

While implementations MUST implement the subset of the Basic Profile necessary for the particular set of WAMP roles they provide, they MAY implement any subset of features from the Advanced Profile. Implementers SHOULD implement the maximum of features possible considering the aims of an implementation.

> Note: Features listed here may be experimental or underspecced and yet unimplemented in any implementation. This part of the specification is very much a work in progress. An approximate status of each feature is given at the beginning of the feature section.

{{text/advanced/ap_messages.md}}

{{text/advanced/ap_features.md}}


## WAMP Meta API

{{text/advanced/ap_session_meta_api.md}}

{{text/advanced/ap_rpc_registration_meta_api.md}}

{{text/advanced/ap_pubsub_subscription_meta_api.md}}


## Advanced RPC Features

{{text/advanced/ap_rpc_progressive_call_results.md}}

{{text/advanced/ap_rpc_progressive_calls.md}}

{{text/advanced/ap_rpc_call_timeout.md}}

{{text/advanced/ap_rpc_call_canceling.md}}

{{text/advanced/ap_rpc_call_rerouting.md}}

{{text/advanced/ap_rpc_caller_identification.md}}

{{text/advanced/ap_rpc_call_trustlevels.md}}

{{text/advanced/ap_rpc_pattern_based_registration.md}}

{{text/advanced/ap_rpc_shared_registration.md}}

{{text/advanced/ap_rpc_sharded_registration.md}}

{{text/advanced/ap_rpc_registration_revocation.md}}


## Advanced PubSub Features

{{text/advanced/ap_pubsub_subscriber_blackwhite_listing.md}}

{{text/advanced/ap_pubsub_publisher_exclusion.md}}

{{text/advanced/ap_pubsub_publisher_identification.md}}

{{text/advanced/ap_pubsub_publication_trustlevels.md}}

{{text/advanced/ap_pubsub_pattern_based_subscription.md}}

{{text/advanced/ap_pubsub_sharded_subscription.md}}

{{text/advanced/ap_pubsub_event_history.md}}

{{text/advanced/ap_pubsub_subscription_revocation.md}}

{{text/advanced/ap_pubsub_testament.md}}


## Authentication Methods

{{text/advanced/ap_authentication.md}}

{{text/advanced/ap_authentication_cra.md}}

{{text/advanced/ap_authentication_ticket.md}}

{{text/advanced/ap_authentication_scram.md}}


## Transports and Serialization Features

{{text/advanced/ap_transports.md}}

{{text/advanced/ap_transport_rawsocket.md}}

{{text/advanced/ap_transport_batched_websocket.md}}

{{text/advanced/ap_transport_http_longpoll.md}}

{{text/advanced/ap_transport_multiplexed.md}}

{{text/advanced/ap_serialization_binary_json.md}}


## WAMP Interfaces

{{text/advanced/ap_interface_definition.md}}

{{text/advanced/ap_interface_reflection.md}}

{{text/advanced/ap_node_control_api.md}}


## Router-to-Router Links

{{text/advanced/ap_r2r.md}}


{backmatter}
