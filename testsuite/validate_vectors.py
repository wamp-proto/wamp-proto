#!/usr/bin/env python3
"""
Validate every WAMP test-vector file under testsuite/ against testsuite/SCHEMA.json.

This is the corpus's safety net: it keeps the canonical test vectors and the
schema that documents their format from drifting apart. Run it in CI and locally.

Usage:
    pip install jsonschema
    python testsuite/validate_vectors.py

Exits non-zero (and prints the offending file + first error) if any vector file
does not conform to the schema.
"""
import glob
import json
import os
import sys

import jsonschema

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    schema_path = os.path.join(HERE, "SCHEMA.json")
    with open(schema_path, encoding="utf-8") as fp:
        schema = json.load(fp)

    # Fail fast if the schema itself is not a valid draft-07 schema.
    jsonschema.Draft7Validator.check_schema(schema)
    validator = jsonschema.Draft7Validator(schema)

    pattern = os.path.join(HERE, "**", "*.json")
    files = sorted(
        f for f in glob.glob(pattern, recursive=True)
        if os.path.basename(f) != "SCHEMA.json"
    )

    failures = 0
    for path in files:
        rel = os.path.relpath(path, HERE)
        with open(path, encoding="utf-8") as fp:
            data = json.load(fp)
        errors = sorted(validator.iter_errors(data), key=lambda e: list(e.path))
        if errors:
            failures += 1
            err = errors[0]
            location = "/".join(str(p) for p in err.path) or "<root>"
            print(f"INVALID  {rel}\n    at {location}: {err.message}")
        else:
            print(f"ok       {rel}")

    print(f"\n{len(files)} file(s) checked, {failures} invalid")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
