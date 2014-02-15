# The WebSocket Application Messaging Protocol

[WAMP](http://wamp.ws) is an open WebSocket subprotocol that provides two asynchronous messaging patterns:

  * Remote Procedure Calls
  * Publish and Subscribe

Find out more on the [Web site](http://wamp.ws) or get in touch on the [mailing list](https://groups.google.com/group/wampws).

Note:

WAMP v2 is currently under development. Along with a name change ('Web Application Messaging Protocol'), this greatly extends the power and flexibility of the protocol. Comments to the [draft spec](https://github.com/tavendo/WAMP/tree/master/spec) are highly welcome!

For a working (in progress) implementation of WAMP v2, and examples illustrating the benefits of the new version, take a look at [AutobahnPython](https://github.com/tavendo/AutobahnPython/tree/master/examples/twisted/wamp).

## WAMP Project Web site development

The WAMP project Web site is built using [Flask](http://flask.pocoo.org/) and [Jinja2](http://jinja.pocoo.org/docs/) templating, and then frozen for production into a set of static files using [Frozen-Flask](http://pythonhosted.org/Frozen-Flask/).

To install relevant stuff:

    easy_install flask
	easy_install frozen-flask

To test:

      make test

This will run Flask via a WSGI server based Twisted Web.

To deploy the Web site to Amazon S3 (only relevant for those authorized):

	make deploy

