## Payload End-to-End Encryption

*WAMP End-to-End Encryption* ("WAMP-E2EE" or "E2EE" for short) is a feature in the *WAMP Advanced Profile* that 
enables an **enhanced security model** for WAMP based systems which isolates WAMP endpoints (e.g. *Callers* 
and *Callees*) from routers. It provides enhanced application payload

* **Authenticity**,
* **Confidentiality** and
* **Integrity**

not only between WAMP endpoints and routers versus outside third-parties, but also versus the WAMP router nodes
themselves, transporting the application payload between WAMP endpoints.

### Enhanced Security Model

The security model of *Payload End-to-End Encryption* provides enhanced **Authenticity**, **Confidentiality** and
**Integrity** levels, namely end-to-end between WAMP endpoints, rather than only for a WAMP endpoint-to-router link,
while **Availability** remains independent and at the original level.

Further, guarantees include

* **Privacy**
* **Plausible-deniability**
* **Non-repudiability**

of the application payload versus the *Router*.
Note that this only applies to the payload, not the metadata such as the URI, which might itself e.g. reveal
information to a router. Of course the metadata is necessary for a WAMP router to read, as it needs to take
correct WAMP routing decisions based on WAMP message metadata.

### How it works

*Payload End-to-End Encryption* works by encrypting the application payload contained in WAMP messages
(e.g. `CALL.args|list`) with keys only accessible to authorized WAMP endpoints. Routers transporting traffic between
WAMP endpoints can only read and process the WAMP message and e.g. take routing decisions based on the WAMP URI in
the message, but can not decrypt and read the contained application payload.

Note that payload end-to-end encryption is different from link-level transport encryption, e.g. when a WAMP endpoint
uses TLS to connect to its uplink router. In this case, the WAMP message, and the (plaintext) application payload
embedded in the message can not be read by third parties (anyone outside the TLS connection), but it can be read
by the router.

{align="left"}
```
                       .-------------------.                                   
                      ( Payload Encryption  )                                  
                       `---------+---------'                                   
                                  +                +-------------+             
                                  v                |WAMP Message |             
 +------+     +----------+     +----------------+  | +---------+ |     +------+
 |      |     |Serialized|     |XSalsa20Poly1306|  | |Encrypted| |     |      |
 |Peer 1+(1)->| Payload  +(2)->|Symmetric Cipher+--+>| Payload | +(3)->|Peer 2|
 |      |     |          |     |                |  | |         | |     |      |
 +------+     +----------+     +----------------+  | +---------+ |     +------+
                                        ^          +-------------+        (8)  
                                        |           E2E Encrypted              
                               +--------+-------+  Payload Traffic             
                               |  Secret Data   |                              
                    Ephemeral  | Encryption Key |                              
                     Payload   +----------------+                              
                   Encryption  +----------------+                              
                      Keys     |  Secret Data   |                              
                               | Encryption Key |                              
                               +----------------+                              
                               +----------------+                              
 Client Session                |  Secret Data   |               Client Session 
 Authentication                | Encryption Key |               Authentication 
      Keys                     +--------+-------+                    Keys      
 +----------+    .---------------.      |                          +----------+
 |Peer 1 CS |   (Key Distribution )     |                          |Peer 2 CS |
 |Public Key|    `---------+-----'      |                 +------+-+Public Key|
 |          |                           |                 |      | |          |
 +----------+              |            v                 |      | +----------+
 +----------+               - >+----------------+         |      | +----------+
 |Peer 1 CS |                  |   Curve25519   |         |      | |Peer 2 CS |
 | Private  +----------------->|   Asymmetric   |<--------+      | | Private  |
 |   Key    |                  |     Cipher     |                | |   Key    |
 +----------+                  +--------+-------+                | +----------+
                                        |     Request Payload    |             
                                        |      Encryption Key    |             
                                       (7)   +----------------+  |             
                                        |    |  WAMP Message  |  |             
                                 +------+    |+--------------+|  |             
                                 |           ||Peer 2 Signed ||  |             
     +---------------------------+-----------+|EIP712Delegate||<-+--(4)----+   
     |                           |           || Certificate  ||  |         |   
     |                  +--------+-------+   |+--------------+|  |         |   
     |                  |  WAMP M|ssage  |   +--------^-------+  |         |   
     v                  |        v       |            |          |         |   
 +------+               |+--------------+|            |          |     +---+--+
 |      |               ||  Encrypted   ||            |          |     |      |
 |Peer 1+-----(6)------>|| Secret Data  |+------------+----------+---->|Peer 2|
 |      |               ||Encryption Key||            |          |     |      |
 +------+               |+--------------+|            |          |     +------+
                        |                |            |          |             
                        +----------------+  +---------+--------+ |             
                         Response Payload   |sec256k1 / EIP712 | |             
                          Encryption Key  ->|    Asymmetric    |<+             
                                         |  |    Signature     |               
                                            +------------------+               
 +----------+                            |            ^            +----------+
 |Peer 1 ETH|                 .-------------------.   |            |Peer 2 ETH|
 |Public Key|                ( Trust Establishment )  |            |Public Key|
 |          |                 `-------------------'   |            |          |
 +----------+                                         |            +----------+
 +----------+                                         |            +----------+
 |Peer 1 ETH|                                         |            |Peer 2 ETH|
 | Private  |                                         +--(5)-------+ Private  |
 |   Key    |                                                      |   Key    |
 +----------+                                                      +----------+
   Delegate                                                          Delegate  
 Certificate                                                       Certificate 
 Signing Keys                                                      Signing Keys
