## Message Definitions

The Advanced Profile defines additional WAMP-level messages which are explained in detail in separate sections. The following 4 additional message types MAY be used in the Advanced Profile and their direction between peer roles.


### Advanced Sessions

#### CHALLENGE

The `CHALLENGE` message is used with certain Authentication Methods. During authenticated session establishment, a **Router** sends a challenge message.

{align="left"}
        [CHALLENGE, AuthMethod|string, Extra|dict]

#### AUTHENTICATE

The `AUTHENTICATE` message is used with certain Authentication Methods. A **Client** having received a challenge is expected to respond by sending a signature or token.

{align="left"}
        [AUTHENTICATE, Signature|string, Extra|dict]

### Advanced Remote Procedure Calls

#### CANCEL

The `CANCEL` message is used with the Call Canceling advanced feature. A *Caller* can cancel and issued call actively by sending a cancel message to the *Dealer*.

{align="left"}
        [CANCEL, CALL.Request|id, Options|dict]

#### INTERRUPT

The `INTERRUPT` message is used with the Call Canceling advanced feature. Upon receiving a cancel for a pending call, a *Dealer* will issue an interrupt to the *Callee*.

{align="left"}
        [INTERRUPT, INVOCATION.Request|id, Options|dict]


### Message Codes and Direction

Here, "Tx" ("Rx") means the message is sent (received) by a peer of the respective role.

{align="left"}
| Code | Message        | Publisher | Broker | Subscriber | Caller | Dealer | Callee |
|------|----------------|-----------|--------|------------|--------|--------|--------|
|  4   | `CHALLENGE`    | Rx        | Tx     | Rx         | Rx     | Tx     | Rx     |
|  5   | `AUTHENTICATE` | Tx        | Rx     | Tx         | Tx     | Rx     | Tx     |
|      |                |           |        |            |        |        |        |
| 49   | `CANCEL`       |           |        |            | Tx     | Rx     |        |
| 69   | `INTERRUPT`    |           |        |            |        | Tx     | Rx     |
