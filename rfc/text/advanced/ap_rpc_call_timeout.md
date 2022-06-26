## Call Timeouts {#rpc-call-timeout}

A *Caller* might want to issue a call and provide a *timeout* after which the call will finish.

A *timeout* allows for **automatic** cancellation of a call after a specified time either at the *Callee* or at the *Dealer*.

A *Caller* specifies a timeout by providing

{align="left"}
        CALL.Options.timeout|integer

in ms. A timeout value of `0` deactivates automatic call timeout. This is also the default value.

The timeout option is a companion to, but slightly different from the `CANCEL` and `INTERRUPT` messages that allow a *Caller* and *Dealer* to **actively** cancel a call or invocation.

In fact, a timeout timer might run at three places:

 * *Caller*
 * *Dealer*
 * *Callee*


**Feature Announcement**

Support for this feature MUST be announced by *Callers* (`role := "caller"`), *Callees* (`role := "callee"`) and *Dealers* (`role := "dealer"`) via

{align="left"}
        HELLO.Details.roles.<role>.features.call_timeout|bool := true
