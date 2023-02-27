## Authorization {#authorization}

WAMP allows user services to integrate seamlessly while enabling *Clients* to perform *Actions*, namely, to

* **register** procedures using fully qualified URIs or URI patterns in order to receive invocations
* **call** procedures at (fully qualified) URIs
* **subscribe** to topics on fully qualified URIs or URI patterns receiving events
* **publish** events to (fully qualified) URIs

Doing so requires *Clients* to have an open *Session* to the same shared *Realm*.

A *Session* is established originating from a *Client* to a *Router*.

*Session*s MAY be required to *Authenticate* to a *Router* on a *Realm*.

*Authentication* lets the *Router* verify the identity of a *Session* often as a prerequisite to allowing access to resources in a *Realm*.

When the *Session* authenticates to a *Router* successfully, the *Router* will have established

* `realm|string`
* `authrole|string`
* `authid|string`

_for_ that *Session* running _in_ that *Client*.

The triple `(realm, authrole, authid)` is called *Principal*, and the *Session* is authenticated under that *Principal*.

At any moment, there can be zero, one or many *Session*s with different `sessionid|int`s authenticated under the _same_ *Principal*.

*Session*s MAY be required to *Authorize* to perform a specific *Action* on an URI or URI pattern in a *Realm*.

This distinction between *Authentication* and *Authorization* follows the established practice called "AAA":

- **A**uthentication: Establishes who it is (**"subject"**)?
- **A**uthorization: Decide in a *Realm* whether *Action* (**"operation"**) on URI or URI pattern (**"object"**) is allowed for the requesting *Principal* (**"subject"**)?
- **A**ccounting: Record for a *Realm* what *Action* (**"operation"**) on what URI or URI pattern (**"object"**) was requested by which *Principal* (**"subject"**), and was it allowed or denied?
