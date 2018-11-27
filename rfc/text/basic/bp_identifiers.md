## Identifiers

### URIs {#uris}

WAMP needs to identify the following persistent resources:

1.  Topics
2.  Procedures
3.  Errors

These are identified in WAMP using Uniform Resource Identifiers (URIs) [@!RFC3986] that MUST be Unicode strings.

> When using JSON as WAMP serialization format, URIs (as other strings) are transmitted in UTF-8 [@!RFC3629] encoding.

*Examples*

* `com.myapp.mytopic1`
* `com.myapp.myprocedure1`
* `com.myapp.myerror1`

The URIs are understood to form a single, global, hierarchical namespace for WAMP.

> The namespace is unified for topics, procedures and errors - these different resource types do NOT have separate namespaces.
>

To avoid resource naming conflicts, the package naming convention from Java is used, where URIs SHOULD begin with (reversed) domain names owned by the organization defining the URI.

#### Relaxed/Loose URIs

URI components (the parts between two `.`s, the head part up to the first `.`, the tail part after the last `.`) MUST NOT contain a `.`, `#` or whitespace characters and MUST NOT be empty (zero-length strings).

> The restriction not to allow `.` in component strings is due to the fact that `.` is used to separate components, and WAMP associates semantics with resource hierarchies, such as in pattern-based subscriptions that are part of the Advanced Profile. The restriction not to allow empty (zero-length) strings as components is due to the fact that this may be used to denote wildcard components with pattern-based subscriptions and registrations in the Advanced Profile. The character `#` is not allowed since this is reserved for internal use by Dealers and Brokers.

As an example, the following regular expression could be used in Python to check URIs according to the above rules:

{align="left"}
``` python
    <CODE BEGINS>
        ## loose URI check disallowing empty URI components
        pattern = re.compile(r"^([^\s\.#]+\.)*([^\s\.#]+)$")
    <CODE ENDS>
```

When empty URI components are allowed (which is the case for specific messages that are part of the Advanced Profile), this following regular expression can be used (shown used in Python):

{align="left"}
``` python
    <CODE BEGINS>
        ## loose URI check allowing empty URI components
        pattern = re.compile(r"^(([^\s\.#]+\.)|\.)*([^\s\.#]+)?$")
    <CODE ENDS>
```

#### Strict URIs

While the above rules MUST be followed, following a stricter URI rule is recommended: URI components SHOULD only contain lower-case letters, digits and `_`.

As an example, the following regular expression could be used in Python to check URIs according to the above rules:

{align="left"}
```python
    <CODE BEGINS>
        ## strict URI check disallowing empty URI components
        pattern = re.compile(r"^([0-9a-z_]+\.)*([0-9a-z_]+)$")
    <CODE ENDS>
```

When empty URI components are allowed (which is the case for specific messages that are part of the Advanced Profile), the following regular expression can be used (shown in Python):

{align="left"}
```python
    <CODE BEGINS>
        ## strict URI check allowing empty URI components
        pattern = re.compile(r"^(([0-9a-z_]+\.)|\.)*([0-9a-z_]+)?$")
    <CODE ENDS>
```

> Following the suggested regular expression will make URI components valid identifiers in most languages (modulo URIs starting with a digit and language keywords) and the use of lower-case only will make those identifiers unique in languages that have case-insensitive identifiers. Following this suggestion can allow implementations to map topics, procedures and errors to the language environment in a completely transparent way.

#### Reserved URIs

Further, application URIs MUST NOT use `wamp` as a first URI component, since this is reserved for URIs predefined with the WAMP protocol itself.

*Examples*

* `wamp.error.not_authorized`
* `wamp.error.procedure_already_exists`


### IDs {#ids}

WAMP needs to identify the following ephemeral entities each in the scope noted:

1. Sessions (*global scope*)
2. Publications (*global scope*)
3. Subscriptions (*router scope*)
4. Registrations (*router scope*)
5. Requests (*session scope*)

These are identified in WAMP using IDs that are integers between (inclusive) **1** and **2^53** (9007199254740992):

* IDs in the *global scope* MUST be drawn *randomly* from a *uniform distribution* over the complete range [1, 2^53]
* IDs in the *router scope* CAN be chosen freely by the specific router implementation
* IDs in the *session scope* MUST be incremented by 1 beginning with 1 (for each direction - *Client-to-Router* and *Router-to-Client*)

> The reason to choose the specific lower bound as 1 rather than 0 is that 0 is the null-like (falsy) value for many programming languages.
> The reason to choose the specific upper bound is that 2^53 is the largest integer such that this integer and *all* (positive) smaller integers can be represented exactly in IEEE-754 doubles. Some languages (e.g. JavaScript) use doubles as their sole number type. Most languages do have signed and unsigned 64-bit integer types that both can hold any value from the specified range.
>

The following is a complete list of usage of IDs in the three categories for all WAMP messages. For a full definition of these see [messages section](#messages).

#### Global Scope IDs

* `WELCOME.Session`
* `PUBLISHED.Publication`
* `EVENT.Publication`


#### Router Scope IDs

* `EVENT.Subscription`
* `SUBSCRIBED.Subscription`
* `REGISTERED.Registration`
* `UNSUBSCRIBE.Subscription`
* `UNREGISTER.Registration`
* `INVOCATION.Registration`


#### Session Scope IDs

* `ERROR.Request`
* `PUBLISH.Request`
* `PUBLISHED.Request`
* `SUBSCRIBE.Request`
* `SUBSCRIBED.Request`
* `UNSUBSCRIBE.Request`
* `UNSUBSCRIBED.Request`
* `CALL.Request`
* `CANCEL.Request`
* `RESULT.Request`
* `REGISTER.Request`
* `REGISTERED.Request`
* `UNREGISTER.Request`
* `UNREGISTERED.Request`
* `INVOCATION.Request`
* `INTERRUPT.Request`
* `YIELD.Request`
