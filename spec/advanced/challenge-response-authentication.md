# Challenge Response Authentication

WAMP Challenge-Response ("WAMP-CRA") authentication is a simple, secure authentication mechanism using a shared secret. The client and the server share a *secret*. The secret never travels the wire, hence WAMP-CRA can be used via non-TLS connections. The actual pre-sharing of the secret is outside the scope of the authentication mechanism.

A typical authentication begins with the client sending a `HELLO` message specifying the `wampcra` method as (one of) the authentication methods:

```javascript
[1, "realm1",
    {
        "roles": ...,
        "authmethods": ["wampcra"],
        "authid": "peter"
    }
]
```

The `HELLO.Details.authmethods|list` is used by the client to announce the authentication methods it is prepared to perform. For WAMP-CRA, this MUST include `"wampcra"`.

The `HELLO.Details.authid|string` is the authentication ID (e.g. username) the client wishes to authenticate as. For WAMP-CRA, this MUST be provided.

If the server is unwilling or unable to perform WAMP-CRA authentication, it'll either skip forward trying other authentication methods (if the client announced any) or send an `ABORT` message.

If the server is willing to let the client authenticate using WAMP-CRA, and the server recognizes the provided `authid`, it'll send a `CHALLENGE` message:

```javascript
[4, "wampcra",
    {
        "challenge": "{\"nonce\": \"LHRTC9zeOIrt_9U3\", \"authprovider\": \"userdb\", \"authid\": \"peter\",
                       \"timestamp\": \"2014-06-22T16:36:25.448Z\", \"authrole\": \"user\",
                       \"authmethod\": \"wampcra\", \"session\": 3251278072152162}"
    }
]
```

The `CHALLENGE.Details.challenge|string` is a string the client needs to create a signature for. The string MUST BE a JSON serialized object which MUST contain:

 1. `authid|string`: The authentication ID the client will be authenticated as when the authentication succeeds.
 2. `authrole|string`: The authentication role the client will be authenticated as when the authentication succeeds.
 3. `authmethod|string`: The authentication methods, here `"wampcra"`
 4. `authprovider|string`: The actual provider of authentication. For WAMP-CRA, this can be freely chosen by the app, e.g. `userdb`.
 5. `nonce|string`: A random value.
 6. `timestamp|string`: The UTC timestamp (ISO8601 format) the authentication was started, e.g. `2014-06-22T16:51:41.643Z`.
 7. `session|int`: The WAMP session ID that will be assigned to the session once it is authenticated successfully.

The client needs to compute the signature as follows:

    signature := HMAC[SHA256]_{secret} (challenge)

That is, compute the HMAC-SHA256 using the shared `secret` over the `challenge`.

After computing the signature, the client will send an `AUTHENTICATE` message containing the signature:

```javascript
[5, "gir1mSx+deCDUV7wRM5SGIn/+R/ClqLZuH4m7FJeBVI=", {}]
```

The server will then check if

* the signature matches the one expected
* the `AUTHENTICATE` message was sent in due time

If the authentication succeeds, the server will finally respond with a `WELCOME` message:

```javascript
[2, 3251278072152162,
    {
        "authid": "peter",
        "authrole": "user",
        "authmethod": "wampcra",
        "authprovider": "userdb",
        "roles": ...
    }
]
```

The `WELCOME.Details` again contain the actual authentication information active.

If the authentication fails, the server will response with an `ABORT` message.


## Server-side Verification

The challenge sent during WAMP-CRA contains

1. random information (the `nonce`) to make WAMP-CRA robust against replay attacks
2. timestamp information (the `timestamp`) to allow WAMP-CRA timeout on authentication requests that took too long
3. session information (the `session`) to bind the authentication to a WAMP session ID
4. all the authentication information that relates to authorization like `authid` and `authrole`


## Three-legged Authentication

The signing of the challenge sent by the server usually is done directly on the client. However, this is no strict requirement.

E.g. a client might forward the challenge to another party (hence the "three-legged") for creating the signature. This can be used when the client was previously already authenticated to that third party, and WAMP-CRA should run piggy packed on that authentication.

The third party would, upon receiving a signing request, simply check if the client is already authenticated, and if so, create a signature for WAMP-CRA.

In this case, the secret is actually shared between the WAMP server who wants to authenticate clients using WAMP-CRA and the third party server, who shares a secret with the WAMP server.

This scenario is also the reason the challenge sent with WAMP-CRA is not simply a random value, but a JSON serialized object containing sufficient authentication information for the thrid party to check.


## Password Salting

WAMP-CRA operates using a shared secret. While the secret is never sent over the wire, a shared secret often requires storage of that secret on the client and the server - and storing a password verbatim (unencrypted) is not recommended in general.

WAMP-CRA allows the use of salted passwords following the [PBKDF2](http://en.wikipedia.org/wiki/PBKDF2) key derivation scheme. With salted passwords, the password itself is never stored, but only a key derived from the password and a password salt. This derived key is then practically working as the new shared secret.

When the password is salted, the server will during WAMP-CRA send a `CHALLENGE` message containing additional information:

```javascript
[4, "wampcra",
    {
        "challenge": "{\"nonce\": \"LHRTC9zeOIrt_9U3\", \"authprovider\": \"userdb\", \"authid\": \"peter\",
                       \"timestamp\": \"2014-06-22T16:36:25.448Z\", \"authrole\": \"user\",
                       \"authmethod\": \"wampcra\", \"session\": 3251278072152162}",
        "salt": "salt123",
        "keylen": 32,
        "iterations": 1000
    }
]
```

The `CHALLENGE.Details.salt|string` is the password salt in use. The `CHALLENGE.Details.keylen|int` and `CHALLENGE.Details.iterations|int` are parameters for the PBKDF2 algorithm.
