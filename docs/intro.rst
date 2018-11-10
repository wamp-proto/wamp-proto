:github_url: https://github.com/wamp-proto/wamp-proto/edit/master/docs/intro.rst

.. _Intro:

Introduction
============

WebSocket
---------

The WebSocket protocol brings bi-directional (soft) real-time and wire traffic efficient
connections to the browser. Today (2018) WebSocket is universally supported in browsers,
network equipment, servers and client languages.

Despite having opened completely new possibilities on the Web, WebSocket defines an API for
application developers at the *message* level, and *point-to-point*, requiring users who want
to use WebSocket connections in their applications to define their own semantics on top of it.

The Web Application Messaging Protocol (WAMP) aims to provide application developers
with the right level of semantics, with what they need to handle messaging and communication
between components in distributed applications at a convenient and abstracted way.

WAMP was initially defined as a WebSocket sub-protocol, which provided
**Publish & Subscribe (PubSub)** functionality as well as **routed Remote Procedure Calls (rRPC)**
for procedures implemented in a WAMP router. Feedback from implementers and users of this was
included in a second version of the protocol which this document defines. Among the changes
was that WAMP can now run over any transport which is message-oriented, ordered, reliable,
and bi-directional.

.. note::

    If you want to read more about WebSocket, we recommend two blog posts of the creators
    of WAMP;)

    * `WebSocket - Why, what, and - can I use it? <https://crossbario.com/blog/Websocket-Why-What-Can-I-Use-It/>`_
    * `Dissecting WebSocket's Overhead <https://crossbario.com/blog/Dissecting-Websocket-Overhead/>`_

WAMP
----

WAMP is a routed protocol, with all components connecting to a WAMP Router, where the
WAMP Router performs message routing between the components, and provides two messaging
patterns in one Web native protocol:

* **Publish & Subscribe (PubSub)** and 
* routed **Remote Procedure Calls (rRPC)**

Publish & Subscribe (PubSub) is an established messaging pattern where a component,
the Subscriber, informs the router that it wants to receive information on a topic
(i.e., it subscribes to a topic). Another component, a Publisher, can then publish
to this topic, and the router distributes events to all Subscribers.

Routed Remote Procedure Calls (rRPCs) rely on the same sort of decoupling that is used by
the Publish & Subscribe pattern. A component, the Callee, announces to the router that
it provides a certain procedure, identified by a procedure name. Other components,
Callers, can then call the procedure, with the router invoking the procedure on the
Callee, receiving the procedure's result, and then forwarding this result back to the Caller.
Routed RPCs differ from traditional client-server RPCs in that the router serves as an
intermediary between the Caller and the Callee.


**Advantages of decoupling and routed RPCs**

The decoupling in routed RPCs arises from the fact that the Caller is no longer required to
have knowledge of the Callee; it merely needs to know the identifier of the procedure it
wants to call. There no longer is a need for a direct network connection or path between the
caller and the callee, since all messages are routed at the WAMP level.

This approach enables a whole range os possibilities:

* calling into procedures in components which are not reachable from outside at the network
  level (e.g. on a NATted connection), but which can establish an outgoing network connection
  to the WAMP router.
* This decoupling of transport and application layer traffic allows a "reversal of command"
  where a cloud-based system can securely control remote devices
* It also allows to treat frontend and backend components (microservices) the same, and it
  even allows to develop backend code in the browser
  (`Free Your Code - Backends in the Browser <https://crossbario.com/blog/Free-Your-Code-Backends-in-the-Browser/>`_).
* Since no ports on edge devices need to be opened for WAMP to work (in both directions), the
  remote attack surface of these (potentially many) devices is completely closed
  (`Security in the IoT  <https://crossbario.com/static/presentations/iot-security/index.html>`_).
* Finally, since the Caller is not aware where, or even who is processing the call (and it should
  not care!), it is easily possible to make application components highly-available (using hot standby
  components) or scale-out application components
  (`Scaling microservices with Crossbar.io <https://crossbario.com/static/presentations/microservices/index.html>`_).


**Summary**

Combining the Publish & Subscribe and routed Remote Procedure Calls in one Web native, real-time
transport protocol (WebSocket) allows WAMP to be used for the entire messaging requirements of
component and microservice based applications, reducing technology stack complexity and overhead,
providing a capable and secure fundament for applications to rely on.
