:github_url: https://github.com/wamp-proto/wamp-proto/edit/master/docs/implementations.rst

.. _Implementations:

Implementations
===============

Get started with WAMP by choosing **client libraries** and a **router**:

* To *write application components* in your favorite language, you will need a **WAMP client library**
* To actually *run your application* consisting of components, you will need a **WAMP router**

In theory, you should be able to use any combination and mix of WAMP client libraries with routers
and select the best or most fitting for each. That's one promise of WAMP, one freedom of choice.

.. note::

    - You can choose your WAMP router independently of the programming language you want to write your
      components in since routers do not run application code directly.
    - Want your WAMP implementation listed here? Please open `issue <https://github.com/wamp-proto/wamp-proto/issues/new>`_
      on github and introduce your project or even create a pull request with addition to this
      `file <https://github.com/wamp-proto/wamp-proto/edit/master/docs/implementations.rst>`_.


Libraries
---------

The following table lists WAMP compliant **client library implementations**.

==================  ==================================  =====================
Name                Language/Run-time                   Description
==================  ==================================  =====================
akka-wamp_          Scala, Java 8 and Akka              WAMP implementation written in Scala with Akka HTTP, usable from Java 8.
AngularWAMP_        JavaScript                          AngularWAMP is wrapper for AutobahnJS that provides deeper integration for AngularJS apps.
AutobahnCpp_        C++ 11 and Boost/ASIO               C++ 11 implementation using Futures, Continuations and Lambdas. Runs on top of `Boost <http://www.boost.org>`_ and `ASIO <http://think-async.com/>`_.
AutobahnJava_       Java 8, Android or Netty            WAMP client library for Java and Android applications based on Java 8 ``CompletableFuture``.
AutobahnJS_         Javascript, HTML5 and NodeJS        WAMP client library for both browsers (HTML5) and `NodeJS <http://nodejs.org/>`_ using Promises.
AutobahnPython_     Python 2/3, Twisted and asyncio     WAMP client library + WebSocket client/server impl. for Python 2 and 3, on `Twisted <https://twistedmatrix.com>`_ and `asyncio <https://docs.python.org/3/library/asyncio.html>`_.
awre_               Erlang                              awre is a WAMP V2 implementation in `Erlang <http://www.erlang.org/>`_ with client roles.
Backbone.wamp_      JavaScript                          Allows two-way synchronisation of Backbone models & collections between frontends and backends.
connectanum_        Java, Netty                         A Java WAMP implementation based on Netty. Both Client and Router roles.
connectanum-dart_   Dart, Flutter                       A WAMP client implementation for the `dart language <https://dart.dev/>`_ and `flutter <https://flutter.dev/>`_ projects.
CppWAMP_            C++ 11                              CppWAMP is a WAMP V2 implementation in C++11.
haskell-wamp_       Haskell                             An experimental Haskell implementation of WAMP Basic Profile.
kraftfahrstrasse_   TypeScript                          Modern WAMP Client library for browsers and node utilizing native ES6+.
KWAMP_              Kotlin                              A Kotlin WAMP client (aims for basic profile).
jawampa_            Java + RxJava, Netty                A Java WAMP implementation based on `Netty <http://netty.io/>`_ and `RxJava <https://github.com/ReactiveX/RxJava>`_. Both Client and Router roles.
Loowy_              Lua, lib-ev                         Lua WAMP client implementation on top of lua-websockets and lib-ev.
MDWamp_             Objective-C                         Client library for iOS apps built on `SocketRocket <https://github.com/square/SocketRocket>`_ for WebSocket.
Minion_             PHP                                 Client library and command line tool with `Laravel <http://laravel.com/>`_ support. Based on `Thruway <https://github.com/voryx/Thruway>`_.
Nexus_              Go                                  A full-feature WAMP client written in Go (also a Router).
p5-Net-WAMP_        Perl 5                              A WAMP implementation in Perl. See the `docs <https://metacpan.org/pod/Net::WAMP>`_ for details.
ruby_wamp_client_   Ruby                                A WAMP client for Ruby
rx-wamp_            JavaScript                          A `RxJS <https://github.com/Reactive-Extensions/RxJS>`_ wrapper library for WAMP. Built on AutobahnJS, running in the browser and NodeJS.
Thruway_            PHP                                 Thruway is a WAMP library built in PHP that provides both Client and Router roles.
Octamp_             PHP                                 A Wamp client written in PHP using extension Swoole / Open Swoole
Turnpike_           Go                                  A Go implementation of WAMP V2
Spell_              Elixir/Erlang                       Spell is a WAMP library built using Elixir, running on the Erlang VM.
Swamp_              Swift                               WAMP client library in pure Swift using Starscream and SwiftyJSON.
wampcc_             C++                                 A C++ WAMP library that aims to depend only on C libraries. Includes a basic router.
WAMP_POCO_          C++                                 A fork of AutobahnCpp that is using `POCO <http://pocoproject.org/>`_ instead of Boost.
wamped_             C++                                 Intended for running on `ARM mbed OS <https://www.mbed.com/en/>`_. Experimental.
WAMPexClient_       Elixir                              Elixir client library that implements the complete client Basic Profile and much of the Advanced Profile.
wamplv_             LabVIEW / G                         A WAMP client written in National Instrument's `LabVIEW <https://en.wikipedia.org/wiki/LabVIEW>`_, also available as a `VIPM package <https://www.vipm.io/package/samangh_lib_wamplv_wamp_client/>`_.
WampSyncClient_     PHP                                 Synchronous (blocking) PHP client implementing Caller and Publisher roles
wamprx.js_          TypeScript                          Simple WAMP TypeScript client-side implementation (of course also usable in JavaScript). It heavily relies on RxJS.
WampSharp_          C#                                  C# implementation of WAMP: both client and router roles, both JSON and `MessagePack <http://msgpack.org/>`_ support.
wampy_              Python                              Python implementation for classic blocking Python applications.
wampy.js_           JavaScript                          Feature-rich lightweight WAMP Javascript implementation for browsers and node.js.
wamp_async_         Rust                                Rust client library. It features ergonomic async API
xconn-dart_         Dart, Flutter                       A Dart WAMP client library with full Flutter support, featuring async APIs and cross-platform compatibility.
xconn-go_           Go                                  WAMP v2 Router and Client for Go.
xconn-kotlin_       Kotlin                              WAMP client for Kotlin.
xconn-python_       Python                              A Python WAMP client library with both synchronous and asynchronous support.
xconn-rust_         Rust                                WAMP client in Rust. It includes two implementations one is sync and the other async.
xconn-swift_        Swift                               A Swift WAMP client library designed for iOS and macOS, with async/await support.
xconn-ts_           TypeScript                          A TypeScript WAMP client library built for both browser and Node.js environments.
==================  ==================================  =====================


