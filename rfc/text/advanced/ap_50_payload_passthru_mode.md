## Payload Passthru Mode {#payload-passthru-mode}

In some situations, you may want to reduce the access the router has to the information users transmit, or
payload data is presented in some specific format that can not be simply recognized by WAMP router serializer.

Here are some use cases:

* Using WAMP via gateways to other technologies like MQTT Brokers or AMQP Queues. So the actual payload
  is, for example, MQTT message that should be delivered to a WAMP topic as is.
* Sensitive user data that should be delivered to a target *Callee* without any possibility of unveiling it in transit.

The above use cases can be fulfilled with the `Payload Passthru Mode` feature. This feature allows:

* Specifying additional attributes within `CALL`, `PUBLISH`, `EVENT`, `YIELD`, `RESULT` messages
  to signal the *Router* to skip payload inspection/conversion.
* The forwarding of these additional attributes via `INVOCATION` and `ERROR` messages
* Encrypting and decrypting payload using cryptographic algorithms.
* Providing additional information about payload format and type.

**Feature Announcement**

Support for this advanced feature MUST be announced by *Callers* (`role := "caller"`), *Callees* (`role := "callee"`),
*Dealers* (`role := "dealer"`), *Publishers* (`role := "publisher"`), *Subscribers* (`role := "subscriber"`)
and *Brokers* (`role := "broker"`) via

{align="left"}
HELLO.Details.roles.<role>.features.payload_passthru_mode|bool := true

Payload Passthru Mode can work only if all three nodes (*Caller*, *Dealer*, *Callee* or
*Publisher*, *Broker*, *Subscriber*) support and announced this feature.

Cases where a *Caller* sends a `CALL` message with `payload passthru` without announcing it during the `HELLO`
handshake MUST be treated as *PROTOCOL ERRORS* and underlying WAMP connections must be aborted with
the `wamp.error.protocol_violation` error reason.

Cases where a *Caller* sends a `CALL` message with `payload passthru` to a *Dealer*, the latter not announcing
`payload passthru` support during `WELCOME` handshake MUST be treated as *PROTOCOL ERRORS* and the underlying WAMP
connections must be aborted with the `wamp.error.protocol_violation` error reason.

Cases where a *Caller* sends a `CALL` message with `payload passthru` to a *Dealer* that supports this feature,
which then must be routed to a *Callee* which doesn't support `payload passthru`, MUST be treated as
*APPLICATION ERRORS* and the *Dealer* MUST respond to the *Caller* with a `wamp.error.feature_not_supported`
error message.

Cases where a *Publisher* sends a `PUBLISH` message with `payload passthru`, without announcing it during `HELLO`
handshake, MUST be treated as *PROTOCOL ERRORS* and the underlying WAMP connections must be aborted with
the `wamp.error.protocol_violation` error reason.

Cases where a *Publisher* sends a `PUBLISH` message with `payload passthru` to a *Broker*, with the latter not
announcing `payload passthru` support during the `WELCOME` handshake, MUST be treated as *PROTOCOL ERRORS* and
the underlying WAMP connections must be aborted with the `wamp.error.protocol_violation` error reason.

Cases where a *Publisher* sends a `PUBLISH` message with `payload passthru` to a *Broker* that supports this feature,
which then must be routed to a *Subscriber* which doesn't support `payload passthru`, cannot be recognized at the
protocol level due to asynchronous message processing and must be covered at the *Subscriber* side.

Cases where a *Callee* sends a `YIELD` message with `payload passthru` without announcing it during the `HELLO`
handshake MUST be treated as *PROTOCOL ERRORS* and the underlying WAMP connections must be aborted with
the `wamp.error.protocol_violation` error reason.

Cases where a *Callee* sends a `YIELD` message with `payload passthru` to a *Dealer*, with the latter not announcing
`payload passthru` support during the `WELCOME` handshake, MUST be treated as *PROTOCOL ERRORS* and the
underlying WAMP connections must be aborted with the `wamp.error.protocol_violation` error reason.

Cases where a *Callee* sends a `YIELD` message with `payload passthru` to a *Dealer* that supports this feature,
which then must be routed to the *Caller* which doesn't support `payload passthru`, MUST be treated as
*APPLICATION ERRORS* and the *Dealer* MUST respond to the *Callee* with a `wamp.error.feature_not_supported`
error message.

**Message Attributes**

To use payload passthru mode, the options for `CALL`, `PUBLISH` and `YIELD` messages MUST be extended with additional
attributes. These additional attributes must be forwarded via `INVOCATION`, `EVENT` and `RESULT` messages, respectively,
as well as `ERROR` messages in the case of failures.

