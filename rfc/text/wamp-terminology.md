## Terminology {#terminology}

This chapter collects the terminology *as used in WAMP*, the group of specialized words and respective meanings
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
| Term                              | Definition                                                                                            |
|-----------------------------------|-------------------------------------------------------------------------------------------------------|
| *User                             | A user runs *Client*s or *Router*s which implement WAMP                                               |
| *Client*                          | A program run by a *User* with application code using WAMP for application level communication        |
| *Router*                          | A program run by a *User* with middleware code using WAMP to provide application routing services     |
| *Peer*                            | A WAMP *Client* or *Router*. An implementation might embed and use both roles                         |
| *Realm*                           |                                                                                                       |
| *Transport*                       | The bidirectional, ordered, full duplex message channel over which *Peers* communicate                |
| *Connection*                      | When a *Client* is using a *Transport* over a network, the underlying network connection (e.g. TCP)   |
| *Session*                         |                                                                                                       |


### Authentication and Authorization

{align="left"}
| Term                              | Definition                                                                                            |
|-----------------------------------|-------------------------------------------------------------------------------------------------------|
| *Authentication*                  | Establishes the identity of a *Session* on a *Realm*                                                  |
| *Principal*                       | Once authenticated, *Session*s identify under a *Principal*                                           |
| *Credentials*                     | Any authentication information and secrets used during *Authentication*                               |
| *Authorization*                   | Decides about permission for a given *Action* on an URI or URI pattern by a *Principal*               |
| *Access Control*                  | Policy for selective restriction of access by *Action*s on URIs or URI patterns and *Principal*s      |
| *Role-based Access Control*       | An *Access Control* policy based on *Realm* (`realm`) and *Role* (`authrole`) of a *Principal*        |
| *Discretionary Access Control*    |                                                                                                       |
| *Mandatory Access Control*        |                                                                                                       |
| *Capability-based Access Control* |                                                                                                       |
| *Subject*                         | The originating *Session* of an *Action* in the context of *Authorization*                            |
| *Object*                          | The target of an *Action* in the context of *Authorization*, an URI or URI pattern                    |
| *Action*                          | One of the four WAMP core operations **register**, **call**, **subscribe** and **publish**            |


{align="left"}
| Term                              | Definition                                                                                            |
|-----------------------------------|-------------------------------------------------------------------------------------------------------|
| *Caller*                          |                                                                                                       |
| *Callee*                          |                                                                                                       |
| *Procedure*                       |                                                                                                       |
| *Registration*                    |                                                                                                       |
| *Call*                            |                                                                                                       |
| *Invocation*                      |                                                                                                       |


{align="left"}
| Term                              | Definition                                                                                            |
|-----------------------------------|-------------------------------------------------------------------------------------------------------|
| *Publisher*                       |                                                                                                       |
| *Subscriber*                      |                                                                                                       |
| *Topic*                           |                                                                                                       |
| *Subscription*                    |                                                                                                       |
| *Publication*                     |                                                                                                       |
| *Event*                           |                                                                                                       |