Routers
-------

The following table lists WAMP compliant **router implementations**.

==================  ==================================  =====================
Name                Language/Run-time                   Description
==================  ==================================  =====================
akka-wamp_          Scala, Java 8 and Akka              A Scala implementation of a basic WAMP router.
Bonefish_           C++, Boost/ASIO                     WAMP router based on C++11 and Boost.Asio. Also usable as a library, Apache 2.0 licensed.
connectanum_        Java, Netty                         A Java WAMP implementation based on Netty. Both Client and Router roles.
Crossbar_           Python (PyPy), Twisted              Crossbar.io WAMP router and microservice middleware. By the creators of WAMP and Autobahn.
CrossbarFX_         Python (PyPy), Twisted              CrossbarFX enterprise WAMP router with central management, edge device platform and clustering.
Cargotube_          Erlang                              A software router in Erlang implementing the wamp.ws protcol (successor of Erwa).
Bondy_              Erlang                              Leapsight Bondy is an open source distributed API Gateway, WAMP Router and networking platform for microservices and IoT applications written in Erlang. It provides scaleable clustering capabilities via TCP/IP using Partisan, Plumtree Epidemic Broadcast Trees and an eventually consistent data store.
Erwa_               Erlang                              Erwa is a WAMP V2 implementation: Erwa will be archived soon, please consider using CargoTube.
fox-wamp_           JavaScript, NodeJS                  Customizable WAMP Router.
jawampa_            Java + RxJava, Netty                A Java WAMP implementation based on `Netty <http://netty.io/>`_ and `RxJava <https://github.com/ReactiveX/RxJava>`_. Both Client and Router roles.
KWAMP_              Kotlin                              A Kotlin WAMP router (aims for basic profile).
Nexus_              Go                                  Router implementation for Go. (also includes a client implementation)
NighlifeRabbit_     JavaScript, NodeJS                  Router implementation for `NodeJS <http://nodejs.org/>`_, MIT licensed.
OctampWamp_         PHP, OpenSwoole                     Octamp WAMP is Router implementation of WAMP Protocol using PHP and OpenSwoole that is scalable, it uses Redis Pub/Sub to connect with other server.
Thruway_            PHP                                 Thruway is a WAMP library built in PHP that provides both Client and Router roles.
Turnpike_           Go                                  turnpike is a WAMP v2 router implemented in Go.
wamp2spring_        Java, Spring                        A Java implementation built on top of the Spring 5 WebSocket support.
wampcc_             C++                                 A C++ WAMP library that aims to depend only on C libraries, making it easier to work and build on a range of platforms.
wamprt_             JavaScript, NodeJS                  Router only implementation for `NodeJS <http://nodejs.org/>`_ created by `Orange <http://opensource.orange.com/home>`_.
WampSharp_          C#                                  C# router implementation of WAMP v2, both JSON and `MessagePack <http://msgpack.org/>`_ support.
Wiola_              Lua                                 Router implementation in `Lua <http://www.lua.org/>`_, using the power of Lua/Nginx, WebSocket and `Redis <http://redis.io/>`_ as cache store.
xconn-go_            Go                                  WAMP v2 Router and Client for Go.
==================  ==================================  =====================


