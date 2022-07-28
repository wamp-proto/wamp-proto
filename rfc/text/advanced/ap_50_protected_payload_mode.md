## Protected Payload Mode

In some situations, you may want to reduce the access the router has to the information users transmit, or
payload data is presented in some specific format that can not be simply recognized by WAMP router serializer.

These are example use cases:
* Using WAMP alongside with gateways to other technologies like MQTT Brokers or AMQP Queues. So actual payload 
  is for example mqtt message that should be simply delivered to wamp topic as is. 
* Sensitive user data that should be delivered to target *Callee* without any possibility to unveil it during delivery.

This needs can be covered with `Protected Payload Mode` feature. This feature allows:

* Specifying additional attributes during `CALL`, `PUBLISH`, `EVENT`, `YIELD`, `RESULT` messages 
  to signal *Router* to skip payload inspection.
* Encrypting and decrypting payload with crypto algorithms.
* Providing additional information about payload format and type.

**Feature Announcement**

Support for this advanced feature MUST be announced by *Callers* (`role := "caller"`), *Callees* (`role := "callee"`),
*Dealers* (`role := "dealer"`), *Publishers* (`role := "publisher"`), *Subscribers* (`role := "subscriber"`) 
and *Brokers* (`role := "broker"`) via

{align="left"}
HELLO.Details.roles.<role>.features.protected_payload_mode|bool := true

Protected Payload Mode can work only if all three nodes (*Caller*, *Dealer*, *Callee* or
*Publisher*, *Broker*, *Subscriber*) support and announced this feature.

Cases where *Caller* sends `CALL` message with `protected payload` without announcing it during `HELLO`
handshake MUST be treated as *PROTOCOL ERRORS* and underlying WAMP connections must be aborted with
`wamp.error.protocol_violation` error reason.

Cases where *Caller* sends `CALL` message with `protected payload` to *Dealer*, that did not announce
protected payload support during `WELCOME` handshake MUST be treated as *PROTOCOL ERRORS* and underlying WAMP
connections must be aborted with `wamp.error.protocol_violation` error reason.

Cases where *Caller* sends `CALL` message with `protected payload` to the *Dealer* that supports this feature,
which then must be routed to the *Callee* which doesn't support `protected payload` MUST be treated as 
*APPLICATION ERRORS* and *Dealer* MUST respond to *Caller* with `wamp.error.feature_not_supported` error message.

Cases where *Publisher* sends `PUBLISH` message with `protected payload` without announcing it during `HELLO`
handshake MUST be treated as *PROTOCOL ERRORS* and underlying WAMP connections must be aborted with
`wamp.error.protocol_violation` error reason.

Cases where *Publisher* sends `PUBLISH` message with `protected payload` to *Broker*, that did not announce
protected payload support during `WELCOME` handshake MUST be treated as *PROTOCOL ERRORS* and underlying WAMP
connections must be aborted with `wamp.error.protocol_violation` error reason.

Cases where *Publisher* sends `PUBLISH` message with `protected payload` to the *Broker* that supports this feature,
which then must be routed to the *Subscriber* which doesn't support `protected payload` cannot be recognized at the
protocol level due to asynchronous message processing and must be covered at *Subscriber* side.

Cases where *Callee* sends `YIELD` message with `protected payload` without announcing it during `HELLO`
handshake MUST be treated as *PROTOCOL ERRORS* and underlying WAMP connections must be aborted with
`wamp.error.protocol_violation` error reason.

Cases where *Callee* sends `YIELD` message with `protected payload` to *Dealer*, that did not announce
protected payload support during `WELCOME` handshake MUST be treated as *PROTOCOL ERRORS* and underlying WAMP
connections must be aborted with `wamp.error.protocol_violation` error reason.

Cases where *Callee* sends `YIELD` message with `protected payload` to the *Dealer* that supports this feature,
which then must be routed to the *Caller* which doesn't support `protected payload` MUST be treated as
*APPLICATION ERRORS* and *Dealer* MUST respond to *Callee* with `wamp.error.feature_not_supported` error message.

**Message attributes**

For this feature to be in use, `CALL`, `PUBLISH` and `YIELD` messages options are extended with additional attributes. 
This attributes then are passed as is within `INVOCATION`, `EVENT` and `RESULT` messages respectively.

{align="left"}
        CALL.Options.enc_serializer|string
        CALL.Options.enc_algo|string
        CALL.Options.enc_keyname|string
        CALL.Options.enc_key|string
        CALL.Options.enc_resp_key|string


{align="left"}
        PUBLISH.Options.enc_serializer|string
        PUBLISH.Options.enc_algo|string
        PUBLISH.Options.enc_keyname|string
        PUBLISH.Options.enc_key|string


{align="left"}
        YIELD.Options.enc_serializer|string
        YIELD.Options.enc_algo|string
        YIELD.Options.enc_keyname|string
        YIELD.Options.enc_key|string

**enc_serializer attribute**

