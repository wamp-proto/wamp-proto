Introduction
============

WebSocket
---------

The WebSocket protocol brings bi-directional (soft) real-time and wire traffic efficient
connections to the browser. Today (2018) WebSocket is universally supported in browsers,
network equipment, servers and client languages.

.. note::

    If you want to read more about WebSocket, we recommend two blog posts of the creators
    of WAMP;)

    * `WebSocket - Why, what, and - can I use it? <https://crossbario.com/blog/Websocket-Why-What-Can-I-Use-It/>`_
    * `Dissecting WebSocket's Overhead <https://crossbario.com/blog/Dissecting-Websocket-Overhead/>`

Despite having opened completely new possibilities on the Web, WebSocket defines an API for
application developers at the *message* level, and *point-to-point*, requiring users who want
to use WebSocket connections in their applications to define their own semantics on top of it.

The Web Application Messaging Protocol (WAMP) aims to provide application developers
with the right level of semantics, with what they need to handle messaging and communication
between components in distributed applications at a convenient and abstracted way.


WAMP
----

WAMP was initially defined as a WebSocket sub-protocol, which provided
**Publish & Subscribe (PubSub)** functionality as well as **routed Remote Procedure Calls (rRPC)**
for procedures implemented in a WAMP router. Feedback from implementers and users of this was
included in a second version of the protocol which this document defines. Among the changes
was that WAMP can now run over any transport which is message-oriented, ordered, reliable,
and bi-directional.

WAMP is a routed protocol, with all components connecting to a _WAMP Router_, where the
WAMP Router performs message routing between the components.

WAMP provides two messaging patterns:

* Publish & Subscribe and 
* routed Remote Procedure Calls

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


Routed RPC Advantages
---------------------

The decoupling in routed RPCs arises from the fact that the Caller is no longer required to
have knowledge of the Callee; it merely needs to know the identifier of the procedure it
wants to call. There is also no longer a need for a direct connection between the caller and
the callee, since all traffic is routed. This enables the calling of procedures in components
which are not reachable externally (e.g. on a NATted connection) but which can establish an
outgoing connection to the WAMP router.

This decoupling of transport and application layer traffic allows a "reversal of command"
where a cloud-based system can call into a device behind firewalls or NATs outside the cloud.
It also allows to treat frontend and backend components (microservices) the same, and it
even allows to develop backend code in the browser
(`Free Your Code - Backends in the Browser <https://crossbario.com/blog/Free-Your-Code-Backends-in-the-Browser/>`_).

Since no ports on edge devices need to be opened for WAMP to work (in both directions), the
remote attack surface of these (potentially many) devices is completely closed
(`Security in the IoT  <https://crossbario.com/static/presentations/iot-security/index.html>`_).

Finally, since the Caller is not aware where, or even who is processing the call (and it should
not care!), it is easily possible to make application components highly-available (using hot standby
components) or scale-out application components
(`Scaling microservices with Crossbar.io <https://crossbario.com/static/presentations/microservices/index.html>`_).

Combining these two patterns into a single protocol allows it to be used for the entire
messaging requirements of an application, thus reducing technology stack complexity, as
well as networking overheads. This is turn allows to quickly realize (and maintain) distributed
IoT applications like this one: `A Smarter Vending Machine <https://crossbario.com/blog/A-Smarter-Vending-Machine/>`_.
