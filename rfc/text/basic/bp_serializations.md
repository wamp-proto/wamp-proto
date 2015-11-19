## Serializations

WAMP is a message based protocol that requires serialization of messages to octet sequences to be sent out on the wire.

A message serialization format is assumed that (at least) provides the following types:

* `integer` (non-negative)
* `string` (UTF-8 encoded Unicode)
* `bool`
* `list`
* `dict` (with string keys)

> WAMP *itself* only uses the above types, e.g. it does not use the JSON data types `number` (non-integer) and `null`. The *application payloads* transmitted by WAMP (e.g. in call arguments or event payloads) may use other types a concrete serialization format supports.
>

There is no required serialization or set of serializations for WAMP implementations (but each implementation MUST, of course, implement at least one serialization format). Routers SHOULD implement more than one serialization format, enabling components using different kinds of serializations to connect to each other.

WAMP defines two bindings for message serialization:

1. JSON
2. MessagePack

Other bindings for serialization may be defined in future WAMP versions.

### JSON

With JSON serialization, each WAMP message is serialized according to the JSON specification as described in RFC4627.

Further, binary data follows a convention for conversion to JSON strings. For details see the Appendix.

### MessagePack

With MessagePack serialization, each WAMP message is serialized according to the MessagePack specification.

> Version 5 or later of MessagePack MUST BE used, since this version is able to differentiate between strings and binary values.
