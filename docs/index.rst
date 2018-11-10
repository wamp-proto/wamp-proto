:github_url: https://github.com/wamp-proto/wamp-proto/edit/master/docs/index.rst

The Web Application Messaging Protocol
======================================

| |Travis| |Docs-S3| |Docs-CDN| |Gitter|

Welcome to the Web Application Messaging Protocol (WAMP).

WAMP is an open standard `WebSocket <https://tools.ietf.org/html/rfc6455>`_
`subprotocol <https://www.iana.org/assignments/websocket/websocket.xml>`_ that provides two 
application messaging patterns in one unified protocol:

* routed **Remote Procedure Calls** and
* **Publish & Subscribe**

Using WAMP you can build distributed systems out of application components which are
loosely coupled and communicate in (soft) real-time.

.. toctree::
    :maxdepth: 2

    intro
    routing
    comparison
    spec
    users
    implementations
    faq
    impressum


Community
---------

Get in touch with us on our mailing list, chat room or on GitHub, search for answers on StackOverflow:

- `WAMP Google group <https://groups.google.com/group/wampws>`_
- `WAMP Gitter chat <https://gitter.im/wamp-proto/wamp-proto>`_
- `WAMP StackOverflow Q&A <http://fix.me>`_
- `WAMP GitHub issue tracker <https://github.com/wamp-proto/wamp-proto/issues>`_

.. note::

    The WAMP protocol is now a community effort and the specification is made available for
    free under an open license for everyone to use or implement. The original design
    and proposal was created by `Crossbar.io <https://crossbar.io>`_ developers in 2012 and
    is sponsored since then by `Crossbar.io (the company) <https://crossbario.com>`_.


.. |Travis| image:: https://travis-ci.org/wamp-proto/wamp-proto.svg?branch=master
    :target: https://travis-ci.org/wamp-proto/wamp-proto

.. |Docs-S3| image:: https://img.shields.io/badge/docs-s3-brightgreen.svg?style=flat
    :target: https://s3.eu-central-1.amazonaws.com/wamp-proto.org/index.html

.. |Docs-CDN| image:: https://img.shields.io/badge/docs-cdn-brightgreen.svg?style=flat
    :target: https://wamp-proto.org/index.html

.. |Gitter| image:: https://gitter.im/crossbar/WAMP](https://badges.gitter.im/Join%20Chat.svg
    :target: https://gitter.im/wamp-proto/wamp-proto
