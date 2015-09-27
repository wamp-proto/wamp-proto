# Tooling for writing a RFC

RFC drafts can be submitted in several formats, with XML the preferred one, since it is easiest on the IETF RFC editors (reuse of existing markup).

## Markdown to XML

We want to author our drafts in a sane format. Furtunately, there is a converter for an extended markdown flavor to XML:

[mmark](https://github.com/miekg/mmark)

This is written in Go, so you need to [install this](https://golang.org/doc/install) (On Ubuntu: `sudo apt-get install golang`). Once you have this, with your paths properly set up, you can just do

```
go get github.com/miekg/mmark
```

to install directly from the GitHub repository. (There is no feedback about a successful installation.)

You then do

```
make all
```

in the directory it was installed to, which creates the executable for your system.

To convert a markdown file into XML, do

```
<the path to your go installation>/src/github.com/miekg/mmark/mmark/mmark -xml2 -page <source file>.md > <output file>.xml
```

A refrence about the markdown flavor used can be found in the [project readme](https://github.com/miekg/mmark/blob/master/README.md), and some famous RFCs are provided in markdown form as [examples](https://github.com/miekg/mmark/tree/master/rfc).

## XML to txt

To check what the draft will look like in the final output format for publication (txt), we need to convert once more.

The tool for this is [xml2rfc](http://xml2rfc.ietf.org/). To install this just do

```
pip install xml2rfc
```

> On Ubuntu you need: `sudo apt-get install libxml2-dev libxslt1-dev`

and to use it

```
xml2rfc <source file>.xml
```

which will create a text file of the same name.


## Checking the XML

Since XML is the standard format for submitting drafts, checking and validation tools are exclusively for this.

http://tools.ietf.org/tools/idspell/webservice - provides spell checking with an IETF-specific wordlist

http://fenron.net/~fenner/ietf/xml2rfc-valid/ - does formal XML validation

http://tools.ietf.org/tools/idnits/ - provides additional checks

(Haven't tested any of the above checking tools yet.)


## Message Sequence Diagrams

Message Sequence Diagrams as ASCII art are generated from UML files using a Java tool (http://plantuml.com/).

The .jar file for this as well as the source files are in the 'diagrams' subdirectory.

After adding or modifying a diagram, just do `make diagrams`. This clears the previously generated text files and processes all *.uml files in the diagram directory.


## Style Guides

https://www.rfc-editor.org/rfc-style-guide/rfc-style
https://www.rfc-editor.org/policy.html



# Formatting for markdown file for RFC

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

