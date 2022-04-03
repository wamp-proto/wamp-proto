# WEP008 - Decentralized WAMP Service Mesh

WAMP is an open standard WebSocket subprotocol that provides two application messaging patterns in one unified protocol: routed Remote Procedure Calls and Publish & Subscribe. This extension allows to federate WAMP routers of different operators to create a decentralized WAMP service mesh with trust anchors in Ethereum.

![Decentralized](../../docs/_static/img/decentralized.png)
> Source: [Hopium Diaries - Dystopian Dreams](https://www.youtube.com/watch?v=v1Z5BnBuFyE)


## Special-purpose TLDs in WAMP URIs

```
<ENS name>.eth                      =>      Ethereum address
<Ethereum address>.addr.reverse     =>      ENS Name
```

> Reverse Registrar: The registrar responsible for managing reverse resolution via the .addr.reverse special-purpose TLD. https://docs.ens.domains/contract-api-reference/reverseregistrar


## Roles

> "We should accept the premise that people will not run their own servers by designing systems that can distribute trust without having to distribute infrastructure."
>
> [My first impressions of web3](https://moxie.org/2022/01/07/web3-first-impressions.html), Moxie Marlinspike (creator of [Signal](https://www.signal.org/))

*Owners:*

* **Library Publisher**
* **Service Vendor**
* **Realm Keeper**
    * sponsor traffic
    * sponsor services
    * insure users

*Operators:*

* **Router Operator**
    * traffic risks
* **Service Operator**
    * traffic costs
    * service risks

*Users:*

* **Service User**
    * traffic costs
    * service costs

```
Role        Function                    Stakes

publisher	Service API                 -
guardian	Service Realm               (C1 => publisher)
developer	Service Implementation      (C1 => publisher)
operator1	Router Node                 C1 => guardian
operator2	Service Instance            C1 => guardian, C2 => operator1, C3 => developer
user	    Service Client              C1 => guardian, C2 => operator1, C3 => operator2
```

* Users and Service Operators stake WMP on a Realm to reserve routing bandwidth (messages/block).
* Router Operators stake WMP on a Realm to provide routing bandwidth (messages/block).
* Service Operators stake WMP on a Realm to provide service bandwidth (messages/block).
* Router Operators receive WMP on a Realm for used routing bandwidth (messages/block).
* Service Operators receive WMP on a Realm for used service bandwidth (messages/block)
* Realms send WMP to Router and Service Operators

* Realm Funding Rate (RFR): 2%
* WMP funding: 2% of sum of WMP for total bandwidth reserved by Clients on a Realm
* WMP funding is distributed to Router Operators, Service Operators and Service Vendors

### Non-staking Roles

*Library Publishers* define *APIs*, which can be enabled in *Realms* and provided by
*Service Operators* (in realms), and may insure *Service Operators/Users*

*Realm Keeper* configures *Permissions* and enables *APIs* in *Realms*, and
may sponsor *Router Operators* in the realm, and
may sponsor *Service Operators* in the realm, and
may insure *Service Users* in the realm.

### Staking Roles

A *Router Operator* stakes WMP in a *Realm* for the **risks** associated with the announced **traffic** availability/bandwidth of the provided public routing endpoints.

A *Service Operator* stakes WMP in a *Realm* for the **costs** associated with the **traffic**, and the **risks** associated with the announced availability/bandwidth of the provided public **service** instances.

A *Service User* stakes WMP in a *Realm* for the **costs** associated with the **traffic** and **services** raised by the user.

------

## Tasks

1. [Ethereum Integration](wep008-ethereum-integration.md)
2. [ENS Integration](wep008-ens-integration.md)
3. [IPFS Integration](wep008-ipfs-integration.md)
4. [The Graph integration](wep008-thegraph-integration.md)
5. [Chainlink Integration](wep008-chainlink-integration.md)
6. [Layer-2 Porting](wep008-layer-2-porting.md)
