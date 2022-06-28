## Testament

When a WAMP client disconnects, or the WAMP session is destroyed, it may want to notify other subscribers or publish some fixed data.
Since a client may disconnect uncleanly, this can't be done reliably by them.
A *Testament*, however, set on the server, can be reliably sent by the *Broker* once either the WAMP session has detached or the client connection has been lost, and allows this functionality.
It can be triggered when a Session is either detached (the client has disconnected from it, or frozen it, in the case of Session Resumption) or destroyed (when the WAMP session no longer exists on the server).

This allows clients that otherwise would not be able to know when other clients disconnect get a notification (for example, by using the WAMP Session Meta API) with a format the disconnected client chose.

**Feature Announcement**

Support for this feature MUST be announced by *Dealers* (`role := "dealer"`) via

{align="left"}
        HELLO.Details.roles.dealer.features.
            testament_meta_api|bool := true

### Testament Meta Procedures

A *Client* can call the following procedures to set/flush Testaments:

* `wamp.session.add_testament` to add a Testament which will be published on a particular topic when the Session is detached or destroyed.
* `wamp.session.flush_testaments` to remove the Testaments for that Session, either for when it is detached or destroyed.

#### wamp.session.add_testament

Adds a new testament:

**Positional arguments**

1. `topic|uri` - the topic to publish the event on
2. `args|list` - positional arguments for the event
3. `kwargs|dict` - keyword arguments for the event

**Keyword arguments**

1. `publish_options|dict` - options for the event when it is published -- see `Publish.Options`. Not all options may be honoured (for example, `acknowledge`). By default, there are no options.
2. `scope|string` - When the testament should be published. Valid values are `detached` (when the WAMP session is detached, for example, when using Event Retention) or `destroyed` (when the WAMP session is finalized and destroyed on the Broker). Default MUST be `destroyed`.

`wamp.session.add_testament` does not return a value.

#### wamp.session.flush_testaments

Removes testaments for the given scope:

**Keyword arguments**

1. `scope|string` - Which set of testaments to be removed. Valid values are the same as `wamp.session.add_testament`, and the default MUST be `destroyed`.

`wamp.session.flush_testaments` does not return a value.

### Testaments in Use

A *Client* that wishes to send some form of data when their *Session* ends unexpectedly or their *Transport* becomes lost can set a testament using the WAMP Testament Meta API, when a *Router* supports it.
For example, a client may call `add_testament` (this example uses the implicit `scope` option of `destroyed`):

```python
yield self.call('wamp.session.add_testament',
                'com.myapp.mytopic', ['Seeya!'], {'my_name': 'app1'})
```

The *Router* will then store this information on the WAMP Session, either in a `detached` or `destroyed` bucket, in the order they were added.
A client MUST be able to set multiple testaments per-scope.
If the *Router* does not support Session Resumption (therefore removing the distinction between a detached and destroyed session), it MUST still use these two separate buckets to allow `wamp.session.flush_testaments` to work.

When a *Session* is *detached*, the *Router* will inspect it for any Testaments in the `detached` scope, and publish them in the order that the Router received them, on the specified topic, with the specified arguments, keyword arguments, and publish options.
The *Router* MAY ignore publish options that do not make sense for a Testament (for example, acknowledged publishes).

When a *Session* is going to be *destroyed*, the *Router* will inspect it for any Testaments in the `destroyed` scope, and publish them in the same way as it would for the `detached` scope, in the order that they were received.

A *Router* that does not allow Session Resumption MUST send `detached`-scope Testaments before `destroyed`-scope Testaments.

A *Client* can also clear testaments if the information is no longer relevant (for example, it is shutting down completely cleanly).
For example, a client may call `wamp.session.flush_testaments`:

```python
yield self.call('wamp.session.flush_testaments', scope='detached')
yield self.call('wamp.session.flush_testaments', scope='destroyed')
```

The *Router* will then flush all Testaments stored for the given scope.
