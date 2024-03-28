## Messages {#messages}

All WAMP messages are a `list` with a first element `MessageType` followed by one or more message type specific elements:

{align="left"}
        [MessageType|integer, ... one or more message type specific
            elements ...]

The notation `Element|type` denotes a message element named `Element` of type `type`, where `type` is one of

* `uri`: a string URI as defined in [URIs](#uris)
* `id`: an integer ID as defined in [IDs](#ids)
* `integer`: a non-negative integer
* `string`: a Unicode string, including the empty string
* `bool`: a boolean value (`true` or `false`) - integers MUST NOT be used instead of boolean value
* `dict`: a dictionary (map) where keys MUST be strings, keys MUST be unique and serialization order is undefined (left to the serializer being used)
* `list`: a list (array) where items can be again any of this enumeration

*Example*

A `SUBSCRIBE` message has the following format

{align="left"}
        [SUBSCRIBE, Request|id, Options|dict, Topic|uri]

Here is an example message conforming to the above format

{align="left"}
        [32, 713845233, {}, "com.myapp.mytopic1"]


### Extensibility

Some WAMP messages contain `Options|dict` or `Details|dict` elements. This allows for future extensibility and implementations that only provide subsets of functionality by ignoring unimplemented attributes. Keys in `Options` and `Details` MUST be of type `string` and MUST match the regular expression `[a-z][a-z0-9_]{2,}` for WAMP predefined keys. Implementations MAY use implementation-specific keys that MUST match the regular expression `_[a-z0-9_]{3,}`. Attributes unknown to an implementation MUST be ignored.


### No Polymorphism

For a given `MessageType` and number of message elements the expected types are uniquely defined. Hence there are no polymorphic messages in WAMP. This leads to a message parsing and validation control flow that is efficient, simple to implement and simple to code for rigorous message format checking.


### Structure

The application payload (that is call arguments, call results, event payload etc) is always at the end of the message element list. The rationale is: Brokers and Dealers have no need to inspect (parse) the application payload. Their business is call/event routing. Having the application payload at the end of the list allows Brokers and Dealers to skip parsing it altogether. This can improve efficiency and performance.
