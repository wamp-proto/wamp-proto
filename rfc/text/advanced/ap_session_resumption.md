### Session Resumption

Lifetimes of WAMP *Sessions* and WAMP *Transports* are independent of each other.

A *Transport* may outlive the lifetime of a *Session*, and a *Session* can exist without a *Transport* being currently attached.

Usually, a WAMP client will establish a new *Transport* connecting to a *Router*, create a new *Session*, attach the *Transport* to the *Session* and then perform an initial authentication handshake joining a *Realm* on the *Router*. After that, the *Session* can be used for PubSub and RPC.

The *Session* can also be **paused (frozen)**, when the *Transport* is lost or actively **detached** from the *Session*. In this case, the *Router* is expected to retain it's router-side *Session* representation and allow the client to reconnect, and **resume** the *Session*.

#### Feature Definition

Session Resumption is when a *Client* can pause (freeze) a *Router* session and resume it later.
This is useful if the *Transport* to the *Router* is potentially unreliable (for example, mobile systems in cars) and the *Client* wishes to have an unbroken session across these *Transport* disconnections.

A *Client* that supports resuming may request a *Router* create a resumable session by setting `Hello.Details.resumable|bool` to `true`.

As an example of a conformant `HELLO` message:

```json
[
    1,
    "realm1",
    {
        "roles": {
            "subscriber": {},
            "publisher": {},
            "caller": {},
            "callee": {}
        },
        "authmethods": ["anonymous"],
        "resumable": true
    }
]
```

If the *Router* supports Session Resumption, they can signal whether the newly created *Session* is resumable by setting `Welcome.Details.resumable|bool`.
If this flag is missing or set to `false`, a client MUST NOT attempt resumption of the session.
If the flag is set to `true`, it MUST be accompanied by `Welcome.Details.resume-token|string`, which contains the "resume token" that a client can use to resume this session.
This "resume token" MUST be a Base64 encoded string of a 16 octet cryptographically generated random token, and MUST NOT be reused for other sessions, or used again as the resume token for this session if it were detached and reattached again.
The Router MUST also set `Welcome.Details.resumed|bool` to `false` if it is a new session.
Clients MUST assume that that lack of this flag means the session is new, and is not resumed.
Clients MUST be able to handle a resumable session request being denied (where `Hello.Details.resumable` is `true` but `Welcome.Details.resumable` is `false`).

As an example of a conformant `WELCOME` message:

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

A Client can then pause the resumable *Session* they are attached to by sending a `GOODBYE` message with `Goodbye.Details.resumable` set to `true`, or close it completely with `Goodbye.Details.resumable` set to `false`.
The *Router* must then respond with a `GOODBYE` of its own, as per regular WAMP semantics, also setting the `Goodbye.Details.resumable` flag.
Lack of a `Goodbye.Details.resumable` flag on either `GOODBYE` message MUST be interpreted as a `false` value.
`Goodbye.Details.resumable` on the *Router*-sent `GOODBYE` MAY be set to `false` if the client's `Goodbye.Details.resumable` was set to `true`, which means that the client cannot resume this session.
`Goodbye.Details.resumable` on the *Router*-sent `GOODBYE` MUST be set to `false` if the client's `Goodbye.Details.resumable` was set to `false`, and the *Session* MUST be destroyed.

As an example of a conformant `GOODBYE` message:

```json
[
    6,
    {
        "resumable": true
    },
    "wamp.close.normal"
]
```

A *Router* may forcibly pause or destroy a *Session* by sending a `GOODBYE` to the *Client*.
As with *Client* initiated disconnections, the `Goodbye.Details.resumable` flag from the server dictates whether the open session can be resumed at a later time.
In *Router* initiated disconnections, a *Client*-sent `GOODBYE` MUST NOT have the `Goodbye.Details.resumable` flag set.

If a *Client* detaches or becomes detached from a *Session*, it MUST be able to attach to the same or other Sessions on the same *Transport*, without reconnection.
*Routers* MAY decide to timeout and disconnect the *Transport* of the *Client* if it stays connected without being attached to a realm for an unreasonable amount of time.

To resume an resumable *Session*, a *Client* sends a special `HELLO` message to the *Router*.
It can send one of two types -- an opportunistic resume, or a dedicated resume.

In a dedicated resume, the *Session* is either resumed or the *Client* does not get a session (and has to create a new session subafterwards).
The `HELLO` sent from the *Client* to the *Router* has `Hello.Realm` set to `null`, `Hello.Details.resume-session|id` set to the session ID the client wishes to resume, and `Hello.Details.resume-token|string` set the resume token given in the last `WELCOME` message from the server.
`Hello.Details` MUST NOT have any keys set other than `resume-session` and `resume-token`.
As an example of a dedicated resume `HELLO` message:

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

