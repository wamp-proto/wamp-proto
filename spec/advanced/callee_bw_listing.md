### Callee Black- and Whitelisting

Support for this feature MUST be announced by *Callers* (`role := "caller"`) and *Dealers* (`role := "dealer"`) via

    HELLO.Details.roles.<role>.features.callee_blackwhite_listing|bool := true


A *Caller* may restrict the endpoints that will handle a call beyond those registered via

 * `CALL.Options.exclude|list`
 * `CALL.Options.eligible|list`

`CALL.Options.exclude` is a list of WAMP session IDs (`integer`s) providing an explicit list of (potential) *Callees* that a call won't be forwarded to, even though they might be registered. In other words, `CALL.Options.exclude` is a blacklist of (potential) *Callees*.

`CALL.Options.eligible` is a list of WAMP session IDs (`integer`s) providing an explicit list of (potential) *Callees* that are (potentially) forwarded the call issued. In other words, `CALL.Options.eligible` is a whitelist of (potential) *Callees*.

The *Dealer* will forward a call only to registered *Callees* that are not explicitly excluded via `CALL.Options.exclude` **and** which are explicitly eligible via `CALL.Options.eligible`.

*Example*

    [48, 7814135, {"exclude": [7891255, 1245751]}, "com.myapp.echo", ["Hello, world!"]]

The above call will (potentially) get forwarded to all *Callees* of `com.myapp.echo`, but not WAMP sessions with IDs `7891255` or `1245751` (and also not the calling session).

*Example*

    [48, 7814135, {"eligible": [7891255, 1245751]}, "com.myapp.echo", ["Hello, world!"]]

The above call will (potentially) get forwarded to WAMP sessions with IDs `7891255` or `1245751` only - but only if those are registered for the procedure `com.myapp.echo`.

*Example*

    [48, 7814135, {"exclude": [7891255], "eligible": [7891255, 1245751, 9912315]},
      "com.myapp.echo", ["Hello, world!"]]

The above call will (potentially) get forwarded to WAMP sessions with IDs `1245751` or `9912315` only (since `7891255` is excluded) - but only if those are registered for the procedure `com.myapp.echo`.
