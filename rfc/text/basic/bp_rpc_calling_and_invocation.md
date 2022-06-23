## Calling and Invocations

The message flow between Callers, a Dealer and Callees for calling procedures and invoking endpoints involves the following messages:

1. `CALL`
2. `RESULT`
3. `INVOCATION`
4. `YIELD`
5. `ERROR`

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
           |                 |  YIELD or ERROR |
           |                 | <----------------
           |                 |                 |
           | RESULT or ERROR |                 |
           | <----------------                 |
        ,--+---.          ,--+---.          ,--+---.
        |Caller|          |Dealer|          |Callee|
        `------'          `------'          `------'


The execution of remote procedure calls is asynchronous, and there may be more than one call outstanding. A call is called outstanding (from the point of view of the Caller), when a (final) result or error has not yet been received by the Caller.

### CALL

When a Caller wishes to call a remote procedure, it sends a `CALL` message to a Dealer:

{align="left"}
        [CALL, Request|id, Options|dict, Procedure|uri]

or

{align="left"}
        [CALL, Request|id, Options|dict, Procedure|uri, Arguments|list]

or

{align="left"}
        [CALL, Request|id, Options|dict, Procedure|uri, Arguments|list,
            ArgumentsKw|dict]

where

* `Request` is a sequential ID in the _session scope_, incremented by the Caller and used to correlate the Dealer's response with the request.
* `Options` is a dictionary that allows to provide additional call request details in an extensible way. This is described further below.
* `Procedure` is the URI of the procedure to be called.
* `Arguments` is a list of positional call arguments (each of arbitrary type). The list may be of zero length.
* `ArgumentsKw` is a dictionary of keyword call arguments (each of arbitrary type). The dictionary may be empty.

*Example*

{align="left"}
        [48, 7814135, {}, "com.myapp.ping"]

*Example*

{align="left"}
        [48, 7814135, {}, "com.myapp.echo", ["Hello, world!"]]

*Example*

{align="left"}
        [48, 7814135, {}, "com.myapp.add2", [23, 7]]

*Example*

{align="left"}
        [48, 7814135, {}, "com.myapp.user.new", ["johnny"],
            {"firstname": "John", "surname": "Doe"}]


### INVOCATION

If the Dealer is able to fulfill (mediate) the call and it allows the call, it sends a `INVOCATION` message to the respective Callee implementing the procedure:

{align="left"}
        [INVOCATION, Request|id, REGISTERED.Registration|id, Details|dict]

or

{align="left"}
        [INVOCATION, Request|id, REGISTERED.Registration|id, Details|dict,
            CALL.Arguments|list]

or

{align="left"}
        [INVOCATION, Request|id, REGISTERED.Registration|id, Details|dict,
            CALL.Arguments|list, CALL.ArgumentsKw|dict]

where

* `Request` is a sequential ID in the _session scope_, incremented by the Dealer and used to correlate the *Callee's* response with the request.
* `REGISTERED.Registration` is the registration ID under which the procedure was registered at the Dealer.
* `Details` is a dictionary that allows to provide additional invocation request details in an extensible way. This is described further below.
* `CALL.Arguments` is the original list of positional call arguments as provided by the Caller.
* `CALL.ArgumentsKw` is the original dictionary of keyword call arguments as provided by the Caller.

*Example*

{align="left"}
        [68, 6131533, 9823526, {}]

*Example*

{align="left"}
        [68, 6131533, 9823527, {}, ["Hello, world!"]]

*Example*

{align="left"}
        [68, 6131533, 9823528, {}, [23, 7]]

*Example*

{align="left"}
        [68, 6131533, 9823529, {}, ["johnny"], {"firstname": "John", "surname": "Doe"}]


### YIELD

If the Callee is able to successfully process and finish the execution of the call, it answers by sending a `YIELD` message to the Dealer:

{align="left"}
        [YIELD, INVOCATION.Request|id, Options|dict]

or

{align="left"}
        [YIELD, INVOCATION.Request|id, Options|dict, Arguments|list]

or

{align="left"}
        [YIELD, INVOCATION.Request|id, Options|dict, Arguments|list, ArgumentsKw|dict]

where

