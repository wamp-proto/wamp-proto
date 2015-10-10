# Tooling

RFC drafts can be submitted in several formats, with XML the preferred one, since it is easiest on the IETF RFC editors.

## Mmark

We want to author our drafts in a sane format. Furtunately, there is [Mmark](https://github.com/miekg/mmark), a converter for an extended markdown flavor to RFC XML.

A reference about the markdown flavor used can be found in the [project readme](https://github.com/miekg/mmark/blob/master/README.md), and some famous RFCs are provided in markdown form as [examples](https://github.com/miekg/mmark/tree/master/rfc).

### Installation

Mmark is written in Go, so you need to [install this](https://golang.org/doc/install):


    sudo apt-get install golang

Go requires a `GOPATH` environment variable to be set, so add the following to your `~/.profile`

    export GOPATH=${HOME}/.go

Now install Mmark directly from the GitHub repository

    go get github.com/miekg/mmark


> There is no feedback about a successful installation.

Installation is not done yet, you need to 

    cd $GOPATH/src/github.com/miekg/mmark
    make all

This should have created the `mmark` executable. Add the following to your `.profile`:

    export $PATH=${GOPATH}/src/github.com/miekg/mmark/mmark:${PATH}

### Testing

Now quickly test if the `mmark` tool works:

```console
oberstet@corei7ub1310:~$ mmark -h
Mmark Markdown Processor
Available at http://github.com/miekg/mmark

Copyright © 2014 Miek Gieben <miek@miek.nl>
Copyright © 2011 Russ Ross <russ@russross.com>
Distributed under the Simplified BSD License

Usage:
  mmark [options] [inputfile [outputfile]]

Options:
  -bib-id="http://xml2rfc.ietf.org/public/rfc/bibxml3/": ID bibliography URL
  -bib-rfc="http://xml2rfc.ietf.org/public/rfc/bibxml/": RFC bibliography URL
  -css="": link to a CSS stylesheet (implies -page)
  -head="": link to HTML to be included in head (implies -page)
  -page=false: generate a standalone HTML page
  -rfc7328=false: parse RFC 7328 style input
  -toml=false: input file is xml2rfc XML which is convert to TOML titleblock
  -xml=false: generate XML2RFC v3 output
  -xml2=false: generate XML2RFC v2 output
```

### Converting

To convert a markdown file into RFC XML, do

    mmark -xml2 -page input.md > output.xml


## xml2rfc

To check what the draft will look like in the final output format for publication (txt), we need to convert once more.

The tool for this is [xml2rfc](http://xml2rfc.ietf.org/) which is written in Python.

### Installation

To install from PyPI

    pip install xml2rfc

> You will need `sudo apt-get install libxml2-dev libxslt1-dev` on Ubuntu/Debian for this.

To install from Ubuntu/Debian package repository

    sudo apt-get xml2rfc


### Testing

Now quickly test if the `xml2rfc` tool works:

```console
oberstet@corei7ub1310:~$ xml2rfc --version
2.4.3
``` 

### Converting

To convert a RFC XML file into text, do

    xml2rfc source.xml

which will create a text file of the same base name with `.txt` file extension.


# Verification

Since XML is the standard format for submitting drafts, checking and validation tools are exclusively for this:

* http://tools.ietf.org/tools/idspell/webservice - provides spell checking with an IETF-specific wordlist
* http://fenron.net/~fenner/ietf/xml2rfc-valid/ - does formal XML validation
* http://tools.ietf.org/tools/idnits/ - provides additional checks

> FIXME: haven't tested any of the above checking tools yet.


# Authoring

## Diagrams

### Message-sequence Diagrams

Message Sequence Diagrams as ASCII art are generated from UML files using a Java tool (http://plantuml.com/).

The .jar file for this as well as the source files are in the 'diagrams' subdirectory.

After adding or modifying a diagram, just do `make diagrams`. This clears the previously generated text files and processes all *.uml files in the diagram directory.

### State-machine Diagrams

* https://github.com/wamp-proto/wamp-proto/blob/master/rfc/diagrams/peer_statechart.txt
* http://asciiflow.com/


## Style Guides

* https://www.rfc-editor.org/rfc-style-guide/rfc-style
* https://www.rfc-editor.org/policy.html


# Formatting the markdown file for RFC

This document collects formatting conventions and formatting tips for drafting a RFC in markdown format when using [mmark](https://github.com/miekg/mmark) to transform the markdown into XML.

## Code indentation

Code, whether marked via triple backticks or four indentations, is correctly marked up as <figure><artwork>, but centered instead of left-aligned.

Adding {align="left"} before a four-identations code block and indenting the codeblock an additional four spaces fixes this, e.g.

{align="left"}
        WON'T RANDOMLY-LOSE

        DON'T RANDOMLY-LOSE

For triple backticks e.g.

{align="left"}
``` python
    ## loose URI check disallowing empty URI components
    pattern = re.compile(r"^([^\s\.#]+\.)*([^\s\.#]+)$")
```


## Line length for code blocks

There is no line wrapping of code blocks, and RFCs are limited to 72 characters per line.

This means that we need to manually line-wrap code blocks.


## Defined Terms

Terms that we define as part of the WAMP spec are 

* capitalized throughout the text and
* italicised on their first use only.

## WAMP MESSAGES

**WAMP message texts** are in all caps.

**Arguments of WAMP messages** are in backticks, e.g. "Keys in `Options` and `Details` must be of type ...".
