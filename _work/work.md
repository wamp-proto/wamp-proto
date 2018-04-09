- this document contains draft blocks of text which transform the WAMP spec into RFC language


# Sessions

The message flow between *Clients* and *Routers* for opening and closing WAMP sessions involves the following messages:

1. `HELLO`
2. `WELCOME`
3. `ABORT`
4. `GOODBYE`

A WAMP session starts its lifetime when the *Router* has sent a `WELCOME` message to the *Client*, and ends when the underlying transport closes or when the session is closed explicitly by either peer sending the `GOODBYE` message (see below).



-- to add somewhere towards the beginning, probably the introduction or design princinples, since this is not directly normative ---


### Role and Feature Announcement

WAMP uses *Role & Feature announcement* instead of *protocol versioning* to allow

* implementations only supporting subsets of functionality
* future extensibility

Both a *Client* and the *Router* announces the *Roles* they support. Under a future Advanced Profile, both may announce particular features which they implement for a specific role.

--------

## Session Establishment

### HELLO

Once the underlying transport has been established, a WAMP session MUST be initiated by the *Client* sending a 'HELLO' message to the *Router*. 

The client MUST NOT send any other WAMP message previous to this, and the *Router* must drop the transport to the *Client* if this is violated.

It is a protocol error to receive a second `HELLO` message during the lifetime of the session and the *Peer* MUST fail the session if this happens.

The `HELLO` message MUST conform to the following structure

{align="left"}
        [HELLO, Realm|uri, Details|dict]

where 

* `Realm` MUST be a string identifying the realm this session should attach to
* `Details` MUST be a dictionary that MUST announce the *Roles* the *Client* supports, and MAY provide additional information (see below).

A *Client* MUST announce support for at least one *Role*, and *MAY* announce support for any number an combinations of roles beyond that. 

Announcement of *Roles* is via a key in the `Hello.Details.roles` dictionary, where the key can be:

* `publisher`
* `subscriber`
* `caller`
* `callee`

The value for each used key is a dictionary that in the WAMP basic profile is empty, but under a future WAMP Advanced Profile may contain announcements for Advanced Profile features which an implementation supports for the particular role.

*Example: A Client that implements the Publisher and Subscriber roles of the WAMP Basic Profile.*

{align="left"}
        [1, "somerealm", {
          "roles": {
              "publisher": {},
              "subscriber": {}
          }
        }]


In the WAMP Basic Profile without any WAMP-level session authentication mechanism, the *Router* MUST reply with either a `WELCOME` or an `ABORT` message.

In a future Advanced Profile, intermediate steps may be introduced for the purpose of a WAMP-level authentication. Such steps will rely on the presence of information in the `Details`. Intermediate steps MUST NOT occur if the client does not send such information in the `Details`.

A *Router* SHOULD send a `WELCOME` message if the `HELLO` message by the *Client* was error-free, else it MUST send an `ABORT` message.

> Note. The behavior if a requested *Realm* does not presently exist is router-specific. A router may e.g. automatically create the realm, or deny the establishment of the session with a `ABORT` reply message.
>

### WELCOME

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

The `WELCOME` message MUST conform to the following structure

{align="left"}
        [WELCOME, Session|id, Details|dict]

where

* `Session` MUST be a randomly generated ID specific to the WAMP session. This applies for the lifetime of the session.
* `Details` MUST be a dictionary that MUST announce the *Roles* the *Router* supports, and MAY provide additional information (see below).

The *Router* MUST announce support for at least one *Role*, and MAY announce support for both *Router* roles.

Announcement of *Roles* is via a key in the `Welcome.Details.roles` dictionary, where the key can be:

* `broker`
* `dealer

The value for each used key is a dictionary that in the WAMP basic profile is empty, but under a future WAMP Advanced Profile may contain announcements for Advanced Profile features which an implementation supports for the particular role.

*Example: A Router implementing the Broker role of the WAMP Basic Profile.*

{align="left"}
        [2, 9129137332, {
           "roles": {
              "broker": {}
           }
        }]


### ABORT


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



## Session Closing