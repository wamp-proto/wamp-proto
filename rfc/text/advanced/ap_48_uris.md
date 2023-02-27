# Advanced Profile URIs {#ap-uris}

WAMP pre-defines the following error URIs for the **Advanced Profile**. WAMP peers SHOULD only use the defined error messages.

## Authentication

No authentication method the *Client* offered is accepted.

{align="left"}
        wamp.error.no_auth_method

The *Client* authenticated for a *Realm* (`realm|string`) that does not (or no longer) exists.

{align="left"}
        wamp.error.no_such_realm

The *Client* authenticated for a *Role* (`authrole|string`) that does not (or no longer) exists.

{align="left"}
        wamp.error.no_such_role

The *Client* authenticated for a *Principal* (`authid|string`) that does not (or no longer) exists.

{align="left"}
        wamp.error.no_such_principal

The authentication as presented by the *Client* is denied (e.g. "wrong password").

{align="left"}
        wamp.error.authentication_denied

The authentication of the *Client* failed technically at run-time, and the *Client* is therefor rejected ("fail secure operation").

{align="left"}
        wamp.error.authentication_failed

The *Client* did not authenticate (at all) and a successful (non-anonymous) authentication is required.

{align="left"}
        wamp.error.authentication_required

## Authorization

The *Principal* is not authorized to perform such *Action*.

{align="left"}
        wamp.error.authorization_denied

Authorization of the *Principal* for the *Action* could not be determined as it failed technically at run-time, and the *Action* is therefor rejected ("fail secure operation").

{align="left"}
        wamp.error.authorization_failed

Authorization of the *Principal* is required for each individual execution of the *Action*. This can be used for capability-based access control.

{align="left"}
        wamp.error.authorization_required

## Remote Procedure Calls

A *Dealer* or *Callee* canceled a call previously issued

{align="left"}
        wamp.error.canceled

A *Dealer* or *Callee* terminated a call that timed out

{align="left"}
        wamp.error.timeout

A *Peer* requested an interaction with an option that was disallowed by the *Router*

{align="left"}
        wamp.error.option_not_allowed

A *Router* rejected client request to disclose its identity

{align="left"}
        wamp.error.option_disallowed.disclose_me

A *Router* encountered a network failure

{align="left"}
        wamp.error.network_failure

A *Callee* is not able to handle an invocation for a *call* and intends for the *Router* to re-route the *call* to another fitting *Callee*. For details, refer to [RPC Call Rerouting](ap_rpc_call_rerouting.md)

{align="left"}
        wamp.error.unavailable

A *Dealer* could not perform a call, since a procedure with the given URI is registered, but all available registrations have responded with `wamp.error.unavailable`

{align="left"}
        wamp.error.no_available_callee

A *Dealer* received a `CALL` message with advanced features that cannot be processed by the *Callee*

{align="left"}
        wamp.error.feature_not_supported

