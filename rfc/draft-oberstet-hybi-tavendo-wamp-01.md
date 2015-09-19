% Title = "Web Application Messaging Protocol - Basic Profile"
% abbrev = "Web Application Messaging Protocol - Basic Profile"
% category = "std"
% docName = "draft-oberstet-hybi-tavendo-wamp-01"
% ipr= "trust200902"
% area = "Applications and Real-Time (art)"
% workgroup = "BiDirectional or Server-Initiated HTTP"
% keyword = ["WebSocket, WAMP, real-time, RPC, PubSub"]
%
% date = 2015-09-17T00:00:00Z
%
% [pi]
% toc = "yes"
%
% #Independent Submission
% [[author]]
% initials="T.O."
% surname="Oberstein"
% fullname="Tobias G. Oberstein"
% organization = "Tavendo GmbH"
%   [author.address]
%   email = "tobias.oberstein@tavendo.de"
%   

.# Abstract

This document defines the basic profile for the Web Application Messaging Protocol (WAMP). WAMP is a routed protocol which provides two messaging patterns: Publish & Subscribe and routed Remote Procedure Calls. It is intended to connect application components in distributed applications. WAMP uses WebSocket as its default transport, but can be transmitted via any other protocol which allows for ordered, reliable, bi-directional and message-based communication.

{mainmatter}



# Introduction

## Background

_This section is non-normative._


-- write me --

* distributed applications the new norm
* realtime a requirement in many cases
* WebSocket a protocol which includes the browser in this
* WS is low-level
* a lot of protocols which implement PubSub on top
* quick PubSub overview
* this does not natively cover the full range of what application components want to communicate
* there is also a need to call procedures and receive results
* the common model for RPCs is a client-server connection. in distributed applications the need for each caller to be aware of the callee's identity and to establish a connection presents at least significant overhead, at worst makes connections impossible (NAT problem)
* WAMP provides routed RPCs in the same protocol as PubSub
* this enables all application messaging to run over a single protocol using native messaging patterns

## Protocol Overview

_This section is non-normative._

This document defines the basic profile of WAMP. The basic profile 

## Desing Philosophy

_This section is non-normative._

### Application Code

WAMP is designed for application code to run inside *Clients*, i.e. *Peers* of the roles *Callee*, *Caller*, *Publisher* and *Subscriber*.

*Routers*, i.e. *Peers* of the roles *Brokers* and *Dealers* are responsible for **generic call and event routing** and do not run application code.

This allows to transparently exchange *Broker* and *Dealer* implementations without affecting the application and to distribute and deploy application components flexibly:

-- adapt figure/appcode.png ---

> Note that a **program** that implements e.g. the *Dealer* role might at the same time implement e.g. a built-in *Callee*. It is the *Dealer* and *Broker* that are generic, not the program.
>

### Router Implementation Specifics

Specific WAMP *Broker* and *Dealer* implementations might differ in aspects such as:

* support for WAMP Advanced Profile
* router networks (clustering and federation)
* authentication and authorization schemes
* message persistence
* management and monitoring

The definition and documentation of implementation specific *Router* features like above is outside the scope of this document.

## Security Model

_This section is non-normative._



# Conformance Requirements

## Terminology and Other Conventions

The keywords **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**,
**SHOULD NOT**, **RECOMMENDED**, **MAY**, and **OPTIONAL**, when they appear in this
document, are to be interpreted as described in [@?RFC2119].



# Realms, Sessions and Transports

A *Realm* is a WAMP routing and administrative domain (optionally) protected by authentication and authorization.
A *Session* is a transient conversation between two *Peers* attached to a *Realm* and running over a *Transport*.

-- adapt sessions2.npg --

A *Transport* connects two WAMP *Peers* and provides a channel over which WAMP messages for a WAMP *Session* can flow in both directions.

WAMP can run over different *transports*. A *Transport* suitable for WAMP must have the following characteristics:

* message-based
* bidirectional
* reliable
* ordered

