# The WAMP DAO

## Metamask

The following describes an easy and still reasonably secure way to interact with Ethereum from nothing more than a browser.

Of course there are multiple ways to increase the level of security further, but since we use a system that requires N out of M signatures by members, having the wallet of a single member stolen or lost is not a fatal error.

So as a browser, best use Firefox or Chrome or a variant of these browsers, and the go an add the [Metamask](https://metamask.io/) browser extension.

Once you start the extension the first time, it will give you the option to generate a new 12-(or more)-word **Secret Recovery Phrase** ("create a wallet"), which is crucial:


Secure your wallet
Before getting started, watch this short video to learn about your Secret Recovery Phrase and how to keep your wallet safe.


* if you loose your seed


## DAO Multisigs

Until the DAO is fully decentralized, and all on-chain transactions are executed directly from within a DAO proposal accepted on-chain, such execution of DAO actions are performed from multisig accounts controlled by founding DAO members.

There are two multisig accounts.

* Admin Multisig
* Treasury Multisig

The Admin Multisig owns all smart contracts deployed and assets configured for the DAO, which includes:

* [ERC20/ERC1155 contracts](https://docs.openzeppelin.com/contracts/4.x/tokens) for tokens
* [Governor contract](https://docs.openzeppelin.com/contracts/4.x/api/governance) for the DAO itself
* [Liquidity pool](https://docs.balancer.fi/products/balancer-pools/liquidity-bootstrapping-pools-lbps) [owned](https://dev.balancer.fi/resources/deploy-pools-from-factory/creation) by the DAO

The Treasury Multisig owns all assets of the DAO, which includes:

* USD stable coin tokens (DAI in particular)
* DAO governance tokens (ERC20)
* DAO NFTs (ERC1155)

### Gnosis Safe

The DAO uses [Gnosis Safe](https://gnosis-safe.io/) based Multisig [Contract Accounts](https://docs.gnosis-safe.io/introduction/the-programmable-account/eoas-vs.-contract-accounts).

Multisigs allow [safe management](https://blog.gnosis.pm/how-to-securely-manage-company-crypto-funds-with-gnosis-safe-multisig-8b3f67485985
) of DAO assets and actions until the DAO becomes fully decentralized, that is managed via on-chain governance with direct on-chain execution.

One can easily [send digital assets to a Safe](https://help.gnosis-safe.io/en/articles/3922053-how-can-i-receive-funds), this includes:

* Ether (ETH)
* ERC-20 Tokens (DAI, USDC, UNI, ..)
* ERC-721 Tokens (NFT's)

> Important: Make sure to only send ETH, ERC-20 tokens and ERC-721 tokens to a Safe. See [here](https://help.gnosis-safe.io/en/articles/4970832-supported-asset-types) and [here](https://help.gnosis-safe.io/en/articles/3964868-erc-721-nfts).

**References**

* [Gnosis Safe - Make dealing with crypto a less scary thing](https://www.youtube.com/watch?v=9gyZRq162A8)
* [What are Safe Apps?](https://help.gnosis-safe.io/en/articles/4022022-what-are-safe-apps)
* [Introducing Gnosis Safe Apps](https://blog.gnosis.pm/introducing-gnosis-safe-apps-faef908f69c6)
* [Gnosis Safe Spending Limits](https://blog.gnosis.pm/gnosis-safe-spending-limits-f05b775d06b3)
* [Set up and use Spending Limits](https://help.gnosis-safe.io/en/articles/4667979-set-up-and-use-spending-limits)
* [CSV Airdrop as Gnosis Safe App](https://github.com/bh2smith/safe-airdrop)

### Admin Multisig

Admin Multisig (3 of 5) draft list:

1. [x] oberstet	(de)
2. [ ] meejah (ca)
3. [ ] om26er (pk)
4. [ ] KSDaemon (ru)
5. [ ] gammazero (uk)

### Treasury Multisig

Treasury Multisig (4 of 7) draft list:

1. [x] oberstet	(de)
2. [x] stephansil (de)
3. [ ] albertxos (de)
4. [ ] meejah (ca)
5. [ ] aramallo	(uk)
6. [ ] ?
7. [ ] ?

* estan	(se)
* konsultaner (de)
* ecorm	(ca)
* ?

## Radicle

https://docs.radicle.xyz/docs/what-is-radicle.html
https://radicle.xyz/blog/radicle-orgs.html
