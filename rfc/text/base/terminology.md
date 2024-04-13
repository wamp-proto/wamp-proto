## Terminology {#terminology}

This chapter contains a list of technical terms used in this specification, along with their respective meanings.

Implementations SHOULD use terms as defined here in their public interfaces and documentation,
and SHOULD NOT reinvent or reinterpret terms. Users SHOULD be able to transfer their WAMP knowledge
from one implementation to another.
This is to support the overarching goal of WAMP to free application developers from restrictions when
building distributed applications, both at the network level, and when choosing (or switching) the WAMP
implementations used.

Our goal is to maximize **user choice and experience** when developing WAMP-based applications,
both formally (open protocol and open source) as well as practically (switching costs).


### Authentication and Authorization (AA)

{align="left"}
| Term                               | Definition                                                                                                |
|------------------------------------|-----------------------------------------------------------------------------------------------------------|
| *Authentication*                   | Establishes the identity of a *Session* within a *Realm*                                                  |
| *Principal*                        | A *Principal* (`authid`) is any *User* that can be authenticated under a *Realm* (`realm`) and runs in the security context of a *Role* (`authrole`) within that *Realm*. |
| *Credentials*                      | The authentication information and secrets used during                                                    |
| *Authorization*                    | A decision on permitting a *Principal* to perform a given *Action* on an *URI or URI pattern*             |
| *Access Control*                   | Policy for selective restriction of *Actions* on *URIs or URI patterns* performed by *Principals*         |
| *Role-based Access Control (RBAC)* | An *Access Control* policy based on *Realm* (`realm`), *Principal*'s *Role* (`authrole`), *URI or URI pattern*, and *Action*   |
| *Discretionary Access Control*     | An *Access Control* policy controlled by *Users* and enforced by *Routers*                                |
| *Mandatory Access Control*         | An *Access Control* policy controlled by *Router Administrators* or *Realm Owners*, and enforced by *Routers* |
| *Capability-based Access Control*  | An *Access Control* policy where *Callers*, *Callees*, *Publishers*, *Subscribers* directly share capabilities with each other |
| *Subject*                          | The originating *Session* of an *Action* in the context of *Authorization*                                |
| *Object*                           | A (fully qualified) *URI or URI pattern* representing the target of an *Action* in the context of *Authorization* |
| *Action*                           | One of the four core WAMP operations: **register**, **call**, **subscribe**, and **publish**              |


### Publish and Subscribe

{align="left"}
| Term             | Definition                                                                                                                    |
|------------------|-------------------------------------------------------------------------------------------------------------------------------|
| *Publisher*      | A *Publisher* is a *Session* that **publishes** application payloads to a (fully qualified) *Topic* for event routing         |
| *Subscriber*     | A *Subscriber* is a *Session* that **subscribes** to a *Topic* to receive application payloads on matching events             |
| *Topic*          | A *Topic* is an URI or URI pattern that can be subscribed to for event routing by *Subscribers*                               |
| *Subscription*   | A *Router* record resulting from a *Subscriber* successfully **subscribing** to a *Topic* for event routing                   |
| *Publication*    | A transient *Router* record resulting from a *Publisher* successfully **publishing** to a *Topic* for event routing           |
| *Event*          | A publication that is routed to *Subscribers* having matching *Subscriptions* to the published *Topic*.                       |


### Remote Procedure Calls

{align="left"}
| Term             | Definition                                                                                                                    |
|------------------|-------------------------------------------------------------------------------------------------------------------------------|
| *Caller*         | A *Caller* is a *Session* that **calls**, with application payloads, a (fully qualified) *Procedure* for call routing         |
| *Callee*         | A *Callee* is a *Session* that responds to *Procedure* call invocations by **yielding** back application result payloads      |
| *Procedure*      | A *Procedure* is an URI or URI pattern that can be registered for call routing by *Callees*                                   |
| *Registration*   | A *Router* record resulting from a *Callee* successfully **registering** a *Procedure* for call routing                       |
| *Call*           | A transient *Router* record resulting from a *Caller* successfully **calling** a *Procedure* for call routing                 |
| *Invocation*     | A call request and payload that are routed to a *Callee* having a matching *Registration* for the called *Procedure*          |

