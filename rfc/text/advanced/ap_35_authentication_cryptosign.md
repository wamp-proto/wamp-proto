## Cryptosign-based Authentication {#cryptosignauth}

*WAMP-Cryptosign* is a WAMP authentication method based on
*public-private key cryptography*. Specifically, it is based on [Ed25519](https://ed25519.cr.yp.to/) digital signatures as described in [@!RFC8032].

**Ed25519** is an [elliptic curve signature scheme](https://ed25519.cr.yp.to/ed25519-20110926.pdf) that instantiates
the Edwards-curve Digital Signature Algorithm (EdDSA) with
elliptic curve parameters which are equivalent to [Curve25519](https://cr.yp.to/ecdh.html).

**Curve25519** is a [SafeCurve](https://safecurves.cr.yp.to/), which means
it is easy to implement securely and avoid security issues resulting from common implementation challenges and bugs.

Ed25519 is intended to operate at around the 128-bit security level, and there are robust native implementations available as open-source, e.g. [libsodium](https://github.com/jedisct1/libsodium), which can be used from script languages, e.g. [PyNaCl](https://github.com/pyca/pynacl).
