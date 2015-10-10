# Submitting

The process of publishing a new RFC draft:

1. increment draft version number/date (`docName` and `date`) in `rfc/draft-oberstet-hybi-tavendo-wamp.md`)
2. `make rfc` to generate the RFC in XML, TXT and HTML format
3. do a quick, manual sanity check of the generated TXT file
4. do an extended check by uploading the XML file to [http://tools.ietf.org/tools/idnits/](http://tools.ietf.org/tools/idnits/)
5. submit the TXT file at [https://datatracker.ietf.org/submit/](https://datatracker.ietf.org/submit/)
6. tag the version `git tag -a draft-01` and push `git push --tags`

**You should upload the TXT file renamed to `draft-oberstet-hybi-tavendo-wamp-<NN>.txt`, where `NN` is the current draft number.**

The new draft should appear here:

* https://tools.ietf.org/html/draft-oberstet-hybi-tavendo-wamp
* https://datatracker.ietf.org/doc/draft-oberstet-hybi-tavendo-wamp/
