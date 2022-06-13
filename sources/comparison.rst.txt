:github_url: https://github.com/wamp-proto/wamp-proto/edit/master/docs/comparison.rst

WAMP compared
=============


| Alright. So how does WAMP stack up versus other technologies?
| Do we really need another wheel? Yes. Please read below to find out
  why we think so.

Below you'll find a table comparing WAMP to other technologies according
to **six criteria**:

#. **PubSub**
   Does it support Publish & Subscribe out of the box?
#. **RPC**
   Does it support Remote Procedure Calls out of the box?
#. **Routed RPC**
   Does it support `routed </why/#unified_routing>`__ (not only
   point-to-point) Remote Procedure Calls?
#. **Web native**
   Does it run *natively* on the Web (without tunneling or bridging)?
#. **Cross Language**
   Does it work from different programming languages and run-times?
#. **Open Standard**
   Is there an open, official specification implemented by different
   vendors?

See also: `Web Technologies for the Internet of
Things <http://iotiran.com/media/k2/attachments/web-technologies.pdf>`__
- A master thesis which contains a comparison of WAMP, MQTT, CoAP, REST,
SOAP, STOMP and MBWS for IoT applications.

+---------------------------------+----------+---------+--------------+--------------+------------------+-----------------+
| Technology                      | PubSub   | RPC     | Routed RPC   | Web native   | Cross Language   | Open Standard   |
+---------------------------------+----------+---------+--------------+--------------+------------------+-----------------+
| WAMP                            | ✔        | ✔       | ✔            | ✔            | ✔                | ✔               |
+---------------------------------+----------+---------+--------------+--------------+------------------+-----------------+
| `AJAX <#ajax>`__                | **-**    | ✔       | **-**        | ✔            | ✔                | **-**           |
+---------------------------------+----------+---------+--------------+--------------+------------------+-----------------+
| `AMQP <#amqp>`__                | ✔        | (✔)     | **-**        | **-**        | ✔                | ✔               |
+---------------------------------+----------+---------+--------------+--------------+------------------+-----------------+
| `Apache Thrift <#thrift>`__     | **-**    | ✔       | **-**        | **-**        | ✔                | **-**           |
+---------------------------------+----------+---------+--------------+--------------+------------------+-----------------+
| `Capn'n'Proto <#capnnproto>`__  | **-**    | ✔       | **-**        | **-**        | ✔                | **-**           |
+---------------------------------+----------+---------+--------------+--------------+------------------+-----------------+
| `Comet <#comet>`__              | **-**    | **-**   | **-**        | ✔            | ✔                | **-**           |
+---------------------------------+----------+---------+--------------+--------------+------------------+-----------------+
| `OMG DDS <#omg-dds>`__          | ✔        | **-**   | **-**        | **-**        | ✔                | ✔               |
+---------------------------------+----------+---------+--------------+--------------+------------------+-----------------+
| `D-Bus <#d-bus>`__              | ✔        | ✔       | ✔            | **-**        | ✔                | ✔               |
+---------------------------------+----------+---------+--------------+--------------+------------------+-----------------+
| `CORBA <#corba>`__              | ✔        | ✔       | **-**        | **-**        | ✔                | ✔               |
+---------------------------------+----------+---------+--------------+--------------+------------------+-----------------+
| `DCOM <#dcom>`__                | ✔        | ✔       | **-**        | **-**        | ✔                | **-**           |
+---------------------------------+----------+---------+--------------+--------------+------------------+-----------------+
| `Java JMS <#jms>`__             | ✔        | **-**   | **-**        | **-**        | **-**            | ✔               |
+---------------------------------+----------+---------+--------------+--------------+------------------+-----------------+
| `Java RMI <#java-rmi>`__        | **-**    | ✔       | **-**        | **-**        | **-**            | ✔               |
+---------------------------------+----------+---------+--------------+--------------+------------------+-----------------+
| `JSON-RPC <#json-rpc>`__        | **-**    | ✔       | **-**        | ✔            | ✔                | ✔               |
+---------------------------------+----------+---------+--------------+--------------+------------------+-----------------+
| `MQTT <#mqtt>`__                | ✔        | **-**   | **-**        | **-**        | ✔                | ✔               |
+---------------------------------+----------+---------+--------------+--------------+------------------+-----------------+
| `OPC-UA <#opc-ua>`__            | (✔)        | ✔     | **-**        | (✔)          | ✔                | ✔               |
+---------------------------------+----------+---------+--------------+--------------+------------------+-----------------+
| `REST <#rest>`__                | **-**    | ✔       | **-**        | ✔            | ✔                | **-**           |
+---------------------------------+----------+---------+--------------+--------------+------------------+-----------------+
| `SOAP <#soap>`__                | **-**    | ✔       | **-**        | ✔            | ✔                | ✔               |
+---------------------------------+----------+---------+--------------+--------------+------------------+-----------------+
| `socket.io <#socketio>`__       | ✔        | **-**   | **-**        | ✔            | **-**            | **-**           |
+---------------------------------+----------+---------+--------------+--------------+------------------+-----------------+
| `SockJS <#sockjs>`__            | **-**    | **-**   | **-**        | ✔            | ✔                | **-**           |
+---------------------------------+----------+---------+--------------+--------------+------------------+-----------------+
| `STOMP <#stomp>`__              | ✔        | **-**   | **-**        | ✔            | ✔                | ✔               |
+---------------------------------+----------+---------+--------------+--------------+------------------+-----------------+
| `XML-RPC <#xml-rpc>`__          | **-**    | ✔       | **-**        | ✔            | ✔                | ✔               |
+---------------------------------+----------+---------+--------------+--------------+------------------+-----------------+
| `XMPP <#xmpp>`__                | ✔        | **-**   | **-**        | ✔            | ✔                | ✔               |
+---------------------------------+----------+---------+--------------+--------------+------------------+-----------------+
| `ZMQ <#zmq>`__                  | ✔        | **-**   | **-**        | **-**        | ✔                | **-**           |
+---------------------------------+----------+---------+--------------+--------------+------------------+-----------------+

