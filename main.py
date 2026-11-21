#!/usr/bin/env python3
"""THE DAILY ATLAS — Friday 20 November 2026 (V2 entry program).

Publishes the bundled front page: it checks that entry.png sits next to
this file and starts with the 8-byte PNG signature, copies it to the
output directory (MAKEFUN_OUTPUT_DIR when set, otherwise /output), and
verifies the copy matches the original by size and sha256. Running it
repeatedly produces a byte-identical output. Python 3.13, standard
library only, no network access.
"""

import hashlib
import os
import shutil
import sys

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    if not os.path.isfile(source):
        print(f"missing bundled image: {source}", file=sys.stderr)
        return 1
    with open(source, "rb") as handle:
        head = handle.read(8)
    if head != PNG_SIGNATURE:
        print("bundled image is not a PNG (bad signature)", file=sys.stderr)
        return 1
    out_dir = (os.environ.get("MAKEFUN_OUTPUT_DIR") or "").strip() or "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(source, target)
    if os.path.getsize(source) != os.path.getsize(target):
        print("copy size mismatch", file=sys.stderr)
        return 1
    if sha256_of(source) != sha256_of(target):
        print("copy sha256 mismatch", file=sys.stderr)
        return 1
    print(f"published {target} ({os.path.getsize(target)} bytes, "
          f"sha256 {sha256_of(target)[:16]}...)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
