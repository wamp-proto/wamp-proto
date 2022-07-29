## Payload Passthru Mode {#payload-passthru-mode}

In some situations, you may want to reduce the access the router has to the information users transmit, or
payload data is presented in some specific format that can not be simply recognized by WAMP router serializer.

These are example use cases:
* Using WAMP alongside with gateways to other technologies like MQTT Brokers or AMQP Queues. So actual payload 
  is for example mqtt message that should be simply delivered to wamp topic as is. 
* Sensitive user data that should be delivered to target *Callee* without any possibility to unveil it during delivery.

This needs can be covered with `Payload Passthru Mode` feature. This feature allows:

* Specifying additional attributes during `CALL`, `PUBLISH`, `EVENT`, `YIELD`, `RESULT` messages 
  to signal *Router* to skip payload inspection.
* Encrypting and decrypting payload with crypto algorithms.
* Providing additional information about payload format and type.

**Feature Announcement**

Support for this advanced feature MUST be announced by *Callers* (`role := "caller"`), *Callees* (`role := "callee"`),
*Dealers* (`role := "dealer"`), *Publishers* (`role := "publisher"`), *Subscribers* (`role := "subscriber"`) 
and *Brokers* (`role := "broker"`) via

{align="left"}
HELLO.Details.roles.<role>.features.payload_passthru_mode|bool := true

Payload Passthru Mode can work only if all three nodes (*Caller*, *Dealer*, *Callee* or
*Publisher*, *Broker*, *Subscriber*) support and announced this feature.

Cases where *Caller* sends `CALL` message with `payload passthru` without announcing it during `HELLO`
handshake MUST be treated as *PROTOCOL ERRORS* and underlying WAMP connections must be aborted with
`wamp.error.protocol_violation` error reason.

Cases where *Caller* sends `CALL` message with `payload passthru` to *Dealer*, that did not announce
`payload passthru` support during `WELCOME` handshake MUST be treated as *PROTOCOL ERRORS* and underlying WAMP
connections must be aborted with `wamp.error.protocol_violation` error reason.

Cases where *Caller* sends `CALL` message with `payload passthru` to the *Dealer* that supports this feature,
which then must be routed to the *Callee* which doesn't support `payload passthru` MUST be treated as 
*APPLICATION ERRORS* and *Dealer* MUST respond to *Caller* with `wamp.error.feature_not_supported` error message.

Cases where *Publisher* sends `PUBLISH` message with `payload passthru` without announcing it during `HELLO`
handshake MUST be treated as *PROTOCOL ERRORS* and underlying WAMP connections must be aborted with
`wamp.error.protocol_violation` error reason.

Cases where *Publisher* sends `PUBLISH` message with `payload passthru` to *Broker*, that did not announce
`payload passthru` support during `WELCOME` handshake MUST be treated as *PROTOCOL ERRORS* and underlying WAMP
connections must be aborted with `wamp.error.protocol_violation` error reason.

Cases where *Publisher* sends `PUBLISH` message with `payload passthru` to the *Broker* that supports this feature,
which then must be routed to the *Subscriber* which doesn't support `payload passthru` cannot be recognized at the
protocol level due to asynchronous message processing and must be covered at *Subscriber* side.

Cases where *Callee* sends `YIELD` message with `payload passthru` without announcing it during `HELLO`
handshake MUST be treated as *PROTOCOL ERRORS* and underlying WAMP connections must be aborted with
`wamp.error.protocol_violation` error reason.

Cases where *Callee* sends `YIELD` message with `payload passthru` to *Dealer*, that did not announce
`payload passthru` support during `WELCOME` handshake MUST be treated as *PROTOCOL ERRORS* and underlying WAMP
connections must be aborted with `wamp.error.protocol_violation` error reason.

Cases where *Callee* sends `YIELD` message with `payload passthru` to the *Dealer* that supports this feature,
which then must be routed to the *Caller* which doesn't support `payload passthru` MUST be treated as
*APPLICATION ERRORS* and *Dealer* MUST respond to *Callee* with `wamp.error.feature_not_supported` error message.

**Message attributes**

For this feature to be in use, `CALL`, `PUBLISH` and `YIELD` messages options are extended with additional attributes. 
This attributes then are passed as is within `INVOCATION`, `EVENT` and `RESULT` messages respectively and to `ERROR`
message in case of failures.

{align="left"}
        CALL.Options.ppt_serializer|string
        CALL.Options.ppt_cipher|string
        CALL.Options.ppt_scheme|string
        CALL.Options.ppt_keyid|string
        ---
        INVOCATION.Details.ppt_serializer|string
        INVOCATION.Details.ppt_cipher|string
        INVOCATION.Details.ppt_scheme|string
        INVOCATION.Details.ppt_keyid|string
        ---
        YIELD.Options.ppt_serializer|string
        YIELD.Options.ppt_cipher|string
        YIELD.Options.ppt_scheme|string
        YIELD.Options.ppt_keyid|string
        ---
        RESULT.Details.ppt_serializer|string
        RESULT.Details.ppt_cipher|string
        RESULT.Details.ppt_scheme|string
        RESULT.Details.ppt_keyid|string
        ---
        ERROR.Details.ppt_serializer|string
        ERROR.Details.ppt_cipher|string
        ERROR.Details.ppt_scheme|string
        ERROR.Details.ppt_keyid|string

