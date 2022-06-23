## Basic Profile

**Incorrect URIs**

When a Peer provides an incorrect URI for any URI-based attribute of a WAMP message (e.g. realm, topic), then the other Peer MUST respond with an `ERROR` message and give the following *Error URI*:

{align="left"}
        wamp.error.invalid_uri


**Interaction**

Peer provided an incorrect URI for any URI-based attribute of WAMP message, such as realm, topic or procedure

{align="left"}
        wamp.error.invalid_uri

A Dealer could not perform a call, since no procedure is currently registered under the given URI.

{align="left"}
        wamp.error.no_such_procedure

A procedure could not be registered, since a procedure with the given URI is already registered.

{align="left"}
        wamp.error.procedure_already_exists

A Dealer could not perform an unregister, since the given registration is not active.

{align="left"}
        wamp.error.no_such_registration

A Broker could not perform an unsubscribe, since the given subscription is not active.

{align="left"}
        wamp.error.no_such_subscription

A call failed since the given argument types or values are not acceptable to the called procedure. In this case the Callee may throw this error. Alternatively a Router may throw this error if it performed *payload validation* of a call, call result, call error or publish, and the payload did not conform to the requirements.

{align="left"}
        wamp.error.invalid_argument

**Session Close**

The Peer is shutting down completely - used as a `GOODBYE` (or `ABORT`) reason.

{align="left"}
        wamp.close.system_shutdown

The Peer want to leave the realm - used as a `GOODBYE` reason.

{align="left"}
        wamp.close.close_realm

A Peer acknowledges ending of a session - used as a `GOODBYE` reply reason.

{align="left"}
        wamp.close.goodbye_and_out

A Peer received invalid WAMP protocol message (e.g. `HELLO` message after session was already established) - used as a `ABORT` reply reason.

{align="left"}
        wamp.error.protocol_violation

**Authorization**

A join, call, register, publish or subscribe failed, since the Peer is not authorized to perform the operation.

{align="left"}
        wamp.error.not_authorized

A Dealer or Broker could not determine if the Peer is authorized to perform a join, call, register, publish or subscribe, since the authorization operation *itself* failed. E.g. a custom authorizer did run into an error.

{align="left"}
        wamp.error.authorization_failed

Peer wanted to join a non-existing realm (and the Router did not allow to auto-create the realm).

{align="left"}
        wamp.error.no_such_realm

A Peer was to be authenticated under a Role that does not (or no longer) exists on the Router. For example, the Peer was successfully authenticated, but the Role configured does not exists - hence there is some misconfiguration in the Router.

{align="left"}
        wamp.error.no_such_role
