


Wire Efficiency
---------------

  * Implement WebSocket per-frame compression extension.
  * Provide pluggable, text/binary serialization formats.


PREFIX Message
--------------

With WAMPv1, the `PREFIX` message serves two purposes:

 1. ease usage of unwieldy long URIs for developers
 2. reduce wire traffic

See [here](http://wamp.ws/spec#prefix_message).

For WAMPv2, 1. is a feature of the WAMP implementation (i.e. dynamically create stub objects and methods). This provides i.e. auto-completition in IDEs and even more comfort.

For 2., see wire efficiency.

WAMPv2 will 

Both peers maintain a per-session map for mapping shorthands to fully qualified URIs.

The shorthands can be set by the peer via a message. That message can now go in both directions.

     [ MSG_TYPE_MAPURI,  <shorthand | str>,  <FQ URI | str>  ]

Effectively, this establishes two compression dicationaries for URIs with a scope and lifetime of WAMP session.


EVENT Message
-------------

    [ MSG_TYPE_EVENT,     <URI>, <Event> ]
    [ MSG_TYPE_EVENT_P,   <URI>, <Event>, <Publisher Session ID> ]
    [ MSG_TYPE_EVENT_I,   <URI>, <Event>, <Event ID> ]
    [ MSG_TYPE_EVENT_PI,  <URI>, <Event>, <Publisher Session ID>, <Event ID> ]


SUBSCRIBE Message
-----------------

    [ MSG_TYPE_SUBSCRIBE,   <URI> ]
    [ MSG_TYPE_SUBSCRIBE_E, <URI>, { .. extra info ..} ]

