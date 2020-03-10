.PHONY: docs rfc

requirements:
	sudo apt update
	sudo apt install -y mmark xml2rfc
	npm install -g grunt-cli
	npm install
	pip install -r requirements.txt

clean:
	-rm -rf ./.tox
	-rm -rf ./.build
	-rm -rf ./docs/_build/*
	-rm -rf ./docs/_static/gen/*

authors:
	git log --pretty=format:"%an <%ae> %x09" rfc | sort | uniq


build: build_images build_spec docs


#
# build the spec target files from sources
#
BUILDDIR = docs/_static/gen

build_spec: build_spec_rfc build_spec_w3c

build_spec_rfc:
	-mkdir ./.build 
	mmark -xml2 -page rfc/wamp.md > .build/wamp.xml
	xml2rfc --text .build/wamp.xml -o $(BUILDDIR)/wamp_latest_ietf.txt
	xml2rfc --html .build/wamp.xml -o $(BUILDDIR)/wamp_latest_ietf.html

build_spec_w3c:
	grunt


#
# build optimized SVG files from source SVGs
#
SCOUR = scour 
SCOUR_FLAGS = --remove-descriptive-elements --enable-comment-stripping --enable-viewboxing --indent=none --no-line-breaks --shorten-ids

# build "docs/_static/gen/*.svg" optimized SVGs from "docs/_graphics/*.svg" using Scour
# note: this currently does not recurse into subdirs! place all SVGs flat into source folder
SOURCEDIR = docs/_graphics

SOURCES = $(wildcard $(SOURCEDIR)/*.svg)
OBJECTS = $(patsubst $(SOURCEDIR)/%.svg, $(BUILDDIR)/%.svg, $(SOURCES))

$(BUILDDIR)_exists:
	mkdir -p $(BUILDDIR)

build_images: $(BUILDDIR)_exists $(BUILDDIR)/$(OBJECTS)

$(BUILDDIR)/%.svg: $(SOURCEDIR)/%.svg
	$(SCOUR) $(SCOUR_FLAGS) $< $@

clean_images:
	-rm -rf docs/_static/gen

#
# build the docs (https://wamp-proto.org website) from ReST sources
#
docs:
	tox -e sphinx

docs_only:
	#cd docs && sphinx-build -nWT -b dummy . _build
	cd docs && sphinx-build -b html . _build

clean_docs:
	-rm -rf docs/_build

run_docs: docs
	twistd --nodaemon web --path=docs/_build --listen=tcp:8010

spellcheck_docs:
	sphinx-build -b spelling -d docs/_build/doctrees docs docs/_build/spelling


#
# build and deploy to:
#
#   * https://s3.eu-central-1.amazonaws.com/wamp-proto.org/
#   * https://wamp-proto.org/
#
publish_docs:
	aws s3 cp --recursive --acl public-read docs/_build s3://wamp-proto.org/
