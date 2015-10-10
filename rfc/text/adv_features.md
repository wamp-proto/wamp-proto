## Features

Support for advanced features must be announced by the peers which implement them. The following is a complete list of advanced features currently defined or proposed.

Status | Description
-------|--------------------------------------------------
sketch | There is a rough description of an itch to scratch, but the feature use case isn't clear, and there is no protocol proposal at all.
alpha  | The feature use case is still fuzzy and/or the feature definition is unclear, but there is at least a protocol level proposal.
beta   | The feature use case is clearly defined and the feature definition in the spec is sufficient to write a prototype implementation. The feature definition and details may still be incomplete and change.
stable | The feature definition in the spec is complete and stable and the feature use case is field proven in real applications. There are multiple, interoperatble implementations.


### RPC Features

| Feature                    | Status | P | B | S | Cr | D | Ce|
|----------------------------|--------|---|---|---|----|---|---|
| progressive_call_results   | beta   |   |   |   | X  | X | X |
| progressive_calls          | sketch |   |   |   | X  | X | X |
| call_timeout               | alpha  |   |   |   | X  | X | X |
| call_canceling             | alpha  |   |   |   | X  | X | X |
| caller_identification      | alpha  |   |   |   | X  | X | X |
| call_trustlevels           | alpha  |   |   |   |    | X | X |
| registration_meta_api      | beta   |   |   |   |    | X |   |
| pattern_based_registration | beta   |   |   |   |    | X | X |
| shared_registration        | beta   |   |   |   |    | X | X |
| sharded_registration       | alpha  |   |   |   |    | X | X |
| registration_revocation    | alpha  |   |   |   |    | X | X |
| procedure_reflection       | sketch |   |   |   |    | X |   |



### PubSub Features

| Feature                       | Status | P | B | S | Cr | D | Ce |
|-------------------------------|--------|---|---|---|----|---|----|
| subscriber_blackwhite_listing | stable | X | X |   |    |   |    |
| publisher_exclusion           | stable | X | X |   |    |   |    |
| publisher_identification      | alpha  | X | X | X |    |   |    |
| publication_trustlevels       | alpha  |   | X | X |    |   |    |
| session_meta_api              | beta   |   | X |   |    |   |    |
| subscription_meta_api         | beta   |   | X |   |    |   |    |
| pattern_based_subscription    | beta   |   | X | X |    |   |    |
| sharded_subscription          | alpha  |   | X | X |    |   |    |
| event_history                 | alpha  |   | X | X |    |   |    |
| topic_reflection              | sketch |   | X |   |    |   |    |


### Other Advanced Features

- authentication
    - WAMP CRA
    - cookie (entirely missing)
    - OTP --> ticket?
- transports
    - batched WS transport
    - longpoll transport
    - rawsocket transport
    - multiplexed transport
- pre-defined URIs
- reflection
- session meta-api


? 
- partitioned registration
- partitioned subscription
