## Cryptosign-based Authentication {#cryptosignauth}

*WAMP-Cryptosign* is a WAMP authentication method based on
*public-private key cryptography*. Specifically, it is based on [Ed25519](https://ed25519.cr.yp.to/) digital signatures as described in [@!RFC8032].

**Ed25519** is an [elliptic curve signature scheme](https://ed25519.cr.yp.to/ed25519-20110926.pdf) that instantiates
the Edwards-curve Digital Signature Algorithm (EdDSA) with
elliptic curve parameters which are equivalent to [Curve25519](https://cr.yp.to/ecdh.html).

**Curve25519** is a [SafeCurve](https://safecurves.cr.yp.to/), which means
it is easy to implement securely and avoid security issues resulting from common implementation challenges and bugs.

Ed25519 is intended to operate at around the 128-bit security level, and there are robust native implementations available as open-source, e.g. [libsodium](https://github.com/jedisct1/libsodium), which can be used from script languages, e.g. [PyNaCl](https://github.com/pyca/pynacl).


### Client Authentication

A *Client* is authenticated to a *Router* by:

1. sending a `HELLO`, announcing its public key
2. signing a (random) challenge received in `CHALLENGE` with its private key
3. let the router verify the signature, proofing the client actually controls the private key, and thus the authenticity of the client as identified by the public key
4. let the router admit the client to a realm under a role, based on the public key

Thus, the client is identified using its public key, and the *Router* needs to know said public key and its desired realm and role in advance.

A *Client* for which the *Router* does not previously know the client's public key MAY use the [Trustroots and Certificates](#name-trustroots-and-certificates) feature to trust a *Client* based on an additional certificate presented by the client.

A *Router* is optionally (see [Router Authentication](#name-router-authentication)) authenticated to a *Client* by:

1. client includes a (random) `HELLO.Details.challenge|string`
2. the router sends the signature as part of its challenge to the client, in `CHALLENGE.extra.signature|string`

Again, in this case, the *Router* includes a trustroot and certificate for the client to verify.


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

The `HELLO.Details.authextra|dict` contains the following members for WAMP-Cryptosign:

| Field             | Type     | Required | Description                                                                          |
|-------------------|----------|----------|--------------------------------------------------------------------------------------|
| pubkey            | string   | yes      | The client public key (32 bytes) as a Hex encoded string, e.g. `545efb0a2192db8d43f118e9bf9aee081466e1ef36c708b96ee6f62dddad9122` |
| channel_binding   | string   | no       | If TLS channel binding is in use, the TLS channel binding type, e.g. `"tls-unique"`. |
| challenge         | string   | no       | A client chosen, random challenge (32 bytes) as a Hex encoded string, to be signed by the router. |
| trustroot         | string   | no       | When the client includes a client certificate (see below), the Ethereum address of the trustroot of the certificate, e.g. `0x72b3486d38E9f49215b487CeAaDF27D6acf22115` |

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

### TLS Channel Binding

Write me.

https://tools.ietf.org/html/rfc5056
https://tools.ietf.org/html/rfc5929
https://www.ietf.org/proceedings/90/slides/slides-90-uta-0.pdf


self._challenge = os.urandom(32)



### Computing the Signature

The challenge sent by the router is a 32 bytes random value, encoded as a Hex string in `CHALLENGE.extra.challenge|string`.

When no channel binding is active, the signature over the 32 bytes message MUST be computed using the WAMP-Cryptosign *private key* of the authenticating client.

When channel binding is active, the challenge MUST first be XOR'ed bytewise with the channel ID, e.g. the 32 bytes from TLS with channel binding `"tls-unique"`, and the resulting message (which again has length 32 bytes) MUST be signed using the WAMP-Cryptosign *private key* of the authenticating client.

To compute the signature


        if channel_id_type == 'tls-unique':
            assert len(
                channel_id_raw) == 32, 'unexpected TLS transport channel ID length (was {}, but expected 32)'.format(
                len(channel_id_raw))

            # with TLS channel binding of type "tls-unique", the message to be signed by the client actually
            # is the XOR of the challenge and the TLS channel ID
            data = util.xor(challenge_raw, channel_id_raw)


we return the concatenation of the signature and the message signed (96 bytes)


https://pynacl.readthedocs.io/en/latest/signing/#algorithm


### Test Vectors

The following test vectors allow to verify an implementation of WAMP-Cryptosign signatures. You can use `channel_id`, `private_key` and `challenge` as input, and check the computed signature matches `signature`.

The test vectors contain instances for both with and without a `channel_id`, which represents the TLS channel ID when using TLS with `tls-unique` channel binding.

{align="left"}
```python
test_vectors_1 = [
    {
        'channel_id': None,
        'private_key': '4d57d97a68f555696620a6d849c0ce582568518d729eb753dc7c732de2804510',
        'challenge': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff',
        'signature': 'b32675b221f08593213737bef8240e7c15228b07028e19595294678c90d11c0cae80a357331bfc5cc9fb71081464e6e75013517c2cf067ad566a6b7b728e5d03ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff'
    },
    {
        'channel_id': None,
        'private_key': 'd511fe78e23934b3dadb52fcd022974b80bd92bccc7c5cf404e46cc0a8a2f5cd',
        'challenge': 'b26c1f87c13fc1da14997f1b5a71995dff8fbe0a62fae8473c7bdbd05bfb607d',
        'signature': 'd4209ad10d5aff6bfbc009d7e924795de138a63515efc7afc6b01b7fe5201372190374886a70207b042294af5bd64ce725cd8dceb344e6d11c09d1aaaf4d660fb26c1f87c13fc1da14997f1b5a71995dff8fbe0a62fae8473c7bdbd05bfb607d'
    },
    {
        'channel_id': None,
        'private_key': '6e1fde9cf9e2359a87420b65a87dc0c66136e66945196ba2475990d8a0c3a25b',
        'challenge': 'b05e6b8ad4d69abf74aa3be3c0ee40ae07d66e1895b9ab09285a2f1192d562d2',
        'signature': '7beb282184baadd08f166f16dd683b39cab53816ed81e6955def951cb2ddad1ec184e206746fd82bda075af03711d3d5658fc84a76196b0fa8d1ebc92ef9f30bb05e6b8ad4d69abf74aa3be3c0ee40ae07d66e1895b9ab09285a2f1192d562d2'
    },
    {
        'channel_id': '62e935ae755f3d48f80d4d59f6121358c435722a67e859cc0caa8b539027f2ff',
        'private_key': '4d57d97a68f555696620a6d849c0ce582568518d729eb753dc7c732de2804510',
        'challenge': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff',
        'signature': '9b6f41540c9b95b4b7b281c3042fa9c54cef43c842d62ea3fd6030fcb66e70b3e80d49d44c29d1635da9348d02ec93f3ed1ef227dfb59a07b580095c2b82f80f9d16ca518aa0c2b707f2b2a609edeca73bca8dd59817a633f35574ac6fd80d00'
    },
    {
        'channel_id': '62e935ae755f3d48f80d4d59f6121358c435722a67e859cc0caa8b539027f2ff',
        'private_key': 'd511fe78e23934b3dadb52fcd022974b80bd92bccc7c5cf404e46cc0a8a2f5cd',
        'challenge': 'b26c1f87c13fc1da14997f1b5a71995dff8fbe0a62fae8473c7bdbd05bfb607d',
        'signature': '305aaa3ac25e98f651427688b3fc43fe7d8a68a7ec1d7d61c61517c519bd4a427c3015599d83ca28b4c652333920223844ef0725eb5dc2febfd6af7677b73f01d0852a29b460fc92ec943242ac638a053bbacc200512b18b30d15083cbdc9282'
    },
    {
        'channel_id': '62e935ae755f3d48f80d4d59f6121358c435722a67e859cc0caa8b539027f2ff',
        'private_key': '6e1fde9cf9e2359a87420b65a87dc0c66136e66945196ba2475990d8a0c3a25b',
        'challenge': 'b05e6b8ad4d69abf74aa3be3c0ee40ae07d66e1895b9ab09285a2f1192d562d2',
        'signature': 'ee3c7644fd8070532bc1fde3d70d742267da545d8c8f03e63bda63f1ad4214f4d2c4bfdb4eb9526def42deeb7e31602a6ff99eba893e0a4ad4d45892ca75e608d2b75e24a189a7f78ca776ba36fc53f6c3e31c32f251f2c524f0a44202f2902d'
    },
]
```


### Router Authentication

Write me.


### Trustroots and Certificates

Write me.
