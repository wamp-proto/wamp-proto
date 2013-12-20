## Feature Announcement

instead of protocol version negotiation, feature announcement

allows for
graceful degration
only implement subsets of functionality

    
> **Polymorphism**. For a given message type, WAMP only uses messages that are polymorphic in the *number* of message arguments. The message type and the message length uniquely determine the type and semantics of the message arguments.
> This leads to message parsing and validation control flow that is efficient, simple to implement and simple to code for rigorous message format checking.

There is however another requirement (desirable goal) in WAMPv2: the *application* payload (that is call arguments, returns, event payload etc) must be at the end of the WAMP message list. The reason is: *brokers* and *dealers* have no need to inspect (parse) that application payloads. Their business is call/event routing. Having the application payload at the end of the list allows brokers/dealers skip parsing altogether. This improves efficiency/performance and probably even allows to transport application encrypted payload transparently.

> **Extensibility**. Some WAMP messages provide options or details with type of dictionary.
> This allows for future extensibility and implementations that only provide subsets of functionality by ignoring unimplemented attributes.
> 




A procedure that is provided by a *Callee* to be called via WAMP by *Callers* is said to be *exported*. An exported procedure is called **RPC endpoint**.

A procedure is always exported under a fully qualified URI and the respective endpoint can be identified by said URI.

There might be more than one endpoint exported under a given URI.

A *Caller* provides the URI of the RPC endpoint to identify the procedure to be called and any arguments for the call.
The *Callee* will execute the procedure using the arguments supplied with the call and return the result of the call or an error to the *Caller*. 



    CallOptions = {TIMEOUT: Timeout|integer := 0,
                   PKEYS: PartitionKeys|list := [null],
                   PMODE: ("all"|"any")|string := "all"}


**Partitioned Calls**

`PKEYS` allows to specify a list of application specific *partition keys*. Applications can use partition keys for data sharding. The RPC is only routed to the database instances that hold the respective partitions.

Results from the individual partitions are returned as progressive results via `CALL_PROGRESS` messages. In any case, the call is completed via a `CALL_RESULT` or `CALL_ERROR` message.

`PMODE` allows to specify the mode of partitioned call: `"all"` or `"any"`.

In mode `"all"` the RPC is routed to all database instances holding data from partitions of the specified list.

In mode `"any"` the RPC is routed to a single database instance, randomly selected from the instances holding data from partitions of the specified list.

