### Caller Exclusion

Support for this feature MUST be announced by *Callers* (`role := "caller"`) and *Dealers* (`role := "dealer"`) via

    HELLO.Details.roles.<role>.features.caller_exclusion|bool := true


By default, a *Caller* of a procedure will **never** itself be forwarded the call issued, even when registered for the `Procedure` the *Caller* is publishing to. This behavior can be overridden via

    CALL.Options.exclude_me|bool

When calling with `CALL.Options.exclude_me := false`, the *Caller* of the procedure might be forwarded the call issued - if it is registered for the `Procedure` called.

*Example*

    [48, 7814135, {"exclude_me": false}, "com.myapp.echo", ["Hello, world!"]]

In this example, the *Caller* might be forwarded the call issued, if it is registered for `com.myapp.echo`.
