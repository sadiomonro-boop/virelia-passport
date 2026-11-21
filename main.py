#!/usr/bin/env python3
"""Virelia Passport — write the passport spread image to the output path.

The image is a pre-rendered 1024x1024 PNG shipped in this repository as
entry.png (drawn fresh in the build session by render.py, a PIL renderer
written for this entry). This program only validates it and copies it to
the output directory, so its output is byte-identical on every run.

Validation (the competition gate):
  * entry.png is a whole PNG (magic bytes 89 50 4E 47 0D 0A 1A 0A)
  * its IHDR declares exactly 1024 x 1024 pixels
  * its size is at most 1,048,576 bytes

Output path: $MAKEFUN_OUTPUT_DIR/entry.png, or /output/entry.png when
that variable is unset (the grader sandbox).
"""
import os
import struct
import sys

ASSET = "entry.png"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1_048_576
EXPECTED_W = 1024
EXPECTED_H = 1024


def fail(message):
    print("error: " + message, file=sys.stderr)
    raise SystemExit(1)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    asset_path = os.path.join(here, ASSET)
    if not os.path.isfile(asset_path):
        fail("missing asset: " + ASSET)

    with open(asset_path, "rb") as handle:
        data = handle.read()

    if len(data) > MAX_BYTES:
        fail("asset is %d bytes, over the 1,048,576 byte limit" % len(data))
    if len(data) < 33 or data[:8] != PNG_MAGIC:
        fail("asset is not a whole PNG file")
    if data[12:16] != b"IHDR":
        fail("asset has no IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (EXPECTED_W, EXPECTED_H):
        fail("asset is %dx%d, expected 1024x1024" % (width, height))

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")
    with open(out_path, "wb") as handle:
        handle.write(data)
    print("wrote %s (%d bytes, %dx%d)" % (out_path, len(data), width, height))


if __name__ == "__main__":
    main()
