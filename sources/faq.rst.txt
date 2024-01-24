:github_url: https://github.com/wamp-proto/wamp-proto/edit/master/docs/faq.rst

.. _Faq:

Frequently Asked Questions
==========================

.. rubric:: Frequently Asked Questions
   :name: frequently-asked-questions

- General

   -  `What is RPC? <#what-is-rpc>`__
   -  `What is PubSub? <#what-is-pubsub>`__
   -  `Why RPC and PubSub in one protocol? <#why-rpc-and-pubsub-in-one-protocol>`__
   -  `Why is it called WAMP and how do I use it? <#why-is-it-called-wamp-and-how-do-i-use-it>`__
   -  `What is Websocket? <#what-is-websocket>`__
   -  `Is WebSocket necessary for WAMP? <#is-websocket-necessary-for-wamp>`__

-  Legal

   -  `What is the legal status of WAMP? <#what-is-the-legal-status-of-wamp>`__
   -  `Are there any requirements if I use WAMP for my project? <#are-there-any-requirements-if-i-use-wamp-for-my-project>`__
   -  `Why is WAMP trademarked? <#why-is-wamp-trademarked>`__
   -  `Who can use the WAMP word mark or the WAMP design mark? <#who-can-use-the-wamp-word-mark-or-the-wamp-design-mark>`__
   -  `What does the CC copyright on this website mean? <#what-does-the-cc-copyright-on-this-website-mean>`__


General
-------

.. rubric:: What is RPC?
   :name: what-is-rpc

**Remote Procedure Call (RPC)** is a messaging pattern involving peers
of three roles:

#. *Caller*
#. *Callee*
#. *Dealer*

A *Caller* issues calls to remote procedures by providing the procedure
URI and any arguments for the call. The *Callee* will execute the
procedure using the supplied arguments to the call and return the result
of the call to the *Caller*.

*Callees* register procedures they provide with *Dealers*. *Callers*
initiate procedure calls first to *Dealers*. *Dealers* route calls
incoming from *Callers* to *Callees* implementing the procedure called,
and route call results back from *Callees* to *Callers*.

The *Caller* and *Callee* will usually run application code, while the
*Dealer* works as a generic router for remote procedure calls decoupling
*Callers* and *Callees*.

`to top <#frequently-asked-questions>`__


.. rubric:: What is PubSub?
   :name: what-is-pubsub

Publish & Subscribe (PubSub) is a messaging pattern involving peers of
three roles:

#. *Publisher*
#. *Subscriber*
#. *Broker*

A *Publishers* publishes events to topics by providing the topic URI and
any payload for the event. *Subscribers* of the topic will receive the
event together with the event payload.

*Subscribers* subscribe to topics they are interested in with *Brokers*.
*Publishers* initiate publication first at *Brokers*. *Brokers* route
events incoming from *Publishers* to *Subscribers* that are subscribed
to respective topics.

The *Publisher* and *Subscriber* will usually run application code,
while the *Broker* works as a generic router for events decoupling
*Publishers* from *Subscribers*.

Read more: `Publish / Subscribe Systems: Design and
Principles <http://books.google.de/books?id=RxsyCBr9eLMC>`__, by Sasu
Tarkoma.

`to top <#frequently-asked-questions>`__


.. rubric:: Why RPC and PubSub in one protocol?
   :name: why-rpc-and-pubsub-in-one-protocol

| Imagine the following situation: an application frontend wants to
  perform some action on an application backend. The frontend also wants
  to get notified when another frontend performs the respective action
  on the backend.
| For example, in a Web application for managing service tickets, a
  frontend might perform the action "create new ticket", and get
  notified via events of "new ticket created".

| A natural approach to realize above would use RPC for performing
  actions, and PubSub for notifications.
| With the service ticket Web app, the frontend would subscribe to the
  topic "OnTicketCreated", and perform it's actions by calling
  "createTicket". The backends implementation of "createTicket" would
  not only perform the action of creating a new ticket, but also publish
  a event on the topic "OnTicketCreated" with the details of the new
  ticket.

Now, a protocol suitable for realizing above will naturally need to
provide both RPC and PubSub messaging patterns. WAMP was designed
exactly with above in mind, so it provides you with a unified protocol
for both RPC and PubSub.

For more about the reasoning behind WAMP, see `this
explanation <routing.html>`__.

`to top <#frequently-asked-questions>`__


.. rubric:: Why is it called WAMP and how do I use it?
   :name: why-is-it-called-wamp-and-how-do-i-use-it

WAMP is an acronym, and the term "Web Application Messaging Protocol" is
a quite precise description of what the protocol provides.

WAMP is pronounced /wa:mp/, as in
`swamp <http://dictionary.cambridge.org/pronunciation/british/swamp_1#>`__
or
`chomp <http://dictionary.cambridge.org/dictionary/british/chomp?q=chomp#>`__.

