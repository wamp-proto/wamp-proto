### Call Canceling

#### Feature Definition

A *Caller* might want to actively cancel a call that was issued, but not has yet returned. An example where this is useful could be a user triggering a long running operation and later changing his mind or no longer willing to wait.

The message flow between *Callers*, a *Dealer* and *Callees* for canceling remote procedure calls involves the following messages:

 * `CANCEL`
 * `INTERRUPT`

A call may be cancelled at the *Callee*

{align="left"}
        ,------.          ,------.          ,------.
        |Caller|          |Dealer|          |Callee|
        `--+---'          `--+---'          `--+---'
           |       CALL      |                 |    
           | ---------------->                 |    
           |                 |                 |    
           |                 |    INVOCATION   |    
           |                 | ---------------->    
           |                 |                 |    
           |      CANCEL     |                 |    
           | ---------------->                 |    
           |                 |                 |    
           |                 |    INTERRUPT    |    
           |                 | ---------------->    
           |                 |                 |    
           |                 |      ERROR      |    
           |                 | <----------------    
           |                 |                 |    
           |      ERROR      |                 |    
           | <----------------                 |    
        ,--+---.          ,--+---.          ,--+---.
        |Caller|          |Dealer|          |Callee|
        `------'          `------'          `------'


A call may be cancelled at the *Dealer*

{align="left"}
        ,------.          ,------.          ,------.
        |Caller|          |Dealer|          |Callee|
        `--+---'          `--+---'          `--+---'
           |       CALL      |                 |    
           | ---------------->                 |    
           |                 |                 |    
           |                 |    INVOCATION   |    
           |                 | ---------------->    
           |                 |                 |    
           |      CANCEL     |                 |    
           | ---------------->                 |    
           |                 |                 |    
           |      ERROR      |                 |    
           | <----------------                 |    
           |                 |                 |    
           |                 |    INTERRUPT    |    
           |                 | ---------------->    
           |                 |                 |    
           |                 |      ERROR      |    
           |                 | <----------------    
        ,--+---.          ,--+---.          ,--+---.
        |Caller|          |Dealer|          |Callee|
        `------'          `------'          `------'


A *Caller* cancels a remote procedure call initiated (but not yet finished) by sending a `CANCEL` message to the *Dealer*:

{align="left"}
        [CANCEL, CALL.Request|id, Options|dict]

A *Dealer* cancels an invocation of an endpoint initiated (but not yet finished) by sending a `INTERRUPT` message to the *Callee*:

{align="left"}
        [INTERRUPT, INVOCATION.Request|id, Options|dict]

Options:

{align="left"}
        CANCEL.Options.mode|string == "skip" | "kill" | "killnowait"


#### Feature Announcement

Support for this feature MUST be announced by *Callers* (`role := "caller"`), *Callees* (`role := "callee"`) and *Dealers* (`role := "dealer"`) via

{align="left"}
        HELLO.Details.roles.<role>.features.call_canceling|bool := true
