# Intro

Lifetimes of WAMP *Sessions* and WAMP *Transports* are independent of each other.

A *Transport* may outlive the lifetime of a *Session*, and a *Session* can exist without a *Transport* being currently attached.

Usually, a WAMP client will establish a new *Transport* connecting to a *Router*, create a new *Session*, attach the *Transport* to the *Session* and then perform an initial authentication handshake joining a *Realm* on the *Router*. After that, the *Session* can be used for PubSub and RPC.

The *Session* can leave the *Realm*, and join a different *Realm*, performing a new (different) authentication handshake.

The *Session* can also be **paused (frozen)**, when the *Transport* is lost or actively **detached** from the *Session*. In this case, the *Router* is expected to retain it's router-side *Session* representation and allow the client to reconnect, and **resume** the *Session*.


# Client Session

## Session States

* `DETATHED-NONRESUMABLE` ("`DETACHED`")
* `DETACHED-RESUMABLE` ("`DETACHED`")
* `ATTACHED-NONRESUMABLE` ("`ATTACHED`")
* `ATTACHED-RESUMABLE` ("`ATTACHED`")

## Realm States (in-session)

* `UNJOINED`
* `JOINING`
* `JOINED`

## Transport States

* `DISCONNECTED`
* `CONNECTED`
* `ATTACHED`


## Behavior

A WAMP *Session* has a client side representation, and a router side representation. The following describes the behavior of a client *Session* by defining a state machine.


### Transport establishment and relation to Sessions

A *Client* establishes a *Transport* to a *Router* (going from `DISCONNECTED` to `CONNECTED`). The details of transport establishment (and any state machines used for transports) are independent of the *Session*.

When a *Transport* has been established and is `CONNECTED`, the transport can be **attached** to a *Session* (going from `CONNECTED` to `ATTACHED`).

A *Transport* can be unattached or attached to a single *Session* - it cannot be attached to more than one *Session* at the same time.

A *Multiplexed Transport* will expose the multiplexed transports running over the single "physical" transport as individual, fully independent *Transports*.

A *Transport* may be detached from a *Session* (going from `ATTACHED` to `CONNECTED`) and attached to a different *Session* or attached to the original *Session* again.

When a *Transport* is disconnected, either deliberately (from the client, the router or from an intermediary) or when the transport connection is lost, the *Transport* is automatically detached from any *Session* it is attached to (if the transport was attached to a session at all) (the transport going from `ATTACHED` to `DISCONNECTED`, and the Session going from one of the `ATTACHED` states to the respective `DETACHED` state).

When a *Transport* is attached to a *Session*, the *Session* can move into the `ATTACHED-NONRESUMABLE` state (when the session cannot be resumed and has to go through a full authentication handshake to join a realm), or move into the `ATTACHED-RESUMABLE` state (when the session can be resumed)


## Session Pause and Resume

A client is not resuming from a previous session, but supports resuming is sending a `HELLO` message

    [HELLO, Realm|uri, Details|dict]

For example:

```json
[
    1,
    "realm1",
    {
        "roles": ...,
        "authmethods": ["anonymous"],
        "resumable": true
    }
]
```

The client is announcing the fact that it supports and wants to use session resuming by setting `"resumable": true` in the `Details|dict`.

When the router is accepting the client, supports resuming and is also willing to allow future client session to resume, it will answer

    [WELCOME, Session|id, Details|dict]

For example:

```json
[
    2,
    657683631,
    {
        "realm": "realm1",
        "authid": "nobody",
        "authrole": "anonymous",
        "authprovider": "static",
        "authextra": {},

        "resumed": false,
        "resumable": true,
        "resume-token": "mazdJ5q6PLHkEbR3WdJzwA=="
    }
]
```

> A missing attribute `resumed` in `WELCOME.Details` or an attribute value of `null` both are equivalent to an attribute value of `false`. The same applies to attribute `resumable`. If `resumable == true`, the `resume-token` MUST be present - see also below.

If no authmethods are provided and no realm is provided in the `HELLO` message, a session that is not joined to any realm is created. For example:

```json
[
    2,
    657683631,
    {
        "realm": null,

        "resumed": false,
        "resumable": true,
        "resume-token": "mazdJ5q6PLHkEbR3WdJzwA=="
    }
]
```

Here is an example message exchange started by a client sending a `HELLO` message, resuming session ID `657683631` using resume token `2xqzPLsm+wuG5nsZhgNLAK70plE=`. A resuming client is sending a `HELLO` message

    [HELLO, Realm|uri, Details|dict]

For example:


```json
[
    1,
    null,
    {
        "resume-session": 657683631,
        "resume-token": "mazdJ5q6PLHkEbR3WdJzwA=="
    }
]
```

The client is using the `resume-token` that it previously received from the router for session resuming. A `resume-token` MUST be a Base64 encoded string of a 16 octet random token. The token must be a cryptographically strong high quality random value.

Note how the `HELLO` message has left out **all** unnecessary information that would be present in a `HELLO` message of a non-resuming session. This serves to minimize the wire level overhead when resuming sessions:

