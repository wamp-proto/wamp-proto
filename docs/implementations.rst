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


Client libraries
----------------

The following table lists **WAMP compliant client library implementations**.

.. note::

    For each implementation, an "x" marks a WAMP role supported by
    the implementation. The last column marks principle support
    for features from *WAMP Advanced Profile*.

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
CppWAMP_            C++ 11                              CppWAMP is a WAMP V2 implementation in C++11.
haskell-wamp_       Haskell                             An experimental Haskell implementation of WAMP Basic Profile.
kraftfahrstrasse_   TypeScript                          Modern WAMP Client library for browsers and node utilizing native ES6+.
jawampa_            Java + RxJava, Netty                A Java WAMP implementation based on `Netty <http://netty.io/>`_ and `RxJava <https://github.com/ReactiveX/RxJava>`_. Both Client and Router roles.
Loowy_              LUA, lib-ev                         LUA WAMP client implementation on top of lua-websockets and lib-ev.
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
WampSharp_          C#                                  C# implementation of WAMP: both client and router roles, both JSON and `MessagePack <http://msgpack.org/>`_ support.
wampy_              Python                              Python implementation for classic blocking Python applications.
wampyjs_            JavaScript                          WAMP Client library for browsers using callbacks. See `here <https://github.com/KSDaemon/wampy.js#quick-comparison-to-other-libs>`_ for comparison to AutobahnJS.
==================  ==================================  =====================


Routers
-------



.. _akka-wamp: https://github.com/angiolep/akka-wamp
.. _AngularWAMP: https://github.com/voryx/angular-wamp
.. _AutobahnCpp: https://github.com/crossbario/autobahn-cpp
.. _AutobahnJava: https://github.com/crossbario/autobahn-java
.. _AutobahnJS: https://github.com/crossbario/autobahn-js
.. _AutobahnPython: https://github.com/crossbario/autobahn-python
.. _awre: https://github.com/bwegh/awre
.. _Backbone: https://github.com/darrrk/backbone.wamp
.. _connectanum: http://www.connectanum.com/
.. _CppWAMP: https://github.com/ecorm/cppwamp
.. _haskell-wamp: https://github.com/mulderr/haskell-wamp
.. _jawampa: https://github.com/Matthias247/jawampa
.. _kraftfahrstrasse: https://github.com/Verkehrsministerium/kraftfahrstrasse
.. _Loowy: https://github.com/KSDaemon/Loowy
.. _MDWamp: https://github.com/mogui/MDWamp
.. _Minion: https://github.com/Vinelab/minion
.. _Nexus: https://github.com/gammazero/nexus
.. _p5-Net-WAMP: https://github.com/FGasper/p5-Net-WAMP
.. _ruby_wamp_client: https://github.com/ericchapman/ruby_wamp_client
.. _rx-wamp: https://github.com/paulpdaniels/rx.wamp
.. _Thruway: https://github.com/voryx/Thruway
.. _Turnpike: https://github.com/jcelliott/turnpike
.. _Spell: https://github.com/MyMedsAndMe/spell
.. _Swamp: https://github.com/iscriptology/swamp
.. _wampcc: https://github.com/darrenjs/wampcc
.. _WAMP_POCO: https://github.com/rafzi/WAMP_POCO
.. _wamped: https://github.com/alvistar/wamped
.. _WampSharp: https://github.com/Code-Sharp/WampSharp
.. _wampy: https://github.com/noisyboiler/wampy
.. _wampyjs: https://github.com/KSDaemon/wampy.js
