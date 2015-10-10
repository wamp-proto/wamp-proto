### Subscriber Black- and Whitelisting

#### Introduction

**Subscriber Black- and Whitelisting** is an advanced *Broker* feature where a *Publisher* is able to restrict the set of receivers of a published event.

Under normal Publish & Subscriber event dispatching, a *Broker* will dispatch a published event to all (authorized) *Subscribers* other than the *Publisher* itself. This set of receivers can be further reduced on a per-publication basis by the *Publisher* using **Subscriber Black- and Whitelisting**.

The *Publisher* can explicitly **exclude** *Subscribers* based on WAMP `sessionid`, `authid` or `authrole`. This is referred to as **Blacklisting**.

A *Publisher* may also explicitly define a **eligible** list of *Subscribers** based on WAMP `sessionid`, `authid` or `authrole`. This is referred to as **Whitelisting**.

#### Use Cases

##### Avoiding Callers from being self-notified

Consider an application that exposes a procedure to update a product price. The procedure might not only actually update the product price (e.g. in a backend database), but additionally publish an event with the updated product price, so that **all** application components get notified actively of the new price.

However, the application might want to exclude the originator of the product price update (the **Caller** of the price update procedure) from receiving the update event - as the originator naturally already knows the new price, and might get confused when it receives an update the **Caller** has triggered himself.

The product price update procedure can use `PUBLISH.Options.exclude|list[int]` to exclude the **Caller** of the procedure.

> Note that the product price update procedure needs to know the session ID of the **Caller** to be able to exclude him. For this, please see **Caller Identification**.

A similar approach can be used for other CRUD-like procedures.

##### Restricting receivers of sensitive information

Consider an application with users that have different `authroles`, such as "manager" and "staff" that publishes events with updates to "customers". The topics being published to could be structured like

{align="left"}
        com.example.myapp.customer.<customer ID>

The application might want to restrict the receivers of customer updates depending on the `authrole` of the user. E.g. a user authenticated under `authrole` "manager" might be allowed to receive any kind of customer update, including personal and business sensitive information. A user under `authrole` "staff" might only be allowed to receive a subset of events.

The application can publish **all** customer updates to the **same** topic `com.example.myapp.customer.<customer ID>` and use `PUBLISH.Options.eligible_authrole|list[string]` to safely restrict the set of actual receivers as desired.

#### Feature Definition

A *Publisher* may restrict the actual receivers of an event from the set of *Subscribers* through the use of

* Blacklisting Options
   * `PUBLISH.Options.exclude|list[int]`
   * `PUBLISH.Options.exclude_authid|list[string]`
   * `PUBLISH.Options.exclude_authrole|list[string]`
* Whitelisting Options
   * `PUBLISH.Options.eligible|list[int]`
   * `PUBLISH.Options.eligible_authid|list[string]`
   * `PUBLISH.Options.eligible_authrole|list[string]`

`PUBLISH.Options.exclude` is a list of integers with WAMP `sessionids` providing an explicit list of (potential) *Subscribers* that won't receive a published event, even though they may be subscribed. In other words, `PUBLISH.Options.exclude` is a **blacklist** of (potential) *Subscribers*.

`PUBLISH.Options.eligible` is a list of integeres with WAMP WAMP `sessionids` providing an explicit list of (potential) *Subscribers* that are allowed to receive a published event. In other words, `PUBLISH.Options.eligible` is a **whitelist** of (potential) *Subscribers*.

The `exclude_authid`, `exclude_authrole`, `eligible_authid` and `eligible_authrole` options work similar, but not on the basis of WAMP `sessionid`, but `authid` and `authrole`.

An (authorized) *Subscriber* to topic T will receive an event published to T if and only if all of the following statements hold true:

1. if there is an `eligible` attribute present, the *Subscriber*'s `sessionid` is in this list
2. if there is an `eligible_authid` attribute present, the *Subscriber*'s `authid` is in this list
3. if there is an `eligible_authrole` attribute present, the *Subscriber*'s `authrole` is in this list
4. if there is an `exclude attribute` present, the *Subscriber*'s `sessionid` is NOT in this list
5. if there is an `exclude_authid` attribute present, the *Subscriber*'s `authid` is NOT in this list
6. if there is an `exclude_authrole` attribute present, the *Subscriber*'s `authrole` is NOT in this list

For example, if both `PUBLISH.Options.exclude` and `PUBLISH.Options.eligible` are present, the *Broker* will dispatch events published only to *Subscribers* that are not explicitly excluded in `PUBLISH.Options.exclude` **and** which are explicitly eligible via `PUBLISH.Options.eligible`.

*Example*

{align="left"}
```json
    [
       16,
       239714735,
       {
          "exclude": [
             7891255,
             1245751
          ]
       },
       "com.myapp.mytopic1",
       [
          "Hello, world!"
       ]
    ]
```

The above event will get dispatched to all *Subscribers* of `com.myapp.mytopic1`, but not WAMP sessions with IDs `7891255` or `1245751` (and also not the publishing session).

*Example*

{align="left"}
```json
    [
       16,
       239714735,
       {
          "eligible": [
             7891255,
             1245751
          ]
       },
       "com.myapp.mytopic1",
       [
          "Hello, world!"
       ]
    ]
```

The above event will get dispatched to WAMP sessions with IDs `7891255` or `1245751` only - but only if those are actually subscribed to the topic `com.myapp.mytopic1`.

*Example*

{align="left"}
```json
    [
       16,
       239714735,
       {
          "eligible": [
             7891255,
             1245751,
             9912315
          ],
          "exclude": [
             7891255
          ]
       },
       "com.myapp.mytopic1",
       [
          "Hello, world!"
       ]
    ]
```

The above event will get dispatched to WAMP sessions with IDs `1245751` or `9912315` only, since `7891255` is excluded - but only if those are actually subscribed to the topic `com.myapp.mytopic1`.

#### Feature Announcement

Support for this feature MUST be announced by *Publishers* (`role := "publisher"`) and *Brokers* (`role := "broker"`) via

{align="left"}
        HELLO.Details.roles.<role>.features.
            subscriber_blackwhite_listing|bool := true
