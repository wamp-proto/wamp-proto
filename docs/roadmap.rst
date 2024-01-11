:github_url: https://github.com/wamp-proto/wamp-proto/edit/master/docs/roadmap.rst

.. _Roadmap:

Roadmap
=======

IETF RFC
--------

WAMP has come a long way since its inception and first incarnation back in 2012.

The jump in expressivness and power with WAMP v2 was big, and some other changes
allowed WAMP v2 to ingest a lot of user requirements and wishes without breaking
a basically very simple and coherent design.

And even better: we believe we can really complete the original vision of WAMP
under WAMP v2, and just fill in the remaining gaps:

* The WAMP Basic Profile is feature complete. The job is to polish and improve the spec text.
* The WAMP Advanced Profile: here we have a couple of gaps to fill for already defined features.
  The job is to come up with proposals for spec text, discuss, process feedback, ..

Finally, given we continue to work on above, the WAMP IETF RFC is in a stage where 
it makes sense to enter the RFC draft process, with the final goal of getting WAMP
released as an IETF RFC with a proper RFC number.


New advanced features
---------------------

The following are some areas we are exploring:

* progressive call arguments and streams
* sharded registrations
* Flatbuffers strongly typed application payload
* end-to-end payload encryption


The next level
--------------

With the feature areas listed above, where we want to close the final gaps
in the WAMP protocol to fullfil its promise and mission, our (now Crossbar.io
specifically as original creators of WAMP) focus will increasingly be on
what be believe is the next frontier

Now that we have WAMP, we want to use it to actually build a wider ecosystem of
**open data markets**, where WAMP components and microservices can trade their data
driven services, allowing consumers to buy service from providers.

This new project is called **XBR**, and you can find out more on the 
`XBR Network <https://xbr.network/>`_ homepage and the
`XBR Protocol <https://xbr.network/docs/index.html>`_ documentation.
