### Ticket-based Authentication {#ticketauth}

With *Ticket-based authentication*, the client needs to present the server an authentication "ticket" - some magic value to authenticate itself to the server.

This "ticket" could be a long-lived, pre-agreed secret (e.g. a user password) or a short-lived authentication token (like a Kerberos token). WAMP does not care or interpret the ticket presented by the client.

> Caution: This scheme is extremely simple and flexible, but the resulting security may be limited. E.g., the ticket value will be sent over the wire. If the transport WAMP is running over is not encrypted, a man-in-the-middle can sniff and possibly hijack the ticket. If the ticket value is reused, that might enable replay attacks.
>

A typical authentication begins with the client sending a `HELLO` message specifying the `ticket` method as (one of) the authentication methods:

{align="left"}
```javascript
    [1, "realm1",
      {
        "roles": ...,
        "authmethods": ["ticket"],
        "authid": "joe"
      }
    ]
```

The `HELLO.Details.authmethods|list` is used by the client to announce the authentication methods it is prepared to perform. For Ticket-based, this MUST include `"ticket"`.

The `HELLO.Details.authid|string` is the authentication ID (e.g. username) the client wishes to authenticate as. For Ticket-based authentication, this MUST be provided.

If the server is unwilling or unable to perform Ticket-based authentication, it'll either skip forward trying other authentication methods (if the client announced any) or send an `ABORT` message.

If the server is willing to let the client authenticate using a ticket and the server recognizes the provided `authid`, it'll send a `CHALLENGE` message:

{align="left"}
```javascript
    [4, "ticket", {}]
```

The client will send an `AUTHENTICATE` message containing a ticket:

{align="left"}
```javascript
    [5, "secret!!!", {}]
```

The server will then check if the ticket provided is permissible (for the `authid` given).

If the authentication succeeds, the server will finally respond with a `WELCOME` message:

{align="left"}
```javascript
    [2, 3251278072152162,
      {
        "authid": "joe",
        "authrole": "user",
        "authmethod": "ticket",
        "authprovider": "static",
        "roles": ...
      }
    ]
```

where

1. `authid|string`: The authentication ID the client was (actually) authenticated as.
2. `authrole|string`: The authentication role the client was authenticated for.
3. `authmethod|string`: The authentication method, here `"ticket"`
4. `authprovider|string`: The actual provider of authentication. For Ticket-based authentication, this can be freely chosen by the app, e.g. `static` or `dynamic`.

The `WELCOME.Details` again contain the actual authentication information active. If the authentication fails, the server will response with an `ABORT` message.
