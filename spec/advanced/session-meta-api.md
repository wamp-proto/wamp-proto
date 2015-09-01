Session Meta API
================

WAMP enables the monitoring of when sessions join a realm on the router or when they leave it via
_session meta-events_. It also allows retrieving information about currently connected sessions via session
_meta-procedures_.

Meta-events are created by the router itself. This means that the events, as well as the data received when calling a meta-procedure, can be accorded the same trust level as the router.

Support for this feature **must** be announced by _Dealers_ and _Brokers_ via:

    HELLO.Details.roles.<role>.features.session_meta_api|bool := true


Session Meta-Events
-------------------

A client can subscribe to the following session meta-events, which cover the lifecycle of a session:

- `wamp.session.on_join`: Fired when a session joins a realm on the router.
- `wamp.session.on_leave`: Fired when a session leaves a realm on the router or is disconnected.

The WAMP session meta events shall be dispatched by the router to the same realm as the WAMP session which triggered the event.

### Meta-Event Specifications

---------------------------

#### `wamp.session.on_join`

Fired when a session joins a realm on the router.

**Event Arguments**
- `SessionDetails|dict`: Information on the session that has joined.

**Object Schemas**

```javascript
SessionDetails :=
{
    "authid": authid|string,
    "authrole": authrole|string,
    "authmethod": authmethod|string,
    "authprovider": authprovider|string,
    "realm": realm|uri,
    "session": session|id,
    "transport": TransportInfo|dict // Implementation defined?
}
```

See [Authentication](authentication.md) for a description of the `authid`, `authrole`, `authmethod` and `authprovider` properties.

---------------------------

#### `wamp.session.on_leave`

Fired when a session leaves a realm on the router or is disconnected.

**Event Arguments**
- `session|id`

---------------------------


Session Meta-Procedures
-----------------------

A client can actively retrieve information about sessions via the following meta-procedures:

- `wamp.session.count`: Obtains the number of sessions currently attached to the realm.
- `wamp.session.list`: Retrieves a list of the session IDs for all sessions currently attached to the realm
- `wamp.session.get`: Retrieves information on a specific session.

### Meta-Procedure Specifications

---------------------------

#### `wamp.session.count`

Obtains the number of sessions currently attached to the realm.

**Arguments**
- (Optional) `filter_authroles|list`: If provided, only count sessions with an authrole from this list.

**Results**
- `count|int`: The number of sessions currently attached to the realm.

---------------------------

#### `wamp.session.list`

Retrieves a list of the session IDs for all sessions currently attached to the realm.

**Arguments**
- (Optional) `filter_authroles|list`: If provided, only return sessions with an authrole from this list.

**Results**
- `session_ids|list`: List of WAMP session IDs (order undefined).

---------------------------

#### `wamp.session.get`

Retrieves information on a specific session.

**Arguments**
- `session|id`: If provided, only return sessions with an authrole from this list.

**Results**
- `SessionDetails|dict`: Information on a particular session.

**Error URIs**
- `wamp.error.no_such_session`: No session with the given ID exists on the router.

**Object Schemas**

```javascript
SessionDetails :=
{
    "authid": authid|string,
    "authrole": authrole|string,
    "authmethod": authmethod|string,
    "authprovider": authprovider|string,
    "realm": realm|uri,
    "session": session|id,
    "transport": TransportInfo|dict // Implementation defined?
}
```

See [Authentication](authentication.md) for a description of the `authid`, `authrole`, `authmethod` and `authprovider` properties.

---------------------------