```

*Overview of End-to-End Encryption flow*

1. Peer 1 decides to use E2EE Payload for sending message to Peer 2 (this can be RPC Call or Publishing event to topic).
2. Peer 1 generates runtime ephemeral encryption key and encrypt payload using `XSalsa20Poly1306 Symmetric Cipher`.
3. WAMP message with Encrypted Payload is delivered to Peer 2 and Peer 2 doesn't have encryption key to decrypt payload.
4. Peer 2 makes an RPC CALL to procedure that name is provided by Peer 1 via options in sent WAMP message. 
5. Peer 2 attaches to CALL message its own `Client Session Public Key` and signs it with its own Delegate Certificate 
Private Key using `sec256k1 Asymmetric Signature`.
6. Peer 1 receives RPC invocation, verifies message signature and certificate chain up to known Trustroot 
(Standalone Trustroot, Shared Trustroot or On-chain Trustroot). 
7. Then Peer 1 encrypts runtime ephemeral encryption key used for encryption of original payload with its own 
`Client Session Private Key` and `Peer 2 Client Session Public Key` that was received in invocation message using
`Curve25519 Asymmetric Cipher` and sends YIELD->RESULT message to Peer 2.
8. Peer 2 decrypts RPC CALL RESULT with its own `Client Session Private Key` and gets runtime ephemeral encryption 
key using which Peer 2 now can decrypt original E2EE Payload.

*Payload End-to-End Encryption* can be divided into the following subproblems, and the approach taken by *WAMP-E2EE*
is described in the following sections:

1. [Payload Encryption](#payloadencr)
2. [Payload Transport](#payloadtnsp)
3. [Key Distribution](#keydist)
4. [Trust Management](#trustmgmt)


#### Payload Encryption {#payloadencr}

Payload Encryption consists of next steps: 

1. payload serialization
2. optional compression
3. symmetric encryption with XSalsa20Poly1305 (a.k.a. [NaCl crypto_secretbox](https://nacl.cr.yp.to/secretbox.html))

In regular WAMP clients communication payload may be delivered as `Arguments|list` an/or as `ArgumentsKw|dict`. For
optimal performance and security reasons `Arguments|list` and `ArgumentsKw|dict` are not encrypted separately and 
thus need to be serialized into one item

{align="left"}
```javascript
payload = {
    "args": Arguments|list,
    "kwargs": ArgumentsKw|dict,
    "uri": uri  // URI of RPC or Topic, read about this below
}
```

#TODO: Write some words about `optional compression` or maybe put to the future revision?

Then serialized payload is encrypted using XSalsa20Poly1305 
[authenticated encryption](https://en.wikipedia.org/wiki/Authenticated_encryption) cipher based on
the [XSalsa20](https://en.wikipedia.org/wiki/Salsa20) [stream cipher](https://en.wikipedia.org/wiki/Stream_cipher)
and the [Poly1305](https://en.wikipedia.org/wiki/Poly1305) hash function, which acts as a message authentication code.

Initiator peer that is going to send encrypted messages generate in runtime Ephemeral Payload Encryption Keys. 
The secret encryption keys for XSalsa20Poly1305 are 32 octets in length, and message nonces are 24 octets.
Peer can decide to choose different secret key rotation strategies: 

* on per message basis
* on per topic basis
* regenerate keys every N messages
* regenerate keys based on time

#### Payload Transport {#payloadtnsp}

After payload is encrypted it needs to be delivered within WAMP message to destination part. This is done using WAMP 
AP [Payload Passthru Mode](#payload-passthru-mode).

#### Encrypted Payload Flows {#encryptedpayloadflows}

There are few possible encrypted message flows:

* PUBLISHing an encrypted message to a topic. In this case **Publisher** choose secret key to encrypt data and all
subscribers interested in that data must get that key.
* CALLing an RPC with plain unencrypted payload and receiving encrypted results. In this case **Callee** choose
secret key to encrypt data and **Caller** must get that key.
* CALLing an RPC with encrypted payload and receiving plain unencrypted results. In this case **Caller** choose
secret key to encrypt data and **Callee** must get that key.
* CALLing an RPC with encrypted payload and receiving encrypted results. In this case there are 2 bidirectional
flows with encrypted data. In general every peer can use its own secret key and other peer has to obtain that key.
This can be suboptimal in some cases, especially with `Shared Registration`/`Sharded Registration` AP features
and may be improved by **Caller** requesting to use the same key to encrypt the result. So only one secret key
request will be needed.

#### Key Distribution {#keydist}

After encrypted message is delivered to destination target, how Peer can decrypt it if it doesn't have a secret key?
This problem can be solved in different ways:

* Initiator peer can provide an RPC to get the keys directly from it. In this case Initiator peer registers 
an RPC for getting a secret encryption keys and passes the `URI` of this RPC as options attribute to underlying 
WAMP message carrying encrypted payload. If target peer doesn't have a secret key it can examine message 
details and make a `CALL` to provided RPC requesting encryption key.
* Or there can be a third party WAMP peer the `Key exchange` which initiator peer trusts to and which is responsible
for key management. In this case Initiator peer passes the `URI` of trusted `Key exchange` RPC as options
attribute to underlying WAMP message carrying encrypted payload. If target peer doesn't have a secret key it can
examine message details and make a `CALL` to provided RPC requesting encryption key.

RPC may be registered on any side that encrypts payload: *Caller*, *Callee* or *Publisher* or by 3rd party
Key exchange component.

In any case at this point there is no secure channel between peers, so initiator peer can not simply send 
secret key as this will violate E2EE principle. Secure transfer of encryption keys are done using 
[Public-key cryptography](https://en.wikipedia.org/wiki/Public-key_cryptography) 
[Authenticated encryption](https://en.wikipedia.org/wiki/Authenticated_encryption).
This includes:

* sending target peer `Client Session Public Key` signed by target's peer `Delegated Certificate Private Key` 
to initiator or `Key exchange`.
* then initiator or `Key exchange` peer encrypts `secret key` with its own `Client Session Private Key` and 
`Target Peer Client Session Public Key` that was received using [Curve25519](https://en.wikipedia.org/wiki/Curve25519) 
Asymmetric Cipher
* and sends encrypted `secret key` and its own `Client Session Public Key` back to the target peer as a 
RESULT of RPC Invocation so target peer can decrypt RESULT with its own `Client Session Private Key` and get
the `secret key`.

Independently of who is providing an RPC for obtaining secret key (Initiator peer or Key exchange), RPC
registration must conform next rules:

* Must be single
* Must be not pattern-based
* Must be not shared
* Must be with `single` invocation policy

The Initiator peer or Key exchange may decide how and when to register this RPC:

* It can be registered on per URI basis. One request key RPC for every topic or procedure.
* It can be registered one time and serve all incoming requests for keys for all topics this peer publishes to
  and all procedures invoked by this peer. Invocation to this RPC contains all required information. This
  is described later in this chapter.
* Peer may decide to unregister RPC after invocation or on time basis.

Secret Key request RPC must be called with next `ArgumentsKw|dict` payload:

```
    {
        "uri": "URI of RPC or Topic for which/from which encrypted payload is intended",
        "uri_type": "rpc|topic",
        "peer_type": "caller|calee|publisher|subscriber",
        "pubkey": "32 bytes hex encoded string of peer Ed25519 Public Key"
    }
