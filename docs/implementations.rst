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
    - Want your WAMP implementation listed here? Please join the `mailing list <https://groups.google.com/group/wampws>`_
      or `Gitter chat <https://gitter.im/wamp-proto/wamp-proto>`_ and introduce your project.


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
Backbone_           JavaScript                          Allows two-way synchronisation of Backbone models & collections between frontends and backends.
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
Turnpike_           Go                                  A Go implementation of WAMP V2
Spell_              Elixir/Erlang                       Spell is a WAMP library built using Elixir, running on the Erlang VM.
Swamp_              Swift                               WAMP client library in pure Swift using Starscream and SwiftyJSON.
wampcc_             C++                                 A C++ WAMP library that aims to depend only on C libraries. Includes a basic router.
WAMP_POCO_          C++                                 A fork of AutobahnCpp that is using `POCO <http://pocoproject.org/>`_ instead of Boost.
wamped_             C++                                 Intended for running on `ARM mbed OS <https://www.mbed.com/en/>`_. Experimental.
WAMPexClient_       Elixir                              Elixir client library that implements the complete client Basic Profile and much of the Advanced Profile.
WampSyncClient_      PHP                                 Synchronous (blocking) PHP client implementing Caller and Publisher roles
wamprx.js_          TypeScript                          Simple WAMP TypeScript client-side implementation (of course also usable in JavaScript). It heavily relies on RxJS.
WampSharp_          C#                                  C# implementation of WAMP: both client and router roles, both JSON and `MessagePack <http://msgpack.org/>`_ support.
wampy_              Python                              Python implementation for classic blocking Python applications.
wampy.js_           JavaScript                          WAMP JavaScript client for browsers and node.js using callbacks. See `here <https://github.com/KSDaemon/wampy.js#quick-comparison-to-other-libs>`_ for comparison to AutobahnJS.
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
jawampa_            Java + RxJava, Netty                A Java WAMP implementation based on `Netty <http://netty.io/>`_ and `RxJava <https://github.com/ReactiveX/RxJava>`_. Both Client and Router roles.
KWAMP_              Kotlin                              A Kotlin WAMP router (aims for basic profile).
Nexus_              Go                                  Router implementation for Go. (also includes a client implementation)
NighlifeRabbit_     JavaScript, NodeJS                  Router implementation for `NodeJS <http://nodejs.org/>`_, MIT licensed.
Thruway_            PHP                                 Thruway is a WAMP library built in PHP that provides both Client and Router roles.
Turnpike_           Go                                  turnpike is a WAMP v2 router implemented in Go.
wamp2spring_        Java, Spring                        A Java implementation built on top of the Spring 5 WebSocket support.
wampcc_             C++                                 A C++ WAMP library that aims to depend only on C libraries, making it easier to work and build on a range of platforms.
wamprt_             JavaScript, NodeJS                  <td class="notes">Router only implementation for `NodeJS <http://nodejs.org/>`_ created by `Orange <http://opensource.orange.com/home>`_.
WampSharp_          C#                                  C# router implementation of WAMP v2, both JSON and `MessagePack <http://msgpack.org/>`_ support.
Wiola_              Lua                                 Router implementation in `Lua <http://www.lua.org/>`_, using the power of Lua/Nginx, WebSocket and `Redis <http://redis.io/>`_ as cache store.
==================  ==================================  =====================


.. _akka-wamp: https://github.com/angiolep/akka-wamp
.. _AngularWAMP: https://github.com/voryx/angular-wamp
.. _AutobahnCpp: https://github.com/crossbario/autobahn-cpp
.. _AutobahnJava: https://github.com/crossbario/autobahn-java
.. _AutobahnJS: https://github.com/crossbario/autobahn-js
.. _AutobahnPython: https://github.com/crossbario/autobahn-python
.. _awre: https://github.com/bwegh/awre
.. _Backbone: https://github.com/darrrk/backbone.wamp
.. _Bondy: https://gitlab.com/leapsight/bondy
.. _Bonefish: https://github.com/tplgy/bonefish
.. _Cargotube: https://github.com/CargoTube/cargotube
.. _connectanum: https://www.connectanum.com/
.. _connectanum-dart: https://pub.dev/packages/connectanum/
.. _CppWAMP: https://github.com/ecorm/cppwamp
.. _Crossbar: https://crossbar.io
.. _CrossbarFX: https://crossbario.com
.. _Erwa: https://github.com/bwegh/erwa
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
.. _WampSyncClient: https://github.com/jszczypk/WampSyncClient
.. _wamprt: https://github.com/Orange-OpenSource/wamp.rt
.. _wamprx.js: https://github.com/Jopie64/wamprx.js
.. _WampSharp: https://github.com/Code-Sharp/WampSharp
.. _wampy: https://github.com/noisyboiler/wampy
.. _wampy.js: https://github.com/KSDaemon/wampy.js
.. _Wiola: http://ksdaemon.github.io/wiola/