If the session can be resumed, the *Router* will respond with a similarly small `WELCOME` message, with `Welcome.Session|id` set to the resumed session ID, `Welcome.Details.resumed|bool` set to `true`, `Welcome.Details.resumable|bool` set to `true` if the session can be resumed (`false` otherwise), and `Welcome.Details.resume-token|string` set to a new cryptographically secure resume token (as per the `WELCOME` in the original session creation) if `Welcome.Details.resumable` is `true`.
A session that cannot be resumed again MUST NOT have `Welcome.Details.resume-token` set, and `Welcome.Details.resumable` MUST explicitly be set to `false`.

As an example of this small `WELCOME` message:

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

If the *Session* cannot be resumed either, the *Router* will respond with an `ABORT` message, with `Abort.Reason|uri` set to `wamp.error.nonresumable_session`.
The *Client* will stay unattached and MUST be able to retry without having to create a new *Transport*.

In an opportunistic resume, the *Session* is either resumed or a new *Session* is created.
This is useful if a second round trip if the session is not resumable is too high of a cost.
An opportunistic resume can be initiated by the unattached *Client* sending a `HELLO` message to the *Router* as if they were creating a new resumable *Session*, but with the extra `Hello.Details.resume-session|id` and `Hello.Details.resume-token|string` keys set as if it were a dedicated resume.
The *Router* will then attempt to resume the requested *Session*, but will create a new one if the *Session* is no longer available, the resume token is invalid, or `Hello.Realm|uri` does not match the realm of the *Session*.
As an example of an opportunistic resume `HELLO` message:

```json
[
    1,
    "realm1",
    {
        "roles": {
            "subscriber": {},
            "publisher": {},
            "caller": {},
            "callee": {}
        },
        "authmethods": ["anonymous"],
        "resumable": true,
        "resume-session": 657683631,
        "resume-token": "mazdJ5q6PLHkEbR3WdJzwA=="
    }
]
```

If the *Router* can resume the session, it will send back a small `WELCOME` message the same as a dedicated resume, but if it cannot, it will create a new session and send back a full `WELCOME` message with `Welcome.Details.resumed|bool` set to `false`.
As an example of a `WELCOME` message from the *Router* that has not been able to resume the session:

```json
[
    2,
    1385728471,
    {
        "realm": "realm1",
        "authid": "nobody",
        "authrole": "anonymous",
        "authprovider": "static",
        "authextra": {},

        "resumed": false,
        "resumable": true,
        "resume-token": "1zDqEuwmDAKn38y64+7ZTg=="
    }
]
```

A resumed *Session* MUST maintain the same *Registrations* and *Subscriptions* that were on the session before it was frozen, unless the *Router* explicity removed them from the session.
Messages sent to the *Session* whilst the *Session* was unattached MUST NOT be resent after the Session reconnects, the Session should use Event History to recover messages during unattachment.
Procedures that the *Session* has registered MUST return with an `ERROR` with error URI `wamp.error.session_unattached` for single-registered procedures, and MUST NOT be taken into consideration for load balancing in a shared registration.

If a *Client* attempts to resume a non-paused *Session* on the *Broker*, the Broker MUST detatch the Session from the Client it is currently attached to, and attach it on the new Client.
It must detatch it by way of a `GOODBYE` message with `Goodbye.Details.resumable|bool` set to `false` (as the single-use token will have been used by the new client) and `Goodbye.Reason|uri` set to `wamp.error.other_client_attached`.
This can be used for Sessions which are attached to Clients that are disconnected, but have not yet timed out (for example, on high-latency wireless networks).

#### Session Resumption Meta Events

Furthermore, two new Session Meta Events are defined:

##### wamp.session.on_attach

Fired when a session is attached to a transport.
This SHOULD fired BEFORE `wamp.session.on_join`, if it is a new session, or fired when a client resumes a session.
The event payload consists of a single positional argument, `session|id`, the session ID of the attached session.

##### wamp.session.on_detach

Fired when a session is detached from a transport.
This SHOULD fired AFTER `wamp.session.on_attach`, if the session is closing, or fired when a client detaches from a session.
The event payload consists of a single positional argument, `session|id`, the session ID of the detached session.


#### Feature Announcement

Because of the requirement for a *Client* to handle servers denying a request to create a resumable *Session*, clients that implement this Advanced Profile feature will operate backwards-compatibly with non-implementing *Servers*.

Support for the Session Resumption Meta Events MUST be announced by the *Broker*:

{align="left"}
        HELLO.Details.roles.broker.features.
            session_resumption_meta_api|bool := true