The default transport for WAMP is [WebSocket](http://tools.ietf.org/html/rfc6455), where WAMP is an [officially registered](http://www.iana.org/assignments/websocket/websocket.xml) subprotocol. Other transports may be defined in a subsequent WAMP Advanced Profile document.

WAMP is currently defined for the following *serializations*:

* JSON
* MsgPack

When the transport allows for - as is the case with WebSocket - WAMP lets you combine the transport with any serialization.



# Peers and Roles

A WAMP *Session* connects two *Peers*, a *Client* and a *Router*. Each WAMP *Peer* can implement one or more roles.

A *Client* can implement any combination of the *Roles*:

 * *Callee*
 * *Caller*
 * *Publisher*
 * *Subscriber*

and a *Router* can implement either or both of the *Roles*:

 * *Dealer*
 * *Broker*

> This document describes WAMP as in client-to-router communication. Direct client-to-client communication is not supported by WAMP. Router-to-router communication MAY be defined by a specific router implementation.
>


## Symmetric Messaging

It is important to note that though the establishment of a *Transport* might have a inherent asymmetry (like a TCP client establishing a WebSocket connection to a server), and *Clients* establish WAMP sessions by attaching to *Realms* on *Routers*, WAMP itself is designed to be fully symmetric for application components.

After the transport and a session have been established, any application component may act as *Caller*, *Callee*, *Publisher* and *Subscriber* at the same time. And *Routers* provide the fabric on top of which WAMP runs a symmetric application messaging service.


## Remote Procedure Call Roles

The Remote Procedure Call messaging pattern involves peers of three different roles:

* *Callee (Client)*
* *Caller (Client)*
* *Dealer (Router)*

A *Caller* issues calls to remote procedures by providing the procedure URI and any arguments for the call.
The *Callee* will execute the procedure using the supplied arguments to the call and return the result of the call to the *Caller*.

*Callees* register procedures they provide with *Dealers*. *Callers* initiate procedure calls first to *Dealers*. *Dealers* route calls incoming from *Callers* to *Callees* implementing the procedure called, and route call results back from *Callees* to *Callers*.

The *Caller* and *Callee* will usually run application code, while the *Dealer* works as a generic router for remote procedure calls decoupling *Callers* and *Callees*.


## Publish & Subscribe Roles

The Publish & Subscribe messaging pattern involves peers of three different roles:

* *Subscriber (Client)*
* *Publisher (Client)*
* *Broker (Router)*

A *Publishers* publishes events to topics by providing the topic URI and any payload for the event. *Subscribers* of the topic will receive the event together with the event payload.

*Subscribers* subscribe to topics they are interested in with *Brokers*. *Publishers* initiate publication first at *Brokers*. *Brokers* route events incoming from *Publishers* to *Subscribers* that are subscribed to respective topics.

The *Publisher* and *Subscriber* will usually run application code, while the *Broker* works as a generic router for events decoupling *Publishers* from *Subscribers*.


## Peers with multiple Roles

Note that *Peers* might implement more than one role: e.g. a *Peer* might act as *Caller*, *Publisher* and *Subscriber* at the same time. Another *Peer* might act as both a *Broker* and a *Dealer*.



# Building Blocks

WAMP is defined with respect to the following building blocks

1.  Identifiers
2.  Serializations
3.  Transports

For each building block, WAMP only assumes a defined set of requirements, which allows to run WAMP variants with different concrete bindings.


## Identifiers

### URIs

WAMP needs to identify the following *persistent* resources:

1.  Topics
2.  Procedures
3.  Errors

These are identified in WAMP using *Uniform Resource Identifiers* (URIs) that MUST be Unicode strings.

> Note: When using JSON as WAMP serialization format, URIs (as other strings) are transmitted in UTF-8 encoding.

*Examples*

* com.myapp.mytopic1
* com.myapp.myprocedure1
* com.myapp.myerror1

The URIs are understood to form a single, global, hierarchical namespace for WAMP.

> The namespace is unified for topics, procedures and errors - these different resource types do NOT have separate namespaces.
>

To avoid resource naming conflicts, we follow the package naming convention from Java where URIs SHOULD begin with (reversed) domain names owned by the organization defining the URI.

#### Relaxed/Loose URIs

URI components (the parts between two `.`s, the head part up to the first `.`, the tail part after the last `.`) MUST NOT contain a `.`, `#` or whitespace characters and MUST NOT be empty (zero-length strings).

> The restriction not to allow `.` in component strings is due to the fact thate `.` is used to separate components, and WAMP associates semantics with resource hierarchies, such as in pattern-based subscriptions which may be part of an Advanced Profile. The restriction not to allow empty (zero-length) strings as components is due to the fact that this may be used to denote wildcard components with pattern-based subscriptions and registrations in an Advanced Profile. The character `#` is not allowed since this is reserved for internal use by *Dealers* and *Brokers*.

As an example, the following regular expression could be used in Python to check URIs according to above rules:

```python
## loose URI check disallowing empty URI components
pattern = re.compile(r"^([^\s\.#]+\.)*([^\s\.#]+)$")
```

When empty URI components are allowed (which may the case for specific messages which are part of an Advanced Profile), you can use this regular expression:

```python
## loose URI check allowing empty URI components
pattern = re.compile(r"^(([^\s\.#]+\.)|\.)*([^\s\.#]+)?$")
```

#### Strict URIs

While the above rules MUST be followed, following a stricter URI rule is recommeded: URI components SHOULD only contain letters, digits and `_`.

As an example, the following regular expression could be used in Python to check URIs according to the above rules:

```python
## strict URI check disallowing empty URI components
pattern = re.compile(r"^([0-9a-z_]+\.)*([0-9a-z_]+)$")
```

When empty URI components are allowed (which may the case for specific messages which are part of an Advanced Profile), you can use this regular expression:

```python
## strict URI check allowing empty URI components
pattern = re.compile(r"^(([0-9a-z_]+\.)|\.)*([0-9a-z_]+)?$")
```

> Following the suggested regular expression will make URI components valid identifiers in most languages (modulo URIs starting with a digit and language keywords) and the use of lower-case only will make those identifiers unique in languages that have case-insensitive identifiers. Following this suggestion can allow implementations to map topics, procedures and errors to the language environment in a completely transparent way.

#### Reserved URIs

Further, application URIs MUST NOT use `wamp` as a first URI component, since this is reserved for URIs predefined with the WAMP protocol itself.

*Examples*

* wamp.error.not_authorized
* wamp.error.procedure_already_exists




# Security Considerations

-- write me --

# IANA Considerations

TBD

# Appendixes

# References

# Contributors

# Acknowledgements

<reference anchor='DSM-IV' target='http://www.psychiatryonline.com/resourceTOC.aspx?resourceID=1'>
  <front>
   <title>Diagnostic and Statistical Manual of Mental Disorders (DSM)</title>
   <author></author>
   <date></date>
  </front>
</reference>

{backmatter}
