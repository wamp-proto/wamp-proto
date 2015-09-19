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

### Message Definitions 

For message definitions, we do one element per line e.g.

    [
        ERROR,
        REQUEST.Type|int,
        REQUEST.Request|id,
        Details|dict,
        Error|uri,
        Arguments|list,
        ArgumentsKw|dict
    ]