Utilities
---------

The following table lists WAMP compliant utilities.

==================  ==================================  =====================
Name                Language/Run-time                   Description
==================  ==================================  =====================
wamp-cli_           JavaScript, NodeJS                  CLI tool to help building applications with WAMP
wampy.js_           JavaScript, NodeJS                  CLI tool built on top of Wampy.js library and exposes almost the same API to Command line charged with rich shell auto completion, description and examples. You can use it for testing WAMP API during development, debugging, or just exploring the new APIs.
wick_               Go                                  CLI tool to make WAMP RPCs and PubSub. Useful for developing WAMP Components and their testing.
wick-ui_            Dart, Flutter                       Web tool for testing WAMP APIs, Postman for WAMP.
==================  ==================================  =====================


.. _akka-wamp: https://github.com/angiolep/akka-wamp
.. _AngularWAMP: https://github.com/voryx/angular-wamp
.. _AutobahnCpp: https://github.com/crossbario/autobahn-cpp
.. _AutobahnJava: https://github.com/crossbario/autobahn-java
.. _AutobahnJS: https://github.com/crossbario/autobahn-js
.. _AutobahnPython: https://github.com/crossbario/autobahn-python
.. _awre: https://github.com/bwegh/awre
.. _Backbone.wamp: https://github.com/darrrk/backbone.wamp
.. _Bondy: https://bondy.io
.. _Bonefish: https://github.com/tplgy/bonefish
.. _Cargotube: https://github.com/CargoTube/cargotube
.. _connectanum: https://www.connectanum.com/
.. _connectanum-dart: https://pub.dev/packages/connectanum/
.. _CppWAMP: https://github.com/ecorm/cppwamp
.. _Crossbar: https://crossbar.io
.. _CrossbarFX: https://crossbario.com
.. _Erwa: https://github.com/bwegh/erwa
.. _fox-wamp: https://github.com/kalmyk/fox-wamp
.. _haskell-wamp: https://github.com/mulderr/haskell-wamp
.. _jawampa: https://github.com/Matthias247/jawampa
.. _KWAMP: https://github.com/LaurenceGA/kwamp
.. _kraftfahrstrasse: https://github.com/Verkehrsministerium/kraftfahrstrasse
.. _Loowy: https://github.com/KSDaemon/Loowy
.. _MDWamp: https://github.com/mogui/MDWamp
.. _Minion: https://github.com/Vinelab/minion
.. _NighlifeRabbit: https://github.com/christian-raedel/nightlife-rabbit
.. _Nexus: https://github.com/gammazero/nexus
.. _p5-Net-WAMP: https://github.com/FGasper/p5-Net-WAMP
.. _ruby_wamp_client: https://github.com/ericchapman/ruby_wamp_client
.. _rx-wamp: https://github.com/paulpdaniels/rx.wamp
.. _Thruway: https://github.com/voryx/Thruway
.. _Turnpike: https://github.com/jcelliott/turnpike
.. _Spell: https://github.com/MyMedsAndMe/spell
.. _Swamp: https://github.com/iscriptology/swamp
.. _wamp2spring: https://github.com/ralscha/wamp2spring
.. _wampcc: https://github.com/darrenjs/wampcc
.. _WAMP_POCO: https://github.com/rafzi/WAMP_POCO
.. _wamped: https://github.com/alvistar/wamped
.. _WAMPexClient: https://gitlab.com/entropealabs/wampex_client
.. _wamplv: https://github.com/samangh/wamplv
.. _WampSyncClient: https://github.com/jszczypk/WampSyncClient
.. _wamprt: https://github.com/Orange-OpenSource/wamp.rt
.. _wamprx.js: https://github.com/Jopie64/wamprx.js
.. _WampSharp: https://github.com/Code-Sharp/WampSharp
.. _wampy: https://github.com/noisyboiler/wampy
.. _wampy.js: https://github.com/KSDaemon/wampy.js
.. _Wiola: http://ksdaemon.github.io/wiola/
.. _wamp-cli: https://github.com/johngeorgewright/wamp-cli
.. _wamp_async: https://github.com/elast0ny/wamp_async
.. _wick: https://github.com/codebasepk/wick
.. _Octamp: https://github.com/cydrickn/octamp-client
.. _OctampWamp: https://github.com/octamp/wamp
.. _xconn-dart: https://github.com/xconnio/xconn-dart
.. _xconn-go: https://github.com/xconnio/xconn-go
.. _xconn-kotlin: https://github.com/xconnio/xconn-kotlin
.. _xconn-python: https://github.com/xconnio/xconn-python
.. _xconn-rust: https://github.com/xconnio/xconn-rust
.. _xconn-swift: https://github.com/xconnio/xconn-swift
.. _xconn-ts: https://github.com/xconnio/xconn-ts
.. _wick-ui: https://github.com/xconnio/wick-ui
