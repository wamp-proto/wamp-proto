-- move to: "ap_transport_multiplexed.md" --

# Multiplexed Transport

A *Transport* may support the multiplexing of multiple logical transports over a single "physical" transport.

By using such a *Transport*, multiple WAMP sessions can be transported over a single underlying transport at the same time.

![alt text](../figure/sessions3.png "Transports, Sessions and Peers")

As an example, the proposed [WebSocket extension "permessage-priority"](https://github.com/oberstet/permessage-priority/blob/master/draft-oberstein-hybi-permessage-priority.txt) would allow creating multiple logical *Transports* for WAMP over a single underlying WebSocket connection.

Sessions running over a multiplexed *Transport* are completely independent: they get assigned different session IDs, may join different realms and each session needs to authenticate itself.

Because of above, *Multiplexed Transports* for WAMP are actually not detailed in the WAMP spec, but a feature of the transport being used.

> Note: Currently no WAMP transport supports multiplexing. The work on the MUX extension with WebSocket has stalled, and the `permessage-priority` proposal above is still just a proposal. However, with RawSocket, we should be able to add multiplexing in the the future (with downward compatibility).
