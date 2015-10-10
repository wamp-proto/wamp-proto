# A HTTP Longpoll Transport for WAMP

The *Long-Poll Transport* is able to transmit a WAMP session over plain old HTTP 1.0/1.1. This is realized by the *Client* issuing HTTP/POSTs requests, one for sending, and one for receiving. Those latter requests are kept open at the server when there are no messages currently pending to be received.

**Opening a Session**

With the *Long-Poll Transport*, a *Client* opens a new WAMP session by sending a HTTP/POST request to a well-known URL, e.g.

    http://mypp.com/longpoll/open

Here, `http://mypp.com/longpoll` is the base URL for the *Long-Poll Transport* and `/open` is a path dedicated for opening new sessions.

The HTTP/POST request *SHOULD* have a `Content-Type` header set to `application/json` and *MUST* have a request body with a JSON document that is a dictionary:

```javascript
{
   "protocols": ["wamp.2.json"]
}
```

The (mandatory) `protocols` attribute specifies the protocols the client is willing to speak. The server will chose one from this list when establishing the session or fail the request when no protocol overlap was found.

The valid protocols are:

 * `wamp.2.json.batched`
 * `wamp.2.json`
 * `wamp.2.msgpack.batched`
 * `wamp.2.msgpack`

> The request path with this and subsequently described HTTP/POST requests *MAY* contain a query parameter `x` with some random or sequentially incremented value:
>
>   http://mypp.com/longpoll/open?x=382913
>
> The value is ignored, but may help in certain situations to prevent intermediaries from caching the request.
>

Returned is a JSON document containing a transport ID and the protocol to speak:

```javascript
{
   "protocol": "wamp.2.json",
   "transport": "kjmd3sBLOUnb3Fyr"
}
```

As an implied side-effect, two HTTP endpoints are created

    http://mypp.com/longpoll/<transport_id>/receive
    http://mypp.com/longpoll/<transport_id>/send

where `transport_id` is the transport ID returned from `open`, e.g.

    http://mypp.com/longpoll/kjmd3sBLOUnb3Fyr/receive
    http://mypp.com/longpoll/kjmd3sBLOUnb3Fyr/send


**Receiving WAMP Messages**

The *Client* will then issue HTTP/POST requests (with empty request body) to

    http://mypp.com/longpoll/kjmd3sBLOUnb3Fyr/receive

When there are WAMP messages pending downstream, a request will return with a single WAMP message (unbatched modes) or a batch of serialized WAMP messages (batched mode).

The serialization format used is the one agreed during opening the session.

The batching uses the same scheme as with `wamp.2.json.batched` and `wamp.2.msgpack.batched` transport over WebSocket.

> Note: In unbatched mode, when there is more than one message pending, there will be at most one message returned for each request. The other pending messages must be retrieved by new requests. With batched mode, all messages pending at request time will be returned in one batch of messages.
>

**Sending WAMP Messages**

For sending WAMP messages, the *Client* will issue HTTP/POST requests to

    http://mypp.com/longpoll/kjmd3sBLOUnb3Fyr/send

with request body being a single WAMP message (unbatched modes) or a batch of serialized WAMP messages (batched mode).

The serialization format used is the one agreed during opening the session.

The batching uses the same scheme as with `wamp.2.json.batched` and `wamp.2.msgpack.batched` transport over WebSocket.

Upon success, the request will return with HTTP status code 202 ("no content"). Upon error, the request will return with HTTP status code 400 ("bad request").


**Closing a Session**

To orderly close a session, a *Client* will issue a HTTP/POST to

    http://mypp.com/longpoll/kjmd3sBLOUnb3Fyr/close

with an empty request body. Upon success, the request will return with HTTP status code 202 ("no content").
