# Sessions

The message flow between Clients and Routers for opening and closing WAMP sessions involves the following messages:

1. `HELLO`
2. `WELCOME`
3. `ABORT`
4. `GOODBYE`

## Session Establishment

### HELLO

After the underlying transport has been established, the opening of a WAMP session is initiated by the Client sending a `HELLO` message to the Router

{align="left"}
        [HELLO, Realm|uri, Details|dict]

where

* `Realm` is a string identifying the realm this session should attach to
* `Details` is a dictionary that allows to provide additional opening information (see below).

The `HELLO` message MUST be the very first message sent by the Client after the transport has been established.

In the WAMP Basic Profile without session authentication the Router will reply with a `WELCOME` or `ABORT` message.

{align="left"}
        ,------.          ,------.
        |Client|          |Router|
        `--+---'          `--+---'
           |      HELLO      |
           | ---------------->
           |                 |
           |     WELCOME     |
           | <----------------
        ,--+---.          ,--+---.
        |Client|          |Router|
        `------'          `------'


A WAMP session starts its lifetime when the Router has sent a `WELCOME` message to the Client, and ends when the underlying transport closes or when the session is closed explicitly by either peer sending the `GOODBYE` message (see below).

It is a [protocol error](#protocol_error) to receive a second `HELLO` message during the lifetime of the session and the Peer MUST close the session if that happens.

#### Client: Role and Feature Announcement

WAMP uses *Role & Feature announcement* instead of *protocol versioning* to allow

* implementations only supporting subsets of functionality
* future extensibility

A Client must announce the roles it supports via `Hello.Details.roles|dict`, with a key mapping to a `Hello.Details.roles.<role>|dict` where `<role>` can be:

* `publisher`
* `subscriber`
* `caller`
* `callee`

A Client can support any combination of the above roles but must support at least one role.

The `<role>|dict` is a dictionary describing features supported by the peer for that role.

This MUST be empty for WAMP Basic Profile implementations, and MUST be used by implementations implementing parts of the Advanced Profile to list the specific set of features they support.

*Example: A Client that implements the Publisher and Subscriber roles of the WAMP Basic Profile.*

{align="left"}
        [1, "somerealm", {
          "roles": {
              "publisher": {},
              "subscriber": {}
          }
        }]

### WELCOME

A Router completes the opening of a WAMP session by sending a `WELCOME` reply message to the Client.

{align="left"}
        [WELCOME, Session|id, Details|dict]

where

* `Session` MUST be a randomly generated ID specific to the WAMP session. This applies for the lifetime of the session.
* `Details` is a dictionary that allows to provide additional information regarding the open session (see below).

In the WAMP Basic Profile without session authentication, a `WELCOME` message MUST be the first message sent by the Router, directly in response to a `HELLO` message received from the Client. Extensions in the Advanced Profile MAY include intermediate steps and messages for authentication.

> Note. The behavior if a requested `Realm` does not presently exist is router-specific. A router may e.g. automatically create the realm, or deny the establishment of the session with a `ABORT` reply message.
>

#### Router: Role and Feature Announcement

Similar to a Client announcing Roles and Features supported in the ``HELLO` message, a Router announces its supported Roles and Features in the `WELCOME` message.

A Router MUST announce the roles it supports via `Welcome.Details.roles|dict`, with a key mapping to a `Welcome.Details.roles.<role>|dict` where `<role>` can be:

* `broker`
* `dealer`

A Router must support at least one role, and MAY support both roles.

The `<role>|dict` is a dictionary describing features supported by the peer for that role. With WAMP Basic Profile implementations, this MUST be empty, but MUST be used by implementations implementing parts of the Advanced Profile to list the specific set of features they support

*Example: A Router implementing the Broker role of the WAMP Basic Profile.*

{align="left"}
        [2, 9129137332, {
           "roles": {
              "broker": {}
           }
        }]

### ABORT

Both the Router and the Client may abort the opening of a WAMP session by sending an `ABORT` message.

{align="left"}
        [ABORT, Details|dict, Reason|uri]

where

* `Reason` MUST be an URI.
* `Details` MUST be a dictionary that allows to provide additional, optional closing information (see below).

No response to an `ABORT` message is expected.

{align="left"}
        ,------.          ,------.
        |Client|          |Router|
        `--+---'          `--+---'
           |      HELLO      |
           | ---------------->
           |                 |
           |      ABORT      |
           | <----------------
        ,--+---.          ,--+---.
        |Client|          |Router|
        `------'          `------'


*Example*

{align="left"}
        [3, {"message": "The realm does not exist."},
            "wamp.error.no_such_realm"]


## Session Closing

A WAMP session starts its lifetime with the Router sending a `WELCOME` message to the Client and ends when the underlying transport disappears or when the WAMP session is closed explicitly by a `GOODBYE` message sent by one Peer and a `GOODBYE` message sent from the other Peer in response.

{align="left"}
        [GOODBYE, Details|dict, Reason|uri]

where

* `Reason` MUST be an URI.
* `Details` MUST be a dictionary that allows to provide additional, optional closing information (see below).

{align="left"}
        ,------.          ,------.
        |Client|          |Router|
        `--+---'          `--+---'
           |     GOODBYE     |
           | ---------------->
           |                 |
           |     GOODBYE     |
           | <----------------
        ,--+---.          ,--+---.
        |Client|          |Router|
        `------'          `------'


{align="left"}
        ,------.          ,------.
        |Client|          |Router|
        `--+---'          `--+---'
           |     GOODBYE     |
           | <----------------
           |                 |
           |     GOODBYE     |
           | ---------------->
        ,--+---.          ,--+---.
        |Client|          |Router|
        `------'          `------'

*Example*. One Peer initiates closing

{align="left"}
        [6, {"message": "The host is shutting down now."},
            "wamp.error.system_shutdown"]

and the other peer replies

{align="left"}
        [6, {}, "wamp.error.goodbye_and_out"]


*Example*. One Peer initiates closing

{align="left"}
        [6, {}, "wamp.error.close_realm"]

and the other peer replies

{align="left"}
        [6, {}, "wamp.error.goodbye_and_out"]


### Difference between ABORT and GOODBYE

The differences between `ABORT` and `GOODBYE` messages are:

1. `ABORT` gets sent only *before* a Session is established, while `GOODBYE` is sent only *after* a Session is already established.
2. `ABORT` is never replied to by a Peer, whereas `GOODBYE` must be replied to by the receiving Peer

> Though `ABORT` and `GOODBYE` are structurally identical, using different message types serves to reduce overloaded meaning of messages and simplify message handling code.
>


### Session Statechart

The following state chart gives the states that a WAMP peer can be in during the session lifetime cycle.

{align="left"}
                             +--------------+                           
    +--------(6)------------->              |                           
    |                        | CLOSED       <--------------------------+
    | +------(4)------------->              <---+                      |
    | |                      +--------------+   |                      |
    | |                               |         |                      |
    | |                              (1)       (7)                     |
    | |                               |         |                      |
    | |                      +--------v-----+   |                   (11)
    | |                      |              +---+                      |
    | |         +------------+ ESTABLISHING +----------------+         |
    | |         |            |              |                |         |
    | |         |            +--------------+                |         |
    | |         |                     |                     (10)       |
    | |         |                    (9)                     |         |
    | |         |                     |                      |         |
    | |        (2)           +--------v-----+       +--------v-------+ |
    | |         |            |              |       |                | |
    | |         |     +------> FAILED       <--(13)-+ CHALLENGING /  +-+
    | |         |     |      |              |       | AUTHENTICATING |  
    | |         |     |      +--------------+       +----------------+  
    | |         |    (8)                                     |          
    | |         |     |                                      |          
    | |         |     |                                      |          
    | | +-------v-------+                                    |          
    | | |               <-------------------(12)-------------+          
    | | | ESTABLISHED   |                                               
    | | |               +--------------+                                
    | | +---------------+              |                                
    | |         |                      |                                
    | |        (3)                    (5)                               
    | |         |                      |                                
    | | +-------v-------+     +--------v-----+                          
    | | |               +--+  |              |                          
    | +-+ SHUTTING DOWN |  |  | CLOSING      |                          
    |   |               |(14) |              |                          
    |   +-------^-------+  |  +--------------+                          
    |           |----------+           |                                
    +----------------------------------+     


| #  |  State                                                        |
|----|---------------------------------------------------------------|
| 1  | Sent HELLO                                                    |
| 2  | Received WELCOME                                              |
| 3  | Sent GOODBYE                                                  |
| 4  | Received GOODBYE                                              |
| 5  | Received GOODBYE                                              |
| 6  | Sent GOODBYE                                                  |
| 7  | Received invalid HELLO / Send ABORT                           |
| 8  | Received HELLO or AUTHENTICATE                                |
| 9  | Received other                                                |
| 10 | Received valid HELLO [needs authentication] / Send CHALLENGE  |
| 11 | Received invalid AUTHENTICATE / Send ABORT                    |
| 12 | Received valid AUTHENTICATE / Send WELCOME                    |
| 13 | Received other                                                |
| 14 | Received other / ignore                                       |




# Agent Identification

When a software agent operates in a network rotocol, it often identifies itself, its application type, operating system, software vendor, or software revision, by submitting a characteristic identification string to its operating peer.

Similar to what browsers do with the `User-Agent` HTTP header, both the `HELLO` and the `WELCOME` message MAY disclose the WAMP implementation in use to its peer:

{align="left"}
        HELLO.Details.agent|string

and

{align="left"}
        WELCOME.Details.agent|string

*Example: A Client "HELLO" message.*

{align="left"}
        [1, "somerealm", {
             "agent": "AutobahnJS-0.9.14",
             "roles": {
                "subscriber": {},
                "publisher": {}
             }
        }]


*Example: A Router "WELCOME" message.*

{align="left"}
        [2, 9129137332, {
            "agent": "Crossbar.io-0.10.11",
            "roles": {
              "broker": {}
            }
        }]
