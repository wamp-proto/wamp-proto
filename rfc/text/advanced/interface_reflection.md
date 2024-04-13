### Interface Reflection {#interface-reflection}

Feature status: **sketch**

*Reflection* denotes the ability of WAMP peers to examine the procedures, topics and errors provided or used by other peers.

I.e. a WAMP *Caller*, *Callee*, *Subscriber* or *Publisher* may be interested in retrieving a machine readable list and description of WAMP procedures and topics it is authorized to access or provide in the context of a WAMP session with a *Dealer* or *Broker*.

Reflection may be useful in the following cases:

 * documentation
 * discoverability
 * generating stubs and proxies

WAMP predefines the following procedures for performing run-time reflection on WAMP peers which act as *Brokers* and/or *Dealers*.

Predefined WAMP reflection procedures to *list* resources by type:

{align="left"}
        wamp.reflection.topic.list
        wamp.reflection.procedure.list
        wamp.reflection.error.list

Predefined WAMP reflection procedures to *describe* resources by type:

{align="left"}
        wamp.reflection.topic.describe
        wamp.reflection.procedure.describe
        wamp.reflection.error.describe

A peer that acts as a *Broker* SHOULD announce support for the reflection API by sending

{align="left"}
        HELLO.Details.roles.broker.reflection|bool := true

A peer that acts as a *Dealer* SHOULD announce support for the reflection API by sending

{align="left"}
        HELLO.Details.roles.dealer.reflection|bool := true

> Since *Brokers* might provide (broker) procedures and *Dealers* might provide (dealer) topics, both SHOULD implement the complete API above (even if the peer only implements one of *Broker* or *Dealer* roles).

**Reflection Events and Procedures**

A topic or procedure is defined for reflection:

{align="left"}
        wamp.reflect.define

A topic or procedure is asked to be described (reflected upon):

{align="left"}
        wamp.reflect.describe

A topic or procedure has been defined for reflection:

{align="left"}
        wamp.reflect.on_define

A topic or procedure has been undefined from reflection:

{align="left"}
        wamp.reflect.on_undefine
