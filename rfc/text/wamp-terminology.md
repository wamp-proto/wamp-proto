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


### Fundamental

{align="left"}
| Term                              | Definition                                                                                              |
|-----------------------------------|---------------------------------------------------------------------------------------------------------|
| *User*                            | A person (or organization) running a WAMP *Client* or *Router* |
| *Client*                          | A program run by a *User*, with application code using WAMP for application level communications        |
| *Router*                          | A program run by a *User*, with middleware code using WAMP to provide application routing services      |
| *Peer*                            | A WAMP *Client* or *Router*. An implementation might embed, provide or use both roles                   |
| *Realm*                           | Isolated WAMP URI namespace serving as a routing and administrative domain, optionally protected by **AA**          |
| *Transport*                       | A message-based, reliable, ordered, bidirectional (full-duplex) channel over which *Peers* communicate  |
| *Connection*                      | An underlying entity (if any) carrying the *Transport*, e.g. a network connection, pipe, queue or such  |
| *Session*                         | Transient conversation between a *Client* and a *Router*, within a *Realm* and over a *Transport*                |
| *Message*                         | Indivisible unit of information transmitted between peers                                               |
| *Serializer*                      | Encodes WAMP messages, with application payloads, into byte strings for transport         |


### Authentication and Authorization (AA)

{align="left"}
| Term                               | Definition                                                                                                                     |
|------------------------------------|--------------------------------------------------------------------------------------------------------------------------------|
| *Authentication*                   | Establishes the identity of a *Session* within a *Realm*                                                                           |
| *Principal*                        | The authenticated entity associated with a *Session* |
| *Credentials*                      | The authentication information and secrets used during *Authentication*                                                        |
| *Authorization*                    | A decision on permitting a *Principal* to perform a given *Action* on an *URI or URI pattern* |
| *Access Control*                   | Policy for selective restriction of *Action*s on *URIs or URI patterns* performed by *Principal*s                             |
| *Role-based Access Control (RBAC)* | An *Access Control* policy based on *Realm* (`realm`), *Principal*'s *Role* (`authrole`), *URI or URI pattern*, and *Action*   |
| *Discretionary Access Control*     | An *Access Control* policy controlled by *Users* and enforced by *Routers*                                                     |
| *Mandatory Access Control*         | An *Access Control* policy controlled by *Router Administrators* or *Realm Owners* and enforced by *Routers*                   |
| *Capability-based Access Control*  | An *Access Control* policy where *Caller*s, *Callee*s, *Publisher*s, *Subscriber*s directly share capabilities with each other |
| *Subject*                          | The originating *Session* of an *Action* in the context of *Authorization*                                                     |
| *Object*                           | The target of an *Action* in the context of *Authorization*, a (fully qualified) *URI or URI pattern*                          |
| *Action*                           | One of the four WAMP core operations **register**, **call**, **subscribe** and **publish**                                     |


### Remote Procedure Calls

{align="left"}
| Term             | Definition                                                                                                                    |
|------------------|-------------------------------------------------------------------------------------------------------------------------------|
| *Caller*         | A *Caller* is a *Session* that **calls** with application payloads a (fully qualified) *Procedure* for call routing           |
| *Callee*         | A *Callee* is a *Session* that **yields** application payloads from a *Procedure* by answering invocations on matching calls  |
| *Procedure*      | A *Procedure* is an URI or URI pattern that can be registered for call routing by *Callee*s                                   |
| *Registration*   | A *Registration* (in a *Router*) results from a *Callee* successfully **registering** of a *Procedure* for call routing       |
| *Call*           | A transient *Router* record resulting from a *Caller* successfully **calling** a *Procedure* for call routing |
| *Invocation*     | A call request and payload that are routed to a *Callee* having a matching *Registration* for the called *Procedure*            |


### Publish and Subscribe

{align="left"}
| Term             | Definition                                                                                                                    |
|------------------|-------------------------------------------------------------------------------------------------------------------------------|
| *Publisher*      | A *Publisher* is a *Session* that **publishes** application payloads to a (fully qualified) *Topic* for event routing         |
| *Subscriber*     | A *Subscriber* is a *Session* that **subscribes** to a *Topic* to receive application payloads on matching events             |
| *Topic*          | A *Topic* is an URI or URI pattern that can be subscribed to for event routing by *Subscriber*s                               |
| *Subscription*   | A *Router* record resulting from a *Subscriber* successfully **subscribing** to a *Topic* for event routing      |
| *Publication*    | A transient Router record resulting from a *Publisher* successfully **publishing** to a *Topic* for event routing         |
| *Event*          | A publication that is routed to a *Subscribers* having matching *Subscriptions* to the published *Topic*.              |
