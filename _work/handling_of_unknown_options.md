Handling of Unknown Options
---------------------------

We want WAMP implementations to be forwards compatible, i.e. an older implementation should be able to talk to a newer one with additional features.

There are two stages where this is important:

1. A peer with a more basic implementation connecting to one with more advanced features.
2. A peer with an advanced feature attempting to use the feature, but the other peer (or, with RPCs, the callee) does not support the feature.

For 1., the connection stage, with the feature announcement we use a peer just ignores any unknown features which are announced. 

For 2. let's first take a look at some actual use cases:

1. A client which uses subscriber black/whitelisting connects to a broker which does not support this and sends messages with subscribers blacklisted. The blacklisted subscribers receive events.
2. A client which uses progressive call results issues a call to a callee which does not support the feature. It does not receive any progressive call results.
3. A client which requires publisher identification and a publisher are connected via a broker which does not implement the feature. The client does not receive any publisher details.
4. A router tries to authenticate a client which does not support authentication.

Case 4. is the odd one out, since this uses an unknown message. Here the only sane option is to drop the connection. A peer simply cannot handle unknown messages. With the example of authentication, this would otherwise leave things hanging indefinitely.

The other cases may be problematic to the application trying to use the features to varying degrees, e.g. with 1. the blacklisted subscribers receiving an event may be really bad, while the non-availability of progressive call resulst in 2. may only mean that the application cannot display a progress bar, but otherwise works. 

In all of 1. - 3., because of the forwards compatibility, the router cannot give the clients any error feedback. 

Feature announcement is a solution to this for the application: Since features are required to be announced, older implementations can correctly be identified. The application can then decide how to handle the lack of any features it uses. It may do anything from closing the connection to going into a mode where the reduced features available are handled through reduced functionality.


Error handling during the session lifetime
------------------------------------------

Routers that do not implement a feature cannot give any error feedback. An action will succeed without the feature. It is up to the application to decide what to do. 

Different from these are the cases where a peer offers a feature or is at least aware of it, and receives a message which uses this feature without a prior announcement by the other peer, e.g.

   A client has not announced support for progressive call results to a router which supports the feature. The client then sends a call which requests progressive call results.

This is not something that is connected to forwards compatibility: Both the client and the router implement the feature, and the client takes an action which directly contradicts its earlier announcement to the contrary. This is a protocol error and should lead to the connection being dropped.


Special Case: Callee Cooperation
--------------------------------

With the majority of advanced features the implemenation is required in two peers (client/router). For some, however, there are three involved parties. For example:

   A client has announced support for progressive call results, and so has the router. The client then issues a call with a request for progressive call results, but the callee does not support the feature.

This is not an error on the caller's side: Feature announcement only covers the router's capabilities. The router is aware of the problem and should give feedback to the caller. 