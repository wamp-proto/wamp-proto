These are the working faucets on [Rinkeby](https://www.rinkeby.io/) as of Dez, 2021:
* https://faucet.rinkeby.io/
* https://faucets.chain.link/rinkeby

1. The device has access to a HSM which can create Ethereum signatures (eg NXP SE050)

2. The device uses it's Ethereum public key (the address corresponding to the key-pair) to do a reverse-ENS lookup (EIP181)

3. The resulting ENS name can be used as the user name, and a forward ENS lookup for the ENS text records (EIP634) is done

  eth.wamp-proto.url    - a WAMP endpoint to connect
  eth.wamp-proto.realm  - a WAMP realm to join

4. The client connects to eth.wamp-proto.url, joining realm eth.wamp-proto.realm, and
  - if the client is completely new/unknown, will be authenticated as "anonymous" => onboarding
  - if the client is known, will be authenticated



Supports public Infura, Cloudflare and custom Ethereum gateways
Supports up to 5 gateways and (re)trying all

https://cloudflare-eth.com/


Hardware based Security

Ethereum key pair:

  NXP SE050

Ethereum gateway configuration:

  Key         Enabled       Configuration
  ---------------------------------------
  infura      true|false    hard-coded
  cloudflare  true|false    hard-coded
  custom1     true|false    configurable
  custom2     true|false    configurable
  custom3     true|false    configurable


https://docs.ens.domains/ens-improvement-proposals/ensip-3-reverse-resolution

https://docs.ens.domains/ens-improvement-proposals/ensip-7-contenthash-field

1. L1 (Ethereum nodes): trust anchors (ENS, IPFS, The Graph, Chainlink), L2 transfers (zkSync)
2. L2 (zkSync nodes): WAMP metadata transactions (WAMP smart contracts)
3. L3 (Crossbar.io nodes): WAMP service transactions

L1: Domain, Library, Realm
  Domain:   URL, Nodes
  Library:  Name, APIs
  Realm:    Name, APIs, Nodes

L2: Workers, RLinks, Services

