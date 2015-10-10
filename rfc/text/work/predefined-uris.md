# Predefined URIs

WAMP predefines the following URIs in the *advanced profile*. For URIs, used in *basic profile*, please, see appendix in basic profile specification.

## Predefined Errors

*Dealer* or *Callee* canceled a call previously issued

    wamp.error.canceled

A *Peer* requested an interaction with an option that was disallowed by the *Router*

    wamp.error.option_not_allowed

A *Dealer* could not perform a call, since a procedure with the given URI is registered, but *Callee Black- and Whitelisting* and/or *Caller Exclusion* lead to the exclusion of (any) *Callee* providing the procedure.

    wamp.error.no_eligible_callee

A *Router* rejected client request to disclose its identity

    wamp.error.option_disallowed.disclose_me

A *Router* encountered a network failure

    wamp.error.network_failure
