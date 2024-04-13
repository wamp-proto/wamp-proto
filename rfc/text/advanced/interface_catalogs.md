### Interface Catalogs {#interface-catalogs}

Collections of types defined in FlatBuffers IDL are bundled in *Interface Catalogs* which are just ZIP files with

* one [catalog.yaml](catalog.yaml) file with catalog metadata
* one or more `*.bfbs` compiled FlatBuffer IDL schemas

and optionally

* schema source files
* image and documentation files

#### Catalog Archive File

The contents of an `example.zip` interface catalog:

```sh
unzip -l build/example.zip
Archive:  build/example.zip
  Length      Date    Time    Name
---------  ---------- -----   ----
        0  1980-00-00 00:00   schema/
    14992  1980-00-00 00:00   schema/example2.bfbs
    15088  1980-00-00 00:00   schema/example4.bfbs
    13360  1980-00-00 00:00   schema/example3.bfbs
     8932  1980-00-00 00:00   schema/example1.bfbs
     6520  1980-00-00 00:00   schema/wamp.bfbs
     1564  1980-00-00 00:00   README.md
        0  1980-00-00 00:00   img/
    13895  1980-00-00 00:00   img/logo.png
     1070  1980-00-00 00:00   LICENSE.txt
     1288  1980-00-00 00:00   catalog.yaml
---------                     -------
    76709                     11 files
```

The bundled Catalog Interfaces in above are FlatBuffers binary schema files which are compiled using `flatc`

```
flatc -o ./schema --binary --schema --bfbs-comments --bfbs-builtins ./src
```

from FlatBuffers IDL sources, for example:

```flatbuffers
rpc_service IExample1 (
    type: "interface", uuid: "bf469db0-efea-425b-8de4-24b5770e6241"
) {
    my_procedure1 (TestRequest1): TestResponse1 (
        type: "procedure", wampuri: "com.example.my_procedure1"
    );

    on_something1 (TestEvent1): Void (
        type: "topic", wampuri: "com.example.on_something1"
    );
}
```

#### Catalog Metadata

The `catalog.yaml` file contains catalog metadata in [YAML Format](https://yaml.org/):

{align="left"}
| Field         | Description |
|---------------|-------------|
| `name`        | Catalog name, which must contain only lower-case letter, numbers, hyphen and underscore so the catalog name can be used in HTTP URLs |
| `version`     | Catalog version (e.g. semver or calendarver version string) |
| `title`       | Catalog title for display purposes |
| `description` | Catalog description, a short text describing the API catalog |
| `schemas`     | FlatBuffers schemas compiled into binary schema reflection format |
| `author`      | Catalog author |
| `publisher`   | Ethereum Mainnet address of publisher |
| `license`     | SPDX license identifier (see https://spdx.org/licenses/) for the catalog |
| `keywords`    | Catalog keywords to hint at the contents, topic, usage or similar of the catalog |
| `homepage`    | Catalog home page or project page |
| `git`         | Git source repository location |
| `theme`       | Catalog visual theme |

Here is a complete example:

```yaml
name: example

version: 22.6.1

title: WAMP Example API Catalog

description: An example of a WAMP API catalog.

schemas:
  - schema/example1.bfbs
  - schema/example2.bfbs
  - schema/example3.bfbs
  - schema/example4.bfbs

author: typedef int GmbH

publisher: "0x60CC48BFC44b48A53e793FE4cB50e2d625BABB27"

license: MIT

keywords:
  - wamp
  - sample

homepage: https://wamp-proto.org/

git: https://github.com/wamp-proto/wamp-proto.git

theme:
  background: "#333333"
  text: "#e0e0e0"
  highlight: "#00ccff"
  logo: img/logo.png
```

#### Catalog Sharing and Publication

**Archive File Preparation**

The [ZIP](https://linux.die.net/man/1/zip) archive format and tools, by default, include filesystem and other metadata from the host producing the archive. That information usually changes, per-archive run, as e.g. the current datetime is included,
which obviously progresses.

When sharing and publishing a WAMP Interface Catalog, it is crucial that the archive only depends on the actual contents of the compressed files.

Removing all unwanted ZIP archive metadata can be achieved using [stripzip](https://github.com/KittyHawkCorp/stripzip):

```
stripzip example.zip
```

The user build scripts for compiling and bundling an Interface Catalog ZIP file MUST be repeatable, and only depend on the input source files. A build process that fulfills this requirement is called [Reproducible build](https://en.wikipedia.org/wiki/Reproducible_builds).

The easiest way to check if your build scripts producing `example.zip` is reproducible is repeat the build and check that the file fingerprint of the resulting archive stays the same:

```
openssl sha256 example.zip
```

**Catalog Publication on Ethereum and IPFS**

Write me.
