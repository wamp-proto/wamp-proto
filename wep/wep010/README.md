# WEP010 - Crossbar.io Maintenance

The purpose of this WEP is to properly maintain the Crossbar.io router software,
which includes the following activities:

1. fix bugs
2. close gaps
3. add small features
4. add samples and demos
5. add unit and functional tests
6. improve documentation
7. operate and manage CI
7. build and publish official binaries
8. maintain and publish website
9. operate and supervise forum

and covers the router software and library components contained in the following
code repositories:

* [crossbar](https://github.com/crossbario/crossbar/issues)
* [autobahn-python](https://github.com/crossbario/autobahn-python/issues)
* [txaio](https://github.com/crossbario/txaio/issues)
* [zlmdb](https://github.com/crossbario/zlmdb/issues)
* [cfxdb](https://github.com/crossbario/cfxdb/issues)

> Crossbar.io is a Python 3 application with [100+ direct and indirect dependencies](https://github.com/crossbario/crossbar/blob/master/requirements-pinned.txt) on other Python packages. The above repositories contain all packages created by this project.


## Crossbar.io Documentation

Consolidate, polish and close gaps in Crossbar.io documentation:

* [docs](https://github.com/crossbario/crossbar/tree/master/docs)
* [docs-old](https://github.com/crossbario/crossbar/tree/master/docs-old)
* [docs-cfx](https://github.com/crossbario/crossbar/tree/master/docs-cfx)


## Crossbar.io Binaries

> The build scripts and repository for this section is currently still private to Crossbar.io GmbH, but will be released publicitly when the WAMP DAO receives and accepts donation of IP by Crossbar.io GmbH.

* [Crossbar.io Binaries](https://github.com/crossbario/crossbar-binaries)

*Crossbar.io Binaries* is the subtask of creating and operating build automation for official Crossbar.io binary packages published by the WAMP DAO in different formats:

1. Docker images
2. Snap packages
3. Single-file executables

*The binary packages are built from sources (upstream and our own projects) and come fully enabled with federation in the WAMP Network.*

*The binary packages are licensed under an EULA published by the WAMP DAO (tbd) which allows decentralized and permissionless access to the WAMP Network.*


## Crossbar.io Machine Images

*Crossbar.io Machine Images* is the subtask of creating and operating build automation for official Crossbar.io VM images published by the WAMP DAO in different formats:

1. [Amazon AMI](https://www.packer.io/docs/builders/amazon)
2. [Azure Virtual Machine Image](https://www.packer.io/docs/builders/azure)
3. [VMware](https://www.packer.io/docs/builders/vmware)
4. [VirtualBox](https://www.packer.io/docs/builders/virtualbox)

[Packer](https://www.packer.io/) allows to automate image creation for [various VM target platforms](https://www.packer.io/docs/builders), including all of above.

*The VM images are built from Docker images and come fully enabled with federation in the WAMP Network.*

*The VM images are licensed under an EULA published by the WAMP DAO (tbd) which allows decentralized and permissionless access to the WAMP Network.*


## Crossbar.io Workbench

> The build scripts and repository for this section is currently still private to Crossbar.io GmbH, but will be released publicitly when the WAMP DAO receives and accepts donation of IP by Crossbar.io GmbH.

* [Crossbar.io Workbench](https://github.com/crossbario/crossbar-workbench)

*Crossbar.io Workbench* is the subtask of creating and operating build automation for official Crossbar.io Workbench binary packages published by the WAMP DAO as Docker images.

*Crossbar.io Workbench*


*These binary packages are built from sources (upstream and our own projects) and come fully enabled with federation in the WAMP Network.*

*The binary packages are licensed under an EULA published by the WAMP DAO (tbd) which allows decentralized and permissionless access to the WAMP Network.*
