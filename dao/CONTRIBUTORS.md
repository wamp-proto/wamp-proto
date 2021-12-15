# WAMP Contributors

## Testing

### GitHub Access Token

[Create a new personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) [here](https://github.com/settings/tokens/new) with permissions:

* `repo:public_repo`
* `user:email`

Add your [GITHUB_TOKEN](https://docs.github.com/en/actions/security-guides/automatic-token-authentication) to your env:

```
export GITHUB_TOKEN=ghp_9z01..
```

### Create Contributors List

```
(cpy310_1) oberstet@intel-nuci7:~/scm/wamp-proto/wamp-proto/dao$ make wamp_dao_contributors
python wamp_dao_contrib.py --output wamp-dao-contrib.json
2021-12-15T22:05:27+0100    master @ wamp-proto/wamp-proto ..
2021-12-15T22:05:28+0100 WEP002: 1 repos with 424 stars, 93 forks, 39 contributors and 99 open issues
2021-12-15T22:05:29+0100    master @ crossbario/crossbar ..
2021-12-15T22:05:31+0100    master @ crossbario/txaio ..
2021-12-15T22:05:32+0100    master @ crossbario/autobahn-python ..
2021-12-15T22:05:35+0100    master @ crossbario/zlmdb ..
2021-12-15T22:05:36+0100    master @ crossbario/cfxdb ..
2021-12-15T22:05:36+0100 WEP010: 5 repos with 4337 stars, 1040 forks, 147 contributors and 493 open issues
2021-12-15T22:05:36+0100    master @ crossbario/autobahn-js ..
2021-12-15T22:05:38+0100    master @ crossbario/autobahn-java ..
2021-12-15T22:05:39+0100    master @ crossbario/autobahn-cpp ..
2021-12-15T22:05:40+0100 WEP011: 3 repos with 3084 stars, 764 forks, 101 contributors and 170 open issues
2021-12-15T22:05:40+0100
2021-12-15T22:05:40+0100 Written 12007 bytes to output file wamp-dao-contrib.json
jq . wamp-dao-contrib.json > wamp-dao-contrib-pp.json
```

## Allocation

Per WEP (WEP002, WEP010, WEP011) OR per repository and per contributor,
allocate WMP Tokens and WAMP Contributor NFTs:

- top3 contributor: xx WMP and GOLD
- top12 contributor: xx WMP and SILVER
- contributor: xx WMP and BRONCE

Total contributors: 39 + 147 + 101 = 287

- **9 GOLD** (x1)
- **36 SILVER** (x4)
- **287 BRONCE** (x8)

**Total NFTs: 332**
