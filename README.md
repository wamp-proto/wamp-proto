# The WebSocket Application Messaging Protocol

[WAMP](http://wamp.ws) is an open WebSocket subprotocol that provides two asynchronous messaging patterns:

  * Remote Procedure Calls
  * Publish and Subscribe

Find out more on the [Web site](http://wamp.ws) or get in touch on the [mailing list](https://groups.google.com/group/wampws).

## Web site development

The Web site is built using [Flask](http://flask.pocoo.org/) and [Jinja2](http://jinja.pocoo.org/docs/) templating, and then frozen for production into a set of static files using [Frozen-Flask](http://pythonhosted.org/Frozen-Flask/).

To install relevant stuff:

    easy_install flask
	easy_install frozen-flask

To test:

      make test

This will run Flask via a WSGI server based Twisted Web.

To deploy the Web site to Amazon S3 (only relevant for those authorized):

	make deploy