```

If RPC holder (Peer or Key exchange) is willing to fulfill request it must answer with 
next `ArgumentsKw|dict` payload:


```
    {
        "secret": "hex encoded string with secret key encrypted with Curve25519 Asymmetric Cipher",
        "pubkey": "32 bytes hex encoded string of peer Ed25519 Public Key",
        "nonce": "24 bytes hex encoded unique nonce used for exactly this one encryption of secret key",
        "keyid": "secret key id string",
        "expires": "unix timestamp when secret key will be expired if peer is making time-based key rotation. Optional"
    }
```

#### Trust Management {#trustmgmt}

[trust on first use](https://en.wikipedia.org/wiki/Trust_on_first_use)

management of the Operator-CA to Realm-CA relationships

* mutual trust problem: decentralized on-chain certificates
* remote trust problem: e2ee and remote attestation

1) standalone trustroots / centralized trust model
2) on-chain trustroots / decentralized trust model

### Message structure

**Feature Announcement**

Support for this advanced feature MUST be announced by *Callers* (`role := "caller"`), *Callees* (`role := "callee"`),
*Dealers* (`role := "dealer"`), *Publishers* (`role := "publisher"`), *Subscribers* (`role := "subscriber"`)
and *Brokers* (`role := "broker"`) via

{align="left"}
HELLO.Details.roles.<role>.features.payload_encryption|bool := true

Payload End-to-End Encryption can work only if all three nodes (*Caller*, *Dealer*, *Callee* or
*Publisher*, *Broker*, *Subscriber*) support and announced this feature.

Cases where a *Caller* sends a `CALL` message with `encrypted payload` without announcing it during the `HELLO`
handshake MUST be treated as *PROTOCOL ERRORS* and underlying WAMP connections must be aborted with
the `wamp.error.protocol_violation` error reason.

Cases where a *Caller* sends a `CALL` message with `encrypted payload` to a *Dealer*, the latter not announcing
`encrypted payload` support during `WELCOME` handshake MUST be treated as *PROTOCOL ERRORS* and the underlying WAMP
connections must be aborted with the `wamp.error.protocol_violation` error reason.

Cases where a *Caller* sends a `CALL` message with `encrypted payload` to a *Dealer* that supports this feature,
which then must be routed to a *Callee* which doesn't support `encrypted payload`, MUST be treated as
*APPLICATION ERRORS* and the *Dealer* MUST respond to the *Caller* with a `wamp.error.feature_not_supported`
error message.

Cases where a *Publisher* sends a `PUBLISH` message with `encrypted payload`, without announcing it during `HELLO`
handshake, MUST be treated as *PROTOCOL ERRORS* and the underlying WAMP connections must be aborted with
the `wamp.error.protocol_violation` error reason.

Cases where a *Publisher* sends a `PUBLISH` message with `encrypted payload` to a *Broker*, with the latter not
announcing `encrypted payload` support during the `WELCOME` handshake, MUST be treated as *PROTOCOL ERRORS* and
the underlying WAMP connections must be aborted with the `wamp.error.protocol_violation` error reason.

Cases where a *Publisher* sends a `PUBLISH` message with `encrypted payload` to a *Broker* that supports this feature,
which then must be routed to a *Subscriber* which doesn't support `encrypted payload`, cannot be recognized at the
protocol level due to asynchronous message processing and must be covered at the *Subscriber* side.

Cases where a *Callee* sends a `YIELD` message with `encrypted payload` without announcing it during the `HELLO`
handshake MUST be treated as *PROTOCOL ERRORS* and the underlying WAMP connections must be aborted with
the `wamp.error.protocol_violation` error reason.

Cases where a *Callee* sends a `YIELD` message with `encrypted payload` to a *Dealer*, with the latter not announcing
`encrypted payload` support during the `WELCOME` handshake, MUST be treated as *PROTOCOL ERRORS* and the
underlying WAMP connections must be aborted with the `wamp.error.protocol_violation` error reason.

Cases where a *Callee* sends a `YIELD` message with `encrypted payload` to a *Dealer* that supports this feature,
which then must be routed to the *Caller* which doesn't support `encrypted payload`, MUST be treated as
*APPLICATION ERRORS* and the *Dealer* MUST respond to the *Callee* with a `wamp.error.feature_not_supported`
error message.

**Message Attributes**

Payload End-to-End Encryption works on top of another WAMP advanced profile feature 
[Payload Passthru Mode](#name-payload-passthru-mode). It reuses next attributes:

* The `ppt_scheme` identifies the Payload Schema. There is a predefined scheme for End-to-End Encryption `wamp`.
* The `ppt_serializer` specifies what serializer was used to encode the payload.
* The `ppt_cipher` specifies the cryptographic algorithm that was used to encrypt the payload.
* The `ppt_keyid` can contain the encryption key id that was used to encrypt the payload.

And introduces a few more specific attributes:

**e2ee_request_key_rpc Attribute** 

The `e2ee_request_key_rpc` identifies the Initiator Peer or Key exchange registered RPC URI which other peers can
call to get *Secret Data Encryption Key* for payload decryption if they don't have it. It is a required string
attribute. Must conform to URI check rules. This must be existing registered RPC.

**e2ee_use_same_key Attribute**

The `e2ee_use_same_key` boolean attribute indicates the wish of the **Caller** sending the encrypted data -
that **Callee** uses the same secret key to send the result back.

{align="left"}
CALL.Options.ppt_scheme|string
CALL.Options.ppt_serializer|string
CALL.Options.ppt_cipher|string
CALL.Options.ppt_keyid|string
CALL.Options.e2ee_request_key_rpc|string
CALL.Options.e2ee_use_same_key|boolean
---
INVOCATION.Details.ppt_scheme|string
INVOCATION.Details.ppt_serializer|string
INVOCATION.Details.ppt_cipher|string
INVOCATION.Details.ppt_keyid|string
INVOCATION.Details.e2ee_request_key_rpc|string
INVOCATION.Details.e2ee_use_same_key|boolean
---
YIELD.Options.ppt_scheme|string
YIELD.Options.ppt_serializer|string
YIELD.Options.ppt_cipher|string
YIELD.Options.ppt_keyid|string
YIELD.Options.e2ee_request_key_rpc|string
---
RESULT.Details.ppt_scheme|string
RESULT.Details.ppt_serializer|string
RESULT.Details.ppt_cipher|string
RESULT.Details.ppt_keyid|string
RESULT.Details.e2ee_request_key_rpc|string
---
ERROR.Details.ppt_scheme|string
ERROR.Details.ppt_serializer|string
ERROR.Details.ppt_cipher|string
ERROR.Details.ppt_keyid|string
ERROR.Details.e2ee_request_key_rpc|string

{align="left"}
PUBLISH.Options.ppt_scheme|string
PUBLISH.Options.ppt_serializer|string
PUBLISH.Options.ppt_cipher|string
PUBLISH.Options.ppt_keyid|string
PUBLISH.Options.e2ee_request_key_rpc|string
---
EVENT.Details.ppt_scheme|string
EVENT.Details.ppt_serializer|string
EVENT.Details.ppt_cipher|string
EVENT.Details.ppt_keyid|string
EVENT.Details.e2ee_request_key_rpc|string
---
ERROR.Options.ppt_scheme|string
ERROR.Options.ppt_serializer|string
ERROR.Options.ppt_cipher|string
ERROR.Options.ppt_keyid|string
ERROR.Options.e2ee_request_key_rpc|string

**Message Structure**

When `Payload End-to-End Encryption` is in use, the message payload MUST be sent as one binary item within
`Arguments|list`, while `ArgumentsKw|dict` MUST be absent or empty.

Since many WAMP messages assume the possibility of simultaneous use of `Arguments|list` and `ArgumentsKw|dict`,
WAMP client implementations must package arguments into the following hash table and then serialize it and
transmit as a single element within `Arguments|list`.

{align="left"}
```
{
    "uri": "URI of called RPC or Topic published to",
    "args": Arguments|list,
    "kwargs": ArgumentsKw|dict
}
```

*Example.* Caller-to-Dealer `CALL` with encryption and key ID

{align="left"}
```
    [
        48,
        25471,
        {
            "ppt_scheme": "wamp",
            "ppt_serializer": "cbor",
            "ppt_cipher": "xsalsa20poly1305",
            "ppt_keyid": "GTtQ37XGJO2O4R8Dvx4AUo8pe61D9evIWpKGQAPdOh0=",
            "e2ee_request_key_rpc": "peer.runtime.generated.registered.rpc.Uo8pe61D9ev"
        },
        "com.myapp.secret_rpc_for_sensitive_data",
        [Payload|binary]
    ]
