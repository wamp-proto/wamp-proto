## Terminology {#terminology}

This chapter contains a list of technical terms used in this specification, along with their respective meanings.
as used in this specification.

Implementations SHOULD use terms as defined here in their public interfaces and documentation,
and SHOULD NOT reinvent or reinterpret terms. Users SHOULD be able to transfer their knowledge gained on WAMP
in the context of one implementation when starting to use another implementation.
This is to support the overarching goal of WAMP to free application developers from restrictions when
building distributed applications, both at the network level, and when choosing or switching the WAMP client
libraries or routers used.

Our goal is to maximize **User Choice and Experience** for developers of WAMP based applications,
both formally (open protocol and open source) as well as practically (switching costs).


### Fundamental

{align="left"}
| Term                              | Definition                                                                                              |
|-----------------------------------|---------------------------------------------------------------------------------------------------------|
| *User*                            | A user runs *Client*s or *Router*s which implement WAMP                                                 |
| *Client*                          | A program run by a *User* with application code using WAMP for application level communication          |
| *Router*                          | A program run by a *User* with middleware code using WAMP to provide application routing services       |
| *Peer*                            | A WAMP *Client* or *Router*. An implementation might embed, provide or use both roles                   |
| *Realm*                           | Isolated WAMP URI namespace, routing and administrative domain, optionally protected by **AA**          |
| *Transport*                       | A message-based, reliable, ordered, bidirectional (full-duplex) channel over which *Peers* communicate  |
| *Connection*                      | An underlying entity (if any) carrying the *Transport*, e.g. a network connection, pipe, queue or such  |
| *Session*                         | Transient conversation between a *Client* and a *Router* on a *Realm* over a *Transport*                |
| *Message*                         | Indivisible unit of information transmitted between peers                                               |
| *Serializer*                      | A *Serializer* encodes WAMP messages with application payloads into bytes strings for transport         |


### Authentication and Authorization (AA)

{align="left"}
| Term                               | Definition                                                                                                                     |
|------------------------------------|--------------------------------------------------------------------------------------------------------------------------------|
| *Authentication*                   | Establishes the identity of a *Session* on a *Realm*                                                                           |
| *Principal*                        | Once authenticated, *Session*s identify under a *Principal*                                                                    |
| *Credentials*                      | Any authentication information and secrets used during *Authentication*                                                        |
| *Authorization*                    | Decides about permission for a given *Action* on an *URI or URI pattern* by a *Principal*                                      |
| *Access Control*                   | Policy for selective restriction of access by *Action*s on *URIs or URI patterns* and *Principal*s                             |
| *Role-based Access Control (RBAC)* | An *Access Control* policy based on *Realm* (`realm`), *Role* (`authrole`) of *Principal*, *URI or URI pattern* and *Action*   |
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
| *Call*           | A *Call* (in a *Router*) results from a *Caller* successfully **calling** of a *Procedure* for call routing                   |
| *Invocation*     | An *Invocation* with application payload is received by *Callee*s for matching *Registration*s they registered for            |


### Publish and Subscribe

{align="left"}
| Term             | Definition                                                                                                                    |
|------------------|-------------------------------------------------------------------------------------------------------------------------------|
| *Publisher*      | A *Publisher* is a *Session* that **publishes** application payloads to a (fully qualified) *Topic* for event routing         |
| *Subscriber*     | A *Subscriber* is a *Session* that **subscribes** to a *Topic* to receive application payloads on matching events             |
| *Topic*          | A *Topic* is an URI or URI pattern that can be subscribed to for event routing by *Subscriber*s                               |
| *Subscription*   | A *Subscription* (in a *Router*) results from a *Subscriber* successfully **subscribing** to a *Topic* for event routing      |
| *Publication*    | A *Publication* (in a *Router*) results from a *Publisher* successfully **publishing** to a *Topic* for event routing         |
| *Event*          | An *Event* with application payload is received by *Subscriber*s for matching *Subscription*s they subscribed to              |
