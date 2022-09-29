## Payload End-to-End Encryption

*WAMP End-to-End Encryption* ("WAMP-E2EE") is a feature in the *WAMP Advanced Profile* that enables an
**enhanced security model** for WAMP based systems which isolates WAMP endpoints (e.g. *Callers* and *Callees*)
from routers. It provides enhanced application payload

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
3. [Trust Management](#trustmgmt)
4. [Key Distribution](#keydist)


#### Payload Encryption {#payloadencr}

1. payload serialization
2. optional compression
3. symmetric encryption with XSalsa20Poly1305 (a.k.a. [NaCl crypto_secretbox](https://nacl.cr.yp.to/secretbox.html))

XSalsa20Poly1305 is an [authenticated encryption](https://en.wikipedia.org/wiki/Authenticated_encryption) cipher
based on
the [XSalsa20](https://en.wikipedia.org/wiki/Salsa20) [stream cipher](https://en.wikipedia.org/wiki/Stream_cipher)
and the [Poly1305](https://en.wikipedia.org/wiki/Poly1305) hash function, which acts as a message authentication code.

The secret encryption keys for XSalsa20Poly1305 are 32 octets in length, and message nonces are 24 octets.

#### Payload Transport {#payloadtnsp}

transport using WAMP AP [Payload Passthru Mode](#payload-passthru-mode)

#### Trust Management {#trustmgmt}

[trust on first use](https://en.wikipedia.org/wiki/Trust_on_first_use)

management of the Operator-CA to Realm-CA relationships

* mutual trust problem: decentralized on-chain certificates
* remote trust problem: e2ee and remote attestation

1) standalone trustroots / centralized trust model
2) on-chain trustroots / decentralized trust model

#### Key Distribution {#keydist}

Write me.
