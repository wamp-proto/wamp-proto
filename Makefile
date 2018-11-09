.PHONY: docs rfc deploy

requirements:
	sudo apt install -y mmark xml2rfc
	sudo npm install -g grunt-cli

clean:
	-rm -rf ./.build
	-rm -rf ./dos/_build

authors:
	git log --pretty=format:"%an <%ae> %x09" rfc | sort | uniq


build: build_rfc build_w3c

build_w3c:
	grunt

build_rfc:
	mmark -xml2 -page rfc/draft-oberstet-hybi-crossbar-wamp.md > rfc/draft-oberstet-hybi-crossbar-wamp.xml
	xml2rfc --text rfc/draft-oberstet-hybi-crossbar-wamp.xml
	xml2rfc --html rfc/draft-oberstet-hybi-crossbar-wamp.xml

deploy_rfc: build_rfc
	cp rfc/draft-oberstet-hybi-crossbar-wamp.txt ../wamp-web/website/wampws/static/rfc/
	cp rfc/draft-oberstet-hybi-crossbar-wamp.html ../wamp-web/website/wampws/static/rfc/


docs:
	# cd docs && sphinx-build -nWT -b dummy . _build
	cd docs && sphinx-build -b html . _build

clean_docs:
	-rm -rf docs/_build

run_docs: docs
	twistd --nodaemon web --path=docs/_build --listen=tcp:8010

spellcheck_docs:
	sphinx-build -b spelling -d docs/_build/doctrees docs docs/_build/spelling

# build and deploy latest docs:
#   => https://s3.eu-central-1.amazonaws.com/xbr.foundation/docs/index.html
#   => https://xbr.network/docs/index.html
publish_docs:
	aws s3 cp --recursive --acl public-read docs/_build s3://xbr.foundation/docs