```

*Example.* Caller-to-Dealer `CALL` with encryption and requesting Callee to use the same encryption key for results

{align="left"}
```
    [
        48,
        25471,
        {
            "ppt_scheme": "wamp",
            "ppt_serializer": "cbor",
            "ppt_cipher": "xsalsa20poly1305",
            "e2ee_use_same_key": true,
            "e2ee_request_key_rpc": "peer.runtime.generated.registered.rpc.Uo8pe61D9ev"
        },
        "com.myapp.secret_rpc_for_sensitive_data",
        [Payload|binary]
    ]
```

*Example.* Caller-to-Dealer progressive `CALL` with encryption and key ID.

Note that nothing prevents the use of `Payload End-to-End Encryption` with other features such as,
for example, `Progressive Calls`.

{align="left"}
```
    [
        48,
        25471,
        {
            "ppt_scheme": "wamp",
            "ppt_serializer": "flatbuffers",
            "ppt_cipher": "xsalsa20poly1305",
            "ppt_keyid": "GTtQ37XGJO2O4R8Dvx4AUo8pe61D9evIWpKGQAPdOh0=",
            "progress": true,
            "e2ee_request_key_rpc": "peer.runtime.generated.registered.rpc.1D9evIWpKGQ"
        },
        "com.myapp.progressive_rpc_for_sensitive_data",
        [Payload|binary]
    ]
