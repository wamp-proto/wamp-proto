## Payload End-to-End Encryption

*Payload End-to-End Encryption* ("PE3") is a feature in the *WAMP Advanced Profile* that enables an **enhanced security model** for WAMP based systems which isolates WAMP endpoints (e.g. *Callers* and *Callees*) from routers. It provides Authenticity, Confidentiality and Integrity of data not only between WAMP endpoints and routers versus outside third-parties, but also versus the WAMP router nodes themself, transporting the application payload between WAMP endpoints.

**Enhanced Security Model**

The security model of *Payload End-to-End Encryption* provides enhanced **Authenticity**, **Confidentiality** and **Integrity** levels, namely end-to-end between WAMP endpoints, rather than only for a WAMP endpoint-to-router link, while **Availability** remains independent and at the original level. Further new guarantees include

* **Privacy**
* **Plausible-deniability**
* **Non-repudiability**

of the application payload versus the *Router*. Note that this only applies to the payload, not the metadata such as the URI, which might itself e.g. reveal information to a router. Of course the metadata is necessary for a WAMP router to read, as it needs to take correct WAMP routing decisions based on WAMP message metadata.

This is enabled by encrypting the application payload contained in WAMP messages (e.g. `CALL.args|list`) with keys only accessible to authorized WAMP endpoints. Routers transporting traffic between WAMP endpoints can only read and process the WAMP message and e.g. take routing decisions based on the WAMP URI in the message, but can not decrypt and read the contained application payload.

Note that payload end-to-end encryption is different from link-level transport encryption, e.g. when a WAMP endpoint uses TLS to connect to its uplink router. In this case, the WAMP message, and the (plaintext) application payload embedded in the message can not be read by third parties (anyone outside the TLS connection), but it can be read by the router.

**How it works**

symmetric payload encryption
decentralized trust establishment
payload encryption key distribution

1. serialize
2. (compress)
3. encrypt

uses Payload Passthru

mutual trust problem: decentralized on-chain certificates
remote trust problem: e2ee and remote attestation

1) standalone trustroots
2) on-chain trustroots

1) centralized trust model
2) decentralized trust model

management of the Operator-CA to Realm-CA relationships
