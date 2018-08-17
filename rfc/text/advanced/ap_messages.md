## Messages

The Advanced Profile defines the following additional messages which are explained in detail in separate sections.

### Message Definitions

The following 4 additional message types MAY be used in the Advanced Profile.

#### CHALLENGE

The `CHALLENGE` message is used with certain Authentication Methods. During authenticated session establishment, a **Router** sends a challenge message.

{align="left"}
        [CHALLENGE, AuthMethod|string, Extra|dict]

#### AUTHENTICATE

The `AUTHENTICATE` message is used with certain Authentication Methods. A **Client** having received a challenge is expected to respond by sending a signature or token.

{align="left"}
        [AUTHENTICATE, Signature|string, Extra|dict]

#### CANCEL

The `CANCEL` message is used with the Call Canceling advanced feature. A *Caller* can cancel and issued call actively by sending a cancel message to the *Dealer*.

{align="left"}
        [CANCEL, CALL.Request|id, Options|dict]

#### INTERRUPT

The `INTERRUPT` message is used with the Call Canceling advanced feature. Upon receiving a cancel for a pending call, a *Dealer* will issue an interrupt to the *Callee*.

{align="left"}
        [INTERRUPT, INVOCATION.Request|id, Options|dict]

### Message Codes and Direction

The following table list the message type code for **the OPTIONAL messages** defined in this part of the document and their direction between peer roles.

{align="left"}
| Cod | Message        |  Pub |  Brk | Subs |  Calr |  Dealr | Callee|
|-----|----------------|------|------|------|-------|--------|-------|
|  4  | `CHALLENGE`    | Rx   | Tx   | Rx   | Rx    | Tx     | Rx    |
|  5  | `AUTHENTICATE` | Tx   | Rx   | Tx   | Tx    | Rx     | Tx    |
| 49  | `CANCEL`       |      |      |      | Tx    | Rx     |       |
| 69  | `INTERRUPT`    |      |      |      |       | Tx     | Rx    |


> "Tx" ("Rx") means the message is sent (received) by a peer of the respective role.