```

*Example.* Dealer-to-Callee `INVOCATION` with encryption, key ID and requesting Callee to use the same encryption
key for results

{align="left"}
```
    [
        68,
        35477,
        1147,
        {
            "ppt_scheme": "wamp",
            "ppt_serializer": "cbor",
            "ppt_cipher": "xsalsa20poly1305",
            "ppt_keyid": "GTtQ37XGJO2O4R8Dvx4AUo8pe61D9evIWpKGQAPdOh0=",
            "e2ee_use_same_key": true,
            "e2ee_request_key_rpc": "peer.runtime.generated.registered.rpc.7XGJO2"
        },
        [Payload|binary]
    ]
```

*Example.* Callee-to-Dealer `YIELD` with encryption and key ID

{align="left"}
```
    [
        70,
        87683,
        {
            "ppt_scheme": "wamp",
            "ppt_serializer": "flatbuffers",
            "ppt_cipher": "xsalsa20poly1305",
            "ppt_keyid": "GTtQ37XGJO2O4R8Dvx4AUo8pe61D9evNSpGMDQWdOh1=",
            "e2ee_request_key_rpc": "peer.runtime.generated.registered.rpc.GMDQW"
        },
        [Payload|binary]
    ]
```

*Example.* Callee-to-Dealer progressive `YIELD` with encryption and key ID

Nothing prevents the use of `Payload End-to-End Encryption` with other features such as, 
for example, `Progressive Call Results`.

{align="left"}
```
    [
        70,
        87683,
        {
            "ppt_scheme": "wamp",
            "ppt_serializer": "flatbuffers",
            "ppt_cipher": "xsalsa20poly1305",
            "ppt_keyid": "GTtQ37XGJO2O4R8Dvx4AUo8pe61D9evNSpGMDQWdOh1=",
            "progress": true,
            "e2ee_request_key_rpc": "peer.runtime.generated.registered.rpc.4AUo8pe61D"
        },
        [Payload|binary]
    ]
