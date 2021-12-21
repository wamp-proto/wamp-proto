# Layer-2 Porting

## Introduction

We define layer-2 as a chain that fully or partially derives its security from layer-1 Ethereum so that users do not have to rely on the honesty of L2 validators for the security of their funds.

### Types of Ethereum scaling

   * Sidechains (independent chains with Ethereum bridge)
   * Ethereum Layer-1 scaling (Eth2 PoS/Sharding)
   * [Ethereum Layer-2 scaling solutions](https://ethereum.by/en/developers/docs/layer-2-scaling/#types)
       1. State Channels
       2. Rollups

          A. *Optimistic Rollups*
            - **Arbitrum**
            - Optimism
            - Polygon

          B. *Zero-Knowledge Rollups*
            - **zkSync 2.0**
            - Starkware
            - Aztec
            - ZKSwap
            - Hermez
  ...

### References

* [L2BEAT](https://l2beat.com/#about)
* [L2 Risks](https://l2beat.com/?view=risk)
* [L2 Fees](https://l2fees.info/)
* [L2 Stats](https://cryptostats.community/)
* [An Incomplete Guide to Rollups](https://vitalik.ca/general/2021/01/05/rollup.html)
* [Arbitrum (Optimistic Rollups)](https://developer.offchainlabs.com/docs/rollup_basics)
* [zkSync (Zero-Knowledge Rollups)](https://zksync.io/zkevm/#what-is-a-zk-rollup)

-----

## zkSync

**A deeper dive into zkSync 2.0 architecture**

> zkSync’s zkRollup technology combined with Eth2 data sharding is the endgame, hitting 100,000+ TPS without sacrifices on any of the 4 factors (security, decentralization, programmability, scalability).

You may have heard of the blockchain trilemma, but when it comes to scaling Ethereum, there’s a 4th factor: programmability. All current scaling solutions reside on a spectrum of sacrificing some security, decentralization, and programmability for scalability. The design of zkSync 2.0 maximizes on all 4 features with the combination of the following 2 technological breakthroughs:

1. zk EVM: The engine powering our EVM-compatible zkRollup, the only solution with L1 security and solidity smart contract support.
2. zkPorter: An off-chain data availability system with 2 orders of magnitude more scalability than rollups.

* [](https://rinkeby.zksync.io/)
* [](https://zksync.io/api/sdk/js/)
* [zkEVM FAQ](https://zksync.io/zkevm/)

**Rinkeby Testnet**

[zkSync 2.0 Rinkeby Block Explorer](https://zksync2-alpha.zkscan.io/) [hosted by Matterlabs](https://blog.matter-labs.io/zksync-2-0-hello-ethereum-ca48588de179)

> The next release will include our Web3 API implementation, which will be compatible with the Web3 standard as defined by the Ethereum documentation.

**Signing Transactions**

Transactions in zkSync 2.0 can be authorized in 2 ways (in addition to the priority queue mechanism):

1. Users can sign transactions with their normal Ethereum wallets (such as Metamask or any WalletConnect one) by signing an EIP712 message.
2. Any account can set up a public key to create our internal Schnorr signatures to sign transactions. This allows smart-contract based wallets to perform interactions with zkSync 2.0 without the extra costs of sending L1 messages.

**Precompiles**

The mechanism of "precompiles" is planned, but will be released later on. We plan to support keccak256, sha256 hashes, and ECDSA recovery primitives first.


## Arbitrum

* [Arbitrum One (Mainnet) Bridge](https://bridge.arbitrum.io/)
* [RinkArby Testnet Bridge](https://bridge.arbitrum.io/)
* [Contract Development](https://developer.offchainlabs.com/docs/contract_deployment)
* [Arbitrum Integrates The Graph](https://thegraph.com/blog/arbitrum-graph)

**Running a Node**

[Running full node for Arbitrum One](https://developer.offchainlabs.com/docs/running_node)

```
rm -rf ${HOME}/.arbitrum/rinkeby
mkdir -p ${HOME}/.arbitrum/rinkeby
chmod -fR 777 ${HOME}/.arbitrum/rinkeby

docker run --rm -it  \
  -v ${HOME}/.arbitrum/rinkeby/:/home/user/.arbitrum/rinkeby \
  -p 0.0.0.0:8547:8547 \
  -p 0.0.0.0:8548:8548 \
  offchainlabs/arb-node:v1.1.2-cffb3a0 \
  --l1.url https://rinkeby.infura.io/v3/1c91...
```
