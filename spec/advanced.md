# The Web Application Messaging Protocol

This document specifies the *Advanced Profile* of the [Web Application Messaging Protocol (WAMP)](http://wamp.ws/).

Document Revision: **2015/09/01**

For the *Basic Profile*, please see [The Web Application Messaging Protocol, Part 1: Basic Profile](basic.md).

> Copyright (C) 2014-2015 [Tavendo GmbH](http://www.tavendo.com). Licensed under the [Creative Commons CC-BY-SA license](http://creativecommons.org/licenses/by-sa/3.0/). "WAMP", "Crossbar.io" and "Tavendo" are trademarks of Tavendo GmbH.


# Part 2: Advanced Profile

**Contents**

1. [Messages](#messages)
    * [Message Definitions](#message-definitions)
    * [Message Codes and Direction](#message-codes-and-direction)
2. [Advanced Features](#advanced-features)
3. [Alternative Transports](advanced/transports.md)
4. [Authentication Methods](advanced/authentication.md)


## Preface

This is **part 2** of the WAMP specification. It describes advanced features and aspects of the protocol and its usage from the **WAMP Advanced Profile**.

This part as a whole is considered partially finished and unstable. Some features are presently underspecified. Features may yet be added or removed, and there is no guarantee that an existing feature in this part will remain unchanged.

Some features, however, are already specified and should remain unchanged. These are specifically marked as *STABLE*.

For an introduction to the protocol, and a description of basic features and usage that are part of the **WAMP Basic Profile**, please see [The Web Application Messaging Protocol, Part 1: Basic Profile](basic.md)


## Messages

WAMP Advanced Profile defines the following additional messages which are explained in detail in separate sections.

### Message Definitions

The following 4 additional message types are used in the WAMP Advanced Profile.

#### `CHALLENGE`

The `CHALLENGE` message is used with certain [Authentication Methods](advanced/authentication.md). During authenticated session establishment, a **Router** sends a challenge message.

    [CHALLENGE, AuthMethod|string, Extra|dict]

#### `AUTHENTICATE`

The `AUTHENTICATE` message is used with certain [Authentication Methods](advanced/authentication.md). A **Client** having received a challenge is expected to respond by sending a signature or token.

    [AUTHENTICATE, Signature|string, Extra|dict]

#### `CANCEL`

The `CANCEL` message is used with the [Call Canceling](advanced/call-canceling.md) advanced feature. A *Caller* can cancel and issued call actively by sending a cancel message to the *Dealer*.

    [CANCEL, CALL.Request|id, Options|dict]

#### `INTERRUPT`

The `INTERRUPT` message is used with the [Call Canceling](advanced/call-canceling.md) advanced feature. Upon receiving a cancel for a pending call, a *Dealer* will issue an interrupt to the *Callee*.

    [INTERRUPT, INVOCATION.Request|id, Options|dict]


### Message Codes and Direction

The following table list the message type code for **the OPTIONAL messages** defined in this part of the document and their direction between peer roles.

| Code | Message        |  Profile |  Publisher  |  Broker  |  Subscriber  |  Caller  |  Dealer  |  Callee  |
|------|----------------|----------|-------------|----------|--------------|----------|----------|----------|
|  4   | `CHALLENGE`    | advanced | Rx          | Tx       | Rx           | Rx       | Tx       | Rx       |
|  5   | `AUTHENTICATE` | advanced | Tx          | Rx       | Tx           | Tx       | Rx       | Tx       |
| 49   | `CANCEL`       | advanced |             |          |              | Tx       | Rx       |          |
| 69   | `INTERRUPT`    | advanced |             |          |              |          | Tx       | Rx       |

> "Tx" ("Rx") means the message is sent (received) by a peer of the respective role.

---


## Advanced Features

Support for advanced features must be announced by the peers which implement them. The following is a complete list of advanced features currently defined or proposed.

Status | Description
---|---
sketch | There is a rough description of an itch to scratch, but the feature use case isn't clear, and there is no protocol proposal at all.
alpha | The feature use case is still fuzzy and/or the feature definition is unclear, but there is at least a protocol level proposal.
beta | The feature use case is clearly defined and the feature definition in the spec is sufficient to write a prototype implementation. The feature definition and details may still be incomplete.
stable | The feature definition in the spec is complete and stable and the feature use case is field proven in real applications. There are multiple, interoperatble implementations.

### Advanced RPC Features

| Feature                                                                    |  Status   |  Publisher  |  Broker  |  Subscriber  |  Caller  |  Dealer  |  Callee  |
|----------------------------------------------------------------------------|-----------|-------------|----------|--------------|----------|----------|----------|
| [progressive_call_results](advanced/progressive-call-results.md)           |**stable** |             |          |              | X        | X        | X        |
| [progressive_calls](advanced/progressive-calls.md)                         | alpha     |             |          |              | X        | X        | X        |
| [call_timeout](advanced/call-timeout.md)                                   | alpha     |             |          |              | X        | X        | X        |
| [call_canceling](advanced/call-canceling.md)                               | alpha     |             |          |              | X        | X        | X        |
| [caller_identification](advanced/caller-identification.md)                 | alpha     |             |          |              | X        | X        | X        |
| [call_trustlevels](advanced/call-trustlevels.md)                           | alpha     |             |          |              |          | X        | X        |
| [session_meta_api](advanced/session-meta-api.md)                           | beta      |             |          |              |          | X        |          |
| [registration_meta_api](advanced/registration-meta-api.md)                 | beta      |             |          |              |          | X        |          |
| [pattern_based_registration](advanced/pattern-based-registration.md)       | beta      |             |          |              |          | X        | X        |
| [shared_registration](advanced/shared-registration.md)                     | beta      |             |          |              |          | X        | X        |
| [sharded_registration](advanced/sharded-registration.md)                   | alpha     |             |          |              |          | X        | X        |
| [registration_revocation](advanced/registration-revocation.md)             | alpha     |             |          |              |          | X        | X        |
| [procedure_reflection](advanced/procedure-reflection.md)                   | sketch    |             |          |              |          | X        |          |

### Advanced PubSub Features

| Feature                                                                    |  Status   |  Publisher  |  Broker  |  Subscriber  |  Caller  |  Dealer  |  Callee  |
|----------------------------------------------------------------------------|-----------|-------------|----------|--------------|----------|----------|----------|
| [subscriber_blackwhite_listing](advanced/subscriber-blackwhite-listing.md) |**stable** | X           | X        |              |          |          |          |
| [publisher_exclusion](advanced/publisher-exclusion.md)                     |**stable** | X           | X        |              |          |          |          |
| [publisher_identification](advanced/publisher-identification.md)           | alpha     | X           | X        | X            |          |          |          |
| [publication_trustlevels](advanced/publication-trustlevels.md)             | alpha     |             | X        | X            |          |          |          |
| [session_meta_api](advanced/session-meta-api.md)                           | beta      |             | X        |              |          |          |          |
| [subscription_meta_api](advanced/subscription-meta-api.md)                 | beta      |             | X        |              |          |          |          |
| [pattern_based_subscription](advanced/pattern-based-subscription.md)       | beta      |             | X        | X            |          |          |          |
| [sharded_subscription](advanced/sharded-subscription.md)                   | alpha     |             | X        | X            |          |          |          |
| [event_history](advanced/event-history.md)                                 | alpha     |             | X        | X            |          |          |          |
| [topic_reflection](advanced/topic-reflection.md)                           | sketch    |             | X        |              |          |          |          |

---