{align="left"}
        CALL.Options.ppt_scheme|string
        CALL.Options.ppt_serializer|string
        CALL.Options.ppt_cipher|string
        CALL.Options.ppt_keyid|string
        ---
        INVOCATION.Details.ppt_scheme|string
        INVOCATION.Details.ppt_serializer|string
        INVOCATION.Details.ppt_cipher|string
        INVOCATION.Details.ppt_keyid|string
        ---
        YIELD.Options.ppt_scheme|string
        YIELD.Options.ppt_serializer|string
        YIELD.Options.ppt_cipher|string
        YIELD.Options.ppt_keyid|string
        ---
        RESULT.Details.ppt_scheme|string
        RESULT.Details.ppt_serializer|string
        RESULT.Details.ppt_cipher|string
        RESULT.Details.ppt_keyid|string
        ---
        ERROR.Details.ppt_scheme|string
        ERROR.Details.ppt_serializer|string
        ERROR.Details.ppt_cipher|string
        ERROR.Details.ppt_keyid|string

{align="left"}
        PUBLISH.Options.ppt_scheme|string
        PUBLISH.Options.ppt_serializer|string
        PUBLISH.Options.ppt_cipher|string
        PUBLISH.Options.ppt_keyid|string
        ---
        EVENT.Details.ppt_scheme|string
        EVENT.Details.ppt_serializer|string
        EVENT.Details.ppt_cipher|string
        EVENT.Details.ppt_keyid|string
        ---
        ERROR.Options.ppt_scheme|string
        ERROR.Options.ppt_serializer|string
        ERROR.Options.ppt_cipher|string
        ERROR.Options.ppt_keyid|string


**ppt_scheme Attribute**

The `ppt_scheme` identifies the Payload Schema. It is a required string attribute. For End-2-End Encryption flow
this attribute can contain the name or identifier of a key management provider that is known to the target peer,
so it can be used with help of additional `ppt_*` attributes to obtain information about encryption keys.
For gateways and external schemas this can contain the name of related technology. The one predefined is `mqtt`.
Others may be introduced later. A *Router* can recognize that `Payload Passthru Mode` is in use by checking
the existence and non-empty value of this attribute within the options of `CALL`, `PUBLISH` and `YIELD` messages.

**ppt_serializer Attribute**

The `ppt_serializer` attribute is optional. It specifies what serializer was used to encode the payload.
It can be a `native` value to indicate that the incoming data is tunneling through other technologies
specified by the `ppt_scheme`, or it can be ordinary `json`, `msgpack`, `cbor`, `flatbuffers` data serializers.
For some predefined `ppt_scheme` schemas this option may be omitted as schema defines the concrete serializer.
See predefined schemas below.

**ppt_cipher Attribute**

The `ppt_cipher` attribute is optional. It is required if the payload is encrypted. This attribute specifies the
cryptographic algorithm that was used to encrypt the payload. It can be `xsalsa20poly1305`, `aes256gcm` for now.

**ppt_keyid Attribute**

The `ppt_keyid` attribute is optional. This attribute can contain the encryption key id that was used to encrypt
the payload. The `ppt_keyid` attribute is a string type. The value can be a hex-encoded string, URI, DNS name,
Ethereum address, UUID identifier - any meaningful value which allows the target peer to choose a private key
without guessing. The format of the value may depend on the `ppt_scheme` attribute.

**ppt_ Predefined Schemes**

**MQTT Predefined Scheme**

{align="left"}

| Attribute      | Required? | Value                        |
|----------------|-----------|------------------------------|
| ppt_scheme     | Y         | mqtt                         |
| ppt_serializer | N*        | native, json, msgpack, cbor  |
| ppt_cipher     | N         | -                            |
| ppt_keyid      | N         | -                            |

*: If `ppt_serializer` is not provided then it is assuming as `native`. So no additional serialization
will be applied to payload and payload will be serialized within WAMP message with session serializer.

**End-to-End Encryption Predefined Scheme**

For `End-to-End Encryption` flow both peers must support chosen `ppt_serializer` regardless of their own
session serializer.

{align="left"}

| Attribute      | Required? | Value                       |
|----------------|-----------|-----------------------------|
| ppt_scheme     | Y         | wamp                        |
| ppt_serializer | Y         | cbor, flatbuffers           |
| ppt_cipher     | N         | xsalsa20poly1305, aes256gcm |
| ppt_keyid      | N         | *                           |

*: The least significant 20 bytes (160 bits) of the SHA256 of the public key (32 bytes) of the data encryption key,
as a hex-encoded string with prefix `0x` and either uppercase/lowercase alphabetic characters, encoding a
checksum according to EIP55.

