#!/usr/bin/env python3
"""
Expand the "ubjson" test-vector serializations with the BJData encoding.

Background
----------
The WAMP "ubjson" serializer in autobahn-python switched its backend from
the unmaintained ``py-ubjson`` (used up to and including autobahn-python
25.12.2) to the maintained ``bjdata`` package (from autobahn-python 26.6.1
onwards). ``bjdata`` implements BJData, a UBJSON *superset* whose octet-level
encoding differs from plain UBJSON, e.g.:

  * integers are little-endian (marker ``m``/``M``) instead of big-endian
    (marker ``l``/``L``);
  * binary data uses the BJData ``[$B#...`` byte-array marker instead of the
    UBJSON ``[$U#...`` uint8-array marker.

The WAMP serializer id stays ``"ubjson"`` for transport negotiation, but the
bytes on the wire change. The test-vector format stores each serializer as a
*list* of valid encodings and matches with "at least one must match"
semantics, so we keep the existing (py-ubjson) bytes and *add* the new
(bjdata) bytes as a second entry. Both entries get a ``note`` identifying the
backend that produced them.

Source of truth
---------------
The bjdata bytes are derived from the sibling ``msgpack`` vector in the same
sample: the message object is decoded with ``msgpack`` and re-encoded with
``bjdata``. This is byte-identical to what autobahn-python's
``UBJSONObjectSerializer.serialize()`` emits (which is simply
``bjdata.dumpb(obj)``), and it avoids any dependency on the deprecated
``py-ubjson`` package in this generator.

Usage
-----
    pip install msgpack bjdata          # bjdata is CPython-only
    python testsuite/regen_ubjson_vectors.py

The script is idempotent: samples whose ``ubjson`` list already carries the
bjdata entry are left untouched. Whole files are rewritten with stable JSON
formatting (2-space indent, ASCII-escaped), so the only changes that appear in
a diff are the expanded ``ubjson`` arrays.
"""
import glob
import json
import os
import sys

import bjdata
import msgpack

# autobahn-python <= 25.12.2: py-ubjson 0.16.1 backend (plain UBJSON encoding)
LEGACY_NOTE = "UBJSON encoding (autobahn-python <= 25.12.2, py-ubjson 0.16.1 backend)"
# autobahn-python >= 26.6.1: bjdata backend (BJData encoding, a UBJSON superset)
BJDATA_NOTE = "BJData encoding, a UBJSON superset (autobahn-python >= 26.6.1, bjdata 0.6.x backend)"

HERE = os.path.dirname(os.path.abspath(__file__))


def iter_serializer_blocks(node):
    """Yield every ``serializers`` dict found anywhere in a loaded vector file."""
    if isinstance(node, dict):
        block = node.get("serializers")
        if isinstance(block, dict):
            yield block
        for value in node.values():
            yield from iter_serializer_blocks(value)
    elif isinstance(node, list):
        for value in node:
            yield from iter_serializer_blocks(value)


def bjdata_hex_from_msgpack(msgpack_hex):
    """Decode a msgpack vector and re-encode it as BJData, returning hex."""
    obj = msgpack.unpackb(bytes.fromhex(msgpack_hex), raw=False, strict_map_key=False)
    return bjdata.dumpb(obj).hex()


def expand_block(block):
    """Expand a single ``serializers`` dict in place; return True if changed."""
    ubjson = block.get("ubjson")
    if not ubjson:
        return False
    # idempotent: already expanded with the bjdata entry
    if any(item.get("note") == BJDATA_NOTE for item in ubjson):
        return False
    if "msgpack" not in block or not block["msgpack"]:
        raise RuntimeError("ubjson sample without a msgpack sibling to source from")

    msgpack_hex = block["msgpack"][0]["bytes_hex"]
    new_hex = bjdata_hex_from_msgpack(msgpack_hex)

    # annotate the existing (legacy) entry, then append the bjdata entry
    ubjson[0].setdefault("note", LEGACY_NOTE)
    ubjson.append({"bytes_hex": new_hex, "note": BJDATA_NOTE})
    return True


def main():
    pattern = os.path.join(HERE, "**", "*.json")
    changed_files = 0
    expanded = 0
    for path in sorted(glob.glob(pattern, recursive=True)):
        if os.path.basename(path) == "SCHEMA.json":
            continue
        with open(path, encoding="utf-8") as fp:
            data = json.load(fp)
        file_changed = False
        for block in iter_serializer_blocks(data):
            if expand_block(block):
                expanded += 1
                file_changed = True
        if file_changed:
            with open(path, "w", encoding="utf-8") as fp:
                fp.write(json.dumps(data, indent=2, ensure_ascii=True) + "\n")
            changed_files += 1
            print("expanded:", os.path.relpath(path, HERE))
    print(f"\n{expanded} ubjson vector(s) expanded across {changed_files} file(s)")


if __name__ == "__main__":
    sys.exit(main())
