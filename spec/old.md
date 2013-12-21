




A procedure that is provided by a *Callee* to be called via WAMP by *Callers* is said to be *exported*. An exported procedure is called **RPC endpoint**.

A procedure is always exported under a fully qualified URI and the respective endpoint can be identified by said URI.

There might be more than one endpoint exported under a given URI.

A *Caller* provides the URI of the RPC endpoint to identify the procedure to be called and any arguments for the call.
The *Callee* will execute the procedure using the arguments supplied with the call and return the result of the call or an error to the *Caller*. 



    CallOptions = {TIMEOUT: Timeout|integer := 0,
                   PKEYS: PartitionKeys|list := [null],
                   PMODE: ("all"|"any")|string := "all"}

