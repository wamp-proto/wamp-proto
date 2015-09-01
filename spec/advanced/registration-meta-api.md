# Registration Meta API

Registration _meta-events_ are fired when RPC registrations are first created, when other clients attach/remove themselves to them, and when registrations are deleted. Furthermore, WAMP allows actively retrieving information about registrations via _meta-procedures_.

Support for this feature **must** be announced by _Dealers_ (`role := "dealer"`) via:

   	HELLO.Details.roles.dealer.features.registration_meta_api|bool := true

Meta-events are created by the router itself. This means that the events as well as the data received when calling a meta-procedure can be accorded the same trust level as the router.

Registration Meta Events
------------------------

A client can subscribe to the following registration meta-events, which cover the lifecycle of a registration:

- `wamp.registration.on_create`: Fired when a registration is created through a registration request for an URI which was previously without a registration.
- `wamp.registration.on_register`: Fired when a session is added to a registration.
- `wamp.registration.on_unregister`: Fired when a session is removed from a registration.
- `wamp.registration.on_delete`: Fired when a registration is deleted after the last session attached to it has been removed.

A `wamp.registration.on_register` event **shall** always be fired subsequent to a `wamp.registration.on_create` event, since the first registration results in both the creation of the registration and the addition of a session. Similarly, the `wamp.registration.on_delete` event **shall** always be preceded by a `wamp.registration.on_unregister` event.

The WAMP registration meta events **shall** be dispatched by the router to the same realm as the WAMP session which triggered the event.

### Meta Event Specifications

----------------------------------

#### `wamp.registration.on_create`

Fired when a registration is created through a registration request for an URI which was previously without a registration.

**Event Arguments**
- `session|id`: The session ID performing the registration request.
- `RegistrationDetails|dict`: Information on the created registration.

**Object Schemas**

```javascript
RegistrationDetails :=
{
    "id": registration|id,
    "created": time_created|iso_8601_string,
    "uri": procedure|uri,
    "match": match_policy|string,
    "invoke": invocation_policy|string
}
```

See [Pattern-based Registrations](pattern-based-registration.md) for a description of `match_policy`.

> NOTE: invocation_policy IS NOT YET DESCRIBED IN THE ADVANCED SPEC

----------------------------------

#### `wamp.registration.on_register`

Fired when a session is added to a registration.

**Event Arguments**
- `session|id`: The ID of the session being added to a registration.
- `registration|id`: The ID of the registration to which a session is being added.

----------------------------------

#### `wamp.registration.on_unregister`

Fired when a session is removed from a subscription.

**Event Arguments**
- `session|id`: The ID of the session being removed from a registration.
- `registration|id`: The ID of the registration from which a session is being removed.

----------------------------------

#### `wamp.registration.on_delete`

Fired when a registration is deleted after the last session attached to it has been removed.

**Event Arguments**
- `session|id`: The ID of the last session being removed from a registration.
- `registration|id`: The ID of the registration being deleted.

----------------------------------


Registration Meta-Procedures
----------------------------

A client can actively retrieve information about registrations via the following meta-procedures:

- `wamp.registration.list`: Retrieves registration IDs listed according to match policies.
- `wamp.registration.lookup`: Obtains the registration (if any) managing a procedure, according to some match policy.
- `wamp.registration.match`: Obtains the registration best matching a given procedure URI.
- `wamp.registration.get`: Retrieves information on a particular registration.
- `wamp.registration.list_callees`: Retrieves a list of session IDs for sessions currently attached to the registration.
- `wamp.registration.count_callees`: Obtains the number of sessions currently attached to the registration.


### Meta-Procedure Specifications

----------------------------------

#### `wamp.registration.list`

Retrieves registration IDs listed according to match policies.

**Arguments**
- None

**Results**
- `RegistrationLists|dict`: A dictionary with a list of registration IDs for each match policy.

**Object Schemas**

```javascript
RegistrationLists :=
{
    "exact": registration_ids|list,
    "prefix": registration_ids|list,
    "wildcard": registration_ids|list
}
```

See [Pattern-based Registrations](pattern-based-registration.md) for a description of match policies.

----------------------------------

#### `wamp.registration.lookup`

Obtains the registration (if any) managing a procedure, according to some match policy.

**Arguments**
- `procedure|uri`: The procedure to lookup the registration for.
- (Optional) `options|dict`: Same options as when registering a procedure.

**Results**
- (Nullable) `registration|id`: The ID of the registration managing the procedure, if found, or null.

----------------------------------

#### `wamp.registration.match`

Obtains the registration best matching a given procedure URI.

**Arguments**
- `procedure|uri`: The procedure URI to match

**Results**
- (Nullable) `registration|id`: The ID of best matching registration, or null.

----------------------------------

#### `wamp.registration.get`

Retrieves information on a particular registration.

**Arguments**
- `registration|id`: The ID of the registration to retrieve.

**Results**
- `RegistrationDetails|dict`: Details on the registration.

**Error URIs**
- `wamp.error.no_such_registration`: No registration with the given ID exists on the router.

**Object Schemas**

```javascript
RegistrationDetails :=
{
    "id": registration|id,
    "created": time_created|iso_8601_string,
    "uri": procedure|uri,
    "match": match_policy|string,
    "invoke": invocation_policy|string
}
```

See [Pattern-based Registrations](pattern-based-registration.md) for a description of match policies.

*NOTE: invocation_policy IS NOT YET DESCRIBED IN THE ADVANCED SPEC*

----------------------------------

#### `wamp.registration.list_callees`

Retrieves a list of session IDs for sessions currently attached to the registration.

**Arguments**
- `registration|id`: The ID of the registration to get calles for.

**Results**
- `callee_ids|list`: A list of WAMP session IDs of callees currently attached to the registration.

**Error URIs**
- `wamp.error.no_such_registration`: No registration with the given ID exists on the router.

----------------------------------

#### `wamp.registration.count_callees`

Obtains the number of sessions currently attached to a registration.

**Arguments**
- `registration|id`: The ID of the registration to get the number of callees for.

**Results**
- `count|int`: The number of callees currently attached to a registration.

**Error URIs**
- `wamp.error.no_such_registration`: No registration with the given ID exists on the router.

----------------------------------
