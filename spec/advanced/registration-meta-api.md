### Callee Events

In certain scenarios, application components might be interested in getting notified when a *Dealer* registers or unregisters a *Callee* for a procedure on a *different* session.

When a *Callee* registers a procedure at a *Dealer*, the *Dealer* can signal the registration to other components by publishing a WAMP metaevent:

  wamp.procedure.on_register

Further, a *Dealer* might *additionally* publish a WAMP event upon the first *Callee* registering for a given procedure:

  wamp.procedure.on_first_register

A *Callee* has unregistered a (previously registered) procedure, either actively (via `UNREGISTER`) or because the *Callee* session has closed or the underlying transport was closed or dropped:

  wamp.procedure.on_unregister

When the last *Callee* registered for a given procedure has unregistered, a *Dealer* might *additionally* publish a WAMP event:

  wamp.procedure.on_last_unregister

*Event Contents*

FIXME

*Configuration*

When a *Dealer* supports *Callee Events*, it might

* simply produce respective WAMP metaevents always or
* it might produce WAMP metaevents only when the URI of the respective procedure was configured for *Callee Events* or

Note that generating above WAMP metaevents is never under control of the *Callee* registering/unregistering or the *Subscriber* to the metaevent.

A *Subscriber* that has subscribed to a *Callee* metaevent will (when authorized) receive respective metaevents for *all* procedures configured to trigger metaevents. The *Subscriber* cannot subscribe to *Callee* metaevents only for a single or a set of procedures.

*Feature Announcement*

FIXME


### Callee Listing

Write me.


