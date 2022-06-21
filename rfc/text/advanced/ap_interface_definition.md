### Interface Definition Language {#wamp-idl}

*Background*

WAMP was designed with the goals of being easy to approach and use for application developers. Creating a procedure to expose some custom functionality should be possible in any supported programming language using that language's native elements, with the least amount of additional effort.

Following from that, WAMP uses *dynamic typing* for the application payloads of calls, call results and error, as well as event payloads.

A WAMP router will happily forward *any* application payload on *any* procedure or topic URI as long as the client is _authorized_ (has permission) to execute the respective WAMP action (call, register, publish or subscribe) on the given URI.

This approach has served WAMP well, as application developers can get started immediately, and evolve and change payloads as they need without extra steps.
These advantages in flexibility of course come at a price, as nothing is free, and knowing that price is important to be aware of the tradeoffs one is accepting when using dynamic typing:

* problematic coordination of interfaces within larger developer teams or between different parties
* no easy way to stabilize, freeze, document or share interfaces
* no way to programmatically describe interfaces ("interface reflection") at run-time
* ...

*Introduction*

* application payload validation
* API autodocs Web service
* reflection in WAMP meta API
* binding code generation
