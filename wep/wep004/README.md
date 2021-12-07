# WEP004 - WAMP Router-to-Router Links

Router-to-router links allow to connect WAMP router nodes to support transparent routing services on shared realms for clients connected to any of the nodes.

Router-to-router links are a low-level facility that allows to configure and setup networks of nodes in different scenarios:

1. scaling and high-availability (both single node scale-up, and multi-node cluster scale-out)
2. edge/cloud topologies with edge routers connecting (tree-like) to cloud hosted nodes
3. federation/decentralization, with nodes operated by different operators connecting

----

1. single operator
2. decentralized, single impl
3. decentralized, multiple impl

Specific features:

* ENS support for rlink targets