```

*Example.* Dealer-to-Caller `RESULT` with encryption and key ID

{align="left"}
```
    [
        50,
        77133,
        {
            "ppt_scheme": "wamp",
            "ppt_serializer": "flatbuffers",
            "ppt_cipher": "xsalsa20poly1305",
            "ppt_keyid": "GTtQ37XGJO2O4R8Dvx4AUo8pe61D9evNSpGMDQWdOh1=",
            "e2ee_request_key_rpc": "peer.runtime.generated.registered.rpc.37XGJO"
        },
        [Payload|binary]
    ]
```

*Example.* Dealer-to-Caller progressive `RESULT` with encryption and key ID

Nothing prevents the use of `Payload End-to-End Encryption` with other features such as, 
for example, `Progressive Call Results`.

{align="left"}
```
    [
        50,
        77133,
        {
            "ppt_scheme": "wamp",
            "ppt_serializer": "flatbuffers",
            "ppt_cipher": "xsalsa20poly1305",
            "ppt_keyid": "GTtQ37XGJO2O4R8Dvx4AUo8pe61D9evNSpGMDQWdOh1=",
            "progress": true,
            "e2ee_request_key_rpc": "peer.runtime.generated.registered.rpc.37XGJO"
        },
        [Payload|binary]
    ]
