# Status Overview

Overview of the present state of the WAMP spec RFC.
Generally follows the current file structure to enable a per-file status. 
Includes links to relevant GitHub issues [I] and mailing list discussions [D]. 


| Spec Part                         | feat. status  |  spec status  |  File            | Issues & Discussions   |
|-----------------------------------|---------------|---------------|------------------|------------------------|
| Introduction                      |               |               | -    |
|   Background                      |               |               | [basic/bp_intro_background.md](text/basic/bp_intro_background.md) |  |
|   Protocol Overview               |               |               | [basic/bp_intro_protocol_overview.md](text/basic/bp_intro_protocol_overview.md) |  |
|   Design Philosophy               |               |               | [basic/bp_intro_design_philosophy.md](text/basic/bp_intro_design_philosophy.md) |  |
| Realms, Sessions & Transports     |               |               | [main doc](draft-oberstet-hybi-tavendo-wamp.md) |  |
| Peers and Roles                   |               |               | [basic/peers_and_roles.md](text/basic/peers_and_roles.md) |  |
| Building Blocks                   |               |               | [main doc](draft-oberstet-hybi-tavendo-wamp.md) |  |
|   Identifiers                     |               |               | [basic/bp_identifiers.md](text/basic/bp_identifiers.md) |  |
|   Serializations                  |               |               | [basic/bp_serializations.md](text/basic/bp_serializations.md) |  |
|   Transports                      |               |               | [basic/bp_transports.md](text/basic/bp_transports.md) |  |
| Messages                          |               |               | [basic/bp_messages.md](text/basic/bp_messages.md) |  |
| Sessions                          |               |               | [basic/bp_sessions.md](text/basic/bp_sessions.md) |  |
| Publish & Subscribe               |               |               | [main doc](draft-oberstet-hybi-tavendo-wamp.md) |  |
|   Subscribing & Unsubscribing     |               |               | [basic/bp_pubsub_subscribing_and_undsubscribing.md](text/basic/bp_pubsub_subscribing_and_undsubscribing.md) |  |
|   Publishing & Events             |               |               | [basic/bp_pubsub_publishing_and_events.md](text/basic/bp_pubsub_publishing_and_events.md) |  |
| Remote Procedure Calls            |               |               | [main doc](draft-oberstet-hybi-tavendo-wamp.md) |  |
|   Registering & Unregistering     |               |               | [basic/bp_rpc_registering_and_unregistering.md](text/basic/bp_rpc_registering_and_unregistering.md) |  |
|   Calling & Invocations           |               |               | [basic/bp_calling_and_invocations.md](text/basic/bp_calling_and_invocations.md) |  |
| Predefined URIs                   |               |               | [main doc](draft-oberstet-hybi-tavendo-wamp.md) |  |
|   Basic Profile                   |               |               | [basic/bp_uris.md](text/basic/bp_uris.md) |  |
|   Advanced Profile                |               |               | [advanved/ap_uris.md](text/advanced/ap_uris.md) |  |
| Ordering Guarantees               |               |               | [basic/bp_ordering_guarantees.md](text/basic/bp_ordering_guarantees.md) |  |
| Security Model                    |               |               | [basic/bp_security_model.md](text/basic/bp_security_model.md) |  |
| Advanced Profile                  |               |               | [main doc](draft-oberstet-hybi-tavendo-wamp.md) |  |
|   Messages                        |               |               | [advanced/ap_messages.md](text/advanced/ap_messages.md) |  |
|   Features                        |               |               | [advanced/ap_features.md](text/advanced/ap_features.md) |  |
|   Adv. RPC Features               |               |               | -
|     Progressive Call Results      |               |               | [advanced/ap_rpc_progressive_call_results.md](text/advanced/ap_rpc_progressive_call_results.md) |  |
|     Progressive Calls             |               |               | [advanced/ap_rpc_progressive_calls.md](text/advanced/ap_rpc_progressive_calls.md) |  |
|     Call Timeouts                 |               |               | [advanced/ap_rpc_call_timeout.md](text/advanced/ap_rpc_call_timeout.md) |  |
|     Call Cancelling               |               |               | [advanced/ap_rpc_call_canceling.md](text/advanced/ap_rpc_call_canceling.md) |  |
|     Caller Identification         |               |               | [advanced/ap_rpc_caller_identification.md](text/advanced/ap_rpc_caller_identification.md) |  |
|     Call Trust Levels             |               |               | [advanced/ap_rpc_call_trustlevels.md](text/advanced/ap_rpc_call_trustlevels.md) |  |
|     Registration Meta API         |               |               | [advanced/ap_rpc_registration_meta_api.md](text/advanced/ap_rpc_registration_meta_api.md) |  |
|     Pattern-based Registrations   |               |               | [advanced/ap_rpc_pattern_based_registrations.md](text/advanced/ap_rpc_pattern_based_registrations.md) |  |
|     Shared Registrations          |               |               | [advanced/ap_rpc_shared_registrations.md](text/advanced/ap_rpc_shared_registrations.md) |  |
|     Sharded Registrations         |               |               | [advanced/ap_rpc_sharded_registrations.md](text/advanced/ap_rpc_sharded_registrations.md) |  |
|     Registration Revocation       |               |               | [advanced/ap_rpc_registration_revocation.md](text/advanced/ap_rpc_registration_revocation.md) |  |
|     Procedure Reflection          |               |               | [advanced/ap_rpc_procedure_reflection.md](text/advanced/ap_rpc_procedure_reflection.md) |  |
|   Adv. PubSub Features            |               |               | -
|     Subscr. Black & Whitelisting  |               |               | [advanced/ap_pubsub_subscriber_blackwhite_listing.md](text/advanced/ap_pubsub_subscriber_blackwhite_listing.md) |  |
|     Publisher Exclusion           |               |               | [advanced/ap_pubsub_publisher_exclusion.md](text/advanced/ap_pubsub_publisher_exclusion.md) |  |
|     Publisher Identification      |               |               | [advanced/ap_pubsub_publisher_identification.md](text/advanced/ap_pubsub_publisher_identification.md) |  |
|     Publication Trust Levels      |               |               | [advanced/ap_pubsub_publication_trustlevels.md](text/advanced/ap_pubsub_publication_trustlevels.md) |  |
|     Subscription Meta-API         |               |               | [advanced/ap_pubsub_subscription_meta_api.md](text/advanced/ap_pubsub_subscription_meta_api.md) |  |
|     Pattern-based Subscriptions   |               |               | [advanced/ap_pubsub_pattern_based_subscriptions.md](text/advanced/ap_pubsub_pattern_based_subscriptions.md) |  |
|     Sharded Subsciptions          |               |               | [advanced/ap_pubsub_sharded_subscriptions.md](text/advanced/ap_pubsub_sharded_subscriptions.md) |  |
|     Event History                 |               |               | [advanced/ap_pubsub_messages.md](text/advanced/ap_pubsub_messages.md) |  |
|     Registration Revocation       |               |               | [advanced/ap_pubsub_registration_revocation.md](text/advanced/ap_pubsub_registration_revocation.md) |  |
|     Topic Reflection              |               |               | [advanced/ap_pubsub_topic_reflection.md](text/advanced/ap_pubsub_topic_reflection.md) |  |
|   Other Adv. Features             |               |               | -
|     Session Meta-API              |               |               | [advanced/ap_session_meta_api.md](text/advanced/ap_session_meta_api.md) |  |
|     Authentication                |               |               | [advanced/ap_authentication.md](text/advanced/ap_authentication.md) |  |
|       Challenge-Response          |               |               | [advanced/ap_authentication_cra.md](text/advanced/ap_authentication_cra.md) |  |
|       Ticket                      |               |               | [advanced/ap_authentication_ticket.md](text/advanced/ap_authentication_ticket.md) |  |
|     Alternative Transports        |               |               | [advanced/ap_transport.md](text/advanced/ap_transport.md) |  |
|       RawSocket                   |               |               | [advanced/ap_transport_rawsocket.md](text/advanced/ap_transport_rawsocket.md) |  |
|       Batched WebSocket           |               |               | [advanced/ap_transport_batched_websocket.md](text/advanced/ap_transport_batched_websocket.md) |  |
|       HTTP Longpoll               |               |               | [advanced/ap_transport_http_longpoll.md](text/advanced/ap_transport_http_longpoll.md) |  |
|       Multiplexed                 |               |               | [advanced/ap_transport_multiplexed.md](text/advanced/ap_transport_multiplexed.md) |  | |  |
| Binary Conversion of JSON Strings |               |               | [basic/bp_binbary_conversion_of_json.md](text/basic/bp_binbary_conversion_of_json.md) |  |
| Security Considerations           |               |               | [main doc](draft-oberstet-hybi-tavendo-wamp.md) |  |
| Contributors                      |               |               | [main doc](draft-oberstet-hybi-tavendo-wamp.md) |  |
| Acknowledgements                  |               |               | [main doc](draft-oberstet-hybi-tavendo-wamp.md) |  |
| References                        |               |               | [main doc](draft-oberstet-hybi-tavendo-wamp.md) |  |
