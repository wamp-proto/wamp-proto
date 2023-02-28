## Authorization {#authorization}

WAMP allows user services to integrate seamlessly while enabling *Clients* to perform *Actions*, namely, to

* **register** procedures using fully qualified URIs or URI patterns in order to receive invocations
* **call** procedures at (fully qualified) URIs
* **subscribe** to topics using fully qualified URIs or URI patterns in order to receive events
* **publish** events to (fully qualified) URIs

Performing these actions requires *Clients* to have an open *Session* to the same shared *Realm*.

A *Session* is established between a *Client* to a *Router*, and is initiated by a *Client*.

*Session*s MAY be required to *Authenticate* access to a *Realm* hosted by a *Router*.

*Authentication* is the sequence of operations that allow a *Router* to verify the identity of a *Session*, often as a prerequisite to allowing access to resources within a *Realm*.

When the *Session* authenticates to a *Router* successfully, the *Router* will have established the

* `realm|string`,
* `authrole|string`, and
* `authid|string`

for that *Session* running in the *Client*.

The triple `(realm, authrole, authid)` is called *Principal*, and a *Session* is authenticated under that *Principal*.

At any moment, there can be zero, one, or many *Session*s with different *session ids* authenticated under the _same_ *Principal*.

*Session*s MAY be required to *Authorize* in order to perform a specific *Action* on an URI — or an URI pattern — within a *Realm*.

This distinction between *Authentication* and *Authorization* follows the established practice called "AAA":

- **A**uthentication: Establishes who it is (**"subject"**)
- **A**uthorization: Decides within a *Realm* whether an *Action* (**"operation"**) on an URI or URI pattern (**"object"**) is allowed for the requesting *Principal* (**"subject"**)
- **A**ccounting: Records, for a *Realm*, what *Action* (**"operation"**) on what URI or URI pattern (**"object"**) was requested by which *Principal* (**"subject"**), and whether it was allowed or denied