* `INVOCATION.Request` is the ID from the original invocation request.
* `Options`is a dictionary that allows to provide additional options.
* `Arguments` is a list of positional result elements (each of arbitrary type). The list may be of zero length.
* `ArgumentsKw` is a dictionary of keyword result elements (each of arbitrary type). The dictionary may be empty.


*Example*

{align="left"}
        [70, 6131533, {}]

*Example*

{align="left"}
        [70, 6131533, {}, ["Hello, world!"]]

*Example*

{align="left"}
        [70, 6131533, {}, [30]]

*Example*

{align="left"}
        [70, 6131533, {}, [], {"userid": 123, "karma": 10}]


### RESULT

The Dealer will then send a `RESULT` message to the original Caller:

{align="left"}
        [RESULT, CALL.Request|id, Details|dict]

or

{align="left"}
        [RESULT, CALL.Request|id, Details|dict, YIELD.Arguments|list]

or

{align="left"}
        [RESULT, CALL.Request|id, Details|dict, YIELD.Arguments|list,
            YIELD.ArgumentsKw|dict]

where

* `CALL.Request` is the ID from the original call request.
* `Details` is a dictionary of additional details.
* `YIELD.Arguments` is the original list of positional result elements as returned by the Callee.
* `YIELD.ArgumentsKw` is the original dictionary of keyword result elements as returned by the Callee.

*Example*

{align="left"}
        [50, 7814135, {}]

*Example*

{align="left"}
        [50, 7814135, {}, ["Hello, world!"]]

*Example*

{align="left"}
        [50, 7814135, {}, [30]]

*Example*

{align="left"}
        [50, 7814135, {}, [], {"userid": 123, "karma": 10}]


### Invocation ERROR


If the Callee is unable to process or finish the execution of the call, or the application code implementing the procedure raises an exception or otherwise runs into an error, the Callee sends an `ERROR` message to the Dealer:

{align="left"}
        [ERROR, INVOCATION, INVOCATION.Request|id, Details|dict, Error|uri]

or

{align="left"}
        [ERROR, INVOCATION, INVOCATION.Request|id, Details|dict, Error|uri, Arguments|list]

or

{align="left"}
        [ERROR, INVOCATION, INVOCATION.Request|id, Details|dict, Error|uri, Arguments|list,
            ArgumentsKw|dict]

where

* `INVOCATION.Request` is the ID from the original `INVOCATION` request previously sent by the Dealer to the Callee.
* `Details` is a dictionary with additional error details.
* `Error` is a URI that identifies the error of why the request could not be fulfilled.
* `Arguments` is a list containing arbitrary, application defined, positional error information. This will be forwarded by the Dealer to the Caller that initiated the call.
* `ArgumentsKw` is a dictionary containing arbitrary, application defined, keyword-based error information. This will be forwarded by the Dealer to the Caller that initiated the call.

*Example*

{align="left"}
        [8, 68, 6131533, {}, "com.myapp.error.object_write_protected",
            ["Object is write protected."], {"severity": 3}]


### Call ERROR

The Dealer will then send a `ERROR` message to the original Caller:

{align="left"}
        [ERROR, CALL, CALL.Request|id, Details|dict, Error|uri]

or

{align="left"}
        [ERROR, CALL, CALL.Request|id, Details|dict, Error|uri, Arguments|list]

or

{align="left"}
        [ERROR, CALL, CALL.Request|id, Details|dict, Error|uri, Arguments|list,
            ArgumentsKw|dict]

where

* `CALL.Request` is the ID from the original `CALL` request sent by the Caller to the Dealer.
* `Details` is a dictionary with additional error details.
* `Error` is a URI identifying the type of error as returned by the Callee to the Dealer.
* `Arguments` is a list containing the original error payload list as returned by the Callee to the Dealer.
* `ArgumentsKw` is a dictionary containing the original error payload dictionary as returned by the Callee to the Dealer

*Example*

{align="left"}
        [8, 48, 7814135, {}, "com.myapp.error.object_write_protected",
            ["Object is write protected."], {"severity": 3}]

If the original call already failed at the Dealer **before** the call would have been forwarded to any Callee, the Dealer will send an `ERROR` message to the Caller:

{align="left"}
        [ERROR, CALL, CALL.Request|id, Details|dict, Error|uri]

*Example*

{align="left"}
        [8, 48, 7814135, {}, "wamp.error.no_such_procedure"]
