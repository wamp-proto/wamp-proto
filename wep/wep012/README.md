# WEP012 - Hardware security module support for WAMP-cryptosign

A hardware security module (HSM) is a dedicated crypto processor that is specifically designed for the protection of the crypto key lifecycle. Hardware security modules act as trust anchors that protect the cryptographic infrastructure by securely managing, processing, and storing cryptographic keys inside a hardened, tamper-resistant device.

## Goal

Use the HW-based crypto for Ed25519 signing in WAMP-cryptosign authentication with support for the following chips:

* [NXP SE050Cx](https://www.nxp.com/products/security-and-authentication/authentication/edgelock-se050-plug-trust-secure-element-family-enhanced-iot-security-with-maximum-flexibility:SE050)
* [NXP SE051Cx](https://www.nxp.com/products/security-and-authentication/authentication/edgelock-se051-proven-easy-to-use-iot-security-solution-with-support-for-updatability-and-custom-applets:SE051)

## Result

AutobahnPython can be installed with support for NXP SE050Cx/SE051Cx in WAMP-cryptosign authentication.
