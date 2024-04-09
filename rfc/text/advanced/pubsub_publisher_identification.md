### Publisher Identification {#pubsub-pub-identification}

A *Publisher* may request the disclosure of its identity (its WAMP session ID) to receivers of a published event by setting

{align="left"}
        PUBLISH.Options.disclose_me|bool := true

*Example*

{align="left"}
        [16, 239714735, {"disclose_me": true}, "com.myapp.mytopic1",
            ["Hello, world!"]]

If above event is published by a *Publisher* with WAMP session ID `3335656`, the *Broker* would send an `EVENT` message to *Subscribers* with the *Publisher's* WAMP session ID in `EVENT.Details.publisher`:

*Example*

{align="left"}
        [36, 5512315355, 4429313566, {"publisher": 3335656},
            ["Hello, world!"]]

Note that a *Broker* may deny a *Publisher's* request to disclose its identity:

*Example*

{align="left"}
        [8, 239714735, {}, "wamp.error.option_disallowed.disclose_me"]

A *Broker* may also (automatically) disclose the identity of a *Publisher* even without the *Publisher* having explicitly requested to do so when the *Broker* configuration (for the publication topic) is set up to do so.

**Additional Identity Information**

When publisher disclosure is allowed for a particular PUBLISH message, the
corresponding `EVENT` message MAY also contain the following additional
properties in its `Details` dictionary:

- `EVENT.Details.publisher_authid|string`
- `EVENT.Details.publisher_authrole|string`

**Feature Announcement**

Support for this feature MUST be announced by *Publishers* (`role := "publisher"`), *Brokers* (`role := "broker"`) and *Subscribers* (`role := "subscriber"`) via

{align="left"}
        HELLO.Details.roles.<role>.features.
            publisher_identification|bool := true
