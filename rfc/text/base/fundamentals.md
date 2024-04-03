## Fundamentals

{align="left"}
| Term                              | Definition                                                                                                 |
|-----------------------------------|------------------------------------------------------------------------------------------------------------|
| *User*                            | A person (or organization) running a WAMP *Client* or *Router*                                             |
| *Client*                          | A program run by a *User*, with application code using WAMP for application-level communications           |
| *Router*                          | A program run by a *User*, with middleware code using WAMP to provide application routing services         |
| *Peer*                            | A WAMP *Client* or *Router*. An implementation might embed, provide or use both roles                      |
| *Realm*                           | Isolated WAMP URI namespace serving as a routing and administrative domain, optionally protected by **AA** |
| *Transport*                       | A message-based, reliable, ordered, bidirectional (full-duplex) channel over which *Peers* communicate     |
| *Connection*                      | An underlying entity (if any) carrying the *Transport*, e.g. a network connection, pipe, queue or such     |
| *Session*                         | Transient conversation between a *Client* and a *Router*, within a *Realm* and over a *Transport*          |
| *Message*                         | Indivisible unit of information transmitted between peers                                                  |
| *Serializer*                      | Encodes WAMP messages, with application payloads, into byte strings for transport                          |
