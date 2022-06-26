## WAMP IDL {#wamp-idl}

WAMP was designed with the goals of being easy to approach and use for application developers. Creating a procedure to expose some custom functionality should be possible in any supported programming language using that language's native elements, with the least amount of additional effort.

Following from that, WAMP uses *dynamic typing* for the application payloads of calls, call results and error, as well as event payloads.

A WAMP router will happily forward *any* application payload on *any* procedure or topic URI as long as the client is _authorized_ (has permission) to execute the respective WAMP action (call, register, publish or subscribe) on the given URI.

This approach has served WAMP well, as application developers can get started immediately, and evolve and change payloads as they need without extra steps.
These advantages in flexibility of course come at a price, as nothing is free, and knowing that price is important to be aware of the tradeoffs one is accepting when using dynamic typing:

* problematic coordination of *Interfaces* within larger developer teams or between different parties
* no easy way to stabilize, freeze, document or share *Interfaces*
* no way to programmatically describe *Interfaces* ("interface reflection") at run-time

Problems such above could be avoided when WAMP supported an _option_ to formally define WAMP-based *Interfaces*. This needs to answer the following questions:

1. How to specify the `args|List` and `kwargs|Dict` application payloads that are used in WAMP calls, errors and events?
2. How to specify the type and URI (patterns) for WAMP RPCs *Procedures* and WAMP PubSub *Topics* that make up an *Interface*, and how to identify an *Interface* itself as a collection of *Procedures* and *Topics*?
3. How to package, publish and share *Catalogs* as a collection of *Interfaces* plus metadata

The following sections will describe the solution to each of above questions using WAMP IDL.

Using WAMP Interfaces finally allows to support the following application developer level features:

1. router-based application payload validation and enforcement
2. WAMP interface documentation generation and autodocs Web service
3. publication and sharing of WAMP Interfaces and Catalogs
4. client binding code generation from WAMP Interfaces
5. run-time WAMP type reflection as part of the WAMP meta API

**Application Payload Typing**

User defined WAMP application payloads are transmitted in `Arguments|list` and `ArgumentsKw|dict` elements of the following WAMP messages:

* `PUBLISH`
* `EVENT`
* `CALL`
* `INVOCATION`
* `YIELD`
* `RESULT`
* `ERROR`

A *Publisher* uses the

* `PUBLISH.Arguments|list`, `PUBLISH.ArgumentsKw|dict`

message to send the event payload to be published to the *Broker*. When the event is accepted by the *Broker*, it will dispatch

* `EVENT.Arguments|list`, `EVENT.ArgumentsKw|dict`

messages to all (eligible, and not excluded) *Subscribers.

A *Caller* uses the

* `CALL.Arguments|list`, `CALL.ArgumentsKw|dict`

message to send the call arguments to be used to the *Dealer*. When the call is accepted by the *Dealer*, it will forward

* `INVOCATION.Arguments|list`, `INVOCATION.ArgumentsKw|dict`

to the (or one of) *Callee*, and receive a

* `YIELD.Arguments|list`, `YIELD.ArgumentsKw|dict`

message, which it will return to the original *Caller*

* `RESULT.Arguments|list`, `RESULT.ArgumentsKw|dict`

In the error case, a *Callee* MAY return an

* `ERROR.Arguments|list`, `ERROR.ArgumentsKw|dict`

which again is returned to the original *Caller*.

It is important to note that the above messages and message elements are the only ones free for use with application and user defined payloads. In particular, even though the following WAMP messages and message element carry payloads defined by the specific WAMP authentication method used, they do *not* carry arbitrary application payloads:

* `HELLO.Details["authextra"]|dict`
* `WELCOME.Details["authextra"]|dict`
* `CHALLENGE.Extra|dict`
* `AUTHENTICATE.Extra|dict`

**Typing Procedures, Topics and Interfaces**

Write me.
