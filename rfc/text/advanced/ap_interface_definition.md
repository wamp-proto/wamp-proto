## WAMP IDL {#wamp-idl}

### Application Payload Typing

User defined WAMP application payloads are transmitted in `Arguments|list` and `ArgumentsKw|dict` elements of the following WAMP messages:

* `PUBLISH`
* `EVENT`
* `CALL`
* `INVOCATION`
* `YIELD`
* `RESULT`
* `ERROR`

A *Publisher* uses the

* `PUBLISH.Arguments|list`, `PUBLISH.ArgumentsKw|dict`

message to send the event payload to be published to the *Broker*. When the event is accepted by the *Broker*, it will dispatch

* `EVENT.Arguments|list`, `EVENT.ArgumentsKw|dict`

messages to all (eligible, and not excluded) *Subscribers.

A *Caller* uses the

* `CALL.Arguments|list`, `CALL.ArgumentsKw|dict`

message to send the call arguments to be used to the *Dealer*. When the call is accepted by the *Dealer*, it will forward

* `INVOCATION.Arguments|list`, `INVOCATION.ArgumentsKw|dict`

to the (or one of) *Callee*, and receive a

* `YIELD.Arguments|list`, `YIELD.ArgumentsKw|dict`

message, which it will return to the original *Caller*

* `RESULT.Arguments|list`, `RESULT.ArgumentsKw|dict`

In the error case, a *Callee* MAY return an

* `ERROR.Arguments|list`, `ERROR.ArgumentsKw|dict`

which again is returned to the original *Caller*.

> It is important to note that the above messages and message elements are the only ones free for use with application and user defined payloads. In particular, even though the following WAMP messages and message element carry payloads defined by the specific WAMP authentication method used, they do *not* carry arbitrary application payloads: `HELLO.Details["authextra"]|dict`, `WELCOME.Details["authextra"]|dict`, `CHALLENGE.Extra|dict`, `AUTHENTICATE.Extra|dict`.