.. rubric:: AJAX
   :name: ajax

`AJAX <http://en.wikipedia.org/wiki/Ajax_(programming)>`__ is neither a
protocol nor an API, but a programming pattern for JavaScript in
browsers that uses HTTP requests to realize RPC-like communication
between frontends (browsers) and backends.

AJAX being a programming practice, isn't a complete RPC system either.
You need to agree upon how calls, results and errors are formatted and
serialized. See `JSON-RPC <#json-rpc>`__ and `XML-RPC <#xml-rpc>`__.

Even when you bake some RPC mechanism using AJAX techniques, this is
point-to-point RPC: calls aren't routed between different servers or
application components, but strictly travel from point (browser) to
point (server the browser is connected to).

Further, AJAX does not provide PubSub - in fact, it doesn't address how
to actively push any kind of information from server to client (however,
see `Comet <#comet>`__).

Since AJAX uses plain HTTP for wrapping any kind of RPC-like messages,
it suffers from the overhead and limitations intrinsic to HTTP. E.g. you
cannot have more than 6-8 concurrent RPCs, as browsers will limit the
number of HTTP connections to a single destination.

.. rubric:: AMQP
   :name: amqp

`AMQP <http://en.wikipedia.org/wiki/Advanced_Message_Queuing_Protocol>`__
is a ...



.. rubric:: Apache Thrift
   :name: thrift

`Apache Thrift <https://thrift.apache.org/>`__ is a cross-language RPC
system. It uses a statically typed approach where procedures first need
to be described using an `Interface Definition
Language <http://en.wikipedia.org/wiki/Interface_definition_language>`__,
and then code for language specific bindings needs to be generated.

Compared to WAMP, Apache Thrift only provides RPC as an application
messaging pattern, not PubSub.

