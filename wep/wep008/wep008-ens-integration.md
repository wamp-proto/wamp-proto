# ENS Integration

## ENS Names for WAMP

* `mainnet.network.wamp-proto.eth`
* `arbitrum.network.wamp-proto.eth`
* `zksync.network.wamp-proto.eth`

reverseRegistrar.setName('arachnid.eth', {from: eth.accounts[0]});


## ENS Name Resolution

[ENS](https://ens.domains/) support in decentralized WAMP allows

1. WAMP clients to find a WAMP routing endpoint to connect to, given a realm
2. WAMP routers to find other WAMP routers to connect to (via federated router-to-router links), given a realm

For both, the realm is a globally defined, on-chain record with an address that can be resolved via ENS from a name:

0. WAMP clients and routers to retrieve a global WAMP realm, given an ENS name


ENS allows for regular, forward resolution of names to ENS records:

> Resolving a name in ENS is a two-step process. First, the ENS registry is called with the name to resolve, after hashing it using the procedure described below. If the record exists, the registry returns the address of its resolver. Then, the resolver is called, using the method appropriate to the resource being requested. The resolver then returns the desired result. Here is an example [forward record](https://app.ens.domains/name/chrisbell.eth) and [reverse record](https://app.ens.domains/address/0xddd3964d75d59b6b6d5c31eb313bba5ebf076364).

ENS also allows reverse resolution of Ethereum addresses to ENS names:

> Reverse records allow the owner of an address to claim a name as authoritative for that address. Reverse ENS records are stored in the ENS hierarchy in the same fashion as regular records, under a reserved domain, addr.reverse.

A connecting WAMP client or router could for example follow a procedure like this:

1. Use configured network (Ethereum gateway, DNS resolver, IP gateway)
2. Use configured wallet (NXP SE050)
3. Resolve public wallet address => ENS name (using [ENS reverse resolution](https://docs.ens.domains/ens-improvement-proposals/ensip-3-reverse-resolution))
4. Resolve ENS name => ENS resolver (using regular [ENS resolution](https://docs.ens.domains/ens-improvement-proposals/ensip-1-ens))
5. Query ENS resolver => WAMP urls & realm
6. Connect to WAMP (any of) url & join realm
7. Authenticate with WAMP-cryptosign

## Realm Name Resolution

* realm name => realm address
* realm address => realm data: realm url, realm name


`WampRealm`

    0x5678..

`example.eth`

    eth             0xabcd..

    wamp            0x1234..

`0xabcd..`

    ETH             25

`0x5678..`

    WampRealm.get   0x1234..

`WampRealm[0x1234..]`

    name            realm1

    meta            ipfs://QmRAQB6YaCyidP37UdDnjFY5vQuiBrcqdyoW1CuDgwxkD4

    endpoints       {"eu": [(10, "wss://example1.com/ws"), (20, "wss://example2.com/ws")],
                     "us": [(30, "wss://example3.com/ws")]}


---------


This EIP defines a resolver profile for ENS that permits the lookup of arbitrary key-value text data. This allows ENS name holders to associate e-mail addresses, URLs and other informational data with a ENS name.

https://medium.com/the-ethereum-name-service/new-text-records-now-available-for-ens-names-in-manager-a0ebb9cda73a

Service Keys must be made up of a reverse dot notation for a namespace which the service owns, for example, DNS names (e.g. .com, .io, etc) or ENS name (i.e. .eth). Service Keys must contain at least one dot.

org.matrix - a Matrix ID user

eth.wamp-proto - a WAMP realm address

eth.wamp-proto.url    - a WAMP endpoint to connect
eth.wamp-proto.realm  - a WAMP realm to join

eth.wamp-proto.url    - wss://eu1.thing.com/ws
eth.wamp-proto.realm  - om26er-home1

EIP-634: Storage of text records in ENS
https://eips.ethereum.org/EIPS/eip-634

EIP-181: ENS support for reverse resolution of Ethereum addresses
https://eips.ethereum.org/EIPS/eip-181
