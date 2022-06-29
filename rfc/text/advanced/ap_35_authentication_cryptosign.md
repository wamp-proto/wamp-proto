## Cryptosign-based Authentication {#cryptosignauth}

*WAMP-Cryptosign* is a WAMP authentication method based on
*public-private key cryptography*. Specifically, it is based on [Ed25519](https://ed25519.cr.yp.to/) digital signatures as described in [@!RFC8032].

**Ed25519** is an [elliptic curve signature scheme](https://ed25519.cr.yp.to/ed25519-20110926.pdf) that instantiates
the Edwards-curve Digital Signature Algorithm (EdDSA) with
elliptic curve parameters which are equivalent to [Curve25519](https://cr.yp.to/ecdh.html).

**Curve25519** is a [SafeCurve](https://safecurves.cr.yp.to/), which means
it is easy to implement securely and avoid security issues resulting from common implementation challenges and bugs.

Ed25519 is intended to operate at around the 128-bit security level, and there are robust native implementations available as open-source, e.g. [libsodium](https://github.com/jedisct1/libsodium), which can be used from script languages, e.g. [PyNaCl](https://github.com/pyca/pynacl).


### Example Message Flow

A typical authentication begins with the client sending a `HELLO` message specifying the `cryptosign` method as (one of) the authentication methods:

{align="left"}
```javascript
[1, "realm1", {
    "roles": {/* see below */},
    "authmethods": ["cryptosign"],
    "authid": "client01@example.com",
    "authextra": {
        "pubkey": "545efb0a2192db8d43f118e9bf9aee081466e1ef36c708b96ee6f62dddad9122",
        "channel_binding": null
    }
}]
```

The `HELLO.Details.authmethods|list` is used by the client to announce the authentication methods it is prepared to perform. For WAMP-Cryptosign, this MUST include `"cryptosign"`.

The `HELLO.Details.authid|string` is the authentication ID (e.g. username) the client wishes to authenticate as. For WAMP-Cryptosign authentication, this MAY be provided. If no `authid` is provided, the router SHOULD automatically chose and assign an `authid` (e.g. the Hex encode public key).

The client needs to announce the WAMP `roles` and features it supports, for example:

{align="left"}
```javascript
{"callee": {"features": {"call_canceling": True,
                         "caller_identification": True,
                         "pattern_based_registration": True,
                         "payload_encryption_cryptobox": True,
                         "payload_transparency": True,
                         "progressive_call_results": True,
                         "registration_revocation": True,
                         "shared_registration": True}},
"caller": {"features": {"call_canceling": True,
                        "caller_identification": True,
                        "payload_encryption_cryptobox": True,
                        "payload_transparency": True,
                        "progressive_call_results": True}},
"publisher": {"features": {"payload_encryption_cryptobox": True,
                           "payload_transparency": True,
                           "publisher_exclusion": True,
                           "publisher_identification": True,
                           "subscriber_blackwhite_listing": True,
                           "x_acknowledged_event_delivery": True}},
"subscriber": {"features": {"pattern_based_subscription": True,
                            "payload_encryption_cryptobox": True,
                            "payload_transparency": True,
                            "publisher_identification": True,
                            "subscription_revocation": True}}}}
```

If the router is unwilling or unable to perform WAMP-Cryptosign authentication, it'll either skip forward trying other authentication methods (if the client announced any) or send an `ABORT` message.

If the router is willing to let the client authenticate using WAMP-Cryptosign and the router recognizes the provided `HELLO.Details.authextra.pubkey|string`, it'll send a `CHALLENGE` message:

{align="left"}
```javascript
[4, "cryptosign", {
    "challenge": "fa034062ad76352b53a25358854577730db82f367aa439709c91296d04a5716c",
    "channel_binding": null
}]
```

The client will send an `AUTHENTICATE` message containing a signature:

{align="left"}
```javascript
[5 'e2f0297a193b63b7a4a92028e9e2e6107f82730560d54a657bd982cb4b3151490399debbbde998e494d3c3b2a5e2e91271291e10dee85a6cfaa127885ddd8b0afa034062ad76352b53a25358854577730db82f367aa439709c91296d04a5716c', {}]
```

If the authentication succeeds, the server will router respond with a `WELCOME` message:

{align="left"}
```javascript
[2, 7562122397119786, {
    "authextra": {
        "x_cb_node": "intel-nuci7-27532",
        "x_cb_peer": "tcp4:127.0.0.1:49032",
        "x_cb_pid": 27637,
        "x_cb_worker": "worker001"
    },
    "authid": "client01@example.com",
    "authmethod": "cryptosign",
    "authprovider": "static",
    "authrole": "user",
    "realm": "realm1",
    "roles": {/* see below */}
}]
```

where

1. `authid|string`: The authentication ID the client was (actually) authenticated as.
2. `authrole|string`: The authentication role the client was authenticated for.
3. `authmethod|string`: The authentication method, here `"cryptosign"`
4. `authprovider|string`: The actual provider of authentication. For Ticket-based authentication, this can be freely chosen by the app, e.g. `static` or `dynamic`.

The `WELCOME.Details` again contain the actual authentication information active. If the authentication fails, the router will response with an `ABORT` message.

When the authentication is successful, `WELCOME.Details.authextra.roles|dict` will announce the roles and features the router supports:

{align="left"}
```javascript
{"broker": {"features": {"event_retention": True,
                                    "pattern_based_subscription": True,
                                    "payload_encryption_cryptobox": True,
                                    "payload_transparency": True,
                                    "publisher_exclusion": True,
                                    "publisher_identification": True,
                                    "session_meta_api": True,
                                    "subscriber_blackwhite_listing": True,
                                    "subscription_meta_api": True,
                                    "subscription_revocation": True}},
            "dealer": {"features": {"call_canceling": True,
                                    "caller_identification": True,
                                    "pattern_based_registration": True,
                                    "payload_encryption_cryptobox": True,
                                    "payload_transparency": True,
                                    "progressive_call_results": True,
                                    "registration_meta_api": True,
                                    "registration_revocation": True,
                                    "session_meta_api": True,
                                    "shared_registration": True,
                                    "testament_meta_api": True}}
    }
```

### Computing the Signature

Write me.

### TLS Channel Binding

Write me.

### Router Challenge

Write me.

### Trustroots and Certificates

Write me.
