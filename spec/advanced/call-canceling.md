# Canceling Calls

Support for this feature MUST be announced by *Callers* (`role := "caller"`), *Callees* (`role := "callee"`) and *Dealers* (`role := "dealer"`) via

    HELLO.Details.roles.<role>.features.call_canceling|bool := true


A *Caller* might want to actively cancel a call that was issued, but not has yet returned. An example where this is useful could be a user triggering a long running operation and later changing his mind or no longer willing to wait.

The message flow between *Callers*, a *Dealer* and *Callees* for canceling remote procedure calls involves the following messages:

 * `CANCEL`
 * `INTERRUPT`

A call may be cancelled at the *Callee*

![alt text](figure/rpc_cancel1.png "RPC Message Flow: Calls")

A call may be cancelled at the *Dealer*

![alt text](figure/rpc_cancel2.png "RPC Message Flow: Calls")

A *Caller* cancels a remote procedure call initiated (but not yet finished) by sending a `CANCEL` message to the *Dealer*:

    [CANCEL, CALL.Request|id, Options|dict]

A *Dealer* cancels an invocation of an endpoint initiated (but not yet finished) by sending a `INTERRUPT` message to the *Callee*:

    [INTERRUPT, INVOCATION.Request|id, Options|dict]

Options:

    CANCEL.Options.mode|string == "skip" | "kill" | "killnowait"
