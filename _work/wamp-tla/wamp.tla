-------------------------------- MODULE wamp --------------------------------

EXTENDS Integers, TLC

CONSTANT CLIENTS, ROUTERS

Clients == 1..CLIENTS
Routers == 1..ROUTERS

VARIABLES
    transports,
    clients,
    routers

vars == <<transports, clients, routers>>

TransportLoss ==
    /\ \E tr \in transports: transports' = transports \ {tr}
    /\ UNCHANGED <<clients, routers>>

ConnectClient(c) ==
    /\ \E rt \in routers: TRUE

Init ==
    /\ transports = {}
    /\ clients = <<>>
    /\ routers = <<>>

Next ==
    UNCHANGED vars

Types == TRUE

Safety == TRUE

Liveness == TRUE

Fairness == TRUE

Spec == Init /\ [][Next]_vars

=============================================================================
\* Modification History
\* Last modified Sun Jan 08 09:03:52 CET 2023 by oberstet
\* Created Sun Jan 08 08:57:35 CET 2023 by oberstet
