.PHONY: rfc

rfc:
	mmark -xml2 -page rfc/draft-oberstet-hybi-tavendo-wamp.md > rfc/draft-oberstet-hybi-tavendo-wamp.xml
	xml2rfc --text rfc/draft-oberstet-hybi-tavendo-wamp.xml
	xml2rfc --html rfc/draft-oberstet-hybi-tavendo-wamp.xml
