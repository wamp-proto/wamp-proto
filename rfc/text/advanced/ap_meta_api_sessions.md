## Sessions Meta API

WAMP enables the monitoring of when sessions join a realm on the router or when they leave it via **Session Meta Events**. It also allows retrieving information about currently connected sessions via **Session Meta Procedures**.

Meta events are created by the router itself. This means that the events, as well as the data received when calling a meta procedure, can be accorded the same trust level as the router.

> Note that an implementation that only supports a *Broker* or *Dealer* role, not both at the same time, essentially cannot offer the **Session Meta API**, as it requires both roles to support this feature.

The following sections contain an informal, easy to digest description of the WAMP procedures and topics
available in (this part of) the WAMP Meta API.
A formal definition of the WAMP Meta API in terms of available WAMP procedures and topics including
precise and complete type definitions of the application payloads, that is procedure arguments and
results or event payloads is contained in

* Compiled Binary Schema: `<WAMP API Catalog>/schema/wamp-meta.bfbs`
* FlatBuffers Schema Source: `<WAMP API Catalog>/src/wamp-meta.fbs`

which uses FlatBuffers IDL to describe the API. The method of using FlatBuffers IDL and type definitions to formally define WAMP procedures and topics is detailed in section [WAMP IDL](#wamp-idl).


**Feature Announcement**

Support for this feature MUST be announced by **both** *Dealers* and *Brokers* via:

{align="left"}
        HELLO.Details.roles.<role>.features.
            session_meta_api|bool := true

Here is a `WELCOME` message from a *Router* with support for both the *Broker* and *Dealer* role, and with support for **Session Meta API**:

{align="left"}
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

> Note in particular that the feature is announced on both the *Broker* and the *Dealer* roles.


### Events

A client can subscribe to the following session meta-events, which cover the lifecycle of a session:

* `wamp.session.on_join`: Fired when a session joins a realm on the router.
* `wamp.session.on_leave`: Fired when a session leaves a realm on the router or is disconnected.

**Session Meta Events** MUST be dispatched by the *Router* to the same realm as the WAMP session which triggered the event.

#### wamp.session.on_join

Fired when a session joins a realm on the router. The event payload consists of a single positional argument `details|dict`:

* `session|id` - The session ID of the session that joined
* `authid|string` - The authentication ID of the session that joined
* `authrole|string` - The authentication role of the session that joined
* `authmethod|string` - The authentication method that was used for authentication the session that joined
* `authprovider|string`- The provider that performed the authentication of the session that joined
* `transport|dict` - Optional, implementation defined information about the WAMP transport the joined session is running over.

> See **Authentication** for a description of the `authid`, `authrole`, `authmethod` and `authprovider` properties.

#### wamp.session.on_leave

Fired when a session leaves a realm on the router or is disconnected. The event payload consists of three positional arguments:

* `session|id` - The session ID of the session that left
* `authid`|string` - The authentication ID of the session that left
* `authrole|string` - The authentication role of the session that left


### Procedures

A client can actively retrieve information about sessions, or forcefully close sessions, via the following meta-procedures:

* `wamp.session.count`: Obtains the number of sessions currently attached to the realm.
* `wamp.session.list`: Retrieves a list of the session IDs for all sessions currently attached to the realm.
* `wamp.session.get`: Retrieves information on a specific session.
* `wamp.session.kill`: Kill a single session identified by session ID.
* `wamp.session.kill_by_authid`: Kill all currently connected sessions that have the specified authid.
* `wamp.session.kill_by_authrole`: Kill all currently connected sessions that have the specified authrole.
* `wamp.session.kill_all`: Kill all currently connected sessions in the caller's realm.

Session meta procedures MUST be registered by the *Router* on the same realm as the WAMP session about which information is retrieved.

#### wamp.session.count

Obtains the number of sessions currently attached to the realm.

**Positional arguments**

1. `filter_authroles|list[string]` - Optional filter: if provided, only count sessions with an `authrole` from this list.

**Positional results**

1. `count|int` - The number of sessions currently attached to the realm.


#### wamp.session.list

Retrieves a list of the session IDs for all sessions currently attached to the realm.

**Positional arguments**

1. `filter_authroles|list[string]` - Optional filter: if provided, only count sessions with an `authrole` from this list.

**Positional results**

1. `session_ids|list` - List of WAMP session IDs (order undefined).


#### wamp.session.get

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

> See **Authentication** for a description of the `authid`, `authrole`, `authmethod` and `authprovider` properties.

**Errors**

* `wamp.error.no_such_session` - No session with the given ID exists on the router.


#### wamp.session.kill

Kill a single session identified by session ID.

The caller of this meta procedure may only specify session IDs other than its own session.  Specifying the caller's own session will result in a `wamp.error.no_such_session` since no _other_ session with that ID exists.

The keyword arguments are optional, and if not provided the reason defaults to `wamp.close.normal` and the message is omitted from the `GOODBYE` sent to the closed session.

**Positional arguments**

1. `session|id` - The session ID of the session to close.

**Keyword arguments**

1. `reason|uri` - reason for closing session, sent to client in `GOODBYE.Reason`.
2. `message|string` - additional information sent to client in `GOODBYE.Details` under the key "message".

**Errors**

* `wamp.error.no_such_session` - No session with the given ID exists on the router.
* `wamp.error.invalid_uri` - A `reason` keyword argument has a value that is not a valid non-empty URI.

##### wamp.session.kill_by_authid

Kill all currently connected sessions that have the specified `authid`.

If the caller's own session has the specified `authid`, the caller's session is excluded from the closed sessions.

The keyword arguments are optional, and if not provided the reason defaults to `wamp.close.normal` and the message is omitted from the `GOODBYE` sent to the closed session.

**Positional arguments**

1. `authid|string` - The authentication ID identifying sessions to close.

**Keyword arguments**

1. `reason|uri` - reason for closing sessions, sent to clients in `GOODBYE.Reason`
2. `message|string` - additional information sent to clients in `GOODBYE.Details` under the key "message".

**Positional results**

1. `count|int` - The number of sessions closed by this meta procedure.

**Errors**

* `wamp.error.invalid_uri` - A `reason` keyword argument has a value that is not a valid non-empty URI.


#### wamp.session.kill_by_authrole

Kill all currently connected sessions that have the specified `authrole`.

If the caller's own session has the specified `authrole`, the caller's session is excluded from the closed sessions.

The keyword arguments are optional, and if not provided the reason defaults to `wamp.close.normal` and the message is omitted from the `GOODBYE` sent to the closed session.

**Positional arguments**

1. `authrole|string` - The authentication role identifying sessions to close.

**Keyword arguments**

1. `reason|uri` - reason for closing sessions, sent to clients in `GOODBYE.Reason`
2. `message|string` - additional information sent to clients in `GOODBYE.Details` under the key "message".

**Positional results**

1. `count|int` - The number of sessions closed by this meta procedure.

**Errors**

* `wamp.error.invalid_uri` - A `reason` keyword argument has a value that is not a valid non-empty URI.


#### wamp.session.kill_all

Kill all currently connected sessions in the caller's realm.

The caller's own session is excluded from the closed sessions.  Closing all sessions in the realm will not generate session meta events or testament events, since no subscribers would remain to receive these events.

The keyword arguments are optional, and if not provided the reason defaults to `wamp.close.normal` and the message is omitted from the `GOODBYE` sent to the closed session.

**Keyword arguments**

1. `reason|uri` - reason for closing sessions, sent to clients in `GOODBYE.Reason`
2. `message|string` - additional information sent to clients in `GOODBYE.Details` under the key "message".

**Positional results**

1. `count|int` - The number of sessions closed by this meta procedure.

**Errors**

* `wamp.error.invalid_uri` - A `reason` keyword argument has a value that is not a valid non-empty URI.
