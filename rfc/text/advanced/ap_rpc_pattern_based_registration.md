### Pattern-based Registrations

#### Feature Definition

##### Introduction

By default, *Callees* register procedures with **exact matching policy**. That is a call will only be routed to a *Callee* by the *Dealer* if the procedure called (`CALL.Procedure`) *exactly* matches the endpoint registered (`REGISTER.Procedure`).

A *Callee* might want to register procedures based on a *pattern*. This can be useful to reduce the number of individual registrations to be set up or to subscribe to a open set of topics, not known beforehand by the *Subscriber*.

If the *Dealer* and the *Callee* support **pattern-based registrations**, this matching can happen by

* **prefix-matching policy**
* **wildcard-matching policy**


##### Prefix Matching

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


##### Wildcard Matching

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


##### General

###### No set semantics

Since each *Callee*'s' registrations "stands on it's own", there is no *set semantics* implied by pattern-based registrations.

E.g. a *Callee* cannot register to a broad pattern, and then unregister from a subset of that broad pattern to form a more complex registration. Each registration is separate.

###### Calls matching multiple registrations

The behavior when a single call matches more than one of a *Callee's* registrations or more than one registration in general is still being discussed - see https://github.com/tavendo/WAMP/issues/182.

###### Concrete procedure called

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

#### Feature Announcement

Support for this feature MUST be announced by *Callees* (`role := "callee"`) and *Dealers* (`role := "dealer"`) via

{align="left"}
        HELLO.Details.roles.<role>.features.
            pattern_based_registration|bool := true
