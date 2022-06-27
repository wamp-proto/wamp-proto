# WAMP Advanced Profile

While all implementations MUST implement the subset of the Basic Profile necessary for the particular set of WAMP roles they provide, they MAY implement any subset of features from the Advanced Profile. Implementers SHOULD implement the maximum of features possible considering the aims of an implementation.

> Note: Features listed here may be experimental or underspecced and yet unimplemented in any implementation. This part of the specification is very much a work in progress. An approximate status of each feature is given at the beginning of the feature section.

{{advanced/ap_features.md}}

{{advanced/ap_messages.md}}


# Meta API

{{advanced/ap_meta_api_sessions.md}}

{{advanced/ap_meta_api_registrations.md}}

{{advanced/ap_meta_api_subscriptions.md}}


# Advanced RPC

{{advanced/ap_rpc_progressive_call_results.md}}

{{advanced/ap_rpc_progressive_calls.md}}

{{advanced/ap_rpc_call_timeout.md}}

{{advanced/ap_rpc_call_canceling.md}}

{{advanced/ap_rpc_call_rerouting.md}}

{{advanced/ap_rpc_caller_identification.md}}

{{advanced/ap_rpc_call_trustlevels.md}}

{{advanced/ap_rpc_pattern_based_registration.md}}

{{advanced/ap_rpc_shared_registration.md}}

{{advanced/ap_rpc_sharded_registration.md}}

{{advanced/ap_rpc_registration_revocation.md}}


# Advanced PubSub

{{advanced/ap_pubsub_subscriber_blackwhite_listing.md}}

{{advanced/ap_pubsub_publisher_exclusion.md}}

{{advanced/ap_pubsub_publisher_identification.md}}

{{advanced/ap_pubsub_publication_trustlevels.md}}

{{advanced/ap_pubsub_pattern_based_subscription.md}}

{{advanced/ap_pubsub_sharded_subscription.md}}

{{advanced/ap_pubsub_event_history.md}}

{{advanced/ap_pubsub_subscription_revocation.md}}

{{advanced/ap_pubsub_testament.md}}


# Authentication Methods

{{advanced/ap_authentication.md}}

{{advanced/ap_authentication_ticket.md}}

{{advanced/ap_authentication_cra.md}}

{{advanced/ap_authentication_scram.md}}

{{advanced/ap_authentication_cryptosign.md}}


# Dynamic Authentication API

{{advanced/ap_authentication_dynamic.md}}


# Advanced Transports and Serializers

{{advanced/ap_transports.md}}

{{advanced/ap_transport_rawsocket.md}}

{{advanced/ap_transport_batched_websocket.md}}

{{advanced/ap_transport_http_longpoll.md}}

{{advanced/ap_transport_multiplexed.md}}

{{advanced/ap_serialization_binary_json.md}}


# WAMP Interfaces

{{advanced/ap_interfaces.md}}

{{advanced/ap_interface_definition.md}}

{{advanced/ap_interface_catalogs.md}}

{{advanced/ap_interface_reflection.md}}


# Router-to-Router Links

{{advanced/ap_router_to_router_link.md}}


# Advanced Profile URIs

{{advanced/ap_uris.md}}