```

*Example.* Callee-to-Dealer `ERROR` with encryption and key ID

{align="left"}
```
    [
        8,
        68,
        87683,
        {
            "ppt_scheme": "wamp",
            "ppt_serializer": "cbor",
            "ppt_cipher": "xsalsa20poly1305",
            "ppt_keyid": "GTtQ37XGJO2O4R8Dvx4AUo8pe61D9evNSpGMDQWdOh1=",
            "e2ee_request_key_rpc": "peer.runtime.generated.registered.rpc.8Dvx4AUo8"
        },
        "com.myapp.invalid_revenue_year",
        [Payload|binary]
    ]
```

*Example.* Publishing event to a topic with encryption and key ID

{align="left"}
```
    [
        16,
        45677,
        {
            "ppt_scheme": "wamp",
            "ppt_serializer": "cbor",
            "ppt_cipher": "xsalsa20poly1305",
            "ppt_keyid": "GTtQ37XGJO2O4R8Dvx4AUo8pe61D9evNSpGMDQWdOh1=",
            "e2ee_request_key_rpc": "peer.runtime.generated.registered.rpc.AUo8pe"
        },
        "com.myapp.mytopic1",
        [Payload|binary]
    ]
```

*Example.* Receiving event for a topic with encryption and key ID

{align="left"}
```
    [
        36,
        5512315355,
        4429313566,
        {
            "ppt_scheme": "wamp",
            "ppt_serializer": "flatbuffers",
            "ppt_cipher": "xsalsa20poly1305",
            "ppt_keyid": "GTtQ37XGJO2O4R8Dvx4AUo8pe61D9evNSpGMDQWdOh1=",
            "e2ee_request_key_rpc": "peer.runtime.generated.registered.rpc.GJO2O4R"
        },
        [Payload|binary]
    ]
```
