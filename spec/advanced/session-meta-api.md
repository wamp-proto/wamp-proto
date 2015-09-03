# Session Meta API

WAMP enables the monitoring of when sessions join a realm on the router or when they leave it via
[Session Meta Events](#session-meta-events). It also allows retrieving information about currently connected sessions via [Session Meta Procedures](#session-meta-procedures).

Meta events are created by the router itself. This means that the events, as well as the data received when calling a meta procedure, can be accorded the same trust level as the router.


## Session Meta Events

A client can subscribe to the following session meta-events, which cover the lifecycle of a WAMP session:

* `wamp.session.on_join`: Fired when a session joins a realm on the router.
* `wamp.session.on_leave`: Fired when a session leaves a realm on the router or is disconnected.

Session meta events MUST be dispatched by the *Router* to the same realm as the WAMP session which triggered the event.

### `wamp.session.on_join`

Fired when a session joins a realm on the router. The event payload consists of a single positional argument `details|dict`:

* `session|id` - The session ID of the session that joined
* `authid|string` - The authentication ID of the session that joined
* `authrole|string` - The authentication role of the session that joined
* `authmethod|string` - The authentication method that was used for authentication the session that joined
* `authprovider|string`- The provider that performed the authentication of the session that joined
* `transport|dict` - Optional, implementation defined information about the WAMP transport the joined session is running over.

> See [Authentication](authentication.md) for a description of the `authid`, `authrole`, `authmethod` and `authprovider` properties.

### `wamp.session.on_leave`

Fired when a session leaves a realm on the router or is disconnected. The event payload consists of a single positional argument `session|id` with the session ID of the session that left.


## Session Meta Procedures

A client can actively retrieve information about sessions via the following meta-procedures:

* `wamp.session.count`: Obtains the number of sessions currently attached to the realm.
* `wamp.session.list`: Retrieves a list of the session IDs for all sessions currently attached to the realm.
* `wamp.session.get`: Retrieves information on a specific session.

Session meta procedures MUST be registered by the *Router* on the same realm as the WAMP session about which information is retrieved.

### `wamp.session.count`

Obtains the number of sessions currently attached to the realm:

**Positional arguments**
1. `filter_authroles|list[string]` - Optional filter: if provided, only count sessions with an `authrole` from this list.

**Positional results**
1. `count|int` - The number of sessions currently attached to the realm.


### `wamp.session.list`

Retrieves a list of the session IDs for all sessions currently attached to the realm.

**Positional arguments**
1. `filter_authroles|list[string]` - Optional filter: if provided, only count sessions with an `authrole` from this list.

**Positional results**
1. `session_ids|list` - List of WAMP session IDs (order undefined).


### `wamp.session.get`

Retrieves information on a specific session.

**Positional arguments**
1. `session|id` - The session ID of the session to retrieve details for.

**Positional results**
1. `details|dict` - Information on a particular session:
    * `session|id` - The session ID of the session that joined
    * `authid|string` - The authentication ID of the session that joined
    * `authrole|string` - The authentication role of the session that joined
    * `authmethod|string` - The authentication method that was used for authentication the session that joined
    * `authprovider|string`- The provider that performed the authentication of the session that joined
    * `transport|dict` - Optional, implementation defined information about the WAMP transport the joined session is running over.

> See [Authentication](authentication.md) for a description of the `authid`, `authrole`, `authmethod` and `authprovider` properties.

**Errors**
* `wamp.error.no_such_session` - No session with the given ID exists on the router.

---

## Feature Announcement

Support for this feature MUST be announced by **both** *Dealers* and *Brokers* via:

    HELLO.Details.roles.<role>.features.session_meta_api|bool := true

**Example**

Here is a `WELCOME` message from a *Router* with support for both the *Broker* and *Dealer* role, and with support for **Session Meta API**:

```json
[
    2,
    4580268554656113,
    {
        "authid":"OL3AeppwDLXiAAPbqm9IVhnw",
        "authrole": "anonymous",
        "authmethod": "anonymous",
        "roles": {
            "broker": {
                "features": {
                    "session_meta_api": true
                }
            },
            "dealer": {
                "features": {
                    "session_meta_api": true
                }
            }
        }
    }
]
```

---
