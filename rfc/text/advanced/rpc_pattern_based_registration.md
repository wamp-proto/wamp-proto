## Pattern-based Registrations {#rpc-pattern-reg}

By default, *Callees* register procedures with **exact matching policy**. That is a call will only be routed to a *Callee* by the *Dealer* if the procedure called (`CALL.Procedure`) *exactly* matches the endpoint registered (`REGISTER.Procedure`).

A *Callee* might want to register procedures based on a *pattern*. This can be useful to reduce the number of individual registrations to be set up or to subscribe to a open set of topics, not known beforehand by the *Subscriber*.

If the *Dealer* and the *Callee* support **pattern-based registrations**, this matching can happen by

* **prefix-matching policy**
* **wildcard-matching policy**

**Feature Announcement**

Support for this feature MUST be announced by *Callees* (`role := "callee"`) and *Dealers* (`role := "dealer"`) via

{align="left"}
        HELLO.Details.roles.<role>.features.
            pattern_based_registration|bool := true


### Prefix Matching

A *Callee* requests **prefix-matching policy** with a registration request by setting

{align="left"}
        REGISTER.Options.match|string := "prefix"

*Example*

{align="left"}
```json
    [
        64,
        612352435,
        {
            "match": "prefix"
        },
        "com.myapp.myobject1"
    ]
```

When a **prefix-matching policy** is in place, any call with a procedure that has `REGISTER.Procedure` as a *prefix* will match the registration, and potentially be routed to *Callees* on that registration.

In above example, the following calls with `CALL.Procedure`

* `com.myapp.myobject1.myprocedure1`
* `com.myapp.myobject1-mysubobject1`
* `com.myapp.myobject1.mysubobject1.myprocedure1`
* `com.myapp.myobject1`

will all apply for call routing. A call with one of the following `CALL.Procedure`

* `com.myapp.myobject2`
* `com.myapp.myobject`

will not apply.


### Wildcard Matching

A *Callee* requests **wildcard-matching policy** with a registration request by setting

{align="left"}
        REGISTER.Options.match|string := "wildcard"

Wildcard-matching allows to provide wildcards for **whole** URI components.

*Example*

{align="left"}
```json
    [
        64,
        612352435,
        {
            "match": "wildcard"
        },
        "com.myapp..myprocedure1"
    ]
```

In the above registration request, the 3rd URI component is empty, which signals a wildcard in that URI component position. In this example, calls with `CALL.Procedure` e.g.

* `com.myapp.myobject1.myprocedure1`
* `com.myapp.myobject2.myprocedure1`

will all apply for call routing. Calls with `CALL.Procedure` e.g.

* `com.myapp.myobject1.myprocedure1.mysubprocedure1`
* `com.myapp.myobject1.myprocedure2`
* `com.myapp2.myobject1.myprocedure1`

will not apply for call routing.

When a single call matches more than one of a *Callees* registrations, the call MAY be routed for invocation on multiple registrations, depending on call settings.


### Design Aspects

**No set semantics**

Since each *Callee*'s' registrations "stands on its own", there is no *set semantics* implied by pattern-based registrations.

E.g. a *Callee* cannot register to a broad pattern, and then unregister from a subset of that broad pattern to form a more complex registration. Each registration is separate.

**Calls matching multiple registrations**

There can be situations, when some call URI matches more then one registration. In this case a call is routed to one and only one best matched RPC registration, or fails with ERROR `wamp.error.no_such_procedure`.

The following algorithm MUST be applied to find a single RPC registration to which a call is routed:

1. Check for exact matching registration. If this match exists — use it.
2. If there are prefix-based registrations, find the registration with the longest prefix match. Longest means it has more URI components matched, e.g. for call URI `a1.b2.c3.d4` registration `a1.b2.c3` has higher priority than registration `a1.b2`. If this match exists — use it.
3. If there are wildcard-based registrations, find the registration with the longest portion of URI components matched before each wildcard. E.g. for call URI `a1.b2.c3.d4` registration `a1.b2..d4` has higher priority than registration `a1...d4`, see below for more complex examples. If this match exists — use it.
4. If there is no exact match, no prefix match, and no wildcard match, then *Dealer* MUST return ERROR `wamp.error.no_such_procedure`.

*Examples*

{align="left"}
```
Registered RPCs:
    1. 'a1.b2.c3.d4.e55' (exact),
    2. 'a1.b2.c3' (prefix),
    3. 'a1.b2.c3.d4' (prefix),
    4. 'a1.b2..d4.e5',
    5. 'a1.b2.c33..e5',
    6. 'a1.b2..d4.e5..g7',
    7. 'a1.b2..d4..f6.g7'

Call request RPC URI: 'a1.b2.c3.d4.e55' →
    exact match. Use RPC 1
Call request RPC URI: 'a1.b2.c3.d98.e74' →
    no exact match, single prefix match. Use RPC 2
Call request RPC URI: 'a1.b2.c3.d4.e325' →
    no exact match, 2 prefix matches (2,3), select longest one.
    Use RPC 3
Call request RPC URI: 'a1.b2.c55.d4.e5' →
    no exact match, no prefix match, single wildcard match.
    Use RPC 4
Call request RPC URI: 'a1.b2.c33.d4.e5' →
    no exact match, no prefix match, 2 wildcard matches (4,5),
    but RPC 5 has longer first portion (a1.b2.c33). Use RPC 5
Call request RPC URI: 'a1.b2.c88.d4.e5.f6.g7' →
    no exact match, no prefix match, 2 wildcard matches (6,7),
    both having equal first portions (a1.b2), but RPC 6 has longer
    second portion (d4.e5). Use RPC 6
Call request RPC URI: 'a2.b2.c2.d2.e2' →
    no exact match, no prefix match, no wildcard match.
    Return wamp.error.no_such_procedure
```

**Concrete procedure called**

If an endpoint was registered with a pattern-based matching policy, a *Dealer* MUST supply the original `CALL.Procedure` as provided by the *Caller* in

{align="left"}
        INVOCATION.Details.procedure

to the *Callee*.

*Example*

{align="left"}
```json
    [
        68,
        6131533,
        9823527,
        {
            "procedure": "com.myapp.procedure.proc1"
        },
        ["Hello, world!"]
    ]
```