{align="left"}
        PUBLISH.Options.ppt_serializer|string
        PUBLISH.Options.ppt_cipher|string
        PUBLISH.Options.ppt_scheme|string
        PUBLISH.Options.ppt_keyid|string
        ---
        EVENT.Details.ppt_serializer|string
        EVENT.Details.ppt_cipher|string
        EVENT.Details.ppt_scheme|string
        EVENT.Details.ppt_keyid|string
        ---
        ERROR.Options.ppt_serializer|string
        ERROR.Options.ppt_cipher|string
        ERROR.Options.ppt_scheme|string
        ERROR.Options.ppt_keyid|string


**ppt_serializer attribute**

`ppt_serializer` attribute is required. It specifies what serializer was used to build up payload object.
It can be `mqtt`, `amqp`, `stomp` value just to inform that coming data is from related technologies or ordinary 
`json`, `msgpack`, `cbor`, `flatbuffers` data serializers. *Router* understands that `Payload Passthru Mode` is in use
by checking the existence and non-empty value of this attribute in `CALL`, `PUBLISH` and `YIELD` messages options.

**ppt_cipher attribute**

`ppt_cipher` attribute is optional. It is required if payload is encrypted. This attribute specifies cryptographic
algorithm that was used to encrypt payload. It can be `xsalsa20poly1305`, `aes256gcm` for now.

**ppt_scheme attribute**

`ppt_scheme` stands for Key Management Schema. It is optional string attribute. This attribute can contain name or
identifier of key management provider which is known to target peer, so it can be used to obtain information
about encryption keys.

**ppt_keyid attribute**

`ppt_keyid` attribute is optional. This attribute can contain encryption key id that was used to encrypt payload.
`ppt_keyid` attribute is always a type of string. The value can be a hex-encoded string, uri, DNS name, 
Ethereum address, UUID identifier - any meaningful value by which target peer can choose private key 
without guessing. Format of the value may depend on `ppt_scheme` attribute.

**Message structure**

With `Payload Passthru Mode` in use message payload MUST BE sent as one binary item inside 
`Arguments|list`, while `ArgumentsKw|dict` MUST BE missing or empty.

*Example.* Caller-to-Dealer `CALL` with encryption and key ID

{align="left"}
```json
    [
        48,
        25471,
        {
            "ppt_serializer": "json",
            "ppt_cipher": "xsalsa20poly1305",
            "ppt_keyid": "GTtQ37XGJO2O4R8Dvx4AUo8pe61D9evIWpKGQAPdOh0="
        },
        "com.myapp.secret_rpc_for_sensitive_data",
        [Payload|binary]
    ]
```

*Example.* Caller-to-Dealer progressive `CALL` with encryption and key ID.

Nothing prevents to use `Payload Passthru Mode` with other features, for example `Progressive Calls`

{align="left"}
```json
    [
        48,
        25471,
        {
            "ppt_serializer": "json",
            "ppt_cipher": "xsalsa20poly1305",
            "ppt_keyid": "GTtQ37XGJO2O4R8Dvx4AUo8pe61D9evIWpKGQAPdOh0=",
            "progress": true
        },
        "com.myapp.progressive_rpc_for_sensitive_data",
        [Payload|binary]
    ]
```

*Example.* Caller-to-Dealer `CALL` with mqtt payload

{align="left"}
```json
    [
        48,
        25471,
        {
            "ppt_serializer": "mqtt"
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
            "ppt_serializer": "json",
            "ppt_cipher": "xsalsa20poly1305",
            "ppt_keyid": "GTtQ37XGJO2O4R8Dvx4AUo8pe61D9evIWpKGQAPdOh0="
        },
        [Payload|binary]
    ]
```

*Example.* Dealer-to-Callee `INVOCATION` with mqtt payload

{align="left"}
```json
    [
        68,
        35479,
        3344,
        {
            "ppt_serializer": "mqtt"
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
            "ppt_serializer": "flatbuffers",
            "ppt_cipher": "xsalsa20poly1305",
            "ppt_keyid": "GTtQ37XGJO2O4R8Dvx4AUo8pe61D9evNSpGMDQWdOh1="
        },
        [Payload|binary]
    ]
```

*Example.* Callee-to-Dealer progressive `YIELD` with encryption and key ID

Nothing prevents to use `Payload Passthru Mode` with other features, for example `Progressive Call Results`

{align="left"}
```json
    [
        70,
        87683,
        {
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
            "ppt_serializer": "flatbuffers",
            "ppt_cipher": "xsalsa20poly1305",
            "ppt_keyid": "GTtQ37XGJO2O4R8Dvx4AUo8pe61D9evNSpGMDQWdOh1="
        },
        [Payload|binary]
    ]
```

*Example.* Dealer-to-Caller progressive `RESULT` with encryption and key ID

Nothing prevents to use `Payload Passthru Mode` with other features, for example `Progressive Call Results`

{align="left"}
```json
    [
        50,
        77133,
        {
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
            "ppt_serializer": "json",
            "ppt_cipher": "xsalsa20poly1305",
            "ppt_keyid": "GTtQ37XGJO2O4R8Dvx4AUo8pe61D9evNSpGMDQWdOh1="
        },
        [Payload|binary]
    ]
```

**About supported serializers and cryptographic cyphers**

WAMP works as infrastructure for delivering messages between peers. Regardless of what encryption algorithm 
and serializer were chosen for `Payload Passthru Mode`, *Router* will not inspect and analyze related encryption 
message options and payload. It is up to an application side code responsibility to use serializers and 
cyphers known to every peer involved into message processing.
