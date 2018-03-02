#### Salted Challenge Response Authentication Mechanism {#wamp-scram}

The WAMP Salted Challenge Response Authentication Mechanism ("WAMP-SCRAM"), is a password-based authentication method where the shared secret is neither transmitted nor stored as cleartext. WAMP-SCRAM is based on [RFC5802](https://tools.ietf.org/html/rfc5802) (_Salted Challenge Response Authentication Mechanism_) and [RFC7677](https://tools.ietf.org/html/rfc7677) (_SCRAM-SHA-256 and SCRAM-SHA-256-PLUS_).


##### Security Considerations

With WAMP-SCRAM, if the password database is stolen, an attacker cannot impersonate a user unless they guess the password offline by brute force. WAMP-SCRAM supports strong password-based key derivation functions, such as bcrypt, scrypt, or Argon2.

In the event that the server's password database is stolen, and the attacker either eavesdrops on one authentication exchange or impersonates a server, the attacker gains the ability to impersonate that particular user on that server. If the same salt is used on other servers, the attacker would gain the ability to impersonate that user on all servers using the same salt. That's why it's important to use a per-user random salt.

An evesdropper that captures a user anthentication exchange has enough information to mount an offline, brute-force dictionary attack for that particular user. If passwords are sufficiently strong, the cost/time needed to crack a password becomes prohibitive.

Note that when HTML/Javascript assets are served to a web browser, WAMP-SCRAM does not safeguard against a man-in-the-middle tampering with those assets. Those assets could be tampered with in a way that captures the user's password and sends it to the attacker.

In light of the above security concerns, a secure TLS transport is therefore advised to prevent such attacks. The channel binding feature of SCRAM can be used to ensure that the TLS endpoints are the same between client and router.


##### Deviations from RFC5802

1. To simplify parsing, SCRAM attributes in the authentication exchange messages are encoded as members of the `Options`/`Details` objects without escaping the `,` and `=` characters as `=2C` and `=3D`. However the `AuthMessage` used to compute the client and server signatures DOES use the exact syntax specified in [RFC5802, section 7](https://tools.ietf.org/html/rfc5802#section-7). This makes it possible to use existing test vectors to verify WAMP-SCRAM implementations.

2. The hashing based on the weaker SHA-1 is not supported in favor of SHA-256.

3. Stronger key derivation functions MAY be used instead of PBKDF2.


##### WAMP-SCRAM Family of Authentication Methods

WAMP-SCRAM supports several variants of authentication methods that use different key derivation functions for hashing passwords:

WAMP authmethod String          | Key Derivation Function
--------------------------      | -----------------------
wamp-scram-pbkdf2[-plus]        | PBKDF2 + SHA256
wamp-scram-bcrypt[-plus]        | bcrypt
wamp-scram-scrypt[-plus]        | scrypt
wamp-scram-argon2d[-plus]       | Argon2d
wamp-scram-argon2i[-plus]       | Argon2i
wamp-scram-argon2id[-plus]      | Argon2id

where [-plus] is an optional suffix that indicates that channel binding is supported. See [Channel Bindings](#channel-bindings).

See [Key Derivation Functions](#key-derivation-funtions) for descriptions and the parameters used for each function.

Hashing based on the weaker SHA-1 specified in [RFC5802](https://tools.ietf.org/html/rfc5802) is intentionally not supported by WAMP-SCRAM, in favor of the stronger SHA-256 specified in [RFC7677](https://tools.ietf.org/html/rfc7677).

Announcement of supported WAMP-SCRAM methods by routers is outside the scope of this document.

##### Conventions

###### Base64 encoding

Base64 encoding of octet strings is restricted to canonical form with no whitespace, as defined in [RFC4648](https://tools.ietf.org/html/rfc4648) (_The Base16, Base32, and Base64 Data Encodings_).

###### Nonces

In SCRAM, a _nonce_ (number used once) is sequence of random printable ASCII characters excluding `','`. Characters can be in the ranges of 0x21-0x2b and 0x2D-0x7E (inclusive). This value MUST be different for each authentication.

See [RFC4086](https://tools.ietf.org/html/rfc4086) (_Randomness Requirements for Security_) for best practices concerning randomness.

Note that a base64 or hex-encoded integer meets the requirements for SCRAM nonces.

###### Username/Password String Normalization

Username and password strings SHALL be normalized according to the _SASLprep_ profile described in [RFC4013](https://tools.ietf.org/html/rfc4013), using the _stringprep_ algorithm described in [RFC3454](https://tools.ietf.org/html/rfc3454).

While SASLprep preserves the case of usernames, the server MAY choose to perform case insensitve comparisons when searching for a username in the authentication database.


##### User Impersonation

_Impersonation_ allows a priviledged user to log in using his/her credentials, but act as a different identity within the application, using the permissions of that different identify. A use case for this feature would be an administrator authenticating using his/her credentials and then customizing a user's settings as if the administrator were that user. Another use case would be a technical support representative remotely logging into the server, but acting as if he/she is the customer.

SCRAM supports the SASL _authorization identity_ defined in [RFC4422, section 3.4.1](https://tools.ietf.org/html/rfc4422#section-3.4.1). This SASL authorization identify allows a client to impersonate a user.

How the application behaves for an impersonated user, or whether user impersonation is even permitted, is a local matter outside the scope of this document.

##### Channel Bindings

_Channel binding_ is a feature that allows higher layers to establish that the other end of an underlying secure channel is bound to its higher layer counterpart. See [RFC5056](https://tools.ietf.org/html/rfc5056) (_On the Use of Channel Bindings_) for an in-depth discussion.

The following table summarizes the possible values than can be used for the `gs2_cbind_flag` attribute, as specified by [RFC5802, section 7](https://tools.ietf.org/html/rfc5802#section-7).

Flag               | Meaning
------------------ | -------
`null`             | Client doesn't support channel binding (same as `"n"`).
`"n"`              | Client doesn't support channel binding.
`"y"`              | Client does support channel binding but thinks the server does not.
`"p="` + `cb-name` | Client requires channel binding, e.g., `"p=tls-server-end-point"`

where `cb-name` is a channel binding type string, and "`+`" represents string concatenation.

[RFC5929](https://tools.ietf.org/html/rfc5929) defines binding types for use with TLS transports, of which `"tls-server-end-point"` may be used with SCRAM. Note that [RFC7677, section 1](https://tools.ietf.org/html/rfc7677#section-1), states that TLS did not have the expected properties for `"tls-unique"` to be secure.

The `"y"` flag is intended to safeguard against downgrade attacks (e.g. "-plus" mechanisms were removed from the router's authmethod list by an attacker). Since WAMP router feature announcement is only done as part of the `WELCOME` message, routers cannot rely on WAMP feature announcement to advertize support for "-plus" mechanisms before the client sends its `WELCOME` message. Announcement of channel binding support by routers is therefore outside the scope of this WAMP protocol document.


##### Authentication Exchange

WAMP-SCRAM uses a single round of challenge/response pairs after the client authentication request and before the authentication outcome.

The mapping of RFC5802 messages to WAMP messages is as follows:

SCRAM Message                              | WAMP Message
----------------------                     | ------------
`client-first-message`                     | `WELCOME`
`server-first-message`                     | `CHALLENGE`
`client-final-message`                     | `AUTHENTICATE`
`server-final-message` with `verifier`     | `WELCOME`
`server-final-message` with `server-error` | `ABORT`


###### Initial Client Authentication Message

WAMP-SCRAM authentication begins with the client sending a `HELLO` message specifying the `wamp-scram-*` method as (one of) the authentication methods:

{align="left"}
```javascript
    [1, "realm1",
        {
            "roles": ...,
            "authmethods": ["wamp-scram-pbkdf2"],
            "authid": "user",
            "nonce": "rOprNGfwEbeRWgbNEkqO",
            "impersonated_id": null,
            "gs2_cbind_flag": null,
        }
    ]
```
where:

1. `authid|string`: The identity of the user performing authentication. This corresponds to the `username` parameter in RFC5802.
2. `nonce|string`: A sequence of random printable ASCII characters generated by the client. See [Nonces](#nonces).
3. `impersonated_id|string`: Optional string that identifies the user as which to impersonate (see [User Impersonation](#user-impersonation)). If absent, the client is requesting to act as the identity associated with `authid`.
4. `gs2_cbind_flag|string`: Optional string containing the channel binding flag. See [Channel Bindings](#channel-bindings).

Upon receiving the WELCOME message, the server MUST terminate the authentication process by sending an `ABORT` message under any of the following circumstances:

* The server does not support any of the given WAMP-SCRAM `authmethods`, and there are no other methods left that the server supports for this `authid`.
* Impersonation was requested by the client, but the server does not support impersonation.
* The user associated with `authid` does not have permission to impersonate the given `impersonated_id`.
* Ther server recognizes `authid` but does not recognize `impersonated_id`.
* The `gs2_cbind_flag` was set to `"y"` and the server supports channel binding. If this happens, then it is an indication that there may have been a downgrade attack.
* The `gs2_cbind_flag` was set to `"p"` and the server does not support the requested binding type.
* (Optional) The server does not recognize the given `authid`.

###### Initial Server Authentication Message

If none of the above failure conditions apply, and the server is ready to let the client authenticate using WAMP-SCRAM, then it MUST send a `CHALLENGE` message:

{align="left"}
```javascript
    [4, "wamp-scram-pbkdf2",
        {
            "nonce": "rOprNGfwEbeRWgbNEkqO%hvYDpWUa2RaTCAfuxFIlj)hNlF$k0",
            "salt": "W22ZaJ0SNY7soEsUEjb6gQ==",
            "cost": 4096,
            "memory": null,
            "parallel": null,
            "version_num": null,
            "version_str": null
        }
    ]
```

where:

1. `nonce|string`: A server-generatated nonce that is appended to the client-generated nonce sent in the previous `WELCOME` message. See [Nonces](#nonces).
2. `salt|string`: The base64-encoded salt for this user, to be passed to the password hash function. To prevent rainbow table attacks in the event of database theft, the salt MUST be generated randomly by the server **for each user**. The random salt is stored with each user record in the password database.
3. `cost|integer`: The runtime cost factor to use for generating the `SaltedPassword` hash. For most key derivation functions, this is an iteration count. This value is stored with each user record in the password database.
4. `memory|integer`: The memory cost factor to use for generating the `SaltedPassword` hash. This is only used by the scrypt and Argon2 functions. This value is stored with each user record in the password database.
5. `parallel|integer`: The parallization factor to use for generating the `SaltedPassword` hash. This is only used by the scrypt and Argon2 functions. This value is stored with each user record in the password database.
6. `version_num|integer`: The version number of the Argon2 function to use. This value is stored with each user record in the password database.
7. `version_str|string`: This version ID of the bcrypt function to use. This value is stored with each user record in the password database.

To prevent a rogue server from obtaining a weak password hash, the client SHOULD check that the various cost parameters are not unusually low.

In the case of an unrecognized `authid` received via the `AUTHENTICATE` message, the server MAY choose to respond with a mock `CHALLENGE` message in order to avoid leaking information about the existence of a username. This mock `CHALLENGE` SHOULD contain a generated `salt` value that is always the same for a given `authid`, otherwise an attacker may discover that the user doesn't actually exist.

###### Final Client Authentication Message

Upon receiving the `CHALLENGE` message, the client SHALL respond with an `AUTHENTICATE` message:

{align="left"}
```javascript
    [5, "dHzbZapWIk4jUhN+Ute9ytag9zjfMHgsqmmiz7AndVQ=",
        {
            "nonce": "rOprNGfwEbeRWgbNEkqO%hvYDpWUa2RaTCAfuxFIlj)hNlF$k0",
            "impersonated_id": null,
            "gs2_cbind_flag": null,
            "cbind_data": null
        }
    ]
```
where:

1. `Signature|string` argument: The base64-encoded `ClientProof`, computed as described in the [SCRAM-Algorithms](#scram-algorithms) section.
2. `nonce|string`: The concatenated client-server nonce from the previous `CHALLENGE` message.
3. `impersonated_id|string`: Optional string containing the impersonated user ID that was sent in the original `HELLO` message.
4. `gs2_cbind_flag|string`: Optional string containing the channel binding flag that was sent in the original `HELLO` message.
5. `cbind_data|string`: Optional base64-encoded channel binding data. MUST be present if and only if the `gs2_cbind_flag` is `"p"`. The format of the binding data is dependent on the binding type.

Upon receiving the `AUTHENTICATE` message, the server SHALL then check that:

* The `AUTHENTICATE` message was received in due time.
* The `ClientProof` passed via the `Signature|string` argument is validated against the `StoredKey` and `ServerKey` stored in the password database. See [SCRAM Algorithms](#scram-algorithms).
* The `impersonated_id` matches the one sent in the `HELLO` message.
* The `gs2_cbind_flag` matches the one sent in the `HELLO` message.
* The `cbind_data`, if applicable, is valid.


###### Final Server Authentication Message - Success

If the authentication succeeds, the server SHALL finally respond with a `WELCOME` message:

{align="left"}
```javascript
    [2, 3251278072152162,
        {
            "authid": "user",
            "authrole": "admin",
            "authmethod": "wamp-scram-sha-256",
            "authprovider": "static",
            "roles": ...
            "scram_verifier": "v=6rriTRBi23WpRR/wtup+mMhUZUn/dB5nLTJRsjl95G4="
        }
    ]
```

where:

1. `authid|string`: The authentication ID the client was actually authenticated as. If user impersonation was requested, `authid` SHALL be the same ID as `impersonated_id`.
2. `authrole|string`: The authentication role the client was authenticated for.
3. `authmethod|string`: The authentication method, here `"wamp-scram-*"`.
4. `authprovider|string`: The actual provider of authentication. For WAMP-SCRAM authentication, this can be freely chosen by the app, e.g. static or dynamic.
5. `scram_verifier|string`: The base64-encoded `ServerSignature`, computed as described in the [SCRAM Algorithms](#scram-algorithms) section. The client SHOULD check this verifier for mutual authentication.


###### Final Server Authentication Message - Failure

If the authentication fails, the server SHALL respond with an `ABORT` message.

The server MAY include a SCRAM-specific error string in the `ABORT` message as a `Details.scram` attribute. SCRAM error strings are listed in [RFC5802, section 7](https://tools.ietf.org/html/rfc5802#section-7), under `server-error-value`.


##### SCRAM Algorithms

_This section is non-normative_.

[RFC5802](https://tools.ietf.org/html/rfc5802) specifies the algorithms used to compute the `ClientProof`, `ServerSignature`, `ServerKey`, and `StoredKey` values referenced by this document. Those algorithms are summarized here in pseudocode for reference.

###### Notation

* `"="`: The variable on the left-hand side is the result of the expression on the right-hand side.
* `"+"`: String concatenation.
* `ValueOr(attribute, fallback)`: If the given `attribute` is absent or null, evaluates to the given `fallback` value, otherwize evaluates to `attribute`.
* `Decimal(integer)`: The decimal string representation of the given `integer`.
* `Base64(octets)`: Base64 encoding of the given octet sequence, restricted to canonical form with no whitespace, as defined in [RFC4648](https://tools.ietf.org/html/rfc4648).
* `UnBase64(str)`: Decode the given Base64 string into an octet sequence.
* `Normalize(str)`: Normalize the given string using the SASLprep profile [RFC4013](https://tools.ietf.org/html/rfc4013) of the "stringprep" algorithm [RFC3454](https://tools.ietf.org/html/rfc3454).
* `XOR`: The exclusive-or operation applied to each octet of the left and right-hand-side octet sequences.
* `SHA256(str)`: The SHA-256 cryptographic hash function.
* `HMAC(key, str)`: Keyed-hash message authentication code, as defined in [RFC2104](https://www.ietf.org/rfc/rfc2104.txt), with SHA-256 as the underlying hash function.
* `KDF(str, salt, params...)`: One of the supported key derivations function, with the output key length the same as the SHA-256 output length (32 octets). `params...` are the additional parameters that are applicable for the function: `cost`, `memory`, `parallel`, `version-num`, `version_str`.
* `Escape(str)`: Replace every occurrence of "`,`" and "`=`" in the given string with "`=2C`" and "`=3D`" respectively.


###### Data Stored on the Server

For each user, the server needs to store:

1. A random, per-user salt.
2. Parameters that are applicable to the key derivation function : `cost`, `memory`, `parallel`, `version_num`, `version_str`.
3. The `StoredKey`.
4. The `ServerKey`.

where `StoredKey` and `ServerKey` are computed as follows:

{align="left"}
```javascript
SaltedPassword  = KDF(Normalize(password), salt, params...)
ClientKey       = HMAC(SaltedPassword, "Client Key")
StoredKey       = SHA256(ClientKey)
ServerKey       = HMAC(SaltedPassword, "Server Key")
```

Note that `"Client Key"` are `"Server Key"` are string literals.

The manner in which the `StoredKey` and `ServerKey` are shared with the server is outside the scope of SCRAM and WAMP.


###### AuthMessage

In SCRAM, `AuthMessage` is used for computing `ClientProof` and `ServerSignature`. `AuthMessage` is computed using attributes that were sent in the first three messages of the authentication exchange.

{align="left"}
```javascript
ClientFirstBare = "n=" + Escape(HELLO.Details.authid) + "," +
                  "r=" + HELLO.Details.nonce

ServerFirst = "r=" + CHALLENGE.Details.nonce + "," +
              "s=" + CHALLENGE.Details.salt + "," +
              "i=" + Decimal(CHALLENGE.Details.cost)

CBindInput = ValueOr(HELLO.Details.gs2_cbind_flag, "n") + "," +
             Escape(ValueOr(HELLO.Details.impersonated_id, "")) + "," +
             UnBase64(ValueOr(AUTHENTICATE.Extra.cbind_data, ""))

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

The `ServerSignature` is then sent to the client, base64-encoded, via the `WELCOME.Details.scram_verifier` attribute.

The client verifies the `ServerSignature` by computing it and comparing it with the `ServerSignature` sent by the server:

{align="left"}
```javascript
ServerKey       = HMAC(SaltedPassword, "Server Key")
ServerSignature = HMAC(ServerKey, AuthMessage)
```

##### Key Derivation Function Parameters

The section describes the key derivation functions that are supported by WAMP-SCRAM.

###### wamp-scram-pbkdf2

`wamp-scram-pbkdf2` uses the PBKDF2 key derivation function, defined in [RFC2898](https://tools.ietf.org/html/rfc2898). PBKDF2 is used with SHA-256 as the pseudorandom function (PRF).

The PDBKDF2 hash is computed using the folowing parameters:

* `CHALLENGE.Details.salt` as the cryptographic salt,
* `CHALLENGE.Details.cost` as the iteration count, and,
* 32 octets as the output key length (`dkLen`), which matches the SHA-256 output length.

###### wamp-scram-bcrypt

`wamp-scram-bcrypt` uses the [bcrypt](https://www.usenix.org/legacy/event/usenix99/provos/provos.pdf) key derivation function, computed using the following parameters:

* `CHALLENGE.Details.salt` as the cryptographic salt,
* `CHALLENGE.Details.cost` as the base 2 work factor exponent (iterations = 2^cost),
* `CHALLENGE.Details.version_str` as the algorithm version, and,
* 32 octets as the output key length.

bcrypt has a maximum password length, which varies among implementations between 51 and 71 octets. WAMP-SCRAM removes this limitation by requiring that the normalized password be pre-processed using SHA-256 and Base64.

The output hash of bcrypt is fed into SHA-256 to produce a `SaltedPassword` hash with the required length of 32 octets.

In pseudocode:

{align="left"}
```javascript
PreprocessedPassword = Base64(SHA256(Normalize(password)))
SaltedPassword = SHA256(bcrypt(PreprocessedPassword, params...))
```

###### scrypt

`wamp-scram-scrypt` uses the scrypt key derivation function, defined in  ([RFC7914](https://tools.ietf.org/html/rfc7914)), computed using the following parameters:

* `CHALLENGE.Details.salt` as the cryptographic salt,
* `CHALLENGE.Details.cost` as the CPU/Memory cost parameter,
* `CHALLENGE.Details.memory` as the blockSize parameter,
* `CHALLENGE.Details.parallel` as the parallization parameter, and,
* 32 octets as the output key length.

###### Argon2

The `wamp-scram-argon*` family of authorization methods uses the Argon2 key derivation function, proposed in [draft-irtf-cfrg-argon2](https://datatracker.ietf.org/doc/draft-irtf-cfrg-argon2/), computed using the following parameters:

* `CHALLENGE.Details.salt` as the cryptographic salt,
* `CHALLENGE.Details.cost` as the number of iterations,
* `CHALLENGE.Details.memory` as the memory size (in kibibytes),
* `CHALLENGE.Details.parallel` as the degree of parallelism,
* `CHALLENGE.Details.version_num` as the algorithm version, and,
* 32 octets as the output key length.
