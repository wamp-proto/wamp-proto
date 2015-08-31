# Pattern-based Registrations

Support for this feature MUST be announced by *Callees* (`role := "callee"`) and *Dealers* (`role := "dealer"`) via

    HELLO.Details.roles.<role>.features.pattern_based_registration|bool := true


By default, *Callees* register procedures with **exact matching policy**. That is a call will only be routed to a *Callee* by the *Dealer* if the procedure called (`CALL.Procedure`) *exactly* matches the endpoint registered (`REGISTER.Procedure`).

A *Callee* might want to register procedures based on a *pattern*. This can be useful to reduce the number of individual registrations to be set up.

If the *Dealer* and the *Callee* support **pattern-based registrations**, this matching can happen by

 * prefix-matching policy
 * wildcard-matching policy

*Dealers* and *Callees* MUST announce support for non-exact matching policies in the `HELLO.Details` (see that chapter).

## Prefix Matching

A *Callee* requests **prefix-matching policy** with a registration request by setting

    REGISTER.Options.match|string := "prefix"

*Example*

    [64, 612352435, {"match": "prefix"}, "com.myapp.myobject1"]

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

The *Dealer* will apply the prefix-matching based on the UTF-8 encoded byte string for the `CALL.Procedure` and the `REGISTER.Procedure`.

## Wildcard Matching

A *Callee* requests **wildcard-matching policy** with a registration request by setting

    REGISTER.Options.match|string := "wildcard"

Wildcard-matching allows to provide wildcards for **whole** URI components.

*Example*

    [64, 612352435, {"match": "wildcard"}, "com.myapp..myprocedure1"]

In the above registration request, the 3rd URI component is empty, which signals a wildcard in that URI component position. In this example, calls with `CALL.Procedure` e.g.

 * `com.myapp.myobject1.myprocedure1`
 * `com.myapp.myobject2.myprocedure1`

will all apply for call routing. Calls with `CALL.Procedure` e.g.

 * `com.myapp.myobject1.myprocedure1.mysubprocedure1`
 * `com.myapp.myobject1.myprocedure2`
 * `com.myapp2.myobject1.myprocedure1`

will not apply for call routing.

When a single call matches more than one of a *Callees* registrations, the call MAY be routed for invocation on multiple registrations, depending on call settings.

--------------
FIXME: The *Callee* can detect the invocation of that same call on multiple registrations via `INVOCATION.CALL.Request`, which will be identical.

Since each *Callees* registrations "stands on it's own", there is no *set semantics* implied by pattern-based registrations. E.g. a *Callee* cannot register to a broad pattern, and then unregister from a subset of that broad pattern to form a more complex registration. Each registration is separate.

If an endpoint was registered with a pattern-based matching policy, a *Dealer* MUST supply the original `CALL.Procedure` as provided by the *Caller* in `INVOCATION.Details.procedure` to the *Callee*.

