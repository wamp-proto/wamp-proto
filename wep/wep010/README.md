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

and covers the router software and library components contained in the following Crossbar.io **Source
Code** repositories:

* [crossbar](https://github.com/crossbario/crossbar/issues)
* [autobahn-python](https://github.com/crossbario/autobahn-python/issues)
* [txaio](https://github.com/crossbario/txaio/issues)
* [zlmdb](https://github.com/crossbario/zlmdb/issues)
* [cfxdb](https://github.com/crossbario/cfxdb/issues)

> Crossbar.io is a Python 3 application with [140+ direct and indirect dependencies](https://github.com/crossbario/crossbar/blob/master/requirements-pinned.txt) on other Python packages. The above repositories contain all source code created and maintained by this project.

Bigger recurring tasks include building and publishing:

* Crossbar.io **Software Packages**
* Crossbar.io **Software Binaries**
* Crossbar.io **Machine Images**
* Crossbar.io **Device Images**

with tasks depending on each other as in this *CI-Release Pipeline*:

```
Source Code
    |
    +-- Software Packages (wheel *)
             |
             +-- Software Binaries (Docker, snap, EXE **)
                      |
                      +--[Docker]-- Machine Images (AMI, VirtualBox ***)
                      |
                      +--[snap]-- Device Images (Yocto)
```

> *: created with [setuptools](https://github.com/pypa/setuptools), [pip](https://pip.pypa.io/), [wheel](https://github.com/pypa/wheel)
> **: created with [Docker](https://www.docker.com/), [Snapcraft](https://snapcraft.io/), [PyInstaller](https://www.pyinstaller.org/)
> ***: created with [Packer](https://www.packer.io/), [Vagrant](https://www.vagrantup.com/), [VirtualBox](https://www.virtualbox.org/)

and more tasks:

* Crossbar.io **Documentation**
* Crossbar.io **Workbench**
* Crossbar.io **Samples and Demos**


## Crossbar.io Software Packages

Crossbar.io has currently 141 direct and indirect Python packages as dependencies:

```
oberstet@intel-nuci7:~/scm/wamp-proto/wamp-proto$ wc -l ~/scm/crossbario/crossbar/LICENSES-OSS
142 /home/oberstet/scm/crossbario/crossbar/LICENSES-OSS
```

*Crossbar.io Wheels* is the subtask of creating and operating build automation for official Crossbar.io Python packages, including direct and indirect dependencies, published as Python wheels on a self-hosted Python package index that can be used with [pip](https://pip.pypa.io/en/stable/).


## Crossbar.io Software Binaries

> The build scripts and repository for this section is currently still private to Crossbar.io GmbH, but will be released publicitly when the WAMP DAO receives and accepts donation of IP by Crossbar.io GmbH.

* [Crossbar.io Binaries](https://github.com/crossbario/crossbar-binaries)

*Crossbar.io Binaries* is the subtask of creating and operating build automation for official Crossbar.io binary packages published by the WAMP DAO in different formats:

1. Docker images (x86-64, arm64)
2. Snap packages (x86-64, arm64)
3. Single-file executables (x86-64)

*The binary packages are built from sources (upstream and our own projects) and come fully enabled with federation in the WAMP Network.*

*The binary packages are licensed under an EULA published by the WAMP DAO (tbd) which allows decentralized and permissionless access to the WAMP Network.*


## Crossbar.io Machine Images

*Crossbar.io Machine Images* is the subtask of creating and operating build automation for official Crossbar.io VM images published by the WAMP DAO in different formats:

1. [Amazon AMI](https://www.packer.io/docs/builders/amazon) (x86-64, arm64)
2. [Azure Virtual Machine Image](https://www.packer.io/docs/builders/azure) (x86-64)
3. [VMware](https://www.packer.io/docs/builders/vmware) (x86-64)
4. [VirtualBox](https://www.packer.io/docs/builders/virtualbox) (x86-64)

[Packer](https://www.packer.io/) allows to automate image creation for [various VM target platforms](https://www.packer.io/docs/builders), including all of above.

*The VM images are built from Docker images and come fully enabled with federation in the WAMP Network.*

*The VM images are licensed under an EULA published by the WAMP DAO (tbd) which allows decentralized and permissionless access to the WAMP Network.*


## Crossbar.io Workbench

> The build scripts and repository for this section is currently still private to Crossbar.io GmbH, but will be released publicitly when the WAMP DAO receives and accepts donation of IP by Crossbar.io GmbH.

* [Crossbar.io Workbench](https://github.com/crossbario/crossbar-workbench)

*Crossbar.io Workbench* is the subtask of creating and operating build automation for official Crossbar.io Workbench binary packages and machine images published by the WAMP DAO.

*These binary packages are built from sources (upstream and our own projects) and come fully enabled with federation in the WAMP Network.*

*The binary packages are licensed under an EULA published by the WAMP DAO (tbd) which allows decentralized and permissionless access to the WAMP Network.*

1. Docker image (x86-64)
2. [VirtualBox VM image](https://www.packer.io/docs/builders/virtualbox) (x86-64)


## Crossbar.io Documentation

Consolidate, polish and close gaps in Crossbar.io documentation:

* [docs](https://github.com/crossbario/crossbar/tree/master/docs)
* [docs-old](https://github.com/crossbario/crossbar/tree/master/docs-old)
* [docs-cfx](https://github.com/crossbario/crossbar/tree/master/docs-cfx)

and

* [Cookiecutter Autobahn C++](https://api.github.com/repos/crossbario/cookiecutter-autobahn-cpp)
* [Cookiecutter Autobahn Java](https://api.github.com/repos/crossbario/cookiecutter-autobahn-java)
* [Cookiecutter Autobahn JS](https://api.github.com/repos/crossbario/cookiecutter-autobahn-js)
* [Cookiecutter Autobahn Pyython](https://api.github.com/repos/crossbario/cookiecutter-autobahn-python)
* [Cookiecutter Crossbar.io](https://api.github.com/repos/crossbario/cookiecutter-crossbar)
* [Cookiecutter CrossbarFX](https://api.github.com/repos/crossbario/cookiecutter-crossbarfx)
* [Cookiecutter CrossbarFX Cloud](https://api.github.com/repos/crossbario/cookiecutter-crossbarfx-cloud)
* [Cookiecutter Nexus Go](https://api.github.com/repos/crossbario/cookiecutter-nexus-go)
* [Cookiecutter Thruway](https://api.github.com/repos/crossbario/cookiecutter-thruway)
* [Cookiecutter WAMPSharp](https://api.github.com/repos/crossbario/cookiecutter-wampsharp)
* [Cookiecutter XBR JS](https://api.github.com/repos/crossbario/cookiecutter-xbr-javascript)
* [Cookiecutter XBR Python](https://api.github.com/repos/crossbario/cookiecutter-xbr-python)


## Samples and Demos

* [Crossbar.io Examples](https://github.com/crossbario/crossbar-examples)
* [Crossbar.io IoT Cookbook](https://github.com/crossbario/iotcookbook)
* [Data Square Platform: Code examples, notebooks and tutorials](https://github.com/crossbario/dsq-examples)
* [IDMA Examples](https://api.github.com/repos/crossbario/idma-examples)
* [Katakoda Example](https://api.github.com/repos/crossbario/katacoda-demos)
