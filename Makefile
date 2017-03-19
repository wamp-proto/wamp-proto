.PHONY: rfc

rfc:
	mmark -xml2 -page rfc/draft-oberstet-hybi-crossbar-wamp.md > rfc/draft-oberstet-hybi-crossbar-wamp.xml
	xml2rfc --text rfc/draft-oberstet-hybi-crossbar-wamp.xml
	xml2rfc --html rfc/draft-oberstet-hybi-crossbar-wamp.xml

requirements:
	sudo apt install -y mmark xml2rfc
