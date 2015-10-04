### Shared Registration

Feature status: **alpha**

#### Feature Definition

As a default, only a single **Callee** may register a procedure for an URI.

There are use cases where more flexibility is required. As an example, for an application component with a high computing load, several instances may run, and load balancing of calls across these may be desired. As another example, in an an application a second or third component providing a procedure may run, which are only to be called in case the primary component is no longer reachable (hot standby).

When shared registrations are supported, then the first **Callee** to register a procedure for a particular URI MAY determine that additional registrations for this URI are allowed, and what **Invocation Rules** to apply in case such additional registrations are made.

This is done through setting

{align="left"}
        REGISTER.Options.invoke|string := <invocation_policy>

where <invocation_policy> is one of

* 'single'
* 'roundrobin'
* 'random'
* 'first'
* 'last'

If the option is not set, 'single' is applied as a default.

With 'single', the **Dealer** MUST fail all subsequent attempts to register a procedure for the URI while the registration remains in existence.

With the other values, the **Dealer** MUST fail all subsequent attempst to register a procedure for the URI where the value for this option does not match that of the initial registration. 

##### Load Balancing

For sets of registrations registered using either 'roundrobin' or 'random', load balancing is performed across calls to the URI. 

For 'roundrobin', callees are picked subsequently from the list of registrations (ordered by the order of registration), with the picking looping back to the beginning of the list once the end has been reached.

For 'random' a callee is picked randomly from the list of registrations for each call.

##### Hot Stand-By

For sets of registrations registered using either 'first' or 'last', the first respectively last callee on the current list of registrations (ordered by the order of registration) is called. 


#### Feature Announcement

Support for this feature MUST be announced by *Callees* (`role := "callee"`) and *Dealers* (`role := "dealer"`) via

{align="left"}
        HELLO.Details.roles.<role>.features.
            shared_registration|bool := true