While Thrift uses a statically typed approach involving IDLs and code
generation, WAMP follows a dynamic typing approach. There is no IDL and
no code generation. Instead, WAMP will provide run-time reflection
capabilities instead.

Different from WAMP, Thrift also (only) runs over raw TCP and cannot
(natively) run over the Web, right into the browser. It is designed for
communication within the data-center, between backend components.

Similar to WAMP, Apache Thrift features different serialization formats,
and also is able to compress a transport (using zlib). WAMP currently
offers two serializations (JSON and MsgPack) and can run over standard,
compressed WebSocket ("permessage-deflate") to further reduce wire
traffic.

Apache Thrift currently has a lot more language bindings than WAMP and
is used/pushed by Facebook.


.. rubric:: Capn'n'Proto
   :name: capnnproto

`Capn'n'Proto <http://kentonv.github.io/capnproto/>`__ is a ...


.. rubric:: Comet
   :name: comet

`Comet <http://en.wikipedia.org/wiki/Comet_(programming)>`__ is a ...


.. rubric:: OMG DDS
   :name: omg-dds

OMG's `Data Distribution
Service <http://en.wikipedia.org/wiki/Data_Distribution_Service>`__ is a
...


.. rubric:: D-Bus
   :name: d-bus

`D-Bus <http://en.wikipedia.org/wiki/D-Bus>`__ is a platform-neutral messaging service that runs by default in most Linux distributions. It offers the same two basic workflows as WAMP, but whereas WAMP is designed for use over a network, D-Bus is designed for inter-process communication (IPC) on a single host.


.. rubric:: CORBA
   :name: corba

`CORBA <http://en.wikipedia.org/wiki/Corba>`__ is a ... CORBA
Notification Services


.. rubric:: DCOM
   :name: dcom

`DCOM <http://en.wikipedia.org/wiki/Dcom>`__ is a ...
`specification <http://msdn.microsoft.com/library/cc201989.aspx>`__ COM+
Event Service


.. rubric:: Java Message Service (JMS)
   :name: jms

`Java Message Service
(JMS) <http://en.wikipedia.org/wiki/Java_Message_Service>`__ is a Java
**API** specification for an (abstract) PubSub service. Programs are
written in Java against the JMS API. JMS does not provide RPC (but see
`Java RMI <#java-rmi>`__).

JMS does not guarantee interoperability between implementations, and the
JMS-compliant messaging system in use may need to be deployed on both
client and server.

In contrast, WAMP is a wire-level protocol specification. Conforming
WAMP implementations will be able to talk transparently to each other,
and different implementations can be mixed and matched in one larger
system.


.. rubric:: Java RMI
   :name: java-rmi

`Java
RMI <http://en.wikipedia.org/wiki/Java_remote_method_invocation>`__ is a
...


.. rubric:: JSON-RPC
   :name: json-rpc

`JSON-RPC <http://json-rpc.org/>`__ is a ...


.. rubric:: MQTT
   :name: mqtt

`MQTT <http://en.wikipedia.org/wiki/Mqtt>`__ is a ...

.. rubric:: OPC-UA
   :name: opc-ua

`OPC-UA <https://en.wikipedia.org/wiki/OPC_Unified_Architecture>`__ is
protocol and communication stack with roots in industrial automation.
It's an open standard with a complex and abstract set of specifications
that have different conrete mappings or bindings, eg for the transport
layer: there are two transport layer bindings defined.

OPC-UA / UA-TCP runs over port 4840 and carries payload in a binary
encoded format. The binary format is proprietory to OPC-UA - it is not
used anywhere else. When using OPC-UA with UA-TCP as a transport, the
resulting protocol cannot traverse the Web and can't be implemented eg
in browsers. UA-TCP is a bandwidth efficient transport, and can
transport binary payload natively without escaping.

OPC-UA / UA-SOAP is based on HTTP/SOAP, runs over ports 80/443 and
carries XML enoded payload. When using OPC-UA with UA-SOAP as a
transport, the resulting protocol can traverse the Web and can be
implemented in browsers. UA-SOAP suffers from excessive verbosity and
inefficient use of wire bandwidth. Binary payloads can only be
transmitted in reencoded (escaped) form.

