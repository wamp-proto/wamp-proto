# Call Timeouts

Support for this feature MUST be announced by *Callers* (`role := "caller"`), *Callees* (`role := "callee"`) and *Dealers* (`role := "dealer"`) via

    HELLO.Details.roles.<role>.features.call_timeout|bool := true

A *Caller* might want to issue a call providing a *timeout* for the call to finish.

A *timeout* allows to **automatically** cancel a call after a specified time either at the *Callee* or at the *Dealer*.

A *Caller* specifies a timeout by providing

    CALL.Options.timeout|integer

in ms. A timeout value of `0` deactivates automatic call timeout. This is also the default value.

The timeout option is a companion to, but slightly different from the `CANCEL` and `INTERRUPT` messages that allow a *Caller* and *Dealer* to **actively** cancel a call or invocation.

In fact, a timeout timer might run at three places:

 * *Caller*
 * *Dealer*
 * *Callee*
