## Registering and Unregistering

The message flow between Callees and a Dealer for registering and unregistering endpoints to be called over RPC involves the following messages:

1. `REGISTER`
2. `REGISTERED`
4. `UNREGISTER`
5. `UNREGISTERED`
6. `ERROR`

{align="left"}
        ,------.          ,------.               ,------.
        |Caller|          |Dealer|               |Callee|
        `--+---'          `--+---'               `--+---'
           |                 |                      |
           |                 |                      |
           |                 |       REGISTER       |
           |                 | <---------------------
           |                 |                      |
           |                 |  REGISTERED or ERROR |
           |                 | --------------------->
           |                 |                      |
           |                 |                      |
           |                 |                      |
           |                 |                      |
           |                 |                      |
           |                 |      UNREGISTER      |
           |                 | <---------------------
           |                 |                      |
           |                 | UNREGISTERED or ERROR|
           |                 | --------------------->
        ,--+---.          ,--+---.               ,--+---.
        |Caller|          |Dealer|               |Callee|
        `------'          `------'               `------'


### REGISTER

A Callee announces the availability of an endpoint implementing a procedure with a Dealer by sending a `REGISTER` message:

{align="left"}
        [REGISTER, Request|id, Options|dict, Procedure|uri]

where

* `Request` is a sequential ID in the _session scope_, incremented by the Callee and used to correlate the Dealer's response with the request.
* `Options` is a dictionary that allows to provide additional registration request details in a extensible way. This is described further below.
* `Procedure`is the procedure the Callee wants to register

*Example*

{align="left"}
        [64, 25349185, {}, "com.myapp.myprocedure1"]

### REGISTERED

If the Dealer is able to fulfill and allowing the registration, it answers by sending a `REGISTERED` message to the `Callee`:

{align="left"}
        [REGISTERED, REGISTER.Request|id, Registration|id]

where

* `REGISTER.Request` is the ID from the original request.
*  `Registration` is an ID chosen by the Dealer for the registration.

*Example*

{align="left"}
        [65, 25349185, 2103333224]

### Register ERROR

When the request for registration cannot be fulfilled by the Dealer, the Dealer sends back an `ERROR` message to the Callee:

{align="left"}
        [ERROR, REGISTER, REGISTER.Request|id, Details|dict, Error|uri]

where

* `REGISTER.Request` is the ID from the original request.
* `Error` is a URI that gives the error of why the request could not be fulfilled.

*Example*

{align="left"}
        [8, 64, 25349185, {}, "wamp.error.procedure_already_exists"]

### UNREGISTER

When a Callee is no longer willing to provide an implementation of the registered procedure, it sends an `UNREGISTER` message to the Dealer:

{align="left"}
        [UNREGISTER, Request|id, REGISTERED.Registration|id]

where

* `Request` is a sequential ID in the _session scope_, incremented by the Callee and used to correlate the Dealer's response with the request.
* `REGISTERED.Registration` is the ID for the registration to revoke, originally handed out by the Dealer to the Callee.

*Example*

{align="left"}
        [66, 788923562, 2103333224]

### UNREGISTERED

Upon successful unregistration, the Dealer sends an `UNREGISTERED` message to the Callee:

{align="left"}
        [UNREGISTERED, UNREGISTER.Request|id]

where

* `UNREGISTER.Request` is the ID from the original request.

*Example*

{align="left"}
        [67, 788923562]

### Unregister ERROR

When the unregistration request fails, the Dealer sends an `ERROR` message:

{align="left"}
        [ERROR, UNREGISTER, UNREGISTER.Request|id, Details|dict, Error|uri]

where

* `UNREGISTER.Request` is the ID from the original request.
* `Error` is a URI that gives the error of why the request could not be fulfilled.

*Example*

{align="left"}
        [8, 66, 788923562, {}, "wamp.error.no_such_registration"]
