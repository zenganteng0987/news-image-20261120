#!/usr/bin/env python3
"""THE DAILY ATLAS - Friday 20 November 2026.

Publishes the entry image: copies the bundled entry.png that sits next
to this file into the output directory (MAKEFUN_OUTPUT_DIR, default
/output), creating it if needed. Before copying, it checks that the
source file exists and is really a PNG by its 8-byte signature; after
copying, it verifies the copy matches the original by size and sha256.
Deterministic, Python 3.13 standard library only, no network access.
Running it twice produces a byte-identical output.
"""
import hashlib
import os
import shutil
import sys
from pathlib import Path

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
SOURCE_NAME = "entry.png"


def sha256_of(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    here = Path(__file__).resolve().parent
    source = here / SOURCE_NAME
    if not source.is_file():
        print(f"missing entry image: {source}", file=sys.stderr)
        return 1
    if source.read_bytes()[:8] != PNG_SIGNATURE:
        print("entry image is not a PNG (bad 8-byte signature)", file=sys.stderr)
        return 1
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / SOURCE_NAME
    shutil.copyfile(source, target)
    if target.stat().st_size != source.stat().st_size:
        print("copy size mismatch", file=sys.stderr)
        return 1
    digest = sha256_of(target)
    if digest != sha256_of(source):
        print("copy sha256 mismatch", file=sys.stderr)
        return 1
    print(f"published {target} ({target.stat().st_size} bytes, sha256 {digest[:12]}… verified)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