`enc_serializer` attribute is required. It specifies what serializer was used to build up payload object.
It can be `mqtt`, `amqp`, `stomp` value when processing data from related technologies or ordinary 
`json`, `msgpack`, `cbor` data serializers. *Router* understands that `Protected Payload Mode` is in use
by checking the existence and non-empty value of this attribute in `CALL`, `PUBLISH` and `YIELD` messages options.

**enc_algo attribute**

`enc_algo` attribute is optional. It is required if payload is encrypted. This attribute specifies cryptographic
algorithm that was used to encrypt payload. It can be `curve25519`, `xsalsa20poly1305` or any other valid algorithm.

**enc_kms attribute**

`enc_kms` stands for Key Management Schema. It is optional string attribute. This attribute can contain name or
identifier of key management provider which is known to target peer, so it can be used to obtain information
about encryption keys.

**enc_key attribute**

`enc_key` attribute is optional. This attribute can contain encryption key id that was used to encrypt payload.
`enc_key` attribute is always a type of string. The value can be a hex-encoded string, uri, DNS name, 
Ethereum address, UUID identifier - any meaningful value by which target peer can choose private key 
without guessing. Format of the value may depend on `enc_kms` attribute.

**enc_key_val attribute**

`enc_key_val` attribute is optional. As opposed to `enc_key` attribute this one can contain encryption key itself.
As payload encryption is done with public key there is no need to hide it. And sometimes it is useful to pass it
through the wire. `enc_key_val` attribute is a type of string. To store the key which is binary, the key need to be
converted to base64-encoded string.

**enc_resp_key attribute**

`enc_resp_key` attribute is optional. One RPC can be called by many clients. To securely transmit RPC results to the
client, they need also to be encrypted with *Caller* public key. This can be hard to maintain all keys for every client.
Instead of this client can send his public key to use for encrypting payload right with the `CALL` request. And
*Callee* then will use it for encrypting results. To store the key which is binary, the key need to be
converted to base64-encoded string.

**Message structure**

With `Protected Payload Mode` in use message payload MUST BE sent as one binary item inside 
`Arguments|list`, while `ArgumentsKw|dict` MUST BE missing.

*Example.* Caller-to-Dealer `CALL` with encryption and key ID

{align="left"}
```json
    [
        48,
        25471,
        {
            "enc_serializer": "json",
            "enc_algo": "curve25519",
            "enc_key": "the_one_you_generated_yesterday"
        },
        "com.myapp.secret_rpc_for_sensitive_data",
        [Payload|binary]
    ]
```

If RPC doesn't provide any results, or it is kind of `success` flag and there is no need to encrypt it, 
`enc_resp_key` option can be omitted.

*Example.* Caller-to-Dealer `CALL` with encryption and key ID and response key

{align="left"}
```json
    [
        48,
        25471,
        {
            "enc_serializer": "json",
            "enc_algo": "curve25519",
            "enc_key": "the_one_you_generated_yesterday",
            "enc_resp_key": "caller_public_key"
        },
        "com.myapp.secret_rpc_for_sensitive_data",
        [Payload|binary]
    ]
```

*Example.* Caller-to-Dealer `CALL` with encryption and public key itself and response key

{align="left"}
```json
    [
        48,
        25471,
        {
            "enc_serializer": "json",
            "enc_algo": "curve25519",
            "enc_key": "GTtQ37XGJO2O4R8Dvx4AUo8pe61D9evIWpKGQAPdOh0=",
            "enc_resp_key": "caller_public_key"
        },
        "com.myapp.secret_rpc_for_sensitive_data",
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
            "enc_serializer": "mqtt"
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
            "enc_serializer": "json",
            "enc_algo": "curve25519",
            "enc_key": "the_one_you_generated_yesterday"
        },
        [Payload|binary]
    ]
```

*Example.* Dealer-to-Callee `INVOCATION` with encryption and key ID and response key

{align="left"}
```json
    [
        68,
        35477,
        1147,
        {
            "enc_serializer": "json",
            "enc_algo": "curve25519",
            "enc_key": "the_one_you_generated_yesterday",
            "enc_resp_key": "caller_public_key"
        },
        [Payload|binary]
    ]
```

*Example.* Dealer-to-Callee `INVOCATION` with encryption and public key itself and response key

{align="left"}
```json
    [
        68,
        35478,
        2192,
        {
            "enc_serializer": "json",
            "enc_algo": "curve25519",
            "enc_key": "GTtQ37XGJO2O4R8Dvx4AUo8pe61D9evIWpKGQAPdOh0=",
            "enc_resp_key": "caller_public_key"
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
            "enc_serializer": "mqtt"
        },
        [Payload|binary]
    ]
```

TODO: Provide more examples of messages of different types and options.


**About supported serializers and cryptographic cyphers**

WAMP works as infrastructure for delivering messages between peers. Regardless of what encryption algorithm 
and serializer were chosen for protected payload mode, *Router* will not inspect and analyze related encryption 
message options and payload. It is up to an application side code responsibility to use serializers and 
cyphers known to every peer involved into message processing.
