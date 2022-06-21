### Node Control API {#node-control-api}

Write me.

#### WAMP Meta API Remoting

The *local WAMP meta API* exists on URI prefix `wamp.` on the respective application realm:

```
wamp.session.on_join (session_id, session_details)
```

The *globally identified WAMP meta API* has all procedures and topics extended with
`(domain_adr, node_id, worker_id, realm_id)` arguments and exists on a `wamp.network.remote.meta.wamp.`
URI prefix on the respective management realm of the domain:

```
wamp.network.remote.meta.wamp.session.on_join (domain_adr, node_id, worker_id, realm_id, session_id, session_details)
```

See also: https://github.com/crossbario/crossbar/blob/6b6e25b1356b0641eff5dc5086d3971ecfb9a421/crossbar/master/api/wamp.py#L17
