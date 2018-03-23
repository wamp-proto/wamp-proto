#### Salted Challenge Response Authentication Mechanism {#wamp-scram}

The WAMP Salted Challenge Response Authentication Mechanism ("WAMP-SCRAM"), is a password-based authentication method where the shared secret is neither transmitted nor stored as cleartext. WAMP-SCRAM is based on [RFC5802](https://tools.ietf.org/html/rfc5802) (_Salted Challenge Response Authentication Mechanism_) and [RFC7677](https://tools.ietf.org/html/rfc7677) (_SCRAM-SHA-256 and SCRAM-SHA-256-PLUS_).

WAMP-SCRAM supports the Argon2 ([draft-irtf-cfrg-argon2](https://datatracker.ietf.org/doc/draft-irtf-cfrg-argon2/)) password-based key derivation function, a memory-hard algorithm intended to resist cracking on GPU hardware. PBKDF2 ([RFC2898](https://tools.ietf.org/html/rfc2898)) is also supported for applications that are required to use primitives currently approved by cryptographic standards.

##### Security Considerations

With WAMP-SCRAM, if the authentication database is stolen, an attacker cannot impersonate a user unless they guess the password offline by brute force.

In the event that the server's authentication database is stolen, and the attacker either eavesdrops on one authentication exchange or impersonates a server, the attacker gains the ability to impersonate that particular user on that server. If the same salt is used on other servers, the attacker would gain the ability to impersonate that user on all servers using the same salt. That's why it's important to use a per-user random salt.

An evesdropper that captures a user anthentication exchange has enough information to mount an offline, brute-force dictionary attack for that particular user. If passwords are sufficiently strong, the cost/time needed to crack a password becomes prohibitive.

Note that when HTML/Javascript assets are served to a web browser, WAMP-SCRAM does not safeguard against a man-in-the-middle tampering with those assets. Those assets could be tampered with in a way that captures the user's password and sends it to the attacker.

In light of the above security concerns, a secure TLS transport is therefore advised to prevent such attacks. The channel binding feature of SCRAM can be used to ensure that the TLS endpoints are the same between client and router.


##### Deviations from RFC5802

1. To simplify parsing, SCRAM attributes in the authentication exchange messages are encoded as members of the `Options`/`Details` objects without escaping the `,` and `=` characters. However, the `AuthMessage` used to compute the client and server signatures DOES use the exact syntax specified in [RFC5802, section 7](https://tools.ietf.org/html/rfc5802#section-7). This makes it possible to use existing test vectors to verify WAMP-SCRAM implementations.

2. Hashing based on the weaker SHA-1 specified in [RFC5802](https://tools.ietf.org/html/rfc5802) is intentionally not supported by WAMP-SCRAM, in favor of the stronger SHA-256 specified in [RFC7677](https://tools.ietf.org/html/rfc7677).

3. The [Argon2](https://datatracker.ietf.org/doc/draft-irtf-cfrg-argon2) key derivation function MAY be used instead of PBKDF2.

4. Nonces are required to be base64-encoded, which is stricter than the `printable` syntax specification of [RFC5802](https://tools.ietf.org/html/rfc5802).

5. The `"y"` channel binding flag is not used as there is currently no standard way for WAMP routers to announce channel binding capabilities.

6. The use of `authzid` for user impersonation is not supported.

##### authmethod Type String

`"wamp-scram"` SHALL be used as the `authmethod` type string for WAMP-SCRAM authentication. Announcement by routers of WAMP-SCRAM support is outside the scope of this document.

##### Conventions

###### Base64 encoding

Base64 encoding of octet strings is restricted to canonical form with no whitespace, as defined in [RFC4648](https://tools.ietf.org/html/rfc4648) (_The Base16, Base32, and Base64 Data Encodings_).

###### Nonces

In WAMP-SCRAM, a _nonce_ (number used once) is a base64-encoded sequence of random octets. It SHOULD be of sufficient length to make a replay attack unfeasible. A length of 16 octets (128 bits) is recommended for each of the client and server-generated nonces.

See [RFC4086](https://tools.ietf.org/html/rfc4086) (_Randomness Requirements for Security_) for best practices concerning randomness.

###### Salts

A _salt_ is a base64-encoded sequence of random octets.

To prevent rainbow table attacks in the event of database theft, the salt MUST be generated randomly by the server **for each user**. The random salt is stored with each user record in the authentication database.

###### Username/Password String Normalization

Username and password strings SHALL be normalized according to the _SASLprep_ profile described in [RFC4013](https://tools.ietf.org/html/rfc4013), using the _stringprep_ algorithm described in [RFC3454](https://tools.ietf.org/html/rfc3454).

While SASLprep preserves the case of usernames, the server MAY choose to perform case insensitve comparisons when searching for a username in the authentication database.


##### Channel Binding

_Channel binding_ is a feature that allows a higher layer to establish that the other end of an underlying secure channel is bound to its higher layer counterpart. See [RFC5056](https://tools.ietf.org/html/rfc5056) (_On the Use of Channel Bindings_) for an in-depth discussion.

[RFC5929](https://tools.ietf.org/html/rfc5929) defines binding types for use with TLS transports, of which `tls-unique` and `tls-server-end-point` are applicable for WAMP-SCRAM. For each channel binding type, there is a corresponding definition of the _channel binding data_ that must be sent in response to the authentication challenge.

Negotiation and announcement of channel binding is outside the scope of this document. [RFC5929 section 6](https://tools.ietf.org/html/rfc5929#section-6) recommends that application protocols use `tls-unique` exclusively, except perhaps where server-side proxies are commonly deployed.

Note that WAMP-SCRAM channel binding is not generally possible with web browser clients due to the lack of a suitable API for this purpose.

###### The tls-unique Channel Binding Type

The `tls-unique` channel binding type allows the WAMP layer to establish that the other peer is authenticating over the same, unique TLS connection. The channel binding data for this type corresponds to the bytes of the first TLS Finished message, as described in [RFC5929, section 3](https://tools.ietf.org/html/rfc5929#section-3). [RFC5929 section 10.2](https://tools.ietf.org/html/rfc5929#section-10.2) addresses the concern of disclosing this data over the TLS channel (in short, the TLS Finished message would already be visible to evesdroppers).

To safeguard against the _triple handshake attack_ described in [RFC7627](https://tools.ietf.org/html/rfc7627), this channel binding type MUST be used over a TLS channel that uses the _extended master secret_ extension, or over a TLS channel where session resumption is not permitted.

###### The tls-server-end-point Channel Binding Type

The `tls-server-end-point` channel binding type allows the WAMP layer to establish that the other peer is authenticating over a TLS connection to a server having been issued a Public Key Infrastructure Certificate. The channel binding data for this type is a hash of the TLS server's certificate, computed as described in [RFC5929, section 4.1](https://tools.ietf.org/html/rfc5929#section-4.1). The certificate is hashed to accomodate memory-constrained implementations.

##### Authentication Exchange

WAMP-SCRAM uses a single round of challenge/response pairs after the client authentication request and before the authentication outcome.

The mapping of RFC5802 messages to WAMP messages is as follows:

SCRAM Message                              | WAMP Message
----------------------                     | ------------
`client-first-message`                     | `HELLO`
`server-first-message`                     | `CHALLENGE`
`client-final-message`                     | `AUTHENTICATE`
`server-final-message` with `verifier`     | `WELCOME`
`server-final-message` with `server-error` | `ABORT`


###### Initial Client Authentication Message

WAMP-SCRAM authentication begins with the client sending a `HELLO` message specifying the `wamp-scram` method as (one of) the authentication methods:

{align="left"}
```javascript
    [1, "realm1",
        {
            "roles": ...,
            "authmethods": ["wamp-scram"],
            "authid": "user",
            "authextra":
                {
                    "nonce": "egVDf3DMJh0=",
                    "channel_binding": null
                }

        }
    ]
```
where:

1. `authid|string`: The identity of the user performing authentication. This corresponds to the `username` parameter in RFC5802.
2. `authextra.nonce|string`: A base64-encoded sequence of random octets, generated by the client. See [Nonces](#nonces).
3. `authextra.channel_binding|string`: Optional string containing the desired channel binding type. See [Channel Bindings](#channel-binding).

Upon receiving the `HELLO` message, the server MUST terminate the authentication process by sending an `ABORT` message under any of the following circumstances:

* The server does not support the WAMP-SCRAM `authmethods`, and there are no other methods left that the server supports for this `authid`.
* The the server does not support the requested `channel_binding` type.
* (Optional) The server does not recognize the given `authid`. In this case, the server MAY proceed with a mock `CHALLENGE` message to avoid leaking information on the existence of usernames. This mock `CHALLENGE` SHOULD contain a generated `salt` value that is always the same for a given `authid`, otherwise an attacker may discover that the user doesn't actually exist.

###### Initial Server Authentication Message

If none of the above failure conditions apply, and the server is ready to let the client authenticate using WAMP-SCRAM, then it SHALL send a `CHALLENGE` message:

{align="left"}
```javascript
    [4, "wamp-scram",
        {
            "nonce": "egVDf3DMJh0=SBmkFIh7sSo=",
            "salt": "aBc+fx0NAVA=",
            "kdf": "pbkdf2",
            "iterations": 4096,
            "memory": null
        }
    ]
```

where:

1. `nonce|string`: A server-generatated nonce that is appended to the client-generated nonce sent in the previous `HELLO` message. See [Nonces](#nonces).
2. `salt|string`: The base64-encoded salt for this user, to be passed to the key derivation function. This value is stored with each user record in the authentication database. See [Salts](#salts).
3. `kdf`: The key derivation function (KDF) used to hash the password. This value is stored with each user record in the authentication database. See [Key Derivation Functions](#key-derivation-functions).
4. `iterations|integer`: The execution time cost factor to use for generating the `SaltedPassword` hash. This value is stored with each user record in the authentication database.
5. `memory|integer`: The memory cost factor to use for generating the `SaltedPassword` hash. This is only used by the Argon2 key derivation function, where it is stored with each user record in the authentication database.

The client MUST respond with an ABORT message if `CHALLENGE.Details.nonce` does not begin with the client nonce sent in `HELLO.Details.nonce`.

The client SHOULD respond with an ABORT message if it detects that the cost parameters are unusually low. Such low-cost parameters could be the result of a rogue server attempting to obtain a weak password hash that can be easily cracked. What constitutes unusually low parameters is implementation-specific and is not covered by this document.


###### Final Client Authentication Message

Upon receiving a valid `CHALLENGE` message, the client SHALL respond with an `AUTHENTICATE` message:

{align="left"}
```javascript
    [5, "dHzbZapWIk4jUhN+Ute9ytag9zjfMHgsqmmiz7AndVQ=",
        {
            "nonce": "egVDf3DMJh0=SBmkFIh7sSo=",
            "channel_binding": null,
            "cbind_data": null
        }
    ]
```
where:

1. `Signature|string` argument: The base64-encoded `ClientProof`, computed as described in the [SCRAM-Algorithms](#scram-algorithms) section.
2. `nonce|string`: The concatenated client-server nonce from the previous `CHALLENGE` message.
3. `channel_binding|string`: Optional string containing the channel binding type that was sent in the original `HELLO` message.
4. `cbind_data|string`: Optional base64-encoded channel binding data. MUST be present if and only if `channel_binding` is not `null`. The format of the binding data is dependent on the binding type. See [Channel Binding](#channel-binding).

Upon receiving the `AUTHENTICATE` message, the server SHALL then check that:

* The `AUTHENTICATE` message was received in due time.
* The `ClientProof` passed via the `Signature|string` argument is validated against the `StoredKey` and `ServerKey` stored in the authentication database. See [SCRAM Algorithms](#scram-algorithms).
* `nonce` matches the one previously sent via `CHALLENGE`.
* The `channel_binding` matches the one sent in the `HELLO` message.
* The `cbind_data` sent by the client matches the channel binding data that the server sees on its side of the channel.


###### Final Server Authentication Message - Success

If the authentication succeeds, the server SHALL finally respond with a `WELCOME` message:

{align="left"}
```javascript
    [2, 3251278072152162,
        {
            "authid": "user",
            "authrole": "frontend",
            "authmethod": "wamp-scram",
            "authprovider": "static",
            "roles": ...,
            "authextra":
                {
                    "verifier":
                      "v=6rriTRBi23WpRR/wtup+mMhUZUn/dB5nLTJRsjl95G4="
                }
        }
    ]
```

where:

1. `authid|string`: The authentication ID the client was actually authenticated as.
2. `authrole|string`: The authentication role the client was authenticated for.
3. `authmethod|string`: The authentication method, here `"wamp-scram"`.
4. `authprovider|string`: The actual provider of authentication. For WAMP-SCRAM authentication, this can be freely chosen by the app, e.g. static or dynamic.
5. `authextra.verifier|string`: The base64-encoded `ServerSignature`, computed as described in the [SCRAM Algorithms](#scram-algorithms) section.

The client SHOULD check the `verifier` for mutual authentication, terminating the session if invalid.

###### Final Server Authentication Message - Failure

If the authentication fails, the server SHALL respond with an `ABORT` message.

The server MAY include a SCRAM-specific error string in the `ABORT` message as a `Details.scram` attribute. SCRAM error strings are listed in [RFC5802, section 7](https://tools.ietf.org/html/rfc5802#section-7), under `server-error-value`.


##### SCRAM Algorithms

_This section is non-normative_.

[RFC5802](https://tools.ietf.org/html/rfc5802) specifies the algorithms used to compute the `ClientProof`, `ServerSignature`, `ServerKey`, and `StoredKey` values referenced by this document. Those algorithms are summarized here in pseudocode for reference.

###### Notation

* `"="`: The variable on the left-hand side is the result of the expression on the right-hand side.
* `"+"`: String concatenation.
* `IfNull(attribute, value, else)`: If the given `attribute` is absent or null, evaluates to the given `value`, otherwise evaluates to the given `else` value.
* `Decimal(integer)`: The decimal string representation of the given `integer`.
* `Base64(octets)`: Base64 encoding of the given octet sequence, restricted to canonical form with no whitespace, as defined in [RFC4648](https://tools.ietf.org/html/rfc4648).
* `UnBase64(str)`: Decode the given Base64 string into an octet sequence.
* `Normalize(str)`: Normalize the given string using the SASLprep profile [RFC4013](https://tools.ietf.org/html/rfc4013) of the "stringprep" algorithm [RFC3454](https://tools.ietf.org/html/rfc3454).
* `XOR`: The exclusive-or operation applied to each octet of the left and right-hand-side octet sequences.
* `SHA256(str)`: The SHA-256 cryptographic hash function.
* `HMAC(key, str)`: Keyed-hash message authentication code, as defined in [RFC2104](https://www.ietf.org/rfc/rfc2104.txt), with SHA-256 as the underlying hash function.
* `KDF(str, salt, params...)`: One of the supported key derivations function, with the output key length the same as the SHA-256 output length (32 octets). `params...` are the additional parameters that are applicable for the function: `iterations` and `memory`.
* `Escape(str)`: Replace every occurrence of "`,`" and "`=`" in the given string with "`=2C`" and "`=3D`" respectively.


###### Data Stored on the Server

For each user, the server needs to store:

1. A random, per-user salt.
2. The type string corresponding to the key derivation function (KDF) used to hash the password (e.g. `"argon2id13"`). This is needed to handle future revisions of the KDF, as well as allowing migration to stronger KDFs that may be added to WAMP-SCRAM in the future. This may also be needed if the KDF used during user registration is configurable or selectable on a per-user basis.
3. Parameters that are applicable to the key derivation function : `iterations` and possibly `memory`.
4. The `StoredKey`.
5. The `ServerKey`.

where `StoredKey` and `ServerKey` are computed as follows:

{align="left"}
```javascript
SaltedPassword  = KDF(Normalize(password), salt, params...)
ClientKey       = HMAC(SaltedPassword, "Client Key")
StoredKey       = SHA256(ClientKey)
ServerKey       = HMAC(SaltedPassword, "Server Key")
```

Note that `"Client Key"` and `"Server Key"` are string literals.

The manner in which the `StoredKey` and `ServerKey` are shared with the server during user registration is outside the scope of SCRAM and this document.


###### AuthMessage

In SCRAM, `AuthMessage` is used for computing `ClientProof` and `ServerSignature`. `AuthMessage` is computed using attributes that were sent in the first three messages of the authentication exchange.

{align="left"}
```javascript
ClientFirstBare = "n=" + Escape(HELLO.Details.authid) + "," +
                  "r=" + HELLO.Details.authextra.nonce

ServerFirst = "r=" + CHALLENGE.Details.nonce + "," +
              "s=" + CHALLENGE.Details.salt + "," +
              "i=" + Decimal(CHALLENGE.Details.iterations)

CBindName = AUTHENTICATE.Extra.channel_binding

CBindData = AUTHENTICATE.Extra.cbind_data

CBindFlag = IfNull(CBindName, "n", "p=" + CBindName)

CBindInput = CBindFlag + ",," +
             IfNull(CBindData, "", UnBase64(CBindData))

ClientFinalNoProof = "c=" + Base64(CBindInput) + "," +
                     "r=" + AUTHENTICATE.Extra.nonce

AuthMessage = ClientFirstBare + "," + ServerFirst + "," +
              ClientFinalNoProof
```

###### ClientProof

`ClientProof` is computed by the client during the authentication exchange as follows:

{align="left"}
```javascript
SaltedPassword  = KDF(Normalize(password), salt, params...)
ClientKey       = HMAC(SaltedPassword, "Client Key")
StoredKey       = SHA256(ClientKey)
ClientSignature = HMAC(StoredKey, AuthMessage)
ClientProof     = ClientKey XOR ClientSignature
```

The `ClientProof` is then sent to the server, base64-encoded, via the `AUTHENTICATE.Signature` argument.

The server verifies the `ClientProof` by computing the `RecoveredStoredKey` and comparing it to the actual `StoredKey`:

{align="left"}
```javascript
ClientSignature    = HMAC(StoredKey, AuthMessage)
RecoveredClientKey = ClientSignature XOR ReceivedClientProof
RecoveredStoredKey = SHA256(RecoveredClientKey)
```

Note that the client MAY cache the `ClientKey` and `StoredKey` (or just `SaltedPassword`) to avoid having to perform the expensive KDF computation for every authentication exchange. Storing these values securely on the client is outside the scope of this document.

###### ServerSignature

`ServerSignature` is computed by the server during the authentication exchange as follows:

{align="left"}
```javascript
ServerSignature = HMAC(ServerKey, AuthMessage)
```

The `ServerSignature` is then sent to the client, base64-encoded, via the `WELCOME.Details.authextra.verifier` attribute.

The client verifies the `ServerSignature` by computing it and comparing it with the `ServerSignature` sent by the server:

{align="left"}
```javascript
ServerKey       = HMAC(SaltedPassword, "Server Key")
ServerSignature = HMAC(ServerKey, AuthMessage)
```

##### Key Derivation Functions

SCRAM uses a password-based key derivation function (KDF) to hash user passwords. WAMP-SCRAM supports both [Argon2](https://datatracker.ietf.org/doc/draft-irtf-cfrg-argon2/) and [PBKDF2](https://tools.ietf.org/html/rfc2898) as the KDF. Argon2 is recommended because of its memory hardness and resistance against GPU hardware. PBKDF2, which does not feature memory hardness, is also supported for applications that are required to use primitives currently approved by cryptographic standards.

The following table maps the `CHALLENGE.Details.kdf` type string to the corresponding KDF.

KDF type string | Function
--------------- | --------
`"argon2id13"` | Argon2id variant of Argon2, version 1.3
`"pbkdf2"`      | PBKDF2

To promote interoperability, WAMP-SCRAM client/server implementations SHOULD support both of the above KDFs. During authentication, there is no "negotiation" of the KDF, and the client MUST use the same KDF than the one used to create the keys stored in the authentication database.

Which KDF is used to hash the password during user registration is up to the application and/or server implementation, and is not covered by this document. Possibilities include:

* making the KDF selectable at runtime during registration,
* making the KDF statically configurable on the server, or,
* hard-coding the KDF selection on the server.

###### Argon2

The Argon2 key derivation function, proposed in [draft-irtf-cfrg-argon2](https://datatracker.ietf.org/doc/draft-irtf-cfrg-argon2/), is computed using the following parameters:

* `CHALLENGE.Details.salt` as the cryptographic salt,
* `CHALLENGE.Details.iterations` as the number of iterations,
* `CHALLENGE.Details.memory` as the memory size (in kibibytes),
* 1 as the parallelism parameter,
* Argon2id as the algorithm variant, and,
* 32 octets as the output key length.

For WAMP-SCRAM, the parallelism parameter is fixed to 1 due to the password being hashed on the client side, where it is not generally known how many cores/threads are available on the client's device.

Section 4 of the Argon2 internet draft recommends the general procedure for selecting parameters, of which the following guidelines are applicable to WAMP-SCRAM:

* A 128-bit salt is recommended, which can be reduced to 64-bit if space is limited.
* The `memory` parameter is to be configured to the maximum amount of memory usage that can be tolerated on client devices for computing the hash.
* The `iterations` parameter is to be determined experimentally so that execution time on the client reaches the maximum that can be tolerated by users during authentication. If the execution time is intolerable with `iterations` = 1, then reduce the `memory` parameter as needed.

###### PBKDF2

The PBKDF2 key derivation function, defined in [RFC2898](https://tools.ietf.org/html/rfc2898), is used with SHA-256 as the pseudorandom function (PRF).

The PDBKDF2 hash is computed using the folowing parameters:

* `CHALLENGE.Details.salt` as the cryptographic salt,
* `CHALLENGE.Details.iterations` as the iteration count, and,
* 32 octets as the output key length (`dkLen`), which matches the SHA-256 output length.

[RFC2898 section 4.1](https://tools.ietf.org/html/rfc2898) recommends at least 64 bits for the salt.

The `iterations` parameter SHOULD be determined experimentally so that execution time on the client reaches the maximum that can be tolerated by users during authentication. [RFC7677 section 4](https://tools.ietf.org/html/rfc7677#section-4) recommends an iteration count of at least 4096, with a significantly higher value on non-mobile clients.