To define the application payload `Arguments|list` and `ArgumentsKw|dict`, WAMP IDL reuses the [FlatBuffers IDL](https://google.github.io/flatbuffers/md__schemas.html), specifically, we map a pair of `Arguments|list` and `ArgumentsKw|dict` to a FlatBuffers Table with WAMP defined FlatBuffers *Attributes*.

For example, the [Session Meta API]({#session-metapi}) includes a procedure to [kill all sessions by authid](#name-wampsessionkill_by_authid) with:

**Positional arguments** (`args|list`)

1. `authid|string` - The authentication ID identifying sessions to close.

**Keyword arguments** (`kwargs|dict`)

1. `reason|uri` - reason for closing sessions, sent to clients in `GOODBYE.Reason`
2. `message|string` - additional information sent to clients in `GOODBYE.Details` under the key "message".

as arguments. When successful, this procedure will return a call result with:

**Positional results** (`results|list`)

1. `sessions|list` - The list of WAMP session IDs of session that were killed.

**Keyword results** (`kwresults|dict`)

1. `None`

To specify the call arguments in FlatBuffers IDL, we can define a FlatBuffers table for both `args` and `kwargs`:

```flatbuffers
/// Call args/kwargs for "wamp.session.kill_by_authid"
table SessionKillByAuthid
{
    /// The WAMP authid of the sessions to kill.
    authid: string (wampuri);

    /// A reason URI provided to the killed session(s).
    reason: string (kwarg, wampuri);

    /// A message provided to the killed session(s).
    message: string (kwarg);
}
```

The table contains the list `args` as table elements (in order), unless the table element has an *Attribute* `kwarg`, in which case the element one in `kwarg`.

The attributes `wampid` and `wampuri` are special markers that denote values that follow the respective WAMP identifier rules for WAMP IDs and URIs.

When successful, the procedure will return a list of WAMP session IDs of session that were killed. Again, we can map this to FlatBuffers IDL:

```flatbuffers
table WampIds
{
    /// List of WAMP IDs.
    value: [uint64] (wampid);
}
```

### WAMP IDL Attributes

WAMP IDL uses *custom FlatBuffer attributes* to

* mark `kwarg` fields which map to WAMP keyword argument vs `arg` (default)
* declare fields of a scalar base type to follow (stricter) WAMP rules (for IDs and URIs)
* specify the WAMP action type, that is *Procedure* vs *Topic*, on service declarations

> "Attributes may be attached to a declaration, behind a field, or after the name of a table/struct/enum/union. These may either have a value or not. Some attributes like deprecated are understood by the compiler; user defined ones need to be declared with the attribute declaration (like priority in the example above), and are available to query if you parse the schema at runtime. This is useful if you write your own code generators/editors etc., and you wish to add additional information specific to your tool (such as a help text)." (from [source](https://google.github.io/flatbuffers/md__schemas.html)).

The *Attributes* used in WAMP IDL are defined in `<WAMP API Catalog>/src/wamp.fbs`, and are described in the following sections:

* `arg`, `kwarg`
* `wampid`
* `wampname`, `wampname_s`
* `wampuri`, `wampuri_s`, `wampuri_p`, `wampuri_sp`, `wampuri_pp`, `wampuri_spp`
* `type`

**WAMP Positional and Keyword-based Payloads**

Positional payloads `args|list` and keyword-based payloads `kwargs|dict` are table elements that have one of the following *Attributes*:

* `arg` (default)
* `kwarg`

One pair of `args` and `kwarg` types is declared by one FlatBuffer table with optional attributes on table fields, and the following rules apply or must be followed:

1. If neither `arg` nor `kwarg` attribute is provided, `arg` is assumed.
2. Only one of either `arg` or `kwarg` MUST be specified.
3. When a field has an attribute `kwarg`, all subsequent fields in the same table MUST also have attribute `kwarg`.

**WAMP IDs and URIs**

Integers which contain WAMP IDs use *Attribute*

1. `wampid`: WAMP ID, that is an integer `[1, 2^53]`

Strings which contain WAMP names ("URI components"), for e.g. WAMP roles or authids use *Attributes*

2. `wampname`: WAMP URI component (aka "name"), loose rules (minimum required to combine to dotted URIs), must match regular expression `^[^\s\.#]+$`.
3. `wampname_s`: WAMP URI component (aka "name"), strict rules (can be used as identifier in most languages), must match regular expression `^[\da-z_]+$`.

Strings which contain WAMP URIs or URI patterns use *Attribute*

4. `wampuri`: WAMP URI, loose rules, no empty URI components (aka "concrete or fully qualified URI"), must match regular expression `^([^\s\.#]+\.)*([^\s\.#]+)$`.
5. `wampuri_s`: WAMP URI, strict rules, no empty URI components, must match regular expression `^([\da-z_]+\.)*([\da-z_]+)$`.
6. `wampuri_p`: WAMP URI or URI (prefix or wildcard) pattern, loose rules (minimum required to combine to dotted URIs), must match regular expression `^(([^\s\.#]+\.)|\.)*([^\s\.#]+)?$`.
7. `wampuri_sp`: WAMP URI or URI (prefix or wildcard) pattern, strict rules (can be used as identifier in most languages), must match regular expression `^(([\da-z_]+\.)|\.)*([\da-z_]+)?$`.
8. `wampuri_pp`: WAMP URI or URI prefix pattern, loose rules (minimum required to combine to dotted URIs), must match regular expression `^([^\s\.#]+\.)*([^\s\.#]*)$`.
9. `wampuri_spp`: WAMP URI or URI prefix pattern, strict rules (can be used as identifier in most languages), must match regular expression `^([\da-z_]+\.)*([\da-z_]*)$`.

**WAMP Actions**

The type of WAMP action **procedure** or **topic** is designated using the *Attribute*

1. `type`: one of `"procedure"` or `"topic"`

The `type` *Attribute* can be used to denote WAMP service interfaces, e.g. continuing with above WAMP Meta API procedure example, the `wamp.session.kill_by_authid` procedure can be declared like this:

```flatbuffers
session_kill_by_authid (SessionKillByAuthid): WampIds (
    type: "procedure",
    wampuri: "wamp.session.kill_by_authid"
);
```

The value of attribute `type` specifies a WAMP *Procedure*, and the call arguments and result types of the procedure are given by:

* `SessionKillByAuthid`: procedure call arguments `args` (positional argument) and `kwargs` (keyword arguments) call argument follow this type
* `WampIds`: procedure call results `args` (positional results) and `kwargs` (keyword results)

The procedure will be registered under the WAMP URI `wamp.session.kill_by_authid` on the respective realm.
