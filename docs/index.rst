:github_url: https://github.com/wamp-proto/wamp-proto/edit/master/docs/index.rst

.. _Home:

The Web Application Messaging Protocol
======================================

| |Spec| |Docs-CDN|

.. |Docs-CDN| image:: https://img.shields.io/badge/docs-cdn-brightgreen.svg?style=flat
    :target: https://wamp-proto.org/index.html

.. |Spec| image:: https://img.shields.io/badge/spec-latest-ff69b4.svg
    :target: wamp_latest_ietf.html

-------

Welcome to the Web Application Messaging Protocol (WAMP)!

WAMP is an open application level protocol that provides two
messaging patterns in one unified protocol:

* Routed **Remote Procedure Calls** and
* **Publish & Subscribe**

and can run over different transport, like:

* `WebSocket <https://tools.ietf.org/html/rfc6455>`_
`subprotocol <https://www.iana.org/assignments/websocket/websocket.xml>`_
* Raw TCP Socket
* Unix domain sockets

The WAMP protocol is a community effort and the specification is made available for
free under an open license for everyone to use or implement. The original design
and proposal was created by `Crossbar.io <https://crossbar.io>`_ developers in 2012 and
WAMP development is sponsored since then by `Crossbar.io (the company) <https://crossbario.com>`_.

.. toctree::
    :maxdepth: 2

    intro
    routing
    spec
    comparison
    implementations
    users
    roadmap
    faq
    impressum

**Get in touch** with us on our mailing list, github or search for answers on StackOverflow:

- `WAMP Google group <https://groups.google.com/group/wampws>`_
- `WAMP Protocol GitHub Repository <https://github.com/wamp-proto/wamp-proto>`_
- `WAMP StackOverflow Q&A <https://stackoverflow.com/questions/tagged/wamp-protocol>`_

The WAMP protocol is also looking for contributors that help polishing up the spec,
filling in gaps. A good starting point are our open issues on our
`issue tracker <https://github.com/wamp-proto/wamp-proto/issues>`_.
