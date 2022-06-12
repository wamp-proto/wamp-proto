UNAME := $(shell uname)

ifeq ($(UNAME), Linux)
	sed_args = -i
endif
ifeq ($(UNAME), Darwin)
	sed_args = -i ''
endif

CURRENTDATE := $(shell TZ=UTC date -Iseconds)

OUTPUTDIR = ./dist
TMPBUILDDIR = ./.build
SITEBUILDDIR = ./docs/_static/gen
# build optimized SVGs from "docs/_graphics/*.svg" using Scour
# note: this currently does not recurse into subdirs! place all SVGs flat into source folder
SOURCEDIR = ./docs/_graphics

SOURCES = $(wildcard $(SOURCEDIR)/*.svg)
OBJECTS = $(patsubst $(SOURCEDIR)/%.svg, $(SITEBUILDDIR)/%.svg, $(SOURCES))

SCOUR = scour
SCOUR_FLAGS = --remove-descriptive-elements --enable-comment-stripping --enable-viewboxing --indent=none --no-line-breaks --shorten-ids

usage:
	@echo "make build - build spec in all formats"
	@echo "make grep_options - show places where *.Options are used"
	@echo "make clean - clean all generated data"
	@echo "make authors - show authors based on git log data"
	@echo "make publish_aws - publish generated spec to aws"
	@echo "make run_docs - run http server on 8010 port to serve docs"
	@echo "make spellcheck_docs - spell check the docs via sphinx-build"

.PHONY: build grep_options clean authors publish_aws run_docs spellcheck_docs

grep_options:
	@find rfc/ -name "*.md" -type f -exec grep -o "\`\w*\.Options\.[a-z_]*|.*\`" {} \;

clean:
	if [ -d $(OUTPUTDIR) ]; then rm -rf $(OUTPUTDIR); fi
	if [ -d $(TMPBUILDDIR) ]; then rm -rf $(TMPBUILDDIR); fi
	if [ -d $(SITEBUILDDIR) ]; then rm -rf $(SITEBUILDDIR); fi
	if [ -f ./rfc/aux/authors.json ]; then rm ./rfc/aux/authors.json; fi
	rm mmark
	mkdir -p $(OUTPUTDIR)
	mkdir -p $(TMPBUILDDIR)
	mkdir -p $(SITEBUILDDIR)

authors:
	git log --pretty=format:"%an <%ae> %x09" rfc | sort | uniq

#
# build and deploy to:
#
# * https://s3.eu-central-1.amazonaws.com/wamp-proto.org/
# * https://wamp-proto.org/
#
publish_aws:
	aws s3 cp --recursive --acl public-read docs/_build s3://wamp-proto.org/

run_docs:
	cd dist && python -m http.server 8010

spellcheck_docs:
	sphinx-build -b spelling -d $(TMPBUILDDIR)/docs/doctrees docs $(TMPBUILDDIR)/docs/spelling

start_build:
	@echo "Building with WAMP_BUILD_ID=$(WAMP_BUILD_ID)"

$(SITEBUILDDIR)/%.svg: $(SOURCEDIR)/%.svg
	$(SCOUR) $(SCOUR_FLAGS) $< $@

build: clean start_build build_images build_spec sphinx-build-docs

build_images: $(SITEBUILDDIR)/$(OBJECTS)

build_spec: build_spec_rfc build_spec_w3c

# https://github.com/mmarkdown/mmark
# sudo apt install -y mmark
requirements_mmark:
	wget https://github.com/mmarkdown/mmark/releases/download/v2.2.25/mmark_2.2.25_linux_amd64.tgz
	tar xvzf mmark_2.2.25_linux_amd64.tgz
	rm -f ./mmark*.tgz

# https://mmark.miek.nl/post/syntax/
build_spec_rfc: requirements_mmark build_spec_rfc_mmark

build_spec_rfc_mmark:
	sed $(sed_args) -e 's/^date = .*/date = $(CURRENTDATE)/g' ./rfc/wamp.md
	./mmark ./rfc/wamp.md > $(TMPBUILDDIR)/wamp.xml
	sed $(sed_args) 's/<sourcecode align="left"/<sourcecode/g' $(TMPBUILDDIR)/wamp.xml
	sed $(sed_args) 's/<t align="left"/<t/g' $(TMPBUILDDIR)/wamp.xml
	xmllint --noout $(TMPBUILDDIR)/wamp.xml
	xml2rfc --v3 --text $(TMPBUILDDIR)/wamp.xml -o $(OUTPUTDIR)/wamp_latest_ietf.txt
	xml2rfc --v3 --html $(TMPBUILDDIR)/wamp.xml -o $(OUTPUTDIR)/wamp_latest_ietf.html

build_spec_w3c:
	git log --pretty=format:"{ name: \"%an\" }," rfc | \
		grep -v -e "ecorm" -e "Andrew J. Gillis" | \
		sort | uniq > ./rfc/aux/authors.json
	grunt

sphinx-build-docs:
	# first test with all warnings fatal
	sphinx-build -nWT -b dummy ./docs $(TMPBUILDDIR)/docs

	# run spell checker
	sphinx-build -b spelling -d $(TMPBUILDDIR)/docs/.doctrees ./docs $(TMPBUILDDIR)/docs/spelling

	# generate HTML output
	sphinx-build -b html ./docs $(TMPBUILDDIR)/site_build

	cp -R $(TMPBUILDDIR)/site_build/* $(OUTPUTDIR)