**Custom Scheme Example**

{align="left"}

| Attribute      | Required? | Value    |
|----------------|-----------|----------|
| ppt_scheme     | Y         | x_my_ppt |
| ppt_serializer | N         | custom   |
| ppt_cipher     | N         | custom   |
| ppt_keyid      | N         | custom   |


When `Payload Passthru Mode` is used for gateways to other technologies, such as MQTT Brokers, then
the `ppt_serializer` attribute may be set to the `native` value. This means that the payload is not to be modified
by WAMP peers, nor serialized in any manner, and is delivered as-is from the originating peer. Another possible case
is when the `ppt_serializer` attribute is set to any valid serializer, for example `msgpack`. In this case the
originating WAMP client peer first applies `ppt_serializer` to serialize the payload (without encryption), then
the resulting binary payload is embedded in the WAMP message, the latter having possibly a different serializer
depending on the one chosen during WAMP Session establishment.

**Important Note Regarding JSON Serialization**

With `Payload Passthru Mode`, payloads are treated as binary. To send these binary payloads, the WAMP session
serializer MUST support byte arrays. Most serialization formats known to WAMP support byte arrays, but JSON does
not support them natively. To use `Payload Passthru Mode` with a JSON serializer, WAMP peers MUST perform the special
[Binary serialization in JSON](#binary-support-in-json). This conversion may have unacceptable overhead, so it is
generally advised to use WAMP session serializers with native byte array support, for example,
`MessagePack`, `CBOR`, or `FlatBuffers`.

**Message Structure**

When `Payload Passthru Mode` is in use, the message payload MUST be sent as one binary item within
`Arguments|list`, while `ArgumentsKw|dict` MUST be absent or empty.

Since many WAMP messages assume the possibility of simultaneous use of `Arguments|list` and `ArgumentsKw|dict`,
WAMP client implementations must package arguments into the following hash table and then serialize it and
transmit as a single element within `Arguments|list`.

{align="left"}
```json
{
    "args": Arguments|list,
    "kwargs": ArgumentsKw|dict
}
```

This will allow maintaining a single interface for client applications, regardless of whether the
```Payload Passthru Mode``` mode, or especially `Payload End-to-End Encryption` which is built on top of
`Payload End-to-End Encryption` is used or not.

*Example.* Caller-to-Dealer `CALL` with encryption and key ID

{align="left"}
```json
    [
        48,
        25471,
        {
            "ppt_scheme": "wamp",
            "ppt_serializer": "cbor",
            "ppt_cipher": "xsalsa20poly1305",
            "ppt_keyid": "GTtQ37XGJO2O4R8Dvx4AUo8pe61D9evIWpKGQAPdOh0="
        },
        "com.myapp.secret_rpc_for_sensitive_data",
        [Payload|binary]
    ]
```

*Example.* Caller-to-Dealer progressive `CALL` with encryption and key ID.

Note that nothing prevents the use of `Payload Passthru Mode` with other features such as,
for example, `Progressive Call Results` or `Progressive Call Invocations`.

{align="left"}
```json
    [
        48,
        25471,
        {
            "ppt_scheme": "wamp",
            "ppt_serializer": "flatbuffers",
            "ppt_cipher": "xsalsa20poly1305",
            "ppt_keyid": "GTtQ37XGJO2O4R8Dvx4AUo8pe61D9evIWpKGQAPdOh0=",
            "progress": true
        },
        "com.myapp.progressive_rpc_for_sensitive_data",
        [Payload|binary]
    ]
```

*Example.* Caller-to-Dealer `CALL` with MQTT payload. Specifying `"ppt_serializer": "native"` means that
the original MQTT message payload is passed as WAMP payload message as is, without any transcoding.

{align="left"}
```json
    [
        48,
        25471,
        {
            "ppt_scheme": "mqtt",
            "ppt_serializer": "native"
        },
        "com.myapp.mqtt_processing",
        [Payload|binary]
    ]
```

*Example.* Caller-to-Dealer `CALL` with MQTT payload. Specifying `"ppt_scheme": "mqtt"` simply indicates that
the original source of payload data is received from a related system. Specifying `"ppt_serializer": "json"`
means that the original MQTT message payload was parsed and encoded with the `json` serializer before
embedding it into WAMP message.

{align="left"}
```json
    [
        48,
        25471,
        {
            "ppt_scheme": "mqtt",
            "ppt_serializer": "json"
        },
        "com.myapp.mqtt_processing",
        [Payload|binary]
    ]
```

*Example.* Dealer-to-Callee `INVOCATION` with encryption and key ID

{align="left"}
```json
    [
        68,
        35477,
        1147,
        {
            "ppt_scheme": "wamp",
            "ppt_serializer": "cbor",
            "ppt_cipher": "xsalsa20poly1305",
            "ppt_keyid": "GTtQ37XGJO2O4R8Dvx4AUo8pe61D9evIWpKGQAPdOh0="
        },
        [Payload|binary]
    ]
```

*Example.* Dealer-to-Callee `INVOCATION` with MQTT payload

{align="left"}
```json
    [
        68,
        35479,
        3344,
        {
            "ppt_scheme": "mqtt",
            "ppt_serializer": "native"
        },
        [Payload|binary]
    ]
```

*Example.* Callee-to-Dealer `YIELD` with encryption and key ID

{align="left"}
```json
    [
        70,
        87683,
        {
            "ppt_scheme": "wamp",
            "ppt_serializer": "flatbuffers",
            "ppt_cipher": "xsalsa20poly1305",
            "ppt_keyid": "GTtQ37XGJO2O4R8Dvx4AUo8pe61D9evNSpGMDQWdOh1="
        },
        [Payload|binary]
    ]
```

*Example.* Callee-to-Dealer progressive `YIELD` with encryption and key ID

Nothing prevents the use of `Payload Passthru Mode` with other features such as, for example, `Progressive Call Results`.

{align="left"}
```json
    [
        70,
        87683,
        {
            "ppt_scheme": "wamp",
            "ppt_serializer": "flatbuffers",
            "ppt_cipher": "xsalsa20poly1305",
            "ppt_keyid": "GTtQ37XGJO2O4R8Dvx4AUo8pe61D9evNSpGMDQWdOh1=",
            "progress": true
        },
        [Payload|binary]
    ]
```

*Example.* Dealer-to-Caller `RESULT` with encryption and key ID

{align="left"}
```json
    [
        50,
        77133,
        {
            "ppt_scheme": "wamp",
            "ppt_serializer": "flatbuffers",
            "ppt_cipher": "xsalsa20poly1305",
            "ppt_keyid": "GTtQ37XGJO2O4R8Dvx4AUo8pe61D9evNSpGMDQWdOh1="
        },
        [Payload|binary]
    ]
```

*Example.* Dealer-to-Caller progressive `RESULT` with encryption and key ID

Nothing prevents the use of `Payload Passthru Mode` with other features such as, for example, `Progressive Call Results`.

{align="left"}
```json
    [
        50,
        77133,
        {
            "ppt_scheme": "wamp",
            "ppt_serializer": "flatbuffers",
            "ppt_cipher": "xsalsa20poly1305",
            "ppt_keyid": "GTtQ37XGJO2O4R8Dvx4AUo8pe61D9evNSpGMDQWdOh1=",
            "progress": true
        },
        [Payload|binary]
    ]
```

*Example.* Callee-to-Dealer `ERROR` with encryption and key ID

{align="left"}
```json
    [
        8,
        68,
        87683,
        {
            "ppt_scheme": "wamp",
            "ppt_serializer": "cbor",
            "ppt_cipher": "xsalsa20poly1305",
            "ppt_keyid": "GTtQ37XGJO2O4R8Dvx4AUo8pe61D9evNSpGMDQWdOh1="
        },
        "com.myapp.invalid_revenue_year",
        [Payload|binary]
    ]
```

*Example.* Publishing event to a topic with encryption and key ID

{align="left"}
```json
    [
        16,
        45677,
        {
            "ppt_scheme": "wamp",
            "ppt_serializer": "cbor",
            "ppt_cipher": "xsalsa20poly1305",
            "ppt_keyid": "GTtQ37XGJO2O4R8Dvx4AUo8pe61D9evNSpGMDQWdOh1="
        },
        "com.myapp.mytopic1",
        [Payload|binary]
    ]
```

*Example.* Receiving event for a topic with encryption and key ID

{align="left"}
```json
    [
        36,
        5512315355,
        4429313566,
        {
            "ppt_scheme": "wamp",
            "ppt_serializer": "flatbuffers",
            "ppt_cipher": "xsalsa20poly1305",
            "ppt_keyid": "GTtQ37XGJO2O4R8Dvx4AUo8pe61D9evNSpGMDQWdOh1="
        },
        [Payload|binary]
    ]
```

**About Supported Serializers and Cryptographic Ciphers**

WAMP serves as infrastructure for delivering messages between peers. Regardless of what encryption algorithm
and serializer were chosen for `Payload Passthru Mode`, a *Router* shall not inspect and analyze the `ppt_` options
and payload of encrypted messages. The application is responsible for choosing serializers and
ciphers known to every peer involved in message processing.
