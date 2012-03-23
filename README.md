The WebSocket Application Messaging Protocol
============================================

WAMP(http://wamp.ws) is an open WebSocket subprotocol that provides
two asynchronous messaging patterns:

  * RPC and
  * PubSub


Mailing List
------------

   https://groups.google.com/group/wampws


Web Site
--------

Developing and testing the Web site content is easy. The Web site is
built using Flask http://flask.pocoo.org/

Just do:

      easy_install flask

then:

      cd website/wampws
      python __init__.py -d -s

This will run Flask via a WSGI server based on standard Python socketserver.

Note. This server sometimes does hang etc. If you leave out the "-s", then
it will run under Twisted. You need to have that of course, then.
The "-d" makes Flask automatically reload changed stuff (debug). This _only_
works with socketserver, not Twisted.
