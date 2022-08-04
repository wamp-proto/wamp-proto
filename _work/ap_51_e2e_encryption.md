
ppt_scheme      = "wamp.eth"
ppt_serializer  = "cbor" | "flatbuffers"
ppt_compressor  = "lzss" | "brotli" | null
ppt_cipher      = "xsalsa20poly1305" | "aes256gcm"
ppt_keyid       = "0x..."

https://lib.rs/crates/brotli
https://lib.rs/crates/lzss



Quote:
contains set of PCR values (measurement) signed by the TPM

PCRs:
- Platform Firmware
- EFI
- Bootloader (2-stage)
- OS kernel
- OS kernel command line
- Docker daemon
- Docker image


NO (!): Attestation Certificate
Endorsement Certificate
Manufactorer Certificate


---------------


Announcement: The End of the 3rd Round - the First PQC Algorithms to be Standardized

The primary algorithms NIST recommends be implemented for most use cases are CRYSTALS-KYBER (key-establishment) and CRYSTALS-Dilithium (digital signatures).

Public-Key Encryption/KEMs: CRYSTALS-KYBER
Digital Signatures: CRYSTALS-Dilithium

https://groups.google.com/a/list.nist.gov/g/pqc-forum/c/G0DoD7lkGPk


---------------


Who is "the user" of your system, service or application?

Here are a couple of user categories by **intent**.

Paying users include:

1. Well behaved (active, normal and regular users)
2. Explorative (power users)
3. Ignorant (lazy and careless users)
4. Dormant (sleepers)

Non-paying user (might) include:

5. Opportunistic (freeriders)
6. Competitive (copy cats)
7. Malicious (criminals, organized crime)
8. Advanced persistent threat (nations, authorities, regulators, agencies)

For which user categories do you plan, design and manage for?

--------------

* authenticity
* confidentiality
* integrity
* availability

* privacy
* non-repudiability
* plausible-deniability

--------------

XSalsa20Poly1305 (a.k.a. NaCl crypto_secretbox) is an authenticated encryption cipher amenable
to fast, constant-time implementations in software, based on the Salsa20 stream cipher (with
XSalsa20 192-bit nonce extension) and the Poly1305 universal hash function, which acts as a
message authentication code.

This algorithm has largely been replaced by the newer ChaCha20Poly1305 (and the associated
XChaCha20Poly1305) AEAD ciphers (RFC 8439), but is useful for interoperability with legacy
NaCl-based protocols.

https://docs.rs/xsalsa20poly1305/latest/xsalsa20poly1305/


For most applications it should be sufficient to bind against PCR 7 (and possibly PCR 14, if
shim/MOK is desired), as this includes measurements of the trusted certificates (and possibly
hashes) that are used to validate all components of the boot process up to and including the
OS kernel. In order to simplify firmware and OS version updates it's typically not advisable
to include PCRs such as 0 and 2 in the binding of the enrollment, since the program code they
cover should already be protected indirectly through the certificates measured into PCR 7.
Validation through these certificates is typically preferable over validation through direct
measurements as it is less brittle in context of OS/firmware updates: the measurements will
change on every update, but code signatures likely will validate against pre-existing certificates.

https://www.freedesktop.org/software/systemd/man/systemd-cryptenroll.html#--tpm2-pcrs=PCR

