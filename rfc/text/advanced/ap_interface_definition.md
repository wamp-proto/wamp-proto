## WAMP IDL {#wamp-idl}

WAMP was designed with the goals of being easy to approach and use for application developers. Creating a procedure to expose some custom functionality should be possible in any supported programming language using that language's native elements, with the least amount of additional effort.

Following from that, WAMP uses *dynamic typing* for the application payloads of calls, call results and error, as well as event payloads.

A WAMP router will happily forward *any* application payload on *any* procedure or topic URI as long as the client is _authorized_ (has permission) to execute the respective WAMP action (call, register, publish or subscribe) on the given URI.

This approach has served WAMP well, as application developers can get started immediately, and evolve and change payloads as they need without extra steps.
These advantages in flexibility of course come at a price, as nothing is free, and knowing that price is important to be aware of the tradeoffs one is accepting when using dynamic typing:

* problematic coordination of *Interfaces* within larger developer teams or between different parties
* no easy way to stabilize, freeze, document or share *Interfaces*
* no way to programmatically describe *Interfaces* ("interface reflection") at run-time

Problems such above could be avoided when WAMP supported an _option_ to formally define WAMP-based *Interfaces*. This needs to answer the following questions:

1. How to specify the `args|List` and `kwargs|Dict` application payloads that are used in WAMP calls, errors and events?
2. How to specify the type and URI (patterns) for WAMP RPCs *Procedures* and WAMP PubSub *Topics* that make up an *Interface*, and how to identify an *Interface* itself as a collection of *Procedures* and *Topics*?
3. How to package, publish and share *Catalogs* as a collection of *Interfaces* plus metadata

The following sections will describe the solution to each of above questions using WAMP IDL.

Using WAMP Interfaces finally allows to support the following application developer level features:

1. router-based application payload validation and enforcement
2. WAMP interface documentation generation and autodocs Web service
3. publication and sharing of WAMP Interfaces and Catalogs
4. client binding code generation from WAMP Interfaces
5. run-time WAMP type reflection as part of the WAMP meta API

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

Attributes may be attached to a declaration, behind a field, or after the name of a table/struct/enum/union. These may either have a value or not. Some attributes like deprecated are understood by the compiler; user defined ones need to be declared with the attribute declaration (like priority in the example above), and are available to query if you parse the schema at runtime. This is useful if you write your own code generators/editors etc., and you wish to add additional information specific to your tool (such as a help text).


**Positional and Keyword-based Payloads**

Positional payloads `args|list` and keyword-based payloads `kwargs|dict` are table elements that have one of the following *Attributes*:

* `arg` (default)
* `kwarg`

**WAMP Actions**

The type of WAMP action **procedure** or **topic** is designated using the *Attribute*

* `type`: one of `"procedure"` or `"topic"`

**WAMP IDs and URIs**

Integers which contain WAMP IDs use *Attribute*

* `wampid`: WAMP ID, that is an integer `[1, 2^53]`

Strings which contain WAMP names ("URI components"), for e.g. WAMP roles or authids use *Attributes*

* `wampname`: WAMP URI component (aka "name"), loose rules (minimum required to combine to dotted URIs), must match regular expression `^[^\s\.#]+$`.
* `wampname_s`: WAMP URI component (aka "name"), strict rules (can be used as identifier in most languages), must match regular expression `^[\da-z_]+$`.

Strings which contain WAMP URIs or URI patterns use *Attribute*

* `wampuri`: WAMP URI, loose rules, no empty URI components (aka "concrete or fully qualified URI"), must match regular expression `^([^\s\.#]+\.)*([^\s\.#]+)$`.
* `wampuri_s`: WAMP URI, strict rules, no empty URI components, must match regular expression `^([\da-z_]+\.)*([\da-z_]+)$`.
* `wampuri_p`: WAMP URI or URI (prefix or wildcard) pattern, loose rules (minimum required to combine to dotted URIs), must match regular expression `^(([^\s\.#]+\.)|\.)*([^\s\.#]+)?$`.
* `wampuri_sp`: WAMP URI or URI (prefix or wildcard) pattern, strict rules (can be used as identifier in most languages), must match regular expression `^(([\da-z_]+\.)|\.)*([\da-z_]+)?$`.
* `wampuri_pp`: WAMP URI or URI prefix pattern, loose rules (minimum required to combine to dotted URIs), must match regular expression `^([^\s\.#]+\.)*([^\s\.#]*)$`.
* `wampuri_spp`: WAMP URI or URI prefix pattern, strict rules (can be used as identifier in most languages), must match regular expression `^([\da-z_]+\.)*([\da-z_]*)$`.


**Typing Procedures, Topics and Interfaces**

```flatbuffers
/// Forcefully kill all sessions with given authid.
session_kill_by_authid (SessionKillByAuthid): WampIds
    (type: "procedure", wampuri: "wamp.session.kill_by_authid");
```