OPC-UA, both when using UA-TCP and UA-SOAP transports, suffer from open
ports requirement: each and every device/machine, running an OPC-UA
server, has to open a listening port for incoming OPC-UA client
connections. This is a **security issue**, since the attack surface now
is the whole collection of all devices and machines. It is also a
**networking issue**, since OPC-UA servers need to be directly reachable
from OPC-UA clients, and firewalls, NATs and proxies will hide OPC-UA
servers. And finally, it's a **coupling issue**, since the host names /
IP addresses of all OPC-UA servers (machines/devices) need to be known
to or discovered by OPC-UA clients, which introduces a coupling between
application code and infrastructure/deployment artifacts (the hostnames
/ IP addresses).

OPC-UA servers can provide Notification services that are roughly
modeled after a Publish & Subscribe model. However, OPC-UA clients have
to **poll** for notifications and cannot receive events asynchronously and in
real-time. Increasing the polling frequency reduces the latency between
the occurence of an event in the machine (a change of a value in the
node tree of an OPA-UA server) and the actual reception of the event in
an OPC-UA client (via a response to a polling request on a
subscription), but the tradeoff is an increase in the wire traffic as
well (polling when no change occured).




.. rubric:: REST
   :name: rest

`REST <http://en.wikipedia.org/wiki/Representational_State_Transfer>`__
is neither a library, nor protocol or framework. It's a software
architecture style. REST stands for "Representational State Transfer"
and assumes that data should be transfered over network in one
of the standard formats like HTML, XML or JSON and follows an
architecture based on 6 limitations:

-  Uniform Interface
-  Stateless
-  Cacheable
-  Client-Server
-  Layered System
-  Code on Demand (optional)

In a World Wide Web, RESTful systems use URL for an information unit
address, and http status codes
for corresponding \ `CRUD <http://en.wikipedia.org/wiki/Create,_read,_update_and_delete>`__
operations.

It is difficult to compare the WAMP protocol and a software architecture
paradigm. They both are multilayered and can use different data
presentation format. But one of the clearest difference is that WAMP is
bidirectional, while REST pattern is not. In RESTful applications only
client acts as initiator for data manipulations, and there is no options
about how server can send data to client. In contrast to this, WAMP
workflow allows data to be transfered to and form server.

Another difference is that REST deliberately uses URLs from the HTTP
scheme which serve a dual function of **identifying** and **addressing**
resources. With WAMP, URIs are formed **com.example.myprocedure** and
only **identify**, but NOT address the procedure to be called. This
means, the implementation of the procedure can reside anywhere - it's
location is only known to the WAMP router. This provides location
transparency for WAMP application components.

There is no problem to use WAMP and REST together. For example, you can
make basic CRUD-operations over HTTP using GET/POST/PUT/DELETE methods,
and in parallel, use WAMP PubSub service for notifications about
changes, and WAMP RPC's for making some explicit business logic
operations (like sending SMS, or batch picture resizing and so on).


.. rubric:: SOAP
   :name: soap

`SOAP <http://en.wikipedia.org/wiki/SOAP>`__ is a ...

Being based on `XML Information
Set <http://en.wikipedia.org/wiki/XML_Information_Set>`__ and XML for
serialization, SOAP is *extremely* verbose and inefficient on the wire.
Any kind of binary application payload first needs to be encoded.
Further, parsing and serialization with XML can produce significant CPU
loads. For these reasons alone, SOAP is considered unsuitable for
applications where wire level and battery efficiency come into play: IoT
and mobile.

SOAP usually runs over HTTP (or SMTP) as a transport. Recently,
Microsoft published a specification for running `SOAP over
WebSocket <http://msdn.microsoft.com/en-us/library/hh536812.aspx>`__.
This reduces the overhead induces by the HTTP protocol, allows for real
bidirectional messaging but retains the vast inefficiency that comes
from XML.

