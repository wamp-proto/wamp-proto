## Cryptosign-based Authentication {#cryptosignauth}

*WAMP-Cryptosign* is a WAMP authentication method based on
*public-private key cryptography*. Specifically, it is based on [Ed25519](https://ed25519.cr.yp.to/) digital signatures as described in [@!RFC8032].

**Ed25519** is an [elliptic curve signature scheme](https://ed25519.cr.yp.to/ed25519-20110926.pdf) that instantiates the Edwards-curve Digital Signature Algorithm (EdDSA) with elliptic curve parameters which are equivalent to [Curve25519](https://cr.yp.to/ecdh.html).
**Curve25519** is a [SafeCurve](https://safecurves.cr.yp.to/), which means it is easy to implement securely and avoid security issues resulting from common implementation challenges and bugs.
Ed25519 is intended to operate at around the 128-bit security level, and there are robust native implementations available as open-source, e.g. [libsodium](https://github.com/jedisct1/libsodium), which can be used from script languages, e.g. [PyNaCl](https://github.com/pyca/pynacl).

An implementation of *WAMP-Cryptosign* MUST provide

* [Client Authentication](#clientauth)

and MAY implement one or more of

* [TLS Channel Binding](#channelbinding)
* [Router Authentication](#routerauth)
* [Trustroots and Certificates](#trustrootcerts)

Examples of complete authentication message exchanges can be found in

* [Example Message Exchanges](#examplemessageexchanges)


### Client Authentication {#clientauth}

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


#### Computing the Signature

The challenge sent by the router is a 32 bytes random value, encoded as a Hex string in `CHALLENGE.extra.challenge|string`.

When no channel binding is active, the Ed25519 signature over the 32 bytes message MUST be computed using the WAMP-Cryptosign *private key* of the authenticating client.

When channel binding is active, the challenge MUST first be XOR'ed bytewise with the channel ID, e.g. the 32 bytes from TLS with channel binding `"tls-unique"`, and the resulting message (which again has length 32 bytes) MUST be signed using the WAMP-Cryptosign *private key* of the authenticating client.

The client MUST return the concatenation of the signature and the message signed (96 bytes) in the `AUTHENTICATE` message.


#### Example Message Flow

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

#### Test Vectors

The following test vectors allow to verify an implementation of WAMP-Cryptosign signatures. You can use `channel_id`, `private_key` and `challenge` as input, and check the computed signature matches `signature`.

The test vectors contain instances for both with and without a `channel_id`, which represents the TLS channel ID when using TLS with `tls-unique` channel binding.

{align="left"}
```
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

### TLS Channel Binding {#channelbinding}

Write me.

* https://tools.ietf.org/html/rfc5056
* https://tools.ietf.org/html/rfc5929
* https://www.ietf.org/proceedings/90/slides/slides-90-uta-0.pdf


### Router Authentication {#routerauth}

Write me.


### Trustroots and Certificates {#trustrootcerts}

Write me.


#### Certificate Chains

A public-key certificate is a signed statement that is used to establish an association between an identity and a public key. This is called a machine identity. The entity that vouches for this association and signs the certificate is the issuer of the certificate and the identity whose public key is being vouched for is the subject of the certificate. In order to associate the identity and the public key, a chain of certificates is used. The certificate chain is also called the certification path or chain of trust.

*What is a Certificate Chain?*

A certificate chain is a list of certificates (usually starting with an end-entity certificate) followed by one or more CA certificates (usually the last one being a self-signed certificate), with the following properties:

* The **issuer** of each certificate (except the last one) matches the **subject of** the next certificate in the list.
* Each certificate (except the last one) is supposed to be signed by the secret key corresponding to the next certificate in the chain (i.e. the signature of one certificate can be verified using the public key contained in the following certificate).
* The last certificate in the list is a **trust anchor**: a certificate that you trust because it was delivered to you by some trustworthy procedure. A trust anchor is a CA certificate (or more precisely, the public verification key of a CA) used by a relying party as the starting point for path validation.

*What are On-chain Trust Anchors?*

In x509, the set of trusted root CA certificates are stored in a machine/device local certificate store. This set of trusted root CA certificates are:

1. filled and fixed by the software or device vendor with a default root CA certificates set
2. may be extendable or replaceable by a user provided custom root CA certificates set

With 1., the user implicitly trusts the vendor, and all root CAs in the set installed by the vendor.
With 2., the user must manage a public-private key infrastructure, and when information is to be
shared with other parties, the use PKI must be made available to those parties, and the parties
will operationally and administratively depend on the PKI hosting party.
In summary, x509 follows a centralized and hierarchical trust model.

With WAMP-Cryptosign, we use a public blockchain for certificate chain trust anchors. Using a public blockchain, specifically Ethereum, provides a decentralized, shared and cryptographically secure
storage for root CA certificates, that is trust anchors. These anchors can be associated with
other entities stored on-chain, such as *federated Realms*.

The following diagram shows the structure of certificate chains in WAMP-Cryptosign:

```
           EIP712AuthorityCertificate
        +------------------------------+
        |   chainId                    |       Root Certificate
        |   verifyingContract          |
        |   validFrom                  |         * trust anchor, stored on-chain
   +----+-- issuer (== realm owner)    |         * tied to a realm
   +----+-> subject (== issuer) -------+----+    * self-signed by realm owner
        |   realm                      |    |
        |   capabilities               |    |
        |   meta                       |    |
        +------------------------------+    |   +------------------------------+
        |   issuerSignature            +----+---> Public Blockchain (L1 or L2) |
        +------------------------------+    |   +------------------------------+
                                            |
                                            |
                                            |
                                            |
                                            |
           EIP712AuthorityCertificate       |
        +------------------------------+    |
        |   chainId                    |    |   Intermediate Certificate
        |   verifyingContract          |    |
        |   validFrom                  |    |    * stored off-chain
        |   issuer  <------------------+----+    * same realm as issueing cert
  +-----+-- subject                    |         * subset of capabilities
  |     |   realm                      |             of issueing cert
  |     |   capabilities               |
  |     |   meta                       |
  |     +------------------------------+
  |     |   issuerSignature            |
  |     +------------------------------+
  |


optional hierarchical chain of intermediate certificates


  |
  |        EIP712AuthorityCertificate
  |     +------------------------------+
  |     |   chainId                    |        Intermediate Certificate
  |     |   verifyingContract          |
  |     |   validFrom                  |         * stored off-chain
  +-----+-> issuer                     |         * same realm as issueing cert
        |   subject--------------------+----+    * subset of capabilities
        |   realm                      |    |        of issueing cert
        |   capabilities               |    |
        |   meta                       |    |
        +------------------------------+    |
        |   issuerSignature            |    |
        +------------------------------+    |
                                            |
                                            |
                                            |
                                            |
                                            |
           EIP712DelegateCertificate        |
        +------------------------------+    |
        |   chainId                    |    |   End-point Certificate
        |   verifyingContract          |    |
        |   validFrom                  |    |     * ephemeral, generate per-boot
        |   delegate <-----------------+----+     * subject is WAMP-Cryptosign pubkey
        |   csPubKey                   |          * Boot time (UTC in Posix ns)
        |   bootedAt                   |
        |   meta                       |
        |                              |
        |                              |
        +------------------------------+         +--------------------------+
        |   delegateSignature          +---------> Hardware Security Module |
        +------------------------------+         +--------------------------+
```

#### Certificate Types

The certificate types `EIP712AuthorityCertificate` and `EIP712DelegateCertificate` follow [EIP712](https://eips.ethereum.org/EIPS/eip-712) and use Ethereum signatures.

`EIP712AuthorityCertificate`:

```json
[
    {
        "name": "chainId",
        "type": "uint256"
    },
    {
        "name": "verifyingContract",
        "type": "address"
    },
    {
        "name": "validFrom",
        "type": "uint256"
    },
    {
        "name": "issuer",
        "type": "address"
    },
    {
        "name": "subject",
        "type": "address"
    },
    {
        "name": "realm",
        "type": "address"
    },
    {
        "name": "capabilities",
        "type": "uint64"
    },
    {
        "name": "meta",
        "type": "string"
    }
]
```

`EIP712DelegateCertificate`:

```json
[
    {
        "name": "chainId",
        "type": "uint256"
    },
    {
        "name": "verifyingContract",
        "type": "address"
    },
    {
        "name": "validFrom",
        "type": "uint256"
    },
    {
        "name": "delegate",
        "type": "address"
    },
    {
        "name": "csPubKey",
        "type": "bytes32"
    },
    {
        "name": "bootedAt",
        "type": "uint64"
    },
    {
        "name": "meta",
        "type": "string"
    }
]
```

#### Capabilities

* **Bit 0**: `CAPABILITY_ROOT_CA`
* **Bit 1**: `CAPABILITY_INTERMEDIATE_CA`
* **Bit 2**: `CAPABILITY_PUBLIC_RELAY`
* **Bit 3**: `CAPABILITY_PRIVATE_RELAY`
* **Bit 4**: `CAPABILITY_GATEWAY`
* **Bit 5**: `CAPABILITY_EXCHANGE`
* **Bit 6**: `CAPABILITY_PROVIDER`
* **Bit 7**: `CAPABILITY_CONSUMER`
* **Bits 8 - 63**: future use, all set to `0`


#### Certificate Chain Verification

To verify a certificate chain and respective certificate signatures

```
[
    (EIP712DelegateCertificate, Signature),       // delegate certificate
    (EIP712AuthorityCertificate, Signature),      // intermediate CA certificate
    ...
    (EIP712AuthorityCertificate, Signature),      // intermediate CA certificate
    (EIP712AuthorityCertificate, Signature)       // root CA certificate
]
```

the following Certificate Chain Rules (CCR) must be checked:

1. **CCR-1**: The `chainId` and `verifyingContract` must match for all certificates to what we expect, and `validFrom` before current block number on the respective chain.
2. **CCR-2**: The `realm` must match for all certificates to the respective realm.
3. **CCR-3**: The type of the first certificate in the chain must be a `EIP712DelegateCertificate`, and all subsequent certificates must be of type `EIP712AuthorityCertificate`.
4. **CCR-4**: The last certificate must be self-signed (`issuer` equals `subject`), it is a root CA certificate.
5. **CCR-5**: The intermediate certificate's `issuer` must be equal to the `subject` of the previous certificate.
6. **CCR-6**: The root certificate must be `validFrom` before the intermediate certificate
7. **CCR-7**: The `capabilities` of intermediate certificate must be a subset of the root cert
8. **CCR-8**: The intermediate certificate's `subject` must be the delegate certificate `delegate`
9. **CCR-9**: The intermediate certificate must be `validFrom` before the delegate certificate
10. **CCR-10**: The root certificate's signature must be valid and signed by the root certificate's `issuer`.
11. **CCR-11**: The intermediate certificate's signature must be valid and signed by the intermediate certificate's `issuer`.
12. **CCR-12**: The delegate certificate's signature must be valid and signed by the `delegate`.


### Example Message Exchanges {#examplemessageexchanges}

#### Example 1

* *with* router challenge
* *without* TLS channel binding

```
WAMP-Transmit(-, -) >>
  HELLO::
    [1,
     'devices',
     {'authextra': {'challenge': 'bbae60ea44cdd7b20dc7010a618b0f0803fab25a817520b4b7f057299b524deb',
                    'channel_binding': None,
                    'pubkey': '545efb0a2192db8d43f118e9bf9aee081466e1ef36c708b96ee6f62dddad9122'},
      'authmethods': ['cryptosign'],
      'roles': {'callee': {'features': {'call_canceling': True,
                                        'caller_identification': True,
                                        'pattern_based_registration': True,
                                        'payload_encryption_cryptobox': True,
                                        'payload_transparency': True,
                                        'progressive_call_results': True,
                                        'registration_revocation': True,
                                        'shared_registration': True}},
                'caller': {'features': {'call_canceling': True,
                                        'caller_identification': True,
                                        'payload_encryption_cryptobox': True,
                                        'payload_transparency': True,
                                        'progressive_call_results': True}},
                'publisher': {'features': {'payload_encryption_cryptobox': True,
                                           'payload_transparency': True,
                                           'publisher_exclusion': True,
                                           'publisher_identification': True,
                                           'subscriber_blackwhite_listing': True,
                                           'x_acknowledged_event_delivery': True}},
                'subscriber': {'features': {'pattern_based_subscription': True,
                                            'payload_encryption_cryptobox': True,
                                            'payload_transparency': True,
                                            'publisher_identification': True,
                                            'subscription_revocation': True}}}}]
>>

WAMP-Receive(-, -) <<
  CHALLENGE::
    [4,
     'cryptosign',
     {'challenge': '0e9192bc08512c8198da159c1ae600ba91729215f35d56102ee318558e773537',
      'channel_binding': None,
      'pubkey': '4a3838f6fe75251e613329d53fc69b262d5eac97fb1d73bebbaed4015b53c862',
      'signature': 'fd5128d2d207ba58a9d1d6f41b72c747964ad9d1294077b3b1eee6130b05843ab12c53c7f2519f73d4feb82db19d8ca0fc26b62bde6518e79a882f5795bc9f00bbae60ea44cdd7b20dc7010a618b0f0803fab25a817520b4b7f057299b524deb'}]
<<

WAMP-Transmit(-, -) >>
  AUTHENTICATE::
    [5,
     'a3a178fe792ed772a8fc092f8341e455de96670c8901264a7c312dbf940d5743626fe9fbc29b23dcd2169b308eca309de85a89ccd296b24835de3d95b16b77030e9192bc08512c8198da159c1ae600ba91729215f35d56102ee318558e773537',
     {}]
>>

WAMP-Receive(-, -) <<
  WELCOME::
    [2,
     3735119691078036,
     {'authextra': {'x_cb_node': 'intel-nuci7-49879',
                    'x_cb_peer': 'tcp4:127.0.0.1:53976',
                    'x_cb_pid': 49987,
                    'x_cb_worker': 'worker001'},
      'authid': 'client01@example.com',
      'authmethod': 'cryptosign',
      'authprovider': 'static',
      'authrole': 'device',
      'realm': 'devices',
      'roles': {'broker': {'features': {'event_retention': True,
                                        'pattern_based_subscription': True,
                                        'payload_encryption_cryptobox': True,
                                        'payload_transparency': True,
                                        'publisher_exclusion': True,
                                        'publisher_identification': True,
                                        'session_meta_api': True,
                                        'subscriber_blackwhite_listing': True,
                                        'subscription_meta_api': True,
                                        'subscription_revocation': True}},
                'dealer': {'features': {'call_canceling': True,
                                        'caller_identification': True,
                                        'pattern_based_registration': True,
                                        'payload_encryption_cryptobox': True,
                                        'payload_transparency': True,
                                        'progressive_call_results': True,
                                        'registration_meta_api': True,
                                        'registration_revocation': True,
                                        'session_meta_api': True,
                                        'shared_registration': True,
                                        'testament_meta_api': True}}},
      'x_cb_node': 'intel-nuci7-49879',
      'x_cb_peer': 'tcp4:127.0.0.1:53976',
      'x_cb_pid': 49987,
      'x_cb_worker': 'worker001'}]
<<

WAMP-Transmit(3735119691078036, client01@example.com) >>
  GOODBYE::
    [6, {}, 'wamp.close.normal']
>>

WAMP-Receive(3735119691078036, client01@example.com) <<
  GOODBYE::
    [6, {}, 'wamp.close.normal']
<<
```

#### Example 2

* *with* router challenge
* *with* TLS channel binding

```
WAMP-Transmit(-, -) >>
  HELLO::
    [1,
     'devices',
     {'authextra': {'challenge': '4f861f12796c2972b7b0026522a687aa851d90355122a61d4f1fdce4d06b564f',
                    'channel_binding': 'tls-unique',
                    'pubkey': '545efb0a2192db8d43f118e9bf9aee081466e1ef36c708b96ee6f62dddad9122'},
      'authmethods': ['cryptosign'],
      'roles': {'callee': {'features': {'call_canceling': True,
                                        'caller_identification': True,
                                        'pattern_based_registration': True,
                                        'payload_encryption_cryptobox': True,
                                        'payload_transparency': True,
                                        'progressive_call_results': True,
                                        'registration_revocation': True,
                                        'shared_registration': True}},
                'caller': {'features': {'call_canceling': True,
                                        'caller_identification': True,
                                        'payload_encryption_cryptobox': True,
                                        'payload_transparency': True,
                                        'progressive_call_results': True}},
                'publisher': {'features': {'payload_encryption_cryptobox': True,
                                           'payload_transparency': True,
                                           'publisher_exclusion': True,
                                           'publisher_identification': True,
                                           'subscriber_blackwhite_listing': True,
                                           'x_acknowledged_event_delivery': True}},
                'subscriber': {'features': {'pattern_based_subscription': True,
                                            'payload_encryption_cryptobox': True,
                                            'payload_transparency': True,
                                            'publisher_identification': True,
                                            'subscription_revocation': True}}}}]
>>

WAMP-Receive(-, -) <<
  CHALLENGE::
    [4,
     'cryptosign',
     {'challenge': '358625312c6c3bf64ed51d17d210ce21af1639c774cabf5735a9651d7d91fc6a',
      'channel_binding': 'tls-unique',
      'pubkey': '4a3838f6fe75251e613329d53fc69b262d5eac97fb1d73bebbaed4015b53c862',
      'signature': 'aa05f4cd7747d36b79443f1d4703a681e107edc085d876b508714e2a3a8135bacaae1c018452c4acb3ad2818aa97a6d23e5ac7e3734c7b1f40e6232a70938205a6f5a1f034a28090b195fb2ce2454a82532f5c8baf6ba1dfb5ddae63c09ce72f'}]
<<

WAMP-Transmit(-, -) >>
  AUTHENTICATE::
    [5,
     '25114474580d6e99a6126b091b4565c23db567d686c5b8c3a94e3f2f09dc80300c5b40a124236733fa56396df721eb12ac092362379bd5b27b4db9e2beaa1408dcf59bd361a2921448f0e45e12f303097924f5798a83b895cf6b179a6d664d0a',
     {}]
>>

WAMP-Receive(-, -) <<
  WELCOME::
    [2,
     7325966140445461,
     {'authextra': {'x_cb_node': 'intel-nuci7-49879',
                    'x_cb_peer': 'tcp4:127.0.0.1:54046',
                    'x_cb_pid': 49987,
                    'x_cb_worker': 'worker001'},
      'authid': 'client01@example.com',
      'authmethod': 'cryptosign',
      'authprovider': 'static',
      'authrole': 'device',
      'realm': 'devices',
      'roles': {'broker': {'features': {'event_retention': True,
                                        'pattern_based_subscription': True,
                                        'payload_encryption_cryptobox': True,
                                        'payload_transparency': True,
                                        'publisher_exclusion': True,
                                        'publisher_identification': True,
                                        'session_meta_api': True,
                                        'subscriber_blackwhite_listing': True,
                                        'subscription_meta_api': True,
                                        'subscription_revocation': True}},
                'dealer': {'features': {'call_canceling': True,
                                        'caller_identification': True,
                                        'pattern_based_registration': True,
                                        'payload_encryption_cryptobox': True,
                                        'payload_transparency': True,
                                        'progressive_call_results': True,
                                        'registration_meta_api': True,
                                        'registration_revocation': True,
                                        'session_meta_api': True,
                                        'shared_registration': True,
                                        'testament_meta_api': True}}},
      'x_cb_node': 'intel-nuci7-49879',
      'x_cb_peer': 'tcp4:127.0.0.1:54046',
      'x_cb_pid': 49987,
      'x_cb_worker': 'worker001'}]
<<
2022-07-13T17:38:29+0200 session joined: {'authextra': {'x_cb_node': 'intel-nuci7-49879',
               'x_cb_peer': 'tcp4:127.0.0.1:54046',
               'x_cb_pid': 49987,
               'x_cb_worker': 'worker001'},
 'authid': 'client01@example.com',
 'authmethod': 'cryptosign',
 'authprovider': 'static',
 'authrole': 'device',
 'realm': 'devices',
 'resumable': False,
 'resume_token': None,
 'resumed': False,
 'serializer': 'cbor.batched',
 'session': 7325966140445461,
 'transport': {'channel_framing': 'websocket',
               'channel_id': {'tls-unique': b'\xe9s\xbe\xe2M\xce\xa9\xe2'
                                            b'\x06%\xf9I\xc0\xe3\xcd('
                                            b'\xd62\xcc\xbe\xfeI\x07\xc2'
                                            b'\xfa\xc2r\x87\x10\xf7\xb1`'},
               'channel_serializer': None,
               'channel_type': 'tls',
               'http_cbtid': None,
               'http_headers_received': None,
               'http_headers_sent': None,
               'is_secure': True,
               'is_server': False,
               'own': None,
               'own_fd': -1,
               'own_pid': 50690,
               'own_tid': 50690,
               'peer': 'tcp4:127.0.0.1:8080',
               'peer_cert': None,
               'websocket_extensions_in_use': None,
               'websocket_protocol': None}}

WAMP-Transmit(7325966140445461, client01@example.com) >>
  GOODBYE::
    [6, {}, 'wamp.close.normal']
>>

WAMP-Receive(7325966140445461, client01@example.com) <<
  GOODBYE::
    [6, {}, 'wamp.close.normal']
<<
```

#### Example 3

* *with* router challenge
* *with* TLS channel binding
* *with* client trustroot and certificates