```console
Python 3.5.1 (default, Apr 18 2016, 22:23:23)
[GCC 4.8.5] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import cbor
>>> import json
>>> len(json.dumps([1, None, {u"resume-session": 657683631, u"resume-token": u"mazdJ5q6PLHkEbR3WdJzwA=="}]))
84
>>> len(cbor.dumps([1, None, {u"resume-session": 657683631, u"resume-token": u"mazdJ5q6PLHkEbR3WdJzwA=="}]))
63
>>>
```

A *Router*, upon receiving a `HELLO` message from the client asking for resuming a session will lookup the `resume-session` ID in it's map of paused session. If the session is found and the `resume-token` provided by the client matches, the *Router* will unpause the router side representation of the *Session*, generate a new `resume-token` (if the router is willing to let the client resume again later) and send a `WELCOME` message

    [WELCOME, Session|id, Details|dict]

For example:

```json
[
    2,
    657683631,
    {
        "resumed": true,
        "resumable": true,
        "resume-token": "Jv/p47RxBzj2U0LK7/rCyQ=="
    }
]
```

The `WELCOME` message for a resuming session is again minimized for size:

```console
Python 3.5.1 (default, Apr 18 2016, 22:23:23)
[GCC 4.8.5] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import cbor
>>> import json
>>> len(json.dumps([2, 657683631, {"resumed": True, "resumable": True, "resume-token": "Jv/p47RxBzj2U0LK7/rCyQ=="}]))
97
>>> len(cbor.dumps([2, 657683631, {"resumed": True, "resumable": True, "resume-token": "Jv/p47RxBzj2U0LK7/rCyQ=="}]))
68
>>>
```

**Joining**

To initiate a new authentication handshake, a *Session* in the `ATTACHED` state and with an `UNJOINED` realm state sends a `JOIN` message to the *Router* and starts a **authentication handshake completion timer**.

    [JOIN, Realm|uri, Details|dict]

Using `Realm|uri`, the client anounces the realm it wishes to join.

The `uri` MUST be a proper WAMP URI. The *Router* MUST **fail the connection** when the `uri` is not a valid WAMP URI.

The `Realm|uri` MAY be `null`, when the *Router* support dynamic realm assignment.

The `Details` dict may include authentication information, similar to `HELLO`, and `Challenge`/`Authenticate` packets may be sent to provide challenge based authentication, like a `HELLO`.

The *Session* realm state will then move from `UNJOINED` to `JOINING` whilst it waits for the following message.

The *Router*, if it accepts this `JOIN`, will send a `JOINED` message:

    [JOINED, Realm|uri, Details|dict]

The `Details` dict may contain authentication details like the `WELCOME` packet.

The *Session* realm state will then move from `JOINING` to the `JOINED` state on success.

If the *Router* does not accept this `JOIN`, it will respond with an `ABORT`.

**Leaving**

TODO: Router-initiated session quits? Maybe just destroy the session.

An attached *Session* in the `JOINED` realm state can leave the realm it is joined to by sending a `LEAVE` message to the *Router*.

    [LEAVE, Details|dict]

The *Router* will then respond with a `LEFT` message to confirm:

    [LEFT, Details|dict]

This then moves the *Session* realm state into `UNJOINED`.

**Pausing**

A *Session* in the `ATTACHED-RESUMABLE` state may pause (freeze) a *Session* by sending a `GOODBYE` packet to the *Router* requesting later resumption:

    [GOODBYE, Details|dict, Reason|uri]

For example:

```json
[
    6,
    {
        "resumable": true
    },
    "wamp.close.normal"
]
```

A *Router* will then respond to the client with a `GOODBYE` with `Goodbye.Details.resumable` being `true` if the session is resumable later, or `false` if the session will not be able to be resumed (for example, administrative reasons).

Lack of `Goodbye.Details.resumable` sent from either the client or the Router MUST be interpreted as a `false` value.

**Resuming**

When the *Session* has been previously joined a realm, and then the transport was lost or actively detached from the session, and the *Router* supports session pause/resume, the *Session* will have received


**Router-initiated Disconnection**

A *Router* may signal to a client that it wishes to detatch the `ATTACHED-RESUMABLE` *Session* from the *Transport* (for example, to shut down the Transport).
To do this, a *Router* sends a `GOODBYE`:

```json
[
    6,
    {
        "resumable": true
    },
    "wamp.error.system_shutdown"
]
```

It uses the `Goodbye.Details.resumable` flag to communicate whether a client will be able to reconnect to the session later.
This may be different to what was provided in the `WELCOME` message for administrative reasons (for example, a complete system shutdown on a router that does not have persistent session storage).

Lack of `Goodbye.Details.resumable` sent from either the client or the Router MUST be interpreted as a `false` value.

**Closing**

If a *Router* receives a `GOODBYE` on a *Session* that is `ATTACHED-RESUMABLE` with the `Goodbye.Details.resumable` flag set to `false`, it MUST not allow subsequent resumptions of that session, and should completely close the session (disconnecting it from any realms, etc).