| "When relying on HTTP as a transport protocol and not using
  `WS-Addressing <http://en.wikipedia.org/wiki/WS-Addressing>`__ or an
  `ESB <http://en.wikipedia.org/wiki/Enterprise_service_bus>`__, the
  roles of the interacting parties are fixed. Only one party (the
  client) can use the services of the other. Developers must use polling
  instead of notification in these common cases."
| From: `Wikipedia on SOAP <http://en.wikipedia.org/wiki/SOAP>`__

In contrast, WAMP provides all roles to any client. A WAMP client can
act as a Caller, Callee, Publisher and Subscriber, all at the same time.
This works with all WAMP transports. WAMP has built transport
independent addressing and routing right into the protocol.


.. rubric:: socket.io
   :name: socketio

`socket.io <http://socket.io/>`__ is a client-server PubSub service
implementation written in JavaScript. It uses node.js on server side,
browser counter part and own communication protocol. Socket.IO uses
WebSocket under the hood, when it's possible, but also has a polyfill as
fallback.

Comparing to WAMP, library allows you to subscribe to different topics,
has a broadcast messages and message namespaces, which works like
a realms in WAMP. Binary data transfer is possible, but that needs
additional modules on both sides
(`socket.io-stream <https://github.com/nkzawa/socket.io-stream>`__)
and additional amount of work for developers. They need to program
that explicitly.

Socket.IO does not provide remote procedure calls.


.. rubric:: SockJS
   :name: sockjs

`SockJS <https://github.com/sockjs>`__ is a WebSocket emulation/polyfill
library and provides a transport for raw, bidirectional, message-based
communication between two directly connected peers (a browser and a
server).

The `SockJS JavaScript
client <https://github.com/sockjs/sockjs-client>`__ adds a
WebSocket-like API for JavaScript in browsers lacking native WebSocket
support. The bidirectional communication capabilities of WebSocket are
emulated using various mechanism under the hood, including HTTP
long-poll. The `"emulation"
protocol(s) <http://sockjs.github.io/sockjs-protocol/sockjs-protocol-dev.html>`__
must be implemented on the server-side (available server implementations
include NodeJS, Ruby and Erlang).

Compared to WAMP, SockJS is lower level in that it is only concerned
about the *transport layer*. It does not provide *application messaging
patterns* like RPC or PubSub.

WAMP also provides a **HTTP Long-poll transport** as a fallback for
browsers lacking native WebSocket support. There are fewer fallback
variants for WAMP than SockJS currently specified (only "long-poll"),
but this transport also supports binary messages and all WAMP
serialization formats (JSON and MsgPack currently). I am
`unsure <https://github.com/sockjs/sockjs-protocol/issues/74>`__ if
SockJS supports binary messages at all.


.. rubric:: STOMP
   :name: stomp

`STOMP <http://en.wikipedia.org/wiki/Streaming_Text_Oriented_Messaging_Protocol>`__
is a ...


.. rubric:: XML-RPC
   :name: xml-rpc

`XML-RPC <http://en.wikipedia.org/wiki/XML-RPC>`__ is a ...


.. rubric:: XMPP
   :name: xmpp

`XMPP <http://en.wikipedia.org/wiki/XMPP>`__ is a ...


.. rubric:: ZMQ
   :name: zmq

`ZMQ <http://en.wikipedia.org/wiki/Zero_MQ>`__ is a light-weight,
high-performance library for messaging between application components.
It works without a server. http://zeromq.org/whitepapers:brokerless

While ZMQ has a request-response message exchange pattern ("REQ-REP
sockets"), it does not support RPC out of the box. There exist libraries
(e.g. `ZeroRPC <http://zerorpc.dotcloud.com/>`__ by Docker or
`ThriftZMQ <https://github.com/thriftzmq/thriftzmq-java>`__) that layer
on top of ZMQ to provide applications with first-class RPC services.

`to Top <#top>`__
