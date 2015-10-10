.PHONY: rfc

rfc:
	mmark -xml2 -page rfc/draft-oberstet-hybi-tavendo-wamp-00.md > rfc/draft-oberstet-hybi-tavendo-wamp-00.xml
	xml2rfc rfc/draft-oberstet-hybi-tavendo-wamp-00.xml
