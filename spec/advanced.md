# The Web Application Messaging Protocol

This document specifies the *Advanced Profile* of the [Web Application Messaging Protocol (WAMP)](http://wamp.ws/).

Document Revision: **RC4**, 2015/08/31

For the *Basic Profile*, please see [The Web Application Messaging Protocol, Part 1: Basic Profile](basic.md).

> Copyright (C) 2014-2015 [Tavendo GmbH](http://www.tavendo.com). Licensed under the [Creative Commons CC-BY-SA license](http://creativecommons.org/licenses/by-sa/3.0/). "WAMP", "Crossbar.io" and "Tavendo" are trademarks of Tavendo GmbH.


# Part 2: Advanced Profile

**Contents**

1. [Messages](#messages)
    * [Message Definitions](#message-definitions)
    * [Message Codes and Direction](#message-codes-and-direction)
2. [Advanced Features](#advanced-features)
3. [Alternative Transports](#alternative-transports)


## Preface

This is *part 2* of the WAMP specification. It describes advanced features and aspects of the protocol and its usage from the **WAMP Advanced Profile**.

This part as a whole is considered partially finished and unstable. Some features are presently underspecified. Features may yet be added or removed, and there is no guarantee that an existing feature in this part will remain unchanged.

Some features, however, are already specified and should remain unchanged. These are specifically marked as *STABLE*.

For an introduction to the protocol, and a description of basic features and usage that are part of the **WAMP Basic Profile**, please see [The Web Application Messaging Protocol, Part 1: Basic Profile](basic.md)


## Messages

WAMP Advanced Profile defines the following additional messages which are explained in detail in the following sections.

### Message Definitions

The following 5 message types are used in the WAMP Advanced Profile.

#### `CHALLENGE`

During authenticated session establishment, a *Router* sends a challenge message.

    [CHALLENGE, AuthMethod|string, Extra|dict]

#### `AUTHENTICATE`

A *Client* having received a challenge is expected to respond by sending a signature or token.

    [AUTHENTICATE, Signature|string, Extra|dict]

#### `CANCEL`

A *Caller* can cancel and issued call actively by sending a cancel message to the *Dealer*.

    [CANCEL, CALL.Request|id, Options|dict]

#### `INTERRUPT`

Upon receiving a cancel for a pending call, a *Dealer* will issue an interrupt to the *Callee*.

    [INTERRUPT, INVOCATION.Request|id, Options|dict]


### Message Codes and Direction

The following table list the message type code for **the OPTIONAL messages** defined in this part of the document and their direction between peer roles.

| Code | Message        |  Profile |  Publisher  |  Broker  |  Subscriber  |  Caller  |  Dealer  |  Callee  |
|------|----------------|----------|-------------|----------|--------------|----------|----------|----------|
|  4   | `CHALLENGE`    | advanced | Rx          | Tx       | Rx           | Rx       | Tx       | Rx       |
|  5   | `AUTHENTICATE` | advanced | Tx          | Rx       | Tx           | Tx       | Rx       | Tx       |
| 49   | `CANCEL`       | advanced |             |          |              | Tx       | Rx       |          |
| 69   | `INTERRUPT`    | advanced |             |          |              |          | Tx       | Rx       |

> "Tx" means the message is sent by the respective role, and "Rx" means the message is received by the respective role.


## Advanced Features

*Advanced features* need to be announced by the peer which implements them. The complete list of *advanced features* currently defined or proposed per role is:

| Feature                                                         |  Publisher  |  Broker  |  Subscriber  |  Caller  |  Dealer  |  Callee  |
|-----------------------------------------------------------------|-------------|----------|--------------|----------|----------|----------|
| **Remote Procedure Calls**                                      |             |          |              |          |          |          |
|                                                                 |             |          |              |          |          |          |
| [caller_identification](advanced/caller-identification.md)      |             |          |              | X        | X        | X        |
| [call_trustlevels]()                                            |             |          |              |          | X        | X        |
| [pattern_based_registration]()                                  |             |          |              |          | X        | X        |
| [session_meta_api]()                                            |             |          |              |          | X        |          |
| [registration_meta_api]()                                       |             |          |              |          | X        |          |
| [shared_registration]()                                         |             |          |              |          | X        | X        |
| [call_timeout]()                                                |             |          |              | X        | X        | X        |
| [call_canceling]()                                              |             |          |              | X        | X        | X        |
| [progressive_call_results]()                                    |             |          |              | X        | X        | X        |
|                                                                 |             |          |              |          |          |          |
| **Publish & Subscribe**                                         |             |          |              |          |          |          |
|                                                                 |             |          |              |          |          |          |
| [publisher_identification]()                                    | X           | X        | X            |          |          |          |
| [publication_trustlevels]()                                     |             | X        | X            |          |          |          |
| [pattern_based_subscription]()                                  |             | X        | X            |          |          |          |
| [session_meta_api]()                                            |             | X        |              |          |          |          |
| [subscription_meta_api]()                                       |             | X        |              |          |          |          |
| [subscriber_blackwhite_listing]()                               | X           | X        |              |          |          |          |
| [publisher_exclusion]()                                         | X           | X        |              |          |          |          |
| [event_history]()                                               |             | X        | X            |          |          |          |


## Alternative Transports

As mentioned in the [Basic Profile](basic.md), the only requirements that WAMP expects from a transport are: the transport must be message-based, bidirectional, reliable and ordered. This allows WAMP to run over different transports without any impact at the application layer.

Besides the WebSocket transport, the following WAMP transports are currently specified:

* [RawSocket Transport](advanced/rawsocket-transport.md)
* [Batched WebSocket Transport](advanced/batched-websocket-transport.md)
* [LongPoll Transport](advanced/longpoll-transport.md)
* [Multiplexed Transport](advanced/multiplexed-transport.md)

> Other transports such as HTTP 2.0 ("SPDY") or UDP might be defined in the future.
