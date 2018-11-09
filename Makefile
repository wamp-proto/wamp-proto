.PHONY: docs rfc deploy

requirements:
	sudo apt install -y mmark xml2rfc
	sudo npm install -g grunt-cli
	npm install

clean:
	-rm -rf ./.build/*
	-rm -rf ./docs/_build/*

authors:
	git log --pretty=format:"%an <%ae> %x09" rfc | sort | uniq


build: build_rfc build_w3c

build_w3c:
	grunt

build_rfc:
	-mkdir ./.build 
	mmark -xml2 -page rfc/wamp.md > .build/wamp.xml
	xml2rfc --text .build/wamp.xml -o docs/_static/wamp_latest_ietf.txt
	xml2rfc --html .build/wamp.xml -o docs/_static/wamp_latest_ietf.html


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
