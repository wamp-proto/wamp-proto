# Status Overview

Overview of the present state of the WAMP spec RFC.
Generally follows the current file structure to enable a per-file status. 
Includes links to relevant GitHub issues [I] and mailing list discussions [D]. 

Feature Status | Description
---------------|--------------------------------------------------
sketch         | There is a rough description of an itch to scratch, but the feature use case isn't clear, and there is no protocol proposal at all.
alpha          | The feature use case is still fuzzy and/or the feature definition is unclear, but there is at least a protocol level proposal.
beta           | The feature use case is clearly defined and the feature definition in the spec is sufficient to write a prototype implementation. The feature definition and details may still be incomplete and change.
stable         | The feature definition in the spec is complete and stable and the feature use case is field proven in real applications. There are multiple, interoperatble implementations.


Spec Status    | Description
----------------------------------------------------------------
missing        | There is no text, or what is there is not sufficient to even cover the basics of the feature/section
sketch         | The text is sufficient to give the reader some idea of the feature/section content.
draft          | Some content is missing, or the language/structure is in clear need of improvement.
polish         | The section has all content and is free of errors. The language may be improved, though.
final          | The section does not require any more attention. 


| Spec Part                         | feat. status  |  spec status  |  File            | Issues & Discussions   |
|-----------------------------------|---------------|---------------|------------------|------------------------|
| Introduction                      | -             |  -            | -    |
|   Background                      | -             |  draft        | [basic/bp_intro_background.md](text/basic/bp_intro_background.md) |  |
|   Protocol Overview               | -             |  draft        | [basic/bp_intro_protocol_overview.md](text/basic/bp_intro_protocol_overview.md) |  |
|   Design Philosophy               | -             |  draft        | [basic/bp_intro_design_philosophy.md](text/basic/bp_intro_design_philosophy.md) |  |
| Realms, Sessions & Transports     | -             |  polish       | [main doc](draft-oberstet-hybi-tavendo-wamp.md) |  |
| Peers and Roles                   | -             |  polish       | [basic/bp_peers_and_roles.md](text/basic/bp_peers_and_roles.md) |  |
| Building Blocks                   | -             |  polish       | [main doc](draft-oberstet-hybi-tavendo-wamp.md) |  |
|   Identifiers                     | stable        |  draft        | [basic/bp_identifiers.md](text/basic/bp_identifiers.md) | https://github.com/wamp-proto/wamp-proto/issues/161, https://github.com/wamp-proto/wamp-proto/issues/121, https://github.com/wamp-proto/wamp-proto/issues/115  |
|   Serializations                  | stable        |               | [basic/bp_serializations.md](text/basic/bp_serializations.md) | https://github.com/wamp-proto/wamp-proto/issues/191, https://github.com/wamp-proto/wamp-proto/issues/151, https://github.com/wamp-proto/wamp-proto/issues/72 |
|   Transports                      | stable        |               | [basic/bp_transports.md](text/basic/bp_transports.md) |  |
| Messages                          | stable        |               | [basic/bp_messages.md](text/basic/bp_messages.md) | https://github.com/wamp-proto/wamp-proto/issues/192, https://github.com/wamp-proto/wamp-proto/issues/150, https://github.com/wamp-proto/wamp-proto/issues/120 |
| Sessions                          | stable        |               | [basic/bp_sessions.md](text/basic/bp_sessions.md) | https://github.com/wamp-proto/wamp-proto/issues/145, https://github.com/wamp-proto/wamp-proto/issues/127, https://github.com/wamp-proto/wamp-proto/issues/108 |
| Publish & Subscribe               | -             |               | [main doc](draft-oberstet-hybi-tavendo-wamp.md) |  |
|   Subscribing & Unsubscribing     | stable        |               | [basic/bp_pubsub_subscribing_and_unsubscribing.md](text/basic/bp_pubsub_subscribing_and_unsubscribing.md) | https://github.com/wamp-proto/wamp-proto/issues/142 |
|   Publishing & Events             | stable        |               | [basic/bp_pubsub_publishing_and_events.md](text/basic/bp_pubsub_publishing_and_events.md) |  |
| Remote Procedure Calls            | -             |               | [main doc](draft-oberstet-hybi-tavendo-wamp.md) |  |
|   Registering & Unregistering     | stable        |               | [basic/bp_rpc_registering_and_unregistering.md](text/basic/bp_rpc_registering_and_unregistering.md) | https://github.com/wamp-proto/wamp-proto/issues/104 |
|   Calling & Invocations           | stable        |               | [basic/bp_rpc_calling_and_invocation.md](text/basic/bp_rpc_calling_and_invocation.md) |  |
| Predefined URIs                   | -             |               | [main doc](draft-oberstet-hybi-tavendo-wamp.md) |  |
|   Basic Profile                   | stable        |               | [basic/bp_uris.md](text/basic/bp_uris.md) |  |
|   Advanced Profile                |               |               | [advanved/ap_uris.md](text/advanced/ap_uris.md) |  |
| Ordering Guarantees               | stable        |               | [basic/bp_ordering_guarantees.md](text/basic/bp_ordering_guarantees.md) |  |
| Security Model                    |               |               | [basic/bp_security_model.md](text/basic/bp_security_model.md) |  |
| Advanced Profile                  |               |               | [main doc](draft-oberstet-hybi-tavendo-wamp.md) | https://github.com/wamp-proto/wamp-proto/issues/159, https://github.com/wamp-proto/wamp-proto/issues/157 |
|   Messages                        |               |               | [advanced/ap_messages.md](text/advanced/ap_messages.md) |  |
|   Features                        |               |               | [advanced/ap_features.md](text/advanced/ap_features.md) |  |
|   Adv. RPC Features               | -             |               | -
|     Progressive Call Results      | beta          |               | [advanced/ap_rpc_progressive_call_results.md](text/advanced/ap_rpc_progressive_call_results.md) | https://github.com/wamp-proto/wamp-proto/issues/199 |
|     Progressive Calls             | sketch        |               | [advanced/ap_rpc_progressive_calls.md](text/advanced/ap_rpc_progressive_calls.md) | https://github.com/wamp-proto/wamp-proto/issues/167 |
|     Call Timeouts                 | alpha         |               | [advanced/ap_rpc_call_timeout.md](text/advanced/ap_rpc_call_timeout.md) | https://github.com/wamp-proto/wamp-proto/issues/155 |
|     Call Cancelling               | alpha         |               | [advanced/ap_rpc_call_canceling.md](text/advanced/ap_rpc_call_canceling.md) | https://github.com/wamp-proto/wamp-proto/issues/160, https://github.com/wamp-proto/wamp-proto/issues/156, https://github.com/wamp-proto/wamp-proto/issues/141, https://github.com/wamp-proto/wamp-proto/issues/140 |
|     Caller Identification         | alpha         |               | [advanced/ap_rpc_caller_identification.md](text/advanced/ap_rpc_caller_identification.md) |  |
|     Call Trust Levels             | alpha         |               | [advanced/ap_rpc_call_trustlevels.md](text/advanced/ap_rpc_call_trustlevels.md) |  |
|     Registration Meta API         | beta          |               | [advanced/ap_rpc_registration_meta_api.md](text/advanced/ap_rpc_registration_meta_api.md) | https://github.com/wamp-proto/wamp-proto/issues/169, https://github.com/wamp-proto/wamp-proto/issues/55, https://github.com/wamp-proto/wamp-proto/issues/30 |
|     Pattern-based Registrations   | beta          |               | [advanced/ap_rpc_pattern_based_registration.md](text/advanced/ap_rpc_pattern_based_registration.md) | https://github.com/wamp-proto/wamp-proto/issues/182, https://github.com/wamp-proto/wamp-proto/issues/174 |
|     Shared Registrations          | beta          |               | [advanced/ap_rpc_shared_registration.md](text/advanced/ap_rpc_shared_registration.md) | https://github.com/wamp-proto/wamp-proto/issues/188, https://github.com/wamp-proto/wamp-proto/issues/103, https://github.com/wamp-proto/wamp-proto/issues/89 |
|     Sharded Registrations         | alpha         |               | [advanced/ap_rpc_sharded_registration.md](text/advanced/ap_rpc_sharded_registration.md) |  |
|     Registration Revocation       | alpha         |               | [advanced/ap_rpc_registration_revocation.md](text/advanced/ap_rpc_registration_revocation.md) |  |
|     Procedure Reflection          | sketch        |               | [advanced/ap_rpc_procedure_reflection.md](text/advanced/ap_rpc_procedure_reflection.md) | https://github.com/wamp-proto/wamp-proto/issues/61 |
|   Adv. PubSub Features            | -             |               | -
|     Subscr. Black & Whitelisting  | stable        |               | [advanced/ap_pubsub_subscriber_blackwhite_listing.md](text/advanced/ap_pubsub_subscriber_blackwhite_listing.md) |  |
|     Publisher Exclusion           | stable        |               | [advanced/ap_pubsub_publisher_exclusion.md](text/advanced/ap_pubsub_publisher_exclusion.md) |  |
|     Publisher Identification      | alpha         |               | [advanced/ap_pubsub_publisher_identification.md](text/advanced/ap_pubsub_publisher_identification.md) |  |
|     Publication Trust Levels      | alpha         |               | [advanced/ap_pubsub_publication_trustlevels.md](text/advanced/ap_pubsub_publication_trustlevels.md) | https://github.com/wamp-proto/wamp-proto/issues/139  |
|     Subscription Meta-API         | beta          |               | [advanced/ap_pubsub_subscription_meta_api.md](text/advanced/ap_pubsub_subscription_meta_api.md) | https://github.com/wamp-proto/wamp-proto/issues/176, https://github.com/wamp-proto/wamp-proto/issues/169, https://github.com/wamp-proto/wamp-proto/issues/124, https://github.com/wamp-proto/wamp-proto/issues/55, https://github.com/wamp-proto/wamp-proto/issues/30  |
|     Pattern-based Subscriptions   | beta          |               | [advanced/ap_pubsub_pattern_based_subscription.md](text/advanced/ap_pubsub_pattern_based_subscription.md) | https://github.com/wamp-proto/wamp-proto/issues/174, https://github.com/wamp-proto/wamp-proto/issues/114 |
|     Sharded Subsciptions          | alpha         |               | [advanced/ap_pubsub_sharded_subscription.md](text/advanced/ap_pubsub_sharded_subscription.md) |  |
|     Event History                 | alpha         |               | [advanced/ap_pubsub_event_history.md](text/advanced/ap_pubsub_event_history.md) | https://github.com/wamp-proto/wamp-proto/issues/69, https://github.com/wamp-proto/wamp-proto/issues/43, https://github.com/wamp-proto/wamp-proto/issues/42 |
|     Subscription Revocation       |               |               | [advanced/ap_pubsub_subscription_revocation.md](text/advanced/ap_pubsub_subscription_revocation.md) |  |
|     Topic Reflection              | sketch        |               | [advanced/ap_pubsub_topic_reflection.md](text/advanced/ap_pubsub_topic_reflection.md) | https://github.com/wamp-proto/wamp-proto/issues/76, https://github.com/wamp-proto/wamp-proto/issues/61 |
|   Other Adv. Features             | -             |               | -
|     Session Meta-API              | beta          |               | [advanced/ap_session_meta_api.md](text/advanced/ap_session_meta_api.md) |  |
|     Authentication                | -             |               | [advanced/ap_authentication.md](text/advanced/ap_authentication.md) | https://github.com/wamp-proto/wamp-proto/issues/183, https://github.com/wamp-proto/wamp-proto/issues/143, https://github.com/wamp-proto/wamp-proto/issues/135, https://github.com/wamp-proto/wamp-proto/issues/99, https://github.com/wamp-proto/wamp-proto/issues/68, https://github.com/wamp-proto/wamp-proto/issues/57 |
|       Challenge-Response          | beta          |               | [advanced/ap_authentication_cra.md](text/advanced/ap_authentication_cra.md) | https://github.com/wamp-proto/wamp-proto/issues/164, https://github.com/wamp-proto/wamp-proto/issues/128, https://github.com/wamp-proto/wamp-proto/issues/100 |
|       Ticket                      | beta          |               | [advanced/ap_authentication_ticket.md](text/advanced/ap_authentication_ticket.md) | https://github.com/wamp-proto/wamp-proto/issues/70 |
|     Alternative Transports        | -             |               | [advanced/ap_transports.md](text/advanced/ap_transports.md) |  |
|       RawSocket                   | stable        |               | [advanced/ap_transport_rawsocket.md](text/advanced/ap_transport_rawsocket.md) |  |
|       Batched WebSocket           | sketch        |               | [advanced/ap_transport_batched_websocket.md](text/advanced/ap_transport_batched_websocket.md) |  |
|       HTTP Longpoll               | beta          |               | [advanced/ap_transport_http_longpoll.md](text/advanced/ap_transport_http_longpoll.md) |  |
|       Multiplexed                 | sketch        |               | [advanced/ap_transport_multiplexed.md](text/advanced/ap_transport_multiplexed.md) |  | |  |
| Binary Conversion of JSON Strings | stable        | polish        | [basic/bp_binary_conversion_of_json.md](text/basic/bp_binary_conversion_of_json.md) |  |
| Security Considerations           | -             | missing       | [main doc](draft-oberstet-hybi-tavendo-wamp.md) |  |
| Contributors                      | -             |               | [main doc](draft-oberstet-hybi-tavendo-wamp.md) |  |
| Acknowledgements                  | -             |               | [main doc](draft-oberstet-hybi-tavendo-wamp.md) |  |
| References                        | -             |               | [main doc](draft-oberstet-hybi-tavendo-wamp.md) |  |


not directly fitting into any of the sections, but still protocol related:

* https://github.com/wamp-proto/wamp-proto/issues/36

*Issues in this repository are covered up to 2015.10.17.*