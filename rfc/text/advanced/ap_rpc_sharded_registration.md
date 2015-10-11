### Sharded Registration

Feature status: **sketch**


#### Feature Definition

**Sharded Registrations** are intended to allow calling a procedure which is offered by a sharded database, by routing the call to a single shard.


#### "Partitioned" Calls

If `CALL.Options.runmode == "partition"`, then `CALL.Options.rkey` MUST be present.

The call is then routed to all endpoints that were registered ..

The call is then processed as for "All" Calls.


#### Feature Announcement

Support for this feature MUST be announced by *Callers* (`role := "caller"`), *Callees* (`role := "callee"`) and *Dealers* (`role := "dealer"`) via

    HELLO.Details.roles.<role>.features.sharded_registration|bool := true