Note that there is another technology also abbreviated WAMP: the Web
technology stack "Windows + Apache + MySQL + PHP". I.e. Wikipedia has a
corresponding `disambiguation
page <http://en.wikipedia.org/wiki/WAMP_%28disambiguation%29>`__.

Because of this potential ambiguity, here is what we recommend for
**authors/implementors**:

#. Use **"WAMP"** in text and speech
#. The first occurrence in text should read: **"WAMP (Web Application
   Messaging Protocol)"**
#. Add the hashtag/keyword **"wampws"** to the contents metadata

And here is what we recommend for **users**:


#. Use the terms **"wamp"** and **"protocol"** *combined* when using Web
   search engines
#. Use the hashtag/keyword **"wampws"** when search on Web platform like
   `Twitter <https://twitter.com>`__ or
   `StackOverflow <http://stackoverflow.com/>`__

`to top <#frequently-asked-questions>`__


.. rubric:: What is WebSocket?
   :name: what-is-websocket

WebSocket is a protocol providing full-dupley communcations channels
over a single TCP connection. It started out in the Web world, where it
was created to replace things like Comet, and to allow true
bi-directional, low-latency connections between browser and server. It's
standardized by the IETF and the W3C. Usage is not limited to the
browser, with implementations available for all major programming
languages. For more details see this `introductory blog
post <http://crossbario.com/blog/Websocket-Why-What-Can-I-Use-It/>`__.

`to top <#frequently-asked-questions>`__

.. rubric:: Is WebSocket necessary for WAMP?
   :name: is-websocket-necessary-for-wamp

| WAMP started out as the WebSocket Application Messaging Protocol.
  WebSocket is still the preferred transport in many cases, but the
  transport layer is fully decoupled. Any bi-directional, reliable,
  message-based and ordered transport works. Transports like Unix Domain
  Sockets or Unix Pipes are being used in implementations.
| Additionally, a transport for WAMP transports can be implemented on
  top of other transports which lack some of the requirements, e.g.
  using longpoll bi-directionality can be built on top of HTTP.

`to top <#frequently-asked-questions>`__

Legal
-----

.. rubric:: What is the legal status of WAMP?
   :name: what-is-the-legal-status-of-wamp

| WAMP is free - both as in beer and as in speech. Do with it what you
  like. If WAMP fills your needs as it is, then the easiest thing is to
  just use it without any changes. The more compatible implementations,
  the better for interoperability. If your needs require modifications,
  or you want to start your own development based on WAMP, then you are
  also free to do so.
| Whatever you do with WAMP - an announcement on the mailing list is
  always welcome.

`to top <#frequently-asked-questions>`__

.. rubric:: Are there any requirements if I use WAMP for my project?
   :name: are-there-any-requirements-if-i-use-wamp-for-my-project

| WAMP is free to use for anybody, be it as part of an open source or a
  commercial project. There are no strings attached here, no licenses to
  pay, and no known other intellectual property (such as patents).
| If you do use WAMP for your project, then both a mention of this
  somewhere in your project, and an announcement on the mailing list
  would be welcome.

`to top <#frequently-asked-questions>`__

.. rubric:: Why is WAMP trademarked?
   :name: why-is-wamp-trademarked

The WAMP word- and design mark are trademarked as a way to ensure that
only proper use is made of them. This is especially the case in regard
to assurances regarding compatibility. A trademark policy detailing
correct use is in the works. For now, and for a quick overview of the
base principles of the trademark policy, see the following question.

`to top <#frequently-asked-questions>`__

.. rubric:: Who can use the WAMP word mark or the WAMP design mark?
   :name: who-can-use-the-wamp-word-mark-or-the-wamp-design-mark

| The fact that WAMP is a word mark does not prevent factual use. If you
  e.g. announced that you were working on a WAMP implementation, or
  discussed details of your implementation work, or recommended this
  website, these are all, naturally, entirely unproblematic uses.
| For any use of the word mark which could imply a direct endorsement,
  or other official connection with the WAMP project, or when in doubt,
  please get in contact with typedef int GmbH. The same goes for any use
  of the design mark (i.e. the WAMP logo at the top of the project
  page).
| We will take a look as quickly as possible, and try to arrange a
  license if this should be necessary. (And a license does not need to
  be a big deal.)

`to top <#frequently-asked-questions>`__

.. rubric:: What does the CC copyright on this website mean?
   :name: what-does-the-cc-copyright-on-this-website-mean

| The threshold for using WAMP should be as low as possible. This
  includes the documentation for what you are doing. The CC BY license
  simply means that you are free to use any materials on this website
  (with the exception of the WAMP word mark or WAMP design mark) for
  your project. You can copy & paste or edit anything you think useful
  to for e.g. your own project website or your documentation. This
  applies irrespective of whether your project is commercial or
  non-commercial.
| The only requirement is that you attribute this use. In an internet
  context, this is most easily done by providing something like 'some
  materials copied/adapted from' + a link to the WAMP website.

`to top <#frequently-asked-questions>`__
